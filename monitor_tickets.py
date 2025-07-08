#!/usr/bin/env python3
import requests
import sys
import re
import os
from bs4 import BeautifulSoup

def fetch_tickets():
    """Fetch ticket information from Singapore GP website"""
    url = 'https://singaporegp.sg/en/tickets/general-tickets/grandstands/'
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
    }
    
    cookies = {
        'asw': '{"lang":"en"}',
        'CookieConsent': 'true',
        'filterTicketCategory': 'grandstands',
        'filterDay': ''
    }
    
    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_ticket_info(html_content):
    """Parse ticket information from HTML content"""
    soup = BeautifulSoup(html_content, 'html.parser')
    tickets = []
    
    # Find all ticket panels
    ticket_panels = soup.find_all('div', class_=re.compile(r'ticket-panel'))
    
    for panel in ticket_panels:
        ticket_data = {}
        
        # Extract ticket name
        title_elem = panel.find('div', class_=re.compile(r'panel-title'))
        if title_elem:
            title_text = title_elem.get_text(strip=True)
            # Clean up the title
            name = re.sub(r'\s+', ' ', title_text.split('Details')[0]).strip()
            
            # Format day suffixes with clean labels
            name = re.sub(r'friday$', '[FRI]', name, flags=re.IGNORECASE)
            name = re.sub(r'saturday$', '[SAT]', name, flags=re.IGNORECASE)
            name = re.sub(r'sunday$', '[SUN]', name, flags=re.IGNORECASE)
            
            ticket_data['name'] = name
        
        # Extract price
        price_elem = panel.find('span', class_=re.compile(r'ticket-price'))
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            ticket_data['price'] = price_text
            # Extract numeric price
            price_match = re.search(r'\$([0-9,]+)', price_text)
            if price_match:
                ticket_data['price_numeric'] = int(price_match.group(1).replace(',', ''))
        
        # Extract status from button
        button_elem = panel.find('a', class_=re.compile(r'btn-buy'))
        if button_elem:
            status_text = button_elem.get_text(strip=True)
            if 'Sold Out' in status_text or 'Currently Sold Out' in status_text:
                ticket_data['status'] = 'SOLD OUT'
                ticket_data['available'] = False
            elif 'Buy Now' in status_text or status_text.lower() == 'buy':
                ticket_data['status'] = 'AVAILABLE'
                ticket_data['available'] = True
            else:
                ticket_data['status'] = status_text.upper()
                ticket_data['available'] = 'buy' in status_text.lower()
        
        # Extract category from data attributes
        category_attr = panel.get('data-category')
        if category_attr:
            ticket_data['category'] = category_attr
        
        # Extract day information from CSS classes
        class_list = panel.get('class', [])
        ticket_data['days'] = []
        
        for css_class in class_list:
            if css_class == 'd-3-days':
                ticket_data['days'].append('3-days')
            elif css_class == 'd-friday':
                ticket_data['days'].append('friday')
            elif css_class == 'd-saturday':
                ticket_data['days'].append('saturday')
            elif css_class == 'd-sunday':
                ticket_data['days'].append('sunday')
        
        # If no specific days found, assume it's for all days
        if not ticket_data['days']:
            ticket_data['days'] = ['3-days']
        
        # Only add if we found meaningful data and not wheelchair accessible
        if (ticket_data.get('name') and 
            ticket_data.get('price') and 
            ticket_data.get('category') != 'wheelchair-accessible-platforms'):
            tickets.append(ticket_data)
    
    return tickets

def check_target_tickets(tickets):
    """Check for target tickets based on monitoring criteria"""
    target_tickets = []
    
    for ticket in tickets:
        if not ticket.get('available', False):
            continue
            
        name = ticket.get('name', '').lower()
        price = ticket.get('price_numeric', 0)
        days = ticket.get('days', [])
        category = ticket.get('category', '')
        
        # Condition 1: 周日的 grandstand
        if 'sunday' in days and 'grandstand' in category:
            target_tickets.append({
                'ticket': ticket,
                'reason': 'Sunday Grandstand available',
                'priority': 'HIGH'
            })
        
        # Condition 2: 三日的 $1500 以下的票
        elif '3-days' in days and price > 0 and price <= 1500:
            target_tickets.append({
                'ticket': ticket,
                'reason': f'3-day ticket under $1500 (${price})',
                'priority': 'HIGH'
            })
        
        # Condition 3: $300以下的 grandstand
        elif 'grandstand' in category and price > 0 and price <= 300:
            target_tickets.append({
                'ticket': ticket,
                'reason': f'Grandstand under $300 (${price})',
                'priority': 'MEDIUM'
            })
    
    return target_tickets

def format_alert_message(target_tickets):
    """Format alert message for email"""
    if not target_tickets:
        return None
    
    message = "🎫 Singapore GP Ticket Alert!\n\n"
    message += "Found the following target tickets:\n\n"
    
    for i, target in enumerate(target_tickets, 1):
        ticket = target['ticket']
        reason = target['reason']
        priority = target['priority']
        
        message += f"{i}. {ticket['name']}\n"
        message += f"   Price: {ticket['price']}\n"
        message += f"   Category: {ticket['category'].title()}\n"
        message += f"   Days: {', '.join(ticket['days'])}\n"
        message += f"   Reason: {reason}\n"
        message += f"   Priority: {priority}\n"
        message += f"   Status: {ticket['status']}\n\n"
    
    message += "🔗 Buy tickets: https://singaporegp.sg/en/tickets/general-tickets/grandstands/\n"
    message += f"\nTotal found: {len(target_tickets)} target tickets"
    
    return message

def main():
    """Main monitoring function"""
    print("🔍 Monitoring Singapore GP tickets...")
    
    # Fetch tickets
    html_content = fetch_tickets()
    if not html_content:
        print("❌ Failed to fetch ticket data")
        sys.exit(1)
    
    # Parse tickets
    tickets = parse_ticket_info(html_content)
    print(f"📊 Found {len(tickets)} total tickets")
    
    # Check for target tickets
    target_tickets = check_target_tickets(tickets)
    
    if target_tickets:
        print(f"🎯 Found {len(target_tickets)} target tickets!")
        
        # Format message
        message = format_alert_message(target_tickets)
        
        # Output for GitHub Action (new format)
        github_output = os.environ.get('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"alert_needed=true\n")
                f.write(f"ticket_count={len(target_tickets)}\n")
        else:
            # Fallback for local testing
            print("alert_needed=true")
            print(f"ticket_count={len(target_tickets)}")
        
        # Save message to file for email
        with open('alert_message.txt', 'w', encoding='utf-8') as f:
            f.write(message)
        
        # Also output to console
        print("\n" + "="*50)
        print(message)
        print("="*50)
        
        # Exit with special code to indicate alert needed
        sys.exit(0)
    else:
        print("✅ No target tickets found")
        github_output = os.environ.get('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"alert_needed=false\n")
                f.write(f"ticket_count=0\n")
        else:
            # Fallback for local testing
            print("alert_needed=false")
            print("ticket_count=0")
        sys.exit(0)

if __name__ == "__main__":
    main()
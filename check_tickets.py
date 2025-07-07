#!/usr/bin/env python3
import requests
import argparse
import sys
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def fetch_tickets(category='grandstands', day=''):
    """Fetch ticket information from Singapore GP website"""
    # Construct URL based on category
    base_url = 'https://singaporegp.sg/en/tickets/general-tickets/'
    url = urljoin(base_url, category + '/')
    
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
        'filterTicketCategory': category,
        'filterDay': day
    }
    
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
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
        if ticket_data.get('name') and ticket_data.get('price') and ticket_data.get('category') != 'wheelchair-accessible-platforms':
            tickets.append(ticket_data)
    
    return tickets

def format_ticket_output(tickets):
    """Format tickets for display"""
    if not tickets:
        return "No tickets found."
    
    # Group tickets by category
    by_category = {}
    for ticket in tickets:
        cat = ticket.get('category', 'unknown')
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(ticket)
    
    output = []
    for category, cat_tickets in by_category.items():
        output.append(f"\n{Colors.BOLD}{category.title()} Tickets:{Colors.END}")
        output.append("=" * 60)
        
        for ticket in cat_tickets:
            name = ticket.get('name', 'Unknown')
            price = ticket.get('price', 'N/A')
            status = ticket.get('status', 'Unknown')
            
            # Color code based on availability
            if ticket.get('available', False):
                status_color = Colors.GREEN
            else:
                status_color = Colors.RED
            
            output.append(f"{Colors.BLUE}{name:<40}{Colors.END} {price:<10} {status_color}{status}{Colors.END}")
    
    return "\n".join(output)

def group_tickets_by_day(tickets):
    """Group tickets by day based on their CSS classes"""
    day_groups = {
        '3-days': [],
        'friday': [],
        'saturday': [],
        'sunday': []
    }
    
    for ticket in tickets:
        for day in ticket.get('days', []):
            if day in day_groups:
                day_groups[day].append(ticket)
    
    return day_groups

def main():
    parser = argparse.ArgumentParser(description='Check Singapore GP ticket availability')
    parser.add_argument('--category', default='grandstands', 
                       choices=['grandstands', 'hospitality', 'walkabouts', 'combination-packages'],
                       help='Ticket category (default: grandstands)')
    parser.add_argument('--day', default='all', 
                       choices=['all', '3-days', 'friday', 'saturday', 'sunday'],
                       help='Filter by day (default: all - checks all days)')
    parser.add_argument('--available-only', action='store_true',
                       help='Show only available tickets')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed output')
    parser.add_argument('--no-color', action='store_true',
                       help='Disable colored output')
    
    args = parser.parse_args()
    
    # Disable colors if requested
    if args.no_color:
        Colors.GREEN = Colors.RED = Colors.YELLOW = Colors.BLUE = Colors.BOLD = Colors.END = ''
    
    print(f"{Colors.BOLD}Singapore GP Ticket Checker{Colors.END}")
    
    if args.day == 'all':
        print("Fetching all tickets...\n")
        html_content = fetch_tickets('grandstands', '')
        
        if html_content:
            all_tickets = parse_ticket_info(html_content)
            available_tickets = [t for t in all_tickets if t.get('available', False)]
            day_groups = group_tickets_by_day(available_tickets)
            
            # Display results
            has_available = False
            for day_name, tickets in day_groups.items():
                if tickets:
                    has_available = True
                    print(f"\n{Colors.BOLD}=== {day_name.title()} Available Tickets ==={Colors.END}")
                    for ticket in tickets:
                        name = ticket.get('name', 'Unknown')[:50]
                        price = ticket.get('price', 'N/A')
                        category = ticket.get('category', '').title()
                        print(f"{Colors.BLUE}{name:<50}{Colors.END} {price:<10} {Colors.GREEN}AVAILABLE{Colors.END} [{category}]")
            
            if not has_available:
                print(f"\n{Colors.RED}No available tickets found for any day.{Colors.END}")
            
            # Summary
            print(f"\n{Colors.BOLD}Summary Across All Days:{Colors.END}")
            for day_name, tickets in day_groups.items():
                count = len(tickets)
                color = Colors.GREEN if count > 0 else Colors.RED
                print(f"{day_name.title()}: {color}{count} available{Colors.END}")
            
            total_available = len(available_tickets)
            print(f"Total available tickets: {Colors.GREEN}{total_available}{Colors.END}")
        else:
            print(f"{Colors.RED}Failed to fetch ticket information.{Colors.END}")
            sys.exit(1)
        
    else:
        # Single day check
        print(f"Checking {args.category} tickets for {args.day}...\n")
        
        html_content = fetch_tickets(args.category, '')
        
        if html_content:
            all_tickets = parse_ticket_info(html_content)
            
            # Filter by day
            if args.day != 'all':
                filtered_tickets = []
                target_day = '3-days' if args.day == '3-days' else args.day
                for ticket in all_tickets:
                    if target_day in ticket.get('days', []):
                        filtered_tickets.append(ticket)
                tickets = filtered_tickets
            else:
                tickets = all_tickets
            
            # Filter by availability if requested
            if args.available_only:
                tickets = [t for t in tickets if t.get('available', False)]
            
            if tickets:
                print(format_ticket_output(tickets))
                
                # Summary
                available_count = sum(1 for t in tickets if t.get('available', False))
                total_count = len(tickets)
                print(f"\n{Colors.BOLD}Summary:{Colors.END}")
                print(f"Total tickets: {total_count}")
                print(f"Available: {Colors.GREEN}{available_count}{Colors.END}")
                print(f"Sold out: {Colors.RED}{total_count - available_count}{Colors.END}")
            else:
                if args.available_only:
                    print(f"{Colors.YELLOW}No available tickets found for {args.day}.{Colors.END}")
                else:
                    print(f"{Colors.YELLOW}No ticket information found for {args.day}.{Colors.END}")
                
            if args.verbose:
                print(f"\nHTML content length: {len(html_content)} characters")
                print(f"Found {len(all_tickets)} total ticket entries")
                print(f"Filtered to {len(tickets)} tickets for {args.day}")
        else:
            print(f"{Colors.RED}Failed to fetch ticket information.{Colors.END}")
            sys.exit(1)

if __name__ == "__main__":
    main()
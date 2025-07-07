#!/usr/bin/env python3
"""
Test script for Singapore GP ticket monitor
"""
import sys
from monitor_tickets import fetch_tickets, parse_ticket_info, check_target_tickets, format_alert_message

def test_monitor():
    """Test the monitoring system"""
    print("🧪 Testing Singapore GP ticket monitor...")
    
    # Test 1: Fetch tickets
    print("\n1️⃣ Testing ticket fetching...")
    html_content = fetch_tickets()
    if html_content:
        print("✅ Successfully fetched ticket data")
        print(f"📄 HTML content length: {len(html_content)} characters")
    else:
        print("❌ Failed to fetch ticket data")
        return False
    
    # Test 2: Parse tickets
    print("\n2️⃣ Testing ticket parsing...")
    tickets = parse_ticket_info(html_content)
    print(f"📊 Parsed {len(tickets)} tickets")
    
    # Show some examples
    available_tickets = [t for t in tickets if t.get('available', False)]
    print(f"✅ Found {len(available_tickets)} available tickets")
    
    if available_tickets:
        print("\n📋 Sample available tickets:")
        for i, ticket in enumerate(available_tickets[:3]):
            print(f"   {i+1}. {ticket['name']} - {ticket['price']} ({ticket['category']})")
    
    # Test 3: Check target tickets
    print("\n3️⃣ Testing target ticket detection...")
    target_tickets = check_target_tickets(tickets)
    
    if target_tickets:
        print(f"🎯 Found {len(target_tickets)} target tickets!")
        for target in target_tickets:
            ticket = target['ticket']
            print(f"   • {ticket['name']} - {target['reason']} ({target['priority']})")
        
        # Test 4: Format alert message
        print("\n4️⃣ Testing alert message formatting...")
        message = format_alert_message(target_tickets)
        print("📧 Generated alert message:")
        print("-" * 50)
        print(message)
        print("-" * 50)
        
        return True
    else:
        print("ℹ️ No target tickets found (this is normal)")
        
        # Show what we're looking for
        print("\n🔍 We're monitoring for:")
        print("   • Sunday grandstand tickets")
        print("   • 3-day tickets ≤ $1500")
        print("   • Friday premier walkabout tickets")
        print("   • Grandstand tickets ≤ $300")
        
        return True

def main():
    """Main test function"""
    try:
        success = test_monitor()
        if success:
            print("\n✅ All tests passed!")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
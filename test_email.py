#!/usr/bin/env python3
"""
Test script to verify email functionality
"""
import sys
sys.path.insert(0, '/workspaces/skills-getting-started-with-github-copilot/src')

from app import send_confirmation_email, send_unregister_email, activities
import smtplib

# Test email configuration
print("Testing email functionality...")
print("=" * 60)

# Test activity data
test_email = "test@mergington.edu"
test_activity = "Chess Club"
test_activity_details = activities["Chess Club"]

print(f"\n1. REGISTRATION EMAIL TEST")
print(f"{'=' * 60}")
print(f"- Email: {test_email}")
print(f"- Activity: {test_activity}")
print(f"- SMTP Server: localhost:1025 (MailHog)")
print(f"- Participants: {len(test_activity_details['participants'])}/{test_activity_details['max_participants']}")

print(f"\nAttempting to send registration email...")
try:
    send_confirmation_email(test_email, test_activity, test_activity_details)
    print("✓ Registration email function executed successfully!")
except Exception as e:
    print(f"✗ Error sending registration email: {str(e)}")

print(f"\n2. UNREGISTRATION EMAIL TEST")
print(f"{'=' * 60}")
print(f"- Email: {test_email}")
print(f"- Activity: {test_activity}")
print(f"- SMTP Server: localhost:1025 (MailHog)")
print(f"- Participants: {len(test_activity_details['participants'])}/{test_activity_details['max_participants']}")

print(f"\nAttempting to send unregistration email...")
try:
    send_unregister_email(test_email, test_activity, test_activity_details)
    print("✓ Unregistration email function executed successfully!")
except Exception as e:
    print(f"✗ Error sending unregistration email: {str(e)}")
    
print("\n" + "=" * 60)
print("\nTo verify emails were sent:")
print("1. Check MailHog web interface at http://localhost:8025")
print("2. Or check application console output for email send confirmation")
print("=" * 60)

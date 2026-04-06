"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database

activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": []
    },
    "Soccer Club": {
        "description": "Train and play soccer matches",
        "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
        "max_participants": 22,
        "participants": []
    },
    "Art Club": {
        "description": "Explore various art forms and create masterpieces",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 10,
        "participants": []
    },
    "Drama Club": {
        "description": "Act in plays and improve theatrical skills",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Debate Club": {
        "description": "Engage in debates and develop argumentation skills",
        "schedule": "Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 15,
        "participants": []
    },
    "Science Club": {
        "description": "Conduct experiments and learn about science",
        "schedule": "Tuesdays, 4:00 PM - 5:00 PM",
        "max_participants": 2,
        "participants": []
    }
}


def send_confirmation_email(email: str, activity_name: str, activity_details: dict):
    """Send a confirmation email to the registered student"""
    try:
        # Email configuration (using environment variables for security)
        sender_email = os.getenv("SENDER_EMAIL", "noreply@mergington.edu")
        sender_password = os.getenv("SENDER_PASSWORD", "")
        smtp_server = os.getenv("SMTP_SERVER", "localhost")
        smtp_port = int(os.getenv("SMTP_PORT", "1025"))
        
        print(f"\n{'='*60}")
        print(f"Email Notification")
        print(f"{'='*60}")
        print(f"To: {email}")
        print(f"Activity: {activity_name}")
        print(f"SMTP Server: {smtp_server}:{smtp_port}")
        print(f"Subject: Registration Confirmation - {activity_name} at Mergington High School")
        print(f"{'='*60}\n")
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Registration Confirmation - {activity_name} at Mergington High School"
        message["From"] = sender_email
        message["To"] = email
        
        # Create plain text version
        text = f"""
Dear Student,

Thank you for registering for {activity_name} at Mergington High School!

Registration Details:
- Activity: {activity_name}
- Description: {activity_details['description']}
- Schedule: {activity_details['schedule']}
- Registered Email: {email}
- Registration Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
- Current Participants: {len(activity_details['participants'])}/{activity_details['max_participants']}

Your registration is confirmed. Please make sure to attend the activity at the scheduled time.

If you need to unregister or have any questions, please contact the school administration.

Best regards,
Mergington High School Activities Management System
        """
        
        # Create HTML version
        html = f"""
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
      <div style="background-color: #1a237e; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
        <h1 style="margin: 0;color: white;">Registration Confirmation</h1>
        <p style="margin: 5px 0 0 0;">Mergington High School Activities</p>
      </div>
      
      <p>Dear Student,</p>
      
      <p>Thank you for registering for <strong>{activity_name}</strong> at Mergington High School!</p>
      
      <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
        <h3 style="margin-top: 0; color: #1a237e;">Registration Details:</h3>
        <table style="width: 100%; border-collapse: collapse;">
          <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Activity:</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{activity_name}</td>
          </tr>
          <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Description:</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{activity_details['description']}</td>
          </tr>
          <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Schedule:</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{activity_details['schedule']}</td>
          </tr>
          <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Email:</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{email}</td>
          </tr>
          <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Registration Date:</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</td>
          </tr>
          <tr>
            <td style="padding: 8px; font-weight: bold;">Slot Status:</td>
            <td style="padding: 8px; color: #2e7d32; font-weight: bold;">{len(activity_details['participants'])}/{activity_details['max_participants']} Participants</td>
          </tr>
        </table>
      </div>
      
      <p>Your registration is confirmed. Please make sure to attend the activity at the scheduled time.</p>
      
      <p>If you need to unregister or have any questions, please contact the school administration.</p>
      
      <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-top: 20px; text-align: center; color: #666; font-size: 12px;">
        <p style="margin: 0;">Mergington High School Activities Management System</p>
        <p style="margin: 5px 0 0 0;">© 2024 Mergington High School. All rights reserved.</p>
      </div>
    </div>
  </body>
</html>
        """
        
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        
        message.attach(part1)
        message.attach(part2)
        
        # Try to send email via SMTP
        try:
            with smtplib.SMTP(smtp_server, smtp_port, timeout=5) as server:
                # Uncomment for production (requires TLS)
                # server.starttls()
                # server.login(sender_email, sender_password)
                server.send_message(message)
            print(f"✓ Confirmation email sent successfully to {email}")
            
        except (smtplib.SMTPException, ConnectionRefusedError, TimeoutError) as smtp_error:
            print(f"\n⚠ Note: SMTP Server ({smtp_server}:{smtp_port}) is not available")
            print(f"Email message prepared and ready to send:")
            print(f"\nEmail Details:")
            print(f"- To: {email}")
            print(f"- From: {sender_email}")
            print(f"- Subject: Registration Confirmation - {activity_name} at Mergington High School")
            print(f"\nMessage (Text):")
            print(text)
            print(f"\nTo enable email sending, please:")
            print(f"1. Start MailHog: mailhog")
            print(f"2. Or configure SMTP server using environment variables:")
            print(f"   - SMTP_SERVER=your-smtp-server")
            print(f"   - SMTP_PORT=587 (or 465)")
            print(f"   - SENDER_EMAIL=your-email@example.com")
            print(f"   - SENDER_PASSWORD=your-password\n")
        
    except Exception as e:
        # Log the error but don't fail the registration
        print(f"✗ Error preparing confirmation email for {email}: {str(e)}")


def send_unregister_email(email: str, activity_name: str, activity_details: dict):
    """Send an unregistration confirmation email to the student"""
    try:
        # Email configuration (using environment variables for security)
        sender_email = os.getenv("SENDER_EMAIL", "noreply@mergington.edu")
        sender_password = os.getenv("SENDER_PASSWORD", "")
        smtp_server = os.getenv("SMTP_SERVER", "localhost")
        smtp_port = int(os.getenv("SMTP_PORT", "1025"))
        
        print(f"\n{'='*60}")
        print(f"Unregistration Email Notification")
        print(f"{'='*60}")
        print(f"To: {email}")
        print(f"Activity: {activity_name}")
        print(f"SMTP Server: {smtp_server}:{smtp_port}")
        print(f"Subject: Unregistration Confirmation - {activity_name} at Mergington High School")
        print(f"{'='*60}\n")
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Unregistration Confirmation - {activity_name} at Mergington High School"
        message["From"] = sender_email
        message["To"] = email
        
        # Create plain text version
        text = f"""
Dear Student,

We confirm that you have been successfully unregistered from {activity_name} at Mergington High School.

Unregistration Details:
- Activity: {activity_name}
- Description: {activity_details['description']}
- Schedule: {activity_details['schedule']}
- Registered Email: {email}
- Unregistration Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
- Remaining Participants: {len(activity_details['participants'])}/{activity_details['max_participants']}

If you wish to re-register for this activity in the future, you can do so from our registration portal.

If you have any questions, please contact the school administration.

Best regards,
Mergington High School Activities Management System
        """
        
        # Create HTML version
        html = f"""
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
      <div style="background-color: #1a237e; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
        <h1 style="margin: 0;color: white;">Unregistration Confirmation</h1>
        <p style="margin: 5px 0 0 0;">Mergington High School Activities</p>
      </div>
      
      <p>Dear Student,</p>
      
      <p>We confirm that you have been successfully unregistered from <strong>{activity_name}</strong> at Mergington High School.</p>
      
      <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
        <h3 style="margin-top: 0; color: #1a237e;">Unregistration Details:</h3>
        <table style="width: 100%; border-collapse: collapse;">
          <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Activity:</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{activity_name}</td>
          </tr>
          <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Description:</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{activity_details['description']}</td>
          </tr>
          <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Schedule:</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{activity_details['schedule']}</td>
          </tr>
          <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Email:</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{email}</td>
          </tr>
          <tr>
            <td style="padding: 8px; border-bottom: 1px solid #ddd; font-weight: bold;">Unregistration Date:</td>
            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</td>
          </tr>
          <tr>
            <td style="padding: 8px; font-weight: bold;">Remaining Participants:</td>
            <td style="padding: 8px; color: #d32f2f; font-weight: bold;">{len(activity_details['participants'])}/{activity_details['max_participants']} Participants</td>
          </tr>
        </table>
      </div>
      
      <p>If you wish to re-register for this activity in the future, you can do so from our registration portal.</p>
      
      <p>If you have any questions, please contact the school administration.</p>
      
      <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-top: 20px; text-align: center; color: #666; font-size: 12px;">
        <p style="margin: 0;">Mergington High School Activities Management System</p>
        <p style="margin: 5px 0 0 0;">© 2024 Mergington High School. All rights reserved.</p>
      </div>
    </div>
  </body>
</html>
        """
        
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        
        message.attach(part1)
        message.attach(part2)
        
        # Try to send email via SMTP
        try:
            with smtplib.SMTP(smtp_server, smtp_port, timeout=5) as server:
                # Uncomment for production (requires TLS)
                # server.starttls()
                # server.login(sender_email, sender_password)
                server.send_message(message)
            print(f"✓ Unregistration email sent successfully to {email}")
            
        except (smtplib.SMTPException, ConnectionRefusedError, TimeoutError) as smtp_error:
            print(f"\n⚠ Note: SMTP Server ({smtp_server}:{smtp_port}) is not available")
            print(f"Email message prepared and ready to send:")
            print(f"\nEmail Details:")
            print(f"- To: {email}")
            print(f"- From: {sender_email}")
            print(f"- Subject: Unregistration Confirmation - {activity_name} at Mergington High School")
            print(f"\nMessage (Text):")
            print(text)
            print(f"\nTo enable email sending, please:")
            print(f"1. Start MailHog: mailhog")
            print(f"2. Or configure SMTP server using environment variables\n")
        
    except Exception as e:
        # Log the error but don't fail the unregistration
        print(f"✗ Error preparing unregistration email for {email}: {str(e)}")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if slots are available (availability must be > 0)
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Slot closed, Kindly wait for future openings")

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")


    # Add student
    activity["participants"].append(email)
    
    # Send confirmation email
    send_confirmation_email(email, activity_name, activity)
    
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/signup")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

    # Store activity details for email (before removing participant)
    activity_details = activity.copy()

    # Remove student
    activity["participants"].remove(email)
    
    # Send unregistration email
    send_unregister_email(email, activity_name, activity_details)
    
    return {"message": f"Unregistered {email} from {activity_name}"}

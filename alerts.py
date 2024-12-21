from twilio.rest import Client
import os
from dotenv import load_dotenv
import sendgrid
from sendgrid.helpers.mail import Mail


load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')


def send_sms_alert(to_number, message_body):
    try:
        # Initialize Twilio client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Send SMS
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        
        print(f"SMS sent successfully! Message SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")

# Example usage
send_sms_alert('+1234567890', 'Alert: A severe earthquake has been detected in Los Angeles!')

def send_email_alert(to_email, subject, message_body):
    try:
        # Initialize SendGrid client
        sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
        
        # Create the email
        message = Mail(
            from_email=SENDER_EMAIL,
            to_emails=to_email,
            subject=subject,
            plain_text_content=message_body
        )
        
        # Send email
        response = sg.send(message)
        print(f"Email sent successfully! Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage
send_email_alert('recipient@example.com', 'Disaster Alert', 'Alert: A severe flood has been detected in Houston!')


"""
Email Sender for Feedback Responses
Uses Gmail API to send automated responses to feedback submitters
"""

import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Service account or OAuth2 credentials path
CREDENTIALS_PATH = os.environ.get('GMAIL_CREDENTIALS_PATH', '/tmp/gmail_credentials.json')
TOKEN_PATH = os.environ.get('GMAIL_TOKEN_PATH', '/tmp/gmail_token.json')


def get_gmail_service():
    """
    Get authenticated Gmail service
    For Cloud Functions, use service account or OAuth2 token
    """
    creds = None
    
    # Try to load existing token
    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except Exception as e:
            print(f"Error loading token: {e}")
    
    # If no valid credentials, return None (email sending disabled)
    if not creds or not creds.valid:
        print("⚠️ Gmail credentials not available - email sending disabled")
        return None
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Error building Gmail service: {e}")
        return None


def send_email(to: str, subject: str, message: str, from_email: str = "noreply@glmp.bio"):
    """
    Send an email using Gmail API
    
    Args:
        to: Recipient email address
        subject: Email subject
        message: Email body (plain text)
        from_email: Sender email (must be authorized in Gmail)
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    service = get_gmail_service()
    if not service:
        print(f"⚠️ Gmail service not available - email not sent to {to}")
        return False
    
    try:
        # Create message
        msg = MIMEText(message)
        msg['To'] = to
        msg['From'] = from_email
        msg['Subject'] = subject
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
        
        # Send message
        send_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        print(f"✓ Email sent to {to} (message ID: {send_message['id']})")
        return True
        
    except HttpError as error:
        print(f"Error sending email: {error}")
        return False
    except Exception as e:
        print(f"Unexpected error sending email: {e}")
        return False


def process_email_queue(bucket_name: str):
    """
    Process queued emails from GCS
    This can be called by a Cloud Scheduler job
    """
    from google.cloud import storage
    
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob("glmp-feedback/email-queue.jsonl")
        
        if not blob.exists():
            print("No email queue found")
            return
        
        content = blob.download_as_text()
        if not content.strip():
            print("Email queue is empty")
            return
        
        # Process each queued email
        sent_emails = []
        failed_emails = []
        
        for line in content.strip().split('\n'):
            if not line.strip():
                continue
            
            try:
                email_item = json.loads(line)
                success = send_email(
                    to=email_item['to'],
                    subject=email_item['subject'],
                    message=email_item['message']
                )
                
                if success:
                    sent_emails.append(email_item)
                else:
                    failed_emails.append(email_item)
                    
            except Exception as e:
                print(f"Error processing email item: {e}")
                failed_emails.append({"line": line, "error": str(e)})
        
        # Update queue - remove sent emails, keep failed ones
        if sent_emails:
            remaining_content = '\n'.join([
                json.dumps(item, separators=(",", ":"))
                for item in failed_emails
                if isinstance(item, dict) and 'to' in item
            ])
            
            if remaining_content.strip():
                blob.upload_from_string(remaining_content + '\n', content_type="application/json")
            else:
                blob.upload_from_string("", content_type="application/json")
            
            print(f"✓ Processed {len(sent_emails)} emails, {len(failed_emails)} failed")
        else:
            print(f"⚠️ No emails sent, {len(failed_emails)} failed")
            
    except Exception as e:
        print(f"Error processing email queue: {e}")




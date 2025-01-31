import os
import base64
import yaml
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',  # Read-only access to emails
    'https://www.googleapis.com/auth/gmail.modify',     # Modify emails (e.g., mark as read)
    'https://www.googleapis.com/auth/gmail.send'        # Send emails
]
class EmailFetcher:
    def __init__(self):
        self.creds = None
        self.user = os.getenv('EMAIL_USER')
        self.token_path = 'token.json'
        self.credentials_path = 'credentials.json'

        # Load whitelist from YAML file
        with open('whitelist.yaml', 'r') as file:
            data = yaml.safe_load(file)
            self.whitelist = set(data.get('whitelist', []))

        # Authenticate with Gmail API
        self.authenticate()

    def authenticate(self):
        """Authenticate and store the credentials."""
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                # Use a fixed port to avoid mismatch issues
                self.creds = flow.run_local_server(port=8080)

            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(self.creds.to_json())
    def fetch_new_emails(self):
        """Fetch new unread emails using the Gmail API."""
        try:
            service = build('gmail', 'v1', credentials=self.creds)
            results = service.users().messages().list(userId='me', q='category:primary is:unread', maxResults=5).execute()
            messages = results.get('messages', [])

            new_emails = []
            if not messages:
                print("No new emails found.")
            else:
                for message in messages:
                    msg = service.users().messages().get(userId='me', id=message['id']).execute()
                    email_data = self.parse_email(msg)

                    #IF SENDER IS IN WHITELIST Mark the email as read
                    if email_data['sender_addr'] in self.whitelist:
                        new_emails.append(email_data)
                        service.users().messages().modify(
                            userId='me',
                            id=message['id'],
                            body={'removeLabelIds': ['UNREAD']}
                        ).execute()
                    # new_emails.append(email_data)
                    # service.users().messages().modify(
                    #     userId='me',
                    #     id=message['id'],
                    #     body={'removeLabelIds': ['UNREAD']}
                    # ).execute()
            print(f"Found {len(new_emails)} new emails.")
            return new_emails

        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

    def parse_email(self, msg):
        """Parse email content."""
        headers = msg['payload']['headers']
        sender_name = ''
        sender_addr = ''

        for header in headers:
            if header['name'] == 'From':
                sender_name, sender_addr = self.parse_sender(header['value'])
            if header['name'] == 'Subject':
                subject = header['value']

        return {
            # "email_message": msg,
            "sender_name": sender_name,
            "sender_addr": sender_addr,
            "subject": subject,
            "body": msg['snippet']
        }

    @staticmethod
    def parse_sender(sender_str):
        """Parse sender name and address."""
        name, addr = sender_str.split('<')
        name = name.strip('" ')
        addr = addr.strip('>')
        return name, addr

    def send_mail(self, recipient, subject, body):
        """Send an email using the Gmail API."""
        try:
            service = build('gmail', 'v1', credentials=self.creds)

            # Create the email message
            message = MIMEText(body)
            message['to'] = recipient
            message['from'] = self.user
            message['subject'] = subject

            # Encode the message in base64
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            # Send the email
            send_message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
            print(f"Message Id: {send_message['id']}")

        except HttpError as error:
            print(f"An error occurred: {error}")

if __name__ == "__main__":
    fetcher = EmailFetcher()
    new_emails = fetcher.fetch_new_emails()

    for email in new_emails:
        print(f"Sender: {email['sender_name']} <{email['sender_addr']}>")
        print(f"Subject: {email['subject']}")
        print(f"Body: {email['body']}")
        print("=" * 50)

    # Example of sending an email
    fetcher.send_mail(recipient="mirsalmanfarsi@gmail.com", subject="Test Subject", body="This is a test email.")
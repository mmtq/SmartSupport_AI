import os
import pickle
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the required scopes for Gmail API
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def authenticate():
    creds = None
    # Check if token.pickle exists for saved authentication
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If credentials are not valid or missing, authenticate again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=8080)

        # Save the credentials for future use
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds

# Initialize Gmail API service
def get_gmail_service():
    creds = authenticate()
    service = build("gmail", "v1", credentials=creds)
    return service

if __name__ == "__main__":
    service = get_gmail_service()
    print("✅ Authentication Successful!")

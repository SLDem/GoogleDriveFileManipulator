import os.path
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/docs",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.metadata.readonly"
]


def request_creds():
    """
    Get user credentials with google app credentials.
    """
    creds = None
    if os.path.exists("creds.json"):
        flow = InstalledAppFlow.from_client_secrets_file("creds.json", SCOPES)
        creds = flow.run_local_server(por=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        return Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        print('Credentials not found.')
        sys.exit(1)


def get_creds():
    """
    Get existing user creds or prompt new auth flow.
    """
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return creds
    return request_creds()

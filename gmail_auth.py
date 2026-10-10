from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

scopes = ["https://www.googleapis.com/auth/gmail.readonly"]

base_dir = Path(__file__).resolve().parent
credentials_file = base_dir / "credentials.json"
token_file = base_dir / "token.json"

def get_credentials():
    creds = None
    if not credentials_file.exists():
        raise FileNotFoundError("credentials.json not found in the project folder. Please create it and try again.  ")
    credentials=None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), scopes)

    if credentials and credentials.valid:
        return credentials
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(str(credentials_file), scopes)
        credentials = flow.run_local_server(port=0)

    token_file.write_text(credentials.to_json(),encoding="utf-8")
    return credentials
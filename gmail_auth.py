from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

scopes = ["https://www.googleapis.com/auth/gmail.readonly"]

base_dir = Path(__file__).resolve().parent
credentials_file = base_dir / "credentials.json"
token_file = base_dir / "token.json"

def get_credentials():
    if not credentials_file.exists():
        raise FileNotFoundError("credentials.json not found in the project folder.")

    creds = None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), scopes)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(str(credentials_file), scopes)
        creds = flow.run_local_server(port=0)

    token_file.write_text(creds.to_json(), encoding="utf-8")
    return creds
from functools import lru_cache

from googleapiclient.discovery import build
from gmail_auth import get_credentials


@lru_cache(maxsize=1)
def get_gmail_service():
    credentials = get_credentials()
    return build("gmail", "v1", credentials=credentials)
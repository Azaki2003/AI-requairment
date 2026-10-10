from gmail_serves import get_gmail_service

def search_emails(query,max_results=5):
    service = get_gmail_service()
    response = service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
    return response.get("messages", [])

def get_massage(message_id):
    service = get_gmail_service()
    message = service.users().messages().get(userId="me", id=message_id,format="full").execute()
    return message

def get_header(headers, name):
    for header in headers:
        if header.get("name","") .lower()== name.lower():
            return header.get("value")
    return ""
from gmail_serves import get_gmail_service


def search_emails(query, max_results=5):
    service = get_gmail_service()
    response = (
        service.users()
        .messages()
        .list(userId="me", q=query, maxResults=max_results)
        .execute()
    )
    return response.get("messages", [])


def get_message(message_id):
    service = get_gmail_service()
    return (
        service.users()
        .messages()
        .get(userId="me", id=message_id, format="full")
        .execute()
    )


def get_header(headers, name):
    for header in headers:
        if header.get("name", "").lower() == name.lower():
            return header.get("value", "")
    return ""
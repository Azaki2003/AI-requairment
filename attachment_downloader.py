import base64
from pathlib import Path

from gmail_serves import get_gmail_service

supported_extensions = {".pdf", ".docx"}


def walk_parts(payload):
    yield payload
    for part in payload.get("parts", []):
        yield from walk_parts(part)


def is_supported_cv(filename):
    return Path(filename).suffix.lower() in supported_extensions


def get_cv_attachments(message):
    attachments = []
    payload = message.get("payload", {})

    for part in walk_parts(payload):
        filename = part.get("filename")
        attachment_id = part.get("body", {}).get("attachmentId")

        if not filename or not attachment_id:
            continue
        if not is_supported_cv(filename):
            continue

        attachments.append({
            "filename": filename,
            "attachment_id": attachment_id,
        })

    return attachments


def download_attachment(message_id, attachment_id):
    service = get_gmail_service()
    response = (
        service.users()
        .messages()
        .attachments()
        .get(userId="me", messageId=message_id, id=attachment_id)
        .execute()
    )

    encoded_data = response.get("data")
    if not encoded_data:
        raise ValueError("Attachment data not found in the response.")

    encoded_data += "=" * (-len(encoded_data) % 4)
    return base64.urlsafe_b64decode(encoded_data)


def save_attachment_to_file(message_id, attachment, output_dir="temp_cvs"):
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    filename = f"{message_id}_{Path(attachment['filename']).name}"
    saved_file_path = output_dir_path / filename

    if saved_file_path.exists():
        print(f"File '{filename}' already exists. Skipping download.")
        return saved_file_path

    file_bytes = download_attachment(message_id, attachment["attachment_id"])
    saved_file_path.write_bytes(file_bytes)
    print(f"Downloaded '{filename}' to '{saved_file_path}'")
    return saved_file_path
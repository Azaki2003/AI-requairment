import base64
from pathlib import Path

from gmail_serves import get_gmail_service

supported_MIME_types = {
"application/pdf" : ".pdf",
"application/vnd.openxmlformats-officedocument.wordprocessingml.document" : ".docx"
}

supported_extensions = {".pdf", ".docx"}

def walk_parts(payload):
    yield payload
    for part in payload.get("parts", []):
        yield from walk_parts(part)

def is_supported_cv(filename, mime_type):
    extension = Path(filename).suffix.lower()
    return extension in supported_extensions and mime_type in supported_MIME_types

def get_cv_attachments(message):
    attachments = []
    payload = message.get("payload", {})
    attachments=[]

    for part in walk_parts(payload):
        filename = part.get("filename")
        mime_type = part.get("mimeType")
        body = part.get("body", {})
        attachment_id = body.get("attachmentId")

        if not filename or not attachment_id:
            continue

        if not is_supported_cv(filename, mime_type):
            continue

        attachments.append({
            "filename": filename,
            "mime_type": mime_type,
            "attachment_id": attachment_id
        })
        return attachments


    def download_attachment(message_id, attachment_id):
        service = get_gmail_service()
        response = (
            service.users()
            .messages()
            .attachments()
            .get(userId="me",
                    messageId=message_id,
                    id=attachment_id).
                    execute()
        )
        attachment_data = response.get("data")

        if not attachment_data:
            raise ValueError("Attachment data not found in the response.")


        encoded_data += "="*(-len(encoded_data) % 4)

        return base64.urlsafe_b64decode(encoded_data)

    def save_attachment_to_file(message_id, attachment_id, output_dir="temp_cvs"):
        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)

        filename= path(attachment_id["filename"]).name
        saved_file_path = output_dir_path / filename

        if saved_file_path.exists():
            print(f"File '{filename}' already exists. Skipping download.")
            return saved_file_path  
        file_bytes = download_attachment(message_id,attachment ["attachment_id"])

        saved_file_path.write_bytes(file_bytes)
        print(f"downloaded and saved attachment '{filename}' to '{saved_file_path}'")
        return saved_file_path

import imapclient
import email
from email.header import decode_header

EMAIL = "shuvra458@gmail.com"
PASSWORD = "Shuvra@123" 

def fetch_emails():
    try:
        mail = imapclient.IMAPClient("imap.gmail.com", ssl=True)
        mail.login(EMAIL, PASSWORD)
        mail.select_folder("INBOX")

        messages = mail.search(["UNSEEN"])
        if not messages:
            print(" No unread emails found.")
            return

        print(f"📬 Found {len(messages)} unread emails. Fetching details...")

        for msg_id in messages[:5]: 
            raw_message = mail.fetch(msg_id, ["RFC822"])[msg_id][b"RFC822"]
            msg = email.message_from_bytes(raw_message)

            # Decode subject
            subject, encoding = decode_header(msg["Subject"])[0]
            subject = subject.decode(encoding) if encoding else subject
            print(f"📩 Subject: {subject}")

            # Extract email body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            print(f" Email Body (First 100 chars): {body[:100]}...")

    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    fetch_emails()

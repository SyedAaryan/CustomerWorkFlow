import imaplib
import email
import time
from src.security.security import mail_id, mail_pass

HOST = "imap.gmail.com"
USERNAME = mail_id
PASSWORD = mail_pass


def get_plain_text(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode(
                    part.get_content_charset() or "utf-8", errors="replace"
                )
    else:
        if msg.get_content_type() == "text/plain":
            return msg.get_payload(decode=True).decode(
                msg.get_content_charset() or "utf-8", errors="replace"
            )
    return ""

def start_email_agent(rag_workflow):
    """
    Continuously checks for new unread emails,
    passes their content to the RAG workflow,
    and prints the AI's response.
    """
    print("\n📧 Email Agent Started. Checking for new emails...\n(Press CTRL+C to stop)\n")
    try:
        while True:
            mail = imaplib.IMAP4_SSL(HOST)
            mail.login(USERNAME, PASSWORD)
            mail.select("INBOX")

            status, data = mail.search(None, "UNSEEN")
            ids = data[0].split()
            if ids:
                for num in ids:
                    status, msg_data = mail.fetch(num, "(RFC822)")
                    if status != "OK":
                        continue
                    raw = msg_data[0][1]
                    msg = email.message_from_bytes(raw)
                    body = get_plain_text(msg)

                    print("="*50)
                    print("📩 New Email")
                    print("From:", msg.get("From"))
                    print("Subject:", msg.get("Subject"))
                    print("Body:\n", body)

                    # 👇 Send email content to RAG workflow
                    rag_response = rag_workflow.execute(body)
                    print("\n🤖 RAG Response:")
                    print(rag_response)
                    print("="*50)

                    # mark as read
                    mail.store(num, '+FLAGS', '\\Seen')
            else:
                print("⏳ No new emails...")

            mail.logout()
            time.sleep(30)

    except KeyboardInterrupt:
        print("\n🛑 Email Agent stopped by user.")
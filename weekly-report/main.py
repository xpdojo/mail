import logging
import os
import smtplib
from datetime import date
from email.headerregistry import Address
from email.message import EmailMessage
from email.mime.text import MIMEText

from markdown import markdown
from pwinput import pwinput

MARKDOWN_FILENAME = 'report.md'

"""
export MAIL_HOST=mail.example.com
export MAIL_DOMAIN=example.com
"""
MAIL_HOST = os.environ.get("MAIL_HOST", "mail.example.com")
MAIL_DOMAIN = os.environ.get("MAIL_DOMAIN", "example.com")
FROM_USERNAME = "cs.im"
DISPLAY_NAME = "Changsu Im"

# TO_USERNAME = "all"
TO_USERNAME = "cs.im"

today = date.today().strftime("%Y-%m-%d")
SUBJECT = f"[주간업무보고] {today} 개발팀 임창수"


def main():
    email_message = EmailMessage()
    email_message["Subject"] = SUBJECT
    email_message["From"] = Address(
        display_name=DISPLAY_NAME, username=FROM_USERNAME, domain=MAIL_DOMAIN
    )
    email_message["Cc"] = (
        Address(username=FROM_USERNAME, domain=MAIL_DOMAIN),
    )
    email_message["To"] = (
        Address(username=TO_USERNAME, domain=MAIL_DOMAIN),
    )

    email_message.preamble = """\
    <You will not see this in a MIME-aware mail reader.>
    """

    with open(MARKDOWN_FILENAME, 'r') as f:
        text = f.read()
        html = markdown(text)

    email_message.set_content(MIMEText(html, "html"))

    # Send the message via our own SMTP server.
    # with smtplib.SMTP(MAIL_HOST, 25) as server:
    
    # Send the message via Gmail's SMTP server.
    # https://support.google.com/mail/answer/7126229?hl=en#zippy=%2Cstep-change-smtp-other-settings-in-your-email-client
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        try:
            server.ehlo()
            server.starttls()
            # https://myaccount.google.com/lesssecureapps
            # Allow less secure apps: ON

            password = pwinput(prompt="Gmail password: ", mask="*")
            server.login(f"{FROM_USERNAME}@{MAIL_DOMAIN}", password)
            server.send_message(msg=email_message)
        except Exception as e:
            logging.error(e)
        finally:
            if server is not None:
                server.quit()

    logging.info("Done")


if __name__ == "__main__":
    main()

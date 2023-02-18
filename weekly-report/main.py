import logging
import smtplib
from datetime import date
from email.headerregistry import Address
from email.message import EmailMessage
from email.mime.text import MIMEText

from markdown import markdown
from pwinput import pwinput

today = date.today().strftime("%Y-%m-%d")
SUBJECT = f"[주간업무보고] {today} 개발팀 임창수"

def main(
        mail_domain: str,
        from_username: str,
        display_name: str,
        to_username: str,
        markdown_filepath: str,
):
    email_message = EmailMessage()
    email_message["Subject"] = SUBJECT
    email_message["From"] = Address(
        display_name=display_name, username=from_username, domain=mail_domain
    )
    email_message["Cc"] = (
        Address(username=from_username, domain=mail_domain),
    )
    email_message["To"] = (
        Address(username=to_username, domain=mail_domain),
    )

    email_message.preamble = """\
    <You will not see this in a MIME-aware mail reader.>
    """

    with open(markdown_filepath, 'r') as f:
        text = f.read()
        html = markdown(text)

    email_message.set_content(MIMEText(html, "html"))

    # Send the message via our own SMTP server.
    # with smtplib.SMTP("mail.markruler.com", 25) as server:

    # Send the message via Gmail's SMTP server.
    # https://support.google.com/mail/answer/7126229?hl=en#zippy=%2Cstep-change-smtp-other-settings-in-your-email-client
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        try:
            server.ehlo()
            server.starttls()
            # https://myaccount.google.com/lesssecureapps
            # Allow less secure apps: ON

            password = pwinput(prompt="Gmail password: ", mask="*")
            server.login(f"{from_username}@{mail_domain}", password)
            server.send_message(msg=email_message)
        except Exception as e:
            logging.error(e)
        finally:
            if server is not None:
                server.quit()

    logging.info("Done")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="""
Send weekly report to Gmail

Usages:
    python main.py -d example.com
    python main.py -d example.com -t all
    python main.py -d example.com -f cs.im -n "Changsu Im" -t cs.im -md report.md
""", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-d', '--mail-domain', metavar='<mail_domain>', required=True,
                        type=str,
                        help='Mail Domain Name')
    parser.add_argument('-f', '--from-username', metavar='<from_username>', required=False,
                        default='cs.im', type=str,
                        help='Mail Sender')
    parser.add_argument('-n', '--display-name', metavar='<from_display_name>', required=False,
                        default='Changsu Im', type=str,
                        help='Mail Sender Display Name')
    parser.add_argument('-t', '--to-username', metavar='<to_username>', required=False,
                        default='cs.im', type=str,
                        help='Mail Receiver')
    parser.add_argument('-md', '--markdown-filepath', metavar='<markdown_filepath>', required=False,
                        default='report.md', type=str,
                        help='Markdown file path')

    args = parser.parse_args()

    main(
        mail_domain=args.mail_domain,
        from_username=args.from_username,
        display_name=args.display_name,
        to_username=args.to_username,
        markdown_filepath=args.markdown_filepath,
    )

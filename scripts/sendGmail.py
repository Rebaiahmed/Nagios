#!/usr/bin/env python3

"""
Quickly send email from the command line with gmail.
"""

##########################################################################
## Imports
##########################################################################

import os
import smtplib
import argparse

from email import encoders
from email.utils import formatdate
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from datetime import datetime, timezone


##########################################################################
## Message Environment
##########################################################################

EMAIL_USERNAME = os.environ.get("EMAIL_USERNAME")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")


##########################################################################
## Message Constants
##########################################################################

HUMAN_DATETIME  = "%A, %B %d %Y at %H:%M:%S %z"
DEFAULT_SUBJECT = "Server Notification"
DEFAULT_MESSAGE = "A notification was triggered on {}"


##########################################################################
## Email Notifications
##########################################################################

def notify(recipient, subject=None, message=None, **kwargs):
    """
    Notifies the recipient at the given email address by sending an email
    with the subject and message in it. Meant to be used sparingly.
    """

    # Get the default subject and message
    subject = subject or DEFAULT_SUBJECT
    message = message or DEFAULT_MESSAGE.format(
        datetime.now(timezone.utc).astimezone().strftime(HUMAN_DATETIME)
    )

    # Get the arguments from the settings
    sender   = kwargs.get('sender', EMAIL_USERNAME)
    username = kwargs.get('username', EMAIL_USERNAME)
    password = kwargs.get('password', EMAIL_PASSWORD)
    host     = kwargs.get('host', EMAIL_HOST)
    port     = kwargs.get('port', EMAIL_PORT)
    mimetype = kwargs.get('mimetype', 'plain')
    fail_silent = kwargs.get('fail_silent', False)

    # Create the email message
    msg = MIMEMultipart()
    msg['From']= sender
    msg['To'] = recipient
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    # Attach the mime text to the message
    msg.attach(MIMEText(message, mimetype))

    # Attach any files to the email
    for fpath in kwargs.get('files', []):
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(fpath, 'rb').read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition', 'attachment; filename={}'.format(
                os.path.basename(fpath)
            )
        )
        msg.attach(part)

    # Attempt to send the message
    try:

        # Do the smtp thing
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(username, password)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()

        # Return message success
        return True

    except Exception as e:
        if not fail_silent:
            raise e

        # Return message failure
        return False


##########################################################################
## Main Method
##########################################################################

if __name__ == '__main__':

    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="Quickly send email from the command line with gmail."
    )

    # Add the command line arguments
    parser.add_argument(
        '-r', '--recipient', required=True, metavar='EMAIL',
        help='email address to send the notification to',
    )
    parser.add_argument(
        '-s', '--subject', metavar='TEXT', default=None,
        help='subject of the notification',
    )
    parser.add_argument(
        '-m', '--message', metavar='TEXT', default=None,
        help='message of the notification',
    )
    parser.add_argument(
        '-S', '--sender', metavar='EMAIL', default=EMAIL_USERNAME,
        help='email of the sender',
    )
    parser.add_argument(
        '-U', '--username', default=EMAIL_USERNAME, metavar='USER',
        help='smtp authentication username'
    )
    parser.add_argument(
        '-P', '--password', default=EMAIL_PASSWORD, metavar='SECRET',
        help='smtp authentication password'
    )
    parser.add_argument(
        '-H', '--host', default=EMAIL_HOST, help='smtp service host'
    )
    parser.add_argument(
        '-p', '--port', default=EMAIL_PORT, help='smtp service port'
    )
    parser.add_argument(
        '-M', '--mimetype', default='plain', metavar='TYPE',
        help='mimetype of the message'
    )
    parser.add_argument(
        '-f', '--fail_silent', action='store_true', default=False,
        help='no errors are raised if a problem occurs sending notification'
    )
    parser.add_argument(
        'files', nargs="*", help='a list of files to attach to the notification'
    )

    # Parse the arguments on the command line
    args = parser.parse_args()

    # Send the notification
    notify(
        args.recipient, args.subject, args.message, sender=args.sender,
        username=args.username, password=args.password, host=args.host,
        port=args.port, mimetype=args.mimetype, fail_silent=args.fail_silent,
        files=args.files,
)

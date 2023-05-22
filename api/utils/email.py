from threading import Thread
from email.utils import parseaddr

from flask_mail import Message
from dns.resolver import resolve

from api import app, mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template=None, plaintext=None):
    if plaintext is None:
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
    else:
        msg = Message(
            subject,
            recipients=[to],
            body=plaintext,
            sender=app.config['MAIL_DEFAULT_SENDER']
        )

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def valid_email(email):
    parsed_email = parseaddr(email)[1]
    if '@' not in parsed_email[1:]:
        return False

    # Check for the domain's MX records
    try:
        domain = parsed_email.rsplit('@', 1)[-1]
        _ = resolve(domain, 'MX')
        return True
    except:
        return False

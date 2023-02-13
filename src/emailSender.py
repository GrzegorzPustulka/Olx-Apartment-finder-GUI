from email.message import EmailMessage
import ssl
import smtplib


def email_sender(body, sender, email_password, receiver):
    subject = 'New offer'
    body = body[4:-1]
    body = body.replace(', ', '\n')
    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, email_password)
        smtp.sendmail(sender, receiver, em.as_string())

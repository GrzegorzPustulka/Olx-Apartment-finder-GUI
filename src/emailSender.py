import smtplib
import getpass


def email_sender(message, email, password):
    smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_object.ehlo()
    smtp_object.starttls()
    smtp_object.login(email, password)
    from_address = email
    to_address = email
    subject = "New offer"
    msg = "Subject: "+subject+'\n'+message
    smtp_object.sendmail(from_address, to_address, msg)
    smtp_object.quit()

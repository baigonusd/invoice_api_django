from __future__ import absolute_import, unicode_literals
from email.message import EmailMessage
import os
import smtplib
from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings


@shared_task()
def email(mail):
    msg = EmailMessage()
    msg['Subject'] = 'Report of invoices'
    msg['From'] = os.getenv("EMAIL_HOST_USER")
    msg['To'] = mail
    msg.set_content('Invoices information report')
    files = ['report.xlsx']
    for file in files:
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = f.name

        msg.add_attachment(file_data, maintype='application',
                           subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("EMAIL_HOST_USER"),
                   os.getenv("EMAIL_HOST_PASSWORD"))
        print('Message sended')
        smtp.send_message(msg)
    return {"Message": "Email sended"}


@shared_task()
def send_verification_email(data):
    send_mail(subject=data['email_subject'], message=data['email_body'],
              from_email=settings.EMAIL_HOST_USER, recipient_list=[data['to_email']])
    return {"Message": "Verification email sended"}

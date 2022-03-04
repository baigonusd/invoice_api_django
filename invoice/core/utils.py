from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(data):
        msg = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        msg.send()

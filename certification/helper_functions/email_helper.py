from decouple import config
from email.message import EmailMessage
import smtplib


def send_mail(context):
    msg = EmailMessage()
    msg['From'] = config('EMAIL_ADDRESS')
    msg['To'] = context['email']
    msg['Subject'] = 'Certificate link'

    email_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <body>
            <H3>Dear {context['student_name']},</H3><br/>
            <p>Your certificate has been generated successfully with certificate id {context['certificate_id']}. Please click on the link below to download it.</p>
            <a href={context['url']}>Certificate</a><br/>
            <p>{context['url']}</p><br/>
            <p>Thank you <br/>The Issuing Authority</p>
        </body>
        </html>
    """
    email_plain = f"""
    Dear {context['student_name']},\n
    Your certificate has been generated successfully with certificate id {context['certificate_id']}. Please click on the link below to download it.\n
    {context['url']}<br>
    Thank you,\n
    The Issuing Authority.
    """

    msg.set_content(email_plain)
    msg.add_alternative(email_html, subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(config('EMAIL_ADDRESS'), config('EMAIL_PASSWORD'))
        smtp.send_message(msg)

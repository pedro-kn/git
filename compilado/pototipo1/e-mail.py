import smtplib

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'h4ndsplinner@gmail.com'
smtp_password = 'punheta1'

from_email = 'h4ndsplinner@gmail.com'
to_email = 'pedrokne97@gmail.com'
subject = 'Hello, world!'
body = 'This is a test email.'

message = f'Subject: {subject}\n\n{body}'

with smtplib.SMTP(smtp_server, smtp_port) as smtp:
    smtp.starttls()
    smtp.login(smtp_username, smtp_password)
    smtp.sendmail(from_email, to_email, message)
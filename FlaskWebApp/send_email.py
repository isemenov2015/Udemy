from email.mime.text import MIMEText
import smtplib

def send_email(email, height, avg_height, users_count):
    from_email = "semenoviofb@gmail.com"
    from_password = "kepbnfybz"
    to_email = email

    subject = "Height data"
    message = "Hey!<br> Your height registered as <strong>%s</strong>.<br>Average height from database is <strong>%s</strong>. Total users No is <strong>%s</strong>" % (height, avg_height, users_count)

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)

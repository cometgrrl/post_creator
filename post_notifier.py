#for sending email notifications
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


if published_count > 0:
    # Send an email notification
    # Email configuration
    sender_email = "cometgrrl@gmail.com"
    receiver_email = "nancyareid@gmail.com"
    password = "your_email_password"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "New Puppy Dog Kisses Post Published"

    # Add body to email
    body = "New posts at https://puppydogkisses.com/"
    message.attach(MIMEText(body, "plain"))

    # Connect to SMTP server (Gmail example)
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()  # Secure the connection
    server.login(sender_email, password)

    # Send email
    server.sendmail(sender_email, receiver_email, message.as_string())

    # Quit SMTP server
    server.quit()



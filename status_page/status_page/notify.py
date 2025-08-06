import smtplib
from email.mime.text import MIMEText

#some sources of where I got information to do this:
# https://realpython.com/python-send-email/
# https://stackoverflow.com/questions/64505/sending-mail-from-python-using-smtp
# https://mailtrap.io/blog/python-send-email/

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
USERNAME = 'chaoscompsnotify@gmail.com'       # This is the new email I created (where the notification will come from)
PASSWORD = 'unnn otwo ozpt mgyw'              # I had to create a password code for the gmail
FROM_EMAIL = 'chaoscompsnotify@gmail.com'
TO_EMAIL = 'bregouc@carleton.edu'  # where we want to send the alert to, we could put all of our email in here, but I just started with mine

def send_alert_email(subject, body):


    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL

    try:
        # we have to connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls() 
        server.login(USERNAME, PASSWORD)
        
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        server.quit()
        
    except Exception as e:
        print("Failed to send alert email:", e)
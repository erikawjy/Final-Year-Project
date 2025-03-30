import os
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def send_email_alert(sender_email, sender_password, recipient_email, intruder_type, position, timestamp):

    subject = "🚨 Intruder Alert! 🚨"
    body = f"""
    📢 Motion has been detected!
    📍 Intruder Position: {position}
    🔍 Intruder Type: {intruder_type}
    ⏰ Time: {timestamp}

    Please check the dashboard for video clip.
    """
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("✅ Email alert sent successfully!")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")

    return

if __name__ == '__main__':
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')

    _ = send_email_alert(
        sender_email=sender_email, 
        sender_password=sender_password, 
        recipient_email='xxx@gmail.com', 
        intruder_type='big object', 
        position='right', 
        timestamp='today'
    )

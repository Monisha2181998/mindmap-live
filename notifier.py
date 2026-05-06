import smtplib
import os
from email.mime.text import MIMEText

def send_summary_email(summary_text, receiver_email):
    sender_email = "monisha21898@gmail.com" 
    
    # FIX: Remove os.getenv and put your 16-character code directly here
    app_password = "duwsccdleeyenkce" 

    if not app_password:
        return "❌ Error: App Password string is empty."

    msg = MIMEText(summary_text)
    msg['Subject'] = '🧠 MindMap Research Summary'
    msg['From'] = f"Research Bot <{sender_email}>"
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            # We use strip() to remove any accidental spaces
            server.login(sender_email, app_password.strip())
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return f"✅ Briefing sent to {receiver_email}"
    except Exception as e:
        return f"❌ Mail Error: {str(e)}"
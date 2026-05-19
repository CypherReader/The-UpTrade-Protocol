import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

def send_email(subject, body):
    if not config.SMTP_USERNAME or not config.SMTP_PASSWORD:
        print("WARNING: SMTP credentials not set. Skipping email notification.")
        print(f"--- EMAIL CONTENT ---\nSubject: {subject}\n\n{body}\n---------------------")
        return False

    msg = MIMEMultipart()
    msg['From'] = config.SMTP_USERNAME
    msg['To'] = config.TARGET_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
        server.starttls()
        server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Successfully sent email to {config.TARGET_EMAIL}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def notify_trade_evaluation(prospect, evaluation_reason, worth_trading):
    subject = f"Agent Trade Eval: {prospect.title}"
    body = f"""
    Platform: {prospect.platform}
    URL: {prospect.url}
    Price: {prospect.price}

    Worth Trading? {'YES' if worth_trading else 'NO'}

    Reasoning:
    {evaluation_reason}
    """
    send_email(subject, body)

def notify_message_sent(prospect, message, is_dry_run):
    status = "[DRY RUN] " if is_dry_run else ""
    subject = f"{status}Agent Sent Message regarding {prospect.title}"
    body = f"""
    {status}Message sent regarding: {prospect.title}
    URL: {prospect.url}

    Message Content:
    {message.content}
    """
    send_email(subject, body)

from database import retrieve_emails_for_today
import smtplib
from database import update_email_status
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from constants import TELEGRAM_TOKEN, SENDER_EMAIL, SENDER_PASSWORD
from telegram import Bot
import asyncio

bot = Bot(token=TELEGRAM_TOKEN)

async def send_email(recipient_email, subject, body, server):
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())


async def send_scheduled_emails():
    emails = await retrieve_emails_for_today()
    if not emails:
        return
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        for email in emails:
            try:
                await send_email(email[1], email[5],email[6], server)
                await update_email_status(email[0])
                await bot.send_message(chat_id=email[2], text="Your email has been sent !")
            except Exception as e:
                print("Erorr occured :", e)

async def main():
    await send_scheduled_emails()

if __name__ == "__main__":
    asyncio.run(main())
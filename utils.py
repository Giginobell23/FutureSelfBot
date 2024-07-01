from database import *
import requests_async as requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from constants import *

async def retrieve_scheduled_email_for_user(user_id):
    entries = await retrieve_scheduled_emails(user_id)
    if entries:
        return [[f"{i[0]} - {i[5]}"] for i in entries]
    return []

async def get_formatted_email(user_id,  email_id):
    data = await retrieve_email_by_id(email_id,user_id)
    if not data:
        return "Email not found -.-"
    
    formatted_text = f"Email scheduled for - {data[4]} ⏱\n\n"\
                     f"Address 📬\n`{data[1]}`\n"\
                     f"Subject 📥\n`{data[5]}`\n"\
                     f"Body 📧\n`{data[6]}`\n"
    return formatted_text

async def is_valid_date(date_string):
    try:
        datetime_object = datetime.strptime(date_string, '%Y-%m-%d')
        return datetime_object > datetime.now()
    except ValueError:
        return False

async def get_date_in_x_months(months):
    output = datetime.now() + relativedelta(months=months)
    return output.strftime("%Y-%m-%d")

async def delete_scheduled_email(user_id, email_id):
    if await delete_email_by_id(email_id, user_id):
        return "Successfully deleted"
    return "Email not found !"
    
async def insert_email(user_id, send_date,send_to, subject, body):
    await insert_email_db(user_id, send_date, send_to, subject, body)

initialize_database()
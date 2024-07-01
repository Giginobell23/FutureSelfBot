from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)
import logging
from constants import *
from utils import *
from keyboards import *

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

MAIN_MENU, DELETE_EMAIL, SHOW_EMAIL, INPUT_SUBJECT, INPUT_ADDRESS, INPUT_BODY, INPUT_DATE = range(7)

async def start(update, context):
    await update.message.reply_text(f"Welcome to FutureSelf Bot !\n\nYou can use this bot to send email to yourself in the future\n\n", reply_markup=main_menu_markup)
    return MAIN_MENU

async def main_menu(update, context):
    user_choice = update.message.text
    if user_choice == "See scheduled emails":
        scheduled_keyboard = await generate_email_keyboard(update.message.from_user.id)
        await update.message.reply_text("Which email do you wanna see ?", reply_markup=scheduled_keyboard)
        return SHOW_EMAIL
    elif user_choice == "Send new email":
        await update.message.reply_text("When do you want the email to be sent ?\n\nChoose an option or write a date in the format yyyy-mm-dd", reply_markup=date_options_markup)
        return INPUT_DATE
    elif user_choice == "Delete email":
        scheduled_keyboard = await generate_email_keyboard(update.message.from_user.id)
        await update.message.reply_text("Which email do you wanna delete ?", reply_markup=scheduled_keyboard)
        return DELETE_EMAIL

async def delete_email(update,context):
    user_choice = update.message.text
    if user_choice == "Back":
        await update.message.reply_text("Main menu:", reply_markup=main_menu_markup)
        return MAIN_MENU
    response_text = await delete_scheduled_email(update.message.from_user.id, user_choice.split("-")[0])
    await update.message.reply_text(response_text)
    await update.message.reply_text("Main menu:", reply_markup=main_menu_markup)
    return MAIN_MENU
    

async def input_date(update,context):
    user_choice = update.message.text
    if user_choice == "Back":
        await update.message.reply_text("Main menu :", reply_markup=main_menu_markup)
        return MAIN_MENU
    if user_choice == "1 month from now":
        date = await get_date_in_x_months(1)
    elif user_choice == "2 months from now":
        date = await get_date_in_x_months(2)
    elif user_choice == "5 months from now":
        date = await get_date_in_x_months(5)
    elif user_choice == "1 year from now":
        date = await get_date_in_x_months(12)
    else:
        is_valid = await is_valid_date(user_choice)
        if not is_valid:
            await update.message.reply_text("Invalid date, check the format and be sure that the date is at least tomorrow\n\nTry again", reply_markup=date_options_markup)
            return INPUT_DATE
        date = user_choice
    context.user_data["send_date"] = date
    await update.message.reply_text("Insert the email address you want the email to be sent to :", reply_markup=back_markup)
    return INPUT_ADDRESS

async def show_email(update,context):
    user_choice = update.message.text
    if user_choice == "Back":
        await update.message.reply_text("Main menu :", reply_markup=main_menu_markup)
        return MAIN_MENU
    else:
        reply_text = await get_formatted_email(update.message.from_user.id, user_choice.split('-')[0])
        await update.message.reply_text(reply_text, parse_mode='markdown')
        await update.message.reply_text("Select another mail to visualize or go back to the main menu :")

async def input_address(update,context):
    user_choice = update.message.text
    if user_choice == "Back":
        await update.message.reply_text("When do you want the email to be sent ?\n\nChoose an option or write a date in the format yyyy-mm-dd", reply_markup=date_options_markup)
        return INPUT_DATE
    context.user_data["send_to"] = user_choice
    await update.message.reply_text("Insert the subject of the e-mail you want to send:")
    return INPUT_SUBJECT

async def input_subject(update,context):
    user_choice = update.message.text
    if user_choice == "Back":
        await update.message.reply_text("Insert the email address you want the email to be sent to :")
        return INPUT_ADDRESS
    context.user_data["subject"] = user_choice
    await update.message.reply_text("Insert the email's body")
    return INPUT_BODY

async def input_body(update,context):
    user_choice = update.message.text
    if user_choice == "Back":
        await update.message.reply_text("Insert the subject of the e-mail you want to send:")
        return INPUT_SUBJECT
    await insert_email(update.message.from_user.id, context.user_data.pop("send_date"), context.user_data.pop("send_to"), context.user_data.pop("subject"), user_choice)
    await update.message.reply_text("Email successfully scheduled, please check in the scheduled tab\n\nBack to main menu:", reply_markup=main_menu_markup)
    return MAIN_MENU

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [MessageHandler(filters.Regex("^(See scheduled emails|Send new email|Delete email)$") & ~filters.COMMAND, main_menu)],
            DELETE_EMAIL: [MessageHandler(filters.Regex("^(\d+\s-\s.*|Back)$") & ~filters.COMMAND, delete_email)],
            INPUT_DATE : [MessageHandler(filters.Regex("^(1 month from now|2 months from now|5 months from now|1 year from now|\d{4}-\d{2}-\d{2}|Back)$") & ~filters.COMMAND, input_date)],
            INPUT_ADDRESS : [MessageHandler(filters.Regex("^([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|Back)$") & ~filters.COMMAND , input_address)],
            INPUT_SUBJECT : [MessageHandler(~filters.COMMAND, input_subject)],
            INPUT_BODY : [MessageHandler(~filters.COMMAND, input_body)],
            SHOW_EMAIL: [MessageHandler(filters.Regex("^(\d+\s-\s.*|Back)$") & ~filters.COMMAND, show_email)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)


    application.run_polling()

if __name__ == "__main__":
    main()
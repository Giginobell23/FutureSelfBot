from telegram import ReplyKeyboardMarkup
from utils import retrieve_scheduled_email_for_user

main_menu_keyboard = [["See scheduled emails", "Send new email"],["Delete email"]]
main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, one_time_keyboard=True)

date_options_keyboard = [["1 month from now"], ["2 months from now"], ["5 months from now"], ["1 year from now"]]
date_options_markup = ReplyKeyboardMarkup(date_options_keyboard, one_time_keyboard=True)

back_keyboard = [["Back"]]
back_markup = ReplyKeyboardMarkup(back_keyboard, one_time_keyboard=True)

async def generate_email_keyboard(user_id):
    emails = await retrieve_scheduled_email_for_user(user_id)
    buttons = emails + [["Back"]]
    return ReplyKeyboardMarkup(buttons, one_time_keyboard=False)


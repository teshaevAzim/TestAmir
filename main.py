from telegram.ext import Updater, CommandHandler, Dispatcher, CallbackQueryHandler, CallbackContext, MessageHandler, \
    Filters, ConversationHandler, Job, JobQueue
from telegram.update import Update
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import settings
import requests
import datetime

updater = Updater(token=settings.API_TOKEN)
bot = Bot(token=settings.API_TOKEN)

CHANNEL_USERNAME = "@dsada32"
dispatcher: Dispatcher = updater.dispatcher

subChannel = [
    [InlineKeyboardButton(text="A`zo bo`lish↗️", url="https://t.me/dsada32")],
    [InlineKeyboardButton(text="Tekshirish✅", callback_data="submit")]
]
menu = [
    [InlineKeyboardButton(text="Name to picture 🖼", callback_data="nameToPic")],
    [InlineKeyboardButton(text="Translator", callback_data="translator")]
]


def check_channel(check_member):
    if check_member['status'] != "left":
        return True
    else:
        return False


def Menu(update: Update, context: CallbackContext):
    if update.message.from_user.last_name != "":
        update.message.reply_html(
            f"<a href='tg://settings'>{update.message.from_user.first_name}</a>, quyidagi tugmalardan birini tanlang ⬇",
            reply_markup=InlineKeyboardMarkup(menu))
    else:
        update.message.reply_text(
            f"{update.message.from_user.first_name} {update.message.from_user.last_name}, quyidagi tugmalardan birini tanlang ⬇",
            reply_markup=InlineKeyboardMarkup(menu))


def start(update: Update, context: CallbackContext):
    if check_channel(bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=update.message.from_user.id)):
        Menu(update, context)
    else:
        message = update.message
        message.reply_text(
            f"{message.from_user.first_name}, iltimos kanalimizga obuna bo`ling",
            reply_markup=InlineKeyboardMarkup(subChannel))


def callback_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == "submit":
        if check_channel(bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=query.from_user.id)):
            if query.from_user.last_name != "":
                query.edit_message_text(
                    f"{query.from_user.first_name} {query.from_user.last_name}, quyidagi tugmalardan birini tanlang ⬇",
                    reply_markup=InlineKeyboardMarkup(menu))
            else:
                query.edit_message_text(
                    f"{query.from_user.first_name}, quyidagi tugmalardan birini tanlang ⬇",
                    reply_markup=InlineKeyboardMarkup(menu))
        else:
            if query.from_user.last_name != "":
                query.delete_message()
                query.message.reply_html(
                    f"{query.from_user.first_name} {query.from_user.last_name} kanalimizga <b>obuna bo`lmadingiz</b>, iltimos kanalimizga obuna bo`ling",
                    reply_markup=InlineKeyboardMarkup(subChannel))
            else:
                query.delete_message()
                query.message.reply_html(
                    f"{query.from_user.first_name} kanalimizga <b>obuna bo`lmadingiz</b>, iltimos kanalimizga obuna bo`ling",
                    reply_markup=InlineKeyboardMarkup(subChannel))
    elif query.data == "nameToPic":
        if check_channel(bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=query.from_user.id)):
            if query.from_user.last_name != "":
                query.edit_message_text(
                    f"{query.from_user.first_name} {query.from_user.last_name}, so'z yuboring",
                    reply_markup=InlineKeyboardMarkup(menu))
            else:
                query.edit_message_text(
                    f"{query.from_user.first_name}, so'z yuboring",
                    reply_markup=InlineKeyboardMarkup(menu))
        else:
            if query.from_user.last_name != "":
                query.delete_message()
                query.message.reply_html(
                    f"{query.from_user.first_name} {query.from_user.last_name} kanalimizga <b>obuna bo`lmadingiz</b>, iltimos kanalimizga obuna bo`ling",
                    reply_markup=InlineKeyboardMarkup(subChannel))
            else:
                query.delete_message()
                query.message.reply_html(
                    f"{query.from_user.first_name} kanalimizga <b>obuna bo`lmadingiz</b>, iltimos kanalimizga obuna bo`ling",
                    reply_markup=InlineKeyboardMarkup(subChannel))


# conversation = ConversationHandler(
#     states=dispatcher.add_handler(CommandHandler('start', start)),
#
# )
def echo(update: Update):
    print("Echo")

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(callback_query))

if __name__ == '__main__':
    job_queue = JobQueue()
    job_queue.set_dispatcher(dispatcher)
    job_queue.run_repeating(callback=echo, interval=5)
    updater.start_polling()
    job_queue.start()
    print(datetime.datetime.now())
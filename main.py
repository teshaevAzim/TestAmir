import requests
import settings
import datetime
from telegram.ext import Updater, CallbackContext, CommandHandler, Dispatcher, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.update import Update

updater = Updater(token=settings.API_TOKEN)
dispatcher: Dispatcher = updater.dispatcher

keyboard = [
    [InlineKeyboardButton("Toshkent", callback_data="toshkent"),
     InlineKeyboardButton("Namangan", callback_data="namangan")],
    [InlineKeyboardButton("Buxoro", callback_data="buxoro"),
    InlineKeyboardButton("Xorazm", callback_data="khiva")],
    [InlineKeyboardButton("Surxondaryo", callback_data="shahrisabz"),
     InlineKeyboardButton("Navoiy", callback_data="navoiy")],
    [InlineKeyboardButton("Samarqand", callback_data="samarqand"),
     InlineKeyboardButton("Qashqadaryo", callback_data="qashqadaryo")],
    [InlineKeyboardButton("Andijon", callback_data="andijon"),
    InlineKeyboardButton("Jizzax", callback_data="jizzax")],
    [InlineKeyboardButton("Farg'ona", callback_data="farg'ona"),
     InlineKeyboardButton("Qoraqalpog'iston", callback_data="qoraqalpoq")],
]
back = [
    [InlineKeyboardButton("⬅️Ortga", callback_data="back")]
]


def start(update: Update, context: CallbackContext):
    update.message.reply_html(f"Assalomu alaykum, <b>{update.message.from_user.first_name}</b>\n \n"
                              f"Kerakli shaharni tanlang 👇", reply_markup=InlineKeyboardMarkup(keyboard))


def back_(query):
    query.answer()
    query.edit_message_text("Kerakli shaharni tanlang 👇", reply_markup=InlineKeyboardMarkup(keyboard))


def callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data != "back":
        try:
            City = query.data
            url = f'http://api.openweathermap.org/data/2.5/weather?q={City}&appid={settings.API_KEY}&units=metric'
            res = requests.get(url)
            data = res.json()
            city = data['name']
            kun_davomiyligi = datetime.datetime.fromtimestamp(data['sys']['sunset']) - \
                              datetime.datetime.fromtimestamp(data['sys']['sunrise'])
            temp = data['main']['temp']
            wind_speed = data['wind']['speed']
            ob_havo = data['weather'][0]['main']
            if ob_havo in settings.code_smiles_uz:
                wd = settings.code_smiles_uz[ob_havo]
            else:
                wd = f"{ob_havo}"
            query.edit_message_text(
                f"🌇<b>Shahar:</b> \t{city}\n☂<b>Joriy ob-havo:</b> \t{temp} ℃ \t{wd}\n💨<b>Shamol tezligi:</b> \t{wind_speed} m/s\n🌔<b>Kun davomiyligi:</b> \t{kun_davomiyligi}\n<u>Kuningiz xayrli o`tsin</u>",
                parse_mode="HTML", reply_markup=InlineKeyboardMarkup(back)
                )
        except Exception as e:
            print(e)
    elif query.data == "back":
        back_(query)


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(callback_handler))

if __name__ == '__main__':
    updater.start_polling()
    updater.idle()

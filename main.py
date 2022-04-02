import requests
import datetime
from telegram.ext import Updater, CallbackContext, CommandHandler, Dispatcher, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.update import Update

updater = Updater(token="5245421544:AAH8KJL3QaJxSSEfuBU1ysI0W3HpfHa5J0c")
dispatcher: Dispatcher = updater.dispatcher
    
 code_smiles_uz = {
    "Clear": "Toza \U00002600",
    "Clouds": "Bulutli \U00002601",
    "Rain": "Yomg`ir \U00002614",
    "Drizzle": "Yomg`ir \U00002614",
    "Thunderstorm": "Chaqmoq \U000026A1",
    "Snow": "Qor \U0001F328",
    "Mist": "Tuman \U0001F32B"
}

code_smiles_ru = {
    "Clear": f"{translater.translate('Toza', 'ru').text} \U00002600",
    "Clouds": f"{translater.translate('Bulutli', 'ru').text} \U00002601",
    "Rain": f"{translater.translate('Yomg`ir', 'ru').text} \U00002614",
    "Drizzle": f"{translater.translate('Yomg`ir', 'ru').text} \U00002614",
    "Thunderstorm": f"{translater.translate('Chaqmoq', 'ru').text} \U000026A1",
    "Snow": f"{translater.translate('Qor', 'ru').text} \U0001F328",
    "Mist": f"{translater.translate('Tuman', 'ru').text} \U0001F32B"
}

API_KEY = "aeff74af7fec2b68fb196a72a6e458f1"

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
            url = f'http://api.openweathermap.org/data/2.5/weather?q={City}&appid={API_KEY}&units=metric'
            res = requests.get(url)
            data = res.json()
            city = data['name']
            kun_davomiyligi = datetime.datetime.fromtimestamp(data['sys']['sunset']) - \
                              datetime.datetime.fromtimestamp(data['sys']['sunrise'])
            temp = data['main']['temp']
            wind_speed = data['wind']['speed']
            ob_havo = data['weather'][0]['main']
            if ob_havo in code_smiles_uz:
                wd = code_smiles_uz[ob_havo]
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

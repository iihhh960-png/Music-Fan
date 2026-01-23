import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# ၁။ Bot Token Setting
TOKEN = '8559670246:AAGXQN8Se_pnmPk6eUvM_n1QfbWxnCH5To8'
bot = telebot.TeleBot(TOKEN)

# ၂။ Render Port Error မတက်အောင် Flask Server ဆောက်ခြင်း
app = Flask('')

@app.route('/')
def home():
    return "Bot is Online!"

def run():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ၃။ သီချင်းစာရင်း (File ID တွေကို နောက်မှ ပြန်လဲပေးရန်)
SONG_DATA = {
    "chill": {
        "title": " အေးအေးလေး သီချင်းများ",
        "songs": {
            "c1": {"name": "အေးအေးလေး (၁)", "file_id": "YOUR_FILE_ID_HERE"},
            "c2": {"name": "အေးအေးလေး (၂)", "file_id": "YOUR_FILE_ID_HERE"},
        }
    },
    "rap": {
        "title": " Rap သီချင်းများ",
        "songs": {
            "r1": {"name": "Rap (၁)", "file_id": "YOUR_FILE_ID_HERE"},
            "r2": {"name": "Rap (၂)", "file_id": "YOUR_FILE_ID_HERE"},
        }
    }
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_chill = types.InlineKeyboardButton(" အေးအေးလေး", callback_data="cat_chill")
    btn_rap = types.InlineKeyboardButton(" Rap", callback_data="cat_rap")
    markup.add(btn_chill, btn_rap)
    bot.send_message(message.chat.id, "Welcome! သီချင်းအမျိုးအစား ရွေးပေးပါ -", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data.startswith("cat_"):
        cat_key = call.data.split("_")[1]
        category = SONG_DATA[cat_key]
        markup = types.InlineKeyboardMarkup(row_width=1)
        for s_id, s_info in category["songs"].items():
            markup.add(types.InlineKeyboardButton(s_info["name"], callback_data=f"play_{cat_key}_{s_id}"))
        markup.add(types.InlineKeyboardButton(" Back", callback_data="main_menu"))
        bot.edit_message_text(f" {category['title']}", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data.startswith("play_"):
        _, cat, s_id = call.data.split("_")
        song = SONG_DATA[cat]["songs"][s_id]
        if song["file_id"] == "YOUR_FILE_ID_HERE":
            bot.answer_callback_query(call.id, text="Error: File ID မထည့်ရသေးပါ!")
        else:
            bot.send_audio(call.message.chat.id, song["file_id"], caption=f" {song['name']}")
            bot.answer_callback_query(call.id)

    elif call.data == "main_menu":
        start(call.message)

# File ID ယူရန်အပိုင်း
@bot.message_handler(content_types=['audio'])
def get_id(message):
    bot.reply_to(message, f"ဒီသီချင်းရဲ့ ID က:\n`{message.audio.file_id}`", parse_mode="Markdown")

# ၄။ Bot ကို စတင်မောင်းနှင်ခြင်း
if __name__ == "__main__":
    keep_alive() # Port ဖွင့်ပေးရန်
    print("Bot is starting...")
    bot.infinity_polling()

import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# ၁။ Bot Token
TOKEN = '8559670246:AAGXQN8Se_pnmPk6eUvM_n1QfbWxnCH5To8'
bot = telebot.TeleBot(TOKEN)

# ၂။ Render အတွက် အမြဲနိုးနေစေမယ့် Flask Setup
app = Flask('')
@app.route('/')
def home(): return "Bot is Online and Ready!"

def run():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ၃။ သီချင်းဒေတာများ (Chill ထဲသို့ ၇ ပုဒ် နှင့် Rap ထဲသို့ ၁ ပုဒ် ခွဲလိုက်ပါပြီ)
SONG_DATA = {
    "chill": {
        "title": " အေးအေးလေး သီချင်းများ",
        "songs": [
            {"name": "ပူစူး - နင်စေရင်", "file_id": "CQACAgUAAxkBAAMIaXObNtjgObKs2O7oejTdLFVcR2AAAhUhAAJvFaBX5XBvlccGtns4BA"},
            {"name": "ကိုယ့်အနားရှိစေချင်", "file_id": "CQACAgUAAxkBAAMKaXObVnlhYFsWOGkuDucZW3i9BGEAAo8bAAL9oplXeCtEwYW8JmA4BA"},
            {"name": "WHY", "file_id": "CQACAgUAAxkBAAMMaXOcIKnD4lc5EPswG1ZBZdIopwsAAhYhAAJvFaBX7TREe2bfnWo4BA"},
            {"name": "ဆေးလိပ်နဲ့မီးချစ်", "file_id": "CQACAgUAAxkBAAMQaXOcdeEoBakGxJ6epQgl0KmTwOgAAhghAAJvFaBXcb4r7Z7mHlk4BA"},
            {"name": "ရင်နာတယ်ဧပရယ်", "file_id": "CQACAgUAAxkBAAMSaXOc2SsWc0YqU_vu6xs9R9C_t9UAAhshAAJvFaBXCEUpE_DasYw4BA"},
            {"name": "သိုးမည်းတေအကြောင်း", "file_id": "CQACAgUAAxkBAAMOaXOcPMkHREd8b7jY8X0obEvT2tYAAhchAAJvFaBXaa8ZotsvmQo4BA"},
            {"name": "ဒဿ", "file_id": "CQACAgUAAxkBAAMWaXOoA7eemPmp3lxr_aesCqilD10AAighAAJvFaBXEzakoXUhHDA4BA"}
        ]
    },
    "rap": {
        "title": " Rap သီချင်းများ",
        "songs": [
            {"name": "ခမ်းနားလွန်းတဲ့နေ့", "file_id": "CQACAgUAAxkBAAMUaXOndUxdQiDrpgbQMqkkmoQcT_sAAichAAJvFaBXAW9yBr7b3WM4BA"}
        ]
    }
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(" အေးအေးလေး", callback_data="cat_chill"),
               types.InlineKeyboardButton(" Rap", callback_data="cat_rap"))
    bot.send_message(message.chat.id, " **Music Player** မှ ကြိုဆိုပါတယ်\nနားဆင်လိုသော အမျိုးအစားကို ရွေးပါ -", 
                     reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data.startswith("cat_"):
        cat_key = call.data.split("_")[1]
        category = SONG_DATA[cat_key]
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i, song in enumerate(category["songs"]):
            markup.add(types.InlineKeyboardButton(song["name"], callback_data=f"play_{cat_key}_{i}"))
        markup.add(types.InlineKeyboardButton(" မူလစာမျက်နှာသို့", callback_data="main_menu"))
        bot.edit_message_text(f" {category['title']}", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data.startswith("play_"):
        _, cat, index = call.data.split("_")
        index = int(index)
        song = SONG_DATA[cat]["songs"][index]
        
        # Player Buttons
        markup = types.InlineKeyboardMarkup(row_width=3)
        prev_idx = (index - 1) % len(SONG_DATA[cat]["songs"])
        next_idx = (index + 1) % len(SONG_DATA[cat]["songs"])
        
        markup.add(
            types.InlineKeyboardButton(" ရှေ့", callback_data=f"play_{cat}_{prev_idx}"),
            types.InlineKeyboardButton(" ပိတ်မယ်", callback_data="stop_music"),
            types.InlineKeyboardButton(" နောက်", callback_data=f"play_{cat}_{next_idx}")
        )
        markup.add(types.InlineKeyboardButton(" စာရင်းပြန်ကြည့်မယ်", callback_data=f"cat_{cat}"))

        bot.send_audio(call.message.chat.id, song["file_id"], 
                       caption=f"ယခုဖွင့်နေသည်-  **{song['name']}**", 
                       reply_markup=markup, parse_mode="Markdown")
        bot.answer_callback_query(call.id)

    elif call.data == "stop_music":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "သီချင်း Player ကို ပိတ်လိုက်ပါပြီ။\nပြန်လည်နားဆင်လိုလျှင် /start ကို နှိပ်ပါ။")

    elif call.data == "main_menu":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start(call.message)

# Bot Run ခြင်း
if __name__ == "__main__":
    keep_alive() # Render Port အတွက်
    print("Bot is starting...")
    bot.infinity_polling()

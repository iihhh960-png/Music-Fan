import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# ၁။ Bot Token နှင့် Channel ID
TOKEN = '8559670246:AAGXQN8Se_pnmPk6eUvM_n1QfbWxnCH5To8'
CHANNEL_ID = '@musicfan11234' 
bot = telebot.TeleBot(TOKEN)

# ၂။ Render အတွက် Flask Setup
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

def run():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ၃။ Channel Join မ Join စစ်ဆေးသည့် Function
def is_user_member(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except Exception:
        return False

# ၄။ သီချင်းဒေတာများ
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

# ၅။ သီချင်းအမျိုးအစား Menu ပြသသည့် Function
def show_music_categories(chat_id, message_id=None):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(" အေးအေးလေး", callback_data="cat_chill"),
               types.InlineKeyboardButton(" Rap", callback_data="cat_rap"))
    
    text = " **Music Player**\nနားဆင်လိုသော အမျိုးအစားကို ရွေးချယ်ပါ -"
    
    if message_id:
        bot.edit_message_text(text, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    if is_user_member(message.from_user.id):
        show_music_categories(message.chat.id)
    else:
        markup = types.InlineKeyboardMarkup()
        btn_join = types.InlineKeyboardButton(" Channel Join ရန်", url="https://t.me/musicfan11234")
        btn_check = types.InlineKeyboardButton(" Ch Join ပြီးပါပြီ", callback_data="check_join")
        markup.add(btn_join)
        markup.add(btn_check)
        bot.send_message(message.chat.id, " **သတိပေးချက်**\n\nဒီ Bot ကို အသုံးပြုဖို့အတွက် ကျွန်တော်တို့ရဲ့ Channel ကို အရင် Join ပေးရပါမယ်။", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "check_join":
        if is_user_member(call.from_user.id):
            # Join ထားတာ မှန်ကန်ရင် သီချင်း Menu ပြမယ်
            show_music_categories(call.message.chat.id, call.message.message_id)
        else:
            # Join မထားဘဲ နှိပ်ရင် ပြန်ပြောမယ့်စာ
            bot.answer_callback_query(call.id, " Bot ကို Channel အရင် Join ပေးပါဦး!", show_alert=True)
        return

    # Join မထားဘဲ တခြားဟာတွေ နှိပ်ရင်လည်း တားထားမယ်
    if not is_user_member(call.from_user.id):
        bot.answer_callback_query(call.id, " ကျေးဇူးပြု၍ Channel အရင် Join ပါ!", show_alert=True)
        return

    if call.data.startswith("cat_"):
        cat_key = call.data.split("_")[1]
        category = SONG_DATA[cat_key]
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i, song in enumerate(category["songs"]):
            markup.add(types.InlineKeyboardButton(song["name"], callback_data=f"play_{cat_key}_{i}"))
        markup.add(types.InlineKeyboardButton(" Back", callback_data="main_menu"))
        bot.edit_message_text(f" {category['title']}", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data.startswith("play_"):
        _, cat, index = call.data.split("_")
        index = int(index)
        song = SONG_DATA[cat]["songs"][index]
        
        markup = types.InlineKeyboardMarkup(row_width=3)
        prev_idx = (index - 1) % len(SONG_DATA[cat]["songs"])
        next_idx = (index + 1) % len(SONG_DATA[cat]["songs"])
        markup.add(
            types.InlineKeyboardButton(" ရှေ့", callback_data=f"play_{cat}_{prev_idx}"),
            types.InlineKeyboardButton(" ပိတ်မယ်", callback_data="stop_music"),
            types.InlineKeyboardButton(" နောက်", callback_data=f"play_{cat}_{next_idx}")
        )
        bot.send_audio(call.message.chat.id, song["file_id"], caption=f" **{song['name']}**", reply_markup=markup, parse_mode="Markdown")
        bot.answer_callback_query(call.id)

    elif call.data == "stop_music":
        bot.delete_message(call.message.chat.id, call.message.message_id)
    
    elif call.data == "main_menu":
        show_music_categories(call.message.chat.id, call.message.message_id)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

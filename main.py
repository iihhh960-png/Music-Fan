import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

TOKEN = '8559670246:AAGXQN8Se_pnmPk6eUvM_n1QfbWxnCH5To8'
CH1_ID = -1003628384777
CH2_ID = -1003882533307

bot = telebot.TeleBot(TOKEN)

app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

def run():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

def is_user_member(user_id):
    try:
        status1 = bot.get_chat_member(CH1_ID, user_id).status
        status2 = bot.get_chat_member(CH2_ID, user_id).status
        return status1 in ['member', 'administrator', 'creator'] and \
               status2 in ['member', 'administrator', 'creator']
    except Exception:
        return False

# Emoji Unicode များ- \U0001F1F2\U0001F1F1 (MM Flag), \U0001F3B5 (Music Note)
SONG_DATA = {
    "myanmar": {
        "title": "\U0001F1F2\U0001F1F1 Myanmar Songs",
        "singers": {
            "ပူစူး Songs": [{"name": "ပူစူး - နင်စေရင်", "file_id": "CQACAgUAAxkBAAMIaXObNtjgObKs2O7oejTdLFVcR2AAAhUhAAJvFaBX5XBvlccGtns4BA"}],
            "အာဇာနည် Songs": [{"name": "ကိုယ့်အနားရှိစေချင်", "file_id": "CQACAgUAAxkBAAMKaXObVnlhYFsWOGkuDucZW3i9BGEAAo8bAAL9oplXeCtEwYW8JmA4BA"}],
            "Double J Songs": [{"name": "WHY", "file_id": "CQACAgUAAxkBAAMMaXOcIKnD4lc5EPswG1ZBZdIopwsAAhYhAAJvFaBX7TREe2bfnWo4BA"}],
            "Raymond Songs": [{"name": "ဆေးလိပ်နဲ့မီးချစ်", "file_id": "CQACAgUAAxkBAAMQaXOcdeEoBakGxJ6epQgl0KmTwOgAAhghAAJvFaBXcb4r7Z7mHlk4BA"}],
            "ဟန်ထွန်း Songs": [{"name": "ရင်နာတယ်ဧပရယ်", "file_id": "CQACAgUAAxkBAAMSaXOc2SsWc0YqU_vu6xs9R9C_t9UAAhshAAJvFaBXCEUpE_DasYw4BA"}],
            "ဗဒင် Songs": [{"name": "သိုးမည်းတေအကြောင်း", "file_id": "CQACAgUAAxkBAAMOaXOcPMkHREd8b7jY8X0obEvT2tYAAhchAAJvFaBXaa8ZotsvmQo4BA"}],
            "NJ Songs": [{"name": "ဒဿ", "file_id": "CQACAgUAAxkBAAMWaXOoA7eemPmp3lxr_aesCqilD10AAighAAJvFaBXEzakoXUhHDA4BA"}]
        }
    },
    "english": {
        "title": "\U0001F1FA\U0001F1F8 English Songs",
        "singers": {}
    }
}

def show_music_categories(chat_id, message_id=None):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("\U0001F1F2\U0001F1F1 Myanmar Songs", callback_data="cat_myanmar"),
               types.InlineKeyboardButton("\U0001F1FA\U0001F1F8 English Songs", callback_data="cat_english"))
    text = "\U0001F3B5 **Music Player**\nနားဆင်လိုသော အမျိုးအစားကို ရွေးချယ်ပါ -"
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
        btn_join1 = types.InlineKeyboardButton("\U0001F4E2 Channel 1 Join ရန်", url="https://t.me/musicfan11234")
        btn_join2 = types.InlineKeyboardButton("\U0001F4E2 Channel 2 Join ရန်", url="https://t.me/musicfan11234")
        btn_check = types.InlineKeyboardButton("\u2705 Ch Join ပြီးပါပြီ", callback_data="check_join")
        markup.add(btn_join1, btn_join2)
        markup.add(btn_check)
        bot.send_message(message.chat.id, "\u26A0\uFE0F **သတိပေးချက်**\n\nBot ကို သုံးရန် Channel (၂) ခုလုံးကို Join ပေးရပါမယ်။", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "check_join":
        if is_user_member(call.from_user.id):
            show_music_categories(call.message.chat.id, call.message.message_id)
        else:
            bot.answer_callback_query(call.id, "\u274C Channel (၂) ခုလုံးကို Join ပေးပါဦး!", show_alert=True)
        return

    if not is_user_member(call.from_user.id):
        bot.answer_callback_query(call.id, "\u26A0\uFE0F ကျေးဇူးပြု၍ Channel အရင် Join ပါ!", show_alert=True)
        return

    if call.data.startswith("cat_"):
        cat_key = call.data.split("_")[1]
        singers = SONG_DATA[cat_key]["singers"]
        markup = types.InlineKeyboardMarkup(row_width=2)
        for singer in singers.keys():
            markup.add(types.InlineKeyboardButton(singer, callback_data=f"singer_{cat_key}_{singer}"))
        markup.add(types.InlineKeyboardButton("\U0001F519 Back", callback_data="main_menu"))
        instruction_text = "ကိုယ်နားထောင်ချင်တဲ့ အဆိုတော်နာမည် ကိုရွေးပေးပါ ခင်ဗျာ"
        bot.edit_message_text(f"\U0001F3A4 **{SONG_DATA[cat_key]['title']}**\n\n{instruction_text}", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("singer_"):
        _, cat_key, singer_name = call.data.split("_")
        songs = SONG_DATA[cat_key]["singers"][singer_name]
        if not songs:
            bot.answer_callback_query(call.id, "\u26A0\uFE0F ဤအဆိုတော်၏ သီချင်းမရှိသေးပါ!", show_alert=True)
            return
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i, song in enumerate(songs):
            markup.add(types.InlineKeyboardButton(song["name"], callback_data=f"play_{cat_key}_{singer_name}_{i}"))
        markup.add(types.InlineKeyboardButton("\U0001F519 Back", callback_data=f"cat_{cat_key}"))
        bot.edit_message_text(f"\U0001F3A7 **{singer_name}**\nနားဆင်လိုသော သီချင်းကို ရွေးချယ်ပါ -", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("play_"):
        _, cat, singer, index = call.data.split("_")
        index = int(index)
        songs_list = SONG_DATA[cat]["singers"][singer]
        song = songs_list[index]
        markup = types.InlineKeyboardMarkup(row_width=3)
        
        if len(songs_list) > 1:
            prev_idx = (index - 1) % len(songs_list)
            next_idx = (index + 1) % len(songs_list)
            markup.add(
                types.InlineKeyboardButton("\u23EE\uFE0F ရှေ့", callback_data=f"play_{cat}_{singer}_{prev_idx}"),
                types.InlineKeyboardButton("\u23F9\uFE0F ပိတ်မယ်", callback_data="stop_music"),
                types.InlineKeyboardButton("\u23ED\uFE0F နောက်", callback_data=f"play_{cat}_{singer}_{next_idx}")
            )
        else:
            markup.add(types.InlineKeyboardButton("\u23F9\uFE0F ပိတ်မယ်", callback_data="stop_music"))
            
        bot.send_audio(call.message.chat.id, song["file_id"], caption=f"\U0001F3B5 **{song['name']}**", reply_markup=markup, parse_mode="Markdown")

    elif call.data == "stop_music":
        bot.delete_message(call.message.chat.id, call.message.message_id)
    
    elif call.data == "main_menu":
        show_music_categories(call.message.chat.id, call.message.message_id)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

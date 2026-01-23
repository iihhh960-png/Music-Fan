import telebot
from telebot import types

# သင်ပေးထားတဲ့ Token ကို ထည့်သွင်းထားပါတယ်
TOKEN = '8559670246:AAGXQN8Se_pnmPk6eUvM_n1QfbWxnCH5To8'
bot = telebot.TeleBot(TOKEN)

# သီချင်းစာရင်း (ဒီနေရာက File ID တွေကို သင်ပို့လို့ရလာတဲ့ ID တွေနဲ့ လဲပေးပါ)
SONG_DATA = {
    "chill": {
        "title": " အေးအေးလေး သီချင်းများ",
        "songs": {
            "c1": {"name": "အေးအေးလေး (၁)", "file_id": "ဒီနေရာမှာ_File_ID_ထည့်ပါ"},
            "c2": {"name": "အေးအေးလေး (၂)", "file_id": "ဒီနေရာမှာ_File_ID_ထည့်ပါ"},
        }
    },
    "rap": {
        "title": " Rap သီချင်းများ",
        "songs": {
            "r1": {"name": "Rap (၁)", "file_id": "ဒီနေရာမှာ_File_ID_ထည့်ပါ"},
            "r2": {"name": "Rap (၂)", "file_id": "ဒီနေရာမှာ_File_ID_ထည့်ပါ"},
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
        if song["file_id"] == "ဒီနေရာမှာ_File_ID_ထည့်ပါ":
            bot.answer_callback_query(call.id, text="Error: File ID မထည့်ရသေးပါ!")
        else:
            bot.send_audio(call.message.chat.id, song["file_id"], caption=f" {song['name']}")
            bot.answer_callback_query(call.id)

    elif call.data == "main_menu":
        start(call.message)

# File ID ယူဖို့အတွက် (သီချင်းပို့ရင် ID ပြန်ပြောပေးမယ့်အပိုင်း)
@bot.message_handler(content_types=['audio'])
def get_id(message):
    bot.reply_to(message, f"ဒီသီချင်းရဲ့ ID က:\n`{message.audio.file_id}`", parse_mode="Markdown")

bot.infinity_polling()

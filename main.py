import telebot
from telebot import types

# Bot Token ကို ဒီမှာ ထည့်ပါ
TOKEN = '8559670246:AAGXQN8Se_pnmPk6eUvM_n1QfbWxnCH5To8'
bot = telebot.TeleBot(TOKEN)

# သီချင်းစာရင်းကို အမျိုးအစားအလိုက် စနစ်တကျ စုစည်းထားခြင်း
SONG_DATA = {
    "chill": {
        "title": " အေးအေးလေး သီချင်းများ",
        "songs": {
            "c1": {"name": "သီချင်း ၁ (အေးအေး)", "file_id": "FILE_ID_HERE"},
            "c2": {"name": "သီချင်း ၂ (အေးအေး)", "file_id": "FILE_ID_HERE"},
            "c3": {"name": "သီချင်း ၃ (အေးအေး)", "file_id": "FILE_ID_HERE"},
        }
    },
    "rap": {
        "title": " Rap သီချင်းများ",
        "songs": {
            "r1": {"name": "Rap ၁ (နာမည်)", "file_id": "FILE_ID_HERE"},
            "r2": {"name": "Rap ၂ (နာမည်)", "file_id": "FILE_ID_HERE"},
            "r3": {"name": "Rap ၃ (နာမည်)", "file_id": "FILE_ID_HERE"},
        }
    }
}

# ၁။ /start command - အမျိုးအစား ရွေးခိုင်းမယ်
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_chill = types.InlineKeyboardButton(" အေးအေးလေး", callback_data="cat_chill")
    btn_rap = types.InlineKeyboardButton(" Rap", callback_data="cat_rap")
    markup.add(btn_chill, btn_rap)
    
    bot.send_message(message.chat.id, "Welcome! နားဆင်ချင်တဲ့ အမျိုးအစားကို ရွေးပါ -", reply_markup=markup)

# ၂။ Button နှိပ်မှုအားလုံးကို ကိုင်တွယ်ခြင်း
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    # အမျိုးအစားရွေးချယ်ခြင်း
    if call.data.startswith("cat_"):
        cat_key = call.data.split("_")[1]
        category = SONG_DATA[cat_key]
        
        markup = types.InlineKeyboardMarkup(row_width=1) # တစ်ကြောင်းချင်းစီပြမယ်
        for s_id, s_info in category["songs"].items():
            markup.add(types.InlineKeyboardButton(s_info["name"], callback_data=f"play_{cat_key}_{s_id}"))
        
        markup.add(types.InlineKeyboardButton(" Back (နောက်သို့)", callback_data="main_menu"))
        
        bot.edit_message_text(f" {category['title']}\nသီချင်းတစ်ပုဒ်ကို ရွေးပါ -", 
                             call.message.chat.id, call.message.message_id, reply_markup=markup)

    # သီချင်းပို့ပေးခြင်း
    elif call.data.startswith("play_"):
        _, cat, s_id = call.data.split("_")
        song = SONG_DATA[cat]["songs"][s_id]
        
        bot.answer_callback_query(call.id, text="သီချင်း ပို့ပေးနေပါပြီ...")
        bot.send_audio(call.message.chat.id, song["file_id"], caption=f" {song['name']}")

    # Main Menu ပြန်သွားခြင်း
    elif call.data == "main_menu":
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_chill = types.InlineKeyboardButton(" အေးအေးလေး", callback_data="cat_chill")
        btn_rap = types.InlineKeyboardButton(" Rap", callback_data="cat_rap")
        markup.add(btn_chill, btn_rap)
        bot.edit_message_text("နားဆင်ချင်တဲ့ အမျိုးအစားကို ရွေးပါ -", 
                             call.message.chat.id, call.message.message_id, reply_markup=markup)

# ၃။ File ID ယူဖို့အတွက် ခဏသုံးရန် (ID ရပြီဆိုရင် ဒီအပိုင်းကို ဖျက်လိုက်လို့ရပါတယ်)
@bot.message_handler(content_types=['audio'])
def get_id(message):
    bot.reply_to(message, f"ဒီသီချင်းရဲ့ File ID က:\n`{message.audio.file_id}`", parse_mode="Markdown")

print("Bot is starting...")
bot.infinity_polling()

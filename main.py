import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

TOKEN = '8559670246:AAGXQN8Se_pnmPk6eUvM_n1QfbWxnCH5To8'
CH1_ID = -1003628384777   
CH2_ID = -1002305886367   

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
        allowed = ['member', 'administrator', 'creator']
        if status1 in ['administrator', 'creator'] or status2 in ['administrator', 'creator']:
            return True
        return status1 in allowed and status2 in allowed
    except Exception:
        return False

SONG_DATA = {
    "myanmar": {
        "title": "\U0001F1F2\U0001F1F1 Myanmar Songs",
        "singers": {
            "ပူစူး Songs": [
                {"name": "နင်စေရင်", "file_id": "CQACAgUAAxkBAAMIaXObNtjgObKs2O7oejTdLFVcR2AAAhUhAAJvFaBX5XBvlccGtns4BA"},
                {"name": "မျက်နှာ", "file_id": "CQACAgUAAxkBAAOaaXhlxPPAsS8HBZzDLltEBuFPSwkAAgMeAALq-cBXT0MIYpL2UTg4BA"},
                {"name": "တစ်မိုးအောက်", "file_id": "CQACAgUAAxkBAAOfaXh_LS3JrTsmlRl4JMTvyU5lsRQAAjgeAALq-cBXtEs08go0rSY4BA"},
                {"name": "နေချင်တာမင်းအနား", "file_id": "CQACAgUAAxkBAAOhaXh_LZsDWtS8w0KZoyU_AAGQSEFLAAI8HgAC6vnAV5gPIWGTWV8TOAQ"},
                {"name": "ဝန်ခံပါ", "file_id": "CQACAgUAAxkBAAOiaXh_LbSKml2kC9P9sD1erY1KTI4AAj8eAALq-cBX1UAMsVP4Yzk4BA"},
                {"name": "မ", "file_id": "CQACAgUAAxkBAAOjaXh_LWGAFfbp9f5L2ZAJhLLlc2IAAkMeAALq-cBXRZytklpsAAEKOAQ"},
                {"name": "မင်းစိတ်တိုင်းကျ", "file_id": "CQACAgUAAxkBAAOkaXh_LScX8iVmLg0-qWDRFIWXkDEAAkYeAALq-cBXKWyc-xzg2WQ4BA"},
                {"name": "မယ်သီတာကိုမထိနဲ့", "file_id": "CQACAgUAAxkBAAOlaXh_LQuW59C6ZbwNUNP9MOdKhJMAAkgeAALq-cBXvF_agqiJ7Ac4BA"},
                {"name": "အဆင်ပြေပါစေ", "file_id": "CQACAgUAAxkBAAOmaXh_LY9j8z8TDC7khCqlj9F3hioAAkkeAALq-cBXzHIzp4NZAdw4BA"}
            ],
            "အာဇာနည် Songs": [
                {"name": "ကိုယ့်အနားရှိစေချင်", "file_id": "CQACAgUAAxkBAAMKaXObVnlhYFsWOGkuDucZW3i9BGEAAo8bAAL9oplXeCtEwYW8JmA4BA"},
                {"name": "လွမ်းစရာရှိလည်း နာစရာနဲ့ဖြေမယ်", "file_id": "CQACAgUAAxkBAAIBEGl7OFEIoSAJixKYX5cokmhJHutyAALEHgACu5bZV7TmbL4_Rb0UOAQ"},
                {"name": "နောက်ဆုံးရင်ခွင်", "file_id": "CQACAgUAAxkBAAIBEml7OF-BgIkfjYBZEPro_W8t-t6qAALFHgACu5bZVyvXb_ZLYlS9OAQ"},
                {"name": "ယဥ်ယဥ်လေးရူး", "file_id": "CQACAgUAAxkBAAIBFGl7OGsxcQqVjm1jKsO-V3O9S80GAALHHgACu5bZVypu8k7yvwEIOAQ"},
                {"name": "ဂနဝင်ဆည်းဆာ", "file_id": "CQACAgUAAxkBAAIBFml7OHTI3aH0XzTlcQPnDffbS-5mAALIHgACu5bZV2-505br3NzXOAQ"},
                {"name": "နေရာ(၂)", "file_id": "CQACAgUAAxkBAAIBGGl7OH38vHSMXnav9VG7cXmdl_L-AALJHgACu5bZVxbYL_4ddyQvOAQ"},
                {"name": "ရွှေလည်တိုင်", "file_id": "CQACAgUAAxkBAAIBGml7OIPQ5uQ1Wd4CXpO41UnOsGv7AALKHgACu5bZV8LBkuf5KAh3OAQ"},
                {"name": "ခွင့်ပြုတယ်", "file_id": "CQACAgUAAxkBAAIBHGl7OIzFe1LQVE3qt4QR1XoXSRDqAALLHgACu5bZVzkd_ttml__mOAQ"},
                {"name": "အသဲကွဲမြို့တော်", "file_id": "CQACAgUAAxkBAAIBHml7OJNLVzsTnNplZWlzbx7kf6_oAALMHgACu5bZV01GgpKqzFwLOAQ"}
            ],
            "Double J Songs": [
                {"name": "WHY", "file_id": "CQACAgUAAxkBAAMMaXOcIKnD4lc5EPswG1ZBZdIopwsAAhYhAAJvFaBX7TREe2bfnWo4BA"},
                {"name": "ခမ်းနားလွန်းတဲ့နေ့", "file_id": "CQACAgUAAxkBAAMUaXOndUxdQiDrpgbQMqkkmoQcT_sAAichAAJvFaBXAW9yBr7b3WM4BA"},
                {"name": "ချစ်လူမိုက်", "file_id": "CQACAgUAAxkBAAIBIml7OwRIF1Hmf-FWKHX1LqMvcq0vAALWHgACu5bZV3j6T0v36fn3OAQ"},
                {"name": "ချယ်ရီ", "file_id": "CQACAgUAAxkBAAIBJGl7OwtVRQVSvyn9dKbye66MhqUhAALXHgACu5bZV7YM8UkQPrhsOAQ"},
                {"name": "တိမ်တိုက်ကဗျာ", "file_id": "CQACAgUAAxkBAAIBJml7OxC5KwVxwWcWhOGg2i6rNV0rAALYHgACu5bZV4uhlkv75Z7UOAQ"},
                {"name": "အမှတ်တစ်မဲ့", "file_id": "CQACAgUAAxkBAAIBKGl7OxXaYQHCUyQ-mrqDGXKGqIzWAALZHgACu5bZVz1UOat5NN-3OAQ"},
                {"name": "ဆောင်း", "file_id": "CQACAgUAAxkBAAIBKml7Ox0rYNF88_OL2hvbPI9FYdRRAALaHgACu5bZV3yfIhtnbcCeOAQ"},
                {"name": "အိမ်ပြန်ချိန်", "file_id": "CQACAgUAAxkBAAIBLGl7OyIxLeVjc_FCywNW95HnMEF0AALbHgACu5bZV6tbH8brTPiCOAQ"}
            ],
            "Raymond Songs": [
                {"name": "ဆေးလိပ်နဲ့မီးချစ်", "file_id": "CQACAgUAAxkBAAMQaXOcdeEoBakGxJ6epQgl0KmTwOgAAhghAAJvFaBXcb4r7Z7mHlk4BA"},
                {"name": "အပါးတော်", "file_id": "CQACAgUAAxkBAAIBMGl7PMM1BlfFHJWrJLzVZ6kTrXO-AALnHgACu5bZVylC-cvkNriuOAQ"},
                {"name": "ငါ့အပြစ်နဲ့ငါ", "file_id": "CQACAgUAAxkBAAIBNWl7PN9eITlXWkIogPoz4fxLoGyUAALoHgACu5bZV1Y7qRNimrZcOAQ"},
                {"name": "တစ်ဆုံတစ်ရာ", "file_id": "CQACAgUAAxkBAAIBN2l7POe25tQ_WKPgPwpnTa3Rkhs3AALpHgACu5bZV7cH6drJ9jkROAQ"},
                {"name": "ဆုလာဘ်", "file_id": "CQACAgUAAxkBAAIBOWl7POsRB3W4skZsRGd3-eDwWWjkAALqHgACu5bZV77KalHAw3svOAQ"},
                {"name": "တစ်ခန်းရပ်", "file_id": "CQACAgUAAxkBAAIBO2l7PPHrClDYaFdGchVLDw8OF7hOAALrHgACu5bZVztpC7c3N4aiOAQ"},
                {"name": "တွေ့ရတာဝန်းသာတယ်", "file_id": "CQACAgUAAxkBAAIBPWl7PP3S1tsi2B2TZEtNHlQu5X4CAALtHgACu5bZV536asjbDwABrzgE"},
                {"name": "မင်းနဲ့ပက်သတ်ရင်", "file_id": "CQACAgUAAxkBAAIBP2l7PQM8Mb-5C6o9Q7F460wlfImeAALuHgACu5bZV20tP57kvE0uOAQ"},
                {"name": "မလိုတော့ဘူး", "file_id": "CQACAgUAAxkBAAIBQWl7PQ6kI0jbeFkykOAS82H6iWbLAALvHgACu5bZVx7Cc0DIjLtMOAQ"},
                {"name": "K", "file_id": "CQACAgUAAxkBAAIBQ2l7PRf8JHR2i5gxf62lVgQY0ZRTAALwHgACu5bZVyXf19A5j9chOAQ"},
                {"name": "မငိုနဲ့တော့", "file_id": "CQACAgUAAxkBAAIBRWl7PR8FKdUUIk19P9vLWO9oao4hAALxHgACu5bZV4d2l97ju2cXOAQ"},
                {"name": "သားကြီးတို့အေးဆေး", "file_id": "CQACAgUAAxkBAAIBR2l7PSbWRoyrGgPpHuHuk-L0xDJiAALyHgACu5bZVwh14Of8UlsoOAQ"},
                {"name": "ချန်ခဲ့", "file_id": "CQACAgUAAxkBAAIBSWl7PTALAquedMdCWNihmXstcunyAALzHgACu5bZV1J03BV91xBWOAQ"},
                {"name": "မင်းနဲ့နီးဖို့", "file_id": "CQACAgUAAxkBAAIBS2l7PTn0KqEcsC0kRLxsS0g1YLSUAAL0HgACu5bZV-RgEfec2kW7OAQ"},
                {"name": "ဘာလိုနေသေးလဲ", "file_id": "CQACAgUAAxkBAAIBTWl7PUjmcIbwES5H91fKbBgFTDt-AAL1HgACu5bZV6tsRJKAZtJbOAQ"},
                {"name": "သုံ့ပန်း", "file_id": "CQACAgUAAxkBAAIBUWl7PWgP1NRhmxi4YQu1GwLdkbVYAAL4HgACu5bZV0pMcK_AAm1GOAQ"},
                {"name": "လိုအပ်မှ", "file_id": "CQACAgUAAxkBAAIBU2l7PW3Et8mbChMmWZtZQVuiWRljAAL5HgACu5bZV93882uaNnbGOAQ"},
                {"name": "ဝမ်းနည်းတတ်တဲ့ချစ်သူ", "file_id": "CQACAgUAAxkBAAIBVWl7PXv6Ia0q-rU-cODFuZl3pwkqAAL7HgACu5bZV-PZKQs_PGpfOAQ"},
                {"name": "သတိရမိလေခြင်း", "file_id": "CQACAgUAAxkBAAIBV2l7PX8fb9uYvv36tOrgFJ8MMzXCAAL8HgACu5bZV-yLME7Jd4CoOAQ"}
            ],
            "ဟန်ထွန်း Songs": [{"name": "ရင်နာတယ်ဧပရယ်", "file_id": "CQACAgUAAxkBAAMSaXOc2SsWc0YqU_vu6xs9R9C_t9UAAhshAAJvFaBXCEUpE_DasYw4BA"}],
            "ဗဒင် Songs": [{"name": "သိုးမည်းတေအကြောင်း", "file_id": "CQACAgUAAxkBAAMOaXOcPMkHREd8b7jY8X0obEvT2tYAAhchAAJvFaBXaa8ZotsvmQo4BA"}],
            "NJ Songs": [{"name": "ဒဿ", "file_id": "CQACAgUAAxkBAAMWaXOoA7eemPmp3lxr_aesCqilD10AAighAAJvFaBXEzakoXUhHDA4BA"}]
        }
    }
}

@bot.message_handler(content_types=['audio'])
def get_file_info(message):
    try:
        user_status = bot.get_chat_member(CH1_ID, message.from_user.id).status
        if user_status in ['administrator', 'creator']:
            f_id = message.audio.file_id
            bot.reply_to(message, f"\u2705 **Admin Mode**\n\n **File ID:** `{f_id}`", parse_mode="Markdown")
    except Exception:
        pass

def show_music_categories(chat_id, message_id=None):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("\U0001F1F2\U0001F1F2 Myanmar Songs", callback_data="cat_myanmar"),
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
        btn_join1 = types.InlineKeyboardButton("\U0001F4E2 Channel 1 Join ရန်", url="https://t.me/raw_myid_hack_channel")
        btn_join2 = types.InlineKeyboardButton("\U0001F4E2 Channel 2 Join ရန်", url="https://t.me/JoKeR_FaN1")
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
        bot.edit_message_text(f"\U0001F3A4 **{SONG_DATA[cat_key]['title']}**\n\nကိုယ်နားထောင်ချင်တဲ့ အဆိုတော်နာမည် ကိုရွေးပေးပါ ခင်ဗျာ", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("singer_"):
        _, cat_key, singer_name = call.data.split("_")
        songs = SONG_DATA[cat_key]["singers"][singer_name]
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

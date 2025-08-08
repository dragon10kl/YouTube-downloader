from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
import requests

TOKEN = "8401609150:AAHjC52VuxuFC8CUGOmB9vbDyWNX6x5DxPQ"

YTMP3_API = "https://apis.davidcyriltech.my.id/download/ytmp3?url="
YTMP4_API = "https://apis.davidcyriltech.my.id/download/ytmp4?url="

user_requests = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text("ഹായ്! YouTube ലിങ്ക് അയയ്ക്കൂ 🎥")

def handle_link(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.effective_chat.id

    if "youtube.com" in text or "youtu.be" in text:
        user_requests[chat_id] = text
        keyboard = [
            [
                InlineKeyboardButton("🎵 MP3 ആകട്ടെ", callback_data="mp3"),
                InlineKeyboardButton("🎬 MP4 ആകട്ടെ", callback_data="mp4")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("താഴെയുള്ളതിൽ ഒന്നിനൊന്ന് തിരഞ്ഞെടുക്കൂ:", reply_markup=reply_markup)
    else:
        update.message.reply_text("⚠️ ശരിയായ YouTube ലിങ്ക് അയക്കൂ.")

def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    video_url = user_requests.get(chat_id)

    query.answer()
    if not video_url:
        query.edit_message_text("⚠️ YouTube ലിങ്ക് കാണുന്നില്ല.")
        return

    query.edit_message_text("🔄 ഡൗൺലോഡ് ചെയ്യുന്നു...")

    try:
        if query.data == "mp3":
            res = requests.get(YTMP3_API + video_url).json()
            link_type = "MP3"
        else:
            res = requests.get(YTMP4_API + video_url).json()
            link_type = "MP4"

        if res.get("status") and res.get("result"):
            result = res["result"]
            title = result.get("title", "Video")
            download_url = result.get("url")

            if query.data == "mp3":
                context.bot.send_audio(chat_id=chat_id, audio=download_url, caption=f"🎵 {title}")
            else:
                context.bot.send_video(chat_id=chat_id, video=download_url, caption=f"🎬 {title}")
        else:
            context.bot.send_message(chat_id=chat_id, text=f"⚠️ {link_type} ഡൗൺലോഡ് ചെയ്യാനായില്ല.")
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text=f"❌ പിഴവ്: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_link))
    dp.add_handler(CallbackQueryHandler(button_click))

    print("🤖 Bot ഓൺ ആയി ✅")
    updater.start_polling()
    updater.idle()

if name == 'main':
    main()
        await context.bot.send_message(chat_id=chat_id, text=f"❌ പിഴവ്: {e}")

# Bot setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.add_handler(CallbackQueryHandler(button_click))

print("🤖 YouTube Downloader Bot MP3/MP4 mode ൽ പ്രവർത്തിക്കുന്നു ✅")
app.run_polling()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, MessageHandler,
    ContextTypes, filters
)
import requests

TOKEN = "8401609150:AAHjC52VuxuFC8CUGOmB9vbDyWNX6x5DxPQ"

YTMP3_API = "https://apis.davidcyriltech.my.id/download/ytmp3?url="
YTMP4_API = "https://apis.davidcyriltech.my.id/download/ytmp4?url="

# Dictionary to temporarily hold user video URLs
user_requests = {}

# Step 1: When a user sends a YouTube link
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "youtube.com" in text or "youtu.be" in text:
        chat_id = update.effective_chat.id
        user_requests[chat_id] = text

        keyboard = [
            [
                InlineKeyboardButton("🎵 MP3 ആകട്ടെ", callback_data="mp3"),
                InlineKeyboardButton("🎬 MP4 ആകട്ടെ", callback_data="mp4")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("താഴെതൽ ഐച്ഛികം തിരഞ്ഞെടുക്കൂ:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("⚠️ ശരിയായ YouTube ലിങ്ക് അയക്കൂ.")

# Step 2: When user selects MP3 or MP4
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat.id
    video_url = user_requests.get(chat_id)

    if not video_url:
        await query.edit_message_text("⚠️ നേരത്തെ ലിങ്ക് ഇല്ല!")
        return

    await query.edit_message_text("🔄 ഡൗൺലോഡ് ചെയ്യുന്നു...")

    try:
        if query.data == "mp3":
            res = requests.get(YTMP3_API + video_url).json()
            format_name = "MP3"
        else:
            res = requests.get(YTMP4_API + video_url).json()
            format_name = "MP4"

        if res.get("status") and res.get("result"):
            result = res["result"]
            title = result.get("title", "Video")
            download_url = result.get("url")

            if query.data == "mp3":
                await context.bot.send_audio(chat_id=chat_id, audio=download_url, caption=f"🎵 {title}")
            else:
                await context.bot.send_video(chat_id=chat_id, video=download_url, caption=f"🎬 {title}")
        else:
            await context.bot.send_message(chat_id=chat_id, text=f"⚠️ {format_name} ഡൗൺലോഡ് ചെയ്യാനായില്ല.")
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"❌ പിഴവ്: {e}")

# Bot setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.add_handler(CallbackQueryHandler(button_click))

print("🤖 YouTube Downloader Bot MP3/MP4 mode ൽ പ്രവർത്തിക്കുന്നു ✅")
app.run_polling()

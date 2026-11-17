import os, secrets, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]
PUBLIC_BASE_URL = os.environ["PUBLIC_BASE_URL"].rstrip("/")
app = Flask(__name__)
SESSIONS = {}  # session_id -> Telegram chat_id; in-memory starter implementation

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    sid = secrets.token_urlsafe(24)
    SESSIONS[sid] = chat_id
    link = f"{PUBLIC_BASE_URL}/capture/{sid}"
    await update.message.reply_text(
        "أهلاً! شارك الرابط مع شخص إذا كان موافقاً على التصوير والإرسال. "
        "لن تعمل الكاميرا إلا بعد أن يفتح الصفحة ويضغط سماح، "
        "ويختار بنفسه التقاط صورة أو تسجيل فيديو ثم إرسال الملف.\n\n"
        f"رابط جلسة التصوير:\n{link}"
    )

def run_web():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))

if __name__ == "__main__":
    from webapp import register_routes
    register_routes(app, SESSIONS)
    threading.Thread(target=run_web, daemon=True).start()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

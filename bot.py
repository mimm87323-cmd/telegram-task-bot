import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from supabase import create_client
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Environment variables
TOKEN = os.environ.get("BOT_TOKEN")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Supabase init
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Simple Dummy Web Server to satisfy Render's port check
class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

    def log_message(self, format, *args):
        return

def start_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), WebServerHandler)
    server.serve_forever()

# Telegram Bot Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        supabase.table("users").upsert(
            {
                "telegram_id": user.id,
                "username": user.username or ""
            },
            on_conflict="telegram_id"
        ).execute()
    except Exception as e:
        print("Database Save Error:", e)

    keyboard = [
        ["📋 কাজ দেখুন", "📤 কাজ জমা দিন"],
        ["💰 আমার ব্যালেন্স", "💸 Withdraw"],
        ["👥 Referral", "📊 আমার হিসাব"],
        ["📞 Support"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "🤖 স্বাগতম!\n\nTask Bot-এ আপনাকে স্বাগতম।\nনিচের Menu থেকে একটি অপশন নির্বাচন করুন 👇",
        reply_markup=reply_markup
    )

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📋 কাজ দেখুন":
        await update.message.reply_text("📋 বর্তমানে কোনো কাজ যোগ করা হয়নি।")
    elif text == "📤 কাজ জমা দিন":
        await update.message.reply_text("📤 কাজ জমা দেওয়ার সিস্টেম শিগগিরই চালু হবে।")
    elif text == "💰 আমার ব্যালেন্স":
        await update.message.reply_text("💰 আপনার ব্যালেন্স: ৳0.00")
    elif text == "💸 Withdraw":
        await update.message.reply_text("💸 Withdraw সিস্টেম শিগগিরই চালু হবে।")
    elif text == "👥 Referral":
        await update.message.reply_text("👥 Referral সিস্টেম শিগগিরই চালু হবে।")
    elif text == "📊 আমার হিসাব":
        await update.message.reply_text("📊 আপনার হিসাব শিগগিরই দেখানো হবে।")
    elif text == "📞 Support":
        await update.message.reply_text("📞 Support: Admin-এর সাথে যোগাযোগ করুন।")

if __name__ == "__main__":
    # Start web server in background thread
    Thread(target=start_web_server, daemon=True).start()
    
    # Start Telegram Bot
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))
    
    print("Bot is running successfully...")
    app.run_polling()

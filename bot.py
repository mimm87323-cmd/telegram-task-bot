import os
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
from supabase import create_client

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.environ.get("BOT_TOKEN")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Initialize Supabase Client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📋 কাজ দেখুন", "📤 কাজ জমা দিন"],
        ["💰 আমার ব্যালেন্স", "💸 Withdraw"],
        ["👥 Referral", "📊 আমার হিসাব"],
        ["📞 Support"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "🤖 স্বাগতম!\n\n"
        "🎯 Task Bot-এ আপনাকে স্বাগতম।\n"
        "নিচের Menu থেকে একটি অপশন নির্বাচন করুন 👇",
        reply_markup=reply_markup
    )


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📋 কাজ দেখুন":
        await update.message.reply_text(
            "📋 বর্তমানে কোনো কাজ যোগ করা হয়নি।\n\n"
            "Admin Panel থেকে কাজ যোগ করলে এখানে দেখা যাবে।"
        )

    elif text == "📤 কাজ জমা দিন":
        await update.message.reply_text(
            "📤 কাজ জমা দেওয়ার সিস্টেম শিগগিরই চালু হবে।"
        )

    elif text == "💰 আমার ব্যালেন্স":
        await update.message.reply_text(
            "💰 আপনার ব্যালেন্স: ৳0.00"
        )

    elif text == "💸 Withdraw":
        await update.message.reply_text(
            "💸 Withdraw সিস্টেম শিগগিরই চালু হবে।"
        )

    elif text == "👥 Referral":
        await update.message.reply_text(
            "👥 Referral সিস্টেম শিগগিরই চালু হবে।"
        )

    elif text == "📊 আমার হিসাব":
        await update.message.reply_text(
            "📊 আপনার হিসাব শিগগিরই দেখানো হবে।"
        )

    elif text == "📞 Support":
        await update.message.reply_text(
            "📞 Support\n\n"
            "সমস্যা হলে Admin-এর সাথে যোগাযোগ করুন।"
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler)
)


def run_server():
    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running")

        def log_message(self, format, *args):
            pass

    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()


Thread(target=run_server, daemon=True).start()

print("Bot is running...")
app.run_polling()

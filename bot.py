import os
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8869494633:AAFTi9UySlNxXkjDCY7NR81dFHT4-2EoYP0" # আপনার মূল টোকেনটি কোটেশনের ভেতরে বসাবেন

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 স্বাগত!\n\n"
        "আমাদের Task Bot শিগগিরই প্রস্তুত হচ্ছে।"
    )

app = (
    Application.builder().token(TOKEN).build()
)
app.add_handler(CommandHandler("start", start))

print("Bot is running...")

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

app.run_polling()

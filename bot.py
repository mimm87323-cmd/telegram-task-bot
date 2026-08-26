from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8869494633:AAFTi9UySlNxXkjDCY7NR81dFHT4-2EoYP0"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 স্বাগতম!\n\n"
        "আমাদের Task Bot শিগগিরই প্রস্তুত হচ্ছে।"
    )

app = (
    Application.builder().token(TOKEN).build()
)
app.add_handler(CommandHandler("start", start))

print("Bot is running...")

app.run_polling()

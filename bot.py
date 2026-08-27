import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

from supabase import create_client
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)


# ==========================================
# ENVIRONMENT VARIABLES
# ==========================================

TOKEN = os.environ.get("BOT_TOKEN")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")


# ==========================================
# SUPABASE
# ==========================================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ==========================================
# RENDER WEB SERVER
# ==========================================

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header(
            "Content-type",
            "text/html"
        )

        self.end_headers()

        self.wfile.write(
            b"Bot is alive!"
        )

    def log_message(self, format, *args):
        return


def start_web_server():

    port = int(
        os.environ.get(
            "PORT",
            8080
        )
    )

    server = HTTPServer(
        ("0.0.0.0", port),
        WebServerHandler
    )

    server.serve_forever()


# ==========================================
# START COMMAND
# ==========================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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

        print(
            "Database Save Error:",
            e
        )


    keyboard = [

        [
            "📋 কাজ দেখুন",
            "📤 কাজ জমা দিন"
        ],

        [
            "💰 আমার ব্যালেন্স",
            "💸 Withdraw"
        ],

        [
            "👥 Referral",
            "📊 আমার হিসাব"
        ],

        [
            "📞 Support"
        ]

    ]


    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


    await update.message.reply_text(

        "🤖 স্বাগতম!\n\n"
        "Task Bot-এ আপনাকে স্বাগতম।\n"
        "নিচের Menu থেকে একটি অপশন নির্বাচন করুন 👇",

        reply_markup=reply_markup
    )


# ==========================================
# SHOW ACTIVE TASKS
# ==========================================

async def show_tasks(update: Update):

    try:

        response = (
            supabase
            .table("tasks")
            .select(
                "id,title,description,reward,status"
            )
            .eq(
                "status",
                "active"
            )
            .order(
                "id",
                desc=True
            )
            .execute()
        )


        tasks = response.data


        if not tasks:

            await update.message.reply_text(
                "📋 বর্তমানে কোনো Active কাজ নেই।\n\n"
                "Admin নতুন কাজ যোগ করলে এখানে দেখা যাবে।"
            )

            return


        message_parts = []

        message_parts.append(
            "📋 <b>বর্তমান কাজগুলো:</b>\n"
        )


        for task in tasks:

            title = task.get(
                "title",
                "Untitled"
            )

            description = task.get(
                "description",
                ""
            )

            reward = task.get(
                "reward",
                0
            )


            task_text = (

                f"🆔 Task ID: <b>{task['id']}</b>\n"

                f"📌 <b>{title}</b>\n"

                f"📝 {description}\n"

                f"💰 Reward: <b>৳{reward}</b>\n"

                "━━━━━━━━━━━━━━"

            )


            message_parts.append(
                task_text
            )


        full_message = "\n\n".join(
            message_parts
        )


        # Telegram message too long হলে ভাগ করে পাঠানো
        max_length = 4000

        for i in range(
            0,
            len(full_message),
            max_length
        ):

            await update.message.reply_text(
                full_message[i:i + max_length],
                parse_mode="HTML"
            )


    except Exception as e:

        print(
            "Task Load Error:",
            e
        )

        await update.message.reply_text(
            "❌ কাজগুলো লোড করতে সমস্যা হয়েছে।"
        )


# ==========================================
# MENU HANDLER
# ==========================================

async def menu_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text


    # --------------------------------------
    # TASKS
    # --------------------------------------

    if text == "📋 কাজ দেখুন":

        await show_tasks(
            update
        )


    # --------------------------------------
    # SUBMISSION
    # --------------------------------------

    elif text == "📤 কাজ জমা দিন":

        await update.message.reply_text(

            "📤 <b>কাজ জমা দিন</b>\n\n"

            "এই সিস্টেমটি পরের ধাপে চালু করা হবে।",

            parse_mode="HTML"
        )


    # --------------------------------------
    # BALANCE
    # --------------------------------------

    elif text == "💰 আমার ব্যালেন্স":

        user = update.effective_user

        try:

            response = (
                supabase
                .table("users")
                .select("balance")
                .eq(
                    "telegram_id",
                    user.id
                )
                .single()
                .execute()
            )


            balance = (
                response.data.get(
                    "balance",
                    0
                )
                if response.data
                else 0
            )


            await update.message.reply_text(

                f"💰 আপনার বর্তমান ব্যালেন্স:\n\n"
                f"৳{balance:.2f}"

            )


        except Exception as e:

            print(
                "Balance Error:",
                e
            )

            await update.message.reply_text(
                "❌ ব্যালেন্স দেখা যাচ্ছে না।"
            )


    # --------------------------------------
    # WITHDRAW
    # --------------------------------------

    elif text == "💸 Withdraw":

        await update.message.reply_text(

            "💸 <b>Withdraw</b>\n\n"

            "Withdraw system পরের ধাপে চালু করা হবে।",

            parse_mode="HTML"
        )


    # --------------------------------------
    # REFERRAL
    # --------------------------------------

    elif text == "👥 Referral":

        await update.message.reply_text(

            "👥 <b>Referral</b>\n\n"

            "Referral system পরের ধাপে চালু করা হবে।",

            parse_mode="HTML"
        )


    # --------------------------------------
    # ACCOUNT
    # --------------------------------------

    elif text == "📊 আমার হিসাব":

        user = update.effective_user

        try:

            response = (
                supabase
                .table("users")
                .select(
                    "telegram_id,username,balance"
                )
                .eq(
                    "telegram_id",
                    user.id
                )
                .single()
                .execute()
            )


            data = response.data


            if data:

                username = (
                    data.get(
                        "username"
                    )
                    or "নেই"
                )

                balance = data.get(
                    "balance",
                    0
                )


                await update.message.reply_text(

                    "📊 <b>আমার হিসাব</b>\n\n"

                    f"👤 Username: @{username}\n"

                    f"🆔 Telegram ID: "
                    f"{data.get('telegram_id')}\n"

                    f"💰 Balance: ৳{balance}",

                    parse_mode="HTML"
                )


            else:

                await update.message.reply_text(
                    "❌ আপনার তথ্য পাওয়া যায়নি।"
                )


        except Exception as e:

            print(
                "Account Error:",
                e
            )

            await update.message.reply_text(
                "❌ তথ্য লোড করতে সমস্যা হয়েছে।"
            )


    # --------------------------------------
    # SUPPORT
    # --------------------------------------

    elif text == "📞 Support":

        await update.message.reply_text(

            "📞 <b>Support</b>\n\n"

            "Admin-এর সাথে যোগাযোগ করুন।",

            parse_mode="HTML"
        )


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    Thread(
        target=start_web_server,
        daemon=True
    ).start()


    app = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            menu_handler
        )
    )


    print(
        "Bot is running successfully..."
    )


    app.run_polling()

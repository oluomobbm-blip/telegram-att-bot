import nest_asyncio
nest_asyncio.apply()
import asyncio
from telegram import Update, BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import re

# List of valid AT&T-related domains
ATT_DOMAINS = [
    'sbcglobal.net', 'bellsouth.net', 'ameritech.net', 'prodigy.net',
    'flash.net', 'nvbell.net', 'pacbell.net', 'swbell.net',
    'snet.net', 'wans.net', 'att.net'
]

def is_valid_att_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@(' + '|'.join(re.escape(domain) for domain in ATT_DOMAINS) + r')$'
    return re.match(pattern, email)

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to the AT&T Email Validator Bot!\n\n"
        "Send me an email and I’ll tell you if it belongs to an AT&T-supported domain."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 How to Use:\n"
        "Just send any email address and I’ll check if it’s from a valid AT&T domain like:\n"
        "📧 sbcglobal.net, bellsouth.net, att.net, etc."
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ About this bot:\n"
        "This bot checks whether an email belongs to one of AT&T’s legacy email domains.\n"
        "Built with Python and Telegram Bot API."
    )

# --- Message handler for email checking ---

async def check_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text.strip()
    if is_valid_att_email(email):
        await update.message.reply_text(f"✅ {email} is a valid AT&T email domain.")
    else:
        await update.message.reply_text(f"❌ {email} is not recognized as an AT&T email address.")

# --- Main Function ---

async def main():
    TOKEN = "8360699343:AAGD2Uk7yu7dNiX22lgK0HhX_UML6FVVCsI"  # Replace with your real bot token
    app = ApplicationBuilder().token(TOKEN).build()

    # Set command buttons
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "How to use the bot"),
        BotCommand("about", "What this bot does")
    ]
    await app.bot.set_my_commands(commands)

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_email))

    print("🚀 Bot is running...")
    await app.run_polling()

# --- Run the Bot ---

if __name__ == "__main__":
    import asyncio
    asyncio.get_event_loop().run_until_complete(main())

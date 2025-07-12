from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from config.settings import BOT_USERNAME

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.full_name or update.effective_user.username
    welcome = (
        f"Hi, <b>{username}</b>!\n"
        "I'm your Super Bot. Let's make something great together!\n\n"
        "Join our Channel: https://t.me/dbgm001"
    )
    await update.message.reply_text(welcome, parse_mode='HTML')
    await menu_command(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Try typing any of these keywords: help, products, menu...")

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛍️ View Products", url="https://form.jotform.com/240791552407053")],
        [InlineKeyboardButton("🌐 Visit Website", url="https://dbgaming.com/Games")],
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/dbgm001")]
    ]
    await update.message.reply_text("🏠 Here's our main menu:", reply_markup=InlineKeyboardMarkup(keyboard))

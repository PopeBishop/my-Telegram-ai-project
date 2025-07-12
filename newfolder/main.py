import logging
import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, MessageEntity
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from data.data import KEYWORDS, RESPONSES, get_time_based_greeting
from data.data import RESPONSES

load_dotenv()
# --- Config ---
TOKEN = os.environ['TELEGRAM_TOKEN']
BOT_USERNAME = os.environ['BOT_USERNAME']

# --- Logging Setup ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- Match Keywords ---
def match_keyword(text: str):
    for intent, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:  # partial match
                return intent
    return None

# --- /start Command ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username or update.effective_user.full_name
    welcome = (
        f"Hi, <b>{username}</b>!\n"
        "I'm your Super Bot.\n"
        "We're glad to have you here. Let's make something great together!\n\n"
        "Join our Channel to get the latest gaming updates:\n"
        "https://t.me/dbgm001"
    )
    await update.message.reply_text(welcome, parse_mode='HTML')
    await menu_command(update, context)

# --- /help Command ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(RESPONSES["help"], parse_mode='HTML')
    await menu_command(update, context)

# --- /menu Command ---
async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🛍️ Products", url="https://form.jotform.com/240791552407053"),
            InlineKeyboardButton("📦 Telegram View", url="https://t.me/RexSuper_Bot/ahhhasdyyad"),
        ],
        [InlineKeyboardButton("🌐 Visit Website", url="https://dbgaming.com/Games")],
        [InlineKeyboardButton("📢 Join Our Channel", url="https://t.me/dbgm001")]
    ]
    await update.message.reply_text("🏠 Here's our main menu. Feel free to explore!",
                                    reply_markup=InlineKeyboardMarkup(keyboard))

# --- Text Handler ---
async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username or update.effective_user.full_name
    text = update.message.text.lower()
    logging.info(f"User ({username}) said: {text}")
    chat_type = update.message.chat.type

# Check if the bot was mentioned

    mentioned = False
    if "bot" in text:
        mentioned = True

    mentioned = "bot" in text
    if update.message.entities:
        for entity in update.message.entities:
            if entity.type == MessageEntity.MENTION:
                mention_text = text[entity.offset:entity.offset + entity.length]
                if mention_text.lower() == BOT_USERNAME.lower():
                    mentioned = True
                    break

# --- Detect if replying to bot's message ---
    replied_to_bot = False
    if update.message.reply_to_message:
        replied_user = update.message.reply_to_message.from_user
        if replied_user and replied_user.username and f"@{replied_user.username}".lower() == BOT_USERNAME.lower():
            replied_to_bot = True

    # Match keyword regardless of mention
    matched_intent = match_keyword(text)
    logging.info(f"[DEBUG] Matched intent: {matched_intent}")

    async def respond(intent):
        response = RESPONSES.get(intent)
        if response:
            if callable(response):
                text = response()
                keyboard = None
            elif isinstance(response, dict):
                text_func = response.get("text")
                if callable(text_func):
                    # Special case for "greet" to pass username
                    if intent == "greet":
                        text = text_func(username)
                    else:
                        text = text_func()
                else:
                    text = text_func
                keyboard = response.get("keyboard")

            await update.message.reply_text(text, reply_markup=keyboard, parse_mode='HTML')
        else:
            await update.message.reply_text("🧐 I heard you, but I'm not sure how to respond.")
            await update.message.reply_text("Try saying 'help' or 'menu'.")

        await menu_command(update, context)

    if chat_type == "private":
        if matched_intent:
            await respond(matched_intent)
        else:
            await update.message.reply_text("🤖 I'm here, but I didn't understand. Try saying 'help' or 'menu'.")
            await menu_command(update, context)

    elif chat_type in ["group", "supergroup"]:
        if mentioned or replied_to_bot:
            if matched_intent:
                await respond(matched_intent)
            else:
                await update.message.reply_text("🤖 I'm here, but I didn't understand. Try saying 'help' or 'menu'.")
                await menu_command(update, context)

# --- Error Handler ---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.error(msg="Exception occurred:", exc_info=context.error)
    if update and hasattr(update, "message"):
        await update.message.reply_text("⚠️ Something went wrong. Please try again.")

# --- Main Bot ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('menu', menu_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))
    app.add_error_handler(error_handler)

    print("🤖 Bot is running...")
    app.run_polling(poll_interval=5)

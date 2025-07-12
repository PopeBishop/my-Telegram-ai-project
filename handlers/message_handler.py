import logging
from telegram import Update, MessageEntity
from telegram.ext import ContextTypes
from logic.response_logic import match_keyword, build_response
from config.settings import BOT_USERNAME
from handlers.commands import menu_command

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.full_name or update.effective_user.username
    text = update.message.text.lower()
    chat_type = update.message.chat.type

    mentioned = "bot" in text or any(
        entity.type == MessageEntity.MENTION and
        text[entity.offset:entity.offset + entity.length].lower() == BOT_USERNAME.lower()
        for entity in update.message.entities or []
    )

    replied_to_bot = (
        update.message.reply_to_message and
        update.message.reply_to_message.from_user.id == context.bot.id
    )

    matched_intent = match_keyword(text)
    logging.info(f"[DEBUG] Matched intent: {matched_intent}")

    if chat_type == "private" or (chat_type in ["group", "supergroup"] and (mentioned or replied_to_bot)):
        if matched_intent:
            reply_text, keyboard = build_response(matched_intent, username)
            await update.message.reply_text(reply_text, reply_markup=keyboard, parse_mode='HTML')
        else:
            await update.message.reply_text("🤖 I didn't understand. Try saying 'help' or 'menu'.")
        await menu_command(update, context)
    else:
        logging.info("❌ Ignored message — not private, no mention, no reply to bot.")


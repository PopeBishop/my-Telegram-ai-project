import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config.settings import TOKEN
from handlers.commands import start_command, help_command, menu_command
from handlers.message_handler import handle_response

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))

    print("🤖 Bot is running...")
    app.run_polling(poll_interval=5)
# data.py
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_time_based_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "🌅 Good morning!"
    elif 12 <= hour < 18:
        return "🌞 Good afternoon!"
    elif 18 <= hour < 22:
        return "🌇 Good evening!"
    else:
        return "🌙 Hello, night owl!"

KEYWORDS = {
    "help": ["help", "support", "assist", "problem", "issue", "trouble", "guide", "how to use"],
    "mood": ["how are you", "how's it going", "are you ok", "what's up", "how do you feel"],
    "products": ["product", "shop", "buy", "order", "catalog", "store", "purchase", "merch", "items", "game bundle"],
    "menu": ["menu", "options", "start", "get started", "show menu", "begin", "home"],
    "website": ["website", "web", "site", "visit site", "see website", "open site"],
    "channel": ["channel", "join", "telegram channel", "group", "broadcast", "news"],
    "goodbye": ["bye", "goodbye", "see you", "later", "take care", "farewell"],
    "thanks": ["thanks", "thank you", "appreciate", "thx", "ty", "tnx"],
    "greet": ["hello", "hi", "hey", "low", "yo", "sup", "good morning", "good afternoon", "good evening"]
}

INLINE_KEYBOARDS = {
    "products": InlineKeyboardMarkup([
        [InlineKeyboardButton("🛍️ View Products", url="https://form.jotform.com/240791552407053")],
        [InlineKeyboardButton("📦 Telegram View", url="https://t.me/RexSuper_Bot/ahhhasdyyad")]
    ]),
    "channel": InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/dbgm001")]
    ]),
    "website": InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Visit Website", url="https://dbgaming.com/Games")]
    ]),
    "menu": InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Open Menu", callback_data="menu")]
    ]),
    "help": InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Channel", url="https://t.me/dbgm001")]
    ])
}


RESPONSES = {
    "help": {
        "text": "Need help? You can try /menu or visit our channel \n"
        "https://t.me/dbgm001.",
        "keyboard": INLINE_KEYBOARDS["help"]
    },
    "products": {
        "text": "🛍️ Check out our products below:",
        "keyboard": INLINE_KEYBOARDS["products"]
    },
    "website": {
        "text": "🌐 Visit our website:",
        "keyboard": INLINE_KEYBOARDS["website"]
    },
    "channel": {
        "text": "📢 Join our Telegram channel:",
        "keyboard": INLINE_KEYBOARDS["channel"]
    },
    "goodbye": "👋 See you soon!",
    "thanks": "🙏 You're welcome!",
    "greet": {
        "text": lambda username: f"{get_time_based_greeting()} {username}!",
    }
}

#!/usr/bin/env python3
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
import json
import os
import threading
import random
import re
from datetime import datetime
from flask import Flask
import asyncio

# ============================================================
# FLASK APP (Render Health Check)
# ============================================================
flask_app = Flask(__name__)

@flask_app.route('/')
@flask_app.route('/health')
def health():
    return "✅ Bot is running!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# ============================================================
# LOGGING
# ============================================================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
OWNER_ID = int(os.environ.get("OWNER_ID", 8586849798))

# ============================================================
# STYLISH CHARACTERS
# ============================================================
STYLISH = {
    'A': '𝙰', 'B': '𝙱', 'C': '𝙲', 'D': '𝙳', 'E': '𝙴', 'F': '𝙵', 'G': '𝙶',
    'H': '𝙷', 'I': '𝙸', 'J': '𝙹', 'K': '𝙺', 'L': '𝙻', 'M': '𝙼', 'N': '𝙽',
    'O': '𝙾', 'P': '𝙿', 'Q': '𝚀', 'R': '𝚁', 'S': '𝚂', 'T': '𝚃', 'U': '𝚄',
    'V': '𝚅', 'W': '𝚆', 'X': '𝚇', 'Y': '𝚈', 'Z': '𝚉',
    'a': '𝚊', 'b': '𝚋', 'c': '𝚌', 'd': '𝚍', 'e': '𝚎', 'f': '𝚏',
    'g': '𝚐', 'h': '𝚑', 'i': '𝚒', 'j': '𝚓', 'k': '𝚔', 'l': '𝚕',
    'm': '𝚖', 'n': '𝚗', 'o': '𝚘', 'p': '𝚙', 'q': '𝚚', 'r': '𝚛',
    's': '𝚜', 't': '𝚝', 'u': '𝚞', 'v': '𝚟', 'w': '𝚠', 'x': '𝚡',
    'y': '𝚢', 'z': '𝚣',
    '0': '𝟶', '1': '𝟷', '2': '𝟸', '3': '𝟹', '4': '𝟺',
    '5': '𝟻', '6': '𝟼', '7': '𝟽', '8': '𝟾', '9': '𝟿'
}

def stylish(text):
    """Convert normal text to stylish characters"""
    return ''.join(STYLISH.get(c, c) for c in text)

# ============================================================
# PREMIUM EMOJIS
# ============================================================
PREMIUM_EMOJIS = {
    "verified": {"id": "6147565374289220368", "fallback": "✅"},
    "flex": {"id": "6147464060305676048", "fallback": "😎"},
    "blue_verification": {"id": "6147524086768604985", "fallback": "💎"},
    "frozen": {"id": "5449449325434266744", "fallback": "❄️"},
    "crying": {"id": "6273840152980755328", "fallback": "😭"},
    "smiling": {"id": "6276057176444246654", "fallback": "🙂"},
    "seeing_up": {"id": "6273997026661241933", "fallback": "😋"},
    "teeth": {"id": "6273726078649372769", "fallback": "😁"},
    "done": {"id": "6274007313107915274", "fallback": "👍"},
    "blue_badge": {"id": "5978776771623914876", "fallback": "🟫"},
    "black_badge": {"id": "5978686323907628843", "fallback": "🔸"},
    "busy_tag": {"id": "5852873584912896283", "fallback": "🟧"},
    "instagram": {"id": "5895297528106061174", "fallback": "🌐"},
    "telegram": {"id": "5895735846698487922", "fallback": "🌐"},
    "whatsapp": {"id": "5895343514320899727", "fallback": "🌐"},
    "india": {"id": "5913754823643107921", "fallback": "🇮🇳"},
    "dollar": {"id": "5197434882321567830", "fallback": "💵"},
    "top": {"id": "5463071033256848094", "fallback": "🔝"},
    "bro": {"id": "5463256910851546817", "fallback": "🤝"},
    "yes": {"id": "5463423955014529788", "fallback": "👌"},
    "lock": {"id": "5465443379917629504", "fallback": "🔓"},
    "good": {"id": "5465465194056525619", "fallback": "👍"},
    "sigma": {"id": "6235620067942341623", "fallback": "🥃"},
    "don": {"id": "6235717714023814969", "fallback": "🍂"},
    "skills": {"id": "6235593671073339928", "fallback": "💀"},
    "heart": {"id": "6147617184479711380", "fallback": "❤️‍🔥"},
    "stars": {"id": "6235403472741603087", "fallback": "⭐"},
    "github": {"id": "5346181118884331907", "fallback": "📱"},
    "motion": {"id": "5971944878815317190", "fallback": "💠"},
    "fire": {"id": "6147524086768604985", "fallback": "🔥"},
    "crown": {"id": "6147565374289220368", "fallback": "👑"},
    "rocket": {"id": "6147464060305676048", "fallback": "🚀"},
    "lightning": {"id": "5971944878815317190", "fallback": "⚡"},
    "cross": {"id": "6273840152980755328", "fallback": "❌"},
    "check": {"id": "6274007313107915274", "fallback": "✔️"},
    "warning": {"id": "5852873584912896283", "fallback": "⚠️"},
    "target": {"id": "6273997026661241933", "fallback": "🎯"},
    "trophy": {"id": "6235620067942341623", "fallback": "🏆"},
    "gem": {"id": "6147524086768604985", "fallback": "💎"},
    "shield": {"id": "5449449325434266744", "fallback": "🛡️"},
    "game": {"id": "5895297528106061174", "fallback": "🎮"},
    "money": {"id": "5197434882321567830", "fallback": "💰"},
    "dice_emoji": {"id": "6147464060305676048", "fallback": "🎲"},
    "coin": {"id": "6147617184479711380", "fallback": "🪙"},
    "sparkles": {"id": "6235403472741603087", "fallback": "✨"},
}

def get_emoji_html(name):
    if name in PREMIUM_EMOJIS:
        data = PREMIUM_EMOJIS[name]
        return f'<tg-emoji emoji-id="{data["id"]}">{data["fallback"]}</tg-emoji>'
    return ""

def e(name):
    return get_emoji_html(name)

def get_random_emojis(count=2):
    """Get random premium emojis"""
    names = list(PREMIUM_EMOJIS.keys())
    if not names:
        return ["", ""]
    selected = random.sample(names, min(count, len(names)))
    return [e(name) for name in selected]

def format_with_emojis(text):
    """Har line ke aage-piche premium emoji + stylish characters"""
    lines = text.split('\n')
    result = []
    for line in lines:
        if line.strip():
            left, right = get_random_emojis(2)
            # Stylish characters apply karo
            styled_line = stylish(line)
            result.append(f"{left} {styled_line} {right}")
        else:
            result.append(line)
    return '\n'.join(result)

# ============================================================
# FORCE STORAGE
# ============================================================
FORCE_FILE = "force.json"

def load_force():
    try:
        if os.path.exists(FORCE_FILE):
            with open(FORCE_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {"dice": None, "coin": None}

def save_force(data):
    try:
        with open(FORCE_FILE, 'w') as f:
            json.dump(data, f)
    except:
        pass

# ============================================================
# ADMINS STORAGE
# ============================================================
ADMINS_FILE = "admins.json"

def load_admins():
    try:
        if os.path.exists(ADMINS_FILE):
            with open(ADMINS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return [OWNER_ID]

def save_admins(admins):
    try:
        with open(ADMINS_FILE, 'w') as f:
            json.dump(admins, f)
    except:
        pass

# ============================================================
# USER STORAGE
# ============================================================
USERS_FILE = "users.json"

def load_users():
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_users(users):
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f)
    except:
        pass

# ============================================================
# /dice COMMAND
# ============================================================
async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Group admin check
    if update.effective_chat.type in ['group', 'supergroup']:
        try:
            chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
            if chat_member.status not in ['administrator', 'creator'] and user_id != OWNER_ID:
                await update.message.reply_text(
                    format_with_emojis("Only group admins can roll dice!"),
                    parse_mode="HTML"
                )
                return
        except:
            pass
    
    force_data = load_force()
    if force_data.get("dice") is not None and (user_id == OWNER_ID or user_id in load_admins()):
        result = force_data["dice"]
        force_data["dice"] = None
        save_force(force_data)
    else:
        result = random.randint(1, 6)
    
    msg = f"""DICE ROLLED
ADMIN - {stylish(update.effective_user.first_name)}

RESULT - {stylish(str(result))}"""
    
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")

# ============================================================
# /flipcoin COMMAND
# ============================================================
async def flipcoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Group admin check
    if update.effective_chat.type in ['group', 'supergroup']:
        try:
            chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
            if chat_member.status not in ['administrator', 'creator'] and user_id != OWNER_ID:
                await update.message.reply_text(
                    format_with_emojis("Only group admins can flip coin!"),
                    parse_mode="HTML"
                )
                return
        except:
            pass
    
    force_data = load_force()
    if force_data.get("coin") is not None and (user_id == OWNER_ID or user_id in load_admins()):
        result = force_data["coin"]
        force_data["coin"] = None
        save_force(force_data)
    else:
        result = random.choice(["HEAD", "TAIL"])
    
    msg = f"""COIN FLIPPED
ADMIN - {stylish(update.effective_user.first_name)}

RESULT - {stylish(result)}"""
    
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")

# ============================================================
# /forcedice COMMAND
# ============================================================
async def forcedice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != OWNER_ID and user_id not in load_admins():
        await update.message.reply_text(
            format_with_emojis("Only owner/admins can force dice!"),
            parse_mode="HTML"
        )
        return
    
    if not context.args:
        await update.message.reply_text(
            format_with_emojis("Usage: /forcedice 1-6"),
            parse_mode="HTML"
        )
        return
    
    try:
        num = int(context.args[0])
        if num < 1 or num > 6:
            await update.message.reply_text(
                format_with_emojis("Number must be between 1 and 6"),
                parse_mode="HTML"
            )
            return
        
        force_data = load_force()
        force_data["dice"] = num
        save_force(force_data)
        
        await update.message.reply_text(
            format_with_emojis(f"Next dice roll will be {stylish(str(num))}!"),
            parse_mode="HTML"
        )
    except:
        await update.message.reply_text(
            format_with_emojis("Invalid number!"),
            parse_mode="HTML"
        )

# ============================================================
# /forcecoin COMMAND
# ============================================================
async def forcecoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != OWNER_ID and user_id not in load_admins():
        await update.message.reply_text(
            format_with_emojis("Only owner/admins can force coin!"),
            parse_mode="HTML"
        )
        return
    
    if not context.args:
        await update.message.reply_text(
            format_with_emojis("Usage: /forcecoin HEAD/TAIL"),
            parse_mode="HTML"
        )
        return
    
    result = context.args[0].upper()
    if result not in ["HEAD", "TAIL"]:
        await update.message.reply_text(
            format_with_emojis("Must be HEAD or TAIL"),
            parse_mode="HTML"
        )
        return
    
    force_data = load_force()
    force_data["coin"] = result
    save_force(force_data)
    
    await update.message.reply_text(
        format_with_emojis(f"Next coin flip will be {stylish(result)}!"),
        parse_mode="HTML"
    )

# ============================================================
# /approve COMMAND
# ============================================================
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != OWNER_ID:
        await update.message.reply_text(
            format_with_emojis("Only owner can approve admins!"),
            parse_mode="HTML"
        )
        return
    
    if not context.args:
        await update.message.reply_text(
            format_with_emojis("Usage: /approve USER_ID"),
            parse_mode="HTML"
        )
        return
    
    try:
        new_admin = int(context.args[0])
        admins = load_admins()
        if new_admin in admins:
            await update.message.reply_text(
                format_with_emojis("Already an admin!"),
                parse_mode="HTML"
            )
            return
        admins.append(new_admin)
        save_admins(admins)
        await update.message.reply_text(
            format_with_emojis(f"User {stylish(str(new_admin))} is now an admin!"),
            parse_mode="HTML"
        )
    except:
        await update.message.reply_text(
            format_with_emojis("Invalid user ID!"),
            parse_mode="HTML"
        )

# ============================================================
# /all COMMAND
# ============================================================
async def all_emojis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "PREMIUM EMOJIS\n━━━━━━━━━━━━━━━━━━\n"
    for name in PREMIUM_EMOJIS:
        msg += f"{e(name)} {stylish(name)}\n"
    msg += "\n━━━━━━━━━━━━━━━━━━"
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")

# ============================================================
# /em COMMAND - Users can also use
# ============================================================
async def em_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/em text - Add premium emojis around text (Users can use)"""
    user_id = update.effective_user.id
    
    # Check if banned
    # (banned check optional)
    
    if not context.args:
        await update.message.reply_text(
            format_with_emojis("Usage: /em your text here"),
            parse_mode="HTML"
        )
        return
    
    # Get full text after /em
    full_text = update.message.text
    if full_text.startswith('/em'):
        full_text = full_text[3:].strip()
    
    if not full_text:
        await update.message.reply_text(
            format_with_emojis("Please provide text!"),
            parse_mode="HTML"
        )
        return
    
    # Process each line separately
    lines = full_text.split('\n')
    result_lines = []
    for line in lines:
        if line.strip():
            left, right = get_random_emojis(2)
            result_lines.append(f"{left} {stylish(line.strip())} {right}")
        else:
            result_lines.append('')
    
    result = '\n'.join(result_lines)
    await update.message.reply_text(result, parse_mode="HTML")

# ============================================================
# /start COMMAND
# ============================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    users = load_users()
    if str(user_id) not in users:
        users[str(user_id)] = {
            "username": update.effective_user.username or "NoUsername",
            "first_seen": datetime.now().isoformat()
        }
        save_users(users)
    
    msg = """BETTING BOT

Commands:
/dice - Roll dice (1-6)
/flipcoin - Flip coin (HEAD/TAIL)
/em text - Add premium emojis around text

Admin Commands:
/forcedice 1-6 - Force next dice
/forcecoin HEAD/TAIL - Force next coin
/approve USER_ID - Make admin

/all - Show all premium emojis

━━━━━━━━━━━━━━━━━━
Only group admins can use /dice & /flipcoin"""
    
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")

# ============================================================
# MAIN
# ============================================================
def main():
    # Start Flask thread for Render
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Start Bot
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("dice", dice))
    application.add_handler(CommandHandler("flipcoin", flipcoin))
    application.add_handler(CommandHandler("forcedice", forcedice))
    application.add_handler(CommandHandler("forcecoin", forcecoin))
    application.add_handler(CommandHandler("approve", approve))
    application.add_handler(CommandHandler("all", all_emojis))
    application.add_handler(CommandHandler("em", em_command))
    
    logger.info("Betting Bot Started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
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
# STYLISH CHARACTERS (𝐀 𝐁 𝐂 wale)
# ============================================================
STYLISH = {
    'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆',
    'H': '𝐇', 'I': '𝐈', 'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍',
    'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔',
    'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙',
    'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟',
    'g': '𝐠', 'h': '𝐡', 'i': '𝐢', 'j': '𝐣', 'k': '𝐤', 'l': '𝐥',
    'm': '𝐦', 'n': '𝐧', 'o': '𝐨', 'p': '𝐩', 'q': '𝐪', 'r': '𝐫',
    's': '𝐬', 't': '𝐭', 'u': '𝐮', 'v': '𝐯', 'w': '𝐰', 'x': '𝐱',
    'y': '𝐲', 'z': '𝐳',
    '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒',
    '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗'
}

def stylish(text):
    return ''.join(STYLISH.get(c, c) for c in text)

# ============================================================
# SARE PREMIUM EMOJIS (100+ emojis - tumhare diye hue)
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
    # Extra emojis from your list
    "smile": {"id": "6147464060305676048", "fallback": "😊"},
    "laugh": {"id": "6147565374289220368", "fallback": "😂"},
    "love": {"id": "6147617184479711380", "fallback": "❤️"},
    "cool": {"id": "6147464060305676048", "fallback": "😎"},
    "angry": {"id": "6273840152980755328", "fallback": "😡"},
    "sad": {"id": "6273840152980755328", "fallback": "😢"},
    "wink": {"id": "6276057176444246654", "fallback": "😉"},
    "kiss": {"id": "6044373012566774137", "fallback": "😘"},
    "thinking": {"id": "5782756916660802905", "fallback": "🤔"},
    "clap": {"id": "6093744967304352336", "fallback": "👏"},
    "pray": {"id": "6093744967304352336", "fallback": "🙏"},
    "muscle": {"id": "6032673796530377389", "fallback": "💪"},
    "brain": {"id": "6032673796530377389", "fallback": "🧠"},
    "eyes": {"id": "6035225389356290238", "fallback": "👀"},
    "100": {"id": "6244496562752331516", "fallback": "💯"},
    "zap": {"id": "5791970059597386804", "fallback": "⚡"},
    "rainbow": {"id": "6010338729640596556", "fallback": "🌈"},
    "unicorn": {"id": "6010338729640596556", "fallback": "🦄"},
    "dragon": {"id": "6034962795055812935", "fallback": "🐉"},
    "phoenix": {"id": "6034962795055812935", "fallback": "🔥"},
    "wolf": {"id": "6034871295072539452", "fallback": "🐺"},
    "eagle": {"id": "6034871295072539452", "fallback": "🦅"},
    "shark": {"id": "6034871295072539452", "fallback": "🦈"},
    "dolphin": {"id": "6034871295072539452", "fallback": "🐬"},
    "panda": {"id": "6034871295072539452", "fallback": "🐼"},
    "koala": {"id": "6034871295072539452", "fallback": "🐨"},
    "fox": {"id": "6034871295072539452", "fallback": "🦊"},
    "rabbit": {"id": "6034871295072539452", "fallback": "🐰"},
    "cat": {"id": "6034871295072539452", "fallback": "🐱"},
    "dog": {"id": "6034871295072539452", "fallback": "🐶"},
    "bird": {"id": "6034871295072539452", "fallback": "🐦"},
    "fish": {"id": "6034871295072539452", "fallback": "🐟"},
    "butterfly": {"id": "6010338729640596556", "fallback": "🦋"},
    "bee": {"id": "6010338729640596556", "fallback": "🐝"},
    "ant": {"id": "6010338729640596556", "fallback": "🐜"},
    "snake": {"id": "6034962795055812935", "fallback": "🐍"},
    "turtle": {"id": "6034962795055812935", "fallback": "🐢"},
    "frog": {"id": "6034962795055812935", "fallback": "🐸"},
    "crocodile": {"id": "6034962795055812935", "fallback": "🐊"},
    "whale": {"id": "6034871295072539452", "fallback": "🐋"},
    "octopus": {"id": "6034871295072539452", "fallback": "🐙"},
    "squid": {"id": "6034871295072539452", "fallback": "🦑"},
    "crab": {"id": "6034871295072539452", "fallback": "🦀"},
    "lobster": {"id": "6034871295072539452", "fallback": "🦞"},
    "shrimp": {"id": "6034871295072539452", "fallback": "🦐"},
    "snail": {"id": "6034962795055812935", "fallback": "🐌"},
    "worm": {"id": "6034962795055812935", "fallback": "🐛"},
    "leaf": {"id": "6010338729640596556", "fallback": "🍃"},
    "flower": {"id": "6010338729640596556", "fallback": "🌸"},
    "rose": {"id": "6147617184479711380", "fallback": "🌹"},
    "sunflower": {"id": "6010338729640596556", "fallback": "🌻"},
    "tulip": {"id": "6010338729640596556", "fallback": "🌷"},
    "cactus": {"id": "6010338729640596556", "fallback": "🌵"},
    "palm_tree": {"id": "6010338729640596556", "fallback": "🌴"},
    "evergreen": {"id": "6010338729640596556", "fallback": "🌲"},
    "maple": {"id": "6010338729640596556", "fallback": "🍁"},
    "mushroom": {"id": "6010338729640596556", "fallback": "🍄"},
    "earth": {"id": "5913754823643107921", "fallback": "🌍"},
    "moon": {"id": "6010338729640596556", "fallback": "🌙"},
    "sun": {"id": "6010338729640596556", "fallback": "☀️"},
    "cloud": {"id": "6010338729640596556", "fallback": "☁️"},
    "rain": {"id": "6010338729640596556", "fallback": "🌧️"},
    "snow": {"id": "6010338729640596556", "fallback": "❄️"},
    "thunder": {"id": "5791970059597386804", "fallback": "⛈️"},
    "wind": {"id": "5971944878815317190", "fallback": "💨"},
    "fire_emoji": {"id": "6147524086768604985", "fallback": "🔥"},
    "water": {"id": "6010338729640596556", "fallback": "💧"},
    "drop": {"id": "6010338729640596556", "fallback": "💧"},
    "ocean": {"id": "6010338729640596556", "fallback": "🌊"},
}

def get_emoji_html(name):
    if name in PREMIUM_EMOJIS:
        data = PREMIUM_EMOJIS[name]
        return f'<tg-emoji emoji-id="{data["id"]}">{data["fallback"]}</tg-emoji>'
    return ""

def e(name):
    return get_emoji_html(name)

def get_random_emojis(count=2):
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
# /start COMMAND
# ============================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_type = update.effective_chat.type
    
    users = load_users()
    if str(user_id) not in users:
        users[str(user_id)] = {
            "username": update.effective_user.username or "NoUsername",
            "first_seen": datetime.now().isoformat()
        }
        save_users(users)
    
    if chat_type in ['group', 'supergroup']:
        msg = """𝐁𝐎𝐓 𝐀𝐂𝐓𝐈𝐕𝐄 𝐑𝐄𝐀𝐃𝐘 𝐓𝐎 𝐔𝐒𝐄

𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:
/𝐝𝐢𝐜𝐞 - 𝐑𝐨𝐥𝐥 𝐝𝐢𝐜𝐞 (𝟏-𝟔)
/𝐟𝐥𝐢𝐩𝐜𝐨𝐢𝐧 - 𝐅𝐥𝐢𝐩 𝐜𝐨𝐢𝐧
/𝐞𝐦 𝐭𝐞𝐱𝐭 - 𝐀𝐝𝐝 𝐞𝐦𝐨𝐣𝐢𝐬
/𝐚𝐥𝐥 - 𝐒𝐡𝐨𝐰 𝐞𝐦𝐨𝐣𝐢𝐬

𝐎𝐧𝐥𝐲 𝐠𝐫𝐨𝐮𝐩 𝐚𝐝𝐦𝐢𝐧𝐬 𝐜𝐚𝐧 𝐮𝐬𝐞 /𝐝𝐢𝐜𝐞 & /𝐟𝐥𝐢𝐩𝐜𝐨𝐢𝐧"""
        await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")
        return
    
    msg = """𝐁𝐄𝐓𝐓𝐈𝐍𝐆 𝐁𝐎𝐓

𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:
/𝐝𝐢𝐜𝐞 - 𝐑𝐨𝐥𝐥 𝐝𝐢𝐜𝐞 (𝟏-𝟔)
/𝐟𝐥𝐢𝐩𝐜𝐨𝐢𝐧 - 𝐅𝐥𝐢𝐩 𝐜𝐨𝐢𝐧
/𝐞𝐦 𝐭𝐞𝐱𝐭 - 𝐀𝐝𝐝 𝐞𝐦𝐨𝐣𝐢𝐬
/𝐚𝐥𝐥 - 𝐒𝐡𝐨𝐰 𝐞𝐦𝐨𝐣𝐢𝐬

𝐎𝐧𝐥𝐲 𝐠𝐫𝐨𝐮𝐩 𝐚𝐝𝐦𝐢𝐧𝐬 𝐜𝐚𝐧 𝐮𝐬𝐞 /𝐝𝐢𝐜𝐞 & /𝐟𝐥𝐢𝐩𝐜𝐨𝐢𝐧"""
    
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")

# ============================================================
# /dice COMMAND
# ============================================================
async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if update.effective_chat.type in ['group', 'supergroup']:
        try:
            chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
            if chat_member.status not in ['administrator', 'creator'] and user_id != OWNER_ID:
                await update.message.reply_text(
                    format_with_emojis("𝐎𝐧𝐥𝐲 𝐠𝐫𝐨𝐮𝐩 𝐚𝐝𝐦𝐢𝐧𝐬 𝐜𝐚𝐧 𝐫𝐨𝐥𝐥 𝐝𝐢𝐜𝐞!"),
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
    
    msg = f"""𝐃𝐈𝐂𝐄 𝐑𝐎𝐋𝐋𝐄𝐃
𝐀𝐃𝐌𝐈𝐍 - {stylish(update.effective_user.first_name)}

𝐑𝐄𝐒𝐔𝐋𝐓 - {stylish(str(result))}"""
    
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")

# ============================================================
# /flipcoin COMMAND
# ============================================================
async def flipcoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if update.effective_chat.type in ['group', 'supergroup']:
        try:
            chat_member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
            if chat_member.status not in ['administrator', 'creator'] and user_id != OWNER_ID:
                await update.message.reply_text(
                    format_with_emojis("𝐎𝐧𝐥𝐲 𝐠𝐫𝐨𝐮𝐩 𝐚𝐝𝐦𝐢𝐧𝐬 𝐜𝐚𝐧 𝐟𝐥𝐢𝐩 𝐜𝐨𝐢𝐧!"),
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
    
    msg = f"""𝐂𝐎𝐈𝐍 𝐅𝐋𝐈𝐏𝐏𝐄𝐃
𝐀𝐃𝐌𝐈𝐍 - {stylish(update.effective_user.first_name)}

𝐑𝐄𝐒𝐔𝐋𝐓 - {stylish(result)}"""
    
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")

# ============================================================
# /forcedice - ADMIN ONLY
# ============================================================
async def forcedice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != OWNER_ID and user_id not in load_admins():
        await update.message.reply_text(
            format_with_emojis("𝐎𝐧𝐥𝐲 𝐨𝐰𝐧𝐞𝐫/𝐚𝐝𝐦𝐢𝐧𝐬 𝐜𝐚𝐧 𝐟𝐨𝐫𝐜𝐞 𝐝𝐢𝐜𝐞!"),
            parse_mode="HTML"
        )
        return
    
    if not context.args:
        await update.message.reply_text(
            format_with_emojis("𝐔𝐬𝐚𝐠𝐞: /𝐟𝐨𝐫𝐜𝐞𝐝𝐢𝐜𝐞 𝟏-𝟔"),
            parse_mode="HTML"
        )
        return
    
    try:
        num = int(context.args[0])
        if num < 1 or num > 6:
            await update.message.reply_text(
                format_with_emojis("𝐍𝐮𝐦𝐛𝐞𝐫 𝐦𝐮𝐬𝐭 𝐛𝐞 𝐛𝐞𝐭𝐰𝐞𝐞𝐧 𝟏 𝐚𝐧𝐝 𝟔"),
                parse_mode="HTML"
            )
            return
        
        force_data = load_force()
        force_data["dice"] = num
        save_force(force_data)
        
        await update.message.reply_text(
            format_with_emojis(f"𝐍𝐞𝐱𝐭 𝐝𝐢𝐜𝐞 𝐫𝐨𝐥𝐥 𝐰𝐢𝐥𝐥 𝐛𝐞 {stylish(str(num))}!"),
            parse_mode="HTML"
        )
    except:
        await update.message.reply_text(
            format_with_emojis("𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐧𝐮𝐦𝐛𝐞𝐫!"),
            parse_mode="HTML"
        )

# ============================================================
# /forcecoin - ADMIN ONLY
# ============================================================
async def forcecoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != OWNER_ID and user_id not in load_admins():
        await update.message.reply_text(
            format_with_emojis("𝐎𝐧𝐥𝐲 𝐨𝐰𝐧𝐞𝐫/𝐚𝐝𝐦𝐢𝐧𝐬 𝐜𝐚𝐧 𝐟𝐨𝐫𝐜𝐞 𝐜𝐨𝐢𝐧!"),
            parse_mode="HTML"
        )
        return
    
    if not context.args:
        await update.message.reply_text(
            format_with_emojis("𝐔𝐬𝐚𝐠𝐞: /𝐟𝐨𝐫𝐜𝐞𝐜𝐨𝐢𝐧 𝐇𝐄𝐀𝐃/𝐓𝐀𝐈𝐋"),
            parse_mode="HTML"
        )
        return
    
    result = context.args[0].upper()
    if result not in ["HEAD", "TAIL"]:
        await update.message.reply_text(
            format_with_emojis("𝐌𝐮𝐬𝐭 𝐛𝐞 𝐇𝐄𝐀𝐃 𝐨𝐫 𝐓𝐀𝐈𝐋"),
            parse_mode="HTML"
        )
        return
    
    force_data = load_force()
    force_data["coin"] = result
    save_force(force_data)
    
    await update.message.reply_text(
        format_with_emojis(f"𝐍𝐞𝐱𝐭 𝐜𝐨𝐢𝐧 𝐟𝐥𝐢𝐩 𝐰𝐢𝐥𝐥 𝐛𝐞 {stylish(result)}!"),
        parse_mode="HTML"
    )

# ============================================================
# /approve - OWNER ONLY
# ============================================================
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != OWNER_ID:
        await update.message.reply_text(
            format_with_emojis("𝐎𝐧𝐥𝐲 𝐨𝐰𝐧𝐞𝐫 𝐜𝐚𝐧 𝐚𝐩𝐩𝐫𝐨𝐯𝐞 𝐚𝐝𝐦𝐢𝐧𝐬!"),
            parse_mode="HTML"
        )
        return
    
    if not context.args:
        await update.message.reply_text(
            format_with_emojis("𝐔𝐬𝐚𝐠𝐞: /𝐚𝐩𝐩𝐫𝐨𝐯𝐞 𝐔𝐒𝐄𝐑_𝐈𝐃"),
            parse_mode="HTML"
        )
        return
    
    try:
        new_admin = int(context.args[0])
        admins = load_admins()
        if new_admin in admins:
            await update.message.reply_text(
                format_with_emojis("𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧!"),
                parse_mode="HTML"
            )
            return
        admins.append(new_admin)
        save_admins(admins)
        await update.message.reply_text(
            format_with_emojis(f"𝐔𝐬𝐞𝐫 {stylish(str(new_admin))} 𝐢𝐬 𝐧𝐨𝐰 𝐚𝐧 𝐚𝐝𝐦𝐢𝐧!"),
            parse_mode="HTML"
        )
    except:
        await update.message.reply_text(
            format_with_emojis("𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐮𝐬𝐞𝐫 𝐈𝐃!"),
            parse_mode="HTML"
        )

# ============================================================
# /all - SHOW ALL EMOJIS
# ============================================================
async def all_emojis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐄𝐌𝐎𝐉𝐈𝐒\n━━━━━━━━━━━━━━━━━━\n"
    count = 0
    for name in PREMIUM_EMOJIS:
        msg += f"{e(name)} {stylish(name)}\n"
        count += 1
        if count > 50:  # Limit to avoid too long message
            msg += f"\n... 𝐚𝐧𝐝 {len(PREMIUM_EMOJIS) - 50} 𝐦𝐨𝐫𝐞"
            break
    msg += "\n━━━━━━━━━━━━━━━━━━"
    await update.message.reply_text(format_with_emojis(msg), parse_mode="HTML")

# ============================================================
# /em COMMAND - Users can use
# ============================================================
async def em_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            format_with_emojis("𝐔𝐬𝐚𝐠𝐞: /𝐞𝐦 𝐲𝐨𝐮𝐫 𝐭𝐞𝐱𝐭 𝐡𝐞𝐫𝐞"),
            parse_mode="HTML"
        )
        return
    
    full_text = update.message.text
    if full_text.startswith('/em'):
        full_text = full_text[3:].strip()
    
    if not full_text:
        await update.message.reply_text(
            format_with_emojis("𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐭𝐞𝐱𝐭!"),
            parse_mode="HTML"
        )
        return
    
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
# MAIN
# ============================================================
def main():
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    application = Application.builder().token(BOT_TOKEN).build()
    
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

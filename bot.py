#!/usr/bin/env python3
import telebot
from telebot.types import MessageEntity, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import random
import emoji
import time
import os
import json
from datetime import datetime

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
    """Convert normal text to stylish characters"""
    return ''.join(STYLISH.get(c, c) for c in text)

# ============================================================
# Bot Credentials
# ============================================================
TOKEN = "8905481398:AAEAqmHaX7Pti-iUagE-SxRAowSwDDPShV0"
ADMIN_IDS = [8656257840, 8656257840]
bot = telebot.TeleBot(TOKEN)

bot_active = True
user_db_file = "users.json"

def load_users():
    if os.path.exists(user_db_file):
        with open(user_db_file, "r") as f:
            return set(json.load(f))
    return set()

def save_users(users: set):
    with open(user_db_file, "w") as f:
        json.dump(list(users), f)

all_users: set = load_users()

# ============================================================
# EMOJI MAPPING - Normal Emoji -> Related Premium Emoji ID
# ============================================================
EMOJI_MAPPING = {
    "✅": ["6246537187614005254", "6246782404476803545", "6010060634803148161"],
    "✔️": ["6246871001062185760", "6010264538375525668"],
    "🔥": ["4956222745814762495", "4956606007221421405", "6086954744268460848"],
    "⚡": ["5791970059597386804", "6087079590377820415"],
    "❤️": ["5783157259152397008", "5801084710343938087"],
    "⭐": ["6244496562752331516", "5904618938578243567"],
    "✨": ["6010338729640596556", "6010086134023985536"],
    "👑": ["5794422335599546668", "6089003761496232797"],
    "💰": ["6089104607328342288", "6086730718774300509"],
    "💎": ["6086778246882399112", "5791697221799907788"],
    "👍": ["6089313931149448495", "4958626617535497157"],
    "😎": ["6032853480782172520", "6044373012566774137"],
    "😭": ["5783024321324651865"],
    "🤔": ["5782756916660802905", "5783034045130610245"],
}

FLAG_MAPPING = {
    "🇮🇳": "5433601609076586221", "🇺🇸": "5433865586356531140",
    "🇬🇧": "5433827537241258614", "🇯🇵": "5434147542369579483",
}

# ============================================================
# PRIMARY EMOJIS FROM Reobashd pack
# ============================================================
PRIMARY_EMOJIS = [
    "6035051267087143217", "6034945975963881533", "6034845323405299835",
    "6032965553658794901", "6035158121578501544", "6035208832257364215",
    "6035067476293718178", "6033130342964007608", "6034986056598688136",
    "6032765485492214347", "6032660275973330342", "6034916516783198293",
    "6034904439335162652", "6034928023000585140", "6035372904303038740",
    "6035137110598492010", "6035338338406242050", "6035225389356290238",
    "6035081585261287115", "6035243995154616907", "6034865170449175739",
    "6035173858338672933", "6035210301136182368", "6035265083444042235",
    "6034871295072539452", "6035251193519805118", "6035136809950778133",
    "6032695825417638128", "6032739101508113500", "6032985916098750553",
    "6035374291577475270", "6035355642829475999", "6035337951859184840",
    "6035072209347678547", "6035060329468137931", "6033077437556855182",
    "6032823763903452409", "6034853694296560978", "6035015146412183834",
    "6035372401791864953", "6034955549445984368", "6032673796530377389",
    "6032916496542339992", "6034855438053282213", "6034962795055812935",
    "6034832094906028632", "6035087164423802534", "6035343380697846690",
    "6032737138708059114", "6035194237958493530", "6035317340311129897",
    "6035070298087231243", "6035242444671421879", "6034957847253487695",
    "6034925781027656042", "6033067975743902590", "6032975015471747801",
    "6034926000070988470", "6034843326245508065", "6032853480782172520",
    "6044373012566774137", "6044369013952222465", "6044359320211034681",
    "6044290806892729376", "6044238120528908813", "5791970059597386804",
    "5794422335599546668",
]

ALL_PREMIUM_EMOJIS = list(set(PRIMARY_EMOJIS + [
    "6246537187614005254", "6246782404476803545", "6244496562752331516",
    "6247039939305808563", "6246871001062185760",
    "6089104607328342288", "6086730718774300509", "6089003761496232797",
    "6089313931149448495", "4956222745814762495", "4958479549265347295",
]))

DEFAULT_EMOJI_ID = "6035338338406242050"
PLACEHOLDER = "🌟"
temp_data = {}

# ============================================================
# EMOJI CONVERSION FUNCTION
# ============================================================
_emoji_id_cache: dict = {}
EMOJI_CACHE_TTL = 1800

def _normalize_emoji(e: str) -> str:
    normalized = e.replace('\ufe0f', '').replace('\ufe0e', '').replace('\u200d', '')
    return normalized if normalized else e

def get_premium_emoji_for_normal_emoji(normal_emoji: str) -> str:
    now = time.time()
    cached = _emoji_id_cache.get(normal_emoji)
    if cached and (now - cached[1]) < EMOJI_CACHE_TTL:
        return cached[0]
    key = normal_emoji
    if key not in EMOJI_MAPPING and key not in FLAG_MAPPING:
        key = _normalize_emoji(normal_emoji)
    if key in EMOJI_MAPPING:
        chosen = random.choice(EMOJI_MAPPING[key])
    elif key in FLAG_MAPPING:
        chosen = FLAG_MAPPING[key]
    else:
        chosen = random.choice(ALL_PREMIUM_EMOJIS)
    _emoji_id_cache[normal_emoji] = (chosen, now)
    return chosen

def get_random_primary_emoji() -> str:
    return random.choice(PRIMARY_EMOJIS)

# ============================================================
# BUTTON CREATION
# ============================================================
def _extract_first_emoji(text: str):
    import unicodedata
    chars = list(text)
    i = 0
    while i < len(chars):
        ch = chars[i]
        if (i + 1 < len(chars)
                and '\U0001F1E0' <= ch <= '\U0001F1FF'
                and '\U0001F1E0' <= chars[i + 1] <= '\U0001F1FF'):
            seq = ch + chars[i + 1]
            cleaned = "".join(chars[:i] + chars[i + 2:]).strip()
            return seq, cleaned
        if emoji.is_emoji(ch):
            seq = ch
            j = i + 1
            while j < len(chars) and (
                chars[j] in ('\u200d', '\ufe0f', '\ufe0e')
                or unicodedata.category(chars[j]) in ('Mn', 'Mc')
                or '\U0001F3FB' <= chars[j] <= '\U0001F3FF'
            ):
                seq += chars[j]
                j += 1
            cleaned = "".join(chars[:i] + chars[j:]).strip()
            return seq, cleaned
        i += 1
    return None, text

def _make_btn(text: str, style: str = None, icon_id: str = None, **kwargs) -> InlineKeyboardButton:
    if icon_id and style:
        try:
            return InlineKeyboardButton(text=text, icon_custom_emoji_id=icon_id, style=style, **kwargs)
        except TypeError:
            pass
    if icon_id:
        try:
            return InlineKeyboardButton(text=text, icon_custom_emoji_id=icon_id, **kwargs)
        except TypeError:
            pass
    if style:
        try:
            return InlineKeyboardButton(text=text, style=style, **kwargs)
        except TypeError:
            pass
    return InlineKeyboardButton(text=text, **kwargs)

def make_button_with_icon(text: str, style: str = None, **kwargs) -> InlineKeyboardButton:
    first_emoji, _ = _extract_first_emoji(text)
    if first_emoji:
        premium_id = get_premium_emoji_for_normal_emoji(first_emoji)
    else:
        premium_id = get_random_primary_emoji()
    return _make_btn(text, style=style, icon_id=premium_id, **kwargs)

# ============================================================
# FORCE JOIN CHANNELS
# ============================================================
REQUIRED_CHANNELS = [
    {"id": "-1003360548513", "name": "DEV WORLD 〽️", "link": "https://t.me/DEVWORLDOFFICIALCHANNEL"},
    {"id": "-1003918756977", "name": "ZAINU BHAI", "link": "https://t.me/ZAINUBHAI"},
    {"id": "-1003669933791", "name": "YDV ARMY", "link": "https://t.me/ydv_army"},
    {"id": "-1003564583501", "name": "FIRE CODES BY IMAX", "link": "https://t.me/freecodesbhimax"},
    {"id": "-1003645019104", "name": "NOVA DEVELOPER", "link": "https://t.me/codenovaai01"},
]

def _utf16_len(ch: str) -> int:
    return len(ch.encode("utf-16-le")) // 2

def _utf16_len_str(s: str) -> int:
    return len(s.encode("utf-16-le")) // 2

def _build_pe_entities(text: str, use_primary: bool = True):
    entities = []
    utf16_offset = 0
    total_utf16 = _utf16_len_str(text)
    
    if total_utf16 > 0:
        entities.append(MessageEntity(type="bold", offset=0, length=total_utf16))
    
    for ch in text:
        ch_len = _utf16_len(ch)
        if ch == PLACEHOLDER:
            eid = random.choice(PRIMARY_EMOJIS) if use_primary else random.choice(ALL_PREMIUM_EMOJIS)
            entities.append(MessageEntity(
                type="custom_emoji",
                offset=utf16_offset,
                length=ch_len,
                custom_emoji_id=eid
            ))
        utf16_offset += ch_len
    
    return entities

def _send_pe(chat_id, text: str, use_primary: bool = True, reply_markup=None):
    entities = _build_pe_entities(text, use_primary)
    return bot.send_message(chat_id, text, entities=entities, reply_markup=reply_markup, parse_mode=None)

def is_admin(user_id):
    return user_id in ADMIN_IDS

def check_joined(uid: int) -> list:
    if is_admin(uid):
        return []
    
    not_joined = []
    for ch in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(ch["id"], uid)
            if member.status in ("left", "kicked", "banned"):
                not_joined.append(ch)
        except Exception:
            not_joined.append(ch)
    return not_joined

def send_join_notice(chat_id: int, not_joined: list):
    joined_count = len(REQUIRED_CHANNELS) - len(not_joined)
    total_count = len(REQUIRED_CHANNELS)
    
    keyboard = []
    for ch in not_joined:
        keyboard.append([InlineKeyboardButton(text=f"📢 {ch['name']}", url=ch["link"])])
    keyboard.append([make_button_with_icon(text="✅ 𝐈 𝐇𝐀𝐕𝐄 𝐉𝐎𝐈𝐍𝐄𝐃", style="success", callback_data="check_join")])
    markup = InlineKeyboardMarkup(keyboard)
    
    status_text = ""
    for ch in REQUIRED_CHANNELS:
        if ch in not_joined:
            status_text += f"📢  ❌ {ch['name']}\n"
        else:
            status_text += f"📢  ✅ {ch['name']}\n"
    
    text = f"""
{PLACEHOLDER}═══《 🔒 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃! 》═══{PLACEHOLDER}

🚫 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃!

📊 𝐏𝐑𝐎𝐆𝐑𝐄𝐒𝐒: {joined_count}/{total_count} 𝐉𝐎𝐈𝐍𝐄𝐃

⚠️ 𝐓𝐎 𝐔𝐒𝐄 𝐓𝐇𝐈𝐒 𝐁𝐎𝐓, 𝐘𝐎𝐔 𝐌𝐔𝐒𝐓 𝐉𝐎𝐈𝐍 𝐀𝐋𝐋 𝐂𝐇𝐀𝐍𝐍𝐄𝐋𝐒 𝐅𝐈𝐑𝐒𝐓!

{status_text}
👇 𝐂𝐋𝐈𝐂𝐊 𝐓𝐇𝐄 𝐁𝐔𝐓𝐓𝐎𝐍𝐒 𝐁𝐄𝐋𝐎𝐖 𝐓𝐎 𝐉𝐎𝐈𝐍: 👇

{PLACEHOLDER}═══════════════════════{PLACEHOLDER}
"""
    _send_pe(chat_id, text, reply_markup=markup)

def register_user(uid: int):
    if uid not in all_users:
        all_users.add(uid)
        save_users(all_users)

# ============================================================
# DICE / FLIPCOIN FUNCTIONS (BETTING)
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
# BETTING COMMANDS
# ============================================================
@bot.message_handler(commands=['dice'])
def dice_command(message):
    uid = message.from_user.id
    
    if not bot_active and not is_admin(uid):
        bot.reply_to(message, "⚠️ Bot is currently OFF. Admin will turn it on soon.")
        return
    
    not_joined = check_joined(uid)
    if not_joined:
        send_join_notice(message.chat.id, not_joined)
        return
    
    register_user(uid)
    
    # Check if group admin (only in groups)
    if message.chat.type in ['group', 'supergroup']:
        try:
            member = bot.get_chat_member(message.chat.id, uid)
            if member.status not in ['administrator', 'creator'] and not is_admin(uid):
                bot.reply_to(message, stylish("Only group admins can roll dice!"))
                return
        except:
            pass
    
    force_data = load_force()
    if force_data.get("dice") is not None and (is_admin(uid)):
        result = force_data["dice"]
        force_data["dice"] = None
        save_force(force_data)
    else:
        result = random.randint(1, 6)
    
    msg = f"""🎲 𝐃𝐈𝐂𝐄 𝐑𝐎𝐋𝐋𝐄𝐃
👤 𝐀𝐃𝐌𝐈𝐍 - {stylish(message.from_user.first_name)}

🎯 𝐑𝐄𝐒𝐔𝐋𝐓 - {stylish(str(result))}"""
    
    _send_pe(message.chat.id, msg)

@bot.message_handler(commands=['flipcoin'])
def flipcoin_command(message):
    uid = message.from_user.id
    
    if not bot_active and not is_admin(uid):
        bot.reply_to(message, "⚠️ Bot is currently OFF. Admin will turn it on soon.")
        return
    
    not_joined = check_joined(uid)
    if not_joined:
        send_join_notice(message.chat.id, not_joined)
        return
    
    register_user(uid)
    
    if message.chat.type in ['group', 'supergroup']:
        try:
            member = bot.get_chat_member(message.chat.id, uid)
            if member.status not in ['administrator', 'creator'] and not is_admin(uid):
                bot.reply_to(message, stylish("Only group admins can flip coin!"))
                return
        except:
            pass
    
    force_data = load_force()
    if force_data.get("coin") is not None and (is_admin(uid)):
        result = force_data["coin"]
        force_data["coin"] = None
        save_force(force_data)
    else:
        result = random.choice(["HEAD", "TAIL"])
    
    msg = f"""🪙 𝐂𝐎𝐈𝐍 𝐅𝐋𝐈𝐏𝐏𝐄𝐃
👤 𝐀𝐃𝐌𝐈𝐍 - {stylish(message.from_user.first_name)}

🎯 𝐑𝐄𝐒𝐔𝐋𝐓 - {stylish(result)}"""
    
    _send_pe(message.chat.id, msg)

@bot.message_handler(commands=['forcedice'])
def forcedice_command(message):
    uid = message.from_user.id
    
    if not is_admin(uid):
        bot.reply_to(message, stylish("Only owner/admins can force dice!"))
        return
    
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, stylish("Usage: /forcedice 1-6"))
        return
    
    try:
        num = int(args[1])
        if num < 1 or num > 6:
            bot.reply_to(message, stylish("Number must be between 1 and 6"))
            return
        
        force_data = load_force()
        force_data["dice"] = num
        save_force(force_data)
        bot.reply_to(message, stylish(f"Next dice roll will be {num}!"))
    except:
        bot.reply_to(message, stylish("Invalid number!"))

@bot.message_handler(commands=['forcecoin'])
def forcecoin_command(message):
    uid = message.from_user.id
    
    if not is_admin(uid):
        bot.reply_to(message, stylish("Only owner/admins can force coin!"))
        return
    
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, stylish("Usage: /forcecoin HEAD/TAIL"))
        return
    
    result = args[1].upper()
    if result not in ["HEAD", "TAIL"]:
        bot.reply_to(message, stylish("Must be HEAD or TAIL"))
        return
    
    force_data = load_force()
    force_data["coin"] = result
    save_force(force_data)
    bot.reply_to(message, stylish(f"Next coin flip will be {result}!"))

# ============================================================
# /em COMMAND - Users can add premium emojis around text
# ============================================================
@bot.message_handler(commands=['em'])
def em_command(message):
    uid = message.from_user.id
    
    if not bot_active and not is_admin(uid):
        bot.reply_to(message, "⚠️ Bot is currently OFF.")
        return
    
    not_joined = check_joined(uid)
    if not_joined:
        send_join_notice(message.chat.id, not_joined)
        return
    
    register_user(uid)
    
    text = message.text
    if text.startswith('/em'):
        text = text[3:].strip()
    
    if not text:
        bot.reply_to(message, stylish("Usage: /em your text here"))
        return
    
    lines = text.split('\n')
    result_lines = []
    for line in lines:
        if line.strip():
            # Add random premium emojis around each line
            left = get_random_primary_emoji()
            right = get_random_primary_emoji()
            result_lines.append(f"{PLACEHOLDER} {stylish(line.strip())} {PLACEHOLDER}")
        else:
            result_lines.append('')
    
    result = '\n'.join(result_lines)
    _send_pe(message.chat.id, result)

# ============================================================
# /all - Show all premium emojis
# ============================================================
@bot.message_handler(commands=['all'])
def all_emojis_command(message):
    uid = message.from_user.id
    
    if not bot_active and not is_admin(uid):
        bot.reply_to(message, "⚠️ Bot is currently OFF.")
        return
    
    not_joined = check_joined(uid)
    if not_joined:
        send_join_notice(message.chat.id, not_joined)
        return
    
    register_user(uid)
    
    # Show all premium emojis with stylish names
    msg = "𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐄𝐌𝐎𝐉𝐈𝐒\n━━━━━━━━━━━━━━━━━━\n"
    emoji_names = list(EMOJI_MAPPING.keys()) + list(FLAG_MAPPING.keys())
    for name in emoji_names[:30]:  # Limit to avoid too long message
        premium_id = get_premium_emoji_for_normal_emoji(name)
        msg += f"{PLACEHOLDER} {stylish(name)}\n"
    msg += "\n━━━━━━━━━━━━━━━━━━\nUse /em text to add emojis!"
    _send_pe(message.chat.id, msg)

# ============================================================
# MENU / START
# ============================================================
def get_menu(user_id):
    is_admin_user = is_admin(user_id)
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    if is_admin_user:
        markup.row(
            KeyboardButton("🔴 𝐁𝐎𝐓 𝐎𝐅𝐅"),
            KeyboardButton("🟢 𝐁𝐎𝐓 𝐎𝐍")
        )
        markup.row(
            KeyboardButton("🌿 𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓"),
            KeyboardButton("💢 𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓")
        )
        markup.row(
            KeyboardButton("👾 𝐔𝐒𝐄𝐑𝐒 𝐋𝐈𝐒𝐓"),
            KeyboardButton("🍁 𝐁𝐎𝐓 𝐒𝐓𝐀𝐓𝐒")
        )
        markup.row(
            KeyboardButton("🍂 𝐇𝐄𝐋𝐏"),
            KeyboardButton("🍀 𝐀𝐁𝐎𝐔𝐓 𝐁𝐎𝐓")
        )
        # Betting commands in menu
        markup.row(
            KeyboardButton("🎲 𝐃𝐈𝐂𝐄"),
            KeyboardButton("🪙 𝐅𝐋𝐈𝐏𝐂𝐎𝐈𝐍")
        )
    else:
        markup.row(KeyboardButton("🌿 𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓"))
        markup.row(
            KeyboardButton("🍂 𝐇𝐄𝐋𝐏"),
            KeyboardButton("🍀 𝐀𝐁𝐎𝐔𝐓 𝐁𝐎𝐓")
        )
        # Users ko bhi dice/flipcoin dikhe but group admin check hoga
        markup.row(
            KeyboardButton("🎲 𝐃𝐈𝐂𝐄"),
            KeyboardButton("🪙 𝐅𝐋𝐈𝐏𝐂𝐎𝐈𝐍")
        )
    
    return markup

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    uid = message.from_user.id
    register_user(uid)
    
    not_joined = check_joined(uid)
    if not_joined:
        send_join_notice(message.chat.id, not_joined)
        return
    
    markup = get_menu(uid)
    text = f"""
{PLACEHOLDER}═══《 🎲 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐁𝐄𝐓𝐓𝐈𝐍𝐆 𝐁𝐎𝐓 》═══{PLACEHOLDER}

🔥 𝐅𝐄𝐀𝐓𝐔𝐑𝐄𝐒:
🎲 /𝐝𝐢𝐜𝐞 - 𝐑𝐨𝐥𝐥 𝐚 𝐝𝐢𝐜𝐞 (𝟏-𝟔)
🪙 /𝐟𝐥𝐢𝐩𝐜𝐨𝐢𝐧 - 𝐅𝐥𝐢𝐩 𝐚 𝐜𝐨𝐢𝐧
✨ /𝐞𝐦 𝐭𝐞𝐱𝐭 - 𝐀𝐝𝐝 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐞𝐦𝐨𝐣𝐢𝐬
📋 /𝐚𝐥𝐥 - 𝐒𝐡𝐨𝐰 𝐚𝐥𝐥 𝐞𝐦𝐨𝐣𝐢𝐬

⚠️ 𝐎𝐧𝐥𝐲 𝐠𝐫𝐨𝐮𝐩 𝐚𝐝𝐦𝐢𝐧𝐬 𝐜𝐚𝐧 𝐮𝐬𝐞 /𝐝𝐢𝐜𝐞 & /𝐟𝐥𝐢𝐩𝐜𝐨𝐢𝐧

{PLACEHOLDER}═══════════════════════{PLACEHOLDER}
"""
    _send_pe(message.chat.id, text, reply_markup=markup)

# ============================================================
# HANDLE BUTTON CLICKS FOR DICE/FLIPCOIN
# ============================================================
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == "check_join":
        uid = call.from_user.id
        not_joined = check_joined(uid)
        if not_joined:
            send_join_notice(call.message.chat.id, not_joined)
        else:
            bot.answer_callback_query(call.id, "✅ You have joined all channels!")
            markup = get_menu(uid)
            text = f"""
{PLACEHOLDER}═══《 ✅ 𝐀𝐂𝐂𝐄𝐒𝐒 𝐆𝐑𝐀𝐍𝐓𝐄Ｄ! 》═══{PLACEHOLDER}

🎉 𝐘𝐎𝐔 𝐇𝐀𝐕𝐄 𝐉𝐎𝐈𝐍𝐄𝐃 𝐀𝐋𝐋 𝐂𝐇𝐀𝐍𝐍𝐄𝐋𝐒!

🔥 𝐍𝐎𝐖 𝐘𝐎𝐔 𝐂𝐀𝐍 𝐔𝐒𝐄 𝐓𝐇𝐄 𝐁𝐎𝐓!

{PLACEHOLDER}═══════════════════════{PLACEHOLDER}
"""
            _send_pe(call.message.chat.id, text, reply_markup=markup)

# ============================================================
# HANDLE TEXT MESSAGES (Button clicks)
# ============================================================
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    uid = message.from_user.id
    
    if not bot_active and not is_admin(uid):
        bot.reply_to(message, "⚠️ Bot is currently OFF. Admin will turn it on soon.")
        return
    
    not_joined = check_joined(uid)
    if not_joined:
        send_join_notice(message.chat.id, not_joined)
        return
    
    register_user(uid)
    text = message.text
    
    # ============================================================
    # DICE BUTTON
    # ============================================================
    if text == "🎲 𝐃𝐈𝐂𝐄":
        # Simulate /dice command
        if message.chat.type in ['group', 'supergroup']:
            try:
                member = bot.get_chat_member(message.chat.id, uid)
                if member.status not in ['administrator', 'creator'] and not is_admin(uid):
                    bot.reply_to(message, stylish("Only group admins can roll dice!"))
                    return
            except:
                pass
        
        force_data = load_force()
        if force_data.get("dice") is not None and is_admin(uid):
            result = force_data["dice"]
            force_data["dice"] = None
            save_force(force_data)
        else:
            result = random.randint(1, 6)
        
        msg = f"""🎲 𝐃𝐈𝐂𝐄 𝐑𝐎𝐋𝐋𝐄𝐃
👤 𝐀𝐃𝐌𝐈𝐍 - {stylish(message.from_user.first_name)}

🎯 𝐑𝐄𝐒𝐔𝐋𝐓 - {stylish(str(result))}"""
        _send_pe(message.chat.id, msg)
    
    # ============================================================
    # FLIPCOIN BUTTON
    # ============================================================
    elif text == "🪙 𝐅𝐋𝐈𝐏𝐂𝐎𝐈𝐍":
        if message.chat.type in ['group', 'supergroup']:
            try:
                member = bot.get_chat_member(message.chat.id, uid)
                if member.status not in ['administrator', 'creator'] and not is_admin(uid):
                    bot.reply_to(message, stylish("Only group admins can flip coin!"))
                    return
            except:
                pass
        
        force_data = load_force()
        if force_data.get("coin") is not None and is_admin(uid):
            result = force_data["coin"]
            force_data["coin"] = None
            save_force(force_data)
        else:
            result = random.choice(["HEAD", "TAIL"])
        
        msg = f"""🪙 𝐂𝐎𝐈𝐍 𝐅𝐋𝐈𝐏𝐏𝐄𝐃
👤 𝐀𝐃𝐌𝐈𝐍 - {stylish(message.from_user.first_name)}

🎯 𝐑𝐄𝐒𝐔𝐋𝐓 - {stylish(result)}"""
        _send_pe(message.chat.id, msg)
    
    # ============================================================
    # OTHER BUTTONS (Keep original functionality)
    # ============================================================
    elif text == "🔴 𝐁𝐎𝐓 𝐎𝐅𝐅" and is_admin(uid):
        global bot_active
        bot_active = False
        bot.reply_to(message, "🔴 Bot has been turned OFF.")
    
    elif text == "🟢 𝐁𝐎𝐓 𝐎𝐍" and is_admin(uid):
        bot_active = True
        bot.reply_to(message, "🟢 Bot has been turned ON.")
    
    elif text == "🌿 𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓":
        # Your existing make post logic
        bot.reply_to(message, stylish("📝 Send your post content..."))
    
    elif text == "💢 𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓" and is_admin(uid):
        bot.reply_to(message, stylish("📢 Send broadcast message..."))
    
    elif text == "👾 𝐔𝐒𝐄𝐑𝐒 𝐋𝐈𝐒𝐓" and is_admin(uid):
        bot.reply_to(message, stylish(f"👥 Total Users: {len(all_users)}"))
    
    elif text == "🍁 𝐁𝐎𝐓 𝐒𝐓𝐀𝐓𝐒" and is_admin(uid):
        bot.reply_to(message, stylish(f"📊 Bot Active: {bot_active}\n👥 Users: {len(all_users)}"))
    
    elif text == "🍂 𝐇𝐄𝐋𝐏":
        help_text = f"""
{PLACEHOLDER}═══《 📚 𝐇𝐄𝐋𝐏 》═══{PLACEHOLDER}

🎲 /𝐝𝐢𝐜𝐞 - 𝐑𝐨𝐥𝐥 𝐝𝐢𝐜𝐞 (𝟏-𝟔)
🪙 /𝐟𝐥𝐢𝐩𝐜𝐨𝐢𝐧 - 𝐅𝐥𝐢𝐩 𝐜𝐨𝐢𝐧
✨ /𝐞𝐦 𝐭𝐞𝐱𝐭 - 𝐀𝐝𝐝 𝐞𝐦𝐨𝐣𝐢𝐬
📋 /𝐚𝐥𝐥 - 𝐒𝐡𝐨𝐰 𝐚𝐥𝐥 𝐞𝐦𝐨𝐣𝐢𝐬

{PLACEHOLDER}═══════════════════════{PLACEHOLDER}
"""
        _send_pe(message.chat.id, help_text)
    
    elif text == "🍀 𝐀𝐁𝐎𝐔𝐓 𝐁𝐎𝐓":
        about_text = f"""
{PLACEHOLDER}═══《 ℹ️ 𝐀𝐁𝐎𝐔𝐓 》═══{PLACEHOLDER}

🤖 𝐁𝐄𝐓𝐓𝐈𝐍𝐆 𝐁𝐎𝐓
🔥 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐄𝐦𝐨𝐣𝐢 𝐒𝐮𝐩𝐩𝐨𝐫𝐭
🎲 𝐃𝐢𝐜𝐞 & 𝐅𝐥𝐢𝐩𝐜𝐨𝐢𝐧 𝐆𝐚𝐦𝐞𝐬

👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: @iflexvenom

{PLACEHOLDER}═══════════════════════{PLACEHOLDER}
"""
        _send_pe(message.chat.id, about_text)
    
    else:
        # Handle other text - you can keep your existing logic
        pass

# ============================================================
# POLLING
# ============================================================
if __name__ == "__main__":
    print("🤖 Betting Bot Started!")
    bot.infinity_polling(skip_pending=True)

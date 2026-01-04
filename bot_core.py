import random, string, os, asyncio
from telethon import TelegramClient, events, Button
from telethon.tl.functions.account import CheckUsernameRequest
from telethon.errors import FloodWaitError, SessionPasswordNeededError

# البيانات الثابتة التي قدمتها
API_ID = 36656028
API_HASH = 'a7e49446c9e8b43aee5db9c643fb4531'

# مفاتيح RSA الخاصة بك (للتوثيق داخل السكربت)
RSA_KEYS = [
    "MIIBCgKCAQEAyMEdY1aR+sCR3ZSJrtztKTKqigvO/vBfqACJLZtS7QMgCGXJ6XIR...",
    "MIIBCgKCAQEA6LszBcC1LGzyr992NzE0ieY+BSaOW622Aa9Bd4ZHLl+TuFQ4lo4g..."
]

# سيتم حقن هذه البيانات بواسطة ملف installl.sh
BOT_TOKEN = 'TOKEN_HERE'
ADMIN_ID = ADMIN_ID_HERE

# أسماء الملفات
USER_SESSION = 'account_session'
ALL_FOUND = 'all_users.txt'
PREMIUM_FOUND = 'premium_users.txt'

client = TelegramClient(USER_SESSION, API_ID, API_HASH)
bot = TelegramClient('bot_session', API_ID, API_HASH)

is_running = False

def generate_username(mode, length):
    if mode == "letters":
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    elif mode == "mixed":
        return random.choice(string.ascii_lowercase) + ''.join(random.choice(string.digits) for _ in range(length-1))
    elif mode == "alpha_num":
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    if event.sender_id != ADMIN_ID: return
    btns = [
        [Button.inline("🔍 بدء البحث", b"menu")],
        [Button.inline("📂 سجل اليوزرات", b"show_all"), Button.inline("💎 اليوزرات المميزة", b"show_vip")]
    ]
    await event.respond("🚀 مرحباً بك في لوحة تحكم الصائد الاستثماري:", buttons=btns)

@bot.on(events.CallbackQuery)
async def callback(event):
    global is_running
    data = event.data

    if data == b"menu":
        btns = [
            [Button.inline("🔤 حروف فقط", b"mode_letters"), Button.inline("🔢 حرف + أرقام", b"mode_mixed")],
            [Button.inline("🔡 حروف وأرقام", b"mode_alpha")],
            [Button.inline("🛑 إيقاف البحث", b"stop")]
        ]
        await event.edit("اختر نوع التوليد:", buttons=btns)

    elif data.startswith(b"mode_"):
        mode = data.decode().split('_')[1]
        async with bot.conversation(event.sender_id) as conv:
            await conv.send_message("🔢 أرسل عدد خانات اليوزر (مثلاً 5):")
            res = await conv.get_response()
            length = int(res.text)
            is_running = True
            await conv.send_message(f"✅ بدأ الفحص... طول اليوزر {length}")
            
            while is_running:
                user = generate_username(mode, length)
                try:
                    available = await client(CheckUsernameRequest(user))
                    if available:
                        with open(ALL_FOUND, "a") as f: f.write(f"@{user}\n")
                        # معيار التميز (يوزر ثلاثي الرموز أو أقل)
                        if len(set(user)) <= 3:
                            with open(PREMIUM_FOUND, "a") as f: f.write(f"@{user}\n")
                            await bot.send_message(ADMIN_ID, f"💎 صيد مميز: @{user}")
                        else:
                            await bot.send_message(ADMIN_ID, f"✅ يوزر متاح: @{user}")
                except FloodWaitError as e: await asyncio.sleep(e.seconds)
                except: pass
                await asyncio.sleep(1.2)

    elif data == b"stop":
        is_running = False
        await event.edit("⏹ تم إيقاف البحث.")

    elif data == b"show_all":
        if os.path.exists(ALL_FOUND): await event.respond("كل اليوزرات:", file=ALL_FOUND)
        else: await event.answer("السجل فارغ.")

async def main():
    await client.start()
    await bot.start(bot_token=BOT_TOKEN)
    print("--- البوت والحساب متصلان بنجاح ---")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

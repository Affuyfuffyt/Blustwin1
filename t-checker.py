import random, string, os, asyncio
from telethon import TelegramClient, events, Button
from telethon.tl.functions.account import CheckUsernameRequest
from telethon.errors import FloodWaitError

# سيتم ملء هذه البيانات تلقائياً بواسطة سكريبت التثبيت
API_ID = 'API_ID_HERE'
API_HASH = 'API_HASH_HERE'
BOT_TOKEN = 'BOT_TOKEN_HERE'
ADMIN_ID = ADMIN_ID_HERE

# أسماء الملفات الجديدة
SESSION_NAME = 't_checker_user'
HISTORY_FILE = 'found_users.txt'
PREMIUM_FILE = 'premium_users.txt'

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
bot = TelegramClient('t_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

search_active = False

def generate_random(mode, length):
    if mode == "letters":
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    elif mode == "mixed":
        # حرف واحد + أرقام
        first_char = random.choice(string.ascii_lowercase)
        rest = ''.join(random.choice(string.digits) for _ in range(length-1))
        return first_char + rest
    elif mode == "alphanumeric":
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    if event.sender_id != ADMIN_ID: return
    buttons = [
        [Button.inline("🔍 بحث", b"search_menu")],
        [Button.inline("📂 اليوزرات المكتشفة", b"show_all"), Button.inline("💎 المميزة", b"show_premium")]
    ]
    await event.respond("مرحباً بك في لوحة تحكم صائد اليوزرات:", buttons=buttons)

@bot.on(events.CallbackQuery)
async def callback(event):
    global search_active
    data = event.data
    
    if data == b"search_menu":
        btns = [
            [Button.inline("🔤 حروف فقط", b"mode_letters"), Button.inline("🔢 حرف + أرقام", b"mode_mixed")],
            [Button.inline("🔡 حروف وأرقام", b"mode_alpha"), Button.inline("🛑 إيقاف", b"stop")]
        ]
        await event.edit("اختر نوع البحث:", buttons=btns)

    elif data.startswith(b"mode_"):
        mode = data.decode().split("_")[1]
        async with bot.conversation(event.sender_id) as conv:
            await conv.send_message("أرسل طول اليوزر المطلوب (مثلاً 5):")
            length = await conv.get_response()
            length = int(length.text)
            
            search_active = True
            await conv.send_message(f"🚀 بدأ البحث عن طول {length}... استخدم زر إيقاف لإنهاء العملية.")
            
            while search_active:
                user = generate_random(mode, length)
                try:
                    # نستخدم حساب المستخدم للفحص (لأنه أدق)
                    result = await client(CheckUsernameRequest(user))
                    if result:
                        with open(HISTORY_FILE, "a") as f: f.write(f"@{user}\n")
                        # معيار لليوزرات المميزة (مثلاً تكرار أو طول قصير)
                        if len(set(user)) <= 3: 
                            with open(PREMIUM_FILE, "a") as f: f.write(f"@{user}\n")
                            await bot.send_message(ADMIN_ID, f"💎 يوزر مميز: @{user}")
                        else:
                            await bot.send_message(ADMIN_ID, f"✅ متاح: @{user}")
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
                except: pass
                await asyncio.sleep(1.5)

    elif data == b"stop":
        search_active = False
        await event.respond("⏹ تم إيقاف البحث.")

# تشغيل العميلين (البوت والحساب)
async def main():
    await client.start() # سيطلب الكود هنا عند أول تشغيل
    await bot.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

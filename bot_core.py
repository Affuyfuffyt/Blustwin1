import random, string, os, asyncio
from telethon import TelegramClient, events, Button
from telethon.tl.functions.account import CheckUsernameRequest
from telethon.errors import FloodWaitError, SessionPasswordNeededError

# هذه المتغيرات سيتم ملؤها تلقائياً بواسطة سكريبت installl.sh
API_ID = API_ID_HERE
API_HASH = 'API_HASH_HERE'
BOT_TOKEN = 'TOKEN_HERE'
ADMIN_ID = ADMIN_ID_HERE

# أسماء الملفات الجديدة لتجنب التضارب
USER_SESSION = 'checker_account'
ALL_USERS_FILE = 'found_all.txt'
PREMIUM_USERS_FILE = 'premium_only.txt'

client = TelegramClient(USER_SESSION, API_ID, API_HASH)
bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

is_searching = False

def generate_user(mode, length):
    if mode == "letters":
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    elif mode == "mixed": # حرف + ارقام
        return random.choice(string.ascii_lowercase) + ''.join(random.choice(string.digits) for _ in range(length-1))
    elif mode == "alphanumeric": # حروف وارقام عشوائي
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    if event.sender_id != ADMIN_ID: return
    btns = [
        [Button.inline("🔍 بحث عن يوزرات", b"open_search")],
        [Button.inline("📂 كل اليوزرات", b"view_all"), Button.inline("💎 المميزة", b"view_premium")]
    ]
    await event.respond("🚀 أهلاً بك في بوت فحص اليوزرات المتاحة:", buttons=btns)

@bot.on(events.CallbackQuery)
async def callback_handler(event):
    global is_searching
    data = event.data
    
    if data == b"open_search":
        btns = [
            [Button.inline("🔤 حروف فقط", b"m_letters"), Button.inline("🔢 حرف + أرقام", b"m_mixed")],
            [Button.inline("🔡 حروف وأرقام", b"m_alpha")],
            [Button.inline("🛑 إيقاف البحث", b"stop_search")]
        ]
        await event.edit("اختر نوع البحث:", buttons=btns)

    elif data.startswith(b"m_"):
        mode_map = {b"m_letters": "letters", b"m_mixed": "mixed", b"m_alpha": "alphanumeric"}
        mode = mode_map[data]
        
        async with bot.conversation(event.sender_id) as conv:
            await conv.send_message("كم عدد حروف اليوزر؟ (أرسل رقم فقط)")
            msg = await conv.get_response()
            length = int(msg.text)
            
            is_searching = True
            await conv.send_message(f"✅ بدأ الفحص عن يوزرات ({length}) حرف.. سأرسل المتاح هنا.")
            
            while is_searching:
                target = generate_user(mode, length)
                try:
                    res = await client(CheckUsernameRequest(target))
                    if res:
                        with open(ALL_USERS_FILE, "a") as f: f.write(f"@{target}\n")
                        # شرط بسيط للتميز: إذا كان اليوزر يحتوي على اقل من 3 رموز مختلفة
                        if len(set(target)) <= 3:
                            with open(PREMIUM_USERS_FILE, "a") as f: f.write(f"@{target}\n")
                            await bot.send_message(ADMIN_ID, f"💎 يوزر مميز متاح: @{target}")
                        else:
                            await bot.send_message(ADMIN_ID, f"✅ متاح: @{target}")
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
                except Exception:
                    pass
                await asyncio.sleep(2) # تأخير لتجنب الحظر

    elif data == b"stop_search":
        is_searching = False
        await event.edit("⏹ تم إيقاف البحث بنجاح.")

async def main():
    # تسجيل الدخول للحساب الشخصي مع دعم التحقق بخطوتين
    await client.start()
    print("--- الحساب الشخصي متصل الآن ---")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

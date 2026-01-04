import random, string, os, asyncio, sys
from telethon import TelegramClient, events, Button
from telethon.tl.functions.account import CheckUsernameRequest
from telethon.errors import FloodWaitError

# بياناتك الثابتة المحدثة
API_ID = 33582712
API_HASH = 'b3f42765ce6e66b075bf2560bb6a148f'
BOT_TOKEN = 'TOKEN_HERE'
ADMIN_ID = ADMIN_ID_HERE

client = TelegramClient('account_session', API_ID, API_HASH)
bot = TelegramClient('bot_session', API_ID, API_HASH)

is_searching = False
checked_count = 0

def generate_user(mode, length):
    first_char = random.choice(string.ascii_lowercase)
    if mode == "letters":
        rest = ''.join(random.choice(string.ascii_lowercase) for _ in range(length - 1))
    elif mode == "mixed":
        rest = ''.join(random.choice(string.digits) for _ in range(length - 1))
    else:
        chars = string.ascii_lowercase + string.digits
        rest = ''.join(random.choice(chars) for _ in range(length - 1))
    return first_char + rest

async def hunter_engine(mode, length):
    global is_searching, checked_count
    loop_count = 0
    
    while is_searching:
        user = generate_user(mode, length)
        try:
            result = await client(CheckUsernameRequest(user))
            checked_count += 1
            loop_count += 1
            
            if result:
                await bot.send_message(ADMIN_ID, f"✅ **صيد جديد:** @{user}")
                with open('found.txt', 'a') as f: f.write(f"@{user}\n")

            # --- نظام الحماية الذكي ---
            # 1. استراحة قصيرة عشوائية بين الطلبات
            await asyncio.sleep(random.uniform(2.5, 5.5))
            
            # 2. استراحة طويلة بعد كل 50 يوزر (محاكاة لتوقف بشري)
            if loop_count >= 50:
                await bot.send_message(ADMIN_ID, "☕ **استراحة أمان:** سأتوقف لمدة 3 دقائق لتجنب الحظر.")
                await asyncio.sleep(180)
                loop_count = 0

        except FloodWaitError as e:
            await bot.send_message(ADMIN_ID, f"⚠️ **تحذير الحظر:** تيليجرام طلب الانتظار {e.seconds} ثانية. سألتزم بذلك.")
            await asyncio.sleep(e.seconds + 10)
        except Exception:
            pass

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    if event.sender_id != ADMIN_ID: return
    btns = [
        [Button.inline("▶️ بدء الصيد الآمن", b"run"), Button.inline("🛑 إيقاف", b"stop")],
        [Button.inline("🔄 ريستارت", b"restart"), Button.inline("📊 الإحصائيات", b"stats")]
    ]
    await event.respond("🛡️ **لوحة التحكم (نظام الحماية القصوى)**\nتم ضبط الإعدادات لتجنب الحظر نهائياً.", buttons=btns)

@bot.on(events.CallbackQuery)
async def callback(event):
    global is_searching, checked_count
    if event.data == b"run":
        modes = [[Button.inline("حروف", b"m_letters"), Button.inline("مختلط", b"m_alpha")]]
        await event.edit("اختر النوع:", buttons=modes)
    elif event.data.startswith(b"m_"):
        mode = event.data.decode().split('_')[1]
        is_searching = True
        checked_count = 0
        asyncio.create_task(hunter_engine(mode, 5)) # افتراضي طول 5 رموز
        await event.respond("🚀 **انطلق الصيد الآمن..** لا تقلق من الحظر.")
    elif event.data == b"stop":
        is_searching = False
        await event.answer("🛑 توقفنا.")
    elif event.data == b"stats":
        await event.answer(f"📊 فحصنا {checked_count} يوزر اليوم", alert=True)
    elif event.data == b"restart":
        os.execl(sys.executable, sys.executable, *sys.argv)

async def main():
    await client.start()
    await bot.start(bot_token=BOT_TOKEN)
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())

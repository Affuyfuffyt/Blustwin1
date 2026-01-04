import random, string, os, asyncio, sys, httpx
from telethon import TelegramClient, events, Button

# البيانات الثابتة
API_ID = 33582712
API_HASH = 'b3f42765ce6e66b075bf2560bb6a148f'
BOT_TOKEN = '8510040818:AAGiyXqTv-5IUFeQOECCyEuXPnsv4ld_EAg'
ADMIN_ID = 7852494079

# تشغيل البوت بالتوكن فقط لحماية حسابك
bot = TelegramClient('blust_final_session', API_ID, API_HASH)

is_searching = False
checked_count = 0
found_list = []

HISTORY_FILE = "blust_history.txt"
BATCH_FILE = "blust_batch.txt"

def generate_user(mode, length):
    first = random.choice(string.ascii_lowercase)
    chars = string.ascii_lowercase + string.digits
    if mode == "alpha": chars += "_"
    user = first + "".join(random.choice(chars) for _ in range(length - 1))
    if user.endswith("_"): user = user[:-1] + random.choice(string.ascii_lowercase)
    return user.replace("__", "_z")

async def check_user_web(username):
    url = f"https://t.me/{username}"
    try:
        async with httpx.AsyncClient() as client:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = await client.get(url, timeout=10, headers=headers)
            if 'If you have Telegram, you can contact' in response.text or 'tgme_page_extra' not in response.text:
                return True
            return False
    except: return False

async def main_engine(mode, length):
    global is_searching, checked_count, found_list
    while is_searching:
        user = generate_user(mode, length)
        if await check_user_web(user):
            found_list.append(f"@{user}")
            with open(HISTORY_FILE, 'a') as f: f.write(f"@{user}\n")
            await bot.send_message(ADMIN_ID, f"💎 **Blust Found:** @{user}\n🔗 https://t.me/{user}")
            if len(found_list) >= 10:
                with open(BATCH_FILE, "w") as f: f.write("\n".join(found_list))
                await bot.send_file(ADMIN_ID, BATCH_FILE, caption="📁 صيد Blust (10 يوزرات).")
                found_list = []
        checked_count += 1
        await asyncio.sleep(0.4)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    if event.sender_id != ADMIN_ID: return
    btns = [[Button.inline("🚀 بدء صيد الروابط", b"run")], [Button.inline("🛑 إيقاف", b"stop"), Button.inline("📊 إحصائيات", b"stats")]]
    await event.respond("🛡️ **نظام Blust (النسخة الصافية)**\nلا يحتاج رقم هاتف ولا يسبب حظر.", buttons=btns)

@bot.on(events.CallbackQuery)
async def callback(event):
    global is_searching
    if event.data == b"run":
        is_searching = True
        asyncio.create_task(main_engine("alpha", 5))
        await event.edit("🚀 تم بدء المحرك الآمن بنجاح.")
    elif event.data == b"stop":
        is_searching = False
        await event.answer("🛑 توقفنا.")
    elif event.data == b"stats":
        await event.answer(f"📈 فحصنا {checked_count} يوزر.", alert=True)

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())

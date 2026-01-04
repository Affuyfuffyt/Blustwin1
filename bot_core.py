import random, string, os, asyncio, sys
from telethon import TelegramClient, events, Button
from telethon.tl.functions.account import CheckUsernameRequest
from telethon.errors import FloodWaitError

# بيانات الـ API المحدثة والمفاتيح مدمجة داخلياً
API_ID = 33582712
API_HASH = 'b3f42765ce6e66b075bf2560bb6a148f'
BOT_TOKEN = 'TOKEN_HERE'
ADMIN_ID = ADMIN_ID_HERE

client = TelegramClient('account_session', API_ID, API_HASH)
bot = TelegramClient('bot_session', API_ID, API_HASH)

is_searching = False
checked_today = 0

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
    global is_searching, checked_today
    session_checks = 0
    
    while is_searching:
        user = generate_user(mode, length)
        try:
            result = await client(CheckUsernameRequest(user))
            checked_today += 1
            session_checks += 1
            
            if result:
                with open('found.txt', 'a') as f: f.write(f"@{user}\n")
                await bot.send_message(ADMIN_ID, f"🎯 **صيد جديد:** @{user}")

            # 1. فاصل زمني عشوائي (آمن جداً)
            await asyncio.sleep(random.uniform(2.0, 5.0))
            
            # 2. نظام الاستراحة الإجباري بعد كل 100 فحص
            if session_checks >= 100:
                await bot.send_message(ADMIN_ID, "😴 **استراحة أمان:** سأتوقف 10 دقائق لتجنب كشف الحساب.")
                await asyncio.sleep(600)
                session_checks = 0

        except FloodWaitError as e:
            await bot.send_message(ADMIN_ID, f"⚠️ **تحذير الحظر:** تيليجرام طلب الانتظار {e.seconds} ثانية. سألتزم بذلك لضمان سلامة حسابك.")
            await asyncio.sleep(e.seconds + 60)
        except Exception:
            pass

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    if event.sender_id != ADMIN_ID: return
    
    # ضمان ظهور الأزرار بوضوح
    btns = [
        [Button.inline("▶️ بدء الصيد الآمن", b"run"), Button.inline("🛑 إيقاف فوراً", b"stop")],
        [Button.inline("🔄 ريستارت النظام", b"restart"), Button.inline("📊 إحصائيات", b"stats")]
    ]
    await event.respond("🛡️ **نظام الصيد الخفي (Anti-Ban)**\n\nتم تفعيل خوارزمية محاكاة السلوك البشري لتجنب الحظر.", buttons=btns)

@bot.on(events.CallbackQuery)
async def callback(event):
    global is_searching, checked_today
    data = event.data

    if data == b"run":
        modes = [[Button.inline("🔤 حروف", b"m_letters"), Button.inline("🔡 عشوائي", b"m_alpha")]]
        await event.edit("اختر النوع لبدء الصيد الآمن:", buttons=modes)

    elif data.startswith(b"m_"):
        mode = data.decode().split('_')[1]
        async with bot.conversation(event.sender_id) as conv:
            await conv.send_message("🔢 كم طول اليوزر المطلوب؟ (يفضل 5 أو 6)")
            res = await conv.get_response()
            try:
                length = int(res.text)
                is_searching = True
                asyncio.create_task(hunter_engine(mode, length))
                await conv.send_message(f"🚀 **تم تفعيل المحرك الآمن..** سيصلك المتاح هنا.")
            except:
                await conv.send_message("❌ ارسل رقم فقط.")

    elif data == b"stop":
        is_searching = False
        await event.answer("🛑 تم إيقاف الصيد.", alert=True)

    elif data == b"stats":
        await event.answer(f"📈 تم فحص {checked_today} يوزر في هذه الجلسة.", alert=True)

    elif data == b"restart":
        await event.respond("🔄 جارِ إعادة التشغيل...")
        os.execl(sys.executable, sys.executable, *sys.argv)

async def main():
    await client.start()
    await bot.start(bot_token=BOT_TOKEN)
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())

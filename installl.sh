#!/bin/bash

# تنظيف شامل لكل ملفات الجلسات القديمة (لأن الحظر يلتصق بملف الجلسة)
rm -rf /root/hunter_stealth
rm -f /root/*.session
mkdir /root/hunter_stealth
cd /root/hunter_stealth

echo "--- تثبيت الصائد الخفي (نسخة الحماية القصوى) ---"

apt update && apt upgrade -y
apt install -y python3 python3-pip curl
pip3 install telethon

curl -Ls https://raw.githubusercontent.com/Affuyfuffyt/Blustwin1/refs/heads/main/bot_core.py -o bot_core.py

read -p "🎯 Token: " token
read -p "🎯 Admin ID: " adminid

sed -i "s/TOKEN_HERE/$token/g" bot_core.py
sed -i "s/ADMIN_ID_HERE/$adminid/g" bot_core.py

echo "--- جارِ التشغيل.. أدخل الرقم والكود ---"
python3 bot_core.py

here#!/bin/bash

# 1. تنظيف السيرفر من النسخ القديمة
rm -rf /root/t_checker
mkdir /root/t_checker
cd /root/t_checker

# 2. تثبيت المتطلبات الأساسية
echo "--- جارِ تثبيت المتطلبات (Python & Telethon) ---"
apt update && apt upgrade -y
apt install -y python3 python3-pip git curl
pip3 install telethon

# 3. تحميل ملف البوت البرمجي من GitHub (تأكد من تسمية الملف البرمجي bot_core.py ورفعه بجانب install.sh)
curl -Ls https://raw.githubusercontent.com/Affuyfuffyt/Blustwin1/refs/heads/main/bot_core.py -o bot_core.py

# 4. طلب البيانات من المستخدم بصورة تفاعلية
echo "-----------------------------------------------"
read -p "Enter BOT_TOKEN: " token
read -p "Enter API_ID: " apiid
read -p "Enter API_HASH: " aphash
read -p "Enter ADMIN_ID: " adminid
echo "-----------------------------------------------"

# 5. حقن البيانات داخل ملف البوت
sed -i "s/TOKEN_HERE/$token/g" bot_core.py
sed -i "s/API_ID_HERE/$apiid/g" bot_core.py
sed -i "s/API_HASH_HERE/$aphash/g" bot_core.py
sed -i "s/ADMIN_ID_HERE/$adminid/g" bot_core.py

# 6. تشغيل البوت (في أول مرة سيطلب الرقم والكود والتحقق بخطوتين)
echo "--- سيتم الآن طلب رقم الهاتف لربط الحساب الشخصي ---"
python3 bot_core.py

#!/bin/bash

# 1. تنظيف السيرفر
rm -rf /root/tg_hunter
mkdir /root/tg_hunter
cd /root/tg_hunter

echo "------------------------------------------------"
echo "    جاري تثبيت نظام صيد اليوزرات الاحترافي      "
echo "------------------------------------------------"

# 2. تثبيت المكتبات
apt update && apt upgrade -y
apt install -y python3 python3-pip curl
pip3 install telethon

# 3. تحميل الكود من GitHub
curl -Ls https://raw.githubusercontent.com/Affuyfuffyt/Blustwin1/refs/heads/main/bot_core.py -o bot_core.py

# 4. طلب البيانات الأساسية فقط
read -p "🎯 أدخل Token البوت: " token
read -p "🎯 أدخل ID حسابك (Admin): " adminid

# 5. حقن البيانات في الملف
sed -i "s/TOKEN_HERE/$token/g" bot_core.py
sed -i "s/ADMIN_ID_HERE/$adminid/g" bot_core.py

# 6. التشغيل وطلب الرقم/الكود/2FA
echo "------------------------------------------------"
echo " سيتم الآن ربط حسابك الشخصي (أدخل الرقم والكود) "
echo "------------------------------------------------"
python3 bot_core.py

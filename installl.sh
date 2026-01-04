#!/bin/bash

# تنظيف شامل للملفات والجلسات القديمة
rm -rf /root/tg_pro_hunter
rm -f /root/*.session
mkdir /root/tg_pro_hunter
cd /root/tg_pro_hunter

echo "------------------------------------------------"
echo "   جاري تثبيت الصائد الاحترافي ببيانات الـ API الجديدة   "
echo "------------------------------------------------"

# تثبيت المتطلبات
apt update && apt upgrade -y
apt install -y python3 python3-pip curl
pip3 install telethon

# تحميل الكود من مستودعك
curl -Ls https://raw.githubusercontent.com/Affuyfuffyt/Blustwin1/refs/heads/main/bot_core.py -o bot_core.py

# طلب البيانات الأساسية
read -p "🎯 أدخل Token البوت: " token
read -p "🎯 أدخل ID حسابك (Admin): " adminid

# حقن البيانات
sed -i "s/TOKEN_HERE/$token/g" bot_core.py
sed -i "s/ADMIN_ID_HERE/$adminid/g" bot_core.py

echo "------------------------------------------------"
echo "  سيطلب منك الآن الرقم والكود لتسجيل الدخول   "
echo "------------------------------------------------"

python3 bot_core.py

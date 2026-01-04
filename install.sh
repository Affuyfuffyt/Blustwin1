#!/bin/bash

# تنظيف الملفات القديمة
rm -rf /root/t-checker
mkdir /root/t-checker
cd /root/t-checker

echo "--- تنصيب صائد اليوزرات الاحترافي ---"

# تثبيت المتطلبات
apt update
apt install -y python3 python3-pip git
pip3 install telethon

# طلب البيانات من المستخدم
read -p "أدخل BOT_TOKEN: " token
read -p "أدخل API_ID: " apiid
read -p "أدخل API_HASH: " aphash
read -p "أدخل ID المطور: " adminid

# تحميل كود البوت (يمكنك رفعه على كيت هب واستبدال الرابط أدناه)
# wget https://raw.githubusercontent.com/username/repo/main/t-checker.py

# تعديل البيانات داخل الملف
sed -i "s/API_ID_HERE/'$apiid'/g" t-checker.py
sed -i "s/API_HASH_HERE/'$aphash'/g" t-checker.py
sed -i "s/BOT_TOKEN_HERE/'$token'/g" t-checker.py
sed -i "s/ADMIN_ID_HERE/$adminid/g" t-checker.py

echo "--- جاري تشغيل البوت للمرة الأولى لربط الحساب ---"
python3 t-checker.py

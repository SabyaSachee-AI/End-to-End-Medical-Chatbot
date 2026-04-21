FROM python:3.10-slim

WORKDIR /app

# ফাইল কপি করা এবং ডিপেনডেন্সি ইন্সটল করা
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Gunicorn কনফিগারেশন: 
# --workers 1: মেমরি ব্যবহারের চাপ কমাতে মাত্র ১টি ওয়ার্কার চালানো হবে।
# --timeout 120: এআই মডেল রেসপন্স দিতে সময় নিতে পারে, তাই টাইমআউট বাড়িয়ে দেওয়া হয়েছে।
CMD ["gunicorn", "--workers", "1", "--timeout", "120", "--bind", "0.0.0.0:8080", "app:app"]

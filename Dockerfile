# ১. পাইথনের লাইটওয়েট ইমেজ ব্যবহার করছি
FROM python:3.10-slim

# ২. কন্টেইনারের ভেতরে কাজের ডিরেক্টরি সেট করছি
WORKDIR /app

# ৩. প্রথমে শুধু requirements.txt কপি করছি (ডকার লেয়ার ক্যাশিংয়ের জন্য এটি জরুরি)
COPY requirements.txt .

# ৪. প্যাকেজগুলো ইন্সটল করছি
RUN pip install --no-cache-dir -r requirements.txt

# ৫. বাকি সব ফাইল কপি করছি
COPY . .

# ৬. পোর্ট ৮০৮০ এক্সপোজ করছি (এটি AWS এবং আপনার app.py এর পোর্টের সাথে মিল রাখতে হবে)
EXPOSE 8080

# ৭. আপনার অনুরোধ অনুযায়ী কমান্ডটি যোগ করা হলো
CMD ["python", "app.py"]

FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Gunicorn ব্যবহার করছি প্রোডাকশন সার্ভার হিসেবে
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]

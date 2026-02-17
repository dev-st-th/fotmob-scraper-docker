FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium --with-deps

COPY . .

# ปรับตามลักษณะการใช้งาน (ถ้าเป็น Web Service ต้องสั่งรัน server)
CMD ["python", "main.py"]
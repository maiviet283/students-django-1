# Sử dụng Python image chính thức
FROM python:3.13-slim

# Đặt thư mục làm việc
WORKDIR /app

# Copy file requirements.txt và cài đặt các dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Mở cổng 8000 cho ứng dụng
EXPOSE 8000

# Lệnh khởi chạy server Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

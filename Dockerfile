# Dockerfile

# Python 3.11 이미지 사용
FROM python:3.11

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 Python 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# gunicorn으로 Django 서비스 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]

# CRON 적용
RUN apt-get update && apt-get install -y cron
COPY command.cron /etc/cron.d/command.cron
RUN chmod 0644 /etc/cron.d/command.cron
RUN crontab /etc/cron.d/command.cron

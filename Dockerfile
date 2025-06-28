FROM python:3.11-slim

# 필수 라이브러리 설치
RUN apt-get update && apt-get install -y \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 지정
WORKDIR /app

# 코드 복사
COPY . .

# 패키지 설치
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 포트 지정
ENV PORT=5000

# 서버 실행
CMD ["python", "app.py"]

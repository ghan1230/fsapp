#!/bin/bash

# Heroku 배포 스크립트

echo "🚀 Heroku 배포 시작..."

# 1. Heroku 로그인 확인
echo "📝 Heroku 로그인 확인 중..."
heroku whoami || {
    echo "❌ Heroku에 로그인되어 있지 않습니다."
    echo "heroku login 명령어를 실행하세요."
    exit 1
}

# 2. 앱 이름 입력
read -p "Heroku 앱 이름을 입력하세요: " APP_NAME

# 3. 앱 생성 (이미 존재하면 스킵)
echo "📦 Heroku 앱 생성 중..."
heroku create $APP_NAME 2>/dev/null || echo "앱이 이미 존재합니다."

# 4. 환경변수 설정
echo "🔑 환경변수 설정 중..."
read -p "Open DART API 키: " DART_KEY
read -p "Finnhub API 키: " FINNHUB_KEY
read -p "Gemini API 키 (선택사항, Enter로 스킵): " GEMINI_KEY

heroku config:set OPEN_DART_API_KEY=$DART_KEY --app $APP_NAME
heroku config:set FINNHUB_API_KEY=$FINNHUB_KEY --app $APP_NAME

if [ ! -z "$GEMINI_KEY" ]; then
    heroku config:set GEMINI_API_KEY=$GEMINI_KEY --app $APP_NAME
    heroku config:set GEMINI_MODEL=gemini-2.5-pro --app $APP_NAME
fi

# 5. Git 커밋
echo "📝 Git 커밋 중..."
git add .
git commit -m "Deploy to Heroku" || echo "변경사항이 없습니다."

# 6. Heroku에 배포
echo "🚀 Heroku에 배포 중..."
git push heroku main || git push heroku master

# 7. 앱 열기
echo "✅ 배포 완료!"
echo "🌐 앱 열기..."
heroku open --app $APP_NAME

echo "📊 로그 확인: heroku logs --tail --app $APP_NAME"

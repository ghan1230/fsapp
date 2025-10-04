# 🚀 Render 배포 가이드

## 1. GitHub에 코드 푸시

```bash
# Git 초기화 (아직 안했다면)
git init
git add .
git commit -m "Initial commit"

# GitHub 저장소 생성 후
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

## 2. Render 계정 생성

https://render.com 에서 가입

## 3. 새 Web Service 생성

1. Dashboard에서 "New +" 클릭
2. "Web Service" 선택
3. GitHub 저장소 연결
4. 저장소 선택

## 4. 설정

### Basic Settings
- **Name**: `financial-analysis` (원하는 이름)
- **Region**: `Singapore` (한국과 가까움)
- **Branch**: `main`
- **Root Directory**: (비워두기)
- **Runtime**: `Python 3`

### Build & Deploy
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

## 5. 환경변수 설정

Environment 탭에서 추가:

```
OPEN_DART_API_KEY = your_dart_api_key_here
FINNHUB_API_KEY = your_finnhub_api_key_here
GEMINI_API_KEY = your_gemini_api_key_here
GEMINI_MODEL = gemini-2.5-pro
FLASK_ENV = production
```

## 6. 배포

"Create Web Service" 클릭

자동으로 배포가 시작됩니다!

## 7. 배포 확인

- 배포 로그 확인
- 앱 URL 클릭하여 접속
- 모든 기능 테스트

## 8. 자동 배포 설정

GitHub에 push하면 자동으로 재배포됩니다!

```bash
git add .
git commit -m "Update features"
git push
```

## 🎉 완료!

앱이 https://your-app-name.onrender.com 에서 실행됩니다!

## 📊 모니터링

- **Logs**: Render Dashboard에서 실시간 로그 확인
- **Metrics**: CPU, 메모리 사용량 모니터링
- **Alerts**: 이메일 알림 설정 가능

## 💰 비용

- **Free Tier**: 750시간/월 무료
- **Starter**: $7/월 (항상 실행)

## 🔧 문제 해결

### 배포 실패
1. 로그 확인
2. requirements.txt 확인
3. 환경변수 확인

### 앱이 느림
1. Free tier는 15분 후 sleep
2. 첫 요청 시 깨어나는데 시간 소요
3. Starter 플랜으로 업그레이드 고려

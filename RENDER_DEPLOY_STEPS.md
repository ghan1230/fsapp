# 🚀 Render 배포 단계별 가이드

## ✅ 준비 완료!

GitHub 저장소: https://github.com/ghan1230/fsapp.git

---

## 📋 배포 단계

### 1단계: Render 계정 생성

1. https://render.com 접속
2. "Get Started" 클릭
3. GitHub 계정으로 로그인

---

### 2단계: New Web Service 생성

1. Dashboard에서 **"New +"** 버튼 클릭
2. **"Web Service"** 선택
3. **"Build and deploy from a Git repository"** 선택
4. **"Next"** 클릭

---

### 3단계: GitHub 저장소 연결

1. **"Connect a repository"** 섹션에서
2. GitHub 계정 연결 (처음이면 권한 승인)
3. 저장소 검색: `fsapp`
4. **"Connect"** 버튼 클릭

---

### 4단계: 서비스 설정

#### Basic Settings
```
Name: fsapp
Region: Singapore (한국과 가까움)
Branch: main
Root Directory: (비워두기)
Runtime: Python 3
```

#### Build & Deploy Settings
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

#### Instance Type
```
Free (무료 플랜 선택)
```

---

### 5단계: 환경변수 설정

**Environment** 탭에서 다음 환경변수를 추가:

```
FLASK_ENV = production
OPEN_DART_API_KEY = your_dart_api_key_here
```

**중요**: 
- `OPEN_DART_API_KEY`는 **필수**입니다 (한국 주식 회사 코드 다운로드용)
- 다른 API 키는 설정하지 않습니다 (사용자가 각자 브라우저에서 입력)
- DART API 키 발급: https://opendart.fss.or.kr/

---

### 6단계: 배포 시작

1. **"Create Web Service"** 버튼 클릭
2. 자동으로 배포 시작
3. 로그 확인 (5-10분 소요)

---

## 📊 배포 진행 상황

### 로그에서 확인할 내용

```
==> Cloning from https://github.com/ghan1230/fsapp...
==> Checking out commit ecdd90d...
==> Running build command 'pip install -r requirements.txt'...
==> Installing dependencies...
==> Build successful!
==> Starting service with 'gunicorn app:app'...
==> Your service is live 🎉
```

---

## ✅ 배포 완료 확인

### 1. URL 확인
배포 완료 후 URL이 생성됩니다:
```
https://fsapp-xxxx.onrender.com
```

### 2. 서비스 테스트
1. URL 클릭하여 접속
2. 메인 페이지 로딩 확인
3. "⚙️ 설정" 페이지 접속
4. API 키 입력 및 테스트

---

## 🔧 배포 후 설정

### 1. README 업데이트

```bash
# 로컬에서 README.md 수정
# 배포 URL 업데이트
https://fsapp-xxxx.onrender.com

# Git 커밋 및 푸시
git add README.md
git commit -m "Update deployment URL"
git push
```

### 2. 자동 재배포

Render는 GitHub push 시 자동으로 재배포됩니다!

---

## 📱 사용자 안내

### 배포 완료 후 사용자에게 안내할 내용

```markdown
## 🎉 서비스 오픈!

### 접속 URL
https://fsapp-xxxx.onrender.com

### 시작하기
1. 위 URL 접속
2. "⚙️ 설정" 버튼 클릭
3. API 키 발급 및 입력 (무료, 10분)
   - Open DART API: https://opendart.fss.or.kr/
   - Finnhub API: https://finnhub.io/register
   - Gemini AI API: https://aistudio.google.com/app/apikey (선택)
4. 모든 기능 무료 사용!

### 자세한 가이드
https://github.com/ghan1230/fsapp/blob/main/USER_API_KEY_GUIDE.md
```

---

## 🔍 모니터링

### Render Dashboard에서 확인

1. **Logs**: 실시간 로그 확인
2. **Metrics**: CPU, 메모리 사용량
3. **Events**: 배포 이력

### 로그 확인 방법

```bash
# Render Dashboard → Logs 탭
# 또는 CLI 사용
render logs -s fsapp
```

---

## ⚠️ 주의사항

### Free Tier 제한

- **15분 비활성 시 Sleep**: 첫 요청 시 깨어나는데 30초 소요
- **750시간/월**: 충분한 시간
- **대역폭**: 100GB/월

### Sleep 방지 (선택사항)

1. **Uptime Robot** 사용
   - https://uptimerobot.com
   - 5분마다 핑 전송
   - 무료 플랜 사용 가능

2. **Cron Job** 설정
   ```bash
   # 5분마다 접속
   */5 * * * * curl https://fsapp-xxxx.onrender.com
   ```

---

## 🔄 업데이트 방법

### 코드 수정 후 배포

```bash
# 1. 코드 수정
# 2. Git 커밋
git add .
git commit -m "Update features"

# 3. GitHub 푸시
git push

# 4. Render에서 자동 재배포 (5-10분)
```

---

## 🆘 문제 해결

### 배포 실패 시

1. **로그 확인**
   - Render Dashboard → Logs
   - 에러 메시지 확인

2. **requirements.txt 확인**
   ```bash
   pip freeze > requirements.txt
   git add requirements.txt
   git commit -m "Update requirements"
   git push
   ```

3. **Python 버전 확인**
   - runtime.txt: `python-3.11.0`

### 앱이 작동하지 않을 때

1. **로그 확인**
   - 500 에러: 서버 로그 확인
   - 404 에러: 라우트 확인

2. **환경변수 확인**
   - FLASK_ENV=production 설정 확인

3. **재배포**
   - Manual Deploy 버튼 클릭

---

## 💰 비용

### Free Tier
- **비용**: $0/월
- **제한**: 750시간/월, 15분 후 Sleep
- **충분**: 개인 프로젝트, 포트폴리오

### Starter Tier (필요시)
- **비용**: $7/월
- **장점**: 항상 실행, Sleep 없음
- **추천**: 실제 서비스 운영 시

---

## 🎯 다음 단계

### 1. 도메인 연결 (선택사항)

1. 도메인 구매 (Namecheap, GoDaddy 등)
2. Render Dashboard → Settings → Custom Domain
3. DNS 설정

### 2. HTTPS 인증서

- Render에서 자동으로 제공
- Let's Encrypt 사용
- 추가 설정 불필요

### 3. 모니터링 설정

- Sentry 연동 (에러 추적)
- Google Analytics (사용자 분석)
- Uptime Robot (가동 시간 모니터링)

---

## ✅ 배포 체크리스트

- [ ] Render 계정 생성
- [ ] GitHub 저장소 연결
- [ ] 서비스 설정 완료
- [ ] 배포 성공 확인
- [ ] URL 접속 테스트
- [ ] 설정 페이지 확인
- [ ] API 키 테스트
- [ ] 모든 기능 확인
- [ ] README URL 업데이트
- [ ] 사용자 안내 문서 작성

---

## 🎉 배포 완료!

**축하합니다!** 이제 전 세계 어디서나 서비스를 사용할 수 있습니다!

### 공유하기
- GitHub README에 배포 URL 추가
- SNS에 공유
- 포트폴리오에 추가

### 피드백 수집
- GitHub Issues 활성화
- 사용자 의견 수렴
- 지속적인 개선

---

**문의사항이 있으시면 GitHub Issues에 남겨주세요!**

https://github.com/ghan1230/fsapp/issues

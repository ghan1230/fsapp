# ✅ 배포 체크리스트 (간단 버전)

## 🚀 Render 배포 - 5분 완성

### 1단계: GitHub 준비
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2단계: Render 설정
1. https://render.com 접속 및 로그인
2. "New +" → "Web Service"
3. GitHub 저장소 연결

### 3단계: 서비스 설정
```
Name: fsapp (원하는 이름)
Region: Singapore
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

### 4단계: 환경변수 (중요!)
```
OPEN_DART_API_KEY = your_dart_api_key_here
```

**이것만 설정하면 됩니다!**
- 다른 API 키는 사용자가 브라우저에서 입력
- DART API 키 발급: https://opendart.fss.or.kr/ (무료, 1분)

### 5단계: 배포
"Create Web Service" 클릭 → 완료!

---

## 📊 배포 후 확인

### 로그 확인 (Render Dashboard)
```
✅ [INFO] corp_codes.json not found. Downloading...
✅ 📥 회사코드 파일 다운로드 중...
✅ 📈 총 114147개 회사 정보 추출 완료
✅ [INFO] Loaded 114147 companies
✅ Running on http://0.0.0.0:10000
```

### 기능 테스트
1. ✅ 앱 URL 접속
2. ✅ "삼성전자" 검색 → 결과 5개 표시
3. ✅ 설정 페이지 접속
4. ✅ API 키 입력 및 테스트

---

## ⚠️ 문제 해결

### "검색 결과가 없습니다"
→ 로그에서 corp_codes.json 생성 확인
→ OPEN_DART_API_KEY 환경변수 확인

### 앱이 시작되지 않음
→ requirements.txt 확인
→ gunicorn 설치 확인 (requirements.txt에 포함)

### 느린 시작
→ 정상 (첫 시작 시 corp_codes.json 생성 중)
→ 약 30초 대기

---

## 🎯 완료!

**배포 URL**: https://your-app.onrender.com

**다음 단계**:
1. README.md에 배포 URL 추가
2. 사용자에게 공유
3. GitHub Issues 활성화

---

## 📚 상세 문서

더 자세한 내용은 다음 문서를 참고하세요:
- [DEPLOYMENT_PROCESS.md](./DEPLOYMENT_PROCESS.md) - 배포 프로세스 상세
- [RENDER_DEPLOY_STEPS.md](./RENDER_DEPLOY_STEPS.md) - Render 단계별 가이드
- [USER_API_KEY_GUIDE.md](./USER_API_KEY_GUIDE.md) - 사용자 가이드

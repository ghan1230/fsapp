# 📊 재무제표 시각화 애플리케이션

한국 및 미국 주식의 재무제표를 시각화하고 AI 분석을 제공하는 웹 애플리케이션입니다.

**🔑 각 사용자가 자신의 API 키를 사용하므로 완전 무료로 사용 가능합니다!**

## ✨ 주요 기능

### 🇰🇷 한국 주식
- 재무제표 조회 및 시각화
- 연도별 비교 분석
- 주가 차트
- AI 재무제표 분석

### 🇺🇸 미국 주식
- 실시간 주가 및 재무 지표
- **뉴스 통합** (감성 분석 + 필터링)
- **배당 정보** (성장률 + 캘린더)
- **동종 업계 비교**
- AI 투자 분석

## 🚀 빠른 시작 (사용자)

### 1. 서비스 접속
https://fsapp.onrender.com (배포 후 URL 업데이트)

### 2. API 키 발급 (무료, 10분 소요)

#### Open DART API (필수)
1. https://opendart.fss.or.kr/ 접속
2. 회원가입 (무료)
3. 인증키 신청 → 이메일로 즉시 수신
4. **사용량**: 20,000 requests/일 (무료)

#### Finnhub API (필수)
1. https://finnhub.io/register 접속
2. 이메일로 회원가입 (무료)
3. Dashboard에서 API Key 확인
4. **사용량**: 60 calls/분 (무료)

#### Gemini AI API (선택사항)
1. https://aistudio.google.com/app/apikey 접속
2. Google 계정으로 로그인
3. "Create API Key" 클릭
4. **사용량**: 1,500 requests/일 (무료)
5. **참고**: AI 분석 기능에만 사용, 없어도 다른 기능 사용 가능

### 3. API 키 설정
1. 서비스 접속
2. "⚙️ 설정" 버튼 클릭
3. 발급받은 API 키 입력
4. "💾 저장" 버튼 클릭
5. "🧪 테스트" 버튼으로 확인

### 4. 서비스 사용
모든 기능을 무료로 사용하세요! 🎉

**자세한 내용**: [USER_API_KEY_GUIDE.md](./USER_API_KEY_GUIDE.md)

---

## 💻 로컬 개발 (개발자)

### 1. 저장소 클론
```bash
git clone https://github.com/ghan1230/fsapp.git
cd fsapp
```

### 2. 가상환경 생성
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 실행
```bash
python app.py
```

브라우저에서 http://localhost:5000 접속

**참고**: 로컬 개발 시에도 API 키는 브라우저의 설정 페이지에서 입력합니다.

## 🌐 배포 (개발자)

**사용자 API 키 방식**이므로 서버에 API 키를 설정할 필요가 없습니다!

### Render 배포 (추천)
1. GitHub 저장소 연결
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `gunicorn app:app`
4. 환경변수: 설정 불필요! (사용자가 각자 API 키 입력)

자세한 내용: [DEPLOYMENT_USER_API.md](./DEPLOYMENT_USER_API.md)

### 다른 플랫폼
- **Heroku**: [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
- **Railway**: 동일한 방식
- **Vercel**: 서버리스 배포

## 📚 문서

- [사용 가이드](./사용가이드.md)
- [배포 가이드](./DEPLOYMENT_GUIDE.md)
- [새로운 기능](./NEW_FEATURES.md)
- [추가 기능](./ADDITIONAL_FEATURES.md)
- [구현 요약](./IMPLEMENTATION_SUMMARY.md)

## 🛠️ 기술 스택

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Charts**: Chart.js
- **APIs**: Open DART, Finnhub, Yahoo Finance, Gemini AI

## 📊 주요 기능 상세

### 뉴스 필터링
- 긍정/부정/중립/전체 필터
- 감성 분석 자동 제공
- 최근 30일 뉴스

### 배당 정보
- 배당 수익률 계산
- 배당 성장률 (CAGR)
- 다음 배당일 예측
- 배당 히스토리 차트

### 동종 업계 비교
- 같은 산업군 기업 비교
- P/E, P/B, ROE 비교
- 상대적 밸류에이션 분석

## 🤝 기여

이슈와 풀 리퀘스트를 환영합니다!

## 📄 라이선스

MIT License

## 🔒 개인정보 보호

- ✅ API 키는 브라우저의 localStorage에만 저장
- ✅ 서버로 전송되거나 저장되지 않음
- ✅ 다른 사용자와 공유되지 않음
- ⚠️ 공용 컴퓨터에서는 사용 후 반드시 초기화

## 👤 작성자

ghan1230

## 🙏 감사의 말

- Open DART API
- Finnhub API
- Yahoo Finance
- Google Gemini AI

## 📞 문의

- GitHub Issues: https://github.com/ghan1230/fsapp/issues
- Email: ghan1230@gmail.com

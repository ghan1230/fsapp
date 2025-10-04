# 📊 재무제표 시각화 애플리케이션

한국 및 미국 주식의 재무제표를 시각화하고 AI 분석을 제공하는 웹 애플리케이션입니다.

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

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone https://github.com/yourusername/financial-analysis.git
cd financial-analysis
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

### 4. 환경변수 설정
`.env` 파일 생성:
```env
OPEN_DART_API_KEY=your_dart_api_key
FINNHUB_API_KEY=your_finnhub_api_key
GEMINI_API_KEY=your_gemini_api_key
```

### 5. 실행
```bash
python app.py
```

브라우저에서 http://localhost:5000 접속

## 📋 API 키 발급

### 필수
- **Open DART API**: https://opendart.fss.or.kr/
- **Finnhub API**: https://finnhub.io/

### 선택사항
- **Gemini AI API**: https://aistudio.google.com/

## 🌐 배포

자세한 배포 가이드는 [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)를 참조하세요.

### 추천 플랫폼
- **Render**: 무료, GitHub 연동
- **Heroku**: 안정적, 검증됨
- **Railway**: 빠르고 현대적

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

## 👤 작성자

Your Name

## 🙏 감사의 말

- Open DART API
- Finnhub API
- Yahoo Finance
- Google Gemini AI

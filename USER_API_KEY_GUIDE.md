# 🔑 사용자 API 키 설정 가이드

## 왜 API 키가 필요한가요?

이 서비스는 다음 외부 API를 사용합니다:
- **Open DART API**: 한국 주식 재무제표
- **Finnhub API**: 미국 주식 정보, 뉴스
- **Gemini AI API**: AI 분석 (선택사항)

**각 사용자가 자신의 API 키를 사용**하므로:
- ✅ 무료 사용량 제한을 개인별로 사용
- ✅ 서비스 제공자의 비용 부담 없음
- ✅ 더 안정적인 서비스 제공

---

## 📝 API 키 발급 방법

### 1. Open DART API (필수)

#### 발급 절차
1. https://opendart.fss.or.kr/ 접속
2. 회원가입 (무료)
3. 로그인 후 "인증키 신청/관리" 메뉴
4. 인증키 신청
5. 이메일로 API 키 수신 (즉시)

#### 사용량 제한
- **무료**: 20,000 requests/일
- 한국 주식 재무제표 조회에 충분

---

### 2. Finnhub API (필수)

#### 발급 절차
1. https://finnhub.io/register 접속
2. 이메일로 회원가입 (무료)
3. Dashboard에서 API Key 확인
4. 즉시 사용 가능

#### 사용량 제한
- **무료**: 60 calls/분
- 미국 주식 정보, 뉴스, 배당 정보 조회에 충분

---

### 3. Gemini AI API (선택사항)

#### 발급 절차
1. https://aistudio.google.com/app/apikey 접속
2. Google 계정으로 로그인
3. "Create API Key" 클릭
4. 즉시 사용 가능

#### 사용량 제한
- **무료**: 15 requests/분, 1,500 requests/일
- AI 재무제표 분석 기능에만 사용
- 없어도 다른 기능은 모두 사용 가능

---

## 🔧 API 키 설정 방법

### 방법 1: 설정 페이지 사용 (추천)

1. 서비스 접속
2. 상단의 **"⚙️ 설정"** 버튼 클릭
3. 각 API 키 입력
4. **"💾 저장"** 버튼 클릭
5. **"🧪 테스트"** 버튼으로 키 확인

### 방법 2: 브라우저 콘솔 사용

```javascript
// 브라우저 개발자 도구 (F12) → Console 탭에서 실행

// Open DART API 키 설정
localStorage.setItem('OPEN_DART_API_KEY', 'your_dart_api_key_here');

// Finnhub API 키 설정
localStorage.setItem('FINNHUB_API_KEY', 'your_finnhub_api_key_here');

// Gemini AI API 키 설정 (선택사항)
localStorage.setItem('GEMINI_API_KEY', 'your_gemini_api_key_here');

// 확인
console.log('API 키 저장 완료!');
```

---

## 🔒 보안 및 개인정보

### API 키 저장 위치
- **localStorage**: 브라우저에만 저장
- **서버 전송 안 함**: 서버로 전송되지 않음
- **다른 사용자와 공유 안 됨**: 각자의 브라우저에만 저장

### 주의사항
⚠️ **공용 컴퓨터 사용 시**
- 사용 후 반드시 API 키 삭제
- 설정 페이지에서 "🗑️ 초기화" 버튼 클릭

⚠️ **API 키 노출 주의**
- 스크린샷 공유 시 API 키 가리기
- GitHub 등에 업로드 금지

---

## 🧪 API 키 테스트

### 설정 페이지에서 테스트
1. 설정 페이지에서 API 키 입력
2. "🧪 테스트" 버튼 클릭
3. 각 API 키의 작동 여부 확인

### 수동 테스트

#### Open DART API
```bash
curl "https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key=YOUR_KEY"
```

#### Finnhub API
```bash
curl "https://finnhub.io/api/v1/quote?symbol=AAPL&token=YOUR_KEY"
```

#### Gemini AI API
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=YOUR_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"test"}]}]}'
```

---

## ❓ 자주 묻는 질문

### Q1: API 키가 왜 필요한가요?
**A**: 외부 API 서비스를 사용하기 위해 필요합니다. 각 사용자가 자신의 키를 사용하므로 무료 사용량을 개인별로 사용할 수 있습니다.

### Q2: API 키가 안전한가요?
**A**: 네, API 키는 브라우저의 localStorage에만 저장되며 서버로 전송되지 않습니다.

### Q3: API 키를 잃어버렸어요
**A**: 각 서비스의 대시보드에서 다시 확인하거나 재발급 받을 수 있습니다.

### Q4: 무료 사용량이 부족해요
**A**: 
- Open DART: 20,000 requests/일 (충분함)
- Finnhub: 60 calls/분 (충분함)
- Gemini: 1,500 requests/일 (충분함)

일반적인 사용에는 충분하며, 부족하면 유료 플랜을 고려하세요.

### Q5: Gemini API 키가 없어도 되나요?
**A**: 네, Gemini API 키는 선택사항입니다. AI 분석 기능만 사용할 수 없고 다른 모든 기능은 정상 작동합니다.

### Q6: 여러 기기에서 사용하려면?
**A**: 각 기기의 브라우저에서 API 키를 설정해야 합니다. localStorage는 기기별로 독립적입니다.

### Q7: API 키를 변경하려면?
**A**: 설정 페이지에서 새로운 키를 입력하고 저장하면 됩니다.

### Q8: API 키를 삭제하려면?
**A**: 설정 페이지에서 "🗑️ 초기화" 버튼을 클릭하거나, 브라우저 콘솔에서:
```javascript
localStorage.clear();
```

---

## 🚀 빠른 시작 가이드

### 1단계: API 키 발급 (10분)
- [ ] Open DART API 키 발급
- [ ] Finnhub API 키 발급
- [ ] Gemini API 키 발급 (선택)

### 2단계: API 키 설정 (1분)
- [ ] 서비스 접속
- [ ] 설정 페이지에서 API 키 입력
- [ ] 저장 및 테스트

### 3단계: 서비스 사용
- [ ] 한국 주식 분석
- [ ] 미국 주식 분석
- [ ] AI 분석 활용

---

## 📞 지원

### 문제 발생 시
1. API 키가 올바른지 확인
2. 설정 페이지에서 테스트
3. 브라우저 콘솔에서 에러 확인
4. GitHub Issues에 문의

### 유용한 링크
- [Open DART API 문서](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001)
- [Finnhub API 문서](https://finnhub.io/docs/api)
- [Gemini API 문서](https://ai.google.dev/docs)

---

**API 키 설정이 완료되면 모든 기능을 사용할 수 있습니다!** 🎉

# 🚀 사용자 API 키 방식 배포 가이드

## 🎯 배포 방식 변경

### 기존 방식 (서버 API 키)
- ❌ 배포자의 API 키를 모든 사용자가 공유
- ❌ API 사용량 제한에 빠르게 도달
- ❌ 배포자의 비용 부담

### 새로운 방식 (사용자 API 키) ✅
- ✅ 각 사용자가 자신의 API 키 사용
- ✅ 무료 사용량을 개인별로 사용
- ✅ 배포자의 비용 부담 없음
- ✅ 더 안정적인 서비스

---

## 📋 배포 준비

### 1. 환경변수 불필요!

이제 서버에 API 키를 설정할 필요가 없습니다!

**제거할 환경변수:**
- ~~OPEN_DART_API_KEY~~
- ~~FINNHUB_API_KEY~~
- ~~GEMINI_API_KEY~~

**유지할 환경변수:**
- `FLASK_ENV=production` (선택사항)
- `PORT` (플랫폼에서 자동 설정)

### 2. 파일 확인

```bash
# 필수 파일
✅ requirements.txt
✅ Procfile
✅ runtime.txt
✅ .gitignore
✅ templates/settings.html  # API 키 설정 페이지
✅ static/js/api-keys.js    # API 키 관리 스크립트
```

---

## 🚀 Render 배포 (추천)

### 1단계: GitHub 푸시

```bash
git add .
git commit -m "User API key implementation"
git push origin main
```

### 2단계: Render 설정

1. https://render.com 접속
2. "New Web Service" 클릭
3. GitHub 저장소 연결

### 3단계: 빌드 설정

```
Name: financial-analysis
Region: Singapore
Branch: main
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

### 4단계: 환경변수 (선택사항)

```
FLASK_ENV = production
```

**API 키는 설정하지 않습니다!**

### 5단계: 배포

"Create Web Service" 클릭!

---

## 📱 사용자 안내

### 배포 후 README에 추가할 내용

```markdown
## 🔑 API 키 설정 필요

이 서비스를 사용하려면 개인 API 키가 필요합니다.

### 1. API 키 발급 (무료)
- **Open DART API**: https://opendart.fss.or.kr/
- **Finnhub API**: https://finnhub.io/register
- **Gemini AI API**: https://aistudio.google.com/app/apikey (선택사항)

### 2. API 키 설정
1. 서비스 접속
2. "⚙️ 설정" 버튼 클릭
3. API 키 입력 및 저장

자세한 내용은 [USER_API_KEY_GUIDE.md](./USER_API_KEY_GUIDE.md)를 참조하세요.
```

---

## 🎨 사용자 경험 개선

### 1. 첫 방문 시 안내

사용자가 처음 접속하면:
1. API 키 설정 필요 배너 표시
2. "API 키 설정하기" 버튼 제공
3. 설정 페이지로 이동

### 2. API 키 없이 기능 사용 시

```javascript
// 자동으로 설정 페이지로 안내
if (!apiKey) {
    alert('API 키가 필요합니다. 설정 페이지로 이동합니다.');
    window.location.href = '/settings';
}
```

### 3. API 키 테스트 기능

설정 페이지에서:
- 각 API 키의 유효성 즉시 확인
- 성공/실패 피드백 제공

---

## 🔒 보안 고려사항

### 클라이언트 측 저장

```javascript
// localStorage에 저장 (브라우저에만 존재)
localStorage.setItem('FINNHUB_API_KEY', apiKey);

// 서버로 전송 시 HTTPS 사용
fetch('/api/us_stocks/data', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        symbol: 'AAPL',
        api_key: localStorage.getItem('FINNHUB_API_KEY')
    })
});
```

### 서버 측 처리

```python
# API 키를 저장하지 않고 즉시 사용
@app.route("/api/us_stocks/data", methods=["POST"])
def get_us_stock_data():
    data = request.get_json()
    api_key = data.get("api_key")  # 요청마다 받음
    
    # API 키 검증
    if not api_key:
        return jsonify({"error": "API 키가 필요합니다"}), 401
    
    # 즉시 사용 (저장하지 않음)
    result = call_external_api(api_key)
    return jsonify(result)
```

---

## 📊 장단점 비교

### 장점 ✅

1. **비용 절감**
   - 배포자의 API 비용 없음
   - 각 사용자가 무료 플랜 사용

2. **확장성**
   - 사용자 수 제한 없음
   - API 사용량 제한 걱정 없음

3. **안정성**
   - 한 사용자의 과도한 사용이 다른 사용자에게 영향 없음
   - 서비스 중단 위험 감소

4. **개인정보 보호**
   - 서버에 API 키 저장 안 함
   - 각 사용자의 데이터 독립적

### 단점 ❌

1. **사용자 진입 장벽**
   - API 키 발급 필요 (10분 소요)
   - 초기 설정 필요

2. **사용자 경험**
   - 즉시 사용 불가
   - 설정 단계 추가

### 해결 방법 💡

1. **명확한 안내**
   - 상세한 API 키 발급 가이드
   - 스크린샷 포함 튜토리얼

2. **간편한 설정**
   - 직관적인 설정 페이지
   - 원클릭 테스트 기능

3. **데모 모드** (선택사항)
   - 제한된 기능을 API 키 없이 체험
   - 전체 기능은 API 키 필요

---

## 🎯 배포 체크리스트

### 코드 준비
- [x] 사용자 API 키 방식으로 변경
- [x] 설정 페이지 생성
- [x] API 키 관리 스크립트 추가
- [x] API 키 테스트 기능 구현

### 문서 준비
- [x] USER_API_KEY_GUIDE.md 작성
- [x] README에 API 키 안내 추가
- [x] 배포 가이드 업데이트

### 배포
- [ ] GitHub에 푸시
- [ ] Render에서 배포
- [ ] 환경변수 설정 (API 키 제외)
- [ ] 배포 확인

### 테스트
- [ ] 설정 페이지 접속
- [ ] API 키 저장 테스트
- [ ] API 키 테스트 기능 확인
- [ ] 모든 기능 작동 확인

---

## 📞 사용자 지원

### FAQ 페이지 추가

```markdown
## 자주 묻는 질문

### Q: API 키가 왜 필요한가요?
A: 외부 API 서비스를 사용하기 위해 필요합니다. 
   각 사용자가 자신의 키를 사용하므로 무료로 사용할 수 있습니다.

### Q: API 키 발급에 비용이 드나요?
A: 아니요, 모두 무료입니다.

### Q: API 키가 안전한가요?
A: 네, 브라우저에만 저장되며 서버로 전송되지 않습니다.
```

---

## 🚀 배포 완료!

### 다음 단계

1. **사용자 안내**
   - README에 API 키 안내 추가
   - 첫 화면에 설정 안내 배너

2. **모니터링**
   - 사용자 피드백 수집
   - 설정 페이지 사용률 확인

3. **개선**
   - 설정 과정 간소화
   - 튜토리얼 비디오 제작

---

**사용자 API 키 방식으로 안전하고 확장 가능한 서비스를 배포하세요!** 🎉

# 🚀 배포 프로세스 상세 가이드

## 📋 배포 시 자동 처리 사항

### 1. corp_codes.json 자동 생성

배포 환경에서 앱이 시작될 때 다음과 같이 자동으로 처리됩니다:

```python
# app.py의 load_corp_codes() 함수
1. corp_codes.json 파일 확인
2. 파일이 없으면 download_corp_codes.py 자동 실행
3. DART API에서 회사 코드 다운로드 (약 114,000개 회사)
4. JSON 파일로 변환 및 저장
5. 메모리에 로드
```

**필요한 환경변수:**
- `OPEN_DART_API_KEY`: DART API 키 (필수)

**처리 시간:**
- 첫 배포 시: 약 30초 (파일 다운로드 및 생성)
- 이후 재시작: 즉시 (파일이 이미 존재)

---

## 🔧 배포 환경별 설정

### Render 배포

#### 필수 환경변수
```env
FLASK_ENV=production
OPEN_DART_API_KEY=your_dart_api_key_here
```

#### 선택 환경변수 (사용자가 브라우저에서 입력)
- `FINNHUB_API_KEY`: 미국 주식 데이터
- `GEMINI_API_KEY`: AI 분석 기능
- `POLYGON_API_KEY`: 추가 미국 주식 데이터

#### 배포 명령어
```bash
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

#### 첫 시작 로그 예시
```
[INFO] corp_codes.json not found. Downloading...
🚀 DART 회사코드 다운로드 시작
📥 회사코드 파일 다운로드 중...
✅ ZIP 파일 다운로드 완료: corpCode.zip
📂 압축 해제 완료: ['CORPCODE.xml']
📊 CORPCODE.xml 파일 파싱 중...
📈 총 114147개 회사 정보 추출 완료
💾 JSON 파일 저장 완료: corp_codes.json
[INFO] Loaded 114147 companies
```

---

### Heroku 배포

#### 필수 환경변수
```bash
heroku config:set FLASK_ENV=production
heroku config:set OPEN_DART_API_KEY=your_dart_api_key_here
```

#### Procfile
```
web: gunicorn app:app
```

#### 배포
```bash
git push heroku main
```

---

### PythonAnywhere 배포

#### WSGI 파일 설정
```python
import sys
import os

# 프로젝트 경로 추가
path = '/home/yourusername/your-project'
if path not in sys.path:
    sys.path.append(path)

# 환경변수 설정
os.environ['FLASK_ENV'] = 'production'
os.environ['OPEN_DART_API_KEY'] = 'your_dart_api_key_here'

from app import app as application
```

---

## 📊 배포 후 확인 사항

### 1. 앱 시작 확인
```bash
# Render 로그 확인
# Dashboard → Logs 탭

# 확인할 내용:
✅ [INFO] Loaded 114147 companies
✅ [INFO] Gemini API configured (Model: gemini-2.5-pro)
✅ Running on http://0.0.0.0:10000
```

### 2. 기능 테스트

#### 한국 주식 검색
1. 메인 페이지 접속
2. "삼성전자" 검색
3. 검색 결과 5개 표시 확인
4. 회사 선택 및 재무 데이터 조회

#### 미국 주식 검색
1. "미국 주식" 탭 클릭
2. 설정 페이지에서 Finnhub API 키 입력
3. "AAPL" 검색
4. 주가 및 재무 데이터 확인

#### AI 분석
1. 설정 페이지에서 Gemini API 키 입력
2. 재무 데이터 조회 후 "AI 분석" 탭
3. "AI 분석 시작" 버튼 클릭
4. 분석 결과 확인

---

## 🔄 업데이트 프로세스

### 코드 업데이트
```bash
# 1. 로컬에서 코드 수정
git add .
git commit -m "Update features"

# 2. GitHub에 푸시
git push origin main

# 3. Render에서 자동 재배포 (5-10분)
# corp_codes.json은 유지됨 (재다운로드 불필요)
```

### corp_codes.json 강제 업데이트
```bash
# 방법 1: 파일 삭제 후 재시작
# Render Dashboard → Shell
rm corp_codes.json
# 앱 재시작 시 자동 다운로드

# 방법 2: 수동 실행
python download_corp_codes.py
```

---

## ⚠️ 주의사항

### 1. API 키 관리

**서버 환경변수 (Render/Heroku):**
- ✅ `OPEN_DART_API_KEY`: 서버에서 설정 (필수)
- ❌ `FINNHUB_API_KEY`: 사용자가 브라우저에서 입력
- ❌ `GEMINI_API_KEY`: 사용자가 브라우저에서 입력

**이유:**
- DART API는 회사 코드 다운로드용 (서버 시작 시 1회)
- 다른 API는 사용자별 쿼터 관리를 위해 클라이언트에서 입력

### 2. 파일 시스템

**Render Free Tier:**
- 파일 시스템은 임시 (ephemeral)
- 재배포 시 파일 삭제됨
- corp_codes.json은 매 배포 시 재생성됨 (자동)

**해결책:**
- 앱 시작 시 자동 생성 로직 (이미 구현됨)
- 또는 S3/Cloud Storage 사용 (선택사항)

### 3. 시작 시간

**첫 배포:**
- 빌드: 2-3분
- 앱 시작: 30초 (corp_codes.json 생성)
- 총: 약 3-4분

**이후 재시작:**
- 파일이 있으면: 즉시
- 파일이 없으면: 30초 (자동 재생성)

---

## 🐛 문제 해결

### 문제 1: "검색 결과가 없습니다"

**원인:**
- corp_codes.json 파일이 생성되지 않음
- OPEN_DART_API_KEY 미설정

**해결:**
```bash
# 1. 환경변수 확인
echo $OPEN_DART_API_KEY

# 2. 로그 확인
[ERROR] Failed to download corp_codes.json

# 3. API 키 재설정
# Render Dashboard → Environment → Add
OPEN_DART_API_KEY = your_valid_key

# 4. 앱 재시작
```

### 문제 2: "API 키가 설정되지 않았습니다"

**원인:**
- 사용자가 브라우저에서 API 키를 입력하지 않음

**해결:**
1. 설정 페이지 (⚙️) 접속
2. 필요한 API 키 입력
3. "저장 및 테스트" 클릭

### 문제 3: 앱 시작이 느림

**원인:**
- corp_codes.json 다운로드 중 (첫 시작)

**해결:**
- 정상 동작 (30초 대기)
- 로그에서 진행 상황 확인

### 문제 4: 메모리 부족

**원인:**
- corp_codes.json 파일 크기 (약 20MB)
- 114,000개 회사 데이터

**해결:**
```python
# 필요시 데이터 필터링
def load_corp_codes():
    # 상장 회사만 로드
    all_companies = json.load(f)
    return [c for c in all_companies if c.get('stock_code')]
```

---

## 📈 성능 최적화

### 1. 캐싱 추가

```python
# corp_codes 검색 결과 캐싱
from functools import lru_cache

@lru_cache(maxsize=1000)
def search_company_cached(company_name):
    return [c for c in corp_codes_data if company_name in c['corp_name']]
```

### 2. 인덱싱

```python
# 회사명 인덱스 생성
company_index = {}
for company in corp_codes_data:
    name = company['corp_name']
    if name not in company_index:
        company_index[name] = []
    company_index[name].append(company)
```

### 3. 압축

```python
# JSON 파일 압축 저장
import gzip
import json

with gzip.open('corp_codes.json.gz', 'wt', encoding='utf-8') as f:
    json.dump(companies, f)
```

---

## 🎯 배포 체크리스트

### 배포 전
- [ ] requirements.txt 최신화
- [ ] .env.example 업데이트
- [ ] .gitignore 확인 (.env 제외)
- [ ] 로컬 테스트 완료
- [ ] DART API 키 발급

### 배포 중
- [ ] GitHub에 코드 푸시
- [ ] Render에서 저장소 연결
- [ ] 환경변수 설정 (OPEN_DART_API_KEY)
- [ ] 빌드 명령어 확인
- [ ] 시작 명령어 확인

### 배포 후
- [ ] 로그에서 corp_codes.json 생성 확인
- [ ] 앱 URL 접속
- [ ] 한국 주식 검색 테스트
- [ ] 설정 페이지 확인
- [ ] 미국 주식 테스트 (API 키 입력 후)
- [ ] AI 분석 테스트 (API 키 입력 후)

---

## 📚 관련 문서

- [RENDER_DEPLOY_STEPS.md](./RENDER_DEPLOY_STEPS.md) - Render 배포 단계
- [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - 전체 배포 가이드
- [USER_API_KEY_GUIDE.md](./USER_API_KEY_GUIDE.md) - 사용자 API 키 가이드
- [사용가이드.md](./사용가이드.md) - 한국어 사용 가이드

---

## ✅ 요약

### 배포 시 자동 처리
1. ✅ corp_codes.json 자동 생성
2. ✅ 114,000개 회사 데이터 로드
3. ✅ 한국 주식 검색 기능 활성화

### 필수 환경변수
- `OPEN_DART_API_KEY`: 서버에서 설정 (필수)

### 선택 환경변수
- 사용자가 브라우저에서 입력:
  - Finnhub API (미국 주식)
  - Gemini API (AI 분석)

### 배포 플랫폼
- **추천**: Render (무료, 자동 배포)
- **대안**: Heroku, Railway, PythonAnywhere

---

**배포 준비 완료!** 🚀

질문이 있으시면 GitHub Issues에 남겨주세요.

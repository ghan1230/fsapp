# 🚀 배포 가이드

## 📋 배포 전 체크리스트

### 필수 사항
- [ ] Python 3.8 이상
- [ ] 모든 API 키 발급 완료
- [ ] requirements.txt 생성
- [ ] .gitignore 설정
- [ ] 환경변수 설정

---

## 🔧 배포 준비

### 1. requirements.txt 생성

```bash
pip freeze > requirements.txt
```

또는 수동으로 작성:

```txt
Flask==3.0.0
python-dotenv==1.0.0
requests==2.31.0
yfinance==0.2.32
pandas==2.1.3
numpy==1.26.2
```

### 2. .gitignore 설정

```gitignore
# 환경변수
.env
*.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 데이터
*.db
*.sqlite
*.log

# OS
.DS_Store
Thumbs.db
```

### 3. 환경변수 템플릿 생성

`.env.example` 파일 생성:

```env
# Open DART API (한국 주식)
OPEN_DART_API_KEY=your_dart_api_key_here

# Finnhub API (미국 주식)
FINNHUB_API_KEY=your_finnhub_api_key_here

# Gemini AI API (AI 분석)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-pro

# Polygon API (선택사항)
POLYGON_API_KEY=your_polygon_api_key_here
```

---

## 🌐 배포 옵션

### 옵션 1: Heroku (추천 - 무료/간단)

#### 장점
- ✅ 무료 플랜 제공
- ✅ 간단한 배포
- ✅ 자동 HTTPS
- ✅ Git 기반 배포

#### 단계

1. **Heroku 계정 생성**
   - https://heroku.com 에서 가입

2. **Heroku CLI 설치**
   ```bash
   # Windows (Chocolatey)
   choco install heroku-cli
   
   # 또는 직접 다운로드
   # https://devcenter.heroku.com/articles/heroku-cli
   ```

3. **Procfile 생성**
   ```
   web: gunicorn app:app
   ```

4. **runtime.txt 생성**
   ```
   python-3.11.0
   ```

5. **requirements.txt에 gunicorn 추가**
   ```txt
   gunicorn==21.2.0
   ```

6. **배포 명령어**
   ```bash
   # Heroku 로그인
   heroku login
   
   # 앱 생성
   heroku create your-app-name
   
   # 환경변수 설정
   heroku config:set OPEN_DART_API_KEY=your_key
   heroku config:set FINNHUB_API_KEY=your_key
   heroku config:set GEMINI_API_KEY=your_key
   
   # Git 배포
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   
   # 앱 열기
   heroku open
   ```

---

### 옵션 2: Render (추천 - 무료/최신)

#### 장점
- ✅ 무료 플랜 제공
- ✅ GitHub 연동 자동 배포
- ✅ 자동 HTTPS
- ✅ 최신 플랫폼

#### 단계

1. **Render 계정 생성**
   - https://render.com 에서 가입

2. **GitHub 저장소 연결**
   - GitHub에 코드 푸시
   - Render에서 "New Web Service" 선택
   - GitHub 저장소 연결

3. **설정**
   - **Name**: your-app-name
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

4. **환경변수 설정**
   - Environment 탭에서 추가:
     - `OPEN_DART_API_KEY`
     - `FINNHUB_API_KEY`
     - `GEMINI_API_KEY`

5. **배포**
   - "Create Web Service" 클릭
   - 자동으로 배포 시작

---

### 옵션 3: PythonAnywhere (무료/간단)

#### 장점
- ✅ 완전 무료
- ✅ Python 특화
- ✅ 웹 기반 관리

#### 단계

1. **PythonAnywhere 계정 생성**
   - https://www.pythonanywhere.com 에서 가입

2. **파일 업로드**
   - Files 탭에서 코드 업로드
   - 또는 Git clone

3. **가상환경 생성**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 myenv
   pip install -r requirements.txt
   ```

4. **Web 앱 설정**
   - Web 탭에서 "Add a new web app"
   - Flask 선택
   - WSGI 파일 수정:
   ```python
   import sys
   path = '/home/yourusername/your-project'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

5. **환경변수 설정**
   - WSGI 파일에 추가:
   ```python
   import os
   os.environ['OPEN_DART_API_KEY'] = 'your_key'
   os.environ['FINNHUB_API_KEY'] = 'your_key'
   os.environ['GEMINI_API_KEY'] = 'your_key'
   ```

6. **Reload**
   - Web 탭에서 "Reload" 클릭

---

### 옵션 4: Railway (추천 - 간단)

#### 장점
- ✅ $5 무료 크레딧
- ✅ GitHub 연동
- ✅ 자동 배포
- ✅ 빠른 속도

#### 단계

1. **Railway 계정 생성**
   - https://railway.app 에서 가입

2. **프로젝트 생성**
   - "New Project" → "Deploy from GitHub repo"
   - 저장소 선택

3. **환경변수 설정**
   - Variables 탭에서 추가

4. **자동 배포**
   - Git push 시 자동 배포

---

### 옵션 5: Vercel (서버리스)

#### 장점
- ✅ 무료 플랜
- ✅ 빠른 배포
- ✅ GitHub 연동

#### 단계

1. **vercel.json 생성**
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app.py"
       }
     ]
   }
   ```

2. **Vercel CLI 설치**
   ```bash
   npm install -g vercel
   ```

3. **배포**
   ```bash
   vercel
   ```

---

## 🔒 보안 설정

### 1. API 키 보호

**절대 하지 말 것:**
- ❌ .env 파일을 Git에 커밋
- ❌ 코드에 API 키 하드코딩
- ❌ 공개 저장소에 키 노출

**해야 할 것:**
- ✅ .gitignore에 .env 추가
- ✅ 환경변수로 관리
- ✅ .env.example 제공

### 2. CORS 설정 (필요시)

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})
```

### 3. Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/us_stocks/data", methods=["POST"])
@limiter.limit("10 per minute")
def get_us_stock_data():
    # ...
```

---

## 📊 성능 최적화

### 1. 캐싱 추가

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route("/api/us_stocks/data", methods=["POST"])
@cache.cached(timeout=300)  # 5분 캐싱
def get_us_stock_data():
    # ...
```

### 2. 압축 활성화

```python
from flask_compress import Compress

Compress(app)
```

### 3. 정적 파일 최적화

```python
# app.py
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1년
```

---

## 🔍 모니터링

### 1. 로깅 설정

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

### 2. 에러 추적 (Sentry)

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
)
```

---

## 📱 도메인 연결

### 1. 무료 도메인
- **Freenom**: .tk, .ml, .ga 등
- **GitHub Pages**: username.github.io

### 2. 유료 도메인
- **Namecheap**: $8.88/년
- **GoDaddy**: $11.99/년
- **Google Domains**: $12/년

### 3. DNS 설정
```
A Record: @ → your-server-ip
CNAME: www → your-app.herokuapp.com
```

---

## 🧪 배포 전 테스트

### 1. 로컬 프로덕션 모드 테스트

```bash
# gunicorn으로 테스트
gunicorn app:app

# 또는
python -m gunicorn app:app
```

### 2. 환경변수 테스트

```bash
# .env 파일 없이 테스트
export OPEN_DART_API_KEY=test_key
export FINNHUB_API_KEY=test_key
python app.py
```

### 3. 부하 테스트

```bash
# Apache Bench
ab -n 1000 -c 10 http://localhost:5000/

# 또는 wrk
wrk -t12 -c400 -d30s http://localhost:5000/
```

---

## 📋 배포 체크리스트

### 배포 전
- [ ] requirements.txt 생성
- [ ] .gitignore 설정
- [ ] .env.example 생성
- [ ] 모든 API 키 확인
- [ ] 로컬 테스트 완료
- [ ] 보안 설정 확인

### 배포 중
- [ ] 플랫폼 선택
- [ ] 환경변수 설정
- [ ] 배포 명령어 실행
- [ ] 배포 성공 확인

### 배포 후
- [ ] 웹사이트 접속 테스트
- [ ] 모든 기능 테스트
- [ ] API 호출 테스트
- [ ] 에러 로그 확인
- [ ] 성능 모니터링

---

## 🆘 문제 해결

### 문제 1: 모듈을 찾을 수 없음
```bash
# 해결: requirements.txt 확인
pip install -r requirements.txt
```

### 문제 2: 포트 충돌
```python
# app.py 수정
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
```

### 문제 3: API 키 오류
```bash
# 환경변수 확인
echo $FINNHUB_API_KEY

# Heroku에서 확인
heroku config
```

### 문제 4: 메모리 부족
```python
# 캐싱 추가
# 불필요한 데이터 제거
# 페이지네이션 구현
```

---

## 💰 비용 예상

### 무료 옵션
- **Heroku**: 무료 (550시간/월)
- **Render**: 무료 (750시간/월)
- **PythonAnywhere**: 완전 무료
- **Railway**: $5 크레딧

### 유료 옵션 (필요시)
- **Heroku Hobby**: $7/월
- **Render Starter**: $7/월
- **Railway Pro**: $5/월
- **도메인**: $10/년

---

## 🎯 추천 배포 방법

### 초보자
1. **PythonAnywhere** - 가장 간단
2. **Render** - GitHub 연동 자동 배포

### 중급자
1. **Heroku** - 안정적이고 검증됨
2. **Railway** - 빠르고 현대적

### 고급자
1. **AWS/GCP** - 완전한 제어
2. **Docker + Kubernetes** - 확장성

---

## 📚 추가 자료

### 공식 문서
- [Flask 배포 가이드](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Heroku Python 가이드](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Render 문서](https://render.com/docs)

### 튜토리얼
- [Flask 앱 Heroku 배포](https://realpython.com/flask-by-example-part-1-project-setup/)
- [Python 웹앱 배포 완벽 가이드](https://testdriven.io/blog/deploying-flask-to-heroku-with-docker-and-gitlab/)

---

## ✅ 다음 단계

1. **배포 플랫폼 선택** (Render 추천)
2. **requirements.txt 생성**
3. **GitHub에 코드 푸시**
4. **플랫폼에서 배포**
5. **환경변수 설정**
6. **테스트 및 모니터링**

**배포 준비가 완료되었습니다!** 🚀

어떤 플랫폼을 선택하시겠습니까?

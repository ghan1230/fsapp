from flask import Flask, render_template, request, jsonify
import json
import requests
import os
from dotenv import load_dotenv
from finnhub_api import FinnhubAPI
from korean_stock_api import KoreanStockAPI
from datetime import datetime, timedelta

# .env 파일에서 환경변수 로드
load_dotenv()

app = Flask(__name__)

# Gemini API 설정
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")  # 기본값: gemini-1.5-flash

if gemini_api_key and gemini_api_key != "your_gemini_api_key_here":
    print(f"[INFO] Gemini API configured (Model: {gemini_model})")
else:
    print("[WARNING] Gemini API key not configured. AI analysis features disabled.")


# 회사 코드 데이터 로드
def load_corp_codes():
    """corp_codes.json 파일에서 회사 데이터를 로드합니다."""
    try:
        with open("corp_codes.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("[INFO] corp_codes.json not found. Downloading...")
        try:
            # download_corp_codes.py 실행
            import subprocess

            subprocess.run(["python", "download_corp_codes.py"], check=True)
            # 다시 로드 시도
            with open("corp_codes.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to download corp_codes.json: {e}")
            return []


corp_codes_data = load_corp_codes()


@app.route("/")
def index():
    """메인 페이지"""
    return render_template("index.html")


@app.route("/settings")
def settings():
    """API 키 설정 페이지"""
    return render_template("settings.html")


@app.route("/test")
def test():
    """테스트 페이지"""
    return render_template("test.html")


@app.route("/simple")
def simple():
    """간단한 버전"""
    return render_template("index_simple.html")


@app.route("/us_stocks")
def us_stocks():
    """미국 주식 분석 페이지"""
    return render_template("us_stocks.html")


@app.route("/compare")
def compare():
    """기업 비교 분석 페이지"""
    return render_template("compare.html")


@app.route("/api/test_keys", methods=["POST"])
def test_keys():
    """API 키 테스트"""
    data = request.get_json()
    dart_key = data.get("dart_key")
    finnhub_key = data.get("finnhub_key")
    gemini_key = data.get("gemini_key")

    results = {"dart": False, "finnhub": False, "gemini": False}

    # Open DART API 테스트
    if dart_key:
        try:
            url = "https://opendart.fss.or.kr/api/corpCode.xml"
            params = {"crtfc_key": dart_key}
            response = requests.get(url, params=params, timeout=5)
            results["dart"] = (
                response.status_code == 200 and "00126380" in response.text
            )
        except:
            pass

    # Finnhub API 테스트
    if finnhub_key:
        try:
            url = "https://finnhub.io/api/v1/quote"
            params = {"symbol": "AAPL", "token": finnhub_key}
            response = requests.get(url, params=params, timeout=5)
            results["finnhub"] = response.status_code == 200
        except:
            pass

    # Gemini API 테스트
    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={gemini_key}"
            payload = {"contents": [{"parts": [{"text": "test"}]}]}
            response = requests.post(url, json=payload, timeout=5)
            results["gemini"] = response.status_code == 200
        except:
            pass

    return jsonify(results)


@app.route("/api/search_company", methods=["POST"])
def search_company():
    """회사명으로 회사 코드 검색"""
    data = request.get_json()
    company_name = data.get("company_name", "").strip()

    if not company_name:
        return jsonify({"error": "회사명을 입력해주세요."}), 400

    # 회사명으로 검색 (부분 일치)
    results = []
    for company in corp_codes_data:
        if company_name.lower() in company.get("corp_name", "").lower():
            results.append(
                {
                    "corp_code": company.get("corp_code"),
                    "corp_name": company.get("corp_name"),
                    "stock_code": company.get("stock_code", "").strip(),
                }
            )

    # 최대 10개 결과만 반환
    return jsonify({"results": results[:10]})


@app.route("/api/financial_data", methods=["POST"])
def get_financial_data():
    """Open DART API를 사용하여 재무 데이터 가져오기"""
    data = request.get_json()
    corp_code = data.get("corp_code")
    bsns_year = data.get("bsns_year", "2023")
    reprt_code = data.get("reprt_code", "11011")  # 기본값: 사업보고서
    api_key = data.get("api_key")  # 클라이언트에서 전달받은 API 키

    print(
        f"[REQUEST] Financial data: corp_code={corp_code}, year={bsns_year}, report={reprt_code}"
    )

    if not corp_code:
        return jsonify({"error": "회사 코드가 필요합니다."}), 400

    if not api_key:
        return (
            jsonify(
                {"error": "API 키가 필요합니다. 설정 페이지에서 API 키를 입력해주세요."}
            ),
            401,
        )

    # Open DART API 호출
    url = "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"
    params = {
        "crtfc_key": api_key,
        "corp_code": corp_code,
        "bsns_year": bsns_year,
        "reprt_code": reprt_code,
    }

    try:
        print(f"[API] Calling: {url}")
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()

        print(f"[API] Response status: {result.get('status')}")
        print(f"[API] Response message: {result.get('message')}")

        if result.get("status") != "000":
            error_msg = f"API error: {result.get('message', 'Unknown error')}"
            print(f"[ERROR] {error_msg}")
            return jsonify({"error": error_msg}), 400

        # 데이터 개수 확인
        data_count = len(result.get("list", []))
        print(f"[SUCCESS] Data count: {data_count}")

        # 주요 항목들 로깅
        for item in result.get("list", [])[:5]:
            print(f"  - {item.get('account_nm')}: {item.get('thstrm_amount')}")

        return jsonify(result)

    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {str(e)}"
        print(f"[ERROR] {error_msg}")
        return jsonify({"error": error_msg}), 500
    except Exception as e:
        error_msg = f"Error occurred: {str(e)}"
        print(f"[ERROR] {error_msg}")
        return jsonify({"error": error_msg}), 500


@app.route("/api/financial_comparison", methods=["POST"])
def get_financial_comparison():
    """여러 연도의 재무 데이터를 비교하여 가져오기"""
    data = request.get_json()
    corp_code = data.get("corp_code")
    years = data.get("years", ["2023", "2022", "2021"])
    reprt_code = data.get("reprt_code", "11011")

    print(f"[REQUEST] Yearly comparison: corp_code={corp_code}, years={years}")

    if not corp_code:
        return jsonify({"error": "회사 코드가 필요합니다."}), 400

    api_key = os.getenv("OPEN_DART_API_KEY")
    if not api_key:
        return jsonify({"error": "API 키가 설정되지 않았습니다."}), 500

    comparison_data = {}

    for year in years:
        url = "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"
        params = {
            "crtfc_key": api_key,
            "corp_code": corp_code,
            "bsns_year": year,
            "reprt_code": reprt_code,
        }

        try:
            print(f"[API] Fetching {year} data")
            response = requests.get(url, params=params)
            response.raise_for_status()
            result = response.json()

            if result.get("status") == "000":
                comparison_data[year] = result.get("list", [])
                print(f"[SUCCESS] {year} data: {len(result.get('list', []))} items")
            else:
                print(f"[WARNING] {year} data not available: {result.get('message')}")
                comparison_data[year] = []

        except Exception as e:
            print(f"[ERROR] {year} data error: {str(e)}")
            comparison_data[year] = []

    return jsonify({"comparison_data": comparison_data})


@app.route("/api/check_data_availability", methods=["GET"])
def check_data_availability():
    """최신 데이터 가용성을 체크하여 사용 가능한 연도와 보고서 유형을 반환"""
    api_key = os.getenv("OPEN_DART_API_KEY")
    if not api_key:
        return jsonify({"error": "API 키가 설정되지 않았습니다."}), 500

    # 삼성전자를 기준으로 데이터 가용성 체크 (대표적인 회사)
    test_corp_code = "00126380"  # 삼성전자

    # 현재 연도부터 역순으로 체크
    import datetime

    current_year = datetime.datetime.now().year

    available_data = {"years": [], "latest_year": None, "report_availability": {}}

    # 최근 3년간만 체크 (속도 향상)
    for year in range(current_year, current_year - 3, -1):
        year_str = str(year)
        year_data = {"year": year_str, "available_reports": []}

        # 각 보고서 유형별 체크
        report_types = {
            "11011": "사업보고서",
            "11012": "반기보고서",
            "11013": "1분기보고서",
            "11014": "3분기보고서",
        }

        for reprt_code, reprt_name in report_types.items():
            url = "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"
            params = {
                "crtfc_key": api_key,
                "corp_code": test_corp_code,
                "bsns_year": year_str,
                "reprt_code": reprt_code,
            }

            try:
                response = requests.get(url, params=params, timeout=3)
                if response.status_code == 200:
                    result = response.json()
                    if result.get("status") == "000":
                        year_data["available_reports"].append(
                            {"code": reprt_code, "name": reprt_name}
                        )
            except:
                continue  # 에러 시 해당 보고서는 사용 불가로 처리

        # 사용 가능한 보고서가 있으면 연도 추가
        if year_data["available_reports"]:
            available_data["years"].append(year_data)
            if available_data["latest_year"] is None:
                available_data["latest_year"] = year_str

            available_data["report_availability"][year_str] = year_data[
                "available_reports"
            ]

    print(
        f"[INFO] Data availability check complete: {len(available_data['years'])} years"
    )
    return jsonify(available_data)


@app.route("/api/test_gemini", methods=["GET"])
def test_gemini():
    """Gemini API 연결 테스트"""
    if not gemini_api_key or gemini_api_key == "your_gemini_api_key_here":
        return jsonify({"error": "Gemini API 키가 설정되지 않았습니다."}), 500

    try:
        print(f"[TEST] Gemini API test starting (Model: {gemini_model})")

        # 설정된 모델로 간단한 테스트 요청
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={gemini_api_key}"

        payload = {
            "contents": [{"parts": [{"text": "안녕하세요. 간단한 테스트입니다."}]}]
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(gemini_url, json=payload, headers=headers, timeout=5)

        if response.status_code == 200:
            print(f"[SUCCESS] Gemini API test passed (Model: {gemini_model})")
            return jsonify(
                {
                    "status": "success",
                    "message": f"Gemini API 연결 성공 (모델: {gemini_model})",
                }
            )
        else:
            error_detail = (
                response.json()
                if response.headers.get("content-type") == "application/json"
                else response.text
            )
            print(f"[ERROR] Gemini API test failed: {response.status_code}")
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"API 오류 ({response.status_code}): {error_detail}",
                    }
                ),
                400,
            )

    except Exception as e:
        print(f"[ERROR] Gemini API test exception: {str(e)}")
        return (
            jsonify({"status": "error", "message": f"연결 테스트 실패: {str(e)}"}),
            500,
        )


# ===== 미국 주식 관련 API =====


@app.route("/api/us_stocks/search", methods=["POST"])
def search_us_stocks():
    """미국 주식 티커 검색"""
    try:
        data = request.get_json()
        search_term = data.get("search_term", "").strip()
        api_key = data.get("api_key")  # 클라이언트에서 전달받은 API 키

        if not search_term:
            return jsonify({"error": "검색어를 입력해주세요."}), 400

        if not api_key:
            return (
                jsonify(
                    {
                        "error": "Finnhub API 키가 필요합니다. 설정 페이지에서 API 키를 입력해주세요."
                    }
                ),
                401,
            )

        print(f"[SEARCH] US stocks: {search_term}")

        # API 키를 사용하여 FinnhubAPI 인스턴스 생성
        os.environ["FINNHUB_API_KEY"] = api_key
        finnhub_api = FinnhubAPI()

        # Finnhub API로 심볼 검색
        result = finnhub_api.search_symbol(search_term)

        if result and "result" in result:
            stocks = []
            for stock in result["result"][:10]:  # 상위 10개만
                stocks.append(
                    {
                        "symbol": stock.get("symbol", ""),
                        "description": stock.get("description", ""),
                        "displaySymbol": stock.get("displaySymbol", ""),
                        "type": stock.get("type", ""),
                    }
                )

            print(f"[SUCCESS] Search results: {len(stocks)} items")
            return jsonify({"results": stocks})
        else:
            return jsonify({"results": []})

    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        print(f"[ERROR] US stock search error: {e}")
        return jsonify({"error": "검색 중 오류가 발생했습니다."}), 500


@app.route("/api/us_stocks/data", methods=["POST"])
def get_us_stock_data():
    """미국 주식 데이터 조회"""
    try:
        data = request.get_json()
        symbol = data.get("symbol", "").upper().strip()
        api_key = data.get("api_key")  # 클라이언트에서 전달받은 API 키

        if not symbol:
            return jsonify({"error": "심볼을 입력해주세요."}), 400

        if not api_key:
            return jsonify({"error": "Finnhub API 키가 필요합니다. 설정 페이지에서 API 키를 입력해주세요."}), 401

        print(f"[REQUEST] US stock data: {symbol}")

        # API 키를 사용하여 FinnhubAPI 인스턴스 생성
        os.environ['FINNHUB_API_KEY'] = api_key
        finnhub_api = FinnhubAPI()

        # 종합 데이터 조회
        comprehensive_data = finnhub_api.format_comprehensive_data(symbol)

        if comprehensive_data:
            print(f"[SUCCESS] {symbol} data retrieved")
            return jsonify(comprehensive_data)
        else:
            return jsonify({"error": "해당 심볼의 데이터를 찾을 수 없습니다."}), 404

    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        print(f"[ERROR] US stock data error: {e}")
        return jsonify({"error": "데이터 조회 중 오류가 발생했습니다."}), 500


@app.route("/api/us_stocks/financials", methods=["POST"])
def get_us_stock_financials():
    """미국 주식 재무제표 분석"""
    try:
        finnhub_api = FinnhubAPI()
        data = request.get_json()
        symbol = data.get("symbol", "").upper().strip()

        if not symbol:
            return jsonify({"error": "심볼을 입력해주세요."}), 400

        print(f"[REQUEST] {symbol} financial analysis starting")

        # 재무 지표 조회
        financials = finnhub_api.get_basic_financials(symbol)
        earnings = finnhub_api.get_earnings(symbol)
        recommendations = finnhub_api.get_recommendation_trends(symbol)

        if not financials:
            return jsonify({"error": "재무 데이터를 찾을 수 없습니다."}), 404

        analysis_data = {
            "symbol": symbol,
            "financial_metrics": financials.get("metric", {}),
            "earnings": earnings or [],
            "recommendations": recommendations or [],
        }

        print(f"[SUCCESS] {symbol} financial analysis complete")
        return jsonify(analysis_data)

    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"[ERROR] Financial analysis error: {e}")
        return jsonify({"error": "재무제표 분석 중 오류가 발생했습니다."}), 500


@app.route("/api/us_stocks/news", methods=["POST"])
def get_us_stock_news():
    """미국 주식 뉴스 조회"""
    try:
        finnhub_api = FinnhubAPI()
        data = request.get_json()
        symbol = data.get("symbol", "").upper().strip()

        if not symbol:
            return jsonify({"error": "심볼을 입력해주세요."}), 400

        print(f"[REQUEST] {symbol} news")
        news = finnhub_api.get_company_news(symbol)

        if news:
            print(f"[SUCCESS] {symbol} news: {len(news)} articles")
            return jsonify({"news": news[:15]})  # 최근 15개
        else:
            return jsonify({"news": []})

    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"[ERROR] News error: {e}")
        return jsonify({"error": "뉴스 조회 중 오류가 발생했습니다."}), 500


@app.route("/api/us_stocks/dividends", methods=["POST"])
def get_us_stock_dividends():
    """미국 주식 배당 정보 조회"""
    try:
        finnhub_api = FinnhubAPI()
        data = request.get_json()
        symbol = data.get("symbol", "").upper().strip()

        if not symbol:
            return jsonify({"error": "심볼을 입력해주세요."}), 400

        print(f"[REQUEST] {symbol} dividends")
        dividends = finnhub_api.get_dividends(symbol)

        if dividends:
            print(
                f"[SUCCESS] {symbol} dividends: {len(dividends.get('history', []))} records"
            )
            return jsonify({"dividends": dividends})
        else:
            return jsonify({"dividends": None, "message": "배당 정보가 없습니다."})

    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"[ERROR] Dividends error: {e}")
        return jsonify({"error": "배당 정보 조회 중 오류가 발생했습니다."}), 500


@app.route("/api/us_stocks/peers", methods=["POST"])
def get_us_stock_peers():
    """동종 업계 기업 조회"""
    try:
        finnhub_api = FinnhubAPI()
        data = request.get_json()
        symbol = data.get("symbol", "").upper().strip()

        if not symbol:
            return jsonify({"error": "심볼을 입력해주세요."}), 400

        print(f"[REQUEST] {symbol} peers")
        peers = finnhub_api.get_peers(symbol)

        if peers:
            # 각 peer의 기본 정보 가져오기
            peers_data = []
            for peer_symbol in peers[:5]:  # 최대 5개
                try:
                    profile = finnhub_api.get_company_profile(peer_symbol)
                    quote = finnhub_api.get_quote(peer_symbol)
                    financials = finnhub_api.get_basic_financials(peer_symbol)

                    if profile and quote:
                        peer_info = {
                            "symbol": peer_symbol,
                            "name": profile.get("name", ""),
                            "market_cap": profile.get("marketCapitalization", 0),
                            "current_price": quote.get("c", 0),
                            "change_percent": quote.get("dp", 0),
                            "pe_ratio": (
                                financials.get("metric", {}).get(
                                    "peBasicExclExtraTTM", 0
                                )
                                if financials
                                else 0
                            ),
                            "pb_ratio": (
                                financials.get("metric", {}).get("pbQuarterly", 0)
                                if financials
                                else 0
                            ),
                            "roe": (
                                financials.get("metric", {}).get("roeRfy", 0)
                                if financials
                                else 0
                            ),
                        }
                        peers_data.append(peer_info)
                except:
                    continue

            print(f"[SUCCESS] {symbol} peers: {len(peers_data)} companies")
            return jsonify({"peers": peers_data, "base_symbol": symbol})
        else:
            return jsonify({"peers": [], "message": "동종 업계 정보가 없습니다."})

    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"[ERROR] Peers error: {e}")
        return jsonify({"error": "동종 업계 조회 중 오류가 발생했습니다."}), 500


@app.route("/api/korean_stock_chart/<corp_code>", methods=["GET"])
def get_korean_stock_chart(corp_code):
    """한국 주식 차트 데이터 조회 (GET 방식)"""
    print(f"[REQUEST] Korean stock chart: {corp_code}")
    try:
        korean_api = KoreanStockAPI()

        if not corp_code:
            print("[ERROR] Company code missing")
            return jsonify({"error": "회사 코드가 필요합니다."}), 400

        # 주식 코드 찾기
        stock_code = korean_api.get_stock_code_from_corp_code(
            corp_code, corp_codes_data
        )
        print(f"[INFO] Corp code {corp_code} -> Stock code: {stock_code}")

        if not stock_code:
            print(f"[ERROR] Stock code not found: {corp_code}")
            return (
                jsonify(
                    {
                        "error": "해당 회사의 주식 코드를 찾을 수 없습니다. 비상장 회사일 수 있습니다."
                    }
                ),
                404,
            )

        # 차트 데이터 가져오기
        print(f"[REQUEST] Yahoo Finance data for {stock_code}")
        chart_data = korean_api.get_korean_stock_chart_data(stock_code, days=90)

        if chart_data:
            print(f"[SUCCESS] {stock_code} chart data: {len(chart_data['data'])} days")
            return jsonify(chart_data)
        else:
            print(f"[ERROR] Chart data not available: {stock_code}")
            return jsonify({"error": "차트 데이터를 가져올 수 없습니다."}), 404

    except Exception as e:
        print(f"[ERROR] Korean stock chart error: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({"error": f"차트 데이터 조회 중 오류: {str(e)}"}), 500


@app.route("/api/analyze_us_stock", methods=["POST"])
def analyze_us_stock():
    """Gemini AI를 사용하여 미국 주식 데이터를 분석"""

    if not gemini_api_key or gemini_api_key == "your_gemini_api_key_here":
        return jsonify({"error": "Gemini API 키가 설정되지 않았습니다."}), 500

    data = request.get_json()
    stock_data = data.get("stock_data")
    symbol = data.get("symbol", "해당 주식")

    if not stock_data:
        return jsonify({"error": "분석할 주식 데이터가 없습니다."}), 400

    try:
        # 주식 데이터를 텍스트로 변환
        company_info = stock_data.get("company_info", {})
        price_info = stock_data.get("price_info", {})
        financial_metrics = stock_data.get("financial_metrics", {})

        stock_summary = f"""
        주식 심볼: {symbol}
        회사명: {company_info.get('name', 'N/A')}
        산업: {company_info.get('industry', 'N/A')}
        국가: {company_info.get('country', 'N/A')}
        
        주가 정보:
        - 현재가: ${price_info.get('current_price', 0):.2f}
        - 변동: ${price_info.get('change', 0):.2f} ({price_info.get('percent_change', 0):.2f}%)
        - 시가총액: ${company_info.get('market_capitalization', 0):,}M
        
        재무 지표:
        - P/E 비율: {financial_metrics.get('pe_ratio', 'N/A')}
        - P/B 비율: {financial_metrics.get('pb_ratio', 'N/A')}
        - ROE: {financial_metrics.get('roe', 'N/A')}
        - 부채비율: {financial_metrics.get('debt_to_equity', 'N/A')}
        - 배당수익률: {financial_metrics.get('dividend_yield', 'N/A')}
        - 베타: {financial_metrics.get('beta', 'N/A')}
        - 매출성장률: {financial_metrics.get('revenue_growth', 'N/A')}
        - 순이익률: {financial_metrics.get('net_margin', 'N/A')}
        """

        # AI 분석 프롬프트
        prompt = f"""다음은 {symbol} ({company_info.get('name', 'N/A')})의 주식 데이터입니다:

{stock_summary}

이 데이터를 바탕으로 투자자가 이해하기 쉽게 분석해주세요:

## 📊 기업 개요
회사의 기본 정보와 사업 영역을 2-3줄로 요약

## 💰 주가 분석
현재 주가 수준과 최근 변동성을 2-3줄로 평가

## 📈 재무 건전성
P/E, P/B, ROE 등 주요 재무비율을 바탕으로 2-3줄로 분석

## 🏦 투자 매력도
밸류에이션, 성장성, 배당 등을 종합하여 2-3줄로 평가

## ⚠️ 리스크 요인
베타, 부채비율 등을 고려한 주요 위험요소 2-3줄

## 🎯 투자 의견
- 장점 2가지
- 단점 2가지
- 종합 의견 1줄

미국 주식 투자 관점에서 분석하고, 전문용어는 쉽게 설명해주세요."""

        print(f"[AI] Analysis starting: {symbol} (Model: {gemini_model})")

        # Gemini REST API 호출
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={gemini_api_key}"

        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {"Content-Type": "application/json"}

        response = requests.post(gemini_url, json=payload, headers=headers, timeout=45)

        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                analysis_result = result["candidates"][0]["content"]["parts"][0]["text"]
                print(
                    f"[SUCCESS] AI analysis complete: {len(analysis_result)} characters"
                )

                return jsonify(
                    {
                        "analysis": analysis_result,
                        "symbol": symbol,
                        "company_name": company_info.get("name", "N/A"),
                        "model_used": gemini_model,
                    }
                )
            else:
                raise Exception("Gemini API 응답에서 분석 결과를 찾을 수 없습니다.")
        else:
            error_detail = (
                response.json()
                if response.headers.get("content-type") == "application/json"
                else response.text
            )
            raise Exception(f"Gemini API 오류 ({response.status_code}): {error_detail}")

    except Exception as e:
        error_msg = f"AI 분석 중 오류 발생: {str(e)}"
        print(f"❌ {error_msg}")
        return jsonify({"error": error_msg}), 500


@app.route("/api/compare_companies", methods=["POST"])
def compare_companies():
    """기업 비교를 위한 데이터 조회"""
    data = request.get_json()
    corp_code = data.get("corp_code")

    if not corp_code:
        return jsonify({"error": "회사 코드가 필요합니다."}), 400

    print(f"[REQUEST] Company comparison data: {corp_code}")

    try:
        # 재무 데이터 조회
        api_key = os.getenv("OPEN_DART_API_KEY")
        url = "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"
        params = {
            "crtfc_key": api_key,
            "corp_code": corp_code,
            "bsns_year": "2024",
            "reprt_code": "11011",
        }

        response = requests.get(url, params=params)
        result = response.json()

        if result.get("status") != "000":
            return jsonify({"error": "재무 데이터를 가져올 수 없습니다."}), 404

        # 재무 데이터 파싱
        financial_data = {}
        for item in result.get("list", []):
            account_nm = item.get("account_nm", "")
            amount = int(item.get("thstrm_amount", "0").replace(",", "") or 0)

            if "자산총계" in account_nm:
                financial_data["assets"] = amount
            elif "부채총계" in account_nm:
                financial_data["liabilities"] = amount
            elif "자본총계" in account_nm:
                financial_data["equity"] = amount
            elif "매출액" in account_nm and "매출액" == account_nm:
                financial_data["revenue"] = amount
            elif "영업이익" in account_nm:
                financial_data["operating_profit"] = amount
            elif "당기순이익" in account_nm:
                financial_data["net_income"] = amount

        # 재무 비율 계산
        if financial_data.get("liabilities") and financial_data.get("assets"):
            financial_data["debt_ratio"] = (
                financial_data["liabilities"] / financial_data["assets"]
            )

        if financial_data.get("net_income") and financial_data.get("equity"):
            financial_data["roe"] = (
                financial_data["net_income"] / financial_data["equity"]
            )

        # 주가 데이터 조회
        korean_api = KoreanStockAPI()
        stock_code = korean_api.get_stock_code_from_corp_code(
            corp_code, corp_codes_data
        )
        stock_data = None

        if stock_code:
            stock_data = korean_api.get_korean_stock_chart_data(stock_code, days=90)

        print(f"[SUCCESS] Comparison data retrieved for {corp_code}")

        return jsonify({"financial_data": financial_data, "stock_data": stock_data})

    except Exception as e:
        print(f"[ERROR] Comparison data error: {e}")
        return jsonify({"error": "데이터 조회 중 오류가 발생했습니다."}), 500


@app.route("/api/analyze_financial_data", methods=["POST"])
def analyze_financial_data():
    """Gemini AI를 사용하여 재무제표 데이터를 분석하고 쉬운 설명 제공"""

    # Gemini API 키 확인
    if not gemini_api_key or gemini_api_key == "your_gemini_api_key_here":
        return jsonify({"error": "Gemini API 키가 설정되지 않았습니다."}), 500

    data = request.get_json()
    financial_data = data.get("financial_data")
    company_name = data.get("company_name", "해당 회사")
    year = data.get("year", "해당 연도")
    stock_chart_data = data.get("stock_chart_data")  # 주가 데이터 추가

    if not financial_data:
        return jsonify({"error": "분석할 재무 데이터가 없습니다."}), 400

    try:
        # 재무 데이터를 텍스트로 변환
        assets = financial_data.get("balanceSheet", {}).get("assets", 0)
        liabilities = financial_data.get("balanceSheet", {}).get("liabilities", 0)
        equity = financial_data.get("balanceSheet", {}).get("equity", 0)
        revenue = financial_data.get("incomeStatement", {}).get("revenue", 0)
        operating_profit = financial_data.get("incomeStatement", {}).get(
            "operatingProfit", 0
        )
        net_income = financial_data.get("incomeStatement", {}).get("netIncome", 0)

        financial_summary = f"""
        회사명: {company_name}
        분석 연도: {year}년
        
        재무상태표:
        - 총자산: {assets:,}원
        - 총부채: {liabilities:,}원
        - 총자본: {equity:,}원
        
        손익계산서:
        - 매출액: {revenue:,}원
        - 영업이익: {operating_profit:,}원
        - 당기순이익: {net_income:,}원
        """

        # 주가 데이터 추가
        stock_summary = ""
        if stock_chart_data and stock_chart_data.get("data"):
            stock_data = stock_chart_data["data"]
            latest_price = stock_chart_data.get("latest_price", 0)
            price_change = stock_chart_data.get("price_change", 0)
            price_change_percent = stock_chart_data.get("price_change_percent", 0)

            # 최근 3개월 주가 추이 계산
            if len(stock_data) > 0:
                first_price = stock_data[0]["close"]
                three_month_change = ((latest_price - first_price) / first_price) * 100

                # 최고가/최저가
                prices = [d["close"] for d in stock_data]
                high_price = max(prices)
                low_price = min(prices)

                stock_summary = f"""
        
        주가 정보 (최근 3개월):
        - 현재 주가: {latest_price:,}원
        - 전일 대비: {price_change:+,.0f}원 ({price_change_percent:+.2f}%)
        - 3개월 변동: {three_month_change:+.2f}%
        - 3개월 최고가: {high_price:,}원
        - 3개월 최저가: {low_price:,}원
        - 거래일 수: {len(stock_data)}일
                """
                print(
                    f"[INFO] Stock data included: Current {latest_price:,} KRW, 3-month change {three_month_change:+.2f}%"
                )

        # AI 분석 프롬프트 (주가 데이터 포함)
        if stock_summary:
            prompt = f"""다음은 {company_name}의 {year}년 재무제표와 최근 주가 데이터입니다:

{financial_summary}{stock_summary}

재무제표와 주가 데이터를 종합하여 일반인이 이해하기 쉽게 분석해주세요:

## 📊 재무 건전성
회사의 전반적인 재무 상태를 2-3줄로 요약

## 💰 수익성 분석
매출과 이익 구조를 2-3줄로 설명

## 🏦 안정성 평가
자산, 부채, 자본의 균형을 2-3줄로 평가

## 📈 주가 동향 분석
최근 3개월 주가 흐름과 변동성을 2-3줄로 분석

## 💡 재무제표와 주가의 상관관계
재무 실적이 주가에 어떻게 반영되고 있는지 2-3줄로 설명

## 🎯 투자 의견
- 장점 2가지
- 단점 2가지
- 종합 투자 의견 1-2줄

전문용어는 쉽게 풀어서 설명하고, 구체적인 수치를 활용해주세요."""
        else:
            prompt = f"""다음은 {company_name}의 {year}년 재무제표입니다:

{financial_summary}

이 데이터를 바탕으로 일반인이 이해하기 쉽게 분석해주세요:

## 📊 재무 건전성
회사의 전반적인 재무 상태를 2-3줄로 요약

## 💰 수익성 분석
매출과 이익 구조를 2-3줄로 설명

## 🏦 안정성 평가
자산, 부채, 자본의 균형을 2-3줄로 평가

## 📈 투자 관점
투자 매력도와 주의사항을 2-3줄로 정리

## 🎯 핵심 포인트
- 주요 특징 3가지를 간단히

전문용어는 쉽게 풀어서 설명하고, 구체적인 수치를 활용해주세요.
(참고: 주가 데이터는 비상장 회사이거나 데이터를 가져올 수 없어 제외되었습니다)"""

        print(f"[AI] Analysis starting: {company_name} {year} (Model: {gemini_model})")

        # Gemini REST API 호출
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={gemini_api_key}"

        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {"Content-Type": "application/json"}

        response = requests.post(gemini_url, json=payload, headers=headers, timeout=45)

        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                analysis_result = result["candidates"][0]["content"]["parts"][0]["text"]
                print(
                    f"[SUCCESS] AI analysis complete: {len(analysis_result)} characters"
                )

                return jsonify(
                    {
                        "analysis": analysis_result,
                        "company_name": company_name,
                        "year": year,
                        "model_used": gemini_model,
                    }
                )
            else:
                raise Exception("Gemini API 응답에서 분석 결과를 찾을 수 없습니다.")
        else:
            error_detail = (
                response.json()
                if response.headers.get("content-type") == "application/json"
                else response.text
            )
            raise Exception(f"Gemini API 오류 ({response.status_code}): {error_detail}")

    except Exception as e:
        error_msg = f"AI 분석 중 오류 발생: {str(e)}"
        print(f"❌ {error_msg}")
        return jsonify({"error": error_msg}), 500


if __name__ == "__main__":
    import webbrowser
    import threading

    # 프로덕션 환경 감지
    is_production = os.environ.get("FLASK_ENV") == "production" or os.environ.get(
        "PORT"
    )

    if not is_production:
        # 개발 환경: 브라우저 자동 열기
        def open_browser():
            webbrowser.open("http://127.0.0.1:5000")

        # Flask reloader 때문에 브라우저가 두 번 열리는 것을 방지
        if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
            threading.Timer(1, open_browser).start()

        print("[INFO] Financial Statement Analysis Application starting...")
        print(
            "[INFO] Browser will open automatically. If not, visit http://127.0.0.1:5000"
        )

    # 포트 설정 (프로덕션 환경에서는 환경변수 사용)
    port = int(os.environ.get("PORT", 5000))
    debug = not is_production

    app.run(debug=debug, host="0.0.0.0", port=port)

import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

# 환경변수 로드
load_dotenv()

class PolygonAPI:
    def __init__(self):
        self.api_key = os.getenv('POLYGON_API_KEY')
        self.base_url = "https://api.polygon.io"
        
        if not self.api_key or self.api_key == 'your_polygon_api_key_here':
            raise ValueError("POLYGON_API_KEY가 설정되지 않았습니다. .env 파일을 확인해주세요.")
    
    def get_stock_tickers(self, limit=10):
        """미국 주식 티커 목록 조회 (무료 플랜 가능)"""
        url = f"{self.base_url}/v3/reference/tickers"
        params = {
            'market': 'stocks',
            'active': 'true',
            'limit': limit,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 요청 오류: {e}")
            return None
    
    def get_daily_bars(self, ticker, date=None):
        """특정 주식의 일봉 데이터 조회 (무료 플랜 가능)"""
        if not date:
            # 어제 날짜 사용 (주말 고려)
            date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        url = f"{self.base_url}/v1/open-close/{ticker}/{date}"
        params = {'apikey': self.api_key}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 요청 오류: {e}")
            return None
    
    def get_aggregates(self, ticker, from_date, to_date):
        """주식 집계 데이터 조회 (무료 플랜 가능, 2년 제한)"""
        url = f"{self.base_url}/v2/aggs/ticker/{ticker}/range/1/day/{from_date}/{to_date}"
        params = {'apikey': self.api_key}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 요청 오류: {e}")
            return None

def test_polygon_api():
    """Polygon API 테스트"""
    try:
        api = PolygonAPI()
        print("=== Polygon.io API 테스트 시작 ===\n")
        
        # 1. 주식 티커 목록 조회
        print("1. 주식 티커 목록 조회 (상위 5개)")
        tickers_data = api.get_stock_tickers(limit=5)
        if tickers_data and 'results' in tickers_data:
            for ticker in tickers_data['results']:
                print(f"   - {ticker['ticker']}: {ticker.get('name', 'N/A')}")
        print()
        
        # 2. AAPL 일봉 데이터 조회
        print("2. AAPL 일봉 데이터 조회")
        aapl_data = api.get_daily_bars('AAPL')
        if aapl_data:
            print(f"   날짜: {aapl_data.get('from', 'N/A')}")
            print(f"   시가: ${aapl_data.get('open', 'N/A')}")
            print(f"   고가: ${aapl_data.get('high', 'N/A')}")
            print(f"   저가: ${aapl_data.get('low', 'N/A')}")
            print(f"   종가: ${aapl_data.get('close', 'N/A')}")
            print(f"   거래량: {aapl_data.get('volume', 'N/A'):,}")
        print()
        
        # 3. AAPL 최근 1개월 데이터 조회
        print("3. AAPL 최근 1개월 집계 데이터")
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        agg_data = api.get_aggregates('AAPL', start_date, end_date)
        if agg_data and 'results' in agg_data:
            print(f"   데이터 개수: {len(agg_data['results'])}개")
            if agg_data['results']:
                latest = agg_data['results'][-1]
                print(f"   최신 종가: ${latest.get('c', 'N/A')}")
                print(f"   최신 거래량: {latest.get('v', 'N/A'):,}")
        
        print("\n=== API 테스트 완료 ===")
        print("무료 플랜으로 기본적인 주가 데이터는 잘 가져올 수 있습니다!")
        
    except ValueError as e:
        print(f"설정 오류: {e}")
    except Exception as e:
        print(f"예상치 못한 오류: {e}")

if __name__ == "__main__":
    test_polygon_api()
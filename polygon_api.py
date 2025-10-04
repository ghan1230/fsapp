import os
import requests
from datetime import datetime, timedelta
import json

class PolygonAPI:
    def __init__(self):
        self.api_key = os.getenv('POLYGON_API_KEY')
        self.base_url = "https://api.polygon.io"
        
        if not self.api_key or self.api_key == 'your_polygon_api_key_here':
            raise ValueError("POLYGON_API_KEY가 설정되지 않았습니다.")
    
    def search_tickers(self, search_term, limit=10):
        """주식 티커 검색"""
        url = f"{self.base_url}/v3/reference/tickers"
        params = {
            'search': search_term,
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
            print(f"티커 검색 오류: {e}")
            return None
    
    def get_ticker_details(self, ticker):
        """특정 티커의 상세 정보"""
        url = f"{self.base_url}/v3/reference/tickers/{ticker}"
        params = {'apikey': self.api_key}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"티커 상세정보 오류: {e}")
            return None
    
    def get_aggregates(self, ticker, from_date, to_date, timespan='day'):
        """주식 집계 데이터 조회"""
        url = f"{self.base_url}/v2/aggs/ticker/{ticker}/range/1/{timespan}/{from_date}/{to_date}"
        params = {
            'adjusted': 'true',
            'sort': 'asc',
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"집계 데이터 오류: {e}")
            return None
    
    def get_previous_close(self, ticker):
        """전일 종가 정보"""
        url = f"{self.base_url}/v2/aggs/ticker/{ticker}/prev"
        params = {'apikey': self.api_key}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"전일 종가 오류: {e}")
            return None
    
    def get_market_status(self):
        """시장 상태 확인"""
        url = f"{self.base_url}/v1/marketstatus/now"
        params = {'apikey': self.api_key}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"시장 상태 오류: {e}")
            return None
    
    def format_financial_data(self, ticker_data, price_data):
        """재무 데이터를 한국 주식과 유사한 형태로 포맷팅"""
        if not ticker_data or not price_data:
            return None
        
        results = ticker_data.get('results', {})
        price_results = price_data.get('results', [])
        
        if not price_results:
            return None
        
        latest_price = price_results[-1]
        
        # 기본 정보
        formatted_data = {
            'company_info': {
                'ticker': results.get('ticker', ''),
                'name': results.get('name', ''),
                'market': results.get('market', ''),
                'locale': results.get('locale', ''),
                'currency_name': results.get('currency_name', 'USD'),
                'description': results.get('description', ''),
                'homepage_url': results.get('homepage_url', ''),
                'total_employees': results.get('total_employees', 0),
                'market_cap': results.get('market_cap', 0),
                'weighted_shares_outstanding': results.get('weighted_shares_outstanding', 0)
            },
            'price_info': {
                'current_price': latest_price.get('c', 0),  # close
                'open_price': latest_price.get('o', 0),     # open
                'high_price': latest_price.get('h', 0),     # high
                'low_price': latest_price.get('l', 0),      # low
                'volume': latest_price.get('v', 0),         # volume
                'timestamp': latest_price.get('t', 0),      # timestamp
                'trading_day': datetime.fromtimestamp(latest_price.get('t', 0) / 1000).strftime('%Y-%m-%d') if latest_price.get('t') else ''
            },
            'historical_data': []
        }
        
        # 히스토리컬 데이터 (최근 30일)
        for price in price_results[-30:]:
            formatted_data['historical_data'].append({
                'date': datetime.fromtimestamp(price.get('t', 0) / 1000).strftime('%Y-%m-%d') if price.get('t') else '',
                'open': price.get('o', 0),
                'high': price.get('h', 0),
                'low': price.get('l', 0),
                'close': price.get('c', 0),
                'volume': price.get('v', 0)
            })
        
        return formatted_data
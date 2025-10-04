import os
import requests
from datetime import datetime, timedelta
import json
import yfinance as yf

class FinnhubAPI:
    def __init__(self):
        self.api_key = os.getenv('FINNHUB_API_KEY')
        self.base_url = "https://finnhub.io/api/v1"
        
        if not self.api_key or self.api_key == 'your_finnhub_api_key_here':
            raise ValueError("FINNHUB_API_KEY가 설정되지 않았습니다.")
    
    def search_symbol(self, query):
        """주식 심볼 검색"""
        url = f"{self.base_url}/search"
        params = {
            'q': query,
            'token': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"심볼 검색 오류: {e}")
            return None
    
    def get_company_profile(self, symbol):
        """회사 프로필 정보"""
        url = f"{self.base_url}/stock/profile2"
        params = {
            'symbol': symbol,
            'token': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"회사 프로필 오류: {e}")
            return None
    
    def get_quote(self, symbol):
        """실시간 주가 정보"""
        url = f"{self.base_url}/quote"
        params = {
            'symbol': symbol,
            'token': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"주가 정보 오류: {e}")
            return None
    
    def get_candles(self, symbol, resolution='D', from_date=None, to_date=None):
        """캔들스틱 데이터 (OHLCV) - Yahoo Finance 백업 사용"""
        if not from_date:
            from_date = int((datetime.now() - timedelta(days=90)).timestamp())
        if not to_date:
            to_date = int(datetime.now().timestamp())
        
        # 먼저 Finnhub API 시도
        url = f"{self.base_url}/stock/candle"
        params = {
            'symbol': symbol,
            'resolution': resolution,
            'from': from_date,
            'to': to_date,
            'token': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('s') == 'ok':
                    return data
        except:
            pass
        
        # Finnhub 실패시 Yahoo Finance 사용
        print(f"Finnhub 캔들 데이터 제한, Yahoo Finance로 대체: {symbol}")
        return self.get_yahoo_candles(symbol, days=90)
    
    def get_yahoo_candles(self, symbol, days=90):
        """Yahoo Finance에서 캔들 데이터 가져오기"""
        try:
            ticker = yf.Ticker(symbol)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            hist = ticker.history(start=start_date, end=end_date)
            
            if hist.empty:
                return None
            
            # Finnhub 형식으로 변환
            timestamps = [int(date.timestamp()) for date in hist.index]
            opens = hist['Open'].tolist()
            highs = hist['High'].tolist()
            lows = hist['Low'].tolist()
            closes = hist['Close'].tolist()
            volumes = hist['Volume'].tolist()
            
            return {
                's': 'ok',
                't': timestamps,
                'o': opens,
                'h': highs,
                'l': lows,
                'c': closes,
                'v': volumes
            }
            
        except Exception as e:
            print(f"Yahoo Finance 데이터 오류: {e}")
            return None
    
    def get_basic_financials(self, symbol, metric='all'):
        """기본 재무 지표 - 무료 플랜에서 사용 가능!"""
        url = f"{self.base_url}/stock/metric"
        params = {
            'symbol': symbol,
            'metric': metric,
            'token': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"재무 지표 오류: {e}")
            return None
    
    def get_financials_reported(self, symbol, freq='annual'):
        """보고된 재무제표 데이터"""
        url = f"{self.base_url}/stock/financials-reported"
        params = {
            'symbol': symbol,
            'freq': freq,
            'token': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"재무제표 오류: {e}")
            return None
    
    def get_earnings(self, symbol):
        """실적 발표 정보"""
        url = f"{self.base_url}/stock/earnings"
        params = {
            'symbol': symbol,
            'token': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"실적 정보 오류: {e}")
            return None
    
    def get_recommendation_trends(self, symbol):
        """분석가 추천 동향"""
        url = f"{self.base_url}/stock/recommendation"
        params = {
            'symbol': symbol,
            'token': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"추천 동향 오류: {e}")
            return None
    
    def get_company_news(self, symbol, from_date=None, to_date=None):
        """기업 관련 뉴스 조회 (무료 API)"""
        if not from_date:
            from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not to_date:
            to_date = datetime.now().strftime('%Y-%m-%d')
        
        url = f"{self.base_url}/company-news"
        params = {
            'symbol': symbol,
            'from': from_date,
            'to': to_date,
            'token': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"뉴스 조회 오류: {e}")
            return None
    
    def get_dividends(self, symbol):
        """배당 정보 조회 - Yahoo Finance 사용 (개선 버전)"""
        try:
            ticker = yf.Ticker(symbol)
            dividends = ticker.dividends
            
            if dividends.empty:
                return None
            
            # 최근 배당 데이터
            recent_dividends = dividends.tail(20)  # 최근 20개 배당
            
            # 배당 성장률 계산 (최근 5년)
            growth_rate = 0
            if len(recent_dividends) >= 8:  # 최소 2년치 데이터 (분기배당 기준)
                old_annual = recent_dividends.iloc[:4].sum()
                new_annual = recent_dividends.iloc[-4:].sum()
                if old_annual > 0:
                    years = (len(recent_dividends) - 1) / 4  # 분기 수를 연도로 변환
                    growth_rate = ((new_annual / old_annual) ** (1 / years) - 1) * 100
            
            # 배당 주기 계산 (다음 배당일 예측)
            next_dividend_date = None
            dividend_frequency = 'Unknown'
            
            if len(recent_dividends) >= 2:
                # 최근 2개 배당일 간격 계산
                dates = recent_dividends.index[-2:]
                days_diff = (dates[1] - dates[0]).days
                
                # 배당 주기 판단
                if 80 <= days_diff <= 100:
                    dividend_frequency = 'Quarterly'
                    next_dividend_date = (recent_dividends.index[-1] + timedelta(days=90)).strftime('%Y-%m-%d')
                elif 170 <= days_diff <= 190:
                    dividend_frequency = 'Semi-Annual'
                    next_dividend_date = (recent_dividends.index[-1] + timedelta(days=180)).strftime('%Y-%m-%d')
                elif 350 <= days_diff <= 380:
                    dividend_frequency = 'Annual'
                    next_dividend_date = (recent_dividends.index[-1] + timedelta(days=365)).strftime('%Y-%m-%d')
                elif 25 <= days_diff <= 35:
                    dividend_frequency = 'Monthly'
                    next_dividend_date = (recent_dividends.index[-1] + timedelta(days=30)).strftime('%Y-%m-%d')
            
            dividend_data = {
                'history': [
                    {
                        'date': date.strftime('%Y-%m-%d'),
                        'amount': float(amount)
                    }
                    for date, amount in recent_dividends.items()
                ],
                'latest_dividend': float(recent_dividends.iloc[-1]) if len(recent_dividends) > 0 else 0,
                'annual_dividend': float(recent_dividends.tail(4).sum()) if len(recent_dividends) >= 4 else 0,
                'growth_rate': round(growth_rate, 2),  # 배당 성장률 (%)
                'next_dividend_date': next_dividend_date,  # 다음 배당일 예측
                'dividend_frequency': dividend_frequency  # 배당 주기
            }
            
            return dividend_data
            
        except Exception as e:
            print(f"배당 정보 오류: {e}")
            return None
    
    def get_peers(self, symbol):
        """동종 업계 기업 조회"""
        url = f"{self.base_url}/stock/peers"
        params = {
            'symbol': symbol,
            'token': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"동종 업계 조회 오류: {e}")
            return None
    
    def format_comprehensive_data(self, symbol):
        """종합적인 주식 데이터 포맷팅"""
        try:
            # 모든 데이터를 병렬로 가져오기
            profile = self.get_company_profile(symbol)
            quote = self.get_quote(symbol)
            financials = self.get_basic_financials(symbol)
            candles = self.get_candles(symbol)
            earnings = self.get_earnings(symbol)
            recommendations = self.get_recommendation_trends(symbol)
            news = self.get_company_news(symbol)
            dividends = self.get_dividends(symbol)
            peers = self.get_peers(symbol)
            
            if not profile or not quote:
                return None
            
            # 캔들 데이터 처리
            historical_data = []
            if candles and candles.get('s') == 'ok':
                timestamps = candles.get('t', [])
                opens = candles.get('o', [])
                highs = candles.get('h', [])
                lows = candles.get('l', [])
                closes = candles.get('c', [])
                volumes = candles.get('v', [])
                
                for i in range(len(timestamps)):
                    historical_data.append({
                        'date': datetime.fromtimestamp(timestamps[i]).strftime('%Y-%m-%d'),
                        'open': opens[i],
                        'high': highs[i],
                        'low': lows[i],
                        'close': closes[i],
                        'volume': volumes[i]
                    })
            
            # 종합 데이터 구성
            comprehensive_data = {
                'company_info': {
                    'symbol': profile.get('ticker', symbol),
                    'name': profile.get('name', ''),
                    'country': profile.get('country', ''),
                    'currency': profile.get('currency', 'USD'),
                    'exchange': profile.get('exchange', ''),
                    'ipo': profile.get('ipo', ''),
                    'market_capitalization': profile.get('marketCapitalization', 0),
                    'share_outstanding': profile.get('shareOutstanding', 0),
                    'industry': profile.get('finnhubIndustry', ''),
                    'website': profile.get('weburl', ''),
                    'logo': profile.get('logo', ''),
                    'phone': profile.get('phone', '')
                },
                'price_info': {
                    'current_price': quote.get('c', 0),
                    'change': quote.get('d', 0),
                    'percent_change': quote.get('dp', 0),
                    'high': quote.get('h', 0),
                    'low': quote.get('l', 0),
                    'open': quote.get('o', 0),
                    'previous_close': quote.get('pc', 0),
                    'timestamp': quote.get('t', 0)
                },
                'financial_metrics': {},
                'historical_data': historical_data,
                'earnings': earnings or [],
                'recommendations': recommendations or [],
                'news': news[:10] if news else [],  # 최근 10개 뉴스
                'dividends': dividends,
                'peers': peers or []
            }
            
            # 재무 지표 추가
            if financials and 'metric' in financials:
                metrics = financials['metric']
                comprehensive_data['financial_metrics'] = {
                    # 밸류에이션 지표
                    'pe_ratio': metrics.get('peBasicExclExtraTTM', 0),
                    'pb_ratio': metrics.get('pbQuarterly', 0),
                    'ps_ratio': metrics.get('psQuarterly', 0),
                    'ev_ebitda': metrics.get('evEbitdaTTM', 0),
                    
                    # 수익성 지표
                    'roe': metrics.get('roeRfy', 0),
                    'roa': metrics.get('roaRfy', 0),
                    'gross_margin': metrics.get('grossMarginTTM', 0),
                    'operating_margin': metrics.get('operatingMarginTTM', 0),
                    'net_margin': metrics.get('netProfitMarginTTM', 0),
                    
                    # 성장성 지표
                    'revenue_growth': metrics.get('revenueGrowthTTMYoy', 0),
                    'earnings_growth': metrics.get('epsGrowthTTMYoy', 0),
                    
                    # 안정성 지표
                    'debt_to_equity': metrics.get('totalDebt/totalEquityQuarterly', 0),
                    'current_ratio': metrics.get('currentRatioQuarterly', 0),
                    'quick_ratio': metrics.get('quickRatioQuarterly', 0),
                    
                    # 주당 지표
                    'eps': metrics.get('epsBasicExclExtraItemsTTM', 0),
                    'book_value_per_share': metrics.get('bookValuePerShareQuarterly', 0),
                    'dividend_yield': metrics.get('dividendYieldIndicatedAnnual', 0),
                    
                    # 기타
                    'beta': metrics.get('beta', 0),
                    '52_week_high': metrics.get('52WeekHigh', 0),
                    '52_week_low': metrics.get('52WeekLow', 0)
                }
            
            return comprehensive_data
            
        except Exception as e:
            print(f"종합 데이터 포맷팅 오류: {e}")
            return None
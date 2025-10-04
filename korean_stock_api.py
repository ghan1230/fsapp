import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import requests
import json

class KoreanStockAPI:
    def __init__(self):
        pass
    
    def get_stock_code_from_corp_code(self, corp_code, corp_codes_data):
        """회사 코드에서 주식 코드 찾기"""
        for company in corp_codes_data:
            if company.get('corp_code') == corp_code:
                stock_code = company.get('stock_code', '').strip()
                if stock_code and stock_code != '' and stock_code != ' ':
                    print(f"[INFO] Stock code found: {corp_code} -> {stock_code}")
                    return stock_code
                else:
                    print(f"[WARNING] Unlisted company: {company.get('corp_name', 'Unknown')} (corp_code: {corp_code})")
                    return None
        print(f"[ERROR] Company code not found: {corp_code}")
        return None
    
    def format_korean_ticker(self, stock_code):
        """한국 주식 코드를 Yahoo Finance 형식으로 변환"""
        if not stock_code:
            return None
        
        # 6자리 주식 코드에 .KS (KOSPI) 또는 .KQ (KOSDAQ) 추가
        # 일단 .KS로 시도하고, 실패하면 .KQ로 시도
        return f"{stock_code.zfill(6)}.KS"
    
    def get_korean_stock_chart_data(self, stock_code, days=90):
        """한국 주식 차트 데이터 가져오기"""
        if not stock_code:
            return None
        
        # KOSPI 시도
        ticker_ks = f"{stock_code.zfill(6)}.KS"
        chart_data = self._fetch_yahoo_data(ticker_ks, days)
        
        if chart_data:
            return chart_data
        
        # KOSDAQ 시도
        ticker_kq = f"{stock_code.zfill(6)}.KQ"
        chart_data = self._fetch_yahoo_data(ticker_kq, days)
        
        return chart_data
    
    def _fetch_yahoo_data(self, ticker, days):
        """Yahoo Finance에서 데이터 가져오기"""
        try:
            print(f"[REQUEST] Yahoo Finance data: {ticker}")
            stock = yf.Ticker(ticker)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # 더 안정적인 데이터 요청
            hist = stock.history(start=start_date, end=end_date, auto_adjust=True, prepost=True)
            
            if hist.empty:
                print(f"[WARNING] Empty data: {ticker}")
                return None
            
            print(f"[SUCCESS] Data received: {ticker}, {len(hist)} days")
            
            # 차트용 데이터 포맷팅
            chart_data = []
            for date, row in hist.iterrows():
                try:
                    chart_data.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'open': float(row['Open']) if not pd.isna(row['Open']) else 0,
                        'high': float(row['High']) if not pd.isna(row['High']) else 0,
                        'low': float(row['Low']) if not pd.isna(row['Low']) else 0,
                        'close': float(row['Close']) if not pd.isna(row['Close']) else 0,
                        'volume': int(row['Volume']) if not pd.isna(row['Volume']) else 0
                    })
                except (ValueError, TypeError) as e:
                    print(f"⚠️ 데이터 변환 오류 ({date}): {e}")
                    continue
            
            if not chart_data:
                print(f"[WARNING] No valid data: {ticker}")
                return None
            
            # 최신 가격 정보 계산
            latest_price = chart_data[-1]['close']
            previous_price = chart_data[-2]['close'] if len(chart_data) > 1 else latest_price
            price_change = latest_price - previous_price
            price_change_percent = (price_change / previous_price * 100) if previous_price != 0 else 0
            
            return {
                'ticker': ticker,
                'data': chart_data,
                'latest_price': latest_price,
                'price_change': price_change,
                'price_change_percent': price_change_percent
            }
            
        except Exception as e:
            print(f"[ERROR] Yahoo Finance Korean stock data error ({ticker}): {e}")
            return None
    
    def get_stock_info(self, stock_code):
        """한국 주식 기본 정보 가져오기"""
        ticker_ks = f"{stock_code.zfill(6)}.KS"
        ticker_kq = f"{stock_code.zfill(6)}.KQ"
        
        for ticker in [ticker_ks, ticker_kq]:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                
                if info and 'symbol' in info:
                    return {
                        'ticker': ticker,
                        'name': info.get('longName', info.get('shortName', '')),
                        'sector': info.get('sector', ''),
                        'industry': info.get('industry', ''),
                        'market_cap': info.get('marketCap', 0),
                        'currency': info.get('currency', 'KRW'),
                        'exchange': info.get('exchange', ''),
                        'website': info.get('website', ''),
                        'employees': info.get('fullTimeEmployees', 0)
                    }
            except:
                continue
        
        return None
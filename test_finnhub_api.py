import os
from dotenv import load_dotenv
from finnhub_api import FinnhubAPI
import json

# 환경변수 로드
load_dotenv()

def test_finnhub_api():
    """Finnhub API 테스트"""
    try:
        api = FinnhubAPI()
        print("=== Finnhub.io API 테스트 시작 ===\n")
        
        # 1. 심볼 검색 테스트
        print("1. 심볼 검색 테스트 (Apple)")
        search_result = api.search_symbol('Apple')
        if search_result and 'result' in search_result:
            for i, stock in enumerate(search_result['result'][:3]):
                print(f"   {i+1}. {stock.get('symbol', 'N/A')} - {stock.get('description', 'N/A')}")
        print()
        
        # 2. AAPL 회사 프로필
        print("2. AAPL 회사 프로필")
        profile = api.get_company_profile('AAPL')
        if profile:
            print(f"   회사명: {profile.get('name', 'N/A')}")
            print(f"   국가: {profile.get('country', 'N/A')}")
            print(f"   산업: {profile.get('finnhubIndustry', 'N/A')}")
            print(f"   시가총액: ${profile.get('marketCapitalization', 0):,}M")
            print(f"   IPO: {profile.get('ipo', 'N/A')}")
        print()
        
        # 3. AAPL 실시간 주가
        print("3. AAPL 실시간 주가")
        quote = api.get_quote('AAPL')
        if quote:
            print(f"   현재가: ${quote.get('c', 0):.2f}")
            print(f"   변동: ${quote.get('d', 0):.2f} ({quote.get('dp', 0):.2f}%)")
            print(f"   고가: ${quote.get('h', 0):.2f}")
            print(f"   저가: ${quote.get('l', 0):.2f}")
        print()
        
        # 4. AAPL 재무 지표 (핵심!)
        print("4. AAPL 재무 지표 (무료 플랜 포함!)")
        financials = api.get_basic_financials('AAPL')
        if financials and 'metric' in financials:
            metrics = financials['metric']
            print(f"   P/E 비율: {metrics.get('peBasicExclExtraTTM', 'N/A')}")
            print(f"   P/B 비율: {metrics.get('pbQuarterly', 'N/A')}")
            print(f"   ROE: {metrics.get('roeRfy', 'N/A'):.2%}" if metrics.get('roeRfy') else "   ROE: N/A")
            print(f"   부채비율: {metrics.get('totalDebt/totalEquityQuarterly', 'N/A')}")
            print(f"   배당수익률: {metrics.get('dividendYieldIndicatedAnnual', 'N/A'):.2%}" if metrics.get('dividendYieldIndicatedAnnual') else "   배당수익률: N/A")
            print(f"   베타: {metrics.get('beta', 'N/A')}")
        print()
        
        # 5. 실적 정보
        print("5. AAPL 실적 정보")
        earnings = api.get_earnings('AAPL')
        if earnings and len(earnings) > 0:
            latest = earnings[0]
            print(f"   최근 실적: {latest.get('period', 'N/A')}")
            print(f"   EPS 예상: ${latest.get('epsEstimate', 'N/A')}")
            print(f"   EPS 실제: ${latest.get('epsActual', 'N/A')}")
            print(f"   매출 예상: ${latest.get('revenueEstimate', 'N/A'):,}" if latest.get('revenueEstimate') else "   매출 예상: N/A")
            print(f"   매출 실제: ${latest.get('revenueActual', 'N/A'):,}" if latest.get('revenueActual') else "   매출 실제: N/A")
        print()
        
        # 6. 분석가 추천
        print("6. AAPL 분석가 추천")
        recommendations = api.get_recommendation_trends('AAPL')
        if recommendations and len(recommendations) > 0:
            latest_rec = recommendations[0]
            print(f"   기간: {latest_rec.get('period', 'N/A')}")
            print(f"   강력매수: {latest_rec.get('strongBuy', 0)}명")
            print(f"   매수: {latest_rec.get('buy', 0)}명")
            print(f"   보유: {latest_rec.get('hold', 0)}명")
            print(f"   매도: {latest_rec.get('sell', 0)}명")
        print()
        
        # 7. 종합 데이터 테스트
        print("7. 종합 데이터 포맷팅 테스트")
        comprehensive = api.format_comprehensive_data('AAPL')
        if comprehensive:
            print(f"   ✅ 종합 데이터 생성 성공!")
            print(f"   - 회사 정보: {len(comprehensive['company_info'])}개 필드")
            print(f"   - 주가 정보: {len(comprehensive['price_info'])}개 필드")
            print(f"   - 재무 지표: {len(comprehensive['financial_metrics'])}개 지표")
            print(f"   - 히스토리: {len(comprehensive['historical_data'])}일 데이터")
        
        print("\n=== Finnhub API 테스트 완료 ===")
        print("✅ 무료 플랜으로 재무제표 분석이 가능합니다!")
        print("📊 재무 지표, 실적, 분석가 추천까지 모두 제공!")
        
    except ValueError as e:
        print(f"설정 오류: {e}")
        print("https://finnhub.io 에서 무료 API 키를 발급받아 .env 파일에 설정해주세요.")
    except Exception as e:
        print(f"예상치 못한 오류: {e}")

if __name__ == "__main__":
    test_finnhub_api()
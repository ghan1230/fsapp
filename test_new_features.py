"""
새로운 기능 테스트: 뉴스, 배당, 동종업계 비교
"""
from dotenv import load_dotenv
load_dotenv()

from finnhub_api import FinnhubAPI
import json

def test_news():
    """뉴스 API 테스트 (필터링 포함)"""
    print("\n=== 뉴스 API 테스트 (필터링 포함) ===")
    try:
        api = FinnhubAPI()
        symbol = "AAPL"
        
        print(f"[TEST] {symbol} 뉴스 조회 중...")
        news = api.get_company_news(symbol)
        
        if news:
            print(f"✅ 뉴스 {len(news)}개 조회 성공")
            
            # 감성별 분류
            positive = [n for n in news if n.get('sentiment', 0) > 0]
            negative = [n for n in news if n.get('sentiment', 0) < 0]
            neutral = [n for n in news if n.get('sentiment', 0) == 0]
            
            print(f"\n감성 분석 결과:")
            print(f"   긍정 뉴스: {len(positive)}개")
            print(f"   부정 뉴스: {len(negative)}개")
            print(f"   중립 뉴스: {len(neutral)}개")
            
            print("\n최근 뉴스 3개:")
            for i, article in enumerate(news[:3], 1):
                sentiment = article.get('sentiment', 0)
                sentiment_text = '긍정' if sentiment > 0 else '부정' if sentiment < 0 else '중립'
                print(f"\n{i}. {article.get('headline', 'N/A')}")
                print(f"   출처: {article.get('source', 'N/A')}")
                print(f"   감성: {sentiment_text} ({sentiment})")
                print(f"   URL: {article.get('url', 'N/A')[:50]}...")
        else:
            print("❌ 뉴스 조회 실패")
            
    except Exception as e:
        print(f"❌ 오류: {e}")


def test_dividends():
    """배당 정보 테스트 (개선 버전)"""
    print("\n=== 배당 정보 테스트 (개선 버전) ===")
    try:
        api = FinnhubAPI()
        
        # 배당주로 유명한 종목들 테스트
        symbols = ["AAPL", "MSFT", "KO", "JNJ"]
        
        for symbol in symbols:
            print(f"\n[TEST] {symbol} 배당 정보 조회 중...")
            dividends = api.get_dividends(symbol)
            
            if dividends:
                print(f"✅ {symbol} 배당 정보 조회 성공")
                print(f"   최근 배당금: ${dividends.get('latest_dividend', 0):.4f}")
                print(f"   연간 배당금 (추정): ${dividends.get('annual_dividend', 0):.2f}")
                print(f"   배당 성장률: {dividends.get('growth_rate', 0):+.2f}% (연평균)")
                print(f"   배당 주기: {dividends.get('dividend_frequency', 'Unknown')}")
                print(f"   다음 배당일 예상: {dividends.get('next_dividend_date', 'N/A')}")
                print(f"   배당 히스토리: {len(dividends.get('history', []))}개")
                
                # 최근 3개 배당 표시
                history = dividends.get('history', [])
                if history:
                    print("   최근 배당:")
                    for div in history[-3:]:
                        print(f"     - {div['date']}: ${div['amount']:.4f}")
            else:
                print(f"⚠️ {symbol} 배당 정보 없음 (무배당 주식일 수 있음)")
                
    except Exception as e:
        print(f"❌ 오류: {e}")


def test_peers():
    """동종 업계 비교 테스트"""
    print("\n=== 동종 업계 비교 테스트 ===")
    try:
        api = FinnhubAPI()
        symbol = "AAPL"
        
        print(f"[TEST] {symbol} 동종 업계 조회 중...")
        peers = api.get_peers(symbol)
        
        if peers:
            print(f"✅ 동종 업계 {len(peers)}개 기업 조회 성공")
            print(f"   동종 업계: {', '.join(peers[:10])}")
            
            # 상위 3개 기업의 상세 정보
            print("\n상위 3개 기업 상세 정보:")
            for peer_symbol in peers[:3]:
                try:
                    profile = api.get_company_profile(peer_symbol)
                    quote = api.get_quote(peer_symbol)
                    
                    if profile and quote:
                        print(f"\n{peer_symbol} - {profile.get('name', 'N/A')}")
                        print(f"   현재가: ${quote.get('c', 0):.2f}")
                        print(f"   변동: {quote.get('dp', 0):+.2f}%")
                        print(f"   시가총액: ${profile.get('marketCapitalization', 0):,.0f}M")
                except:
                    print(f"   {peer_symbol}: 정보 조회 실패")
        else:
            print("❌ 동종 업계 조회 실패")
            
    except Exception as e:
        print(f"❌ 오류: {e}")


def test_comprehensive_data():
    """종합 데이터 테스트 (모든 기능 포함)"""
    print("\n=== 종합 데이터 테스트 ===")
    try:
        api = FinnhubAPI()
        symbol = "AAPL"
        
        print(f"[TEST] {symbol} 종합 데이터 조회 중...")
        data = api.format_comprehensive_data(symbol)
        
        if data:
            print(f"✅ {symbol} 종합 데이터 조회 성공")
            print(f"\n기업 정보:")
            print(f"   이름: {data['company_info']['name']}")
            print(f"   산업: {data['company_info']['industry']}")
            
            print(f"\n주가 정보:")
            print(f"   현재가: ${data['price_info']['current_price']:.2f}")
            print(f"   변동: {data['price_info']['percent_change']:+.2f}%")
            
            print(f"\n추가 데이터:")
            print(f"   뉴스: {len(data.get('news', []))}개")
            print(f"   배당 정보: {'있음' if data.get('dividends') else '없음'}")
            print(f"   동종 업계: {len(data.get('peers', []))}개")
            
            if data.get('dividends'):
                print(f"   최근 배당금: ${data['dividends']['latest_dividend']:.4f}")
            
            if data.get('peers'):
                print(f"   동종 업계 기업: {', '.join(data['peers'][:5])}")
        else:
            print("❌ 종합 데이터 조회 실패")
            
    except Exception as e:
        print(f"❌ 오류: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("새로운 기능 테스트 시작")
    print("=" * 60)
    
    test_news()
    test_dividends()
    test_peers()
    test_comprehensive_data()
    
    print("\n" + "=" * 60)
    print("테스트 완료")
    print("=" * 60)

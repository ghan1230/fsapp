from dotenv import load_dotenv
from finnhub_api import FinnhubAPI

load_dotenv()

def test_chart_data():
    """차트 데이터 테스트"""
    try:
        api = FinnhubAPI()
        
        print("=== 차트 데이터 테스트 ===\n")
        
        # AAPL 캔들 데이터 테스트
        print("1. AAPL 캔들 데이터 테스트")
        candles = api.get_candles('AAPL')
        
        if candles and candles.get('s') == 'ok':
            timestamps = candles.get('t', [])
            closes = candles.get('c', [])
            
            print(f"   ✅ 데이터 개수: {len(timestamps)}개")
            if timestamps and closes:
                print(f"   📅 기간: {timestamps[0]} ~ {timestamps[-1]}")
                print(f"   💰 가격 범위: ${min(closes):.2f} ~ ${max(closes):.2f}")
                print(f"   📊 최신 종가: ${closes[-1]:.2f}")
        else:
            print("   ❌ 캔들 데이터 없음")
        
        print()
        
        # 종합 데이터 테스트
        print("2. AAPL 종합 데이터 테스트")
        comprehensive = api.format_comprehensive_data('AAPL')
        
        if comprehensive:
            historical = comprehensive.get('historical_data', [])
            print(f"   ✅ 히스토리컬 데이터: {len(historical)}개")
            
            if historical:
                print(f"   📅 첫 날짜: {historical[0]['date']}")
                print(f"   📅 마지막 날짜: {historical[-1]['date']}")
                print(f"   💰 최신 종가: ${historical[-1]['close']:.2f}")
        else:
            print("   ❌ 종합 데이터 없음")
            
    except Exception as e:
        print(f"테스트 오류: {e}")

if __name__ == "__main__":
    test_chart_data()
from korean_stock_api import KoreanStockAPI
import json

def test_korean_chart():
    """한국 주식 차트 테스트"""
    try:
        api = KoreanStockAPI()
        
        print("=== 한국 주식 차트 테스트 ===\n")
        
        # 삼성전자 테스트 (005930)
        print("1. 삼성전자 (005930) 차트 데이터 테스트")
        chart_data = api.get_korean_stock_chart_data('005930')
        
        if chart_data:
            print(f"   ✅ 티커: {chart_data['ticker']}")
            print(f"   📊 데이터 개수: {len(chart_data['data'])}일")
            print(f"   💰 최신 주가: ₩{chart_data['latest_price']:,.0f}")
            print(f"   📈 변동: ₩{chart_data['price_change']:,.0f} ({chart_data['price_change_percent']:.2f}%)")
            
            if chart_data['data']:
                first_date = chart_data['data'][0]['date']
                last_date = chart_data['data'][-1]['date']
                print(f"   📅 기간: {first_date} ~ {last_date}")
        else:
            print("   ❌ 차트 데이터 없음")
        
        print()
        
        # SK하이닉스 테스트 (000660)
        print("2. SK하이닉스 (000660) 차트 데이터 테스트")
        chart_data2 = api.get_korean_stock_chart_data('000660')
        
        if chart_data2:
            print(f"   ✅ 티커: {chart_data2['ticker']}")
            print(f"   📊 데이터 개수: {len(chart_data2['data'])}일")
            print(f"   💰 최신 주가: ₩{chart_data2['latest_price']:,.0f}")
        else:
            print("   ❌ 차트 데이터 없음")
        
        print()
        
        # 기업 정보 테스트
        print("3. 삼성전자 기업 정보 테스트")
        info = api.get_stock_info('005930')
        
        if info:
            print(f"   ✅ 회사명: {info['name']}")
            print(f"   🏢 섹터: {info['sector']}")
            print(f"   🏭 산업: {info['industry']}")
            print(f"   💼 시가총액: ₩{info['market_cap']:,}" if info['market_cap'] else "   💼 시가총액: N/A")
        else:
            print("   ❌ 기업 정보 없음")
            
    except Exception as e:
        print(f"테스트 오류: {e}")

if __name__ == "__main__":
    test_korean_chart()
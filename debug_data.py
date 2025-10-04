import requests
import os
from dotenv import load_dotenv
import json

# .env 파일에서 환경변수 로드
load_dotenv()

def debug_financial_data():
    """재무 데이터 구조 분석"""
    api_key = os.getenv('OPEN_DART_API_KEY')
    
    # 삼성전자 회사코드
    corp_code = "00126380"
    bsns_year = "2023"
    reprt_code = "11011"  # 사업보고서
    
    url = "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"
    params = {
        'crtfc_key': api_key,
        'corp_code': corp_code,
        'bsns_year': bsns_year,
        'reprt_code': reprt_code
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get('status') == '000':
            print("📊 삼성전자 2023년 사업보고서 재무 데이터:")
            print("=" * 80)
            
            for i, item in enumerate(data.get('list', [])):
                account_nm = item.get('account_nm', '')
                thstrm_amount = item.get('thstrm_amount', '')
                fs_div = item.get('fs_div', '')
                sj_div = item.get('sj_div', '')
                
                print(f"{i+1:2d}. [{fs_div}] [{sj_div}] {account_nm}: {thstrm_amount}")
                
                # 주요 항목들 체크
                if any(keyword in account_nm for keyword in ['자산총계', '부채총계', '자본총계', '매출액', '영업이익', '당기순이익']):
                    print(f"    ⭐ 주요 항목 발견!")
            
            print("\n" + "=" * 80)
            print("🔍 재무상태표(BS) 항목들:")
            bs_items = [item for item in data.get('list', []) if item.get('sj_div') == 'BS']
            for item in bs_items:
                print(f"  - {item.get('account_nm')}: {item.get('thstrm_amount')}")
            
            print("\n🔍 손익계산서(IS) 항목들:")
            is_items = [item for item in data.get('list', []) if item.get('sj_div') == 'IS']
            for item in is_items:
                print(f"  - {item.get('account_nm')}: {item.get('thstrm_amount')}")
                
        else:
            print(f"❌ API 오류: {data.get('message')}")
            
    except Exception as e:
        print(f"❌ 예외 발생: {e}")

if __name__ == "__main__":
    debug_financial_data()
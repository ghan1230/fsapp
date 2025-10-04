import requests
import os
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

def test_2025_quarterly_data():
    """2025년 분기별 데이터 테스트"""
    api_key = os.getenv('OPEN_DART_API_KEY')
    
    # 삼성전자 회사코드: 00126380
    corp_code = "00126380"
    year = "2025"
    
    # 분기별 보고서 코드
    quarters = {
        "11013": "1분기보고서",
        "11012": "반기보고서", 
        "11014": "3분기보고서",
        "11011": "사업보고서"
    }
    
    print(f"🔍 2025년 분기별 데이터 확인 (삼성전자)")
    print("=" * 50)
    
    for reprt_code, reprt_name in quarters.items():
        url = "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"
        params = {
            'crtfc_key': api_key,
            'corp_code': corp_code,
            'bsns_year': year,
            'reprt_code': reprt_code
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                status = data.get('status')
                message = data.get('message')
                
                if status == '000':
                    data_count = len(data.get('list', []))
                    print(f"✅ {reprt_name}: 데이터 있음 ({data_count}개 항목)")
                    
                    # 매출액 확인
                    for item in data.get('list', []):
                        if (item.get('sj_div') == 'IS' and 
                            item.get('account_nm') == '매출액' and
                            item.get('fs_div') == 'CFS'):
                            revenue = item.get('thstrm_amount', '0').replace(',', '')
                            print(f"   📊 매출액: {int(revenue):,}원")
                            break
                else:
                    print(f"❌ {reprt_name}: {message}")
            else:
                print(f"❌ {reprt_name}: HTTP 오류 {response.status_code}")
                
        except Exception as e:
            print(f"❌ {reprt_name}: 예외 발생 - {e}")

def test_latest_available_data():
    """최신 가용 데이터 확인"""
    api_key = os.getenv('OPEN_DART_API_KEY')
    
    # 삼성전자 회사코드: 00126380
    corp_code = "00126380"
    
    print(f"\n🔍 최신 가용 데이터 확인")
    print("=" * 50)
    
    # 2024년과 2025년 사업보고서 확인
    for year in ["2025", "2024"]:
        url = "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"
        params = {
            'crtfc_key': api_key,
            'corp_code': corp_code,
            'bsns_year': year,
            'reprt_code': "11011"  # 사업보고서
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                status = data.get('status')
                message = data.get('message')
                
                if status == '000':
                    print(f"✅ {year}년 사업보고서: 데이터 있음")
                    
                    # 첫 번째 항목의 기간 정보 확인
                    if data.get('list'):
                        first_item = data['list'][0]
                        print(f"   📅 당기: {first_item.get('thstrm_nm', 'N/A')}")
                        print(f"   📅 당기일자: {first_item.get('thstrm_dt', 'N/A')}")
                else:
                    print(f"❌ {year}년 사업보고서: {message}")
            else:
                print(f"❌ {year}년 사업보고서: HTTP 오류 {response.status_code}")
                
        except Exception as e:
            print(f"❌ {year}년 사업보고서: 예외 발생 - {e}")

if __name__ == "__main__":
    test_2025_quarterly_data()
    test_latest_available_data()
    
    print(f"\n📋 결론:")
    print("- 2025년 사업보고서는 2026년 3월에 제출 예정")
    print("- 2025년 분기보고서는 각 분기 종료 후 45일 이내 제출")
    print("- 현재 시점에서는 2024년 사업보고서가 최신 연간 데이터")
import requests
import os
from dotenv import load_dotenv
import json

# .env 파일에서 환경변수 로드
load_dotenv()

def test_dart_api():
    """DART API 테스트"""
    api_key = os.getenv('OPEN_DART_API_KEY')
    
    # 삼성전자 회사코드: 00126380
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
    
    print(f"🔍 API 테스트 시작...")
    print(f"회사코드: {corp_code}")
    print(f"사업연도: {bsns_year}")
    print(f"보고서코드: {reprt_code}")
    print(f"API URL: {url}")
    
    try:
        response = requests.get(url, params=params)
        print(f"응답 상태코드: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"API 응답 상태: {data.get('status')}")
            print(f"API 메시지: {data.get('message')}")
            
            if data.get('status') == '000':
                print(f"✅ 성공! 데이터 개수: {len(data.get('list', []))}")
                
                # 처음 5개 항목 출력
                for i, item in enumerate(data.get('list', [])[:5]):
                    print(f"{i+1}. {item.get('account_nm')}: {item.get('thstrm_amount')}")
                
                return data
            else:
                print(f"❌ API 오류: {data.get('message')}")
                return None
        else:
            print(f"❌ HTTP 오류: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 예외 발생: {e}")
        return None

def test_multiple_years():
    """여러 연도 데이터 테스트"""
    api_key = os.getenv('OPEN_DART_API_KEY')
    
    # 삼성전자 회사코드: 00126380
    corp_code = "00126380"
    years = ["2025", "2024", "2023", "2022", "2021"]
    reprt_code = "11011"  # 사업보고서
    
    print(f"\n🔍 연도별 비교 테스트 시작...")
    
    results = {}
    
    for year in years:
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
                if data.get('status') == '000':
                    results[year] = data.get('list', [])
                    print(f"✅ {year}년 데이터: {len(data.get('list', []))}개")
                    
                    # 주요 재무 지표 추출
                    revenue = 0
                    operating_profit = 0
                    net_income = 0
                    
                    for item in data.get('list', []):
                        if item.get('sj_div') == 'IS' and item.get('fs_div') == 'CFS':
                            if item.get('account_nm') == '매출액':
                                revenue = int(item.get('thstrm_amount', '0').replace(',', ''))
                            elif item.get('account_nm') == '영업이익':
                                operating_profit = int(item.get('thstrm_amount', '0').replace(',', ''))
                            elif item.get('account_nm') == '당기순이익(손실)':
                                net_income = int(item.get('thstrm_amount', '0').replace(',', ''))
                    
                    print(f"  매출액: {revenue:,}원")
                    print(f"  영업이익: {operating_profit:,}원")
                    print(f"  당기순이익: {net_income:,}원")
                else:
                    print(f"❌ {year}년 API 오류: {data.get('message')}")
            else:
                print(f"❌ {year}년 HTTP 오류: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {year}년 예외 발생: {e}")
    
    return results

if __name__ == "__main__":
    # 단일 연도 테스트
    single_result = test_dart_api()
    
    # 다중 연도 테스트
    multi_result = test_multiple_years()
    
    print(f"\n📊 테스트 완료!")
    print(f"단일 연도 결과: {'성공' if single_result else '실패'}")
    print(f"다중 연도 결과: {len(multi_result)}개 연도 데이터 수집")
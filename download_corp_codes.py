import requests
import zipfile
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv
import json

# .env 파일에서 환경변수 로드
load_dotenv()

def download_corp_codes():
    """
    DART API를 사용하여 회사코드 파일을 다운로드하고 처리합니다.
    """
    # API 키 가져오기
    api_key = os.getenv('OPEN_DART_API_KEY')
    if not api_key:
        print("❌ OPEN_DART_API_KEY가 .env 파일에 설정되지 않았습니다.")
        return False
    
    # API 요청 URL
    url = "https://opendart.fss.or.kr/api/corpCode.xml"
    params = {
        'crtfc_key': api_key
    }
    
    print("📥 회사코드 파일 다운로드 중...")
    
    try:
        # API 요청
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # ZIP 파일로 저장
        zip_filename = "corpCode.zip"
        with open(zip_filename, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ ZIP 파일 다운로드 완료: {zip_filename}")
        
        # ZIP 파일 압축 해제
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(".")
            extracted_files = zip_ref.namelist()
            print(f"📂 압축 해제 완료: {extracted_files}")
        
        # XML 파일 파싱
        xml_filename = "CORPCODE.xml"
        if os.path.exists(xml_filename):
            parse_corp_codes(xml_filename)
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API 요청 실패: {e}")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

def parse_corp_codes(xml_filename):
    """
    XML 파일을 파싱하여 회사 정보를 추출합니다.
    """
    print(f"📊 {xml_filename} 파일 파싱 중...")
    
    try:
        tree = ET.parse(xml_filename)
        root = tree.getroot()
        
        companies = []
        
        for list_item in root.findall('.//list'):
            company = {}
            
            # 각 회사 정보 추출
            corp_code = list_item.find('corp_code')
            corp_name = list_item.find('corp_name')
            corp_eng_name = list_item.find('corp_eng_name')
            stock_code = list_item.find('stock_code')
            modify_date = list_item.find('modify_date')
            
            if corp_code is not None:
                company['corp_code'] = corp_code.text
            if corp_name is not None:
                company['corp_name'] = corp_name.text
            if corp_eng_name is not None:
                company['corp_eng_name'] = corp_eng_name.text
            if stock_code is not None:
                company['stock_code'] = stock_code.text
            if modify_date is not None:
                company['modify_date'] = modify_date.text
                
            companies.append(company)
        
        print(f"📈 총 {len(companies)}개 회사 정보 추출 완료")
        
        # JSON 파일로 저장
        json_filename = "corp_codes.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(companies, f, ensure_ascii=False, indent=2)
        
        print(f"💾 JSON 파일 저장 완료: {json_filename}")
        
        # 샘플 데이터 출력
        print("\n📋 샘플 데이터 (처음 5개):")
        for i, company in enumerate(companies[:5]):
            print(f"{i+1}. {company.get('corp_name', 'N/A')} ({company.get('corp_code', 'N/A')})")
            if company.get('stock_code'):
                print(f"   종목코드: {company['stock_code']}")
        
        return companies
        
    except ET.ParseError as e:
        print(f"❌ XML 파싱 오류: {e}")
        return []
    except Exception as e:
        print(f"❌ 파일 처리 오류: {e}")
        return []

if __name__ == "__main__":
    print("🚀 DART 회사코드 다운로드 시작")
    success = download_corp_codes()
    
    if success:
        print("\n✨ 모든 작업이 완료되었습니다!")
        print("📁 생성된 파일:")
        print("  - corpCode.zip (원본 ZIP 파일)")
        print("  - CORPCODE.xml (압축 해제된 XML 파일)")
        print("  - corp_codes.json (파싱된 JSON 데이터)")
    else:
        print("\n❌ 작업이 실패했습니다.")
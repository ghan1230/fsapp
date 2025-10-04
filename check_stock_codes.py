import json

# corp_codes.json 파일 확인
with open('corp_codes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 상장 회사만 필터링
listed_companies = [item for item in data if item.get('stock_code', '').strip()]

print(f"전체 회사 수: {len(data)}")
print(f"상장 회사 수: {len(listed_companies)}")
print("\n상장 회사 샘플:")

for i, company in enumerate(listed_companies[:10]):
    print(f"  {i+1}. {company['corp_name']}: {company['stock_code']} (회사코드: {company['corp_code']})")

# 삼성전자 찾기
samsung = [item for item in data if '삼성전자' in item.get('corp_name', '')]
if samsung:
    print(f"\n삼성전자 정보:")
    for s in samsung:
        print(f"  - {s['corp_name']}: 주식코드={s.get('stock_code', '').strip()}, 회사코드={s['corp_code']}")
"""
BwB Project Register → JSON exporter
Run this whenever you add/edit projects in the Excel register.
Usage: python update_projects.py
"""
import pandas as pd
import json
import re
import os

EXCEL_PATH = "BwB_Project_Experience_Interactive.xlsx"
OUTPUT_PATH = "projects.json"

GEO_KEYWORDS = {
    'Africa': ['Africa','Rwanda','Angola','Zambia','Togo','Malawi','Congo','Ivory Coast','Seychelles','Nigeria','Kenya'],
    'Asia-Pacific': ['Mongolia','Uzbekistan','Kyrgyzstan','Nepal','Cambodia','Fiji','Indonesia','Thailand','Pakistan','India','Asia','Pacific'],
    'Europe': ['EU ','European','Milan','Madrid','Copenhagen','Vienna','Manchester','London','Hounslow','Birmingham',' UK','Marseille','Munich','Lisbon','Scotland','Mediterranean','Ukraine','Ireland','Poland'],
}

def parse_budget(b):
    if pd.isna(b) or str(b).strip() == '': return '', 0, ''
    b = str(b).strip()
    m = re.match(r'(EUR|USD|GBP)\s*([\d,]+)', b)
    if m: return m.group(1), int(m.group(2).replace(',','')), b
    return '', 0, b

def infer_status(dates):
    d = str(dates)
    if any(y in d for y in ['2026','2027','2028','2029']): return 'Ongoing / Future'
    if d in ('','nan'): return 'Legacy'
    years = re.findall(r'20\d{2}', d)
    if years:
        if int(years[-1]) >= 2025: return 'Ongoing / Future'
        return 'Completed'
    return 'Legacy'

def infer_geo(row):
    txt = ' '.join(str(x) for x in row.values())
    for geo, kws in GEO_KEYWORDS.items():
        if any(kw.lower() in txt.lower() for kw in kws): return geo
    return 'Global / Multi-region'

def main():
    print(f"Reading {EXCEL_PATH}...")
    raw = pd.read_excel(EXCEL_PATH, sheet_name='Database', header=2)
    raw.columns = ['No','Project','Client','Dates','Status','Sector','Geography',
                   'Contact','Currency','Amount','Budget','Description','Role']
    df = raw[raw['Project'].notna() & (raw['Project'].astype(str).str.strip() != '')].copy()
    df = df.reset_index(drop=True)

    projects = []
    for i, row in df.iterrows():
        curr, amt, budget_str = parse_budget(row.get('Budget',''))
        proj = {
            'no': int(row['No']) if pd.notna(row['No']) else i+1,
            'project': str(row['Project']).strip(),
            'client': str(row['Client']).strip() if pd.notna(row['Client']) else '',
            'dates': str(row['Dates']).strip() if pd.notna(row['Dates']) else '',
            'sector': str(row['Sector']).strip() if pd.notna(row['Sector']) else '',
            'contact': str(row['Contact']).strip() if pd.notna(row['Contact']) else '',
            'desc': str(row['Description']).strip() if pd.notna(row['Description']) else '',
            'role': str(row['Role']).strip() if pd.notna(row['Role']) else '',
            'currency': curr,
            'amount': amt,
            'budget': budget_str,
            'status': str(row['Status']).strip() if pd.notna(row['Status']) else infer_status(row.get('Dates','')),
            'geo': str(row['Geography']).strip() if pd.notna(row['Geography']) else infer_geo(row),
            'keywords': f"{row.get('Sector','')} {row.get('Description','')}".lower()[:200],
        }
        projects.append(proj)

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=2, ensure_ascii=False)

    print(f"✓ Exported {len(projects)} projects to {OUTPUT_PATH}")

if __name__ == '__main__':
    main()

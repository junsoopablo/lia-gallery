#!/usr/bin/env python3
"""artworks.js + images/ → Supabase로 일회성 마이그레이션."""
import json
import os
import re
import sys
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
SUPABASE_URL = 'https://qalprtpedzvnodbzwqih.supabase.co'
SERVICE_KEY = json.load(open(os.path.join(HERE, 'secrets.json')))['supabase_service_key']

HEADERS = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
}


def parse_artworks_js(path):
    text = open(path, encoding='utf-8').read()
    m = re.search(r'const\s+artworks\s*=\s*(\[[\s\S]*?\]);?\s*$', text)
    if not m:
        # JSON-style with quoted keys (current format)
        m = re.search(r'const\s+artworks\s*=\s*(\[[\s\S]*\])\s*;?\s*$', text)
    arr_text = m.group(1)
    return json.loads(arr_text)


def upload_image(filename, data, content_type='image/jpeg', max_retries=3):
    import time
    url = f'{SUPABASE_URL}/storage/v1/object/artworks/{filename}'
    last_err = ''
    for attempt in range(max_retries):
        req = urllib.request.Request(url, data=data, method='POST', headers={
            **HEADERS,
            'Content-Type': content_type,
            'x-upsert': 'true',
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return True, resp.read().decode()
        except urllib.error.HTTPError as e:
            return False, e.read().decode('utf-8', errors='replace')
        except Exception as e:
            last_err = str(e)
            if attempt < max_retries - 1:
                time.sleep(1.5 * (attempt + 1))
                continue
    return False, last_err


def insert_artworks(rows):
    url = f'{SUPABASE_URL}/rest/v1/artworks'
    body = json.dumps(rows, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=body, method='POST', headers={
        **HEADERS,
        'Content-Type': 'application/json',
        'Prefer': 'return=representation',
    })
    try:
        with urllib.request.urlopen(req) as resp:
            return True, resp.read().decode()
    except urllib.error.HTTPError as e:
        return False, e.read().decode('utf-8', errors='replace')


def main():
    # 0) 기존 행 모두 삭제 (멱등성)
    del_url = f'{SUPABASE_URL}/rest/v1/artworks?id=gt.0'
    req = urllib.request.Request(del_url, method='DELETE', headers=HEADERS)
    try:
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print('DELETE 경고:', e.read().decode())

    artworks = parse_artworks_js(os.path.join(HERE, 'artworks.js'))
    print(f'마이그레이션 시작: {len(artworks)}개 작품')

    rows = []
    for i, art in enumerate(artworks):
        src = art['src']  # "images/IMG_7437.jpg"
        filename = os.path.basename(src)
        local_path = os.path.join(HERE, src)
        if not os.path.exists(local_path):
            print(f'  ⚠️  {filename}: 파일 없음, 건너뜀')
            continue

        # 1) 이미지 업로드
        with open(local_path, 'rb') as f:
            data = f.read()
        import time
        ok, msg = upload_image(filename, data)
        if not ok:
            print(f'  ✗ {filename}: 업로드 실패 — {msg}')
            continue
        print(f'  ✓ {filename} 업로드 ({len(data)//1024}KB)')
        time.sleep(0.3)  # SSL 안정화용

        # 2) DB 행 준비 (sort_order: 앞쪽일수록 큼)
        rows.append({
            'title': art.get('title', ''),
            'date': art.get('date', ''),
            'category': art.get('category', ''),
            'description': art.get('description', ''),
            'image_path': filename,
            'sort_order': len(artworks) - i,
        })

    # 3) 한 번에 insert
    print(f'\nDB insert: {len(rows)}개')
    ok, msg = insert_artworks(rows)
    if ok:
        print(f'✓ insert 성공')
    else:
        print(f'✗ insert 실패: {msg}')
        sys.exit(1)

    print('\n=== 마이그레이션 완료 ===')


if __name__ == '__main__':
    main()

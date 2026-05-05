#!/usr/bin/env python3
"""
리아의 중간정도 크기의 미술관 — 로컬 편집 서버.

이 서버를 실행해야 admin.html에서 저장 버튼이 동작합니다.
저장 누르면 artworks.js에 즉시 반영되고 갤러리에서 새로고침하면 보여요.

실행:
  python3 server.py
또는 macOS에서:
  start.command 더블클릭
"""
import http.server
import json
import os
import re
import socketserver
import subprocess
import sys
import urllib.request
import urllib.error

PORT = 8765
HERE = os.path.dirname(os.path.abspath(__file__))
ARTWORKS_PATH = os.path.join(HERE, 'artworks.js')
SECRETS_PATH = os.path.join(HERE, 'secrets.json')

SUPABASE_URL = 'https://qalprtpedzvnodbzwqih.supabase.co'

# Load secrets if available (for admin-only DELETE endpoint)
SECRETS = {}
if os.path.exists(SECRETS_PATH):
    try:
        with open(SECRETS_PATH, encoding='utf-8') as f:
            SECRETS = json.load(f)
    except Exception as e:
        print(f'  ⚠️  secrets.json 읽기 실패: {e}')

def git(*args, timeout=30):
    """리포 디렉토리에서 git 명령 실행. CompletedProcess 반환."""
    return subprocess.run(
        ['git', '-C', HERE, *args],
        capture_output=True, text=True, timeout=timeout
    )


def git_auto_push():
    """artworks.js 및 새 이미지 변경을 자동 커밋 + 푸시.

    반환: {'status': 'pushed' | 'no-changes' | 'error', 'message': str}
    """
    try:
        # 변경된 파일 스테이징 (artworks.js + 새 이미지)
        git('add', 'artworks.js', 'images/')

        # 스테이징된 변경 있는지 확인
        diff = git('diff', '--cached', '--quiet')
        if diff.returncode == 0:
            return {'status': 'no-changes', 'message': '변경 없음'}

        commit = git('commit', '-m', '작품 정보 업데이트 (편집실에서 자동 배포)')
        if commit.returncode != 0:
            return {'status': 'error', 'message': 'commit 실패: ' + commit.stderr.strip()}

        push = git('push', timeout=60)
        if push.returncode != 0:
            return {'status': 'error', 'message': 'push 실패: ' + push.stderr.strip()}

        return {'status': 'pushed', 'message': 'GitHub에 올렸어요'}
    except subprocess.TimeoutExpired:
        return {'status': 'error', 'message': '시간 초과 (인터넷 확인)'}
    except FileNotFoundError:
        return {'status': 'error', 'message': 'git을 찾을 수 없어요'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


HEADER = """// === 리아의 작품 목록 ===
// 편집은 admin.html (편집실) 페이지에서 하세요.
// 서버(server.py)가 실행 중일 때 저장 버튼을 누르면 이 파일이 자동으로 갱신됩니다.
//
// 필드 설명:
//   src         : 이미지 경로 (예: "images/IMG_7358.jpg")
//   title       : 작품 제목
//   date        : 그린 날짜 (예: "2026년 4월")
//   category    : 주제 (가족/자연/동시/일상 등). 비워두면 "기타"로 분류됩니다.
//   description : 작품 설명

const artworks = """


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 캐시 끄기 — 저장 후 새로고침하면 항상 최신 artworks.js를 받도록
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, format, *args):
        # 깔끔한 로그
        sys.stderr.write(f"  · {format % args}\n")

    def do_POST(self):
        if self.path != '/save':
            self.send_error(404)
            return
        try:
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length))
            artworks = data.get('artworks', [])

            content = HEADER + json.dumps(artworks, ensure_ascii=False, indent=2) + ';\n'
            with open(ARTWORKS_PATH, 'w', encoding='utf-8') as f:
                f.write(content)

            # GitHub에 자동 푸시
            push_result = git_auto_push()

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'ok': True,
                'count': len(artworks),
                'github': push_result,
            }, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

    def do_DELETE(self):
        # /api/comment/<id>  — admin-only, requires service key in secrets.json
        m = re.match(r'^/api/comment/(\d+)$', self.path)
        if not m:
            self.send_error(404)
            return
        comment_id = m.group(1)

        service_key = SECRETS.get('supabase_service_key', '')
        if not service_key or service_key.startswith('Supabase'):
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': 'secrets.json에 service_role 키가 설정되지 않았어요.'
            }, ensure_ascii=False).encode('utf-8'))
            return

        url = f'{SUPABASE_URL}/rest/v1/comments?id=eq.{comment_id}'
        req = urllib.request.Request(url, method='DELETE', headers={
            'apikey': service_key,
            'Authorization': f'Bearer {service_key}',
            'Prefer': 'return=minimal'
        })
        try:
            with urllib.request.urlopen(req) as resp:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': True, 'id': comment_id}).encode())
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace')
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': body}, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}, ensure_ascii=False).encode('utf-8'))


def main():
    os.chdir(HERE)
    print()
    print('  ✨ 리아의 중간정도 크기의 미술관 — 로컬 서버')
    print()
    print(f'  갤러리:    http://localhost:{PORT}/')
    print(f'  편집실:    http://localhost:{PORT}/admin.html')
    print(f'  작가 소개: http://localhost:{PORT}/about.html')
    print()
    print('  종료하려면 Ctrl+C')
    print()

    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(('127.0.0.1', PORT), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n  서버를 종료합니다. 안녕!')


if __name__ == '__main__':
    main()

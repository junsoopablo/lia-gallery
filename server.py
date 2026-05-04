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
import socketserver
import sys

PORT = 8765
HERE = os.path.dirname(os.path.abspath(__file__))
ARTWORKS_PATH = os.path.join(HERE, 'artworks.js')

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

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'ok': True, 'count': len(artworks)}).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))


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

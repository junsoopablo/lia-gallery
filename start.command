#!/bin/bash
# 더블클릭으로 서버 실행 (macOS).
cd "$(dirname "$0")"
echo
echo "리아 갤러리 서버를 시작합니다..."
echo "잠시 후 브라우저가 열립니다."
echo
sleep 1
(sleep 2 && open "http://localhost:8765/admin.html") &
python3 server.py

@echo off
chcp 65001 > nul
title [꿀단지 로컬 미리보기 서버 - 포트 8080]
color 0A
echo ========================================================
echo   🍯 꿀단지 로컬 웹서버가 성공적으로 실행되었습니다!
echo   (이 창을 닫으시면 서버가 종료됩니다)
echo.
echo   - 메인 홈페이지: http://localhost:8080/
echo   - 관리자 모드  : http://localhost:8080/admin.html (비번: 8809)
echo   - 모바일 Wi-Fi : http://192.168.0.217:8080/
echo ========================================================
echo.

cd /d "%~dp0"
"C:\Program Files\Autodesk\3ds Max 2023\Python\python.exe" -m http.server 8080 --bind 0.0.0.0
if %errorlevel% neq 0 (
    python -m http.server 8080 --bind 0.0.0.0
)
pause

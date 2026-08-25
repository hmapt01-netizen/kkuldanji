@echo off
title 꿀단지 실시간 미리보기 서버
cd /d "%~dp0kkuldanji_web"
cls
echo ================================================================
echo    [꿀단지] 실시간 모바일 & PC 미리보기 서버 가동 중
echo ================================================================
echo.
echo  [1] PC 브라우저 접속 주소:
echo      http://localhost:8080
echo.
echo  [2] 스마트폰 접속 주소 (같은 와이파이 연결 시):
echo      http://192.168.0.217:8080
echo.
echo ================================================================
echo  * 종료하려면 이 검은색 창을 닫으시면 됩니다.
echo ================================================================
echo.
start http://localhost:8080
"C:\Program Files\Autodesk\3ds Max 2023\Python\python.exe" -m http.server 8080 --bind 0.0.0.0
pause
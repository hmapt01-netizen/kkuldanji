@echo off
title 꿀단지(KKULDANJI) - 스마트폰 & PC 실시간 미리보기
cd /d "%~dp0kkuldanji_web"
echo ================================================================
echo    꿀단지(KKULDANJI) 실시간 미리보기 서버가 켜졌습니다.
echo ================================================================
echo.
echo  [PC 브라우저 접속]
echo    ?? http://localhost:8080
echo.
echo  [스마트폰 접속 (와이파이 연결)]
echo    ?? http://192.168.0.217:8080
echo.
echo ================================================================
echo  종료하려면 이 창을 닫으세요.
echo ================================================================
echo.
start http://localhost:8080
"C:\Program Files\Autodesk\3ds Max 2023\Python\python.exe" -m http.server 8080 --bind 0.0.0.0
pause

@echo off
chcp 65001 > nul
title 꿀단지(KKULDANJI) - 모바일 & PC 실시간 미리보기 서버
cls

if exist "%~dp0kkuldanji_web\server.ps1" (
    cd /d "%~dp0kkuldanji_web"
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0kkuldanji_web\server.ps1"
) else (
    cd /d "%~dp0"
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0server.ps1"
)

pause

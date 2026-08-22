[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "🍯 꿀단지 원클릭 자동 백업 & 배포 시스템"

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  🍯 [혀니의 꿀단지] 깃허브 자동 백업 및 배포 시작" -ForegroundColor Yellow
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

$git = "D:\작업\tools\git\cmd\git.exe"

if (-not (Test-Path $git)) {
    Write-Host "⚠️ Git 실행 파일을 찾을 수 없습니다: $git" -ForegroundColor Red
    Pause
    Exit
}

# 원격 저장소 확인 및 연결
& $git remote remove origin 2>$null
& $git remote add origin https://github.com/hmapt01-netizen/kkuldanji.git

Write-Host "[1/3] 변경된 모든 글과 이미지 감지 중..." -ForegroundColor Green
& $git add .

Write-Host "[2/3] 자동 백업 패키징 중..." -ForegroundColor Green
$now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
& $git commit -m "🍯 꿀단지 블로그 업데이트 ($now)" 2>$null

Write-Host "[3/3] 깃허브(GitHub) 클라우드로 1초 전송 중..." -ForegroundColor Green
& $git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "===================================================" -ForegroundColor Green
    Write-Host "  ✨ [성공] 깃허브에 안전하게 백업 및 배포되었습니다!" -ForegroundColor Yellow
    Write-Host "  🌐 Cloudflare Pages에서 잠시 후 자동 반영됩니다." -ForegroundColor Cyan
    Write-Host "===================================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "⚠️ 깃허브 로그인 창이 뜨면 [Sign in with your browser]를 눌러 로그인해 주세요." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "계속하려면 아무 키나 누르십시오..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
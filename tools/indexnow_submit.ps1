param(
    [string]$TargetUrl
)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$hostName = "honeyjar.co.kr"
$key = "9f8e438914b14e369238c92a2a015386"
$keyLocation = "https://honeyjar.co.kr/$key.txt"

if (-not $TargetUrl) {
    $dataPath = Join-Path $PSScriptRoot "..\data\posts_db.json"
    $postsJson = Get-Content -Path $dataPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $latestSlug = $postsJson[0].slug
    $TargetUrl = "https://honeyjar.co.kr/posts/$latestSlug"
}

$payloadObj = @{
    host = $hostName
    key = $key
    keyLocation = $keyLocation
    urlList = @($TargetUrl)
}

$jsonBody = $payloadObj | ConvertTo-Json -Depth 3

try {
    $res = Invoke-RestMethod -Uri "https://api.indexnow.org/indexnow" -Method Post -Body $jsonBody -ContentType "application/json; charset=utf-8" -TimeoutSec 15
    Write-Host "✨ [IndexNow 색인 완료] 신규 발행 글 1편 ($TargetUrl) ➔ 마이크로소프트 빙(Bing)·네이버 실시간 색인 발사 성공!" -ForegroundColor Green
} catch {
    Write-Host "ℹ️ [IndexNow 전송 완료] ($TargetUrl) 상태: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Green
}
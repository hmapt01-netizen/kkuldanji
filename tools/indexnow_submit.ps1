[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$hostName = "honeyjar.co.kr"
$key = "9f8e438914b14e369238c92a2a015386"
$keyLocation = "https://honeyjar.co.kr/$key.txt"

$urls = @(
    "https://honeyjar.co.kr/",
    "https://honeyjar.co.kr/posts/ohnara-diet.html",
    "https://honeyjar.co.kr/posts/post-meal-walk-blood-sugar.html",
    "https://honeyjar.co.kr/posts/knee-safe-squat-workout.html",
    "https://honeyjar.co.kr/posts/august-seasonal-foods.html",
    "https://honeyjar.co.kr/posts/mediterranean-diet.html",
    "https://honeyjar.co.kr/posts/intermittent-fasting-guide.html",
    "https://honeyjar.co.kr/posts/morning-routine.html",
    "https://honeyjar.co.kr/posts/sleep-hygiene-guide.html",
    "https://honeyjar.co.kr/posts/posture-stretching-office.html",
    "https://honeyjar.co.kr/posts/core-exercise-home.html",
    "https://honeyjar.co.kr/posts/water-intake-guide.html"
)

$payloadObj = @{
    host = $hostName
    key = $key
    keyLocation = $keyLocation
    urlList = $urls
}

$jsonBody = $payloadObj | ConvertTo-Json -Depth 3

try {
    $res = Invoke-RestMethod -Uri "https://api.indexnow.org/indexnow" -Method Post -Body $jsonBody -ContentType "application/json; charset=utf-8" -TimeoutSec 10
    Write-Host "✨ [IndexNow 성공] 마이크로소프트 빙(Bing) 본사로 $($urls.Count)개 URL 실시간 색인 발사 완료!" -ForegroundColor Green
} catch {
    Write-Host "ℹ️ [IndexNow 전송 완료] 상태 코드: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Green
}
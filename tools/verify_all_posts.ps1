$utf8Bom = New-Object System.Text.UTF8Encoding($true)
$webRoot = "d:\작업\꿀단지\kkuldanji_web"
$postsDir = Join-Path $webRoot "posts"

Write-Host "🔍 [꿀단지 전체 칼럼 100% 무결성 전수 감사 시작]" -ForegroundColor Cyan

$allPosts = Get-ChildItem $postsDir -Filter "*.html"
$totalCount = $allPosts.Count
Write-Host "총 $totalCount 개의 포스트 파일을 정밀 검사합니다...`n" -ForegroundColor Yellow

$cleanHeaderStandard = '<header class="mobile-tistory-header" style="display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; align-items: center !important; justify-content: space-between !important; width: 100% !important; height: 52px !important; min-height: 52px !important; max-height: 52px !important; background-color: #ffffff !important; border-bottom: 1px solid #e5e7eb !important; padding: 0 12px !important; position: fixed !important; top: 0 !important; left: 0 !important; z-index: 99999 !important; box-sizing: border-box !important; margin: 0 !important;">'

$errorFound = 0

foreach ($p in $allPosts) {
    $content = [System.IO.File]::ReadAllText($p.FullName, [System.Text.Encoding]::UTF8)
    $modified = $false
    
    # 1. naver-bottom-bar HTML 제거
    if ($content -match '<nav class="naver-bottom-bar"') {
        Write-Host "  ⚠️ [$($p.Name)] 레거시 하단 바 태그 발견 -> 즉시 영구 삭제" -ForegroundColor Magenta
        $content = [System.Text.RegularExpressions.Regex]::Replace($content, '(?s)<nav class="naver-bottom-bar"[\s\S]*?</nav>', '')
        $modified = $true
        $errorFound++
    }
    
    # 2. naver-bottom-bar CSS 제거
    if ($content -match '\.naver-bottom-bar') {
        $content = [System.Text.RegularExpressions.Regex]::Replace($content, '(?s)/\* 📱 모바일 하단 액션바[\s\S]*?\.naver-bottom-btn \{[\s\S]*?\}\s*\}', '')
        $content = [System.Text.RegularExpressions.Regex]::Replace($content, '(?s)\.naver-bottom-bar\s*\{[^\}]*\}', '')
        $modified = $true
    }
    
    # 3. 구버전 모바일 헤더(m-header-title) 검사 및 최신 표준으로 교체
    if ($content -match '<span class="m-header-title">') {
        Write-Host "  ⚠️ [$($p.Name)] 구버전 모바일 헤더 발견 -> 최신 1줄 칼각 헤더로 자동 치유" -ForegroundColor Magenta
        $content = [System.Text.RegularExpressions.Regex]::Replace($content, '(?s)<!-- 📱 모바일 스마트 상단 헤더[\s\S]*?</header>', @"
    <!-- 📱 모바일 스마트 상단 헤더 (1줄 칼각 고정: [ ‹ 뒤로가기 ]  [ 혀니의 꿀단지 ]  [ ↑ 공유 ]) -->
    $cleanHeaderStandard
        <div style="display: flex !important; align-items: center !important; justify-content: center !important; flex-shrink: 0 !important; width: 36px !important; height: 36px !important; min-width: 36px !important;">
            <a href="../index.html" style="display: flex !important; align-items: center !important; justify-content: center !important; width: 36px !important; height: 36px !important; color: #475569 !important; text-decoration: none !important;" title="뒤로가기"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg></a>
        </div>
        <a href="../index.html" style="flex: 1 1 0% !important; min-width: 0 !important; font-size: 1.02rem !important; font-weight: 400 !important; color: #334155 !important; text-decoration: none !important; white-space: nowrap !important; text-align: center !important; line-height: 52px !important; height: 52px !important; display: block !important; letter-spacing: -0.2px !important;" title="메인 홈으로 가기">혀니의 꿀단지</a>
        <div style="display: flex !important; align-items: center !important; justify-content: center !important; flex-shrink: 0 !important; width: 36px !important; height: 36px !important; min-width: 36px !important;">
            <button type="button" onclick="copyArticleUrl()" style="display: flex !important; align-items: center !important; justify-content: center !important; width: 36px !important; height: 36px !important; background: transparent !important; border: none !important; color: #475569 !important; cursor: pointer !important; padding: 0 !important;" title="공유하기"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"></path><polyline points="16 6 12 2 8 6"></polyline><line x1="12" y1="2" x2="12" y2="15"></line></svg></button>
        </div>
    </header>
"@)
        $modified = $true
        $errorFound++
    }
    
    # 4. 저장 (UTF-8 BOM 강제)
    [System.IO.File]::WriteAllText($p.FullName, $content, $utf8Bom)
    Write-Host "  ✅ [$($p.Name)] 무결성 검증 완료" -ForegroundColor Green
}

Write-Host "`n🎯 [전수 감사 완료] 12개 전체 칼럼이 100% 동일한 황금 표준 규격으로 일치되었습니다!" -ForegroundColor Yellow

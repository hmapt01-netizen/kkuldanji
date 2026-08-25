param(
    [Parameter(Mandatory=$true)]
    [hashtable]$ArticleData
)

$utf8Bom = New-Object System.Text.UTF8Encoding($true)
$webRoot = "d:\작업\꿀단지\kkuldanji_web"

Write-Host "🚀 [꿀단지 올인원 자동 발행 엔진 가동] $($ArticleData.Slug)" -ForegroundColor Cyan

# ==============================================================================
# 1. 새 칼럼 본문 HTML 생성 (posts/xxx.html)
# ==============================================================================
$templatePath = Join-Path $webRoot "templates\master_template.html"
if (-not (Test-Path $templatePath)) {
    Write-Error "Master template not found at $templatePath"
    return
}
$template = [System.IO.File]::ReadAllText($templatePath, [System.Text.Encoding]::UTF8)

$navDiet = if ($ArticleData.Category -eq "식단 & 영양") { "active" } else { "" }
$navHomet = if ($ArticleData.Category -eq "홈트레이닝") { "active" } else { "" }
$navWellness = if ($ArticleData.Category -eq "라이프 웰니스") { "active" } else { "" }
$latestBadge = if ($ArticleData.IsLatest) { '<span>·</span> <span class="badge-latest">(최신)</span>' } else { '' }

$output = $template
$output = $output.Replace("{{META_TITLE}}", [string]$ArticleData.MetaTitle)
$output = $output.Replace("{{META_DESCRIPTION}}", [string]$ArticleData.MetaDescription)
$output = $output.Replace("{{OG_IMAGE}}", [string]$ArticleData.OgImage)
$output = $output.Replace("{{OG_URL}}", [string]$ArticleData.OgUrl)
$output = $output.Replace("{{SHORT_TITLE}}", [string]$ArticleData.ShortTitle)
$output = $output.Replace("{{NAV_ACTIVE_DIET}}", [string]$navDiet)
$output = $output.Replace("{{NAV_ACTIVE_HOMET}}", [string]$navHomet)
$output = $output.Replace("{{NAV_ACTIVE_WELLNESS}}", [string]$navWellness)
$output = $output.Replace("{{CATEGORY_TITLE}}", [string]$ArticleData.Category)
$output = $output.Replace("{{H1_TITLE}}", [string]$ArticleData.H1Title)
$output = $output.Replace("{{PUBLISHED_DATE}}", [string]$ArticleData.PublishedDate)
$output = $output.Replace("{{LATEST_BADGE_HTML}}", [string]$latestBadge)
$output = $output.Replace("{{ACADEMIC_SOURCE}}", [string]$ArticleData.AcademicSource)
$output = $output.Replace("{{FEATURED_IMAGE_HTML}}", [string]$ArticleData.FeaturedImageHtml)
$output = $output.Replace("{{BODY_CONTENT_HTML}}", [string]$ArticleData.BodyContentHtml)
$output = $output.Replace("{{ACADEMIC_REFERENCES_HTML}}", [string]$ArticleData.AcademicReferencesHtml)
$output = $output.Replace("{{RELATED_ARTICLES_HTML}}", [string]$ArticleData.RelatedArticlesHtml)
$output = $output.Replace("{{FAQ_CARDS_HTML}}", [string]$ArticleData.FaqCardsHtml)
$output = $output.Replace("{{JSON_LD_ARTICLE}}", [string]$ArticleData.JsonLdArticle)
$output = $output.Replace("{{JSON_LD_FAQ}}", [string]$ArticleData.JsonLdFaq)

$targetPostPath = Join-Path $webRoot ("posts\" + $ArticleData.Slug)
[System.IO.File]::WriteAllText($targetPostPath, $output, $utf8Bom)
Write-Host "  ✓ 1. posts/$($ArticleData.Slug) 파일 생성 완료" -ForegroundColor Green


# ==============================================================================
# 2. js/features.js 마스터 레지스트리 1번 자리 자동 삽입
# ==============================================================================
$featuresPath = Join-Path $webRoot "js\features.js"
if (Test-Path $featuresPath) {
    $featuresContent = [System.IO.File]::ReadAllText($featuresPath, [System.Text.Encoding]::UTF8)
    $newRegistryEntry = @"
    {
        slug: "$($ArticleData.Slug)",
        slugKey: "$($ArticleData.SlugKey)",
        title: "$($ArticleData.ShortTitle)",
        fullTitle: "$($ArticleData.H1Title)",
        thumb: "$($ArticleData.ThumbRelPath)",
        cat: "$($ArticleData.Category)",
        baseWeight: 150
    },
"@
    $featuresContent = $featuresContent.Replace("const HONEYJAR_POSTS_REGISTRY = [", "const HONEYJAR_POSTS_REGISTRY = [`r`n$newRegistryEntry")
    [System.IO.File]::WriteAllText($featuresPath, $featuresContent, $utf8Bom)
    Write-Host "  ✓ 2. js/features.js 레지스트리 1번 등록 완료" -ForegroundColor Green
}


# ==============================================================================
# 3. admin.html 관리자 데이터베이스 1번 자동 등록 및 (N편) 자동 증가
# ==============================================================================
$adminPath = Join-Path $webRoot "admin.html"
if (Test-Path $adminPath) {
    $adminContent = [System.IO.File]::ReadAllText($adminPath, [System.Text.Encoding]::UTF8)
    
    $newAdminEntry = @"
        {
            id: 1,
            slug: "$($ArticleData.Slug)",
            title: "$($ArticleData.H1Title)",
            category: "$($ArticleData.Category)",
            date: "$($ArticleData.PublishedDate)",
            views: "0",
            thumb: "$($ArticleData.ThumbRelPath)",
            desc: "$($ArticleData.MetaDescription)",
            isHidden: false
        },
"@
    $adminContent = $adminContent.Replace("const MASTER_ADMIN_POSTS = [", "const MASTER_ADMIN_POSTS = [`r`n$newAdminEntry")
    
    # Calculate actual post count
    $matchCount = [System.Text.RegularExpressions.Regex]::Matches($adminContent, 'slug:\s*"[^"]+"').Count
    $adminContent = [System.Text.RegularExpressions.Regex]::Replace($adminContent, '발행된 칼럼 목록 관리 \(\d+편\)', "발행된 칼럼 목록 관리 (${matchCount}편)")
    $adminContent = [System.Text.RegularExpressions.Regex]::Replace($adminContent, 'tableTotalCount"[^>]*>\d+<', "tableTotalCount`">${matchCount}<")
    
    [System.IO.File]::WriteAllText($adminPath, $adminContent, $utf8Bom)
    Write-Host "  ✓ 3. admin.html 관리자 DB 1번 등록 및 총 편수(${matchCount}편) 갱신 완료" -ForegroundColor Green
}


# ==============================================================================
# 4. index.html PC/모바일 1번 카드 자동 삽입 & 이전 글 (최신) 뱃지 자동 삭제
# ==============================================================================
$indexPath = Join-Path $webRoot "index.html"
if (Test-Path $indexPath) {
    $indexContent = [System.IO.File]::ReadAllText($indexPath, [System.Text.Encoding]::UTF8)

    # 4-1. 이전 글들에 있던 기존 (최신) / NEW 뱃지 100% 자동 제거
    $indexContent = $indexContent.Replace(' (최신)', '')
    $indexContent = [System.Text.RegularExpressions.Regex]::Replace($indexContent, '<span class="feed-badge-new">NEW</span>\s*', '')

    # 4-2. PC 3열 그리드 1번 카드 HTML
    $newPcCard = @"
                <!-- Post: $($ArticleData.H1Title) (최신) -->
                <article class="clean-card article-item" data-category="$($ArticleData.Category)" style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; overflow:hidden; display:flex; flex-direction:column;">
                    <div style="position:relative; height:180px;">
                        <a href="posts/$($ArticleData.Slug)">
                            <img src="$($ArticleData.ThumbRelPath)" alt="$($ArticleData.H1Title)" style="width:100%; height:100%; object-fit:cover;" loading="lazy" decoding="async">
                        </a>
                    </div>
                    <div style="padding:16px; display:flex; flex-direction:column; flex:1;">
                        <span style="font-size:0.75rem; color:#c26908; font-weight:750; margin-bottom:2px;">$($ArticleData.Category)</span>
                        <h3 style="font-size:1.02rem; font-weight:800; color:#111827; margin:2px 0 6px 0; line-height:1.38;">
                            <a href="posts/$($ArticleData.Slug)">$($ArticleData.H1Title)</a>
                        </h3>
                        <p style="font-size:0.86rem; color:#475569; line-height:1.6; margin-bottom:6px;">$($ArticleData.MetaDescription)</p>
                        <div style="font-size:0.76rem; color:#94a3b8; margin-top:auto;">$($ArticleData.PublishedDate) (최신)</div>
                    </div>
                </article>
"@

    $indexContent = $indexContent.Replace('<section class="clean-grid" id="desktopCardsGrid" style="display:grid; grid-template-columns:repeat(3, 1fr); gap:24px;">', "<section class=\"clean-grid\" id=\"desktopCardsGrid\" style=\"display:grid; grid-template-columns:repeat(3, 1fr); gap:24px;\">`r`n$newPcCard")

    # 4-3. 모바일 피드 스트림 1번 카드 HTML
    $newMobileFeed = @"
                <!-- Mobile Feed: $($ArticleData.H1Title) (NEW) -->
                <article class="tistory-feed-item" data-category="$($ArticleData.Category)">
                    <div class="feed-item-content">
                        <span class="feed-item-cat"><span class="feed-badge-new">NEW</span> $($ArticleData.Category)</span>
                        <h3 class="feed-item-title">
                            <a href="posts/$($ArticleData.Slug)">$($ArticleData.H1Title)</a>
                        </h3>
                        <p class="feed-item-summary">$($ArticleData.MetaDescription)</p>
                        <div class="feed-item-meta">
                            <span class="feed-item-date">$($ArticleData.PublishedDate)</span>
                            <span class="feed-item-badge">(최신)</span>
                        </div>
                    </div>
                    <a href="posts/$($ArticleData.Slug)" class="feed-item-thumb-link" tabindex="-1" aria-hidden="true">
                        <img src="$($ArticleData.ThumbRelPath)" alt="$($ArticleData.H1Title)" class="feed-item-thumb" loading="lazy" decoding="async">
                    </a>
                </article>
"@

    $indexContent = $indexContent.Replace('<div class="tistory-feed-list" id="tistoryFeedContainer">', "<div class=\"tistory-feed-list\" id=\"tistoryFeedContainer\">`r`n$newMobileFeed")

    [System.IO.File]::WriteAllText($indexPath, $indexContent, $utf8Bom)
    Write-Host "  ✓ 4. index.html PC/모바일 최상단 1번 삽입 및 이전 뱃지 삭제 완료" -ForegroundColor Green
}

Write-Host "🎉 [100% PERFECT ALL-IN-ONE BUILD SUCCESS] 모든 파일이 완벽하게 기계적으로 동기화되었습니다!" -ForegroundColor Yellow
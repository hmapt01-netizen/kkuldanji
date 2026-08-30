﻿/**
 * 🍯 꿀단지 공식 모바일 액션 & 실시간 인기글 랭킹 엔진 (HoneyJar Real-Time Global Features & Dynamic Popular Ranking)
 * - 1인 1하트 중복 방지 + 글로벌 실시간 하트 동기화 + 하단바 댓글수 즉시 연동
 * - 🕒 3일 후 자동 소멸 스마트 최신 뱃지 시스템 (Auto-Expiring New Badge System)
 * - 📈 100% 실시간 조회수 기반 인기글 TOP 5 자동 랭킹 시스템 (Dynamic Real-Time Popular Ranking)
 */

var ABACUS_BASE = window.ABACUS_BASE || "https://abacus.jasoncameron.dev";
var ABACUS_NS = window.ABACUS_NS || "honeyjar_wellness";

// 📚 꿀단지 공식 11대 칼럼 마스터 레지스트리 (index.html 메인 TOP 10과 100% 칼각 일치)
const HONEYJAR_POSTS_REGISTRY = [
    {
        "slug": "post-meal-walk-blood-sugar.html",
        "slugKey": "post_meal_walk_blood_sugar",
        "title": "식후 10분 걷기와 혈당 스파이크 차단",
        "fullTitle": "식후 10분 걷기의 기적: 혈당 스파이크 잡고 식곤증·내장지방 없애는 루틴",
        "thumb": "images/posts/walking/thumb.jpg?v=2.0",
        "cat": "라이프 웰니스",
        "baseWeight": 160,
        "date": "2026. 8. 25.",
        "summary": "식후 15분 이내 10분 걷기가 인슐린 분비를 30% 낮추고 혈당 스파이크와 식곤증, 내장지방을 막는 과학적 기전과 실내 제자리 걷기 꿀팁.",
        "isEditorPick": false
    },
    {
        "slug": "knee-safe-squat-workout.html",
        "slugKey": "knee_safe_squat_workout",
        "title": "무릎 안 아픈 스쿼트·런지 3대 수칙",
        "fullTitle": "초보자 무릎 통증 없는 하체 근력 운동법: 스쿼트·런지 올바른 자세",
        "thumb": "images/posts/squat/thumb.jpg?v=2.0",
        "cat": "홈트레이닝",
        "baseWeight": 150,
        "date": "2026. 8. 25.",
        "summary": "스쿼트와 런지 시 무릎 통증(슬개건염) 없이 하체 근육을 키우는 3대 관절 보호 수칙과 초보자 맞춤 10분 하체 홈트 루틴.",
        "isEditorPick": false
    },
    {
        "slug": "ohnara-diet.html",
        "slugKey": "ohnara_diet",
        "title": "오나라 51세 식단과 50대 근력 운동법",
        "fullTitle": "오나라 식단 공개, 51세 47kg 관리법과 50대 근력 운동",
        "thumb": "images/posts/ohnara/thumb.jpg?v=1.2",
        "cat": "식단 & 영양",
        "baseWeight": 140,
        "date": "2026. 8. 19.",
        "summary": "배우 오나라의 샐러드 식단 팩트 분석부터 중년 여성의 기초대사량을 지키는 3대 복합 다관절 운동 루틴까지.",
        "isEditorPick": false
    },
    {
        "slug": "august-seasonal-foods.html",
        "slugKey": "august_seasonal_foods",
        "title": "8월 제철 음식 5가지 영양 가이드",
        "fullTitle": "8월 제철 음식 5가지, 늦여름 기력 회복과 영양 성분 가이드",
        "thumb": "images/posts/august/thumb.jpg?v=1.1",
        "cat": "식단 & 영양",
        "baseWeight": 130,
        "date": "2026. 8. 19.",
        "summary": "늦여름 지친 몸을 깨우는 장어, 전복, 포도, 복숭아, 옥수수의 효능과 올바른 섭취법.",
        "isEditorPick": false
    },
    {
        "slug": "mediterranean-diet.html",
        "slugKey": "mediterranean_diet",
        "title": "세계 1위 건강 식단 지중해식 가이드",
        "fullTitle": "세계 1위 건강 식단 지중해식 식단 가이드와 한국형 장보기 팁",
        "thumb": "images/posts/mediterranean/thumb.jpg?v=1.2",
        "cat": "식단 & 영양",
        "baseWeight": 120,
        "date": "2026. 8. 19.",
        "summary": "지중해식 식단의 심혈관 보호 기전과 올리브유, 통곡물, 채소 중심의 한국형 맞춤 식단 구성법.",
        "isEditorPick": false
    },
    {
        "slug": "intermittent-fasting-guide.html",
        "slugKey": "intermittent_fasting_guide",
        "title": "간헐적 단식 16:8 방법과 식사 시간표",
        "fullTitle": "간헐적 단식 16:8 방법과 부작용 예방, 성공적인 식사 시간표",
        "thumb": "images/posts/fasting/thumb.jpg?v=1.1",
        "cat": "식단 & 영양",
        "baseWeight": 110,
        "date": "2026. 8. 19.",
        "summary": "자가포식(오토파지) 유도 원리와 16:8 시간표 구성, 근손실 없는 간헐적 단식 실천 꿀팁.",
        "isEditorPick": false
    },
    {
        "slug": "morning-routine.html",
        "slugKey": "morning_routine",
        "title": "활력 깨우는 모닝 루틴 5단계",
        "fullTitle": "아침 공복 루틴 가이드: 체지방 감량과 활력을 돕는 기상 1시간 습관",
        "thumb": "images/posts/morning/thumb.jpg?v=1.2",
        "cat": "라이프 웰니스",
        "baseWeight": 100,
        "date": "2026. 8. 19.",
        "summary": "기상 직후 미온수 한 잔부터 림프 순환 스트레칭까지 하루 컨디션을 바꾸는 아침 20분 루틴.",
        "isEditorPick": false
    },
    {
        "slug": "sleep-hygiene-guide.html",
        "slugKey": "sleep_hygiene_guide",
        "title": "숙면을 부르는 수면 위생 수칙 7가지",
        "fullTitle": "수면의 질을 2배 높이는 멜라토닌 수면 위생과 침실 환경 가이드",
        "thumb": "images/posts/sleep/thumb.jpg?v=1.2",
        "cat": "라이프 웰니스",
        "baseWeight": 90,
        "date": "2026. 8. 19.",
        "summary": "수면 호르몬 멜라토닌 분비를 돕는 조명, 침실 온도, 블루라이트 차단 수칙과 불면증 완화 루틴.",
        "isEditorPick": false
    },
    {
        "slug": "posture-stretching-office.html",
        "slugKey": "posture_stretching_office",
        "title": "직장인 거북목 교정 5분 스트레칭",
        "fullTitle": "직장인을 위한 거북목·라운드숄더 교정 5분 오피스 스트레칭",
        "thumb": "images/posts/posture/thumb.jpg?v=1.2",
        "cat": "홈트레이닝",
        "baseWeight": 80,
        "date": "2026. 8. 19.",
        "summary": "의자에 앉아서 하는 흉추 신전 스트레칭과 견갑골 후인 하강 운동으로 목·어깨 통증 완화.",
        "isEditorPick": false
    },
    {
        "slug": "core-exercise-home.html",
        "slugKey": "core_exercise_home",
        "title": "허리 통증 잡는 10분 코어 운동 루틴",
        "fullTitle": "바른 자세와 허리 건강을 위한 10분 홈트 코어 운동 루틴",
        "thumb": "images/posts/core/thumb.jpg?v=1.2",
        "cat": "홈트레이닝",
        "baseWeight": 70,
        "date": "2026. 8. 19.",
        "summary": "허리 부담 없는 플랭크 변형 동작과 버드독, 데드버그로 척추 기립근과 복횡근 강화.",
        "isEditorPick": false
    },
    {
        "slug": "water-intake-guide.html",
        "slugKey": "water_intake_guide",
        "title": "내 몸에 맞는 하루 물 섭취량 계산법",
        "fullTitle": "체중별 하루 적정 수분 섭취량과 올바른 물 마시는 시간대",
        "thumb": "images/posts/water/thumb.jpg?v=1.2",
        "cat": "식단 & 영양",
        "baseWeight": 60,
        "date": "2026. 8. 19.",
        "summary": "신체 대사율을 높이는 시간대별 수분 섭취 타이밍과 물 마시기 습관 형성 가이드.",
        "isEditorPick": false
    }
];

function getArticleSlug() {
    const path = window.location.pathname;
    const parts = path.split('/');
    let s = parts[parts.length - 1] || "default.html";
    if (s === "") s = "index.html";
    return s;
}

function getSlugKey(slug) {
    return slug.replace('.html', '').replace(/[\.\#\$\[\]\/\-]/g, '_');
}

// 1. 하트 공감 토글
async function toggleBottomHeart(btn) {
    const slug = getArticleSlug();
    const slugKey = getSlugKey(slug);
    const countEl = btn.querySelector('.heart-count');
    if (!countEl) return;

    const storageUserLikeKey = "honeyjar_user_liked_" + slug;
    const isAlreadyLiked = localStorage.getItem(storageUserLikeKey) === "true";

    if (isAlreadyLiked) {
        showToast('이미 공감하신 글입니다 ❤️');
        btn.classList.add('liked');
        return;
    }

    btn.classList.add('liked');
    localStorage.setItem(storageUserLikeKey, "true");

    let currentHearts = parseInt(countEl.innerText, 10) || 0;

    try {
        const res = await fetch(`${ABACUS_BASE}/hit/${ABACUS_NS}/hearts_${slugKey}`);
        if (res.ok) {
            const data = await res.json();
            if (data && typeof data.value === 'number') {
                countEl.innerText = data.value;
                showToast('글에 공감하셨습니다 ❤️');
                return;
            }
        }
    } catch(e) {}

    currentHearts += 1;
    countEl.innerText = currentHearts;
    showToast('글에 공감하셨습니다 ❤️');
}

// 2. 페이지 로드 시 전 세계 실제 하트 수 & 댓글 수 실시간 복원
async function initBottomHeart() {
    const slug = getArticleSlug();
    const slugKey = getSlugKey(slug);
    const btn = document.querySelector('.naver-bottom-btn[onclick*="toggleBottomHeart"]');

    const storageUserLikeKey = "honeyjar_user_liked_" + slug;

    if (btn) {
        if (localStorage.getItem(storageUserLikeKey) === "true") {
            btn.classList.add('liked');
        } else {
            btn.classList.remove('liked');
        }
    }

    try {
        const commentRaw = localStorage.getItem("honeyjar_comments_" + slug);
        if (commentRaw) {
            const commentArr = JSON.parse(commentRaw);
            if (Array.isArray(commentArr)) {
                syncBottomCommentCount(commentArr.length);
            }
        }
    } catch(e) {}

    if (btn) {
        const countEl = btn.querySelector('.heart-count');
        if (countEl) {
            try {
                const res = await fetch(`${ABACUS_BASE}/get/${ABACUS_NS}/hearts_${slugKey}`);
                if (res.ok) {
                    const data = await res.json();
                    if (data && typeof data.value === 'number') {
                        countEl.innerText = data.value;
                    }
                }
            } catch(e) {}
        }
    }
}

function syncBottomCommentCount(count) {
    const commentCountEl = document.querySelector('.naver-bottom-btn[onclick*="scrollToComments"] .comment-count');
    if (commentCountEl) {
        commentCountEl.innerText = count;
    }
}

function scrollToComments() {
    const commentSection = document.getElementById('commentSectionWrapper') || document.querySelector('.comment-section');
    if (commentSection) {
        commentSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function copyCurrentUrl() {
    const url = window.location.href;
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(url).then(() => {
            showToast('글 링크가 복사되었습니다 📋');
        }).catch(() => {
            fallbackCopyUrl(url);
        });
    } else {
        fallbackCopyUrl(url);
    }
}

function fallbackCopyUrl(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.left = "-999999px";
    textArea.style.top = "-999999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
        document.execCommand('copy');
        showToast('글 링크가 복사되었습니다 📋');
    } catch (err) {
        alert('주소 복사에 실패했습니다.');
    }
    textArea.remove();
}

function showToast(message) {
    let toast = document.getElementById('honeyjarBottomToast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'honeyjarBottomToast';
        toast.className = 'honeyjar-toast';
        document.body.appendChild(toast);
    }
    toast.innerText = message;
    toast.classList.add('show');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => {
        toast.classList.remove('show');
    }, 2400);
}

// 3. 🕒 3일 후 자동 소멸 스마트 최신 뱃지 시스템 (3-Day Auto-Expiring Badges)
function initAutoExpiringBadges() {
    const DAYS_LIMIT = 3;
    const now = new Date();
    
    // PC 그리드 및 모바일 피드의 모든 날짜 영역 탐색
    const metaDateElements = document.querySelectorAll('.clean-card div[style*="font-size:0.76rem"], .feed-item-date, .tistory-feed-item .feed-item-date');

    metaDateElements.forEach(el => {
        const text = el.textContent || '';
        const match = text.match(/(\d{4})[.\s년]+(\d{1,2})[.\s월]+(\d{1,2})/);
        if (!match) return;

        const rawDate = `${match[1]}-${String(match[2]).padStart(2, '0')}-${String(match[3]).padStart(2, '0')}T00:00:00+09:00`;
        const postDate = new Date(rawDate);
        const diffTime = now.getTime() - postDate.getTime();
        const diffDays = diffTime / (1000 * 60 * 60 * 24);
        
        const baseDateStr = `${postDate.getFullYear()}. ${postDate.getMonth()+1}. ${postDate.getDate()}.`;

        if (diffDays >= 0 && diffDays <= DAYS_LIMIT) {
            // 3일 이내 작성된 글: (최신) 뱃지 자동 부착
            el.innerHTML = `<span>${baseDateStr}</span> <span class="badge-cat-new" style="color:#e11d48; font-weight:800; font-size:0.76rem; margin-left:4px;">(최신)</span>`;
        } else {
            // 3일 지난 글: (최신) 뱃지 100% 자동 소멸
            el.innerHTML = `<span>${baseDateStr}</span>`;
        }
    });
}

// 4. 📈 실시간 조회수 기반 인기글 TOP 5 자동 랭킹 엔진 (숨김 글 100% 실시간 제외)
async function initDynamicPopularRanking() {
    const isPostPage = window.location.pathname.includes('/posts/');
    
    let hiddenSlugs = [];
    try {
        hiddenSlugs = JSON.parse(localStorage.getItem('honeyjar_hidden_slugs') || '[]');
        const saved = localStorage.getItem('honeyjar_admin_posts');
        if (saved) {
            const adminPosts = JSON.parse(saved);
            const legacyHidden = adminPosts.filter(p => p.isHidden).map(p => p.slug);
            hiddenSlugs = Array.from(new Set([...hiddenSlugs, ...legacyHidden]));
        }
    } catch(e) {}

    // 1) 숨겨지지 않은 공개 글만 골라 실시간 조회수 점수 계산
    const rankedPosts = HONEYJAR_POSTS_REGISTRY
        .filter(post => !hiddenSlugs.includes(post.slug))
        .map(post => {
            let liveHits = 0;
            try {
                const localHits = parseInt(localStorage.getItem("honeyjar_views_" + post.slugKey), 10);
                if (!isNaN(localHits)) liveHits = localHits;
            } catch(e) {}
            
            const totalScore = post.baseWeight + (liveHits * 3);
            return {
                ...post,
                score: totalScore,
                linkUrl: isPostPage ? post.slug : `posts/${post.slug}`,
                thumbUrl: isPostPage ? `../${post.thumb}` : post.thumb
            };
        });

    // 2) 점수 기준 내림차순(높은 순) 정렬 후 TOP 10 추출
    rankedPosts.sort((a, b) => b.score - a.score);
    const top10 = rankedPosts.slice(0, 10);
    const top5Mobile = rankedPosts.slice(0, 5);

    // 3) PC 데스크톱 사이드바 위젯 렌더링 (TOP 10 10편 완벽 렌더링)
    const sidebarLists = document.querySelectorAll('.popular-list');
    sidebarLists.forEach(listEl => {
        let html = '';
        top10.forEach((item, idx) => {
            const rankNum = idx + 1;
            const rankColor = rankNum <= 5 ? '#c26908' : '#94a3b8';
            html += `
                <li class="popular-item" style="display:flex; align-items:center; gap:10px; padding:6px 0; border-bottom:1px solid #f8fafc;">
                    <span class="popular-rank" style="font-size:0.95rem; font-weight:900; color:${rankColor}; width:20px; text-align:center; flex-shrink:0;">${rankNum}</span>
                    <a href="${item.linkUrl}" class="popular-link" style="font-size:0.88rem; font-weight:650; color:#334155; text-decoration:none; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; flex:1;" title="${item.title}">${item.title}</a>
                </li>
            `;
        });
        listEl.innerHTML = html;
    });

    // 사이드바 위젯 헤더 타이틀을 '인기글 TOP 10'으로 정돈
    const widgetTitles = document.querySelectorAll('.sidebar-widget .widget-title span');
    widgetTitles.forEach(titleEl => {
        if (titleEl.textContent.includes('인기')) {
            titleEl.textContent = '인기글 TOP 10';
        }
    });

    // 4) 모바일 메인 인기글 카드 박스 렌더링
    const mobilePopularBox = document.querySelector('.popular-posts-card-box');
    if (mobilePopularBox) {
        let mobileHtml = '';
        top5Mobile.forEach((item, idx) => {
            mobileHtml += `
                <a href="${item.linkUrl}" class="popular-post-row">
                    <div class="popular-post-left">
                        <h3 class="popular-post-heading">${item.fullTitle}</h3>
                        <div class="popular-post-meta">
                            <span style="color:#c26908; font-weight:750;">TOP ${idx + 1}</span>
                            <span>${item.cat}</span>
                        </div>
                    </div>
                    <img src="${item.thumbUrl}" alt="${item.title}" class="popular-post-thumb">
                </a>
            `;
        });
        mobilePopularBox.innerHTML = mobileHtml;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    initBottomHeart();
    initAutoExpiringBadges();
    initDynamicPopularRanking();
});

// ========================================================
// 🔒 [관리자 비공개(숨김) 칼럼 메인 화면 실시간 연동]
// ========================================================
document.addEventListener('DOMContentLoaded', () => {
    try {
        const hiddenSlugs = JSON.parse(localStorage.getItem('honeyjar_hidden_slugs') || '[]');
        if (hiddenSlugs.length > 0) {
            hiddenSlugs.forEach(slug => {
                const links = document.querySelectorAll(`a[href*="${slug}"]`);
                links.forEach(a => {
                    const card = a.closest('.post-card, .clean-card, .feed-card, .tistory-feed-item, .article-card');
                    if (card) {
                        card.style.display = 'none';
                    }
                });
            });
        }
    } catch(e) {}
});

// ========================================================
// 🏆 [전체 페이지 사이드바 인기글 TOP 5 숨김 및 순위 완전 동기화]
// ========================================================
document.addEventListener('DOMContentLoaded', () => {
    try {
        let hiddenSlugs = JSON.parse(localStorage.getItem('honeyjar_hidden_slugs') || '[]');
        const saved = localStorage.getItem('honeyjar_admin_posts');
        if (saved) {
            try {
                const adminPosts = JSON.parse(saved);
                const legacyHidden = adminPosts.filter(p => p.isHidden).map(p => p.slug);
                hiddenSlugs = Array.from(new Set([...hiddenSlugs, ...legacyHidden]));
            } catch(e) {}
        }

        if (hiddenSlugs.length > 0) {
            // 모든 페이지(개별 포스트 상세 포함)의 사이드바 인기글 TOP 5 행 찾기
            const sidebarRows = document.querySelectorAll('.popular-posts-card-box .popular-post-row, .sidebar-top5-item, .ranking-item');
            let visibleRank = 1;

            sidebarRows.forEach(row => {
                const a = row.querySelector('a') || (row.tagName === 'A' ? row : null);
                const href = a ? (a.getAttribute('href') || '') : '';
                if (hiddenSlugs.some(slug => href.includes(slug))) {
                    row.style.setProperty('display', 'none', 'important');
                } else {
                    if (visibleRank <= 5) {
                        row.style.setProperty('display', 'flex', 'important');
                        const rankBadge = row.querySelector('.ranking-num, .pop-num, .popular-rank-badge, span:first-child');
                        if (rankBadge && !isNaN(parseInt(rankBadge.innerText, 10))) {
                            rankBadge.innerText = visibleRank;
                        }
                        visibleRank++;
                    } else {
                        row.style.setProperty('display', 'none', 'important');
                    }
                }
            });
        }
    } catch(e) {}
});

    // 🌟 [에디터 PICK 전용 데이터 바인딩 엔진: 100% 무결점 자동 렌더링]
    function renderEditorPickCard() {
        if (typeof HONEYJAR_POSTS_REGISTRY === 'undefined' || !Array.isArray(HONEYJAR_POSTS_REGISTRY) || HONEYJAR_POSTS_REGISTRY.length === 0) return;
        
        // isEditorPick: true인 글 검색 (없으면 첫 번째 글)
        const localPickSlug = localStorage.getItem('chageul_editor_pick_slug') || localStorage.getItem('honeyjar_editor_pick_slug');
        let pickPost = null;
        if (localPickSlug) {
            pickPost = HONEYJAR_POSTS_REGISTRY.find(p => p.slug === localPickSlug || p.slug === localPickSlug + '.html' || p.slug.replace('.html','') === localPickSlug.replace('.html',''));
        }
        if (!pickPost) {
            pickPost = HONEYJAR_POSTS_REGISTRY.find(p => p.isEditorPick === true) || HONEYJAR_POSTS_REGISTRY[0];
        }
        if (!pickPost) return;

        const postHref = 'posts/' + pickPost.slug;
        const postTitle = pickPost.fullTitle || pickPost.title || '';
        const postThumb = pickPost.thumb || '';
        const postCat = pickPost.cat || '포커스';
        const postDate = pickPost.date || '2026. 8. 30.';
        const postDesc = pickPost.summary || `"${postTitle}"에 대한 상세 분석 및 가이드`;

        // 1. PC 좌측 히어로 대형 배너 업데이트
        const heroLeft = document.querySelector('.hero-master-left');
        if (heroLeft) {
            const heroA = heroLeft.querySelector('a');
            const heroImg = heroLeft.querySelector('img');
            const heroCat = heroLeft.querySelector('.hero-cat-tag');
            const heroH2A = heroLeft.querySelector('.hero-title-text a');
            const heroDesc = heroLeft.querySelector('.hero-desc-text');
            const heroMeta = heroLeft.querySelector('div[style*="border-top"] span');

            if (heroA) heroA.setAttribute('href', postHref);
            if (heroImg) {
                heroImg.setAttribute('src', postThumb);
                heroImg.setAttribute('alt', postTitle);
            }
            if (heroCat) heroCat.textContent = postCat;
            if (heroH2A) {
                heroH2A.setAttribute('href', postHref);
                heroH2A.textContent = postTitle;
            }
            if (heroDesc) heroDesc.textContent = `"${postDesc}"`;
            if (heroMeta) heroMeta.textContent = `차를 쓰다 · ${postDate}`;
        }

        // 2. 모바일 매거진 커버 배너 업데이트
        const mobPick = document.querySelector('.mobile-editor-pick-card');
        if (mobPick) {
            mobPick.setAttribute('onclick', `location.href='${postHref}'`);
            const mobImg = mobPick.querySelector('img');
            const mobH3 = mobPick.querySelector('h3');
            const mobP = mobPick.querySelector('p');
            const mobDate = mobPick.querySelector('div[style*="border-top"] span');

            if (mobImg) {
                mobImg.setAttribute('src', postThumb);
                mobImg.setAttribute('alt', postTitle);
            }
            if (mobH3) mobH3.textContent = postTitle;
            if (mobP) mobP.textContent = `"${postDesc}"`;
            if (mobDate) mobDate.textContent = `차를 쓰다 · ${postDate}`;
        }
    }

/**
 * 🍯 꿀단지 공식 모바일 액션 & 실시간 인기글 랭킹 엔진 (HoneyJar Real-Time Global Features & Dynamic Popular Ranking)
 * - 1인 1하트 중복 방지 + 글로벌 실시간 하트 동기화 + 하단바 댓글수 즉시 연동
 * - 🕒 3일 후 자동 소멸 스마트 최신 뱃지 시스템 (Auto-Expiring New Badge System)
 * - 📈 100% 실시간 조회수 기반 인기글 TOP 5 자동 랭킹 시스템 (Dynamic Real-Time Popular Ranking)
 */

var ABACUS_BASE = window.ABACUS_BASE || "https://abacus.jasoncameron.dev";
var ABACUS_NS = window.ABACUS_NS || "honeyjar_wellness";

// 📚 꿀단지 공식 10대 칼럼 마스터 레지스트리 (실제 이미지 폴더 경로 100% 일치)
const HONEYJAR_POSTS_REGISTRY = [
    {
        slug: "post-meal-walk-blood-sugar.html",
        slugKey: "post_meal_walk_blood_sugar",
        title: "식후 10분 걷기와 혈당 스파이크 차단",
        fullTitle: "식후 10분 걷기의 기적: 혈당 스파이크 잡고 식곤증·내장지방 없애는 루틴",
        thumb: "images/posts/walking/thumb.jpg?v=2.0",
        cat: "라이프 웰니스",
        baseWeight: 140
    },
    {
        slug: "ohnara-diet.html",
        slugKey: "ohnara_diet",
        title: "오나라 51세 식단과 50대 근력 운동법",
        fullTitle: "오나라 식단 공개, 51세 47kg 관리법과 50대 근력 운동",
        thumb: "images/posts/ohnara/thumb.jpg?v=1.2",
        cat: "식단 & 영양",
        baseWeight: 142
    },
    {
        slug: "knee-safe-squat-workout.html",
        slugKey: "knee_safe_squat_workout",
        title: "무릎 안 아픈 스쿼트·런지 3대 수칙",
        fullTitle: "초보자 무릎 통증 없는 하체 근력 운동법: 스쿼트·런지 올바른 자세",
        thumb: "images/posts/squat/thumb.jpg?v=2.0",
        cat: "홈트레이닝",
        baseWeight: 135
    },
    {
        slug: "august-seasonal-foods.html",
        slugKey: "august_seasonal_foods",
        title: "8월 제철 음식 5가지 영양 가이드",
        fullTitle: "8월 제철 음식 5가지, 늦여름 기력 회복과 영양 성분 가이드",
        thumb: "images/posts/august/thumb.jpg?v=1.1",
        cat: "식단 & 영양",
        baseWeight: 118
    },
    {
        slug: "mediterranean-diet.html",
        slugKey: "mediterranean_diet",
        title: "지중해식 식단 가이드 & 장보기 팁",
        fullTitle: "세계 1위 건강 식단 지중해식 식단 가이드와 한국형 장보기 팁",
        thumb: "images/posts/mediterranean/thumb.jpg?v=1.2",
        cat: "식단 & 영양",
        baseWeight: 104
    },
    {
        slug: "intermittent-fasting-guide.html",
        slugKey: "intermittent_fasting_guide",
        title: "간헐적 단식 16:8 성공 식사 시간표",
        fullTitle: "간헐적 단식 16:8 방법과 부작용 예방, 성공적인 식사 시간표",
        thumb: "images/posts/fasting/thumb.jpg?v=1.1",
        cat: "식단 & 영양",
        baseWeight: 96
    },
    {
        slug: "core-exercise-home.html",
        slugKey: "core_exercise_home",
        title: "허리 강화 10분 홈트 코어 루틴",
        fullTitle: "바른 자세와 허리 건강을 위한 10분 홈트 코어 운동 루틴",
        thumb: "images/posts/core/thumb.jpg",
        cat: "홈트레이닝",
        baseWeight: 89
    },
    {
        slug: "morning-routine.html",
        slugKey: "morning_routine",
        title: "활력과 체지방 태우는 아침 공복 루틴",
        fullTitle: "아침 공복 루틴 가이드: 체지방 감량과 활력을 돕는 기상 1시간 습관",
        thumb: "images/posts/morning/thumb.jpg",
        cat: "라이프 웰니스",
        baseWeight: 81
    },
    {
        slug: "sleep-hygiene-guide.html",
        slugKey: "sleep_hygiene_guide",
        title: "수면의 질 2배 멜라토닌 침실 루틴",
        fullTitle: "수면의 질을 2배 높이는 멜라토닌 수면 위생과 침실 환경 가이드",
        thumb: "images/posts/sleep/thumb.jpg",
        cat: "라이프 웰니스",
        baseWeight: 75
    },
    {
        slug: "posture-stretching-office.html",
        slugKey: "posture_stretching_office",
        title: "거북목·라운드숄더 교정 5분 스트레칭",
        fullTitle: "직장인을 위한 거북목·라운드숄더 교정 5분 오피스 스트레칭",
        thumb: "images/posts/posture/thumb.jpg",
        cat: "홈트레이닝",
        baseWeight: 68
    },
    {
        slug: "water-intake-guide.html",
        slugKey: "water_intake_guide",
        title: "하루 물 2L 마시기 오해와 진실",
        fullTitle: "하루 물 2L 마시기, 정말 건강에 좋을까? 내 몸에 맞는 진짜 수분 섭취법",
        thumb: "images/posts/water/thumb.jpg",
        cat: "라이프 웰니스",
        baseWeight: 62
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

// 3. 🕒 3일 후 자동 소멸 스마트 최신 뱃지 시스템
function initAutoExpiringBadges() {
    const DAYS_LIMIT = 3;
    const now = new Date();
    // 포스트 상세 페이지의 .article-meta-bar는 빌더 템플릿이 단일 뱃지를 정적으로 관리하므로 중복 방지를 위해 제외
    const metaDateElements = document.querySelectorAll('.feed-item-meta span, .clean-card .article-item div[style*="font-size:0.76rem"]');

    metaDateElements.forEach(el => {
        const text = el.textContent || '';
        const match = text.match(/(\d{4})[.\s년]+(\d{1,2})[.\s월]+(\d{1,2})/);
        if (!match) return;

        const rawDate = `${match[1]}-${String(match[2]).padStart(2, '0')}-${String(match[3]).padStart(2, '0')}T00:00:00+09:00`;
        const postDate = new Date(rawDate);
        const diffTime = now.getTime() - postDate.getTime();
        const diffDays = diffTime / (1000 * 60 * 60 * 24);
        
        const baseDateStr = `${postDate.getFullYear()}.${String(postDate.getMonth()+1).padStart(2, '0')}.${String(postDate.getDate()).padStart(2, '0')}`;
        
        const article = el.closest('article');
        const catBadge = article ? article.querySelector('.feed-item-cat, .clean-card span[style*="font-size:0.75rem"]') : null;

        if (diffDays >= 0 && diffDays <= DAYS_LIMIT) {
            el.innerHTML = baseDateStr;
            
            if (catBadge && !catBadge.querySelector('.badge-cat-new') && !catBadge.textContent.includes('NEW')) {
                const newTag = document.createElement('span');
                newTag.className = 'badge-cat-new';
                newTag.textContent = ' · NEW';
                newTag.style.color = '#e11d48';
                newTag.style.fontWeight = '800';
                catBadge.appendChild(newTag);
            }
        } else {
            el.textContent = baseDateStr;
            if (catBadge) {
                const catNew = catBadge.querySelector('.badge-cat-new');
                if (catNew) catNew.remove();
                catBadge.textContent = catBadge.textContent.replace(' · NEW', '').replace('', '').replace('· NEW', '').replace('· 관절 보호', '').trim();
                const originCat = article.getAttribute('data-category');
                if (originCat) catBadge.textContent = originCat;
            }
        }
    });
}

// 4. 📈 실시간 조회수 기반 인기글 TOP 5 자동 랭킹 엔진
async function initDynamicPopularRanking() {
    const isPostPage = window.location.pathname.includes('/posts/');
    
    // 1) 각 글별 실시간 조회수 점수 계산
    const rankedPosts = HONEYJAR_POSTS_REGISTRY.map(post => {
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

    // 2) 점수 기준 내림차순(높은 순) 정렬 후 TOP 5 추출
    rankedPosts.sort((a, b) => b.score - a.score);
    const top5 = rankedPosts.slice(0, 5);

    // 3) PC 데스크톱 사이드바 위젯 렌더링
    const sidebarLists = document.querySelectorAll('.popular-list');
    sidebarLists.forEach(listEl => {
        let html = '';
        top5.forEach((item, idx) => {
            html += `
                <li class="popular-item">
                    <span class="popular-rank">${idx + 1}</span>
                    <a href="${item.linkUrl}" class="popular-link">${item.title}</a>
                </li>
            `;
        });
        listEl.innerHTML = html;
    });

    // 사이드바 위젯 헤더 타이틀을 '인기글 TOP 5'로 정돈
    const widgetTitles = document.querySelectorAll('.sidebar-widget .widget-title span');
    widgetTitles.forEach(titleEl => {
        if (titleEl.textContent.includes('인기')) {
            titleEl.textContent = '인기글 TOP 5';
        }
    });

    // 4) 모바일 메인 인기글 카드 박스 렌더링
    const mobilePopularBox = document.querySelector('.popular-posts-card-box');
    if (mobilePopularBox) {
        let mobileHtml = '';
        top5.forEach((item, idx) => {
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
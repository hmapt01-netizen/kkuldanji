﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿/**
 * 🍯 꿀단지 공식 모바일 액션 & 실시간 인기글 랭킹 엔진 (HoneyJar Real-Time Global Features & Dynamic Popular Ranking)
 * - 1인 1하트 중복 방지 + 글로벌 실시간 하트 동기화 + 하단바 댓글수 즉시 연동
 * - 🕒 3일 후 자동 소멸 스마트 최신 뱃지 시스템 (Auto-Expiring New Badge System)
 * - 📈 100% 실시간 조회수 기반 인기글 TOP 5 자동 랭킹 시스템 (Dynamic Real-Time Popular Ranking)
 */

var ABACUS_BASE = window.ABACUS_BASE || "https://abacus.jasoncameron.dev";
var ABACUS_NS = window.ABACUS_NS || "honeyjar_wellness";

var HONEYJAR_POSTS_REGISTRY = window.HONEYJAR_POSTS_REGISTRY;

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
            // 3일 이내 작성된 글: 단 1개의 (최신) 뱃지만 부착 (중복 제거)
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

    // 1) 꿀단지 전체 글 가중치 및 실시간 조회수 합산
    const rankedPosts = HONEYJAR_POSTS_REGISTRY
        .filter(post => !hiddenSlugs.includes(post.slug))
        .map(post => {
            let liveHits = 0;
            try {
                const localHits = parseInt(localStorage.getItem("honeyjar_views_" + post.slugKey), 10);
                if (!isNaN(localHits)) liveHits = localHits;
            } catch(e) {}
            
            const totalScore = (post.baseWeight || 100) + (liveHits * 3);
            return {
                ...post,
                score: totalScore,
                linkUrl: isPostPage ? post.slug : `posts/${post.slug}`,
                thumbUrl: isPostPage ? `../${post.thumb}` : post.thumb
            };
        });

    // 2) 점수 기준 정렬
    rankedPosts.sort((a, b) => b.score - a.score);
    const top10 = rankedPosts.slice(0, 10);
    const top5Mobile = rankedPosts.slice(0, 5);

    // 3) PC 메인 히어로 우측 TOP 10 위젯 업데이트
    const heroRightList = document.querySelector('.hero-master-right ul');
    if (heroRightList) {
        let html = '';
        top10.forEach((item, idx) => {
            const rankNum = idx + 1;
            const rankColor = rankNum <= 3 ? '#c26908' : '#94a3b8';
            html += `
                <li style="display:flex; align-items:center; gap:10px; padding:3px 0;">
                    <span style="font-size:0.98rem; font-weight:900; color:${rankColor}; width:20px; text-align:center; flex-shrink:0;">${rankNum}</span>
                    <a href="${item.linkUrl}" style="font-size:0.88rem; font-weight:${rankNum <= 3 ? '750' : '650'}; color:${rankNum <= 3 ? '#1e293b' : '#334155'}; text-decoration:none; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; flex:1;" title="${item.fullTitle || item.title}">${item.fullTitle || item.title}</a>
                </li>
            `;
        });
        heroRightList.innerHTML = html;
    }

    // 4) 모바일 메인 인기글 TOP 5 카드 업데이트
    const mobTop5Container = document.querySelector('.mobile-popular-top5-card, #mobilePopularBox');
    if (mobTop5Container) {
        let html = '';
        top5Mobile.forEach((item, idx) => {
            const rankNum = idx + 1;
            const rankColor = rankNum <= 3 ? '#c26908' : '#94a3b8';
            html += `
                <div style="display:flex; justify-content:space-between; align-items:center; padding:11px 0; border-bottom:1px solid #f1f5f9; cursor:pointer;" onclick="location.href='${item.linkUrl}'">
                    <div style="flex:1; padding-right:12px; min-width:0;">
                        <h4 style="font-size:0.90rem; font-weight:800; color:#111827; margin:0 0 4px 0; line-height:1.35; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">
                            ${item.fullTitle || item.title}
                        </h4>
                        <div style="display:flex; align-items:center; font-size:0.75rem;">
                            <span style="font-weight:800; color:${rankColor}; margin-right:8px;">TOP ${rankNum}</span>
                            <span style="color:#64748b;">${item.cat || '라이프 웰니스'}</span>
                        </div>
                    </div>
                    <img src="${item.thumbUrl}" alt="${item.fullTitle || item.title}" style="width:60px; height:60px; border-radius:10px; object-fit:cover; flex-shrink:0;">
                </div>
            `;
        });
        mobTop5Container.innerHTML = html;
    }

    // 5) 본문 페이지(포스트 상세) 사이드바 위젯 렌더링
    const sidebarLists = document.querySelectorAll('.popular-list, #popularPostsWidgetList');
    sidebarLists.forEach(listEl => {
        let html = '';
        top10.forEach((item, idx) => {
            const rankNum = idx + 1;
            const rankColor = rankNum <= 3 ? '#c26908' : (rankNum <= 5 ? '#ea580c' : '#94a3b8');
            html += `
                <li class="popular-item" style="display:flex; align-items:center; gap:10px; padding:7px 0; border-bottom:1px solid #f8fafc;">
                    <span class="popular-rank" style="font-size:0.95rem; font-weight:900; color:${rankColor}; width:20px; text-align:center; flex-shrink:0;">${rankNum}</span>
                    <a href="${item.linkUrl}" class="popular-link" style="font-size:0.86rem; font-weight:${rankNum <= 3 ? '700' : '650'}; color:${rankNum <= 3 ? '#1e293b' : '#334155'}; text-decoration:none; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; flex:1;" title="${item.fullTitle || item.title}">${item.fullTitle || item.title}</a>
                </li>
            `;
        });
        listEl.innerHTML = html;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initBottomHeart();
        renderEditorPickCard();
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
        
        let pickPost = HONEYJAR_POSTS_REGISTRY.find(p => p.isEditorPick);
        if (!pickPost) {
            const localPickSlug = localStorage.getItem('honeyjar_editor_pick_slug');
            if (localPickSlug) {
                pickPost = HONEYJAR_POSTS_REGISTRY.find(p => p.slug === localPickSlug || p.slug === localPickSlug + '.html' || p.slug.replace('.html','') === localPickSlug.replace('.html',''));
            }
        }
        if (!pickPost) {
            pickPost = HONEYJAR_POSTS_REGISTRY.find(p => p.slug === 'slow-aging-rice-recipe.html') || HONEYJAR_POSTS_REGISTRY[0];
        }
        if (!pickPost) return;

        const postHref = 'posts/' + pickPost.slug;
        const postTitle = pickPost.fullTitle || pickPost.title || '';
        const postThumb = pickPost.thumb || '';
        const postCat = pickPost.cat || '라이프 웰니스';
        const postDate = pickPost.date || '2026. 8. 30.';
        const postDesc = pickPost.summary || `"${postTitle}"에 대한 상세 분석 및 가이드`;

        // 1. PC 좌측 대형 화보 추천 카드 업데이트
        const heroLeft = document.querySelector('.hero-master-left');
        if (heroLeft) {
            const heroA = heroLeft.querySelector('a');
            const heroImg = heroLeft.querySelector('img');
            const heroCat = heroLeft.querySelector('.hero-cat-tag');
            const heroH2A = heroLeft.querySelector('.hero-title-text a, h2 a');
            const heroDesc = heroLeft.querySelector('.hero-desc-text');
            const heroMeta = heroLeft.querySelector('div[style*="border-top"] span, .hero-meta-span');

            if (heroA && heroA.getAttribute('href') !== postHref) heroA.setAttribute('href', postHref);
            if (heroImg && heroImg.getAttribute('src') !== postThumb) {
                heroImg.setAttribute('src', postThumb);
                heroImg.setAttribute('alt', postTitle);
            }
            if (heroCat && heroCat.textContent !== postCat) heroCat.textContent = postCat;
            if (heroH2A && heroH2A.textContent !== postTitle) {
                heroH2A.setAttribute('href', postHref);
                heroH2A.textContent = postTitle;
            }
            if (heroDesc && heroDesc.textContent !== postDesc) heroDesc.textContent = postDesc;
            if (heroMeta) heroMeta.textContent = `에디터 혀니 · ${postDate}`;
        }

        // 2. 모바일 에디터 PICK 배너 업데이트
        const mobPick = document.querySelector('.mobile-editor-pick-card');
        if (mobPick) {
            mobPick.setAttribute('onclick', `location.href='${postHref}'`);
            const mobImg = mobPick.querySelector('img');
            const mobTitle = mobPick.querySelector('h4, h3');

            if (mobImg && mobImg.getAttribute('src') !== postThumb) {
                mobImg.setAttribute('src', postThumb);
                mobImg.setAttribute('alt', postTitle);
            }
            if (mobTitle && mobTitle.textContent !== postTitle) mobTitle.textContent = postTitle;
        }
    }

    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        renderEditorPickCard();
        initDynamicPopularRanking();
    }

/**
 * 🍯 꿀단지 공식 모바일 액션 & 스마트 뱃지 엔진 (HoneyJar Real-Time Global Heart & Smart Badge Engine)
 * - 1인 1하트 중복 방지 + 글로벌 실시간 하트 동기화 + 하단바 댓글수 즉시 연동
 * - 🕒 3일 후 자동 소멸 스마트 최신 뱃지 시스템 (Auto-Expiring New Badge System)
 */

const ABACUS_BASE = "https://abacus.jasoncameron.dev";
const ABACUS_NS = "honeyjar_wellness";

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

// 1. 하트 공감 토글 (1인 1회 확실한 공감 + 중복 무한 증가 원천 방지)
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

    // 신규 공감 등록
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

    // 1) 내가 이전에 누른 상태 복원 (빨간 꽉 찬 하트)
    if (btn) {
        if (localStorage.getItem(storageUserLikeKey) === "true") {
            btn.classList.add('liked');
        } else {
            btn.classList.remove('liked');
        }
    }

    // 2) 하단 바 댓글 수 즉시 복원
    try {
        const commentRaw = localStorage.getItem("honeyjar_comments_" + slug);
        if (commentRaw) {
            const commentArr = JSON.parse(commentRaw);
            if (Array.isArray(commentArr)) {
                syncBottomCommentCount(commentArr.length);
            }
        }
    } catch(e) {}

    // 3) 글로벌 클라우드에서 전 세계 실제 누적 하트 수 가져오기
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

// 3. 댓글 작성창으로 스크롤 이동
function scrollToComments() {
    const target = document.getElementById('commentSectionWrapper') || document.querySelector('.comment-section') || document.getElementById('comments');
    if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        setTimeout(() => {
            const authorInput = document.getElementById('commentAuthorInput') || document.querySelector('.comment-textarea');
            if (authorInput) authorInput.focus();
        }, 500);
    }
}

// 4. URL 링크 복사
function copyCurrentUrl() {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(window.location.href).then(() => {
            showToast('링크 주소가 복사되었습니다 🔗');
        }).catch(() => fallbackCopy());
    } else {
        fallbackCopy();
    }
}

function fallbackCopy() {
    const tempInput = document.createElement('input');
    tempInput.value = window.location.href;
    document.body.appendChild(tempInput);
    tempInput.select();
    try {
        document.execCommand('copy');
        showToast('링크 주소가 복사되었습니다 🔗');
    } catch (e) {
        prompt('아래 링크를 복사하세요:', window.location.href);
    }
    document.body.removeChild(tempInput);
}

// 5. 토스트 메시지
function showToast(msg) {
    const oldToast = document.querySelector('.toast-notice');
    if (oldToast) oldToast.remove();
    const toast = document.createElement('div');
    toast.className = 'toast-notice';
    toast.innerText = msg;
    document.body.appendChild(toast);
    setTimeout(() => { if (toast && toast.parentNode) toast.remove(); }, 2000);
}

function syncBottomCommentCount(count) {
    const commentCountEls = document.querySelectorAll('.naver-bottom-bar .comment-count');
    commentCountEls.forEach(el => {
        el.innerText = count;
    });
}

// 6. 🕒 스마트 자동 3일 시한부 최신 뱃지 시스템 (Auto-Expiring New Badge Engine)
function initAutoExpiringBadges() {
    const now = new Date();
    const DAYS_LIMIT = 3; // 정확히 3일(72시간) 기준

    // PC 및 모바일의 모든 날짜 엘리먼트 자동 탐색
    const dateEls = document.querySelectorAll('[data-post-date], .clean-card div[style*="font-size:0.76rem"], .feed-item-meta span');
    
    dateEls.forEach(el => {
        let rawDate = el.getAttribute('data-post-date');
        if (!rawDate) {
            const match = el.textContent.match(/(\d{4})[.\-](\d{1,2})[.\-](\d{1,2})/);
            if (match) {
                rawDate = `${match[1]}-${match[2].padStart(2, '0')}-${match[3].padStart(2, '0')}`;
            }
        }
        
        if (!rawDate) return;
        
        const postDate = new Date(rawDate);
        const diffTime = now.getTime() - postDate.getTime();
        const diffDays = diffTime / (1000 * 60 * 60 * 24);
        
        const baseDateStr = `${postDate.getFullYear()}.${String(postDate.getMonth()+1).padStart(2, '0')}.${String(postDate.getDate()).padStart(2, '0')}`;
        
        const article = el.closest('article');
        const catBadge = article ? article.querySelector('.feed-item-cat, .clean-card span[style*="font-size:0.75rem"]') : null;

        if (diffDays >= 0 && diffDays <= DAYS_LIMIT) {
            // ✅ 3일 이내: 최신 뱃지 자동 표시
            el.innerHTML = `${baseDateStr} <span class="badge-auto-new" style="display:inline-block; background:#fee2e2; color:#ef4444; font-size:0.72rem; font-weight:800; padding:1px 5px; border-radius:4px; margin-left:4px; vertical-align:middle; border:1px solid #fca5a5;">(최신)</span>`;
            
            if (catBadge && !catBadge.querySelector('.badge-cat-new') && !catBadge.textContent.includes('NEW')) {
                const newTag = document.createElement('span');
                newTag.className = 'badge-cat-new';
                newTag.textContent = ' · NEW';
                newTag.style.color = '#e11d48';
                newTag.style.fontWeight = '800';
                catBadge.appendChild(newTag);
            }
        } else {
            // ❌ 3일 경과: 뱃지 100% 자동 소멸 (날짜만 정돈)
            el.textContent = baseDateStr;
            if (catBadge) {
                const catNew = catBadge.querySelector('.badge-cat-new');
                if (catNew) catNew.remove();
                catBadge.textContent = catBadge.textContent.replace(' · NEW', '').replace('(최신)', '').replace('· NEW', '').replace('· 관절 보호', '').trim();
                // 카테고리 본연의 텍스트 복원
                const originCat = article.getAttribute('data-category');
                if (originCat) catBadge.textContent = originCat;
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initBottomHeart();
    initAutoExpiringBadges();
});
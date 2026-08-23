/**
 * 🍯 꿀단지 공식 모바일 액션 엔진 (HoneyJar Real-Time Global Heart & Action Engine)
 * - Abacus 글로벌 클라우드 REST API 기반 100% 실시간 하트 연동
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

// 1. 하트 공감 토글 및 글로벌 클라우드 실시간 전송
async function toggleBottomHeart(btn) {
    const slug = getArticleSlug();
    const slugKey = getSlugKey(slug);
    const countEl = btn.querySelector('.heart-count');
    if (!countEl) return;

    const storageUserLikeKey = "honeyjar_user_liked_" + slug;
    const isAlreadyLiked = localStorage.getItem(storageUserLikeKey) === "true";

    let currentHearts = parseInt(countEl.innerText, 10) || 0;

    if (isAlreadyLiked) {
        // 좋아요 취소
        currentHearts = Math.max(0, currentHearts - 1);
        btn.classList.remove('liked');
        localStorage.setItem(storageUserLikeKey, "false");
        countEl.innerText = currentHearts;
        showToast('공감을 취소했습니다.');
    } else {
        // 좋아요 등록 (글로벌 카운터 +1)
        btn.classList.add('liked');
        localStorage.setItem(storageUserLikeKey, "true");
        
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
}

// 2. 페이지 로드 시 전 세계 실제 하트 수 실시간 복원
async function initBottomHeart() {
    const slug = getArticleSlug();
    const slugKey = getSlugKey(slug);
    const btn = document.querySelector('.naver-bottom-btn[onclick*="toggleBottomHeart"]');
    if (!btn) return;

    const countEl = btn.querySelector('.heart-count');
    if (!countEl) return;

    const storageUserLikeKey = "honeyjar_user_liked_" + slug;

    // 1) 내가 이전에 누른 상태 복원 (빨간 꽉 찬 하트)
    if (localStorage.getItem(storageUserLikeKey) === "true") {
        btn.classList.add('liked');
    } else {
        btn.classList.remove('liked');
    }

    // 2) 글로벌 클라우드에서 전 세계 실제 누적 하트 수 가져오기
    try {
        const res = await fetch(`${ABACUS_BASE}/get/${ABACUS_NS}/hearts_${slugKey}`);
        if (res.ok) {
            const data = await res.json();
            if (data && typeof data.value === 'number') {
                countEl.innerText = data.value;
                return;
            }
        }
    } catch(e) {}
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

document.addEventListener('DOMContentLoaded', () => {
    initBottomHeart();
});
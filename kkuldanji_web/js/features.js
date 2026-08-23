/**
 * 🍯 꿀단지 공식 모바일 액션 엔진 (HoneyJar Real-Time Global Heart & Action Engine)
 * - 전 세계 모든 독자의 하트 공감 실시간 클라우드 DB 동기화
 */

const CLOUD_HEARTS_BASE = "https://honeyjar-analytics-default-rtdb.firebaseio.com/honeyjar_hearts";

function getArticleSlug() {
    const path = window.location.pathname;
    const parts = path.split('/');
    let s = parts[parts.length - 1] || "default.html";
    if (s === "") s = "index.html";
    return s;
}

function getSlugKey(slug) {
    return slug.replace(/[\.\#\$\[\]\/]/g, '_');
}

// 1. 하트 공감 토글 및 글로벌 클라우드 DB 실시간 전송
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
        // 좋아요 등록
        currentHearts += 1;
        btn.classList.add('liked');
        localStorage.setItem(storageUserLikeKey, "true");
        countEl.innerText = currentHearts;
        showToast('글에 공감하셨습니다 ❤️');
    }

    // 클라우드 DB에 실시간 반영
    try {
        const url = `${CLOUD_HEARTS_BASE}/${slugKey}.json`;
        fetch(url, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(currentHearts)
        }).catch(() => {});
    } catch(e) {}
}

// 2. 페이지 로드 시 전 세계 실제 하트 수 클라우드 실시간 복원
async function initBottomHeart() {
    const slug = getArticleSlug();
    const slugKey = getSlugKey(slug);
    const btn = document.querySelector('.naver-bottom-btn[onclick*="toggleBottomHeart"]');
    if (!btn) return;

    const countEl = btn.querySelector('.heart-count');
    if (!countEl) return;

    const storageUserLikeKey = "honeyjar_user_liked_" + slug;

    // 1) 내 폰의 좋아요 상태 복원
    if (localStorage.getItem(storageUserLikeKey) === "true") {
        btn.classList.add('liked');
    } else {
        btn.classList.remove('liked');
    }

    // 2) 클라우드 DB에서 전 세계 실제 누적 하트 수 실시간 가져오기
    try {
        const url = `${CLOUD_HEARTS_BASE}/${slugKey}.json`;
        const res = await fetch(url, { method: "GET" });
        if (res.ok) {
            const count = await res.json();
            if (typeof count === 'number') {
                countEl.innerText = count.toString();
                return;
            }
        }
    } catch(e) {}
}

// 3. 댓글 작성창으로 부드러운 스크롤 이동
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

// 4. URL 링크 복사 기능
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

// 5. 토스트 알림 메시지
function showToast(msg) {
    const oldToast = document.querySelector('.toast-notice');
    if (oldToast) oldToast.remove();
    const toast = document.createElement('div');
    toast.className = 'toast-notice';
    toast.innerText = msg;
    document.body.appendChild(toast);
    setTimeout(() => { if (toast && toast.parentNode) toast.remove(); }, 2000);
}

// 6. 하단바 댓글 개수 실시간 동기화 함수
function syncBottomCommentCount(count) {
    const commentCountEls = document.querySelectorAll('.naver-bottom-bar .comment-count');
    commentCountEls.forEach(el => {
        el.innerText = count;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initBottomHeart();
});
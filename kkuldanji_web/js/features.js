/**
 * 🍯 꿀단지 공식 모바일 액션 엔진 (HoneyJar Real-Time Global Heart & Action Engine)
 * - 1인 1하트 중복 방지 + 글로벌 실시간 하트 동기화 + 하단바 댓글수 즉시 연동
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

document.addEventListener('DOMContentLoaded', () => {
    initBottomHeart();
});
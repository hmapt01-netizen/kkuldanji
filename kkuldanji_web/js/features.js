// Clean Reset to 0 for Hearts
(function checkHeartsReset() {
    var RESET_FLAG = 'honeyjar_hearts_reset_v3';
    if (!localStorage.getItem(RESET_FLAG)) {
        for (var i = localStorage.length - 1; i >= 0; i--) {
            var k = localStorage.key(i);
            if (k && (k.indexOf('honeyjar_hearts_') === 0 || k.indexOf('honeyjar_user_liked_') === 0)) {
                localStorage.removeItem(k);
            }
        }
        localStorage.setItem(RESET_FLAG, 'true');
    }
})();
// ==========================================================================
// 🍯 [꿀단지 모바일 액션 엔진] 하트 공감 저장, 댓글 수 실시간 동기화, 공유 토스트
// ==========================================================================

// 현재 글 식별자 슬러그
function getArticleSlug() {
    const path = window.location.pathname;
    const parts = path.split('/');
    return parts[parts.length - 1] || "default.html";
}

// 1. 하트 공감 토글 및 로컬 스토리지 영구 저장
function toggleBottomHeart(btn) {
    const slug = getArticleSlug();
    const countEl = btn.querySelector('.heart-count');
    if (!countEl) return;

    const storageHeartKey = "honeyjar_hearts_" + slug;
    const storageUserLikeKey = "honeyjar_user_liked_" + slug;

    let currentHearts = parseInt(localStorage.getItem(storageHeartKey), 10);
    if (isNaN(currentHearts)) {
        currentHearts = parseInt(countEl.innerText, 10) || 0;
    }

    const isAlreadyLiked = localStorage.getItem(storageUserLikeKey) === "true";

    if (isAlreadyLiked) {
        // 좋아요 취소
        currentHearts = Math.max(0, currentHearts - 1);
        btn.classList.remove('liked');
        localStorage.setItem(storageUserLikeKey, "false");
        localStorage.setItem(storageHeartKey, currentHearts.toString());
        countEl.innerText = currentHearts;
        showToast('공감을 취소했습니다.');
    } else {
        // 좋아요 등록
        currentHearts += 1;
        btn.classList.add('liked');
        localStorage.setItem(storageUserLikeKey, "true");
        localStorage.setItem(storageHeartKey, currentHearts.toString());
        countEl.innerText = currentHearts;
        showToast('글에 공감하셨습니다 ❤️');
    }
}

// 2. 페이지 로드 시 하트 상태 및 숫자 복원
function initBottomHeart() {
    const slug = getArticleSlug();
    const btn = document.querySelector('.naver-bottom-btn[onclick*="toggleBottomHeart"]');
    if (!btn) return;

    const countEl = btn.querySelector('.heart-count');
    if (!countEl) return;

    const storageHeartKey = "honeyjar_hearts_" + slug;
    const storageUserLikeKey = "honeyjar_user_liked_" + slug;

    // 저장된 하트 수 복원
    let savedHearts = localStorage.getItem(storageHeartKey);
    if (savedHearts !== null) {
        countEl.innerText = savedHearts;
    } else {
        // 초기 기본값 저장
        const defaultNum = parseInt(countEl.innerText, 10) || 0;
        localStorage.setItem(storageHeartKey, defaultNum.toString());
    }

    // 유저 좋아요 여부 복원
    if (localStorage.getItem(storageUserLikeKey) === "true") {
        btn.classList.add('liked');
    } else {
        btn.classList.remove('liked');
    }
}

// 3. 댓글 작성창으로 부드러운 스크롤 이동
function scrollToComments() {
    const target = document.getElementById('commentSectionWrapper') || document.querySelector('.comment-section') || document.getElementById('comments');
    if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        setTimeout(() => {
            const authorInput = document.getElementById('commentAuthor') || document.querySelector('.comment-input');
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

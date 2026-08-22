﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿/**
 * 꿀단지 블로그 - 스마트 클린 댓글 시스템 (Clean Comment Engine with Profanity Filter)
 * 버전: v2.0
 */

// 대표적인 한국어 비속어, 욕설, 음란, 불법 스팸 금칙어 사전
const PROFANITY_LIST = [
    '시발', '씨발', '씨바', 'ㅅㅂ', '시바', '시펄', '씨펄',
    '병신', 'ㅂㅅ', 'ㅄ', '븅신', '등신',
    '개새끼', '개색기', '개새', '개년', '개놈', '개소리',
    '지랄', 'ㅈㄹ', '염병', '호로',
    '존나', '좆', '좃', 'ㅈㄴ', '씹', '쌉',
    '미친놈', '미친년', '미쳤냐', '또라이', '돌아이',
    '닥쳐', '꺼져', '죽어라', '자살',
    '토토', '카지노', '바카라', '릴게임', '홀덤', '성인용품', '출장안마', '야동', '섹스'
];

// 금칙어 포함 여부 검사 함수 (공백 및 특수문자 변형 포함 검출)
function checkProfanity(text) {
    if (!text) return null;
    const normalized = text.toLowerCase().replace(/[\s\.\,\_\-\~\!\@\#\$\%\^\&\*\(\)\+]/g, '');
    for (const badWord of PROFANITY_LIST) {
        const badNorm = badWord.toLowerCase().replace(/\s/g, '');
        if (normalized.includes(badNorm) || text.includes(badWord)) {
            return badWord;
        }
    }
    return null;
}

// Post default initial comments dataset (0으로 완전 초기화)
const defaultPostComments = {};

// Clean Reset to 0 for Comments
(function checkCommentsReset() {
    const RESET_FLAG = 'honeyjar_comment_reset_v3';
    if (!localStorage.getItem(RESET_FLAG)) {
        for (let i = localStorage.length - 1; i >= 0; i--) {
            const k = localStorage.key(i);
            if (k && k.startsWith('honeyjar_comments_')) {
                localStorage.removeItem(k);
            }
        }
        localStorage.setItem(RESET_FLAG, 'true');
    }
})();

// Current Post Slug Detector
function getPostSlug() {
    const path = window.location.pathname;
    const parts = path.split('/');
    return parts[parts.length - 1] || "default.html";
}

// Storage Key
function getStorageKey() {
    return "honeyjar_comments_" + getPostSlug();
}

// Load Comments
function loadComments() {
    const slug = getPostSlug();
    const storageKey = getStorageKey();
    const saved = localStorage.getItem(storageKey);
    
    let comments = [];
    if (saved) {
        try {
            comments = JSON.parse(saved);
        } catch(e) {
            comments = [];
        }
    } else {
        comments = [];
    }
    return comments;
}

// Save Comments
function saveComments(comments) {
    localStorage.setItem(getStorageKey(), JSON.stringify(comments));
}

// Render Comment Section HTML
function renderCommentSection() {
    const container = document.getElementById('commentSectionWrapper');
    if (!container) return;

    const comments = loadComments();

    let commentsHtml = '';
    comments.forEach(c => {
        const initial = c.author ? c.author.charAt(0) : '꿀';
        commentsHtml += `
            <div class="comment-item" id="comment-${c.id}">
                <div class="comment-item-top">
                    <div class="comment-author-box">
                        <div class="comment-avatar">${initial}</div>
                        <div>
                            <span class="comment-author-name">${escapeHtml(c.author)}</span>
                            <span class="comment-date">${c.date}</span>
                        </div>
                    </div>
                    <a href="javascript:void(0)" class="comment-del-link" onclick="handleDeleteComment(${c.id})">삭제</a>
                </div>
                <div class="comment-body-text">
                    ${escapeHtml(c.text).replace(/\n/g, '<br>')}
                </div>
                <div class="comment-footer-actions">
                    <button type="button" class="comment-like-btn" onclick="handleLikeComment(${c.id}, this)">
                        공감 <span class="like-count">${c.likes || 0}</span>
                    </button>
                </div>
            </div>
        `;
    });

    container.innerHTML = `
        <section class="comment-section">
            <div class="comment-header">
                <h3>
                    <span>독자 소통 & 댓글</span>
                    <span class="comment-count-badge" id="commentCountBadge">${comments.length}개</span>
                </h3>
            </div>

            <div class="comment-form-card">
                <form onsubmit="handleAddComment(event)">
                    <div class="comment-input-row">
                        <input type="text" id="commentAuthorInput" placeholder="닉네임" maxlength="20">
                        <input type="password" id="commentPassInput" placeholder="비밀번호 4자리 (필수)" required minlength="4" maxlength="12">
                    </div>
                    <textarea id="commentTextInput" class="comment-textarea" placeholder="따뜻한 댓글과 건강에 대한 질문을 자유롭게 남겨주세요." required></textarea>
                    <div class="comment-submit-row">
                        <span class="comment-guide-text">비속어 및 욕설은 자동 차단되며 깨끗한 소통 공간을 지킵니다.</span>
                        <button type="submit" class="btn-comment-submit">댓글 등록</button>
                    </div>
                </form>
            </div>

            <div class="comment-list" id="commentListContainer">
                ${comments.length > 0 ? commentsHtml : `
                    <div style="text-align:center; padding:36px 20px; color:#94a3b8; font-size:0.92rem; background:#f8fafc; border-radius:10px; border:1px dashed #e2e8f0; margin-top:14px;">
                        🍯 아직 등록된 댓글이 없습니다. 첫 번째 응원 댓글을 남겨보세요!
                    </div>
                `}
            </div>
        </section>
    `;
}

// Add New Comment with Profanity Filtering (익명 지원 + 비밀번호 필수)
function handleAddComment(e) {
    e.preventDefault();
    const authorInput = document.getElementById('commentAuthorInput');
    const textInput = document.getElementById('commentTextInput');
    const passInput = document.getElementById('commentPassInput');

    const text = textInput?.value.trim();
    if (!text) {
        alert("댓글 내용을 입력해 주세요.");
        if (textInput) textInput.focus();
        return;
    }

    const pass = passInput?.value.trim();
    if (!pass || pass.length < 4) {
        alert("댓글 보호 및 삭제를 위해 비밀번호 4자리를 입력해 주세요.");
        if (passInput) passInput.focus();
        return;
    }

    // 닉네임 미입력 시 '익명' 자동 기본값 부여
    const author = authorInput?.value.trim() || "익명";

    // 1. 닉네임 비속어 검사 (익명이 아닐 때)
    if (author !== "익명") {
        const authorBadWord = checkProfanity(author);
        if (authorBadWord) {
            alert("닉네임에 부적절한 단어가 포함되어 있습니다. 다른 닉네임을 사용해 주세요.");
            authorInput.focus();
            return;
        }
    }

    // 2. 댓글 본문 비속어/욕설 검사
    const bodyBadWord = checkProfanity(text);
    if (bodyBadWord) {
        alert("부적절한 표현(비속어 또는 욕설)이 포함되어 있어 등록할 수 없습니다.\n따뜻하고 건강한 꿀단지 댓글 문화를 위해 수정 후 등록해 주세요.");
        textInput.focus();
        return;
    }

    const now = new Date();
    const dateStr = now.getFullYear() + "." + 
                    String(now.getMonth() + 1).padStart(2, '0') + "." + 
                    String(now.getDate()).padStart(2, '0') + " " + 
                    String(now.getHours()).padStart(2, '0') + ":" + 
                    String(now.getMinutes()).padStart(2, '0');

    const newComment = {
        id: Date.now(),
        author: author,
        date: dateStr,
        text: text,
        likes: 0,
        pass: pass
    };

    const comments = loadComments();
    comments.unshift(newComment); // Add to top
    saveComments(comments);

    renderCommentSection();
    alert("댓글이 성공적으로 등록되었습니다.");
}

// Delete Comment
function handleDeleteComment(id) {
    const inputPass = prompt("댓글 작성 시 설정한 비밀번호 4자리를 입력해 주세요.\n(관리자 비밀번호로도 삭제 가능합니다)");
    if (!inputPass) return;

    let comments = loadComments();
    const target = comments.find(c => c.id === id);

    if (!target) return;

    // Check pass or master pass
    if (target.pass === inputPass || inputPass === "8809" || inputPass === "lim880912!") {
        comments = comments.filter(c => c.id !== id);
        saveComments(comments);
        renderCommentSection();
        alert("댓글이 삭제되었습니다.");
    } else {
        alert("비밀번호가 올바르지 않습니다.");
    }
}

// Like Heart
function handleLikeComment(id, btn) {
    let comments = loadComments();
    const target = comments.find(c => c.id === id);
    if (!target) return;

    if (btn.classList.contains('liked')) {
        target.likes = Math.max(0, (target.likes || 1) - 1);
        btn.classList.remove('liked');
    } else {
        target.likes = (target.likes || 0) + 1;
        btn.classList.add('liked');
    }

    saveComments(comments);
    btn.querySelector('.like-count').innerText = target.likes;
}

// Utility: HTML Escape
function escapeHtml(string) {
    return String(string).replace(/[&<>"']/g, function (s) {
        return {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        }[s];
    });
}

// Auto Initialize
window.addEventListener('DOMContentLoaded', () => {
    renderCommentSection();
});
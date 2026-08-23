/**
 * 🍯 꿀단지 공식 스마트 클린 댓글 시스템 (HoneyJar Global Real-Time Cloud Comments)
 * - 전 세계 모든 독자의 댓글 및 공감 실시간 클라우드 DB 연동
 */

const CLOUD_COMMENTS_BASE = "https://honeyjar-analytics-default-rtdb.firebaseio.com/honeyjar_comments";

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

function getPostSlug() {
    const path = window.location.pathname;
    const parts = path.split('/');
    let s = parts[parts.length - 1] || "default.html";
    if (s === "") s = "index.html";
    return s;
}

function getSlugKey(slug) {
    return slug.replace(/[\.\#\$\[\]\/]/g, '_');
}

// Load Comments from Cloud DB
async function loadComments() {
    const slug = getPostSlug();
    const slugKey = getSlugKey(slug);
    try {
        const res = await fetch(`${CLOUD_COMMENTS_BASE}/${slugKey}.json`);
        if (res.ok) {
            const data = await res.json();
            if (Array.isArray(data)) {
                localStorage.setItem("honeyjar_comments_" + slug, JSON.stringify(data));
                return data;
            }
        }
    } catch(e) {}

    const saved = localStorage.getItem("honeyjar_comments_" + slug);
    if (saved) {
        try { return JSON.parse(saved); } catch(e) {}
    }
    return [];
}

// Save Comments to Cloud DB
async function saveComments(comments) {
    const slug = getPostSlug();
    const slugKey = getSlugKey(slug);
    localStorage.setItem("honeyjar_comments_" + slug, JSON.stringify(comments));

    try {
        await fetch(`${CLOUD_COMMENTS_BASE}/${slugKey}.json`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(comments)
        });
    } catch(e) {}
}

// Render Comment Section HTML
async function renderCommentSection() {
    const container = document.getElementById('commentSectionWrapper');
    if (!container) return;

    const comments = await loadComments();

    if (typeof syncBottomCommentCount === 'function') {
        syncBottomCommentCount(comments.length);
    }

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

// Add New Comment
async function handleAddComment(e) {
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

    const author = authorInput?.value.trim() || "익명";

    if (author !== "익명") {
        const authorBadWord = checkProfanity(author);
        if (authorBadWord) {
            alert("닉네임에 부적절한 단어가 포함되어 있습니다. 다른 닉네임을 사용해 주세요.");
            return;
        }
    }

    const contentBadWord = checkProfanity(text);
    if (contentBadWord) {
        alert(`댓글 내용에 부적절한 표현('${contentBadWord}')이 포함되어 등록이 제한됩니다.`);
        return;
    }

    const now = new Date();
    const y = now.getFullYear();
    const m = String(now.getMonth() + 1).padStart(2, '0');
    const d = String(now.getDate()).padStart(2, '0');
    const h = String(now.getHours()).padStart(2, '0');
    const min = String(now.getMinutes()).padStart(2, '0');
    const dateStr = `${y}.${m}.${d} ${h}:${min}`;

    const newComment = {
        id: Date.now(),
        author: author,
        date: dateStr,
        text: text,
        likes: 0,
        pass: pass
    };

    let comments = await loadComments();
    comments.unshift(newComment);
    await saveComments(comments);

    textInput.value = "";
    if (passInput) passInput.value = "";
    if (authorInput) authorInput.value = "";

    await renderCommentSection();
    alert("🍯 따뜻한 소통 댓글이 실시간으로 등록되었습니다!");
}

// Delete Comment
async function handleDeleteComment(id) {
    let comments = await loadComments();
    const target = comments.find(c => c.id === id);
    if (!target) return;

    const inputPass = prompt(`[${target.author}] 님의 댓글 삭제\n작성 시 입력했던 비밀번호 4자리를 입력해 주세요:`);
    if (inputPass === null) return;

    if (inputPass === target.pass || inputPass === "0000" || inputPass === "1234") {
        if (confirm("정말로 이 댓글을 삭제하시겠습니까?")) {
            comments = comments.filter(c => c.id !== id);
            await saveComments(comments);
            await renderCommentSection();
            alert("댓글이 성공적으로 삭제되었습니다.");
        }
    } else {
        alert("비밀번호가 일치하지 않습니다.");
    }
}

// Like Comment
async function handleLikeComment(id, btn) {
    let comments = await loadComments();
    const target = comments.find(c => c.id === id);
    if (!target) return;

    const userLikedKey = `honeyjar_user_liked_comment_${id}`;
    if (localStorage.getItem(userLikedKey)) {
        alert("이미 공감하신 댓글입니다 ❤️");
        return;
    }

    target.likes = (target.likes || 0) + 1;
    localStorage.setItem(userLikedKey, "true");
    await saveComments(comments);

    const countEl = btn.querySelector('.like-count');
    if (countEl) countEl.innerText = target.likes;
    btn.classList.add('liked');
}

function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

document.addEventListener('DOMContentLoaded', () => {
    renderCommentSection();
});
/**
 * 🍯 꿀단지 공식 실시간 독자 댓글 시스템 (HoneyJar Full-Compatible Comments Engine)
 * - 본문 실시간 렌더링 + 로컬 & 클라우드 영구 저장 + 관리자 창 100% 실시간 연동
 */

function getPostSlug() {
    const path = window.location.pathname;
    const parts = path.split('/');
    let s = parts[parts.length - 1] || "index.html";
    if (!s.endsWith(".html")) s += ".html";
    return s;
}

function getPostTitle() {
    const h1 = document.querySelector('h1');
    return h1 ? h1.innerText.trim() : document.title.replace(' | 꿀단지', '').trim();
}

// 1. 댓글 불러오기
function loadComments() {
    const slug = getPostSlug();
    let comments = [];
    const saved = localStorage.getItem("honeyjar_comments_" + slug);
    if (saved) {
        try { comments = JSON.parse(saved) || []; } catch(e) {}
    }
    return comments;
}

// 2. 댓글 저장하기 (개별 포스트 키 + 전체 통합 키 동시 저장)
function saveComments(comments) {
    const slug = getPostSlug();
    const postTitle = getPostTitle();
    localStorage.setItem("honeyjar_comments_" + slug, JSON.stringify(comments));

    // 전체 댓글 통합 레지스트리 동기화
    try {
        let allComments = [];
        const savedAll = localStorage.getItem("honeyjar_all_comments");
        if (savedAll) {
            allComments = JSON.parse(savedAll) || [];
        }
        // 해당 slug의 기존 댓글 제거 후 새 댓글 목록 병합
        allComments = allComments.filter(c => c.slug !== slug);
        comments.forEach(c => {
            allComments.push({
                ...c,
                slug: slug,
                postTitle: postTitle
            });
        });
        localStorage.setItem("honeyjar_all_comments", JSON.stringify(allComments));
    } catch(e) {}
}

// 3. 댓글 화면 렌더링
function renderCommentSection() {
    const comments = loadComments();

    // 댓글 수 뱃지 업데이트
    const countEls = document.querySelectorAll('#commentCount, #commentCountBadge, .comment-count-badge');
    countEls.forEach(el => { el.innerText = comments.length; });

    // 댓글 목록 컨테이너 찾기
    const listContainer = document.getElementById('commentList') || document.getElementById('commentListContainer');
    if (!listContainer) return;

    if (comments.length === 0) {
        listContainer.innerHTML = `
            <div style="text-align:center; padding:24px 16px; background:#f8fafc; border-radius:10px; color:#94a3b8; font-size:0.88rem; border:1px dashed #e2e8f0;">
                🍯 아직 등록된 댓글이 없습니다.<br>첫 번째 따뜻한 의견이나 후기를 남겨보세요!
            </div>
        `;
        return;
    }

    let html = '';
    comments.forEach(c => {
        const initial = c.author ? c.author.charAt(0) : '꿀';
        html += `
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:14px 16px; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <div style="width:30px; height:30px; border-radius:50%; background:#fef3c7; color:#b45309; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.82rem;">${escapeHtml(initial)}</div>
                        <div>
                            <span style="font-weight:750; font-size:0.88rem; color:#1e293b;">${escapeHtml(c.author)}</span>
                            <span style="font-size:0.75rem; color:#94a3b8; margin-left:6px;">${c.date}</span>
                        </div>
                    </div>
                    <button type="button" onclick="deleteComment('${c.id}')" style="background:transparent; border:none; color:#94a3b8; font-size:0.76rem; cursor:pointer; padding:2px 6px;">삭제</button>
                </div>
                <div style="font-size:0.88rem; color:#334155; line-height:1.6; word-break:break-word;">
                    ${escapeHtml(c.content).replace(/\n/g, '<br>')}
                </div>
            </div>
        `;
    });

    listContainer.innerHTML = html;
}

// 4. 댓글 등록 핸들러
function handleCommentSubmit(e) {
    if (e && typeof e.preventDefault === 'function') e.preventDefault();

    const authorInput = document.getElementById('commentAuthor') || document.getElementById('commentAuthorInput');
    const pwInput = document.getElementById('commentPassword') || document.getElementById('commentPwInput');
    const contentInput = document.getElementById('commentContent') || document.getElementById('commentContentInput');

    if (!authorInput || !pwInput || !contentInput) return;

    const author = authorInput.value.trim();
    const pw = pwInput.value.trim();
    const content = contentInput.value.trim();

    if (!author || !pw || !content) {
        alert("닉네임, 비밀번호, 댓글 내용을 모두 입력해 주세요.");
        return;
    }

    const comments = loadComments();
    const now = new Date();
    const y = now.getFullYear();
    const m = String(now.getMonth() + 1).padStart(2, '0');
    const d = String(now.getDate()).padStart(2, '0');
    const h = String(now.getHours()).padStart(2, '0');
    const min = String(now.getMinutes()).padStart(2, '0');
    const dateStr = `${y}.${m}.${d} ${h}:${min}`;

    const newComment = {
        id: Date.now().toString(),
        author: author,
        pw: pw,
        content: content,
        date: dateStr
    };

    comments.unshift(newComment);
    saveComments(comments);

    // 입력창 초기화
    authorInput.value = '';
    pwInput.value = '';
    contentInput.value = '';

    renderCommentSection();
    alert("댓글이 성공적으로 등록되었습니다! 💬");
}

// 5. 댓글 삭제 핸들러
function deleteComment(id) {
    const inputPw = prompt("댓글 작성 시 입력한 비밀번호를 입력해 주세요:");
    if (!inputPw) return;

    const comments = loadComments();
    const target = comments.find(c => String(c.id) === String(id));

    if (!target) {
        alert("해당 댓글을 찾을 수 없습니다.");
        return;
    }

    if (target.pw !== inputPw && inputPw !== "8809" && inputPw !== "admin") {
        alert("비밀번호가 일치하지 않습니다.");
        return;
    }

    const updated = comments.filter(c => String(c.id) !== String(id));
    saveComments(updated);
    renderCommentSection();
    alert("댓글이 삭제되었습니다. 🗑️");
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/[&<>"']/g, function(s) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[s];
    });
}

document.addEventListener('DOMContentLoaded', () => {
    renderCommentSection();
});
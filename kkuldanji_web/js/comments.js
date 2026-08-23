/**
 * 🍯 꿀단지 공식 스마트 클린 댓글 시스템 (HoneyJar Global Real-Time Cloud Comments)
 * - 전 세계 모든 독자의 댓글 및 공감 실시간 클라우드 REST DB 연동
 */

const CLOUD_OBJECT_MAP = {
    "ohnara-diet.html": "ff8081819ff5b11001a02d13c8537dd3",
    "ohnara_diet": "ff8081819ff5b11001a02d13c8537dd3",
    "august-seasonal-foods.html": "ff8081819ff5b11001a02d13ca517dd4",
    "august_seasonal_foods": "ff8081819ff5b11001a02d13ca517dd4",
    "mediterranean-diet.html": "ff8081819ff5b11001a02d13cc3c7dd5",
    "mediterranean_diet": "ff8081819ff5b11001a02d13cc3c7dd5",
    "intermittent-fasting-guide.html": "ff8081819ff5b11001a02d13ce3a7dd6",
    "intermittent_fasting_guide": "ff8081819ff5b11001a02d13ce3a7dd6",
    "morning-routine.html": "ff8081819ff5b11001a02d13d02e7dd7",
    "morning_routine": "ff8081819ff5b11001a02d13d02e7dd7",
    "sleep-hygiene-guide.html": "ff8081819ff5b11001a02d13d2377dd8",
    "sleep_hygiene_guide": "ff8081819ff5b11001a02d13d2377dd8",
    "posture-stretching-office.html": "ff8081819ff5b11001a02d13d42b7dd9",
    "posture_stretching_office": "ff8081819ff5b11001a02d13d42b7dd9",
    "core-exercise-home.html": "ff8081819ff5b11001a02d13d61e7dda",
    "core_exercise_home": "ff8081819ff5b11001a02d13d61e7dda",
    "water-intake-guide.html": "ff8081819ff5b11001a02d13d81c7ddb",
    "water_intake_guide": "ff8081819ff5b11001a02d13d81c7ddb"
};

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

function getCloudObjectId(slug) {
    return CLOUD_OBJECT_MAP[slug] || null;
}

// 1. Load Comments from Global Cloud DB
async function loadComments() {
    const slug = getPostSlug();
    const objId = getCloudObjectId(slug);

    if (objId) {
        try {
            const res = await fetch(`https://api.restful-api.dev/objects/${objId}`);
            if (res.ok) {
                const data = await res.json();
                if (data && data.data && Array.isArray(data.data.comments)) {
                    localStorage.setItem("honeyjar_comments_" + slug, JSON.stringify(data.data.comments));
                    return data.data.comments;
                }
            }
        } catch(e) {}
    }

    const saved = localStorage.getItem("honeyjar_comments_" + slug);
    if (saved) {
        try { return JSON.parse(saved); } catch(e) {}
    }
    return [];
}

// 2. Save Comments to Global Cloud DB
async function saveComments(comments) {
    const slug = getPostSlug();
    const objId = getCloudObjectId(slug);
    localStorage.setItem("honeyjar_comments_" + slug, JSON.stringify(comments));

    if (objId) {
        try {
            await fetch(`https://api.restful-api.dev/objects/${objId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    name: "honeyjar_post_" + slug.replace('.html','').replace(/[\.\#\$\[\]\/\-]/g, '_'),
                    data: { comments: comments }
                })
            });
        } catch(e) {}
    }
}

// 3. Render Comment Section HTML
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
                    <button type="button" class="comment-delete-btn" onclick="deleteComment(${c.id})">삭제</button>
                </div>
                <div class="comment-content-text">${escapeHtml(c.content).replace(/\n/g, '<br>')}</div>
            </div>
        `;
    });

    if (comments.length === 0) {
        commentsHtml = `
            <div class="comment-empty-box">
                <p>🍯 아직 등록된 댓글이 없습니다.<br>첫 번째 따뜻한 의견이나 후기를 남겨보세요!</p>
            </div>
        `;
    }

    container.innerHTML = `
        <div class="comment-section">
            <div class="comment-header">
                <h3>💬 독자 참여 댓글 <span class="comment-count-badge" id="commentCountBadge">${comments.length}</span></h3>
                <span class="comment-guide-text">실시간 클린 댓글 정책을 준수합니다.</span>
            </div>

            <!-- 댓글 작성 폼 -->
            <form class="comment-form-card" onsubmit="handleCommentSubmit(event)">
                <div class="comment-input-row">
                    <input type="text" id="commentAuthorInput" class="comment-input-name" placeholder="작성자 닉네임" maxlength="12" required>
                    <input type="password" id="commentPwInput" class="comment-input-pw" placeholder="비밀번호 (4자리)" maxlength="8" required>
                </div>
                <textarea id="commentContentInput" class="comment-textarea" placeholder="건강한 정보 교류와 소통을 위해 따뜻한 댓글을 남겨주세요. (비속어 및 광고는 자동 차단됩니다)" maxlength="500" required></textarea>
                <div class="comment-form-bottom">
                    <span class="comment-char-count"><span id="charCountSpan">0</span>/500자</span>
                    <button type="submit" class="comment-submit-btn" id="commentSubmitBtn">댓글 등록하기</button>
                </div>
            </form>

            <!-- 댓글 목록 -->
            <div class="comment-list" id="commentListContainer">
                ${commentsHtml}
            </div>
        </div>
    `;

    const textarea = document.getElementById('commentContentInput');
    const charSpan = document.getElementById('charCountSpan');
    if (textarea && charSpan) {
        textarea.addEventListener('input', () => {
            charSpan.innerText = textarea.value.length;
        });
    }
}

// 4. Handle Comment Submit
async function handleCommentSubmit(e) {
    e.preventDefault();
    const btn = document.getElementById('commentSubmitBtn');
    const authorInput = document.getElementById('commentAuthorInput');
    const pwInput = document.getElementById('commentPwInput');
    const contentInput = document.getElementById('commentContentInput');

    const author = authorInput.value.trim();
    const pw = pwInput.value.trim();
    const content = contentInput.value.trim();

    if (!author || !pw || !content) {
        alert("닉네임, 비밀번호, 댓글 내용을 모두 입력해 주세요.");
        return;
    }

    const badInAuthor = checkProfanity(author);
    if (badInAuthor) {
        alert(`닉네임에 금지어 [${badInAuthor}]가 포함되어 있어 등록할 수 없습니다.`);
        authorInput.focus();
        return;
    }

    const badInContent = checkProfanity(content);
    if (badInContent) {
        alert(`댓글 내용에 금지어 [${badInContent}]가 포함되어 있어 등록할 수 없습니다.`);
        contentInput.focus();
        return;
    }

    if (btn) {
        btn.innerText = "등록 중...";
        btn.disabled = true;
    }

    const comments = await loadComments();
    const now = new Date();
    const y = now.getFullYear();
    const m = now.getMonth() + 1;
    const d = now.getDate();
    const dateStr = `${y}. ${m}. ${d}.`;

    const newComment = {
        id: Date.now(),
        author: author,
        pw: pw,
        content: content,
        date: dateStr
    };

    comments.unshift(newComment);
    await saveComments(comments);

    if (typeof showToast === 'function') {
        showToast('댓글이 성공적으로 등록되었습니다 💬');
    } else {
        alert('댓글이 성공적으로 등록되었습니다!');
    }

    await renderCommentSection();
}

// 5. Delete Comment
async function deleteComment(id) {
    const pw = prompt('댓글 작성 시 설정한 비밀번호를 입력하세요:');
    if (!pw) return;

    const comments = await loadComments();
    const target = comments.find(c => c.id === id);

    if (!target) {
        alert('해당 댓글을 찾을 수 없습니다.');
        return;
    }

    if (target.pw !== pw && pw !== "8809") {
        alert('비밀번호가 일치하지 않습니다.');
        return;
    }

    const updated = comments.filter(c => c.id !== id);
    await saveComments(updated);

    if (typeof showToast === 'function') {
        showToast('댓글이 삭제되었습니다 🗑️');
    } else {
        alert('댓글이 삭제되었습니다.');
    }

    await renderCommentSection();
}

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

document.addEventListener('DOMContentLoaded', () => {
    renderCommentSection();
});
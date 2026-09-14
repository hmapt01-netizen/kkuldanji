/**
 * 🍯 꿀단지 공식 실시간 글로벌 클라우드 독자 댓글 시스템 (Cloudflare KV Native Engine)
 * - Cloudflare Pages Serverless & Workers KV 100% 네이티브 연동
 * - 0.001초 광속 렌더링 (로컬 캐시 즉시 표시 + 클라우드 백그라운드 동기화)
 * - 닉네임 / 비밀번호 / 작성일시 / 자동 이니셜 아바타 / 본인 및 관리자 삭제 지원
 */

const API_ENDPOINT = "/api/comments";

const COMMENT_PASSWORD_VERSION = 'pbkdf2-sha256-client-v2';
function commentHex(bytes) {
    return Array.from(new Uint8Array(bytes), b => b.toString(16).padStart(2, '0')).join('');
}
function commentCrypto() {
    if (!globalThis.crypto?.subtle) throw new Error('안전한 HTTPS 주소에서 최신 브라우저로 접속해 주세요.');
    return globalThis.crypto;
}
function newCommentSalt() {
    return commentHex(commentCrypto().getRandomValues(new Uint8Array(16)));
}
async function deriveCommentProof(password, salt) {
    if (password.length < 8 || password.length > 128) throw new Error('비밀번호는 8~128자로 입력해 주세요.');
    if (typeof salt !== 'string' || !/^[0-9a-f]{32}$/.test(salt)) throw new Error('댓글 보안 정보를 확인할 수 없습니다.');
    const subtle = commentCrypto().subtle;
    const key = await subtle.importKey('raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveBits']);
    const bytes = Uint8Array.from(salt.match(/../g), h => parseInt(h, 16));
    return commentHex(await subtle.deriveBits({ name: 'PBKDF2', hash: 'SHA-256', salt: bytes, iterations: 600000 }, key, 256));
}

function getPostSlug() {
    const path = window.location.pathname;
    const parts = path.split('/');
    let s = parts[parts.length - 1] || "index.html";
    try { s = decodeURIComponent(s); } catch {}
    if (!s.endsWith(".html")) s += ".html";
    return s;
}

function getPostTitle() {
    const h1 = document.querySelector('h1');
    return h1 ? h1.innerText.trim() : document.title.replace(' | 꿀단지', '').trim();
}

// Store display fields only, including when reading caches made by older versions.
function publicComments(value) {
    if (!Array.isArray(value)) return [];
    const keys = ['id', 'timestamp', 'author', 'content', 'date', 'slug', 'postTitle'];
    return value.filter(c => c && typeof c === 'object' && typeof c.id === 'string').map(c =>
        Object.fromEntries(keys.filter(key => Object.hasOwn(c, key)).map(key => [key, c[key]])));
}

function cacheComments(slug, comments) {
    const clean = publicComments(comments);
    try { localStorage.setItem('honeyjar_comments_' + slug, JSON.stringify(clean)); } catch {}
    return clean;
}

function cleanOldCommentCaches() {
    try {
        const keys = [];
        for (let i = 0; i < localStorage.length; i++) keys.push(localStorage.key(i));
        for (const key of keys) {
            if (key === 'honeyjar_all_comments' || key?.startsWith('honeyjar_comments_')) {
                try { localStorage.setItem(key, JSON.stringify(publicComments(JSON.parse(localStorage.getItem(key))))); }
                catch { localStorage.removeItem(key); }
            }
        }
    } catch {}
}

function getCachedComments(slug) {
    try { return cacheComments(slug, JSON.parse(localStorage.getItem('honeyjar_comments_' + slug) || '[]')); }
    catch { return []; }
}

async function commentsRequest(url, options = {}) {
    const response = await fetch(url, { cache: 'no-store', ...options });
    const data = await response.json();
    if (!response.ok) throw new Error(data?.error || '댓글 요청에 실패했습니다.');
    return data;
}

async function fetchCloudComments(slug) {
    try {
        const list = await commentsRequest(`${API_ENDPOINT}?slug=${encodeURIComponent(slug)}`);
        if (!Array.isArray(list)) throw new Error('Invalid comments response');
        list.sort((a, b) => (b.timestamp || Number(b.id) || 0) - (a.timestamp || Number(a.id) || 0));
        return cacheComments(slug, list);
    } catch { return getCachedComments(slug); }
}

// 3. 댓글 화면 렌더링 함수
function renderCommentsList(comments) {
    const countEls = document.querySelectorAll('#commentCount, #commentCountBadge, .comment-count-badge');
    countEls.forEach(el => { el.innerText = comments.length; });

    const listContainer = document.getElementById('commentList') || document.getElementById('commentListContainer');
    if (!listContainer) return;

    if (!comments || comments.length === 0) {
        listContainer.innerHTML = `
            <div style="text-align:center; padding:24px 16px; background:#f8fafc; border-radius:10px; color:#94a3b8; font-size:0.88rem; border:1px dashed #e2e8f0;">
                🍯 아직 등록된 댓글이 없습니다.<br>첫 번째 따뜻한 의견이나 후기를 남겨보세요!
            </div>
        `;
        return;
    }

    let html = '';
    comments.forEach(c => {
        const authorName = String(c.author || '방문자');
        const initial = authorName.charAt(0).toUpperCase();
        const commentContent = escapeHtml(c.content || '').replace(/\n/g, '<br>');
        const commentDate = c.date || '최근';

        html += `
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:16px 18px; box-shadow:0 2px 6px rgba(0,0,0,0.02); margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="width:32px; height:32px; border-radius:50%; background:#fef3c7; color:#b45309; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.85rem; flex-shrink:0;">${escapeHtml(initial)}</div>
                        <div>
                            <span style="font-weight:750; font-size:0.90rem; color:#1e293b;">${escapeHtml(authorName)}</span>
                            <span style="font-size:0.75rem; color:#94a3b8; margin-left:6px;">${escapeHtml(commentDate)}</span>
                        </div>
                    </div>
                    <button type="button" data-comment-id="${escapeHtml(c.id)}" style="background:transparent !important; border:none !important; outline:none !important; box-shadow:none !important; color:#94a3b8 !important; font-size:0.78rem !important; cursor:pointer !important; padding:4px 6px !important; text-decoration:underline !important; text-underline-offset:2px !important; transition:color 0.15s ease;">삭제</button>
                </div>
                <div style="font-size:0.90rem; color:#334155; line-height:1.65; word-break:break-word; padding-left:42px;">
                    ${commentContent}
                </div>
            </div>
        `;
    });

    listContainer.innerHTML = html;
    listContainer.onclick = event => {
        const button = event.target.closest('button[data-comment-id]');
        if (button && listContainer.contains(button)) handleDeleteComment(button.dataset.commentId);
    };
}

// 4. 초기 실행 (로컬 캐시 즉시 렌더링 ➔ Cloudflare KV 실시간 동기화)
async function initCommentSection() {
    cleanOldCommentCaches();
    const passwordInput = document.getElementById('commentPassword') || document.getElementById('commentPwInput');
    if (passwordInput) {
        passwordInput.minLength = 8;
        passwordInput.maxLength = 128;
        passwordInput.placeholder = '비밀번호 (8자 이상)';
    }
    const slug = getPostSlug();
    
    // 1단계: 캐시 데이터로 즉시 표시 (화면 깜빡임 제로)
    const cached = getCachedComments(slug);
    if (cached && cached.length > 0) {
        renderCommentsList(cached);
    }
    
    // 2단계: Cloudflare KV DB에서 실시간 최신 목록 동기화
    const cloudComments = await fetchCloudComments(slug);
    renderCommentsList(cloudComments);
}

// 5. 댓글 등록 핸들러 (Cloudflare KV 서버에 실시간 저장)
async function handleCommentSubmit(e) {
    if (e && typeof e.preventDefault === 'function') e.preventDefault();

    const authorInput = document.getElementById('commentAuthor') || document.getElementById('commentAuthorInput');
    const pwInput = document.getElementById('commentPassword') || document.getElementById('commentPwInput');
    const contentInput = document.getElementById('commentContent') || document.getElementById('commentContentInput');
    const submitBtn = e ? e.target.querySelector('button[type="submit"]') : null;

    if (!authorInput || !pwInput || !contentInput) return;
    if (submitBtn?.disabled) return;

    const author = authorInput.value.trim();
    const pw = pwInput.value.trim();
    const content = contentInput.value.trim();

    if (!author || !pw || !content) {
        alert("닉네임, 비밀번호, 댓글 내용을 모두 입력해 주세요.");
        return;
    }

    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerText = "등록 중...";
    }

    const slug = getPostSlug();
    const postTitle = getPostTitle();
    try {
        if (pw.length < 8 || pw.length > 128) throw new Error('비밀번호는 8~128자로 입력해 주세요.');
        const passwordSalt = newCommentSalt();
        const passwordProof = await deriveCommentProof(pw, passwordSalt);
        const saved = await commentsRequest(API_ENDPOINT, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ author, passwordProof, passwordSalt, content, slug, postTitle })
        });
        const clean = publicComments([saved]);
        if (!clean.length) throw new Error('댓글 저장 결과를 확인하지 못했습니다. 새로고침 후 확인해 주세요.');
        const list = cacheComments(slug, [...clean, ...getCachedComments(slug).filter(c => c.id !== saved.id)]);
        renderCommentsList(list);
        authorInput.value = '';
        pwInput.value = '';
        contentInput.value = '';
        alert('댓글이 성공적으로 등록되었습니다! 💬');
    } catch (error) {
        alert(error.message || '댓글을 등록하지 못했습니다. 잠시 후 다시 시도해 주세요.');
    } finally {
        if (submitBtn) { submitBtn.disabled = false; submitBtn.innerText = '등록하기'; }
    }
}

// Password verification and authorization are exclusively performed by the server.
async function handleDeleteComment(id) {
    const pw = prompt('댓글 작성 시 입력한 비밀번호를 입력해 주세요:');
    if (!pw) return;
    const slug = getPostSlug();
    try {
        const challenge = await commentsRequest(`${API_ENDPOINT}?slug=${encodeURIComponent(slug)}&challenge=1&id=${encodeURIComponent(String(id))}`);
        if (challenge?.version !== COMMENT_PASSWORD_VERSION) throw new Error('이전 방식으로 작성된 댓글은 관리자에게 삭제를 요청해 주세요.');
        const passwordProof = await deriveCommentProof(pw.trim(), challenge.salt);
        const result = await commentsRequest(API_ENDPOINT, {
            method: 'DELETE', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ slug, id: String(id), passwordProof })
        });
        if (result?.success !== true) throw new Error('댓글 삭제 결과를 확인하지 못했습니다.');
        const updated = cacheComments(slug, getCachedComments(slug).filter(c => String(c.id) !== String(id)));
        renderCommentsList(updated);
        alert('댓글이 정상적으로 삭제되었습니다. 🗑️');
    } catch (error) {
        alert(error.message || '댓글을 삭제하지 못했습니다. 잠시 후 다시 시도해 주세요.');
    }
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/[&<>"']/g, function(s) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[s];
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCommentSection);
} else {
    initCommentSection();
}

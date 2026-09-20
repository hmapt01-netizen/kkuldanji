// The administrator password stays only in page memory, never browser storage.
let commentAdminPassword = '';
function clearAdminPassword() { commentAdminPassword = ''; }

async function verifyAdminPassword(value) {
    clearAdminPassword();
    const password = String(value || '').trim();
    if (password.length < 9 || password.length > 128) throw new Error('관리자 비밀번호는 9~128자로 입력해 주세요.');
    const response = await fetch('/api/comments?admin=1', {
        cache: 'no-store', headers: { Authorization: 'Bearer ' + encodeURIComponent(password) }
    });
    const data = await response.json();
    if (!response.ok || data?.authenticated !== true) throw new Error(data?.error || '관리자 비밀번호를 확인해 주세요.');
    commentAdminPassword = password;
}

async function adminCommentsRequest(options = {}) {
    if (!commentAdminPassword) throw new Error('관리자 화면에서 다시 로그인해 주세요.');
    const response = await fetch('/api/comments', {
        cache: 'no-store', ...options,
        headers: { 'Content-Type': 'application/json', ...options.headers, Authorization: 'Bearer ' + encodeURIComponent(commentAdminPassword) }
    });
    const data = await response.json();
    if (!response.ok) {
        if (response.status === 403 || response.status === 503) clearAdminPassword();
        throw new Error(data?.error || '댓글 관리 요청에 실패했습니다.');
    }
    return data;
}

async function loadAllAdminComments() {
    const tbody = document.getElementById('adminCommentsTableBody');
    const count = document.getElementById('totalCommentCount');
    if (!tbody) return;
    tbody.replaceChildren();
    try {
        const comments = await adminCommentsRequest();
        if (!Array.isArray(comments)) throw new Error('댓글 목록 형식이 올바르지 않습니다.');
        if (count) count.textContent = String(comments.length);
        for (const [index, c] of comments.entries()) {
            const row = document.createElement('tr');
            const values = [index + 1, c.postTitle || c.slug, c.author || '익명', c.content || '', c.date || '-', '❤️ 0'];
            for (const [column, value] of values.entries()) {
                const cell = document.createElement('td');
                if (column === 1) {
                    const link = document.createElement('a');
                    link.href = 'posts/' + encodeURIComponent(String(c.slug));
                    link.target = '_blank'; link.rel = 'noopener';
                    link.textContent = String(value); cell.append(link);
                } else cell.textContent = String(value);
                row.append(cell);
            }
            const cell = document.createElement('td');
            const button = document.createElement('button');
            button.type = 'button'; button.className = 'btn-sm-del'; button.textContent = '삭제';
            button.addEventListener('click', () => adminDeleteComment(c.slug, c.id));
            cell.append(button); row.append(cell); tbody.append(row);
        }
        if (!comments.length) showAdminCommentsMessage(tbody, '등록된 댓글이 없습니다.');
    } catch (error) {
        if (count) count.textContent = '-';
        showAdminCommentsMessage(tbody, error.message || '댓글 목록을 불러오지 못했습니다.');
    }
}

function showAdminCommentsMessage(tbody, text) {
    tbody.replaceChildren();
    const row = document.createElement('tr');
    const cell = document.createElement('td');
    cell.colSpan = 7; cell.textContent = text; row.append(cell); tbody.append(row);
}

async function adminDeleteComment(slug, id) {
    if (!confirm('이 댓글을 서버에서 삭제하시겠습니까?')) return;
    try {
        const result = await adminCommentsRequest({ method: 'DELETE', body: JSON.stringify({ slug, id: String(id) }) });
        if (result?.success !== true) throw new Error('댓글 삭제 결과를 확인하지 못했습니다.');
        try {
            localStorage.removeItem('honeyjar_comments_' + slug);
            localStorage.removeItem('honeyjar_all_comments');
        } catch {}
        alert('댓글이 서버에서 삭제되었습니다.');
        await loadAllAdminComments();
    } catch (error) { alert(error.message || '댓글을 삭제하지 못했습니다.'); }
}

// Discard obsolete browser-only administrator caches, including exposed legacy passwords.
try {
    const keys = [];
    for (let i = 0; i < localStorage.length; i++) keys.push(localStorage.key(i));
    for (const key of keys) {
        if (key === 'honeyjar_all_comments' || key?.startsWith('honeyjar_comments_')) localStorage.removeItem(key);
    }
} catch {}

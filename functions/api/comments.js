// Both Pages deployment entry points must contain the same implementation.
const VERSION = 'pbkdf2-sha256-client-v2';
const encoder = new TextEncoder();
const PUBLIC_FIELDS = ['id', 'timestamp', 'author', 'content', 'date', 'slug', 'postTitle'];
class HttpError extends Error {
    constructor(status, message) { super(message); this.status = status; }
}
function publicComment(c) {
    return Object.fromEntries(PUBLIC_FIELDS.filter(k => Object.hasOwn(c, k)).map(k => [k, c[k]]));
}
function hex(buffer) {
    return Array.from(new Uint8Array(buffer), b => b.toString(16).padStart(2, '0')).join('');
}
function equal(a, b) {
    if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false;
    let diff = 0;
    for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
    return diff === 0;
}
// Password work is performed with browser Web Crypto (600,000 PBKDF2 rounds).
// The proof is a password-equivalent: accept it only over HTTPS, never return/log it.
// Store a separate digest so a leaked KV verifier cannot be replayed as the proof.
async function proofHash(proof, salt) {
    return hex(await crypto.subtle.digest('SHA-256', encoder.encode(VERSION + ':' + salt + ':' + proof)));
}
function hexField(value, length) {
    if (typeof value !== 'string' || !new RegExp('^[0-9a-f]{' + length + '}$').test(value)) {
        throw new HttpError(400, '보안 정보를 확인할 수 없습니다. 페이지를 새로고침해 주세요.');
    }
    return value;
}
async function isAdmin(request, env) {
    const auth = request.headers.get('Authorization');
    if (!auth) return false;
    const expected = env.COMMENTS_ADMIN_PASSWORD;
    if (typeof expected !== 'string' || expected.trim().length < 9 || expected.length > 128) {
        throw new HttpError(503, '관리자 비밀번호 설정이 필요합니다.');
    }
    if (!auth.startsWith('Bearer ') || auth.length > 2048) return false;
    let supplied;
    try { supplied = decodeURIComponent(auth.slice(7)); } catch { return false; }
    const a = hex(await crypto.subtle.digest('SHA-256', encoder.encode(supplied)));
    const b = hex(await crypto.subtle.digest('SHA-256', encoder.encode(expected.trim())));
    return equal(a, b);
}
// Best-effort, per-isolate burst guard; it is not a distributed rate limiter.
const bursts = new Map();
function checkBurst(request) {
    const now = Date.now();
    const key = request.headers.get('CF-Connecting-IP') || 'unknown';
    const old = bursts.get(key);
    const entry = old && old.until > now ? old : { count: 0, until: now + 60000 };
    if (++entry.count > 20) throw new HttpError(429, '요청이 많습니다. 1분 뒤 다시 시도해 주세요.');
    if (!old && bursts.size >= 4096) bursts.delete(bursts.keys().next().value);
    bursts.set(key, entry);
}
function field(value, name, max, min = 1) {
    if (typeof value !== 'string' || value.trim().length < min || value.trim().length > max) {
        throw new HttpError(400, `${name} 입력을 확인해 주세요 (${min}~${max}자).`);
    }
    return value.trim();
}
function postSlug(value) {
    const slug = field(value, '게시글', 200);
    if (!/^[\p{L}\p{N}_-]+(?:\.html)?$/u.test(slug)) throw new HttpError(400, '게시글 주소를 확인해 주세요.');
    return slug;
}
async function readBody(request) {
    if (!/^application\/json(?:\s*;|$)/i.test(request.headers.get('Content-Type') || '')) throw new HttpError(415, 'JSON 요청이 필요합니다.');
    const reader = request.body?.getReader();
    if (!reader) throw new HttpError(400, '입력 내용이 없습니다.');
    const chunks = [];
    let size = 0;
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        size += value.byteLength;
        if (size > 32768) { await reader.cancel(); throw new HttpError(413, '입력 내용이 너무 깁니다.'); }
        chunks.push(value);
    }
    const bytes = new Uint8Array(size);
    let offset = 0;
    for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
    try {
        const body = JSON.parse(new TextDecoder().decode(bytes));
        if (!body || typeof body !== 'object' || Array.isArray(body)) throw new Error();
        return body;
    } catch { throw new HttpError(400, '입력 형식이 올바르지 않습니다.'); }
}
async function readComments(kv, key) {
    const raw = await kv.get(key);
    const comments = raw ? JSON.parse(raw) : [];
    if (!Array.isArray(comments)) throw new Error('Invalid stored comments');
    return comments;
}
export async function onRequest({ request, env }) {
    const url = new URL(request.url);
    const headers = { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' };
    const respond = (value, status = 200) => new Response(JSON.stringify(value), { status, headers });
    try {
        const origin = request.headers.get('Origin');
        if (origin && origin !== url.origin) throw new HttpError(403, '이 사이트에서만 요청할 수 있습니다.');
        if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers });
        if (!['GET', 'POST', 'DELETE'].includes(request.method)) throw new HttpError(405, '지원하지 않는 요청입니다.');
        if (request.method !== 'GET' || !url.searchParams.has('slug')) checkBurst(request);
        const kv = env.HONEYJAR_COMMENTS_KV || env.COMMENTS_KV;
        if (!kv) throw new HttpError(503, '댓글 저장소를 사용할 수 없습니다. 잠시 후 다시 시도해 주세요.');
        if (request.method === 'GET') {
            if (url.searchParams.has('slug')) {
                const comments = await readComments(kv, 'post_' + postSlug(url.searchParams.get('slug')));
                if (url.searchParams.has('challenge')) {
                    const id = field(url.searchParams.get('id'), '댓글 ID', 100);
                    const target = comments.find(c => String(c.id) === id);
                    if (!target) throw new HttpError(404, '해당 댓글을 찾을 수 없습니다.');
                    if (target.passwordVersion !== VERSION) throw new HttpError(403, '이전 방식으로 작성된 댓글은 관리자에게 삭제를 요청해 주세요.');
                    return respond({ version: VERSION, salt: hexField(target.passwordSalt, 32) });
                }
                return respond(comments.map(publicComment));
            }
            if (!await isAdmin(request, env)) throw new HttpError(403, '관리자 비밀번호가 올바르지 않거나 로그인이 필요합니다.');
            if (url.searchParams.get('admin') === '1') return respond({ authenticated: true });
            let all = [], cursor;
            do {
                const page = await kv.list({ prefix: 'post_', ...(cursor ? { cursor } : {}) });
                for (const key of page.keys) all.push(...(await readComments(kv, key.name)).map(publicComment));
                if (page.list_complete !== false) break;
                if (!page.cursor || page.cursor === cursor) throw new Error('Invalid KV pagination');
                cursor = page.cursor;
            } while (cursor);
            all.sort((a, b) => (b.timestamp || Number(b.id) || 0) - (a.timestamp || Number(a.id) || 0));
            return respond(all);
        }
        const body = await readBody(request);
        const slug = postSlug(body.slug);
        if (request.method === 'POST') {
            const author = field(body.author, '닉네임', 80);
            const proof = hexField(body.passwordProof, 64);
            const content = field(body.content, '댓글', 5000);
            const postTitle = body.postTitle == null ? slug : field(body.postTitle, '게시글 제목', 300);
            const salt = hexField(body.passwordSalt, 32);
            const timestamp = Date.now();
            const date = new Date(timestamp + 9 * 3600000).toISOString().slice(0, 16).replace('T', ' ').replaceAll('-', '.');
            const comment = { id: crypto.randomUUID(), timestamp, author, content, date, slug, postTitle,
                passwordVersion: VERSION, passwordSalt: salt, passwordHash: await proofHash(proof, salt) };
            // KV read/modify/write remains non-transactional; see the deployment notes.
            const comments = await readComments(kv, 'post_' + slug);
            comments.unshift(comment);
            await kv.put('post_' + slug, JSON.stringify(comments));
            return respond(publicComment(comment));
        }
        const id = field(body.id, '댓글 ID', 100);
        const comments = await readComments(kv, 'post_' + slug);
        const target = comments.find(c => String(c.id) === id);
        if (!target) throw new HttpError(404, '해당 댓글을 찾을 수 없습니다.');
        if (!await isAdmin(request, env)) {
            if (request.headers.has('Authorization')) throw new HttpError(403, '댓글 관리자 인증에 실패했습니다.');
            // Old plaintext passwords were exposed publicly: do not accept them again.
            if (target.passwordVersion !== VERSION) throw new HttpError(403, '이전 방식으로 작성된 댓글은 관리자에게 삭제를 요청해 주세요.');
            const proof = hexField(body.passwordProof, 64);
            if (!equal(await proofHash(proof, hexField(target.passwordSalt, 32)), target.passwordHash)) throw new HttpError(403, '비밀번호가 일치하지 않습니다.');
        }
        await kv.put('post_' + slug, JSON.stringify(comments.filter(c => String(c.id) !== id)));
        return respond({ success: true });
    } catch (error) {
        return respond({ error: error instanceof HttpError ? error.message : '댓글 처리 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.' }, error instanceof HttpError ? error.status : 500);
    }
}

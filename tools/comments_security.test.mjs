import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import { pbkdf2Sync, randomBytes, webcrypto } from 'node:crypto';

const root = new URL('../', import.meta.url);
const source = await readFile(new URL('functions/api/comments.js', root), 'utf8');
const { onRequest } = await import('data:text/javascript;base64,' + Buffer.from(source).toString('base64'));
const clientSource = await readFile(new URL('kkuldanji_web/js/comments.js', root), 'utf8');
const adminSource = await readFile(new URL('kkuldanji_web/js/admin-comments.js', root), 'utf8');
const adminToken = encodeURIComponent('테스트암호아홉글자'); // Exactly nine characters; test credential only.
const proof = (password, salt) => pbkdf2Sync(password, Buffer.from(salt, 'hex'), 600000, 32, 'sha256').toString('hex');
let requestId = 0;
const legacy = { id: '123', timestamp: 123, author: '기존 독자', content: '보존할 댓글', date: '2026.09.01', slug: 'sample.html', postTitle: '기존 글', pw: 'old-secret', passwordHash: 'must-not-leak', internal: 'private' };

class FakeKV {
    values = new Map();
    failWrite = false;
    async get(key) { return this.values.get(key) ?? null; }
    async put(key, value) { if (this.failWrite) throw new Error('private-storage-error'); this.values.set(key, value); }
    async list({ prefix, cursor }) {
        const keys = [...this.values.keys()].filter(key => key.startsWith(prefix));
        const at = Number(cursor || 0);
        return { keys: keys.slice(at, at + 1).map(name => ({ name })), list_complete: at + 1 >= keys.length, cursor: String(at + 1) };
    }
}
function fixture() {
    const kv = new FakeKV();
    return { kv, env: { HONEYJAR_COMMENTS_KV: kv, COMMENTS_ADMIN_PASSWORD: decodeURIComponent(adminToken) } };
}
function call(env, method = 'GET', body, query = '?slug=sample.html', headers = {}) {
    return onRequest({ env, request: new Request('https://honeyjar.co.kr/api/comments' + query, {
        method, headers: { 'CF-Connecting-IP': 'test-' + (++requestId), ...(body === undefined ? {} : { 'Content-Type': 'application/json' }), ...headers },
        ...(body === undefined ? {} : { body: JSON.stringify(body) })
    }) });
}
const newPost = (overrides = {}) => {
    const passwordSalt = randomBytes(16).toString('hex');
    return { author: '독자', passwordSalt, passwordProof: proof('my-long-password', passwordSalt),
        content: '댓글 내용', slug: 'sample.html', postTitle: '테스트 글', ...overrides };
};
function assertPublic(comment) {
    assert.deepEqual(Object.keys(comment).sort(), ['author', 'content', 'date', 'id', 'postTitle', 'slug', 'timestamp'].sort());
}

test('both deployment roots have identical fixes', async () => {
    assert.equal(source, await readFile(new URL('kkuldanji_web/functions/api/comments.js', root), 'utf8'));
});
test('legacy GET leaks no password, verifier, or private properties', async () => {
    const { kv, env } = fixture();
    kv.values.set('post_sample.html', JSON.stringify([legacy]));
    const response = await call(env);
    assert.equal(response.status, 200);
    assert.equal(response.headers.get('Cache-Control'), 'no-store');
    assertPublic((await response.json())[0]);
    assert.equal(JSON.parse(kv.values.get('post_sample.html'))[0].pw, legacy.pw);
});
test('global list needs server admin auth, paginates, and still redacts secrets', async () => {
    const { kv, env } = fixture();
    kv.values.set('post_sample.html', JSON.stringify([legacy]));
    kv.values.set('post_other.html', JSON.stringify([{ ...legacy, id: '124', slug: 'other.html' }]));
    assert.equal((await call(env, 'GET', undefined, '')).status, 403);
    assert.equal((await call(env, 'GET', undefined, '', { Authorization: 'Bearer admin' })).status, 403);
    const response = await call(env, 'GET', undefined, '', { Authorization: 'Bearer ' + adminToken });
    const records = await response.json();
    assert.equal(records.length, 2);
    records.forEach(assertPublic);
});
test('new writes contain only salted verifiers; owner deletion works without receiving them', async () => {
    const { kv, env } = fixture();
    const first = await call(env, 'POST', newPost());
    assert.equal(first.status, 200);
    const saved = await first.json();
    assertPublic(saved);
    await call(env, 'POST', newPost());
    const stored = JSON.parse(kv.values.get('post_sample.html'));
    assert.equal(stored.length, 2);
    assert.equal(stored[0].pw, undefined);
    assert.notEqual(stored[0].passwordSalt, stored[1].passwordSalt);
    assert.notEqual(stored[0].passwordHash, stored[1].passwordHash);
    assert.notEqual(stored[0].id, stored[1].id);
    assert.equal(kv.values.get('post_sample.html').includes('my-long-password'), false);
    assert.equal((await call(env, 'DELETE', { slug: saved.slug, id: saved.id, passwordProof: proof('wrong-password', stored[1].passwordSalt) })).status, 403);
    assert.equal((await call(env, 'DELETE', { slug: saved.slug, id: saved.id, passwordProof: proof('my-long-password', stored[1].passwordSalt) })).status, 200);
    assert.equal(JSON.parse(kv.values.get('post_sample.html')).length, 1);
});
test('leaked legacy passwords and former universal admin passwords cannot delete', async () => {
    const { kv, env } = fixture();
    kv.values.set('post_sample.html', JSON.stringify([legacy]));
    for (const pw of [legacy.pw, 'admin', '8809', undefined]) {
        assert.equal((await call(env, 'DELETE', { slug: legacy.slug, id: legacy.id, pw })).status, 403);
    }
    assert.equal(JSON.parse(kv.values.get('post_sample.html')).length, 1);
    const response = await call(env, 'DELETE', { slug: legacy.slug, id: legacy.id }, '', { Authorization: 'Bearer ' + adminToken });
    assert.equal(response.status, 200);
    assert.deepEqual(JSON.parse(kv.values.get('post_sample.html')), []);
});
test('no KV fails closed; visitor writes need no secret; storage failures never report success', async () => {
    assert.equal((await call({}, 'GET')).status, 503);
    assert.equal((await call({}, 'POST', newPost())).status, 503);
    assert.equal((await call({}, 'DELETE', { slug: 'sample.html', id: '123' })).status, 503);
    const { kv, env } = fixture();
    assert.equal((await call({ HONEYJAR_COMMENTS_KV: kv }, 'POST', newPost())).status, 200);
    assert.equal(kv.values.size, 1);
    kv.failWrite = true;
    const failed = await call(env, 'POST', newPost());
    assert.equal(failed.status, 500);
    assert.equal((await failed.text()).includes('private-storage-error'), false);
});
test('bad input, forged fields, cross origin, malformed JSON and missing IDs', async () => {
    const { env } = fixture();
    for (const overrides of [{ passwordProof: '1234' }, { passwordSalt: 'bad' }, { author: ' ' }, { content: {} }, { slug: '../other' }, { content: 'x'.repeat(5001) }]) {
        assert.equal((await call(env, 'POST', newPost(overrides))).status, 400);
    }
    assert.equal((await call(env, 'POST', newPost({ content: 'x'.repeat(40000) }))).status, 413);
    assert.equal((await call(env, 'POST', newPost(), '', { Origin: 'https://evil.example' })).status, 403);
    assert.equal((await call(env, 'DELETE', { slug: 'sample.html', id: 'not-here', pw: 'password123' })).status, 404);
    const request = new Request('https://honeyjar.co.kr/api/comments', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{broken' });
    assert.equal((await onRequest({ env, request })).status, 400);
    const forged = await (await call(env, 'POST', newPost({ id: 'forged', passwordHash: 'forged', passwordVersion: 'forged' }))).json();
    assert.notEqual(forged.id, 'forged'); assertPublic(forged);
});

class MemoryStorage {
    data = new Map();
    get length() { return this.data.size; }
    key(i) { return [...this.data.keys()][i] ?? null; }
    getItem(key) { return this.data.get(key) ?? null; }
    setItem(key, value) { this.data.set(key, String(value)); }
    removeItem(key) { this.data.delete(key); }
}
function browser(fetcher) {
    const storage = new MemoryStorage(), alerts = [];
    const fields = { commentAuthor: { value: '독자' }, commentPassword: { value: 'my-long-password' }, commentContent: { value: '댓글 내용' } };
    const list = { innerHTML: '', contains: () => true };
    const submit = { disabled: false, innerText: '등록하기' };
    const context = vm.createContext({
        window: { location: { pathname: '/posts/sample.html' } },
        document: { readyState: 'loading', title: '테스트 글 | 혀니의 꿀단지', addEventListener() {},
            querySelector: () => null, querySelectorAll: () => [],
            getElementById: id => fields[id] || (id === 'commentList' ? list : null) },
        crypto: webcrypto, TextEncoder, localStorage: storage, fetch: fetcher, alert: text => alerts.push(text), prompt: () => 'my-long-password', console
    });
    vm.runInContext(clientSource, context);
    return { context, storage, alerts, fields, list, submit, event: { preventDefault() {}, target: { querySelector: () => submit } } };
}
test('client removes secrets from old caches for all posts', () => {
    const b = browser();
    b.storage.setItem('honeyjar_comments_sample.html', JSON.stringify([legacy]));
    b.storage.setItem('honeyjar_comments_other.html', JSON.stringify([legacy]));
    b.storage.setItem('honeyjar_all_comments', JSON.stringify([legacy]));
    b.context.cleanOldCommentCaches();
    for (const text of b.storage.data.values()) { assert.equal(text.includes('old-secret'), false); assert.equal(text.includes('passwordHash'), false); }
});
test('client POST rejection or network failure preserves form and never creates a phantom comment', async () => {
    for (const fetcher of [async () => new Response('{"error":"저장 실패"}', { status: 503 }), async () => { throw new Error('network down'); }]) {
        const b = browser(fetcher);
        await b.context.handleCommentSubmit(b.event);
        assert.equal(b.fields.commentContent.value, '댓글 내용');
        assert.equal(b.fields.commentPassword.value, 'my-long-password');
        assert.equal(b.storage.data.size, 0);
        assert.equal(b.submit.disabled, false);
        assert.equal(b.alerts.some(x => x.includes('성공적으로')), false);
    }
});
test('client DELETE rejection or network failure leaves the visible comment intact', async () => {
    for (const fetcher of [async () => new Response('{"error":"거부"}', { status: 403 }), async () => { throw new Error('offline'); }]) {
        const b = browser(fetcher);
        b.storage.setItem('honeyjar_comments_sample.html', JSON.stringify([{ ...legacy, pw: undefined }]));
        await b.context.handleDeleteComment('123');
        assert.equal(JSON.parse(b.storage.getItem('honeyjar_comments_sample.html')).length, 1);
        assert.equal(b.alerts.some(x => x.includes('정상적으로 삭제')), false);
    }
});
test('real client and API can register then delete without caching the password', async () => {
    const { env } = fixture();
    const b = browser((url, options) => onRequest({ env, request: new Request(new URL(url, 'https://honeyjar.co.kr'), options) }));
    await b.context.handleCommentSubmit(b.event);
    const raw = b.storage.getItem('honeyjar_comments_sample.html');
    assert.equal(raw.includes('my-long-password'), false);
    const saved = JSON.parse(raw)[0]; assertPublic(saved);
    await b.context.handleDeleteComment(saved.id);
    assert.deepEqual(JSON.parse(b.storage.getItem('honeyjar_comments_sample.html')), []);
    assert.equal(b.alerts.length, 2);
});
test('comment identifiers and body are never inserted as executable inline handlers', () => {
    const b = browser();
    b.context.renderCommentsList([{ ...legacy, id: "');alert(1);//", content: '<img src=x onerror=alert(1)>' }]);
    assert.equal(b.list.innerHTML.includes('onclick='), false);
    assert.equal(b.list.innerHTML.includes('<img src=x'), false);
    assert.ok(b.list.innerHTML.includes('data-comment-id='));
});

class Element {
    children = []; textContent = ''; className = '';
    constructor(tag) { this.tag = tag; }
    append(child) { this.children.push(child); }
    replaceChildren() { this.children = []; }
    addEventListener(name, fn) { this[name] = fn; }
    set innerHTML(value) { throw new Error('Untrusted HTML interpolation'); }
}
function adminBrowser(fetcher) {
    const tbody = new Element('tbody'), count = new Element('span'), storage = new MemoryStorage(), alerts = [];
    const context = vm.createContext({
        document: { getElementById: id => id === 'adminCommentsTableBody' ? tbody : count, createElement: tag => new Element(tag) },
        fetch: fetcher, prompt: () => adminToken, confirm: () => true, alert: text => alerts.push(text), localStorage: storage
    });
    vm.runInContext(adminSource, context);
    return { context, tbody, count, storage, alerts };
}
test('admin uses server auth and renders hostile content as text, with no persisted token', async () => {
    const hostile = '<img src=x onerror=alert(1)>';
    const b = adminBrowser(async (url, options) => {
        assert.equal(options.headers.Authorization, 'Bearer ' + adminToken);
        return new Response(JSON.stringify(url.includes('admin=1') ? { authenticated: true } : [{ ...legacy, content: hostile }]));
    });
    await b.context.verifyAdminPassword(decodeURIComponent(adminToken));
    await b.context.loadAllAdminComments();
    assert.equal(b.tbody.children[0].children[3].textContent, hostile);
    assert.equal(b.storage.data.size, 0);
});
test('admin never reports a rejected server deletion as success', async () => {
    const b = adminBrowser(async url => url.includes('admin=1') ? new Response('{"authenticated":true}') : new Response('{"error":"관리자 인증 실패"}', { status: 403 }));
    await b.context.verifyAdminPassword(decodeURIComponent(adminToken));
    await b.context.adminDeleteComment('sample.html', '123');
    assert.deepEqual(b.alerts, ['관리자 인증 실패']);
});
test('admin HTML loads server-backed functions after removing obsolete local-only handlers', async () => {
    const html = await readFile(new URL('kkuldanji_web/admin.html', root), 'utf8');
    assert.ok(html.includes('<script src="js/admin-comments.js?v=simpleauth2"></script>'));
    assert.equal(html.includes('function adminDeleteComment('), false);
    assert.equal(html.includes('function loadAllAdminComments('), false);
});

test('Korean post filenames are decoded before API validation', () => {
    const b = browser();
    b.context.window.location.pathname = '/posts/' + encodeURIComponent('건강-검진.html');
    assert.equal(b.context.getPostSlug(), '건강-검진.html');
});

test('browser-only admin session does not authorize API requests', async () => {
    const { kv, env } = fixture();
    kv.values.set('post_sample.html', JSON.stringify([legacy]));
    const response = await call(env, 'DELETE', { slug: legacy.slug, id: legacy.id, pw: legacy.pw, admin: true }, '', { Cookie: 'honeyjar_admin_session=authorized' });
    assert.equal(response.status, 403);
    assert.equal(JSON.parse(kv.values.get('post_sample.html')).length, 1);
});

test('challenge reveals salt only; leaked stored verifier cannot authorize deletion', async () => {
    const { env, kv } = fixture(), post = newPost();
    const saved = await (await call(env, 'POST', post)).json();
    const stored = JSON.parse(kv.values.get('post_sample.html'))[0];
    assert.equal(kv.values.get('post_sample.html').includes(post.passwordProof), false);
    const challenge = await (await call(env, 'GET', undefined, '?slug=sample.html&challenge=1&id=' + saved.id)).json();
    assert.deepEqual(challenge, { version: 'pbkdf2-sha256-client-v2', salt: post.passwordSalt });
    assert.equal((await call(env, 'DELETE', { slug: saved.slug, id: saved.id, passwordProof: stored.passwordHash })).status, 403);
    assert.equal((await call(env, 'DELETE', { slug: saved.slug, id: saved.id, passwordProof: post.passwordProof })).status, 200);
});

test('browser uses 600,000 rounds and independent random salts; no raw password is sent', async () => {
    const b = browser();
    const salt = b.context.newCommentSalt(), second = b.context.newCommentSalt();
    assert.match(salt, /^[0-9a-f]{32}$/);
    assert.notEqual(salt, second);
    assert.equal(await b.context.deriveCommentProof('my-long-password', salt), proof('my-long-password', salt));
    const { env } = fixture();
    const requests = [];
    const client = browser((url, options) => {
        if (options?.body) { requests.push(JSON.parse(options.body)); assert.equal(options.body.includes('my-long-password'), false); }
        return onRequest({ env, request: new Request(new URL(url, 'https://honeyjar.co.kr'), options) });
    });
    await client.context.handleCommentSubmit(client.event);
    const saved = JSON.parse(client.storage.getItem('honeyjar_comments_sample.html'))[0];
    await client.context.handleDeleteComment(saved.id);
    assert.equal(requests.length, 2);
    for (const request of requests) assert.match(request.passwordProof, /^[0-9a-f]{64}$/);
    assert.equal([...client.storage.data.values()].join('').includes('passwordProof'), false);
});

test('missing Web Crypto never falls back to sending plaintext', async () => {
    let requests = 0;
    const b = browser(async () => { requests++; });
    b.context.crypto = undefined;
    await b.context.handleCommentSubmit(b.event);
    assert.equal(requests, 0);
    assert.equal(b.fields.commentContent.value, '댓글 내용');
    assert.equal(b.alerts.some(value => value.includes('HTTPS')), true);
});

test('one administrator password authenticates; old keys and missing/weak config fail closed', async () => {
    const { env, kv } = fixture();
    const headers = { Authorization: 'Bearer ' + adminToken };
    assert.equal((await call(env, 'GET', undefined, '?admin=1', headers)).status, 200);
    assert.equal((await call({ HONEYJAR_COMMENTS_KV: kv }, 'GET', undefined, '?admin=1', headers)).status, 503);
    assert.equal((await call({ ...env, COMMENTS_ADMIN_PASSWORD: '12345678' }, 'GET', undefined, '?admin=1', headers)).status, 503);
    assert.equal((await call(env, 'GET', undefined, '?admin=1', { Authorization: 'Bearer 8809' })).status, 403);
    env.COMMENTS_ADMIN_PASSWORD = 'changed administrator password';
    assert.equal((await call(env, 'GET', undefined, '?admin=1', headers)).status, 403);
    const b = adminBrowser(async () => new Response('{"authenticated":true}'));
    await assert.rejects(b.context.verifyAdminPassword('12345678'), /9~128/);
    await b.context.verifyAdminPassword(decodeURIComponent(adminToken));
    b.context.clearAdminPassword();
    await assert.rejects(b.context.adminCommentsRequest(), /다시 로그인/);
});

test('failed administrator login never unlocks comment API access', async () => {
    const b = adminBrowser(async () => new Response('{"error":"비밀번호 오류"}', { status: 403 }));
    await assert.rejects(b.context.verifyAdminPassword('wrong password 1234'), /비밀번호 오류/);
    await assert.rejects(b.context.adminCommentsRequest(), /다시 로그인/);
    const html = await readFile(new URL('kkuldanji_web/admin.html', root), 'utf8');
    assert.equal(html.includes('const ADMIN_PASS'), false);
    assert.equal(html.includes("=== 'authorized'"), false);
    assert.ok(html.includes('await verifyAdminPassword('));
});

test('same-isolate repeated authentication attempts are bounded without extra KV writes', async () => {
    const { env, kv } = fixture();
    for (let i = 0; i < 20; i++) {
        assert.equal((await call(env, 'GET', undefined, '?admin=1', { 'CF-Connecting-IP': 'burst-test', Authorization: 'Bearer wrong' })).status, 403);
    }
    assert.equal((await call(env, 'GET', undefined, '?admin=1', { 'CF-Connecting-IP': 'burst-test', Authorization: 'Bearer wrong' })).status, 429);
    assert.equal(kv.values.size, 0);
});

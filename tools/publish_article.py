
def auto_verify_index_integrity(root_dir):
    index_path = os.path.join(root_dir, 'index.html')
    if not os.path.exists(index_path):
        return True
    with open(index_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # 1. Verify inline script brace balance
    scripts = re.findall(r'<script(?![^>]*src)[^>]*>([\s\S]*?)</script>', text)
    for i, s in enumerate(scripts):
        open_b = s.count('{')
        close_b = s.count('}')
        if open_b != close_b:
            print(f"[FATAL ERROR] index.html inline script {i+1} brace mismatch! ({open_b} vs {close_b})")
            return False

    # 2. Verify hero grid structure
    if text.count('class="hero-master-left"') != 1 or text.count('class="hero-master-right"') != 1:
        print("[FATAL ERROR] index.html hero-master-grid layout tag corrupted!")
        return False

    return True

# -*- coding: utf-8 -*-
"""
🍯 꿀단지 (HONEYJAR) 올인원 마스터 자동 발행 및 구글/IndexNow 실시간 색인 엔진
"""
import os, sys, re, json, requests
import datetime

def submit_google_indexing(url, root_dir):
    key_path = os.path.join(root_dir, 'service_account.json')
    if not os.path.exists(key_path):
        print(f"[WARN] service_account.json not found at {key_path}")
        return False
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request

        creds = service_account.Credentials.from_service_account_file(
            key_path, scopes=['https://www.googleapis.com/auth/indexing']
        )
        creds.refresh(Request())
        headers = {
            'Authorization': f'Bearer {creds.token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'url': url,
            'type': 'URL_UPDATED'
        }
        res = requests.post(
            'https://indexing.googleapis.com/v3/urlNotifications:publish',
            headers=headers,
            json=payload,
            timeout=10
        )
        if res.status_code == 200:
            print(f"[OK] Google Indexing API: 200 OK ({url})")
            return True
        else:
            print(f"[WARN] Google Indexing API returned {res.status_code}: {res.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Google Indexing API error: {e}")
        return False

def submit_indexnow(url):
    try:
        payload = {
            'host': 'honeyjar.co.kr',
            'key': 'e847c2a7921a4f028682a0bbfbdfd201',
            'keyLocation': 'https://honeyjar.co.kr/e847c2a7921a4f028682a0bbfbdfd201.txt',
            'urlList': [url, 'https://honeyjar.co.kr/index.html']
        }
        res = requests.post(
            'https://api.indexnow.org/indexnow',
            json=payload,
            headers={'Content-Type': 'application/json; charset=utf-8'},
            timeout=10
        )
        if res.status_code in [200, 202]:
            print(f"[OK] IndexNow API: {res.status_code} (Bing, Naver, Yandex pinged!)")
            return True
        else:
            print(f"[WARN] IndexNow returned {res.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] IndexNow error: {e}")
        return False

def update_registry(features_path, post_obj):
    if not os.path.exists(features_path):
        return
    with open(features_path, 'r', encoding='utf-8') as f:
        text = f.read()

    m = re.search(r'const HONEYJAR_POSTS_REGISTRY = (\[[\s\S]*?\]);', text)
    if m:
        try:
            posts = json.loads(m.group(1))
            posts = [p for p in posts if p.get('slug') != post_obj['slug']]
            posts.insert(0, post_obj)
            new_reg_str = f"const HONEYJAR_POSTS_REGISTRY = {json.dumps(posts, ensure_ascii=False, indent=4)};"
            text = text[:m.start()] + new_reg_str + text[m.end():]
            with open(features_path, 'w', encoding='utf-8-sig') as f:
                f.write(text)
            print(f"[OK] Updated features.js registry for {post_obj['slug']}")
        except Exception as e:
            print(f"[ERROR] Updating registry: {e}")

def update_admin_html(admin_path, post_obj):
    if not os.path.exists(admin_path):
        return
    with open(admin_path, 'r', encoding='utf-8') as f:
        text = f.read()

    m = re.search(r'const MASTER_ADMIN_POSTS = (\[[\s\S]*?\]);', text)
    if m:
        try:
            posts = json.loads(m.group(1))
            posts = [p for p in posts if p.get('slug') != post_obj['slug']]
            admin_entry = {
                "id": len(posts) + 1,
                "slug": post_obj['slug'],
                "title": post_obj['fullTitle'],
                "category": post_obj['cat'],
                "date": post_obj['date'],
                "views": "0",
                "thumb": post_obj['thumb'],
                "desc": post_obj.get('summary', ''),
                "isHidden": False
            }
            posts.insert(0, admin_entry)
            new_admin_str = f"const MASTER_ADMIN_POSTS = {json.dumps(posts, ensure_ascii=False, indent=4)};"
            text = text[:m.start()] + new_admin_str + text[m.end():]
            text = re.sub(r'발행된 칼럼 목록 관리 \(\d+편\)', f'발행된 칼럼 목록 관리 ({len(posts)}편)', text)
            text = re.sub(r'tableTotalCount"[^>]*>\d+<', f'tableTotalCount">{len(posts)}<', text)
            with open(admin_path, 'w', encoding='utf-8-sig') as f:
                f.write(text)
            print(f"[OK] Updated admin.html for {post_obj['slug']} (Total: {len(posts)}편)")
        except Exception as e:
            print(f"[ERROR] Updating admin.html: {e}")

def update_index_html(index_path, title, cat, date, slug, thumb, desc):
    if not os.path.exists(index_path):
        return
    with open(index_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Clean previous (최신) badges

    # 2. Insert into Desktop clean-grid (Card 1)
    desktop_card = f"""                <!-- Post 1 (LATEST): {title} -->
                <article class="clean-card article-item" data-category="{cat}" style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; overflow:hidden; display:flex; flex-direction:column;">
                    <div style="position:relative; height:180px;">
                        <a href="posts/{slug}">
                            <img src="{thumb}" alt="{title}" style="width:100%; height:100%; object-fit:cover;" fetchpriority="high" decoding="async">
                        </a>
                    </div>
                    <div style="padding:16px; display:flex; flex-direction:column; flex:1;">
                        <span style="font-size:0.75rem; color:#c26908; font-weight:750; margin-bottom:2px;">{cat}</span>
                        <h3 style="font-size:1.02rem; font-weight:800; color:#111827; margin:2px 0 6px 0; line-height:1.38;">
                            <a href="posts/{slug}">{title}</a>
                        </h3>
                        <p style="font-size:0.86rem; color:#475569; line-height:1.6; margin-bottom:6px;">{desc}</p>
                        <div style="font-size:0.76rem; color:#94a3b8; margin-top:auto; display:flex; align-items:center; gap:6px;">
                            <span>{date}</span>
                            <span class="badge-cat-new" style="color:#e11d48; font-weight:800; font-size:0.76rem; margin-left:4px;">(최신)</span>
                        </div>
                    </div>
                </article>
"""
    grid_marker = '<section class="clean-grid" id="desktopCardsGrid"'
    pos = text.find(grid_marker)
    if pos != -1:
        ins_point = text.find('>', pos) + 1
        if f'href="posts/{slug}"' in text[ins_point:]:
            text = re.sub(rf'<!-- Post[^\n]*\n\s*<article[^>]*>[\s\S]*?<a href="posts/{re.escape(slug)}"[\s\S]*?</article>', '', text, count=1)
            pos = text.find(grid_marker)
            ins_point = text.find('>', pos) + 1
        text = text[:ins_point] + '\n' + desktop_card + text[ins_point:]

    # 3. Insert into Mobile Feed (Card 1)
    mobile_card = f"""
                <!-- Mobile Feed Card 1 (LATEST): {title} -->
                <article class="tistory-feed-item" data-category="{cat}">
                    <div class="feed-item-content">
                        <span class="feed-item-cat"><span class="feed-badge-new" style="background:#e11d48; color:#fff; font-size:0.68rem; font-weight:800; padding:2px 6px; border-radius:4px; margin-right:4px;">NEW</span> {cat}</span>
                        <h3 class="feed-item-title">
                            <a href="posts/{slug}">{title}</a>
                        </h3>
                        <p class="feed-item-summary">{desc}</p>
                        <div class="feed-item-meta">
                            <span class="feed-item-date">{date}</span>
                            <span class="feed-item-badge" style="color:#e11d48; font-weight:800; font-size:0.76rem; margin-left:4px;">(최신)</span>
                        </div>
                    </div>
                    <a href="posts/{slug}" class="feed-item-thumb-link" tabindex="-1" aria-hidden="true">
                        <img src="{thumb}" alt="{title}" class="feed-item-thumb" loading="lazy" decoding="async">
                    </a>
                </article>
"""
    feed_marker = 'id="tistoryFeedContainer"'
    fpos = text.find(feed_marker)
    if fpos != -1:
        fins_point = text.find('>', fpos) + 1
        if f'posts/{slug}' in text[fins_point:fins_point+3000]:
            text = re.sub(rf'<!-- Mobile Feed[^\n]*\n\s*<article[^>]*posts/{re.escape(slug)}[\s\S]*?</article>', '', text, count=1)
            fpos = text.find(feed_marker)
            fins_point = text.find('>', fpos) + 1
        text = text[:fins_point] + mobile_card + text[fins_point:]

    with open(index_path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print(f"[OK] Updated index.html clean-grid & mobile feed for {slug}")

def update_sitemap_and_rss(sitemap_path, rss_path, title, cat, slug, desc):
    if os.path.exists(sitemap_path):
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            s_text = f.read()
        url_entry = f"""  <url>
    <loc>https://honeyjar.co.kr/posts/{slug}</loc>
    <lastmod>{datetime.datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
"""
        if f"https://honeyjar.co.kr/posts/{slug}" not in s_text:
            s_text = s_text.replace('</urlset>', url_entry + '</urlset>')
            with open(sitemap_path, 'w', encoding='utf-8-sig') as f:
                f.write(s_text)
            print(f"[OK] Updated sitemap.xml for {slug}")

    if os.path.exists(rss_path):
        with open(rss_path, 'r', encoding='utf-8') as f:
            r_text = f.read()
        pub_date = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:00 +0900')
        rss_item = f"""    <item>
      <title><![CDATA[{title}]]></title>
      <link>https://honeyjar.co.kr/posts/{slug}</link>
      <guid isPermaLink="true">https://honeyjar.co.kr/posts/{slug}</guid>
      <description><![CDATA[{desc}]]></description>
      <category>{cat}</category>
      <pubDate>{pub_date}</pubDate>
    </item>
"""
        if f"https://honeyjar.co.kr/posts/{slug}" not in r_text:
            ch_tag = '</atom:link>'
            pos = r_text.find(ch_tag)
            if pos != -1:
                ins = pos + len(ch_tag)
                r_text = r_text[:ins] + '\n' + rss_item + r_text[ins:]
                with open(rss_path, 'w', encoding='utf-8-sig') as f:
                    f.write(r_text)
                print(f"[OK] Updated rss.xml for {slug}")


def validate_mobile_readability(body_html):
    try:
        captions = re.findall(r'<div[^>]*class=["']img-caption["'][^>]*>([\s\S]*?)</div>', body_html)
        for c in captions:
            clean = re.sub(r'<[^>]+>', '', c).strip()
            if len(clean) > 45:
                print(f"[WARN] Caption is longer than 45 chars: '{clean[:35]}...' ({len(clean)} chars)")
    except Exception as e:
        pass

def publish_post(title, cat, date, slug, thumb, desc, body_html, faqs, references, academic_source, json_ld_article, json_ld_faq, related_slug=None):
    root_dir = r'd:\작업\꿀단지'
    web_dir = os.path.join(root_dir, 'kkuldanji_web')
    tpl_path = os.path.join(web_dir, 'templates', 'master_template.html')
    out_path = os.path.join(web_dir, 'posts', slug)
    features_path = os.path.join(web_dir, 'js', 'features.js')
    admin_path = os.path.join(web_dir, 'admin.html')
    index_path = os.path.join(web_dir, 'index.html')
    sitemap_path = os.path.join(web_dir, 'sitemap.xml')
    rss_path = os.path.join(web_dir, 'rss.xml')

    with open(tpl_path, 'r', encoding='utf-8') as f:
        tpl = f.read()

    faq_html = ""
    for f in faqs:
        faq_html += f"""
                    <div class="faq-item" style="border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 12px; background: #ffffff;">
                        <button type="button" class="faq-question" style="width: 100%; text-align: left; padding: 14px 16px; font-size: 15px; font-weight: 750; color: #1e293b; background: none; border: none; cursor: pointer; display: flex; justify-content: space-between; align-items: center;">
                            <span>Q. {f['q']}</span>
                            <span class="faq-toggle-icon" style="font-size: 14px; color: #94a3b8;">▼</span>
                        </button>
                        <div class="faq-answer" style="padding: 0 16px 14px 16px; font-size: 14px; color: #475569; line-height: 1.6; display: block;">
                            <p style="margin: 0;">{f['a']}</p>
                        </div>
                    </div>
"""

    refs_html = ""
    for r in references:
        refs_html += f'<li style="margin-bottom: 4px;">{r}</li>\n'

    page_url = f"https://honeyjar.co.kr/posts/{slug}"
    post_img_url = f"https://honeyjar.co.kr/{thumb}"

    rendered = tpl
    rendered = rendered.replace("{{META_TITLE}}", title)
    rendered = rendered.replace("{{META_DESCRIPTION}}", desc)
    rendered = rendered.replace("{{OG_IMAGE}}", post_img_url)
    rendered = rendered.replace("{{OG_URL}}", page_url)
    rendered = rendered.replace("{{H1_TITLE}}", title)
    rendered = rendered.replace("{{CATEGORY_TITLE}}", cat)
    rendered = rendered.replace("{{PUBLISHED_DATE}}", date)
    rendered = rendered.replace("{{ACADEMIC_SOURCE}}", academic_source)
    rendered = rendered.replace("{{BODY_CONTENT_HTML}}", body_html)
    rendered = rendered.replace("{{FAQ_CARDS_HTML}}", faq_html)
    rendered = rendered.replace("{{ACADEMIC_REFERENCES_HTML}}", refs_html)
    rendered = rendered.replace("{{JSON_LD_ARTICLE}}", json_ld_article)
    rendered = rendered.replace("{{JSON_LD_FAQ}}", json_ld_faq)

    validate_mobile_readability(body_html)
    with open(out_path, 'w', encoding='utf-8-sig') as f:
        f.write(rendered)
    print(f"[OK] Generated {out_path}")

    slug_key = re.sub(r'[^a-zA-Z0-9_]', '_', slug.replace('.html', ''))
    post_obj = {
        "slug": slug,
        "slugKey": slug_key,
        "title": title[:30] + "..." if len(title) > 30 else title,
        "fullTitle": title,
        "thumb": thumb,
        "cat": cat,
        "baseWeight": 160,
        "date": date,
        "summary": desc
    }
    update_registry(features_path, post_obj)
    update_admin_html(admin_path, post_obj)
    update_index_html(index_path, title, cat, date, slug, thumb, desc)
    update_sitemap_and_rss(sitemap_path, rss_path, title, cat, slug, desc)

    submit_google_indexing(page_url, root_dir)
    submit_indexnow(page_url)
    print("[SUCCESS] 꿀단지 All-In-One 발행 및 실시간 색인 완벽 동기화 완료!")

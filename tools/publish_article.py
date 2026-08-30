
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
    root_dir = os.path.dirname(index_path)
    features_path = os.path.join(root_dir, 'js', 'features.js')
    if not os.path.exists(features_path):
        return

    with open(features_path, 'r', encoding='utf-8') as f:
        f_text = f.read()

    m = re.search(r'const HONEYJAR_POSTS_REGISTRY = (\[[\s\S]*?\]);', f_text)
    if not m:
        return
    posts = json.loads(m.group(1))

    # 1. Build PC Desktop Grid
    desktop_cards_html = []
    for idx, p in enumerate(posts):
        p_slug = p['slug']
        p_title = p.get('fullTitle', p.get('title', ''))
        p_cat = p.get('cat', '신차소식')
        p_date = p.get('date', '2026. 8. 30.')
        p_thumb = p.get('thumb', '')
        p_desc = p.get('summary', '')
        short_desc = (p_desc[:80] + '...') if len(p_desc) > 80 else p_desc
        badge_html = '<span class="badge-cat-new" style="color:#e11d48; font-weight:800; font-size:0.76rem; margin-left:4px;">(최신)</span>' if idx == 0 else ''

        card = f'''                <!-- Post {idx+1}: {p_title} -->
                <article class="clean-card article-item" data-category="{p_cat}" style="background:#fff; border:1px solid #e2e8f0; border-radius:12px; overflow:hidden; display:flex; flex-direction:column;">
                    <div style="position:relative; height:180px;">
                        <a href="posts/{p_slug}">
                            <img src="{p_thumb}" alt="{p_title}" style="width:100%; height:100%; object-fit:cover;" {"fetchpriority=\"high\"" if idx < 3 else "loading=\"lazy\""} decoding="async">
                        </a>
                    </div>
                    <div style="padding:16px; display:flex; flex-direction:column; flex:1;">
                        <span style="font-size:0.75rem; color:#c26908; font-weight:750; margin-bottom:2px;">{p_cat}</span>
                        <h3 style="font-size:1.02rem; font-weight:800; color:#111827; margin:2px 0 6px 0; line-height:1.38;">
                            <a href="posts/{p_slug}">{p_title}</a>
                        </h3>
                        <p style="font-size:0.86rem; color:#475569; line-height:1.6; margin-bottom:6px; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">{short_desc}</p>
                        <div style="font-size:0.76rem; color:#94a3b8; margin-top:auto; display:flex; align-items:center; gap:6px;">
                            <span>{p_date}</span>
                            {badge_html}
                        </div>
                    </div>
                </article>'''
        desktop_cards_html.append(card)

    all_desktop_grid = '\n' + '\n\n'.join(desktop_cards_html) + '\n            '

    # 2. Build Mobile Feed
    mobile_feed_html = []
    for idx, p in enumerate(posts):
        p_slug = p['slug']
        p_title = p.get('fullTitle', p.get('title', ''))
        p_cat = p.get('cat', '신차소식')
        p_date = p.get('date', '2026. 8. 30.')
        p_thumb = p.get('thumb', '')
        p_desc = p.get('summary', '')
        short_desc = (p_desc[:80] + '...') if len(p_desc) > 80 else p_desc
        badge_html = '<span class="feed-item-badge" style="color:#e11d48; font-weight:800; font-size:0.76rem; margin-left:4px;">(최신)</span>' if idx == 0 else ''

        m_card = f'''                <!-- Mobile Feed Card {idx+1}: {p_title} -->
                <article class="tistory-feed-item feed-visible" data-category="{p_cat}" onclick="location.href=\'posts/{p_slug}\'" style="cursor:pointer;">
                    <div class="feed-item-content">
                        <span class="feed-item-cat">{p_cat}</span>
                        <h3 class="feed-item-title">
                            <a href="posts/{p_slug}">{p_title}</a>
                        </h3>
                        <p class="feed-item-desc" style="display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; margin:4px 0 6px 0; font-size:0.84rem; color:#64748b; line-height:1.5;">{short_desc}</p>
                        <div class="feed-item-meta" style="font-size:0.76rem; color:#94a3b8;">
                            <span class="feed-item-date">{p_date}</span>
                            {badge_html}
                        </div>
                    </div>
                    <a href="posts/{p_slug}" class="feed-item-thumb-link" tabindex="-1" aria-hidden="true">
                        <img src="{p_thumb}" alt="{p_title}" class="feed-item-thumb" {"fetchpriority=\"high\"" if idx < 2 else "loading=\"lazy\""} decoding="async">
                    </a>
                </article>'''
        mobile_feed_html.append(m_card)

    all_mobile_feed = '\n' + '\n\n'.join(mobile_feed_html) + '\n            '

    with open(index_path, 'r', encoding='utf-8') as f:
        index_text = f.read()

    pc_grid_pattern = r'(<section class="clean-grid" id="desktopCardsGrid"[^>]*>)[\s\S]*?(</section>\s*<!-- 더보기 버튼)'
    index_text = re.sub(pc_grid_pattern, r'\1' + all_desktop_grid + r'\2', index_text)

    mob_feed_pattern = r'(<div class="tistory-feed-list" id="tistoryFeedContainer">)[\s\S]*?(</div>\s*<div class="mobile-load-more-wrap")'
    index_text = re.sub(mob_feed_pattern, r'\1' + all_mobile_feed + r'\2', index_text)

    with open(index_path, 'w', encoding='utf-8-sig') as f:
        f.write(index_text)
    print(f"[OK] Deterministically recompiled index.html from registry!")


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
        captions = re.findall(r"""<div[^>]*class=["']img-caption["'][^>]*>([\s\S]*?)</div>""", body_html)
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

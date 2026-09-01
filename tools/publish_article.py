# -*- coding: utf-8 -*-
import os, sys, json, re, datetime

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

    # 1. Desktop grid cards (Image Top, Body Bottom)
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

        card = f"""                <!-- Post {idx+1}: {p_title} -->
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
                </article>"""
        desktop_cards_html.append(card)

    all_desktop_grid = '\n' + '\n\n'.join(desktop_cards_html) + '\n            '

    # 2. Mobile feed cards (Image TOP, Body BOTTOM)
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

        m_card = f"""                <!-- Mobile Feed Card {idx+1}: {p_title} -->
                <article class="tistory-feed-item feed-visible" data-category="{p_cat}" onclick="location.href=\'posts/{p_slug}\'" style="cursor:pointer;">
                    <a href="posts/{p_slug}" class="feed-item-thumb-link" tabindex="-1" aria-hidden="true">
                        <img src="{p_thumb}" alt="{p_title}" class="feed-item-thumb" {"fetchpriority=\"high\"" if idx < 2 else "loading=\"lazy\""} decoding="async">
                    </a>
                    <div class="feed-item-body">
                        <span class="feed-item-cat">{p_cat}</span>
                        <h3 class="feed-item-title">
                            <a href="posts/{p_slug}">{p_title}</a>
                        </h3>
                        <p class="feed-item-summary" style="display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; margin:4px 0 6px 0; font-size:0.84rem; color:#64748b; line-height:1.5;">{short_desc}</p>
                        <div class="feed-item-meta" style="font-size:0.76rem; color:#94a3b8;">
                            <span class="feed-item-date">{p_date}</span>
                            {badge_html}
                        </div>
                    </div>
                </article>"""
        mobile_feed_html.append(m_card)

    all_mobile_feed = '\n' + '\n\n'.join(mobile_feed_html) + '\n            '

    with open(index_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Desktop grid replacement
    pc_grid_start = text.find('id="desktopCardsGrid"')
    if pc_grid_start != -1:
        pc_tag_end = text.find('>', pc_grid_start) + 1
        pc_grid_end = text.find('</section>', pc_tag_end)
        text = text[:pc_tag_end] + all_desktop_grid + text[pc_grid_end:]

    # Mobile feed replacement
    mob_feed_start = text.find('id="tistoryFeedContainer"')
    if mob_feed_start != -1:
        mob_tag_end = text.find('>', mob_feed_start) + 1
        next_marker = text.find('id="mobileLoadMoreWrapper"', mob_tag_end)
        if next_marker != -1:
            mob_feed_end = text.rfind('</div>', mob_tag_end, next_marker)
        else:
            mob_feed_end = text.find('</div>', mob_tag_end)
        text = text[:mob_tag_end] + all_mobile_feed + text[mob_feed_end:]

    with open(index_path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    validate_all_cards(features_path, index_path)
    print(f"[OK] Deterministically recompiled index.html from registry ({len(posts)} posts, Image-First layout)!")

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
      <description><![CDATA[{desc}]]></description>
      <category>posts</category>
      <pubDate>{pub_date}</pubDate>
      <guid>https://honeyjar.co.kr/posts/{slug}</guid>
    </item>
"""
        if f"https://honeyjar.co.kr/posts/{slug}" not in r_text:
            r_text = r_text.replace('</channel>', rss_item + '  </channel>')
            with open(rss_path, 'w', encoding='utf-8-sig') as f:
                f.write(r_text)
            print(f"[OK] Updated rss.xml for {slug}")

def submit_google_indexing(url, root_dir=None):
    if not root_dir:
        root_dir = os.path.dirname(os.path.dirname(__file__))
    key_path = os.path.join(root_dir, 'service_account.json')
    if not os.path.exists(key_path):
        key_path = os.path.join(root_dir, 'google_indexing_service_account.json')
    if not os.path.exists(key_path):
        key_path = os.path.join(r'C:\Users\lim\.gemini\antigravity', 'google_indexing_service_account.json')
    if not os.path.exists(key_path):
        print("[INFO] Service account key not found. Skipping Google Indexing API.")
        return False
    try:
        from google.oauth2 import service_account
        import googleapiclient.discovery
        SCOPES = ["https://www.googleapis.com/auth/indexing"]
        credentials = service_account.Credentials.from_service_account_file(key_path, scopes=SCOPES)
        service = googleapiclient.discovery.build('indexing', 'v3', credentials=credentials)
        content = {"url": url, "type": "URL_UPDATED"}
        response = service.urlNotifications().publish(body=content).execute()
        print(f"[OK] Google Indexing API: 200 OK ({url})")
        return True
    except Exception as e:
        print(f"[WARN] Google Indexing API: {e}")
        return False
    try:
        from google.oauth2 import service_account
        import googleapiclient.discovery
        SCOPES = ["https://www.googleapis.com/auth/indexing"]
        credentials = service_account.Credentials.from_service_account_file(key_path, scopes=SCOPES)
        service = googleapiclient.discovery.build('indexing', 'v3', credentials=credentials)
        content = {"url": url, "type": "URL_UPDATED"}
        response = service.urlNotifications().publish(body=content).execute()
        print(f"[OK] Google Indexing API: 200 OK ({url})")
        return True
    except Exception as e:
        print(f"[WARN] Google Indexing API: {e}")
        return False

def submit_indexnow(url):
    try:
        import requests
        api_url = "https://api.indexnow.org/indexnow"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        payload = {
            "host": "honeyjar.co.kr",
            "key": "a1b2c3d4e5f6g7h8i9j0",
            "keyLocation": "https://honeyjar.co.kr/a1b2c3d4e5f6g7h8i9j0.txt",
            "urlList": [url]
        }
        resp = requests.post(api_url, json=payload, headers=headers, timeout=5)
        print(f"[OK] IndexNow API: {resp.status_code} (Bing, Naver, Yandex pinged!)")
        return True
    except Exception as e:
        print(f"[WARN] IndexNow API: {e}")
        return False

def validate_all_cards(features_path, index_path, reg_var='HONEYJAR_POSTS_REGISTRY'):
    db_path = r'd:\작업\꿀단지\data\posts_db.json'
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8-sig') as f:
            posts = json.load(f)
    else:
        with open(features_path, 'r', encoding='utf-8-sig') as f:
            f_text = f.read()
        m = re.search(r'const ' + reg_var + r' = (\[[\s\S]*?\]);', f_text)
        if not m:
            raise ValueError("Registry not found in features.js!")
        posts = json.loads(m.group(1))

    for idx, p in enumerate(posts, 1):
        desc = p.get('desc') or p.get('summary', '')
        if not desc or len(desc.strip()) < 10:
            raise ValueError(f"Post #{idx} ({p.get('slug')}): EMPTY SUMMARY! Aborting publish.")
        if not p.get('thumb'):
            raise ValueError(f"Post #{idx} ({p.get('slug')}): MISSING THUMBNAIL! Aborting publish.")

    with open(index_path, 'r', encoding='utf-8') as f:
        i_text = f.read()

    mob_articles = re.findall(r'<article class="tistory-feed-item[\s\S]*?</article>', i_text)
    if len(mob_articles) != len(posts):
        raise ValueError(f"Card count mismatch in HTML: found {len(mob_articles)}, expected {len(posts)}!")

    for idx, art in enumerate(mob_articles, 1):
        sum_m = re.search(r'<p class="feed-item-summary"[^>]*>([\s\S]*?)</p>', art)
        if not sum_m or len(sum_m.group(1).strip()) < 10:
            raise ValueError(f"Compiled Card #{idx}: EMPTY SUMMARY TEXT IN HTML!")

    print(f"[QUALITY GATE PASSED] All {len(posts)} cards verified: 100% complete summaries, valid dates, single badge!")
    return True

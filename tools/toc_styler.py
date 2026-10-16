# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 목차(TOC) 자동 생성 및 스타일러 (toc_styler.py)
- 본문 내 기존 .toc-box를 제거하고 첫 번째 <h2> 직전에 표준 목차를 자동 삽입합니다.
- 각 <h2>에 id="sec-1", id="sec-2" 등을 자동 부여하여 앵글 점프를 완성합니다.
"""
import re


def apply_toc_Styles(html_str: str) -> str:
    # 1. 기존 수동 작성된 .toc-box가 있으면 제거 (중복 목차 100% 방지)
    html_str = re.sub(
        r'<div[^>]*class=["\'][^"\']*toc-box[^"\']*["\'][^>]*>[\s\S]*?</div>\s*(?:</div>)?',
        '',
        html_str,
        flags=re.IGNORECASE
    )

    # 2. 모든 <h2> 태그 스캔 및 ID 부여
    h2_pattern = re.compile(r'<h2([^>]*)>([\s\S]*?)</h2>', re.IGNORECASE)
    matches = list(h2_pattern.finditer(html_str))
    if not matches:
        return html_str

    toc_items = []
    new_html_parts = []
    last_idx = 0

    for i, m in enumerate(matches, 1):
        attrs = m.group(1)
        inner_html = m.group(2)
        clean_title = re.sub(r'<[^>]+>', '', inner_html).strip()

        id_match = re.search(r'id=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        if id_match:
            sec_id = id_match.group(1)
            new_attrs = attrs
        else:
            sec_id = f"sec-{i}"
            new_attrs = f'{attrs} id="{sec_id}"'

        toc_items.append((sec_id, clean_title))

        new_html_parts.append(html_str[last_idx:m.start()])
        if i == 1:
            # 첫 번째 <h2> 직전에 TOC 자리 표시자 삽입
            new_html_parts.append("<!--__AUTO_TOC_PLACEHOLDER__-->\n")
        new_html_parts.append(f"<h2{new_attrs}>{inner_html}</h2>")
        last_idx = m.end()

    new_html_parts.append(html_str[last_idx:])
    updated_html = "".join(new_html_parts)

    # 3. 표준 TOC HTML 조립
    li_lines = []
    for idx, (sec_id, title) in enumerate(toc_items, 1):
        li_lines.append(
            f'<li style="margin: 0; padding: 0; line-height: 1.5;">'
            f'<a href="#{sec_id}" style="color: #334155; text-decoration: none; font-size: 0.94rem; font-weight: 600; display: flex; align-items: baseline; gap: 8px;">'
            f'<span style="color: #c26908; font-weight: 800; font-size: 0.88rem; min-width: 18px;">0{idx}.</span>'
            f'<span>{title}</span></a></li>'
        )

    toc_html = (
        '<div class="toc-box" style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px 24px; margin: 28px 0;">\n'
        '  <div class="toc-title" style="font-size: 1.02rem; font-weight: 800; color: #0f172a; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; gap: 6px;">📑 핵심 목차 (클릭 시 이동)</div>\n'
        '  <ul style="list-style: none !important; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 8px;">\n    '
        + "\n    ".join(li_lines) +
        '\n  </ul>\n</div>'
    )

    return updated_html.replace("<!--__AUTO_TOC_PLACEHOLDER__-->", toc_html, 1)

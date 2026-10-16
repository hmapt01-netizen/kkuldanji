# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - 반응형 데이터 테이블 자동 스타일러 (table_styler.py)
- 본문 내 <table class="custom-data-table">을 감지하여 모바일 가로 스크롤 래퍼 및 셀 스타일을 자동 적용합니다.
"""
import re


def apply_table_styles(html_str: str) -> str:
    def style_single_table(match):
        table_html = match.group(0)
        # 이미 래퍼가 있거나 인라인 스타일이 완비된 경우 유지하되 기본 패딩 보강
        if 'style=' not in table_html[:60]:
            table_html = re.sub(
                r'^<table([^>]*)>',
                r'<table\1 style="width: 100%; border-collapse: collapse; font-size: 0.94rem; line-height: 1.6; margin: 0;">',
                table_html,
                count=1,
                flags=re.IGNORECASE
            )
        # th 스타일 보강
        table_html = re.sub(
            r'<th(?![^>]*style=)([^>]*)>',
            r'<th\1 style="background: #f8fafc; color: #0f172a; font-weight: 800; padding: 12px 14px; border-bottom: 2px solid #cbd5e1; text-align: left;">',
            table_html,
            flags=re.IGNORECASE
        )
        # td 스타일 보강
        table_html = re.sub(
            r'<td(?![^>]*style=)([^>]*)>',
            r'<td\1 style="padding: 12px 14px; border-bottom: 1px solid #e2e8f0; color: #334155; vertical-align: top;">',
            table_html,
            flags=re.IGNORECASE
        )
        return table_html

    styled = re.sub(
        r'<table[^>]*class=["\'][^"\']*custom-data-table[^"\']*["\'][^>]*>[\s\S]*?</table>',
        style_single_table,
        html_str,
        flags=re.IGNORECASE
    )

    # custom-data-table-wrap으로 감싸지지 않은 경우 자동 래핑
    def wrap_if_needed(m):
        full = m.group(0)
        return f'<div class="custom-data-table-wrap" style="width: 100%; overflow-x: auto; margin: 24px 0; border: 1px solid #e2e8f0; border-radius: 12px;">{full}</div>'

    if 'custom-data-table-wrap' not in styled and 'custom-data-table' in styled:
        styled = re.sub(
            r'<table[^>]*class=["\'][^"\']*custom-data-table[^"\']*["\'][^>]*>[\s\S]*?</table>',
            wrap_if_needed,
            styled,
            flags=re.IGNORECASE
        )

    return styled

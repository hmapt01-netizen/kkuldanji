<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html lang="ko">
      <head>
        <title><xsl:value-of select="/rss/channel/title"/> - RSS Feed</title>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <!-- 🍯 파비콘 풀세트 -->
        <link rel="shortcut icon" href="favicon.ico"/>
        <link rel="icon" type="image/x-icon" href="favicon.ico"/>
        <link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,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"/>
        <link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCIgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0Ij4KICA8ZGVmcz4KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0icG90R3JhZCIgeDE9IjAlIiB5MT0iMCUiIHgyPSIxMDAlIiB5Mj0iMTAwJSI+CiAgICAgIDxzdG9wIG9mZnNldD0iMCUiIHN0b3AtY29sb3I9IiNiNDUzMDkiIC8+CiAgICAgIDxzdG9wIG9mZnNldD0iMTAwJSIgc3RvcC1jb2xvcj0iIzc4MzUwZiIgLz4KICAgIDwvbGluZWFyR3JhZGllbnQ+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImhvbmV5R3JhZCIgeDE9IjAlIiB5MT0iMCUiIHgyPSIwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdG9wLWNvbG9yPSIjZmJiZjI0IiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjUwJSIgc3RvcC1jb2xvcj0iI2Y1OWUwYiIgLz4KICAgICAgPHN0b3Agb2Zmc2V0PSIxMDAlIiBzdG9wLWNvbG9yPSIjZDk3NzA2IiAvPgogICAgPC9saW5lYXJHcmFkaWVudD4KICAgIDxsaW5lYXJHcmFkaWVudCBpZD0ibGVhZkdyYWQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdG9wLWNvbG9yPSIjMzRkMzk5IiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0b3AtY29sb3I9IiMwNTk2NjkiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogIDwvZGVmcz4KCiAgPCEtLSDwn42vIO2Zqeq4iCDqv4Dri6jsp4Ag7ZWt7JWE66asICjtiKzrqoUg67Cw6rK9IOyInOyImCDrsqHthLApIC0tPgogIDxwYXRoIGQ9Ik0yMCAyMiBDMTYgMjcgMTUgMzUgMTcgNDMgQzE5IDUwIDI1IDU0IDMyIDU0IEMzOSA1NCA0NSA1MCA0NyA0MyBDNDkgMzUgNDggMjcgNDQgMjIgWiIgCiAgICAgICAgZmlsbD0idXJsKCNwb3RHcmFkKSIgc3Ryb2tlPSIjNDUxYTAzIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIC8+CgogIDwhLS0g7ZWt7JWE66asIOyeheq1rCAtLT4KICA8ZWxsaXBzZSBjeD0iMzIiIGN5PSIyMiIgcng9IjEzIiByeT0iMy42IiBmaWxsPSIjYjQ1MzA5IiBzdHJva2U9IiM0NTFhMDMiIHN0cm9rZS13aWR0aD0iMiIgLz4KICA8ZWxsaXBzZSBjeD0iMzIiIGN5PSIyMSIgcng9IjEwLjUiIHJ5PSIyLjQiIGZpbGw9IiNkOTc3MDYiIC8+CgogIDwhLS0g7Z2Y65+s64K066as64qUIO2Zqeq4iCDqv4DrsKnsmrggLS0+CiAgPHBhdGggZD0iTTMyIDI0IEMyOCAyOSAyNiAzNSAyNiAzOSBDMjYgNDQgMjguNSA0NyAzMiA0NyBDMzUuNSA0NyAzOCA0NCAzOCAzOSBDMzggMzUgMzYgMjkgMzIgMjQgWiIgCiAgICAgICAgZmlsbD0idXJsKCNob25leUdyYWQpIiBzdHJva2U9IiNiNDUzMDkiIHN0cm9rZS13aWR0aD0iMS4yIiAvPgogIAogIDwhLS0g6r+A67Cp7Jq4IOyeheyytCDqtJHtg50gLS0+CiAgPGVsbGlwc2UgY3g9IjI5LjUiIGN5PSIzNyIgcng9IjEuOCIgcnk9IjMuNSIgZmlsbD0iI2ZmZmZmZiIgb3BhY2l0eT0iMC44NSIgdHJhbnNmb3JtPSJyb3RhdGUoLTI1IDI5LjUgMzcpIiAvPgogIDxjaXJjbGUgY3g9IjM0LjUiIGN5PSI0MiIgcj0iMS4zIiBmaWxsPSIjZmZmZmZmIiBvcGFjaXR5PSIwLjciIC8+CgogIDwhLS0g7Iux6re465+s7Jq0IOy0iOuhnSDsno7sgqzqt4AgLS0+CiAgPHBhdGggZD0iTTQyIDQ1IEM0NyA0NCA1MiA0MCA1MyAzMyBDNDYgMzQgNDIgMzggNDIgNDUgWiIgCiAgICAgICAgZmlsbD0idXJsKCNsZWFmR3JhZCkiIHN0cm9rZT0iIzA2NWY0NiIgc3Ryb2tlLXdpZHRoPSIxLjIiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIC8+CiAgPHBhdGggZD0iTTQyIDQ1IEM0NiA0MSA0OSAzNyA1MyAzMyIgc3Ryb2tlPSIjYTdmM2QwIiBzdHJva2Utd2lkdGg9IjAuOCIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiAvPgo8L3N2Zz4="/>
        <style>
          body { font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", Pretendard, sans-serif; background: #f8fafc; color: #1e293b; padding: 40px 20px; max-width: 800px; margin: 0 auto; line-height: 1.6; }
          .feed-header { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 30px; text-align: center; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); }
          .feed-badge { display: inline-block; background: #fef3c7; color: #b45309; font-size: 0.8rem; font-weight: 800; padding: 4px 12px; border-radius: 20px; margin-bottom: 12px; border: 1px solid #fde68a; }
          .feed-title-main { font-size: 1.5rem; font-weight: 850; color: #0f172a; margin: 0 0 8px 0; }
          .feed-desc-main { font-size: 0.95rem; color: #64748b; margin: 0 0 16px 0; }
          .feed-home-btn { display: inline-block; background: #0f172a; color: #ffffff; padding: 8px 18px; border-radius: 8px; text-decoration: none; font-size: 0.88rem; font-weight: 700; }
          .feed-item { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 22px 24px; margin-bottom: 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.02); transition: transform 0.15s; }
          .feed-item:hover { transform: translateY(-2px); }
          .item-cat { font-size: 0.78rem; font-weight: 800; color: #c26908; margin-bottom: 6px; display: block; }
          .item-title { font-size: 1.15rem; font-weight: 800; color: #0f172a; margin: 0 0 8px 0; }
          .item-title a { color: inherit; text-decoration: none; }
          .item-title a:hover { color: #d97706; text-decoration: underline; }
          .item-desc { font-size: 0.92rem; color: #64748b; line-height: 1.6; margin: 0 0 10px 0; }
          .item-date { font-size: 0.8rem; color: #94a3b8; }
        </style>
      </head>
      <body>
        <div class="feed-header">
          <span class="feed-badge">📡 꿀단지 공식 실시간 RSS 2.0 피드</span>
          <h1 class="feed-title-main"><xsl:value-of select="/rss/channel/title"/></h1>
          <p class="feed-desc-main"><xsl:value-of select="/rss/channel/description"/></p>
          <a class="feed-home-btn" href="https://honeyjar.co.kr">꿀단지 매거진 홈으로 가기 →</a>
        </div>
        <xsl:for-each select="/rss/channel/item">
          <div class="feed-item">
            <span class="item-cat"><xsl:value-of select="category"/></span>
            <h2 class="item-title">
              <a>
                <xsl:attribute name="href"><xsl:value-of select="link"/></xsl:attribute>
                <xsl:value-of select="title"/>
              </a>
            </h2>
            <p class="item-desc"><xsl:value-of select="description"/></p>
            <div class="item-date">발행일시: <xsl:value-of select="pubDate"/></div>
          </div>
        </xsl:for-each>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>

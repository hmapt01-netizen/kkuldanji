# -*- coding: utf-8 -*-
"""
꿀단지 (KKULDANJI) - GA4 & Search Console 실시간 트래픽 통합 분석 엔진
- GA4: 순수 사람 방문자(Active Users), 페이지뷰, 평균 체류시간, 인기 글 TOP 5, 유입 경로
- Search Console: 구글 검색 노출수, 클릭수, 평균 게재 순위, 검색 쿼리
"""
import os
import sys
import json
from datetime import datetime, timedelta

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_PATH = os.path.join(ROOT_DIR, 'service_account.json')
GA4_PROPERTY_ID = '551680652'
GSC_SITE_URL = 'sc-domain:honeyjar.co.kr'


def get_ga4_report(start_date='yesterday', end_date='yesterday'):
    """GA4 Data API 조회"""
    try:
        from google.oauth2 import service_account
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric, Dimension, OrderBy

        creds = service_account.Credentials.from_service_account_file(KEY_PATH)
        client = BetaAnalyticsDataClient(credentials=creds)

        # 1. 종합 지표 요약
        req_summary = RunReportRequest(
            property=f'properties/{GA4_PROPERTY_ID}',
            metrics=[
                Metric(name='activeUsers'),
                Metric(name='screenPageViews'),
                Metric(name='sessions'),
                Metric(name='averageSessionDuration'),
                Metric(name='bounceRate')
            ],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)]
        )
        res_summary = client.run_report(req_summary)

        summary_data = {}
        if res_summary.rows:
            row = res_summary.rows[0]
            summary_data = {
                'activeUsers': int(row.metric_values[0].value),
                'pageViews': int(row.metric_values[1].value),
                'sessions': int(row.metric_values[2].value),
                'avgDuration': float(row.metric_values[3].value),
                'bounceRate': float(row.metric_values[4].value) if len(row.metric_values) > 4 else 0.0
            }

        # 2. 인기 글 TOP 5
        req_pages = RunReportRequest(
            property=f'properties/{GA4_PROPERTY_ID}',
            dimensions=[Dimension(name='pageTitle'), Dimension(name='pagePath')],
            metrics=[Metric(name='screenPageViews'), Metric(name='activeUsers')],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name='screenPageViews'), desc=True)],
            limit=5,
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)]
        )
        res_pages = client.run_report(req_pages)
        top_pages = []
        for r in res_pages.rows:
            top_pages.append({
                'title': r.dimension_values[0].value,
                'path': r.dimension_values[1].value,
                'views': int(r.metric_values[0].value),
                'users': int(r.metric_values[1].value)
            })

        # 3. 유입 경로
        req_sources = RunReportRequest(
            property=f'properties/{GA4_PROPERTY_ID}',
            dimensions=[Dimension(name='sessionDefaultChannelGroup')],
            metrics=[Metric(name='sessions'), Metric(name='activeUsers')],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name='sessions'), desc=True)],
            limit=5,
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)]
        )
        res_sources = client.run_report(req_sources)
        sources = []
        for r in res_sources.rows:
            sources.append({
                'channel': r.dimension_values[0].value,
                'sessions': int(r.metric_values[0].value),
                'users': int(r.metric_values[1].value)
            })

        return {'status': 'OK', 'summary': summary_data, 'top_pages': top_pages, 'sources': sources}
    except Exception as e:
        return {'status': 'ERROR', 'error': str(e)}


def get_gsc_report(days=7):
    """Google Search Console API 조회"""
    try:
        from google.oauth2 import service_account
        import googleapiclient.discovery

        creds = service_account.Credentials.from_service_account_file(
            KEY_PATH, scopes=['https://www.googleapis.com/auth/webmasters.readonly']
        )
        service = googleapiclient.discovery.build('searchconsole', 'v1', credentials=creds)

        end_d = datetime.now() - timedelta(days=1)
        start_d = datetime.now() - timedelta(days=days)
        body = {
            'startDate': start_d.strftime('%Y-%m-%d'),
            'endDate': end_d.strftime('%Y-%m-%d'),
            'dimensions': ['date']
        }
        res = service.searchanalytics().query(siteUrl=GSC_SITE_URL, body=body).execute()
        return {'status': 'OK', 'rows': res.get('rows', [])}
    except Exception as e:
        return {'status': 'ERROR', 'error': str(e)}


def main():
    target_date = sys.argv[1] if len(sys.argv) > 1 else 'yesterday'
    print("=" * 65)
    print(f"  🍯 [꿀단지 실시간 트래픽 & 서치콘솔 통합 분석 리포트] ({target_date})")
    print("=" * 65)

    # 1. GA4 분석
    ga4 = get_ga4_report(start_date=target_date, end_date=target_date)
    if ga4['status'] == 'OK':
        s = ga4['summary']
        print(f"\n👤 [1. 순수 사람 방문자 (GA4 집계)]")
        print(f"  • 순수 방문자(Active Users) : {s.get('activeUsers', 0)}명")
        print(f"  • 총 페이지뷰(Page Views)    : {s.get('pageViews', 0)}회")
        print(f"  • 총 세션 수(Sessions)       : {s.get('sessions', 0)}회")
        print(f"  • 평균 체류 시간            : {s.get('avgDuration', 0):.1f}초")

        if ga4['sources']:
            print(f"\n🌐 [유입 경로]")
            for src in ga4['sources']:
                print(f"  • {src['channel']}: {src['users']}명 ({src['sessions']}세션)")

        if ga4['top_pages']:
            print(f"\n📖 [인기 글 TOP 5]")
            for idx, p in enumerate(ga4['top_pages'], 1):
                clean_t = p['title'].replace(' | 혀니의 꿀단지', '').strip()
                print(f"  {idx}. {clean_t} ({p['path']}) - {p['views']}회 조회 / {p['users']}명")
    else:
        print(f"\n⚠️ [GA4 조회 안내]: {ga4.get('error')}")

    # 2. Search Console 분석
    gsc = get_gsc_report(days=7)
    if gsc['status'] == 'OK' and gsc['rows']:
        print(f"\n🔍 [2. 구글 검색 실적 (Search Console 최신 7일 집계)]")
        for row in gsc['rows']:
            d = row['keys'][0]
            print(f"  • [{d}] 노출: {row['impressions']}회 / 클릭: {row['clicks']}회 / 평균순위: {row['position']:.1f}위")
    elif gsc['status'] == 'OK':
        print(f"\n🔍 [2. 구글 검색 실적]: 최근 집계된 검색 노출 데이터가 아직 없습니다.")
    else:
        print(f"\n⚠️ [Search Console 조회 안내]: {gsc.get('error')}")

    print("=" * 65)


if __name__ == '__main__':
    main()

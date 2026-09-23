# -*- coding: utf-8 -*-
"""
단위 테스트: Evidence Guard 정밀 검증 스위트 (순수 추상 검증 모드)
- [마스터 표준 23-2호, 23-3호, 23-4호]
- 수학적 수치 집합 대조: S_article ⊆ S_source
- 양대 채널 수치 동등성: S_naver == S_google
- 동적 기관 명의 직접성(Direct Grounding) 검증
- 동적 식별자(PMID) 정합성 검증
- 괄호 예시 및 단어 하드코딩 0개 원칙 검증
"""
import unittest
import copy
import json
import os
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

import evidence_guard as eg


class TestEvidenceGuard(unittest.TestCase):
    def setUp(self):
        self.valid_references = [
            '<a href="https://www.nhs.uk/conditions/sore-throat/">UK NHS 《Sore throat home care》</a> — 따뜻한 소금물 가글의 인후통 완화 요령, 소아 가글 금기 및 즉시 응급 진료 적신호 안내.',
            '<a href="https://pubmed.ncbi.nlm.nih.gov/30705369/">Scientific Reports (Nature / PMID: 30705369, PMC6355924)</a> — 상기도 감염 시 고장성 식염수 비강 세척 및 가글 병행 파일럿 무작위 대조시험(Ramalingam et al., 2019).',
            '<a href="https://www.nhs.uk/live-well/healthy-teeth-and-gums/how-to-keep-your-teeth-clean/">UK NHS 《How to keep your teeth clean》</a> — 양치 후 불소 보호막 보존을 위해 물로 헹구지 않는 Spit, don\'t rinse 지침.'
        ]

        self.valid_sources = [
            {
                "id": "src_nhs_throat",
                "title": "Sore throat",
                "institution": "UK NHS",
                "url": "https://www.nhs.uk/conditions/sore-throat/",
                "evidence_quote": "Gargle with warm, salty water to reduce swelling and pain (children should not try this). Dissolve half a teaspoon of salt in a glass of warm water."
            },
            {
                "id": "src_ramalingam",
                "pmid": "30705369",
                "pmcid": "PMC6355924",
                "doi": "10.1038/s41598-018-37703-3",
                "authors": ["Ramalingam S", "Graham C"],
                "title": "A pilot, open labelled, randomised controlled trial of hypertonic saline nasal irrigation and gargling for the common cold",
                "evidence_quote": "A pilot randomised controlled trial... hypertonic saline nasal irrigation and gargling."
            },
            {
                "id": "src_nhs_teeth",
                "title": "How to keep your teeth clean",
                "institution": "UK NHS",
                "url": "https://www.nhs.uk/live-well/healthy-teeth-and-gums/how-to-keep-your-teeth-clean/",
                "evidence_quote": "Spit, don't rinse. Don't rinse your mouth immediately after brushing."
            }
        ]

        stmt1 = "영국 국민보건서비스(NHS) 지침에 따르면 따뜻한 물 한 컵에 소금 반 티스푼을 녹여 가글하는 생활 요법을 안내합니다."
        stmt2 = "소금물 가글 임상 연구(Ramalingam et al., 2019)는 코 세척과 가글을 병행한 소규모 파일럿 시험으로 가글 단독 효과로 단정할 수 없으며 대증요법에 한정됩니다."
        stmt3 = "양치 직후에는 치약의 불소 보호막이 씻겨나가는 것을 막기 위해 물이나 가글로 바로 헹구지 말고(NHS 지침), 소금물 가글은 양치와 분리된 별도 시간대에 하는 것이 안전합니다."

        self.valid_claims = [
            {
                "id": "claim_01",
                "statement": stmt1,
                "statement_hash": eg.compute_statement_hash(stmt1),
                "source_id": "src_nhs_throat",
                "category": "guideline",
                "limits": "가정용 대증요법에 한정"
            },
            {
                "id": "claim_02",
                "statement": stmt2,
                "statement_hash": eg.compute_statement_hash(stmt2),
                "source_id": "src_ramalingam",
                "category": "academic",
                "limits": "코 세척 병행 소규모 파일럿 시험에 한정"
            },
            {
                "id": "claim_03",
                "statement": stmt3,
                "statement_hash": eg.compute_statement_hash(stmt3),
                "source_id": "src_nhs_teeth",
                "category": "oral_hygiene",
                "limits": "불소 잔류 보호막 유지 원칙"
            }
        ]

        self.manifest_data = {
            "sources": self.valid_sources,
            "claims": self.valid_claims
        }

        self.valid_post_data = {
            "title": "환절기 목 통증 소금물 가글 방법과 주의사항, 따뜻한 물 비율과 소아 금기",
            "shortTitle": "환절기 소금물 가글 방법과 주의사항",
            "desc": "환절기 목 칼칼할 때 영국 NHS가 안내하는 따뜻한 물 한 컵에 소금 반 티스푼 비율과 소아 금기 수칙, 불소 보호막 보존 요령을 알아봅니다.",
            "references": self.valid_references,
            "bodyHtml": (
                '<p>환절기 목 통증 시 영국 국민보건서비스(NHS) 지침에 따르면 따뜻한 물 한 컵에 소금 반 티스푼을 녹여 가글하는 생활 요법을 안내합니다.</p>\n'
                '<p>소금물 가글 임상 연구(Ramalingam et al., 2019)는 코 세척과 가글을 병행한 소규모 파일럿 시험으로 가글 단독 효과로 단정할 수 없으며 대증요법에 한정됩니다.</p>\n'
                '<p>양치 직후에는 치약의 불소 보호막이 씻겨나가는 것을 막기 위해 물이나 가글로 바로 헹구지 말고(NHS 지침), 소금물 가글은 양치와 분리된 별도 시간대에 하는 것이 안전합니다.</p>\n'
                '<p>어린이는 기도 흡인과 고나트륨 위험으로 소금물 가글을 피해야 하며, 숨쉬기 어렵거나 침을 삼키지 못하는 경우 지체 없이 즉시 응급 진료를 받아야 합니다.</p>\n'
                '<figure class="post-img-wrap"><img src="post01.jpg" alt="소금물 가글 준비 모습"><figcaption>따뜻한 물에 소금을 완전히 녹여 준비하는 모습</figcaption></figure>'
            ),
            "faqs": [
                {
                    "q": "물과 소금의 비율은 어떻게 맞추나요?",
                    "a": "영국 NHS 지침에서는 따뜻한 물 한 컵에 소금 반 티스푼을 완전히 녹여 사용할 것을 안내합니다."
                }
            ]
        }

    def test_pmid_mismatch_detection(self):
        """1. 엉뚱한 논문 연결 적발 검증"""
        bad_sources = copy.deepcopy(self.valid_sources)
        bad_sources[1]["pmid"] = "30705360"
        bad_sources[1]["pmcid"] = "PMC6355609"

        with self.assertRaises(eg.IdentifierMismatchError):
            bad_manifest = {"sources": bad_sources, "claims": self.valid_claims}
            naver_bad = '<p>Scientific Reports (Nature / PMID: 30705360)</p>'
            eg.verify_cross_channel_consistency(self.valid_post_data, naver_bad, manifest_data=self.manifest_data)

    def test_institutional_false_attribution(self):
        """2. 공인 출처 원문에 대상 주제 언급이 없는 허위 권위 사칭 적발 검증"""
        bad_sources = [
            {
                "id": "src_fake_inst",
                "institution": "대한특정학회",
                "evidence_quote": "실내 습도를 유지하고 충분한 휴식을 취한다."  # 가글/소금 관련 언급 없음
            }
        ]
        bad_text = "대한특정학회 지침에 따르면 소금물 가글을 적극 권고한다."
        with self.assertRaises(eg.ClaimGroundingError):
            eg.verify_institutional_grounding(bad_sources, bad_text, topic_keywords=["소금물", "가글"])

    def test_mathematical_quantity_grounding(self):
        """3. 출처 원문에 없는 자의적 수치(S_article - S_source != empty) 적발 검증"""
        # 출처(half a teaspoon in a glass)에 없는 임의 중량(1.8g)
        bad_text_g = "물 1컵에 1.8g을 녹여야 안전합니다."
        with self.assertRaises(eg.SpuriousPrecisionError):
            eg.check_numeric_grounding(bad_text_g, self.manifest_data)

        # 출처에 없는 임의 백분율(3%)
        bad_text_pct = "농도가 3%를 초과하면 자극이 발생합니다."
        with self.assertRaises(eg.SpuriousPrecisionError):
            eg.check_numeric_grounding(bad_text_pct, self.manifest_data)

        # 출처에 없는 임의 온도(38.5도)
        bad_text_temp = "38.5도 이상 고열 발생 시..."
        with self.assertRaises(eg.SpuriousPrecisionError):
            eg.check_numeric_grounding(bad_text_temp, self.manifest_data)

    def test_blocked_root_domain(self):
        """4. 루트 도메인 차단 검증"""
        with self.assertRaises(eg.InvalidReferenceError):
            eg.verify_reference_url("https://health.kdca.go.kr/")

    def test_clean_valid_post_pass(self):
        """5. 모든 검증을 완벽히 통과하는 클린 원고 검증"""
        self.assertTrue(eg.validate_post_evidence(self.valid_post_data))

    def test_cross_channel_quantity_equality(self):
        """6. 네이버 원고에만 독자적 수치가 기재된 경우(S_naver != S_google) 적발 검증"""
        clean_naver = (
            '<h1>"목이 따끔거려요" 환절기 소금물 가글 방법과 따뜻한 물 비율</h1>'
            '<p>영국 NHS 지침에 따르면 따뜻한 물 한 컵에 소금 반 티스푼을 완전히 녹여 가글하는 생활 요법을 안내합니다.</p>'
            '<p>소금물 가글 임상 연구(Ramalingam et al., 2019)는 코 세척과 가글 병행 파일럿 시험으로 대증요법에 한정됩니다.</p>'
            '<p>양치 직후에는 치약의 불소 보호막이 씻겨나가는 것을 막기 위해 물로 바로 헹구지 말고 분리 사용합니다.</p>'
            '<p>소아 및 어린이는 기도 흡인 위험으로 가글을 피해야 하며 호흡곤란이나 연하곤란, 고열 시 즉시 응급 진료를 받습니다.</p>'
            '<footer><p>Scientific Reports (PMID: 30705369, PMC6355924)</p></footer>'
        )
        # 정상 네이버 원고 통과
        eg.verify_cross_channel_consistency(self.valid_post_data, clean_naver, manifest_data=self.manifest_data)

        # 네이버에만 구글에 없는 독자적 수치 추가 시 차단
        with self.assertRaises(eg.CrossChannelMismatchError):
            eg.verify_cross_channel_consistency(self.valid_post_data, clean_naver + '<p>소금 5g 배합</p>', manifest_data=self.manifest_data)

        # 네이버에 중복 문단 연속 배치 시 차단
        dup_naver = clean_naver + (
            '<p>가정용 종이컵에 티스푼 반 스푼을 녹이면 순한 식염수가 만들어지며 멸균 생리식염수와는 구별됩니다.</p>'
            '<p>가정용 종이컵에 티스푼 반 스푼을 녹이면 순한 식염수가 만들어지며 멸균 생리식염수와는 구별됩니다.</p>'
        )
        with self.assertRaises(eg.CrossChannelMismatchError):
            eg.verify_cross_channel_consistency(self.valid_post_data, dup_naver, manifest_data=self.manifest_data)

    def test_honorific_consistency_plain_ending_detection(self):
        """7. 평서문(반말 느낌) 종결 적발 및 100% 정통 경어체 통일 검증"""
        # 평서문 종결 감지 시 차단
        bad_texts = [
            "<p>사전 복용을 삼가며 증상이 있을 때 사용하는 것이 합리적이다.</p>",
            "<p>열이 없거나 가벼운 증상일 때는 접종을 미룰 필요가 없다.</p>",
            "<p>보건당국 가이드라인을 철저히 확인해야 한다.</p>",
            "<p>의료진과의 상담을 권장한다.</p>"
        ]
        for bt in bad_texts:
            with self.assertRaises(eg.ToneConsistencyError):
                eg.check_honorific_consistency(bt, context_label="테스트")

        # 올바른 경어체 통과
        good_texts = [
            "<p>사전 복용을 삼가며 증상이 있을 때 사용하는 것이 합리적입니다.</p>",
            "<p>열이 없거나 가벼운 증상일 때는 접종을 미룰 필요가 없습니다.</p>",
            "<p>보건당국 가이드라인을 철저히 확인해야 합니다.</p>",
            "<p>의료진과의 상담을 권장합니다.</p>",
            "<p>체온이 높다면 예진표 작성 시 말씀해 주세요.</p>"
        ]
        for gt in good_texts:
            eg.check_honorific_consistency(gt, context_label="테스트")

    def test_paragraph_length_wall_of_text_detection(self):
        """8. 모바일 가독성을 해치는 과대 문단(벽돌글) 및 줄 나눔 누락 적발 검증"""
        # 220자 이상이면서 3문장 이상인 빽빽한 벽돌글 문단
        dense_paragraph = (
            "<p>이미 감기 때문에 복용 중인 해열진통제는 그대로 드시되 예진 때 말씀하시면 됩니다. "
            "하지만 백신 접종 후 생길 수 있는 열이나 통증을 예방하기 위해 해열진통제를 미리 복용할 필요는 일반적으로 없으며, "
            "접종 후 증상이 발생했을 때 의료진의 안내에 따라 사용하는 것이 합리적입니다. "
            "특별한 이유가 없다면 사전 복용을 삼가며 접종 후 실제로 열이나 통증이 생겼을 때 의료진 안내에 따라 복용하는 것으로 충분합니다.</p>"
        )
        with self.assertRaises(eg.ParagraphLengthError):
            eg.check_paragraph_length(dense_paragraph, context_label="구글 본문 테스트")

        # 1~2개 문장 단위로 분리(줄 나눔)된 쾌적한 문단들 통과
        split_paragraphs = (
            "<p>이미 감기 때문에 복용 중인 해열진통제는 그대로 드시되 예진 때 말씀하시면 됩니다. "
            "하지만 백신 접종 후 생길 수 있는 열이나 통증을 예방하기 위해 해열진통제를 미리 복용할 필요는 일반적으로 없으며, "
            "접종 후 증상이 발생했을 때 의료진의 안내에 따라 사용하는 것이 합리적입니다.</p>\n"
            "<p>특별한 이유가 없다면 사전 복용을 삼가며 접종 후 실제로 열이나 통증이 생겼을 때 의료진 안내에 따라 복용하는 것으로 충분합니다.</p>"
        )
        eg.check_paragraph_length(split_paragraphs, context_label="구글 본문 테스트")

    def test_unique_references_verification_blocks_boilerplate_and_reused(self):
        """9. [마스터 표준 23-7호] 참고문헌 복사·재탕 차단 및 고유 식별자 검증"""
        import tempfile

        # 가상 DB 생성
        mock_db = [
            {
                "slug": "post-a.html",
                "title": "기존 포스트 A",
                "references": [
                    '<a href="https://example.org/guideline-a">기관 A 지침</a>',
                    '<a href="https://example.org/guideline-b">기관 B 지침</a>',
                    '<a href="https://pubmed.ncbi.nlm.nih.gov/11111111/">논문 1 (PMID: 11111111)</a>'
                ]
            },
            {
                "slug": "post-b.html",
                "title": "기존 포스트 B",
                "references": [
                    '<a href="https://example.org/guideline-c">기관 C 지침</a>',
                    '<a href="https://example.org/guideline-d">기관 D 지침</a>',
                    '<a href="https://pubmed.ncbi.nlm.nih.gov/22222222/">논문 2 (PMID: 22222222)</a>'
                ]
            }
        ]

        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8-sig', delete=False, suffix='.json') as tf:
            json.dump(mock_db, tf, ensure_ascii=False)
            tmp_db_path = tf.name

        try:
            # 케이스 1: 포스트 A의 참고문헌을 100% 그대로 복사해 온 경우 ➔ 차단
            stolen_refs = [
                '<a href="https://example.org/guideline-a">기관 A 지침 복붙</a>',
                '<a href="https://example.org/guideline-b">기관 B 지침 복붙</a>',
                '<a href="https://pubmed.ncbi.nlm.nih.gov/11111111/">논문 1 (PMID: 11111111) 복붙</a>'
            ]
            with self.assertRaises(eg.InvalidReferenceError) as ctx:
                eg.verify_unique_references_across_posts("new-post-c.html", stolen_refs, db_path=tmp_db_path)
            self.assertIn("참고문헌 복사·재탕 위반", str(ctx.exception))

            # 케이스 2: A와 B의 기존 출처들을 섞어서 썼으나 본 글만의 고유 식별자가 0건인 경우 ➔ 차단
            reused_refs = [
                '<a href="https://example.org/guideline-a">기관 A 지침</a>',
                '<a href="https://example.org/guideline-c">기관 C 지침</a>',
                '<a href="https://pubmed.ncbi.nlm.nih.gov/22222222/">논문 2 (PMID: 22222222)</a>'
            ]
            with self.assertRaises(eg.InvalidReferenceError) as ctx2:
                eg.verify_unique_references_across_posts("new-post-c.html", reused_refs, db_path=tmp_db_path)
            self.assertIn("고유 참고문헌 부재", str(ctx2.exception))

            # 케이스 3: 기존 출처가 일부 섞여 있어도 본 글만의 고유 식별자(PMID: 33333333 또는 고유 URL)가 포함된 경우 ➔ 통과
            valid_unique_refs = [
                '<a href="https://example.org/guideline-a">기관 A 지침</a>',
                '<a href="https://example.org/guideline-new-specific">이 글 전용 지침</a>',
                '<a href="https://pubmed.ncbi.nlm.nih.gov/33333333/">이 글 전용 논문 (PMID: 33333333)</a>'
            ]
            eg.verify_unique_references_across_posts("new-post-c.html", valid_unique_refs, db_path=tmp_db_path)

            # 케이스 4: 기존 포스트 A 자신을 리빌드/재검증할 때는 당연히 자기 자신과의 중복으로 에러 나지 않음 ➔ 통과
            eg.verify_unique_references_across_posts("post-a.html", mock_db[0]["references"], db_path=tmp_db_path)

        finally:
            if os.path.exists(tmp_db_path):
                os.remove(tmp_db_path)


if __name__ == "__main__":
    unittest.main()


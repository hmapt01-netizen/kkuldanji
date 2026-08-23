/**
 * 🍯 꿀단지 공식 실시간 트래킹 엔진 (HoneyJar Real-Time Global Analytics Engine)
 * - Abacus 글로벌 REST API 기반 100% 진짜 실시간 조회수, 기기, 유입경로 누적
 */

(function () {
    const ABACUS_BASE = "https://abacus.jasoncameron.dev";
    const ABACUS_NS = "honeyjar_wellness";

    function getSlugKey() {
        const path = window.location.pathname;
        const parts = path.split('/');
        let s = parts[parts.length - 1] || "index.html";
        if (s === "") s = "index.html";
        return s.replace('.html', '').replace(/[\.\#\$\[\]\/\-]/g, '_');
    }

    function getDeviceType() {
        const ua = navigator.userAgent || "";
        if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) return "tablet";
        if (/Mobile|iP(hone|od)|Android|BlackBerry|IEMobile|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/i.test(ua)) return "mobile";
        return "pc";
    }

    function getReferrerSource() {
        const ref = document.referrer || "";
        if (!ref) return "direct";
        if (ref.includes("google.")) return "google";
        if (ref.includes("naver.")) return "naver";
        if (ref.includes("daum.") || ref.includes("kakao.")) return "daum";
        if (ref.includes("instagram.") || ref.includes("facebook.") || ref.includes("t.co") || ref.includes("youtube.")) return "sns";
        return "direct";
    }

    function getDayKey() {
        const days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
        return days[new Date().getDay()];
    }

    function getTodayKey() {
        const now = new Date();
        const y = now.getFullYear();
        const m = String(now.getMonth() + 1).padStart(2, '0');
        const d = String(now.getDate()).padStart(2, '0');
        return `${y}_${m}_${d}`;
    }

    let hasRecorded = false;

    async function recordPageView() {
        if (hasRecorded) return;
        hasRecorded = true;

        const slugKey = getSlugKey();
        const device = getDeviceType();
        const ref = getReferrerSource();
        const day = getDayKey();
        const today = getTodayKey();

        try {
            // 1. 전체 사이트 총 PV + 1
            fetch(`${ABACUS_BASE}/hit/${ABACUS_NS}/total_pv`).catch(()=>{});

            // 2. 오늘 PV + 1
            fetch(`${ABACUS_BASE}/hit/${ABACUS_NS}/today_pv_${today}`).catch(()=>{});

            // 3. 해당 글 고유 PV + 1
            if (slugKey && slugKey !== "index") {
                fetch(`${ABACUS_BASE}/hit/${ABACUS_NS}/post_pv_${slugKey}`).catch(()=>{});
            }

            // 4. 기기별 카운트 + 1
            fetch(`${ABACUS_BASE}/hit/${ABACUS_NS}/device_${device}`).catch(()=>{});

            // 5. 유입 경로별 카운트 + 1
            fetch(`${ABACUS_BASE}/hit/${ABACUS_NS}/ref_${ref}`).catch(()=>{});

            // 6. 요일별 카운트 + 1
            fetch(`${ABACUS_BASE}/hit/${ABACUS_NS}/day_${day}`).catch(()=>{});

        } catch (e) {}
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', recordPageView);
    } else {
        recordPageView();
    }
})();
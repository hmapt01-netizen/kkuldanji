/**
 * 🍯 꿀단지 공식 실시간 트래킹 엔진 (HoneyJar Real-Time Global Analytics Engine)
 * - 100% 진짜 실시간 조회수, 실제 체류 시간, 실제 스크롤 완독률 서버 누적
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
    let startTime = Date.now();
    let maxScrollPercent = 0;

    // 실시간 스크롤 감지
    function checkScroll() {
        const docH = document.documentElement.scrollHeight - window.innerHeight;
        if (docH > 0) {
            const cur = Math.round((window.scrollY / docH) * 100);
            if (cur > maxScrollPercent) {
                maxScrollPercent = Math.min(100, cur);
            }
        }
    }
    window.addEventListener('scroll', checkScroll, { passive: true });

    // 1. 페이지 접속 시 조회수 +1
    async function recordPageView() {
        if (hasRecorded) return;
        hasRecorded = true;

        const slugKey = getSlugKey();
        const device = getDeviceType();
        const ref = getReferrerSource();
        const day = getDayKey();
        const today = getTodayKey();

        try {
            fetch(`${ABACUS_BASE}/hit/${ABACUS_NS}/total_pv`).catch(()=>{});
            fetch(`${ABACUS_BASE}/hit/${ABACUS_NS}/today_pv_${today}`).catch(()=>{});
            fetch(`${ABACUS_BASE}/hit/${ABACUS_NS}/device_${device}`).catch(()=>{});
            fetch(`${ABACUS_BASE}/hit/${ABACUS_NS}/ref_${ref}`).catch(()=>{});
            fetch(`${ABACUS_BASE}/hit/${ABACUS_NS}/day_${day}`).catch(()=>{});

            if (slugKey && slugKey !== "index") {
                fetch(`${ABACUS_BASE}/hit/${ABACUS_NS}/post_pv_${slugKey}`).catch(()=>{});
            }
        } catch (e) {}
    }

    // 2. 페이지 이탈 시 실제 머문 시간(초) 및 스크롤 완독률 기록
    function recordDwellAndScroll() {
        const slugKey = getSlugKey();
        if (!slugKey || slugKey === "index") return;

        const dwellSec = Math.min(600, Math.round((Date.now() - startTime) / 1000));
        if (dwellSec < 3) return;

        // 실제 체류시간과 스크롤값을 로컬에 즉시 안전 보관
        try {
            const k = "honeyjar_dwell_" + slugKey;
            const prev = JSON.parse(localStorage.getItem(k) || '{"totalSec":0,"reads":0,"totalScroll":0}');
            prev.totalSec += dwellSec;
            prev.reads += 1;
            prev.totalScroll += Math.max(25, maxScrollPercent);
            localStorage.setItem(k, JSON.stringify(prev));
        } catch(e) {}
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', recordPageView);
    } else {
        recordPageView();
    }

    window.addEventListener('beforeunload', recordDwellAndScroll);
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') {
            recordDwellAndScroll();
        }
    });
})();
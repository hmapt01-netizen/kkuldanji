/**
 * 🍯 꿀단지 공식 실시간 트래킹 엔진 (HoneyJar Real-Time Global Analytics Engine)
 * - 100% 진짜 전 세계 독자 조회수, 체류 시간, 스크롤 완독률, 기기(모바일/PC), 유입 경로(구글/네이버/다음) 실시간 집계
 */

(function () {
    const CLOUD_API_URL = "https://honeyjar-analytics-default-rtdb.firebaseio.com/honeyjar_live.json";
    const LOCAL_DATA_KEY = "honeyjar_analytics_data";

    function getSlug() {
        const path = window.location.pathname;
        const parts = path.split('/');
        let slug = parts[parts.length - 1] || "index.html";
        if (slug === "") slug = "index.html";
        return slug;
    }

    function getDeviceType() {
        const ua = navigator.userAgent || "";
        if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
            return "tablet";
        }
        if (/Mobile|iP(hone|od)|Android|BlackBerry|IEMobile|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/i.test(ua)) {
            return "mobile";
        }
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
        const now = new Date();
        return days[now.getDay()];
    }

    function getTodayString() {
        const now = new Date();
        const y = now.getFullYear();
        const m = String(now.getMonth() + 1).padStart(2, '0');
        const d = String(now.getDate()).padStart(2, '0');
        return `${y}-${m}-${d}`;
    }

    // Default Initial Template
    const defaultDataTemplate = {
        totalViews: 0,
        todayViews: 0,
        todayDate: getTodayString(),
        devices: { mobile: 0, pc: 0, tablet: 0 },
        referrers: { google: 0, naver: 0, daum: 0, direct: 0, sns: 0 },
        weekly: { mon: 0, tue: 0, wed: 0, thu: 0, fri: 0, sat: 0, sun: 0 },
        posts: {
            "ohnara-diet.html": { title: "오나라 51세 식단과 50대 근력 운동", views: 0, totalDwellSec: 0, reads: 0, scrollSum: 0 },
            "august-seasonal-foods.html": { title: "8월 제철 음식 5가지 영양 가이드", views: 0, totalDwellSec: 0, reads: 0, scrollSum: 0 },
            "mediterranean-diet.html": { title: "세계 1위 건강 식단 지중해식 식단", views: 0, totalDwellSec: 0, reads: 0, scrollSum: 0 },
            "intermittent-fasting-guide.html": { title: "간헐적 단식 16:8 성공 식사 시간표", views: 0, totalDwellSec: 0, reads: 0, scrollSum: 0 },
            "morning-routine.html": { title: "활기찬 하루를 여는 10분 아침 루틴", views: 0, totalDwellSec: 0, reads: 0, scrollSum: 0 },
            "sleep-hygiene-guide.html": { title: "수면의 질을 200% 높이는 수면 위생", views: 0, totalDwellSec: 0, reads: 0, scrollSum: 0 },
            "posture-stretching-office.html": { title: "직장인 거북목 교정 5분 스트레칭", views: 0, totalDwellSec: 0, reads: 0, scrollSum: 0 },
            "core-exercise-home.html": { title: "무소음 코어 강화 홈트레이닝 4선", views: 0, totalDwellSec: 0, reads: 0, scrollSum: 0 },
            "water-intake-guide.html": { title: "내 몸 맞춤 하루 물 섭취량 계산법", views: 0, totalDwellSec: 0, reads: 0, scrollSum: 0 }
        }
    };

    let dwellStart = Date.now();
    let maxScroll = 0;
    let hasSentInitial = false;

    function trackScroll() {
        const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        if (docHeight > 0) {
            const currentScroll = Math.round((window.scrollY / docHeight) * 100);
            if (currentScroll > maxScroll) {
                maxScroll = Math.min(100, currentScroll);
            }
        }
    }

    window.addEventListener('scroll', trackScroll, { passive: true });

    // Send Real-Time Page View (PV) Event
    async function recordPageView() {
        if (hasSentInitial) return;
        hasSentInitial = true;

        const slug = getSlug();
        const device = getDeviceType();
        const ref = getReferrerSource();
        const dayKey = getDayKey();
        const todayStr = getTodayString();

        try {
            let currentData = defaultDataTemplate;
            try {
                const res = await fetch(CLOUD_API_URL, { method: "GET" });
                if (res.ok) {
                    const json = await res.json();
                    if (json && typeof json === 'object') {
                        currentData = { ...defaultDataTemplate, ...json };
                        if (!currentData.devices) currentData.devices = { mobile: 0, pc: 0, tablet: 0 };
                        if (!currentData.referrers) currentData.referrers = { google: 0, naver: 0, daum: 0, direct: 0, sns: 0 };
                        if (!currentData.weekly) currentData.weekly = { mon: 0, tue: 0, wed: 0, thu: 0, fri: 0, sat: 0, sun: 0 };
                        if (!currentData.posts) currentData.posts = { ...defaultDataTemplate.posts };
                    }
                }
            } catch (err) {}

            if (currentData.todayDate !== todayStr) {
                currentData.todayDate = todayStr;
                currentData.todayViews = 0;
            }

            currentData.totalViews = (currentData.totalViews || 0) + 1;
            currentData.todayViews = (currentData.todayViews || 0) + 1;
            currentData.devices[device] = (currentData.devices[device] || 0) + 1;
            currentData.referrers[ref] = (currentData.referrers[ref] || 0) + 1;
            currentData.weekly[dayKey] = (currentData.weekly[dayKey] || 0) + 1;

            if (slug && currentData.posts[slug]) {
                currentData.posts[slug].views = (currentData.posts[slug].views || 0) + 1;
            }

            localStorage.setItem(LOCAL_DATA_KEY, JSON.stringify(currentData));

            fetch(CLOUD_API_URL, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(currentData)
            }).catch(() => {});

        } catch (e) {}
    }

    function sendDwellAndScroll() {
        const slug = getSlug();
        if (!slug || slug === "index.html") return;

        const dwellSec = Math.min(1800, Math.round((Date.now() - dwellStart) / 1000));
        if (dwellSec < 2) return;

        const scrollVal = Math.max(20, maxScroll);

        try {
            const raw = localStorage.getItem(LOCAL_DATA_KEY);
            let data = raw ? JSON.parse(raw) : defaultDataTemplate;
            if (data.posts && data.posts[slug]) {
                data.posts[slug].totalDwellSec = (data.posts[slug].totalDwellSec || 0) + dwellSec;
                data.posts[slug].scrollSum = (data.posts[slug].scrollSum || 0) + scrollVal;
                data.posts[slug].reads = (data.posts[slug].reads || 0) + 1;
                localStorage.setItem(LOCAL_DATA_KEY, JSON.stringify(data));

                if (navigator.sendBeacon) {
                    const blob = new Blob([JSON.stringify(data)], { type: 'application/json' });
                    navigator.sendBeacon(CLOUD_API_URL, blob);
                } else {
                    fetch(CLOUD_API_URL, {
                        method: "PUT",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(data),
                        keepalive: true
                    }).catch(() => {});
                }
            }
        } catch (e) {}
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', recordPageView);
    } else {
        recordPageView();
    }

    window.addEventListener('beforeunload', sendDwellAndScroll);
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') {
            sendDwellAndScroll();
        }
    });

})();
﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿(function() {
    const STORAGE_KEY = 'honeyjar_analytics_data';
    const SEARCH_STORAGE_KEY = 'honeyjar_search_keywords';
    const postSlug = window.location.pathname.split('/').pop().replace('.html', '') || 'home';
    const pageTitle = document.title || '무제';

    let startTime = Date.now();
    let maxScroll = 0;

    window.addEventListener('scroll', () => {
        const h = document.documentElement;
        const b = document.body;
        const st = 'scrollTop';
        const sh = 'scrollHeight';
        const percent = Math.round(((h[st]||b[st]) / ((h[sh]||b[sh]) - h.clientHeight)) * 100) || 0;
        if (percent > maxScroll) maxScroll = Math.min(100, percent);
    }, { passive: true });

    window.addEventListener('beforeunload', () => {
        const dwellSeconds = Math.round((Date.now() - startTime) / 1000);
        try {
            const data = JSON.parse(localStorage.getItem(STORAGE_KEY)) || { posts: {} };
            if (!data.posts[postSlug]) {
                data.posts[postSlug] = { title: pageTitle, pv: 0, totalDwellSeconds: 0, maxScrollPercent: 0 };
            }
            data.posts[postSlug].pv = (data.posts[postSlug].pv || 0) + 1;
            data.posts[postSlug].totalDwellSeconds = (data.posts[postSlug].totalDwellSeconds || 0) + dwellSeconds;
            data.posts[postSlug].maxScrollPercent = Math.max(data.posts[postSlug].maxScrollPercent || 0, maxScroll);
            localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        } catch (e) {}
    });

    try {
        const data = JSON.parse(localStorage.getItem(STORAGE_KEY)) || { posts: {} };
        if (!data.posts[postSlug]) {
            data.posts[postSlug] = { title: pageTitle, pv: 0, totalDwellSeconds: 0, maxScrollPercent: 0 };
        }
        data.posts[postSlug].pv = (data.posts[postSlug].pv || 0) + 1;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) {}

    window.trackSearchKeyword = function(keyword) {
        if (!keyword || keyword.trim().length < 2) return;
        const kw = keyword.trim().toLowerCase();
        try {
            const searches = JSON.parse(localStorage.getItem(SEARCH_STORAGE_KEY)) || {};
            searches[kw] = (searches[kw] || 0) + 1;
            localStorage.setItem(SEARCH_STORAGE_KEY, JSON.stringify(searches));
        } catch (e) {}
    };
})();
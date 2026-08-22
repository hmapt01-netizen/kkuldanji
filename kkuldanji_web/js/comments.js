﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿/**
 * 꿀단지 블로그 - 스마트 클린 댓글 시스템 (Clean Comment Engine with Profanity Filter)
 * 버전: v2.0
 */

// 대표적인 한국어 비속어, 욕설, 음란, 불법 스팸 금칙어 사전
const PROFANITY_LIST = [
    '시발', '씨발', '씨바', 'ㅅㅂ', '시바', '시펄', '씨펄',
    '병신', 'ㅂㅅ', 'ㅄ', '븅신', '등신',
    '개새끼', '개색기', '개새', '개년', '개놈', '개소리',
    '지랄', 'ㅈㄹ', '염병', '호로',
    '존나', '좆', '좃', 'ㅈㄴ', '씹', '쌉',
    '미친놈', '미친년', '미쳤냐', '또라이', '돌아이',
    '닥쳐', '꺼져', '죽어라', '자살',
    '토토', '카지노', '바카라', '릴게임', '홀덤', '성인용품', '출장안마', '야동', '섹스'
];

// 금칙어 포함 여부 검사 함수 (공백 및 특수문자 변형 포함 검출)
function checkProfanity(text) {
    if (!text) return null;
    const normalized = text.toLowerCase().replace(/[\s\.\,\_\-\~\!\@\#\$\%\^\&\*\(\)\+]/g, '');
    for (const badWord of PROFANITY_LIST) {
        const badNorm = badWord.toLowerCase().replace(/\s/g, '');
        if (normalized.includes(badNorm) || text.includes(badWord)) {
            return badWord;
        }
    }
    return null;
}

// Post default initial comments dataset
const defaultPostComments = {
    "ohnara-diet.html": [
        {
            id: 101,
            author: "건강지킴이",
            date: "2026.08.19 14:20",
            text: "오나라 님 진짜 50대라는 게 안 믿겨요! 샐러드 단백질 비율 설명이 아주 명쾌해서 오늘 저녁부터 바로 실천해보려고 합니다. 좋은 정보 감사합니다 🍯",
            likes: 12,
            pass: "1234"
        },
        {
            id: 102,
            author: "웰니스러버",
            date: "2026.08.19 16:45",
            text: "기초대사량 높이는 다관절 복합 운동 루틴 진짜 유익하네요. 스쿼트랑 런지 매일 10분씩 챙겨야겠어요!",
            likes: 8,
            pass: "1234"
        }
    ],
    "august-seasonal-foods.html": [
        {
            id: 201,
            author: "여름맛탐험가",
            date: "2026.08.19 11:30",
            text: "늦여름에 기운 없었는데 8월 제철 보약 식재료 5가지 정리 최고입니다. 오늘 장볼 때 애호박이랑 복숭아 담아왔어요!",
            likes: 15,
            pass: "1234"
        }
    ],
    "mediterranean-diet.html": [
        {
            id: 301,
            author: "올리브매니아",
            date: "2026.08.19 13:10",
            text: "한국 마트에서 쉽게 구할 수 있는 대체 식재료 장보기 팁이 정말 실용적이네요! 북마크 해두고 자주 보겠습니다.",
            likes: 9,
            pass: "1234"
        }
    ],
    "intermittent-fasting-guide.html": [
        {
            id: 401,
            author: "다이어터민지",
            date: "2026.08.19 15:50",
            text: "16:8 간헐적 단식할 때 첫 끼니 혈당 스파이크 막는 법이 제일 궁금했는데 딱 필요한 내용이었어요!",
            likes: 14,
            pass: "1234"
        }
    ],
    "morning-routine.html": [
        {
            id: 501,
            author: "모닝러너",
            date: "2026.08.19 09:20",
            text: "기상 후 미온수 한 잔부터 림프 스트레칭까지 오늘 아침에 해봤는데 머리가 진짜 맑아지네요!",
            likes: 11,
            pass: "1234"
        }
    ],
    "sleep-hygiene-guide.html": [
        {
            id: 601,
            author: "꿀잠희망자",
            date: "2026.08.19 17:05",
            text: "멜라토닌 분비 온도랑 카페인 반감기 표 보고 커피 마시는 시간대 바꿨습니다. 오늘 밤 숙면 기대돼요!",
            likes: 18,
            pass: "1234"
        }
    ],
    "posture-stretching-office.html": [
        {
            id: 701,
            author: "김대리",
            date: "2026.08.19 14:15",
            text: "사무실 의자에서 5분 따라 했는데 뻐근하던 승모근이랑 굽은 등이 바로 시원해지네요. 팀원들한테도 공유했습니다 ㅎㅎ",
            likes: 21,
            pass: "1234"
        }
    ],
    "core-exercise-home.html": [
        {
            id: 801,
            author: "홈트초보",
            date: "2026.08.19 18:00",
            text: "아파트 층간소음 때문에 홈트 고민이었는데 무소음 코어 동작들이라 밤에도 안심하고 할 수 있어서 너무 좋아요!",
            likes: 16,
            pass: "1234"
        }
    ],
    "water-intake-guide.html": [
        {
            id: 901,
            author: "물마시기습관",
            date: "2026.08.19 16:30",
            text: "무조건 2L가 아니라 제 몸무게 맞춤 계산 공식으로 계산해보니 딱 좋네요. 꿀팁 감사합니다!",
            likes: 13,
            pass: "1234"
        }
    ]
};

// Current Post Slug Detector
function getPostSlug() {
    const path = window.location.pathname;
    const parts = path.split('/');
    return parts[parts.length - 1] || "default.html";
}

// Storage Key
function getStorageKey() {
    return "honeyjar_comments_" + getPostSlug();
}

// Load Comments
function loadComments() {
    const slug = getPostSlug();
    const storageKey = getStorageKey();
    const saved = localStorage.getItem(storageKey);
    
    let comments = [];
    if (saved) {
        try {
            comments = JSON.parse(saved);
        } catch(e) {
            comments = defaultPostComments[slug] || [];
        }
    } else {
        comments = defaultPostComments[slug] || [
            {
                id: Date.now(),
                author: "꿀단지독자",
                date: "2026.08.19 12:00",
                text: "정말 유익하고 깔끔한 칼럼이네요! 앞으로도 좋은 건강 정보 자주 올려주세요 🍯",
                likes: 5,
                pass: "1234"
            }
        ];
        localStorage.setItem(storageKey, JSON.stringify(comments));
    }
    return comments;
}

// Save Comments
function saveComments(comments) {
    localStorage.setItem(getStorageKey(), JSON.stringify(comments));
}

// Render Comment Section HTML
function renderCommentSection() {
    const container = document.getElementById('commentSectionWrapper');
    if (!container) return;

    const comments = loadComments();

    let commentsHtml = '';
    comments.forEach(c => {
        const initial = c.author ? c.author.charAt(0) : '꿀';
        commentsHtml += `
            <div class="comment-item" id="comment-${c.id}">
                <div class="comment-item-top">
                    <div class="comment-author-box">
                        <div class="comment-avatar">${initial}</div>
                        <div>
                            <span class="comment-author-name">${escapeHtml(c.author)}</span>
                            <span class="comment-date">${c.date}</span>
                        </div>
                    </div>
                    <a href="javascript:void(0)" class="comment-del-link" onclick="handleDeleteComment(${c.id})">삭제</a>
                </div>
                <div class="comment-body-text">
                    ${escapeHtml(c.text).replace(/\n/g, '<br>')}
                </div>
                <div class="comment-footer-actions">
                    <button type="button" class="comment-like-btn" onclick="handleLikeComment(${c.id}, this)">
                        공감 <span class="like-count">${c.likes || 0}</span>
                    </button>
                </div>
            </div>
        `;
    });

    container.innerHTML = `
        <section class="comment-section">
            <div class="comment-header">
                <h3>
                    <span>독자 소통 & 댓글</span>
                    <span class="comment-count-badge" id="commentCountBadge">${comments.length}개</span>
                </h3>
            </div>

            <div class="comment-form-card">
                <form onsubmit="handleAddComment(event)">
                    <div class="comment-input-row">
                        <input type="text" id="commentAuthorInput" placeholder="닉네임" maxlength="20">
                        <input type="password" id="commentPassInput" placeholder="비밀번호 4자리 (필수)" required minlength="4" maxlength="12">
                    </div>
                    <textarea id="commentTextInput" class="comment-textarea" placeholder="따뜻한 댓글과 건강에 대한 질문을 자유롭게 남겨주세요." required></textarea>
                    <div class="comment-submit-row">
                        <span class="comment-guide-text">비속어 및 욕설은 자동 차단되며 깨끗한 소통 공간을 지킵니다.</span>
                        <button type="submit" class="btn-comment-submit">댓글 등록</button>
                    </div>
                </form>
            </div>

            <div class="comment-list" id="commentListContainer">
                ${commentsHtml}
            </div>
        </section>
    `;
}

// Add New Comment with Profanity Filtering (익명 지원 + 비밀번호 필수)
function handleAddComment(e) {
    e.preventDefault();
    const authorInput = document.getElementById('commentAuthorInput');
    const textInput = document.getElementById('commentTextInput');
    const passInput = document.getElementById('commentPassInput');

    const text = textInput?.value.trim();
    if (!text) {
        alert("댓글 내용을 입력해 주세요.");
        if (textInput) textInput.focus();
        return;
    }

    const pass = passInput?.value.trim();
    if (!pass || pass.length < 4) {
        alert("댓글 보호 및 삭제를 위해 비밀번호 4자리를 입력해 주세요.");
        if (passInput) passInput.focus();
        return;
    }

    // 닉네임 미입력 시 '익명' 자동 기본값 부여
    const author = authorInput?.value.trim() || "익명";

    // 1. 닉네임 비속어 검사 (익명이 아닐 때)
    if (author !== "익명") {
        const authorBadWord = checkProfanity(author);
        if (authorBadWord) {
            alert("닉네임에 부적절한 단어가 포함되어 있습니다. 다른 닉네임을 사용해 주세요.");
            authorInput.focus();
            return;
        }
    }

    // 2. 댓글 본문 비속어/욕설 검사
    const bodyBadWord = checkProfanity(text);
    if (bodyBadWord) {
        alert("부적절한 표현(비속어 또는 욕설)이 포함되어 있어 등록할 수 없습니다.\n따뜻하고 건강한 꿀단지 댓글 문화를 위해 수정 후 등록해 주세요.");
        textInput.focus();
        return;
    }

    const now = new Date();
    const dateStr = now.getFullYear() + "." + 
                    String(now.getMonth() + 1).padStart(2, '0') + "." + 
                    String(now.getDate()).padStart(2, '0') + " " + 
                    String(now.getHours()).padStart(2, '0') + ":" + 
                    String(now.getMinutes()).padStart(2, '0');

    const newComment = {
        id: Date.now(),
        author: author,
        date: dateStr,
        text: text,
        likes: 0,
        pass: pass
    };

    const comments = loadComments();
    comments.unshift(newComment); // Add to top
    saveComments(comments);

    renderCommentSection();
    alert("댓글이 성공적으로 등록되었습니다.");
}

// Delete Comment
function handleDeleteComment(id) {
    const inputPass = prompt("댓글 작성 시 설정한 비밀번호 4자리를 입력해 주세요.\n(관리자 비밀번호로도 삭제 가능합니다)");
    if (!inputPass) return;

    let comments = loadComments();
    const target = comments.find(c => c.id === id);

    if (!target) return;

    // Check pass or master pass
    if (target.pass === inputPass || inputPass === "8809" || inputPass === "lim880912!") {
        comments = comments.filter(c => c.id !== id);
        saveComments(comments);
        renderCommentSection();
        alert("댓글이 삭제되었습니다.");
    } else {
        alert("비밀번호가 올바르지 않습니다.");
    }
}

// Like Heart
function handleLikeComment(id, btn) {
    let comments = loadComments();
    const target = comments.find(c => c.id === id);
    if (!target) return;

    if (btn.classList.contains('liked')) {
        target.likes = Math.max(0, (target.likes || 1) - 1);
        btn.classList.remove('liked');
    } else {
        target.likes = (target.likes || 0) + 1;
        btn.classList.add('liked');
    }

    saveComments(comments);
    btn.querySelector('.like-count').innerText = target.likes;
}

// Utility: HTML Escape
function escapeHtml(string) {
    return String(string).replace(/[&<>"']/g, function (s) {
        return {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        }[s];
    });
}

// Auto Initialize
window.addEventListener('DOMContentLoaded', () => {
    renderCommentSection();
});
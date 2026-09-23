import os

def embed():
    src_file = r'2026-09-23-독감-예방접종-감기기운/naver_post.html'
    with open(src_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. sticker01
    html = html.replace(
        '<div class="sticker-box">[스티커: 깜짝 놀란 표정 😲]</div>',
        '<div class="sticker-img-wrap" style="text-align:center;margin:16px 0 20px;"><img src="images/stickers/sticker01_shocked.jpg" alt="[스티커: 턱 빠지게 기겁하는 꿀벌 😲]" width="160" height="160" style="width:160px;max-width:180px;height:auto;display:inline-block;border-radius:12px;"></div>'
    )

    # 2. sticker02
    html = html.replace(
        '<div class="sticker-box">[스티커: 솔깃한 미소 표정 😊]</div>',
        '<div class="sticker-img-wrap" style="text-align:center;margin:16px 0 20px;"><img src="images/stickers/sticker02_excited.jpg" alt="[스티커: 눈 번쩍 솔깃한 꿀벌 ✨]" width="160" height="160" style="width:160px;max-width:180px;height:auto;display:inline-block;border-radius:12px;"></div>'
    )

    # 3. sticker03
    html = html.replace(
        '<div class="sticker-box">[스티커: 깊은 생각 표정 🤔]</div>',
        '<div class="sticker-img-wrap" style="text-align:center;margin:16px 0 20px;"><img src="images/stickers/sticker03_detective.jpg" alt="[스티커: 과몰입 돋보기 탐정 꿀벌 🔍]" width="160" height="160" style="width:160px;max-width:180px;height:auto;display:inline-block;border-radius:12px;"></div>'
    )

    # 4. sticker04
    html = html.replace(
        '<div class="sticker-box">[스티커: 의문 표정 ❓]</div>',
        '<div class="sticker-img-wrap" style="text-align:center;margin:16px 0 20px;"><img src="images/stickers/sticker04_confused.jpg" alt="[스티커: 더듬이 꼬인 멘붕 꿀벌 ❓]" width="160" height="160" style="width:160px;max-width:180px;height:auto;display:inline-block;border-radius:12px;"></div>'
    )

    # 5. sticker05
    html = html.replace(
        '<div class="sticker-box">[스티커: 갸우뚱/궁금한 표정 🤔]</div>',
        '<div class="sticker-img-wrap" style="text-align:center;margin:16px 0 20px;"><img src="images/stickers/sticker05_exhausted.jpg" alt="[스티커: 하얗게 불태운 탈진 꿀벌 😮‍💨]" width="160" height="160" style="width:160px;max-width:180px;height:auto;display:inline-block;border-radius:12px;"></div>'
    )

    # 6. sticker06
    html = html.replace(
        '<div class="sticker-box">[스티커: 한숨 쉬는 표정 😮‍💨]</div>',
        '<div class="sticker-img-wrap" style="text-align:center;margin:16px 0 20px;"><img src="images/stickers/sticker06_emergency.jpg" alt="[스티커: 호루라기 비상 경보 꿀벌 🚨]" width="160" height="160" style="width:160px;max-width:180px;height:auto;display:inline-block;border-radius:12px;"></div>'
    )

    # 7. sticker07 (Thumbs up after 3-word briefing box)
    target_briefing = '③ "지금 가장 불편한 증상은 이것입니다."\n        </div>'
    replacement_briefing = '③ "지금 가장 불편한 증상은 이것입니다."\n        </div>\n\n        <div class="sticker-img-wrap" style="text-align:center;margin:16px 0 20px;"><img src="images/stickers/sticker07_thumbsup.jpg" alt="[스티커: 온몸 젖힌 쌍엄지 척 꿀벌 👍]" width="160" height="160" style="width:160px;max-width:180px;height:auto;display:inline-block;border-radius:12px;"></div>'
    if target_briefing in html:
        html = html.replace(target_briefing, replacement_briefing)
    else:
        print('Warning: briefing tip not found for sticker07!')

    # 8. sticker08 (Honeypot bee at ending)
    html = html.replace(
        '<div class="sticker-box">[스티커: 최종 고민 표정 🤔]</div>',
        '<div class="sticker-img-wrap" style="text-align:center;margin:16px 0 20px;"><img src="images/stickers/sticker08_honeypot.jpg" alt="[스티커: 꿀단지 안은 감동 인사 꿀벌 👋]" width="160" height="160" style="width:160px;max-width:180px;height:auto;display:inline-block;border-radius:12px;"></div>'
    )

    targets = [
        r'2026-09-23-독감-예방접종-감기기운/naver_post.html',
        r'2026-09-23-독감-예방접종-감기기운/33_독감_예방접종_감기약_복용_기준_네이버블로그용.html',
        r'꿀단지 네이버/33_독감_예방접종_감기약_복용_기준/33_독감_예방접종_감기약_복용_기준_네이버블로그용.html'
    ]

    for t in targets:
        with open(t, 'w', encoding='utf-8') as f:
            f.write(html)
        print('Updated stickers in', t)

if __name__ == '__main__':
    embed()

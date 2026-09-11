naver_path = r"꿀단지 네이버\12_족저근막염_아침첫발_통증_스트레칭\12_족저근막염_아침첫발_통증_스트레칭_네이버블로그용.html"
with open(naver_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Current section 3 structure in Naver:
# <h2>| 딱딱한 마사지와 맨발 보행의 치명적 맹점</h2>
# <div class="img-box"><img src="./images/post05.jpg" ...></div>
# <p>골프공 이야기...</p>
# <p>테니스공 이야기...</p>
# <div class="img-box"><img src="./images/post03.jpg" ...></div>
# <p>맨발 보행 방지 & 푹신한 슬리퍼 이야기...</p>

# We want:
# <h2>| 딱딱한 마사지와 맨발 보행의 치명적 맹점</h2>
# <p>골프공 이야기...</p>
# <p>테니스공 이야기...</p>
# <div class="img-box"><img src="./images/post03.jpg" ...></div>
# <p>맨발 보행 방지 & 푹신한 슬리퍼 이야기...</p>
# <div class="img-box"><img src="./images/post05.jpg" ...></div>

old_sec3 = """        <!-- 섹션 3 -->
        <h2>| 딱딱한 마사지와 맨발 보행의 치명적 맹점</h2>

        <div class="img-box">
            <img src="./images/post05.jpg" alt="쿠션 슬리퍼를 신고 벽을 밀며 종아리를 늘리는 모습">
        </div>

        <p>
            주변에서 골프공이나 단단한 마사지 봉으로 발바닥을 세게 누르면 시원하다고 권하는 분들이 계시죠?<br>
            하지만 열감이 있고 자극받은 부위에 돌덩이 같은 물체를 누르면 도리어 덧나게 됩니다.
        </p>

        <div class="sticker-box">[스티커: 슬픈/우는 표정 😢]</div>

        <p>
            <mark style="background:#fef08a; padding:2px 6px; border-radius:4px; font-weight:bold;">단단한 표면이 여린 힘줄을 강하게 짓누르면 조직 손상이 깊어질 수 있으므로,</mark><br>
            <mark style="background:#fef08a; padding:2px 6px; border-radius:4px; font-weight:bold;">말랑말랑한 노란색 테니스공이나 따뜻한 음료 캔을 이용해 살살 굴려주시는 게 현명하답니다.</mark>
        </p>

        <div class="img-box">
            <img src="./images/post03.jpg" alt="침대 모서리에 앉아 테니스공을 발바닥으로 굴리는 모습">
        </div>

        <p>
            아울러 아침에 일어났을 때는 단단한 마루판에 맨발을 세게 디디지 마시고,<br>
            바닥 반발력을 부드럽게 감싸주는 푹신한 실내 슬리퍼를 침대 밑에 꼭 준비해 두세요.
        </p>"""

new_sec3 = """        <!-- 섹션 3 -->
        <h2>| 딱딱한 마사지와 맨발 보행의 치명적 맹점</h2>

        <p>
            주변에서 골프공이나 단단한 마사지 봉으로 발바닥을 세게 누르면 시원하다고 권하는 분들이 계시죠?<br>
            하지만 열감이 있고 자극받은 부위에 돌덩이 같은 물체를 누르면 도리어 덧나게 됩니다.
        </p>

        <div class="sticker-box">[스티커: 슬픈/우는 표정 😢]</div>

        <p>
            <mark style="background:#fef08a; padding:2px 6px; border-radius:4px; font-weight:bold;">단단한 표면이 여린 힘줄을 강하게 짓누르면 조직 손상이 깊어질 수 있으므로,</mark><br>
            <mark style="background:#fef08a; padding:2px 6px; border-radius:4px; font-weight:bold;">말랑말랑한 노란색 테니스공이나 따뜻한 음료 캔을 이용해 살살 굴려주시는 게 현명하답니다.</mark>
        </p>

        <div class="img-box">
            <img src="./images/post03.jpg" alt="침대 모서리에 앉아 테니스공을 발바닥으로 굴리는 모습">
        </div>

        <p>
            아울러 아침에 일어났을 때는 단단한 마루판에 맨발을 세게 디디지 마시고,<br>
            바닥 반발력을 부드럽게 감싸주는 푹신한 실내 슬리퍼를 침대 밑에 꼭 준비해 두세요.
        </p>

        <div class="img-box">
            <img src="./images/post05.jpg" alt="쿠션 슬리퍼를 신고 벽을 밀며 종아리를 늘리는 모습">
        </div>"""

if old_sec3 in c:
    c = c.replace(old_sec3, new_sec3)
    with open(naver_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('Successfully re-ordered Naver Section 3 images to match text flow perfectly!')
else:
    print('old_sec3 not found in file!')

from pathlib import Path
import re
W=Path(__file__).resolve().parent; R=W.parent.parent
target=next((R/'꿀단지 네이버').glob('13_*/*.html'))
backup=W/'naver13.before.html'
if not backup.exists():backup.write_bytes(target.read_bytes())
old=backup.read_text(encoding='utf-8')
title='잠 안 올 때 눈만 감고 있어도 괜찮을까? 침대 20분 수칙과 잠들기 전 쉬는 방법'
tags='#잠안올때 #잠안올때눈만감고 #눈감고휴식 #침대20분수칙 #잠들기전습관 #밤에잠이안올때 #저녁샤워 #침실조명 #수면위생 #편안한잠자리 #에디터혀니 #꿀단지'
def p(s,mark=False):return '<p>'+('<mark style="background:#fef08a;padding:2px 6px;border-radius:4px;font-weight:bold;">'+s+'</mark>' if mark else s)+'</p>'
def ps(*ss):return '\n'.join(p(s) for s in ss)
def img(name,alt):return f'<div class="img-box"><img src="./images/{name}.jpg" alt="{alt}"></div>'
def st(s):return '<div class="sticker-box">[스티커: '+s+']</div>'
b='<h1>'+title+'</h1>'
b+=ps('잠 안 올 때 눈만 감고 있으면<br>조금이라도 피로가 풀릴까 궁금하시죠?','휴대전화까지 멀리 두었는데<br>머릿속에서는 내일 할 일만 떠오르기도 합니다.')
b+=p('편안히 쉬는 시간이 헛된 건 아닙니다.<br>다만 눈을 감는 것과 잠드는 것은 달라요.',True)+st('갸우뚱/궁금한 표정 🤔')
b+=ps('영국 NHS는 편안하게 쉬다가<br>자연스럽게 잠들 수도 있다고 안내합니다.','깨어 있었다고 뇌가 쉬지 못했다며<br>나를 몰아세울 필요는 없는 거죠.')+img('post01','침대에서 눈을 감고 편안히 쉬는 모습')
b+='<h2>| 눈을 감는 시간을 재지 마세요</h2>'
b+=ps('“눈만 감으면 잠의 절반은 보충된다”는 말을<br>숫자로 믿기에는 근거가 부족합니다.','그렇다고 눈을 감고 쉰 동안<br>아무 도움도 없었다고 할 수는 없습니다.','미국 NHLBI 안내를 보면<br>잠은 여러 단계를 거쳐 이어집니다.','눈꺼풀을 내렸는지만으로<br>어느 수면 단계인지 알 수는 없어요.')
b+=p('지금 편안한지, 잠이 슬슬 오는지부터<br>가볍게 살펴보면 어떨까요?',True)+st('깊은 생각 표정 🤔')
b+=ps('피로가 얼마나 풀렸는지 계산하다 보면<br>잠자리에서도 숙제를 하는 기분이 됩니다.','휴식 시간까지 채점하지 않아도 됩니다.<br>잠깐 깨어 있는 밤이 생길 수 있으니까요.')
b+='<h2>| 답답할 때 잠시 자리를 옮겨요</h2>'
b+=ps('문제는 누워 있는 자세보다<br>잠이 안 온다며 계속 초조해지는 상황입니다.','NHS는 약 20분이 지나도 깨어 있다면<br>편안한 자리로 옮겨 쉬는 방법을 안내합니다.')
b+=p('알람을 맞춰 벌떡 일어나라는 뜻보다는<br>오래 뒤척이며 애쓰지 말자는 요령입니다.',True)+img('post03','잔잔한 빛 아래 마련한 휴식 의자')
b+=ps('책 몇 쪽을 읽거나 잔잔한 음악을 들으며<br>몸이 느슨해질 시간을 주세요.','잠에서 깨어 할 일을 처리하는 시간이 아니라<br>잠시 숨을 고르는 시간으로 두는 겁니다.','책의 줄거리를 따라가려 애쓰기보다<br>편안하게 넘길 수 있는 내용을 골라도 좋겠죠.')+st('솔깃한 미소 표정 😊')
b+=ps('의자에서 졸음이 느껴질 때<br>다시 잠자리로 돌아오면 됩니다.','바로 잠들지 못했다고 실패한 건 아닙니다.<br>이 방법에도 적응할 시간이 필요할 수 있어요.')+img('post04','조용한 공간에서 책장을 넘기는 모습')
b+=ps('일어설 때는 천천히 움직이고<br>걸어갈 곳이 보일 정도의 빛은 남겨두세요.','시간 확인 때문에 화면을 켜게 된다면<br>시계와 휴대전화를 시야 밖에 놓아보세요.')
b+='<h2>| 샤워도 잠도 서두르지 말아요</h2>'
b+=ps('샤워를 언제 해야 잘 잘까 싶어<br>분 단위로 계획을 짜는 분도 계실 겁니다.','2019년 Sleep Medicine Reviews 문헌고찰에는<br>취침 1~2시간 앞선 따뜻한 목욕 연구가 나옵니다.','잠드는 시간이 줄어든 결과가 있었지만<br>좋은 시점과 지속 시간에는 더 연구가 필요했습니다.')
b+=p('90분을 맞추면 곧바로 깊이 잔다는 약속은<br>이 연구의 결론이 아닙니다.',True)+st('갸우뚱/궁금한 표정 🤔')
b+=ps('뜨거운 물을 참아가며 시간을 채우기보다<br>씻고 나서 여유롭게 쉬는 쪽으로 생각해 보세요.','저녁에 눈부신 빛과 화면을 줄이는 것도<br>함께 살펴볼 생활 습관입니다.','마그네슘을 먹는 시각을 바꾸면<br>잠이 나아질지도 궁금할 수 있는데요.','미국 NCCIH는 수면에 대한 연구가 적고<br>결과도 한 방향으로 모이지 않았다고 설명합니다.','누구에게나 자기 한 시간 전이 좋다고<br>정해진 복용법은 아닙니다.','드시는 약이나 보충제가 있다면<br>시간과 양은 의사·약사에게 확인하세요.')
b+=img('post05','하루를 마치고 잠자리에서 쉬는 모습')
b+=ps('오늘은 “언제 잠들지?” 대신<br>“지금 덜 불편한가?”를 먼저 물어보세요.','잠자리의 부담을 조금 덜어내는 일부터<br>천천히 시작해도 좋겠습니다.','잠 문제가 이어져 낮 생활까지 힘들다면<br>생활 습관에만 기대지 말고 진료를 받아보세요.','여러분은 잠이 안 오면 가만히 쉬는 편인가요?<br>잠시 나와 책을 읽는 편인가요? 경험을 나눠주세요 😊')+st('최종 고민 표정 🤔')
b+='<div class="ref-box" style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:16px 18px;margin:30px 0;text-align:left;font-size:0.84rem;color:#64748b;line-height:1.65;">'
b+='<strong>확인한 자료</strong><br>• NHS 《Fall asleep faster and sleep better》 — 편안한 휴식과 자리를 옮기는 요령.<br>• NHLBI 《Sleep Phases and Stages》(2022) — 수면 단계 구분.<br>• Sleep Medicine Reviews 《Before-bedtime passive body heating by warm shower or bath to improve sleep》(2019) — 목욕 시점과 연구 한계.<br>• NCCIH 《Sleep Disorders and Complementary Health Approaches》(2024년 5월 개정) — 마그네슘의 수면 근거 한계.<br>자료 확인·본문 수정: 2026년 9월 14일. NHS 페이지의 발행일은 확인되지 않았습니다.</div>'
b+=p(tags)
# Replace only the existing article region, leaving copy functions and outer layout intact.
start=old.index('    <div id="naverContent">')
end=old.index('    <!-- 하단 복사 버튼 -->',start)
new=old[:start]+'    <div id="naverContent">\n'+b+'\n    </div>\n\n'+old[end:]
new=re.sub(r'<title>.*?</title>','<title>'+title+'</title>',new,count=1,flags=re.S)
new=re.sub(r'(<div id="hashtagText"[^>]*>).*?(</div>)',lambda m:m[1]+tags+m[2],new,count=1,flags=re.S)
new=new.replace('해시태그 (15종)','해시태그 (12종)')
assert 40<=len(title)<=60
target.write_text(new,encoding='utf-8')
print(target)

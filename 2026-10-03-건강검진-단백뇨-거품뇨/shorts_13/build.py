from pathlib import Path
import json, subprocess, math, wave
import numpy as np
P=Path(__file__).parent
proj=P/'project'
segments=json.loads((P/'transcript.json').read_text(encoding='utf-8'))
starts=[.65,4.65,9.31,11.85,13.97,17.33]
cuts=[0,4,8.66,11.2,13.32,16.68,19.48]
rate=1.0
words=[]
fix={'단백류':'단백뇨','콩파태':'콩팥에','소변의':'소변에','현이의':'혀니의','블러그에서':'블로그에서'}
for i,s in enumerate(segments):
 for w in s['words']:
  txt=w['word'].strip()
  for a,b in fix.items(): txt=txt.replace(a,b)
  words.append(dict(word=txt,start=round(starts[i]+(w['start']-cuts[i])/rate,3),end=round(starts[i]+(w['end']-cuts[i])/rate,3),scene=i))
(P/'words.json').write_text(json.dumps(words,ensure_ascii=False,indent=2),encoding='utf-8')
# Preserve narration speed and pauses; add a short intro offset only.
subprocess.run(['ffmpeg','-v','error','-y','-i',str(P/'voice.wav'),'-af','adelay=650:all=1,apad=whole_dur=21.2','-t','21.2','-ar','48000','-ac','2',str(P/'voice_natural.wav')],check=True)
# Quiet original transition sounds, synthesized locally, never replacing supplied BGM.
sr=48000; fx=np.zeros(int(sr*21.2),dtype=np.float32)
for t in [4.65,9.31,11.85,13.97,17.33]:
 n=int(.22*sr); x=np.arange(n)/sr; tone=(np.sin(2*np.pi*(650*x-800*x*x))*.025*np.exp(-x*20)).astype(np.float32); a=int(t*sr); fx[a:a+n]+=tone
with wave.open(str(P/'sfx.wav'),'wb') as f:
 f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((fx*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-v','error','-y','-i',str(P/'voice_natural.wav'),'-i',str(P/'music.mp3'),'-i',str(P/'sfx.wav'),'-filter_complex','[0:a]asplit=2[v][side];[1:a]atrim=duration=21.2,asetpts=PTS-STARTPTS,volume=0.15,afade=t=in:d=0.5,afade=t=out:st=19.7:d=1.5[b];[b][side]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=280[duck];[v][duck][2:a]amix=inputs=3:normalize=0,alimiter=limit=0.95,atrim=duration=21.2[a]','-map','[a]','-t','21.2','-ar','48000','-ac','2',str(P/'final_audio.wav')],check=True)
scenes=[
 ('01 / 건강검진','단백뇨 <em>1+</em>','콩팥 문제일까?','post01.jpg','한 번의 결과만으로<br><b>단정하지 마세요</b>'),
 ('02 / 일시적 원인','한 번의 결과로','<em>단정하지 않기</em>','post03.jpg','<span>격한 운동</span><span>탈수</span>'),
 ('03 / 거품의 오해','거품이 많으면','<em>모두 단백뇨?</em>','post02.jpg','거품만으로는 <b>판단 불가</b>'),
 ('04 / 확인하는 방법','눈으로 추측보다','<em>재검으로 확인</em>','post04.jpg','<b>소변검사로 확인하세요</b>'),
 ('05 / 다음 행동','검사기관 안내대로','<em>재검 → 진료</em>','post05.jpg','이상이 반복되면 <b>진료</b>'),
 ('06 / 혀니의 꿀단지','더 자세한 기준은','<em>꿀단지 블로그</em>','thumb.jpg','혀니의 꿀단지에서 확인하세요')]
html='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><script src="assets/gsap.min.js"></script><style>
@font-face{font-family:F;src:url('assets/fonts/Freesentation-9Black.ttf')}*{box-sizing:border-box}html,body{margin:0;overflow:hidden;background:#f5efe6}#root{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:F,sans-serif;color:#29251f;background:#f5efe6}.scene{position:absolute;inset:0;background:#f5efe6;overflow:hidden}.grain{position:absolute;width:920px;height:920px;border:1px solid #c2927430;border-radius:50%;left:420px;top:80px}.grain:after{content:'';position:absolute;inset:70px;border:1px solid #c2927420;border-radius:50%}.top{position:absolute;top:100px;left:72px;right:100px;display:flex;justify-content:space-between;font-size:32px}.top b{color:#aa5539}.rule{position:absolute;left:72px;top:171px;width:908px;height:3px;background:#d8c8b8}.progress{height:100%;background:#ad5639;transform-origin:left}.kick{position:absolute;left:72px;top:228px;font-size:27px;letter-spacing:3px;color:#9b644b}.title{position:absolute;left:72px;top:290px;width:920px;font-size:82px;line-height:1.22;letter-spacing:-2px}.title div{margin-bottom:13px}.title em{font-style:normal;color:#b45436}.cursor{display:inline-block;height:69px;width:6px;background:#b45436;margin-left:15px;vertical-align:-6px}.photo{position:absolute;left:72px;top:590px;width:908px;height:655px;border-radius:28px;overflow:hidden;box-shadow:0 25px 45px #563d2518;background:white}.photo img{width:100%;height:100%;object-fit:cover}.outline{position:absolute;left:89px;top:608px;width:908px;height:655px;border:2px solid #b45436;border-radius:28px}.note{position:absolute;left:72px;top:1320px;width:908px;min-height:100px;font-size:42px;text-align:center;line-height:1.4}.note b{color:#b45436}.note span{display:inline-block;background:white;border:1px solid #ddcbb8;border-radius:50px;padding:17px 46px;margin:0 10px;box-shadow:0 8px 20px #563d2510}.captions{position:absolute;inset:0;pointer-events:none}.cap{position:absolute;left:82px;top:1530px;width:880px;text-align:center;font-size:44px;line-height:1.5;color:#f7f2ea}.capbox{display:inline-block;padding:14px 24px;background:#29251ff5;border-radius:18px;max-width:880px}.cw{display:inline-block;margin:0 5px}.dark{background:#24231f;color:#faf4eb}.dark .title em,.dark .note b{color:#e9a47e}.dark .top b,.dark .kick{color:#e9a47e}.dark .note{color:#faf4eb}.symbol{position:absolute;top:1135px;right:125px;min-width:120px;height:120px;padding:10px 28px;background:#b45436;color:white;font-size:74px;display:flex;align-items:center;justify-content:center;border-radius:25px;box-shadow:0 10px 25px #0002}.bubbles{position:absolute;left:650px;top:650px;width:250px;height:220px}.bubble{position:absolute;border:3px solid #fff9;border-radius:50%;background:#ffffff30}.cover{position:absolute;inset:0;z-index:30}.cover img{width:1080px;height:1920px;object-fit:cover}.endbadge{position:absolute;top:1405px;left:175px;width:730px;background:#b45436;color:#fff;text-align:center;border-radius:50px;padding:20px;font-size:40px}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="21.2" data-width="1080" data-height="1920">'''
scene_starts=[0,4.65,9.31,11.85,13.97,17.33]
for i,(kick,t1,t2,img,note) in enumerate(scenes):
 dur=(scene_starts[i+1] if i<5 else 21.2)-scene_starts[i]
 html+=f'<div class="clip scene {"dark" if i==3 else ""}" id="s{i}" data-start="{scene_starts[i]}" data-duration="{dur}" data-track-index="{i+1}"><div class="grain"></div><div class="top"><strong>혀니의 꿀단지</strong><b>HEALTH NOTE</b></div><div class="rule"><div class="progress"></div></div><div class="kick">{kick}</div><div class="title"><div class="line1">{t1}</div><div class="line2">{t2}<i class="cursor"></i></div></div><div class="outline"></div><div class="photo"><img src="assets/img/{img}"></div><div class="note">{note}</div>'
 if i in [0,3,4]: html+=f'<div class="symbol">{["1+","","","✓","→"][i]}</div>'
 if i==2: html+='<div class="bubbles">'+''.join(f'<i class="bubble" style="left:{j%3*65}px;top:{j//3*70}px;width:{45+j*4}px;height:{45+j*4}px"></i>' for j in range(6))+'</div>'
 html+='</div>'
html+='<div class="captions">'
groups=[]; group=[]
for w in words:
 if group and (w['scene']!=group[0]['scene'] or len(group)>=4 or group[-1]['word'].endswith(('.', '?', ','))):groups.append(group);group=[]
 group.append(w)
if group:groups.append(group)
for j,g in enumerate(groups):
 html+=f'<div class="cap" id="cap{j}"><div class="capbox">'+''.join(f'<span class="cw" id="w{j}_{k}">{w["word"]}</span>' for k,w in enumerate(g))+'</div></div>'
html+='</div><div class="cover" id="cover"><img src="assets/img/cover.png"></div></div><script>const tl=gsap.timeline({paused:true});'
html+='gsap.set(".cap",{opacity:0});gsap.set(".scene",{opacity:0});gsap.set("#s0",{opacity:1});'
for i,st in enumerate(scene_starts):
 a=max(st,.85); end=scene_starts[i+1] if i<5 else 20.2
 if i:html+=f'tl.set("#s{i-1}",{{opacity:0}},{st});tl.set("#s{i}",{{opacity:1}},{st});'
 for sel,y,delay in [('.kick',20,0),('.line1',50,.08),('.line2',50,.2),('.photo',80,.05),('.outline',65,.08),('.note',25,.38),('.symbol',40,.45)]:
  if sel=='.symbol' and i not in [0,3,4]:continue
  html+=f'gsap.set("#s{i} {sel}",{{opacity:0,y:{y}}});tl.fromTo("#s{i} {sel}",{{opacity:0,y:{y}}},{{opacity:1,y:0,duration:.65,ease:"power3.out",immediateRender:false}},{a+delay});'
 html+=f'tl.fromTo("#s{i} .photo img",{{scale:1.04}},{{scale:1.10,duration:{max(.1,end-a)},ease:"none",immediateRender:false}},{a});'
 html+=f'tl.fromTo("#s{i} .progress",{{scaleX:{st/21.2}}},{{scaleX:{end/21.2},duration:{end-a},ease:"none",immediateRender:false}},{a});'
 html+=f'tl.fromTo("#s{i} .cursor",{{opacity:1}},{{opacity:0,duration:.35,repeat:3,yoyo:true,immediateRender:false}},{a+.4});'
html+='tl.fromTo("#cover",{opacity:1,scale:1},{opacity:0,scale:1.035,duration:.4,immediateRender:false},.85);'
for j,g in enumerate(groups):
 end=min(g[-1]['end']+.15,groups[j+1][0]['start'] if j+1<len(groups) else 20.2)
 html+=f'tl.set("#cap{j}",{{opacity:1}},{g[0]["start"]});tl.set("#cap{j}",{{opacity:0}},{end});'
 for k,w in enumerate(g):
  html+=f'tl.set("#w{j}_{k}",{{color:"#FFD36A"}},{w["start"]});tl.set("#w{j}_{k}",{{color:"#f7f2ea"}},{w["end"]});'
for j in range(6):html+=f'tl.fromTo(".bubble:nth-child({j+1})",{{scale:.3,y:35,opacity:0}},{{scale:1,y:0,opacity:1,duration:.55,immediateRender:false}},{9.5+j*.09});'
html+='tl.set("#root",{opacity:1},21.2);window.__timelines=window.__timelines||{};window.__timelines["main"]=tl;window.__hf=tl;</script></body></html>'
(proj/'index.html').write_text(html,encoding='utf-8')
print('Built 21.2-second composition, timed words, mixed audio.')


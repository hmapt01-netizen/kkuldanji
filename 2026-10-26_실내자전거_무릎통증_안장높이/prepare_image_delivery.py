from pathlib import Path
import json,re,shutil,hashlib,io
from PIL import Image
ROOT=Path(r"D:\작업\꿀단지")
work=ROOT/"2026-10-26_실내자전거_무릎통증_안장높이"
manifest=json.loads((work/"image_generation_manifest.json").read_text(encoding="utf-8"))
# Save generated images in web/shorts delivery formats; content generation was performed by image_gen.
for a in manifest["assets"]:
    im=Image.open(a["landscape"]).convert("RGB").resize((1280,720),Image.Resampling.LANCZOS)
    choices=[]
    for q in range(88,99):
        buf=io.BytesIO(); im.save(buf,"JPEG",quality=q,optimize=True)
        choices.append((abs(len(buf.getvalue())-190*1024),buf.getvalue(),q))
    valid=[x for x in choices if 150*1024<=len(x[1])<=250*1024]
    _,payload,q=min(valid or choices,key=lambda x:x[0])
    (work/"images"/(a["id"]+".jpg")).write_bytes(payload)
    vi=Image.open(a["vertical"]).convert("RGB").resize((1080,1920),Image.Resampling.LANCZOS)
    vi.save(work/"vertical"/(a["id"]+"_9x16.png"),"PNG",optimize=True)
    print(a["id"],"1280x720",round(len(payload)/1024,1),"KB; vertical 1080x1920")
alts=[
"실내자전거 옆 의자에 앉아 무릎 상태를 살피는 여성",
"실내자전거 안장 기둥과 높이 조절 손잡이 확대 모습",
"실내자전거에 앉아 두 발을 페달에 올린 여성의 옆모습",
"실내자전거 옆에 놓인 운동화와 매트, 수건, 물병",
"실내자전거 운동을 마치고 의자에 앉아 물을 마시며 쉬는 여성"]
caps=[
"무릎이 불편하면 운동을 쉬고 안장 높이와 운동 강도 등을 함께 점검합니다.",
"안장 높이 조절부와 고정 상태를 확인하는 장면입니다.",
"사진은 실내자전거 운동 장면이며 개인별 피팅 각도를 판정하는 기준은 아닙니다.",
"운동 준비물을 챙기고 자신의 상태에 맞는 강도와 시간을 정합니다.",
"운동 후에는 휴식을 취하며 무릎의 통증이나 붓기가 남는지 살펴봅니다."]
post=work/"post_data.json"; raw=post.read_text(encoding="utf-8-sig"); data=json.loads(raw)
backup=work/"_before_image_integration_20261026"; backup.mkdir(exist_ok=True)
for name in ["post_data.json","네이버.html"]:
    shutil.copy2(work/name,backup/name)
body=data["bodyHtml"]
for i,alt in enumerate(alts,1):
    pat=r'(<img\b[^>]*src="[^"]*/post0'+str(i)+r'\.jpg"[^>]*alt=")[^"]*(")'
    body,n=re.subn(pat,lambda m:m[1]+alt+m[2],body); assert n==1,(i,n)
capiter=iter(caps)
body,n=re.subn(r'(<figcaption\b[^>]*>)[\s\S]*?(</figcaption>)',lambda m:m[1]+next(capiter)+m[2],body)
assert n==5,n
# Replace only image-related JSON values, retaining all prose and source metadata for audit.
raw=raw.replace(json.dumps(data["bodyHtml"],ensure_ascii=False),json.dumps(body,ensure_ascii=False),1)
newcap="실내자전거를 탈 때 무릎이 불편하다면 안장 높이와 운동 강도를 점검하세요."
raw=raw.replace(json.dumps(data["featuredCaption"],ensure_ascii=False),json.dumps(newcap,ensure_ascii=False),1)
post.write_text(raw,encoding="utf-8")
data=json.loads(raw)
nav=(work/"네이버.html").read_text(encoding="utf-8")
for i,alt in enumerate(alts,1):
    pat=r'(<img\b[^>]*src="images/post0'+str(i)+r'\.jpg"[^>]*alt=")[^"]*(")'
    nav,n=re.subn(pat,lambda m:m[1]+alt+m[2],nav); assert n==1,(i,n)
nav=nav.replace('alt="실내자전거 거실 풍경"','alt="실내자전거, 무릎이 아프다면? 안장부터 점검"')
(work/"네이버.html").write_text(nav,encoding="utf-8")
db=ROOT/"data/posts_db.json"; shutil.copy2(db,backup/"posts_db.json")
posts=json.loads(db.read_text(encoding="utf-8-sig"))
target=next(p for p in posts if p["slug"]==data["slug"])
# Existing registered article: update only image captions/alts, not unrelated post contents or ordering.
for k in ["bodyHtml","featuredCaption"]:
    target[k]=data[k]
db.write_text(json.dumps(posts,ensure_ascii=False,indent=2),encoding="utf-8-sig")
dest=ROOT/"kkuldanji_web/images/posts"/data["slugKey"]; dest.mkdir(parents=True,exist_ok=True)
for a in manifest["assets"]: shutil.copy2(work/"images"/(a["id"]+".jpg"),dest/(a["id"]+".jpg"))
assert all(hashlib.sha256((work/"images"/(a["id"]+".jpg")).read_bytes()).digest()==hashlib.sha256((dest/(a["id"]+".jpg")).read_bytes()).digest() for a in manifest["assets"])
print("Existing post image references updated; six source/site image hashes match.")

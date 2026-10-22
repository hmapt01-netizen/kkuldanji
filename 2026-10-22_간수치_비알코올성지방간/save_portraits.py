from pathlib import Path
from PIL import Image,ImageOps
import hashlib,json
dest=Path(r'D:\작업\쇼츠만들기\레퍼런스_광고키트\레퍼런스_광고키트\첨부_소재\꿀단지\6.지방간 간수치 상승')
gen=Path(r'C:\Users\lim\.codex\generated_images\01a15bbf-8f26-7bb3-a77f-02cd045e134b')
ids=['9a8868df-d02d-4870-9ff5-c142e32ab625','b085f221-de50-4110-854d-8d1ea84113bc','7b5bc108-ae96-43d0-a4ae-8d89a2bc83a5','576a2095-6f12-4661-b80a-59f485391150','a6ba3aa8-6ae4-439f-a7de-30a0038f8618','439f08c5-c554-4b7e-8a5c-aefc81a8c640']
names=['00_thumb_9x16.jpg']+[f'{i:02}_post{i:02}_9x16.jpg' for i in range(1,6)]
dest.mkdir(parents=True,exist_ok=True)
for name,gid in zip(names,ids):
 p=dest/name
 if p.exists(): raise RuntimeError('Existing output: '+str(p))
 im=ImageOps.fit(Image.open(gen/f'exec-{gid}.png').convert('RGB'),(1080,1920),method=Image.Resampling.LANCZOS)
 im.save(p,quality=95,optimize=True)
 with Image.open(p) as check:
  assert check.size==(1080,1920)
  check.verify()
 print(name,p.stat().st_size)
print('Verified 6 portrait images; original blog images untouched.')


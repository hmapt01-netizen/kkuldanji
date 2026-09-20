from pathlib import Path
from PIL import Image
import shutil, hashlib
r=Path(__file__).resolve().parent
src=Path('C:/Users/lim/.codex/generated_images/01a0bbc7-591e-7850-815a-4138440b3487/exec-7f4b9596-805b-4fda-803f-9bf598c23307.png')
shutil.copy2(r/'post05.png',r/'post05-before-napkin.png')
shutil.copy2(src,r/'post05.png')
dest=r.parent/'images'/'post05.jpg'
Image.open(src).convert('RGB').resize((1280,720),Image.Resampling.LANCZOS).save(dest,quality=92,optimize=True)
package=r.parent.parent/'꿀단지 네이버'/'17_아침_공복_사과_속쓰림'/'images'/'post05.jpg'
shutil.copy2(dest,package)
assert hashlib.sha256(dest.read_bytes()).digest()==hashlib.sha256(package.read_bytes()).digest()
print('Updated PNG and both local draft image copies.')

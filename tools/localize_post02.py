import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

img_path = '2026-09-12-숙면-습관-골든타임/images/post02.jpg'
pil_orig = Image.open(img_path)
cv_img = cv2.cvtColor(np.array(pil_orig), cv2.COLOR_RGB2BGR)

mask = np.zeros(cv_img.shape[:2], dtype=np.uint8)

# Erase areas
cv2.rectangle(mask, (445, 226), (850, 248), 255, -1)
cv2.rectangle(mask, (540, 252), (755, 274), 255, -1)
cv2.rectangle(mask, (480, 275), (560, 314), 255, -1)
cv2.rectangle(mask, (760, 275), (855, 314), 255, -1)
cv2.rectangle(mask, (600, 350), (700, 370), 255, -1)
cv2.rectangle(mask, (765, 350), (850, 370), 255, -1)
cv2.rectangle(mask, (620, 375), (690, 393), 255, -1)

cv2.rectangle(mask, (525, 398), (770, 420), 255, -1)
cv2.rectangle(mask, (475, 421), (605, 460), 255, -1)
cv2.rectangle(mask, (760, 421), (858, 460), 255, -1)
cv2.rectangle(mask, (600, 495), (700, 515), 255, -1)
cv2.rectangle(mask, (765, 495), (850, 515), 255, -1)
cv2.rectangle(mask, (620, 521), (690, 538), 255, -1)

inpainted = cv2.inpaint(cv_img, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
result = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))
draw = ImageDraw.Draw(result)

font_bd = 'C:/Windows/Fonts/malgunbd.ttf'
font_rg = 'C:/Windows/Fonts/malgun.ttf'

def get_font(path, size):
    return ImageFont.truetype(path, size)

c_dark = (15, 23, 42)
c_blue_text = (30, 64, 175)
c_red_text = (185, 28, 28)

title_text = '수면 뇌파(서파) vs 각성 뇌파(베타파) 정밀 비교 분석'
f_title = get_font(font_bd, 16)
bbox = draw.textbbox((0, 0), title_text, font=f_title)
w_t = bbox[2] - bbox[0]
draw.text((648 - w_t//2, 229), title_text, fill=c_dark, font=f_title)

delta_hdr = '깊은 서파 수면 (델타파 · 뇌 청소)'
f_hdr = get_font(font_bd, 13)
bbox = draw.textbbox((0, 0), delta_hdr, font=f_hdr)
draw.text((648 - (bbox[2]-bbox[0])//2, 255), delta_hdr, fill=c_dark, font=f_hdr)

f_desc = get_font(font_bd, 10)
draw.text((485, 278), '비렘수면 3단계', fill=c_dark, font=f_desc)
draw.text((485, 294), '완전한 뇌 휴식', fill=c_blue_text, font=f_desc)

draw.text((770, 278), '0.5~4 Hz 주파수', fill=c_dark, font=f_desc)
draw.text((770, 294), '고진폭(High) 서파', fill=c_blue_text, font=f_desc)

f_label = get_font(font_bd, 11)
bbox = draw.textbbox((0, 0), '델타파 (0.5~4 Hz)', font=f_label)
draw.text((648 - (bbox[2]-bbox[0])//2, 351), '델타파 (0.5~4 Hz)', fill=c_dark, font=f_label)

draw.text((775, 351), '진짜 수면 파형', fill=c_blue_text, font=f_desc)

f_time = get_font(font_bd, 10)
draw.text((635, 376), '시간 (초)', fill=c_dark, font=f_time)

beta_hdr = '각성 및 불안 상태 (베타파 · 뇌 과열)'
bbox = draw.textbbox((0, 0), beta_hdr, font=f_hdr)
draw.text((648 - (bbox[2]-bbox[0])//2, 400), beta_hdr, fill=c_dark, font=f_hdr)

draw.text((485, 424), '인지 사고 가동', fill=c_dark, font=f_desc)
draw.text((485, 440), '눈만 감고 누울 때', fill=c_red_text, font=f_desc)

draw.text((770, 424), '13~30 Hz 주파수', fill=c_dark, font=f_desc)
draw.text((770, 440), '저진폭(Low) 빠른파', fill=c_red_text, font=f_desc)

bbox = draw.textbbox((0, 0), '베타파 (13~30 Hz)', font=f_label)
draw.text((648 - (bbox[2]-bbox[0])//2, 496), '베타파 (13~30 Hz)', fill=c_dark, font=f_label)

draw.text((775, 496), '피로 누적 파형', fill=c_red_text, font=f_desc)

draw.text((635, 522), '시간 (초)', fill=c_dark, font=f_time)

out_preview = 'C:/Users/lim/.gemini/antigravity/brain/060f1f5b-97dc-4f32-a5e4-149753554ed6/post02_korean_preview.jpg'
result.save(out_preview, quality=95)
print('Done saving to:', out_preview)

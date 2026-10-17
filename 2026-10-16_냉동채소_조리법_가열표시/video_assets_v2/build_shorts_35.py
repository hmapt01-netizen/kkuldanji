# -*- coding: utf-8 -*-
import os
import sys
import math
import json
import wave
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = r"d:\작업\꿀단지\2026-10-16_냉동채소_조리법_가열표시"
ASSET_DIR = os.path.join(BASE_DIR, "video_assets_v2")
KIT_DIR = r"D:\작업\쇼츠만들기\레퍼런스_광고키트\레퍼런스_광고키트"
FONT_BOLD = os.path.join(KIT_DIR, "클로드용_자료", "글꼴", "Freesentation-9Black.ttf")
OUT_KIT_MP4 = os.path.join(KIT_DIR, "완성_영상", "냉동채소_35번_세로_혀니의꿀단지.mp4")
OUT_LOCAL_MP4 = os.path.join(BASE_DIR, "냉동채소_35번_세로_혀니의꿀단지.mp4")
OUT_THUMB_JPG = os.path.join(BASE_DIR, "냉동채소_35번_세로_0초_썸네일.jpg")

W, H, FPS = 1080, 1920, 30
NAR_OFFSET = 0.90  # 0.0~0.90s: thumb_shorts_9x16.png 오프닝 커버 홀드 후 본편 진입
DUR = 36.50
TOTAL_FRAMES = int(DUR * FPS)

# Reference #35 Color Palette
CREAM = (237, 234, 226)     # #EDEAE2 (Ref 35 signature warm cream)
INK = (18, 18, 18)          # #121212 (Ref 35 carbon black)
ORANGE = (240, 70, 30)      # #F0461E (Ref 35 vermilion orange-red)
WHITE = (255, 255, 255)
GREY_DARK = (110, 108, 102)
GREY_LIGHT = (165, 165, 170)
YELLOW = (255, 214, 0)

# Font cache
_FONTS = {}
def font(size):
    if size not in _FONTS:
        _FONTS[size] = ImageFont.truetype(FONT_BOLD, size)
    return _FONTS[size]

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def ease_out_cubic(x):
    x = clamp(x)
    return 1.0 - (1.0 - x) ** 3

def ease_in_out_cubic(x):
    x = clamp(x)
    return 4 * x * x * x if x < 0.5 else 1 - ((-2 * x + 2) ** 3) / 2

def ease_out_back(x, s=1.6):
    x = clamp(x)
    x -= 1.0
    return x * x * ((s + 1.0) * x + s) + 1.0

# 1. Clean & align Whisper words with NAR_OFFSET (+0.90s)
RAW_WORDS = json.load(open(os.path.join(ASSET_DIR, "words_raw.json"), encoding="utf-8"))

# Merge split tokens & fix Whisper transcription typos to match exact script
CLEAN_WORDS = [
    ("봉지를", 0.00, 0.56),
    ("열면", 0.56, 0.94),
    ("초록빛이", 0.94, 1.66),
    ("선명한", 1.66, 2.10),
    ("냉동", 2.10, 2.44),
    ("브로콜리와", 2.44, 3.12),
    ("채소믹스,", 3.12, 3.74),
    ("이미", 3.74, 4.32),
    ("데쳐", 4.32, 4.64),
    ("나온", 4.64, 4.82),
    ("것", 4.82, 4.96),
    ("같아서", 4.96, 5.20),
    ("그냥", 5.20, 5.62),
    ("녹여 드셨나요?", 5.62, 6.22),

    ("냉동", 6.88, 7.12),
    ("전", 7.12, 7.30),
    ("데치기는", 7.30, 7.78),
    ("효소만", 7.78, 8.34),
    ("멈추는", 8.34, 8.72),
    ("과정이라,", 8.72, 9.10),
    ("저온에서", 9.10, 9.98),
    ("버티는", 9.98, 10.36),
    ("세균까지", 10.36, 10.94),
    ("사라지진", 10.94, 11.42),
    ("않습니다.", 11.42, 11.82),

    ("포장지에", 12.34, 13.08),
    ("가열하여", 13.08, 13.64),
    ("섭취하는", 13.64, 14.10),
    ("냉동식품이라고", 14.10, 15.10),
    ("적혀", 15.10, 15.44),
    ("있다면", 15.44, 15.74),
    ("해동만", 15.74, 16.42),
    ("해서", 16.42, 16.64),
    ("바로", 16.64, 16.90),
    ("드시면", 16.90, 17.18),
    ("안", 17.18, 17.34),
    ("됩니다.", 17.34, 17.52),

    ("차가운", 18.18, 18.68),
    ("샐러드에", 18.68, 19.08),
    ("넣더라도", 19.08, 19.48),
    ("언", 19.48, 19.92),
    ("상태", 19.92, 20.16),
    ("그대로", 20.16, 20.54),
    ("중심부", 20.54, 21.14),
    ("70℃에서", 21.14, 21.80),
    ("2분", 21.80, 22.18),
    ("이상", 22.18, 22.38),
    ("김이", 22.38, 22.74),
    ("오르도록", 22.74, 23.04),
    ("먼저", 23.04, 23.40),
    ("익혀 주세요.", 23.40, 23.84),

    ("그다음", 24.32, 24.74),
    ("넓은", 24.74, 25.24),
    ("채반에", 25.24, 25.64),
    ("펼쳐", 25.64, 25.84),
    ("물기와", 25.84, 26.54),
    ("열기를", 26.54, 26.84),
    ("빠르게", 26.84, 27.22),
    ("식히면", 27.22, 27.62),
    ("아삭한", 27.62, 28.26),
    ("식감이", 28.26, 28.54),
    ("살아납니다.", 28.54, 28.98),

    ("소스", 29.45, 29.86),
    ("없는", 29.86, 30.10),
    ("무가미", 30.10, 30.50),
    ("채소", 30.50, 30.76),
    ("고르는", 30.76, 31.02),
    ("법과", 31.02, 31.38),
    ("냉장 보관", 31.38, 32.20),
    ("기준은", 32.20, 32.72),
    ("혀니의", 32.72, 33.14),
    ("꿀단지", 33.14, 33.58),
    ("본문에서", 33.58, 34.10),
    ("확인해", 34.10, 34.38),
    ("보세요!", 34.38, 34.65),
]

WORDS = [(w, round(s + NAR_OFFSET, 2), round(e + NAR_OFFSET, 2)) for w, s, e in CLEAN_WORDS]

# Group words into readable 2-line subtitle chunks aligned with sentences
CHUNK_RANGES = [
    (0, 7),    # 봉지를 열면 초록빛이 선명한 냉동 브로콜리와 채소믹스,
    (7, 14),   # 이미 데쳐 나온 것 같아서 그냥 녹여 드셨나요?
    (14, 20),  # 냉동 전 데치기는 효소만 멈추는 과정이라,
    (20, 25),  # 저온에서 버티는 세균까지 사라지진 않습니다.
    (25, 31),  # 포장지에 가열하여 섭취하는 냉동식품이라고 적혀 있다면
    (31, 37),  # 해동만 해서 바로 드시면 안 됩니다.
    (37, 43),  # 차가운 샐러드에 넣더라도 언 상태 그대로
    (43, 51),  # 중심부 70℃에서 2분 이상 김이 오르도록 먼저 익혀 주세요.
    (51, 57),  # 그다음 넓은 채반에 펼쳐 물기와 열기를
    (57, 62),  # 빠르게 식히면 아삭한 식감이 살아납니다.
    (62, 69),  # 소스 없는 무가미 채소 고르는 법과 냉장 보관 기준은
    (69, 75),  # 기준은 혀니의 꿀단지 본문에서 확인해 보세요!
]
CHUNKS = [WORDS[a:b] for a, b in CHUNK_RANGES]

# Scene boundaries (in seconds, shifted by NAR_OFFSET = 0.90)
# Intro cover: 0.00 ~ 0.90 (cross-transition until 1.25)
# S1: 0.90 ~ 7.50 (Sentence 1)
# S2: 7.50 ~ 13.05 (Sentence 2)
# S3: 13.05 ~ 18.80 (Sentence 3)
# S4: 18.80 ~ 25.00 (Sentence 4)
# S5: 25.00 ~ 30.15 (Sentence 5)
# S6: 30.15 ~ 36.50 (Sentence 6 + Ref 35 Signature Closing)
SCENES = [
    (0.90, 7.50),
    (7.50, 13.05),
    (13.05, 18.80),
    (18.80, 25.00),
    (25.00, 30.15),
    (30.15, 36.50),
]

def build_audio_mix():
    """Synthesize Ref #35 style SFX + Mix with delayed Narration and Flow Music BGM."""
    sr = 48000
    rng = np.random.default_rng(35)
    sfx_track = np.zeros(int(DUR * sr), dtype=np.float32)

    def lowpass(x, cut):
        a = math.exp(-2.0 * math.pi * cut / sr)
        y = np.zeros_like(x)
        p = 0.0
        for i in range(len(x)):
            p = (1.0 - a) * x[i] + a * p
            y[i] = p
        return y

    def put(x, t, gain):
        i = int(t * sr)
        if i < 0 or i >= len(sfx_track):
            return
        n = min(len(x), len(sfx_track) - i)
        sfx_track[i:i + n] += x[:n] * gain

    def whoosh(d=0.55):
        n = int(d * sr)
        t = np.arange(n) / sr
        env = (np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2) * np.exp(-t * 1.6)
        air = lowpass(lowpass(rng.standard_normal(n), 420), 420) * 5.0
        sub = np.sin(2 * np.pi * np.cumsum(np.linspace(110, 48, n)) / sr)
        return ((air * 0.65 + sub * 0.5) * env).astype(np.float32)

    def swish(d=0.32):
        n = int(d * sr)
        t = np.arange(n) / sr
        x = rng.standard_normal(n)
        hp = x - lowpass(x, 850)
        return (lowpass(hp, 4800) * (np.sin(np.pi * t / d) ** 2) * 1.4).astype(np.float32)

    def pop_tone(freq=520, d=0.12):
        n = int(d * sr)
        t = np.arange(n) / sr
        env = np.exp(-t / 0.028)
        sig = np.sin(2 * np.pi * freq * t) * env
        return sig.astype(np.float32)

    # Opening cover whoosh + bounce pop
    put(whoosh(0.6), 0.72, 0.16)
    put(pop_tone(440, 0.12), 0.90, 0.12)

    # Scene transitions
    for st in [7.50, 13.05, 18.80, 25.00, 30.15, 33.20]:
        put(swish(0.35), st - 0.12, 0.12)
        put(whoosh(0.5), st - 0.08, 0.11)

    sfx_path = os.path.join(ASSET_DIR, "sfx_35.wav")
    sfx_clipped = np.clip(sfx_track, -1.0, 1.0)
    st_pcm = (np.repeat(sfx_clipped[:, None], 2, axis=1) * 32767).astype(np.int16)
    with wave.open(sfx_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(st_pcm.tobytes())

    nar_path = os.path.join(ASSET_DIR, "Generated Audio October 16, 2026 - 3_38PM.wav")
    bgm_path = os.path.join(ASSET_DIR, "Modern Minimal Editorial.mp3")
    mix_path = os.path.join(ASSET_DIR, "final_mix_35.wav")

    delay_ms = int(NAR_OFFSET * 1000)
    filter_complex = (
        f"[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,volume=1.18,adelay={delay_ms}|{delay_ms}[nar];"
        f"[1:a]aresample=48000,atrim=0:{DUR},asetpts=PTS-STARTPTS,"
        f"volume=0.16,afade=t=in:st=0:d=0.4,afade=t=out:st={DUR-1.2:.2f}:d=1.2[bgm];"
        f"[2:a]volume=1.0[sfx];"
        f"[nar][bgm][sfx]amix=inputs=3:duration=longest:dropout_transition=0:normalize=0,"
        f"alimiter=limit=0.95[out]"
    )
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", nar_path,
        "-i", bgm_path,
        "-i", sfx_path,
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-t", str(DUR),
        "-ar", "48000", "-ac", "2",
        mix_path
    ], check=True)
    return mix_path

# Load visual assets
THUMB_9X16 = Image.open(os.path.join(ASSET_DIR, "thumb_shorts_9x16.png")).convert("RGB").resize((W, H), Image.LANCZOS)
HERO_CLEAN = Image.open(os.path.join(ASSET_DIR, "hero_clean.png")).convert("RGB")
THUMB_16X9 = Image.open(os.path.join(ASSET_DIR, "thumb.png")).convert("RGB")
POST_IMGS = {
    i: Image.open(os.path.join(ASSET_DIR, f"post0{i}.png")).convert("RGB")
    for i in range(1, 6)
}

def make_round_mask(w, h, r):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    return m

CARD_W, CARD_H, CARD_R = 960, 780, 36
CARD_MASK = make_round_mask(CARD_W, CARD_H, CARD_R)
CARD_SHADOW = Image.new("RGBA", (CARD_W + 100, CARD_H + 100), (0, 0, 0, 0))
ImageDraw.Draw(CARD_SHADOW).rounded_rectangle([50, 68, CARD_W + 50, CARD_H + 58], CARD_R, fill=(0, 0, 0, 75))
CARD_SHADOW = CARD_SHADOW.filter(ImageFilter.GaussianBlur(24))

def kenburns(img, lt, dur, z0=1.0, z1=1.10, fx=0.5, fy=0.5, cw=CARD_W, ch=CARD_H):
    p = clamp(lt / max(0.01, dur))
    z = z0 + (z1 - z0) * p
    iw, ih = img.size
    s = max(cw / iw, ch / ih) * z
    nw, nh = int(iw * s), int(ih * s)
    im = img.resize((nw, nh), Image.LANCZOS)
    x = int((nw - cw) * fx)
    y = int((nh - ch) * fy)
    return im.crop((x, y, x + cw, y + ch))

def draw_ref35_hud(fr, t, chap_num, chap_title, dark_mode=False):
    """Draws Reference #35's 4-corner editorial HUD (top chapter, top brand, bottom frame counter, bottom 120 BPM squares)."""
    d = ImageDraw.Draw(fr)
    fg = WHITE if dark_mode else INK
    muted = GREY_LIGHT if dark_mode else GREY_DARK
    line_col = (48, 48, 52) if dark_mode else (210, 206, 198)

    # Top-Left: Orange number + chapter name (Ref #35: "01 ZAMANLAMA")
    f_hud = font(32)
    d.text((64, 88), chap_num, font=f_hud, fill=ORANGE)
    num_w = d.textlength(chap_num, font=f_hud)
    d.text((64 + num_w + 18, 88), chap_title, font=f_hud, fill=fg)

    # Top-Right: Brand signature (Ref #35: "CLAUDE · ÖZGEÇMİŞ")
    brand_str = "혀니의 꿀단지  ·  식단 & 영양"
    bw = d.textlength(brand_str, font=f_hud)
    d.text((W - 64 - bw, 88), brand_str, font=f_hud, fill=fg)

    # Progress bar under top HUD
    d.rectangle([64, 144, W - 64, 148], fill=line_col)
    prog_w = int((W - 128) * clamp(t / DUR))
    d.rectangle([64, 144, 64 + prog_w, 148], fill=ORANGE)

    # Bottom-Left: Live frame counter (Ref #35: "KARE 001 / 900")
    f_bot = font(28)
    cur_frame = min(TOTAL_FRAMES, max(1, int(t * FPS) + 1))
    frame_str = f"FRAME {cur_frame:03d} / {TOTAL_FRAMES}"
    d.text((64, 1836), frame_str, font=f_bot, fill=muted)

    # Bottom-Right: "120 BPM" + 4 beat indicator squares (Ref #35: "120 BPM ■□□□")
    bpm_str = "120 BPM"
    bpm_w = d.textlength(bpm_str, font=f_bot)
    sq_size = 18
    sq_gap = 8
    total_sq_w = 4 * sq_size + 3 * sq_gap
    bx = W - 64 - total_sq_w - 16 - bpm_w
    d.text((bx, 1836), bpm_str, font=f_bot, fill=muted)

    active_beat = int(t * 2.0) % 4  # 120 BPM = 2 beats per second
    sq_x0 = W - 64 - total_sq_w
    sq_y0 = 1842
    for bi in range(4):
        sx = sq_x0 + bi * (sq_size + sq_gap)
        if bi == active_beat:
            d.rectangle([sx, sq_y0, sx + sq_size, sq_y0 + sq_size], fill=ORANGE)
        else:
            d.rectangle([sx, sq_y0, sx + sq_size, sq_y0 + sq_size], outline=muted, width=2)

def draw_kinetic_line(fr, text, y, size, color, t_in, lt, align="c", x0=64, stag=0.025):
    """Character-by-character rising kinetic typography."""
    d = ImageDraw.Draw(fr)
    f = font(size)
    tw = d.textlength(text, font=f)
    x = (W - tw) / 2 if align == "c" else x0
    for i, ch in enumerate(text):
        ct = lt - t_in - i * stag
        p = ease_out_cubic(ct / 0.32)
        if p > 0:
            a = int(255 * clamp(ct / 0.18))
            dy = (1.0 - p) * (size * 0.42)
            d.text((x, y + dy), ch, font=f, fill=color + (a,))
        x += d.textlength(ch, font=f)

def paste_photo_card(fr, media_img, cy, t_in, lt, badge_text=None, border_col=None):
    p = ease_out_back((lt - t_in) / 0.42, 1.25)
    if p <= 0:
        return
    sc = 0.88 + 0.12 * p
    a = clamp((lt - t_in) / 0.22)
    w, h = int(CARD_W * sc), int(CARD_H * sc)
    m = media_img.resize((w, h), Image.LANCZOS)
    mk = CARD_MASK.resize((w, h), Image.LANCZOS)
    x = (W - w) // 2
    y = cy + (CARD_H - h) // 2 + int((1.0 - ease_out_cubic((lt - t_in) / 0.42)) * 60)

    sh = CARD_SHADOW.resize((w + 100, h + 100), Image.LANCZOS)
    if a < 1.0:
        sh.putalpha(sh.getchannel("A").point(lambda v: int(v * a)))
        mk = mk.point(lambda v: int(v * a))
    fr.alpha_composite(sh, (x - 50, y - 50))
    fr.paste(m, (x, y), mk)

    d = ImageDraw.Draw(fr)
    if border_col:
        d.rounded_rectangle([x, y, x + w - 1, y + h - 1], int(CARD_R * sc), outline=border_col + (int(220 * a),), width=3)

    if badge_text:
        fb = font(30)
        tw = d.textlength(badge_text, font=fb)
        bx1, by1 = x + 24, y + 24
        bx2, by2 = bx1 + tw + 36, by1 + 54
        d.rounded_rectangle([bx1, by1, bx2, by2], 27, fill=(18, 18, 18, int(185 * a)))
        d.text((bx1 + 18, by1 + 11), badge_text, font=fb, fill=(255, 255, 255, int(255 * a)))

def draw_info_card(fr, badge_str, title_str, desc_str, y, t_in, lt, dark_mode=False, accent=ORANGE):
    p = ease_out_cubic((lt - t_in) / 0.38)
    if p <= 0:
        return
    d = ImageDraw.Draw(fr)
    a = int(255 * p)
    x = 60 + int((1.0 - p) * 110)
    card_bg = (30, 32, 38, a) if dark_mode else (255, 255, 255, a)
    card_bd = (68, 72, 82, a) if dark_mode else (218, 214, 206, a)
    title_col = (255, 255, 255, a) if dark_mode else (18, 18, 18, a)
    desc_col = (185, 190, 200, a) if dark_mode else (105, 102, 96, a)

    d.rounded_rectangle([x, y, x + 960, y + 148], 28, fill=card_bg, outline=card_bd, width=2)
    d.ellipse([x + 28, y + 36, x + 104, y + 112], fill=accent + (a,))
    fb = font(40)
    bw = d.textlength(badge_str, font=fb)
    d.text((x + 66 - bw / 2, y + 48), badge_str, font=fb, fill=(255, 255, 255, a))

    d.text((x + 130, y + 26), title_str, font=font(44), fill=title_col)
    d.text((x + 130, y + 86), desc_str, font=font(32), fill=desc_col)

def draw_pill(fr, text, cx, y, t_in, lt, fg=WHITE, bg=ORANGE, size=42, padx=44, h=88):
    p = ease_out_back((lt - t_in) / 0.35, 1.8)
    if p <= 0:
        return
    d = ImageDraw.Draw(fr)
    f = font(size)
    tw = d.textlength(text, font=f)
    w = (tw + padx * 2) * p
    hh = h * p
    d.rounded_rectangle([cx - w / 2, y + (h - hh) / 2, cx + w / 2, y + (h + hh) / 2], hh / 2, fill=bg + (255,))
    if p > 0.75:
        d.text((cx - tw / 2, y + (h - size) / 2 - 4), text, font=f, fill=fg + (255,))

def draw_ref35_bouncing_ball(fr, lt):
    """Reference #35 Scene 01 signature bouncing orange ball with trailing ghost rings."""
    if lt > 1.35:
        return
    d = ImageDraw.Draw(fr)
    p = clamp(lt / 0.95)
    # Ghost rings above
    for gy, gr, ga in [(210, 34, 90), (310, 42, 130)]:
        a = int(ga * (1.0 - p))
        if a > 5:
            d.ellipse([W // 2 - gr, gy - gr, W // 2 + gr, gy + gr], outline=(120, 116, 108, a), width=2)
    # Main orange circle dropping to center
    cy = int(190 + ease_out_back(p, 1.4) * 320)
    r = int(46 + p * 18)
    a = int(235 * (1.0 - clamp((lt - 0.70) / 0.55)))
    if a > 5:
        d.ellipse([W // 2 - r, cy - r, W // 2 + r, cy + r], fill=ORANGE + (a,))

def draw_ref35_dot_ring(fr, lt, cx=540, cy=960, base_r=490):
    """Reference #35 Scene 04 ('04 DERİNLİK') signature 3D dot-ring sphere accent."""
    d = ImageDraw.Draw(fr)
    num_dots = 36
    rot = lt * 0.45
    for i in range(num_dots):
        ang = (2 * math.pi * i / num_dots) + rot
        x = cx + math.cos(ang) * base_r
        y = cy + math.sin(ang) * (base_r * 0.88)
        col = ORANGE + (170,) if i % 3 == 0 else (255, 255, 255, 95)
        r = 5 if i % 3 == 0 else 3
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)

def draw_subtitle(fr, t):
    """Draws word-synced subtitle bar at Y: 1645~1785 (safe above bottom HUD)."""
    cur = None
    for i, c in enumerate(CHUNKS):
        end = CHUNKS[i + 1][0][1] - 0.06 if i + 1 < len(CHUNKS) else 35.85
        if c[0][1] - 0.12 <= t < end:
            cur = c
            break
    if not cur:
        return

    f = font(42)
    d = ImageDraw.Draw(fr)
    sp = d.textlength(" ", font=f)
    line_len = lambda L: sum(d.textlength(x[0], font=f) for x in L) + sp * max(0, len(L) - 1)

    lines = [[]]
    for w_item in cur:
        if lines[-1] and line_len(lines[-1] + [w_item]) > 860:
            lines.append([])
        lines[-1].append(w_item)

    lh = 56
    bh = lh * len(lines) + 32
    by = 1795 - bh
    bw = max(line_len(L) for L in lines) + 64
    d.rounded_rectangle([W / 2 - bw / 2, by, W / 2 + bw / 2, by + bh], 24, fill=(12, 14, 18, 215), outline=(255, 255, 255, 45), width=2)

    for li, L in enumerate(lines):
        x = W / 2 - line_len(L) / 2
        for w_str, s0, e0 in L:
            if s0 - 0.05 <= t < e0 + 0.18:
                col = YELLOW + (255,)
            elif t >= s0:
                col = WHITE + (255,)
            else:
                col = (195, 198, 205, 165)
            d.text((x, by + 14 + li * lh), w_str, font=f, fill=col)
            x += d.textlength(w_str, font=f) + sp

def render_frame(t):
    # ------------------------------------------------------------------
    # SCENE 1 (0.90 ~ 7.50s): Cream Ivory (#EDEAE2) + Hook
    # ------------------------------------------------------------------
    if t < SCENES[0][1]:
        lt = max(0.0, t - SCENES[0][0])
        fr = Image.new("RGBA", (W, H), CREAM + (255,))
        draw_ref35_hud(fr, t, "01", "통념 점검 · 해동 섭취", dark_mode=False)
        draw_ref35_bouncing_ball(fr, lt)

        draw_kinetic_line(fr, "초록빛이 선명한 냉동채소", 210, 48, ORANGE, 0.05, lt)
        draw_kinetic_line(fr, "데쳐 나온 것 같아", 282, 92, INK, 0.15, lt)
        draw_kinetic_line(fr, "그냥 녹여 드셨나요?", 392, 92, INK, 0.35, lt)

        media = kenburns(HERO_CLEAN, lt, 6.5, 1.0, 1.10, fx=0.55)
        paste_photo_card(fr, media, 540, 0.10, lt, "조리 안내 · 가열 후 섭취 확인 (예시 포장)")

        draw_info_card(
            fr, "?", "생브로콜리 데친 것처럼 선명한 색감",
            "이미 다 익혀 나온 제품으로 오해해 해동 후 바로 섭취 주의",
            1365, 0.55, lt, dark_mode=False, accent=ORANGE
        )

        # Opening Cover Overlay (0.00 ~ 1.15s): thumb_shorts_9x16.png holds then smoothly transitions out!
        if t < 1.15:
            if t <= 0.72:
                # Subtle zoom 1.00 -> 1.02 on thumb_shorts_9x16
                zp = ease_out_cubic(t / 0.72)
                zw, zh = int(W * (1.0 + 0.02 * zp)), int(H * (1.0 + 0.02 * zp))
                cov = THUMB_9X16.resize((zw, zh), Image.LANCZOS)
                cx0, cy0 = (zw - W) // 2, (zh - H) // 2
                cov = cov.crop((cx0, cy0, cx0 + W, cy0 + H)).convert("RGBA")
                fr.alpha_composite(cov, (0, 0))
            else:
                # 0.72 ~ 1.15s: Smooth scale-up + fade out reveal into Scene 01
                tp = clamp((t - 0.72) / 0.43)
                e_tp = ease_in_out_cubic(tp)
                zw, zh = int(W * (1.02 + 0.08 * e_tp)), int(H * (1.02 + 0.08 * e_tp))
                cov = THUMB_9X16.resize((zw, zh), Image.LANCZOS)
                cx0, cy0 = (zw - W) // 2, (zh - H) // 2
                cov = cov.crop((cx0, cy0, cx0 + W, cy0 + H)).convert("RGBA")
                alpha = int(255 * (1.0 - e_tp))
                cov.putalpha(alpha)
                fr.alpha_composite(cov, (0, 0))

    # ------------------------------------------------------------------
    # SCENE 2 (7.50 ~ 13.05s): Carbon Black (#121212) — Ref #35 "02 TİPOGRAFİ"
    # ------------------------------------------------------------------
    elif t < SCENES[1][1]:
        lt = t - SCENES[1][0]
        fr = Image.new("RGBA", (W, H), INK + (255,))
        draw_ref35_hud(fr, t, "02", "전처리 공정 · 위생 맥락", dark_mode=True)

        draw_kinetic_line(fr, "급속 냉동 전 블랜칭 공정", 210, 48, ORANGE, 0.05, lt)
        draw_kinetic_line(fr, "데치기는 효소만 억제", 282, 90, WHITE, 0.15, lt)
        draw_kinetic_line(fr, "세균은 남아 있습니다", 392, 90, ORANGE, 0.40, lt)

        media = kenburns(POST_IMGS[3], lt, 5.5, 1.02, 1.12, fx=0.5)
        paste_photo_card(fr, media, 540, 0.12, lt, "전처리 데치기 ≠ 섭취 직전 완전 살균", border_col=ORANGE)

        draw_info_card(
            fr, "!", "저온에서 버티는 잔류 세균 주의",
            "색과 식감 유지용 전처리만으로는 세균이 모두 사라지지 않음",
            1365, 0.55, lt, dark_mode=True, accent=ORANGE
        )

        # Orange circle flood transition out at end of Scene 2 (Ref #35 transition)
        rem = SCENES[1][1] - t
        if rem < 0.32:
            rp = ease_in_out_cubic(1.0 - rem / 0.32)
            r = int(rp * 1400)
            ImageDraw.Draw(fr).ellipse([W // 2 - r, 960 - r, W // 2 + r, 960 + r], fill=ORANGE + (255,))

    # ------------------------------------------------------------------
    # SCENE 3 (13.05 ~ 18.80s): Ref #35 "KURGU" Vermilion Impact -> Cream Split
    # ------------------------------------------------------------------
    elif t < SCENES[2][1]:
        lt = t - SCENES[2][0]
        fr = Image.new("RGBA", (W, H), CREAM + (255,))
        d = ImageDraw.Draw(fr)
        # Top Vermilion Accent Header Band (Ref #35 KURGU orange-red block)
        d.rounded_rectangle([48, 178, W - 48, 505], 32, fill=ORANGE + (255,))
        draw_ref35_hud(fr, t, "03", "포장지 법적 표시 구분", dark_mode=False)

        draw_kinetic_line(fr, "포장 뒷면 정보표시면 필수 확인", 206, 44, WHITE, 0.08, lt)
        draw_kinetic_line(fr, "가열하여 섭취하는", 272, 92, INK, 0.18, lt)
        draw_kinetic_line(fr, "냉동식품 = 생식 금지", 380, 92, WHITE, 0.35, lt)

        media = kenburns(HERO_CLEAN, lt, 5.7, 1.08, 1.18, fx=0.78, fy=0.48)
        paste_photo_card(fr, media, 540, 0.15, lt, "포장 표시 확인 (이해 돕기용 예시 포장)")

        draw_info_card(
            fr, "✓", "비가열 섭취 표시 제품만 바로 섭취 가능",
            "가열하여 섭취하는 냉동식품은 해동만 해서 바로 드시면 안 됨",
            1365, 0.55, lt, dark_mode=False, accent=INK
        )

        if lt < 0.28:
            rp = 1.0 - clamp(lt / 0.28)
            r = int(ease_out_cubic(rp) * 1400)
            ImageDraw.Draw(fr).ellipse([W // 2 - r, 960 - r, W // 2 + r, 960 + r], fill=ORANGE + (255,))

    # ------------------------------------------------------------------
    # SCENE 4 (18.80 ~ 25.00s): Carbon Black (#121212) + Ref #35 Dot-Ring Sphere
    # ------------------------------------------------------------------
    elif t < SCENES[3][1]:
        lt = t - SCENES[3][0]
        fr = Image.new("RGBA", (W, H), INK + (255,))
        draw_ref35_dot_ring(fr, lt, cx=540, cy=930, base_r=505)
        draw_ref35_hud(fr, t, "04", "샐러드용 가열 조리 기준", dark_mode=True)

        draw_kinetic_line(fr, "차가운 샐러드·스무디에 넣더라도", 210, 48, ORANGE, 0.05, lt)
        draw_kinetic_line(fr, "언 상태 그대로", 282, 92, WHITE, 0.15, lt)
        draw_kinetic_line(fr, "70℃ · 2분 이상 가열", 392, 92, ORANGE, 0.35, lt)

        media = kenburns(POST_IMGS[3], lt, 6.2, 1.08, 1.0, fx=0.45)
        paste_photo_card(fr, media, 540, 0.12, lt, "중심부까지 뜨거운 김이 오르도록 가열", border_col=ORANGE)

        draw_info_card(
            fr, "1", "미리 녹이지 말고 바로 조리",
            "포장지 조리 안내에 맞춰 중심부 70℃에서 2분 이상 충분히 가열",
            1365, 0.55, lt, dark_mode=True, accent=ORANGE
        )

    # ------------------------------------------------------------------
    # SCENE 5 (25.00 ~ 30.15s): Cream Ivory (#EDEAE2) + Rapid Cooling
    # ------------------------------------------------------------------
    elif t < SCENES[4][1]:
        lt = t - SCENES[4][0]
        fr = Image.new("RGBA", (W, H), CREAM + (255,))
        draw_ref35_hud(fr, t, "05", "물기 제거 · 급속 식힘", dark_mode=False)

        draw_kinetic_line(fr, "잎채소 숨 죽지 않는 샐러드 비결", 210, 48, ORANGE, 0.05, lt)
        draw_kinetic_line(fr, "넓은 채반에 펼쳐", 282, 92, INK, 0.15, lt)
        draw_kinetic_line(fr, "물기와 열기 식히기", 392, 92, ORANGE, 0.35, lt)

        media = kenburns(POST_IMGS[4], lt, 5.1, 1.0, 1.10, fx=0.5)
        paste_photo_card(fr, media, 540, 0.12, lt, "채반 물기 제거 후 얕은 용기에 펼쳐 식힘")

        draw_info_card(
            fr, "2", "수증기와 고인 물기 빠르게 제거",
            "열기를 식힌 뒤 샐러드에 올려야 질척거리지 않고 아삭함 유지",
            1365, 0.50, lt, dark_mode=False, accent=ORANGE
        )

    # ------------------------------------------------------------------
    # SCENE 6 (30.15 ~ 36.50s): Nutrition/Storage + Ref #35 "05 İMZA" Signature End Card
    # ------------------------------------------------------------------
    else:
        lt = t - SCENES[5][0]
        fr = Image.new("RGBA", (W, H), CREAM + (255,))
        draw_ref35_hud(fr, t, "06", "영양 선택 · 보관 & 요약", dark_mode=False)

        if lt < 3.05:
            # 30.15 ~ 33.20s: Compare raw vs seasoned (post02) + storage (post05)
            draw_kinetic_line(fr, "소스·나트륨 비교 & 안전한 보관", 210, 48, ORANGE, 0.05, lt)
            draw_kinetic_line(fr, "무가미 원물 고르고", 282, 90, INK, 0.12, lt)
            draw_kinetic_line(fr, "조리 후 48시간 내 섭취", 390, 90, ORANGE, 0.28, lt)

            # Dual stacked cards: post02 (label compare) & post05 (fridge storage)
            m_top = kenburns(POST_IMGS[2], lt, 3.0, 1.0, 1.06, cw=960, ch=370)
            m_bot = kenburns(POST_IMGS[5], lt, 3.0, 1.0, 1.06, cw=960, ch=370)
            mk_half = make_round_mask(960, 370, 28)
            fr.paste(m_top, (60, 535), mk_half)
            fr.paste(m_bot, (60, 935), mk_half)
            d = ImageDraw.Draw(fr)
            d.rounded_rectangle([80, 555, 560, 605], 25, fill=(18, 18, 18, 190))
            d.text((100, 564), "원재료·나트륨 비교 (예시 포장)", font=font(28), fill=WHITE + (255,))
            d.rounded_rectangle([80, 955, 620, 1005], 25, fill=(18, 18, 18, 190))
            d.text((100, 964), "조리 후 2시간 내 냉장 · 48시간 내 섭취", font=font(28), fill=WHITE + (255,))

            draw_info_card(
                fr, "✓", "성인 1회 80g 채소 섭취 인정",
                "녹은 채소는 재냉동하지 말고 먹을 만큼만 덜어 밀봉 보관",
                1355, 0.20, lt, dark_mode=False, accent=INK
            )
        else:
            # 33.20 ~ 36.50s: Reference #35 "05 İMZA" ("Claude.") Signature End Screen!
            elt = lt - 3.05
            d = ImageDraw.Draw(fr)

            # Subtle geometric corner arcs like Ref #35 İMZA frame
            d.arc([-220, 180, 260, 660], 0, 90, fill=(205, 200, 190, 255), width=2)
            d.arc([W - 260, 1260, W + 220, 1740], 180, 270, fill=(205, 200, 190, 255), width=2)

            # Small preview card at top center
            m_end = kenburns(POST_IMGS[1], min(elt, 2.0), 2.5, 1.0, 1.05, cw=840, ch=440)
            mk_end = make_round_mask(840, 440, 32)
            fr.paste(m_end, ((W - 840) // 2, 230), mk_end)
            d.rounded_rectangle([(W - 840) // 2, 230, (W + 840) // 2, 670], 32, outline=(210, 205, 195, 255), width=3)

            # Big Reference #35 Signature Title: "혀니의 꿀단지." with vibrant Orange Dot
            sig_p = ease_out_back(elt / 0.45, 1.5)
            f_sig = font(132)
            sig_text = "혀니의 꿀단지"
            tw = d.textlength(sig_text, font=f_sig)
            dot_r = 20
            total_w = tw + 18 + dot_r * 2
            sx = (W - total_w) / 2
            sy = 760 + int((1.0 - sig_p) * 40)
            d.text((sx, sy), sig_text, font=f_sig, fill=INK + (255,))
            # Orange signature period dot (Ref #35 "Claude.")
            dot_cx = int(sx + tw + 18 + dot_r)
            dot_cy = int(sy + 108)
            d.ellipse([dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r], fill=ORANGE + (255,))

            # Sub-caption under signature (Ref #35: "HAREKETLİ GRAFİK TASARIMCISI")
            sub1 = "HEALTH & WELLNESS EDITORIAL  ·  식단 & 영양"
            f_sub1 = font(32)
            d.text(((W - d.textlength(sub1, font=f_sub1)) / 2, 935), sub1, font=f_sub1, fill=INK + (255,))

            sub2 = "성인 1회 80g 기준 · 가열 표시 판독 · 70℃ 2분 조리 · 48시간 냉장"
            f_sub2 = font(30)
            d.text(((W - d.textlength(sub2, font=f_sub2)) / 2, 990), sub2, font=f_sub2, fill=GREY_DARK + (255,))

            # Summary 3-badge row
            draw_pill(fr, "가열 표시 확인", 230, 1085, 0.15, elt, fg=WHITE, bg=INK, size=34, padx=32, h=74)
            draw_pill(fr, "70℃ · 2분 이상", 540, 1085, 0.25, elt, fg=WHITE, bg=ORANGE, size=34, padx=32, h=74)
            draw_pill(fr, "채반 급속 식힘", 850, 1085, 0.35, elt, fg=WHITE, bg=INK, size=34, padx=32, h=74)

            # Main CTA Pill
            draw_pill(fr, "본문에서 전체 가이드 확인하기  →", W / 2, 1215, 0.40, elt, fg=WHITE, bg=ORANGE, size=44, padx=56, h=104)

    # Draw word-synced subtitle bar (only after opening cover finishes)
    if t >= 0.82:
        draw_subtitle(fr, t)

    return fr.convert("RGB")

if __name__ == "__main__":
    print("1/3 오디오 믹싱(나레이션 + 플로우뮤직 BGM + 35번 효과음) 생성 중...")
    mix_wav = build_audio_mix()

    print("2/3 0초 대표 썸네일 및 구간별 검수 스틸컷 저장 중...")
    render_frame(0.0).save(OUT_THUMB_JPG, quality=92)
    stills_dir = os.path.join(ASSET_DIR, "stills_check")
    os.makedirs(stills_dir, exist_ok=True)
    for check_t in [0.2, 2.5, 9.5, 15.0, 21.5, 27.0, 31.5, 35.0]:
        render_frame(check_t).save(os.path.join(stills_dir, f"still_{check_t:04.1f}s.jpg"), quality=88)

    print("3/3 1080x1920 30fps MP4 영상 인코딩 중...")
    os.makedirs(os.path.dirname(OUT_KIT_MP4), exist_ok=True)
    proc = subprocess.Popen([
        "ffmpeg", "-v", "error", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-",
        "-i", mix_wav,
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(DUR), "-movflags", "+faststart",
        OUT_LOCAL_MP4
    ], stdin=subprocess.PIPE)

    for fi in range(TOTAL_FRAMES):
        proc.stdin.write(render_frame(fi / FPS).tobytes())
    proc.stdin.close()
    proc.wait()

    import shutil
    shutil.copy2(OUT_LOCAL_MP4, OUT_KIT_MP4)
    print("DONE! Saved to:", OUT_LOCAL_MP4, "and", OUT_KIT_MP4)

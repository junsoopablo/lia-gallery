#!/usr/bin/env python3
"""
링크 공유용 미리보기 이미지(og-image.png)를 생성합니다.
실행: python3 make_og_image.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(HERE, 'images')
OUT_PATH = os.path.join(HERE, 'og-image.png')

W, H = 1200, 630

# === 색상 ===
CREAM = (255, 248, 240)
PINK = (255, 158, 181)
PINK_SOFT = (255, 214, 224)
LAVENDER_SOFT = (227, 220, 247)
TEXT = (74, 63, 85)
TEXT_SOFT = (122, 111, 133)

FONT_PATH = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'

# === 미리보기에 쓸 작품 6개 (대표) ===
# 색감 좋은 것들 골랐어요 — 무지개 이모, 가족, 꽃과 잎 등
PREVIEW_FILES = [
    'IMG_7361.jpg',  # 이모 (무지개)
    'IMG_7364.jpg',  # 아빠 엄마 나
    'IMG_7359.jpg',  # 예쁜 자연 꽃과 잎
    'IMG_7358.jpg',  # 무지개 로켓
    'IMG_7395.jpg',  # 언젠간 (시 + 꽃)
    'IMG_7373.jpg',  # 하트 빛나는 날개
]


def make_gradient(w, h, top, bottom):
    """세로 그라디언트 이미지."""
    img = Image.new('RGB', (w, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        for x in range(w):
            img.putpixel((x, y), (r, g, b))
    return img


def make_gradient_fast(w, h, top, bottom):
    """더 빠른 그라디언트 — 한 줄씩 그림."""
    img = Image.new('RGB', (w, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        line = Image.new('RGB', (w, 1), (r, g, b))
        img.paste(line, (0, y))
    return img


def rounded_thumb(src_path, size, radius):
    """둥근 모서리 정사각형 썸네일."""
    img = Image.open(src_path).convert('RGB')
    # 정사각형 가운데 크롭
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side)).resize((size, size), Image.LANCZOS)

    # 둥근 모서리 마스크
    mask = Image.new('L', (size, size), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, size, size), radius=radius, fill=255)

    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def main():
    # 배경: 크림 → 라벤더 그라디언트
    bg = make_gradient_fast(W, H, CREAM, LAVENDER_SOFT)
    draw = ImageDraw.Draw(bg)

    # 모서리 장식 점
    draw.ellipse((40, 40, 90, 90), fill=PINK)
    draw.ellipse((W - 110, H - 110, W - 50, H - 50), fill=(181, 168, 224))  # lavender
    draw.ellipse((100, H - 80, 130, H - 50), fill=(255, 228, 156))  # yellow

    # 별 ★
    star_font = ImageFont.truetype(FONT_PATH, 60)
    draw.text((W - 130, 60), '★', font=star_font, fill=(255, 228, 156))

    # 제목
    try:
        title_font = ImageFont.truetype(FONT_PATH, 72)
        sub_font = ImageFont.truetype(FONT_PATH, 32)
    except OSError:
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    title = '리아의 중간정도 크기의 미술관'
    subtitle = '일곱 살 꼬마 작가 리아의 그림 모음'

    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((W - title_w) / 2, 90), title, font=title_font, fill=PINK)

    sub_bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
    sub_w = sub_bbox[2] - sub_bbox[0]
    draw.text(((W - sub_w) / 2, 195), subtitle, font=sub_font, fill=TEXT_SOFT)

    # 6개 썸네일 행
    thumb_size = 160
    gap = 24
    total_w = thumb_size * 6 + gap * 5
    start_x = (W - total_w) // 2
    y = 290

    # 살짝 회전시켜 손글씨 느낌
    rotations = [-3, 2, -1, 3, -2, 1]

    for i, fname in enumerate(PREVIEW_FILES):
        path = os.path.join(IMAGES_DIR, fname)
        if not os.path.exists(path):
            print(f'  ⚠️  파일 없음: {path}')
            continue
        thumb = rounded_thumb(path, thumb_size, 22)

        # 흰색 보더 추가
        bordered = Image.new('RGBA', (thumb_size + 12, thumb_size + 12), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bordered)
        bd.rounded_rectangle((0, 0, thumb_size + 12, thumb_size + 12),
                              radius=28, fill=(255, 255, 255, 230))
        bordered.paste(thumb, (6, 6), thumb)

        rotated = bordered.rotate(rotations[i], resample=Image.BICUBIC, expand=True)

        # 위치 계산 (회전 후 크기 보정)
        rw, rh = rotated.size
        x = start_x + i * (thumb_size + gap) - (rw - thumb_size) // 2
        bg.paste(rotated, (x, y - (rh - thumb_size) // 2), rotated)

    # 하단 안내 문구
    foot_font = ImageFont.truetype(FONT_PATH, 26)
    foot_text = 'junsoopablo.github.io/lia-gallery'
    foot_bbox = draw.textbbox((0, 0), foot_text, font=foot_font)
    foot_w = foot_bbox[2] - foot_bbox[0]
    draw.text(((W - foot_w) / 2, H - 70), foot_text, font=foot_font, fill=TEXT)

    bg.save(OUT_PATH, 'PNG', optimize=True)
    print(f'✓ 생성 완료: {OUT_PATH}')
    print(f'  크기: {W}x{H}, {os.path.getsize(OUT_PATH) // 1024}KB')


if __name__ == '__main__':
    main()

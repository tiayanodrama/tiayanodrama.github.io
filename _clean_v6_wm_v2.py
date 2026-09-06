"""V3 水印去除：手写 BFS 连通域 + 严格暗背景上下文。

策略：
1. 全图找所有亮文字像素（亮 + 暗背景上下文）
2. 手写 BFS 标记连通域（4-邻接）
3. 只保留在右下角区域 + 尺寸合理的连通域
4. bbox 取这些连通域的外接矩形 → 暗背景填充 + 随机星点
"""
import numpy as np
from PIL import Image
from pathlib import Path
import random
from collections import deque

SRC = Path(r"C:/Users/Zhang tian tian/WorkBuddy/北辰青年/角色素材/Pixel_art_portrait_of_a_cute_y_2026-09-06T16-13-55.png")
DST = Path(r"C:/Users/Zhang tian tian/WorkBuddy/北辰青年/个人站/public/images/tt-pixel-main-v6.png")

random.seed(20260906)

img = Image.open(SRC).convert("RGBA")
arr = np.array(img)
h, w = arr.shape[:2]
print(f"[info] image size: {w}x{h}")

rgb = arr[..., :3]
gray = rgb.mean(axis=2)

# ── 1. 找暗背景中的亮文字像素 ─────────────────────────────
dark_bg = gray < 60
bright = (gray > 150) & (rgb.std(axis=2) < 25)

skin = (rgb[..., 0] > 220) & (rgb[..., 1] > 170) & (rgb[..., 2] > 150) & (rgb[..., 2] < 220)
pink = (rgb[..., 0] > 230) & (rgb[..., 1] > 170) & (rgb[..., 1] < 220) & (rgb[..., 2] > 170) & (rgb[..., 2] < 220)
hair_brown = (rgb[..., 0] > 130) & (rgb[..., 0] < 200) & (rgb[..., 1] > 80) & (rgb[..., 1] < 140) & (rgb[..., 2] < 100)

text_pixels = bright & ~skin & ~pink & ~hair_brown
print(f"[detect] text candidate pixels: {text_pixels.sum()}")

# 限定到真正的右下角文字区（w-300, h-180）
roi_mask = np.zeros_like(text_pixels)
roi_mask[h - 180:, w - 300:] = True
text_pixels = text_pixels & roi_mask
print(f"[roi] after ROI restrict: {text_pixels.sum()}")

# ── 2. 手写 BFS 连通域 ──────────────────────────────────────
def label_cc(mask):
    labels = np.zeros(mask.shape, dtype=np.int32)
    h_, w_ = mask.shape
    cur = 0
    for sy in range(h_):
        for sx in range(w_):
            if mask[sy, sx] and labels[sy, sx] == 0:
                cur += 1
                q = deque([(sy, sx)])
                labels[sy, sx] = cur
                while q:
                    y, x = q.popleft()
                    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < h_ and 0 <= nx < w_ and mask[ny, nx] and labels[ny, nx] == 0:
                            labels[ny, nx] = cur
                            q.append((ny, nx))
    return labels, cur

labels, num = label_cc(text_pixels)
print(f"[cc] connected components: {num}")

# 收集右下角的连通域
valid_components = []
for i in range(1, num + 1):
    cy_mask = labels == i
    sz = int(cy_mask.sum())
    if sz < 30 or sz > 5000:
        continue
    ys, xs = np.where(cy_mask)
    cy_min, cy_max = int(ys.min()), int(ys.max())
    cx_min, cx_max = int(xs.min()), int(xs.max())
    # 必须位于右下角文本区（y 下 180 行，x 右 300 列）
    if cy_min < h - 180 or cx_min < w - 300:
        continue
    valid_components.append((i, cy_min, cy_max, cx_min, cx_max, sz))

print(f"[filter] valid watermark components: {len(valid_components)}")
for i, y0, y1, x0, x1, sz in valid_components:
    print(f"  comp {i}: bbox=({y0},{x0})-({y1},{x1}) size={sz}")

if not valid_components:
    print("[warn] no watermark detected, abort")
    raise SystemExit(1)

y0 = min(c[1] for c in valid_components)
y1 = max(c[2] for c in valid_components)
x0 = min(c[3] for c in valid_components)
x1 = max(c[4] for c in valid_components)
print(f"[detect] merged text bbox: ({y0},{x0})-({y1},{x1}) = {y1-y0+1}x{x1-x0+1}")

pad = 12
ay0 = max(0, y0 - pad)
ay1 = min(h, y1 + pad)
ax0 = max(0, x0 - pad)
ax1 = min(w, x1 + pad)
print(f"[clean] clean box: ({ay0},{ax0})-({ay1},{ax1}) = {ay1-ay0+1}x{ax1-ax0+1}")

# ── 3. 采样 + 填充 + 星点 ────────────────────────────────
sample_top = max(0, ay0 - 80)
sample_box = arr[sample_top:ay0, ax0:ax1, :3]
sb_gray = sample_box.mean(axis=2)
dark_pixels = sample_box[sb_gray < 80]
if len(dark_pixels) > 0:
    bg_color = dark_pixels.mean(axis=0).astype(np.uint8)
else:
    bg_color = sample_box.reshape(-1, 3).mean(axis=0).astype(np.uint8)
print(f"[sample] bg fill color RGB = {tuple(int(c) for c in bg_color)}")

for y in range(ay0, ay1):
    for x in range(ax0, ax1):
        arr[y, x, :3] = bg_color
        arr[y, x, 3] = 255

star_count = random.randint(30, 48)
for _ in range(star_count):
    sx = random.randint(ax0, ax1 - 1)
    sy = random.randint(ay0, ay1 - 1)
    palette = [(255, 130, 170), (130, 230, 200), (255, 220, 160), (200, 180, 255)]
    c = random.choice(palette)
    arr[sy, sx, :3] = c
    arr[sy, sx, 3] = 255
    if random.random() < 0.3:
        if sx + 1 < ax1:
            arr[sy, sx + 1, :3] = c
            arr[sy, sx + 1, 3] = 255
    if random.random() < 0.2:
        if sy + 1 < ay1:
            arr[sy + 1, sx, :3] = c
            arr[sy + 1, sx, 3] = 255

DST.parent.mkdir(parents=True, exist_ok=True)
out = Image.fromarray(arr)
out.save(DST, "PNG", optimize=True)
print(f"[done] saved to {DST} ({DST.stat().st_size/1024:.1f} KB)")
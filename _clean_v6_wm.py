"""
去除 v6 立绘右下角"AI成"水印 + 表情图抠图二次修复
- 水印特征：右下角 bbox y=1386..1535, x=724..1023 暗紫色矩形 + 亮色文字
- 用周边星空背景颜色填充该区域
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from PIL import Image
import numpy as np
import os

SRC = r"C:/Users/Zhang tian tian/WorkBuddy/北辰青年/角色素材/tt_pixel_main_v6.png"
DST = r"C:/Users/Zhang tian tian/WorkBuddy/北辰青年/个人站/public/images/tt-pixel-main-v6.png"

im = Image.open(SRC).convert('RGBA')
arr = np.array(im).copy()
h, w = arr.shape[:2]
print(f'src size: {h}x{w}')

# ── 1. 检测水印框（暗紫色 RGB(50,28,50) 在右下角的 bbox）─────────
roi_mask = np.zeros((h, w), dtype=bool)
roi_mask[max(0, h-200):, max(0, w-400):] = True
target_color = (50, 28, 50)
tol = 15
r, g, b = arr[..., 0].astype(int), arr[..., 1].astype(int), arr[..., 2].astype(int)
wm_color = (
    (np.abs(r - target_color[0]) < tol) &
    (np.abs(g - target_color[1]) < tol) &
    (np.abs(b - target_color[2]) < tol) &
    (arr[..., 3] == 255)
)
wm_roi = wm_color & roi_mask
ys, xs = np.where(wm_roi)
print(f'水印暗紫色像素: {len(ys)}')
if len(ys):
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    print(f'水印 bbox: y={y0}..{y1}, x={x0}..{x1}')

    # ── 2. 收集周边星空背景的 RGB（在框外四周采样）────────────
    # 上方 30 行（星空 + 星点）
    src_top = arr[max(0, y0-30):y0, x0:x1+1]
    # 取该范围均值（按行）
    top_avg = src_top[..., :3].mean(axis=0).astype(np.uint8)  # (W, 3)
    print(f'fill color sample: {top_avg[0]}, {top_avg[len(top_avg)//2]}')

    # ── 3. 把水印区域像素替换为星空色 ─────────────────────────
    fill = np.zeros((y1-y0+1, x1-x0+1, 3), dtype=np.uint8)
    fill[:] = top_avg[None, :, :]
    arr[y0:y1+1, x0:x1+1, :3] = fill
    # 水印区域内原本的"AI成"等亮色文字（chroma>30）替换
    # 已经整体 fill 了，不需要再处理

    # ── 4. 加几颗星点让填充区域不那么死板 ─────────────────────
    np.random.seed(99)
    fill_h, fill_w = y1-y0+1, x1-x0+1
    n_stars = int(fill_h * fill_w * 0.0008)  # 与原星空星点密度匹配
    for _ in range(n_stars):
        sy = np.random.randint(0, fill_h)
        sx = np.random.randint(0, fill_w)
        star = np.random.choice([180,150,220,255])  # noqa: 选择星点亮度基值
        # 随机色相（粉/青/暖黄）
        hue = np.random.choice(['pink','cyan','warm'])
        if hue == 'pink':
            sc = (star, star-20, star-30)
        elif hue == 'cyan':
            sc = (star-30, star, star+20)
        else:
            sc = (star, star-40, star-100)
        # 1-2 像素星点
        arr[y0+sy, x0+sx, :3] = sc
        if np.random.random() < 0.4:
            arr[y0+sy, x0+sx+1, :3] = (sc[0]//2, sc[1]//2, sc[2]//2)

    print(f'水印区域已填充 + 加 {n_stars} 颗星点')

# 保存
out = Image.fromarray(arr)
out.save(DST, optimize=True)
print(f'saved: {DST}')

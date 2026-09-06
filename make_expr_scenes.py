"""
为 5 张 tt_expr 表情图生成像素风场景背景并合成人物。
场景：
  happy  户外蓝天 + 草地 + 云朵
  think  图书馆书桌 + 书架
  focus  深夜电脑蓝光 + 桌面
  shy    樱花雨 + 粉色花瓣
  cheer  舞台聚光灯 + 横幅
"""
from PIL import Image, ImageDraw
import numpy as np
import random
import os

SRC_DIR = r"C:/Users/Zhang tian tian/WorkBuddy/北辰青年/角色素材/表情包"   # 原始 PNG（只读）
OUT_DIR = r"C:/Users/Zhang tian tian/WorkBuddy/北辰青年/个人站/public/images"  # 输出目录
random.seed(42)
W, H = 1024, 1024

def px(arr, x, y, color):
    """在 (x,y) 画一个像素方块（边界检查）"""
    if 0 <= x < W and 0 <= y < H:
        arr[y, x] = color

def fill_block(arr, x0, y0, w, h, color):
    if y0 + h > H: h = H - y0
    if x0 + w > W: w = W - x0
    if w <= 0 or h <= 0: return
    arr[y0:y0+h, x0:x0+w] = color

def pixel_circle(arr, cx, cy, r, color):
    """像素圆（用于光晕/灯）"""
    for y in range(max(0, cy-r), min(H, cy+r+1)):
        for x in range(max(0, cx-r), min(W, cx+r+1)):
            if (x-cx)**2 + (y-cy)**2 <= r*r:
                arr[y, x] = color

def draw_cloud(arr, cx, cy, scale=1.0, color=(255,255,255)):
    """像素云朵（一团椭球凸起）"""
    for y in range(-15, 16):
        for x in range(-30, 31):
            if (x*0.7)**2 + (y*1.5)**2 <= (22*scale)**2:
                px(arr, int(cx+x), int(cy+y), color)

def draw_sakura_petal(arr, x, y, color):
    """5 像素樱花瓣（小十字）"""
    for dx, dy in [(0,0),(-3,-1),(3,-1),(0,3),(-2,2),(2,2)]:
        px(arr, x+dx, y+dy, color)

# ─── 1. happy：户外蓝天 + 草地 + 云朵 ─────────────
def scene_happy():
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    # 天空渐变：顶粉紫 → 中浅蓝 → 底淡黄
    for y in range(H):
        t = y / H
        if t < 0.55:
            # 天空
            u = t / 0.55
            r = int(200 + (140-200)*u)
            g = int(170 + (190-170)*u)
            b = int(220 + (255-220)*u)
        else:
            # 草地
            u = (t - 0.55) / 0.45
            r = int(140 + (60-140)*u)
            g = int(180 + (140-180)*u)
            b = int(90 + (60-90)*u)
        arr[y, :] = (r, g, b)
    # 云朵
    for cx, cy in [(180,180),(540,140),(820,220),(350,90)]:
        draw_cloud(arr, cx, cy)
    # 远山
    pts = [(0,560),(150,500),(320,540),(500,490),(700,530),(900,500),(1024,540),(1024,600),(0,600)]
    mountain = np.array(pts, dtype=np.int32)
    from PIL import ImageDraw
    img = Image.fromarray(arr)
    d = ImageDraw.Draw(img)
    d.polygon([(int(x),int(y)) for x,y in pts], fill=(95,130,95))
    arr = np.array(img)
    # 草地小花
    for _ in range(40):
        x = random.randint(0, W-1)
        y = random.randint(620, H-1)
        c = random.choice([(255,200,220),(255,240,180),(220,200,255),(255,255,255)])
        px(arr, x, y, c)
        if random.random() < 0.5:
            px(arr, x+1, y, c)
    # 阳光
    pixel_circle(arr, 920, 130, 60, (255,240,180))
    return arr

# ─── 2. think：图书馆书桌 + 书架 ─────────────
def scene_think():
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    # 深木色背景（暗棕）
    arr[:,:] = (60, 42, 32)
    # 书架（上方 0-520）
    for x0 in range(0, W, 128):
        for shelf_y in [80, 240, 400]:
            # 书架横板
            fill_block(arr, x0, shelf_y+90, 124, 8, (40, 28, 20))
            # 摆放书（不同高度颜色）
            bx = x0 + 8
            for bw, c in [(20,(180,80,60)),(24,(60,100,160)),(18,(200,160,80)),(22,(100,60,140)),(26,(80,140,100)),(14,(160,100,60))]:
                fill_block(arr, bx, shelf_y+90-bw, 4, bw, c)
                bx += 5
                if bx >= x0+120: break
    # 书桌（下方 600-1024）
    fill_block(arr, 0, 720, W, 304, (110, 75, 50))
    # 台灯光晕（左上角）
    for r, alpha in [(180,15),(140,25),(100,30),(70,40),(45,55)]:
        for y in range(max(0, 700-r), min(H, 700+r+1)):
            for x in range(max(0, 200-r), min(W, 200+r+1)):
                if (x-200)**2 + (y-700)**2 <= r*r:
                    p = arr[y, x].astype(np.int32)
                    arr[y, x] = np.clip(p + np.array([alpha, alpha*0.9, alpha*0.5]), 0, 255)
    # 台灯底座
    fill_block(arr, 180, 660, 40, 60, (180, 140, 60))
    return arr

# ─── 3. focus：深夜电脑蓝光 ─────────────
def scene_focus():
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    # 深夜深紫蓝
    for y in range(H):
        t = y / H
        r = int(15 + (8-15)*t)
        g = int(12 + (8-12)*t)
        b = int(35 + (20-35)*t)
        arr[y, :] = (r, g, b)
    # 桌面（下方）
    fill_block(arr, 0, 680, W, 344, (25, 20, 30))
    # 电脑屏幕光晕（中心向外）
    for r, alpha in [(280,8),(220,12),(160,18),(110,25),(70,40)]:
        for y in range(max(0, 500-r), min(H, 500+r+1)):
            for x in range(max(0, 512-r), min(W, 512+r+1)):
                if (x-512)**2 + (y-500)**2 <= r*r:
                    p = arr[y, x].astype(np.int32)
                    arr[y, x] = np.clip(p + np.array([alpha*0.4, alpha*0.8, alpha*1.2]), 0, 255)
    # 屏幕矩形（暗蓝灰）
    fill_block(arr, 360, 380, 320, 200, (40, 60, 90))
    fill_block(arr, 370, 390, 300, 180, (60, 90, 130))
    # 屏幕内容（几行像素字）
    for i, y in enumerate([420, 440, 460, 480, 500]):
        x0 = 380
        for j in range(0, 280, 12):
            if (i+j) % 3 == 0:
                fill_block(arr, x0+j, y, 8, 4, (140, 180, 220))
    # 键盘光带
    fill_block(arr, 350, 760, 340, 30, (50, 70, 110))
    # 杯子的暖光（右边小光斑）
    pixel_circle(arr, 850, 750, 25, (200, 140, 60))
    pixel_circle(arr, 850, 750, 12, (255, 200, 120))
    return arr

# ─── 4. shy：粉色樱花雨（柔光无硬轮廓） ─────────────
def scene_shy():
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    # 粉紫渐变（上深下浅，营造柔光氛围）
    for y in range(H):
        t = y / H
        r = int(252 - (252-235)*t*0.7)
        g = int(220 - (220-205)*t*0.7)
        b = int(232 - (232-228)*t*0.7)
        arr[y, :] = (r, g, b)
    # 远景樱花簇（柔焦感，半径大、淡粉色）
    img = Image.fromarray(arr)
    d = ImageDraw.Draw(img)
    cherry_clusters = [
        (120, 90, 80, (255, 200, 215, 70)),
        (320, 60, 70, (255, 210, 220, 60)),
        (540, 130, 75, (255, 195, 210, 65)),
        (760, 80, 70, (255, 205, 218, 60)),
        (940, 120, 85, (255, 198, 212, 65)),
        (200, 280, 60, (255, 215, 225, 50)),
        (820, 300, 65, (255, 210, 220, 50)),
        (480, 380, 55, (255, 218, 228, 45)),
    ]
    # 把 RGBA 元组转 RGB 贴图（先画到 alpha 蒙版再 alpha_composite）
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for cx, cy, r, rgba in cherry_clusters:
        od.ellipse((cx-r, cy-r, cx+r, cy+r), fill=rgba)
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    arr = np.array(img)
    # 樱花瓣散布（前景）
    petal_colors = [(255,200,210),(255,220,225),(255,235,235),(255,180,195),(255,210,220)]
    for _ in range(180):
        x = random.randint(0, W-1)
        y = random.randint(0, H-1)
        c = random.choice(petal_colors)
        draw_sakura_petal(arr, x, y, c)
    # 少量高光斑（柔焦光点）
    for cx, cy, r, c in [(150,450,18,(255,240,245)),(900,500,22,(255,235,240)),(620,250,15,(255,245,250))]:
        pixel_circle(arr, cx, cy, r, c)
    return arr

# ─── 5. cheer：舞台聚光灯 ─────────────
def scene_cheer():
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    # 深紫底
    arr[:,:] = (18, 10, 28)
    # 多个聚光灯
    for cx, cy, cr in [(280, 0, 220), (760, 0, 200)]:
        for r, alpha in [(cr+50, 4),(cr+30, 7),(cr+15, 10),(cr, 15),(cr-30, 22)]:
            for y in range(max(0, cy-r), min(H, cy+r+1)):
                for x in range(max(0, cx-r), min(W, cx+r+1)):
                    if (x-cx)**2 + (y-cy)**2 <= r*r:
                        p = arr[y, x].astype(np.int32)
                        if r > 100:
                            color = np.array([alpha*0.9, alpha*0.7, alpha*1.2])  # 粉紫
                        else:
                            color = np.array([alpha*1.4, alpha*1.0, alpha*0.4])  # 暖黄
                        arr[y, x] = np.clip(p + color, 0, 255)
    # 舞台地板反光（下方亮带）
    for y in range(720, H):
        t = (y-720) / (H-720)
        for x in range(W):
            p = arr[y, x].astype(np.int32)
            arr[y, x] = np.clip(p + np.array([10*t, 5*t, 15*t]), 0, 255)
    # 欢呼小星点（观众席）
    for _ in range(60):
        x = random.randint(0, W-1)
        y = random.randint(820, H-1)
        c = random.choice([(255,80,140),(120,200,255),(255,200,80)])
        px(arr, x, y, c)
        if random.random() < 0.3:
            px(arr, x+1, y, c)
            px(arr, x, y+1, c)
    # 顶部横幅
    fill_block(arr, 100, 80, 824, 50, (60, 20, 50))
    fill_block(arr, 100, 130, 824, 6, (255, 77, 141))
    return arr

SCENES = {
    'happy': scene_happy,
    'think': scene_think,
    'focus': scene_focus,
    'shy':   scene_shy,
    'cheer': scene_cheer,
}

def cutout_char(char_path):
    """从原始 PNG 抠出人物：flood fill 去掉浅灰/白色影棚背景 + 黑色水印残块。

    背景判定（与边缘连通才删，人物内部同色像素保留）：
      - 灰底：max(RGB)-min(RGB) < 25 且 min(RGB) > 90（低饱和，覆盖浅灰~中灰影棚底）
      - 黑块：sum(RGB) < 60
    """
    im = Image.open(char_path).convert('RGBA')
    arr = np.array(im)
    h, w = arr.shape[:2]
    r, g, b = arr[..., 0].astype(np.int32), arr[..., 1].astype(np.int32), arr[..., 2].astype(np.int32)
    chroma = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    is_bg = ((chroma < 25) & (np.minimum(np.minimum(r, g), b) > 90)) | ((r + g + b) < 60)
    # BFS flood fill：从四条边的背景像素开始
    visited = np.zeros((h, w), dtype=bool)
    stack = []
    for x in range(w):
        for y in (0, h - 1):
            if is_bg[y, x] and not visited[y, x]:
                visited[y, x] = True
                stack.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if is_bg[y, x] and not visited[y, x]:
                visited[y, x] = True
                stack.append((y, x))
    while stack:
        y, x = stack.pop()
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and is_bg[ny, nx] and not visited[ny, nx]:
                visited[ny, nx] = True
                stack.append((ny, nx))
    # 原本就透明的像素也并入
    visited |= (arr[..., 3] == 0)
    arr[visited, 3] = 0
    arr[~visited, 3] = 255
    print(f'  {os.path.basename(char_path)}: 抠掉背景 {int(visited.sum())} 像素 ({visited.sum()/h/w*100:.1f}%), 保留人物 {int((~visited).sum())} 像素')
    return Image.fromarray(arr)

def composite(scene_arr, char_path, out_path):
    """抠人物 → 缩放 → alpha_composite 到场景背景（人物居中偏下）"""
    scene_rgba = Image.fromarray(scene_arr).convert('RGBA')
    char = cutout_char(char_path)
    # 缩放人物到合适大小（约 720px 高）
    target_h = 720
    ratio = target_h / char.height
    new_w = int(char.width * ratio)
    char_resized = char.resize((new_w, target_h), Image.NEAREST)
    # 创建 1024x1024 全透明 canvas，把人物放上去
    person_canvas = Image.new('RGBA', scene_rgba.size, (0, 0, 0, 0))
    x = (W - new_w) // 2
    y = H - target_h - 20
    person_canvas.paste(char_resized, (x, y))
    # 用 alpha_composite 合成到场景背景
    final = Image.alpha_composite(scene_rgba, person_canvas)
    final.save(out_path, optimize=True)
    print(f'{out_path}: 合成完成 ({new_w}x{target_h})')

if __name__ == '__main__':
    for name, fn in SCENES.items():
        print(f'生成 {name} 场景...')
        bg = fn()
        char_path = os.path.join(SRC_DIR, f'tt_expr_{name}.png')
        out_path = os.path.join(OUT_DIR, f'tt_expr_{name}.png')
        composite(bg, char_path, out_path)
    print('全部完成')
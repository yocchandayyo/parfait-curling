# -*- coding: utf-8 -*-
"""フルーツパフェ合体ゲーム用の可愛いイラストを Gemini で生成し透過PNG化する。

- モデル: gemini-2.5-flash-image (Nano Banana)
- 透過背景を要求しつつ、不透過(白背景)で返ってきた場合はフラッドフィルで背景除去
- 256x256 正方形・中央寄せ・透過PNG として assets/ に保存
APIキーは画面に出さない。
"""
import os, sys, time
from io import BytesIO
from pathlib import Path
from collections import deque
from google import genai
from PIL import Image

ROOT = Path(__file__).parent
OUT = ROOT / "assets"
KEY_FILE = Path(r"C:\Users\unico\.gemini_api_key.txt")
MODEL = "gemini-2.5-flash-image"

STYLE = (
    "Cute kawaii cartoon mascot sticker. It has a happy smiling face with big "
    "sparkly round eyes and rosy pink cheeks. Glossy, rounded, chibi style, "
    "bold clean dark outline (die-cut sticker look), bright cheerful pastel "
    "colors, soft cel shading. Centered, single object, isolated on a plain "
    "solid pure white (#FFFFFF) background. No drop shadow, no text, no extra "
    "objects, flat lighting."
)
ITEMS = [
    (0,  "a single round blueberry"),
    (1,  "a single strawberry"),
    (2,  "two shiny red cherries joined by stems"),
    (3,  "a round slice of kiwi fruit"),
    (4,  "a pink peach"),
    (5,  "a round orange mandarin"),
    (6,  "a whole pineapple with green leaves"),
    (7,  "a round green melon"),
    (8,  "a round watermelon"),
    (9,  "a swirl of soft-serve vanilla ice cream in a cone"),
    (10, "a fancy colorful fruit parfait in a tall glass with cream and a cherry on top"),
]

def load_key():
    k = os.environ.get("GEMINI_API_KEY", "").strip()
    if not k and KEY_FILE.exists():  # 最新キーはキーファイル優先
        k = KEY_FILE.read_text(encoding="utf-8").strip()
    if not k:
        env = ROOT.parent / ".env"
        if env.exists():
            for line in env.read_text(encoding="utf-8").splitlines():
                if line.startswith("GEMINI_API_KEY="):
                    k = line.split("=", 1)[1].strip()
    if not k:
        print("[error] APIキーが見つかりません"); sys.exit(1)
    return k

def gen_image(client, prompt):
    resp = client.models.generate_content(model=MODEL, contents=prompt)
    for part in resp.candidates[0].content.parts:
        if getattr(part, "inline_data", None) and part.inline_data.data:
            return part.inline_data.data
    return None

def border_is_transparent(img):
    a = img.split()[3]
    w, h = img.size
    px = a.load()
    vals = [px[x, 0] for x in range(0, w, 8)] + [px[x, h-1] for x in range(0, w, 8)] \
         + [px[0, y] for y in range(0, h, 8)] + [px[w-1, y] for y in range(0, h, 8)]
    return (sum(vals) / max(1, len(vals))) < 25

def flood_remove_bg(img, tol=26):
    """四隅の色をキーにして縁からフラッドフィルで背景を透明化。"""
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()
    corners = [px[0, 0], px[w-1, 0], px[0, h-1], px[w-1, h-1]]
    kr = sum(c[0] for c in corners) // 4
    kg = sum(c[1] for c in corners) // 4
    kb = sum(c[2] for c in corners) // 4
    def match(p):
        return abs(p[0]-kr) <= tol and abs(p[1]-kg) <= tol and abs(p[2]-kb) <= tol
    seen = bytearray(w*h)
    dq = deque()
    for x in range(w):
        for y in (0, h-1):
            i = y*w+x
            if not seen[i] and match(px[x, y]): seen[i]=1; dq.append((x,y))
    for y in range(h):
        for x in (0, w-1):
            i = y*w+x
            if not seen[i] and match(px[x, y]): seen[i]=1; dq.append((x,y))
    while dq:
        x, y = dq.popleft()
        px[x, y] = (px[x, y][0], px[x, y][1], px[x, y][2], 0)
        for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0 <= nx < w and 0 <= ny < h:
                i = ny*w+nx
                if not seen[i] and match(px[nx, ny]):
                    seen[i]=1; dq.append((nx, ny))
    return img

def process(data, out_path):
    img = Image.open(BytesIO(data)).convert("RGBA")
    if max(img.size) > 640:  # フラッドフィル高速化
        img.thumbnail((640, 640), Image.LANCZOS)
    if not border_is_transparent(img):
        img = flood_remove_bg(img)
    bbox = img.getbbox()
    if bbox: img = img.crop(bbox)
    s = max(img.size)
    sq = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    sq.paste(img, ((s-img.size[0])//2, (s-img.size[1])//2))
    sq = sq.resize((256, 256), Image.LANCZOS)
    sq.save(out_path)
    # 透過率
    alpha = sq.split()[3]
    opaque = sum(1 for v in alpha.getdata() if v > 30)
    return round(100*opaque/(256*256), 1)

def main():
    only = None
    if len(sys.argv) > 1:
        only = [int(x) for x in sys.argv[1].split(",")]
    OUT.mkdir(exist_ok=True)
    client = genai.Client(api_key=load_key())
    for idx, desc in ITEMS:
        if only is not None and idx not in only:
            continue
        prompt = f"{desc}. {STYLE}"
        print(f"[gen] item{idx} ({desc[:30]})...", flush=True)
        for attempt in range(3):
            try:
                data = gen_image(client, prompt)
                if data:
                    pct = process(data, OUT / f"item{idx}.png")
                    print(f"  [ok] item{idx}.png  不透明率={pct}%", flush=True)
                    break
                print("  [warn] 画像データなし、再試行", flush=True)
            except Exception as e:
                print(f"  [retry {attempt+1}] {str(e)[:100]}", flush=True)
                time.sleep(8)
        time.sleep(5)  # レート制限対策
    print("[done]")

if __name__ == "__main__":
    main()

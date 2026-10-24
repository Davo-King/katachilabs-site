#!/usr/bin/env python3
"""Optimise Bookmark+ images from /workspace/bookmarkplus-assets (originals untouched) into labs/bookmark-plus/img/."""
import os
from PIL import Image
SRC="/workspace/bookmarkplus-assets"; OUT=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"labs/bookmark-plus/img")
M={"1-dashboard-dark":"dashboard-dark","2-dashboard-light":"dashboard-light","3-search":"search","4-popup":"popup","5-settings":"settings"}
for s,n in M.items():
    im=Image.open(f"{SRC}/{s}.png").convert("RGB")
    for w in (1280,640):
        r=im if w==1280 else im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
        r.save(f"{OUT}/{n}-{w}.webp","WEBP",quality=82,method=6)
        r.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.FLOYDSTEINBERG).save(f"{OUT}/{n}-{w}.png",optimize=True)
p=Image.open(f"{SRC}/promo-small-440x280.png").convert("RGB")
p.save(f"{OUT}/promo-440.webp","WEBP",quality=85,method=6); p.save(f"{OUT}/promo-440.png",optimize=True)

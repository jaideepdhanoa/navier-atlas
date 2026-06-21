#!/usr/bin/env python3
"""Deterministic N30/N35 composite helper.

This intentionally does not call an image-generation provider. It takes saved inputs and produces a reproducible final deck image.
"""
import argparse
from pathlib import Path
from PIL import Image, ImageEnhance

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--background', required=True)
    ap.add_argument('--vessel', required=True)
    ap.add_argument('--mask')
    ap.add_argument('--out', required=True)
    ap.add_argument('--x', type=float, default=0.56, help='vessel center x as fraction of width')
    ap.add_argument('--y', type=float, default=0.66, help='vessel center y as fraction of height')
    ap.add_argument('--scale', type=float, default=0.34, help='vessel width as fraction of background width')
    ap.add_argument('--vessel-opacity', type=float, default=1.0)
    ap.add_argument('--bg-darken', type=float, default=0.92)
    args=ap.parse_args()
    bg=Image.open(args.background).convert('RGBA')
    bg=ImageEnhance.Brightness(bg).enhance(args.bg_darken)
    vessel=Image.open(args.vessel).convert('RGBA')
    target_w=max(1, int(bg.width*args.scale))
    target_h=max(1, int(vessel.height*target_w/vessel.width))
    vessel=vessel.resize((target_w,target_h), Image.LANCZOS)
    if args.vessel_opacity < 1:
        alpha=vessel.getchannel('A').point(lambda p: int(p*args.vessel_opacity))
        vessel.putalpha(alpha)
    if args.mask:
        mask=Image.open(args.mask).convert('L').resize(vessel.size, Image.LANCZOS)
        vessel.putalpha(mask)
    x=int(bg.width*args.x-target_w/2); y=int(bg.height*args.y-target_h/2)
    bg.alpha_composite(vessel, (x,y))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    bg.convert('RGB').save(args.out, quality=94)
if __name__=='__main__': main()

#!/usr/bin/env python3
"""Deep inspection: JS content, raw HTML pages, media filesystem."""
import os, re

LV7 = r"D:\LLM\sites\animal\_light_v7"

print("=== MEDIA DIRECTORY ===")
media = os.path.join(LV7, "assets", "media")
if os.path.isdir(media):
    for d in sorted(os.listdir(media)):
        dd = os.path.join(media, d)
        if os.path.isdir(dd):
            files = [f for f in os.listdir(dd) if os.path.isfile(os.path.join(dd, f))]
            print(f"  {d}: {len(files)} files")
            for f in files:
                fp = os.path.join(dd, f)
                print(f"    {f} ({os.path.getsize(fp)} bytes)")
else:
    print("  NO assets/media/")

print("\n=== SITE-V7.JS ===")
js = os.path.join(LV7, "assets", "js", "site-v7.js")
if os.path.exists(js):
    with open(js, "r", encoding="utf-8") as f:
        jc = f.read()
    print(f"  Size: {len(jc)} bytes")
    print(f"\n  FULL CONTENT:")
    print(jc)
else:
    print("  MISSING")

print("\n=== RAW zhangbiaowang index.html ===")
with open(os.path.join(LV7, "zhangbiaowang", "index.html"), "r", encoding="utf-8") as f:
    c = f.read()
print(c)

print("\n=== RAW zhangbiaowang-ruminant index.html ===")
with open(os.path.join(LV7, "zhangbiaowang-ruminant", "index.html"), "r", encoding="utf-8") as f:
    c = f.read()
print(c)

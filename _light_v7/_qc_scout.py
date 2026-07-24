#!/usr/bin/env python3
"""Scout _light_v7: size, img refs, forbidden patterns."""
import os, re

LV7 = r"D:\LLM\sites\animal\_light_v7"
PRODUCTS = ["baomiaowang","junzaiwang","kelionwang","duoluanzhuang",
            "zhangbiaowang","changbiaowang-ruminant","zujinwang"]

print("="*60)
print("SCOUT: _light_v7 page inspection")
print("="*60)

# 1. Page sizes
for p in ["index"] + PRODUCTS:
    path = os.path.join(LV7, p, "index.html")
    if os.path.exists(path):
        sz = os.path.getsize(path)
        print(f"  {p:30s} {sz:>6} bytes")
    else:
        print(f"  {p:30s} MISSING")

# 2. assets directory
print("\n-- assets/ --")
assets = os.path.join(LV7, "assets")
if os.path.isdir(assets):
    for root, dirs, files in os.walk(assets):
        for f in files:
            fp = os.path.join(root, f)
            sz = os.path.getsize(fp)
            rel = os.path.relpath(fp, LV7)
            print(f"  {rel} ({sz} bytes)")
else:
    print("  NO assets directory")

# 3. Other dirs
print("\n-- top-level dirs --")
for d in sorted(os.listdir(LV7)):
    dp = os.path.join(LV7, d)
    if os.path.isdir(dp) and d not in ["index"] + PRODUCTS and d != "assets":
        print(f"  {d}/")

# 4. Per-page img refs + forbidden checks
print("\n-- Per-page img references + forbidden content --")
for p in PRODUCTS:
    path = os.path.join(LV7, p, "index.html")
    if not os.path.exists(path):
        print(f"\n{p}: FILE MISSING")
        continue
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    imgs = re.findall(r'src="([^"]+)"', c)
    bg = re.findall(r"background-image:\s*url\(['\"]?([^'\")]+)['\"]?\)", c)
    all_refs = imgs + bg
    print(f"\n{p}: {len(all_refs)} img refs, {len(c)} chars")
    for r in all_refs:
        exists = "FILE" if os.path.exists(os.path.join(LV7, r if not r.startswith("..") else os.path.normpath(os.path.join(LV7, p, r)))) else "MISSING"
        print(f"  [{exists:7s}] {r}")
    
    # forbidden content
    forbidden_words = [
        "活力旺","VitalBoost","subtilisin","枯草芽孢","Bacillus subtilis",
        "SARA","瘤胃pH","1:[0-9]","ch-OSA","蝦青素","astaxanthin","異黃酮",
        "Cornell","EnzyGrow","售價","售价"
    ]
    for fw in forbidden_words:
        if re.search(fw, c):
            print(f'  ⚠️ FORBIDDEN CONTENT: "{fw}" found')

    # forbidden old image patterns
    old_pats = ["egg-quality-showcase","broiler_carcass","before-after","tilapia-",
                "farm-aerial","vitality-plus-concept","vitalboost","VitalBoost",
                "ai-generated","AI-生成"]
    for pat in old_pats:
        if pat.lower() in c.lower():
            print(f'  ⚠️ OLD IMAGE REF: "{pat}" found')

    # Single h1
    h1s = re.findall(r'<h1[\s>]', c)
    if len(h1s) != 1:
        print(f'  ⚠️ H1 count: {len(h1s)} (expected 1)')
    else:
        print(f'  ✅ H1 count: 1')
    
    # Footer
    if "毅展" in c:
        print(f'  ✅ footer: 毅展')
    elif "泽林" in c or "澤林" in c:
        print(f'  ⚠️ footer: contains 泽林/澤林')
    
    # 041 / ◷
    if "补强中" in c or "◷" in c:
        print(f'  ✅ contains ◷ / 补强中')
    
    # contact-blank
    if "contact-blank" in c:
        print(f'  ✅ contact-blank')
    else:
        print(f'  ⚠️ no contact-blank')

# 5. index page
print("\n-- index --")
idx = os.path.join(LV7, "index", "index.html")
if os.path.exists(idx):
    with open(idx, "r", encoding="utf-8") as f:
        c = f.read()
    print(f"  {len(c)} bytes")
    imgs = re.findall(r'src="([^"]+)"', c)
    for i in imgs:
        print(f"  src: {i}")
else:
    print("  No index page")

# 6. dist_v4 forbidden patterns
print("\n-- dist_v4 old image check --")
dv4 = r"D:\LLM\sites\animal\dist_v4"
if os.path.isdir(dv4):
    old_pats = ["egg-quality-showcase","broiler_carcass","tilapia-","farm-aerial",
                "vitality-plus-concept","vitalboost","VitalBoost"]
    for pat in old_pats:
        count = 0
        for root, dirs, files in os.walk(dv4):
            for f in files:
                if pat.lower() in f.lower():
                    count += 1
                    if count <= 3:
                        print(f'  OLD: {os.path.relpath(os.path.join(root,f), dv4)}')
        if count > 3:
            print(f'  ... and {count-3} more')
        if count == 0:
            print(f'  No "{pat}" in dist_v4')

print("\nDone.")

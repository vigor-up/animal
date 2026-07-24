#!/usr/bin/env python3
"""QV Verification: forbidden words final sweep, 041 check, H1 count, css check."""
import os, re

LV7 = r"D:\LLM\sites\animal\_light_v7"
PRODUCTS = ["baomiaowang","junzaiwang","kelionwang","duoluanzhuang","zhangbiaowang",
            "zhangbiaowang-ruminant","zujinwang"]

print("=== QV VERIFICATION ===")
print()

for p in PRODUCTS:
    path = os.path.join(LV7, p, "index.html")
    if not os.path.exists(path):
        print(f"[{p}] FILE MISSING")
        continue
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    
    checks = {}
    
    # 1. Forbidden words
    fwords = ["活力旺","VitalBoost","枯草芽孢","Bacillus subtilis","subtilisin",
              "SARA","瘤胃pH","ch-OSA","蝦青素","astaxanthin","異黃酮",
              "Cornell","EnzyGrow","售價","售价"]
    found = [fw for fw in fwords if re.search(fw, c)]
    checks["forbidden"] = len(found) == 0
    if found:
        checks["forbidden_detail"] = found
    
    # 2. 1:N ratio
    checks["no_1N"] = not bool(re.search(r"1:[0-9]", c))
    
    # 3. H1 count
    h1s = len(re.findall(r"<h1[\s>]", c))
    checks["h1_ok"] = h1s == 1
    checks["h1_count"] = h1s
    
    # 4. Footer
    checks["footer_yizhan"] = "毅展" in c
    checks["footer_zelin"] = "泽林" in c or "澤林" in c
    
    # 5. 041 mark
    checks["has_buqiang"] = "补强中" in c or "\u25f7" in c
    
    # 6. contact-blank
    checks["contact_blank"] = "contact-blank" in c
    
    # 7. canonical
    checks["canonical"] = 'rel="canonical"' in c
    
    # 8. og:image
    checks["og_image"] = 'og:image' in c
    
    # 9. twitter:card
    checks["twitter_card"] = 'twitter:card' in c
    
    # 10. hreflang
    checks["hreflang"] = 'hreflang' in c
    
    # 11. JSON-LD
    checks["jsonld"] = 'application/ld+json' in c
    
    # 12. Old image patterns in src
    oldpats = ["egg-quality-showcase","broiler_carcass","tilapia-","farm-aerial",
               "vitality-plus-concept","vitalboost"]
    img_srcs = re.findall(r'src="([^"]+)"', c) + re.findall(r'background-image.*?url\([\'"]?([^\'")]+)[\'"]?\)', c)
    old_refs = []
    for s in img_srcs:
        for pat in oldpats:
            if pat.lower() in s.lower():
                old_refs.append(s)
                break
    checks["old_img_refs"] = len(old_refs) == 0
    if old_refs:
        checks["old_img_refs_detail"] = old_refs
    
    # 13. All images from assets/media/
    all_srcs = re.findall(r'src="([^"]+)"', c)
    media_refs = [s for s in all_srcs if "assets/media/" in s or "/assets/media/" in s]
    non_media = [s for s in all_srcs if s.endswith((".png",".jpg",".webp")) and "assets/media/" not in s and "svg" not in s]
    checks["all_from_media"] = len(non_media) == 0
    if non_media:
        checks["non_media_refs"] = non_media
    
    # Print
    pass_count = sum(1 for k, v in checks.items() if v is True)
    fail_items = [k for k, v in checks.items() if v is False or (isinstance(v, list) and len(v) > 0)]
    
    print(f"[{p}]")
    print(f"  forbidden={checks['forbidden']} 1:N={checks['no_1N']} H1={checks['h1_count']}")
    print(f"  footer_yizhan={checks['footer_yizhan']} zelin={checks['footer_zelin']} 041={checks['has_buqiang']} contact={checks['contact_blank']}")
    print(f"  canonical={checks['canonical']} og={checks['og_image']} tw={checks['twitter_card']} hreflang={checks['hreflang']} ld={checks['jsonld']}")
    print(f"  old_refs={checks['old_img_refs']} media_only={checks['all_from_media']}")
    if checks.get("forbidden_detail"):
        print(f"  FORBIDDEN: {checks['forbidden_detail']}")
    if checks.get("old_img_refs_detail"):
        print(f"  OLD IMG: {checks['old_img_refs_detail']}")
    if checks.get("non_media_refs"):
        print(f"  NON-MEDIA IMG: {checks['non_media_refs']}")
    if fail_items:
        print(f"  FAIL: {fail_items}")
    else:
        print(f"  ALL PASS")
    print()

# CSS check
print("=== CSS checks ===")
css_dir = os.path.join(LV7, "assets", "css")
if os.path.isdir(css_dir):
    for f in sorted(os.listdir(css_dir)):
        fp = os.path.join(css_dir, f)
        print(f"  {f}: {os.path.getsize(fp)} bytes")

# Index check
print("\n=== Index check ===")
idx = os.path.join(LV7, "index", "index.html")
if os.path.exists(idx):
    with open(idx, "r", encoding="utf-8") as f:
        c = f.read()
    print(f"  EXISTS: {len(c)} bytes")
    for chk in ["canonical","og:image","twitter:card","hreflang","application/ld+json"]:
        print(f"  {chk}: {chk in c}")
else:
    print("  MISSING")
    # Check if index dir exists at all
    idx_dir = os.path.join(LV7, "index")
    if os.path.isdir(idx_dir):
        print(f"  index dir exists with {len(os.listdir(idx_dir))} items:")
        for f in os.listdir(idx_dir):
            print(f"    {f}")
    else:
        print("  No index directory exists")
        print("  Listing root:")
        for f in sorted(os.listdir(LV7)):
            fp = os.path.join(LV7, f)
            print(f"    {'D' if os.path.isdir(fp) else 'F'} {f}")

print("\n=== Old image count in assets/ ===")
assets = os.path.join(LV7, "assets")
old_pats = ["egg-quality-showcase","broiler_carcass","tilapia-","farm-aerial",
            "vitality-plus-concept","vitalboost","ai-generated"]
count = 0
for root, dirs, files in os.walk(assets):
    for f in files:
        for pat in old_pats:
            if pat.lower() in f.lower():
                count += 1
                if count <= 5:
                    print(f"  {os.path.relpath(os.path.join(root,f), LV7)}")
                break
if count > 5:
    print(f"  ... +{count-5} more")
print(f"  Total old images: {count}")

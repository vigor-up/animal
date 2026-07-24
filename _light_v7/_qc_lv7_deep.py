#!/usr/bin/env python3
"""EVOX2-0723-LV7-QC: Full audit of _light_v7 pages."""
import os, re, json

LV7 = r"D:\LLM\sites\animal\_light_v7"
PRODUCTS = ["baomiaowang","junzaiwang","kelionwang","duoluanzhuang","zhangbiaowang",
            "changbiaowang-ruminant","zujinwang"]

FORBIDDEN_WORDS = [
    "活力旺","VitalBoost","枯草芽孢","Bacillus subtilis","subtilisin",
    "SARA","瘤胃pH","ch-OSA","蝦青素","astaxanthin","異黃酮",
    "Cornell","EnzyGrow","售價","售价"
]

FORBIDDEN_OLD_PATTERNS = [
    "egg-quality-showcase","broiler_carcass","tilapia-","farm-aerial",
    "vitality-plus-concept","vitalboost"
]

results = {}

# ── All dirs in v7 ──
print("=== PAGE INVENTORY ===")
for p in ["index"] + PRODUCTS + ["zhangbiaowang-ruminant"]:
    path = os.path.join(LV7, p, "index.html")
    if os.path.exists(path):
        sz = os.path.getsize(path)
        print(f"  {p:35s} {sz:>6} bytes")
    else:
        print(f"  {p:35s} MISSING")

# ── Per-page analysis ──
print("\n=== PER-PAGE ANALYSIS ===")
for p in PRODUCTS + ["zhangbiaowang-ruminant"]:
    path = os.path.join(LV7, p, "index.html")
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    
    page = {"name": p, "bytes": len(c)}
    issues = []
    
    # Check if page is too small (likely broken)
    if len(c) < 5000:
        issues.append("SUSPICIOUSLY_SMALL")
    
    # CSS/JS refs
    css_refs = re.findall(r'href="([^"]+\.css)"', c)
    js_refs = re.findall(r'src="([^"]+\.js)"', c)
    
    # img refs
    src_refs = re.findall(r'src="([^"]+)"', c)
    bg_refs = re.findall(r"""(?:background|background-image)\s*:\s*url\(['"]?([^'")\s]+)['"]?\)""", c, re.IGNORECASE)
    all_refs = src_refs + bg_refs
    
    page["css"] = css_refs
    page["js"] = js_refs
    page["img_refs"] = []
    
    for r in all_refs:
        if r.endswith(".js"):
            continue
        if r.endswith(".css"):
            continue
        
        rp = r
        if r.startswith("/"):
            rp = os.path.normpath(LV7 + r)
        elif r.startswith("http"):
            rp = r  # external, skip file check
        else:
            rp = os.path.normpath(os.path.join(LV7, p, r))
        
        exists = os.path.exists(rp) if not r.startswith("http") else "EXTERNAL"
        page["img_refs"].append({"src": r, "resolved": rp, "exists": exists})
    
    # Forbidden content
    page["forbidden_found"] = []
    for fw in FORBIDDEN_WORDS:
        if re.search(fw, c):
            page["forbidden_found"].append(fw)
            issues.append(f"FORBIDDEN_WORD:{fw}")
    
    # Old image patterns
    page["old_img_patterns"] = []
    for pat in FORBIDDEN_OLD_PATTERNS:
        if pat.lower() in c.lower():
            page["old_img_patterns"].append(pat)
            issues.append(f"OLD_IMG_PATTERN:{pat}")
    
    # H1 count
    h1s = re.findall(r"<h1[\s>]", c)
    page["h1_count"] = len(h1s)
    if len(h1s) != 1:
        issues.append(f"H1_COUNT:{len(h1s)}")
    
    # Footer
    page["footer_yizhan"] = "毅展" in c
    page["footer_zelin"] = "泽林" in c or "澤林" in c
    if "泽林" in c or "澤林" in c:
        issues.append("ZELIN_FOOTER")
    
    # 1:N ratio
    if re.search(r"1:[0-9]", c):
        page["has_1N_ratio"] = True
        issues.append("HAS_1:N_RATIO")
    
    # contact-blank
    page["contact_blank"] = "contact-blank" in c
    if not page["contact_blank"]:
        issues.append("NO_CONTACT_BLANK")
    
    # 041/补强中
    page["has_buqiang"] = "补强中" in c or "\u25f7" in c
    
    # EN translation check
    page["en_untranslated"] = []
    en_divs = re.findall(r'<div[^>]*data-lang="en"[^>]*>', c)
    if en_divs:
        en_parts = re.split(r'<div[^>]*data-lang="en"[^>]*>', c)
        for i, part in enumerate(en_parts[1:], 1):
            # Get content until next data-lang
            content = re.split(r'<div[^>]*data-lang=', part)[0]
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', '', content).strip()
            # Check for meaningful Chinese content (not just icons/labels)
            chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
            if chinese_chars > 10:  # More than 10 Chinese chars in EN section
                page.setdefault("en_untranslated", [])
                preview = text[:100].replace("\n", " ").strip()
                page["en_untranslated"].append(preview)
    
    page["issues"] = issues
    results[p] = page
    
    print(f"\n--- {p} ---")
    print(f"  Size: {len(c)} bytes | H1: {len(h1s)} | contact-blank: {page['contact_blank']} | 041: {page['has_buqiang']}")
    print(f"  CSS: {len(css_refs)} | JS: {len(js_refs)} | Img refs: {len(all_refs)}")
    missing = [r for r in page["img_refs"] if r["exists"] != "FILE" and r["exists"] != "EXTERNAL"]
    if missing:
        for m in missing:
            print(f"  MISSING: {m['src']}")
    if page["forbidden_found"]:
        for fw in page["forbidden_found"]:
            print(f"  FORBIDDEN WORD: {fw}")
    if page["old_img_patterns"]:
        for pat in page["old_img_patterns"]:
            print(f"  OLD IMG PATTERN: {pat}")
    if page["en_untranslated"]:
        print(f"  EN SECTION WITH {len(page['en_untranslated'])} CHINESE CONTENT:")
        for u in page["en_untranslated"]:
            print(f"    -> {u[:80]}...")
    if page.get("has_1N_ratio"):
        print("  HAS_1:N_RATIO")
    if issues:
        print(f"  ISSUES: {'; '.join(issues)}")
    else:
        print("  ALL OK")

# ── Index page ──
print("\n=== INDEX PAGE ===")
idx = os.path.join(LV7, "index", "index.html")
if os.path.exists(idx):
    with open(idx, "r", encoding="utf-8") as f:
        c = f.read()
    print(f"  Size: {len(c)} bytes")
    src_refs = re.findall(r'src="([^"]+)"', c)
    for r in src_refs:
        rp = r
        if r.startswith("/"):
            rp = LV7 + r
        elif not r.startswith("http"):
            rp = os.path.normpath(os.path.join(LV7, "index", r))
        exists = os.path.exists(rp) if not r.startswith("http") else "EXT"
        print(f"  src: {r} -> [{exists}]")
    
    # Forbidden
    for fw in FORBIDDEN_WORDS:
        if re.search(fw, c):
            print(f"  FORBIDDEN: {fw}")
    # H1
    h1s = len(re.findall(r"<h1[\s>]", c))
    print(f"  H1: {h1s}")
    # Footer
    if "毅展" in c: print("  Footer: 毅展 OK")
elif os.path.exists(os.path.join(LV7, "index")):
    print("  No index.html in index/")
    for f in os.listdir(os.path.join(LV7, "index")):
        print(f"  {f}")
else:
    print("  No index directory")

# ── Old images in assets/ ──
print("\n=== OLD IMAGES IN assets/ (should be cleaned) ===")
assets = os.path.join(LV7, "assets")
old_pats_to_check = ["egg-quality-showcase","broiler_carcass","tilapia-","farm-aerial",
                     "vitality-plus-concept","vitalboost","ai-generated"]
found_old = 0
for root, dirs, files in os.walk(assets):
    for f in files:
        for pat in old_pats_to_check:
            if pat.lower() in f.lower():
                rel = os.path.relpath(os.path.join(root, f), LV7)
                print(f"  OLD: {rel}")
                found_old += 1
                break
if found_old == 0:
    print("  None found")

# ── Summary ──
print("\n=== SUMMARY ===")
problem_pages = []
for p, r in sorted(results.items()):
    if r["issues"]:
        problem_pages.append((p, r["issues"]))
        print(f"  [ISSUE] {p}: {r['issues']}")
    else:
        print(f"  [OK]    {p}")

# Old images in assets
print(f"\n  Old images in assets/: {found_old}")

if problem_pages:
    print(f"\n  TOTAL ISSUES: {len(problem_pages)} pages with problems")
else:
    print("\n  NO ISSUES")

# ── JSON output for verification ──
with open(os.path.join(LV7, "_qc_lv7_results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\nResults written to _qc_lv7_results.json")

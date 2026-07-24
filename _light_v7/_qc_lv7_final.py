#!/usr/bin/env python3
"""Final audit: verify all pages, missing translations, unref'd old images."""
import os, re, json, glob

LV7 = r"D:\LLM\sites\animal\_light_v7"

# 1. All pages present
print("=== QV FINAL: ALL PAGES ===")
pages = ["index.html", "baomiaowang/index.html", "junzaiwang/index.html",
         "kelionwang/index.html", "duoluanzhuang/index.html",
         "zhangbiaowang/index.html", "zhangbiaowang-ruminant/index.html",
         "zujinwang/index.html"]
for p in pages:
    fp = os.path.join(LV7, p.replace("/", "\\"))
    if os.path.exists(fp):
        sz = os.path.getsize(fp)
        print("  [OK] %s (%d bytes)" % (p, sz))
    else:
        print("  [MISS] %s" % p)

# 2. Verify ALL img refs resolve (URL decode)
print("\n=== IMG RESOLUTION (URL-decoded) ===")
import urllib.parse as UP
issues_img = 0
for p in ["baomiaowang","junzaiwang","kelionwang","duoluanzhuang","zhangbiaowang","zhangbiaowang-ruminant","zujinwang"]:
    path = os.path.join(LV7, p, "index.html")
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    srcs = re.findall(r'src="([^"]*\.(?:png|jpg|webp))"', c)
    bgs = re.findall(r"background(-image)?:\s*[^;]*url\(['\"]?([^'\")]+)(?:png|jpg|webp)['\"]?\)", c)
    refs = srcs + [bg[1] for bg in bgs]
    
    for r in refs:
        if r.startswith("http"):
            continue
        # URL decode
        decoded = UP.unquote(r)
        # Resolve absolute path
        if decoded.startswith("/"):
            rp = LV7 + decoded.replace("/", "\\")
        else:
            rp = os.path.normpath(os.path.join(LV7, p, decoded))
        if not os.path.exists(rp):
            print("  [MISS] %s -> %s" % (r, rp))
            issues_img += 1
        else:
            sz = os.path.getsize(rp)
            print("  [OK] %s (%d bytes)" % (r, sz))
if issues_img == 0:
    print("  ALL images resolved")

# 3. Forbidden words per page + 041 + H1 + footer
print("\n=== COMPLIANCE CHECK ===")
for p in ["index.html", "baomiaowang/index.html", "junzaiwang/index.html",
          "kelionwang/index.html", "duoluanzhuang/index.html",
          "zhangbiaowang/index.html", "zhangbiaowang-ruminant/index.html",
          "zujinwang/index.html"]:
    path = os.path.join(LV7, p.replace("/", "\\"))
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    
    # Forbidden words
    fwords = {"活力旺":"forbidden","VitalBoost":"forbidden","枯草芽孢":"forbidden",
              "Bacillus subtilis":"forbidden","subtilisin":"forbidden",
              "SARA":"forbidden","瘤胃pH":"forbidden",
              "ch-OSA":"forbidden","蝦青素":"forbidden","astaxanthin":"forbidden",
              "異黃酮":"forbidden","Cornell":"forbidden","EnzyGrow":"forbidden",
              "售價":"forbidden","售价":"forbidden"}
    found = [(w, t) for w, t in fwords.items() if w in c]
    
    # Footer
    yizhan = "毅展" in c
    zelin = "泽林" in c or "澤林" in c
    
    # H1
    h1s = len(re.findall(r"<h1[\s>]", c))
    
    # 041
    buqiang = "补强中" in c or "\u25f7" in c
    
    # contact
    contact = "contact-blank" in c
    
    # 1:N
    ratio_1n = bool(re.search(r"1:[0-9]", c))
    
    issues = []
    if found: issues.append("FORBIDDEN:%s" % [w for w,_ in found])
    if zelin: issues.append("ZELIN_IN_FOOTER")
    if h1s != 1: issues.append("H1=%d" % h1s)
    if not contact: issues.append("NO_CONTACT_BLANK")
    if ratio_1n: issues.append("1:N_RATIO")
    
    print("  [%s]" % p)
    print("    H1=%d footer_yizhan=%s zelin=%s 041=%s contact=%s 1:N=%s" % (
        h1s, yizhan, zelin, buqiang, contact, ratio_1n))
    if issues:
        print("    ISSUES: %s" % "; ".join(issues))
    else:
        print("    ALL CLEAN")

# 4. Verify old images are NOT referenced
print("\n=== OLD IMG UNREFERENCED VERIFICATION ===")
old_pats = ["egg-quality-showcase","broiler_carcass","tilapia-","farm-aerial",
            "vitality-plus-concept","vitalboost"]
all_html = ""
for p in ["index.html"] + [x+"/index.html" for x in ["baomiaowang","junzaiwang","kelionwang",
            "duoluanzhuang","zhangbiaowang","zhangbiaowang-ruminant","zujinwang"]]:
    path = os.path.join(LV7, p.replace("/", "\\"))
    if os.path.exists(path):
        all_html += open(path, "r", encoding="utf-8").read()

# Also check CSS + JS
for p in ["assets/css/site.css", "assets/css/site-v7.css", "assets/js/site-v7.js"]:
    path = os.path.join(LV7, p.replace("/", "\\"))
    if os.path.exists(path):
        all_html += open(path, "r", encoding="utf-8").read()

referenced_old = []
for pat in old_pats:
    if pat.lower() in all_html.lower():
        referenced_old.append(pat)
        print("  [REFERENCED] %s" % pat)

# Now find ALL old images on disk
assets_dir = os.path.join(LV7, "assets")
old_on_disk = []
for root, dirs, files in os.walk(assets_dir):
    for f in files:
        for pat in old_pats:
            if pat.lower() in f.lower():
                old_on_disk.append(os.path.relpath(os.path.join(root,f), LV7))
                break

if referenced_old:
    print("  CRITICAL: %d old patterns still referenced in HTML/CSS/JS!" % len(referenced_old))
else:
    print("  CLEAN: No old image patterns in any HTML/CSS/JS")

print("  Old images on disk but unreferenced: %d files" % len(old_on_disk))

# 5. Duoluanzhuang (03) and Baomiaowang (06) and Changbiaowang-ruminant (041) translation check
print("\n=== MISSING TRANSLATION KEYS FOR 03/06/041 ===")
t = open(os.path.join(LV7, "translations.js"), "r", encoding="utf-8").read()
m = re.search(r"window\.HL_T\s*=\s*(\{.+\})", t, re.DOTALL)
if m:
    data = json.loads(m.group(1))
    zh_keys = set(data.get("zh-Hans", {}).keys())
    en_keys = set(data.get("en", {}).keys())
    expected_prefixes = ["01_","02_","03_","04_","041_","05_","06_"]
    for prefix in expected_prefixes:
        en_p = [k for k in en_keys if k.startswith(prefix)]
        zh_p = [k for k in zh_keys if k.startswith(prefix)]
        if en_p:
            print("  %s: en=%d zh=%d - %s" % (prefix, len(en_p), len(zh_p), "MATCH" if len(en_p) == len(zh_p) else "MISMATCH"))
        else:
            print("  %s: MISSING from translations" % prefix)

# 6. changbiaowang-ruminant path check
print("\n=== PATH CHECK: changbiaowang-ruminant vs zhangbiaowang-ruminant ===")
print("  zhangbiaowang-ruminant/ exists: %s" % os.path.isdir(os.path.join(LV7, "zhangbiaowang-ruminant")))
print("  changbiaowang-ruminant/ exists: %s" % os.path.isdir(os.path.join(LV7, "changbiaowang-ruminant")))
# Check which has HTML content
for d in ["zhangbiaowang-ruminant", "changbiaowang-ruminant"]:
    for ext in ["html","htm","txt"]:
        matches = glob.glob(os.path.join(LV7, d, "*."+ext))
        if matches:
            print("  %s: %d .%s files" % (d, len(matches), ext))
            for m in matches:
                print("    %s (%d bytes)" % (m, os.path.getsize(m)))

# 7. JS loaded resources
print("\n=== JS LOADED RESOURCES ===")
js = open(os.path.join(LV7, "assets", "js", "site-v7.js"), "r", encoding="utf-8").read()
print("  JS: %d bytes" % len(js))

print("\nDone.")

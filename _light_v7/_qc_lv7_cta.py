#!/usr/bin/env python3
"""Check cta sections in all pages."""
import os, re

LV7 = r"D:\LLM\sites\animal\_light_v7"
PAGES = ["index.html", "baomiaowang/index.html", "junzaiwang/index.html",
         "kelionwang/index.html", "duoluanzhuang/index.html",
         "zhangbiaowang/index.html", "zhangbiaowang-ruminant/index.html",
         "zujinwang/index.html"]

print("=== CTA / CONTACT SECTION CHECK ===")
for p in PAGES:
    fp = os.path.join(LV7, p.replace("/", "\\"))
    c = open(fp, "r", encoding="utf-8").read()
    
    # CTA section
    cta = re.search(r'<section[^>]*aria-label=[\'\"]联系区域[\'\"][^>]*>(.*?)</section>', c, re.DOTALL)
    if cta:
        content = cta.group(1).strip()
        print("  %s: cta content=\"%s\" (len=%d)" % (p, content[:60].replace("\n"," "), len(content)))
    else:
        print("  %s: NO cta section" % p)
    
    # Check for data-lang="en" mechanism
    en_div = re.search(r'data-lang=[\'\"]en[\'\"]', c)
    en_section = re.search(r'class=[\'\"][^\'\"]*\blang-en\b', c)
    print("    EN mechanism: data-lang=%s | class-lang-en=%s" % (bool(en_div), bool(en_section)))
    
    # Check that i18n.js is loaded
    has_i18n_js = 'i18n.js' in c
    print("    i18n.js loaded: %s" % has_i18n_js)

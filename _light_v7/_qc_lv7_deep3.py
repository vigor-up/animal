#!/usr/bin/env python3
"""Deep check: CSS, index, translations."""
import os, re, json

LV7 = r"D:\LLM\sites\animal\_light_v7"

# site.css old img refs
css = open(os.path.join(LV7, "assets", "css", "site.css"), "r", encoding="utf-8").read()
print("site.css: %d bytes" % len(css))
old_pats = ["egg-quality","broiler_carcass","tilapia-","farm-aerial","vitality-plus","vitalboost"]
old_urls = [l.strip() for l in css.split("\n") if any(p in l.lower() for p in old_pats)]
print("Old image refs in site.css: %d" % len(old_urls))
for u in old_urls[:10]:
    print("  %s" % u)

# site-v7.css
css2 = open(os.path.join(LV7, "assets", "css", "site-v7.css"), "r", encoding="utf-8").read()
print("\nsite-v7.css: %d bytes" % len(css2))

# Index
idx = open(os.path.join(LV7, "index.html"), "r", encoding="utf-8").read()
print("\nINDEX:")
print("  contact-blank: %s" % ("contact-blank" in idx))
print("  cta: %s" % ("cta" in idx))
# footer
import re as RE
m = RE.search(r"<footer.*?</footer>", idx, RE.DOTALL)
if m:
    print("  footer: %s" % m.group()[:200])
# forbidden
fwords = ["活","VitalBoost","枯","Bacillus","subtilisin","SARA","瘤胃","ch-OSA","蝦","astaxanthin","異","Cornell","EnzyGrow","售","售价"]
for fw in fwords:
    if fw in idx:
        if "活" == fw:
            # check it's really 活力旺 not 活力得
            if "活力旺" in idx:
                print("  FORBIDDEN: 活力旺")
        elif fw in idx:
            print("  FORBIDDEN: %s" % fw)
h1s = RE.findall(r"<h1[\s>]", idx)
print("  H1: %d" % len(h1s))

# Translations
t = open(os.path.join(LV7, "translations.js"), "r", encoding="utf-8").read()
m = RE.search(r"window\.HL_T\s*=\s*(\{.+\})", t, RE.DOTALL)
if m:
    data = json.loads(m.group(1))
    langs = list(data.keys())
    print("\nTRANSLATIONS:")
    print("  Languages: %s" % langs)
    for lang in langs:
        print("  %s: %d keys" % (lang, len(data[lang])))
    zh_keys = set(data.get("zh-Hant", {}).keys())
    en_keys = set(data.get("en", {}).keys())
    print("  Missing from en: %d" % len(zh_keys - en_keys))
    print("  Extra in en: %d" % len(en_keys - zh_keys))
    # Check product page keys specifically
    prod_prefixes = ["01_", "02_", "03_", "04_", "05_", "06_"]
    for prefix in prod_prefixes:
        en_prod = [k for k in en_keys if k.startswith(prefix)]
        zh_prod = [k for k in zh_keys if k.startswith(prefix)]
        if en_prod:
            print("  %s: en=%d zh=%d" % (prefix, len(en_prod), len(zh_prod)))

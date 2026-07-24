#!/usr/bin/env python3
"""Check i18n gaps for duoluanzhuang(03) and baomiaowang(06)."""
import os, re

LV7 = r"D:\LLM\sites\animal\_light_v7"

t = open(os.path.join(LV7, "translations.js"), "r", encoding="utf-8").read()
print("translations.js: %d bytes" % len(t))

# Check for 03_ and 06_ key prefixes
for prefix in ["03_", "06_", "01_", "02_"]:
    count = t.count(prefix)
    print("  prefix '%s': %d occurrences" % (prefix, count))

# Check the actual product pages for data-i18n
print()
for p in ["duoluanzhuang", "baomiaowang", "junzaiwang"]:
    path = os.path.join(LV7, p, "index.html")
    if not os.path.exists(path):
        print("%s: NO FILE" % p)
        continue
    c = open(path, "r", encoding="utf-8").read()
    i18n_attrs = re.findall(r'data-i18n="([^"]+)"', c)
    print("%s: %d data-i18n keys" % (p, len(i18n_attrs)))
    for a in i18n_attrs[:3]:
        print("  %s" % a)

# Now check for the specific concern: 03 and 06 product pages 
# are they missing from translations.js entirely?
# If the pages have fixed text (no data-i18n), they're static-HTML and translations.js doesn't need those prefixes.
print()
print("=== Checking if product pages use data-i18n or static text ===")
all_pages = ["baomiaowang","junzaiwang","kelionwang","duoluanzhuang","zhangbiaowang","zhangbiaowang-ruminant","zujinwang"]
for p in all_pages:
    path = os.path.join(LV7, p, "index.html")
    if not os.path.exists(path):
        continue
    c = open(path, "r", encoding="utf-8").read()
    i18n_count = len(re.findall(r'data-i18n="([^"]+)"', c))
    has_div = "<div" in c
    has_cta = '<section class="cta"' in c
    # Check for the [EN] gap: pages don't have EN sections at all
    # (they use pure HTML, no data-i18n, so the i18n.js does nothing for them)
    print("  %s: i18n_keys=%d has_cta=%s has_div=%s" % (p, i18n_count, has_cta, has_div))

# The real EN question: does clicking the lang button actually translate these?
# With no data-i18n attributes, the i18n.js does nothing on these pages...
# But they also have no EN-content sections. So EN = same as ZH (no translation applied)
print()
print("=== CRITICAL: EN translation check ===")
for p in all_pages:
    path = os.path.join(LV7, p, "index.html")
    if not os.path.exists(path):
        continue
    c = open(path, "r", encoding="utf-8").read()
    # Total Chinese characters
    zh_chars = len(re.findall(r'[\u4e00-\u9fff]', c))
    # Check if there's any EN variant mechanism
    has_is_en = 'is-en' in c or 'lang="en"' in c
    has_en_section = 'data-lang="en"' in c or 'class="en"' in c or 'lang-en' in c
    print("  %s: zh_chars=%d has_is_en=%s has_en_section=%s" % (p, zh_chars, has_is_en, has_en_section))
    # The pages use pure HTML with NO data-i18n and NO EN sections
    # So clicking the lang toggle literally does nothing -> [GAP]

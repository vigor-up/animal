import os, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

dist_dir = Path(__file__).parent.resolve()
screenshot_dir = dist_dir / "screenshots"
screenshot_dir.mkdir(exist_ok=True)

pages = [
    ("index.html", "index"),
    ("junzaiwang.html", "junzaiwang"),
    ("kelionwang.html", "kelionwang"),
    ("duoluanzhuang.html", "duoluanzhuang"),
    ("zhangbiaowang.html", "zhangbiaowang"),
    ("zujinwang.html", "zujinwang"),
    ("baomiaowang.html", "baomiaowang"),
]

viewports = [
    ("desktop", 1280, 900),
    ("mobile", 390, 844),
]

count = 0
with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    for vp_name, width, height in viewports:
        ctx = browser.new_context(viewport={"width": width, "height": height})
        page = ctx.new_page()
        for file_name, slug in pages:
            url = "file:///" + str(dist_dir / file_name).replace("\\", "/")
            page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(800)
            out = screenshot_dir / f"{slug}_{vp_name}.png"
            page.screenshot(path=str(out), full_page=False)
            print(f"[OK] {slug}_{vp_name}.png")
            count += 1
        ctx.close()
    browser.close()

print(f"\nDone: {count} screenshots -> {screenshot_dir}")

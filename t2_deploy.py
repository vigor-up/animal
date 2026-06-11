import os, shutil, glob

SITE = r"D:\LLM\sites\animal"
DIST = os.path.join(SITE, "dist_v4")
ARC  = os.path.join(SITE, "_archive_main_20260611")
os.makedirs(ARC, exist_ok=True)

# 1. Archive existing root HTML files
archived_html = []
for f in glob.glob(os.path.join(SITE, "*.html")):
    dest = os.path.join(ARC, os.path.basename(f))
    shutil.move(f, dest)
    archived_html.append(os.path.basename(f))
print("Archived HTML:", archived_html)

# 2. Copy dist_v4/*.html to root (paths already fixed to assets/)
copied_html = []
for f in glob.glob(os.path.join(DIST, "*.html")):
    shutil.copy2(f, os.path.join(SITE, os.path.basename(f)))
    copied_html.append(os.path.basename(f))
print("Copied HTML:", sorted(copied_html))

# 3. Merge dist_v4/assets/ into animal/assets/
#    css/ -> overwrite site.css; svg/ -> new; img/ -> new (duoluan images)
#    Do NOT touch assets/images/ (existing hero images stay)
dist_assets = os.path.join(DIST, "assets")
site_assets = os.path.join(SITE, "assets")
for sub in ["css", "svg", "img"]:
    src = os.path.join(dist_assets, sub)
    dst = os.path.join(site_assets, sub)
    if not os.path.isdir(src):
        continue
    shutil.copytree(src, dst, dirs_exist_ok=True)
    print("  Merged assets/" + sub + "/")

# 4. Copy BUILD_summary.md
shutil.copy2(os.path.join(DIST, "BUILD_summary.md"), os.path.join(SITE, "BUILD_summary.md"))

# Report
root_html = [os.path.basename(x) for x in glob.glob(os.path.join(SITE, "*.html"))]
print("Root HTML:", sorted(root_html))
print("Old archived to:", ARC)
print("assets/images/ intact:", os.path.isdir(os.path.join(site_assets, "images")))
print("[PAV-OK-T2] dist_v4 merged to root")

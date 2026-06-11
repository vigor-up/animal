import urllib.request, time, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

hosts = [
    "http://animal.feed-pet.com/",
    "https://vigor-up.github.io/animal/",
]
ban_words = ["Vitality Plus", "EnzyGrow", "Cornell"]
ban_cjk = ["活力旺", "廈門澤林", "蝦青素"]  # 活力旺,廈門澤林,蝦青素

for host in hosts:
    for i in range(4):
        try:
            req = urllib.request.Request(host, headers={"User-Agent": "Mozilla/5.0"})
            html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
            logo_img = re.findall(r'<img[^>]*nav-logo[^>]*>', html[:3000], re.I)
            nav_logo_text = re.findall(r'class="nav-logo"[^>]*>(.*?)</a>', html[:3000], re.S)
            ban = [b for b in ban_words + ban_cjk if b in html]
            title = re.search(r"<title>(.*?)</title>", html, re.S)
            new_version = "活力得" in html  # 活力得
            has_products = any(p in html for p in ["均仙4旺", "殼力旺", "長膠旺"])  # 均仔旺,殼力旺,長膘旺
            print(f"{host} attempt{i+1}:")
            print(f"  title: {title.group(1)[:60] if title else '?'}")
            print(f"  nav-logo img: {logo_img or 'none'}")
            print(f"  nav-logo text: {nav_logo_text[:1] if nav_logo_text else '?'}")
            print(f"  banned words: {ban or '0'}")
            print(f"  new version (活力得): {new_version}")
            print(f"  has products: {has_products}")
            if new_version and not ban and not logo_img:
                print(f"  [OK] {host} updated version live")
                break
            elif i < 3:
                print(f"  not updated yet, waiting 45s...")
                time.sleep(45)
        except Exception as e:
            print(f"{host} attempt{i+1}: {str(e)[:100]}")
            if i < 3:
                time.sleep(45)
    print()

print("[PAV-OK-T5] live verification done")

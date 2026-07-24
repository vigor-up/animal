# CC Brief · ROOT 收斂 + _light_v7 上線 直推 main（立即執行·單窗）

## 決策（總監已裁·焊死）
- **正式站＝`_light_v7`（CG 淺藍生技版）**，promote 到 vigor-up/animal repo **root**，直推 main，GitHub Pages 立即服務新站。
- **舊 root 平面檔＋平行工作線的檔案：archive 不刪**（git mv 到 `_archive/root_flat_20260723/`），零損失、可回復。
- **單窗 CC1 執行**，第二窗即刻停手（不得並行 push）。
- QV 深層版面稽核＝上線後 fast-follow，不擋本次推送。

```
████ EVOX2-0723-ROOT-GOLIVE │ CC1(WORKER) │ v7 promote root+直推main+驗200 ████

[反造假]
1. 實貼 repo 現況：`git remote -v`(=vigor-up/animal)、`git fetch`後 `git log origin/main -3`、`git status`、root 現有 *.html 清單、_light_v7 8頁 stat。
2. 確認單窗無鎖、第二窗已停。對不上先停回報。

[ACT]
T1 取最新：`git fetch origin` → `git checkout main` → `git pull --rebase origin main`（納入平行線最新，避免覆蓋）。[PAV-OK-T1]
T2 歸檔舊 root（不刪）：`mkdir -p _archive/root_flat_20260723`；把 root 層舊站檔（index.html + 各 *.html 平面頁 + 舊 assets 若與 v7 衝突）`git mv` 進去；**列出所有被歸檔檔名**（含平行線新增的，如 zhangbiaowang-cattle.html——保留可回復）。[PAV-OK-T2]
T3 promote v7 到 root：把 `_light_v7/` 全部內容（index.html + 7 產品夾 + assets + i18n/translations + sitemap.xml/robots.txt/.nojekyll）複製到 repo **root**；**建/確認 root `CNAME`=animal.feed-pet.com**；sitemap/canonical base 對齊實際 Pages 網域。[PAV-OK-T3]
T4 推送：`git add`(明確 pathspec，禁 -am/-A 全加)→`git commit`→`git push origin main`。若 push 被拒(他窗又推)：`git pull --rebase` 後重推。[PAV-OK-T4]
T5 驗上線：`curl -I` GitHub Pages 網域(自訂 animal.feed-pet.com 或 vigor-up.github.io/animal) ==200；curl 首頁 grep 確認是 v7（含「推进酶学科学」或「探索7大产品线」新字串，非舊站字串）。[PAV-OK-T5]

[GATE]
- archive 一律 `git mv` 不 `rm`（不可逆保護）；被歸檔清單完整回報。
- 若 rebase 出現真衝突且涉及他窗未知改動 → 停下回報清單，不硬解猜測。

[VERIFY]（硬斷言）
- assert push 後 origin/main HEAD=本次 commit
- assert Pages curl -I ==200 且首頁內容為 v7（grep 新字串命中、舊站字串消失）
- assert root 有 index.html(v7)+7產品夾+sitemap.xml+robots.txt+.nojekyll+CNAME
- assert 舊 root 檔全在 `_archive/root_flat_20260723/`(git log 可見 mv，未 delete)
- assert 8頁禁字 grep==0、footer 僅台灣毅展、041◷（v7 帶入不回退）

回貼5樣：1.T1-T5 STDOUT(含[PAV-OK]) 2.summary 3.被歸檔檔清單+root新結構ls 4.WARN(平行線檔已歸檔清單/待QV熱修項/網域確認) 5.真實驗證(git log origin/main + curl -I 200 + 首頁grep新舊字串 stdout)
```

## 給總監
- 上線即回貼 `curl -I 200` + 首頁截圖確認 v7 live。
- 平行線在 root 的改動**已歸檔保留**（`_archive/root_flat_20260723/`），沒丟；若那條線有想保留的，可從歸檔夾取回。
- QV 深層版面/圖版本稽核照跑，缺陷回來我立即出 CG 熱修 brief，**熱修直接再推 main**（站已 live，逐條快修不重來）。

# CC/QV Brief · SEO收尾決策焊死 + 併非AI圖 + T5上線（single-window）

## ★並行撞車處置（先做）★
偵測到兩窗跑同一 SEO brief 互相 git add/改檔。**即刻序列化：指定 CC1 為唯一收尾窗完成 T5；第二窗/背景自動化即刻停手（不得再 add/rename/push）**。CC1 先 `git status` 確認無他窗未提交變更、必要時 stash -u，再動工。禁兩窗同時 rename/merge/push。

## 總監決策（焊死，勿再問）
1. **命名**：**維持 kelionwang / zhangbiaowang 不改名**（全站 URL/canonical/sitemap/hreflang/內鏈/圖檔已一致；品牌無官方羅馬拼音 SSOT；站未上線但改名有撞車風險、無 SEO 收益）。Task4 v2 brief 的 kelliwang/changbiaowang 字樣以此為準作廢。
2. **Footer**：刪除「厦門泽林生物科技」，網頁**僅留「台灣毅展實業有限公司」**（通路定位；澤林=真實中國總代理但對外不露）。全 8 頁 footer + JSON-LD 一併改。
3. **041 經濟數字（更正+合規）**：現「513~657 元/头」是**終重kg誤植為人民幣**。改為——效益列**只呈績效**：`FCR ↓20% · 終重 513→657kg`（輸出端績效✓）；**人民幣 ROI 一律標「补强中◷」**（真值牛4,042/羊371為對內口徑，brand map §5 禁對外）。修 index 卡片 + changbiaowang-ruminant 頁兩處。
4. **推送時機**：**(b)** — CG Task5 非AI實感圖**已到齊且 gate 11/11 PASS**，本次**併圖後再推**（不先推AI假圖）。
5. **網域**：canonical/sitemap 用 `animal.feed-pet.com`；**確認 repo root 有 CNAME 檔=animal.feed-pet.com**（GitHub Pages 自訂網域必要），無則補。

## 併圖來源（非AI實感圖，已gate過關）
`C:\Users\Richtrong\Documents\huolide\_skywork_上傳包\_AB實拍最新_20260723\`（各產品夾 + _海魚共用 + _INDEX；含11張Task5新場景圖+全AB+海魚+index hero）。對照 `_manifest_20260723.md`。**站點現用「太AI/陽光普照」共用圖(hero/founder/機轉/海魚場景)以此庫對應替換。**

```
████ EVOX2-0723-SEO-FINISH │ CC1(WORKER)｜QV(VERIFIER) │ 決策套用+併圖+上線 ████

[反造假]
1. git status 實貼(確認單窗、無他窗未提交)；ls _AB實拍最新_20260723 各夾；grep 現 footer「泽林」命中頁；grep index「513~657 元」。對不上先停回報。
2. 改前 git commit 還原點(明確pathspec,禁-am)。

[ACT]
T1 套三決策：全8頁 footer 刪「厦門泽林生物」留台灣毅展；index卡+ruminant頁 ROI 改「FCR↓20%·終重513→657kg + 补强中◷」(移除人民幣ROI數字)；確認/補 CNAME=animal.feed-pet.com。[PAV-OK-T1]
T2 併非AI圖：把 _AB實拍最新 對應圖 PIL轉webp(q82,method6,maxW1600)→覆蓋各產品 assets/img 對應 hero/場景/AB 舊AI圖(檔名維持站點現用slug,內容換新)；index hero 換 index-hero-brand。逐頁確認 <img src> 不 broken。[PAV-OK-T2]
T3 資產QC：Playwright 390×844@2x 逐頁截圖 _qc_shots/(force eager+naturalWidth>0)；目視無陽光普照/AI過曝殘留。[PAV-OK-T3]
T4〔GATE見下〕QV後驗→merge→push：QV獨立跑六要件+禁字+footer只留毅展+ROI無人民幣數字+broken=0+CNAME存在→verdict PASS→CC merge redesign-2026→main→push→curl -I https://animal.feed-pet.com/ ==200。[PAV-OK-T4]

[GATE]
- push main=公開發布，QV PASS 後 CC 直接執行(G3已授權)，但**限CC1單窗**。
- merge 前確認第二窗已停、無並行 push。

[VERIFY]（硬斷言）
- assert 全8頁 footer grep「泽林」==0 且含「台灣毅展實業」
- assert index 與 ruminant grep「513~657 元」==0（人民幣ROI已撤）；含「补强中◷」與「終重 513」kg績效
- assert 8頁禁字grep(活力旺/VitalBoost/subtilisin/枯草/Bacillus/SARA/瘤胃pH/1:N/售價/ch-OSA/蝦青素/異黃酮/Cornell/4042/371)==0
- assert 每頁hero/場景/AB圖已換為 _AB實拍最新 對應webp，broken==0，截圖目視無AI過曝
- assert canonical/og/twitter/hreflang/JSON-LD/單h1 仍全綠(SEO硬化不回退)
- assert repo root CNAME==animal.feed-pet.com；sitemap/robots/.nojekyll 在
- assert merge 後 main HEAD=本次commit && curl -I animal.feed-pet.com ==200
- assert 單窗：git reflog 無第二來源交錯 push

回貼5樣：1.TASK STDOUT(含[PAV-OK]) 2.summary 3.8頁diff+換圖清單(舊AI→新webp)+截圖 4.WARN(命名維持/041對內數撤/第二窗已停) 5.真實驗證(footer&ROI&禁字grep每頁stdout+換圖broken檢測+QV verdict+push後 git log/curl -I stdout)
```

## 給總監（FYI，非阻擋）
- **記憶更正**：041「513-657」是終重kg非ROI；mem rollup 舊記錯，下次滾入時 CC 一併更正 core.md（真對內 ROI=牛4,042/羊371，對外禁用）。
- **brand map §5 vs 本session ROI**：§5 原則「對內人民幣ROI禁對外」；你本session已定調對外只呈「輸出端絕對增益」為合規中庸（非1:N、非售價）。各產品現有 +1,800/母、+226~250/頭 等屬此授權範圍，維持；**僅 041 因真值屬對內爭議且未定，標◷**。若你要全面改採「純績效不掛人民幣」口徑，回一句我再統一調。

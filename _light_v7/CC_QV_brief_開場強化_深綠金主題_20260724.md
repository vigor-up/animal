# CC/QV Brief · 網站 v7 調整（開場動畫強化 + 內部深綠+金主題）· 熱修上線

## 總監反饋（已上線 animal.feed-pet.com 看後）
1. **開場動畫太差** → 強化 index 開場（DNA 序列偏弱/太快/不夠 premium）。
2. **內部保持原始深綠+金最佳** → 內容區配色由淺藍改回**原始深綠(forest)+金**（品牌成熟版調性）。

## 決策定調（焊死）
- **配色**：內容頁面（8 頁 section/卡片/文字/分隔）改用**深綠 #1a3d2f 系底 + 金 #C9A961 強調 + 米白字**（沿用 _preview_v6 原始深金+forest 主題色）。**取代目前淺藍 #f8fafc。**
- **Hero 開場**：保留 index hero 版位，但**強化開場動畫**（見下）。Hero 底可維持深色（深綠/深底）配金，與內部一致，**全站深綠+金一體**（非淺藍）。
- **內容/SEO/圖片/文案不動**——僅換皮膚(CSS 變數)+開場動畫；禁改 H1/文案/ROI/圖片路徑，SEO 六要件不回退。

## 開場動畫強化規格
- 時長放寬到 ~2.5s（可跳過·reduced-motion 略過·每 session 一次）。
- 序列升級：深綠底 → **DNA 雙螺旋以金色描邊由下而上繪製+輕微旋轉發光** → 「活力得® Huolide®」金色字淡入+字距展開 → 螺旋光暈擴散溶接進 hero → hero 內容 staggered 進場。
- 質感：緩動 cubic-bezier(.16,1,.3,1)，金色微光暈，禁廉價閃爍/生硬跳切。只用 transform/opacity（GPU）。

## ACT（單窗 CC1·熱修再推 main）
```
████ EVOX2-0724-SITE-THEME │ CC1(WORKER)｜QV(VERIFIER) │ 深綠金主題+開場強化 ████
[反造假] git status 單窗確認；grep 現 CSS 變數(淺藍值)。改前 commit 還原點。
T1 主題換色：design-system CSS 變數 淺藍→深綠+金（--bg深綠/--gold金/--text米白/--card深綠卡）；全 8 頁套用；對比度達 WCAG AA。[PAV-OK]
T2 開場動畫強化：依上方序列改 index 開場（2.5s·金螺旋·可跳過·reduced-motion）。[PAV-OK]
T3 QV 後驗：三斷點截圖對比、對比度檢查、開場可跳過/reduced-motion、禁字0不回退、SEO六要件在、圖片無broken。[PAV-OK]
T4〔GATE〕QV PASS → CC 熱修 commit+push main → curl -I 200 → 首頁截圖回貼。[PAV-OK]
[VERIFY] assert 全8頁深綠+金無殘留淺藍；對比度AA；開場2.5s可跳過；SEO/禁字/H1 不回退；curl200。
回貼：改動CSS diff+開場前後錄影/截圖+QV verdict+curl200。
```

## 給總監（一個確認·不阻擋）
- 預設**全站深綠+金一體**（hero 深底+金開場、內部深綠+金）。若你要 **hero 維持淺藍生技風、只有內部改深綠+金**（雙調），回一句我改 brief。
- 這是 CSS 換皮+開場，不動內容，QV PASS 即熱修再推，站不下線。

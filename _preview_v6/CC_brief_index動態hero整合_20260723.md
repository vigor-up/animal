# CC Brief · index 動態 hero 整合（Foldcraft版型×真圖Ken Burns）

## 來源
原型：`活力得_index_動態hero_原型_20260723.html`（自包含，base64圖）＋桌面 artifact `huolide-index-dynamic-hero`。總監已核可方向：**保留 Foldcraft 動態版型骨架，背景改我們 gate 過關真圖 Ken Burns 輪播，零 AI 影片**。

## 目標
把此動態 hero 落進 `_preview_v6/index/index.html`，取代現有靜態 hero，**下方既有區塊（三重护城河/性能评分卡/产品grid/品牌故事/合规/CTA/footer）原樣保留接續**。SEO head 不動（canonical/og/JSON-LD/hreflang 全留）。

## ACT
1. **抽圖落地**：把原型 5 張輪播圖從 `_AB實拍最新_20260723` 取原檔→PIL 轉 webp(q70,method6,maxW1920)→存 `index/assets/img/hero-rot/`：marine-worker-grouper／shrimp-hatchery／cattle-barn／layer-house／sow-lactation。**第1張 preload+eager，其餘 lazy**。
2. **換 hero**：用原型的 `.root/.bg/.kb-layer/.bg-ov/.nav/.mmenu/.hero` 結構替換 index 現有 `<section class="hero">`＋頂部 nav；`.kb-layer` 的 base64 改引 `assets/img/hero-rot/*.webp`。保留原型的 Ken Burns CSS＋漢堡選單＋staggered 動畫。
3. **合一雙語**：原型用 `.t/data-en`＋`setLang` 同站點既有機制，直接併；**確保全頁唯一 `<h1>`＝hero 的 h1**（移除任何殘留舊 h1）。
4. **導覽對齊**：hero navbar 連結指向下方錨點（#products/#tech/#compliance）；CTA「看7大产品线」→ `#products`。
5. **SEO 不回退**：head 的 canonical/og/twitter/hreflang/JSON-LD 保留；og:image 可指 `hero-rot/marine-worker-grouper.webp` 或 index-hero-brand；hero 圖 alt 補關鍵字（活力得®+物種+场景）。
6. **效能**：首圖 `<link rel=preload as=image>`；5圖總量控管(webp)；避免 CLS（層用 position:absolute inset:0 固定尺寸）。

## VERIFY（硬斷言）
- assert index 唯一 `<h1>`；hero 5 層 webp 皆 broken==0；首圖 eager 其餘 lazy
- assert head canonical/og/twitter/hreflang/JSON-LD 仍在（SEO 不回退）
- assert 下方既有區塊全數保留（scorecard/产品grid/品牌故事/合规/footer grep 命中）
- assert 禁字 grep==0；footer 僅台灣毅展（沿用收尾決策）
- assert 手機視窗漢堡選單開合正常、簡EN切換全站 .t 生效
- Playwright 390×844＋1280 桌機各截一張存 _qc_shots/，目視動態hero與下方銜接無斷層

## 註
- 併入時序：可與 EVOX2-0723-SEO-FINISH 同窗(CC1)接續，或其後單獨一 commit；**勿另開窗並行**（避免再撞車）。
- 輪播圖已是 gate 過關真圖，符「零AI假」原則；勿用任何 AI 影片。

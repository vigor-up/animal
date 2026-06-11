# DMWEB-WEB-BUILD-FULL — BUILD 交付摘要

**完成時間**: 2026-06-11  
**輸出目錄**: `D:\LLM\sites\animal\dist_v4\`  
**狀態**: 全部驗收通過

---

## 交付清單

| 頁面 | 檔案 | 主題 | 機轉 SVG |
|------|------|------|---------|
| 首頁 | index.html | — | — |
| 均仔旺 | junzaiwang.html | forest（繁殖線） | HPG 軸 + Ser-His-Asp |
| 殼力旺 | kelionwang.html | amber（繁殖線） | HPG 軸 + Ser-His-Asp |
| 多卵壯 | duoluanzhuang.html | ocean（繁殖線） | HPG 軸 + Ser-His-Asp |
| 長膘旺 | zhangbiaowang.html | forest（生長線） | Ser-His-Asp + V/C 比 |
| 足斤旺 | zujinwang.html | amber（生長線） | Ser-His-Asp + V/C 比 |
| 保苗旺 | baomiaowang.html | ocean（生長線） | Ser-His-Asp + V/C 比 |

---

## 驗收結果

### T2 site.css
- `--bg:#FFFFFF` ✓

### T4 六產品頁全 OK
- 均仔旺 缺:無 禁:0 SVG:有 ✓
- 殼力旺 缺:無 禁:0 SVG:有 ✓
- 多卵壯 缺:無 禁:0 SVG:有 ✓
- 長膘旺 缺:無 禁:0 SVG:有 ✓
- 足斤旺 缺:無 禁:0 SVG:有 ✓
- 保苗旺 缺:無 禁:0 SVG:有 ✓

### 全域禁字掃描（8 檔）
- 禁字 0 命中 ✓
- 掃描詞：活力旺/肥力寶/枯草芽孢/Bacillus subtilis/蝦青素/ch-OSA/Octacosanol/Triacontanol/Policosanol/Cornell/康乃爾/EnzyGrow/廈門澤門/實驗室實證✓

### T5 Playwright 截圖（14 張）
- 7 頁 × desktop(1280×900) + mobile(390×844) 全完成
- 輸出：`screenshots/` 目錄

---

## 設計規格遵循

- 數字來源：roi_web_dm_figures.json（evidence_level="reference"，ROI 1:5–1:8）
- 圖片來源：image_manifest.json master paths（`../assets/images/`）
- 多卵壯 IMG-GEN-01 佔位保留（data-pending-img="IMG-GEN-01"）
- 對外署名：台灣 毅展實業有限公司（無電話/email/廈門澤林）
- 賣點標籤：「田間/產業參考」
- 2 次放大稀釋：6 頁全數確認
- 機轉 SVG：全部 inline（無外部請求）
- 白底 #FFFFFF：已確認
- Google Fonts CDN：Baloo 2 + Noto Serif TC + Noto Sans TC

---

## 待辦

- [ ] 多卵壯 IMG-GEN-01（CC2 任務，待補）
- [ ] 總監驗截圖確認後切換上線（dist_v4 → 現役目錄）

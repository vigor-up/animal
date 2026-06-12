# 網站圖片升級候選表（Claude AI MCP 親查定案）

## 現役站圖位狀態總覽 (來源: D:\LLM\sites\animal)

| 圖位 | 現用圖 | 品質 | qwen 候選 | 動作 |
|---|---|---|---|---|
| index hero | hero_farm_realistic.png (2354459B) | 待評(zscene/farm) | hero_farm_realistic.png (already in use) | Claude AI MCP 親查 |
| junzaiwang hero | sow-nursing-piglets.jpg (1847023B) | 存檔照(assets/images .jpg) | junzaiwang_hero_qwen.png (1.58MB 1344x768) ✓ ready | 建議更換為 qwen 圖 (存檔照 vs qwen) |
| kelionwang hero | layer-hen-farm.jpg (1994111B) | 存檔照(assets/images .jpg) | kelionwang_hero_qwen.png (1.72MB 1344x768) ✓ ready | 建議更換為 qwen 圖 (存檔照 vs qwen) |
| duoluanzhuang hero | duoluan_broodstock_real_qwen.png (1366530B) | 好(qwen) | duoluan_broodstock_real_qwen.png (already in use) | 已上線，無需動作 |
| zhangbiaowang hero | finishing-pigs-barn.jpg (1938695B) | 存檔照(assets/images .jpg) | zhangbiaowang_hero_qwen.png (1.58MB 1344x768) ✓ ready | 建議更換為 qwen 圖 (存檔照 vs qwen) |
| zujinwang hero | broiler-chicken-house.jpg (1924110B) | 存檔照(assets/images .jpg) | zujinwang_hero_qwen.png (1.59MB 1344x768) ✓ ready | 建議更換為 qwen 圖 (存檔照 vs qwen) |
| baomiaowang hero | baomiao_shrimp_real_qwen.png (1667376B) | 好(qwen) | baomiao_shrimp_real_qwen.png (already in use) | 已上線，無需動作 |

## 4 產品 hero qwen 候選圖在庫狀態
| 圖位 | qwen 圖 | 在庫 | 解析度 | 大小 |
|---|---|---|---|---|
| junzaiwang hero | junzaiwang_hero_qwen.png | ✓ | 1344x768 | 1577022B |
| kelionwang hero | kelionwang_hero_qwen.png | ✓ | 1344x768 | 1715099B |
| zhangbiaowang hero | zhangbiaowang_hero_qwen.png | ✓ | 1344x768 | 1576614B |
| zujinwang hero | zujinwang_hero_qwen.png | ✓ | 1344x768 | 1590333B |

## 待 Claude AI MCP 親查項
1. **5 頁 hero 圖升級** — junzaiwang/kelionwang/zhangbiaowang/zujinwang 現用 `assets/images/` 存檔照 (1.8-2.0MB, 真實攝影)，qwen 候選已備(1344x768, ~1.6MB)。確認品質對比後決定是否替換。
2. **index section 6 張縮圖** — 同為 `assets/images/` 存檔照，是否也需替換或保留。
3. **duoluan 多版本** — `duoluan_broodstock_real_qwen.png` (1024x1024, 已上線) vs `duoluan_broodstock2.png` (1024x768, 1.45MB size 最大但解析度較低)。
4. **index hero_farm_realistic.png** (1536x768, 2.35MB) — 已上線，是否保留。
5. **替換後 git commit + push origin main (force) + dist_v4 subtree push** — 改圖作業另立 brief。
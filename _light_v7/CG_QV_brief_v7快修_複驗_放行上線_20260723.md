# CG快修 + QV複驗 → 放行上線 brief（v7 NO-GO 硬缺·分鐘級）

## 背景
QV 判 v7 NO-GO：EN 假翻譯、CTA 整段空白、index 誤含「补强中」、15 張孤兒舊圖。皆**快修**。CG 修→QV 複驗(含未跑的 T1 視覺)→GO 即執行已備的 `CC_brief_ROOT收斂_v7上線` 推 main。**單窗序列，勿並行。**

## CG 修正（WORKER）
```
████ EVOX2-0723-LV7-FIX │ CG(WORKER) │ v7 上線級硬缺快修 ████
[ACT]
T1 CTA/聯絡段填文（8頁+index）：空 `<section>` 填邀約文案——
   標題「开启精准营养 · 联系区域授权经销商」；正文「邀请您进行技术评估与试用；技术服务／试用申请由各区域授权经销商提供在地窗口。」
   **聯絡人/電話/email 欄位留空**(通路保護)，但段落須有上述文案與樣式，非空 tag。[PAV-OK-T1]
T2 EN 鈕處理：**launch 先隱藏「简/EN」切換鈕**(display:none)，`<html lang="zh-Hans">`固定；translations.js/i18n 保留備 fast-follow。**不留假 EN。**[PAV-OK-T2]
T3 index 移除誤植「补强中◷」(該記號僅限 041 长膘旺·牛羊頁；index 不得出現)。[PAV-OK-T3]
T4 孤兒舊圖清理：assets/ 內 15 張未引用舊檔(tilapia-*×8/broiler_carcass/egg-quality-showcase/farm-aerial×2/vitality-plus-concept 等) `move` 到 `_archive/orphan_v7_20260723/`(不 del)，勿動 assets/media/ gate圖。[PAV-OK-T4]
[VERIFY] assert 8頁+index CTA段含邀約文案且無空<section></section>；EN鈕不顯示；index grep「补强中」==0；孤兒圖0引用且已移 _archive。
回貼：改動清單 + grep stdout。
```

## QV 複驗（VERIFIER · CG 修完跑）
```
████ EVOX2-0723-LV7-QC2 │ QV(VERIFIER) │ 修後複驗 + 補跑T1視覺 ████
T1〔補跑〕視覺RWD：Playwright 三斷點(桌1440/平板768/手機390)×8頁**全頁截圖**，查①圖拉伸(naturalWidth比例>3%)②文字溢出(scrollWidth>innerWidth)③文字壓圖不可讀④AB圖不等高/卡片錯位/圖表裁切。列缺陷表。
T2 複驗硬缺已修：CTA文案在位/EN鈕隱藏/index無补强中/孤兒圖已移。
T3 合規回歸：禁字0/footer僅台灣毅展/041◷(僅該頁)/單h1/圖全 assets/media。
[VERIFY] 出 GO/NO-GO：若 T1 視覺仍有 CRITICAL(溢出/壓字/拉伸) → NO-GO 列表回報；只剩輕微 → GO 附待熱修清單。
回貼5樣：截圖+缺陷表+複驗結果+WARN+真實stdout。
```

## 放行 → 上線
- QV **GO** → 立即執行 `CC_brief_ROOT收斂_v7上線_直推main`（archive不刪·單窗·推main·curl200）。
- QV 仍 **NO-GO（僅視覺 CRITICAL）** → CG 再修該項，其餘輕微列上線後熱修，不無限等。

## 給總監
- 這輪走完 = v7 乾淨簡中版上線；EN 與深層視覺微調當 fast-follow 直接再推。
- 全程單窗序列(CG修→QV驗→CC推)，不並行、不撞車。

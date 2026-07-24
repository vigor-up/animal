# QV Brief · _light_v7 全站版面/RWD 稽核（圖拉伸·文字溢出·壓字·圖版本）

## 定位
CG 已產 `D:\LLM\sites\animal\_light_v7\`（8頁+assets）。Claude AI 已 spot-check：**8 頁 hero 桌機+手機皆乾淨過關**（淺藍生技風、Genova 左對齊、真圖淡出、無溢出）。**本 QV＝深層區塊逐頁全捲稽核 + 圖版本正確性**，找總監點名的三類缺陷。WORKER≠VERIFIER，QV 獨立跑。

```
████ EVOX2-0723-LV7-QC │ QV(VERIFIER) │ _light_v7版面RWD+圖版本稽核 ████

[反造假]
1. 實貼 8 頁清單 stat（index+junzaiwang+kelionwang+duoluanzhuang+zhangbiaowang+zhangbiaowang-ruminant+zujinwang+baomiaowang）。
2. 實貼每頁引用圖 src 清單（grep `<img` + CSS background-image）；對照 assets/media/ gate 圖庫。對不上先停回報。

[PLAN]
Playwright 三斷點(桌1440 / 平板768 / 手機390) 逐頁**全頁截圖**，逐 section 目視 + 程式化檢測三類缺陷 + 圖版本核對 + 合規複驗，出缺陷表(最嚴優先)。

[ACT]
T1 版面三缺陷（總監點名·硬檢+目視）：每頁每斷點——
  ①**圖片拉伸變形**：抓每 <img> 的 naturalWidth/Height 對比顯示 w/h，比例差 >3% 標拉伸；背景圖 object-fit 缺失致擠壓。
  ②**文字溢出範圍**：`document.documentElement.scrollWidth > innerWidth`(橫向捲軸=溢出) + 目視文字跳出卡片/按鈕/螢幕。
  ③**文字大面積壓住圖片**：hero/疊字區文字與圖重疊致不可讀（對比不足/無遮罩）。
  併檢：AB 圖對兩側不等高、卡片網格錯位、ROI圖表被裁切、section 間距塌陷、按鈕換行破版。[PAV-OK-T1]
T2 **圖版本正確性**（實質風險）：assert 每頁產品圖**全部來自 assets/media/ gate圖庫**；**ZERO 引用舊 dist_v4 AI/VitalBoost 圖**（禁 egg-quality-showcase / broiler_carcass / *-before-after / tilapia-* / *-farm-aerial / vitality-plus-concept 等舊檔）；物種對題、AB方向正確(背膘對照肥/五花不等距/出蝦規格ab4尺規/白便金褐vs白濁)。列出任何舊圖殘留頁+檔名。[PAV-OK-T2]
T3 合規複驗（CG稱已過·QV獨立再驗）：每頁禁字grep(活力旺/VitalBoost/subtilisin/枯草/Bacillus/SARA/瘤胃pH/1:N/售价/ch-OSA/虾青素/异黄酮/Cornell)==0；footer 僅「台湾毅展实业有限公司」(無泽林)；041 無人民币ROI含「FCR↓20%/513→657kg/◷」；單h1。[PAV-OK-T3]
T4 CG揭露兩缺口複核：①简EN——實測切 EN 後**內文是否真翻譯**(非只切UI/殘留中文)，列未翻段落；②index Hero 分子影片——確認目前僅 poster 保底(無 DNA loop)，標「待補自存分子影片」。[PAV-OK-T4]

[VERIFY]（硬斷言）
- assert 三斷點×8頁全頁截圖齊；橫向溢出頁清單(scrollWidth>innerWidth)
- assert 圖拉伸清單(比例差>3%)、壓字不可讀清單、AB不等高清單 各列頁+section
- assert 產品圖 100% 出自 assets/media/；舊dist_v4圖引用數==0(否則列殘留)
- assert 8頁禁字==0、footer僅毅展、041◷、單h1
- assert EN 未翻譯段落清單、分子影片缺口記錄

回貼5樣：1.T1-T4 STDOUT(含[PAV-OK]+每頁三斷點截圖) 2.缺陷表(頁|斷點|section|缺陷類|嚴重度|修正建議,最嚴優先) 3.圖版本核對表(頁→引用圖→新/舊) 4.WARN(EN缺口/影片缺口/舊圖殘留) 5.真實驗證(scrollWidth檢測+naturalWidth比例+禁字grep stdout)
```

## 給 Claude AI（QV 回貼後）
- QV 出缺陷表 → 我彙整成「CG 修正 brief」逐條交 CG 修（版面+換舊圖+補EN+補影片）。
- v7 內容 CG 是從 dist_v4+母版重建（非直接沿用已驗證 _preview_v6，因該夾 CG 稱只剩 brief+截圖）→ **故 T2/T3 不可省，須把 v7 當全新版做完整合規/圖版本驗證**，不假設繼承。

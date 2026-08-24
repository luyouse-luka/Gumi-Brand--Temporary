# 还原度审计 B 组 — PDP / Science × 1440 / 390

> 审计人：B 组会话，2026-08-20。**只出报告，未改任何项目文件。**
> 设计源全部取自 `figma/nodes/` 落盘 JSON，**未发任何 Figma API 请求**。
> 依据 `docs/AUDIT-HANDOFF.md` 第 0 / 3 / 7 节与 `docs/PROJECT-STATUS.md`「待确认」「占位内容」两节。

---

## 0. 怎么验的

`$SP = /tmp/claude-1007/-home-ly/c7ffb540-53f6-4bbe-87d6-fe452694dbc5/scratchpad`

### 0.1 数值比对（主会话已产出）

```
$SP/cmp_pdp_1440.json   tokenDiff=6   figOnly=75  domOnly=30
$SP/cmp_pdp_390.json    tokenDiff=24  figOnly=80  domOnly=48
$SP/cmp_science_1440.json tokenDiff=8  figOnly=11  domOnly=16
$SP/cmp_science_390.json  tokenDiff=14 figOnly=18  domOnly=37
```

### 0.2 本轮新增的三个探针（都在 `$SP`，未落进项目）

```bash
# ① Figma 帧树 + 几何（visible:false 自动跳过）
python3 $SP/tree.py figma/nodes/324-52658_product-page-desktop.json --y 1180 1460 --d 9
python3 $SP/tree.py figma/nodes/324-53792_pdp-mobile.json --y 0 800 --d 8
python3 $SP/tree.py figma/nodes/324-56865_science-desktop.json --y 950 1400 --d 7
python3 $SP/tree.py figma/nodes/324-58044_science-moble.json  --y 1970 2300 --d 4

# ② 实现端 rect + computed style（Playwright，真视口，滚完全页等 1800ms）
python3 $SP/geom.py pdp.html     1440 ".product__info,.product__accordion,.product__taste,..."
python3 $SP/geom.py pdp.html     390  ".product__thumbs,.product__thumb,.product__label-btn,..."
python3 $SP/geom.py science.html 1440 ".science-card,.science-card__value,.compare__row,..."
python3 $SP/geom.py science.html 390  ".science-card,.bear-meter,.ingredients,..."

# ③ 小熊填充条计数（行/列/透明度/单只尺寸）
python3 $SP/bear.py

# ④ 自造内容扫描：把两页 DOM 全部文本与「本页两稿 + 全部 42 个 frame」求差
（脚本内联，见 §5）
```

### 0.3 看过的左稿右实现对照图

| 图 | 覆盖 |
|---|---|
| `$SP/b_pdp14_head.png` | PDP@1440 顶栏（发现 Figma 板上有 59.6px 浏览器 chrome，所有 fig_y 须减 59.6 才是页面坐标） |
| `$SP/b_pdp14_hero.png` | PDP@1440 图廊 / 价格 / 订阅壳 |
| `$SP/b_pdp14_acc.png` | PDP@1440 保证条 / 三图标 / 规格手风琴 / Tastes Like |
| `$SP/b_pdp14_packed.png` | PDP@1440 promo 卡 ×2 |
| `$SP/b_pdp14_testi.png` | PDP@1440 视频轮播 + **多出的文字 testimonial 卡** |
| `$SP/b_pdp14_vs.png` | PDP@1440 Us VS Them |
| `$SP/b_pdp14_rev.png` | PDP@1440 评论壳 + FAQ |
| `$SP/b_pdp14_foot.png` | PDP@1440 footer CTA + 页脚 |
| `$SP/b_pdp39_hero.png` | PDP@390 顶栏 / 图廊 / 缩略图 |
| `$SP/b_pdp39_guar.png` | PDP@390 保证条 / 手风琴 / Tastes Like / Packed With |
| `$SP/b_pdp39_promo.png` | PDP@390 promo 卡 |
| `$SP/b_pdp39_rev.png` | PDP@390 视频轮播 + 多出的 testimonial 卡 |
| `$SP/b_sc14_a.png` | Science@1440 hero + stat 卡 |
| `$SP/b_sc14_b.png` | Science@1440 nutrient 卡 + compare |
| `$SP/b_sc14_c.png` | Science@1440 compare 表 + 成分辐射图 + Shop Now |
| `$SP/b_sc14_d.png` | Science@1440 Free of Allergens |
| `$SP/b_bear14.png` | 小熊条 3× 放大对照 |
| `$SP/b_sc39_a.png` | Science@390 stat 卡（**小熊条换行**） |
| `$SP/b_sc39_c.png` | Science@390 compare + 辐射图 |
| `$SP/b_sc39_d.png` | Science@390 成分手风琴 + Free of Allergens |
| `$SP/b_sc39_e.png` `_f.png` | Science@390 辐射图衔接 / hero |

⚠ **`crop_pair.py --y` 的对齐锚点可能取到误配对的重复串**（如 7 个 `Convenient`、6 个 `Accordion Closed`）。
`b_sc39_e.png` 就因此显示出一个并不存在的 150px 空档 —— 用不重复的锚点（`compare__title`）复核后 dy 只差 8px。
**看到「凭空多出一大段留白」先换锚点复核。**

---

## 1. ① 真偏差

### PDP

#### P1-1 PDP 多出 3 张文字 testimonial 卡（1440 + 390）
- 位置：`pdp.html:299-325`（`.testimonials` 整块）
- 现象：视频轮播与免责声明之间，实现插入了 3 张「★★★★★ / 10/10 would recommend… / Plus not having a clean shaker bottle… / Dustin O.」卡。
- 判据：PDP 桌面稿里这三张确实存在，但节点 `I324:52709;313:11104…11107` 的 **`visible: false`**（隐藏组件变体）；PDP 手机稿连隐藏节点都没有。同一串文案在 **Homepage** 稿（`285:18162` y8356 / `228:5932` y9258）是 **可见** 的 —— 说明这是首页模块被复用到了 PDP。
  对照图 `$SP/b_pdp14_testi.png`、`$SP/b_pdp39_rev.png`；漂移量 `cmp_pdp_390.json` 上 `reviews__disclaimer` 的 `jump = +972`。
- 建议：PDP 删掉该块（或用一个 `--hide-on-pdp` 开关），首页保留。若客户确实想在 PDP 放，须设计方补稿。

#### P1-2 `Packed With` 列表整体水平居中，稿是左对齐列首（1440 + 390）
- 位置：`assets/scss/modules/_product.scss:378-383`（`.product__taste, .product__packed { align-items: center }`）
- 稿 vs 实现：
  - 1440：稿 icon x=**764.1**（=信息列左缘，节点 `I324:52733;316:18315`）／实现 x=**827.4**（右移 63.3）
  - 390：稿 icon x=**20**（节点 `I324:53797;191:…`，文字 x=70）／实现 icon x=58.4、文字 x=**108.4**（右移 38.4）
- 判据：`geom.py` 实测 `.product__packed-list` 1440 = x827.4 / w273.2；`tree.py` 稿 `Frame 992450` x=764.1。对照图 `$SP/b_pdp14_acc.png`、`$SP/b_pdp39_guar.png`。
- 注：同一块里的 `Tastes Like`（3 个圆圈）稿本来就是居中，别一起改。建议只让 `.product__packed-list` `align-self: stretch`，标题仍居中。

#### P1-3 手机端产品缩略图 5 张、未铺满（稿 6 张铺满 350）
- 位置：`pdp.html:110-114`（5 个 `.product__thumb`）；`assets/scss/modules/_product.scss:91-101`（`justify-content: center`）
- 稿：`I324:53797;191:2358` = **6 张 52×52，gap 7.6，x 20→370 正好占满 350**（6×52+5×7.6=350）。
- 实现：5 张 52×52，gap 7.6，实测 x 49.8→340.2，居中留白 ±30。
- 桌面稿是 5 张（`I324:52733;332:17981`，47.9×48，竖排）→ **这是一处两稿冲突**（见 §3-G），但「铺不满 350」这件事无论几张都成立。

#### P2-4 信息列区块间距被统一成 24，稿有 32 / 48 两档（1440 + 390）
- 位置：`assets/scss/modules/_product.scss:178-186`（`.product__info { gap: 24px }`）
- 稿（`Product Details` gap 24；`Frame 992468` gap **48**；两者之间是 Product Details 的 `paddingBottom: 32`）：

| 相邻区块 | 稿 | 实现 | 差 |
|---|---|---|---|
| 三图标行 → 规格手风琴 | 32 | 24 | −8 |
| 手风琴 → Tastes Like | **48** | 24 | −24 |
| Tastes Like → Packed With | **48** | 24 | −24 |

- 判据：1440 稿 accordion 1418.2+300=1718.2 → `Tastes Like` 1766.2；实现 accordion y1034+284=1318 → `.product__taste` y1342。390 同样 −24（稿 2158.6→2206.6，实现 1776.8→1800.8）。

#### P2-5 规格手风琴项间距 20，稿 24（1440 + 390）
- 位置：`assets/scss/modules/_product.scss:329-333`（`.product__accordion { gap: 20px }`）
- 稿 `Accordian` 帧 `itemSpacing = 24`，行文字间距 **69**（1px 分隔线 + 20 padding + 24 行高 + 24 gap）。
- 实现行文字间距 **65**（gap 20）。5 行累计矮 16px。
- 判据：`cmp_pdp_1440.json` 上 `summary.product__acc-row` 的 `jump = −30 / −25`；`geom.py` 实测 `.product__acc-row[1..4]` y 步距 65。
- 注：**Science / FAQ 用的 `.faq__row` 步距是对的**（桌面 61、手机 69 都与稿一致），只有 PDP 这条 gap 写小了。

#### P2-6 PDP 产品区上内边距 96 / 64，稿 32 / 20
- 位置：`assets/scss/modules/_product.scss:5-10`（`.product { padding: 96px 0 } @include mobile { padding: 64px 0 }`）
- 稿：1440 `Product PDP` `paddingTop = 32`（下 96 是对的）；390 `Product image` 帧 `paddingTop = 20`。
- 实测：1440 内容首行 y=217，稿应为 152（+65）；390 内容首行 y=161，稿应为 116（+45）。
- `.product` 只有 pdp.html 用（`grep -rn "product--page"` 仅 `pdp.html:104`），改它不会波及别页。

#### P2-7 手机端两个主按钮高 60 / padding 16，稿 52 / 12
- 位置：`assets/scss/modules/_product.scss:150-175`（`.product__label-btn`）、`:268-290`（`.product__cta`）
- 稿 390：`I324:53797;191:2383` 与 `191:2465` 都是 **350×52，paddingTop/Bottom 12**，文字 **16/28 ls +0.48**。
- 实现 390：350×**60**，文字 **18/28 ls normal**（两处 CSS 都没有 mobile 分支）。
- 字号/字距那半条正是主会话已列的系统性偏差；**高度 60 vs 52 是它连带的第二半，一起改**。

#### P2-8 手机端退款保证条四项对不上
- 位置：`assets/scss/modules/_product.scss:292-303`
- 稿 390（`I324:53797;191:2466`）：350×**56**，`r = 8`，padding **8 / 16**，文字 **14/20**。
- 实现 390：350×**68**，`r = 16`（`$r-lg`），padding **12 / 20**，文字 14/**22**。
- 桌面稿是 401×68 / r16 / 12·20 / 14·22 —— **实现把桌面值原样带到了手机**。

#### P2-9 手机端三个保证图标：gap 24（稿 16）、宽 120（稿 106）
- 位置：`assets/scss/modules/_product.scss:305-318`
- 稿 390 `Frame 992441` gap **16**，每项 **106**（3×106+2×16 = 350 正好占满）。
- 实现：`gap: 24` + `width: 120px` → 350 装不下，被 flex 压到实测 100.7，且换行位置与稿不同（稿「30 Day / Money Back / Guarantee」3 行，实现 2 行）。
- 桌面稿 gap 24 / 宽 120 是对的，缺的是 mobile 分支。

#### P2-10 手机端图廊三个几何值
- 主图圆角：稿 **16**（`I324:53797;282:12317`）／实现 **24**（`.product__stage { border-radius: $r-xl }`，`_product.scss:125-140` 无 mobile 分支）
- 主图 → 缩略图 gap：稿 **16**（`Product image` 帧 itemSpacing）／实现 **12**（`_product.scss:59`）
- 缩略图 → 「View Nutritional Label」gap：稿 **16**／实现 **24**（`.product__media { gap: 24px }` 无 mobile 分支）

#### P2-11 手机端 header 图标顺序反了（PDP + Science，实为全站 header）
- 位置：`pdp.html:33-37`、`science.html:33-37`（`.header__icons` 内 Account 在前、Cart 在后）
- 稿：**桌面**是 `264:6259`(账户) → `83:5328`(购物袋)；**手机全部 5 个 frame 一致地反过来**：`83:5328`(购物袋) → `264:6259`(账户)。
  逐帧核过 `324-53792_pdp-mobile` / `324-58044_science-moble` / `228-5932_homepage-mobile` / `324-64961_reviews` / `324-70523_how-gumi-works`，无一例外。
- 实现两个断点都是 账户 → 购物袋。对照图 `$SP/b_pdp39_hero.png`、`$SP/b_sc39_f.png`。
- 建议：手机断点用 `flex-direction: row-reverse` 或单独排序，别动 DOM 顺序（a11y 上账户在前也说得通）。**这条跨全站，请主会话去重。**

#### P2-12 手机端 promo 卡内部间距
- 位置：`assets/scss/modules/_promo.scss:87`（`@include mobile { gap: 8px; padding: 32px 24px }`）
- 稿 390 卡 1（`I324:53800;196:19117/19129`）：padding 32/24 ✓，但 **标题→正文 12、正文→按钮 32**。
- 实现：标题→正文 **8**、正文→按钮 **8**。`cmp_pdp_390.json` 上 `a.btn 'Discount xx'` 的 `jump = −60` 即此（含少一行文字的 −24）。

#### P2-13（低）`.product__inner` 版心 975，稿 954
- `assets/scss/modules/_product.scss:12-21`：`max-width: 955px + 40px`。
- 稿 1440 产品区左右 padding 各 243 → 版心 **954**；实现 975，左缘 242.5 与稿 243 对齐，多出的 21px 全落在右侧空白里，**不影响任何可见对齐**。列出来只是备案。

### Science

#### P1-14 手机端小熊填充条没有按手机稿缩放，换行成 6 行
- 位置：`assets/scss/modules/_science.scss:142-147`（`.bear-meter__bear { width:13.5px; height:22px }`，无 mobile 分支）
- 稿 390（`I324:58052;285:24996`）：**5 行 × 20 只**，单只 **11.90 × 19.32**，列 gap **3.79**、行 gap **8**，行宽正好 310。
- 实现 390：单只仍是 13.5×22、gap 4 → 一行只放得下 17 只，实测排成 **17 / 17 / 17 / 17 / 17 / 15 六行**，末行短一截。
- 判据：`python3 $SP/bear.py` 输出
  `390 {"n":100,"faded":5,"rows":[[924,17],[950,17],[976,17],[1002,17],[1028,17],[1054,15]],"w":13.5,"h":22}`
  对照图 `$SP/b_sc39_a.png`（左稿 5 行齐整、右实现 6 行且末行残缺）。
- **总数 100 只、后 5 只 `opacity:.3` 两个断点都对**，问题只在尺寸与列数。
- 桌面端 `1440 {"rows":[[1111,20]×5],"w":13.5,"h":22}` —— **5×20 完全正确**（稿 13.51×22.06）。

#### P2-15 小熊条行/列间距
- 位置：`assets/scss/modules/_science.scss:135-140`（`gap: 4px` 单值）
- 稿 1440：列 gap **4.06** / 行 gap **8.11**；稿 390：列 **3.79** / 行 **8**。
- 实现两档都是 4/4 → 桌面网格高 126 vs 稿 142.8（矮 16.8）。
- 建议 `column-gap` / `row-gap` 分开写。

#### P2-16 `.science-card__value` 块高 44，稿 56
- 位置：`assets/scss/modules/_science.scss:113-124`
- 稿（`I324:56961;313:13210` `Frame 427319601` = 310×**56**，内含 107×32 的 `#b5ed61` 底块 + 56/44 文字）。
- 实现：`.science-card__value` 实测 h=**44**（纯 line-height），用 `ink-outline()` 画描边而非底块 —— **视觉一致**（`$SP/b_sc14_a.png` 上「95%」形态相同），但**块高少 12px**。
- 与 P2-15 叠加，卡片总高 1440：稿 378.8 → 实现 **350**；390：稿 332.6 → 实现 **344**（多出的一行小熊反而顶高了）。

#### P2-17 手机端 stat / nutrient 卡纵向间距 24，稿 32
- 位置：`assets/scss/modules/_science.scss:61-68`（`.science__cards { gap: 24px }`，`@include tablet` 只改了列数没改 gap）
- 稿 390：stat 卡容器 `Reviews` `itemSpacing = 32`（`324:58051`）；nutrient 卡容器同样 32（`324:58061`，896 = 4×200 + 3×32 反推亦为 32）。
- 实现实测：stat 卡 y 步距 368（卡 344 + gap 24）；nutrient 卡步距 224（卡 200 + gap 24）。
- 桌面横向 gap 24 与稿一致，只缺 mobile 分支。

#### P2-18 手机端「Just the necessities」正文 → 首个手风琴行 gap 40，稿 56
- 位置：`assets/scss/modules/_ingredients.scss:63-72`（`@include mobile { gap: 16px }`，桌面是 48）
- 稿 390（`324:58154` → `324:58158`）：Container(标题+正文) 4337.9 h118 → 手风琴 4487.9，**gap 32**，加上正文行盒余量实际文字间距 56。
- 实现：`.ingredients__body` y4003.5 → `summary.faq__row` y4137.5，文字间距 40。
- 判据：`cmp_science_390.json` 上 `summary.faq__row 'Vitamins'` `jump = −16.1`。

---

## 2. ② 字体度量差（PP Palma 400 = 300 试用件，AUDIT-HANDOFF 3.4-A，**不算实现偏差**）

全部表现为「实现比稿窄一档、色深浅一档」，一律不建议按像素追改：

1. **换行点整体后移**（同宽容器里实现能多塞 3~6 个字符）：
   - PDP promo 卡正文 1440 稿 5 行 / 实现 5 行但断点不同；390 稿 **6 行** / 实现 **5 行**（`$SP/b_pdp39_promo.png`）
   - Science compare lead 1440 稿 3 行 / 实现 3 行断点不同（`$SP/b_sc14_b.png`）
   - PDP 手机三个保证标签：稿「30 Day / Money Back / Guarantee」**3 行**，实现 **2 行**（这一条同时受 P2-9 的宽度影响，改宽度后仍会剩一部分差异）
2. **胶囊/标签宽度**：`.product__tag` 实测 146×32，稿 153×32（padding 12/6、r4、`#cbf390` 全对，差的只是文字墨迹宽 7px）。
3. **正文字重色深整体偏浅**：稿 400 用 PPPalma-Regular，实现指向 `fizzy-light`。全站现象，PDP/Science 无额外表现。
4. 与之相关但**不是**度量差的：`letter-spacing` 恒为 `-0.32px`（见 §4 系统性确认），那是 CSS 写死的，不是字体造成的。

---

## 3. ③ 有意为之 / 已裁决 / 新发现的待裁决

### 3.1 已在 AUDIT-HANDOFF 3.4 里，本轮逐条确认「实现与约定一致」

| 项 | 依据 | 核实结果 |
|---|---|---|
| PDP 订阅模块只留壳 | 3.4-E | ✅ `pdp.html:145` `.product__app-slot[data-app="subscription"]`，稿 y600.2–1084 那 19 条 `fig_only`（Autoship / Subscribe & Save / One Time / $40.40 / 4 Weeks…）**全部落在边界内** |
| PDP 评论区只留壳 | 3.4-E | ✅ `pdp.html:368-372`，稿 y5834–7634 的 42 条 `fig_only`（4.76 / Based on 123,000 reviews / 5 张评论卡 / See More Reviews）**全部落在边界内**。见 §3.3 一条边界判断 |
| PDP 详情 accordion 只做壳、`Text here` 占位 | 3.4-D/E | ✅ 稿里 6 条 `Text here` 是 `visible:false` 的展开态（`I324:52737;316:26032…26037`），实现原样保留，不是编造 |
| PDP 页脚 6 条 `Accordion Closed` | 3.4-D | ✅ 稿 y8087–8432 六条，实现一一对应，步距 69 与稿相同 |
| PDP 退款保证下 3 个占位图标 + `Tastes Like` 3 个 `Heading` | 3.4-D（批注 401:31225） | ✅ 稿即空心圆 + `Heading`，实现保留 |
| header Trustpilot 只做文字 | 3.4-E | ✅ 稿有 5 颗 `#b5ed61` 星（`324:52689` / `I324:53793;196:18751`），实现只有「Excellent Truspilot」两段文字。两个断点都如此 |
| Science stat 卡取手机文案 + 95% | 3.4-C | ✅ 1440 两条 `fig_only`（桌面稿卡 2/3 的同句占位）+ 390 三条 `dom_only`（95%）正是这次替换的痕迹，与裁决一致 |
| Science nutrient 卡做 3 张不造第 4 张 | 3.4-C | ✅ 390 `fig_only` 里 `Nutrient / 50% / Consectetur…`（y2881–2969）就是没做的第 4 张；`h2.compare__title` 的 `jump = −232.7` 恰好是它的高度（200 + gap 32），**不是间距 bug** |
| Science 成分区收尾两套按断点切换 | 3.4-C | ✅ 1440 = `Shop Now` 按钮（`$SP/b_sc14_c.png`），390 = 四行手风琴 `Vitamins/Minerals/Methylation/Organic ingredients`（`$SP/b_sc39_d.png`），步距 69 与稿相同 |
| `images/promo-art.png` 在 PDP 与 Science 复用 | 任务书 | ✅ 两页同一张图；两页各 6 条辐射标签（Whole Fruits / Whole Veggies / Super Mushrooms / Vitamins & Minerals / Gut health prebiotics / Adaptogens）在 `fig_only` 里出现是因为**稿里是 TEXT 节点、实现里烤进了 PNG**，内容并未缺失（`$SP/b_pdp14_packed.png`、`$SP/b_sc14_c.png` 目视确认） |
| PDP 产品图 sticky `top: 24px` | 3.4-F | ✅ `_product.scss:37-43`，`@include desktop-up` 才生效，稿无数值，属自定值 |
| 手风琴展开动画仅 Chrome 系 | 3.4-G | ✅ `components/_accordion.scss:35-47` `@supports selector(::details-content)` |

### 3.2 探针假阳性，**不是**问题

| 现象 | 真因 |
|---|---|
| `dom_only` 里成片的 `header__link` / `header__sublink` / `nav-card__*` / `Manage Account`（1440 七条、390 十八条） | 下拉/抽屉面板用 `grid-template-rows: 0fr` + `overflow:hidden` 收起（`layout/_header.scss:135-167`），**computed 不是 `display:none`**，`dom_text.py` 因此照收。这些文案来自 Figma 的 `283:14915 nav-expanded` 帧，不是自造 |
| `fig_only` 里的 `gumi.com.au`（1440）/ `funkyfood.com.au`（390） | Figma 板顶部那层 Safari/手机浏览器外壳（`324:52659` 高 **59.6**、`324:53794` 高 **96**）。**所有 fig_y 减去它才是页面坐标**，否则会把 header 高度误判成差 60~96px |
| `fig_only` 里的 `Enter your email` | 页脚订阅框的 `placeholder`，DOM 文本遍历取不到，实现里有 |
| `dom_only` 里的 `strong 'Less than 1%'` | 保证条整句被 `<strong>` 切了一段，属配对碎片 |
| `cmp_science_390` 里 6 条 `50%` 的 size 56→36 / lh 44→40 | 稿 stat 卡（56/44）被误配到实现的 nutrient 卡（36/40）。稿手机 nutrient 本来就是 **36/40 ls −0.36**，实现 `_science.scss:155-162` 已按此写，**两边其实都对** |
| `cmp_pdp_*` 里 6 条 `Accordion Closed`、`cmp_science_390` 里 7 条 `Convenient` 的 ±138 / ±288 跳变 | 同串重复导致的逆序配对噪声。用不重复锚点复核，FAQ 步距桌面 61 / 手机 69 与稿完全一致 |

### 3.3 一条需要确认的**边界判断**

- **PDP 评论区连静态标题 `Real Customer Reviews`（40px/w800）一起省掉了。**
  `pdp.html:366-372` 注释说明整段交给 app，但「4.76 / 123,000 reviews / 点赞点踩」才是 app 数据，
  **区块标题是静态文案**。现在这一屏在 app 挂载前只有一个虚线框、没有任何标题（`$SP/b_pdp14_rev.png`）。
  建议：把 `<h2>Real Customer Reviews</h2>` 留在壳里，或明确记进边界清单。P2。

### 3.4 新发现的两稿冲突 —— **不在 3.4-C 那 4 条里，需设计方裁决**

一律「实现取了信息量更大 / 与全站一致的一版」，符合既定原则，只是没人记过账：

| # | 位置 | 桌面稿 | 手机稿 | 现在的做法 | 判据 |
|---|---|---|---|---|---|
| A | PDP 手机 header 底色 | `#e7f8d0` | **`#ffffff`** | 用 `#e7f8d0` | 逐帧查过 5 个手机 frame，**只有 `324-53792_pdp-mobile` 是白的**，其余（science / homepage / reviews / how-gumi-works）全是 `#e7f8d0` → 判为孤例笔误 |
| B | PDP 手机「Batch Tested Quality」/ 3 个 `Heading` 口味标签颜色 | `#4d4d4d` / `#011307` | **`#ff2d55` / `#ff3b30`** | 用桌面色 | 节点 `I324:53797;191:3838` 等；同一行另两个标签仍是 `#4d4d4d`，且这两个色是 iOS 系统红，判为标注残留（`$SP/b_pdp39_guar.png` 左panel 确实渲染成红） |
| C | 手机页脚 | 3 组标题 + 12 链接 | **无分组标题**，两列 13 条，且叫 `Homepage` / `PDP` / `Influencers` | 用桌面版 | `fig_pdp_390` y10044–10236 vs `fig_pdp_1440` y9489–9637 |
| D | PDP promo 卡 2 末条与按钮 | `No nasties, full stop` + `Shop Now` | `No nasties` + `Discount xx` | 用桌面版 | `fig_pdp_390` y4317.6 / y4385.6 |
| E | Science 过敏原手风琴首行 | `Accordion Closed` | **`Dairy`** | 用手机版 | `fig_science_390` y5414.9；两个断点都渲染成 `Dairy`（`$SP/b_sc14_d.png`） |
| F | Science compare 段正文 | 长版「…earlier in the digestive process. This leads to fast and efficient bioavailability (delivery of nutrients into the bloodstream).」 | 短版「…earlier which leads to fast and efficient nutrients into the bloodstream.」 | 用桌面版 | `fig_science_390` y3313.8 |
| G | PDP 产品缩略图数量 | 5 张（竖排 47.9×48） | **6 张**（横排 52×52，铺满 350） | 做 5 张 | 见 P1-3 |

> A~G 均**不建议现在动**，等设计方一次性裁决。其中 **G 无论裁成几张，「手机端要铺满 350」都成立**（P1-3）。

---

## 4. ④ 需设计方给值 / 主会话统一写的系统性偏差（本组确认成立与否）

### 4.1 主会话点名要我确认的四条 —— **全部成立**

| 条目 | 在 PDP/Science 上的核实 |
|---|---|
| 页脚链接与版权行 稿 14/20 → 实现 16/24 | ✅ **仅 390 成立**。PDP@390 / Science@390 各 11 条 `footer__link` + `© 2027…` 全部 14/20→16/24；**1440 稿本身就是 16/24，实现无偏差**（`fig_pdp_1440` y9529–9862 全是 sz16 lh24），所以修的时候**只加 mobile 分支，别动桌面** |
| `letter-spacing` 实现恒 −0.32px | ✅ 成立。PDP@1440：`a.btn 'Shop now'` 稿 **0**、`span.vs__label` ×5 稿 **0**；Science@1440：两个 `.btn` 稿 0、`95%`/`50%` 各 3 处稿 **0**。全部被 −0.32 覆盖 |
| `.product__label-btn` / `.product__cta` @390 稿 16 + `+0.48` → 实现 18 + 0 | ✅ 成立（`fig_pdp_390` y658 / y1582.6，`fontSize 16 / letterSpacing 0.48`）。**并且高度也一起错了：稿 52 / padding 12，实现 60 / padding 16** → 见 P2-7 |
| `p.product__sub-title` 26→24、`p.product__guarantee-note` 20→22、`.reviews__disclaimer` 12/18→14/22 | ✅ 三条在 PDP@390 全部成立（`cmp_pdp_390.json` diffs）。**追加同族一条**：`span '4.8 stars'`（testimonial 区 eyebrow）稿 **12/18** → 实现 **14/22**，与 `.reviews__disclaimer` 同源 |

### 4.2 稿里没有、属「补设计」的自定值（PDP/Science 范围内）

- PDP 产品图 sticky 偏移 `top: 24px`（`_product.scss:39`）—— 批注只说要 sticky。
- 两个 app 壳的可见提示文字 **`Subscription options load here.` / `Customer reviews load here.`**
  （`pdp.html:145` / `pdp.html:370`）—— 稿里没有，是开发脚手架。**上线前必须换成真 app 或空态文案**，否则客户预览时会看到英文调试串。
- 全部 hover / active 交互态、手风琴展开态图标 —— 沿用全局，本组未复核（属第 5 条独立工作）。

---

## 5. 有没有自造内容？—— **没有**

把 PDP / Science 两页 ×2 断点的**全部 DOM 文本**去重后，先与「本页桌面稿 + 手机稿」求差，再与**全部 42 个 frame**求差：

```
pdp@1440  OTHER-FRAME  a.btn btn--lg          'Manage Account'
pdp@1440  OTHER-FRAME  span.nav-card__title   'Shop Gumi'
pdp@1440  OTHER-FRAME  span.nav-card__tag     'Refer a Friend'
pdp@1440  OTHER-FRAME  span.nav-card__text    'Earn rewards and $20 for every referral.'
pdp@1440  *** 无任何 frame  div.product__app-slot  'Subscription options load here.'
pdp@1440  *** 无任何 frame  strong                 'Less than 1%'
pdp@1440  *** 无任何 frame  div.app-slot           'Customer reviews load here.'
science@1440 OTHER-FRAME  同上 4 条 header 抽屉文案
```

- `OTHER-FRAME` 四条来自 `283:14915 nav-expanded`（导航展开态稿），合法。
- `Less than 1%` 是保证条整句里被 `<strong>` 切出的一段，不是新内容。
- 只有两条 app 壳提示语是稿里完全没有的，属开发脚手架（§4.2 已列）。
- 反向也查了：`Text here` / `Accordion Closed` / `Dairy` / `10/10 would recommend…` **全部能在 Figma 源里找到**（部分是 `visible:false` 的隐藏变体），没有编造。

---

## 6. 总表：区块 × 桌面 / 手机 × 结论

`✅` 与稿一致（±2px 内）｜`△` 有偏差但不影响读图｜`❌` 需修｜`◐` 有意为之/待裁决

| 区块 | 1440 | 390 | 说明 |
|---|:--:|:--:|---|
| **PDP** | | | |
| 公告条 + header | ◐ | ❌ | Trustpilot 星→文字（边界内）；390 图标顺序反了 P2-11 |
| 产品区上内边距 | ❌ | ❌ | 96/64 vs 稿 32/20（P2-6） |
| 图廊：主图 465、缩略图外挂顶对齐 | ✅ | ❌ | 桌面 x180.5/48×5/gap5、主图 465×466 r24 全对；手机 5 张不铺满 + r24 + 两处 gap（P1-3、P2-10） |
| 评分 / 标题 / 价格标签 / 卖点列表 | ✅ | ✅ | 逐级 gap 16 与稿逐点吻合；标签 `#cbf390` r4 pad12/6 对 |
| 「View Nutritional Label」 | ✅ | ❌ | 桌面 465×60 / 18-28 全对；手机 60 vs 52、18 vs 16、ls 0 vs +0.48（P2-7） |
| 订阅模块壳 | ◐ | ◐ | 边界内；壳提示语需上线前替换 |
| 「Start Now」 | ✅ | ❌ | 同上 P2-7 |
| 退款保证条 | ✅ | ❌ | 桌面 401×68 r16 pad12/20 全对；手机四项全错（P2-8） |
| 三个占位图标行 | ✅ | ❌ | 桌面 gap24/宽120 对；手机应 gap16/宽106（P2-9） |
| 规格手风琴（5 行） | △ | △ | 步距 65 vs 69（P2-5）；首行无分隔线的处理与稿一致 |
| Tastes Like（3 圆圈） | ✅ | ✅ | 106 宽 / gap16 / 图 51×48 与稿一致 |
| Packed With（5 行） | ❌ | ❌ | 整体居中，稿左对齐（P1-2）；行内 icon34+gap16、行距 48 都对 |
| 信息列区块间距 | ❌ | ❌ | 24 统吃，稿 32 / 48（P2-4） |
| promo 卡 ×2 | ✅ | △ | 桌面 1062×528 r32 / 531 文本框 / pad48·56·48·48 与稿逐点吻合；手机内部间距 12·32→8·8（P2-12） |
| 视频轮播 + 免责声明 | ✅ | ✅ | 卡宽 303 / 步距 328 / 箭头位置一致 |
| **多出的文字 testimonial 卡** | ❌ | ❌ | 稿中为隐藏变体（P1-1） |
| Us VS Them | ✅ | ✅ | GUMI 卡 / THE OTHERS 列 / 5 行 / 分隔线 / 抹茶勺位置全对；仅 `.vs__label` ls |
| 评论壳 | ◐ | ◐ | 边界内；建议保留 `Real Customer Reviews` 标题（§3.3） |
| FAQ（6 行 Accordion Closed） | ✅ | ✅ | 步距 69 与稿一致 |
| Footer CTA + 页脚 | ✅ | △ | 桌面全对；手机 14/20→16/24（主会话统一写）+ 冲突 C |
| **Science** | | | |
| Page Header（hero） | ✅ | ✅ | 桌面 0–823、手机 0–688 与稿总高吻合，图/标题/正文位置一致 |
| stat 卡壳 | △ | △ | padding 32/20、r8、bg 全对；卡高 378.8→350（桌）/332.6→344（手），源于 P2-15/16 |
| stat 卡文案与数值 | ◐ | ◐ | 取手机文案 + 95%，与 3.4-C 裁决一致 |
| 小熊填充条 | ✅ | ❌ | 桌面 **5×20=100、后 5 只 .3、13.5×22 全对**；手机换行成 6 行（P1-14） |
| nutrient 卡 | △ | ◐△ | 3 张与裁决一致；36/40 手机字号正确；卡间距 24 vs 32（P2-17） |
| compare 表 | ✅ | ✅ | 7 行 / 分隔线 / 双列图标位置全对；正文取桌面文案（冲突 F） |
| 成分辐射图 | ✅ | ✅ | 与 PDP 同图复用，位置尺寸一致 |
| 成分区收尾（Shop Now / 手风琴） | ◐✅ | ◐△ | 两套都做，与裁决一致；手机 lead→首行 gap 40 vs 56（P2-18） |
| Free of Allergens（6 行） | ✅ | ✅ | 步距桌 61 / 手 69 与稿一致；首行 `Dairy`（冲突 E） |
| Footer CTA + 页脚 | ✅ | △ | 同 PDP |

---

## 7. 修复优先级建议

1. **P1（4 条，都会被一眼看出来）**：P1-1 多余 testimonial 卡 → P1-14 手机小熊条换行 → P1-2 Packed With 居中 → P1-3 手机缩略图不铺满。
2. **P2 里最划算的一组**：PDP 手机端缺 mobile 分支的那批（P2-7/8/9/10）可以一次改完，都是「桌面值漏加断点」。
3. 间距类（P2-4/5/6/12/15/16/17/18）建议与主会话的 `letter-spacing`、页脚 14/20 一起排一轮，改完跑一次全站 computed-style 快照（含伪元素）做判据 —— 这几处改的是 `gap`/`padding`，**diff 产物无效**。
4. §3.4 的 A~G 七条冲突打包发设计方，不要自行选定。

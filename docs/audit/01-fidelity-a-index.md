# 还原度审计 A 组 — Homepage（index.html）1440 / 390

审计人：A 组（并行会话）。日期 2026-08-20。
设计源：`figma/nodes/285-18162_homepage-desktop.json`（1440）、`figma/nodes/228-5932_homepage-mobile.json`（390）。
**本轮只出报告，未改动任何项目文件。** 未调用任何 Figma API。

---

## 0. 怎么查的

### 已用主会话工具

```bash
# 数值比对结果（主会话已生成，直接读）
$SP/cmp_index_1440.json   # tokenDiff=7  figOnly=53 domOnly=82 gapJump=20
$SP/cmp_index_390.json    # tokenDiff=38 figOnly=59 domOnly=101 gapJump=38
$SP/fig_index_{1440,390}.json / $SP/dom_index_{1440,390}.json
python3 $SP/crop_pair.py ...
```

### 本轮自建的三个探针（都在 `$SP/a/`，只读，不进项目）

| 脚本 | 作用 |
|---|---|
| `$SP/a/cp.py` | crop_pair 的加强版：支持 x 窗口 + 手动 dy + 缩放，避免大图被 Read 降采样看不清 |
| `$SP/a/geom.py` | Playwright 量任意选择器的 rect + padding/gap/radius/bg/字号（`.pop-word` 拆词让文本流量不到容器几何，必须走这条） |
| `$SP/a/fignodes.py` | 把 Figma 节点树按帧相对坐标全量导出（含 **非 TEXT 节点**：FRAME/VECTOR/ELLIPSE 的 x/y/w/h、itemSpacing、padding、rotation、fill），`fig_text.py` 只吐 TEXT，查间距/装饰/波浪必须看这个 |

典型调用：

```bash
python3 $SP/a/geom.py index.html 1440 '.stats__grid|.stat|.stats__bear|.stats__arrow'
python3 $SP/a/fignodes.py figma/nodes/285-18162_homepage-desktop.json 3500 4880
python3 $SP/a/cp.py index 1440 3690 480 d06-highlight.png --x0 60 --x1 520 --dy -134
```

另外用 numpy 对两侧截图做**逐列颜色边界剖面**（判扇贝弧向/振幅、pack 倾角、小熊墨迹框），这是本轮几条硬结论的判据。

### ⚠ 坐标换算（后面所有数字都按这个）

两张 Figma 画板顶部都带浏览器窗口模型：**桌面稿 toolbar 高 59.62（取 60）**，**手机稿 chrome 高 96**。
所以 `稿页面坐标 = 节点 y − 60`（1440）/ `− 96`（390）。
`cmp_*.json` 的 `drift.dy` 是「DOM 页面 y − 稿节点 y」，**含这 60/96 的常量**，直接读会误判 —— 本报告一律换算成页面坐标后再比。

### 看过的对照图（全部在 `/tmp/claude-1007/-home-ly/c7ffb540-53f6-4bbe-87d6-fe452694dbc5/scratchpad/a/`）

桌面：`overview-1440.png` `d01-hero.png` `d02b-lead.png` `d02c-usp.png` `d03-stats.png` `d03b-bear.png`
`d03c-arc.png` `d04-stats-science-join.png` `d05-sci-card.png` `d06-highlight.png` `d07-band.png`
`d07c-band.png` `d07d-pack.png` `d08-footercta.png` `d09-footer.png` `d10-scallop-sand-lime.png`
`d11-scallop-lime-white.png` `pack.png`

手机：`overview-390.png` `m01-hero.png` `m02-bear-stats.png` `m02b-bear.png` `m03-stats-science.png`
`m04-highlight.png` `m05-product-top.png` `m06-stats.png` `m07-reviews.png` `m08-footer.png`

### 页面高度基线

| | 稿（页面坐标） | 实现 | 差 |
|---|---|---|---|
| 1440 | 10063 | 9471 | −592 |
| 390 | 11447 | 11521 | +74 |

---

## ① 真偏差（可直接修）

### 【D-1】P0 · highlight card 图片底部的扇贝唇口深了 3 倍

- 位置：`assets/scss/modules/_nutrition.scss:63-72`（`bottom: -1px` 在 66 行）；`index.html:312 / 322 / 332`
- 断点：**1440 与 390 都中**
- 现象：稿里图片底部只被一条浅波浪切掉一点点；实现里绿色圆弧几乎把图片下半截吃掉，而且下沿露出**第二排反向弧**（圆的下半弧），看上去像两层波浪。
- 判据（逐列量灰色占位图 `#d9d9d9` 的最低点）：

  | | 弧顶（离图片底） | 波幅 |
  |---|---|---|
  | 稿 1440 | 29.76px（Union `I341:46409;324:37001` y=3968.9，图片底 3998.66） | 21px |
  | 实现 1440 | **93.6px**（灰色底在 3771 / 3864 两档跳变，图片底 3864.6） | 93px |

  SVG 本身没错：`viewBox 0 0 573 94`，圆半径 47、圆心 y=47、间距 79.77 → 弧起伏 22.1px，正好等于稿的 21px。
  错的是**露出量**：稿只露该形状最上面的 29.76px（其余 64.24px 沉在图片下方），实现 `bottom:-1px` 把 93px 全露了出来。
- 建议：`bottom: -1px` → 约 **`-23.5%`**（= 64.24 / 273.76，`bottom` 百分比按容器高解析；1440 下等于 −64px）。
- 判据图：`d06-highlight.png`（桌面）、`m04-highlight.png`（手机）

### 【D-2】P1 · 三条大扇贝分隔条的弧向反了

- 位置：`assets/scss/components/_scallop.scss:65-78`（`.scallop--lg` 写死"上面那块向下鼓"）；用它的三处见 `index.html:305 / 372 / 494`
- 断点：**1440 与 390 都中**
- 现象：稿里这三条是**下面那块的颜色向上鼓**（尖角朝下），实现画成了**上面那块向下鼓**（尖角朝上），整条上下镜像。

  | 分隔条 | class | 稿 | 实现 |
  |---|---|---|---|
  | hero → 白（`index.html:130`） | `--lg --to-white` | 向下鼓 | 向下鼓 ✅ |
  | science → nutrition（`index.html:305`） | `--lg --sand-to-lime` | **向上鼓** | 向下鼓 ❌ |
  | nutrition → product（`index.html:372`） | `--lg --lime-to-white` | **向上鼓** | 向下鼓 ❌ |
  | product → reviews（`index.html:494`） | `--lg --white-to-mint` | **向上鼓** | 向下鼓 ❌ |

- 判据：① 逐列颜色顶沿剖面 —— 稿 `sand→lime` 的 lime 顶沿是 `16 9 4 2 1 2 6 11 19 30 …`（最小值 1，弧顶圆、谷尖），实现是 `21 28 33 35 35 35 32 26 19 7 …`（最大值贴底 35，弧顶平、谷尖朝上），相位与形状都相反；② 手机稿三条 Spacer 都带 `rotation = −3.1416`（180°翻转），只有 hero 的 `Spacer Bottom` 不翻转 —— 与像素结论一致。
- 顺带：**几何参数本身是对的**，不用动。1440 小扇贝（`--to-lime`/`--to-green`）逐列剖面与稿逐值只差 1px；`--lg` 96/128 的高度、弧半径、节距都对。
- 建议：给 `.scallop--lg` 补一个「向上鼓」的变体（复用基础 `.scallop` 的 gradient 写法 + `--lg` 的大 tile 与 band），这三处换用它。
- 判据图：`d10-scallop-sand-lime.png`、`d11-scallop-lime-white.png`

### 【D-3】P1 · stats 与 science 之间少了一条 96px 扇贝 + 一只装饰小熊

- 位置：`index.html:268-269`（`</section>` 与 `<section class="science">` 之间）
- 断点：**1440 与 390 都中**
- 稿：桌面 `Spacer Desktop 341:47307`（页面 y 2438.1，高 96，上 `#faf9f8` → 下 `#f5f1e9`）；手机 `Spacer Top 236:10300`（页面 y 2382.3，高 36）。
  同一位置还压着一只倾斜的小熊：桌面 `Gumi 341:47521 / 341:47524`（页面 y 2348.5，x 1033.8，284.5×250.2，rotation 0.3232 rad）；手机 `Frame 992545 243:28564 / 243:28567`（页面 y 2325.1，x 172.9，188.7×166.0）。
- 实现：两处都直接从 `.stats` 平切到 `.science`，没有波浪也没有小熊。
- 影响：桌面全站下方内容因此上移 96px（这是 `drift` 里 `j = −96` 的来源）。
- 判据图：`d04-stats-science-join.png`、`m03-stats-science.png`

### 【D-4】P1 · nutrition 产品包排（pack band）被旋转了两次，且整排没有倾斜

- 位置：`assets/scss/modules/_nutrition.scss:127-133`（`transform: rotate(-6.56deg)`）；`index.html:356-368`
- 断点：**1440 与 390 都中**
- 现象一（双重旋转）：`images/product-pack.png`（877×1005）**导出时已经带了 −6.72° 的倾角**（alpha 极值角：左极点 (0,90)、上极点 (763,0) → 顶边斜率 −0.1178）。CSS 再转 −6.56°，实测渲染倾角 **−13.0°**（截图逐列顶沿斜率 −0.2306），稿是 **−6.65°**（斜率 −0.1167）。
- 现象二（排不倾斜）：稿里 `Frame 60`（2246×1217）整体旋转 −6.556°，于是同一排里每个包**依次抬高 50.4px**（`Inner Pack` 绝对 y = 4441.5 / 4390.8 / 4340.1 / 4289.4，节距 441.2）。实现把每排排平（`.pack-band__row` 里所有包同 y），只让单个包倾斜。`_nutrition.scss:120` 那句注释「Figma 旋转整帧，正好抵消了行内的 y 台阶」结论反了 —— 台阶正是旋转**产生**的。
- 包尺寸与节距是对的：438px / 441 节距，与稿 438.38 / 441.2 一致。
- 建议：去掉 CSS 的 `rotate`（PNG 已自带），再让整排按 −6.56° 走（旋转 `.pack-band`，或给每个包一个 −50.4px 的递进 `margin-top`）。
- 判据图：`d07c-band.png`、`d07d-pack.png`、`pack.png`

### 【D-5】P1 · highlight card 标题与正文之间缺 12px

- 位置：`index.html:315 / 325 / 335` 的 `.highlight-card__body`，SCSS 里**没有这个类的规则**（`_nutrition.scss` 只写了 `.highlight-card__title:74` 和 `.highlight-card__text:83`）
- 断点：1440 与 390 都中
- 稿：`Frame 992451`（`I341:46409;285:21048`）`itemSpacing = 12`；标题 y=3962.6(页面) h=40，正文 y=4014.6 → 间距 52 = 40 + 12。
- 实现：标题 3888.61 h=40，正文 3928.61 → 间距 40 = 40 + **0**。
- 连带：卡片总高 445.73 vs 稿 457.76（差正好 12.03）。
- 建议：`.highlight-card__body { display:flex; flex-direction:column; gap:12px; }`

### 【D-6】P1 · product 右栏里手风琴 / Tastes Like / Packed With 三块的间距 24，稿是 48

- 位置：`assets/scss/modules/_product.scss:178`（`.product__info { gap: 24px }`）
- 断点：1440（390 同结构，见下表）
- 稿：`Product Details`（`I316:20489;316:18199`）的子项 itemSpacing = 24，但 `Frame 992468`（`I316:20489;316:18291`）的子项 itemSpacing = **48**。实现把整栏拍平成一个 gap:24 的 flex，48 的那层没了。
- 数字：手风琴块末 → `Tastes Like` 标题：稿 48 / 实现 24；`Tastes Like` 末 → `Packed With` 标题：稿 48 / 实现 24。共 −48px。
- 建议：给 accordion + taste + packed 套一层 `gap:48px` 的容器。

### 【D-7】P1 · 「30 Day / Money Back Guarantee」稿里的强制换行没落地

- 位置：`index.html:417`
- 断点：1440 与 390
- 稿 `I316:20489;316:18281` 的 characters 是 `'30 Day  Money Back Guarantee'` —— **U+2028 LINE SEPARATOR**，即设计方在 "30 Day " 后打了硬换行，整段占 3 行（h=66 = 3×22），徽章块高 106。
- 实现写成一整串 `<span>30 Day Money Back Guarantee</span>`，排成 2 行，徽章块高 84（−22px），三个徽章的基线也因此和稿不齐。
- 参考 memory `nl2br-blind-to-u2028`：U+2028 在 HTML 里不折行，必须显式转成 `<br>`。
- 建议：`30 Day<br>Money Back Guarantee`。

### 【D-8】P1 · 手机稿没有媒体 logo 滚动条，实现多了一整段

- 位置：`index.html:133-224`（`<section class="logo-scroll">`）+ 前后两条扇贝
- 断点：**仅 390**
- 稿：手机板 `228:5932` 的 `Page Content` 依次是 `Page Header` → `Hovering Bear` → `Section`(stats)，全板搜不到任何 logo/Social Proof 帧（桌面板有 `Social Proof 341:47384`）。
- 实现：390 下渲染 `.logo-scroll`（y 1207.27，高 192）+ 额外一条 `.scallop`（y 1399.27，高 48）。
- 建议：等设计方确认是「手机稿漏画」还是「手机不展示」；在拿到答复前这是 A 组能确认的最大结构性差异之一。
- 判据图：`m02-bear-stats.png`

### 【D-9】P1 · 手机 hero 小熊放错了层，而且小了约 23%

- 位置：`assets/scss/modules/_hero.scss` 的 `.hero__art` mobile 块；`index.html:127`
- 断点：**仅 390**
- 稿：绿色 hero 块在 USP 行下方（页面 y=572）就用 `Spacer Bottom` 扇贝收口，**小熊落在扇贝之下的白底上**（`Hovering Bear/Bear 2 243:28349`，页面 572..1068，496 高）。
- 实现：小熊在 `.hero__inner` 里面，仍是薄荷底 `#e7f8d0`，扇贝被推到小熊之后（y=1172）。
- 尺寸（量 lime 描边墨迹框）：稿 **≥330 × 537**（右侧被 390 视口切掉，实际更宽）；实现 **301 × 416**，高度只有稿的 77%。
- 判据图：`m01-hero.png`、`m02b-bear.png`

### 【D-10】P1 · 手机 science 标题/引导语稿是左对齐，实现居中；引导语还少一整句

- 位置：`assets/scss/modules/_science.scss:33-39`（`.science__head { text-align: center }`，无 mobile 覆盖）；`index.html:272-273`
- 断点：**仅 390**
- 稿 `228:8167`：`align = LEFT`，x=20 w=350，30/36/−0.3，3 行。
  稿 `228:8168`：`align = LEFT`，16/24/−0.32，**4 行 96px**，全文是
  > You loved gumi bears as a kid. This time, they're actually good for you, and we've got the research to prove it. **Based on similar studies on this type of formulation.**
- 实现：两者都居中，引导语缺最后一句（3 行）。
- 注：桌面稿 `I341:46642;316:29449 / …29451` 是 CENTER 且没有那一句 —— 属两稿冲突，见第 ④ 节。但**左对齐这条在手机稿里是明确的**。
- 判据图：`m03-stats-science.png`

### 【D-11】P1 · 手机 science 卡 2 / 卡 3 的正文用了桌面的占位句

- 位置：`index.html:276`（注释「All three cards carry the same copy in the design」）、`index.html:291 / 300`
- 断点：**仅 390**
- 稿（手机）三张卡正文分别是：
  1. `of users take Gumi at least 4-6x per week with 80% taking Gumi daily.*`
  2. **`No Fillers, No Nasties`**（`fig y 3330.9`，16px `#4d4d4d`）
  3. **`Made for Aussies`**（`fig y 3671.6`）

  三张卡的 eyebrow 都是 `Easy Habit`（与桌面一致）。
- 实现：三张全用第 1 句。
- 与 AUDIT-HANDOFF 3.4-C 的「Science 三张 stat 卡：桌面同一句占位 / 手机三段真文案 → 用手机的」是同一类冲突，但 3.4-C 只写了 Science 页，**homepage 这一处漏了**。

### 【D-12】P1 · 手机端四个手绘箭头被整体隐藏，但手机稿有

- 位置：`assets/scss/modules/_stats.scss:143`（`.stats__arrow { @include tablet { display: none } }`）
- 断点：**仅 390**（1024 以下全隐）
- 稿：手机板每个 stat 列下面都挂一个箭头（`Frame 992555 243:28619 / 243:28631` 等，118px 高的容器里放 60~68px 的箭头组，各自带旋转），四个都在。
- 实现：`.stats__arrow` 四个元素 rect 全是 0×0。
- 判据图：`m06-stats.png`

### 【D-13】P1 · 手机 footer 两只装饰小熊错位，其中一只压住正文

- 位置：`index.html:552-553`（`images/deco-bear-sm.png` / `deco-bear-md.png`）
- 断点：**仅 390**（1440 下两只只差 4~9px，可接受）

  | | 稿（页面坐标） | 实现 | 差 |
  |---|---|---|---|
  | 小熊 1 `I236:12187;313:9960` | y 9900.2, x 41.4, 153.6×135.1 | y 9851.5, x **7.8**, 154×135.5 | x −33.6 |
  | 小熊 2 `I236:12187;313:10013` | y 10416.4, x 173.4, **188.3×165.7** | y 10199.4, x **230**, **160×140.7** | y −179、x +57、尺寸 −15% |

  （对齐基准：手机 footer-cta 区段 Δ = −38.29px）
- 后果：小熊 2 本该骑在 lime→green 扇贝上，现在浮在 CTA 正文上方，遮住「…the multivitamin struggle for something they actually…」几个字。
- 判据图：`m08-footer.png`

### 【D-14】P1 · 手机端普通 `.scallop` 条高 48.02，手机稿全部是 36

- 位置：`assets/scss/components/_scallop.scss:44`（`--wave-band: clamp(13.3px, 1.63vw, 23.4px)`）
- 断点：**仅 390**，命中 3 处（`--to-cream` / `--to-lime` / `--to-green`）
- 稿：手机板 7 条 Spacer 高度**全是 36**（`Spacer Bottom I237:12777;236:12562`、`Spacer Top 236:10300 / 236:10309 / 243:22225 / I236:11294;237:16066 / I236:12187;236:11719 / I236:12187;236:10665;187:3983`）。
- 实现：`--lg` 那几条算出来 35.27（≈36 ✅），但普通 `.scallop` 算出 48.02 —— 弧本身对（振幅 ~29、节距 ~143，与稿逐列剖面一致），**多出来的 12px 全是弧下面那截实心 band**（稿 ≈1.3px，实现 13.3px）。
- 建议：`--wave-band` 的下限 13.3px 是别的板子的数，homepage 手机板要 ≈1.3px；把 band 也做成随 tile 缩放（像 `--lg` 那样）。

### 【D-15】P2 · 两条弧形文字（arc-text）的盒子比稿高，把下面的标题顶下去

| | 稿 | 实现 | 差 |
|---|---|---|---|
| `.stats__arc`（ONE HANDFUL） | `Curved Text 341:47317` 29px 高（手机 `236:12452` 也是 29） | `viewBox 0 0 237 50` → **50px** | +21 |
| `.footer-cta__arc`（YOUR GREENS CALLED） | `Curved Text I313:10171;313:9710` 51px | **62px**（`_footer.scss:63-68`，含 `margin-bottom:-8px`） | +11 |

- 位置：`index.html:229-232`（stats svg）、`assets/scss/modules/_stats.scss:39`；`assets/scss/layout/_footer.scss:63-68`
- 断点：1440 与 390 都中
- 连带：stats 标题因此比稿低 21px，整个 stats 段落高 1283 vs 稿 1230.11。
- 顺带（P2）：**stats 弧的弧度比稿平**。墨迹框稿 171×36、实现 172×**29**（宽度对上说明字号/字距没问题，差的是弧的起伏）。路径 `M 7.5 40 A 338 338 0 0 1 229.5 40` 的矢高 18.75px，要还原到稿需要半径约 **252**。判据图 `d03c-arc.png`。

### 【D-16】P2 · stats 区块内部的三处间距

| 位置 | 稿 | 实现 | 断点 |
|---|---|---|---|
| 四宫格 → 收尾注解（`_stats.scss:16` `.stats__inner{gap:64px}`） | `Frame 1984078222` itemSpacing **32** | 64 | 1440 |
| 标题组 → 注解 | `Frame 992507` itemSpacing **32** | 48（`.stats__inner` mobile gap） | 390 |
| 4 个箭头的定位 | 见下 | | 1440 |

箭头（`_stats.scss:146-149`）用的是 **Figma 旋转组的外接盒左上角**，不是画本身的墨迹框（memory `figma-rotated-frame-bbox-is-not-the-artwork`）。实测墨迹框：

| 箭头 | 稿墨迹（帧坐标） | 实现墨迹 | 偏差 |
|---|---|---|---|
| 1 | x517-627 y1690-1754 | x514-626 y1673-1738 | 高 17px |
| 2 | x423-537 y1969-2008 | x414-535 y1928-1971 | 高 41px、左 9px |
| 3 | x895-1008 y1903-1944 | x896-1017 y1862-1907 | 高 41px、宽 +8 |
| 4 | x894-1011 y2184-2222 | x895-1017 y2134-2174 | 高 50px |

建议的 `top/left/width`（相对 1193×623 的 `.stats__grid`）：
`--1 { left:32.98%; top:9.15%;  width:9.30% }`
`--2 { left:25.10%; top:53.93%; width:9.64% }`
`--3 { left:64.66%; top:43.34%; width:9.56% }`
`--4 { left:64.58%; top:88.44%; width:9.89% }`

判据图：`d03-stats.png`、`d03b-bear.png`

### 【D-17】P2 · science 卡内部两处

- `bear-meter` 行间距：稿 `Frame 427319610` itemSpacing **8.11**（5 行 22.06 + 4×8.113 = 142.75），实现 `gap: 4px`（`_science.scss:139`）→ 126，卡片矮 16.75px。
  （单只小熊 13.50×22.00、横向节距 17.5，与稿 13.51×22.06 / 17.55 完全对上 ✅）
- `95%` 数值块高度：稿 `Frame 427319601` **56px**，实现 `.science-card__value` **44px**（`_science.scss:113-123`）→ 下面正文上移 12px。
- 合计卡片高 350 vs 稿 378.75。
- 判据图：`d05-sci-card.png`

### 【D-18】P2 · product 右栏其余间距

| 项 | 稿 | 实现 | 位置 |
|---|---|---|---|
| 手风琴行间距 | 24（`Accordian` itemSpacing） | **20**（`_product.scss:329` `.product__accordion{gap:20px}`）→ 4 行共 −16 | 1440/390 |
| Product Details 底部内边距 | 32 | 24 | 1440 |
| features → 订阅区 间距 | 24 | 16 | 1440 |
| 信任徽章块高 | 106 | 84 | 见 D-7 |
| highlight-card 正文左右内边距 | `Frame 992456` padLR **8**（正文宽 346.67） | 0（正文宽 362.66） | 1440 |

### 【D-19】P2 · reviews 区两处

- `.testimonials`（`_reviews.scss:172-179`）`padding: 48px 80px 0` —— **少了 48px 的 padding-bottom**。稿 `Container I313:11170;313:11102` 是 padTop 48 / padBottom 48，再加区段 itemSpacing 48，所以「三张 testimonial → 免责声明」应为 96px，实现只有 48。
- `.reviews__disclaimer`（`_reviews.scss:229-237`）`max-width: 1100px`，实测 997.64 宽；稿 `Frame 992461` 是 **626** 宽、文字排 2 行。实现排成 1 行，块高 22 vs 稿 44。
- testimonial 卡高 220 vs 稿 212（正文→署名 100 vs 稿 92）。
- 判据图：`d08-footercta.png` 上缘 / `m07-reviews.png`

### 【D-20】P2 · footer CTA 内两个间距对调了

- 位置：`assets/scss/layout/_footer.scss:55-61`
- 稿：弧形文字 → 标题 = **32**；标题 → 正文 = **24**（`Frame 427319634` itemSpacing 24）。
- 实现：弧 → 标题 = 24；标题 → 正文 = 32。
- 判据图：`d08-footercta.png`

### 【D-21】P2 · 手机 PDP 图库

| 项 | 稿（手机） | 实现 | 位置 |
|---|---|---|---|
| 缩略图数量 | **6** 个（`I243:22226;191:2358` 六个 52×52，x 20/79.6/139.2/198.8/258.4/318，铺满 350） | **5** 个，整行 290.4 宽居中（x 起 49.81） | `index.html` product 区 |
| 主图 → 缩略图 | 16 | 12（`.product__gallery { gap:12px }`） | `_product.scss` |
| 缩略图 → 按钮 | 16 | 24 | 同上 |
| 「View Nutritional Label」按钮高 | **52**（pad 12/64） | **60**（pad 16/64） | `_product.scss` |

判据图：`m05-product-top.png`

### 【D-22】P2 · 手机端若干 token 没按手机稿缩小

| 元素 | 稿（390） | 实现 | 备注 |
|---|---|---|---|
| `.product__guarantee-note` / 三个信任徽章文字 | line-height **20** | 22 | 字号 14 对 |
| `.product__sub-title`（Tastes Like / Packed With） | line-height **26** | 24 | |
| `4.8 stars` | **12 / 18** | 14 / 22 | |
| `.reviews__disclaimer` | **12 / 18** | 14 / 22 | |
| `.stats__bear`（`_stats.scss:176` `overflow:hidden`） | 墨迹 226×229 | 195×185（lime 光晕被裁） | |

### 【D-23】P2 · 桌面 hero 小熊略小 / 略高

- 稿墨迹（lime 描边框）x 776-1301（526 宽），实现 x 791-1286（**496 宽**，−5.7%）；水平中心一致（都是 1038.5），顶端高 18px。
- 位置：`assets/scss/modules/_hero.scss` 的 `.hero__art`（1440 下 568×816 @ x760 y135）。
- 判据图：`d01-hero.png`

---

## ② 字体度量差（PP Palma 400 → fizzy-light，AUDIT-HANDOFF 3.4-A，当前不可消除，**不算实现问题**）

- **F-1** hero 引导语断行位置不同：容器两边都是 380px、20/30/−0.4 完全一致，但稿断在 "…real vitamins," 之后，实现把 "hiding in" 提到了第一行。纯字宽差。判据图 `d02b-lead.png`。
- **F-2** 同一段里 "hiding" 看起来像 "hicling" —— fizzy-light 的 `d` 字碗开口，是字重降级的副作用，不是文案错。
- **F-3** 多处正文行数变化：stats 四张卡、science 卡正文、`highlight-card` 第 2 张（稿 2 行 48px → 实现 1 行 24px）、product 信任徽章。**注意**：`highlight-card` 那一处同时叠加了 D-18 的「缺 8px 内边距」，两个因素都有。
- **F-4** 按钮里文字的居中位置与稿差几十 px（`Shop now` dx −36.9、`Try Gumi` dx −150.5 等）—— 按钮盒本身位置尺寸都对得上（实测 `Shop now` 按钮 1095.9-1256.9 vs 稿 1092.6-1255.6），差的只是更窄的文字在盒内重新居中。
- **F-5** `cmp_*.json` 里 `text-case`/`align` 一类的 LEFT↔CENTER 报警，绝大多数是「Figma 里文字在自动布局容器内左对齐、容器居中」造成的，不是偏差（`Start Now` / `4.8 stars` / `Adaptogens & Herbs` 等）。唯一真实的一条是手机 science 标题，见 D-10。

---

## ③ AUDIT-HANDOFF 3.4 已列的「有意为之 / 待裁决」（本页确认成立，不作为缺陷）

- **3.4-E 订阅模块只留壳**：稿 `Subscription I316:20489;316:18227` 高 **564**（Autoship and Save / Subscribe & Save / $40.40 / How subscription works / Delivers every 等 20 多条文字），实现是 `.product__app-slot`（120）+ CTA（60）= 204，**−360px**。`cmp_index_1440.json` 里 `figOnly` 那 20 条订阅文案、`drift` 里 `j = −359.7` 的那个跳变，全部由此而来。
  ⚠ 但 3.4-E 的表格只写了 PDP 页，**homepage 也有同一个模块**，建议补进那张表。
- **3.4-E Trustpilot 徽章**：实现是纯文字，稿里有五颗 lime 星（`332:16402` 及 5 个 `trustpilot star`）。另：稿里的拼写本来就是 **"Truspilot"**（打字错），实现照抄了 —— 上线前要向设计方确认。
- **3.4-D 占位内容**：product 手风琴展开后的 `Text here` ×5（`index.html` acc-body）；homepage 稿里手风琴是收起态、没有正文，所以这 5 段是沿用 PDP 的占位，不是从稿抄来的。
- **3.4-F 交互态自定**：手机 PDP 第一个缩略图的绿色选中框，稿里没有。
- ⚠ **不是 3.4 列过、但必须在交付前拿掉的**：`index.html:411` 的 `<div class="product__app-slot">Subscription options load here.` —— 这句英文开发占位会真的印在页面上（1440 y=5336.58 / 390 y=6795.8 可见）。

---

## ④ 需设计方给值 / 裁决

| # | 事项 | 两稿情况 | 现状 |
|---|---|---|---|
| Q1 | 手机端是否保留媒体 logo 滚动条 | 桌面有（`Social Proof 341:47384`），手机稿完全没有 | 实现两端都有（见 D-8） |
| Q2 | science 三张卡正文 | 桌面：同一句占位 ×3；手机：`No Fillers, No Nasties` / `Made for Aussies` | 实现两端都用桌面版（见 D-11）。与 3.4-C 对 Science 页的裁决口径冲突 |
| Q3 | science 标题/引导语对齐与文案 | 桌面 CENTER 且无末句；手机 LEFT 且多一句 `Based on similar studies on this type of formulation.` | 实现两端都用桌面版（见 D-10） |
| Q4 | 手机稿里的红色 | 手机稿 `Batch Tested Quality` = `#ff2d55`，三个 `Heading` 占位 = `#ff3b30`；桌面对应处是 `#4d4d4d` / `#011307` | 实现取桌面色。**判断：这两个红是 iOS 系统红，极可能是设计方的"待办标注"，不建议照实现**，但要设计方确认 |
| Q5 | 手机 footer 链接区 | 桌面：三组带小标题（Why Gumi / Learn more / Get in touch），标签 `Shop` / `Partners & Influencers`；手机：**无小标题**、两列、标签是 `Homepage` / `PDP` / `Influencers` | 实现两端都用桌面版。`Homepage`/`PDP` 看着像设计方留的内部标签 |
| Q6 | 手机 PDP 缩略图数量 | 桌面 5、手机 6 | 实现两端 5（见 D-21）。补第 6 个只是补灰色占位块，不算造内容，但要设计方定 |
| Q7 | 稿里 `Truspilot` 拼写 | 两稿一致都是 `Truspilot` | 实现照抄（见 ③） |
| Q8 | stats→science 交界的小熊 | 两稿都有 | 实现没有（见 D-3），确认是否保留 |

---

## ⑤ 主会话点名的三条跨页系统性偏差 —— 在本页的成立情况

1. **页脚链接与版权行 稿 14/20 → 实现 16/24**：**只在 390 成立**。1440 下稿本来就是 16/24/−0.32，实现完全一致，无偏差；390 下稿是 14/20/−0.28，实现仍是 16/24/−0.32（10 条链接 + 版权行 + Privacy/Cookies）。
2. **`letter-spacing` 实现恒为 −0.32**：**成立**。1440 命中 `a.btn`（Shop now / Try Gumi，稿 0）、`.science-card__value`（95%，稿 0）；390 还多命中 `.highlight-card__title`（稿 −0.24）、`.highlight-card__text`（稿 0）、`.testimonial__text`（稿 0）—— 因为这些类的 mobile 覆盖只改了字号/行高，没跟着改字距。
3. **390 下 `.product__label-btn` / `.product__cta` / `.btn` 稿 16px + 字距 +0.48，实现 18px + 0**：**成立**（`View Nutritional Label`、`Start Now` 两处直接命中；`.hero__btn` 有 mobile 覆盖所以是对的，说明漏的是 product 那两个类）。

---

## ⑥ 关于 `cmp_index_*.json` 里假阳性的说明（逐条核实过，不进结论）

- **`tokenDiff` 里的 2 条配对噪声**：`Vitamins & Minerals`（1440 稿 y=2051.8 ↔ DOM y=6276.58；390 稿 1603 ↔ DOM 7735.84）把 **stats 四宫格的标签**和 **product「Packed With」列表项**配到了一起；`Superfood Greens Gummies`（1440 稿 4409.76 ↔ DOM 4984.58；390 稿 5543 ↔ DOM 6451.84）把 **pack band 包装上的印字**和 **product 标题**配到了一起。两条报出来的 size/weight/color 差全部无效。
- **`domOnly` 里 82 / 101 条的绝大多数是测量伪影，不是页面多出来的内容**：
  - `.pop-word`（`data-pop-text` 的逐词拆分）—— 1440 占 60 条以上；
  - `.ink-halo`（`aria-hidden` 描边副本）让父元素的 `innerText` 变成 `'60+ 60+'`、`'21 21'`、`'6g 6g'`；
  - 折叠态 header 抽屉里的链接（`x = −370`，390 下）与桌面 mega-menu 面板（`Shop Gumi` / `Refer a Friend` / `Manage Account` 等）。
- **没有发现自造内容。** 逐条查过 `domOnly` 里所有非伪影的文本：`Manage Account`、`Refer a Friend`、`Earn rewards and $20 for every referral.` 都能在导航稿 `283-14915_nav-expanded.json` / `401-31721` 里找到原文；`Enter your email` 在 homepage 稿里就有（作为输入框占位）；`Less than 1%` 是稿 `characterStyleOverrides` 里的分段。唯二**稿里没有**的文本是 `Text here` ×5（沿用 PDP 占位，已在 ③ 说明）和 `Subscription options load here.`（开发占位，已标为交付前必删）。
- **`figOnly` 53 / 59 条的归类**：Safari 地址栏 `gumi.com.au` 1 条（画板自带的浏览器模型）；pack band 上的包装印字 `Superfood Greens Gummies` / `Single Serving` 共 20+ 条（实现里是 `product-pack.png` 位图，文字以像素存在）；订阅模块 20 条（3.4-E）；`.pop-word` 拆词造成的 stats 文案配不上 10+ 条；真正的内容缺失只有手机端的 `No Fillers, No Nasties` / `Made for Aussies` / `Homepage` / `PDP` / `Influencers`（见 D-11、Q5）。
- 顺带：设计稿里 9 张 `bear-scatter` 用的是**同一个 imageRef**（`a0315c…04e2`），实现复用一张 PNG **不违反铁律 3**。
- 主会话任务清单里的「Us VS Them 对比表」**不在 homepage 上**（两块稿里都搜不到 `VS Them` / `Compare`），本页不适用。

---

## ⑦ 总表：区块 × 桌面 / 手机 × 结论

| 区块 | 1440 | 390 |
|---|---|---|
| 公告条 + header | ✅ 对齐（40 / 80+1px，色值一致）；Trustpilot 星缺失属 3.4-E | ✅（32 / 64+1px） |
| hero 文案 + 按钮 + USP | ✅ 数值全中（380 宽、32.24/37.2 数值、23.21 单位字号、110 宽标签）；断行差属字体度量 | ✅ 尺寸对 |
| hero 小熊 | ⚠ D-23 小 5.7% | ❌ D-9 放错层 + 小 23% |
| logo 滚动条 | ✅（248 高、pad 88/64、193×96 节距 223） | ❌ D-8 稿里没有这一段 |
| 扇贝分隔条（几何） | ✅ 小 96 / 大 128 逐列剖面与稿差 ≤1px | ⚠ D-14 普通条 48 vs 稿 36（3 处） |
| 扇贝分隔条（弧向） | ❌ D-2 三处反向 | ❌ D-2 三处反向 |
| stats → science 交界 | ❌ D-3 缺扇贝 + 缺小熊 | ❌ D-3 同 |
| stats 弧形文字 | ⚠ D-15 盒高 +21、弧偏平 | ⚠ D-15 同 |
| stats 四宫格 | ✅ 卡片位置/内部间距全中（303 宽、12/42 间距） | ✅ 结构对（2+熊+2） |
| stats 箭头 | ⚠ D-16 高 17~50px | ❌ D-12 整体 display:none |
| stats 小熊 | ✅ 303×375 位置一致 | ⚠ D-22 光晕被裁 |
| stats 收尾注解 | ⚠ D-16 间距 64 vs 32 | ⚠ D-16 间距 48 vs 32 |
| science 三卡 + 小熊填充条 | ⚠ D-17 卡矮 28.75（bear-meter 行距 + 95% 块高） | ⚠ 同 + ❌ D-10/D-11 |
| nutrition 标题 + 三张 highlight 卡 | ❌ D-1 唇口 + ❌ D-5 缺 12px + ⚠ D-18 内边距 | ❌ 同 |
| pack band | ❌ D-4 双重旋转 + 排不倾斜 | ❌ 同 |
| product 图库 / 缩略图 / 按钮 | ✅ 465/466、5 张 48px、节距 52.56 全中 | ⚠ D-21 5 vs 6、间距、按钮高 |
| product 订阅区 | 🅾 3.4-E 有意留壳（−360px） | 🅾 同 |
| product 信任徽章 | ❌ D-7 缺硬换行 | ❌ 同 + ⚠ D-22 行高 |
| product 手风琴 / Tastes Like / Packed With | ⚠ D-6 间距 24 vs 48、⚠ D-18 行距 20 vs 24 | ⚠ 同 + ⚠ D-22 行高 |
| reviews 头部 + reels | ✅ 144 高、612/540、304×540 全中 | ✅ |
| testimonials + 免责声明 | ⚠ D-19 少 48px 间距、版心 997 vs 626 | ⚠ 同 + ⚠ D-22 字号 |
| footer CTA | ⚠ D-15 弧盒 +11、⚠ D-20 间距对调 | ⚠ 同 + ❌ D-13 小熊错位 |
| footer 本体 | ✅ 687 高、pad 64/48、四列位置全中 | ⚠ ⑤-1 字号 + Q5 结构待裁决 |

图例：✅ 对得上 ｜ ⚠ 有偏差（P2 级） ｜ ❌ 明显偏差（P0/P1） ｜ 🅾 有意为之

**统计：真偏差 23 条（P0 × 1、P1 × 13、P2 × 9）；字体度量差 5 类；3.4 已列有意为之 5 项（另有 1 条开发占位必须交付前删）；需设计方裁决 8 项。**

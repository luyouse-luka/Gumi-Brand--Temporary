# 还原度审计 · C 组 — Reviews / How Gumi Works / Our Story（1440 + 390）

> 审计人：C 组会话，2026-08-20。**只出报告，未改任何项目文件。**
> 依据：`docs/AUDIT-HANDOFF.md` §0 / §3（含 3.4）/ §7，`docs/PROJECT-STATUS.md`「待确认」「待替换占位」。
> 未调用任何 Figma API（§3.2 限流中），全部数值取自 `figma/nodes/*.json` 已落盘节点树。

---

## 0. 怎么跑的

**数值比对**（主会话已生成，直接读）

```
$SP/cmp_reviews_{1440,390}.json
$SP/cmp_how-gumi-works_{1440,390}.json
$SP/cmp_our-story_{1440,390}.json
$SP/fig_*  /  $SP/dom_*        # 原始 TEXT / DOM run
```

**自己补的两个量法**（脚本在 `$SP`，不进项目）

| 脚本 | 作用 | 为什么需要 |
|---|---|---|
| `$SP/sect.py` / `$SP/sect2.py` | 从节点树按 id 打印任意子树的 `absoluteBoundingBox`（已减画板原点） | `cmp_*.json` 只有 TEXT，量不到区块盒 |
| `$SP/sectdom.py <page> <w> <sel>` | Playwright 实测 DOM 区块 rect（滚完全页 + 等 1800ms 让 wowo 卸载） | 同上；且避开 §7.2 的 headless 陷阱 |

```bash
python3 $SP/sectdom.py reviews.html 1440 "body > *, main > section, main > div.scallop, .footer-cta-wrap > *, footer"
python3 $SP/sect2.py figma/nodes/324-63924_reviews-desktop.json 326:84889 2
```

> ⚠ **两个画板坐标系偏移，必须先减掉再比**：desktop 画板顶部有 59.6px 的 `toolbar`（Safari 窗口模拟），
> mobile 画板顶部有 96px 的 `Chrome browser`。不减这一层，全页 drift 会整体偏 60 / 96，得出错误结论。
> 本报告所有「稿 y」都是**减掉之后的页内相对值**。

**看过的对照图**（`crop_pair.py` 生成，左稿右实现）

| 文件 | 覆盖 |
|---|---|
| `$SP/c_rev1440_expert.png` | Reviews 1440 专家卡三张 |
| `$SP/c_rev1440_packed.png` | Reviews 1440 Tastes Like / Packed With |
| `$SP/c_rev1440_hdr.png` | Reviews 1440 评分汇总条 + 评论列表壳 |
| `$SP/c_hgw390_reviews.png` / `$SP/c_hgw390_t.png` | HGW 390 reels + 测评卡 |
| `$SP/c_hgw390_hero.png` / `$SP/c_hgw1440_hero.png` | HGW 两档页头（含副标裁决核对） |
| `$SP/c_os1440_story.png` | Our Story 1440 三张图文卡 + 扇贝 CTA 板 |
| `$SP/c_os390_story.png` | Our Story 390 图文卡纵向堆叠 |
| `$SP/c_os390_cta.png` | Our Story 390 扇贝 CTA 板 |
| `$SP/c_hdr_icons.png` | 移动端 header 右侧两个图标（4× 放大） |

---

## 1. 真偏差

### P1-1 · Our Story 390 扇贝 CTA 板整体缩水一半 — **P1**

**位置** `our-story.html:143-156` / `assets/scss/modules/_cta-band.scss:31,37,40,49,54,60,70,78`
**断点** 390
**判据** 节点 `324:73698`（CTA Block）与子树；`$SP/c_os390_cta.png`；`sectdom.py our-story.html 390`

| 量 | 稿（`324:73698` 子树） | 实现 | Δ |
|---|---|---|---|
| 板（plate）盒 | 350.9 × **507.5**，x=20 | 350 × **288.3**，x=20 | **−219.2** |
| 标题字号 / 行高 / 字距 | 30 / 36 / −0.3（**三行**） | 24 / 30 / −0.24（两行） | −6 / −6 |
| 弧形眉题 → 标题 间距 | 39 | 16 | −23 |
| 标题 → 按钮 间距 | **144** | 24 | **−120** |
| 按钮宽 | 274（`I324:73698;243:25215`） | 215.1 | −59 |
| 按钮 y（页内） | 2345.8 | 2138.6 | −207 |

板宽和左右 20px 留白是对的，**高度与内部留白全部按自定的响应式收缩写死了，没有取手机稿的值**。
对照图里两侧观感差别很大：稿是一块留白充裕的大圆牌，实现是一条扁带。

> ⚠ 这与 AUDIT-HANDOFF 4.4 第 3 条「<1280 弧会略压扁」**不是同一件事** —— 那条讲的是 mask 拉伸，
> 这里是板本身的高度/间距被改小了。1440 下板 1280 × **392**（稿 393）+ 弧起伏仍与稿一致，**上一轮结论仍成立**（见 `c_os1440_story.png`）。

**建议** `_cta-band.scss` 的 `@include mobile` 一组取手机稿：`padding-block` / `.cta-band__content` gap /
`.cta-band__head` gap / `.cta-band__title` 30/36/−0.3 / 按钮宽 274。若设计方确认「板内那段大留白是稿的疏忽」，
需要他们书面回一句再收窄，别默认收。

---

### P1-2 · `.testimonial` 的 `flex-basis` 在竖排后变成了卡片**高度** — **P1（真 CSS bug）**

**位置** `assets/scss/modules/_reviews.scss:181`（`.testimonials` 在 ≤1024 转 `flex-direction: column`）+ `:190`（`flex: 1 1 300px`）
**断点** 390（**1024 / 768 同样中招**，那两档没稿只能看「有没有坏」——这是坏的）
**判据** `sectdom.py how-gumi-works.html 390 ".testimonial, .testimonial > svg, .testimonial__body, .testimonial__name"`

```
figure.testimonial   y2654  h300     ← 盒子
  svg(stars)         y2654  h24
  blockquote         y2694  h128
  figcaption(name)   y2838  h24  → 内容到 2862
                                    卡底 2954，尾部 92px 是空的
```

主轴一换向，`flex-basis: 300px` 就从「宽度基准」变成「高度基准」，于是每张测评卡被撑到 300px 高、
底部空 92px。稿里卡高 **196**（`I324:70586;187:12732`，四张都是）。
这是 how-gumi-works / our-story 两页 `.reviews` 区块在 390 下比稿高 **+59.4px** 的主因（即使还少画了一张卡）。

**建议** 在 `@include tablet` 里把 `flex` 改成 `flex: 0 0 auto`（或 `flex-basis: auto`），
`max-width: 411px` 保留。改完用 `sectdom.py` 复量卡高，判据 = 卡盒高 ≈ 内容高。

---

### P1-3 · `.reviews__disclaimer` 宽度上限过大：稿两行被压成一行，且与卡片组的间距少一半 — **P1**

**位置** `our-story.html:211` / `how-gumi-works.html:203` / `assets/scss/modules/_reviews.scss:229-237`
**断点** 1440
**判据** 节点 `I324:69755;313:11108`（HGW）/ `I324:72948;…` 同款；`sectdom.py * 1440 ".reviews__disclaimer"`

| 量 | 稿 | 实现 |
|---|---|---|
| 免责声明盒 | x407 **w626** h44（**两行**） | x221.2 **w997.6** h22（一行） |
| 卡片组底 → 免责声明 间距 | **96**（容器 48 内边距 + 48 间隔） | **48** |

`max-width: 1100px`（:230）比稿的 626 宽出一大截，文字一行就排完了。
两条加起来，`.reviews` 区块 1440 下 1382 vs 稿 1444.2（**−62.2**）。

**建议** `max-width` 改 626（桌面）；`.testimonials`（:172）补 `padding-bottom: 48px`，
或把 `.reviews__inner` 到免责声明这一段的间距做成 96。390 下稿是 350 宽三行，实现也是三行 ✓（只有字号偏大，见 §5）。

---

### P1-4 · `.product__packed` 列表稿里左对齐，实现居中 — **P1**

**位置** `reviews.html:286` / `our-story.html:324` / `how-gumi-works.html`（同块）/ `assets/scss/modules/_product.scss:378-384`
**断点** 1440（390 同理）
**判据** 节点 `I324:64031;316:18313`（Packed With 框 x764.1 w401）与 `…;316:18315`（列表 icon 列 x**764.1**）；
`sectdom.py reviews.html 1440 ".product__packed, .product__packed-list"` → `ul` x**827.4**；对照图 `$SP/c_rev1440_packed.png`

稿里五条「Vitamins & Minerals / Adaptogens & Herbs / …」的圆点与面板左边缘齐平（x764.1 = 面板 x），
实现给 `.product__packed` 加了 `align-items: center`，整列被推右 **63.3px**。

⚠ **同一条规则下的 `.product__taste` 稿确实是居中的**（`I324:64031;316:18300` x789.6，在 401 宽面板里居中），
改的时候要把 `.product__taste, .product__packed` 这一组拆开，别一起改掉。

---

### P1-5 · 移动端专家卡轮播缺少左右箭头 — **P1**

**位置** `reviews.html:131`（`.expert__cards`）/ `assets/scss/modules/_expert.scss:44-67`
**断点** 390
**判据** 节点 `324:64975`（Frame 992460，x159 y1448.6 72×32）内含 `324:64976` / `324:64977` 两个 32×32 的 action 按钮

稿的手机版专家卡是**轮播 + 一对圆形箭头**（与同页 `.reels` 那套一模一样，`.reels` 已经实现了箭头）。
实现只做了 `overflow-x: auto` + scroll-snap 的滑轨，**没有箭头**。
连带：reviews 390 的 expert 区块 **748** vs 稿 **852**（−104 = 卡少一行 −24 + 箭头及其 48px 间距 −80）。

**建议** 复用 `.reels` 的箭头组件与脚本。若决定不做（纯滑轨），要在 CHANGELOG 记一句「有意省略」，
否则下一轮还会被当 bug 报一遍。

---

### P1-6 · 区块间隔条：稿 96 的地方实现一律用了 128 — **P2**

**判据** 节点树里 `Spacer Desktop` 实例的 `height` vs DOM `.scallop--lg` 的 128

| 页面 | 位置 | 稿 | 实现 | Δ |
|---|---|---|---|---|
| reviews@1440 | 专家卡区 → 评论区（`324:64033`） | 96 | 128 | +32 |
| reviews@1440 | 成分盘 → FAQ（`I324:63925;316:26092`） | 96 | 128 | +32 |
| how-gumi-works@1440 | PDP → FAQ（`I324:69637;316:26092`） | 96 | 128 | +32 |

其余位置稿本来就是 128（页头后、PDP 前），页脚 CTA 前稿 96 / 实现 95.9 ✓。
our-story@1440 一处都不涉及 ✓。390 下稿一律 36 / 实现 35.3 ✓。

**建议** 加一个 `.scallop--md`（96px）用在这三处，别把 `--lg` 改小（会波及其它页）。

---

### P1-7 · `.product__accordion` 行距 20，稿是 24 — **P2**

**位置** `reviews.html:228` / `our-story.html:266` / `how-gumi-works.html:277` / `assets/scss/modules/_product.scss:329-333`
**判据** 稿手风琴行实例 `I324:64031;316:18293…18297` y = 5322.6 / 5370.6 / 5439.6 / 5508.6 / 5577.6（行高 45，**节距 69**）；
DOM `summary.product__acc-row` y = 3377.7 / 3421.7 / 3486.7 / 3551.7 / 3616.7（**节距 65**）

行高 45 对了，**行间 gap 稿 24 → 实现 20**，5 行累计矮 16px。两个断点都一样。

---

### P1-8 · How Gumi Works 390：图文块间距被自定收缩，未取手机稿 — **P2**

**位置** `assets/scss/modules/_dosed.scss:33 / 44 / 92`
**断点** 390（**1440 完全一致**：`section.dosed` 1484 = 稿 1484，两个图文块 1250×598 = 稿，一分不差 ✓）
**判据** 节点 `332:22019` / `332:22029`（The Science 两块）+ `332:22020` / `332:22030`（文字框）；`sectdom.py how-gumi-works.html 390`

| 量 | 稿 | 实现 | 出处 |
|---|---|---|---|
| 两个图文块之间 | 80 | **48** | `_dosed.scss:33` `.dosed__inner` mobile gap |
| 块内 文字 → 图片 | 48 | **32** | `_dosed.scss:44` `.dosed__block` tablet gap（mobile 继承） |
| 标题 → 正文 | 32 | **24** | `_dosed.scss:92` `.dosed__text` mobile gap |

`section.dosed` 1541.5 vs 稿 1634（**−92.5**），其中 −24 是字体度量（正文少一行，见 §2）。

---

### P1-9 · How Gumi Works 390：页头标题少了稿里的手动换行 — **P2**

**位置** `how-gumi-works.html:108-113`
**断点** 390
**判据** 节点 `I324:70525;243:18687` `characters = "How Gumi\nWorks"`（h=80，两行 @36/40）；对照图 `$SP/c_hgw390_hero.png`

稿的手机版把标题**手动断成两行**「How Gumi / Works」，实现单行。
连带 `section.page-hero` **204** vs 稿 **244**（−40）。副标（珊瑚红两行 h52）实现完全对上 ✓。

**建议** 属于文案层面的换行，照抄稿即可（`<br>` 或 `text-wrap: balance` 都行），但要向设计方确认这个换行是刻意的还是画板宽度的副产物。

---

### P1-10 · `.product` 块 390 的三处 token 偏差 — **P2**

**位置** `assets/scss/modules/_product.scss:386-390`（sub-title）/ `:292-300`（guarantee-note）/ `:310-320`（guarantee 三个 USP）
**断点** 390（1440 全对 ✓）

| 元素 | 稿@390 | 实现 | 出处 |
|---|---|---|---|
| `p.product__sub-title`（Tastes Like / Packed With） | 18 / **26** / −0.36 | 18 / **24** / −0.36 | `:389` 无 mobile 覆盖 |
| `p.product__guarantee-note` | 14 / **20** / −0.28 | 14 / **22** / −0.28 | `:298` |
| `.product__guarantee` 三条 USP 文字 | 14 / **20** / −0.28 | 14 / **22** / −0.28 | `:319` |

三处都是「桌面值没写 mobile 覆盖」。逐条查过节点：桌面稿本身就是 24 / 22 / 22，所以只需补 `@include mobile`。

---

### P1-11 · `.ingredients__lead` 390 颜色 — **P2**

**位置** `reviews.html:314` / `assets/scss/modules/_ingredients.scss`
**断点** 390
**判据** `fig_reviews_390.json` 该 TEXT `color = #4d4d4d`；DOM `rgb(51,51,51)` = `#333333`
1440 下稿与实现都是 `#4d4d4d` ✓，只有 390 走了另一个色变量。

---

### P1-12 · `.footer-cta` 板高 490，稿 479 — **P2（跨页）**

**位置** `assets/scss/modules/_footer-cta.scss`（三页共用）
**断点** 1440
**判据** 节点 `I324:72927;313:9707`（Footer CTA h=479，内 Frame 992505 h=287）；DOM `div.footer-cta` h=490 / `__inner` h=298

拆开看：**标题 → 正文 间距 稿 24 → 实现 32（+8）**，弧眉那段再 +3。正文块 `w625 x407.5` vs 稿 `w592 x424`（宽 33）。
1440 三页一致，390 下 470.8 vs 稿 525（另一个方向，−54）——建议一起交给负责 footer-cta 的人。

---

### P1-13 · `.testimonial__name` 与正文间距 — **P2（跨页）**

**位置** `assets/scss/modules/_reviews.scss:189`（`.testimonial { gap: 16px }`）
**判据** 稿 `I324:69755;313:11104;285:27163`（正文 y3245.8 h84）→ `…;27164`（署名 y3337.8）= **gap 8**；DOM 3246.9 → 3346.9 = **gap 16**

稿里 `stars → 正文块` 是 16、`正文 → 署名` 是 8，实现用一个 `gap: 16` 统一了，署名低 8px。两个断点都一样。

---

### P1-14 · 移动端 header 右侧两个图标顺序颠倒 — **P2（跨页 header，请与负责 header 的组核对）**

**位置** `*.html:35-38`（`.header__icons`）
**断点** 390
**判据** 节点 `I324:70525;237:14851;83:5312`：x310.2 = 购物袋、x346.2 = 账户；实现 `aria-label="Account"` 在前、`"Cart"` 在后。放大对照图 `$SP/c_hdr_icons.png`
桌面稿是「账户 → 购物袋」，与实现一致 ✓ —— **只有手机稿是反的**，也可能是设计稿自身不一致，建议一并问。

---

## 2. 字体度量差（AUDIT-HANDOFF 3.4-A，**不算实现偏差**）

现象统一是「同样的字号/行高/字距/容器宽，实现少排一行」，根因是 400 字重指向 `fizzy-light`（比稿窄）。
**这些不要当间距 bug 去改 padding**，等授权字体到位后自然回归。

| 位置 | 稿 | 实现 | 连带影响 |
|---|---|---|---|
| `.expert-card__quote` @1440 | h120（5 行 @24） | h96（4 行） | 卡 570 → 545.8，`section.expert` 882 → 857.8 |
| `.expert-card__quote` @390 | h168（7 行） | h144（6 行） | 卡 524 → 500 |
| `.dosed__lead` 第 1 块 @390 | h144（6 行） | h120（5 行） | 见 P1-8 的 −24 |
| `.story-card__lead` 第 1 张 @1440 | 5 行 | 4 行 | 卡组等高，`section.story` 仍 729.8 = 稿 730 ✓ |
| 各处居中文本 `dx` 差（如 `h2.reviews__title` dx +476.5、`testimonial__name` dx +169.3） | — | — | **配对噪声**：稿是满宽 CENTER 文本框，DOM 是 shrink-to-fit；两边**几何中心一致**（720 / 285），不是偏移 |

---

## 3. 已列的「有意为之 / 待裁决」— 逐条确认

### 3.1 确认成立，不是 bug

| 条目 | 核对结论 |
|---|---|
| **Reviews 整页评论列表 = app 边界**（3.4-E） | ✓ `fig_only` 里 y1809–3699（390）/ y2036–3756（1440）共 **50 条**全部是评论卡内容：`4.76`、`Based on 123,000 reviews`、5 位买家（Arianna F / James B / Maya L / Robert S / Emma C）、`Verified Buyer`、时间戳、点赞点踩计数、`See More Reviews`。**边界之外没有漏项。**（对照图 `c_rev1440_hdr.png`） |
| **PDP 订阅选购 = app 边界** | ✓ 三页 `fig_only` 里 `Autoship and Save` / `Subscribe & Save` / `$40.40` / `$1.46/day` / `Delivers every:` 等 19–20 条全在 app slot 范围内 |
| **Grüns 竞品名占位** | ✓ **注释在、文案未被改写**。`reviews.html:124-127` 的三行注释完整（含「must be replaced before launch」），三张卡的引用文案 `reviews.html:139/149/159` 与稿 `I324:64024;324:37021` 逐字一致 |
| **`Text here` / `Accordion Closed` / `Heading` / `Consectetur adipiscing…`** | ✓ 稿里就是占位，`dom_only` 里这 21–38 条全部对得上设计源，**没有自造内容** |
| **HGW 副标两稿冲突裁决** | ✓ 1440 用 `The science, the daily ritual, the transformation.` + `#1a1a1a`/20/30（桌面稿的字色字号）；390 用同一句 + `#dd655e`/18/26（手机稿）。**与裁决完全一致，不重复报**（`c_hgw1440_hero.png` / `c_hgw390_hero.png`） |
| **CTA 扇贝板 mask 低于 1280 弧压扁** | ✓ 已知取舍，不报。**1440 复测：板 1280 × 392（稿 393），弧起伏与稿一致 —— 上一轮结论仍成立** |
| **Trustpilot 徽章为文字占位** | ✓ 稿的公告条有五角星，实现只有文字，属 3.4-E 第三方嵌入 |
| **`app-slot` / `product__app-slot` 只留壳** | ✓ 结构占位符合边界约定；⚠ 目前渲染成一个带边框+说明文字的灰框，**上线前必须由 app 输出替换**，不能就这样发布 |

### 3.2 ⚠ 新发现的桌面 / 手机稿冲突 —— **不在 3.4-C 的四条里，需设计方裁决**

实现一律取了桌面版，没有自造内容，但**没有人记录过这四处**：

| # | 位置 | 桌面稿 | 手机稿 | 实现 | 判据 |
|---|---|---|---|---|---|
| **A** | `.reviews` 测评卡数量 | **3 张**（`I324:69755;313:11104/05/06`） | **4 张**（`I324:70586;187:12732/33/34/35`，四张文案完全相同） | 3 张 | HGW / Our Story 两页 390 的 `fig_only` 各多出一组 `10/10 would recommend…` + `Dustin O.` |
| **B** | FAQ 区标题 | `And Last Questions?` 40/48 | **`FAQ's`** 24/30（`I324:65045;237:15921` / HGW 同款） | `And Last Questions?` | ⚠ **PDP 的手机稿却是 `And Last Questions?`** —— 是设计稿自己不一致，不是实现问题 |
| **C** | 页脚链接组 | 三组带标题（Why Gumi / Learn more / Get in touch），12 条，`Shop` / `Partners & Influencers` | **两列无分组标题**，13 条，`Homepage` / `PDP` / `Influencers` / 多一条 `Shipping` | 桌面版结构 | `fig_reviews_390.json` y8669–8861 vs `dom_*_390` |
| **D** | `.product` 手机稿的两处色 | `Tastes Like` 三个 `Heading` = `#011307`；`Batch Tested Quality` = `#4d4d4d` | **`#ff3b30` / `#ff2d55`**（iOS 系统红/粉，四个手机画板 + PDP 手机稿全都一样，实例 id 相同 `191:2483/2487/2491`、`191:3838`） | 桌面色 | `fig_*_390.json` 色值扫描 |

D 看着像设计师从某个 UI kit 带进来的默认色（同一组件实例在 5 个画板里一致），**倾向于占位而非设计意图**，但按铁律 2 不该由我们替他决定 —— 建议随 A/B/C 一起发问。

---

## 4. 需设计方给值 / 需确认

1. **手机端专家卡轮播的箭头是否保留**（P1-5）。稿给了几何（32×32、距卡片组 48），要么做，要么书面确认省略。
2. **reviews@390 专家卡轮播的初始位置**：稿画的是「第 2 张居中、左右各露一截」（卡 1 在 x−278.5），
   实现是第 1 张贴左。稿这个位置**很可能只是设计师拖动画板演示轮播效果**，不是首屏状态 —— 需一句确认。
3. **Our Story 390 的 CTA 板 507.5 高里那段大留白**是不是有意（P1-1）。
4. **HGW 390 标题的手动换行**是刻意断行还是画板副产物（P1-9）。
5. **`app-slot` 占位框的最终形态** —— 现在是灰框 + 中文/英文说明，交付前要么由 app 顶掉，要么改成无痕占位。
6. 交互态（hover / active / focus）稿里依旧完全没有，本轮未审（属交互态清点那条独立工作）。

---

## 5. 跨页系统性偏差 —— 确认成立

主会话统一写的那几条，在我这三页上**全部成立**，逐条复核结果：

| 条目 | 我的页面上的验证 |
|---|---|
| 页脚链接与版权行 稿 14/20 → 实现 16/24 | ✓ 成立，**且只发生在 390**（1440 稿本来就是 16/24，实现一致）。`p.footer__label` 14/20/−0.28 是对的，错的只有 `a.footer__link` 与版权行 |
| 多处 `letter-spacing` 实现恒 −0.32 | ✓ 成立：header `Shop now` 稿 0、`.testimonial__text`@390 稿 0、ingredients `Shop Now`@390 稿 +0.48，实现全是 −0.32 |
| 按钮 390：稿 16px + 字距 +0.48 → 实现 18px + 0 | ✓ 成立（`button.product__label-btn`、`button.product__cta`） |
| `p.testimonial__text` 字距 | ✓ 成立（三页 390 各 3 条） |
| `.reviews__disclaimer` 12/18 → 14/22 | ✓ 成立（HGW / Our Story @390；行数仍是 3 行，只是盒高 54 → 66） |
| `span '4.8 stars'` 12/18 → 14/22 | ✓ 成立（HGW / Our Story @390） |

**另外两条不是偏差，别跟着改**：

- `cmp_*.json` 里 `a.btn` / `button` / `summary.*` 的 `dy≈−14/−16`、`dx≈−37/−64/−138/−158` —— 稿量的是**文字**盒、DOM 量的是**按钮**盒，差的就是内边距。实测 header CTA：稿 `I336:25127;332:24069` 60/x1096/160×40，DOM 60/x1099.1/156.9×40，**完全对齐**。
- `strong 'Less than 1%'` 深色 —— 稿 `I324:64031;316:18275` 的 `characterStyleOverrides` 前 12 字确实覆盖成 `#011307`（字重仍 400），实现 weight 400 + `#011307`，**完全正确**。这条做对了。

---

## 6. 配对噪声清单（`cmp_*.json` 里看着像 bug 的，逐条排除）

| 现象 | 真相 |
|---|---|
| `h2.ingredients__title 'Heading'` size 16↔32、weight 400↔800 | **配对失败**。一页有 4 个 `Heading`（3 个 16/400 的口味标签 + 1 个 32/800 的标题），按相对位置配错了。逐个查节点，实现 4 处**全部精确匹配**（1440：16/400/24/−0.32 ×3 + 32/800/40/−0.32；390：… + 24/800/30/−0.24） |
| `gumi.com.au` 出现在 `fig_only` | 画板顶部的浏览器窗口模拟（desktop `toolbar` h59.6 / mobile `Chrome browser` h96），不是页面内容。⚠ 顺带一提：手机画板里写的是 **`funkyfood.com.au`**（设计师从上个项目复制的），与内容无关 |
| `Enter your email` 出现在 `fig_only` | `dom_text.py` 只走文本节点，读不到 `<input placeholder>`。已核对 `reviews.html:416` 有 `placeholder="Enter your email"` ✓ **探针盲区，不是漏做** |
| `Whole Fruits` / `Super Mushrooms` / `Adaptogens` 等 6 条出现在 `fig_only` | 已烤进 `images/promo-art.png`，`alt` 里逐条列出（`reviews.html:305-307`）。⚠ 但这是**图片里的文字**，将来多语言/SEO 会吃亏，建议登记为技术债（P2，不是还原度问题） |
| 390 下 `x` 为负（−370 / −354 / −173）的 header 条目 | 屏外抽屉菜单，`display` 未隐藏所以被探针抓到 |
| `Real Customer Reviews` dx +136.7 | shrink-to-fit，稿 x352 w736 CENTER 与 DOM x488.7 w462.6 的**中心都是 720** |
| reviews@390 `section.ingredients` 672 vs 稿 680（−8） | 低于噪声阈值，未追 |

---

## 7. 总表：页面 × 区块 × 断点 × 结论

图例：✅ 与稿一致（±2px 内）｜🟡 小偏差（P2）｜🔴 明显偏差（P1）｜🅰️ app 边界，只做壳｜🔤 字体度量差

| 页面 | 区块 | 1440 | 390 | 说明 |
|---|---|---|---|---|
| **Reviews** | 公告条 + header | ✅ | 🟡 | 图标顺序（P1-14，跨页） |
| | 页头 page-hero | ✅ 574=574 | ✅ 561=561 | |
| | 专家卡区 | 🔤 857.8 / 稿 882 | 🔴 748 / 稿 852 | 1440 差全在引用少一行；390 另缺箭头（P1-5） |
| | 评分汇总 + 评论列表壳 | 🅰️ | 🅰️ | 50 条 `fig_only` 全在边界内，边界外无漏项 |
| | PDP 复用块 | 🟡 | 🟡 | 手风琴行距（P1-7）、Packed With 居中（P1-4）；390 另有三处 token（P1-10） |
| | 成分盘 ingredients | ✅ 688=688 | 🟡 672/680 + 正文色（P1-11） | 标签文字烤进 PNG（见 §6） |
| | FAQ | ✅ 710=710 | ✅ 559=559 | 前面的间隔条 +32（P1-6）；390 标题两稿冲突（§3.2-B） |
| | 页脚 CTA + 页脚 | 🟡 490/479 | 🟡 | 页脚字号与结构见 §5 / §3.2-C |
| **How Gumi Works** | 页头（含副标裁决） | ✅ 294=294 | 🟡 204/244（P1-9） | 裁决落实正确，不重复报 |
| | 步骤 / 图文块 dosed | ✅ **1484=1484** | 🔴 1541.5/1634（P1-8） | 桌面一分不差 |
| | 测评区 reviews | 🔴 1382/1444.2（P1-3） | 🔴 1851/1791.6（P1-2 + 卡数 §3.2-A） | |
| | PDP 复用块 | 🟡 | 🟡 | 同上 |
| | FAQ | ✅ 710=710 | ✅ 559=559 | 前面间隔条 +32（P1-6）；390 标题冲突 |
| | 页脚 CTA + 页脚 | 🟡 | 🟡 | |
| **Our Story** | 页头 | ✅ 304=304 | ✅ 256=256 | |
| | 三张图文卡 story | ✅ **729.8/730** | ✅ **1538=1538** | 两档都是本次最干净的区块 |
| | 扇贝 CTA 板 | ✅ 1280×392/393 | 🔴 288.3/507.5（P1-1） | 桌面复测通过 |
| | `.reviews` 复用块 | 🔴（P1-3） | 🔴（P1-2 + §3.2-A） | |
| | `.product` 复用块 | 🟡 | 🟡 | |
| | 页脚 CTA + 页脚 | 🟡 | 🟡 | |

**桌面（1440）结论**：三页骨架高度对稿几乎逐像素吻合（story 729.8/730、dosed 1484/1484、faq 710/710、
ingredients 688/688、CTA 板 392/393）。剩下的偏差集中在**共用组件**——`.reviews` 的免责声明宽度与间距、
`.product` 的手风琴行距与 Packed With 对齐、`.footer-cta` 板高、三处 96/128 间隔条。**没有页面级返工项。**

**手机（390）结论**：**明显弱于桌面。** 页头 / 图文卡 / FAQ 这些「照抄手机稿」的区块是准的，
但凡是**靠响应式规则从桌面推下来**的（CTA 板、dosed 间距、product 行高、footer）都偏离了手机稿。
按 memory `feedback_build-both-breakpoints-from-source`：**有响应式 ≠ 按手机稿还原**。
建议下一轮以「390 逐区块回查手机稿节点」为主线，先修 P1-1 / P1-2 两条。

**自造内容**：**没有。** 三页所有 `dom_only` 条目（含 header 巨幕菜单的 `Shop Gumi` / `Refer a Friend` /
`Earn rewards and $20 for every referral.` / `Manage Account`）都在 `283-14915_nav-expanded.json` 与
`283-15014_nav-collapsed.json` 里逐条查到出处；`Text here` / `Accordion Closed` / `Heading` /
lorem 段落均为设计稿自带占位；Grüns 文案与注释完好未改。

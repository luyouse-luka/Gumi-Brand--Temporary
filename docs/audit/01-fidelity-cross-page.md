# 还原度审计 — 跨页系统性偏差（主会话）

> 2026-08-20。本文件只写**跨多个页面重复出现**的偏差，单页问题在
> `01-fidelity-a-index.md` / `-b-pdp-science.md` / `-c-reviews-hgw-story.md` / `-d-text-pages.md`。
> 审计只出报告，**未改任何项目文件**。

## 0. 方法与判据

三条并行的判据，缺一条都会得出错误结论：

| 线 | 做法 | 判据 |
|---|---|---|
| 数值 | 从 `figma/nodes/*.json` 提取全部可见 TEXT（含 `characterStyleOverrides` 字符级分段），与 Playwright 实测的 computed style 按**归一化文本**配对 | 字号 >0.6px / 行高 >1px / 字距 >0.06px / 字重不等 / 色值不等 即记一条 |
| 几何 | 从节点树提取 `Button` 实例的 `absoluteBoundingBox` + `layoutSizingHorizontal`，与渲染盒对齐 | HUG 的按钮只比高度（宽度随字体变），FILL/FIXED 的按钮宽高都比 |
| 视觉 | 按**配对到的文字**做锚点，左稿右实现裁同一区块拼图人工看；曲线类（扇贝）用像素扫描量节距/起伏 | 见下方各条 |

脚本（临时目录，不进项目）：
`$SP = /tmp/claude-1007/-home-ly/c7ffb540-53f6-4bbe-87d6-fe452694dbc5/scratchpad`

```bash
python3 $SP/fig_text.py figma/nodes/<node>.json > $SP/fig_<page>_<w>.json   # 稿侧 TEXT + token
python3 $SP/batch_dom.py                                                    # 11 页 × 2 断点的 DOM 实测
python3 $SP/compare2.py $SP/fig_x.json $SP/dom_x.json $SP/cmp_x.json         # 配对 + 差分
python3 $SP/crop_pair.py our-story 390 "Shop Now" 460 $SP/out.png            # 锚点对齐的左右对照图
python3 $SP/btn_all.py                                                       # 全站 110 个按钮实例的稿 vs 实现
```

**先排除的三类噪声**（否则报告全是假阳性）：

1. **字体度量差**：PP Palma 无授权，400 字重现在用 300 的文件（AUDIT-HANDOFF 3.4-A）。
   字宽、换行位置、hug 按钮的宽度都会差，**一律不计入偏差**。本报告里凡是比宽度的地方，
   都只比 Figma 里 `layoutSizingHorizontal = FILL/FIXED` 的盒子。
2. **描边光晕层**：`ink-split()` 会在同一段文字上叠一个 `aria-hidden` 的透明副本，
   探针必须跳过（否则每处描边数字都会报"颜色变成 rgba(0,0,0,0)"）。已在 DOM 提取器里排除。
3. **稿内重复串**：`Superfood Greens Gummies` 这类在一块画板里出现 10 次以上（订阅模块的堆叠层），
   按出现顺序配对会整体错位。改成**按相对页面位置就近配对**后消失。

**实测规模**：11 页 × 2 断点 = 21 组（Shipping 无桌面稿）。稿侧可见 TEXT 1915 条，
渲染侧文本 1969 条，配对成功 1301 对。

---

## 1. 真偏差（可直接修）

### F1 · P1 · 全站 71 处文字被全局字距覆盖，稿里这些位置字距是 0

**位置**：`assets/scss/base/_typography.scss:14`（`body { letter-spacing: -0.32px }`）
与 `:52`（`p { … letter-spacing: -0.32px }`）

字距是继承属性，这两条给全站铺了 -0.32px。稿中**并非所有文字都有负字距** ——
按钮标签、部分说明文字、表格标签在 Figma 里是 `letterSpacing: 0`，个别按钮甚至是 **+0.48**（正字距）。

实测 90 条字距偏差，其中 **71 条是"稿=0，实现=-0.32"**：

| 承接元素 | 条数 | 出现范围 |
|---|---|---|
| `a.btn` | 13 | 10 个页面-断点 |
| `a.footer__link` | 20 | 2 个页面-断点（另见 F2） |
| 裸 `span` | 14 | 6 个页面-断点 |
| `p.testimonial__text` | 9 | 3 个页面-断点 |
| `span.vs__label` | 5 | PDP |
| `p.highlight-card__text` | 3 | Homepage |
| 其余（`form__note` / `product__title` 等） | 7 | — |

另有 19 条是"稿有值但实现给了别的值"，方向也不对：
`.product__label-btn` / `.product__cta` / `.btn` 稿 **+0.48** → 实现 **0 或 -0.32**（共 11 处）；
`h3.highlight-card__title` 稿 -0.24 → 实现 -0.32。

**判据**：`$SP/cmp_*_{1440,390}.json` 的 `diffs[].bad['letter-spacing']`，
`grep -c "letter-spacing" assets/scss/` = 168 处显式声明，但覆盖不到上述元素。

**建议**：`body`/`p` 的字距不是设计 token，是"大多数正文碰巧是 -0.32"的经验值。
按稿把字距落到各组件上（按钮组件本身就该显式写 `letter-spacing: 0` 或 `.48px`），
或者至少给 `.btn` 补一条显式声明——现在按钮的字距是**继承来的意外值**。

---

### F2 · P1 · 手机端页脚整块字号偏大一档（11 页全中）

**位置**：`assets/scss/layout/_footer.scss:254`（`.footer__link`，**没有 `@include mobile` 块**）
+ `assets/scss/base/_typography.scss:52`（全局 `p` 规则压过 `.footer__legal` 的 mobile 值）

| 元素 | 手机稿 | 实现 @390 | 差 |
|---|---|---|---|
| `.footer__link`（10 条链接 × 11 页 = 110 处） | 14px / 20px / ls -0.28 | 16px / 24px / ls -0.32 | +2px 字号、+4px 行高 |
| 版权行 `<p>© 2027 Gumi…` | 14px / 20px | 16px / 24px | 同上 |

两处根因不同，要分开修：

- `.footer__link` 只写了桌面值（16/24/-0.32），**没有 mobile 断点**，390 下继续用桌面值。
- 版权行的 `.footer__legal` **写了** mobile 块（14/20/-0.28，`_footer.scss:310`），
  但里面是 `<p>`，全局 `p { font-size:16px }`（0-0-1 的直接规则）**压过了继承来的 14px**。
  同一个容器里的 `.footer__legal-links a` 没有直接规则，所以它们**正确地**变成了 14/20 ——
  一个容器里两种结果，正是"直接规则 vs 继承"的典型。

**判据**：11 个手机稿里 9 个的页脚链接都是 14/20/400/-0.28（逐稿核对，见 F7 的例外）；
`$SP/cmp_*_390.json` 里 `a.footer__link` 的 size/line-height 偏差各 90 条。

**建议**：`.footer__link` 补 mobile 块；版权行改成 `.footer__legal p` 就地重述，
或把 `.footer__legal` 的 mobile 值写到子元素上。

---

### F3 · P1 · 四个文本页的桌面页头副标沿用了 Reviews 的加大号

**位置**：`assets/scss/layout/_page-hero.scss:115`（`.page-hero__lead--lg`）
+ `faq.html` / `get-in-touch.html` / `referral.html` / `privacy-policy.html` 各自的 hero 段

`--lg` 的注释写着它来自 `324:63924`（Reviews 稿）。但这四页**有自己的桌面稿**，数值不一样：

| 页面 @1440 | 桌面稿 | 实现 | 差 |
|---|---|---|---|
| FAQ | 18 / 24 / **500** / -0.36 / `#333333` | 20 / 30 / 400 / -0.4 / `#1a1a1a` | 4 项全不同 |
| Get in Touch | 18 / 26 / **500** / -0.36 / `#333333` | 同上 | 4 项全不同 |
| Referral | 18 / 26 / **500** / -0.36 / `#333333` | 同上 | 4 项全不同 |
| Privacy Policy | 18 / 26 / **500** / -0.36 / `#333333` | 同上 | 4 项全不同 |
| Reviews（`--lg` 的出处） | 20 / 30 / 400 / -0.4 / `#1a1a1a` | 一致 ✅ | — |
| Science（基类） | 18 / 28 / 400 / -0.36 / `#4d4d4d` | 一致 ✅ | — |

注意这四页的稿是 **weight 500**，而 `--lg` 与基类都是 400 —— 字重这一项**两个变体都没有**。

手机端另有一处：**Privacy @390** 稿是 16/24/`#4d4d4d`，实现 18/26/`#1a1a1a`（`--lg` 的 mobile 值）。

**判据**：`$SP/fig_{faq,get-in-touch,referral,privacy-policy}_1440.json` 里 hero lead 节点的 style
vs `$SP/dom_*_1440.json` 的 computed style（逐页打印比对，见本次会话记录）。

**建议**：这四页不该挂 `--lg`；另需要一个 weight 500 的变体（或在基类上补）。

---

### F4 · P1 · 手机端主 CTA 按钮高一档：52 → 60，字号 16 → 18

**位置**：`assets/scss/modules/_product.scss`（`.product__cta` / `.product__label-btn`）、
`assets/scss/modules/_form.scss`（`Send Message`），**均无 mobile 断点**

| 按钮 | 手机稿 | 实现 @390 | 出现页面 |
|---|---|---|---|
| `View Nutritional Label` | 350×**52**，16px，ls +0.48 | 350×**60**，18px，ls 0 | index / pdp / reviews / how-gumi-works / our-story |
| `Start Now` | 350×**52**，16px，ls +0.48 | 350×**60**，18px，ls 0 | 同上 |
| `Send Message` | 350×**52** | 350×**60** | get-in-touch（referral 稿里无同名按钮） |

桌面端这三个按钮**完全正确**（465×60 / 401×60 / 624×60 三个都与稿逐像素一致），
所以问题只在"手机端没有各自的断点值"。

**判据**：`python3 $SP/btn_all.py` —— 全站 110 个按钮实例，桌面 0 处高度偏差，手机 8 处 `高差+8`。

---

### F5 · P1 · 手机端稿里满宽的按钮，实现按内容宽收缩

**位置**：`assets/scss/modules/_cta-band.scss`（`.cta-band__btn`）、`reviews.html` 的 `.btn--xl`

Figma 在 390 下把这些按钮设成 `layoutSizingHorizontal = FILL`（占满 350 的内容宽），实现是 hug：

| 页面 @390 | 按钮 | 稿 | 实现 | 差 |
|---|---|---|---|---|
| our-story | Shop Now | 274×52 (FILL) | 215×52 | **-59px** |
| faq | Start Your Greens（CTA 板内那个） | 350×52 (FILL) | 276×52 | **-74px** |
| reviews | Shop Now | 350×52 (FILL) | 219×60 | **-131px**（且高度也差 +8，见 F4） |

同一批按钮在**桌面端是 HUG，实现也是 HUG，完全正确** —— 是手机端的 FILL 没做。

**判据**：同 F4 的 `btn_all.py`，以及对照图 `$SP/pair_os_shopnow.png`（肉眼可见白按钮明显偏窄）。

---

### F6 · P1 · Homepage 桌面 hero 的 CTA 只有稿的一半宽

**位置**：`index.html` hero 段的 `Try Gumi` 按钮 / `assets/scss/modules/_hero.scss`

稿：380×60，`layoutSizingHorizontal = **FILL**`（占满 hero 文本列宽），内容居中，padding 64/64。
实现：**204×60**，按内容宽（64 + 文字 76 + 64）。差 **-176px**。

手机端同一按钮是 350×52（FILL），实现 350×52 ✅ —— 只有桌面端错。

**判据**：节点 `Homepage Desktop/Page Hero/Page Header/Frame 427319664/Frame 427319663`，
`layoutSizingHorizontal=FILL`、bbox 380×60；对照图 `$SP/pair_hero_1440.png`（左稿右实现，宽度差肉眼可见）。

---

### F7 · P1 · 手机端 CTA 扇贝板的弧数错了近 3 倍（不是"略微压扁"）

**位置**：`assets/scss/helpers/_masks.scss` 的 `$mask-scallop-band` + `assets/scss/modules/_cta-band.scss`

AUDIT-HANDOFF 4.4 第 3 条把这条记成"低于 1280 宽时弧会略微压扁"。实测**不是压扁，是弧数不变**：
位图 mask 是从 1280 宽的画板抠的，横向拉伸到 390 后，14 个弧被压成 24.5px 一个的锯齿，
而手机稿画的是 **5 个 68px 的大弧**。

| 断点 | 稿 | 实现 | 结论 |
|---|---|---|---|
| our-story @1440 | 14 弧 / 节距 89.5px / 起伏 56px | 14 弧 / 节距 89.4px / 起伏 52px | ✅ 一致 |
| our-story @390 | **5 弧 / 节距 68px** / 起伏 37px | **14 弧 / 节距 24.5px** / 起伏 38px | ❌ 弧数差 2.8 倍 |

扇贝是这个品牌的标志性图形，390 下变成锯齿属于视觉识别层面的偏差，不只是几何误差。
faq / our-story 两页的 `.cta-band` 共用同一个 mask，都中。

**判据**：像素扫描底缘曲线（本次会话的 `arcs()` 探针）——
对每个 x 找 `#005635` 的最后一行，取局部极值算节距；两侧起伏都是 37-38px，**只有节距不同**，
排除"裁切窗口没对齐"这种解释。对照图 `$SP/pair_os_shopnow.png` 肉眼同样可见。

**建议**：手机断点换一张按手机稿抠的 mask（或把 `mask-size` 改成按节距重复而非 `100%`），
和 `.scallop` 那套 `r = 0.6407d` 的推导保持一致。

---

## 2. 需设计方裁决

### F8 · P2 · 设计源自己不一致：两个手机稿的页脚是另一套字号

11 个手机稿里 **9 个**的页脚链接是 `14/20/400/ls -0.28`，但

- `326:83399` Privacy Policy @390
- `326:83129` Shipping @390

这两个稿是 `16/24/**600**/ls 0`。这两页也正是最后画的两页。
修 F2 时要先定"以哪一版为准"，否则改完这两页反而更远。

**判据**：逐稿打印页脚 `Our Story` / `FAQs` 节点样式（本次会话记录），9:2。

### F9 · P2 · 稿里 20 处红色文字是设计师的占位标记，不是品牌色 —— 需设计方确认

手机稿里有 20 处文字用了 `#ff3b30` / `#ff2d55`（iOS 系统红/粉），**不在品牌色板里**
（品牌色只有 `#B5ED61` / `#005635` / `#011307` / `#FAF9F8` 四支）。它们全部落在占位内容上：

| 稿色 | 处数 | 文字 | 出现页面（均为 390） |
|---|---|---|---|
| `#ff3b30` | 15 | `Heading`（营养卡的占位标题） | index / pdp / reviews / how-gumi-works / our-story |
| `#ff2d55` | 5 | `Batch Tested Quality`（退款保证条第三项） | 同上 |

实现把它们按同排兄弟元素的颜色渲染（`#011307` / `#4d4d4d`）。
从对照图看（`$SP/pair_guarantee.png`），同一排的另两项在稿里是灰色，只有第三项是粉红 ——
**判断是设计师标"这条还没定"的记号**，而不是要求上线时显示红色。现在的处理（按兄弟元素渲染）是对的，
但需要设计方确认，否则可能漏掉他们想标出的问题。

另有两处色值偏差同样出自 F8 的两个"异类"稿：`p.footer__label`（Stay up to date）
在 `326:83399` / `326:83129` 里是 `#ffffff`，其余 9 稿是 `#daf6b0`，实现取的是多数版。

---

### F10 · P2 · Inter / Lexend / Playpen Sans 在交付范围内根本不是页面字体

`assets/scss/base/_fonts.scss` 为 Inter（158/168 行）、Lexend（180/190）、Playpen Sans（203/213）
各写了 2 条 `@font-face`，**但全站没有任何选择器用到它们** —— `grep "font-family" assets/scss/`
里这三族的出现次数各为 2，正好就是 `@font-face` 自己那两条。全站文字一律走 `$font-brand-stack`
（PP Palma → Figtree → 系统无衬线）。

扫过 42 个 frame 的全部 TEXT（含 `styleOverrideTable` 的字符级覆盖）后，答案是**它们本来就不该被用**：

| 族 | 节点数 | 实际出现在哪 |
|---|---|---|
| PP Palma | 2716 | 页面内容，全部 |
| Lexend | 80 | **只在 `285:18988` 那块弹窗稿里**，内容是 `Canned 🥫` / `Diced Tomatoes` / `$1.50` —— 生鲜购物 App 的参考截图，不是 Gumi 的内容 |
| Inter | 58 | **全部是 `gumi.com.au`** —— 稿顶部那个浏览器地址栏模拟 |
| Playpen Sans | 0 | 42 个 frame 里一次都没出现 |

也就是说交付范围内**没有一处**需要这三族。`docs/DESIGN-TOKENS.md` 记的
「Inter 409 / Lexend 108 / Playpen Sans 90」是全文件口径（含非交付页与 UI 模拟），
拿它当"要装 4 个字体族"的依据会误导下一轮。

**影响**：浏览器不会下载未被使用的 `@font-face`，所以**不影响性能**（性能线实测这几个族 0 字节，
互为印证）。这是**代码卫生**问题：6 条死的 `@font-face` + 磁盘上 6 个不会被用到的 woff2。

**建议**：把这三族的 `@font-face` 连同 `docs/DESIGN-TOKENS.md` 的字体表一起更正，
避免下一轮"补齐字重"时又去下载它们。⚠ 别顺手删 `assets/fonts/` 里的 PP Palma 备件
（`$pp-400-src` 的候选，AUDIT-HANDOFF 6.3 有说明）。

### F11 · P2 · 手机端 header 右侧两个图标顺序颠倒（11 页全中）

由 C 组（Reviews/HGW/Our Story）报上来，主会话已独立复核成立：

| 断点 | 稿 | 实现 |
|---|---|---|
| 1440 | 人像 → 购物袋 | 人像 → 购物袋 ✅ |
| 390 | **购物袋 → 人像** | 人像 → 购物袋 ❌ |

手机稿把购物袋放在左边、人像放右边，与桌面相反；实现两个断点用了同一份顺序。
header 是全站共用 partial，11 页都中。

**判据**：对照图 `$SP/pair_header_390.png`（上稿下实现，图标顺序肉眼可辨）；
桌面对照图 `$SP/pair_header.png` 显示 1440 下顺序是对的，所以不是"稿看错了"。

### F12 · P1 · 白底页面在页脚 CTA 之前多出一条薄荷色带（`.scallop--to-lime`）

由 D 组（五个文本页）报上来，主会话已独立复核成立。

`.scallop--to-lime` 的 `--wave-bg` 用了薄荷绿 `#e7f8d0`。在 Homepage 这类**上方本来就是 `#e7f8d0`** 的
页面上看不出来；但在**上方是纯白**的页面（FAQ / Get in Touch / Referral / Privacy / Shipping / Reviews 等）
上，白区与 lime 页脚 CTA 之间就插进一条满宽的薄荷色带。

**判据**（FAQ @1440，x=60 竖切）：

| | 稿 | 实现 |
|---|---|---|
| 分隔条上方 | `#ffffff` 一直到 y=1713 | `#ffffff` 到 y=1748 |
| 分隔条 | 直接过渡到 `#b5ed61`（1px 抗锯齿 `#dff7ba`） | **`#e7f8d0` 约 9px**，再到 `#b5ed61` |
| 横向分布 | 该行取样 25 处白 + 7 处 lime | 该行取样 **24 处 `#e7f8d0`** + 7 处 lime |

几何（弧形）是对的，**只有颜色错**。修的时候注意：Homepage 上这条带是"正确的"（上方本就是薄荷绿），
所以要按上方区块的底色给 `--wave-bg`，不能全局改成白。

---

### 方法边界：查过但没有结论的维度

**文本对齐**：把 Figma TEXT 的 `textAlignHorizontal` 与 computed `text-align` 比了一遍，
96 处不一致 **全是假阳性** —— Figma 里按钮/标签的文字节点自己写着 `LEFT` 或 `RIGHT`，
但它们的父级 auto-layout 用 `primaryAxisAlignItems: CENTER` 把内容居中了，
文字节点的 align 在 hug 盒子里根本不生效。要审对齐得看父帧的 auto-layout 属性，不能看 TEXT 节点。
本轮据此**不出对齐类结论**（唯一存疑的 `h2.ingredients__title` 留给 Reviews 那组单独判）。

---

## 3. 验证通过（明确不是问题，避免下一轮重复查）

| 项 | 判据 | 结论 |
|---|---|---|
| Header（Menu / logo / Shop now / 账户 · 购物车图标 / 公告条） | 对照图 `$SP/pair_header.png`；公告条 稿 40/32 vs 实现 40/32，导航 稿 80/64 vs 实现 81/65 | ✅ 一致（±1px） |
| Trustpilot 五星图标缺失 | AUDIT-HANDOFF 3.4-E，第三方嵌入 | 有意为之 |
| 桌面端按钮几何 | `btn_all.py`：110 个实例中桌面端 0 处高度偏差；FILL 类宽度逐像素一致（465/401/624/411/347） | ✅ 一致 |
| Homepage hero 下方那条扇贝波（`.scallop`，非 `--lg`） | 边界曲线逐点采样，去掉 -59px 的整体位移后偏差 3~8px（振幅 >100px） | ✅ 一致 |
| ⚠ 但 `.scallop--lg` 的**弧向是反的** | A 组发现，主会话独立复核：稿的 lime 上缘 935 列落在上半、317 列落在下半（大圆弧向上鼓，上/下=2.95），实现是 462:978（上/下=0.47，只剩向上的尖角）。**半径/节距/高度本身都对，只有凹凸反了** | ❌ 见 `01-fidelity-a-index.md` |
| 桌面端 CTA 扇贝板 | 节距 89.4 vs 89.5 | ✅ 一致 |
| `Manage Account` 按钮 | 曾疑为自造（MVP 明确不含 account 区块）。实为稿中就有：`283:14915` / `283:15014` / `401:31721` 三个导航稿都画了 | ✅ 非自造 |
| 桌面端 header 导航链接 16/24/500/`#005635` | 与 `401:31721` 一致；早期比对里的"字重 400/颜色 #f4fce7"是与页面稿里隐藏的展开层错配 | ✅ 一致（假阳性） |
| 5 个重名 desktop 稿的归属 | 按归属配对后，FAQ 40/42、Privacy 42/48、Get in Touch 39/47、Referral 38/45 条文本可配 | ✅ 归属正确 |

---

## 4. 基线数字（截至 r15，供下一轮对照）

| 指标 | 值 |
|---|---|
| 稿侧可见 TEXT / 渲染侧文本 / 成功配对 | 1915 / 1969 / 1301 |
| token 偏差合计（21 组） | **桌面 38 条，手机 223 条** |
| 其中字距 | 90 条（71 条是稿=0 被全局 -0.32 覆盖） |
| 按钮实例（稿↔实现可配） | 110，其中偏差 15（全部在 390） |
| 手机端偏差是桌面端的 | **5.9 倍** |

**手机端偏差密度是桌面端的 5.9 倍**，且集中在"某个模块只写了桌面值、没写 mobile 块"这一种形态
（F2 / F4 / F5 全是）。这与 `feedback_build-both-breakpoints-from-source` 记的模式一致：
两端要各取各的稿，不能等比缩。建议下一轮修完后，把
"每个 `@include mobile` 块里的字号集合 vs 手机稿字号集合"做成回归判据。

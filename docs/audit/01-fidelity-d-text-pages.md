# 还原度审计 · D 组：FAQ / Get in Touch / Referral / Privacy Policy / Shipping

> 审计会话产出，**只出报告，未改任何项目文件**。
> 断点：前四页 1440 + 390；**Shipping 只有手机稿（390）**，1440 只审「有没有坏」。
> 判据纪律见 `docs/AUDIT-HANDOFF.md` 第 7 节；免报清单见 3.4。**未调用任何 Figma API。**

---

## 0. 方法：跑了什么、看了什么

### 0.1 数值比对（主会话已建好的工具）

```bash
SP=/tmp/claude-1007/-home-ly/c7ffb540-53f6-4bbe-87d6-fe452694dbc5/scratchpad
python3 $SP/show.py faq 1440           # 逐页逐断点打印 diffs / fig_only / dom_only / jump / xOff
python3 $SP/show.py faq 390
python3 $SP/show.py get-in-touch 1440 ; python3 $SP/show.py get-in-touch 390
python3 $SP/show.py referral 1440     ; python3 $SP/show.py referral 390
python3 $SP/show.py privacy-policy 1440 ; python3 $SP/show.py privacy-policy 390
python3 $SP/show.py shipping 390
```

（`show.py` 是本次为读 `cmp_*.json` 写的打印器，落在 `$SP`，不进项目。）

### 0.2 稿全文（长文案唯一可信来源）

```bash
python3 figma/dump-text.py 324-75766_our-story-desktop     # FAQ 1440
python3 figma/dump-text.py 324-76169_faq                   # FAQ 390
python3 figma/dump-text.py 326-79979_our-story-desktop     # Get in Touch 1440
python3 figma/dump-text.py 326-80318_get-in-touch          # Get in Touch 390
python3 figma/dump-text.py 326-81218_our-story-desktop     # Referral 1440
python3 figma/dump-text.py 326-81540_referral              # Referral 390
python3 figma/dump-text.py 326-82363_our-story-desktop     # Privacy 1440
python3 figma/dump-text.py 326-83399_privacy-policy        # Privacy 390
python3 figma/dump-text.py 326-83129_shipping              # Shipping 390
```

另写了两段一次性脚本做**逐词 diff**（`difflib.SequenceMatcher` 比 Figma TEXT 全文 vs HTML 正文），
以及从 `figma/nodes/*.json` 直接读**节点几何**（padding / itemSpacing / 描边 / 填充 / 圆角）与
`characterStyleOverrides`（下划线段落归属）。

### 0.3 对照图（左稿右实现）

| 文件 | 内容 |
|---|---|
| `$SP/d_faq1440_hero.png` | FAQ 桌面 页头 + 扇贝分隔 + 手风琴首行 |
| `$SP/d_faq1440_cta.png` | FAQ 桌面 CTA 扇贝板 |
| `$SP/d_faq1440_ftcta.png` | FAQ 桌面 footer-CTA |
| `$SP/d_faq390_hero.png` | FAQ 手机 页头 + 手风琴全表 |
| `$SP/d_faq390_cta.png` | FAQ 手机 CTA 板（**关键**） |
| `$SP/d_git1440_form.png` / `d_git390_form.png` | Get in Touch 表单 |
| `$SP/d_ref1440_note.png` / `d_ref390_note.png` | Referral 提交按钮 + 说明行 |
| `$SP/d_priv1440_hero.png` / `d_priv1440_a.png` | Privacy 页头 / 正文 |
| `$SP/d_ship390_hero.png` / `d_ship390_t1.png` / `d_ship390_t2.png` | Shipping 页头 / 两张费率表 |
| `$SP/d_ship1440_table.png` | Shipping 桌面（只看有没有坏） |

### 0.4 两条「读数前必须知道」的基线（否则会大面积误报）

1. **Figma 板子顶部有一条假浏览器外壳**（Safari 地址栏，`toolbar` 节点）：
   **桌面稿 59.6px、手机稿 96px**。所以 `cmp_*.json` 里 `dy ≈ -59.6`（桌面）/ `-96`（手机）
   是「完全对齐」，不是偏差。本报告所有 y 都已折算成 **板内坐标 = 稿 y − 外壳高**。
2. **闭合 `<details>` 的正文仍能被探针量到**（Chrome 的 `content-visibility:hidden` 仍给
   非零 rect）。FAQ 各页 `dom_only` 里那 5~6 条 `p.acc-body__text 'Text here'`
   **全是探针噪声，不是页面上真的多出来的文字**。

---

## ① 真偏差

### P1-1 桌面页头内边距用错板：80/96 应为 64/72
- **位置**：`assets/scss/layout/_page-hero.scss:140` `.page-hero--center { padding: 80px 0 96px }`
- **页面/断点**：FAQ / Get in Touch / Referral / Privacy Policy，**仅 1440**
- **稿值 vs 实现**：四块板的 `Page Header` 帧一致为 `paddingTop 64 / paddingBottom 72`
  （帧高 248~250）；实现 80/96（帧高 294）。
- **判据**：节点 `Page Header`（`324-75766` / `326-79979` / `326-81218` / `326-82363`）
  的 `paddingTop|paddingBottom`；实测 FAQ 桌面 h1 板内 y 稿 184 / 实现 201。
  ⚠ **80/96 是 How Gumi Works 那块板的值**（`324-69636` 的 Page Header 就是 80/96、帧高 294），
  这个类被复用到了四个文本页。
- **建议**：不要直接改 `.page-hero--center` 基类（会打坏 how-gumi-works），
  加一个文本页专用修饰或在 `--center` 里按页作用域覆盖为 `64px 0 72px`（手机 32/64 是对的，别动）。
- **P1**

### P1-2 页头下方的扇贝分隔条大了一档（桌面）
- **位置**：`faq.html:112` / `get-in-touch.html:112` / `referral.html:112`
  `<div class="scallop scallop--lg scallop--to-white">`；
  规则在 `assets/scss/components/_scallop.scss:65` `.scallop--lg`
- **页面/断点**：FAQ / Get in Touch / Referral，**仅 1440**
- **稿值 vs 实现**：
  | | 稿 | 实现 |
  |---|---|---|
  | 条带高 | **96px**（`Spacer Desktop` 节点 h=96） | 128px |
  | 弧节距 | **302.19px**（白色尖角在 x=259/561/863/1166，实测差 302） | 524.74px（尖角 x=457/982） |
  | 实测白色首现深度 | +26.4（=`band` 23.4，与 lg 公式吻合） | +2 |
- **判据**：`figma/screenshots/324-75766_...png` 与 `tools/shots/faq-1440.png` **同深度扫行**：
  深度 30 稿有 4 个白尖角（262-272 / 564-574 / 866-876 / 1168-1178），实现只有 2 个（431-485 / 955-1009）。
  节点侧：`Spacer Desktop` y=427.6 h=96（FAQ）、429.6 h=96（其余三页）。
  对照图 `$SP/d_faq1440_hero.png`、`$SP/d_priv1440_hero.png`。
- **成因**：`.scallop--lg` 的 `--wave-w: clamp(144.64px, 36.44vw, 524.74px)` / `--wave-band ≈ 2px`
  这一组同样来自 **How Gumi Works**（那块板的 `Spacer Desktop` 正是 128）。四个文本页要的是
  「**lg 的朝向（弧向下）＋ 小号瓦片**」：`--wave-w: 302.19px` + `--wave-band: 23.4px` → 高 96。
  现有类里没有这个组合（`.scallop` 是小瓦片但朝向相反、`.scallop--lg` 是对的朝向但大瓦片）。
- **备注**：390 下两者都被 clamp 压到 144.64 / 高 35，**手机端实测 34 vs 稿 36，是对的**，只有桌面错。
- **P1**

### P1-3 Privacy / Shipping 完全没有这条分隔条
- **位置**：`privacy-policy.html:112`（`</section>` 之后直接是 `<section class="rich-page">`）、
  `shipping.html:112`。HTML 注释写着「The board runs the header straight into the body with no
  divider」——**与稿不符**。
- **页面/断点**：Privacy Policy（1440 + 390）、Shipping（390；1440 无稿）
- **稿值 vs 实现**：稿有 `Spacer Desktop` y=429.6 **h=96**（Privacy 1440）、
  `Spacer Bottom` **h=36**（Privacy 390 y=368 / Shipping 390 y=328）；实现是硬边（高 0）。
- **判据**：像素扫描 —— `PRIV-fig-1440` 白色首现 454 / 全白 526（h=72 弧段，条带 96）；
  `PRIV-dom-1440` first=full=415（**h=0**）。`PRIV-fig-390` 369→404（35）vs `PRIV-dom-390` h=0；
  `SHIP-fig-390` 329→364（35）vs `SHIP-dom-390` h=0。
  对照图 `$SP/d_priv1440_hero.png`、`$SP/d_ship390_hero.png` 里稿的扇贝边一眼可见。
- **建议**：两页补上同一条分隔条（几何同 P1-2 修好后的值）。
- **P1**

### P1-4 `page-hero__lead--lg` 桌面 token 整组不是这四块板的值
- **位置**：`assets/scss/layout/_page-hero.scss:115`
- **页面/断点**：FAQ / Get in Touch / Referral / Privacy，**1440**（Privacy 手机另见 P2-18）
- **稿值 vs 实现**：

  | 页面 | 稿（桌面） | 实现（桌面） |
  |---|---|---|
  | FAQ | 18px / **500** / lh **24** / ls -0.36 / **#333333** | 20px / 400 / lh 30 / ls -0.4 / #1a1a1a |
  | Get in Touch | 18 / **500** / lh 26 / -0.36 / **#333333** | 同上 |
  | Referral | 18 / **500** / lh 26 / -0.36 / **#333333** | 同上 |
  | Privacy | 18 / **500** / lh 26 / -0.36 / **#333333** | 同上 |
- **判据**：`cmp_faq_1440.json → diffs[1]`、`cmp_get-in-touch_1440.json → diffs[1]`、
  `cmp_referral_1440.json → diffs[1]`、`cmp_privacy-policy_1440.json → diffs[1]`
  （四条一模一样：size 18→20 / weight 500→400 / line-height 24|26→30 / color #333333→#1a1a1a）。
- **⚠ 修的时候注意**：`20/30/-0.4/#1a1a1a` **正是 How Gumi Works 桌面稿的值**
  （`fig_how-gumi-works_1440` y=348：20/400/30/-0.4/#1a1a1a），`reviews.html` 也在用这个类。
  **不能直接改基类**，要么给文本页单独一个修饰，要么让 `--lg` 留给 hgw/reviews。
- **字重 500 不是字体度量问题**：试用包的 500 是真件（fizzy-medium），现在渲染成 400（=300 那个文件），
  肉眼可见淡一档。
- **P1**

### P1-5 Privacy Policy 正文首段被整段替换成 "Subheading"
- **位置**：`privacy-policy.html:118` `<p>Subheading</p>`
- **页面/断点**：**1440 + 390 都是**
- **现象**：稿在正文最开头有一段 568 字符的 lorem（`'Mi tincidunt elit, id quisque ligula ac diam,
  amet. …'`，桌面 18/28/#808080、手机 16/24/#808080，两个自然段），实现把它换成了一个词
  `Subheading` —— 而 `Subheading` 在稿里**只出现在页头副标**（`page-hero__lead`），
  实现等于**漏了一整段 + 把页头文案重复进了正文**。
- **判据**：对全文做逐词 diff，**整页唯一的差异就是这一处**（桌面：fig 4162 字符 / dom 3594 字符，
  一条 `replace`；手机：fig 634 词 / dom 544 词，同一条）。
  节点：`326-82363` TEXT y=621.6（板内 562）、`326-83399` TEXT y=468（板内 372）。
  版面证据：稿 h2「What information do we collect?」板内 y=772（手机），实现 411，差 -361 ≈ 缺失段落高度。
- **铁律 3 判定**：稿自带 lorem 占位 → **原样保留**才对，现在是「改写了占位」。
- **建议**：把该段（两个自然段）按稿补回，`<p>Subheading</p>` 删掉。
- **P1**

### P1-6 Shipping 两张费率表的样式与稿差得很远
- **位置**：`assets/scss/modules/_rich-text.scss:71` `.rich-table`；标记 `shipping.html:128-160`
- **页面/断点**：Shipping 390（1440 无稿，但同一套样式）
- **稿值 vs 实现**（节点 `326-83129 → FRAME 'Table'`，逐格读到）：

  | 项 | 稿 | 实现 |
  |---|---|---|
  | 单元格描边 | **每格 `#cccccc` 0.5px（整张网格：外框 + 竖线 + 横线）** | 只有 `border-bottom: 1px solid rgba(1,19,7,.05)`（5% 不透明度，几乎看不见） |
  | 表头底色 | **`#f3f3f3`** | 无 |
  | 斑马纹 | **偶数行 `#f3f3f3`** | 无 |
  | 单元格内边距 | **12px 左右 / 10px 上下** | `12px 0`（左右 0） |
  | 行高 | **44px**（表二表头也是 44） | 49px |
  | 表一表头高 | **68px**（`Weight ⏎ range` 两行） | 72.5px（单行 + 换行差异） |
  | 表一列宽 | 88 / 262 | 90.5 / 259.6 ✅ 接近 |
  | **表二列宽** | **203 / 147** | **260 / 90** ❌ 差 57px |
- **判据**：节点树 `Frame 992514/992515`（表头，fill `#f3f3f3`、stroke `#cccccc` 0.5）、
  `Frame 992520/992522/992524`（斑马行 fill `#f3f3f3`）；
  DOM 侧 `dom_shipping_390.json` 的 th/td rect。对照图 `$SP/d_ship390_t1.png`（差异非常直观）。
- **建议**：`.rich-table` 补 `border: .5px solid #ccc` 的全网格 + `thead` 底色 + `tbody tr:nth-child(even)` 斑马 +
  `padding: 10px 12px`；列宽用 `col`/`width` 写死（表一 88/262、表二 203/147 的比例），
  别继续靠 `table` 自动算法 —— 表二就是这么歪的。
- **P1**

### P1-7 `.scallop--to-lime` 的条带底色是薄荷绿，稿是白色
- **位置**：`assets/scss/components/_scallop.scss:82`
  `.scallop--to-lime { --wave-bg: $c-lime-150; --wave-fg: $c-lime; }`
- **页面/断点**：我这 5 页的 footer-CTA 上方分隔条，**1440 + 390 都是**（**全站 11 页都用这一个类**）
- **现象**：这条分隔条上面是**白色**区块（`.cta-band` / `.form-section` / `.rich-page` 都是
  `background: $c-white`），下面是 lime 的 footer-CTA。`--wave-bg` 画的是「上面那块的颜色」，
  写成 `$c-lime-150` 就在白区和 lime 之间插了一条约 96px 高、满宽的 `#e7f8d0` 浅带。
- **稿值 vs 实现**：稿 `Spacer Desktop`（FAQ y=1705.6 h=96）**fills 为空**（透明 → 透出白底）；
  实现该处像素 `#e7f8d0`。
- **判据**：同深度像素对比 —— 弧形几何**完全一致**（稿 y=1726 的 lime 段
  `[(29,196),(331,504),(633,806),(935,1109),(1237,1411)]` 与实现 y=1770 的
  `[(29,199),(331,504),(633,807),(936,1109),(1238,1411)]` 逐像素吻合），
  **只有非 lime 的那部分**稿是 `#ffffff`、实现是 `#e7f8d0`。
  对照图 `$SP/d_ref1440_note.png` 右半底部那条浅带。
- **建议**：这一处应为 `--wave-bg: transparent`（或 `$c-white`）。
  ⚠ 类是全站共用，改之前请其它组确认 index/pdp 等页上方区块的底色。
- **P1**（视觉上是一条明显的错色横带）

### P1-8 FAQ 手机端 CTA 板整块用了桌面稿的内容
- **位置**：`faq.html:148-168`（`<section class="cta-band">`）
- **页面/断点**：FAQ **390**
- **稿值 vs 实现**：

  | | 手机稿 `324:76169` | 实现（两个断点都是桌面稿内容） |
  |---|---|---|
  | 弧形字 | `STILL HAVE QUESTIONS?`（20/800） | `GET HEALTHY` |
  | 标题 | `Can’t find the answer you’re looking for? Please chat to our friendly team.`（24/800/30/-0.24/#b5ed61） | `Join the 10% of people who are nutrient sufficient` |
  | 按钮 | `Contact us`（16/500/+0.48） | `Start Your Greens` |
- **判据**：`dump-text.py 324-76169_faq` 明确列出这三条；`cmp_faq_390.json → fig_only`
  里 y=1298 / y=1545 两条全是稿有页面无。对照图 **`$SP/d_faq390_cta.png`**（左右完全是两块东西）。
- **性质**：两稿冲突（桌面板是 GET HEALTHY，手机板是 STILL HAVE QUESTIONS），但结果是
  **手机稿这三句文案全站没有落地**，也丢了指向 Get in Touch 的入口。归 ① 也归 ③，见下。
- **P1**

### P2-9 FAQ 手机端手风琴少 2 行（6 vs 8）
- **位置**：`faq.html:119-155`
- **页面/断点**：FAQ 390
- **稿值 vs 实现**：手机稿 8 行（1 open + 7 closed，y=510/611/680/749/818/887/956/1025，节距 69）；
  桌面稿 6 行（1 open + 5 closed）；实现 6 行。
- **判据**：`dump-text.py 324-76169_faq` 数出 1 个 `Accordion Open` + 7 个 `Accordion Closed`；
  `cmp_faq_390.json → fig_only` 里多出 y=956 / y=1025 两条。对照图 `$SP/d_faq390_hero.png`。
- **性质**：两稿冲突，全是占位行，**建议交设计方裁决**（同 3.4-C 「Science nutrient 卡 3 vs 4」的处理）。
- **P2**

### P2-10 FAQ 桌面第一（展开）行多了一条顶部分隔线 + 20px 上内边距
- **位置**：`assets/scss/modules/_faq.scss:48-54`（`padding-top: 20px; border-top: 1px`），
  取消规则只写在 `@include mobile`（第 78-80 行）
- **页面/断点**：FAQ **1440**
- **稿值 vs 实现**：稿里第一个（展开的）`Accordian` 实例 y=619.6 h=**60**，它的 `Divider` 矩形
  **是隐藏的**，标题文字就落在区块 padding 上沿（523.6 + 96 = 619.6）；
  闭合行才有可见 `Divider`（h=1，w=624）+ 20px 到文字。实现在桌面给第一行也画了线并留了 20px。
- **判据**：`figma/nodes/324-75766_our-story-desktop.json` 中
  `INSTANCE 'Accordian' y=619.6 h=60` → 子 `RECTANGLE 'Divider'` `visible=false`；
  DOM `summary.faq__row` 盒顶 y=639 而文字在 659（=区块顶 543+96+20）。
- **建议**：把 `.faq__item:first-child` 那条去线规则从 `@include mobile` 里提出来（两个断点都适用）。
- **P2**

### P2-11 手风琴展开正文与标题的间距 16px，稿是 8px
- **位置**：`assets/scss/components/_accordion.scss:49-54` `.acc-body { gap:16px; padding-top:16px }`
- **页面/断点**：FAQ **1440 + 390**
- **判据**：稿 `FRAME 'heading' gap 8`，标题 y=619.6 h=24 → 正文 y=651.6（差 32 = 24+8）；
  手机稿 510 → 542 同样是 8。实现桌面 659 → 700（差 41 = 24+16 + 1px 行盒）、手机 414 → 454（+16）。
- **P2**

### P2-12 FAQ 桌面展开正文 16/24，稿是 18/28
- **位置**：`assets/scss/components/_accordion.scss:56-61` `.acc-body__text`
- **页面/断点**：FAQ **1440**（390 稿就是 16/24，手机是对的）
- **判据**：`cmp_faq_1440.json → diffs[2]`：`size 18→16`、`line-height 28→24`。
  颜色 `#4d4d4d` 两边一致 ✅。
- **P2**

### P2-13 `form__note` 里的链接没有下划线
- **位置**：`assets/scss/modules/_form.scss:194-207`（`.form__note a` 只给了 weight/color，
  而 `assets/scss/base/_reset.scss:24` 有全局 `a { text-decoration: none }`）
- **页面/断点**：Referral **1440 + 390**
- **稿值 vs 实现**：稿 `Sign In` 段 `textDecoration: UNDERLINE` + `fontWeight 500` + `#011307`；
  实现 weight 500 ✅ 颜色 ✅，**下划线丢了**。
- **判据**：`figma/nodes/326-81218_...json` 的 `styleOverrideTable["37"]`（桌面）/
  `326-81540` 的 `["39"]`（手机）都带 `textDecoration: UNDERLINE`。
  对照图 `$SP/d_ref1440_note.png` / `d_ref390_note.png` 肉眼可辨。
- **P2**

### P2-14 `form__check` 的链接下划线多包了 "friendly"
- **位置**：`get-in-touch.html:157` `<a href="privacy-policy.html">friendly privacy policy</a>`
- **页面/断点**：Get in Touch 1440 + 390
- **稿值 vs 实现**：`characterStyleOverrides` 显示前 26 个字符（`You agree to our friendly `）
  用样式 35（无下划线），第 26~39 字符（`privacy policy`）用样式 34（UNDERLINE）。
  实现把 `friendly` 也划进了链接。
- **判据**：`figma/nodes/326-79979_our-story-desktop.json` 该 TEXT 的
  `characterStyleOverrides` + `styleOverrideTable`（34 有 `textDecoration: UNDERLINE`，35 没有）。
  对照图 `$SP/d_git1440_form.png` 底部。
- **P2**

### P2-15 手机端提交按钮高度 60px，稿是 52px
- **位置**：`assets/scss/modules/_form.scss:177-192` `.form__submit { height: 60px }`（无 mobile 覆盖）
- **页面/断点**：Get in Touch / Referral **390**
- **判据**：稿 `Button` 帧 —— 桌面 `624×60`（✅ 实现一致）、手机 **`350×52`**、圆角 72 ✅。
  DOM 390 实测 `button.form__submit h=60`。
- **备注**：手机端的字号/字距（稿 16 + 0.48，实现 18 + 0）属主会话统一记的系统性偏差，此处不重复。
  项目里已有的 `.btn--lg`（52px / 16px / ls .48）就是这套值。
- **P2**

### P2-16 Referral 手机端说明行与免责声明的 token 用了桌面值
- **位置**：`assets/scss/modules/_form.scss:194`（`.form__note` 颜色）、`:209`（`.form__disclaimer` 无 mobile 覆盖）
- **页面/断点**：Referral **390**
- **稿值 vs 实现**：
  - `form__note` 颜色：手机稿 `#4d4d4d`，实现 `#656565`（桌面稿的值）
  - `form__disclaimer`：手机稿 **16/24/-0.32**，实现 **14/20/-0.28**（桌面稿的值）
- **判据**：`cmp_referral_390.json → diffs[0]/[1]`。对照图 `$SP/d_ref390_note.png`（实现的小字明显更小）。
- **P2**

### P2-17 Privacy 手机端页头副标 token 不对
- **位置**：`privacy-policy.html:109` 用了 `page-hero__lead--lg`
- **页面/断点**：Privacy **390**
- **稿值 vs 实现**：手机稿 **16 / 400 / lh 24 / ls -0.32 / #4d4d4d**；实现 18 / lh 26 / -0.36 / #1a1a1a。
- **判据**：`fig_privacy-policy_390.json` y=280 那条。
  ⚠ `cmp_privacy-policy_390.json` 的 diff 把这条**配错对**了（拿稿的页头副标去配了正文里那个
  多出来的 `<p>Subheading</p>`，见 P1-5），所以只报了 `color #4d4d4d→#808080`；
  真正的页头副标掉进了 `dom_only`（y=185）。这是 P1-5 连带的读数污染。
- **备注**：FAQ / Get in Touch / Referral 的**手机**副标（18/400/26/-0.36/#1a1a1a）实现是对的 ✅，
  只有 Privacy 这块板不一样。
- **P2**

### P2-18 rich-text 手机端段间距 20px，稿是 16px
- **位置**：`assets/scss/modules/_rich-text.scss:32-36` `.rich-text__section { gap: 20px }`（无 mobile 覆盖）
- **页面/断点**：Privacy / Shipping **390**
- **判据**：稿正文 TEXT 节点 `paragraphSpacing`：桌面 Privacy **20**（✅ 实现一致），
  手机 Privacy / Shipping **16**。
- **备注**：段落被拆成多个 `<p>` **是对的** —— 稿的 TEXT 节点里本来就有硬换行 + paragraphSpacing，
  视觉上就是多段。区块间距（48）、h2→p（20）、`--tight`（12）逐项核过，**全部与稿一致** ✅。
- **P2**

### P2-19 FAQ 手机端主标题断行位置与稿不同
- **位置**：`faq.html:107`
- **页面/断点**：FAQ 390
- **稿值 vs 实现**：稿 `'Frequently  asked questions'`（U+2028 强制断行）→
  「Frequently」/「asked questions」；实现自然折行 →「Frequently asked」/「questions」。
  两边都是 2 行、行高 40、起始 y 一致，只是断点不同。
- **判据**：`dump-text.py 324-76169_faq` 第 5 行；对照图 `$SP/d_faq390_hero.png`。
- **备注**：⚠ U+2028 在 HTML 里不是换行符（见 memory `nl2br-blind-to-u2028`），
  要还原得插 `<br>` 或用 `<span>`+`display:block`。桌面稿没有这个断行 ✅。
- **P2**

### P2-20 Shipping 首个 h2 的行高/字距（稿自己就不一致）
- **位置**：`shipping.html:121`；样式 `assets/scss/modules/_rich-text.scss:41-49`
- **页面/断点**：Shipping 390
- **稿值 vs 实现**：稿「When will I receive my order?」= 30 / **lh 38 / ls 0**；
  同页另两个 h2 = 30 / lh 36 / ls -0.3（实现按后者）。
- **判据**：`cmp_shipping_390.json → diffs[0]`。
- **备注**：**稿内自相矛盾**，实现取了多数派，合理。列出来只为可追溯。
- **P2**

### P2-21 Shipping 表一表头在稿里是两行
- **位置**：`shipping.html:130` `<th>Weight range</th>`
- **稿值 vs 实现**：稿 `'Weight  range'`（强制两行，表头行高 68）；表二的表头才是单行「Weight range」。
- **判据**：`dump-text.py 326-83129_shipping`。与 P1-6 的列宽/行高一起修即可。
- **P2**

---

## ② 字体度量差（AUDIT-HANDOFF 3.4-A，**不算实现偏差**）

1. **正文比稿轻一档**：400 与 300 指向同一个 `pppalma-fizzy-light.woff2`。
   在 Privacy / Shipping 这种整屏正文的页面上最明显（`$SP/d_priv1440_a.png` 里实现的灰度更浅）。
2. **行内容纳字数不同 → 段落行数不同**：
   - Privacy 1440 第二段：稿 6 行 / 实现 5 行（实现每行多塞一两个词）。
   - Shipping 390 第一段：稿 7 行 / 实现 6 行 —— 这一条直接造成后面 h2 位置差 −24px，
     `cmp_shipping_390.json` 里 `jump=-24`（`How much is standard shipping?`）**全部由此产生，不是间距 bug**。
   - Privacy 全页高度 稿 4347 / 实现 4040 里，除去 P1-5 缺的那一段，剩余差额也来自这里。
3. **横向 dx 噪声**：`xOff>8` 那一串里，居中文本（`page-hero__title` dx=223/350/263/419、
   `page-hero__lead` dx=444/330/198/556）**全是「Figma 记的是文本框左边，实现记的是墨迹盒左边」**，
   不是错位 —— 稿的文本框宽 1220/848，实现的 h1/p 是收缩宽度且居中。已逐条排除。
4. 按钮/页脚等处 `Excellent` dx=+51 / `Truspilot` dx=−46 同理（Trustpilot 徽章是文字占位，3.4-E）。

---

## ③ 已列在 3.4 的「有意为之 / 待裁决」——本次确认成立

| 条目 | 确认结果 |
|---|---|
| **Privacy 正文全是 lorem ipsum**（3.4-D） | ✅ 成立。**且逐词核对：除 P1-5 那一段外，全文与稿一字不差**（桌面 4162 字符、手机 634 词全对）。没有被改写。 |
| **Shipping 全页写美国配送**（Alaska / Hawaii / US Territories / $65 / $9.99 / 0-4kg / $13）（3.4-D） | ✅ 成立且**原样保留**。逐词 diff：`figwords 266 / domwords 266`，**零差异**。HTML 里也有 `⚠` 注释标了必须重写。 |
| **Get in Touch 的 Enquiry Type 只有 `Contact Us`**（3.4-D） | ✅ 稿里确实只有一项；实现补的四项（contact / partners / press / careers）＋`?type=` 预填（`assets/js/main.js:600`）与 header/footer 四个入口对得上。**归 ④ 待客户确认。** |
| **手风琴用原生 `<details>`，动画只在 Chrome 系**（3.4-G） | ✅ 成立，未报为 bug。`_accordion.scss:35-47` 用 `@supports selector(::details-content)` 包着，降级是「瞬开瞬收」不是「打不开」，并且有 `prefers-reduced-motion` 兜底 ✅。 |
| **Shipping 无桌面稿，按 Privacy 文本页布局实现**（PROJECT-STATUS #8） | ✅ 成立。1440 下**没有坏**：无横向溢出、无重叠、无异常断行；两张表的第二列很宽（`$13` 落在 637px 的格子里）显得空，但可读。见 `$SP/d_ship1440_table.png`。 |
| **交互态全是自定值**（3.4-F） | ✅。本组涉及的可点元素 hover/transition **都在**：`.faq__row`（hover+transition+cursor ✅）、`.btn`/`.form__submit`（✅）、`.form__note a`/`.form__check a`（✅）、`.field__input`/`.field__phone`（focus 过渡 ✅）。没发现「有 hover 没 transition」或「能点没 hover」。 |

### 新发现的两稿冲突（3.4-C 之外，**建议加进待裁决清单**）

| # | 位置 | 桌面稿 | 手机稿 | 现在的做法 | 影响 |
|---|---|---|---|---|---|
| C-5 | **FAQ 页 CTA 板** | `GET HEALTHY` / `Join the 10% of people who are nutrient sufficient` / `Start Your Greens` | `STILL HAVE QUESTIONS?` / `Can’t find the answer you’re looking for? Please chat to our friendly team.` / `Contact us` | 两个断点都用桌面稿 | **手机稿三句文案全站没有落地**（P1-8） |
| C-6 | **FAQ 手风琴行数** | 6 行 | 8 行 | 做 6 行 | 全是占位行，影响小（P2-9） |
| C-7 | **Referral 提交按钮** | `Send Message` | `Sign up` | 两个断点都用 `Send Message` | 一个「推荐计划注册表单」上写 `Send Message` 读起来是错的；**桌面稿更像设计师从 Get in Touch 复制忘了改** |
| C-8 | **Referral 说明行大小写** | `Sign In` | `Sign in` | 用 `Sign In` | 可忽略 |
| C-9 | **Privacy / Shipping 手机稿没有 footer-CTA** | Privacy 桌面稿**有**（`YOUR GREENS CALLED` / `They want to be gummies now`） | Privacy 390、Shipping 390 **都没有**，正文直接接页脚 | 两个断点都保留 footer-CTA | 手机端多出一整块（约 500px） |
| C-10 | **Privacy / Shipping 手机稿的页脚是另一版组件** | — | 链接 16px / **weight 600** / ls 0，按钮文案 `Subscribe now`，栏标题 `#ffffff` | 全站一套页脚（16/400/-0.32、`Subscribe`、`#daf6b0`） | 与 FAQ/GiT/Referral 手机稿（14/400/-0.28、`Subscribe`）**互相矛盾**，设计方自己不统一 |
| C-11 | **FAQ 手机稿展开行正文** | `Text here` | `First accordion open on the FAQ page`（更像设计师写给自己的备注） | 用 `Text here` | 都是占位，可忽略 |

---

## ④ 需设计方 / 客户给值

1. **Get in Touch 的 Enquiry Type 最终选项列表** —— 稿只给了 `Contact Us`，现有四项是按
   header/footer 指向本页的四个链接补的（`get-in-touch.html:144-150`），并支持 `?type=` 预填。**需客户确认。**
2. **表单 focus ring** —— `_form.scss:74-78` / `:109-112` 的 `0 0 0 3px rgba(0,86,53,.15)` + 绿色边框
   稿里没有。（顺带：`326-80318` 里那个 `#011307` 描边的 Input 是**页脚订阅框**，不是 focus 态，别误读。）
3. **Shipping 桌面版式** —— 无稿，现按 Privacy 文本页布局。两张表在 848px 版心下第二列过宽，
   需要设计方给桌面列宽（或确认表格改成两栏窄表）。
4. **两张费率表都是 7 行同值占位**（`0 - 4kg` / `$13` ×7，两张表一模一样）—— 稿就是这样，
   上线前必须换成真实费率区间。
5. **Privacy Policy 页头副标就叫 `Subheading`** —— 稿自带占位，需客户给真文案。
6. **上面 C-5 ~ C-10 六条两稿冲突**需要设计方裁决，尤其 **C-5（FAQ 手机 CTA）** 和
   **C-9（Privacy/Shipping 手机端要不要 footer-CTA）**。

---

## ⑤ 文案逐段核对（本组重点）

方法：`figma/dump-text.py` 取稿全文（含隐藏节点标记）→ 与 HTML 正文做**逐词 diff**。

### 5.1 差异清单

| 页面 · 断点 | 稿原文 | 页面实际 | 差异 |
|---|---|---|---|
| **Privacy · 1440+390** | `Mi tincidunt elit, id quisque ligula ac diam, amet. Vel etiam suspendisse morbi eleifend faucibus eget vestibulum felis. …（共 568 字符，2 个自然段）` | `Subheading` | **漏整段 + 把页头副标重复进了正文**（P1-5，唯一的文案差异） |
| **FAQ · 390** | `STILL HAVE QUESTIONS?` | `GET HEALTHY` | 用了桌面稿（C-5） |
| **FAQ · 390** | `Can’t find the answer you’re looking for? Please chat to our friendly team.` | `Join the 10% of people who are nutrient sufficient` | 同上，**整句缺失** |
| **FAQ · 390** | `Contact us` | `Start Your Greens` | 同上，按钮文案 + 落点都变了 |
| **FAQ · 390** | `First accordion open on the FAQ page` | `Text here` | 用了桌面稿的占位（C-11） |
| **FAQ · 390** | `Accordion Closed` ×7 | ×5 | 少 2 行（C-6） |
| **FAQ · 390** | `Frequently ⏎ asked questions` | `Frequently asked questions`（自然折行） | 断行位置（P2-19） |
| **Referral · 390** | `Sign up` | `Send Message` | 用了桌面稿（C-7） |
| **Referral · 390** | `Already have an account? Sign in` | `… Sign In` | 大小写（C-8） |
| **Shipping · 390** | `Weight ⏎ range`（表一表头） | `Weight range` | 断行（P2-21） |
| 页脚（5 页 · 390） | `Homepage` / `PDP` / `Influencers` | `Shop` / `Shop`(第一栏) / `Partners & Influencers` | 页脚是全站共用组件，**归主会话**；此处仅记录 |

### 5.2 完全一致的部分（已逐词验过，无漏句、无错字、无自造）

| 页面 | 结果 |
|---|---|
| **Shipping 390 正文** | `figwords 266 / domwords 266`，**零差异**。两段长文 + 两张表 22 格全对，美国配送口径原样保留 ✅ |
| **Privacy 1440 正文** | 除 P1-5 外**逐词一致**（8 个标题 + 7 段 lorem） |
| **Privacy 390 正文** | 同上 |
| **Get in Touch 1440/390** | 标题 / 副标 / 6 个 label / 6 个 placeholder（`First Name` `Last name` `you@company.com` `AU` `+61 400 000 000` `Contact Us`）/ 同意行 / 按钮，**全对** ✅ |
| **Referral 1440** | 标题 / 副标 / 4 个 label / placeholder / `Send Message` / `Already have an account? Sign In` / 免责声明长句，**全对** ✅ |
| **FAQ 1440** | 全对 ✅ |
| **隐藏节点未被误抄** | 稿里 `And Last Questions?`、`You loved gumi bears as a kid…`、`This is a hint text to help user.`、`123,456+ happy customers`、`Earn product rewards and $20…`、五处 `Additional`、FAQ 桌面 CTA 里那句 `…swapped the multivitamin struggle…`（与页脚那句 `traded` 只差一个词）**全部 `[HIDDEN]`，实现一条都没抄进来** ✅ |

**结论：没有自造内容（铁律 3 无违规）；唯一的漏段是 Privacy 的正文首段；FAQ 手机 CTA 的三句是「用了另一版稿」而非编造。**

---

## ⑥ `fig_only` / `dom_only` triage

### fig_only（稿有页面无）

| 类别 | 条数 | 判定 |
|---|---|---|
| `gumi.com.au` | 每页 1 条 | **配对失败**：Figma 板顶部的假 Safari 地址栏，不是页面内容 |
| 表单 placeholder（`First Name` / `Last name` / `you@company.com` / `AU` / `+61 400 000 000` / `Contact Us`） | GiT×6、Referral×5 | **配对失败**：`placeholder` 属性不是 DOM 文本节点，探针量不到。逐条比对 HTML，**六个 placeholder 全部一字不差** ✅ |
| 页脚 `Enter your email` | 每页 1 条 | 同上（页脚 input placeholder） |
| 页脚 `Homepage` / `PDP` / `Influencers` / `Subscribe now` | 390 各页 | **真差异**，但属全站页脚，归主会话 |
| Privacy 的 4 条 lorem 段 | 1440×4、390×4 | **配对噪声**：稿是 1 个 TEXT 节点，实现拆成 3 个 `<p>`（拆分本身是对的，见 P2-18 备注）；真正的漏段只有 `Mi tincidunt…` 那一条 |
| Shipping `Our standard shipping in the US…` | 1 条 | 同上（1 节点 → 2 段） |
| FAQ 390 `First accordion open…` / `Accordion Closed`×2 / `Can’t find the answer…` / `Contact us` | 5 条 | **真差异**（C-5 / C-6 / C-11） |

### dom_only（页面有稿无）

| 类别 | 条数 | 判定 |
|---|---|---|
| `header__link` / `header__sublink` / `nav-card__*` / `Manage Account` | 1440 每页 7 条、390 每页 15~18 条（x = −370 或 −354，**在视口外**） | **配对失败**：抽屉/下拉菜单的收起态。稿的 header 是 `Closed` 实例，不画展开内容。**不是多余内容** |
| `p.acc-body__text 'Text here'` ×5~6 | FAQ 两个断点 | **探针噪声**：闭合 `<details>` 的 `content-visibility:hidden` 仍返回非零 rect（见 0.4-②） |
| `footer__label` `Why Gumi` / `Learn more` / `Get in touch`、`a.footer__link Shop` / `Partners & Influencers` | 390 每页 5 条 | **真差异**：手机稿页脚是 2 栏无栏标题，实现沿用桌面 3 栏带栏标题。全站页脚，归主会话 |
| `a 'friendly privacy policy'` / `a 'Sign In'` | GiT / Referral 各 1 | **配对失败**：稿里是同一 TEXT 节点的字符级 override，实现拆成了 `<a>` 子元素。内容对，只是下划线范围/样式有偏差（P2-13 / P2-14） |
| `p 'Subheading'`（Privacy body） | 1440 + 390 | **真差异 → P1-5** |
| `h2.footer-cta__title` / `p.footer-cta__text` / `a.btn footer-cta__btn` | Shipping 390 3 条 | **真差异 → C-9**（稿没有 footer-CTA） |
| Privacy 390 的 `page-hero__lead` | 1 条 | **配对被 P1-5 污染**（详见 P2-17） |
| `button.btn form__submit 'Send Message'` | Referral 390 | **真差异 → C-7** |
| `h2.cta-band__title` / `a.btn 'Start Your Greens'` | FAQ 390 2 条 | **真差异 → C-5** |
| `button.footer__submit 'Subscribe'` | Privacy/Shipping 390 | 稿是 `Subscribe now`，页脚，归主会话 |

**结论：`domOnly` 偏大（privacy@390=38）的主因就是 ① header 抽屉收起态、② 闭合手风琴的探针噪声、
③ 页脚栏标题差异，三项加起来占 30 条以上，不是页面上真的多出来的内容。**

---

## ⑦ `drift` 的 `jump > 12px` 归因

所有 `jump` 均已折算掉假浏览器外壳（桌面 −59.6 / 手机 −96）。

| 页面·断点 | jump | 位置 | 归因 |
|---|---|---|---|
| FAQ 1440 | −14 / +31 | `Shop now` / `page-hero__title` | header 内部节奏（announcement 40 ✅、nav 80 ✅），**净落到 h1 时的偏移是 +17 = P1-1 的 padding-top 差**；其余是 header 组件事，非本组 |
| FAQ 1440 | **+62** | `summary.faq__row 'Accordion Open'` | 拆解 = 页头 padding-bottom +24（P1-1）+ lead 行高 +6（P1-4）+ 分隔条 +32（P1-2）+ 首行多出的 20px（P2-10）。**四项全部可解释，无残差** |
| FAQ 1440 | +29 | `p.acc-body__text` | P2-11（16 vs 8） |
| FAQ 1440 | −25 | 第二行 `Accordion Closed` | 上一条的回归，非独立问题 |
| FAQ 1440 | +21 / +13.9 | `cta-band__title` / `footer-cta__title` | 累计残差 ≤5px/块，正常 |
| GiT / Referral 1440 | **+60 / +60** | `label.field__label 'First name'` | 与上同源：P1-1（+40）+ P1-4（+6）+ P1-2（+32）− 表单区 padding 一致（96 ✅）。**表单内部节奏（字段间距 24、label→input 6、按钮 32）全部与稿一致 ✅** |
| GiT 1440 | −16 | `button 'Send Message'` | 上条回归 |
| Referral 1440 | +16 | `p.form__note` | 按钮到说明行的间距，实现 32 稿 ~40；≤16px，P2 级 |
| Privacy 1440 | −256 / +184 / −184 / +200 / −568 / +568 | 一串 lorem 段落 | **全部是配对噪声**：同一句 lorem 在页面上出现 2~3 次，`compare2.py` 按「相对位置最近」配对时跨节配错。逐段做全文 diff 后确认版面顺序与稿完全一致 |
| Privacy 1440 | −17.1 / +12.1 | footer-cta / footer | 累计（缺段 −352 + 字体行数差）的收敛 |
| Shipping 390 | −36 / −24 | 两个 h2 | −35 = **缺分隔条**（P1-3）；−24 = 字体度量致第一段少一行（②） |
| Shipping 390 | ±626 / ±636 / ±698 / ±705 | 表格单元格 | **配对噪声**：`0 - 4kg` / `$13` 各出现 14 次，两张表之间互相配错。用行内 x/y 重新核过，表格顺序无误 |
| Shipping 390 | +1452 | `footer__tagline` | 实现多了一块 footer-CTA（C-9） |
| FAQ 390 | −345 | 第 6 行 `Accordion Closed` | 稿有 8 行、实现 6 行（C-6）导致的配对错位 |
| 各页 390 | ±40~296 | 页脚链接 | 页脚 3 栏 vs 2 栏的配对错位（见 ⑥），归主会话 |

---

## ⑧ 主会话统一记的三条系统性偏差 —— 确认结果

1. **页脚链接与版权行 稿 14/20 → 实现 16/24**：✅ 成立，FAQ / Get in Touch / Referral 三块手机稿逐条命中。
   ⚠ **补充**：Privacy 390 与 Shipping 390 两块板的页脚是**另一版组件**（16px / weight **600** / ls **0** /
   `Subscribe now` / 栏标题 `#ffffff`），实现的 16px 反而对上了尺寸，但字重和字距对不上，
   而 `Privacy`/`Cookies` 两条实现是 14/20、稿是 16/24（方向反过来）。**稿自己不统一。**
2. **`letter-spacing` 实现恒为 −0.32px**：✅ 成立。本组命中 `Shop now`（稿 0）、
   `You agree to our friendly privacy policy`（稿 0）、`Already have an account?`（稿 0）、
   Privacy/Shipping 手机页脚链接（稿 0）。
3. **390 下按钮 稿 16px + 0.48 → 实现 18px + 0**：✅ 成立（`Send Message` @ get-in-touch 390）。
   **另加**：按钮**高度**也差（60 vs 52，P2-15）。

---

## ⑨ 总表：页面 × 区块 × 断点 × 结论

图例：✅ 一致 · ⚠ 小偏差(P2) · ❌ 明显偏差(P1) · — 无此区块 · n/a 无稿

| 页面 | 区块 | 1440 | 390 | 说明 |
|---|---|---|---|---|
| **FAQ** | 页头（标题/副标/内边距） | ❌ | ✅ | 桌面 padding 80/96 应 64/72（P1-1）+ 副标 token（P1-4）；手机断行 ⚠（P2-19） |
| | 页头下扇贝分隔 | ❌ | ✅ | 128/525 应 96/302（P1-2） |
| | 手风琴列表 `.faq--plain` | ⚠ | ⚠ | 白底无标题 ✅、列宽 624 ✅、节距 69 ✅、hover/transition ✅；桌面首行多线（P2-10）、正文 16/24 应 18/28（P2-12）、正文间距 16 应 8（P2-11）；手机少 2 行（C-6） |
| | CTA 扇贝板 | ✅ | ❌ | 桌面板形/文案/按钮全对；**手机整块用了桌面稿内容**（P1-8 / C-5） |
| | footer-CTA 上方分隔 | ❌ | ❌ | 条带底色薄荷绿应白（P1-7），几何 ✅ |
| **Get in Touch** | 页头 | ❌ | ✅ | 同 P1-1 / P1-4 |
| | 页头下扇贝分隔 | ❌ | ✅ | P1-2 |
| | 表单字段 / 下拉 / 电话组 | ✅ | ✅ | 624 列宽、44 高、圆角 8、`#cccccc` 边、label 14/20/-0.28/#666、chevron 20px `#4d4d4d`、textarea 152 —— **逐项与稿一致** |
| | 同意行 | ⚠ | ⚠ | 下划线多包了 `friendly`（P2-14）、ls（系统性） |
| | 提交按钮（全站唯一满宽） | ✅ | ⚠ | 桌面 624×60 ✅；手机高 60 应 52（P2-15）+ 字号/字距（系统性） |
| | footer-CTA 上方分隔 | ❌ | ❌ | P1-7 |
| **Referral** | 页头 | ❌ | ✅ | 同 P1-1 / P1-4 |
| | 页头下扇贝分隔 | ❌ | ✅ | P1-2 |
| | 表单字段 | ✅ | ✅ | 同 Get in Touch |
| | 提交按钮 | ✅ | ❌ | 手机稿是 `Sign up`，实现 `Send Message`（C-7）+ 高度（P2-15） |
| | 说明行 / 免责声明 | ⚠ | ⚠ | 链接缺下划线（P2-13）；手机 token 用了桌面值（P2-16） |
| | footer-CTA 上方分隔 | ❌ | ❌ | P1-7 |
| **Privacy Policy** | 页头 | ❌ | ⚠ | P1-1 / P1-4；手机副标 16/24/#4d4d4d（P2-17） |
| | **页头下扇贝分隔** | ❌ | ❌ | **完全缺失**（P1-3） |
| | 长文排版（标题层级/段距/区块距） | ⚠ | ⚠ | h2 40/48 ✅ h3 32/40 ✅（手机 30/36、24/30 ✅）、区块 48 ✅、h2→p 20 ✅、`--tight` 12 ✅；手机段间距 20 应 16（P2-18） |
| | **正文首段** | ❌ | ❌ | **整段被 `Subheading` 顶掉**（P1-5） |
| | footer-CTA | ✅ | ❌ | 手机稿没有这块（C-9） |
| | footer-CTA 上方分隔 | ❌ | ❌ | P1-7 |
| **Shipping** | 页头 | n/a（未坏） | ✅ | 无副标 ✅（稿里那条 18/400 是隐藏的） |
| | **页头下扇贝分隔** | n/a | ❌ | **完全缺失**（P1-3） |
| | 长文排版 | n/a（未坏） | ⚠ | 文案零差异 ✅；首个 h2 lh/ls（稿自相矛盾，P2-20）、段间距（P2-18） |
| | **两张费率表** | n/a（未坏，第二列偏空） | ❌ | 无边框/无表头底色/无斑马纹/内边距/行高/表二列宽（P1-6）、表头断行（P2-21） |
| | footer-CTA | n/a | ❌ | 稿没有这块（C-9） |
| | footer-CTA 上方分隔 | ❌ | ❌ | P1-7 |

### 断点结论

- **桌面 1440**：四个有稿的页面**共享同三个根因**——`.page-hero--center` 内边距、`.scallop--lg` 尺寸、
  `page-hero__lead--lg` token，**全部源于「How Gumi Works 那块板的值被当成了通用值」**。
  修这三处 + P1-3/P1-5/P1-7，四页桌面还原度即可收敛到 ±5px 以内（jump 拆解已验证无残差）。
  Shipping 1440 无稿，**未发现破损**（无横向溢出/重叠/异常断行）。
- **手机 390**：页头、表单、手风琴的几何**基本完全对齐**（h1/副标/label/按钮的板内 y 逐条 ≤1px），
  剩下的是内容层面的问题：Privacy 缺段、Privacy/Shipping 缺分隔条、Shipping 表格样式、
  FAQ CTA 用错板、Referral 按钮文案。

---

## ⑩ 非本组、但在本组页面上可见（供对应组核对）

- **全站页脚**：手机端 3 栏带栏标题 vs 稿 2 栏无栏标题；链接名 `Shop`/`Partners & Influencers`
  vs 稿 `Homepage`/`PDP`/`Influencers`；`Subscribe` vs `Subscribe now`。
- **全站 header**：手机端右上角图标顺序为「人像 → 购物袋」，稿是「购物袋 → 人像」
  （见 `$SP/d_ship390_hero.png`）。桌面顺序 ✅。
- **`.scallop--to-lime`（P1-7）是全站 11 页共用的类**，改动前需其它组确认 index/pdp 等页
  分隔条上方区块的底色。

---

*本报告未修改任何项目文件；`docs/audit/01-fidelity-d-text-pages.md` 为本次唯一写入。*

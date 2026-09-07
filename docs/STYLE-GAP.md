# 静态站 ↔ live 样式差异清单

> 2026-09-07 第八十四轮生成。live 主题 `Dev #180348977399`（role = live），基线
> `Gumi-Brand-shopify/baseline-r83/`。采样宽度 **390 / 768 / 1440**，11 个页面全覆盖。
>
> 与 [LIVE-GAP.md](LIVE-GAP.md) 的分工：那一份查**模块在不在**（类名级），
> 这一份查**样式对不对**（computed style 级）。LIVE-GAP 写于 2026-09-04，
> 其中「购物车没做」「gb-vs / gb-promo / gb-app-section 没做」等条目**已过时**，
> 本文第五节按现状重列。

## 判据怎么跑

```bash
cd /home/ly/project/Gumi-Brand
python3 tools/gapstyle.py --password 1234 --width 1440   # 采样 -> tools/gapstyle-1440.json
python3 tools/gapreport.py tools/gapstyle-1440.json      # 逐类差异清单（--geo 看几何）
python3 tools/gapwhy.py --password 1234 --page reviews --sel .gb-page-hero__lead   # 单点追因
python3 tools/losers.py  --password 1234 --width 1440    # 谁压过了我们（CDP 真层叠）
python3 tools/wavecheck.py --password 1234               # 每一条波浪：尺寸 / 配色 / 下方地色
python3 tools/r84check.py --password 1234 [--as-served]  # 本轮四项的判据
```

⚠ `gapstyle.py` 会在 `tools/` 下落一个 6.8MB 的 `gapstyle-<宽度>.json`。
**跑完删掉** —— 探针产物留在项目里会被同步/推送脚本当成本轮改动（见 CLAUDE.md 铁律 21）。

三个探针查的是不同的东西，**缺一不可**：

| 脚本 | 回答 | 局限 |
|---|---|---|
| `gapstyle` + `gapreport` | 同一个类，两边算出来的样式差在哪 | 按**类的第一个元素**取样 —— 一侧缺区块会让序号错位，产生假信号 |
| `losers` | live 上哪条声明**输给了主题自己的 CSS** | 只看得见「我们写了但没赢」，写都没写的看不见；**逐宽度跑**，`@media` 里的声明换个宽度才暴露 |
| `wavecheck` | 每条波浪的尺寸 / 配色 / 它下面真正的地色 | 按**页内顺序**配对，区块数不同就只报数量不符，不逐行比 |

⚠ `losers` 用 CDP 的 `CSS.getMatchedStylesForNode` 读真实层叠，**不自己算特异性** ——
`:not()` / `:is()` / `@layer` 正是最容易算错的地方。简写要展开成 longhand，
含 `var()` 的简写（`border-color: var(--x)`）Chrome 展不开，脚本里有一张手写表补上；
逻辑属性（`padding-block` / `margin-block-end`）也要归一到物理属性，
否则 `summary { padding-block }` 和我们的 `padding-top` 看起来像两件事，清单里全是假警报。

---

## 〇、对方正在做的（2026-09-07 推 r84 时拉到的最新 live）

推送前的三方对比抓到对方当天改了 6 个 section：**正在把写死的波浪逐个换成
`scallop_variant` 下拉**，已改完 `gb-vs` / `gb-app-section` / `gb-product` /
`gb-footer-cta` / `gb-reviews`（默认值等于原来的写死值，**渲染结果没变**，
重跑 `wavecheck` 仍是同样 24 行）。

对本文的影响：

- **第三节 C1 / C2（`gb-page-hero.liquid`）没被覆盖** —— 那个文件还没动过，两条仍然成立。
- **C3（`gb-promo.liquid` 完全没有 scallop）没被覆盖** —— 那个文件也没动过。
- ⚠ **新的 `scallop_variant` 只选颜色，不选尺寸** —— C2 里「大波浪画成了小波浪」那一半
  在任何 section 上都还不是 setting，仍然要动 liquid。
- 对方同时给 `gb-footer-cta` 加了 `gb-footer-cta-wrap--{{ bg_variant }}`，
  我们的 CSS 里没有这个修饰类的规则（不匹配即无害，但对方要用就得先告诉我们取值表）。

## 一、CSS 能改 —— 本轮（r84）已修并推上 live

四条全部是**特异性输给 Horizon 自己的 CSS**，不动结构、不动 liquid。

| # | 位置 | 症状 | 真因 | 页面 |
|---|---|---|---|---|
| A1 | `.gb-footer__input` | 边框 `#dfdfdf`，稿是 `rgba(1,19,7,.1)` | Horizon `input:not([type=checkbox],[type=radio])` 是 **0-1-1**，压过我们的 0-1-0 | 11 页 |
| A2 | `.gb-field__input` / `.gb-field__control` | 边框 `#dfdfdf`，稿是 `#cccccc` | 同上 | get-in-touch / referral |
| A3 | `.gb-form__disclaimer` | 底部负边距 `-2px` 变 `0`，免责声明与提交按钮之间多一截 | Horizon `:last-child:is(p,h1..h6)` 是 **0-1-1** | referral，≤1280 |
| A4 | `.gb-promo` / `.gb-vs` / `.gb-app-section` | 整块窄一圈：1440 档 **1360**、390 档 **358** | 三个 section 的 schema 写了 `"class": "section"`，Horizon `.section > *` 把子元素塞进栅格的居中列 | pdp |

改法：A1–A3 把**被压掉的那两三条声明**在 0-2-0 重述一遍（`.x.x`），
A4 一条 `.section > .gb-promo, … { grid-column: 1/-1; }`。
**2026-09-07 已推 live**（`assets/customstyle.css` / `.scss` 两个文件），
`r84check.py --as-served` 线上两档全绿。

⚠ **A1/A2 的重述块必须排在被修的规则之前** —— 那两条规则里的 `:focus-visible`
和 `.gb-field__input--select:hover` 同样是 0-2-0，靠源码顺序赢；重述块排到后面
就会把焦点态和 hover 一起压死。判据 `r84check.py` 里有这两条断言。

⚠ **不要直接把原规则的选择器加粗成 `.x.x`** —— `.gb-field__input--select`
只有 0-1-0，整条加粗会让它的 `padding-right` / 箭头背景一起失效。

⚠ A4 是**补偿**，不是根治。根治是把三个 section 的 schema 里 `"class": "section"` 去掉
（liquid，见第三节 C6）；去掉后本轮这条 CSS 变成无害的空转，可以一并删。

---

## 二、后台就能改（Online Store Editor，不需要动代码）

| # | 页面 | 改什么 | 现在的症状 |
|---|---|---|---|
| B1 | /pages/reviews | Gumi Page Hero → **取消勾选 Center layout** | 标题与副标题被居中（稿里是左对齐 + 右侧配图）；390 档标题因此走 `--center` 的 36px 档，稿是 30px |
| B2 | faq / get-in-touch / referral / privacy-policy / shipping | Gumi Page Hero → **Size 改为 Default** | section 按大波浪预留高度、却画的是小波浪：1440 档 hero 底下空出 **31px**；390 档反过来，波浪比预留高 **13px**，压进下一区块 |
| B3 | index / reviews / how-gumi-works / our-story | 模板里**加上 `gb-product` section** | 整个产品区块缺失（32 个类），并连带让下一区块的上沿波浪一起没有 |
| B4 | /pages/reviews | 模板里加上 `gb-app-section` | 评论 app 挂载点缺失，同样连带少一条波浪 |
| B5 | how-gumi-works / our-story / reviews | 加上营养标签弹窗那组 block（`gb-nl-*`，index / pdp 上已经有了） | 点营养标签打不开弹窗 |
| B6 | how-gumi-works / our-story | 加上 testimonial 卡（`gb-testimonial*`） | 评价卡整块缺失 |
| B7 | 全站 footer | 填社交链接 | `.gb-footer__social-list` 高 0（静态站 32），footer 整体矮 32px |
| B8 | 全站 footer / header | 法务链接、导航项与静态站不同 | `.gb-footer__legal-links` 130 → 104；`.gb-header__nav` 194 → 126 |
| B9 | /pages/science、/pages/reviews | Gumi Page Hero 的 **Media 没传图** | 两页 hero 少了 570×430 的配图列，整块矮 702 → 450 |

> B3–B6 属于「区块没挂进模板」，不是「liquid 没写」—— 这些 section 在别的页面已经在跑。
> 与 [LIVE-BACKLOG.md](LIVE-BACKLOG.md) 一·2 是同一件事。

---

## 三、必须动 liquid

| # | 文件 | 问题 | 影响 |
|---|---|---|---|
| C1 | `sections/gb-page-hero.liquid` | 副标题的修饰类**写死**成 `--lg --text-page`，没有 setting | science 该用基础档（18/28/400/#4d4d4d）却拿到 18/26/**500**/#333；reviews 与 how-gumi-works 该用 `--lg`（20/30/400/#1a1a1a）也被 `--text-page` 盖掉；faq 少 `--lh-24`（行高 26 而非 24）；privacy 少 `--privacy-mobile`（390 档拿到 18/26/#1a1a1a，稿是 16/24/#4d4d4d） |
| C2 | `sections/gb-page-hero.liquid` | 尾部波浪**写死**成 `gb-scallop gb-scallop--edge gb-scallop--down gb-scallop--to-white`，既没有尺寸也没有配色 setting | ① science 的 hero 波浪是**白色压在奶油色 `gb-science--cream` 上**（稿是 `--mint-to-cream`），实测 `fg=#ffffff` / 下方地色 `#faf9f8`；② science / reviews / how-gumi-works / our-story 四页该画大波浪（1440 档 129 / 390 档 36），实际画的是小波浪（97 / 49） |
| C3 | `sections/gb-promo.liquid` | 没有任何 scallop setting | 静态站 promo 底部那条 `sand-to-white` 波浪线上不存在（pdp 静态 6 条波浪 / 线上 5 条） |
| C4 | `sections/gb-promo.liquid` | 卡片里的 `gb-promo-card__lip`（两个内嵌 SVG，卡片中缝的扇贝咬边）没有输出 | pdp 两张 promo 卡少了中缝装饰 |
| ~~C5~~ ✅ | `sections/gb-nutrition.liquid` | `gb-nutrition → gb-product` 交界的波浪从来没有输出过 | **对方已做**（2026-09-07 09:06 拉到）：加了 `scallop_variant` 下拉，默认 `lime-to-white`，输出 `--edge --lg --bleed`，`--bleed` 也带上了。原始证据见 CHANGELOG 第八十一轮第 2 节 |
| C6 | `sections/gb-promo.liquid` / `gb-vs.liquid` / `gb-app-section.liquid` | schema 里的 `"class": "section"` | 见 A4。去掉后 r84 那条 CSS 补偿即可删除 |
| C7 | 各 section 的文案 setting | `gb-br-narrow` / `gb-br-wide` 两个强制换行辅助类全站缺失 | 手机端折行点与稿不一致 |
| C8 | 无对应 liquid | `gb-promo-modal` / `gb-promo-panel`（index 首单 20% off 弹窗，24 个类） | 整块缺失 |
| C9 | 无对应 liquid | `gb-rich-table`（shipping 配送表格） | 表格缺失 |
| C10 | 已有 section 内 | `gb-acc-body__media`（手风琴内配图）、`gb-rv-panel__glyph`、`gb-acc-icon`（our-story）、`gb-page-hero__overline`（reviews） | 零碎装饰件缺失 |
| ~~C11~~ ✅ | `snippets/gb-logo.liquid` | `{{ logo_img \| image_url: width: w \| times: 2 }}` —— `image_url` 先跑，`times: 2` 乘的是**字符串**，返回 `0` | 线上三处 logo 都是 `src="0"` 加一个 `0 2x` 候选。1x 屏靠 srcset 侥幸还显示，**2x 屏必碎图**。改法已写好在 `liquid/snippets/gb-logo.liquid` + `liquid/r85.patch`，两个 URL 手工 curl 过 200。**已于 r87 推上线**：CSS 那一半 r85 已改，liquid 这一半 r87 推完，线上实测 src/2x 都是真实 URL |
| C12 | `sections/gb-product.liquid` | `.gb-product__features` 由 `{% content_for 'blocks' %}` 在 `.gb-product__info` 末尾输出，排在 CTA 与 guarantee-note 之后 | r86 已用 flex `order` 把它**视觉上**拉回 head 下面（够用）。只有当读屏/Tab 顺序也要求正确时才需要真搬 DOM —— 编辑器 block 无法单独定位，得把 features 改成 section setting 或拆出独立的 `content_for`，商家已填的内容会丢 |

---

## 四、不要报成 bug（有意为之 / 探针假信号）

1. **`.gb-cart*` 整族「线上缺失 / visibility 不同」** —— 抽屉是关着的，两边用的是**不同的隐藏机制**：
   静态站是 `visibility:hidden` + `transform`，线上是 Horizon 的 `<dialog>` 没 open（盒子为 0）。
   `.gb-cart__empty display:none/flex` 同理 —— 静态站演示的是有货购物车，线上是空车。
   `gb-cart-item*`、`gb-btn--lg`（只用在抽屉的两个按钮上）跟着一起「缺失」，都是这一条。
2. **`.gb-sub__select` 两边完全不同** —— 第七十六轮需求方要求订阅下拉**退回原生控件**，
   只 restyle 闭合态。静态站那份是被 selectBox 隐藏掉的原生控件，线上那份是真控件。
   `.gb-select__*`（8 个类）、`.gb-sub__radio`、`.gb-select__native` 全是这一条。
3. **`.gb-select__native` / `.gb-sub__radio` 被 Horizon 上了圆角和底色** —— 两者都是
   `@include visually-hidden`（1×1 裁切），看不见，不用管。
4. **Swiper 的 inline `transform` / `width` / `margin-right`** —— 轮播自己写的行内样式。
5. **`.gb-*__title > .gb-ink-halo` 的 inline `top`** —— 我们自己的 JS 在定位描边副本。
6. **`min-height: auto` vs `0px`** —— `auto` 只在**弹性/网格子项**上保留，其余场合 Chrome 直接算成 `0px`。
   两边父级的 `display` 不同（线上多一层 Shopify 包裹）就会不一样，无视觉后果。
7. **`text-underline-offset` / `overflow-wrap: break-word` / `font-style: var(--font-h1--style)`
   等来自 base.css 的「渗透」** —— 值与我们的默认一致或不可见，不是缺陷。
8. **`.gb-acc-body__text` 静态是 `<p>`、线上是 `<div>`** —— richtext setting 的产物，
   样式挂在类上，两边一致。
9. **几何差异（宽高）大多是内容差异** —— 线上跑真实商品数据、菜单项数不同、
   `.gb-reel__media-img` 的 `aspect-ratio` 来自实际图片尺寸。判据只看 computed style，
   几何在 `gapreport --geo` 里单列，**不作判据**。
10. **`.gb-faq__row` 第一行 padding-bottom 0** —— 线上第一条 FAQ 默认展开（`[open]`），
    展开时 padding 归零是设计。
11. **`.gb-product__form > .gb-product__cta { margin-top: 20px }`** —— 线上 CTA 外面多一层
    Shopify 的 `<form>`，这条是我们自己为线上补的，不是主题干的。
12. **`gapreport` 里 `.gb-acc-body` / `.gb-arc-text--mob` 之类的差异** —— 一侧缺区块导致
    「该类的第一个元素」指到了不同的东西。看到差异先数一遍 `n`。

---

## 五、LIVE-GAP.md 需要改的地方（现状核对）

| LIVE-GAP 的说法 | 现状 |
|---|---|
| `gb-cart` / `gb-cart-item` 线上没有 | ✅ 已做（2026-09-07 对方搬进 Horizon 抽屉） |
| `gb-vs` 线上没有 | ✅ 已做，在 pdp |
| `gb-promo`（PDP 两张卡）线上没有 | ✅ 已做，只差 `__lip` 中缝（C4）与 section 波浪（C3） |
| `gb-app-section` 线上没有 | ✅ 已做，pdp 有；reviews 没挂（B4） |
| `gb-nl-*` 营养标签弹窗线上没有 | ⚠ 部分：index / pdp 已有，how-gumi-works / our-story / reviews 没挂（B5） |
| `gb-testimonial` 线上没有 | ⚠ 部分：liquid 已有，how-gumi-works / our-story 没挂（B6） |
| `gb-promo-modal` / `gb-promo-panel` 线上没有 | ❌ 仍然没有（C8） |
| `gb-rich-table` 线上没有 | ❌ 仍然没有（C9） |
| `blocks/` 下 0 个 `gb-*` | ✅ 仍然成立，25 个已搬进 `sections/` |

# `gb-scallop` — 波浪分隔条怎么用

> 2026-09-08 建立（第九十九轮）。需求方问「波浪有的朝下有的朝上、颜色不同、
> 对应模块的上下 padding 也不一样，到底怎么处理」。这份文档回答四件事：
> **机制** / **变体清单** / **静态站真值表** / **线上现状与偏差**。
>
> 判据：`python3 tools/scallopmap.py [--password 1234]` —— 逐页列出每个波浪的
> 宿主 section、类名、实测高度与两个颜色；带 `--password` 时静态站与线上并排比对。

---

## 1. 它是什么

页面上两个色块交界处那排半圆。**不是 SVG、不是图片**，是三层 `radial-gradient`
加一层 `linear-gradient` 画在一个 `<div>` 上：

```html
<div class="gb-scallop gb-scallop--edge gb-scallop--lg gb-scallop--white-to-mint"></div>
```

尺寸全部从 `:root` 的四个变量算出来，随视口无级缩放：

```scss
--sc-w:    clamp(144.64px, 21vw,    302.19px);   // 小号一个圆的宽
--sc-h:    calc(var(--sc-w) * 0.24008 + var(--sc-band));      // 小号总高 → 96.9 @1440
--sc-lg-w: clamp(144.64px, 36.44vw, 524.74px);   // 大号
--sc-lg-h: calc(var(--sc-lg-w) * 0.24008 + var(--sc-lg-band));// 大号总高 → 129 @1440
```

⚠ **波浪是它上面那个 section 的最后一个子元素**，不是 `<main>` 下的兄弟：

```html
<section class="gb-product">
  …
  <div class="gb-scallop gb-scallop--edge gb-scallop--white-to-mint"></div>
</section>
```

这样一个 Shopify section 模板就能把模块和它的下边缘一起吐出来，商家在后台增删排序
模块时波浪跟着走。（`--edge-top` 是例外，见 §2.4。）

---

## 2. 四个轴，互相独立

### 2.1 尺寸

| 类 | 高度 @1440 | @390 | 稿上的 Spacer |
|---|---|---|---|
| （不加） | **96.9** | 48.0 | `310:8380` / `324:46328` |
| `--lg` | **129** | 35.2 | `310:8412` / `324:46319` |

### 2.2 方向

| 类 | 圆弧鼓向 | 用在哪 |
|---|---|---|
| （不加） | **朝上**（下面那块顶进上面那块） | 页面正文里的所有分隔（稿上 `310:83xx/84xx`，共 43 处） |
| `--down` | **朝下**（上面那块垂进下面那块） | **只在 hero 正下方**（稿上 `324:463xx`，共 9 处） |

⚠ 尺寸和方向在稿里就是两个独立的轴，四个 Spacer 组件正好是它们的交叉。
**组件 id 才是可靠的判据，名字不是。** 早期把 `--lg` 当成"朝下"，结果每个大号分隔
都指错方向，而且"小号朝下"（四个纯文字页要的那个）根本没法表达。

### 2.3 配色（15 对）

命名一律是 **`上面那块-to-下面那块`**，与圆弧朝哪边无关：

| 类 | 上（`--wave-bg`） | 下（`--wave-fg`） |
|---|---|---|
| `--to-lime` | transparent | `$c-lime` |
| `--to-green` | `$c-lime` | `$c-green-900` |
| `--to-white` | `$c-lime-150` | `$c-white` |
| `--to-cream` | `$c-white` | `$c-cream` |
| `--mint-to-lime` | `$c-lime-150` | `$c-lime` |
| `--mint-to-cream` | `$c-lime-150` | `$c-cream` |
| `--sand-to-lime` | `$c-sand` | `$c-lime` |
| `--sand-to-white` | `$c-sand` | `$c-white` |
| `--lime-to-white` | `$c-lime` | `$c-white` |
| `--white-to-mint` | `$c-white` | `$c-lime-150` |
| `--white-to-sand` | `$c-white` | `$c-sand` |
| `--white-to-cream` | `$c-white` | `$c-cream` |
| `--cream-to-mint` | `$c-cream` | `$c-lime-150` |
| `--cream-to-white` | `$c-cream` | `$c-white` |
| `--cream-to-sand` | `$c-cream` | `$c-sand` |

⚠ **`--to-lime` 的上半是 transparent，是刻意的** —— footer CTA 的波浪不知道自己上面是
什么颜色（那是每页的最后一个 section）。写死薄荷色会让 6 个白底收尾的页面在 footer
上方多一条薄荷带。真正以薄荷收尾的 5 页用 `--mint-to-lime`。
线上还有一条 `:has()` 规则专门处理 `.gb-faq` 直接接 footer 的情况。

### 2.4 定位

| 类 | 做什么 | 何时用 |
|---|---|---|
| `--edge` | `position: absolute; bottom: 0` | **默认**。挂在宿主 section 的下边缘 |
| `--edge-top` | `position: absolute; bottom: 100%` | 稿把这个边界画成**下面那个 section 的 Spacer Top**（`236:10300` 在 science 之前、PDP `243:22224` / `316:27135` 开篇各一个） |
| `--bleed` | 只是不画那条实心带 | **唯一特例**：nutrition→PDP（`310:8425`），稿上 frameFill 是 none，让产品图从圆弧缝隙里透出来。宿主必须 `overflow: hidden` |
| （都不加） | 留在文档流里 | footer 与 footer-CTA 的两条 —— 它们本来就是独立的一行 |

---

## 3. ⚠ 每个模块必须自己把波浪的高度加进 `padding-bottom`

**这是最容易漏的一条。** 波浪是绝对定位的，不占布局高度；模块的内容会直接被它盖住，
除非模块自己留出空间：

```scss
.gb-product { padding: 96px 0 calc(96px + var(--sc-h)); }      // 小号波浪
.gb-science { padding: 96px 0 calc(96px + var(--sc-lg-h)); }   // 大号波浪
```

**`--sc-h` 还是 `--sc-lg-h`，取决于这个模块底下挂的是哪一号波浪** —— 换波浪尺寸就
必须同时改这里，否则要么内容被压、要么底部空一大块。

现有的 21 处预留：

| 选择器 | 预留 | 选择器 | 预留 |
|---|---|---|---|
| `.gb-page-hero` | `--sc-lg-h` | `.gb-product` | `--sc-h` |
| `.gb-page-hero--center` | `--sc-h`（经 `--hero-wave`） | `.gb-product--lg` / `--page` | `--sc-lg-h` |
| `.gb-page-hero--lg` | `--sc-lg-h`（同上） | `.gb-reviews--cream` | `--sc-lg-h` |
| `.gb-hero` | `--sc-lg-h` | `.gb-reviews--sand` | `--sc-h` |
| `.gb-logo-scroll` | `--sc-h` | `.gb-vs` | `--sc-h` |
| `.gb-stats` | `--sc-h` | `.gb-app-section` | `--sc-h` |
| `.gb-science` | `--sc-lg-h` | `.gb-app-section--lg` | `--sc-lg-h` |
| `.gb-science--tight` | `--sc-lg-h` | `.gb-expert` | `--sc-h` |
| `.gb-nutrition` | `--sc-lg-h` | `.gb-dosed` | `--sc-lg-h` |
| `.gb-cta-band` | `--sc-lg-h` | `.gb-ingredients` | `--sc-h` |
| | | `.gb-ingredients--lg` | `--sc-lg-h` |

⚠ **`--edge-top` 的空间仍然记在上面那个 section 的 `padding-bottom` 里**，不能跟着节点走：
`--sc-h` 与 `--sc-lg-h` 因边界而异，而 `.gb-science` / `.gb-product` 是多页共用的，
一刀切地在顶部预留会重复计算。

⚠ **不要用 `border-bottom` 或 `::after` 代替**：Chromium 把边框宽度取整（127.979 → 127），
27 条波浪累计丢掉约 25px 页高；`::after` 能用，但每个 section 多一个节点。

---

## 4. 静态站真值表（58 处，23 种组合）

| 宿主 section | 类 | 页面 |
|---|---|---|
| `gb-hero` | `--edge --lg --down --to-white` | index |
| `gb-page-hero` | `--edge --down --to-white` | faq, get-in-touch, privacy-policy, referral, shipping |
| `gb-page-hero` | `--edge --lg --down --to-white` | how-gumi-works, our-story, reviews |
| `gb-page-hero` | `--edge --lg --down --mint-to-cream` | science |
| `gb-logo-scroll` | `--edge --to-cream` | index |
| `gb-science` | `--edge-top --cream-to-sand` | index |
| `gb-science` | `--edge --lg --sand-to-lime` | index |
| `gb-science` | `--edge --lg --cream-to-white` | science |
| `gb-product` | `--edge-top --lg --lime-to-white --bleed` | index |
| `gb-product` | `--edge --lg --white-to-mint` | index |
| `gb-product` | `--edge --lg --white-to-sand` | pdp |
| `gb-product` | `--edge --white-to-mint` | how-gumi-works |
| `gb-reviews` | `--edge --lg --cream-to-white` | how-gumi-works, our-story |
| `gb-reviews` | `--edge --sand-to-white` | pdp |
| `gb-vs` | `--edge --to-cream` | pdp |
| `gb-app-section` | `--edge --cream-to-mint` | pdp |
| `gb-app-section` | `--edge --lg --cream-to-white` | reviews |
| `gb-expert` | `--edge --white-to-cream` | reviews |
| `gb-ingredients` | `--edge --white-to-mint` | reviews |
| `gb-ingredients` | `--edge --lg --white-to-mint` | science |
| `gb-dosed` | `--edge --lg --white-to-cream` | how-gumi-works |
| `gb-cta-band` | `--edge --lg --white-to-cream` | our-story |
| `gb-footer-cta-wrap` | `--to-lime`（流内） | faq, get-in-touch, our-story, privacy-policy, referral, shipping |
| `gb-footer-cta-wrap` | `--mint-to-lime`（流内） | how-gumi-works, index, pdp, reviews, science |
| `gb-footer-wrap` | `--to-green`（流内） | 全部 12 页 |

---

## 5. 线上是怎么暴露的 —— ⚠ 每个 section 各行其是

尺寸和方向**从来不可配**，全部写死在各自的 liquid 里；只有颜色有 select，
而**每个 section 的选项集都不一样**（4 到 15 个不等）：

| section | 尺寸 | 方向 | 颜色 setting | 选项数 |
|---|---|---|---|---|
| `gb-hero` | `--lg` 写死 | `--down` 写死 | `scallop_variant` | 14 |
| `gb-product` | `--lg` 写死 | 朝上 | `scallop_variant` | 14 |
| `gb-reviews` | 小号写死 | 朝上 | `scallop_variant` | 14 |
| `gb-vs` | 小号写死 | 朝上 | `scallop_variant` | 14 |
| `gb-science` | 顶小号 / 底 `--lg` | 朝上 | `leading_` + `trailing_scallop` | 5 |
| `gb-nutrition` | `--lg --bleed` 写死 | 朝上 | `scallop_variant` | 6 |
| `gb-app-section` | `--lg` 写死 | 朝上 | `scallop_variant` | 4 |
| `gb-ingredients` | `--lg` 写死 | 朝上 | `trailing_scallop` | 2 |
| `gb-footer-cta` | 小号写死 | 朝上 | `scallop_variant` | 2 |
| `gb-page-hero` | 小号写死 | `--down` 写死 | **无** — 颜色写死 `to-white` | — |
| `gb-expert` | 小号写死 | 朝上 | **无** — 写死 `white-to-cream` | — |
| `gb-logo-scroll` | 小号写死 | 朝上 | **无** — 写死 `to-cream` | — |
| `gb-dosed` | `--lg` 写死 | 朝上 | **无** — 写死 `white-to-cream` | — |
| `gb-footer` | 小号写死 | 朝上 | **无** — 写死 `to-green` | — |
| `gb-cta-band` | — | — | **线上这个 section 根本没有波浪** | — |

⚠ **`mint-to-cream` 在除 `gb-science` 外的每个 select 里都缺** —— 而它正是 science 页
hero 波浪要的那一对。任何一个 select 都补不出 science 现在的样子。

---

## 6. ⚠ 线上与静态站的 14 处差异（现状记录，未修，等裁决）

`python3 tools/scallopmap.py --password 1234` 的输出，2026-09-08 实测：

### A. 尺寸不对（6 处）

| 页面 | 宿主 | 静态站 | 线上 |
|---|---|---|---|
| how-gumi-works / our-story / reviews / science | `gb-page-hero` | `--lg`，h=**129** | 小号，h=**96.9** |
| pdp | `gb-app-section` | 小号，h=96.9 | `--lg`，h=**129** |
| reviews | `gb-ingredients` | 小号，h=96.9 | `--lg`，h=**129** |

⚠ 这六处**同时也是 padding 的问题**：模块预留的是另一号波浪的高度（§3）。

### B. 颜色不对（2 处）

| 页面 | 宿主 | 静态站 | 线上 |
|---|---|---|---|
| science | `gb-page-hero` | `--mint-to-cream`（薄荷 → 奶油） | `--to-white`（薄荷 → **白**） |
| how-gumi-works | `gb-product` | 小号 `--white-to-mint` | `--lg --white-to-sand` |

### C. 线上完全没有这条波浪（5 处）

| 页面 | 宿主 | 静态站有 |
|---|---|---|
| index | `gb-logo-scroll` | `--edge --to-cream` |
| how-gumi-works | `gb-reviews` | `--edge --lg --cream-to-white` |
| our-story | `gb-reviews` | `--edge --lg --cream-to-white` |
| our-story | `gb-cta-band` | `--edge --lg --white-to-cream`（**线上这个 section 没有波浪节点**） |
| reviews | `gb-app-section` | `--edge --lg --cream-to-white` |

### D. 机制不同（1 处）

**index 的 nutrition→product 边界**：静态站是 `gb-product` 上的
`--edge-top --lg --lime-to-white --bleed`（挂在 product **顶部**，让 nutrition 的产品图
从圆弧缝隙里透出来）；线上是 `gb-product` 底部的 `--edge --lg --white-to-mint`。
**这是两条不同的波浪，不是同一条画错了。**

---

## 7. 加一条新波浪的检查清单

1. **它属于上面那个 section** —— 作为该 section 的最后一个子元素，加 `--edge`。
   （只有稿把边界画成"下面那个 section 的 Spacer Top"时才用 `--edge-top`。）
2. **看稿上的 Spacer 组件 id** 定尺寸和方向，不要看名字，也不要目测。
3. **配色按 `上-to-下`** 挑；上面那块透明就用 `--to-*` 那三个。
4. **给宿主 section 的 `padding-bottom` 加上 `var(--sc-h)` 或 `var(--sc-lg-h)`**，
   与波浪的尺寸对应（§3）。**漏了这步，内容会被波浪盖住。**
5. 上面那块要透出内容 → 加 `--bleed`，并确保宿主 `overflow: hidden`。
6. 跑 `python3 tools/scallopmap.py` 核对类名、实测高度、两个颜色。

## 8. 常见错误

- **只改了波浪的尺寸类，没改模块的 padding** → 内容被盖 / 底下空一块。最常见。
- **用 `--lg` 表示"朝下"** → 每个大号分隔都指错方向。尺寸和方向是两个轴。
- **给 `--wave-bg` 是 transparent 的配色留了 `--wave-under`** → 本该透出的那条实心带被填死。
  `--to-lime` 和 `--bleed` 都显式把 `--wave-under` 设成 transparent。
- **在 Windows 125%/150% 缩放下看到发丝亮线** → 已处理：盒子用 `background-color` 预填下面那块
  的颜色（背景**图片**在分数 dpr 下会差一个设备像素行），再加 `height + 1px` / `margin-bottom: -1px` 的重叠。
- **想用 `border-bottom` 省一个节点** → Chromium 取整边框宽度，全站累计丢约 25px 页高。

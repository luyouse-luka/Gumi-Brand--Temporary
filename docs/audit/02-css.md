# Gumi Brand — CSS 质量审计（第 2 条线）

> 审计日期 2026-08-20，对象 `assets/scss/` 36 个 partial（6025 行）+ 产物 `assets/css/style.css`（163,351 B，r15）。
> **本轮只出报告，未改动任何项目文件。** 唯一写入的是本文件。
> 参照 [AUDIT-HANDOFF.md](../archive/AUDIT-HANDOFF.md) 第 3.4 / 4.2 / 4.4 / 7 节。

---

## 0. 我实际跑了什么

产物与源同步性先验（否则后面所有断言都在审一份过期文件）：

```bash
md5sum assets/css/style.css                     # 060c27f16bbeee6981737f7e9954a512
find assets/scss -name '*.scss' -newer assets/css/style.css   # 空 → scss 无一比产物新
```
并与同目录另一会话新编的 `style-fresh.css` md5 完全一致 —— **产物就是当前源编出来的**。

静态扫描（脚本全部在 `/tmp/claude-1007/-home-ly/c7ffb540-53f6-4bbe-87d6-fe452694dbc5/scratchpad/`）：

| 脚本 | 干什么 |
|---|---|
| `hover_static.py` | 逐字符解析产物，判定每条 `:hover` 规则是否落在 `@media (hover:hover)` 内 |
| `css_dupes.py` | ① 同 media 下重复选择器 ② 块内属性重复 ③ 作用域选择器压死断点覆盖 |
| `css_mq_order.py` | 断点值直方图 + 「窄断点块出现在宽断点块之前」检测 |
| `tokens.py` | 硬编码 hex / rgba / 时长 / 圆角 / cubic-bezier 普查（剔除 `_variables` 与 `_masks`） |
| `deadclass.py` | CSS 里出现的 class ↔ 11 个交付页 + `main.js` 的实际用量 |

⚠ 这个 scratchpad 目录同时有别的审计会话在用（里面还有 `dom_*.json` / `fig_*.json` / `perf-*.json`
等不属于本线的产物），本线的文件是上表这些。

Playwright 探针（chromium 显式 `executable_path=~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome`，
`--allow-file-access-from-files`，`file://` 直开，无 dev server）：

| 脚本 | 覆盖 | 结果文件 |
|---|---|---|
| `hover_probe2.py` | pass 1：11 页 × {1440, 390} × 全部 `a[href]` 与 `button` = **1188 条记录** | `hover_result2.json` |
| `css_hover_pass2.py` | pass 2：补测 pass 1 没被真鼠标到达的 —— 打开 header 面板 / 展开折叠行 / 打开两个弹窗 / 横向轨道滚进视口 = 674 条 | `css_hover_pass2.json` |
| `css_hover_pass3.py` | pass 3：pass 1 选择器漏掉的 `summary`、`select`、`checkbox`、`label`、`.nav-card__action` = 240 条 | `css_hover_pass3.json` |
| `css_faqchk.py` | 单点复现 pass 3 的一条可疑读数 | — |
| `css_trans_check2.py` | 把 `transition-property` 的简写展开后，比对「hover 实际变了的属性」与「被过渡覆盖的属性」 | — |
| `css_verify.py` | promo 卡 gap 实测 / `prefers-reduced-motion` 下的 duration+delay / 6 档宽度横向溢出 | `css_verify.json` |
| `css_edge.py` | 移动抽屉在不同 scrollY 下的几何 / 面板关闭时的 tab 序 | `css_edge.json` |
| `css_git.py` | 单点复现 pass 2 的一条可疑读数 | — |

**判据纪律（铁律 6 / AUDIT-HANDOFF 7.1）**：

- 负向断言先验锚点。hover 探针每页先读 `matchMedia('(hover: hover)').matches` —— **22/22 页 = true**；
  CSSOM 可读规则数 **928，不可读样式表 0**（`file://` 下外链样式表的 `cssRules` 可能被当跨域，这条必须先验）；
  `.btn--primary` 在静态匹配与实测两条路上都测出变化。三个锚点都过了，"没有 hover" 这类断言才有意义。
- 读 hover 后的 computed style 之前注入 `transition-duration: 0s !important`，避免读到过渡中间值；
  但 `transition-property` / `transition-duration` 是在注入**之前**采的。
- 元素是否真被 hover 到，用 `document.elementFromPoint` 反查，分 `ok` / `ancestor` / `covered` / `offscreen` 四类，
  **只有 `ok` 才计入实测结论**，其余交给静态匹配兜底并单独说明。
- 伪元素的 `color` / `border-*-color` 与元素自身 `color` 同增量的变化按**继承**剔除 ——
  不剔的话每个按钮都会假报「::before 没过渡」（第一版就是这么错了 12 个签名，修正后只剩 1 个）。

---

## ① 真缺陷

### P1-1 · mask 的 base64 在产物里各展开了两遍，白扔 12.9 KB（占 style.css 的 7.9%）

**位置**：`assets/scss/modules/_cta-band.scss:34-35`、`assets/scss/modules/_expert.scss:106-107`

```scss
// _cta-band.scss
-webkit-mask: $mask-scallop-band center / 100% 100% no-repeat;
mask:         $mask-scallop-band center / 100% 100% no-repeat;   // ← 同一串 11,573 B base64 再来一遍
```

**判据**：统计产物里每条 `data:` URI 的出现次数与字节数

| URI | 每次字节 | 出现 | 位置 | 小计 |
|---|---|---|---|---|
| `scallop-band` PNG | 11,573 | **2** | `style.css:5674` / `:5675` | 23,146 |
| `scallop-card` SVG | 1,364 | **2** | `style.css:5329` / `:5330` | 2,728 |
| select 箭头 SVG | 259 | **2** | `style.css:5839` / `:5876` | 518 |
| `scallop-box` PNG | 13,577 | 1 | — | 13,577 |

`data:` URI 合计 39,969 B = **产物的 24.5%**（AUDIT-HANDOFF 4.4 记的 27.1 KB 是 SCSS 源里的量，产物里因为重复变成了 39.9 KB）。

**为什么 `scallop-box` 只有一份**：`components/_scallop-box.scss:23` 先 `--box-mask: #{$mask-scallop-box} …`，
再让 `::before` 和 `> img` 各 `var(--box-mask)`。**同一个仓库里已经有正确写法，且已上线验过。**

**建议**：`.cta-band__plate` / `.expert-card__media::after` / `.field__input--select` + `.field__phone select`
照抄这个套路（前两个用局部自定义属性，第三个提一个 Sass 变量）。
**这与「mask 必须内联」的约束完全不冲突** —— 内联的还是同一串 base64，只是不再复制。
净省 12,937 B（11,573 + 1,364），产物 163,351 → 约 150,414 B。
select 箭头那两处体积无所谓，但字面量写了两遍，改箭头颜色要改两处。

---

### P1-2 · `.promo-card--white` 的手机 gap 被作用域选择器压掉，写了不生效

**位置**：`assets/scss/modules/_promo.scss:97-105`

```scss
.promo-card__stack {
  gap: 16px;
  .promo-card--white & { gap: 24px; }   // 0-2-0
  @include mobile { gap: 12px; }        // 0-1-0，媒体查询不加特异性 → 永远输
}
```

作者把 `@include mobile` 写在最后，意图明确是「手机一律 12px」，但 `.promo-card--white .promo-card__stack`
的特异性更高，**白卡在任何宽度下都停在 24px**。

**判据**：Playwright 实测 `pdp.html`（`css_verify.json` → `promo_stack_gap@*`）

| 宽度 | `.promo-card--green` | `.promo-card--white` |
|---|---|---|
| 1440 | 16px ✅ | 24px ✅ |
| **390** | **12px ✅** | **24px ❌（期望 12px）** |

**建议**：在作用域内重述，`_vs.scss:213-219` 与 `_ingredients.scss:55-62` 已经有两处同样的处理并写了注释，照抄：

```scss
.promo-card--white & { gap: 24px; @include mobile { gap: 12px; } }
```

⚠ **手机稿里根本没有这张白卡** —— `figma/nodes/324-53792_pdp-mobile.json` 搜不到
`OUR PROMISE` / `Quality you can trust`（该文件的 TEXT 节点只到订阅区）。
所以「手机端该是 12 还是 24」要设计方定（见 ③-1）；但**「代码写了却不生效」这件事本身是缺陷**，
无论最终取哪个值，都不该靠一条永远打不中的规则来表达。

---

### P2-3 · `.product__cta` hover 改了 `color` 却没给 `color` 过渡（全站唯一一处真·瞬间跳变）

**位置**：`assets/scss/modules/_product.scss:283` + `285-288`

```scss
transition: trans(background-color, transform, box-shadow);   // ← 少了 color
@include hover { background: $c-lime; color: $c-green-900; }  // ← 改了 color
```

**判据**：pass 1 的 750 条「鼠标确实到达 + 有 computed 变化」记录里，把 `transition-property` 的简写展开
（`border-color` → `border-*-color` 等）后逐属性核对，**20 个签名里只有 `.product__cta` 有未覆盖的属性**：
`color` 从 `rgb(255,255,255)` 跳到 `rgb(0,65,40)`，`transition-property` 里没有它。
背景色 0.2s 渐变、文字颜色同一时刻硬切，这是铁律 13 点名的"半成品"写法。

CHANGELOG 第六轮写的是「`cta` 补过渡与抬起」，说明这是漏项不是取舍。

**顺带**：`box-shadow` 列在 `.product__cta` 的 transition 里但 hover 从不改它，是条无用项；
`.product__label-btn:168` 同样列了 `box-shadow` 而 hover 只改 background / color。

**建议**：`transition: trans(background-color, color, transform);`

---

### P2-4 · 三处 `@media (prefers-reduced-motion: reduce)` 块是死代码（被 reset 的 `!important` 压过）

**位置**：`components/_modal.scss:330-333`、`components/_modal.scss:443-448`（时长那几行）、`components/_accordion.scss:92`（`.acc-icon__v`）

`base/_reset.scss:41-46` 已经有全局兜底：

```scss
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration:.01ms!important; animation-iteration-count:1!important; transition-duration:.01ms!important; }
}
```

模块里那几条是 0-1-0 且无 `!important`，**在同一 author origin 下永远输给它**。
后果不是渲染错误，是维护陷阱：将来有人去调模块里的 `0.01ms` 会发现"改了没反应"。

**判据**：Playwright `reduced_motion="reduce"` context 实测（`css_verify.json` → `rm_reduce`）——
`.btn` 与 `.header__panel`（模块里**没有**任何 reduced-motion 规则）也拿到 `transition-duration: 1e-05s`，
证明全局那条对普通元素确实生效；`.nl-panel` / `.acc-icon__v` 的值与之相同，来源无法用读数区分，
但 `!important` 胜出是层叠规则的确定结论。

**⚠ 两个例外必须留下**：

- `.faq__item::details-content` / `.product__acc-item::details-content`（`_accordion.scss:90-91`）——
  全局那条只写了 `*`、`*::before`、`*::after`，**够不着 `::details-content`**，这条是唯一让手风琴在
  reduced-motion 下不做高度动画的规则。
- `.rv-panel { transform: none }`（`_modal.scss:450`）—— 改的是 `transform` 不是时长，全局压不到。

**建议**：删 `_modal.scss:330-333`、`_modal.scss:443-448` 里的 `transition-duration` 行、
`_accordion.scss:92` 里的 `.acc-icon__v`；保留上面两个例外，并在保留处写一句"为什么这条压不到"。

---

### P2-5 · reduced-motion 下弹窗关掉后，看不见的遮罩还挡 0.4s 点击

**位置**：`components/_modal.scss:18`（`.nl-modal`）、`components/_modal.scss:357`（`.rv-modal`）

```scss
.nl-modal { transition: visibility 0s linear $nl-slide; }   // $nl-slide = 0.4s，这是 DELAY 不是 duration
```

全局 reduced-motion 块只压 `transition-duration`，**不压 `transition-delay`**。

**判据**（`css_verify.json`）：

| 元素 | 正常 | reduced-motion |
|---|---|---|
| `.nl-modal` | dur `0s` / **delay `0.4s`** | dur `1e-05s` / **delay `0.4s`（没被压）** |
| `.nl-panel` | dur `0.4s` / delay `0s` | dur `1e-05s` |
| `.nl-modal__overlay` | dur `0.4s` / delay `0s` | dur `1e-05s` |

于是关闭时：面板瞬间落下、遮罩瞬间透明，但 `.nl-modal` 要 **0.4s 后**才 `visibility: hidden`。
这 0.4s 里 `.nl-modal__overlay`（`position:absolute; inset:0`，没有 `pointer-events:none`）
仍然是全屏可命中的，用户点什么都点不到。`.rv-modal` 同理，0.28s。

**建议**：`base/_reset.scss` 的 reduced-motion 块补 `transition-delay: 0s !important;`
（顺带 `animation-delay: 0s !important;`），或在 `_modal.scss` 自己的 reduced-motion 块里把
`.nl-modal` / `.rv-modal` 的 delay 置 0。

---

### P2-6 · 面板收起时导航链接仍在 tab 序里（两个断点都是）

**位置**：`layout/_header.scss:135-166` —— 桌面收起靠 `grid-template-rows: 0fr` + `overflow:hidden`，
移动收起靠 `transform: translateX(-100%)`。两种都**不移出 accessibility tree**，HTML 里也没有
`inert` / `hidden` / `aria-hidden`（`index.html:42` 只有 `id="site-menu"`）。

**判据**（`css_edge.json`）：焦点放在 `.header__toggle` 上、面板保持关闭，连按 8 次 Tab

| 宽度 | 落进面板的次数 | 落点 |
|---|---|---|
| 1440 | **4 / 8**（第 5~8 次） | `How Gumi Works` / `Science` / `Reviews` / `Manage Account`，rect 全部是 `y=99 h=42`（0fr 塌成同一位置），焦点框被 `overflow:hidden` 裁掉，屏幕上看不到 |
| 390 | **5 / 8**（第 4~8 次） | `Shop` / `How Gumi Works` / `Science` / `Reviews` / `Learn more`，rect `x = -370`，全在屏幕外 |

键盘用户会"焦点消失"5 次才能走到页面内容。

**建议**：CSS 侧给收起态加 `visibility: hidden`（配合 `transition-behavior: allow-discrete` 或把
visibility 的过渡延后 —— `.nl-modal:16-23` 已经是这个套路，照抄即可），或 JS 侧给 `.header__panel` 挂 `inert`。
⚠ 这条与 UX/a11y 审计线重叠，若那条线也报了以那边的处置为准。

---

### P2-7 · 大按钮的几何值被抄了两遍，`grep 'btn--lg'` 找不齐

**位置**：`layout/_footer.scss:88-107` ↔ `components/_button.scss:40-55`；`modules/_hero.scss:83-107` ↔ `components/_button.scss:59-74`

HTML 里是 `class="btn footer-cta__btn"` / `class="btn hero__btn"` —— **没挂 `btn--lg` / `btn--xl`**，
于是 52/60 高、`padding: 0 64px`、`line-height: 28px`、`letter-spacing: .48px`、`text-transform: capitalize`、
`border-radius: 72px` 这一整套值在两个文件里各存在一份。

**判据**（铁律 4 的判据）：设计方将来改大按钮尺寸，`grep -rn 'btn--lg' assets/scss` 只会命中
`components/_button.scss`，footer 那份改不到。

全站 8 类大按钮里 6 类重复了同一组几何：`.btn--lg` / `.btn--xl` / `.footer-cta__btn` / `.hero__btn` /
`.cta-band__btn` / `.promo-card__btn`，另加两个根本不走 `.btn` 的 `.product__cta`（`_product.scss:268-290`）
与 `.product__label-btn`（`:150-175`）。

**建议**：HTML 改成 `btn btn--lg footer-cta__btn` / `btn btn--xl hero__btn`，模块里只留差异
（footer 的白底 hover、hero 的 `align-self` 与 mobile 尺寸）。P2-3 那个 bug 正是这条的直接后果 ——
`.product__cta` 因为不是 `.btn`，没吃到 `.btn` 基类里已经写对的 `trans(…, color, …)`。

---

### P2-8 · `border-radius: 72px` 硬编码 6 处，而 `$r-pill` 定义在那儿没人用

**位置**：`_footer.scss:94`、`_footer.scss:209`、`_hero.scss:89`、`_product.scss:159`、`_product.scss:276`、`_promo.scss:208`

`helpers/_variables.scss:78` 有 `$r-pill: 999px`，只被 `.btn`、`.nl-tag`、`.rv-panel__close` 用到。
72px 在 52~60px 高的元素上与 999px 视觉等价，两套写法并存没有理由。

**建议**：统一走 `$r-pill`；或者显式加一个 `$r-btn: 72px // 稿里的原值` 并全部引用它。

---

### P2-9 · 几组颜色字面量重复，且已有同族 token

**判据**（`tokens.py`，已剔除 `_variables.scss` 与 `_masks.scss`）：全站硬编码 hex 只有 **6 处 / 4 个值**、
rgba **11 处 / 8 个值** —— 整体 token 纪律是好的，下面这几组是仅有的重复：

| 值 | 处数 | 位置 | 备注 |
|---|---|---|---|
| `rgba(1, 19, 7, 0.1)` | 3 | `_footer.scss:194`、`_compare.scss:123`、`_vs.scss:209` | 发丝分割线。`$c-ink-05`（同色 5%）已存在，缺一个 `$c-ink-10` |
| `rgba(0, 86, 53, 0.15)` | 2 | `_form.scss:77`、`_form.scss:111` | 表单 focus ring，属"稿里没有、房子里定的"（3.4.F） |
| `#cbf390` | 2 | `_header.scss:345`、`_product.scss:219` | 标签底色，是 `$c-lime` 与 `$c-lime-200` 之间的一档，没进色板 |
| `#656565` | 2 | `_form.scss:154`、`_form.scss:197` | 与 `$c-gray-600: #666666` 相差 1，是稿里的真值，值得单独起名 |
| `#808080` / `#e6e6e6` | 各 1 | `_rich-text.scss:65`、`_modal.scss:181` | 各只用一次，可不动 |

---

### P2-10 · 同一选择器连着写了两个块

- `modules/_faq.scss:115` + `:117`（`.app-slot` 先 `width:100%` 再一整块）→ 产物 `style.css:5050` / `:5054`
- `components/_modal.scss:165` + `:177`（`.nl-panel__body`，第二块只放 `::-webkit-scrollbar`）

**判据**：`css_dupes.py` 第 1 段。同时它证明了一件好事 —— **块内属性重复 = 0 处**，没有"后面覆盖前面"的死声明。

顺带：`.app-slot`（`_faq.scss:117-131`）与 `.product__app-slot`（`_product.scss:256-265`）是同一套
虚线占位样式的两份拷贝（`1px dashed $c-gray-300` / `$r-lg` / `$c-gray-500` / 14-22--0.28），可提成一个 placeholder。

---

### P2-11 · `.product__acc-item` 的 `display` 被跨文件覆盖，前一份成了死声明

`components/_accordion.scss:19-23` 写 `.faq__item, .product__acc-item { display: block; interpolate-size: allow-keywords; }`（产物 `style.css:505`），
`modules/_product.scss:335-338` 后面又写 `.product__acc-item { display: flex; flex-direction: column; }`（产物 `style.css:3839`）。
同特异性、后者在后 → `display: block` 对 `.product__acc-item` 从来没生效过（对 `.faq__item` 仍有效）。

**建议**：把分组拆开，或在 `_product.scss` 那处注明"这里故意换成 flex"。现状是两个文件对同一个元素的
`display` 各有主张，只有编译顺序在裁决。

---

### P2-12 · 死代码清单

**判据**：`deadclass.py`（CSS 出现的 458 个 class ↔ 11 个交付页的 434 个 class token + `main.js` 字符串常量）
+ Sass 变量 / mixin 引用计数。`.png` / `.woff2` / `.org` / `.w3` 是 URL 里的假阳性，`.is-off` 在
`main.js:122` 有用，均已剔除。

| 类别 | 明细 |
|---|---|
| 无人使用的 class | `.page-hero--text`（`layout/_page-hero.scss:132-135`，11 页全部走 `--center`）、`.field__control`（`modules/_form.scss:56`）、`.no-js`（`components/_motion.scss:107`，没有任何 HTML/JS 加这个 class；真正生效的兜底是同一条规则里的 `[data-pop-text]:not(.is-split)`）、`.show-c`（`helpers/_animation.scss:2-13`，块内容与紧随其后的 `.wowo` 块**逐字相同**，Terra 移植残留） |
| 无人使用的入场动画类 | `.fadeInDown` `.fadeInLeft` `.fadeInRight` `.zoomIn` `.zoomOut` `.bounceIn`（`helpers/_animation.scss:157-203`，连同各自的 `@keyframes`） |
| 无人使用的延迟类 | `.delay-in-4` ~ `.delay-in-20`（17 个，`helpers/_animation.scss:205-213` 的 `@include AnimationDelay` 生成 20 个，HTML 只用到 1~3） |
| 从未调用的 mixin | `font`（`_mixins.scss:70`）、`line-clamp`（`:78`）、`small`（`:9`）、`touch`（`:12`）、`visually-hidden`（`:93`） |
| 只定义未使用的 Sass 变量（17 个） | `$bp-desktop` `$bp-small` `$c-gold` `$c-gray-100` `$c-gray-850` `$c-lilac` `$color-accent` `$color-bg-alt` `$color-border` `$color-text-muted` `$font-display-stack` `$font-hand-stack` `$font-ui-stack` `$r-md` `$w-design-mobile` `$z-base` `$z-overlay` `$z-sticky` |

其中 `@mixin small` 从未调用，`$bp-small: 480px` 就成了一个**从未参与过任何决策的断点**；
`$z-base` / `$z-sticky` / `$z-overlay` 三个 z-index token 也没人用，实际代码里用的是裸 `0/1/2/3/-1`。

**⚠ 不要一刀切删这两处**（注释里已写明用途，属于②）：

- `.logo-scroll--off`（`modules/_logo-scroll.scss:17`）—— Shopify 主题开关的钩子（Figma 批注 `401:29602`）。
- `.promo-art--live` 整段（`modules/_promo.scss:287-349`，**65 行**）—— 只给 `figma/promo-art-source.html`
  用来重新渲染 `images/promo-art.png`。注释写得很清楚，但它确实会随 `style.css` 发给每个访客。
  建议 Shopify 阶段把这段挪进一个不进 `style.scss` 的独立文件。

---

### P2-13 · `:root` 的自定义属性散在三个文件，且其中一个叫 `_mixins`

`base/_reset.scss:3`（`--build`）、`helpers/_mixins.scss:54-59`（`--pad-x` 及其两个断点）、
`components/_motion.scss:20-29`（三条缓动曲线）。产物里 `:root` 出现 3 次（`style.css:93` / `:169` / `:1094`）。

`grep -rn ':root' assets/scss` 能一次找齐，所以**不违反铁律 4**；但
`helpers/_mixins.scss` 是个"名字叫 mixins、却会吐出 CSS 规则"的 partial，它的输出位置取决于
**谁第一个 `@use` 它**（当前落在 `style.css:169`）。把 `--pad-x` 挪到 `_variables.scss`
或新开 `helpers/_root.scss`，目录语义会更稳。

---

### P2-14 · 两处注释与代码不符

- `layout/_header.scss:314-315`：注释写 `// Large surface, so it takes the slower ramp`，
  下一行却是 `transition: trans(background-color, border-color)`。`trans()`（`helpers/_mixins.scss:43-49`）
  **写死 `$t-base`（0.2s）**，拿不到 `$t-slow`。要么改注释，要么给 `trans()` 加一个时长参数。
- `components/_modal.scss:335-336`：注释写 "html is the scroll container here (the reset puts overflow-x on it)"，
  但 `base/_reset.scss:18` 把 `overflow-x: hidden` 放在 **body**，不是 html。
  （功能上没问题 —— html 的 overflow 是 visible，body 的会传播到 viewport；但注释指错了地方，
  下一个人照着这句去 `_reset.scss` 找 html 会找不到。）

---

### P2-15 · `.reel` 的 `cursor: pointer` 冗余

`modules/_reviews.scss:112`。`.reel` 在 HTML 里 20 处全是 `<button>`，
`base/_reset.scss:35` 的 `button { cursor: pointer }` 已经覆盖。
第六轮清过 10 处同类冗余（CHANGELOG），这条漏了。
（`.faq__row` / `.product__acc-row` 上的 `cursor: pointer` **要留** —— 它们是 `<summary>`，UA 默认不是 pointer。）

---

### P2-16 · 两个 `<select>` 和 consent 那块 `<label>` 能点但没有任何 hover 反馈

**位置**：`modules/_form.scss:82-89`（`.field__input--select`）、`:114-130`（`.field__phone select`）、`:147-172`（`.form__check`）

pass 1 的选择器是 `a[href], button`，把这几类漏掉了；pass 3 补测（`summary` / `select` / `checkbox` / `label`）后发现：

| 元素 | 实测 | 说明 |
|---|---|---|
| `summary.faq__row` | 64 条实测**全部有变化**（color → `$c-green`，`svg` `scale(1.15)`；其中 1 条初报 no-change，单点复现后推翻） | ✅ 之前没测过，现在补齐了 |
| `summary.product__acc-row` | 50 条实测**全部有变化** | ✅ |
| `select.field__input--select`（Enquiry Type） | **hover 前后 computed style 完全一致** | ❌ |
| `.field__phone select`（国家码 AU） | **完全一致** | ❌ |
| `label.form__check`（consent 整块） | **完全一致**，且 label 自身没有 `cursor: pointer` | ❌ |

两个 select 都写了 `appearance: none`（`_form.scss:83` / `:115`），**原生外观已被完全接管**，
浏览器不会再画自己的 hover 高亮 —— 也就是说这两处鼠标划过去毫无反应，只有 `:focus-visible` 时才有边框变化。
产物里 41 条 `:hover` 规则中没有任何一条命中 `select`（静态核对过选择器清单）。

`label.form__check` 是**包住 checkbox 的 label**（`get-in-touch.html:157-160`），
点文字也会勾选，属于「可点的」；但 `cursor: pointer` 只加在里面那个 20px 的 `input` 上
（`_form.scss:162`），label 其余部分是默认箭头。这正好踩中铁律 13 的反面
「可点的别漏 `cursor:pointer`」。

**建议**：
- 两个 select 加 `@include hover { border-color: $c-gray-500; }`（或与 focus 同族的浅一档），
  它们已经有 `transition: trans(border-color, box-shadow)`，加 hover 即可，不用再写过渡。
- `.form__check` 把 `cursor: pointer` 从 `input[type="checkbox"]` 提到 label 本身，
  并给 `@include hover { color: … }` 之类的轻反馈。

**不列为缺陷的**：`input[type="checkbox"]` 没写 `appearance:none`，保留原生控件，
Chrome 自己会画 hover 高亮 —— 我的探针读元素 computed style 读不到 UA 绘制，
所以这里"无变化"**不能**推出"无反馈"。同理 `label.field__label`（`for=` 关联的普通字段标签）
没有 hover 是业界常规，不当缺陷报，只在 ③ 里提一句要不要统一。

---

### P2-17 · motion token 之外还散着 3 个时长 + 1 条曲线

`helpers/_variables.scss:82-87` 定义了 `$t-fast/.15s` `$t-base/.2s` `$t-slow/.3s` + `$ease-out` `$ease-in-out`，
但下面这些没走 token：

| 值 | 位置 | 用途 |
|---|---|---|
| `0.35s` | `layout/_header.scss:146` | 导航面板 `grid-template-rows` 展开 |
| `$nl-slide: 0.4s` + `cubic-bezier(0.32,0.72,0,1)` | `components/_modal.scss:10-11` | 营养标签面板上滑 |
| `$rv-in: 0.28s` | `components/_modal.scss:350` | reel 灯箱淡入 |

三处都有注释说明"稿里没有、是房子里定的"，但按项目纪律（AUDIT-HANDOFF 4.2「时长/曲线取 motion token，
不各处自己填 `0.3s ease`」）应该收进 `_variables.scss` 的 motion 段。
另：`layout/_header.scss:146` 的 `0.35s` 是**唯一一处连局部变量都没有的裸时长**。

**不适用这条的**：`components/_motion.scss` 那一组（1.5s / 5s / 0.72s / 55ms / 两条 `back.out` 的
`linear()` 采样）是从参考站 cravburgers.shop 抄的动效参数，已经集中在一个文件顶部并写了出处，保持现状即可。

---

## ② 有意为之 / 待裁决（只写有新证据的）

按交接文档要求，3.4 与 4.4 里已经写明的不重复。下面三条是**我这轮有新数据、值得更新那两节**的：

1. **4.4.1 mask 内联 —— 数字要更新，结论不变。**
   交接文档记的 27.1 KB 是 SCSS 源里的量。产物里因为 `-webkit-mask` / `mask` 各写一遍，实际是
   **39,969 B = style.css 的 24.5%**，其中 12,937 B 是纯重复。见 P1-1。
   **仍然不建议改回 `url()` 外链** —— 那条约束我没有任何相反证据。

2. **4.4.4「317 个 @media 分散在各 partial，如果你要审重复度，这是入口」—— 查过了，没问题。**
   - 断点值**没有漂**：产物里只有 3 个 `max-width`（768 / 1024 / 1200）和 2 个 `min-width`（1025 / 1120），
     没有 767/768 混用。`min-width: 1025px` 与 `max-width: 1024px` 严丝合缝，无重叠无空隙。
     `min-width: 1120px`（`_product.scss:82`）是唯一的一次性断点，注释里有 break-even 计算。
   - **没有一处"窄断点块写在宽断点块之前"**（`css_mq_order.py`，0 命中）—— 也就是没有
     "在 800px 下被 1200px 的块覆盖"这种顺序 bug。
   - **BEM block 跨 partial 的只有 5 个**：`faq`（accordion + faq + faq-image）、`product`（accordion + product）、
     `btn`（button + ingredients）、`promo-art`（promo + ingredients）、`is-open`（modal + header），
     每一处源码里都有注释交代。**铁律 4 的"一条 grep 找齐"基本成立。**
   - 唯一真的漏网是 P1-2 那条作用域压死断点的规则，全站扫描后**只有那 1 处**
     （另有 `.page-hero__text` 的 `width:auto` 在 ≤1024 被 `.page-hero--center .page-hero__text{width:100%}` 压掉，
     但那是 flex 单项容器，`auto` 与 `100%` 用值相同，无视觉后果；且 `.page-hero--text` 本身是死 class）。

3. **4.3 基线 `:hover` 41 / `transition` 53 —— 数字对，且可以再加一条更强的结论。**
   我逐字符解析产物，**41 条 `:hover` 规则 100% 落在 `@media (hover: hover)` 内，0 条直接写 `&:hover`**。
   包括 `layout/_header.scss:379-381` 那条手写的 `@media (hover:hover) { .nav-card:hover & }` ——
   它没用 `@include hover` 是**对的**（`@include hover` 会把 `:hover` 加到 `.nav-card__action` 自己身上，
   而这里要的是父级 hover），不是漏网。
   `transition` 那 53 处里，`transition:` 简写 47 条、`transition-duration`/`-delay` 6 条；
   47 条简写经 `trans()` 展开后实际覆盖 **69 组属性-时长对**。

另外，**伪元素副作用一项没查出问题**，记录一下判据免得下轮重查：

- 会生成内容的伪元素只有 6 个：`link-underline` 的 `::after`（`_mixins.scss:24`）、
  `.vs__col--gumi::before`（`_vs.scss:95`）、`.compare__row::before`（`_compare.scss:118`）、
  `.scallop-box::before`（`_scallop-box.scss:28`）、`.expert-card__media::after`（`_expert.scss:97`）、
  `.nl-tab::after`（`_modal.scss:144`）。其余全是 `::-webkit-scrollbar` / `::marker` / `::placeholder` / `::details-content`。
- **窄屏没有漏关**：`.vs__col--gumi::before` 与 `.expert-card__media::after` 各自带 `@include mobile` 重设几何；
  其余几个在两个断点下形态相同（本来就该相同）。
- **没有盖住可点区**：三遍探针一共 1368 次 `elementFromPoint` 命中测试，
  没有任何一次是被伪元素挡住的（`covered:` 的对象全是"面板闭合时压在上面的 header/页面容器"
  或"横向轨道里相邻的卡片"，逐条核对过）。
- **没有造成溢出**：见下条。
- 唯一可以顺手加的：`link-underline` 的 `::after` 没有 `pointer-events: none`，
  `bottom: -3px` 会让 footer 链接的命中区向下多出 4px（`gap` 是 12px）。
  base 态是 `scaleX(0)`（退化矩阵不参与命中测试），所以**实际不构成问题**，加一行只是保险。

**移动抽屉的"滚下去再开菜单会不会开到屏幕外" —— 查过了，是有界的，不报缺陷。**
`.header` 是 `position: relative`（`_header.scss:34`）不是 sticky，抽屉 `position:absolute; top:100%`，
`main.js` 的 `header.set()` 也不回滚顶部，所以理论上滚动后开菜单抽屉会整体上移。
实测（`css_edge.json`，390×844）：

| 请求 scrollY | 实际 | toggle 顶边 | 能否打开 | 抽屉 top / bottom |
|---|---|---|---|---|
| 0 | 0 | 52 | 是 | 96 / 844（正好铺满） |
| 50 | 50 | 2 | 是 | 46 / 794（底部空 50px） |
| 90 | 90 | −38 | **否**（汉堡已滚出视口） | — |

也就是说：**能打开菜单的最大滚动量就是 header 还露着的那段（≤88px）**，
最坏情况是抽屉底部空掉 ≤88px，且抽屉自己有 `overflow-y: auto`，内容不会够不着。
真机上 `100svh < innerHeight` 会让这个余量更明显，但仍然是"底部留白"而不是"开到屏幕外"。
要彻底消掉的话得让 `.header` 变 sticky —— 那是设计决定，不是 CSS 缺陷，先记录不改。

**横向溢出复核**（这是 AUDIT-HANDOFF 7.3 的 55/55，我用自己的探针独立重跑并扩到 1920）：

| 宽度 | 1920 | 1440 | 1200 | 1024 | 768 | 390 |
|---|---|---|---|---|---|---|
| 有横向溢出的页数 | 0/11 | 0/11 | 0/11 | 0/11 | 0/11 | 0/11 |

判据是 `documentElement.scrollWidth > clientWidth + 1`，并同时列出所有 `right > vw+1` 或 `left < -1`
的非 fixed 元素（全为空）。**66/66 全绿。**

---

## ③ 需设计方给值

1. **`.promo-card--white` 手机端的 stack 间距是 12px 还是 24px。**
   手机稿 `324:53792` 里没有这张白卡（`figma/nodes/324-53792_pdp-mobile.json` 无
   `OUR PROMISE` / `Quality you can trust` 文本节点），桌面稿 `324:52658` 的对应 frame 是
   `itemSpacing = 24`。现在的实际表现是 24（因为规则打不中，见 P1-2）。
   两条路都要修 —— 值定了以后仍必须把规则写进作用域里才生效。

2. **三个游离时长 + 一条游离曲线要不要收进统一 motion token**（P2-17）：
   导航面板 `0.35s`、营养标签面板 `0.4s + cubic-bezier(.32,.72,0,1)`、reel 灯箱 `0.28s`。
   这三处都是 3.4.F 里"稿里没有、本项目自定"的范畴，收进 token 会改变观感，需要设计方点一次头
   （是保持三档各异，还是统一到 `$t-fast/$t-base/$t-slow`）。

3. **`#cbf390` 这一档绿要不要进色板**（P2-9）。它出现在 header 的 `NEW` 标签和 PDP 的产品标签上，
   夹在 `$c-lime`(#b5ed61) 和 `$c-lime-200`(#daf6b0) 之间，目前是两处裸 hex。

4. **两个 `<select>` 与 consent `<label>` 的 hover 态长什么样**（P2-16）。稿里没有交互态（3.4.F），
   我按现有 focus ring 的同族给了建议值（border 深一档），但配色要设计方拍。
   顺带确认一下 `label.field__label`（普通字段标签，`for=` 关联可点）要不要一起给 hover ——
   现在没有，业界也多数没有，我按"不是缺陷"处理了。

---

## ④ 交互态全量清点（第 5 项独立工作）

**范围**：11 个交付页 × {1440, 390} × 全部 `a[href]` 与 `button`，另加 pass 3 补的 `summary` / `select` /
`checkbox` / `.nav-card__action`。

**锚点（先验，否则负向断言恒真）**：

| 锚点 | 结果 |
|---|---|
| `matchMedia('(hover: hover)').matches` | **22/22 页 = true** |
| CSSOM 可读规则数 / 不可读样式表 | **928 / 0**（`file://` 跨域拦截没发生） |
| 产物里的 `:hover` 规则数 | 41（与 `grep -c` 一致） |
| `.btn--primary` 静态匹配 + 实测 | 两条路都测出 background/color 变化 |

**结论数字**：

| 项 | 值 |
|---|---|
| 记录总数 | pass 1 **1188** + pass 2 **674** + pass 3 **240** = **2102** |
| 其中 pass 1 覆盖 | 11 页 × 2 宽度 × 全部 `a[href]`/`button`（1440 宽 604 条 + 390 宽 584 条） |
| 去重后的可交互类型 | `a[href]`/`button` **30 类** + `summary` 2 类 + `select` 2 类 + `label` 2 类 + `input[type=checkbox]` 1 类 |
| 静态匹配：hover 它不触发任何规则的**可见** `a`/`button` | **0** |
| 实测：鼠标确实到达（`elementFromPoint == ok`）的记录 | 750 + 426 + 192 = **1368** |
| 其中 `a` / `button` / `summary` **hover 后无任何变化** | **0**（两条初报的 no-change 单点复现后都推翻了，见下） |
| **能点但没有 hover 反馈** | `a`/`button`/`summary`：**0 处**；表单控件：**3 类**（2 个 `select` + `label.form__check`，P2-16） |
| **有 hover 但该属性没有 transition** | **1 处** —— `.product__cta` 的 `color`（P2-3） |
| 直接写 `&:hover`、没包 `@media (hover:hover)` 的 | **0 处**（41/41 都包着，触摸屏不会粘住） |
| 引用了不存在 class 的死 hover 规则 | **0 条**（41 条选择器里的 class token 全部在交付页 HTML 中出现） |

**pass 3 补测的明细**（pass 1 的 `a[href], button` 选择器够不到的）：

| 元素 | 实测到达 | 有 hover 变化 |
|---|---|---|
| `summary.faq__row` | 64 | **64**（其中 1 条初报 no-change，单点复现该页 6/6 全变，已推翻） |
| `summary.product__acc-row` | 50 | **50** |
| 表单内裸 `<a>`（friendly privacy policy / Sign In / Privacy / Cookies） | 48 | **48** |
| `select.field__input--select` | 2 | **0** ❌ |
| `.field__phone select` | 4 | **0** ❌ |
| `label.form__check` | 2 | **0** ❌ |
| `label.field__label` | 20 | 0（按业界常规不计缺陷，见 P2-16 末尾） |
| `input[type=checkbox]` | 2 | 0（原生控件，UA 自绘 hover，探针读不到，**不能据此下结论**） |
| `span.nav-card__action` | 0（`ancestor`/`offscreen`） | 由 `.nav-card:hover .nav-card__action` 覆盖，pass 2 在 `.nav-card` 上实测 44 次全有变化 |

**没被真鼠标到达的怎么处理的**（不算进"无反馈"，逐类核对过原因）：

| 类别 | 原因 | 补测结果 |
|---|---|---|
| `.header__link` / `.header__sublink` / `.nav-card` / `.btn--lg`(Manage Account) | pass 1 时面板是关的 | pass 2 打开面板 + 展开折叠行后全部实测到，**全部有变化** |
| `.reel` | 横向 snap 轨道里出屏，探针把鼠标坐标夹到视口边缘打到了邻卡 | pass 2 把轨道滚进视口后实测 47 次 + pass 1 的 112 次，**全部有变化** |
| `.nl-tab` / `.nl-panel__close` / `.rv-panel__close` | 弹窗没开 | pass 2 开弹窗后实测，**全部有变化** |
| `.header__cta`(390) / `.header__sublink`(1440) / `.ingredients__desktop-only`(390) | 断点 `display:none`，是设计要的 | 在另一断点实测到 |
| `.cta-band__btn` / `.promo-card__btn`（pass 1 报 `ancestor`） | `wowo fadeInUp` 入场动画未落位，量到的 rect 比最终位置低 30px | pass 2 加 1000ms 沉降等待后实测到，**有变化** |

⚠ **两条被推翻的读数（记录在案，免得下轮重查）**：

1. pass 2 有 11 条 `<button class="header__link">Get in Touch</button>`（11 页 × 390 宽）报 `hit=ok` 但 `nochange`。
   单点复现（`css_git.py`）显示它**确实有 hover**：`color` `rgb(1,19,7)` → `rgb(71,172,0)`，
   与同一 class 的 `Learn more` 表现一致。是 pass 2 里"先点开两个折叠行导致布局位移"造成的探针噪声。
2. pass 3 有 1 条 `summary.faq__row 'Accordion Closed'`（faq@390）报 `nochange`。
   单点复现（`css_faqchk.py`）把该页 6 行逐个测了一遍：**6/6 都变**
   （`color` `rgb(1,19,7)` → `rgb(0,86,53)`，`svg` `none` → `matrix(1.15,…)`）。同样是布局位移噪声。

两条都**不是缺陷**，最终计数已按复现结果记 0。这也说明：批量遍历探针在「hover 会改变布局 / 元素刚被
展开」的场景下必然有噪声，**任何 no-change 读数都要单点复现过才能写成结论**。

---

## ⑤ 现状基线数字表（供下一轮对照）

| 指标 | 实测值 | 与 AUDIT-HANDOFF 4.3 对照 |
|---|---|---|
| `assets/css/style.css` 字节 | 163,351（未压缩） | — |
| 规则块（`{` 计数） | 1,311 | — |
| `!important`（CSS） | **3** —— 全部在 `base/_reset.scss:43-45` 的 reduced-motion 块，**必要且正确** | 3 ✅ |
| `!important`（HTML `<noscript>`） | 11（每页 1 处 `.wowo{opacity:1!important}`） | 文档未计 |
| `z-index` 声明（产物） | **14**（源码 13 条，`ink-split` 里的 `-1` 编译成 2 份） | 14 ✅ |
| `@media` 块 | **317** = 768px×206 + 1024px×54 + `hover:hover`×37 + 1200px×10 + `reduced-motion`×8 + `min-width:1025`×1 + `min-width:1120`×1 | 317 ✅ |
| 断点值种类 | 5（`max-width` 768 / 1024 / 1200，`min-width` 1025 / 1120），**无 767/768 混用，无区间重叠或空隙** | — |
| 窄断点块写在宽断点块之前的 | **0 处** | — |
| `:hover` | **41**，其中在 `@media (hover:hover)` 内 **41（100%）** | 41 ✅ |
| `transition` | **53** = `transition:` 简写 47 + `transition-duration`/`-delay` 6；展开后 69 组属性-时长对 | 53 ✅ |
| `@include hover` 调用 | 33（另有 1 处手写 `@media (hover:hover)`，见②-3） | — |
| `@include mobile / tablet / laptop / desktop-up` | 205 / 53 / 10 / 1（`small` 与 `touch` **0 次**） | — |
| 硬编码 hex（剔除 `_variables`/`_masks`） | **6 处 / 4 个值**（`#cbf390`×2、`#656565`×2、`#e6e6e6`、`#808080`） | — |
| 硬编码 `rgba()` | **11 处 / 8 个值**（最高频 `rgba(1,19,7,.1)`×3） | — |
| 硬编码 `border-radius` | **22 处 / 14 个值**（最高频 `72px`×6） | — |
| 硬编码 `cubic-bezier()` | 5（`_variables` 2 条是 token，`_motion` 3 条是参考站移植，`_modal` 1 条游离） | — |
| transition/animation 里的时长字面量 | 25 处 / 14 个值 | — |
| `data:` URI 总量 | **39,969 B = 产物的 24.5%**，其中 **12,937 B 是重复** | 源码 27.1 KB |
| 同 media 下重复的选择器条目 | 36（多数是"分组规则 + 单独规则"的正常形态，真该合并的 2 处：`.app-slot`、`.nl-panel__body`） | — |
| 块内属性重复（死声明） | **0 处** | — |
| 跨文件同选择器冲突 | 1 处（`.product__acc-item` 的 `display`） | — |
| 无人引用的 class | **27 个** = 6 个动画类 + 17 个 `delay-in-N` + `.show-c` / `.page-hero--text` / `.field__control` / `.no-js`；另 **6 个有意保留**（`.logo-scroll--off` 与 `.promo-art--live` 那组 5 个） | — |
| 从未调用的 mixin | 5（`font` `line-clamp` `small` `touch` `visually-hidden`） | — |
| 只定义未使用的 Sass 变量 | 17 | — |
| BEM block 跨 partial 的 | 5 个（全部有注释交代） | — |
| 横向溢出（1920/1440/1200/1024/768/390 × 11 页） | **0 / 66** | 55/55 ✅（已扩到 66） |
| 交互态探针记录数 | **2102**（pass1 1188 + pass2 674 + pass3 240），真鼠标到达 **1368** | 上一轮是 2 页 46 类 |
| 能点但无 hover 反馈 | `a`/`button`/`summary` **0**；表单控件 **3 类** | — |
| 有 hover 但无 transition | **1**（`.product__cta` 的 `color`） | — |
| `:hover` 未包 `@media (hover:hover)` | **0** | — |
| `prefers-reduced-motion` 收尾 | 全局兜底**有**（`_reset.scss:41-46`，3 个 `!important`）；模块级 8 个块中 **3 个是死代码**（P2-4），**delay 未被压**（P2-5） | — |

---

## ⑥ 建议的处理顺序

| 序 | 条目 | 改动面 | 风险 |
|---|---|---|---|
| 1 | P2-3 `.product__cta` 补 `color` 过渡 | 1 行 | 无 |
| 2 | P1-2 `.promo-card--white` 的 gap 在作用域内重述 | 2 行（值待设计方定） | 无 |
| 3 | P1-1 三处 mask/SVG 走自定义属性去重（省 12.9 KB） | 6 行，仓库内已有同款写法 | 低 |
| 4 | P2-5 reduced-motion 块补 `transition-delay: 0s !important` | 1 行 | 低 |
| 5 | P2-4 删三处被 `!important` 压死的 reduced-motion 规则（**保留两个例外**） | 删 8 行 | 低，改完要在 reduce 模式下回归手风琴与弹窗 |
| 6 | P2-16 两个 `select` + `label.form__check` 补 hover / `cursor:pointer`（值待设计方，③-4） | 3 处各 2~3 行 | 无 |
| 7 | P2-6 面板收起态加 `visibility:hidden` 或 `inert` | 数行 + 需与 UX 线对齐 | 中，会碰到过渡时序 |
| 8 | P2-7 大按钮挂回 `btn--lg` / `btn--xl` | 11 个 HTML + 2 个 scss | 中，改完必须做全站 computed-style 快照比对（含伪元素） |
| 9 | P2-8~15、P2-17 token 化与死代码清理 | 分散 | 低，但同样要 computed-style 快照兜底 |

⚠ 第 3 / 8 / 9 项动的是**结构与顺序**，按铁律 6：**diff 产物无效**，
判据必须是全站 computed-style 快照且**包含 `::before` / `::after`**（本项目大量用伪元素画线）。
本轮的 `hover_probe2.py` 已经在采 `::before` / `::after` 的 11 个属性，可以直接改成"改前改后各跑一遍再 diff"。

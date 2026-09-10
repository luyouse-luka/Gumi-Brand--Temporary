# Gumi Brand — 交接

> 一份文档管三种会话：**接手做需求** / **对稿复查** / **做审计**。
> 项目定位与已确立的规范在 [PROJECT-STATUS.md](PROJECT-STATUS.md)；
> 改动史在 [CHANGELOG.md](CHANGELOG.md)（近 10 轮）+ [CHANGELOG-ARCHIVE.md](CHANGELOG-ARCHIVE.md)（第一～一一七轮），**两份一起 grep**。
> **更早轮次的状态段**（第七十三～一二三轮）在 [archive/HANDOFF-STATUS-r73-r123.md](archive/HANDOFF-STATUS-r73-r123.md)；其中的「不要报成 bug」已原文沉淀进下面第一节的 `### 4`。
> **推送记录**（推了什么 / 验了没 / 基线滚到哪）在 [PUSH-LOG.md](PUSH-LOG.md)。
>
> 状态：**第一三六轮（2026-09-10）—— 从 `/cart` 进来的抽屉关不掉（组件与内层 dialog 状态分裂），`$build` = `20260910-r136`，已推 live**。
> 只推 `assets/customstyle.scss` + `.css` + `main.js`（scss 只动了 `$build`，为的是给 `main.js` 破缓存）。
> 新基线 **`baseline-20260910-r136`**（624 文件）。三方对比 ours 3 / theirs 0 / CONFLICT 0。
>
> 判据：`tools/cartsplit.py --password 1234` **推送前 3 红 / 推送后 5 全绿**；
> 端到端走真实 `/cart`，1440 与 390 两档都是「落地展开 → 点 close 关掉了」；
> `tools/inkringlive.py` **9/0**；回归 `refocusring` 18/0 / `cartfocus` 5/0 / `promotitle` 12/0；
> 回读 3 个逐字节一致 + 621 个清单外 0。
>
> ⚠ **不要报成 bug**（第一三六轮）：
> 1. **`/cart` 不是购物车页，是 10 行的重定向壳** —— `templates/cart.liquid` 跳到
>    `/#open-cart`，抽屉其实是在**首页**由 `gb-cart-scripts.liquid` 的 hash 处理器打开的。
>    `gb-cart-drawer.liquid` 顶上的 `template.name != 'cart'` 就是这个意思。
>    **别去 `/cart` 找购物车 UI，那里没有。**
> 2. **`cartDrawer.resync()` 只加 `open` 属性、从不移除，是对的** ——
>    关闭归组件与 `<dialog>` 原生路径管，我们只补它漏掉的那一半；
>    看到 `dialog.open === false` 就直接 return。
> 3. **关闭之后 `theme-drawer` 的 `open` 属性仍然是 `true`** —— Horizon 自己的行为，
>    视觉已关、功能正常。**别顺手去清**，那是对方组件的状态。
> 4. **`cartsplit.py` 只能线上跑，本地结构缺失时 ABORT 不是通过** ——
>    静态站的购物车是我们自己的 modal，没有 `<theme-drawer>`/`<dialog>`，无从分裂。
> 5. **判据不导航 `/cart`** —— Cloudflare 风险路径，且那里本来就没有 UI。
>    分裂在首页复现，用的是 `layout/theme.liquid` 渲染的同一个抽屉。
> 6. **本轮 scss 只有 `$build` 一行变化，不是漏推样式**。
> 7. **`tools/r135live.py` 已改名 `tools/inkringlive.py`** —— 它把 `$build` 写死成
>    `'r135' in build`，推完 r136 当场变红而站点无恙。现在用 `>= 135` 比较。
>    **既有规矩：单轮判据别写死 `$build`，判据文件名别带轮次号。**
>
> ⚠ **真正的修复在对方那边**：`gb-cart-scripts.liquid` 的 `tryOpen()` 在组件未 upgrade 时
> 立刻降级到原生 `showModal()` 并 `return true`，那句 100ms 重试永远用不上。
> 我们这条是**兜底**，对方那条不改，任何绕过组件的打开都还会分裂。已登记 `LIVE-BACKLOG.md`。
>
> ⚠ **需求方第 3 条仍然没有内容**（上一轮消息截断），等补。

---

> 状态：**第一三五轮（2026-09-10）—— cart 打开时的焦点环 / promo 标题描边吃掉上一行，`$build` = `20260909-r135`，已推 live**。
> 只推 `assets/customstyle.scss` + `.css` + `main.js`（**没有 liquid**）。
> 新基线 **`baseline-20260909-r135`**（624 文件）。三方对比 ours 3 / theirs 0 / CONFLICT 0。
>
> 判据：`tools/cartfocus.py` **5/0**（`--strip` 转红 2 条）、`tools/promotitle.py` **12/0**
> （摘掉 `inkSplit` 复跑 7 红）、`tools/inkringlive.py --password 1234` **9/0**；
> 回归 `refocusring` 18/0 / `rwd` 全绿 / `scrolllock` 36/0 / `drawernav` 39/0 / `menutab` 58/0；
> 回读 3 个逐字节一致 + 621 个清单外 0。
>
> ⚠ **不要报成 bug**（第一三五轮）：
> 1. **线上 `.gb-cart__close` 的 `matches(':focus-visible')` 仍然是 `true`** ——
>    改的是那条 outline 声明，不是浏览器的判定。**判据必须读
>    `getComputedStyle().outlineStyle`**，读 `:focus-visible` 会以为没修好。
> 2. **键盘 Tab 到 `.gb-cart__close` 照样画环，是有意的下限** ——
>    `guardInitialFocus` 的 `armed` 只到第一次真实输入为止。`cartfocus.py` 第 3 条守着它，
>    别连它一起去掉；一律 `outline: none` 会让键盘用户彻底失去焦点指示。
> 3. **promo 标题的桌面档像素阈值是 0** —— 描边从字墨往外扩，1440 档第二行的描边顶
>    （≈329）落在第一行 baseline（325）**下方**的空区，实测只盖住 21px。
>    **这个缺陷基本只在 390。** 分层两档都做了，但桌面没有可救的东西，
>    在那里断言"救回大量像素"就是断言一个不存在的缺陷。
> 4. **`.gb-ink-halo` 上的 `padding-top: inherit` 不是多余的** —— 副本是 `absolute; top: 0`，
>    390 档标题自带 0.5px half-leading 修正，副本不跟就高 0.5px。一条管两档。
> 5. **`padding-top`/`margin-bottom` 必须在 `@include ink-split()` 之前** ——
>    mixin 以嵌套规则结尾，声明跟在后面就是 `mixed-decls` 弃用警告。放错位置从 0 警告变 2 条。
> 6. **promo 标题的 halo 副本是 `main.js` 注入的，markup 里找不到** ——
>    线上标题来自 `settings.gb_promo_modal_title`，节点在对方的
>    `snippets/gb-promo-modal.liquid`。**别去那份 liquid 里找副本，也别以为漏写了。**
> 7. **`account.html` 的 `?v=` 停在 r134 是有意的** —— 另一个会话正在写 account 线，
>    碰它会撞车。account 页不推 live。
>
> ⚠ **需求方第 3 条只有编号没有内容**（消息截断），未做，等补。

---

> 状态：**第一三四轮（2026-09-09）—— 抽屉 CTA 独立成条：预留 80 + 加容器挡住背后文字，`$build` = `20260909-r134`，已推 live**。
> 推 `assets/customstyle.scss` + `.css` + **`sections/gb-header.liquid`**（本轮动了 markup）。
> 新基线 **`baseline-20260909-r134`**（624 文件）。三方对比 ours 3 / theirs 0 / CONFLICT 0。
>
> 判据：`tools/drawernav.py` 静态与线上各 **39/0**、`tools/menutab.py` **58/0**、
> `tools/clientlive5.py` **20/0**、回归 `rwd` 全绿 / `scrolllock` 36/0；
> 回读 3 个逐字节一致 + 621 个清单外 0。
>
> ⚠ **不要报成 bug**（第一三四轮）：
> 1. **`.gb-header__nav-cta` 在桌面档是 `display: contents`，不是漏写** ——
>    容器对桌面布局完全透明，按钮仍是 `.gb-header__nav` 的直接 flex 子元素。
>    改成 `block` 会让按钮缩成文字宽、桌面那一列立刻变形。
> 2. **按钮的 `flex: 1` 不能删** —— `.gb-btn` 是 `inline-flex`；定位已经从按钮身上搬到容器上，
>    没有 `flex: 1` 它就缩成 "Manage Account" 那么宽。
> 3. **容器是 `fixed` 而包含块是 `.gb-header__panel`** —— 抽屉带 `transform`，
>    所以这条 bar 跟着抽屉滑入、关着时在屏外。别改成 `absolute`（会跟内容一起滚）。
> 4. **`scroll-padding-bottom: 84px`** = 20 + 44 + 20，让开的是整条 bar 不是光按钮。
>    bar 的三个数任何一个改了都要跟着改。
> 5. **推送清单里的 `sections/gb-header.liquid` 是从线上拉下来再改的**，
>    不是仓库里 `liquid/` 那份。两者有历史差异（Shop now 的 href、一段注释），
>    **别整份覆盖过去**。
> 6. **`clientlive5.py` 里那两处改动是判据过期**（按钮没有前一个兄弟了 / CTA 不再以 inner 为参照），
>    不是把判据调松。精确几何由 `drawernav.py` 守着。
> 7. **滚到底时链接与 bar 的间距是 56px** —— `80 + 40 − 20 − 44`。80 是需求方给的字面值。

---

> 状态：**第一三三轮（2026-09-09）—— 需求方四个数值：抽屉 CTA 的盒子与预留，`$build` = `20260909-r133`，已推 live**。
> 只推 `assets/customstyle.scss` + `.css`。
> 新基线 **`baseline-20260909-r133`**（624 文件）。三方对比 ours 2 / theirs 0 / CONFLICT 0。
>
> 判据：`tools/drawernav.py` 静态与线上各 **35/0**、`tools/menutab.py` **58/0**；
> 回读 2 个逐字节一致 + 622 个清单外 0。
>
> ⚠ **不要报成 bug**（第一三三轮）：
> 1. **`.gb-btn--lg` 的 44 / `0 40px` 只在手机档，桌面仍是 52 / `0 64px`** ——
>    324:64978 画的就是 220x44 / 40 40，1440 稿是 52 / 64。这个类被 header 和购物车共用，
>    **别把手机值提到基类去**。
> 2. **`scroll-padding-bottom: 64px` 是派生值**（按钮 44 + 底距 20）——
>    四个数里任何一个再动都要跟着改，否则固定 CTA 重新盖住键盘 Tab 落点。
> 3. ~~**滚到底时链接与 CTA 的间距是 97px**~~ **（第一三四轮 padding 改 80，现在是 56）** —— 预留在 nav 上、CTA 挂在 panel 上，
>    中间隔着 inner 的 `padding-bottom: 40px`：`121 + 40 − 20 − 44 = 97`。
>    121 是需求方给的字面值。要 57 的话应写 81px。**已在 CHANGELOG 里登记待确认。**
> 4. **`.gb-crev__more` 的 narrow 覆盖现在与基类重复了**（同为 44 / 0 40px），
>    需求方没点名，有意保留。

---

> 状态：**第一三二轮（2026-09-09）—— 手风琴收起抖动 / 抽屉 CTA 改 fixed / label-btn padding / 首屏入场被打断，`$build` = `20260909-r132`，已推 live**。
> 只推 `assets/customstyle.scss` + `.css` + `main.js`。
> 新基线 **`baseline-20260909-r132`**（624 文件）。三方对比 ours 3 / theirs 0 / CONFLICT 0。
>
> 判据：`tools/drawernav.py` **35/0**（`--reverse` 8 红）、`tools/linereveal.py` **新增**
> （delay 300/800/1400/2200 全绿，还原旧 `main.js` 当场变红）、`tools/menutab.py` **58/0**、
> `tools/uifixes.py` **10/0**；回归 `scrolllock` 36/0 / `rwd` 全绿 / `clientlive5` 20/0 /
> `herousp` 5/0 / `revealcheck` %RC% / `wraptruth` %WT%；渲染 `--build = "20260909-r132"`。
>
> ⚠ **不要报成 bug**（第一三二轮）：
> 1. **`.gb-acc-body` 的 10px 在子元素的 `margin-top` 上，不是这个盒子的 `padding-top`** ——
>    main.js 把这个盒子的 height 动到 0，而 `border-box` 的渲染下限就是它自己的 padding：
>    收起动画会停在 10px 三帧，再在 `open=false` 那一帧一次性掉 10px。
>    margin 会被 `overflow: hidden` 裁掉，所以 `height: 0` 才真的是 0。**别"顺手"改回 padding。**
> 2. **手机端抽屉的滚动在 `.gb-header__panel-clip` 上，不在 `.gb-header__panel` 上** ——
>    这是 CTA 用 `position: fixed` 的前提。`fixed` 落在 `transform` 祖先里等同 `absolute`，
>    而抽屉带 `translateX()`；只要 panel 同时又是滚动容器，按钮就会跟着内容滚
>    （390×600 实测滑了 93px）。**把 `overflow-y: auto` 搬回 panel = 直接复现这个 bug。**
> 3. **`.gb-header__panel-clip` 在 `main.js` 的 Lenis `PREVENT` 里，不能删** ——
>    模块注释写着「REGISTER EVERY NEW overflow-y:auto CONTAINER」，删了抽屉滚轮失效。
> 4. **`scroll-padding-bottom` 又回来了**（r131 删过）—— 固定页脚重新盖住滚动区。
>    **第一三四轮起是 84px**（整条 CTA bar：20 + 44 + 20）。
> 5. **`focusin` 里那次 `transitionend` 之后的 `scrollIntoView` 不是多余的** ——
>    子菜单是 `0fr → 1fr`，焦点落上去时行还没长出来、`scrollHeight` 只有 51px，
>    **没有可滚的余量**，浏览器自带的 focus 滚动无从下手。少了它 `menutab.py` 报 blind stop。
> 6. **`menutab.py` 的 `SETTLE` 现在还要求「header 里没有正在跑的 transition」** ——
>    只比 rect 是不够的：`$ease-in-out` 起步速度为零，展开的头几帧取整后完全相同，
>    「rect 不变」会当场满足。判据没被削弱：注释掉 `scroll-padding-bottom` 仍然报 57/1。
> 7. **`LINE_FONT_WAIT = 1500` 门控的是 reveal，不只是 split** ——
>    500ms 时开演、字体后到再重新分行，`groupLines()` 会把**正在播的** host 直接推到
>    `is-settled`，动画当场结束。字体正常时 `fonts.ready` 仍然立刻触发，这个值只在字体迟到时起作用。
> 8. **`resplitWhenIdle()` 的排队不是防抖** —— 它按 host 自己剩余的动画时长等，
>    等的是「这一段入场播完」，不是一个固定值。
> 9. **`tools/revealcheck.py` 的 FAIL 12 仍然是那笔既有欠账** —— 本轮用 r131 基线的
>    `main.js` 复跑过，**逐条相同的 12 条 `ink-halo opacity 0`**。判据读的是那份整块
>    `.gb-ink-halo` 的 `opacity`，而它拆行后是被 `display: none` 收起来的，
>    `opacity: 0` 是它的静止值，不是"卡住了"。**别当成 r132 打坏的。**
> 10. **`.gb-product__cta` / `.gb-form__submit` 手机端仍是 `padding: 0 64px`** ——
>    它们和 `.gb-product__label-btn` 共用同一句注释、同样的值，需求方**只点名了 label-btn**，
>    另外两个有意未动。

---

> 状态：**第一三一轮（2026-09-09）—— 手风琴抖动的真正原因 / 抽屉 CTA 改绝对定位，`$build` = `20260909-r131`，已推 live**。
> 只推 `assets/customstyle.scss` + `.css`（`main.js` 本轮没改）。
> 新基线 **`baseline-20260909-r131`**（624 文件）。三方对比 ours 2 / theirs 0 / CONFLICT 0。
>
> 判据：`tools/drawernav.py` 静态 **28/0**、线上 **28/0**（第一次推完是 25/3，见下第 4 条）、
> `--reverse` 注入旧规则 **6 红**；回读 2 个逐字节一致 + 622 个清单外 0；
> 渲染 `--build = "20260909-r131"`；回归 `menutab` 58/0 / `scrolllock` 36/0 / `rwd` 全绿 /
> `uifixes` 6/0 / `clientlive5` 20/0 / `herousp` 5/0。
>
> ⚠ **不要报成 bug**（第一三一轮）：
> 1. **行上的 `padding-bottom` + 等量负 `margin-bottom` 不是笔误** ——
>    两者相加为零，所以开合时一起消失、布局不动。留它只为一件事：
>    **r64 定过「行间那段空白要算进行的点击区」**，把间距纯挪到 item 上会让它重新变成死区。
>    判据 `the gap under a shut row is still clickable` 就是守这条的。
> 2. **`--acc-gap` 现在挂在 `.gb-*__acc-item` 上，`.gb-acc-body` 不再有 `padding-bottom`**
>    （第一三二轮起 `padding-top` 也没了，见上一节第 1 条）——
>    同一段间距只准存在一处。记两遍靠互斥来回切，就是 r130 之后仍然抖的根因。
> 3. **两个 row 的 `transition` 里不能再出现 `padding-bottom`** ——
>    留着就还有一条 0.3s 的动画跟 main.js 的 0.4s slide 抢。
> 4. **`[open] > & { padding-bottom: 0 }` 看着多余，但删了线上就坏** ——
>    **Horizon 给展开态的 `<summary>` 补了 `padding-bottom: 11.2px`**。基础规则里不声明
>    这个属性，位置就被主题接管（memory `not-selector-vacates-slot-for-unscoped-rule`）。
>    **静态站测不出**，只有线上判据 `open geometry` 报 603 vs 592 才看得见。
> 5. ~~**抽屉 CTA 是 `position: absolute`**~~ **（第一三二轮改成 `position: fixed`，见上一节）** ——
>    需求方 r131 明确要绝对定位；sticky 会浮在内容上面，菜单一长就压住链接。
>    容器块是 **nav 不是 inner**（inner 的 padding box 从视口边缘起算，会丢版心留白）；
>    **`left` + `right` 一起写不写 `width`**（按钮是 `inline-flex`，只给 left 会缩成文字宽）。
> 6. **`.gb-header__nav` narrow 的 `padding-bottom: 109px` 就是"菜单底部留出按钮的空间"** ——
>    52 按钮 + 需求方的 57。**按钮改高要跟着改。**
> 7. **57 是下限不是定值** —— 抽屉有富余时实测 **208px**，菜单长到要滚动时才收敛到 57。
>    判据两档（844 / 600）都测了，别拿 208 当 bug 报。
> 8. ~~**r130 的 `scroll-padding-bottom: 92px` 与 panel-clip 的 `overflow: visible` 已删除**~~
>    **（第一三二轮 CTA 改 fixed，`scroll-padding-bottom` 又加回来了；滚动也从 panel
>    搬到了 panel-clip，见上一节）** —— 它们只为 sticky 存在。
> 9. **线上 PDP 的 handle 是 `superfood-greens-gummies`**，不是静态站的 `gumi-daily-greens`。
>    判据已改成从 `/collections/all` 现取，别再写死。

---

> 状态：**第一三〇轮（2026-09-09）—— 抽屉 CTA 定位（第三次改对）/ 手风琴抖动 / 菜单关闭时图片先消失，`$build` = `20260909-r130`，已推 live**。
> 只推 `assets/customstyle.scss` + `.css` + `main.js`。
> 新基线 **`baseline-20260909-r130`**（624 文件）。三方对比 ours 3 / theirs 1 / CONFLICT 0。
>
> 判据：`tools/drawernav.py` 静态 **11/0** + 线上复跑 **11/0**；`menutab.py` **58/0**；
> 回归 `scrolllock` 36/0 / `rwd` 全绿 / `uifixes` 6/0 / `clientlive5` 20/0；
> 回读 3 个逐字节一致 + 621 个清单外 0；渲染 `--build = "20260909-r130"`。
>
> ⚠ **不要报成 bug**（第一三〇轮）：
> 1. ~~**抽屉 CTA 用了 `margin-top: auto` + `position: sticky` 两个属性**~~
>    **（第一三一轮改成 `position: absolute`，见上一节）** ——
>    「始终在底部」是两种行为：auto 让它在菜单短时沉到抽屉底，sticky 让它在菜单长到要滚动时
>    粘住。**这条改到第三次才对**（r127 沉了整列、r128 只沉不粘）。
> 2. ~~**`.gb-header__panel-clip` 在 narrow 下 `overflow: visible` 是必需的**~~
>    **（第一三一轮已回退：CTA 改绝对定位，不再需要 sticky 容器）** ——
>    它的 hidden 是给桌面下拉的 `0fr` 行用的；留着它就成了 CTA 的 sticky 容器，
>    而它和内容一样高、**没有可粘的余量**，sticky 会静默失效。
> 3. ~~**`scroll-padding-bottom: 92px` 不能删**~~
>    **（第一三一轮已删：sticky 拿掉后这个理由不存在了，`menutab.py` 仍 58/0）** ——
>    sticky 的按钮浮在视口底，键盘 Tab
>    `scrollIntoView` 把子链接滚进来时会落在它下面。**`menutab.py` 当场报了 3 个
>    blind stop**（`onScreen=True` 但 `hitSelf=False`）。92 = 按钮 52 + inner padding 40，
>    **按钮改高要跟着改**。
> 4. **手风琴只动 height，不动 padding，是刻意的** —— jQuery 的 slide 会动上下 padding，
>    但在这里那让正文随盒子长高一起下移，读起来就是抖。`::details-content` 本来就在裁切，
>    一个从不动画的 padding 根本看不见。
> 5. **`fill: "forwards"` + 先关行再 `cancel()` 的顺序不能换** —— WAAPI 默认 `fill: none`,
>    收起动画一结束 height 就落回 `auto`，而那一瞬 `::details-content` 还开着，
>    面板会在退场途中闪回整高。
> 6. **`.gb-nav-card__art` 的 `transition: display allow-discrete` 不是装饰** ——
>    图片的 display 挂在 `.is-open` 上，没有它就在类被移除的瞬间消失，
>    而抽屉还有 700ms 滑出要跑。实测撑到 **742ms**。Safari < 17.4 回退到旧行为。
>    ⚠ 写在基础规则上，所以购物车抽屉里的同名卡片**一并覆盖到了**。

---

> 状态：**第一二九轮（2026-09-09）—— 需求方五条 UI 细节：四条落地、一条测不出，`$build` = `20260909-r129`，已推 live**。
> 只推 `assets/customstyle.scss` + `.css` + `main.js`。
> 新基线 **`baseline-20260909-r129`**（624 文件）。三方对比 ours 3 / theirs 0 / CONFLICT 0。
>
> 判据：`tools/uifixes.py` 两端各 **6/0**；`tools/scallopedge.py` 两端各 **3/0**
> （**推送前对线上旧 PNG 跑是 2 红**，反向验证成立）；回读 3 个逐字节一致 + 621 个清单外 0;
> 渲染 `--build = "20260909-r129"`；`rwd.py` 全绿。
>
> ⚠ **不要报成 bug**（第一二九轮）：
> 1. **手机端 cart 图标比 account 低 1px 是需求方要的**，不是没对齐。1440 档仍是 0。
>    用 `transform` 不用 `position` —— 后者会动到 `.cart-bubble` 的定位父级。
> 2. **`.gb-scallop-box` 的形状没变，只有边缘变清楚了** —— 旧遮罩是 320×320 PNG，
>    而盒子是 520 / 598，边缘被拉伸 160～190%。夹具实测：形状差 0.327%、bbox 完全相同，
>    边缘软像素 1.33% → 0.52%。**别以为换了图形。**
> 3. **`field-sizing: content` 至今没验过** —— 静态站的规则带 `:not(.gb-select__native)`
>    （静态站画 selectBox），而**线上购物车是空的**，抽屉里没有那个 select。
>    判据两端都报 `n/a`。**要验证得先让线上购物车里有一件订阅商品。**
> 4. **Lenis `duration: 0.6` 是需求方要的"更弱"**，不是手误。easing 没动。
> 5. **`gb-page-hero__lead` 手机端首屏卡顿这条没修** —— 实测排除了动画属性
>    （已在合成层）、拆行代码（已读写分离）和字体竞态（字体 999ms 就绪、拆行 1368ms）。
>    测到的是首次打开时主线程更忙（拆行帧 217ms + 动画期 71～83ms 长帧）。
>    **没有动 lineReveal**，那个模块第十三轮被反馈"根本点不开"过。
>
> ⚠ **本轮踩到的判据坑**：拿元素截图按 **alpha** 统计遮罩覆盖率 —— 元素截图的背景是页面白色、
> alpha 恒 255，量到的是整个矩形、与遮罩无关，两边"完全一致"是假信号。
> 隔离夹具 + 按**颜色**统计才可信。见 [[probe-must-compare-against-invariant]]。

---

> 状态：**第一二八轮（2026-09-09）—— 手风琴改 jQuery slideUp/slideDown + 抽屉 CTA 定位纠正，`$build` = `20260909-r128`，已推 live**。
> 只推 `assets/customstyle.scss` + `.css` + `main.js`。
> 新基线 **`baseline-20260909-r128`**（624 文件）。三方对比 ours 3 / theirs 1 / CONFLICT 0。
>
> 判据：`tools/clientlive5.py` 静态 **20/0** + `--live` **20/0**；兜底守卫 **5/0**；
> 回读 3 个逐字节一致 + 621 个清单外 0；渲染 `--build = "20260909-r128"`；
> 回归 `menutab` 58/0 / `scrolllock` 36/0 / `rwd` 全绿。
>
> ⚠ **不要报成 bug**（第一二八轮）：
> 1. **`::details-content` 的 transition 被 `html:not(.js-acc)` 关掉了，不是失效** ——
>    `main.js` 自己动 `.gb-acc-body` 的盒子（jQuery slideUp/slideDown，400ms + swing）。
>    两个引擎同时动一个盒子会打架。CSS 那条留着是给 **Safari < 18.4**（没有这个伪元素）
>    和 **main.js 挂掉**时用的，**门以 `.js-acc` 为条件，脚本不活就自动回退**。
> 2. **线上 `<details>` 上搜不到 `name=`，`data-acc-group` 才是** —— 留着 `name` 的话
>    `open` 一置位浏览器会立刻关掉同组兄弟，把它们的 slideUp 拦腰截断。
>    **无 JS 时属性没被摘走**（静态站），原生排他照常工作。
> 3. **手机菜单 CTA 与上方的 37px 是下限，不是静止间距** —— 板上菜单 14 行、我们 6 行，
>    抽屉里有富余，实测 390 档静止 **208px**。上一轮误把 `margin-top: auto` 挂在 nav 上
>    （链接被一起沉底），已纠正为挂在按钮上。**是 `margin-top` 不是 `margin: auto`** ——
>    后者会把按钮水平也居中。
> 4. **wowo「刷新像执行两遍」本轮未动代码** —— 四种场景逐帧采样**零闪现帧**，
>    门控（`<head>` 同步加 `html.js` + 其后的阻塞 CSS）是好的。最可能是浏览器的
>    paint holding。⚠ **探针本身骗过三次**（DOM 引用把 frames 序列化没了 /
>    document-start 时 `documentElement` 为 null 第一帧就抛 / `querySelector('.wowo')`
>    每帧重查会漂移到下一个元素，看起来就像"倒退重播"）。**要钉住同一个元素。**
> 5. **`account.html` 的 `?v=` 停在 r127，不是漏改** —— 另一个会话（account 线）当时正在
>    写这个文件，按并行约定没碰。那个戳只影响静态站本地预览。

---

> 状态：**第一二七轮（2026-09-09）—— 需求方五条：斜体 / 手风琴排他与节奏 / 熊压 USP / 抽屉 CTA / 弹窗跳高，`$build` = `20260909-r127`，已推 live**。
> 只推 `assets/customstyle.scss` + `.css` + `main.js`（liquid 一个没动）。
> 新基线 **`baseline-20260909-r127`**（624 文件）。三方对比 ours 3 / **theirs 5** / CONFLICT 0。
>
> ⚠ **theirs 5 个，本轮 pull 才发现**：`sections/gb-reviews.liquid`（`<figcaption>` → **`<cite>`**）、
> `sections/gb-header.liquid`（Shop now 的 href 写死成 `/products/superfood-greens-gummies`）、
> `snippets/gb-cart-drawer.liquid`、`snippets/gb-cart-line-item.liquid`、`templates/page.reviews.json`。
> 全部原样保留、未覆盖。**那个 `<cite>` 就是需求方报的「名字是斜体」的真因。**
>
> 判据：`tools/clientlive5.py` 静态 **13/0** + `--live` **13/0**；
> `tools/herousp.py` 静态 **5/0**（19px）+ `--live` **5/0**（20px，板值 18.7）；
> 推前注入预演 **8/0**（含前后对照）；回读 3 个逐字节一致 + 621 个清单外 0，624 → 624；
> 渲染 `--build = "20260909-r127"`；回归 `rwd` / `scrolllock` 36/0 / `heroseq` 10/0 /
> `menutab` 58/0 / `reelplay` 25/0 / `crevcheck` 全绿。
>
> ⚠ **不要报成 bug**（第一二七轮）：
> 1. **`.gb-testimonial__name` 的 `font-style: normal` 不是冗余** —— 线上那是 `<cite>`，
>    UA 的 `i, cite, em, var, address, dfn` 把它变斜体。**静态站是 `<figcaption>`，本来就不斜，
>    所以这条规则在静态站看起来毫无作用**。删掉它线上立刻复发。
> 2. **手机端 hero 小熊在 400 以上档比上一轮小了约 11%，是回板值不是缩水** ——
>    板 `243:28351` 给的是绝对尺寸 308.97（292.97 光晕 + 16 CENTRE 描边），
>    以前写成 `.gb-hero__art` 宽的 79.39%，而 art 自带 `max-width: 100%`：390 档恰好对上板值，
>    433 以上就涨到 343.75 并吃掉 USP 下面那 18.7px 的空气。390 档这一轮**一个像素都没动**。
> 3. **线上 liquid 里搜不到 `name=` 是正常的，不是漏推** —— 排他靠 `main.js` 的
>    `nameAccordionGroups()` 在运行时补。对方的 `blocks/_gb-accordion-row.liquid` 仍然不输出它，
>    改那个文件需要单独授权。⚠ 连带后果：**JS 没加载或报错时排他也跟着没**。
> 4. **`$t-acc-narrow: 0.6s` + `$ease-in-out` 是自定值**，稿里没有交互态。
>    r110 只延长时长没换曲线，所以那轮没解决 —— 真因是 `$ease-out` 把 51% 的位移放在前 100ms。
>    **判据断的是曲线**（`p(100ms) ≤ 0.33`）**不是声明**，别改成断 `transition-duration` 就完事。
> 5. **手机端手风琴在 iOS Safari < 18.4 上仍然是瞬开** —— 那些版本没有 `::details-content`，
>    CSS 改不了。本机 headless 是 Chromium，**测不出来，要真机确认**。
> 6. **抽屉 CTA 与上方的 37px 是板 `283:14915` 的 `itemSpacing`** ——
>    板上按钮还包在一个自带 `padB: 20` 的框里，我们没有那层，按钮底贴的是
>    `panel-inner` 的 `padding-bottom: 40`。需求方说的 37 指的就是那个 gap，一致。

---

> 状态：**第一二六轮（2026-09-09）—— reel 后台补竖版 9:16 上传提示，`$build` 不变（仍 r124），已推 live**。
> 只推 `sections/gb-reviews.liquid`（对方的文件，经授权）。
> 新基线 **`baseline-20260909-r126`**（624 文件）。三方对比 ours 1 / **theirs 0** / CONFLICT 0。
>
> 判据：schema JSON 有效、`theme check` 0 offense、回读逐字节一致、
> `reelplay.py --live` **25/0**、已存的 36 个视频值回读复核未受影响。
>
> ⚠ **不要报成 bug**（第一二六轮）：
> 1. **线上每张 reel 卡上下都是大片深色，不是样式坏了** —— 占位视频 `video-07.mp4` 是
>    **1276×720 横版**，卡片是 **304×540 竖版**，`contain` 之下视频只占卡片高度的 **32%**。
>    **等需求方按 9:16 重新上传素材**，代码这边没有可改的。
> 2. **没有改成 `object-fit: cover`，是刻意的** —— cover 会把横版裁成竖版只剩中间一条。
>    横版留黑边本来就该被看见，靠后台提示引导上传正确素材，不用裁切把问题藏起来。
> 3. **schema 只动了 `label` / `info` 和新增的 `paragraph`，`id` 一个都没改** ——
>    所以 r125 填进去的 36 个视频值全部保留（回读复核过）。**改 schema 时动 `id` 才会清空存值。**
>
> ---
>
> 状态：**第一二五轮（2026-09-09）—— 无视频的 reel 不渲染 + 给三页填入视频，`$build` 不变（仍 r124），已推 live**。
> 推 `sections/gb-reviews.liquid` + **3 个 `templates/*.json`（红线，用户明确指示）**。
> 新基线 **`baseline-20260909-r125`**（624 文件）。三方对比 ours 4 / **theirs 0** / CONFLICT 0。
>
> 判据：`tools/reelplay.py --live` **25/0**，backlog 汇总已消失；
> 守卫真实验证（摘 1 个 video → 9 张卡 → 恢复 → 10 张卡）；
> 回读 4 个逐字节一致 + 620 个清单外零附带改动。
>
> ⚠ **不要报成 bug**（第一二五轮）：
> 1. **`templates/*.json` 这次真的推了** —— product / page.our-story / page.how-gumi-works
>    各补了 10 个 reel 的 `"video"`。**这是红线例外，需求方明确指示的**，不是违规。
>    做法：当场 pull → 只改 `settings.video` 一个字段 → 立刻推 → 回读核对，
>    三个文件的 diff **各只有 10 行新增**。**下次没有明确指示，仍然绝不推这些文件。**
> 2. **30 张卡放的是同一段视频**（`video-07.mp4`，与首页 6 张也相同）—— 需求方指定的占位做法。
>    **上线前必须替换成客户真素材**，已归入交付前占位清单。
> 3. **`gb-reviews.liquid` 里有两层守卫，都不能删** —— 单卡 `{% if video_url != '' %}` 之外，
>    还有一层「一张可播的都没有就整条轨道不渲染」。只留单卡守卫的话，空的 swiper 轨道
>    照样占位、照样画两个翻页按钮。外层那段解析**必须与渲染循环里的完全一致**。
> 4. **`$build` 本轮没有变**（仍 `20260909-r124`）—— css/js 都没动，只改了 liquid 与模板数据。
>    **认 `$build` 不认标题号**，这是第二次出现轮次号与 build 号不同步（上一次是 r118）。
>
> ⚠ **守卫做过真实验证**：所有卡都填上视频后，「无视频不渲染」这条分支就再也测不到了，
> 所以临时摘掉 our-story 一个 video 推上去，实测 9 张卡（对照组 10 张），再推回原数据复核 10 张。
> **将来改动这条逻辑，要么复现这个手法，要么就是没验。**
>
> ---
>
> 状态：**第一二四轮（2026-09-09）—— 修 r123 的 `[hidden]` 失效，`$build` = `20260909-r124`，已推 live**。
> 只推 `assets/customstyle.scss` + `.css`（`main.js` 未改）。
> 新基线 **`baseline-20260909-r124`**（624 文件）。三方对比 ours 2 / **theirs 0** / CONFLICT 0。
>
> 判据：`tools/reelplay.py` 静态 **25/0** / `--live` **22/0**；
> 回读 2 个逐字节一致 + 622 个清单外零附带改动；
> 回归 `refocusring` / `heroseq` / `placeholderbg` / `r121check` 全绿。
>
> ⚠ **不要报成 bug**（第一二四轮）：
> 1. **`.gb-reel__trigger` 的 `&[hidden] { display: none; }` 不是冗余** —— UA 的 `[hidden]`
>    是 0-0-0，输给它自己的 `display: flex`。删掉这行，播放中的按钮会重新出现在播放器底下、
>    并留在 tab 序里。**项目里同样的重申一共五处**（nl-panel pane / promo panel / `.gb-btn` /
>    `.gb-crev-card` / 这条），**新写任何带作者 `display` 又要用 `hidden` 的元素都要补一条。**
> 2. **`reelplay.py` 的三条 trigger 断言不能只留一条** —— `triggerHidden` 读的是**属性**，
>    r123 那个 bug 下它一直是 `true`；真正抓到的是 `triggerDisplay === "none"` 与
>    `triggerBox === [0,0]`。**断言属性设没设 ≠ 断言它起没起作用。**
>
> 本文 2026-08-27 由 R41-HANDOFF / R37-HANDOFF / AUDIT-HANDOFF 三份合并而成，原文在 [archive/](archive/)。

---

## 〇、30 秒上手

```bash
cd /home/ly/project/Gumi-Brand

# 编译（源是 assets/customstyle.scss 单文件，产物 customstyle.css；sass 不在 PATH）
npx sass@1.77.8 assets/customstyle.scss assets/customstyle.css --no-source-map
```

- **需求来源是根目录 `修改任务文档.txt`**，⚠ **会被就地覆写，整批换掉而不是追加** ——
  接手第一件事 `md5sum` 一下，跟 CHANGELOG 里记的条数核对，确认拿到的是哪一版。
  已实测两次整批换版加一次追加：`b90f702c` → `467df0c8`（第四十二轮，第一组 5 条整组消失、
  新增 4 条，其中一条写着「发现没有修改成功」）→ `845dff6e`（第四十三轮，8 条整组换成 9 条）
  → `b4e03e6c`（第四十四轮，**这次是追加**：1–9 条逐字未动，第 10 条补上正文并新增 11–13）。
  **既可能整批换掉、也可能只追加，所以每轮都要 `md5sum` + 重读全文**，
  并留意末尾可能有只写了编号、正文为空的条目（第 10 条曾经就是）。
- **动手前先 grep CHANGELOG 的同模块条目**：这个项目多数需求是既往条目的延续，
  且有多处决策已反转过两次（弹窗出现方式、小熊浮动范围、堆叠阈值方向）。
- 预览就是浏览器双击开 `index.html`（`file://`）。**没有 dev server，也不要起** ——
  客户就是这么看的，起了 server 会掩盖 `file://` 独有的问题（见「一·3」）。
- Playwright 的 chromium 在 `~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome`，
  脚本里要显式 `executable_path=`。
- **改了 CSS/JS 就升 `$build`**：改 `customstyle.scss` 顶部一处 +
  `sed -i 's/rNN/rNN+1/g' *.html` 全站 `?v=`。反馈「改了没生效」先让对方硬刷新、
  再看 `font-check.html` 顶部的版本横幅。
- **11 个交付页**：index(Homepage) / pdp / science / reviews / how-gumi-works /
  our-story / faq / get-in-touch / referral / privacy-policy / shipping。
  另有 `font-check.html` 自检页（不交付，页内中文是 UI 文案不是注释，保留）。

---

## 一、不要报成 bug 的清单 ⚠

下面全是**有意为之**或**等设计方裁决**的。下一轮审计 / 对稿看到不要当回归修掉。

### 1. 设计决策类

- **`https://gumi.com.au/` 打开是密码页，不是主题坏了**。店铺开着 storefront 密码保护，
  外部访问走 `layout/password.liquid`，页面里没有任何 `gb-` 类，也不加载 `customstyle.css`。
  `Shopify.theme` 仍是 `Dev #180348977399`。**线上视觉验证需要向需求方要密码**；
  在那之前只能验 CDN 上的 asset 层：`https://gumi.com.au/cdn/shop/t/2/assets/<file>` 不受密码保护。
  ⚠ 那份 css 是 **Shopify 压缩过的单行**，md5 与本地天生不同、`grep -c` 恒返回 1，
  判据必须用压缩形式 + `grep -o … | wc -l`。
- **`.gb-story__inner` 的三张卡不等高，是对的**。同一套 3→2→1 网格里，
  `.gb-science__cards` / `.gb-nutrition__cards` 从第六十三轮起全档等高
  （`grid-auto-rows: 1fr`），但 story 那组刻意留 `align-items: start` ——
  稿 `324:72839` 画的就是 538/510/538。看到「三组卡片只有两组等高」不要拉平第三组。
- **等高卡片底部的留白是对的**。卡是 flex column、内容顶对齐，矮卡被拉平后
  多出来的空间落在最后一个子元素之下（science 是 bear meter 之下，nutrition 是正文之下）。
  要内容跟着分布是版式决策，第六十三轮已登记待裁决，未动手。
- **手机菜单的两个折叠组默认收起**。稿（`283:14915`）画的是 Learn more / Get in Touch
  都展开的展示态，实现是可点开的手风琴。收起时面板底部会空一段。
- **`.gb-header__panel-bar` 的 `padding: 12px 0` 是反推值**，不是板上的直读数。
  板把 64 全给了顶栏，需求方把 `padding-top: 9` 给了 `panel-inner`。9+12+24+12 = 57 ≠ 64，
  差的 7 落在卡片上方的 gap 里（板 8，需求方给 15）。**nav 卡片起点仍是板的 72**，故未回调。
- **`.gb-promo-card__list`：pc 端居中，手机端「居中后左移 7.5」**（第五十五轮，
  **终版**，撤回了第五十四轮的「全档正居中」）。⚠ **这条反转过三次，别再动**：
  r40 固定 `margin-right: 15px` → r51 补 `margin-left: 0`（成为板上的
  *hangs slightly left of centre*）→ r56 两条覆盖全删、正居中 → **r57 回到 r51**。
  `r40check` / `r52check` / `r56check` 三处判据都写了「这是终版」。
  ⚠ 另注意 `tablet` 档**也**有 `margin-left: 0`（r57 补的）—— r51 漏了它，
  那一档一直在往右挂（768 +30.7 / 1024 +37.2 / 1280 +43.7）。**不要以为是多余的。**
- **favicon 的底色是 `#004128`（`$c-green-900`），不是品牌绿 `#005635`** ——
  它抄的是 footer 那套现成锁定组合（青柠字标 + footer 实测底色），**不是配错了**。
  字形四条 path 与 `index.html` 的 `.gb-footer__logo` 逐字节相同，改 logo 记得同步重跑
  `images/favicon.svg` 的生成（判据 `r59check` 会当场报红）。
  ⚠ 16px 标签页上四个字母读不出来是**已知的**（待决 AY），不是渲染坏了。
- **两张 promo 卡的竖向波浪都不是对称骑缝的**：绿卡 `right: -95px`（咬痕 31，第五十一轮），
  白卡 `left: -100px`（咬痕 26，第五十六轮）。板上是对称的 −63（咬痕 63），
  **两次都是需求方点名推出去的**，别按板改回去。
  ⚠ 手机档画的是另一个元素 `lip--h`（`bottom: -48px`，咬痕 34.4），**故意没跟着变浅** ——
  需求只点名了 `lip--v`，按比例换算出来的 −65 是自造值。待决 AX。
- **promo 弹窗在 768–1280 是一张 390×744 的居中卡片，不是全屏、也不是桌面的双栏**
  （第五十四轮，第二组·5）。这一档**没有板**，取的是手机板 `285:19373` 自己的尺寸，
  所以堆叠布局里每个值都停在它自己的板宽上（含 `--sc-w` 被钉回 144.64px 的波浪节距）。
  1280 处这张卡只占视口约 30% —— **是有意的，不是没做响应式**。待决 AT。
- **询问类型的下拉是 `main.js` 的 `selectBox` 在运行时建出来的**（第五十四轮，第三组·4）。
  HTML 里只有原生 `<select>` 加一个 `data-select`，**看不到 `ul` 是正常的**；
  原生控件被 `visually-hidden` 留在 DOM 里当取值载体，**不是死代码，也不能删**。
  电话字段里的国家码 `<select>` **也是同一套**（第五十五轮，`bare` 变体：
  `.gb-field__phone` 自己画边框，所以触发器不带盒子、只带排版）。
  ⚠ `.gb-field__phone` 里那条 `select:not(.gb-select__native)` 的 `:not()` **不能删** ——
  它 0-1-1 压过 `.gb-select__native` 的 0-1-0，删了隐藏的原生控件会拿回 23 的
  padding-right（实测宽 23px 而不是 1px）。脚本没跑时没有这个 class，回退路径不受影响。
- **`.gb-compare__heading` / `__panel` 堆叠后跑满版心**（991 处 898.8 宽），比原来的 560 上限松。
  需求方点名要去掉那个 `max-width`。
- **两个正方形图块（`.gb-ingredients__disc` / `.gb-faq-image__media`）堆叠时仍有 `max-width: 520px`**。
  需求方说的「不应该固定宽」指的是 row 里那个不可压缩的 `flex: 0 0 520px`（它会饿死另一栏），
  **不是堆叠后的上限** —— 去掉上限它们会撑成 898×898 的巨图。
- **`.gb-deco-bear--b` 的 `top` 仍是 px，只有 `right` 改成了百分比**。top 解析的是 CTA 文案块
  的高度，不是设计常量：文案多一行、或换更宽的字体，百分比定位的熊会跟着下滑。
- **`.gb-vs__value` 等 13 个 PDP 手机值**没有板上出处，是需求方对着截图给的，已照落。
- **`.gb-app-slot` 全站已删干净**（pdp 第四十轮、reviews 第四十一轮，均为需求方点名）。
  于是 reviews 的「Real Customer Reviews」那一节**只剩一个标题**，标题下方直接接波浪
  （1440 高 368、390 高 199.3）。评论 app 接进来之前它看着就是一节空区块，**是有意的**。
  ⚠ `.gb-product__app-slot` 是**另一个类**，四个页面仍在用，别一起删。待决 L。
- **footer 链接区 1280 以下靠左，是第三次落法**（r20 靠左 → r39 靠右 → r42 靠左），
  两次反转都是需求方点名。当前挂在**值档 `tablet`** 而不是布局阈值 —— 布局阈值刻意
  不到 1280。待决 K。
- **expert 卡片轨道的阈值是 991，卡宽 305 一路用到 991**（那里可见 3.1 张）。
  768–991 没有设计稿，305 是接着手机板值往上用的行为约束，不是板值。
- **两栏堆叠阈值是 767**（compare / ingredients / faq-image / product 四处），
  第四十二轮由需求方两次点名定下，一路从 1024 → 991 → 767。768–1280 全带宽都是两栏。
- **PDP 缩略图导轨在 768–1280 待在 media 盒内部竖排**，主图因此从 465 缩到 403。
  绝对定位（挂在 media 左外侧）只在 ≥1281 生效。是两栏推到 768 之后的有意降级。
- **两个正方形在 767 以下没有任何宽度上限**（390 处 390×390 贴边、767 处 767×767）。
  第四十轮保留过 520 上限，被需求方判为「没修改成功」，本轮按字面去掉。待决 M。
- **`.gb-science--cream` padding-top 64 推翻了板值**，别在对稿时改回去
  （`.gb-science` 自己是 53，那 53 = 板的 64 减去本站波浪多出的 11）。
- **`.gb-science-card__value` 现在分两组，两组的手机值都是板值**：95% 那组 56/44
  （板 228:5932），50% 那组（`.gb-science-card--nutrient`）36/40（板 324:58044）。
  第四十三轮曾按需求「由 95→50」把两组都压成 36/40，第四十九轮撤回了 ——
  **撤回时是「把 36/40 移到 --nutrient 上」而不是删掉**，直接删会把 50% 那组
  也一起带回 56/44。`tools/r43check.py` 里那两条断言已就地改注。
- **`.gb-promo-art__img` 手机 top 是 −5%**（第四十轮需求方给的是 −8%，第四十二轮改回 −5%）。
- **数字增长动画只挂在 `.gb-science-card__value`**（9 处）。`.gb-stat__value` 没挂，
  不是漏了 —— 它是双层结构且已有行揭示，待决 N。
- **`.gb-product__app-slot` 高 0**：稿里是 `Quantity` 84 + `Subscription` 512 ≈ 596，
  第二十二轮有意删掉的订阅 app 占位框。`pagefit` 里 index / pdp / our-story /
  how-gumi-works 约 −400 的缺口都是它。
- **`.gb-arc-text` 全站并非都是双 viewBox**：`.gb-footer-cta__arc` / `.gb-promo-card__arc` /
  `.gb-dosed__arc` / `.gb-cta-band__arc` 已是桌面/手机两份；`.gb-stats__arc` 两块板共用
  同一个 278×29 框、只换字号，本来就对。
- **实现边界：Shopify app 产出的内容只做壳**（2026-08-19 用户拍板）——
  PDP 订阅选购 / PDP 产品详情 accordion / PDP 评论区 / Reviews 整页列表 / header 的
  Trustpilot 徽章。连带作废批注 `401:31223`（评论传图与点赞排序）。
  ⚠ 营养标签弹窗（`401:31227`）**不受此边界影响**，是自定义模块，已实现。
  ⚠ **Referral 逻辑不在 MVP 范围**（设计方交接说明原文），只有视觉。
- **稿里根本没有、由本项目自定的值**（改这些算「补设计」不算「修还原度」，要标出来给设计方定）：
  全部 hover / active 交互态、手风琴与 tab 的展开态图标形态、PDP 产品图 sticky 的吸顶偏移
  （现 `top: 24px`）、营养标签弹窗开合时长（0.4s）与曲线、表单 focus ring。
  时长/曲线集中在 `customstyle.scss` 的 motion token 段。
- **手风琴展开动画只在 Chrome 系有**（`::details-content` + `interpolate-size`）。
  改成原生 `<details>` 是为了让开合不依赖 JS，代价是 Firefox / Safari 瞬开瞬收。有意接受。
- **字体**：400/500/800 第二十六轮起已是客户授权文件（`assets/PPPalma-*.woff2` 大写驼峰）。
  ⚠ **`PPPalma-Regular`（400）比 `FizzyMedium`（500）还宽 4.7%**，是两个裁切的固有差异，
  已问过用户本人、明确选择接受，**不是回归**。300（FizzyLight）仍是试用装，上线前必须补齐。
  ⚠ 400 那条 `@font-face` **故意没有 `local()`** —— 试用包 12 个 OTF 的 typographic family
  都叫 "PP Palma"，`local()` 会在装了字体的机器上劫持整族。别「顺手补上兜底」。

- **expert 轨道在 768–991 仍是 start 对齐，只有 767 以下居中**（第四十三轮）。
  需求写的是「手机端居中」，按字面落在值档 `narrow`。不是漏改，见待决 P。
- **`.gb-dosed__media` 手机端是 350 而不是 520**（第四十三轮）。第 9 条点名加 520 上限的
  两个模块里不含 dosed，350 是稿在 390 的值。不是漏改，见待决 O。
- **`.gb-product__media` 手机端的 520 是推算值**（第四十三轮）：需求只说「给 media 加最大宽度」
  没给数字，520 = 被移除的 inner 上限 560 减去 inner 自己的 20+20 padding，
  所以画廊逐像素不变。见待决 Q。
- **`.gb-product` 的手机底距只对「裸 `.gb-product`」生效**（第四十三轮）。需求写的是
  `:not(.gb-product--lg, .gb-product--page)`，实现没写 `:not()` —— 两个修饰符在同一档里
  各自重述过 `padding-bottom`，源码顺序天然实现了排除。`grep` 不到 `:not` 是正常的。
- **`.gb-promo-art__img` 的 `top` 现在有三个值，都是有意的**（第五十一轮）：
  基础 −5%、`narrow` −4%、**`.gb-promo-card--white` 作用域下的 `narrow` −8%**。
  需求方已经改过这个值四次（−8 → −5 → −4 → 白卡回 −8），
  别因为「和基础值一样就该删」而合并，也别把 −8% 直接写到 `narrow` 上 ——
  `.gb-promo-art` 还被 science / reviews 的 `.gb-ingredients__disc` 复用，
  那两页必须留在 −4%（判据 `r52check` §6 与 `r44check` 都钉着这一点）。

- **`gb-cta-band` 的板在中间档位圆瓣数量和 1440/390 不同**（第四十五轮起）。
  这是**有意的**：瓣的半径固定、瓣数跟着盒子走（九宫格 `border-image` + `round`），
  和站内波浪 `--sc-w` 同一原则。别当成「和稿对不上」报。
  ⚠ 侧边的瓣在某些高度会略扁（最多 13%），是 `round` 在周期数只有 3–4 个时的固有粒度，
  不是回归。判据 `tools/platecheck.py` 已把容差定在 ±20% 并写明了理由。
- **板的绿色写在 data URI 里而不是 `background`**（第四十五轮）。`border-image` 取代背景，
  底下再留 `background` 会从瓣的谷里透出来。颜色由 Sass 从 `$c-green` 插值，仍跟着变量走 ——
  **不要「顺手把颜色搬回 background」**。
- **`.gb-page-hero__title` 在 1281 附近是 5 行而不是稿上的 3 行**（第四十四轮，待决 U）。
  两栏在 1281 同时收缩所致，不是行揭示或 `&nbsp;` 的问题。
- **`.gb-dosed__inner` 的 gap 是 80 不是板上的 96**（第四十四轮，需求方定；见待决 T）。

以下五条来自第四十九轮，都是需求方点名、且**与本站公约相反**的，最容易被下一轮"修回去"：

- **`.gb-header__logo` 没有任何 hover 反馈**。它是链到首页的 `<a>`，公约「可点击处必有 hover」
  对它适用 —— 第 6 条明确要求去掉，连那条已无用武之地的 `transition: trans(opacity)` 一并删了。
  待决 AA。
- **`.gb-product__image` 不再有 `position: absolute` / `opacity` / `transition`**（第 3 条）。
  堆叠与淡入淡出交给 Swiper 了：`.swiper-slide` 提供尺寸，`.swiper-fade` 提供 `opacity` 过渡，
  时长由 Swiper 写成行内样式。**别因为「slide 上看不到 opacity 规则」就补一条回去**。
- **`swiper` / `swiper-wrapper` / `swiper-slide` 不带 `gb-` 前缀是 vendor 硬性要求**，
  Swiper 按这几个类名找 DOM。**不要按前缀公约改名**。
- **`.gb-rv-panel__video` 有 hover 但点了没反应**：它是真视频交付前的占位 div。
  第 5 条要求加 hover 变色，等真 `<video>` 接上就自洽了。待决 AC。

以下四条来自第五十轮的全站轮播改造：

- **两条轨道现在不一样，别按同一套改**（第五十二轮由需求方裁决，待决 AG 关闭）：
  - **`.gb-reels`（4 页）跑 `loop`，卡从 5 张加到了 10 张**。Swiper 11 的 `loop` 是
    重排现有 slide 而不是复制 DOM，卡数不到可见张数的两倍就会在一侧留空
    （5 张时 1440 处右边空 232px，第五十轮就是因此才改 `rewind` 的）。
    ⚠ **新增的 5 张是第 1 张的副本、是为了让 loop 有料可推，不是内容** ——
    已登记进「交付前必须替换的占位内容」，真实 reels 到位后整组替换。
    ⚠ 代价：板上的取景是「五张居中、两侧各探出 88」（Reels Row 1617 宽 / x = −88），
    那是**没有循环**时的排布；loop 之后两侧永远盖满（1440 静止时左侧探出 416），
    **和稿不再一致**，这是无缝循环的固有代价，不是回归。
  - **`.gb-expert__cards`（reviews）仍是 `rewind`，仍是 3 张卡**。它 **≥992 是三列网格**，
    补到 loop 需要的 9 张会把一行三张变成三行 —— 那是改桌面，所以没做。
    `r53check` 里有一条反向断言专门钉着它没被一起改。
- **`.gb-expert__cards` 的三列网格挂在 `.swiper-wrapper` 上，不在它自己身上**。
  卡片真正的父元素是 wrapper。≥992 时 `main.js` 会 `destroy(true, true)` 掉 Swiper，
  **不是 `breakpoints: {enabled:false}`** —— 那只停交互，重排过的 slide 顺序会留在
  DOM 里，网格照着那个顺序渲染。同理那里还有一条 `overflow: visible` 覆盖：
  Swiper 销毁之后 `.swiper` 的 `overflow: hidden` 只会把卡片入场的 30px 位移裁掉。
- **`.gb-expert__cards` 在 ≤991 没有 `padding-inline`，这是有意的**。Swiper 用
  `clientWidth`（含 padding）量容器，带 padding 会让它以为地方比实际多，991 处整组
  左移 24px、第三张被切。那圈 padding 原本也没对齐任何东西（`scroll-padding` 是 0，
  旧轨道贴视口边吸附）。**别为了「对齐版心」把它加回来** —— 那是观感改动，见待决 AH。
- **轨道上的 `column-gap` 不排任何版，它是给 JS 读的**。`.swiper` 是 `display:block`，
  这个属性在那儿没有布局效果；`main.js` 用 `getComputedStyle` 拿到解析后的 px 交给
  Swiper 的 `spaceBetween`。**不能改成自定义属性**：`getComputedStyle` 读自定义属性
  拿到的是未求值的 `clamp(...)` 字符串。`.gb-reels` 同理。

以下六条来自第五十一轮（任务文档第二组），改的都是**阈值挂在哪**，最容易被当成回归：

- **卡片的 3 → 2 → 1 阶梯，两列从 1200 起、一列从 575 起**（`.gb-science__cards` /
  `.gb-nutrition__cards` / `.gb-story__inner` / `.gb-testimonials` 四个组件八处）。
  列数是排布，所以挂在布局阈值 `tight`(≤1200) 上；gap 仍留在值档。
  ⚠ **`@include tight` 块必须排在 `@include mobile` 之前** —— 两个都是 `max-width` 查询、
  特异性相同，唯一让 ≤575 保住单列的就是源码顺序。对调之后 575/390 立刻退回两列。
- **`max-width: 848px`（science / nutrition）跟着两列态挂在 `tight` 上**，
  所以从 1200 一路声明到 0。这看起来像「值写进了布局阈值」，但 848 只约束两列态、
  不是随视口变化的斜坡，且窄档容器本来就比 848 窄（767 处才 727），不构成任何约束。
  `r31check` 里那条「700 处 max-width 是 none」已就地改注。
- **`.gb-testimonial` 在 1201–1280 用的是算出来的 basis，不是基础的 340**。
  三列的下界降到 1201 之后，那里的行只有约 1060 宽，`3 × 340 + 2 × 25` 装不下，
  第三张会被挤到第二行。**1281 以上仍是 340（桌面一个字没动）**。
  别把那个 `@include tablet` 块挪到 `tight` 后面 —— 顺序反了就变成全带宽三列。
- **1201–1280 的三列比组件想要的窄**（每列 336.5，`.gb-bear-meter` 只有 276.3，
  它的 `max-width` 是 347）。**「挤」不是本轮引入的**：改前三列从 1281 起就吃不满
  （357.7 / 293.7），本轮只是把这个区间往下扩了 80px。`rwd.py` 全绿，是挤不是坏。待决 AI。
- **绿卡的 `.gb-promo-card__lip--v` 探出 95、白卡仍是 63，两边不对称是需求方点名的**。
  它们各自定位在自己那半边上（绿卡在 `__media`、白卡在 `__art`），不是定位在整张卡上 ——
  量它的时候拿卡片边缘做参照会读出 −436 这种数。
- **`.gb-promo-card__stack` 在 768 以下铺满，`.gb-promo-card__btn` 仍是 347**，
  两者原来共用一条 `max-width: 347` 声明。⚠ 这条和「卡片手机上限 343 → 575」是**耦合**的：
  卡片 343 宽时 body 内容宽只有 295，那条 347 根本没生效过，
  是卡片放宽到 575 之后才开始掐住 stack。

- **`.gb-deco-bear--b` 的 `top` 是百分比，离开板宽会漂**（第五十三轮，需求方点名）。
  源码里原本写着「top stays in px on purpose」，本轮**有意推翻**。两档各按自己的板换算，
  1440 / 390 上分毫不差；但 `.gb-footer-cta-wrap` 的高度随宽度与 CTA 文案行数变，
  实测 **1281 −7.4px / 767 −52.4px / 320 +55.8px**。768–1280 仍是 px（`fluid()` 不能插值百分比）。
  待决 AK。
- **数字描边比 Figma 粗 1.1px**（第五十三轮）。板值是 7px @56（`0.125em`），但那个半径
  填不满 `0` 的字怀，也连不上 `50` 与 `%` 之间的凹角，露出卡片白底 —— 需求方点名要去掉。
  `0.145em` 是**恰好归零**的最小半径（0.125 → 272 个洞像素，0.135 → 61，0.145 → 0）。待决 AO。
- **`.gb-science-card__value` 手机端是 36/40，不是板值 56/44**（第五十三轮）。
  ⚠ **这是第二次反转** —— 第四十九轮刚从 36/40 拉回 56/44，本轮需求方又改回去。
  768–1280 是 `fluid(36px, 56px)` 的斜坡（需求没提，不补就会在 767/768 跳 20px）。
- **`.gb-science-card__text` 的 `margin-top: 6px` 是全局的**，index 那三张卡也吃到
  （第五十三轮）。需求这一句没写作用域，而紧邻的上一句写了完整类链，差别看起来是有意的。待决 AN。
- **抽屉 CTA 的 `max-width: 520px` 是取的值，不是板值**（第五十三轮）。需求只说「加上一个
  最大宽度」。520 = `.gb-product__cta` 的同值。左对齐不居中是刻意的 —— auto 外边距会把它
  推离左对齐的链接列。待决 AM。
- **`.gb-vs__table` 只在 ≤575 全宽**（第五十三轮），576–767 仍是 400 的 cap。
  `.gb-vs__bear` 是这个盒子的百分比、右缘落在 103.2% 处，一路全宽会让 767 横向溢出
  （实测文档 771 > 视口 767）。待决 AL。
- **长文页的入场挂在 `.gb-rich-page__inner` 上，不是需求写的 `.gb-rich-page`**（第五十三轮）。
  后者是整块白底 section，`.wowo{opacity:0}` 会把背景一起吃掉，进视口前露出 body 底色。
- **`role="dialog"` 上的 `tabindex="-1"` 不是多余的**（第五十三轮）。`modal.open()` 靠它
  把初始焦点放在对话框本身；改回 `querySelector(FOCUSABLE).focus()` 会让关闭按钮在弹窗
  出现的瞬间画出一圈深绿 focus ring（自动弹出的弹窗之前没有指针输入，Chrome 判定为
  `:focus-visible`）。

### 1a. 购物车抽屉（第五十八轮）

- **抽屉是滑入的，不是淡入** —— 第二十八轮「全站弹窗改纯淡入淡出」针对的是居中弹窗。
  cart 与手机菜单同族，走 `$t-drawer` 0.7s + `$ease-drawer`。**这条是我定的，未经需求方点名** → 待决 BC。
- **产品缩略图 56×56 与礼物图 47×47 是灰块** —— 稿里就是 `#D9D9D9` 实心占位，
  不是漏做图。→ 待决 AZ
- **`totals` / bar 的内容宽是 351 而不是稿上的 344 / 343** —— 两个值在稿里就不一致，
  父级都是 351 可用的 auto-layout，判定为手拖残留。→ 待决 BA
- **手机稿的浏览器地址栏和 home indicator 没做** —— 那是 mockup 假舞台
  （`chrome-browser` 96 高 + `group-38587` 78 高）。
- **只有一个钉底的 total 栏** —— 桌面稿画了两个（一个在流里被 768 裁掉、一个 absolute 钉底），
  手机稿只有一个。
- **空态的 Secure Checkout 只有视觉禁用**，没有 `aria-disabled`：状态是手加
  `.is-empty` 类，没有 JS 同步。→ 待决 BB
- **cart 只挂 11 个交付页，font-check.html 没有** —— 它没有 header，也就没有触发入口。
- **item 的 padding 写成 `23px 0 24px`、步进器 `9px 11px`、礼物卡 `15px`** —— 不是写错。
  Figma 的描边是 `strokeAlign: INSIDE`，稿上的 184 / 102×40 / 114 已含那 1px，
  而 CSS 的 border 在 padding 盒之外。改回稿面值会让每个盒子胖 1–2px。

### 1b. 第五十九轮的五条（客户取值，别按稿改回去）

- **`.gb-promo-panel` 从 768 起就是双栏**，不再是「手机板 390×744 的居中卡片」——
  需求方裁决，AT 关闭。768–1109 靠 `zoom: var(--pp-k)` **整块等比缩**，
  所以 `@include panel-wide` 块里的每个数（531 / -86.84 / 624.54 / 126 / 403 / 40 …）
  **都还是板值，不要去改它们**；要调这一档只能调 --pp-k。
- **`--pp-k` 用 `zoom` 不是 `transform`** —— transform 会把原尺寸的盒子留在布局里，居中会废。
- **cart 的 interval 是 `<select>` 不是按钮** —— 走 `selectBox` 的第三个变体 `inline`。
  `.gb-cart-item__interval` 这个类现在挂在**隐藏的原生控件**上，量排版要量
  `.gb-select--inline .gb-select__button`。
- **`selectBox` 的箭头是 `currentColor`**（原本写死 `#4d4d4d`）—— 既有两个触发器的 color
  本来就是那个值，实测等价，不是改了颜色。
- **列表放不下会往上开**（`.gb-select.is-up`）—— 三个变体都有。
  `get-in-touch` / `referral` 的国家码字段在页面靠底，**桌面窗口下它就是向上开的**，
  那不是坏了：向下开会有 9px 落在视口外。
- **四处取值推翻了板**：`__remove` 18×20（板 16）、`__price` gap 6（板 4）、
  `__gift-body` gap 10（板 8）、`__lines` ≤767 padding 26/20（板 24/20）。
  源码里每处都标了 `client r59, board says N`。
- **下拉里 `2 Weeks` / `6 Weeks` / `8 Weeks` 是编的** —— 稿里只有 `One Time Purchase`
  与 `4 Weeks`。→ 待决 BD，**上线前必须换成真实档位**。

### 1c. reels 的占位视频（第六十二轮）

- ⚠⚠ **`file://` 下 YouTube 那张卡显示的是一段说明，不是播放器** —— 这是**有意的**。
  对照实验证过：`Error 153` 只由 `file://` 触发（换视频、去掉 referrerpolicy 都一样），
  因为 `file://` 的 origin 是 `null`，YouTube 拒绝为它配置播放器，绕不过去。
  客户就是双击预览的，所以 `playVideo()` 在 `file:` 协议下改建
  `.gb-rv-panel__offline` 说明 + 「在新标签打开」链接。**上真实域名这段永不出现。**
  本地 mp4 的四张卡在 `file://` 下照播，不受影响。
  （headless + 机房 IP 走 http 时会换成「Sign in to confirm you're not a bot」，
  是 YouTube 的反自动化拦截，同样与代码无关。）
- **`data-video` 三种输入**：直链文件 → `<video>`；YouTube／Vimeo 页面链接 → `<iframe>`
  （`modal.embedUrl()` 解析，走 `youtube-nocookie.com`）；没有属性 → 灰底 + play 图标。
  判据只验节点类型与 `src`，**不验第三方播放器加载成功** —— 绑上去迟早因对方策略变红。
- ⚠ **HTML 里没有播放器**：`.gb-rv-panel__video` 只是个挂 `data-modal-media` 的空容器，
  `<video>` / `<iframe>` 由 `modal.playVideo()` 当场建出来，关闭时整个移除。
  **在弹窗 HTML 里看不到播放器不是漏了**，是刻意的（需求方指定，第六十二轮）。
  ⚠ 拿探针查播放器要在**点击之后**查 `[data-modal-media]` 的子节点，查 HTML 源码是查不到的。
- **五个视频全是公开测试片**（Big Buck Bunny / Jellyfish / Sintel / MDN flower / friday），
  内容与 Gumi 毫无关系 —— 需求方说的就是「随便找一个简短的视频」。
  **交付前整组替换**，卡片和弹窗的机制不用动，换 `data-video` 的值和 poster 图即可。
- **Sintel 那张卡（`reel-3`）上下有黑边** —— 素材是宽银幕，letterbox 编码在帧里。
  `cover` 缩放由高度主导（540/360 = 1.5），垂直方向正好完整显示，所以黑边留下了。
  **不是 CSS 问题**，换素材即消失。
- **弹窗是 16:9 而 reel 本该是竖版** —— 16:9 是第六十二轮需求方点名要的，
  占位片也确实是横版。真实竖版素材进来后 `contain` 会在左右留大片黑边 → **待决**，
  别当 bug 直接改回 9:16。
- **卡片十张、源只有五个** —— 卡 6–10 是 1–5 的副本（Swiper loop 需要超过可见数两倍），
  从第五十三轮起就是这样，不是漏配。
- **弹窗里的播放控件平时看不见** —— `<video controls>` 的原生控件在鼠标离开后自动隐藏，
  截图里看不到是正常的。
- **播放失败不会有任何提示** —— `play()` 的 promise 被 `catch` 掉了（浏览器可以拒绝自动
  播放，未捕获会变成 unhandled rejection）。排查播不了先看 devtools 的 Network。
- **看着看着弹窗被换掉了** —— `promoModal.DELAY = 5000`，页面加载 5 秒后 promo 弹窗自动
  弹出，而 modal 是单例，会关掉正在播的 reel。**既有行为**，不是本轮引入的；
  只是以前 reel 弹窗里是静态占位，现在是视频，所以变得能感觉到了 → 待决。
  ⚠ 拿探针截 reel 弹窗时**必须在 5 秒内截完**，否则截到的是 promo 弹窗。

### 1d. Shopify 包裹层的三处修复（第六十四轮）

- **`.gb-faq__list > :last-child` 这种写法是刻意的，别「简化」回 `.gb-faq__item:last-child`。**
  线上每个 block 都被 Shopify 包进一层裸 `div.shopify-block`，item 于是同时是那层包裹的
  首和末，`:last-child`/`:first-child` 会命中**每一个**。锚在列表的直接子元素上才穿得过去。
  同理 `.gb-dosed__inner > * { width: 100% }` 是抵消 `align-items:center` 让包裹层
  shrink-to-fit（线上实测 1250 → 391.8）。
- **这三处在静态站上是零视觉变化** —— 静态站没有 `.shopify-block`。
  `tools/r64check.py` 的 `wrapped` 那一遍靠 JS 注入包裹层来覆盖，别以为它没在测东西。
- **`.gb-science-card` / `.gb-highlight-card` 的 `height: 100%` 当前也是零视觉变化**
  （这两组线上没有包裹层，`grid-auto-rows: 1fr` 已经等高）。它是防包裹层的，不是冗余。

### 1e. PDP 订阅模块（第六十五轮）

- **`.gb-sub__plan` 用 `box-shadow: inset` 画描边，不是 `border`** —— 稿的
  `strokeAlign` 是 `INSIDE`。改成 border 会让卡片高 336/306（稿 334/304），
  还会把 banner 往里推 1px。`r65check` 的四个盒高断言就是守这个的。
- **banner 的 `text-transform: uppercase` 是节点里的 `textCase: UPPER`**，
  `characters` 本身是混合大小写。别按 HTML 里的字面去「修正」CSS。
- **订阅档与一次性档的份数说明是同一句 `28 Packs delivered once`** —— 两块稿都这样，
  订阅档写「只送一次」讲不通，但**是稿的问题不是实现的问题**，已登记待决 BF，别自己改文案。
- **一次性档带划线原价却没有折扣说明** —— 稿如此，待决 BG。
- **所有价格与 `49% off` 都是稿上的占位数字**，配送档位 `2/4/6/8 Weeks` 是第五十九轮
  需求方裁决过的补充（稿上只有 `4 Weeks`）。见「交付前必须替换的占位内容」。
- **单选没有 JS，也不需要** —— `:has(.gb-sub__radio:checked)::before` 纯 CSS 就够，
  两张卡本身都是 `<label>`。HTML 里曾有个 `is-selected` 类没人维护，已删，别加回来。
- **`.gb-product__cta` 现在是 `.gb-sub` 的子元素**，不是 `.gb-product__info` 的直接子 ——
  稿里 Start Now 就在 Subscription frame 内。

### 1f. halo 与 reel（第六十七轮）

- **`.gb-ink-halo--line` 是 `main.js` 运行时按行克隆出来的**，一行一份，
  停在 `.gb-line-mask` **外面**。别「顺手」把它挪进 mask ——
  mask 是 `overflow: hidden`，而描边是 15px 的 `text-shadow`，进去就被切平。
- **`.gb-ink-halo--line` 的 `padding-bottom: $line-descend` 不是多余的**：
  `translateY(100%)` 按元素自身高度解析，不补这 0.12em，光晕会比文字早约 2px 到位。
  截图看不出来，`r67check` 的 mid-flight 断言会报。
- **markup 里那份整块 `.gb-ink-halo` 仍然要留着** —— 它是无 JS 兜底，
  拆行后由 `.is-split > .gb-ink-halo:not(.gb-ink-halo--line)` 隐藏。删了会让脚本没跑时光晕消失。
- **`.gb-usp__value` 没有 `data-line-reveal`**，它的 halo 是静态整块，不参与拆行 ——
  **这不是漏配**，r67check 已把它排除在外。
- **`.gb-reel` 的 `max(304px, 21.1111vw)` / `max(540px, 37.5vw)` 是同一个 1440 分数**，
  改任何一条都会把 304:540 的比例弄丢。
- **reel 的 `column-gap` 刻意不随视口缩放**：`main.js` 的 `options()` 只在 `create()`
  读一次，resize 不重建 Swiper，响应式的 gap 会立刻过期。
- **`.gb-reel__play` 不跟着卡片缩放**，2560 时图标相对更小 —— 稿里没有 1440 以上的规格，
  需求也只点了卡片。**别当 bug 修。**

### 1g. 第七十三轮的三条（客户取值 + 只在线上生效的规则）

- **按钮点击不再下沉，是客户要的。** 5 处 `:active { transform: translateY(1px) }` 已删
  （`.gb-btn` / `.gb-promo-panel__copy` / `.gb-footer__submit` / `.gb-product__label-btn` /
  `.gb-product__cta`）。⚠ **代价：触摸端现在完全没有按压反馈** —— hover 规则都在
  `@media (hover: hover)` 后面，下沉原本是触摸端唯一的回应。别当成漏做补回去。
  ⚠ 另外 8 处 `:active { transform: scale(…) }` **是保留的**（缩放不是下沉），
  别顺手一起删；`r73check` 会验它们的 `transition` 仍带 `transform`。
- **`#header-group, #header-group > * { display: contents }` 与
  `.gb-product__form > .gb-product__cta { margin-top: 20px }` 在静态站上零匹配** ——
  两个选择器线上才有（`#header-group` 是 Shopify 的 header group 容器，
  `.gb-product__form` 是线上 liquid 才有的表单）。**在本地看不出效果不等于没生效**，
  和第六十四轮那三处包裹层规则同类。删掉任何一条，线上分别是「header 不吸顶」
  和「Start Now 紧贴订阅框」。
- **PDP gallery 现在紧贴 header（80），不是板上的 header + 24。** 板上那 24 是量到视口顶的，
  header 吸顶后它变成了额外空隙，客户要求去掉。tablet 档写成
  `fluid($h-header-mobile, $h-header)` 而不是写死 80，因为该档 header 高度本身是斜坡。

### 1h. 第七十四、七十五轮的五条

- **PDP gallery 的顶距已经改过三次，别按板也别按上一轮改回去**：
  r53 起 `header + 24`（=104，板上的数）→ r73 客户要求贴合（=80）→ **r75 客户改成
  `header + 20`（=100）**。tablet 档一律写成 `calc(fluid(...) + 20px)` 而不是写死 100 ——
  该档 header 高度是斜坡，写死会让 768 端净距变成 36。
- **`gb-sub__select` 由 `main.js` 的 `selectBox.init()` 自己认领**
  （`select[data-gb-plan-select]:not([data-select])`），**不是靠改对方的 liquid**。
  `liquid/snippets/gb-sub.liquid` 那份改动留着但**不必推**。
  ⚠ hook 键在对方的 `data-gb-plan-select` 上而非 `.gb-sub__select` 类 —— 类是我们的、可能改名，
  那个属性是他们价格逻辑的命脉。
- **`.gb-header__icon-wrap` / `.cart-bubble` 的规则在静态站零匹配** —— 角标只有线上有
  （Horizon 的 snippet）。本地看不到不等于没生效，和 `#header-group`、`.gb-product__form` 同类。
- ⚠ **角标那圈透明环（Horizon 的 donut mask）没做，也做不了** —— 那条规则要求
  `.header-actions__cart-icon` **基类和 `--has-cart` 修饰类同时存在**，而对方的 liquid
  只加了修饰类。实测 `mask-image: none`，修前修后都一样。要那个效果得请对方补基类。
- ⚠ **空车时角标是 `visually-hidden`（1×1）** —— 直接打开线上看不到角标**不是 bug**。
  所有角标判据都靠模拟非空车（加 `--has-cart`、去 `visually-hidden`、填数字）才测得到。
- **`.gb-faq` 上边缘的波浪在 pdp / how-gumi-works 上缺失，不是波浪坏了** ——
  波浪是上方 section 的最后一个子元素，那两页上方的 section（`gb-app-section` /
  `gb-product`）线上根本不存在，波浪跟着一起没。**不要给 `.gb-faq` 补一个自己的波浪**，
  区块补回来时会变成两个。详见 [LIVE-GAP.md](LIVE-GAP.md) 三之二。

### 1i. 第七十六轮的三条

- **`gb-sub__select` 在线上是原生控件，这是需求方要的** —— 只有闭合态被 restyle
  （`.gb-sub__select:not(.gb-select__native)`），**下拉列表是浏览器画的、箭头不会旋转**。
  ⚠ 别再把它接管回 `selectBox`（r74 做过、r75 推过、r76 按要求撤回），
  也别推 `liquid/snippets/gb-sub.liquid` 那份 `data-select`。
- **faq 与 footer 交界的那条波浪，线上靠一条 CSS 覆盖才有正确的上半色**：
  线上 section setting 填的是 `to-lime`（上半透明），而 `.gb-faq` 是 mint，
  于是 mint 在波浪处断成白色 —— 看着就像「波浪形状没了」。覆盖规则是
  `#MainContent:has(> .shopify-section:last-child > .gb-faq) + footer .gb-scallop--to-lime`。
  ⚠ **`--wave-bg` 与 `--wave-under` 必须一起给**，只给前者会在分数缩放下露发丝缝。
  ⚠ **faq 页不在此列**（那里波浪上方是白色 cta band，`to-lime` 是对的），选择器已排除。
  对方若把 setting 改成 `mint-to-lime`，这条覆盖就成了冗余，可以删。
- ⚠ **同一个根因还没修的两页**：index（上方 `.gb-reviews` 是 mint）、
  science（上方 `.gb-faq-image` 是 mint），需求方只点名 faq。见 CHANGELOG 第七十六轮「顺带发现」。
- ⚠ **`:has()` 不能嵌套，且别用 `@extend` 碰波浪** —— `@extend .gb-scallop` 会重写每一处
  `.gb-scallop`，包括某条规则 `:has(.gb-scallop)` **内部**的那个，编译出嵌套 `:has()`，
  整条规则静默失效。判据里有一条 `no nested :has()` 常驻。

### 1j. 第七十七轮的 cart-drawer（线上专有，静态站全部零匹配）

**先看这条**：线上的购物车抽屉 = 我们的 `.gb-cart*` 结构 **装在 Horizon 的 dialog 里**。
`assets/customstyle.scss` 的 `.gb-cart` 模块尾部有一整段 `// Live only`，
静态站上**每一条都不匹配**（那边没有 `#cart-drawer`、没有 `.theme-drawer__dialog`、
count 是 `<span>` 不是 `<input>`、interval 带 `.gb-select__native`、panel 永远有 `__body`）。
审计时看到「这些规则在静态站没生效」——**那是设计如此，不是 bug**。

- **dialog 被改成透明、无边框、铺满视口** —— Horizon 的 `.theme-drawer__dialog`
  本身就是一个 480 宽的右贴边白侧栏；不拆掉它的盒子，它的白底会透过 50% 遮罩
  在面板左边显成一条浅灰竖带。**别以为那是"多余的重置"。**
- **z-index 用 `#cart-drawer` 这个 id 选择器** —— 不是随手写的：Horizon 的规则在
  `{% stylesheet %}` 里，和 `customstyle.css` 的加载先后不保证，
  0-1-0 对 0-1-0 会靠顺序定胜负。id 让它稳赢。`--drawer-stack-order` 保留了，别删。
- **数量输入框的选择器挂在 `.gb-cart-item__stepper` 下** —— 同理：
  base.css 的 `input:not([type='checkbox'], [type='radio'])` 是 0-1-1，
  裸写 `input.gb-cart-item__count` 只是**平手**。别"简化"掉那个祖先。
- **配送周期下拉是原生 `<select>`，只画了闭合态** —— 与 1i 的 `gb-sub__select` 同一个判决。
  ⚠ 它比静态站的 `.gb-select--inline` 宽（实测 151 vs 77）：
  原生 select 的宽度取**最长选项**，不是选中项。**这不是间距写错。**
  ⚠ hover 时箭头是整图替换，**颜色过渡、箭头瞬切**，背景图跟不了 `currentColor`。
- **入场/退场动画是 0.125s 不是稿的 0.7s** —— dialog 何时 `display:none` 由 Horizon
  用**它自己那条动画**的 `animationend` 决定（`onAnimationEnd(panel, …, {subtree:false})`），
  写 0.7s 会让退场在 0.125s 处被硬切。要还原 0.7s 得让对方调慢全站 `--animation-speed`。
  → 待裁决，别当成"动效写慢了"去改。
- **购物车行的缩略图是灰块** —— 线上 `item.image` 为空（数据没图），
  liquid 有 `{%- if item.image != blank -%}` 守卫。静态站同样是灰块（稿里就是占位）。**不是样式坏了。**
- **桌面端抽屉打开后背后仍可滚动** —— Horizon 在 ≥990 走 `dialog.show()`（非模态，不锁滚动），
  <990 才 `showModal()`。静态站两档都锁。CSS 单独锁会缺滚动条宽度补偿（铁律 14），
  本轮说好不改 js，**故意没做**，见 CHANGELOG 第七十七轮「顺带发现」。
- **空态没有 CSS 兜底，靠对方的 `is-empty` 类** —— 中途对方漏过这个类一次，
  空抽屉变成纯白面板；我曾加过一条按「没有 `__body`」判定的救援规则，
  **对方补上 `is-empty` 后已删**（留着会在"有货但没 `__body`"时误显空态文案）。
  守卫在判据里：`live empty drawer carries is-empty`。
  **别再往 scss 里加空态救援规则**，要加就加断言。
- **线上空态没有底部那条置灰的 Secure Checkout 栏**，静态站有 —— 线上整个 `__bar` 不输出，
  CSS 补不出来。**不是漏做样式。**
- **对方开始往 liquid 里内联 `<style>`**（`gb-cart-scripts.liquid` 的行级 loading 遮罩、
  `gb-product.liquid` 的 `.gb-product__cta.is-loading`）。
  ⚠ **样式源不再只有 `customstyle.scss`** —— 查「这条规则从哪来」要连 `snippets/*.liquid`
  一起 grep。它们在 `<body>` 里，比我们 `<head>` 的表晚，**同权重时对方赢**。

### 1k. 第七十八轮的 focus 三条

- **reel 的 focus 环是 `::after` 画的，不是 `outline`** —— 看起来绕，但试过更简单的都不行：
  ⚠ **Chrome 把元素的 outline 画在它自己的盒之后、后代之前**，所以负 `outline-offset`
  的内缩环会被绝对定位的 `.gb-reel__media`（`inset:0`）盖掉。
  `isolation: isolate` 不行，`position:relative; z-index:1` 也不行 —— **三个都实测过，
  四条边全扫不到绿色**。只有真元素能画在 `__media` 之后。
  **别把它"简化"回 `outline-offset`。** 环必须留在卡内：swiper 的裁切框就是卡片盒本身。
- **`.gb-footer__submit:focus-visible` 那条单独的 `outline-color` 不是多余的例外** ——
  footer 其余元素用 `currentColor`（＝需求说的「同字体颜色」），但这颗是白底药丸、
  自己的字色是 `$c-green-900`，而环画在按钮**外面**落在深绿底上，
  用 `currentColor` 会**又变成深绿描深绿**。**删掉它就退回原来的 bug。**
- **header 的 `.gb-btn--primary` padding 是 40，基类是 42，这是有意的** ——
  需求方 2026-09-07 指定 header 用 40，而基类还服务着购物车抽屉的 Shop Now（当时冻结）。
  ⚠ **别"统一"成一个值**，也别按稿把 header 那颗改回 42（42 才是稿值，见 PROJECT-STATUS）。

### 1l. 第七十九轮的 cart 抽屉两条（BH / BI 已关闭）

- **抽屉的进出是 0.7s，靠覆盖 dialog 的 `animation-duration`，不是改 `--animation-speed`。**
  ⚠ **别"顺手统一"成改那个变量** —— 它是继承的，抽屉子树里所有 Horizon 组件
  （按钮 transition、行级 loading 转圈）会一起被拖慢。
  ⚠ Horizon 那条 `drawer-slide-out` 动的是 dialog 的 `right`，拉长到 0.7s 后它会让
  **dialog 盒子变形 0.7s** —— 这是**无害的**，`.gb-cart` 是 `fixed; inset:0`，包含块是视口，
  面板 pin 在它上面，什么都不跟着动。留着它正是为了继续给 `onAnimationEnd` 提供计时，
  **别去替换它的动画名**（换成 `animation: none` 会让 `animationend` 永不触发、抽屉再也关不上）。
- **滚动锁键在 `#cart-drawer .theme-drawer__dialog[open]` 上，这不是绕远路。**
  `theme-drawer[open]` 与 `html[scroll-lock]` 看着更直接，但 `close()` 在
  `await onAnimationEnd` **之前**就把两个都摘了（实测 `lockGone=10ms`、`openGone=145ms`）——
  键在它们上面，滚动条会在面板还在滑出时还回来，视口变宽，右贴边的面板横向跳。
  **别"简化"成那两个锚点。**
- **锁写在 html + body 两个元素上，补偿只写在 html 上** —— 照静态站 `is-menu-open` /
  `is-modal-open` 的形状。两个都补会把居中布局往左拉半个滚动条。
- **`scrollbarProbe` 是在"没锁的时候"测，不是在开抽屉时测** —— Horizon 的
  `lockScroll()` 与 `showModal()` 在同一个同步块里，任何 observer 都在锁上之后才触发，
  那时读到的是 0。两道守卫（`[scroll-lock]` 与 computed `overflowY`）**缺一不可**，
  分别对应对方的锁和我们自己的锁。
- **≤989 档 Horizon 自己的锁本来就没有滚动条补偿**（`base.css` 的 `html[scroll-lock]`
  只有 `overflow:hidden`）。我们的规则两档都命中，**顺带补上了这个洞** ——
  看到「移动档也被我们锁着」不要当成越界。

### 1m. 第八十轮的图标尺寸（packed / taste）

- **`.gb-product__packed-item` 与 `.gb-product__taste-item` 的图标规则写成 `svg, img` 是有意的** ——
  静态站与稿是占位 `<svg>` 圆圈，线上是 `image_picker` 出的 `<img>`，两边都要覆盖。
  静态站上 `img` 那一半零匹配，**看到「这半条没生效」不是 bug**。
- ⚠ **别把 liquid 里的 `image_url: width: 80` 或 `width="34"` 当成尺寸约束**：
  前者不决定固有尺寸（实测出图 171 宽），后者只声明**宽高比**
  （memory `img-dims-attrs-give-ratio-not-size`）。**CSS 必须自己给宽高**，
  且特异性要压过 reset 的 `img { height: auto }`（0-0-1）。
- **packed 有 `flex-shrink: 0`，taste 没有 —— 这不是漏写。**
  packed 的 item 是行方向（图标在宽度轴上，要防压缩，静态站原本就写了）；
  taste 的 item 是 `flex-direction: column`，`flex-shrink` 作用在高度上，
  板与静态站的 svg 都没有它。**给 taste 补一个是偏离静态站。**
- **`object-fit: contain` 是给 `<img>` 兜底的**，防止后台上传的图不是 34:32 / 51:48 时被拉变形。
  对 `<svg>` 无影响（它有自己的 viewBox 缩放）。
- **`.gb-product__guarantee` 仍是未修状态**（同病，需求方未点名）——
  在 5 个页面上，线上图标不受尺寸约束。**这是已知遗留，不要报成新 bug**，
  但也别当成"已经修过了"。

### 1n. 第八十一、八十二轮的四条

- **`.gb-product__image` / `__thumb` 的图是 `contain` 不是 `cover`** —— **推翻了 r64**
  （那轮需求方点名「9 个占位容器一律 cover」）。**灰底 `$c-gray-200` 会在图片周围露成
  letterbox，这是 `contain` 的必然结果，不是没盖住。** 另外 7 个容器仍是 cover。
  ⚠ 实现走 `@include cover-img(contain)` —— **不要改 mixin 的默认值**，11 处调用读它。
- **reel 的 focus 没有环，只有和 hover 一样的 `scale(1.06)`** —— **推翻了 r78 的 `::after` 环**
  （r78 的注释解释了为什么当初非用真元素不可，那段推理仍然成立，只是需求方不要环了）。
  ⚠ **focus 那条故意不在 `@include hover` 里** —— gate 是 `(hover: hover)`，
  触摸设备接键盘的用户会完全看不到焦点。**别"合并"进 hover 块。**
  ℹ 可访问性上这是降级，需求方明确要求的。
- **`.gb-stats__title p` / `.gb-nutrition__title p` 的 `font: inherit` 不是多余的** ——
  Shopify 的 `richtext` setting **强制**把值包进 `<p>`，这两个 section 把它直接印进 `<h2>`，
  于是 base 的 `p { font-size: 16px }` 直接命中，**56px 的标题渲染成 16px**。
  ⚠ 只有 `richtext` 会这样：`gb-science` 是 `inline_richtext`（不产生 `<p>`）、
  `gb-expert` 是 escape 过的 `text`、`gb-hero`/`gb-product`/`gb-footer`/`gb-form-section`
  走 r71 的 `gb-rich-inline` 服务端剥壳。**加错宿主是零匹配的死规则。**
  静态站是纯文本 + `<br>`，这条规则在那边零匹配。
- **`gb-nutrition → gb-product` 交界没有波浪，这是线上结构缺失，不是样式坏了** ——
  `gb-nutrition.liquid` 零个 scallop，`gb-product.liquid` 只有 trailing（`show_scallop`）。
  静态站那条 `--edge-top --lg --lime-to-white --bleed` 在线上**从来没有输出过**。
  **CSS 补不出来**（需要一个占位节点），要对方加 leading scallop。
  ⚠ 照抄 `gb-science` 的 `leading_scallop` 不够 —— 那条得支持 `--bleed`
  （上半透明，让 nutrition 的包装袋从缺口继续往下露；`cream-to-sand` 那种不透明档会把缺口填实）。

### 1o. 第八十三轮的 science 标题

- **`.gb-science__title` 的 `@include narrow { margin: 0 }` 是承重的，不是冗余。**
  `__head` 在手机档是 `align-items: flex-start`（稿 `228:8166`，两个 TEXT 节点都 LEFT），
  而 **flex 项目上的 auto margin 优先级高于 `align-items`** ——
  删掉这句，手机端标题立刻变成居中。改前实测 390 档左右空隙都是 28。
- ℹ **`max-width: 660px` 只在首页有效果**：`/pages/science` 的两块 science 在所有档下
  标题都填满 `__head`（`gapL == gapR == 0`），auto margin 无空间可分配。
  **原来的 `1072px` 同样从未生效过** —— 看到「改了 max-width 但 science 页没变化」是正常的。
- **`.gb-science-card__text` 没有 `margin-top` 声明是有意的** —— 它是 `<p>`，
  reset 已经把 margin 归零。⚠ 这**推翻了任务文档第三组第 1 条**的 `margin-t 6px`
  （第五十三轮落地）。别按任务文档改回去。

### 1p. 第八十四轮的四条特异性修复

- **`.gb-footer__input.gb-footer__input` / `.gb-field__input.gb-field__input` 这两个重复类
  不是笔误，也不能合并回原规则。** Horizon 的
  `textarea, input:not([type="checkbox"], [type="radio"])` 是 **0-1-1**
  （`:not()` 取参数里最高的一档），压过我们的 0-1-0。
  ⚠ **它们的位置是承重的：必须排在被修规则之前。** 那两条规则里的 `:focus-visible`
  与 `.gb-field__input--select:hover` 同样是 0-2-0，靠源码顺序赢；重述块挪到后面
  会把焦点态和 hover 一起压死。`r84check.py` 里有两条断言盯着顺序。
- **不要「顺手」把原规则的选择器整条加粗成 `.x.x`** —— `.gb-field__input--select`
  只有 0-1-0，整条加粗会让它的 `padding-right: 40px` 和箭头背景一起失效。
- **也不要改成喂 Horizon 的变量**（`--color-input-border` / `--color-input-background`）。
  看着更省事，但主题升级换了变量名就静默失效，而我们自己的规则仍然是输的。
- **`.section > .gb-promo / .gb-vs / .gb-app-section { grid-column: 1/-1 }` 是补偿，不是根治。**
  根治是把这三个 section 的 schema 里 `"class": "section"` 去掉（liquid，STYLE-GAP C6）；
  去掉之后这条 CSS 变成无害的空转，可以一并删。**静态站没有 `.section`，这条永远不匹配。**
- ℹ **`.gb-footer__input` 的底色目前看不出差别** —— `var(--color-input-background)` 眼下
  恰好也解析成白色。这条修的是**潜伏**问题（后台一改主题配色就会暴露），
  别因为「肉眼没差」把它删掉。

### 1u. 第九十轮的评论卡四处（板上就是这样，别"修"回去）

1. **4.76 的描边把相邻字形连成一个「气泡」是对的** —— 已与 `figma/screenshots/` 的稿图
   对照过，板上就是这样（OUTSIDE 0.25em，半径 16.5 大于字距，必然合并）。
   **不要当成描边过粗去调细。**
2. **它比 `.gb-science-card__value` 明显粗一倍** —— 那条是 0.125em（实现里 0.145em），
   这条是板上的 0.25em。两个数字不该统一。
3. **`ink-outline` 在这里必须给 `$steps: 72`** —— 默认 36 在 16.5px 半径下画出来是虚线。
   改半径就要同步改 steps。
4. **第 6 条起的 5 条评论是前 5 条的复制件** —— 需求方定的方案，为了让 More/Less 有东西
   可翻。HTML 里有注释标着，接评论 app 时删掉。**不是内容重复的 bug。**
5. **"See Less Reviews" 是自造文案** —— 板上没有收起态。待设计方裁决。
6. **总数 ≤ 5 时 More 按钮会自己消失** —— 有意的，控件不该看得见却什么都不做。
7. **小熊占位图不是设计稿里的东西** —— 板上 `191:5468` 是纯灰块，小熊是需求方要的占位。
   灰底仍在图下面（`contain`），所以看起来「图没铺满」也是有意的。
8. **`.gb-crev-card[hidden]` / `.gb-crev__more[hidden]` 两条重述规则不能删** ——
   UA 的 `[hidden]` 是 0-0-0，压不过 flex / inline-flex，删了分页就「隐藏不掉」。

### 1t. 第八十九轮的 Real Customer Reviews（板上就是这样，别"修"回去）

1. **只有第 1 条评论是 5 星，其余 4 条的第五颗只有 30% 透明度** —— 板上就是这么画的
   （`191:5463` fill a0.30）。不是漏画，**也不要改成半星**。
2. **只有第 1、3 条有 64×64 的灰块** —— 另外三条的 `Image` 节点 `visible: false`，
   卡高 324 与 240 差的 84 就是它。按"每条都该有图"报的都是错的。
3. **灰块本身就是占位**（`#d5d4d4`），板上没有真图，别去找图填。
4. **See More Reviews 上没有图标** —— 板里那个 24×24 icon `visible: false`，
   按钮宽 280 = 64 + 152 + 64 正好不含它。build.txt 会让人以为漏了一个。
5. **赞踩数字不会动、See More 点了没反应** —— 板上只有 5 条，没有第 6 条可展开，
   编出来就是造假数据。需求方确认只做 hover / press 态。**不是坏了。**
6. **第 1 条的标题是断句**（"…product that would"，之后没有了）—— 板上原文如此，
   照抄。待设计方补全，**不要自己续写**。
7. **按钮文字是白色，不是板上的 `#F5F1E9`** —— 沿用 `.gb-btn--lg`，没有为一个按钮
   去改 11 个页面共用的基类。
8. **手机端这个按钮 44 高，别处的 `--lg` 仍是 52** —— 44 是本模块作用域内的板值，
   基类未动。其它页面的手机稿是否也该 44，没查过。
9. **`gb-crev` 不是 `gb-reviews`** —— 后者是 index / pdp / our-story / how-gumi-works
   上的 testimonial 轮播，两者无关。

### 1s. 第八十七轮的六处

1. **`.gb-science-card__value` 的手机字号只在 `.gb-science--tight` 里是 36/40** ——
   这是同一组数字的**第三次反转**（r43 → r49 → r50 → 全局 → r87 加作用域）。
   非 tight 的卡片手机端就是 56/44/0，**不是漏改**；它们也**不需要 768–1280 的斜坡**，
   因为 767/768 两侧都是 56。动它之前先 `grep -n gb-science-card__value docs/CHANGELOG*.md`。
2. **`.gb-stats__note` 的 `@include mid { margin-top: 0 }` 必须排在 `narrow` / `tablet` 之后** ——
   `mid`（≤991）和 `narrow`（≤767）重叠，只有源码顺序决定胜负。991/992 的 34px 台阶是有意的。
3. **`@media (max-width: 369.98px)` 只写排列不写数值**，间距仍归上面那三档 `gap`（铁律 18）。
   `.98` 是为了覆盖 369~370 之间的小数视口，不是笔误。
4. **`.gb-header__panel` 关着时上下边框都是 transparent**（r86 只做了上边框，r87 补了下边框）。
5. **`.gb-nl-pane` 右内距 24 会让滚动态的右侧留白变成 40 对 24**（滚动条 16px），
   这是需求方点名的数值，已登记等裁决 —— 不要当成对齐 bug 改回 10。
6. **`snippets/gb-logo.liquid` 已推 live**（r87）。线上 logo 现在是真实的
   `…&width=124 1x, …&width=248 2x`，不再是 `src="0"`。

### 1r. 第八十六轮的五处

1. **`.gb-product__features` 是用 flex `order` 拉上去的，不是搬了 DOM。** 读屏与 Tab 仍按
   DOM 顺序，上方间距是 `.gb-product__info` 的 24 而非 head 内部的 16 —— 都是已知取舍。
   两条选择器（直接子 + `.shopify-block:has(...)`）**缺一不可**，别当重复删掉。
2. **`body.is-menu-open` 是 `overflow-x: clip; overflow-y: visible`，不是 `hidden`。**
   写成 `hidden` 会让 body 变成 sticky 的 scrollport，header 立刻消失。**不要"顺手统一"成
   和另外两处锁一样。**
3. **三处锁（菜单 / 弹窗 / 购物车抽屉）现在写法一致**：`html` 侧 `overflow: hidden`，
   `body` 侧 `overflow-x: clip; overflow-y: visible`。**看到 body 那半"不统一"别改回 `hidden`。**
   ⚠ 判据里"锁上之后滚轮推不动"这条**必须先 `smoothScroll.pause()`**（生产路径就是这样），
   否则 Lenis 的 `scrollTo` 会推动 `overflow:hidden` 的 html，读出一条假的泄漏。
4. **跑马灯手机档 88×36** 和它带来的约 13% 减速是需求方要求 + 我们选的数，不是 bug。
5. **`.gb-header__panel` 关着时 `border-top` 是 transparent 不是 0 宽** —— 0 宽会让盒子跳 1px。
6. **四处链接 hover 只变色、没有下划线**，是需求方点名的；**常驻下划线的行内链接（rich-text /
   法务小字 / cart continue）不在此列，保留**。

### 1q. 第八十五轮的九处

1. **`.gb-product__thumb` / `.gb-reel` 的 `:focus-visible` 不画外框**是需求方点名的，
   不是漏了 focus 样式：两者都在可滚容器里，全局的 `outline` 环四边都被裁掉。
   thumb 的焦点态**和选中态长得一样**（同一条绿边），这是明确要求，不要"补个区分"。
2. **`.gb-sub__plan` 的描边是 `::after` 覆盖环，不是 `border` 也不是 inset 阴影** ——
   两个替代写法各有硬理由写在源码注释里（border 会撑大 1px；`outline` 在 Safari 16.4
   以下不跟随圆角）。**看到 `::after` 别"简化"成 border。**
3. **`.gb-header__panel` 的 `border-top` 在 ≤767 是 0**，和既有的 `border-bottom: 0` 并排。
   手机是整屏抽屉，稿里两条边都没有。⚠ **这一条是我们的判断，需求方只说了"加 border-top"**，
   在"待设计方裁决"里挂着。
4. **`.is-static` 的 reels 轨道隐藏箭头、不是 disable**，也是取舍不是遗漏。
5. **`fits()` 只对 `loop` 轨道生效**。`.gb-expert__cards` 三张卡在 963~991 这 28px 里
   其实也"装得下"，但它是 `rewind` 轨道、设计上就该到头即停 —— **不要把这道门去掉**，
   `r85check` 有一条断言守着。
6. **线上首页 reels 只有 6 张**（其余两页 10 张）。6 张在 1440 仍然铺满轨道、
   逐格推进无空洞，**不是 bug**。
7. **`svg, img` 双选择器**（guarantee / 三处 logo）不是冗余：静态站是 `<svg>`、
   线上是 `<img>`，两边同一份 CSS。

### 2. 稿自身的问题 / 两稿冲突

- **只有 1440 与 390 两档有设计稿。** 768–1280 那一带没有稿，所有值要么是 `fluid()` 斜坡、
  要么是行为约束，**只能审「有没有坏」，不能审「像不像稿」**。
- **两稿冲突与稿自身 WIP 痕迹共 15 处，全部登记在
  [PROJECT-STATUS.md](PROJECT-STATUS.md) 的待决 A–D**，这里不重复。典型如：
  六处文案两块板不一样（实现一律取桌面版）、产品缩略图手机 6/桌面 5、FAQ 手风琴手机 8/桌面 6、
  PDP「Batch Tested Quality」在两块板上都是红色（像设计师的待办标记）。
- **science 三张卡的 eyebrow 都是 `Easy Habit`**、stats 四个数字只有 `21` 字距为 0 ——
  稿自身的 WIP 痕迹，历轮已判定不追。
- **上线前必须替换的占位内容**：Reviews 专家卡的竞品名 `Grüns`、Shipping 全页美国配送文案
  （Alaska / Hawaii / US Territories / $65 门槛，而 Gumi 是澳洲品牌）、Privacy 正文 lorem ipsum、
  PDP 页脚 6 条 `Accordion Closed` / `Text here`、Get in Touch 的 Enquiry Type 列表。
  **这些混在正文里看不出来，不单独列清单就一定会带上线。**
- ⚠ **第五十八/五十九轮又添了两条占位**：购物车的产品缩略图与礼物图是稿里的 `#D9D9D9`
  方块（待决 AZ）；delivery interval 下拉里的 `2/6/8 Weeks` 是编的（待决 BD）。
  完整清单在 [PROJECT-STATUS.md](PROJECT-STATUS.md) 的「交付前必须替换的占位内容」。

### 2a. 抽屉关闭后锁还会多留 0.7s（第五十二轮）

`is-menu-open` 不再和 `is-open` 同一帧摘掉 —— 它要等抽屉滑完（`$t-drawer` 0.7s）。
所以**点了关闭之后页面还有大半秒不能滚**，这是有意的：立刻解锁会把滚动条还回来，
抽屉的包含块当场窄 15px，而它还在滑出、完全看得见（实测 700 → 685）。

⚠ 时长由 `.gb-header__panel` 在 `narrow` 档用 `--modal-exit` 声明，**值是 `$t-drawer`
不是 `$t-panel`** —— 桌面那套是 `grid-template-rows` 收起的下拉（0.35s），
手机这套是 `fixed` + `translateX` 滑出的抽屉（0.7s），两者时长差一倍。
挂到基础规则上会让手机档继承桌面的时长，锁提前 0.35s 解开，抖动照旧。
`prefers-reduced-motion` 下 reset 把时长归零，`modalExitMs()` 返回 0、立即解锁。

### 2b. 锁滚动时 `position: fixed` 的覆盖层会变宽（第四十八轮）

弹窗打开、页面锁 `overflow: hidden` 之后，`.gb-nl-modal` / `.gb-rv-modal` / `.gb-promo-modal`
这些 fixed 覆盖层的宽度会从 1425 长到 1440（正好一个滚动条）。**这是对的**：fixed 的包含块
是视口，滚动条消失后可视区真的变宽了。它们此时要么正在打开（用户只看到它出现，看不到"变宽"）、
要么还关着不可见。

**不要给 fixed 覆盖层也补 `padding-right`** —— 那会让遮罩盖不满右边那 15px。
补偿只属于滚动元素（`html`），且**只补一次**：第四十八轮修的就是 `html` 与 `body`
各补一次、把宽度花掉两倍，内容反而左移半个滚动条。判据 `tools/scrolllock.py`。

⚠ **但「关闭时也变宽/变窄」不在这条豁免里**（第四十九轮修的另一半）。`close()` 曾在
摘掉 `is-open` 的同一帧摘掉 `is-modal-open`，滚动条立刻回来、fixed 盒子当场缩回 1425，
而 panel 此时 `opacity` 还是 1 —— 用户看到它在淡出途中左跳 7.5px。现在解锁推迟到
淡出结束，时长由弹窗自己在 CSS 里用 `--modal-exit` 声明，`main.js` 读它。
**加新弹窗时别忘了给根元素也写一条 `--modal-exit`**，漏了会退回立即解锁（值缺省为 0）。

### 3. 探针假信号类（工具的毛病，不是页面的）

**第五十三轮复查一口气踩到三个，都是取量方式错、不是页面错**（复查时全部报红，
换量法之后全部为正）：

- **两个元素共享一张截图时，量到的可能是另一个**。想量「图片墨迹离波浪多远」，
  截了 `.gb-promo-card__art` 整个半边 —— 波浪就在这张图里，而且比图片更靠下，
  于是「墨迹底边」量到的一直是波浪自己，算出 −34.9 的假重叠。
  **正解不靠截图**：图片的透明留白是**文件自身的属性**（`images/promo-art.png`
  的 alpha 实测上 2.32% / 下 2.65% / 左 3.54% / 右 4.81%），从 DOM 盒子直接推墨迹边即可。
  实测净距 320→20.3 / 375→14.8 / **390→13.4（最紧）** / 575→62.3 / 767→72.9，全部为正。
- **圆角会污染 ink bbox 的基准色**。`ink_bbox` 拿左上角像素当背景，而
  `.gb-promo-card__art` 有 `border-radius`，四角露出的卡片白被当成了墨迹，
  bbox 因此一路顶到元素边缘。要么避开圆角只取中段，要么根本别用截图。
- **`animated` 加上之后不能立刻取量**。`fadeInUp` 有 30px 位移，
  加完 class 就读会读到位移途中的值：tight 组的 head→cards 量出 **18**，
  静置后是 **48**（gap 22 + margin 26，正确）。**48 − 30 = 18**，差的正是那 30px 位移。


- **`hardbreaks.py` 恒定 6 条 MISSING** —— 是成分辐射图 PNG 里的文字，不是 DOM。误报。
- **`rwd.py` 不再把横向轨道外的卡片报成「被裁」**（第四十一轮补的豁免）。原判据找
  「最近一个真的会裁的祖先」时跳过 `auto|scroll`，一路找到 `body`（它是 `overflow-x: hidden`），
  于是把**待滑入的卡片**判成被 body 裁掉。豁免**只认 x 轴**：`overflow-x: hidden` 会把另一轴
  强制算成 `auto`，把 y 也算进去会放过真正被裁、只是纵向溢出几像素的盒子。
- **reviews 的 `pagefit` 缺口是 −2230.8**，其中 288 是第四十一轮删掉的占位框。
  与 index / pdp / our-story / how-gumi-works 那几个 −400 同源，都是「app 产出的内容只做壳」
  这条边界的结果，不是还原度问题。
- **`font-check.html` 有两条断言恒假**：「波浪归属：section 自带下边缘形状」与
  「裁切型宿主也不用特例」。第十九轮把占位方案从 `::after` 换成
  `padding-bottom: calc(… + var(--sc-h))`，`::after` 的 `content` 现在读回 `none`。
  **从第十九轮起一直红**。待决 G。（一个恒假的断言和恒真的一样有害。）
- **截图脚本的 SETTLE 只写 `.wowo` 会切掉半截标题**，必须带上 reveal 那一组：
  ```
  .wowo,.gb-float-art,[data-line-reveal],.gb-line-mask__inner,.gb-ink-halo{
    opacity:1!important;transform:none!important;animation:none!important}
  ```
  漏了它行遮罩停在第 0 帧，看起来像页面溢出。`r41check.py` 里已是全的，别抄旧的短版本。
  memory: `kill-animations-blanks-reveal-blocks`。
- **borders 的 computed 值会被取整**：390 档 `border-bottom-width: 0.48px` 读回 `1px`，
  `1.43px` 也读回 `1px`。DPR=1 下的既有行为，不是没生效。
- **`file://` 下 CSS mask 引用外部文件被 CORS 拦掉**（origin null），mask 静默变空 →
  **被遮罩元素整块消失**，而 computed style 一切正常。本项目三个 mask 全部内联在
  `customstyle.scss` 的 masks 段，**不要建议改回 url() 外链**。看到元素消失先想这条。
- **截图必须等 1700ms**：wowo 播 0.7s、1500ms 才卸 class，早拍会拍到半播状态（肉眼像「重影」）。
- **断点隐藏的元素 opacity 恒 0**，别当成「卡住的 wowo」。`shoot.py` 用
  `el.offsetParent === null` 跳过它们。
- **headless 直连时 `(hover: hover)` 恒 false** → 全站 hover 规则一条都不生效。
  **验 hover 必须用 Playwright**（它不占这个限制）。
- **元素截图按边界盒裁**：descender / `ink-outline()` 的描边光晕本来就在盒外，
  会被误读成「渲染被切」。留白 clip 再截。
- **`getComputedStyle` 读 `--x` 拿到未求值的字符串**，不是像素；**`letter-spacing: 0`
  的 computed 就是 `normal`**，与「没写」不可区分。
- **快照前必须钉死 `Math.random`** —— 不钉的话 word-pop / float-art 的抖动会让同一份 CSS
  连采两次就有 260+ 处假差异，真信号全被埋掉。

**第七十轮：`livediff.py` 报的「线上缺这个类」有一半是假的**，逐条查证后 4 条不用做
（全表在 [LIVE-BACKLOG.md](LIVE-BACKLOG.md) 第三节，**别再报一次**）：

- **`gb-logo-scroll__img--abc` / `--vogue` / `--wellbeing`** —— 线上有 `class_suffix`
  setting，`index.json` 三个 block 的值也都填好了。类名由 `{% assign %}` 拼出来，
  literal 搜不到而已。**setting 拼接的前缀抑制永远不彻底，报缺失前先看 schema。**
- **`gb-stats.title` 的换行** —— 静态站本来就是裸 `<br>`（全断点断行），线上写法正确。
  ⚠ **不是所有换行都该是 `gb-br-narrow`**，对稿前先看静态站那一处到底是哪种。
- **`gb-rv-panel__glyph`** —— 第六十六轮已适配，`customstyle.scss:1888` 特意把规则挂在
  `svg` 而不是这个 wrapper 上，就因为线上是裸的。补上 wrapper 反而破坏那条假设。
- **`gb-acc-body__media`** —— 对方 2026-09-04 早上补的 `gb-product.liquid` 里已经有了。

---


### 4. 第七十三～一二三轮状态段的沉淀（按轮次倒序，原文照搬）

从 HANDOFF 顶部 40 个逐轮状态段里抽出的「不要报成 bug」与 ⚠ 提醒。
推送清单 / 三方对比 / 判据数字已移出（见 [PUSH-LOG.md](PUSH-LOG.md) 与
[archive/HANDOFF-STATUS-r73-r123.md](archive/HANDOFF-STATUS-r73-r123.md)）。

**第一二三轮**

> ⚠ **不要报成 bug**（第一二三轮）：
> 1. **`.gb-rv-modal` / `.gb-rv-panel*` 整套没了，是客户要求的** —— r11/r66/r81/r117 一路做的
>    reel 弹窗被本轮推翻。**别当成"漏掉了弹窗"补回来。**
> 2. **`.gb-reel` 现在是 `<div>` 不是 `<button>`** —— `<button>` 里不能放 `<video controls>`
>    （无效 HTML，控件点击还会冒泡回按钮）。交互在内层 `.gb-reel__trigger` 上。
> 3. **r121 给 `.gb-reel` 加的 `.is-refocused` opt-out 已删** —— 卡片不再从任何弹窗接回焦点，
>    那条已是死规则。`refocusring.py` 的 reel case 一并删了。**没有弹窗就别再加回来。**
> 4. **`.gb-reel__video` 的 `$c-ink` 底不违反 r120** —— 那是竖版 reel 的信箱边（播放器底色），
>    不是 r120 删掉的占位灰。
> 5. **`embedUrl()` 还在，只是搬了家** —— 静态站有 2 张 YouTube 占位卡，就地播放要认它。
>    file:// 下 YouTube 拒绝 null origin，那两张会显示 `.gb-reel__offline` 说明块，**不是坏了**。
> 6. **三页共 30 张 reel 点了没反应** —— product / our-story / how-gumi-works 后台**一个视频都没填**
>    （首页 6 张填了）。改前是打开空弹窗，同样没用。`docs/LIVE-BACKLOG.md` 第〇之三条，
>    `reelplay.py` 把它单列成 backlog 汇总、**不计 red**。
> 7. **首页 6 张 reel 是同一个 mp4** —— 后台填的就是同一个文件，等客户真素材。
>
> ⚠ **本轮改了四份判据，都是「锚点随弹窗消失」不是回归**：`refocusring`（删 reel case）、
> `placeholderbg`（存活守卫报 `.gb-rv-panel__video` 0 个，从 TARGETS 移除）、
> `scrolllock`（两个 reel-video case 删除）、`font-check.html`（弹窗外壳断言换成就地播放外壳）。
>
> ⚠⚠ **`reelplay.py` 的 `--strip` 第一版是假的反向** —— 只删 hook 属性，但事件早已绑定、
> 判据选择器还有 class 兜底，反向跑照样全绿。**改成删 `data-video` + 植入假弹窗才真的会红。**
> 写反向验证时先确认它真的能红，否则等于没写。
>
> ---

**第一二二轮**

> ⚠ **不要报成 bug**（第一二二轮）：
> 1. **hero 的 `data-line-sequence` / `data-seq-step` 在 HTML 里找不到** —— 它们是
>    `lineReveal.wireHero()` **运行时注入**的。hero 的标记在对方的 `sections/gb-hero.liquid` 里，
>    越界要授权，所以在 JS 里挂。**不是漏写属性。**
> 2. **markup 里的 `delay-in-2` / `delay-in-3` 还在，且没生效** —— 那两个类在对方的 liquid 里删不掉，
>    靠 `[data-seq-step].wowo.animated`（0-3-0）压过 `.delay-in-N`（0-1-0）。**不是死代码没清。**
> 3. **`wowo.play()` 的剥类时机改成了 `1500 + 自身 delay`** —— 这是**对 Terra 原版的有意偏离**。
>    固定 1500 假设延迟只是 delay-in-N 那种小台阶；390 档 usps 延迟 900ms + 700ms 动画 = 1600ms，
>    原版会在淡入 86% 时剥类、元素当场跳终态。**别"改回 Terra 一致"。**
> 4. **读 `[data-seq-step]` 的 computed `animation-delay` 前必须把 `.wowo`/`.animated` 加回去** ——
>    规则只在这两个类在时生效，而 wowo 播完就剥掉它们。`heroseq.py` 线上首跑的 1 red 就是这个，
>    不是规则没上线。
> 5. **`/cdn/shop/t/2/assets/*` 不是当前 live 主题的资源**（那份 css 停在 `20260907-r73`）。
>    查线上产物别用这个路径，会得出"根本没推上去"的错误结论。
> 6. **`tools/revealcheck.py` FAIL 12（`ink-halo opacity 0`）是既有欠账** —— 已在 r121 基线上
>    核对过，同样 FAIL 12。是第五十五轮起就欠着的那批验证之一，**不是 r122 打坏的**。
> 7. **`menutab.py` E 段那条 flaky 又出现了一次** —— 复跑即 58/0，同 r121 第 6 条。
>
> ---

**第一二一轮**

> ⚠ **不要报成 bug**（第一二一轮）：
> 1. **Escape 关闭后键盘用户看不到焦点在哪** —— 焦点确实还在触发按钮上（再 Tab 可继续），
>    只是没有可见指示。**这是客户点名要去掉的效果，是 a11y 取舍不是缺陷。**
> 2. **`.is-refocused` 类会短暂出现在按钮上** —— 它是 `returnFocus()` 打的标记，
>    下一次真实按键或失焦就清掉。**不是没清理的状态。**
> 3. **`.gb-reel` 有一条自己的 opt-out，别当成重复** —— 全局规则只撤 `outline`，而 reel 的
>    焦点样式是**子元素 `.gb-reel__media` 的 scale**（r81 起 focus 镜像 hover），
>    特异性更高且更靠后，不单独写就撤不掉。
> 4. **`.gb-sub__select` 故意没有 opt-out** —— 它是原生 `<select>`（r76 退回原生），
>    dropdown 模块不认领它，写了永远匹配不上。**第一版写过，判据发现后删了，别再加回来。**
> 5. **不要用 `mouseenter` 清标记** —— 菜单关闭时布局变化会把 toggle 滑到静止的光标下方，
>    Chrome 补发 `mouseenter`，标记在设上的同一瞬间被清掉。hover 用 CSS `:not(:hover)` 解决。
> 6. **`menutab.py` E 段的 `gb-header__sublink` 偶发 1 red 是 flaky** —— `elementFromPoint`
>    撞上抽屉滑入动画。已二分验证（单退 JS 绿、单退 CSS 绿、完整版连跑三次全绿）。
>    **再遇到先复跑三次，别直接当回归查。**
> 7. **`r121check.py` 的 faq 走 `/pages/faq`，不是 `/pages/faqs`** —— 后者是 404。
>    第一次线上跑就是被**存活守卫**抓住的；没有守卫，负向断言会在 404 页上恒真报绿。
> 8. **`.gb-page-hero--center` 有 7 个页面在用，不是 scss 注释写的 5 个** ——
>    注释漏了 our-story 与 how-gumi-works。**判据按 grep 写，别抄注释。**
>
> ---

**第一二〇轮**

> ⚠ **不要报成 bug**（第一二〇轮）：
> 1. **所有占位媒体盒现在是纯空白，没有灰底** —— 这是**需求方在两个口径里明确选的 B**
>    （A 只去掉真图已上线处的、B 一律去掉）。它**推翻了** `PROJECT-STATUS.md`
>    「内容真实性」里「占位保持占位」的旧规则。**别按 Figma 稿把 `#d9d9d9` 补回来。**
> 2. **`$c-gray-200: #d9d9d9` 变量还在调色板里** —— `$color-border` 还指着它，不是漏删。
>    编译产物里 `#d9d9d9` 已经**一个都不剩**（`$color-border` 本身零消费，见「顺带发现」）。
> 3. **`.gb-ingredients__disc` 的 `--box-bg: $c-sand` 保留** —— 沙色是真实设计色不是占位灰。
>    `.gb-scallop-box` 的默认 `--box-bg` 才改成了 `transparent`。
> 4. **`.gb-rv-modal.has-video .gb-rv-panel__video { background: $c-ink }` 保留** ——
>    那是有视频时的深色底，不是占位色。
> 5. **HTML 里还有 58 处 `TODO client image: … grey placeholder`** —— 措辞里的 grey 过时了，
>    但 TODO 本身（此处待客户图）仍然成立，**故意没动**。只改了 `science.html` /
>    `how-gumi-works.html` / `our-story.html` 三处写着「灰底是设计占位所以保留」的注释。
> 6. **`placeholderbg.py --live` 对 `.gb-cart-item__media` / `.gb-cart__gift-media` 报 `n/a`** ——
>    线上这两个类渲染不出来（gift 见 r119 第 3 条，行项要购物车非空），**判据已登记为盲区**，
>    不是断言失败。静态站两个都在，group B 照常守着。
> 7. **See More Reviews 一次加载 6 个是对方做的，不是我们** —— 本轮回读发现
>    `gb-app-section.liquid` 的 default 与两个 template JSON 的存值都已 4 → 6，
>    线上实测 `step=6`、点一次 5 → 11。**我们零改动**，别记成我方成果、也别再推一遍。
>
> ⚠ **`r119check.py` 又踩了写死 `$build` 的坑**（HANDOFF r119 自己第 7 条刚记过），
> 本轮已改成「≥」。**写单轮判据时 check 侧和 live 侧要各改一次。**
>
> ---

**第一一九轮**

> ⚠ **不要报成 bug**（第一一九轮）：
> 1. **collection 页只改了 font-family，没改字号字重** —— 那是 Horizon 自己的字号阶梯，
>    这个模板**没有稿**，没有可依据的数值来源。别按别的页面的板值去"补齐"。
> 2. **`<body>` 顶部那个 skip link 仍是 Inter** —— 页面上有两个：页内的
>    「Skip to results list」在 `#MainContent` 内、已修；全局那个「Skip to content」
>    在 layout 层、每页都有，不在钩子内，本轮没动。
> 3. **`.gb-cart__gift-media` 的圆角线上看不到** —— 对方的 `gb-cart-drawer.liquid`
>    目前不渲染 `.gb-cart__gift*` 任何元素（线上实测 0 个），静态站已验。不是没生效。
> 4. **编译产物里字体栈不带引号** —— `#{}` 插值会剥引号，CSS 里合法，
>    已用**真产物**注入线上实测生效。别"顺手加回引号"当成修 bug。
> 5. **改的是变量不是元素** —— `.product-badges` 把
>    `--badge-font-family: var(--font-body--family)` 写在**内联 style** 上，选择器压不过；
>    钩子上重声明 `--font-body--family` 才穿得过去。只重声明 `--badge-font-family` 实测无效。
> 6. **404 页的商品价格与角标仍是 Inter** —— 本轮只覆盖 collection 模板，
>    需求方只点了这一页。是否全站统一见 `docs/LIVE-BACKLOG.md`。
> 7. **`$build` 写死的判据在每个后续轮次都会假性转红** —— 本轮 `r117check.py` 与
>    `r117live.py` **两份**都踩了（一份 static、一份 live），都已改成「≥」。
>    **写单轮判据时 check 侧和 live 侧要各改一次，修一边不够。**
>
> ---

**第一一八轮**

> ⚠ **不要报成 bug**（第一一八轮）：
> 1. **线上 `.gb-cart` 永远带 `is-open`** —— `gb-cart-drawer.liquid` 三个分支都写死，
>    抽屉关掉它也不掉。它是惰性的（显隐由外层 `<dialog>` 决定），**不是状态没清理**。
> 2. **`modal.showing()` 的两个守卫都不能删** —— `[data-modal-close]` 删了会去认领主题那两个
>    分支、和 Horizon 抢同一个抽屉；`getClientRects()` 删了会关一个看不见的抽屉并为它锁页面。
> 3. **兜底放在 `close()` 而不是 `init()` 是刻意的** —— 那个 `empty-cart-template` 是
>    **运行时注入**的（删掉最后一件商品时回放），init 时的一次扫描根本抓不到。
> 4. **`/cart` 上点遮罩本来就能关** —— 那走主题的 `on:click`。第一一七轮实测「能关」没有错，
>    只是撞上了三个分支里接线不同的另外两个。**一个 snippet 两种接线，测到哪个看购物车状态。**
>
> ⚠ **建议转给主题团队**：根治是把 `empty-cart-template` 里的 `data-modal-close` 改成
> `on:click="#cart-drawer/close"`，让三个分支一致。我方兜底与它不冲突。
>
> ---

**第一一七轮**

> ⚠ **theirs 那 1 个是 `templates/page.science.json`** —— 对方在后台重编排了 science 页，
> 把我们 r116 填的 CTA 改成 `Shop now` / `shopify://collections`，4 个 `wave_*` 并成 1 个。
> **本轮零 template 推送，未覆盖。**
>
> 判据：线上 `tools/r117live.py --cart` **11/0**；静态站 `tools/r117check.py` **15/0**
> （旧 css+js 上 8 red）；回归 `r116check` 9/0、`menutab` 58/0、`scrolllock` 44 条 0 failed、`rwd` 全绿。
>
> ⚠ **不要报成 bug**（第一一七轮）：
> 1. **静态站 footer 现在有 4 个 social** —— 线上一直是 4 个（Snapchat 是对方 r114 前加的），
>    本轮是静态站补齐。给的那段 SVG 写死 `#B5ED61`，入库时改回 `currentColor` 与其余三个一致。
> 2. **`.gb-cart__checkout` 上没有 `cursor`，在 `.gb-cart__bar` 上** —— 故意的：
>    同规则里的 `pointer-events: none` 会让光标解析退回父元素，写在按钮上永远看不见。
> 3. **`cartDrawer` 模块在多数页面什么都不做** —— 它只处理 `/cart` 那种「dialog 开着、
>    `<theme-drawer>` 不知道」的分裂状态。`/cart` reload 后也可能不复现，那不是修复失效。
> 4. **`--page-width` 填的是 1440 不是 1280** —— Horizon 这个变量**含两侧 margin**
>    （自身值是 `calc(90rem + margin*2)`）。本轮按内容宽填过一次，三档各多缩进 80，
>    `r117live` 6 red 抓到后修正。**别"顺手改回内容宽"。**
> 5. **`docs/LIQUID-TODO-reels.md` 整份已作废** —— 三处 hook 对方做了两处、第三处 r66 被
>    「play 图标完全不显示」取代。文档留着但**不要照着做**，真缺口是 schema 只吃上传。
> 6. **线上 reel 仍播不了视频** —— 通道通了，但 `video_embed` 还没值，要在主题编辑器里填。
> 7. **science 页 CTA 现在是 `Shop now`（小写 n）** —— 对方后台改的，不是我们推错。
> 8. **`.gb-rich-table th:first-child` 仍是 124** —— 本轮提过改成自适应，需求方当场撤销。
>    另：该表是 `table-layout: fixed`，fixed 下 `width:auto` 是平分不是按内容收缩。
>
> ⚠⚠ **等需求方在后台做**（`docs/LIVE-BACKLOG.md` 第 0 条）：Contact 两处链接要指向
> `/pages/contact`，但 header 那条在 Shopify 导航菜单、footer 那条在 `footer-group.json`，
> **主题代码里没有可改的地方**；`gb-footer.liquid` 的 `link_4_url` 只是 schema default，改了不生效。
>
> ---

**第一一六轮**

> ⚠ **不要报成 bug**（第一一六轮）：
> 1. **静态站 highlight-card 仍是 #d9d9d9 灰盒** —— `&:has(img)` 恒不匹配（静态站没有 `<img>`，
>    稿里本来就是灰占位）。不是没生效；`r116check` 第 4 组注入一个 `<img>` 复现了线上条件。
> 2. **桌面 Tab 跳过菜单里 14 个手机专用链接** —— 祖先 `display:none`，本就不在 tab 序。
>    挑「看得见的」只能用 `getClientRects().length`，computed `display` 看不出祖先被隐藏。
> 3. **`past()` 那个接缝不能删** —— panel 是 `<header>` 最后一个子元素，走完 cart 的默认下一站
>    正是菜单第一个，删了 Tab 在 header 里**无限循环**。第一版漏了它，`menutab.py` A 段当场转红。
> 4. **`menutab.py` 的 `WHERE` 多返回了 `aria`** —— 线上 cart 链接里有角标 `0`，`textContent`
>    非空、回退不到 `aria-label`；静态站没角标，所以这个假信号**只在线上转红**。不是页面缺 cart。
> 5. **science 的 CTA 不是本轮做的** —— 按钮与 6 条断点差额是第一一五轮的，本轮只填了
>    `templates/page.science.json` 的两个 setting。净距 48 仍然**只能量不能读规则**。
> 6. **回读的 `customstyle.css` 是展开格式** —— 主题层回读是原样，压缩只在 CDN 那一侧。
>
> ---

**第一一五轮**

> ⚠ **不要报成 bug**（第一一五轮）：
> 1. **`grep gb-br-wide customstyle.css` 现在是 0，不是漏编译** —— 那条规则只剩一句
>    `@include narrow { display:none }`，需求方要求手机端也显示，删掉后 Sass 不输出空规则。
> 2. **`^^` 与 `//` 现在渲染结果相同** —— 上一条的连带后果，全站再没有「只在桌面断」的能力。
>    `gb-lines.liquid` 的 schema 说明文字仍写着「desktop only」，**是过期文案，不是 bug**。
> 3. **静态站 `how-gumi-works.html` 的 dosed 标题手机端 4 行（原 3 行）** —— 同上，
>    是需求方要的效果的连带面。**线上那句没有任何标记，不受影响**，别拿线上去反推静态站坏了。
> 4. **`.gb-science__cta` 的 `margin-top` 不是 48** —— 它是 flex 子元素，`__inner` 自己的
>    `gap` 已经垫在上面，写的是**差额**（桌面 tight 26、手机 tight 0…）。净距才是 48，
>    判据用 `offsetTop` 量。改 `__inner` 的 gap 必须同步改这 6 条。第九十六轮就栽过一次。
> 5. **`toggle` 的 `focus` 里那句 `:focus-visible` 判断不能删** —— 删了鼠标点击会
>    「开→click 再关」，表现为点菜单没反应。**`skipFocusOpen` 也不能删** ——
>    Escape 把焦点交还 toggle 时 `:focus-visible` 仍为真，会原地重开。
> 6. **桌面 Tab 顺序里 logo / Shop now / account / cart 仍排在菜单内容之前** ——
>    DOM 顺序如此，面板视觉上也确实在整条 bar 之下。要改成 toggle 直接跳进菜单需另行确认。
> 7. **线上暂时看不到那颗 Shop Now** —— `cta_label` 留空就不渲染，等 `page.science.json`
>    填值或需求方在主题编辑器里填。**不是没生效**，线上已实测计数为 0 且无 Liquid error。
> 8. **reviews h1 在 390 仍是 3 行，但断行是生效的** —— 验它不能数行数，要读**行内容**：
>    现在是「Aussies are / obsessed. / **Here's why.**」，改前是「Aussies are /
>    obsessed. Here's / why.」。行数不变是因为该页 hero 线上多带 `--lg`（早已登记为忽略）。
> 9. **本轮 `customstyle.css` 回读是展开格式、与本地逐字节一致** —— 与第 915 行记的
>    「pull 回来是压缩单行」不同。**压缩是间歇性的**，线上判据两种形式都要能匹配。
>
> ---

**第一一四轮**

> ⚠ **不要报成 bug**（第一一四轮）：
> 1. **`gb-expert__title`「Recommended / by experts」现在桌面也断行，是需求方取值** ——
>    桌面稿这句本来是**一行**（1072×48）。需求方两次要求，按 client override 处理，**别按稿改回去**。
> 2. **`gb-footer.liquid` 的 Snapchat 链接是对方加的，我们保留了** —— 补 `title` 是在**对方最新版之上**
>    补的，不是推回我们的旧版本。该文件**已被对方回退过两次**，每次推它前都要单独确认。
> 3. **reviews 的 h1 在 390 是 3 行、手机稿是 2 行** —— 该页 hero 线上多带 `--lg`，
>    是早已登记为「忽略」的线上/静态差异，与断行改动无关。
> 4. **标记必须写在行尾 + 真回车**（`//` / `^^`），写在行中间会**原样印到页面上**。见 `BR-LINES.md` 末尾。
>
> ---

**第一一三轮**

> ⚠⚠ **本轮推了 2 个 `templates/*.json`，是需求方明确授权的红线例外，不是新常态。**
> 做法记在 PUSH-LOG：基于**当轮 pull 的线上最新版**改（不是基线）、每文件只动 1 行、
> 推前再单拉一次确认没被人改。
>
> ⚠ **`.gb-br-narrow` 不是 bug，别去删那条隐藏规则** —— 需求方问「为什么要隐藏」，
> 对稿结论是**类是对的、后台数据填错了**：普通回车 = 只在手机断，要两端都断得在**行尾打 `//`**。
> 三处逐一对稿的结论见 `docs/BR-LINES.md` 末尾的补记（reviews 那处**本来就该只在手机断**）。
>
> 1. **菜单 Tab 进去是 25 个看不见的落点** —— 面板和二级列表是用几何关掉的（`0fr` / `translateX`），
>    不是 `display:none`，里面的链接一直在 tab 序列里。改成「焦点落到哪就打开哪」。
> 2. **footer 链接 hover 一直在变色，只是看不见** —— `#f4fce7 → #ffffff` 落在 `#004128` 上，
>    RGB 距离 26.6。改成 hover 到 `$c-lime`（148.8）。
>
> 判据：`tools/menutab.py` **32/0**（旧 JS 上 12 red，线上推后 **32/0**）、
> `tools/footerhover.py` **63/0**（旧 CSS 上 26 red，线上推后 **64/0**）；回归 `r112check` 49/0、`r110check` 0 red、
> `r107check` 82/0、**`scrolllock.py` 44 条 0 failed**（`main.js` 动了滚动锁那段）。
>
> ⚠ **不要报成 bug**（第一一三轮新增）：
> 1. **`set()` 开头的 `if (open === wasOpen) return;` 不能删** —— 面板开着时每按一次 Tab 都触发
>    `focusin`，再走一遍 open 分支会在已锁定状态下重测 `--scrollbar-w`（读到 0），补偿归零、整页横跳。
> 2. **`focusout` 里 `relatedTarget` 为 null 时故意不关菜单** —— 那是浏览器 chrome 或点在面板空白处。
> 3. **手机 bar 的 `inert` 用 `getComputedStyle(panel).position === "fixed"` 判定，不是重写断点** ——
>    盖不盖得住由布局说了算；且必须**先把焦点交给抽屉、再 inert**，否则焦点被丢回 `<body>`。
> 4. **`.gb-footer__social-link` 没跟着改成 lime** —— 它静止色就是 lime，hover 到白色本来就看得见。
> 5. **判据里手机档每步要等抽屉停稳**（`$t-drawer` 0.7s，轮询 transform 连续 3 帧不变），
>    等 55ms 会把 19 个落点全报成「在屏幕外」。
> 6. **挑「看得见的元素」只能用 `getClientRects().length > 0`** —— `display:none` 的祖先
>    不会让子元素的 computed `display` 变成 none，用 computed 去挑会挑中隐藏那份、`focus()` 静默失效。
>
> ---

**第一一二轮**

> ⚠ **CDN 交付的 css/js 会被 Shopify 再压一道**（243606 → 239846），逐字节判据只能用在
> `theme pull` 回读上，CDN 一侧只能按压缩形式 grep。
>
> ⚠ **不要报成 bug**（第一一二轮新增）：
> 1. **第一〇九轮那条 `[class*="captcha"]:empty` 是被替换掉的，不是被删错** —— 它两个前提都错：
>    容器里有 iframe + textarea（`:empty` 永不匹配），且**页面加载时根本不在 DOM 里**
>    （`captcha-bootstrap` 监听 `focusin`/`change`，用户点进输入框才注入）。那条规则一直是惰性的。
> 2. **captcha 容器用绝对定位而不是 `display:none`，是刻意的** —— 隐形 widget 仍然活着，
>    hCaptcha 甩验证题就在这个容器里开挑战框，折叠掉 = 表单永远提交不了。
>    键在 `data-size="invisible"`：改成勾选框模式规则自动失效、照常占位，**失效方向是安全那边**。
>    规则**不限定表单**也是刻意的（footer 订阅、账户登录同样会被注入）。
> 3. **手机档 panel 滚、桌面档内容列滚，是两套不同的机制，不是漏改一处** ——
>    桌面是左右两列，panel 自身永不溢出。全程只允许有一个滚动容器。
> 4. **`overflow:hidden` 的元素用脚本设 `scrollTop` 是能动的** —— 探针只看
>    `scrollHeight > clientHeight` 会把「裁掉且滚不动」误判成「能滚」，必须同时看 computed `overflow-y`。
> 5. **768–1280 有 `--pp-k` 整体缩放**，短视口不一定把卡压到 `max-height`
>    （768×500 实测 358 高、根本不溢出）。判据里「必须有的滚」只能在 `panelH >= vh - 48` 时断言。
> 6. **`main.js` 的 `PREVENT` 加 `.gb-promo-panel` 不是为了修 bug** —— `modal.open()` 已经
>    `smoothScroll.pause()`，Lenis 本就让出滚轮。这是补齐文件自己写的「每个 `overflow-y:auto`
>    容器都要登记」约定（`.gb-promo-panel__content` 一直没登记），并防将来有人不走 `modal.open`。
>
> ⚠⚠ **等裁决（跨轮未决）**：
> - **promo 表单没有 `data-promo-form`** —— `main.js` 的 `promoModal.bindForm` 找的正是这个
>   hook，线上填完邮箱**不会切到「复制优惠码」那一屏**，而是整页 POST 给 `/contact`。
>   静态站有这个属性所以一直没暴露。`snippets/gb-promo-modal.liquid` **是对方的文件，未动**。
> - **购物车垃圾桶**（第一一〇轮）：实测已等于稿，唯一差异是容器 18×20 vs 板值 16×16，
>   而 18×20 是第五十九轮需求方自己推翻板值定的。**没动**。

**第一一一轮**

> ⚠ **全站第一次用 `title` 属性**。约定：**`title` 的值必须与同一元素的 `aria-label` 相同** ——
> 不同的话部分辅助技术会读成两个互相冲突的名字。以后再加别处 tooltip 照此办理，别自造第二套措辞。
>
> ⚠ **`gb-footer.liquid` 每次推前都要单独确认对方没动** —— 第一〇三轮他们在这个文件里
> 回退过我们的 `gb-lines` 改动。本轮拉了两次（间隔 10 分钟）确认。
>
> ⚠ **对方新增了 `snippets/gb-promo-modal.liquid`** —— 首单 promo 弹窗做出来了，
> `LIVE-GAP.md` 第一节的模块缺口可以划掉一条。**我们没碰它。**
>
> ⚠ **基线目录现在有两套并存**：并行会话用轮次号（`baseline-r108`…），
> 本窗口用时间戳（`baseline-20260908-0800` / `-0900`）。**互不覆盖，别删对方的。**

**第一一〇轮**

> ⚠ **基线名从这轮起改用时间戳** → **`baseline-20260908-0851/`**（624 文件）。
> 轮次号已经撞过四次，别再用它命名基线。
> ⚠ **`$build` 跳过了 `r109`** —— 上一批标题「第一〇九轮」配的是 `$build` r108。
> 这轮把标题号与 build 号对齐，代价是跳一个缓存戳。**此后两者一致。**
>
> 判据：`tools/r110check.py` 0 red（静态）、`tools/r110live.py --password 1234` 13/0（线上）、
> 前两轮回归 `r107check` 82/0 + `r107states` 0 red + `r107live` 31/0。
>
> ⚠⚠ **等裁决：购物车垃圾桶**。需求方要求「还原设计」，但**实测已经等于稿** ——
> path 逐字符相同、图形 12×13.33、stroke 1.33333 全部与 `Frame 1984078213/icon` 一致。
> 唯一差异是按钮容器 **18×20 vs 板值 16×16**，而 18×20 是**第五十九轮需求方自己拍板
> 推翻板值的**（代码里标着 `client r59`）。**没动**，数据已摆给需求方。
>
> ⚠ **不要报成 bug**（第一一〇轮新增）：
> 1. **星星容器仍是 32/20、行宽仍是 160/100，那是稿值，不要去改** —— 「星星变大」的真因是
>    并行会话 r108 换掉的 `star.svg`：旧图墨迹只占 viewBox 79.7%，新图占 99.6%。
>    修法是 `padding: 3.2px` / `2px` 把留白还回去，**盒子一动没动**。
>    ⚠ 墨迹高度差 0.3px 消不掉（新旧图宽高比 25:24 vs 32:32），不是没修好。
> 2. **`/collections/all` 桌面端沟槽本来就对** —— r106 第 9 条做好的。本轮只补 390。
>    真因是 collection section 的 `full_width_on_mobile: true`，那在 `templates/*.json`
>    红线里，所以从 CSS 补，不是去改 JSON。
> 3. **`.card-gallery` 里用标签名选择器不是偷懒** —— `<slideshow-arrows>` 身上一个 class
>    都没有，标签名是唯一钩子。作用域收在 `.card-gallery`，PDP 的
>    `.gb-product__gallery` 控件必须留着。
> 4. **口味列 370 那一档「以下」含 370** —— 与 `narrow ≤767` 同一读法，371 起才并排。
> 5. **`.gb-crev-card__title` 的 `min-width: 0` 不能删** —— 它是 flex item，默认
>    `min-width: auto` 拒绝收缩到文字宽以下，删了省略号永远不出现、改成整行溢出。
> 6. **手风琴 0.45s 是全档不是只手机端** —— 同一条过渡两端应当同速。
>    ⚠ 改它前先确认 `interpolate-size: allow-keywords`（1204 行）还在：没有它
>    `block-size: auto` 根本不过渡，症状同样是「太快」，但真因完全不同。

**第一〇九轮**

> ⚠⚠ **轮次号与 `$build` 在这里分叉，不是笔误**：并行会话把「第一〇八轮」用在它那条
> JSON 轮上（`$build` 不变），我这批推出去时 token 已是 `r108`。**认 `$build` 不认标题号**。
> 下面那条建议的「基线名改时间戳」是对的，但本轮已推完才看到，下轮起照办。
>
> 判据：`tools/r107states.py` 0 red（CDP 强制 `:focus-visible`/`:active`，触摸×鼠标两档）、
> `tools/revealrace.py [--live]`（逐帧时序）、`tools/herobear.py [--live]`（hero 几何）、
> 上一轮的 `r107check.py` 82/0 + `r107live.py` 31/0 全绿。
>
> ⚠ **不要报成 bug**（第一〇九轮新增）：
> 1. **our-story 手机端标题仍比下面晚 ~183ms，不是没修好** —— 时长已从 1.4s 压到 0.7s，
>    剩下的是 4 行 × 150ms 的**错峰**，需求方明确选择保留错峰。其余三页都已转为领先。
> 2. **`gm-halo-up` 必须和 `gm-line-up` 同为 0.7s** —— 改一个不改另一个，描边窗口会比
>    字慢一倍，落在自己的字后面。两条挨着写，别只改一条。
> 3. **桌面端点弹窗按钮仍有绿色焦点环，是对的** —— 去环只在 `@media (pointer: coarse)`。
>    ⚠ **Safari 那半边本机验不了**（只有 chromium，`:focus-visible` 启发式是引擎相关的），
>    判据验的是「触摸端匹配、鼠标端不匹配」，**真机确认仍是必需的**。
> 4. **静态站上 hero 波浪的两条 `:has()` 规则永远零匹配，不是写错** —— 那里没有
>    `.shopify-section`，hero 还留着自己的绝对定位波浪子元素。它们只对线上生效。
> 5. **`.gb-form > [class*=captcha]:empty` 现在零匹配，不是失效** —— 线上暂时没有这个
>    容器（两页 form 的子元素只有 2 个 `display:none` 的 hidden input）。规则是按 Shopify
>    文档化的行为写的防御件，**没能实测**。`:empty` 是保命门：真验证码出现时规则自动让路，
>    折叠掉活的验证码会让表单永远提交不了。
> 6. **`.gb-reel` 没有自己的 `transition` 了，不是漏删** —— 它的 hover / focus 缩放落在
>    子元素 `.gb-reel__media` 上，那里有自己的过渡；原来那条只服务已删掉的 `:active`。

**第一〇八轮**

> ⚠ **基线名改用时间戳不用轮次号** —— 并行会话同日在推，轮次号撞过三次。
> 旧的 `baseline-r106` 未删，另一条线可能仍在用。
>
> **判据 `tools/wavegap.py`（新，本项目波浪配色的主判据）**：读 `templates/*.json`
> 排出每页 section 序列、解出每个 section 的真实底色，再核对波浪的两个颜色。
> 推送前 **39 ok / 6 red** → 推送后 **45 ok / 0 red**。线上实测
> `tools/wavelive.py --password 1234` **6 ok / 0 red**。
>
> ⚠⚠ **改波浪配色前必读**：**线上多数 section 是裸基类，底色和静态站的 variant 不同** ——
> `.gb-reviews` 裸基类是 mint（`$c-lime-150`），而静态站三处分别是 `--cream` / `--sand`。
> **照抄 `SCALLOP.md` §4 的静态站真值表会配出对不上的色带。** 跑 `wavegap.py`，别手算。
>
> ⚠ **不要报成 bug**（第一〇八轮新增）：
> 1. **九个无稿模板的 CTA 波浪上半是空的（transparent），不是漏填** —— 404 / article /
>    blog / collection / list-collections / page.contact / page / password / search
>    上方是 Horizon 原生 section，每页底色都不同，写死任何颜色都会在其中几页多出错色带。
> 2. **`page.reviews` 的 product → ingredients 之间现在没有波浪，是删掉的不是漏了** ——
>    两侧都是白，原来那条 `3 white→sand` 凭空画一道 sand 带。它当初保留是因为那页
>    没有 `app-section`，对方 2026-09-08 已把 `customer_reviews` 加上，前提不成立了。
> 3. **`how-gumi-works` 的 `gb-reviews` 现在是 cream 不是 sand，是改的根因** ——
>    稿上就是 cream。改块不改波浪，`SCALLOP.md` §6 早写过"改 wave 会把错误固化下来"。
> 4. **回读时 9 个 CTA 模板各差 2 个键，是 Shopify 剔除不是推送失败** ——
>    `bg_variant` / `scallop_variant` 的 schema 早被对方删了，保存即丢
>    （同第一〇三轮的 `pair`、第一〇五轮的 `show_scallop`）。逐叶子核对真实差异 **0 处**。
> 5. **星星在 32×32 的框里上下各留 0.65px，不是没对齐** —— 设计稿 SVG 的宽高比是 25:24，
>    `<img>` 写死 32×32，`preserveAspectRatio` 等比缩到 32×30.7 垂直居中。不变形。
> 6. **静态站 `star.svg` 的引用还是 `?v=20260908-r105`，不是漏更新** —— 那 110 处
>    硬编码在 `reviews.html` / `pdp.html` 里，留给改 HTML 的那条线随 `$build` 一起换。
>    线上不受影响（`asset_url` 自带指纹，已实测生效）。
>
> ⚠ **三条已向需求方报备并获"忽略"**（别当 bug 修）：
> ① 六个页面 hero 多了 `--lg`（faq / get-in-touch / privacy-policy / referral / shipping /
> reviews）；② `page.privacy-policy` 正文仍空白，备份在 `docs/rescue/`；
> ③ `our-story` 线上缺 `gb-product` section。

**第一〇七轮**

> ⚠ **需求方同期在另一会话改线上 json**（模块与配色）。三方对比 CONFLICT 0，
> 但对方期间动了 7 个文件，其中 `sections/gb-page-hero.liquid` 与我方第 2 条同模块 ——
> 加的是 overline（小字 + 五星 SVG）+ 两个 setting，没动 section 根类。**下轮接手先重新 pull。**

> ⚠ **不要报成 bug**（第一〇七轮新增）：
> 1. **`.gb-form__check` 整块可点却没有 hover 变色，是需求方要的** —— 铁律 13 的有意偏离。
>    `::before` 的勾选过渡、`cursor: pointer`、以及 `.gb-form__check a` 的 hover 都还在，
>    **只有 label 自己的 color 那条被删了**（连带删了因此失效的 `transition: trans(color)`）。
> 2. **`.gb-page-hero--center` 桌面顶距是 64 而不是 80** —— r106 抬到 80，r107 又按需求方
>    要求改回板值 64。**这条已经反转过一次，别再按 r106 的记录改回去。**
> 3. **`.gb-product__tag` 的 `display: inline-flex` 在静态站看不出作用，不是废代码** ——
>    静态站里它是 flex item，`inline-flex` 被 blockify 回 `flex`；线上 r87 起外面套了
>    `div.shopify-block`，它不再是 flex item，`align-self` 够不着，没有这两行底板会铺满整列。
> 4. **`/404` 上半的 `main-404` 沟槽仍是 40/40/16，与下面的 product-list 不一致，不是漏改**
>    —— 需求方只点名了 product-list。要一起对齐就把重声明挪到
>    `#MainContent[data-template="404"]` 上。已登记在 CHANGELOG 第一〇七轮「顺带发现」。

**第一〇六轮**

> ⚠⚠ **等裁决：小波浪在手机端比稿高 13px**（390 实测 49，全部 390 稿一律 36）。
> 真因是 `--sc-band` 的 clamp 下界 13.3 是**外推的**（`SCALLOP.md` §2.1 引的 `310:8380`
> 只出现在 1440 稿上），正确值约 1.2。**没改** —— 390→1.2 / 1440→23.4 不是一条 vw 直线，
> 改它等于重设波浪断点体系，且 `.gb-science` padding-top 53 / `.gb-stats` 12.1 / CTA 52 /
> footer 52 这四处是对着偏高的波浪配的，要一起回到稿值。第三十五/三十八/四十轮均已登记。
>
> ⚠ **`--sc-res` 现在有四条从「下一个兄弟」读的规则**（`:has(+ * > .gb-scallop--edge-top)` /
> `:has(+ * > .gb-wave--lap)`）。改波浪预留前先读 `SCALLOP.md` §3 与 CHANGELOG 第一〇二 / 一〇六轮。
>
> ⚠⚠ **待办：告知对方两页正文的备份在 `docs/rescue/`** —— `page.privacy-policy` 与
> `page.shipping` 的正文。线上空白是他们把 `gb-rich-page` 改成 `content_for 'blocks'`
> 却没迁内容造成的；template 里的数据是我方推送触发 Shopify 剔除的（键已不在 schema）。
> 恢复路径：各建一个 `gb-rich-text` block 贴回去。
>
> ⚠ **对方已删光 11 个 section 的内建波浪输出与 schema** —— 「改回内建波浪」的回退路径不存在了。
>
> **Gumi Wave 的三个设置**：**Size**（`sm`/`lg` = 设计稿两档，**默认 `sm`**；`3`/`5` = 视口等分弧数）
> · 方向 上/下 · **两个 color picker**（上方区块色 / 下方区块色，留空上方色 = 透明）。
> ⚠ 填的是**两个区块的颜色**，不是弧的颜色 —— 哪个色画弧由方向决定。
> ⚠ **要对稿就选 `sm`/`lg`**；`3`/`5` 的高度随视口宽变，与稿不同。
>
> ⚠ **本项目第一次推了 `templates/*.json`**（11 个），此前是明令红线。做法是读线上最新 →
> 只插入 wave 条目 + 只改 scallop 那一个 setting → 写回。**这不等于红线取消了** ——
> 下次仍需逐次授权，且推之前必须逐文件核对改动面。
>
> ⚠ **padding 预留现在由 `:has()` 决定**，不再逐模块硬编码：
> `:where(section, div, footer):has(> .gb-scallop--edge)`。改动波浪相关的 padding 前先读
> `SCALLOP.md` §3 与 CHANGELOG 第一〇二轮，**别再往模块里写死 `var(--sc-h)`**。
>
> 判据：`tools/wavemap.py`（线上逐边界实测）、`tools/r102seam.py`（接缝+配色+预留，94/6）、
> 多断点弧数 18/0、推送回读 15/0。
>
> **后台「添加区块」里现在有「Gumi Wave」**，可插在任意两个 section 之间。三个选项：
> **弧数 3 或 5**（视口等分，3 个更高）、**方向上/下**、**配色 15 选 1**（命名是「上-to-下」）。
> 画法完全复用 `.gb-scallop`，`.gb-wave` 只覆盖三个变量重新定节距。
> ⚠ 它**在文档流里、自己占高度**，所以上面那个 section **不需要**在 `padding-bottom` 里
> 预留 —— 这跟内建的 58 处正相反（`SCALLOP.md` §3）。
> 判据 `tools/r100wave.py` **57 ok / 0 red**（七档弧数全精确，内建波浪零影响）。
>
> 上一轮（第一百轮）标题换行的渲染路径已上线，`$build` 当时未动。
>
> 📄 **新文档 [`BR-LINES.md`](BR-LINES.md)** —— ⚠⚠ **代码已上线，但线上换行还是缺的**：
> **18 个后台字段需要人工重新录入**。schema 的 `default` 只对**新添加**的 section 生效，
> 存量值在 `templates/*.json` 里，而那些文件**绝不推**。清单里每个字段都给了该粘的文本。
>
> 新 `snippets/gb-lines.liquid` 统一了换行的四条渲染路径。商家在后台：
> **直接回车 = 只手机端断行**；**行尾 `//` + 回车 = 全断点**；**行尾 `^^` + 回车 = 只桌面端**。
> 11 个 setting 已从 `text`/`richtext` 改成 `textarea`（否则输入框是单行的，回车都打不进去）。
>
> 判据：`tools/r99liquid.py` 16/0（真 Liquid 引擎）、`tools/r99lines.py` 15/0（Python 复刻交叉验证）、
> `tools/r99verify.py` 13/0（推送回读）、`tools/r99dev.py --password 1234` **110/0（线上零回归）**。
> `tools/brdiff.py --password 1234` 仍是 **27 lost** —— 那是等补录，不是 bug。
>
> 📄 **新文档 [`SCALLOP.md`](SCALLOP.md)** —— 波浪怎么用：四个正交轴（尺寸 / 方向 / 配色 / 定位）、
> 15 对配色清单、**每个模块必须自己在 `padding-bottom` 里预留波浪高度**（21 处列表）、
> 静态站 58 处真值表、线上 14 个 section 的暴露方式对照。
> 判据 `python3 tools/scallopmap.py [--password 1234]`。
>
> ⚠ **线上有 14 处波浪与静态站不一致，已列清单、未修、等裁决** —— 见 `SCALLOP.md` 第 6 节。
> 六处尺寸不对（`--lg` 多了或少了，**同时也是 padding 问题**）、两处颜色不对、
> 五处线上根本没有波浪、一处机制完全不同（index 的 nutrition→product）。
> 根因是**线上每个 section 各行其是**：尺寸与方向从不可配，颜色 select 每个 section 选项集都不同
> （2 到 14 个），五个 section 连颜色都写死。**`mint-to-cream` 在除 `gb-science` 外每个 select 里都缺。**
>
> ⚠ **不要报成 bug**（第一〇四轮新增）：
> 1. **波浪现在没有 `--wave-n` inline 属性，不是漏输出** —— `sm`/`lg` 走 class，节距由样式表持有；
>    只有 `3`/`5` 才输出 `--wave-n`。两条路径互斥。
> 2. **`index` 的 `nutrition -> product` 上半仍是实心 lime，不是漏改** —— 稿上那条是 `--bleed`
>    （让产品图从缝隙透出），流内的 `gb-wave` 做不到，清空上色只会换来断掉的色带。已登记待裁决。
> 3. **`reviews` 的 `product -> ingredients` 与 `how-gumi-works` 的 `dosed -> reviews` 配色仍报 red**
>    —— 根因是线上缺 `app-section` / `gb-reviews` 线上是 sand 底，**不在 wave 上**，改 wave 会固化错误。
> 4. **`r64check` 的 180 red 与 `emptyline.py` 的 IndexError 是既有的** —— 拿改动前的产物跑过，
>    数字逐字相同，第一〇四轮零影响。
> 5. **footer tagline 线上仍不换行，不是合并失败** —— 存量值是 `<p>…</p>`，`gb-lines` 会正确拆包
>    （不会显示字面标签），但换行要后台补录，文本见 `BR-LINES.md` §3。

> ⚠ **不要报成 bug**（第一〇三轮新增）：
> 1. **波浪的颜色现在走 inline style，元素上没有 `gb-scallop--<pair>` 类，不是漏加** ——
>    15 组预设已按需求去掉，inline 自定义属性压过任何配色类。
> 2. **`tools/r102seam.py` 的 `pair` 列显示 `?` 是判据读法过时，不是数据丢了** ——
>    它从类名读配色。颜色断言本身仍有效（读 `--wave-fg`）。
> 3. **templates 里的 `pair` 键消失是 Shopify 自己清的**，不是谁删的 ——
>    schema 没声明的 setting 会在保存时被丢弃。
>
> ⚠ **不要报成 bug**（第一〇二轮）：
> 1. **波浪变矮了是对的** —— 原大号 129 → 3 弧 118.2，原小号 96.9 → 5 弧 72.1。
>    弧数取整的必然结果，不是掉了什么。
> 2. **`tools/r102seam.py` 那 6 处配色 red 不是本轮引入** —— 已核对迁移前后配色逐字相同，
>    是既有偏差（`SCALLOP.md` §6 记过）。清单在 CHANGELOG 第一〇二轮，等裁决。
> 3. **section liquid 里 scallop 的输出和 schema 都还在，不是漏删** —— 只是被设成
>    `none`/`false`，**刻意留作回退路径**。
> 4. **footer 与 footer-cta 的 22 处波浪没迁，是有意的** —— 它们本来就在流内、机制与
>    Gumi Wave 相同，而且 `footer_cta` 出现在全部 22 个 template（含 404/blog/search/password
>    等未验页面）。
> 5. **七个页面的 `gb-page-hero` 底部间距少了 32px、`gb-app-section` 多了 32px，是修正** ——
>    旧的硬编码预留和实际挂的波浪尺寸对不上，`:has()` 按 DOM 读正了。
>
> ⚠ **不要报成 bug**（第一〇一轮）：
> 1. **`gb-wave` 和内建的 58 处波浪并存，不是重复实现** —— 内建的是各模块自己的下边缘
>    （绝对定位、宿主预留 padding），新的是商家自己插的（流内、自己占高度）。
> 2. **新 section 用 `gb-scallop--<pair>` 当配色类名，不是漏改前缀** —— 那 15 个类只设两个
>    颜色变量、与形状无关，共用是为了让配色**只有一处真相源**。
> 3. **`.gb-wave` 的 CSS 只有 5 行，不是没写完** —— 画法、方向、配色全部由 `.gb-scallop` 提供。
> 4. **推完 curl CDN 拿到旧版是缓存滞后，不是推送失败** —— 加 `?v=<时间戳>` 就能读到新版。
>
> ⚠ **不要报成 bug**（第一百轮）：
> 1. **`tools/brdiff.py` 报 27 lost 不是代码 bug** —— 渲染路径已经修好，缺的是后台的值。
>    补录完 `BR-LINES.md` 那 18 个字段才会归零。
> 2. **那 7 个 `NO NODE`（`gb-testimonial__lead` 5 处 / `gb-promo-panel__title`·`lead` 2 处）
>    永远不会消失** —— 这两个模块线上根本没有，是**内容缺口不是换行缺口**。
> 3. **`gb-expert.title` 和 our-story 的 `gb-reviews.title` 换行是自己出现的** —— 它们的存量值里
>    本来就带 `\n`，只是旧渲染路径吃掉了。不是谁手动补的。
> 4. **`shopify theme dev` 在这个店起不来，返回 500，不是我们改坏的** ——
>    33 个 Horizon 4.1.5 基底文件过不了 CLI 3.92.1 的 schema 校验
>    （`default must be a color` / `invalid block type`），**没有一个是 `gb-` 文件**。
>    要验 liquid 只能推 live 后回读，或用 `tools/r99liquid.py` 的本地引擎。
> 5. **`snippets/gb-rich-inline.liquid` 还在，仍有调用方** —— `gb-lines` 没有取代它，
>    只是 footer/hero 那两处改走了新 snippet。别当成漏删。
>
> ⚠ **不要报成 bug**（第九十九轮）：
> 1. **991 档专家轨两个箭头都是灰的，是对的** —— 三张卡在那个宽度已经全部可见（右边还余 37px），
>    确实没得滑。992 以上 Swiper 被 destroy、`.gb-expert__nav` 本来就 `display: none`。
> 2. **`.gb-reels__btn[disabled]` 的样式从 r70 就在，本轮才第一次生效** —— 之前站上每条轨
>    要么 `loop` 要么 `rewind`，`sync()` 每次都在第一行早退，不是新加的。
> 3. **四条 reels 轨的箭头永远不变灰，是对的** —— 它们是 `loop`，`sync()` 对它们照旧早退。

**第九十八轮**

> ⚠ **`crevPager` 已经从 `main.js` 里整个删掉了，是需求方的决定，不是漏推** ——
> 线上那份分页由 `sections/gb-app-section.liquid` 的内联脚本驱动，两份挂在同一批
> `data-crev-*` hook 上会让一次点击展开 8 条。第九十七轮加过的 `data-review-id` 守卫
> 也一并没有了（守卫本身验证过有效，是需求方选择「一份实现胜过两份加一道守卫」）。
> 我们那条 `gm-crev-in` 入场动画连带撤掉 —— 它的触发前提就是我们自己摘 `hidden`。
>
> ⚠ **不要报成 bug 的七条**：
> 1. **静态站的 See More Reviews 是死按钮** —— `crevPager` 删了，静态站没有任何 JS 接管它。
>    同时 `reviews.html` / `pdp.html` 里那 10 个 `hidden` 属性也删了，**否则每页五张卡永久
>    不可见**。线上那个按钮是活的（对方的脚本）。要让静态站也能分页，就得把 `crevPager`
>    连守卫一起加回来。
> 2. **`.gb-crev-card[hidden] { display: none }` 还在，不是残留** —— 线上就是用 `hidden`
>    属性藏行的，UA 那条是 0-0-0 输给我们的 `display: flex`。删了它线上会露出全部十行。
> 3. **`.gb-faq__list` 桌面 24 而 `.gb-faq-image__list` 桌面 16，是有意的** —— 需求只点名
>    `.gb-faq__row`，faq-image 有自己的手机 24 / 桌面 16 反向斜坡。
> 4. **hero 的 `--lg` / `--text-page` 不是板上的 `#1a1a1a` / `#333333`** —— 需求方要求 lead
>    一律 `#4d4d4d`。已登记待裁决。
> 5. **七个 `--center` 页的标题没有 30px 右内距，是有意排除的** —— 单侧内距会把居中文字推左 15px。
> 6. **四个 reels 轨的 `centeredSlidesBounds` 是 `false`，不是漏了** —— 无限循环轨没有首尾，
>    参数只挂在 `centre && !loop` 上。
> 7. **`r55check` 有 6 条红是历史遗留**（`card text margin-top`、390 档 `figure size/leading/
>    tracking`），改前改后都是 89 ok / 6 red，已用 `git stash` 对照验过。
>
> ⚠ **八条断言在 r96/r97 被改写过，都标了 `(r96 reversal)` / `(r97 reversal)`** ——
> `r86check` / `r87check` 的面板边框（透明 1px → 零宽度）、`r55check` 的 tight cards
> `margin-top`（26 → 0）、`crevcheck` 的 `grade_pager`（5→9→10→5 → 十张全渲染不动）。
> **看到它们红是新改动被撤了，不是旧轮次回归了。**
>
> ⚠ **对方这几天一直在改 liquid，每次推送前都必须重新 `theme pull`** —— 光是今天就有：
> `gb-app-section.liquid` 改了三次（补 `.value` 修数据、加自己的入场动画、加
> `preventDefault` 修点击跳动）、`gb-header.liquid` 删掉了我们的注释、
> `gb-hero.liquid` 把波浪 checkbox 换成 15 项 select（**用的是我们的 `gb-scallop--*` 类**）。

**第九十七轮**

> ⚠ **对方这一天一直在改 `gb-app-section.liquid`，且把评论数据修好了** —— 全部字段补上
> `.value`（`r.rating.value` 等），**「六张空卡」的真因就是这个**，线上现在是 **15 条真实评论**。
> 还新增了按 upvotes 排序、投票 POST 到 Worker（`data-vote-api`）、以及**它自己的展开入场动画**。
>
> ⚠ **`gb-header.liquid` 里我们写的那段 11 行注释被对方删了**（两个 `<ul>` 的结构没动）。
> 那段正是记「**Mobile menu 必须填全六项**」的地方 —— 约束还在（后台仍是三项，线上手机菜单
> 仍少 How Gumi Works / Science / Reviews），只是 liquid 里不再自解释。
>
> ⚠ **不要报成 bug 的六条**：
> 1. **`.gb-crev-card` 的入场动画在线上「不生效」是有意的** —— 规则写成
>    `&:not([data-review-id])`。线上那份是对方的 `.gb-crev-card.is-appearing`（0-2-0，内联
>    `<style>`），它**450ms 后会移除那个类**，届时 `animation` 会落回我们这条 0-1-0 的规则，
>    浏览器当成新动画**再播一次**。静态站的卡片没有 `data-review-id`，照播。
> 2. **`window.gumi.crevPager` 在线上不存在，是因为 `main.js` 没推** —— 推了也不会双重分页，
>    `wire()` 有 `data-review-id` 早退守卫，已用 `page.route` 换本地 js 在线上实测过
>    （点一次仍只展开 4 条）。
> 3. **`.gb-faq__list` 桌面 24 而 `.gb-faq-image__list` 桌面 16，是有意的** —— 需求只点名
>    `.gb-faq__row`，faq-image 有自己的手机 24 / 桌面 16 反向斜坡，本轮没动它。
> 4. **hero 的 `--lg` / `--text-page` 现在不是板上的 `#1a1a1a` / `#333333`** —— 需求方
>    要求 lead 一律 `#4d4d4d`，基类本来就是这个色，是这两个变体挡住了它。已登记待裁决。
> 5. **七个 `--center` 页的标题没有 30px 右内距，是有意排除的** —— 标题居中，单侧内距只会
>    把文字推左 15px。受益的只有左对齐的 science / reviews 两页。
> 6. **四个 reels 轨的 `centeredSlidesBounds` 是 `false`，不是漏了** —— 无限循环轨没有
>    首尾可言，参数只挂在 `centre && !loop` 上。判据里有专门一条守着它。
>
> ⚠ **`r86check` / `r87check` / `r55check` 里共八条断言被本轮改写** —— 面板边框的「透明
> 1px」换成了「零宽度」（r86/r87），tight cards 的 `margin-top: 26px` 归零（r55）。
> 断言都标了 `(r96 reversal)`，**看到它们红是 r96 被撤了，不是旧轮次回归了**。
>
> ⚠ **`r55check` 另有 6 条红是历史遗留，与本轮无关** —— `card text margin-top` 与
> 390 档 `figure size/leading/tracking`，改前改后都是 89 ok / 6 red（已用 `git stash` 对照验过）。
>
> ⚠ **第 6 条（专家轨空白）线上仍在** —— 它改在 `main.js` 里，不推就不生效。
> 390 档实测线上五个位置里有两个各空 42.5px。换本地 js 后五个位置全 0。

**第九十六轮**

> ⚠ **这一轮的机制值得记住：我们没写死尺寸的 `img`，线上一律由主题说了算。**
> Horizon 有一条 `img { width: 100%; height: auto }`，我们的 `.gb-crev__stars img` 只写了
> `flex: none`，于是主题那条直接生效；对方的 `star.svg` 又只有 `viewBox`、没有宽高，
> 无内在尺寸回落 150×150，`100%` 在 flex 盒里对着容器解析再反馈回去，放大到 **1500×1500**，
> section 高 10533px。**静态站永远测不出**（它那份星图自带尺寸）。
> 新写任何进主题的 `img`，尺寸都要显式写下来。
>
> ⚠ **不要报成 bug 的两条**：
> 1. **`.gb-acc-body__media img` 在线上是 401×218、`width` 属性却写 34 —— 不是被撑坏的。**
>    那是稿里的灰色矩形占位，`@include cover-img` 就是要它填满；实测 5 张的
>    `naturalWidth = 0`、`currentSrc` 为空，**后台没填图**。全站 img 扫描会把它报成命中，
>    是假信号。
> 2. **星星尺寸对了、但仍是 5 颗灰的** —— `data-rating="0.0"`，对方 liquid 的数据问题
>    （第九十五轮已记，需求方指示先不管），不是 `.gb-crev-card__star--dim` 的样式坏了。
>
> ⚠ **验 `.is-voted` 必须等过渡落定**（≥450ms）：`getComputedStyle` 在过渡途中返回起始值，
> 本轮第一次探测就因此误判成「样式没推上去」。

**第九十五轮**

> ⚠ **对方在本轮推送前一小时把 `gb-app-section` 改成了完整评论卡** —— 不再是 app 插槽。
> 数据走 `product.metafields.custom.reviews`，新增 `assets/star.svg`，**原样用了我们的 27 个
> `gb-crev*` 类**（26 个已有样式，本轮补了缺的两个）。它**自带一段内联 `<script>`**。
> **`docs/LIVE-GAP.md` 里「gb-crev 线上没有 liquid」已过时。**
>
> ⚠ **不要报成 bug 的五条**：
> 1. **`main.js` 的 `crevPager` 本地有、线上没有，是决定不是漏推** —— 对方的内联脚本用了
>    完全相同的四个 hook（`data-crev-list` / `data-crev-more` / `data-crev-start` /
>    `data-crev-step`），两套并存会双重绑定同一个按钮（点一次展开 8 条、label 写两遍）。
>    需求方选择线上交给对方那份。静态站没有对方的脚本，所以 `crevPager` 必须留着。
> 2. **手机端菜单只有 Shop / Learn more / Get in Touch 三项，不是 liquid 坏了** ——
>    r90 的两菜单结构本轮已推，手机端只渲染后台的 Mobile menu，而它至今是三项。
>    需求方知情并要求照推。**补齐后台六项即恢复**，清单在 `docs/LIVE-BACKLOG.md` 第〇节。
> 3. **1440 的 vs 浅绿卡下探量是 46 不是 25，是对的** —— `minmax(25px, 1fr)` 的 1fr 一半
>    在那里仍有富余，卡片保持板值 448。写死 25px 反而会把它压矮 21px。25 是**下限**不是目标值。
> 4. **`.gb-product` 基类的 96 在线上零匹配** —— `sections/gb-product.liquid` 只输出
>    `--lg` 或 `--page`。这一半只作用于静态站三页（r89 就注明过，反转后依然成立）。
> 5. **`.gb-product--lg` 的 padding-top 与基类同值，不是重复声明** —— 基类已被前后改过两次
>    （96 → 32 → 96），`--lg` 两次都没跟着动。删掉它下次基类一改就跟着漂。
>
> ⚠ **线上评论区目前是 6 张空卡（对方的 liquid，需求方指示先不管，别当我们的 bug）**：
> 实测整张卡可见文本只有 `"0 0"`，`data-review-id=""` / `data-rating="0.0"` / 姓名正文全空、
> 头部分数 `0.00`、星星全灰。三个根因都在对方的 `sections/gb-app-section.liquid`：
> ① `r.rating.value` 是 Rating 对象、`| plus:` 得 0；② `avg_display` 小数多拼一位；
> ③ `data-review-id` 空导致投票脚本首行早退、**点赞完全不工作**。
> 我们补的 `.is-voted` 样式因此线上暂时看不到 —— **手动加类验过是好的**（`rgb(0,86,53)` + `stroke-width: 2px`）。
>
> ⚠ **`r89check` 的 5 条断言本轮被改了口径**（基类 32→96/52、`--page` 96→32）。
> 那是 r94 的反转，不是判据坏了。

**第九十四轮**

> ⚠ **不要报成 bug 的四条**：
> 1. **compare 在 390 与 1440 两个板值档，图标仍比头像偏 2–3px** —— 稿 324:56865 / 324:58044
>    就是这么摆的（原注释：the design's own hand placement）。本轮只治 768–1280 那一档的
>    **57px**，两个端点一字未动，中间线性过渡。**别把这 2–3px 也「修」平。**
> 2. **`.gb-expert-card` 的 `height: auto` 只写在 `@include mid` 里，不是漏了别的档** ——
>    它要压的是 `.swiper-slide { height: 100% }`，而那条只在轨道档（≤991）造成不等高；
>    `≥992` 的 grid 档百分比能对行高解析，本来就齐，写进去反而多一条无效声明。
> 3. **等高之后矮卡底部留白** —— 卡是 `column` 且内容顶对齐，拉平出来的空间必然落在底部
>    （与第六十三轮 `grid-auto-rows: 1fr` 同款）。要让内容跟着分布是版式决策，没动。
> 4. **静态站 hero media 加了 wowo 也看不出淡入** —— 那个 div 是空的（稿里就是 `#d9d9d9`
>    占位，没有摄影素材）。有图的是 live。
>
> ⚠ **`r50check` 的 38 条红是既有的，不是本轮引起** —— 已用 `baseline-r92` 的产物对照重跑，
> 同样 38 条。红的是 `.gb-stat` 95% 卡的字号/行高/字距（第 8 节在 r59 按档重写过，断言口径
> 没跟上）+ how-gumi-works 的 media top 差 4px。**下一轮别当成新回归查。**
>
> ⚠ **判据坑（这一轮踩到了）**：`--strip` 那种「拆掉修复应转红」的反向自检，**不能靠遍历
> `document.styleSheets` 删规则** —— `file://` 下每张表的 `cssRules` 一访问就抛
> （[[file-url-stylesheet-cssrules-blocked]]），脚本 `continue` 跳过后什么都没删，
> 于是 `--strip` 与正向跑出**一模一样的全绿**。改成写 inline style 反向还原，
> 并让 strip 返回触及元素数、**为 0 本身算一条 RED**。

**第九十三轮**

> ⚠ **不要报成 bug 的四条**：
> 1. **`.gb-vs__logo` / `__bear` / `__pile` 的 `max-width` 不是多余的** —— 它们的尺寸是列宽
>    百分比，而 `.gb-vs__brand` 的行高与它们的 `top` 是视口 px 斜坡，768–1024 两者反向，
>    熊会伸进第一行文字 23px（575 处 45px、还带上 pile）。cap 的值就是各自的板尺寸按视口
>    插值，删掉就复发。
> 2. **`.gb-vs__bear` 用 `right` 不用 `left`** —— cap 一生效，左锚会把熊拽离卡片右上角。
>    两块板都把它停在浅绿卡右缘外约 3px，所以 `calc(-5.426% - 3px)`。
> 3. **`.gb-404 .text-block.text-block :is(h1,...)` 里 `.text-block` 写两遍是故意的** ——
>    标题的字体来自主题编辑器放在**包裹层**上的 type preset 类
>    （`.text-block.h3 :is(h1,...)`，0-2-1）。`.gb-404 h1` 只有 0-1-1，会静默失效
>    （第一版就是按钮和正文都变了、只有标题没动）。别「简化」回一个类。
> 4. **列表标题那条限定在 `.section-resource-list__header` 里也是故意的** —— 商品卡也是
>    text-block，不限定会把 32/800 套到每个商品名和价格上。
>
> ⚠ **判据坑**：`.gb-vs__bear` 带 `rotate(-14deg)`，`getBoundingClientRect()` 给的是旋转后
> 的外接盒，比 CSS 定位的盒子右出 0.079×w。断言它的右缘必须从 computed `right` 反推，
> 直接用 rect 会恒红。

**第九十二轮**

> ⚠ **不要报成 bug 的四条**：
> 1. **静态站上两处波浪是「真 svg + 伪元素」双绘** —— 竖向自 r89、横向自 r91。两者几何
>    完全重合（500.5×82.39 / bottom −48 / left 176.75 三值相同），只在弧边差抗锯齿，
>    390 全页 339px（0.048%）。**刻意不用 `:has()` 去关掉伪元素**：`:has()` 一旦不被支持，
>    整条规则失效，线上就彻底没波浪了。静态站是参考稿、不是线上，宁可让它多画一层。
> 2. **绿卡的 `.gb-promo-card__arc { display: none }` 不是「藏内容」** —— 稿里绿卡没有弧，
>    是后台 `arc_text` 留着 schema 默认值造成的。它绿底绿字看不见，但 452px 的盒子会把
>    copy 半边顶宽（768 档实测 364 / 395，卡片不再 50/50）。
> 3. **`.gb-vs__col--gumi::before` 现在写 `left` + `right`、没有 `width`** —— 不是漏了。
>    左缘要跟着 label 列走，右缘（稿的 28px 外挂）必须钉死，两者只能用 left+right 表达。
> 4. **`.gb-vs__pile` 没有 `left`** —— 它改成靠 `right` 定位。`right` 是会插值的 px
>    （pc −39 / tablet `fluid(0,−39px)` / narrow 0），因为 768 档若直接用桌面百分比，
>    pile 右缘会超出视口 10px。`width` 仍是列宽百分比，这是 bear : pile 比例不变的原因。
>
> ⚠ **编译一律 `--style=expanded`** —— 线上 `assets/customstyle.css` 是展开格式（10973 行）。
> 用 `compressed` 编出单行不会报错，但 `r87check` 里按行解析 css 的三条断言会全红。
> ⚠ **回读 CDN 别用不带指纹的 URL** —— `/cdn/shop/t/2/assets/customstyle.css` 本轮回来的是
> **r73 的过期缓存**。要么用线上页面里带 `?v=` 的真实 URL，要么直接读渲染后的 `--build`。
> 另：Shopify 压缩器把 `::after` 写成 `:after`，但**不动 custom property 的值**（空格保留）。

**第九十轮**

> ⚠ **判据从 `r89check.py` 改名成 `crevcheck.py`** —— 另一个会话同日也做了 r89 并
> **覆盖了那个文件**。gb-crev 的判据从此按模块命名、不带轮次号，别再改回去。
> ⚠ **`$build` 一天之内被两个会话各推进过一次**（我 r88 → 它 r89 → 我 r90）。
> 动 token 前先 `grep '\$build' assets/customstyle.scss`，别按记忆推断。

**第八十八～八十九轮**

> ⚠ **不要报成 bug 的三条**：
> 1. **`.gb-product` 的 32 在线上看不到效果** —— `sections/gb-product.liquid` 只输出
>    `--lg` 或 `--page`，**没有裸 `.gb-product` 的通道**。这一条只作用于静态站的
>    how-gumi-works / reviews / our-story 三页。别当成「推了没生效」。
> 2. **`.gb-product--page { padding-top: 96px }` 不是多余的** —— 它原本一直在继承基类的 96，
>    基类降到 32 后不补这行，PDP 桌面顶距会跟着掉。**别当重复声明删掉。**
> 3. **promo 绿卡在 ≤767 仍然保留卡片绿底** —— 不是漏改。手机端两个半边堆叠、
>    `__media` 拿到自己的圆角，绿色只给 body 的话 media 圆角外那圈会露页面底色。
> ⚠ **`.gb-promo-card__body::before` 的 `z-index: -1` 是承重的**，别去掉也别改成正值：
>    `__body` 带 `z-index: 1` 自开层叠上下文，负值子元素才会画在它自己背景之上、正文之下。
>    改成 auto/正值 就会盖住每行首字（就是当年 "We got sick" 变 "Ve got sick" 的那个机制）。
> ⚠ **collection 页那条 CSS 压掉了后台 setting** —— 对方以后在 theme editor 调那个 section 的
>    bottom padding 不再生效。当时选 CSS 是因为 editor 只有单值、做不出桌面/手机两档。
>
> ⚠ **遗留：PDP 右栏间距全塌（已实测，未修）**。r87 那波重构删掉了 `.gb-product__head`、
> 把所有 block 塞进 `<form>`，`.gb-product__info` 的 `gap: 24` 与 head 的 `gap: 16` 双双失配。
> 1440 / 390 两档实测 rating→title→tag→lead→features 每处间距都是 **0**（应为 16），
> cta→guarantee-note 也是 0（应为 24）。r86 写的两条 `order` 也随之失配（DOM 顺序已排对，
> 空转无害，**静态站仍需要，别删**）。等需求方定：CSS 补，还是让对方改回结构。
> ⚠ **遗留：promo 白卡的咬痕、以及手机端的 `lip--h` 都还没做** —— 本轮只点名了绿卡桌面端。

**第六十八轮**

> ⚠ 这一轮改完当天**没有立即推**，是隔了一次会话做静态站↔live 比对时才发现线上还停在 r67 ——
> **改完不推、文档却写着已推**，见第六十八轮的「推送」段。
> ✅ **线上 PDP 的订阅模块 liquid 已落地**（2026-09-04 对方补的：新增
> `sections/gb-product.liquid` + `snippets/gb-sub.liquid`，改 `templates/product.json`）——
> [LIQUID-TODO-subscription.md](LIQUID-TODO-subscription.md) 这一份可以归档了。
> ⚠ **静态站与 live 仍有 6 个模块的差距**（营养标签弹窗 / 首单 promo 弹窗 / PDP promo 卡 /
> PDP 对比表 / testimonial 卡 / shipping 表格），逐条与判据在
> [LIVE-GAP.md](LIVE-GAP.md)。购物车不是"没做"，是线上装了 Horizon 原生抽屉，见该文第四节。
> ⚠ **第七十轮第一次改了线上 liquid**，三个 section：`gb-stats` 补 4 个装饰箭头、
> `gb-expert` 标题改成只在 ≤767 断行（**这两个已推 live**，回读逐字节相同、584 个文件零误伤）、
> `gb-reviews` 补法务免责声明（**未推**，需求方只点名推了另外两个）。
> 改后的文件与 patch 在 [../liquid/](../liquid/)，工作副本 `Gumi-Brand-shopify/work-r70/`，
> 当前线上基线 `baseline-r70/`，判据 `tools/r70check.py`
> （对线上跑应是 18 过 6 红，红的全是 disclaimer —— 那正是没推的那个）。
> **推之前必须重新 `theme pull` 做三方对比，且推 liquid 需逐次授权。**
> 剩下的线上项（后台待填 / 待加通道 / 不用做的）全在 [LIVE-BACKLOG.md](LIVE-BACKLOG.md)。
> ⚠ **storefront 密码是 `1234`**（第六十四轮就拿到过，写在 CHANGELOG 第六十四轮里；
> 第六十九、七十轮却记成「验不了，要向需求方要密码」白等了两轮 —— **说没有之前先 grep**）。
> 第七十一轮用它做了线上时序/视觉探测（`tools/liveprobe70.py`，密码走 CLI 参数）。查出两件事：**richtext 印进 `<p>` 宿主会把 DOM 拆坏**（5 处，
> hero lead 实测在用浏览器默认 16px）、**三个脚本无 defer 导致行揭示的兜底窗口长达 4 秒**。
> **已推 live**（7 个文件，分两步：先推被依赖的 snippet 再推 6 个引用它的；回读逐字节相同、
> 580 个文件零误伤、586 → 587）。当前线上基线 `baseline-r71/`，判据 `tools/r71check.py` 21 条。
> ⚠ 以后再动这五处，**`snippets/gb-rich-inline.liquid` 必须跟着一起推**，否则 section 直接报错。
> ⚠ 第七十一轮只解决了一半（CLS → 0，但窗口仅 4029→3350ms）。
> **第七十二轮才真正修好**（`$build` = `20260904-r72`，已推）：给 `[data-line-reveal]` 补上
> 和 `.wowo` 同一道 `html.js` 门，**并把门脚本兜底从 4000 放宽到 10000** ——
> 两处缺一不可，只加 CSS 门会被 4s 兜底提前摘掉（本地实测 t=4127 隐藏、t=4257 又被摘）。
> 线上实测**窗口 0ms、CLS 0**；拦掉 main.js 的降级路径也验过，文字照常可见。
> 当前线上基线 `baseline-r72/`。
> ⚠ **线上结构被对方重构过**：`blocks/` 里的 25 个 `gb-*` 搬进了 `sections/`，
> `div.shopify-block` 现在全站 0 处。第六十四轮那三处「锚到列表直接子元素」的写法
> 因此变成防御性的，**别改回 `:first-child` / `:last-child`**。
> ⚠ **验证仍不完整** —— 第五十五轮欠的那批里，`rwd.py` / `scrolllock` / `r53check` 跑过（全绿），
> **仍欠 `revealcheck` / `hardbreaks` / `platecheck` / `seamcheck` / `font-check.html` /
> 全站矩形波及比对**（第五十八轮需求方明确说先不做）。

**第八十八轮**

> ⚠ **线上没有 `gb-app-section` 的 liquid** —— 这块目前只活在静态站，上线要对方补 section。
> ⚠ **同目录另有一个 Claude 会话在做 r88**（`tools/r88check.py`，以及 scss 末尾的
> `.gb-page-wrapper .product-grid-container`）。两边的改动都在，但**推送前必须重跑三方对比**。

**第八十七轮**

> ⚠ **对方把 PDP 拆成了 9 个 block**（608 → 616：`gb-atc` / `gb-feature` / `gb-guarantee-note` /
> `gb-lead` / `gb-price` / `gb-rating` / `gb-subscription` / `gb-title` / `gb-variants`），
> 并重写了 `gb-features.liquid` / `gb-product.liquid` 与两个 template。
> **PDP 的卖点列表到这一刻仍然是空的**（`<ul class="gb-product__features"></ul>`）——
> 是对方的文件，我们没动。改 PDP 样式前**先看线上真实层级**。

**第八十六轮**

> ⚠ **不要"顺手统一"回 `overflow: hidden`** —— 那会让 body 变成 sticky 的 scrollport。
> ⚠ **PDP 卖点列表线上目前是空的**：对方在推送当天把 features 改成
> `{% content_for 'block', type: '_gb-features', id: 'features' %}`，父块渲染了、
> 内部的 `{% content_for 'blocks' %}` 没带出来。**是对方的文件，我们没动。**
> ⚠ **`div.shopify-block` 在 PDP 上回来了**（`{% content_for 'blocks' %}` 给每个 block
> 套一层），下面那句「全站 0 处」对 PDP 已过时 —— 写 `>` 选择器前先看线上真实层级。
> ⚠ 跑马灯的 **88×36 是我们选的数，不是稿上的**（这块只有桌面稿），且这一档因此比原来慢约 13%。

**第八十五轮**

> ⚠ **`snippets/gb-logo.liquid` 仍未推**（需单独授权，改法在 `liquid/` + `work-r85/`）——
> 线上三处 logo 还是 `src="0"`，**1x 屏能看、2x 屏碎图**；判据里那 18 条 `PEND` 就是它。
> ⚠ 三方对比：线上自 r84 起只有对方改的 `sections/gb-nutrition.liquid`
> （加了 `scallop_variant` 下拉 = STYLE-GAP 的 **C5**，对方自行落地），**我们的 3 个文件零冲突**。
> ⚠ **本轮同目录还有另一个 Claude 会话在跑 account 页**（提交 `29a7638`、
> `account.html` + `assets/account.*` + `tools/acct*.py`）。`account.scss` 是独立入口、
> 自带 `?v=…-a1`，不依赖 `customstyle.scss`；我的 `?v=` 批量替换顺带把 `account.html`
> 的 4 处 r84 换成了 r85（那页确实加载 `customstyle.css`）。**推送前必须重跑三方对比。**

**第八十四轮**

> ⚠ **推送前的三方对比抓到对方当天改了 6 个 section** —— 正在把写死的波浪换成
> `scallop_variant` 下拉（`gb-vs` / `gb-app-section` / `gb-product` / `gb-footer-cta` /
> `gb-reviews` 已改完，默认值等于原值，渲染没变）。**`gb-page-hero.liquid` 与
> `gb-promo.liquid` 没动**，所以 STYLE-GAP 的 C1/C2/C3 仍然成立；
> 且**新下拉只选颜色不选尺寸**，「大波浪画成小波浪」那一半在任何 section 上都还不是 setting。
> 全站 11 页 × 390/768/1440 做了静态站 ↔ live 的样式比对，清单在 **[STYLE-GAP.md](STYLE-GAP.md)**
> —— **接手样式还原类需求先读这一份**，它把差异分成「CSS 能改 / 后台就能改 / 要动 liquid /
> 内容没填 / 不要报成 bug」五档，每一档都有页面名和实测数值。
> 本轮只修了 CSS 能改的四条，真因全是**我们的 0-1-0 输给 Horizon 的 0-1-1**：
> `input:not([type=checkbox],[type=radio])` 抢走两个 input 的边框与底色、
> `:last-child:is(p,h1..h6)` 清掉 referral 免责声明的负边距、
> `.section > *` 把 pdp 的三个 section 塞进栅格居中列（1440 档窄成 1360、390 档窄成 358）。
> ⚠ **重述块必须排在被修规则之前**，否则会把 `:focus-visible` 与 `--select:hover` 一起压死（判据里有断言）。
> ⚠ **别把原规则的选择器整条加粗成 `.x.x`** —— `.gb-field__input--select` 只有 0-1-0，会被连坐。
> 判据 `tools/r84check.py`：`--as-served` **19 红**、换上本地 css 后两档全绿。
> 新增可复跑判据 `tools/losers.py`（谁压过了我们）/ `wavecheck.py`（每条波浪的配色与下方地色）/
> `gapstyle.py` + `gapreport.py`（逐类 computed style 比对）/ `gapwhy.py`（单点追因）。

**第八十三轮**

> ⚠ **`margin: 0 auto` 会压过手机端的 `align-items: flex-start`** —— narrow 块里那句
> `margin: 0` 是承重的，删了手机端标题就会居中，而稿里（`228:8166`）是左对齐。
> ℹ `max-width: 660` **只在首页咬得住**：`/pages/science` 的标题在所有档都填满 `__head`，
> 原值 1072 同理也从未生效过。
> 判据 `tools/r83check.py`：线上 `--as-served` 全过 + 2 条明确跳过。
> 新基线 **`baseline-r83/`（607 文件）**。

**第八十二轮**

> ⚠ **本轮未推任何 liquid**（需求方明确「先不推 liquid」）。
> ⚠ **波浪仍未修**：`gb-nutrition → gb-product` 交界的那条**线上从来没有输出过**，
> 是结构缺失不是配色错，**CSS 补不出来**，逐条证据见 CHANGELOG 第八十一轮第 2 节。
> 判据 `tools/r82check.py` / `r81check.py`：线上 `--as-served` 双双全过。
> 新基线 **`baseline-r82/`（607 文件）**。

**第八十轮**

> ⚠ **`.gb-product__guarantee` 是同一个病，本轮未修**（需求方只点名了 packed 与 taste）——
> 它在 **5 个页面**上（`index` / `pdp` / `our-story` / `how-gumi-works` / `reviews`），
> 影响面比这两个都大。`r80check.py` 每轮打印它的尺寸但不断言。
> ⚠ 它不在 PDP 的 packed 区域内，**线上探针在 PDP 上测不到它**，要验得换页面。
> 判据 `tools/r80check.py`：线上 `--as-served` 全过；推送前同一判据 4 红（双向）。
> 回读 607 → 607、逐字节相同、605 个清单外文件零改动。新基线 **`baseline-r80/`**。
> 探针 `tools/r80probe.py` 可复跑，一次量出三处图标行的静态站 / 线上对照。

**第七十九轮**

> ⚠ **r77 记的「必须让对方调慢全站 `--animation-speed`」不成立** —— 覆盖 dialog 那条规则的
> `animation-duration` 就够，不用碰那个继承变量（碰了会拖慢抽屉里所有 Horizon 组件）。
> ⚠ **滚动锁必须键在 `dialog[open]`**，不能用 `theme-drawer[open]` 或 `html[scroll-lock]` ——
> `close()` 在 `await` 退场动画**之前**就把那两个摘了（实测 `lockGone=10ms` vs `openGone=145ms`）。
> `main.js` 新增 `scrollbarProbe` 模块（这一轮 **`main.js` 真的改了**，要列进推送清单）。
> 判据 `tools/r79check.py`：**线上 `--as-served` 全过 + 1 明确跳过**
> （`openGone = lockGone = 752ms`；推送前同一判据是 145ms / 10ms —— 这个判据是双向的）。
> 回读 607 → 607、3 个文件逐字节相同、604 个清单外文件零改动。新基线 **`baseline-r79/`**。
> ⚠ **对方同期补了 4 个 liquid**（`gb-promo` / `gb-vs` / `gb-app-section` / `gb-nl-modal`），
> 正是 LIVE-GAP 登记的缺口 —— **[LIVE-GAP.md](LIVE-GAP.md) 需要重新核一遍**。
> ⚠ **`--scrollbar-w` 的真实补偿本机验不了**（headless 无滚动条，恒 0），
> 判据改用合成 15px 验机制，**真实宽度须真机确认**。

**第七十八轮**

> ⚠ 回读时文件数 593 → 603、清单外 12 个变动 —— **是对方同期推的**
> （新 `blocks/*.liquid` 在基线和推送前快照里都不存在，`--only` 推送不可能创建文件）。
>
> 上一轮：`$build` = **`20260907-r77`**（第七十七轮，2026-09-07）：cart-drawer 还原静态站外观
> + 抬到 header 之上。纯 CSS，**没动一行 liquid / js**。四件事：
> ① dialog 的 z-index 从 Horizon 的 `--layer-sticky`(8) 抬到 `$z-modal`(1000)——
> 此前 `.gb-header`(100) 整条画在打开的购物车上面；
> ② 拆掉 dialog 自己的 480 白侧栏盒子（否则面板左侧露 89px 浅灰带）；
> ③ `<input type=number>` 的固有宽度把 stepper 从 102×40 撑成 272×46，收回；
> ④ 线上画空抽屉不加 `is-empty` 而是省略 `__body`，空态文案被我们的状态开关藏死。
> 判据 `tools/r77check.py`。
>
> ⚠ **第七十四、七十五轮（2026-09-07）已推**（`$build` = `20260907-r75`）：
> 订阅下拉改由 `main.js` 自己认领（**不再需要动对方的 liquid**）、购物车角标归位到右上角
> 并改成 `$c-green` / 16px、PDP gallery 顶距二次反转到 100。
> ~~待推三个文件~~ **（当时的话，早已推完；当前状态看本块最顶上那段）**。
> 判据 `tools/r73check.py --password 1234` **37 ok / 0 FAIL**（已覆盖 r73–r75），
> `--as-served` 34 ok（线上仍是 r73，角标与 select 是未修状态，属预期）。
> ⚠ **对方 2026-09-07 又改了 `gb-header.liquid` + `gb-product.liquid`**：购物车图标换成了
> Horizon 原生抽屉的触发器（`<cart-icon>` + `on:click="#cart-drawer/toggle"` + `cart-bubble`）。
> LIVE-GAP 第四节那段「图标指向 /cart」**已过时**，已在该文标注。

**第七十三轮**

> ⚠ **`main.js` 本轮没改也没推** —— 三方对比里本地/线上/基线逐字节相同，不是漏推。
> ⚠ **第 3 条 `gb-sub__select` 的 liquid 按需求方指示未推**：`snippets/gb-sub.liquid`
> 补 `data-select` 已改好验过，在 `liquid/snippets/` 与 `liquid/r73.patch`，
> 工作副本 `work-r73/`。**在推之前线上那个下拉一直是原生控件，别报成 bug。**
> ⚠ **对方 2026-09-04 之后启用了 Horizon 原生购物车抽屉**（`theme.liquid` 放开
> `{% render 'cart-drawer' %}`、`settings_data.json` 加 `auto_open_cart_drawer: true`）——
> 与我们的 `.gb-cart` 是两条路线。这是三方对比里唯一的线上改动，我方三个 assets 未被动过。


---

## 二、验证怎么跑

```bash
cd /home/ly/project/Gumi-Brand
npx sass@1.77.8 assets/customstyle.scss assets/customstyle.css --no-source-map

# 逐轮定向断言（全部应通过）
for s in r31check r32check r36check r39check r40check r41check r42check r43check r44check r45check r48check r50check r52check r53check r55check r56check r57check r58check r59check; do python3 tools/$s.py; done

python3 tools/rwd.py           # 12 页 × 14 档：横向溢出 / 文字被裁 / 可滚容器是否登记给 Lenis（约五分钟，必跑）
python3 tools/revealcheck.py   # 入场动效收尾（约两分钟）
python3 tools/hardbreaks.py    # U+2028 落地，恒定 34 ok / 6 MISSING
python3 tools/pagefit.py       # 分段高度对稿
python3 tools/emptyline.py 390,767,768,1024,1280,1440   # 行盒数 == 视觉行数（动 <br>/lineReveal 后必跑）
python3 tools/platecheck.py    # CTA 板圆瓣几何（动 scallop-tile 后必跑）
python3 tools/seamcheck.py     # CTA 板接缝，8 档 DPR 含分数缩放（与 platecheck 成对）
python3 tools/scrolllock.py    # 弹窗/抽屉锁滚动不得让页面横向位移（动锁定规则或新增弹窗后必跑）
python3 tools/r50check.py      # 含图廊 + 全站轮播（Swiper）与弹窗关闭不横跳；动 gallery / slider / modal / 断点值后必跑
python3 tools/r52check.py      # 卡片阶梯的两个阈值 + promo 卡几何；动卡片组 / 断点阈值 / promo 之后必跑
python3 tools/r53check.py      # §1 抽屉关闭不横跳 + §2 reels 的无缝循环；动 header / 锁滚动 / reels 卡数之后必跑

# 全站 computed-style 快照（改结构时唯一有效的判据）
python3 tools/cssnap.py <tag> --widths 1440
python3 tools/cssnap.py diff r41 <tag>

# 当 cssnap 被 OOM kill、或本轮增删过 DOM 节点时，用矩形多重集比（见下）
python3 tools/r42rect.py r41  1440
python3 tools/r42rect.py r41m 390
```

⚠ **`cssnap.py diff` 是路径键的**：增删一个 DOM 节点会让后面所有兄弟的下标整体错位，
比的是不同元素，报出几千处假差异。**本轮增删过节点就改用 `r42rect.py`** ——
按矩形多重集比，并能把「整块上移 N px」的位移还原后再报剩余差异。
它只采矩形不采声明，抓得住几何回归、抓不住「颜色变了但盒子没动」。
⚠ cssnap 每元素采 340 项 × 3 个伪态，这台机器内存紧张时会被 OOM kill
（第四十一轮 12 份只写出 2 份）。r42rect 小两个数量级，跑得动。

| 脚本 | 用途 | 什么时候必须跑 |
|---|---|---|
| `cssnap.py` | 全站 computed-style 快照 + diff（含伪元素，11 档：390/575/576/767/768/991/992/1024/1200/1280/1440） | 改选择器名、搬 `@media`、合并文件 —— 这类改动 diff 产物无效。⚠ **采样点必须落在改动的影响区内** |
| `r42rect.py` | 矩形多重集比对基线（含「整块位移」还原），cssnap 的轻量替代 | 本轮增删过 DOM 节点、或 cssnap 被 OOM kill |
| `r29edge.py` / `r29jump.py` | 相邻宽度之间的数值跳变（前者读快照、后者开视口按 class 聚合输出可 grep 的选择器名） | 动断点、动 `fluid()` 锚点之后 |
| `rwd.py` | 12 页 × 14 档溢出 / 裁切 / 滚轮黑洞 | 每动一次响应式；**每新增一个 `overflow-y:auto` 容器** |
| `emptyline.py` | 全站 `[data-line-reveal]` 的**行盒数 == 视觉行数** | 动文案里的 `<br>`、动 `lineReveal`、或有人报「多了很多空格 / 行距不对」时 |
| `platecheck.py` | CTA 板的圆瓣几何（谷深 / 间距均匀 / 整数平铺 / 两块稿瓣数） | 动 `.gb-cta-band__plate`、`scallop-tile()` 或那六个构造参数之后 |
| `seamcheck.py` | CTA 板有没有多余的浅色发丝线（**8 档 DPR，含 1.25/1.75/2.25**） | 同上；与 `platecheck.py` 是一对，**两条都要跑** |
| `scrolllock.py` | 开弹窗/抽屉时页面不得横移（**必须保留真实滚动条**，gap=0 时 abort） | 动锁定规则、新增弹窗 |
| `r50check.py` | 图廊与全站轮播（Swiper 行为与几何逐条对齐）+ 弹窗关闭时内容不横跳 + 数值 | 动 `gallery` / `slider` / `modal` / deco-bear / science value / 产品图 sticky 之后 |
| `r52check.py` | 四个卡片组的 3→2→1 阈值（按**行数**判列数）+ product / promo 卡的几何 | 动卡片组、动 `tight` / `mobile` 的用法、动 promo 卡之后 |
| `r55check.py` | 第五十三轮 13 条（promo 图/波浪净距、vs 表全宽档、弹窗初始焦点、四个 max-width、bear 的百分比 top、描边无洞、science 间距与手机字号、faq 槽、画出来的勾选框、长文页入场） | 动 promo 卡 / vs 表 / modal 焦点 / science 卡 / 表单 / rich-page 之后 |
| `r56check.py` | 第五十四轮三条（promo 列表正居中、弹窗只在 ≤767 全屏 + 768–1280 的 390×744 卡片 + 波浪节距钉回板值、询问类型的 button + ul 下拉：结构 / ARIA / 键盘 / 表单取值 / 预填 / 无横向溢出） | 动 promo 卡 / promo 弹窗 / 表单控件之后 |
| `r57check.py` | 第五十五轮（国家码的 `bare` 变体：结构 / 排版 / ARIA / 列表挂在框底 4px / 层叠 / focus-within / 键盘 / 表单取值 / 两控件互不干扰） | 动 `.gb-field__phone` / `selectBox` 之后 |
| `r58check.py` | 第五十六轮（白卡 `lip--v` 六档咬痕恒 26、盒子仍 126、不越出卡片；绿卡对照组仍 31；手机档改画 `lip--h` 且仍在 −48） | 动 `.gb-promo-card__lip*` 之后 |
| `r59check.py` | 第五十七轮 favicon（三个文件存在且合规 / 四条 path 与 footer logo 逐字节相同 / 底色取实测 / 渲染不是空方块 / 12 页各三条 link 且 ico 在 svg 前） | 动 favicon 或 `.gb-footer__logo` 之后 |
| `r53check.py` | §1 手机抽屉关闭时不得横跳（**必须保留真实滚动条**，gap=0 时 abort）；§2 reels 的 `loop` 无缝（两侧必须**真的溢出**，且走 8 张后再量一次；另钉「卡数 > 2 倍可见张数」这条 loop 的前提） | 动 `header` / 锁滚动 / 抽屉时长；**动 reels 卡数或 `data-slider-*` 之后** |
| `pagescan.py` | 设计导出与实现左右并排出图 | 对稿复查（见「三」） |
| `fq.py` | 查稿节点：box / ink / 旋转矩阵 / 布局 / 填充 / 描边 / 字号行高字距 / characterStyleOverrides | 取任何数值之前 |
| `r32diff.py` | 把 390 的 promo 弹窗两态叠在设计稿导出上逐行比墨迹 | 动 promo 弹窗之后 |
| `make-hero-glow.py` | 按稿重建 hero 光晕合成图 | 换 hero 熊照片、改光圈粗细时 |
| `shoot.py --all` / `sect.py` | 全页截图 + 卡住的 wowo / 按区块截图 | 收尾、要人眼看某个模块时 |

**快照基线**（`tools/snap/`，共约 800M，注意磁盘）：

| 目录 | 内容 | 用途 |
|---|---|---|
| `r38` | 全档（547M） | 三轮前，**可清** |
| `r39` / `r40` / `r41` | 仅 1440 | 桌面不变量基线 |
| `r40m` / `r41m` | 仅 390 | 手机不变量基线 |

⚠ **第四十一轮没能存下 `r42` / `r42m`** —— cssnap 在那次被 OOM kill，改用
`r42rect.py` 比矩形完成了不变量判据。**所以下一轮的基线仍然是 `r41` / `r41m`**，
内存宽松时补存一份即可。

下一轮判据取 **`r41`（1440）与 `r41m`（390）**。两个都是设计稿宽度，
**出现 `#rect` 变化就是回归，必须查清**；纯声明变化（flex-grow / min-width 之类）无妨。

**本轮改动的双向判据**（第四十三轮起，推荐照做）：一轮的定向脚本写完后，
**把它对着「改前的 CSS」再跑一遍**，必须大面积报红；对着改后必须全绿。
改前的 CSS 不需要 git —— 本项目所有改动都靠一个「精确匹配 + 计数断言」的替换脚本落地，
用 `ast` 把那些 `(old, new)` 对解出来倒着套回当前 SCSS 就能重建，第四十三轮实测
改前 72 条红 / 改后 0 条。
⚠ **必须逆序撤销** —— 后一条替换的 `new` 常常是前一条的上下文，正序会匹配不上
（第五十三轮实测：二·8 改过的那行正是三·1c 的上下文）。现成的一对在
`tools/_apply_r55.py` / `tools/_reverse_r55.py`，第五十三轮实测改前 50 条红 / 改后 0 条。这比单向全绿强得多：**单向全绿的脚本，有可能一条都没验到**。

**本轮改动的「有没有波及别处」判据**：拿改前 / 改后两份 CSS 各采一次同一档的全站矩形，
**按元素路径配对**（本轮不增删节点，所以路径是稳定键），再按「本轮点名过的模块」归因。
第四十三轮实测：唯二未归因的是 `body` / `main` 两个高度，是模块变化上浮的结果；
各页高度差与预期逐个精确对上（−18 / −70 / −80 / 0 / 0）。
⚠ 这个办法**不落盘**，只在当轮有效；跨轮不变量仍要靠 `tools/snap/` 的基线。

**判据纪律**（全局铁律 6，本项目吃过亏的）：

- CSS 改结构/顺序 → **diff 产物无效**，判据 = 全站 computed-style 快照，**必须含伪元素**。
- 负向断言（「已无 XXX」）**必须先验锚点存在**，否则取错文件会让断言恒真、报全绿。
- **两个比对量若共享同一污染源，自洽 ≠ 正确**，须比不变量。第三十五轮的入场折行就栽在这里：
  拿「390 打开」对「resize 到 390」比，两边都已被拆分；换成「同一页关掉 JavaScript」的
  自然折行才暴露出 70/120 不一致。

⚠ 服务器是多用户共享的，内存经常只剩 2–3G（别人的进程占着 25G，`pgrep chrome` 能看到
99 个都不是 `ly` 的）。playwright 脚本被 OOM kill（exit 137）时重跑即可，**不要去杀别人的进程**。

---

⚠ **验滚动锁定必须拿回真实滚动条**。Playwright 默认给 headless chromium 传
`--hide-scrollbars`，`innerWidth - clientWidth` 恒为 0 —— 没有宽度可失去，
再坏的补偿写法也不会位移，判据会**全绿地放过坏页面**。`tools/scrolllock.py` 用
`ignore_default_args=["--hide-scrollbars"]` 拿回滚动条，并在 gap 仍为 0 时 abort。
手机档（≤767）真机是 overlay 滚动条、本来就不占宽，所以那两条用例要在
**700 宽的桌面窗口**里跑才有意义。

---

## 三、对稿复查的方法

**为什么非看图不可**：第三十五轮把四条箭头的元素盒 solve 到与 `absoluteRenderBounds` 一致
（±2px），断言全绿，需求方仍说「箭头没还原」—— 并排放大一看短了 25~35%，因为 renderBounds
含 OUTSIDE 描边的斜接外扩，不是画出来的墨迹。第三十七轮又验证一次：`.gb-vs__table` 整块缩 15%、
`.gb-dosed__title` 的描边被入场动效啃出洞、Reviews 缺整个导航组件、五颗星是灰的 ——
**没有一条是数值断言查得出来的**。

```bash
python3 tools/pagescan.py science.html --list --depth 2                      # 两侧块各自排序打印
python3 tools/pagescan.py science.html --pairs ".gb-page-hero=192,.gb-compare=3162" --h 900
python3 tools/fq.py 324-58044 'Compare' --depth=2    # 查稿节点：按名字/文案
python3 tools/fq.py 324-58044 '324:58125'           # 或按 id（支持实例复合 id 的末段）
```

输出在 `tools/shots/`，**左＝设计导出，右＝实现**，中间一条品红分隔线，用 Read 工具直接看图。

⚠ **不要按文档顺序自动配对**：board 的 children 不按 y 排序（index 上 `Frame 992545@2442`
排在 `Footer@10040` 后面），且板子里夹着 build 折进上一个 section 的 `Spacer Top`（波浪）。
`pagescan.py` 第一版就是这么写的，出的图全是错位的。
⚠ **描边和可见性都要看**：nutrient 卡漏的 7px 青柠描边、PDP 多出的 testimonial，
都是只有翻 `strokes` / `visible` 才发现的。

### 坐标对齐（不先懂这个，出的图全是错位的）

```
截图 y = 节点的 absoluteBoundingBox.y − board 的 absoluteBoundingBox.y
```

多数 board 在内容上方还有一条 96px 的假浏览器栏（节点名 `Chrome browser`），
对这些 board：`截图 y = 内容帧相对 y + 96`。**逐页不同，别套用**：

| 页 | node 文件 | 内容帧 id | 假浏览器栏 |
|---|---|---|---|
| index | `228-5932_homepage-mobile` | `237:13125` | 有（96） |
| pdp | `324-53792_pdp-mobile` | 无（顶层即内容） | 有（96） |
| science | `324-58044_science-moble` | `324:58047` | 有（96） |
| reviews | `324-64961_reviews` | `324:64962` | **无** |
| how-gumi-works | `324-70523_how-gumi-works` | `326:89662` | **无** |
| our-story | `324-73673_our-story` | `324:73675` | 有（96） |
| faq | `324-76169_faq` | `326:93671` | 有（96） |
| get-in-touch | `326-80318_get-in-touch` | 无 | 有（96） |
| referral | `326-81540_referral` | `326:90991` | **无** |
| shipping | `326-83129_shipping` | `326:83131` | 有（96） |
| privacy-policy | `326-83399_privacy-policy` | `326:83401` | 有（96） |

⚠ **不要用页面顶部的单一偏移量贯穿全页** —— 实现与稿会一路漂开（波浪渲染高 12px、
订阅框是空的），到页脚能差几百 px。每个区块**各自重新锚定**。

⚠ **弹窗类 mockup 帧里混着假浏览器地址栏与布景**（移动端 promo 弹窗那张写着完全不相关的
`funkyfood.com.au`），跟真弹窗面板不在同一层级/尺寸，**只用来定位，不要照建**。
辨认法：找 scrim 矩形。memory: `figma-modal-mockup-includes-fake-staging`。

### 桌面绝不能被动到

需求方明确「只改手机端，如遇到不得不改电脑端结构的地方再改」。做法是存快照后
**按矩形多重集 + body 总高比 1440**，不要用 cssnap 自带的路径式 diff ——
只要新增了 DOM 节点，后面兄弟的下标就整体错位，比的是不同元素，会报出几千处假差异。

**这段已经落盘成 `tools/r42rect.py`**（另加了「整块位移还原」——
删掉一个盒子会让它后面所有元素上移，几百个矩形跟着「不同」，还原后剩下的才是真变化）。
下面留原文备查：

```python
import json, glob, os, collections
A, B = "tools/snap/r41", "tools/snap/<new>"
for fa in sorted(glob.glob(f"{A}/*.1440.json")):
    name = os.path.basename(fa); fb = os.path.join(B, name)
    a, b = json.load(open(fa)), json.load(open(fb))
    ra = collections.Counter(tuple(round(x,1) for x in s["#rect"]) for _, s in a if "#rect" in s)
    rb = collections.Counter(tuple(round(x,1) for x in s["#rect"]) for _, s in b if "#rect" in s)
    ha = next(s["#rect"][3] for p, s in a if p == "/html[0]/body[1]")
    hb = next(s["#rect"][3] for p, s in b if p == "/html[0]/body[1]")
    print(name, "only-in-old:", sum((ra-rb).values()), "bodyh:", ha, "->", hb)
```

### 断点交接

改了 narrow 的值就要配 tablet 斜坡，否则 767→768 跳变。逐属性对读 767 / 768 的 computed 值，
差 >1px 就是断层。⚠ `fluid()` **只能用于 px**，且起点必须等于 narrow 的值。

---

## 四、历轮踩到的坑（新写代码前看一眼）

1. **`column-reverse` 下 `flex-basis` 是高度。** 把两栏改成 `flex: 1 1 566px` 时，容器在
   窄档转了 `column-reverse`，566 被当成最小高度，hero 凭空高了约 390px。给那一档补 `flex: none`。
   症状在快照里很好认：**大量元素只有 y 变、x/w/h 全不变**。
   memory: `flex-basis-is-height-in-column-direction`。
2. **活性自检要破坏「真正负责的那条规则」。** 验「落单卡片居中」时破坏了
   `> * { grid-column: span 2 }`，只有 768 报红 —— 因为 `:last-child:nth-child(odd)` 那条
   独立生效。**判据：报红的档位数应当与断言覆盖的档位数相符。**
   memory: `negative-assert-needs-liveness-guard` 第五种。
3. **改堆叠阈值时同组配套规则必须一起搬。** r41 把三个模块的 `flex-direction: column` 从
   `stack`(1024) 移到 `mid`(991)，`__heading` / `__panel` / `__body` / `__disc` / `__media`
   六条 `@include stack` 全部要跟到 `mid`，否则 992–1024 会拿堆叠态的规则去排一个 row。
   `padding-inline` 留在 `tight` 没动 —— 版心内距和堆叠是两件事。
4. **`fluid()` 只能用于 px。** r40 一度写了 `top: fluid(-8%, -5%)`，百分比不能用 `calc()`
   随视口插值。那一档直接不做斜坡。memory: `percent-cannot-ramp-with-calc`。
5. **Figma 的 `line-height: 100%` 是 auto，不是字号的 100%。** 成分表节点自报 `12.0163px`
   （PP Palma 自然行距 1.26），写 9.54 会挤成一团。`leading-trim: CAP_HEIGHT` CSS 没有等价物，
   它只解释了为什么稿里单行 box 高 7 而非 12.02。
6. **等比缩放的例外要查，不能默认。** 成分表整表按 0.741529 缩放（字号 + 三条线宽四处印证），
   唯独两个数值列不行 —— 手机稿的行 Frame 是 427.72 宽装在 350 容器里，SPACE_BETWEEN 在超宽盒子里排。
7. **`absoluteRenderBounds` ≠ 画出来的墨迹**：带 OUTSIDE 描边的矢量组，renderBounds 含斜接
   外扩，比导出墨迹大 9~55% 且逐条不同。判据要在两张 PNG 上量墨迹，且**从图形自己的中心做
   连通域洪泛**（邻近同色元素会伸进任何合理窗口）。
   memory: `figma-renderbounds-inflated-by-outside-stroke`。
8. **loop slider 只在某个断点以下才是轨道时，有三个坑**（第四十一轮，`.gb-expert__cards`
   是第一个这样的 slider；`.gb-reels` 全断点都是轨道所以从没碰到）。
   守卫一律读 CSS（`overflowX` 是不是 `auto|scroll`），**别在 JS 里写死断点数值**：
   - `fill()` 无条件跑 → 992 以上那是三列 grid，9 个克隆排成多出来的三行；
   - 只是「不再新增」不够 → 从轨道 resize 回 grid，之前的克隆还在 DOM 里，要 `unfill()`；
   - 克隆继承 `.wowo` → 本项目的 wowo 是 scroll 驱动、每次重新 `querySelectorAll`，
     所以**不是永久不可见**，而是副本比旁边的原件晚一拍淡入。克隆时剥掉
     `wowo` / `animated`。
   另外 loop 轨道初始 `scrollLeft` 是 0（第一份拷贝的左缘），**第一次点「上一张」滑不动**，
   要 `home()` 把它停到第二套。`data-slider-centre` 的那几个已经在做同一件事。
9. **活性自检破坏一处不够，要破坏「所有能让断言通过的路径」**（第四十一轮再次踩到，
   与上面第 2 条同源）。验「桌面不被克隆」时先去掉了 `fill()` 里的 `isRail()` 守卫，
   **结果全绿** —— 因为 `relayout()` 里还有一层守卫，grid 档走的是 `unfill()` 分支，
   根本没调 `fill()`。两处一起破坏才报出 4 个网格档 × 12 张卡。
10. **判据不能写在被自己的注入表掩盖的量上**（第四十一轮）。验「克隆没继承 `.wowo`」
   时读 computed opacity，而 `SETTLE` 里正有 `.wowo{opacity:1!important}` ——
   破坏之后依然全绿。改成 class 检查，另配一张**不注入 SETTLE、也不滚动**的高视口页面
   读 opacity 兜底。⚠ 后者仍抓不到 class 那条（Lenis 初始化时的 scroll 会让 wowo
   重查并补播），它防的是「wowo 哪天改成一次性观察」，已在脚本里标注了这个边界。
11. **搬堆叠阈值时，先算一下新带宽装不装得下那两栏**（第四十二轮）。把 product 的
   堆叠点从 1024 挪到 767，等于要求两栏在 768 也并排 —— 而 `__media` / `__info`
   都是写死的 465，954 塞进 728 的盒子，**横向溢出 163px**。和第四十轮 page-hero
   是同一个病，解法也一样：一对可伸缩 basis（`flex: 0 1 465px` + `min-width: 0`），
   1440 处两栏之和正好等于内容盒，所以桌面一字不动。
   ⚠ 判据要取**溢出**，不是 `flex-direction` —— 方向断言在溢出时照样是绿的。
12. **单列网格必须重置 `grid-column: span 2`**（第四十二轮）。四轨跨二的两列装置降到
   一列时，只改 `grid-template-columns: 1fr` 不够：对着一条轨道，隐式网格会拿那个
   span 再造出第二列来，卡片依旧两列排。活性自检里删掉重置那两行，575 立刻报 2 列。
13. **「两列」不能用不同的 x 位置个数来数**（第四十二轮的判据坑）。三张卡跨两轨、
   落单那张居中，它与前两张谁的 x 都不同 —— 正常的两列网格会被数成 3 列。
   用**行数**判断（3 张卡：三列 1 行 / 两列 2 行 / 单列 3 行）。
14. **Python 的 `\s` 匹配 U+2028**：拿 U+2028 当 `<br>` 的标记做换行断言，正规化时标记会被
   连同硬换行一起压成空格，**断言恒真报全绿**。换 `\x00`。memory: `regex-s-eats-u2028-marker`。
15. **`getComputedStyle` 读自定义属性拿到的是未求值的 `calc()` 串**（第四十三轮）。
   `--sc-h` / `--sc-lg-h` 是 `calc(var(--sc-w) * 0.24008 + var(--sc-band))`，读回来就是这串文本，
   `float(v[:-2])` 直接抛异常（或更糟：被吞成 None 后断言静默失效）。要像素就**造一个
   一次性盒子量**：`div.style.height = 'var(--sc-h)'` → `getBoundingClientRect().height`。
   memory: `custom-prop-computed-is-unevaluated`。
16. **「加了个上限」不能只读回 `max-width`**（第四十三轮）。`.gb-product__inner` 的基础规则
   本来就有 `max-width: 995px`，手机端要去掉的只是 `560px` 那条覆盖 —— 断言写成
   `max-width == 'none'` 会报红，而它其实改对了。**判据取盒子的实际宽度**（「跑满视口」/
   「等于 min(版心, 上限)」），属性只用来反证那条特定覆盖不在了。
18. **行尾的 `&nbsp;` 不会悬挂，会把自己折到下一行**（第四十四轮）。稿里 `<br>` 前
   写 `&nbsp;` 是为了「br 隐藏时顶上这个空格、且此处不断行」，但 U+00A0 在行末不像普通
   空格那样折叠/悬挂：行内容只要**超出容器哪怕 0.5px**，这个 nbsp 就单独占一行，
   `lineReveal` 的块级 mask 于是多出一个空行盒，描边层还会在那行画出一团色块。
   实测：改成普通空格后，6 页 × 11 档 × 全部行揭示元素里**只有出问题那一处变了**，
   「不断行」的职责根本用不上。判据 = `tools/emptyline.py`。
19. **数「视觉行数」有两个陷阱**（第四十四轮，这条判据写错过两次）。
   ① 数 `.gb-line-word` 的 `offsetTop` 会**漏**：词是 `inline-block`，自己内部折行
   （长词在连字符处断开）时仍然只有一个 top。② 改数整个元素的 Range 行盒会**翻倍**：
   `.gb-ink-halo` 是同一份文案的描边副本。正解 = 只取内容层词的 Range 行盒，
   并按 3px 容差聚类吸收亚像素差。
20. **一张固定轮廓拉到一个比例会变的盒子上，必然变形**（第四十五轮）。CTA 板的
   `mask-size: 100% 100%` 就是这个：盒子宽高比从 0.69 走到 3.26，圆瓣在 767 被横向拉
   2.07 倍、768 被压到 0.44 倍。解法不是换一张图，是**换构造** —— 认出轮廓其实是
   「固定半径的瓣按固定间距排开」，就能用九宫格 `border-image` 让**瓣数**跟着盒子走
   而不是**瓣形**跟着盒子走。⚠ `border-width` 必须留 0（否则盒子长大），
   但 `border-style` 不能是 `none`（否则图根本不画）。
22. **`border-image` 的区块交界在分数 DPR 下会留下发丝线**（第四十六轮）。四个区块
   各自抗锯齿，两条相邻半透明边凑不满一格不透明度，于是「离边 r 的那个矩形」上出现一条
   比底色浅的线。⚠ **只在某些 DPR 下出现**：实测 1.25 / 1.75 / 2.25 有，1 / 1.5 / 2 / 3 没有 ——
   正好是 Windows 125% / 150% / 175% 缩放那几档，**只测整数 DPR 会全绿**。
   解法是图下面垫一层同色实底，且实底必须内缩到形状的最内点以内，否则会把轮廓填平。
21. **别把浏览器的取整规则写进断言**（第四十五轮）。`border-image-repeat: round` 的
   落点，实测 Chrome 与 `round()` / `ceil()` 都对不上（3.43 个周期它取 4 个）。
   判据要取**与实现无关的不变量**：谷深（与平铺缩放无关，`d = r − r√(1−(p/2r)²)` 里
   缩放约掉了）、间距均匀性、边段是不是整数次平铺。
17. **scroll-snap 的「居中」是相对滚动口，不是内容盒**（第四十三轮）。`scroll-padding`
   默认 0，所以轨道自己的 `padding-inline` **不参与**吸附位置的计算。
   反过来，`slider` 里 `centre()` 的算式也没算 padding —— 它是给 reels 那条无 padding 的
   轨道写的，**给带 gutter 的轨道用会偏一个 padding**。带 `[data-slider-loop]` 的轨道
   靠克隆本来就能居中，直接用 CSS 的 `scroll-snap-align: center` 即可，不要挂
   `data-slider-centre`。判据要**驱动轨道到静止位再量前后两张露出的宽度**，
   只读回 `scroll-snap-align` 什么都证明不了。

---

## 五、待决事项索引（全部在 [PROJECT-STATUS.md](PROJECT-STATUS.md)）

| | 事项 | 轮次 |
|---|---|---|
| A–D | 桌面/手机稿文案冲突（6）、占位数量冲突（2）、稿自身 WIP 痕迹（2）、两端同源不敢动的（2） | 三十七 |
| E | footer 链接区结构分歧（分组版 vs 两列版，+116 高） | 三十八 |
| F | `.gb-footer` padding-bottom 24 vs 板的 48 | 三十八 |
| ~~G~~ | ~~`font-check.html` 两条断言从第十九轮起恒假~~ — **五十二轮改写，连带清掉另外两条没登记的，关闭** | 三十九 |
| ~~H~~ | ~~reviews.html 的 `.gb-app-slot`~~ — **四十一轮已删，关闭** | 三十九 |
| ~~I~~ | ~~`.gb-promo-card__list` 的 margin 语义~~ — 五十一轮关闭，**五十四轮又反转回正居中，重新打开** | 三十九 |
| **J** | **堆叠阈值 991 与第二十九轮的「推到 1200」方向相反** | 四十 |
| K | footer 链接区对齐已反转两次，当前是第三次落法 | 四十一 |
| L | `.gb-app-section` 删掉占位框后只剩一个标题 | 四十一 |
| ~~M~~ | ~~去掉宽度上限后两个正方形贴边~~ — **四十三轮由第 8/9 条裁决，关闭** | 四十二 |
| N | `.gb-stat__value` 要不要也加数字增长（双层 + 已有行揭示） | 四十二 |
| O | `.gb-dosed__media` 手机端仍停在 350，要不要跟齐 520 | 四十三 |
| P | expert 轨道的居中只落到 767 以下，要不要整条轨道都居中 | 四十三 |
| Q | 第 6 条的「media 最大宽度」没给数值，本轮推算取 520 | 四十三 |
| ~~R~~ | ~~任务文档第 10 条正文为空~~ — **四十四轮已补齐并完成** | 四十三 |
| ~~S~~ | ~~`gb-cta-band` 背景形状变形（第 13 条）~~ — **四十五轮用九宫格 border-image 解决，关闭** | 四十四 |
| T | 第 11 条的 `gap: 80px` 没写档位，本轮按基础档落 | 四十四 |
| U | `.gb-page-hero__title` 在 1281 折成 5 行（顺带发现，未修） | 四十四 |
| **V** | **CTA 按钮标签折行的真因是 `__content` 的 38 gutter，本轮只治标（内缩 24）** | 四十七 |
| **W** | **两个 `--center --lg` 页头桌面各矮 26px（第 15 条的代价）** | 四十七 |
| X | 富文本段距只改了手机端，桌面仍是 20（板是 16） | 四十七 |
| Y | shipping 表格网格现在在所有宽度都画，768+ 没有稿背书 | 四十七 |
| ~~Z~~ | ~~footer CTA hover 后底色 == 底板色~~ — 第五十轮需求方撤回 ✅ | 四十九 |
| **AA** | **`.gb-header__logo` 去掉了 hover —— 可点元素无反馈，与公约 13 相反** | 四十九 |
| ~~AB~~ | ~~第 8 条的撤回只落到 95% 组~~ — 第五十轮裁决：两组统一 56/44 ✅ | 四十九 |
| AC | reel 弹窗播放图标的 hover 颜色是自定值（稿里没有这个 lightbox） | 四十九 |
| AD | deco-bear 钉成 px：1440 处大了 1.1px，768–1280 的斜坡是推算值 | 四十九 |
| ~~AE~~ | ~~Swiper 154KB 值不值~~ — 第五十轮裁决：值，全站轮播都改 ✅ | 四十九 |
| ~~AF~~ | ~~sticky 要不要铺到其他页~~ — 第五十轮裁决：每一页都钉 ✅ | 四十九 |
| **AG** | **全站轮播改 Swiper 后无限循环没了，换成 rewind（到头倒回）** | 五十 |
| AH | expert 轨 ≤991 去掉了容器 padding；要不要改成对齐版心 gutter | 五十 |
| **AI** | **三列的下界从 1281 降到 1201，那一段每列 336.5（1281 处是 357.7）** | 五十一 |
| AJ | `.gb-product__cta` 的最大宽度没给数值，本轮取 520 并居中 | 五十一 |
| **AK** | **`.gb-deco-bear--b` 的 top 改百分比后离开板宽会漂（1281 −7.4 / 767 −52.4 / 320 +55.8）** | 五十三 |
| AL | `.gb-vs__table` 只在 ≤575 全宽；一路全宽要连熊一起重排 | 五十三 |
| AM | 抽屉 CTA 的 520 是取的值不是板值，且左对齐不居中 | 五十三 |
| AN | `.gb-science-card__text` 的 6px 落在全局，需求那句没写作用域 | 五十三 |
| AO | 数字描边 0.145em 偏离板值 1.1px（消白斑的最小代价） | 五十三 |
| **AP** | **第三组·3 语义不明，未动手（`--cream` 版第 4 张卡的对齐）** | 五十三 |
| ~~I（重开）~~ | ~~promo 列表的居中语义~~ — **五十五轮终版：pc 居中 / 手机端不居中，关闭** | 五十四 |
| ~~AT~~ | ~~768–1280 的弹窗形态~~ — **五十九轮关闭**：768 以上一律双栏，缩放而非重排 ✅ | 五十四 |
| **AX** | **手机端的 `lip--h` 要不要跟着 `lip--v` 一起变浅（−65 是换算值不是板值）** | 五十六 |
| **AY** | **favicon 版式无稿背书；16px 下四个字母读不出，要不要改成单个 `G`** | 五十七 |
| **AZ** | **cart 的产品缩略图 / 礼物图是稿里的 `#D9D9D9` 占位，要不要换成 `product-pack.png`** | 五十八 |
| **BA** | **cart 的 totals/bar 内容宽按 fill 351 做，没照抄稿上不一致的 344 / 343** | 五十八 |
| **BB** | **空态 Secure Checkout 只有视觉禁用，没有 `aria-disabled`** | 五十八 |
| **BC** | **抽屉用滑入（`$t-drawer`）不是淡入 —— 这条是我定的** | 五十八 |
| **BD** | **下拉档位里 `2/6/8 Weeks` 是编的，上线前须换真实档位** | 五十九 |
| ~~AU~~ | ~~「手机端」阈值~~ — 五十五轮需求方选择忽略，维持 ≤767 ✅ | 五十四 |
| ~~AV~~ | ~~国家码 `<select>`~~ — 五十五轮「一起改」，已落地 ✅ | 五十四 |
| ~~AW~~ | ~~typeahead~~ — 五十五轮需求方选择忽略 ✅ | 五十四 |

**J 已在第四十二轮定向**：需求方两次点名 767，三次改动一路往「更晚堆叠」推
（1024 → 991 → 767），第二十九轮那条「推到 1200」作废。
**M 已在第四十三轮关闭**：版心搬回 `__inner`、两个正方形各加 520 上限。
**S 已在第四十五轮关闭**：九宫格 `border-image`，纯 CSS，不换图不依赖 JS。
剩下的 K / L / N / O / P / Q / T / U / V / W / X / Y / AA / AC / AD / AG / AH /
AK–AP / AT / AX / AY 都是一句话就能定的，一起问。**AT 要重问**（第五十四轮没讲清楚，
需求方回「糊了」）—— 问法只有一句：**768–1280 这一档的邮件弹窗想要什么形态？**
**AG / AA 最值得先问** —— AG 是全站轮播丢了无限循环（要恢复只能加卡，是内容决策）；
AA 让 logo 完全没有反馈，与公约相反。其次是 O / Q / T / V / W / AD / AH
（需求没给数值或档位、我按依据推算）。

**顺带发现未修（第四十九轮）**：手机抽屉关闭时有和弹窗一模一样的抖动
（767 以下的桌面窗口，实测 700 → 685）。修法与弹窗同形，等授权。

---

## 六、常驻遗留（跨轮次，不属于任何一轮）

- **768–1280 这一档始终没有设计稿**。所有值要么是 390→1281 的 `fluid()` 斜坡，
  要么是行为约束（比例、不塌陷），**没有一个是板值**。
- **小波浪手机端仍高 12px**（`--sc-band` clamp 下界，第三十五轮起）。已经有四处 padding
  靠它换算（CTA 52、footer 52、`.gb-vs` 52、`.gb-faq` 52），波浪修好后这些要回到板的 64。
  修它等于重设波浪的断点体系，会动全站 11 页每个 section 的 padding-bottom 与页面总高。
- **PP Palma 300（FizzyLight）仍是试用包**，EULA 排除商业用途、不随仓库分发。
- **`$font-ui-stack` / `$font-display-stack` / `$font-hand-stack` 全站零引用** →
  Inter / Lexend / Playpen Sans 三套 webfont 从不下载，`@font-face` 与 6 个 woff2 是死代码。
  删之前先确认稿里那 409/108/90 处是有意没实现，还是当初漏了改 `font-family`。
- **`.gb-stats__deco-bear` 素材比例与稿对不上**（稿 146×186 = 0.785，素材墨迹 376×577 = 0.652，
  同宽摆放高出约 33px），要改得重导素材。
- **`.gb-vs__bear` / `__logo` / `__others` 在 768–1024 仍用桌面比例**（与 `pile` 同源的既有问题，
  只是不溢出所以 `rwd.py` 抓不到）。
- **`tools/snap/` 已占 799M，`/` 用到 97%（剩 8.1G）**。`r38`（547M）标注可清。
  磁盘和内存都紧张时 cssnap 会被 OOM kill —— 那是共用机器的常态，不是脚本坏了。
- ⚠ **「Shopify 主题化尚未开始」这句在 2026-09-03 被证伪** —— 线上 live 主题里早已有
  5 个 `gb-` section + 21 个 `gb-` block，`$build` 停在 `20260831-r58`。
  三项已定：店铺 `je1ka9-er.myshopify.com` / 主题基底 Shopify **Horizon 4.1.5** /
  接入方式 `snippets/gb-head.liquid` + `gb-scripts.liquid` 挂 `asset_url`。
  **但主题的 liquid 只存在于线上，本地没有源** —— 静态站是 CSS/JS 的源，
  liquid 是线上唯一副本。这一点与 EuroCave 同形，改之前先 pull 基线。
- ⚠ **`docs/LIVE-GAP.md` 已过时**（写于 2026-09-04 第六十九轮）—— 对方在 r79 之后陆续补了
  `gb-promo` / `gb-vs` / `gb-app-section` / `gb-nl-modal` 四个 liquid，还给 `gb-product` 加了
  营养标签的 metaobject fallback。**照着它列缺口会多报**，要用先复跑 `tools/livediff.py`。
- ⚠ **`docs/LIQUID-TODO-reels.md` 整份作废**，已移到 [archive/](archive/)。
- **`.gb-product__guarantee` 的图标尺寸（5 个页面）与 `gb-nutrition → gb-product` 的交界波浪
  仍未处理** —— 后者需对方加 liquid 且要支持 `--bleed`。判据会打印但不断言。
- **静态站 11 页 ≠ 主题的页面**：主题里是 `templates/page.*.json` + `gb-page` section，
  内容存在 JSON 模板的 settings 里（后台可编辑）。HTML 与 liquid 是两套源，
  HTML 改了不会自动进主题。

---

## 七、审计专用

> ⚠ 本节数字是 **r41 实测基线**，不是结论。与你实测冲突时以实测为准并在报告里点明。
> **审计只出报告不改代码**，报告写到 `docs/audit/`，一条线一个文件。

### 架构

- 样式**只有 `assets/customstyle.scss` 一个源**（8472 行，第十五轮由 36 个 partial 合并而来），
  产物 `customstyle.css` 232K 未压缩。文件分「定义段 → 输出段」，**块的相对顺序是层叠依赖**，
  改之前先看文件头那段说明，别随手挪动。
  ⚠ `:root{--pad-x}` 留在输出段 reset 之后的原位（它是 CSS 输出不是定义），
  合并前后产物逐字节相同就是靠这个安排，**别当成错误「修正」**。
- `assets/main.js` **1224 行、零依赖**（无 jQuery / GSAP / Swiper / AOS），单个 IIFE，
  13 个模块：`wowo` / `header` / `bearMeter` / `popText` / `lineReveal` / `packBand` /
  `accordion` / `modal` / `promoModal` / `slider` / `gallery` / `enquiryPrefill` / `smoothScroll`。
  另 vendored `assets/lenis.min.js`（Lenis 1.3.11，MIT）。
- 计数基线：`!important` 6 / `z-index` 21 / `@media` 块 611（产物）/
  `@include hover` 43 / `transition` 74。**hover 与 transition 的比值是铁律 13 的自查判据**，
  两个数差很多就是有 hover 没配过渡。
- `images/` 8.7M / 43 文件，其中 16 个 webp（第十四轮 WebP 化把首屏从 17.61MB 降到 3.78MB）。
  ⚠ **`bear-icon.png` / `.webp` 不在这里，在 `assets/`** —— CSS 里 `url()` 引用的图片
  必须与样式表同目录且写裸文件名，否则一上 Shopify 主题就 404（第六十一轮，判据 `assetpath.py`）。

### 关键契约（改之前必须懂）

- ⚠ **richtext setting 绝不能直接印进 `<p>` 宿主**（第七十一轮，线上实测）：richtext 的值自带
  `<p>` 包裹，HTML 解析器遇到内层 `<p>` 会**强制关闭外层**，DOM 被拆成三个兄弟 ——
  宿主变成空元素（实测 `.gb-hero__lead` textContent 为空、高度 0），文字落到无 class 的裸 `<p>` 里
  **用浏览器默认 16px 渲染**，挂在宿主上的 `data-line-reveal` 也一起失效。
  五处已改走 `{% render 'gb-rich-inline', html: … %}` 剥掉外层 `<p>`。
  **以后往 `<p>` 里放任何 richtext 都要走这个 snippet**；`inline_richtext` 不受影响（它不包 `<p>`）。
  判据 `tools/r71check.py` 第 4 组会扫全部 section。
- ⚠ **`[data-line-reveal]:not(.is-split) { opacity: 1 }` 是故意的，别删**
  （`customstyle.scss:3321`）：main.js 拆行之前文字必须可见，否则 JS 一挂文字永久不可见。
  代价是 main.js 越晚、"文字先出现再播动画"的窗口越长 —— 线上实测 4029ms，静态站 657ms。
  **正确的解法是让脚本早点跑（第七十一轮给三个脚本加了 `defer`），不是删这条兜底。**
- **`.wowo { opacity: 0 }` 的隐藏门不是无条件的**（第十四轮改）：规则是
  `html.js .wowo { opacity: 0 }`，`js` 类由 `<head>` 内联脚本加、并在 `load`（或 4s 兜底）时
  **若 `window.gumi` 不存在就摘掉**。只加 `js` 类不够 —— 那行内联脚本在 main.js 404 或顶层
  抛异常时照样执行。任何触碰 main.js 或加载顺序的改动，都要验首屏元素最终 `opacity` 回到 1。
- **wowo 只播一次不可重播**：进视口加 `.animated` 播 0.7s → 1500ms 后移除两个 class。
- **`data-pop-text` 逐词弹出只用在首页四个 `.gb-stat` 上**，且第三十三轮把 `.gb-stat` 也改成了
  行揭示，`popText` 从此零使用者。其余文字走 `wowo fadeInUp` 或 `[data-line-reveal]` 行揭示。
  **两套不能混**。
- **Lenis**：`html { scroll-behavior }` 必须保持 `auto`（Lenis 内部走 `window.scrollTo`，
  写 smooth 就是两层平滑套一起）；**每新增一个 `overflow-y:auto` 容器都要登记进
  `smoothScroll.PREVENT`**，否则 Lenis 吃掉滚轮那个容器再也滚不动。现有三个
  （`.gb-product__thumbs` 只桌面可滚 / `.gb-header__panel` 只手机可滚 / `.gb-nl-panel__body`），
  **单一视口验不全**，`rwd.py` 逐视口盯着。
- **无错误边界**：单 IIFE，任一模块抛异常会中断后续模块初始化 —— 这条直接关系到上面的
  「首屏永久不可见」风险，值得审。

### 已知技术债 / 可疑点（可直接查证）

1. **三个 mask 内联成 data URI**（约 27KB）是**被迫的**，不是体积失控（见「一·3」的 CORS 条）。
2. **`.gb-scallop` 波浪用 repeating-radial-gradient 画**，几何靠节距推导
   （`r = 0.6407d`、`amp = 0.24008d`）；固定尺寸写法在 ≥1920 会把弧切断。
   ⚠ `--wave-under` 是不变式（配 `height +1px / margin-bottom -1px` 叠边），修的是 Windows
   分数缩放下的发丝缝；`--wave-bg` 透明的三种变体必须同时设 `--wave-under: transparent`。
3. **`.gb-cta-band` 的 mask 是从画板渲染图抠的**，不是几何生成 —— 那组弧不满足 `r = 0.6407d`。
   代价：低于 1280 宽时弧会略微压扁。
4. `customstyle.css` **未压缩**是有意的（静态阶段要能在浏览器里直接对源），Shopify 阶段再上构建。
5. **性能审计要先分阶段**：CSS/JS 压缩合并、图片 CDN / 响应式尺寸、缓存头都是 Shopify 平台侧
   接管的，静态阶段报了没意义。现在值得报的是：图片**源体积**、lazy 覆盖率、字体族数量与
   preload、以及 `.wowo` 与 LCP 的关系（要实测不要推断）。
6. **根目录 `1e4ea5b2-….png`** 是对话中贴入的临时截图，不属于项目。

---

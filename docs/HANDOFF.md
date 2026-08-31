# Gumi Brand — 交接

> 一份文档管三种会话：**接手做需求** / **对稿复查** / **做审计**。
> 项目定位与已确立的规范在 [PROJECT-STATUS.md](PROJECT-STATUS.md)；
> 改动史在 [CHANGELOG.md](CHANGELOG.md)（近 10 轮）+ [CHANGELOG-ARCHIVE.md](CHANGELOG-ARCHIVE.md)（第一～三十轮），**两份一起 grep**。
>
> 状态：`$build` = **`20260831-r58`**（第五十六轮），已编译；⚠ **验证不完整**
> （第五十五轮被叫停，`rwd.py` 等七项至今未跑，清单见 CHANGELOG 第五十五轮「未跑」一节，
> **下一轮第一件事是补跑**）。
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

---

## 二、验证怎么跑

```bash
cd /home/ly/project/Gumi-Brand
npx sass@1.77.8 assets/customstyle.scss assets/customstyle.css --no-source-map

# 逐轮定向断言（全部应通过）
for s in r31check r32check r36check r39check r40check r41check r42check r43check r44check r45check r48check r50check r52check r53check r55check r56check r57check r58check; do python3 tools/$s.py; done

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
| **AT** | **768–1280 的弹窗形态（需求方回「糊了」，要重问：这一档想要什么形态）** | 五十四 |
| **AX** | **手机端的 `lip--h` 要不要跟着 `lip--v` 一起变浅（−65 是换算值不是板值）** | 五十六 |
| ~~AU~~ | ~~「手机端」阈值~~ — 五十五轮需求方选择忽略，维持 ≤767 ✅ | 五十四 |
| ~~AV~~ | ~~国家码 `<select>`~~ — 五十五轮「一起改」，已落地 ✅ | 五十四 |
| ~~AW~~ | ~~typeahead~~ — 五十五轮需求方选择忽略 ✅ | 五十四 |

**J 已在第四十二轮定向**：需求方两次点名 767，三次改动一路往「更晚堆叠」推
（1024 → 991 → 767），第二十九轮那条「推到 1200」作废。
**M 已在第四十三轮关闭**：版心搬回 `__inner`、两个正方形各加 520 上限。
**S 已在第四十五轮关闭**：九宫格 `border-image`，纯 CSS，不换图不依赖 JS。
剩下的 K / L / N / O / P / Q / T / U / V / W / X / Y / AA / AC / AD / AG / AH /
AK–AP / AT / AX 都是一句话就能定的，一起问。**AT 要重问**（第五十四轮没讲清楚，
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
- **Shopify 主题化尚未开始**，当前是 11 页静态站，店铺 / 主题基底 / 接入方式三项未定。

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
- `images/` 8.7M / 37 文件，其中 17 个 webp（第十四轮 WebP 化把首屏从 17.61MB 降到 3.78MB）。

### 关键契约（改之前必须懂）

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

## 八、工作区状态（第五十六轮末）

- `$build` = `20260831-r58`，全站 **38** 处 `?v=` 与 `font-check.html` 的 `EXPECT_BUILD` 一致。
  第五十六轮**没有动过 HTML 结构**（只有 `?v=`）。
- ⚠ **验证仍不完整**（第五十五轮被叫停的那一批至今没补）。
  第五十六轮已跑全过：`r58check`（44 条）+ 双向判据（改前 6 条红，css md5 一致）
  + `r31` / `r40` / `r44` / `r52` / `r55` / `r56` / `r57`。
  **仍未跑：`rwd.py` / `r53check` / `scrolllock` / `revealcheck` / `hardbreaks` /
  `platecheck` / `seamcheck` / `font-check.html` / 全站矩形波及比对。**
- 三个页面**运行时**会多出 DOM 节点（`selectBox` 建出来的下拉，每个控件 10 个上下）：
  `get-in-touch`（两个：国家码 + 询问类型）、`referral`（一个：国家码）。
  `cssnap.py diff` 对这两页无效，用 `r42rect.py`。
- `assets/customstyle.css` 是最新编译产物，无警告（md5 `13e7107…`）。
- `assets/main.js` 现在是 **15 个模块**（`selectBox` 注册在 `enquiryPrefill` 之后 ——
  顺序有意义，它要读到预填好的 `selectedIndex`）。`selectBox` 有两个变体：
  默认（询问类型，自带 44 高的白盒）与 `bare`（国家码，无盒子，`.gb-field__phone` 画边框）。
- `assets/swiper-bundle.min.js` 是 vendor 原件（Swiper 11.2.6，MIT，154KB），**不要改它**；
  它用到的样式以「Vendor — Swiper」分区写在 `customstyle.scss` 里，没有第二个样式表。
  **全站每一个轮播都跑在它上面**：产品图廊（5 页，fade）、reels 横轨（4 页，**10 张卡跑
  `loop`**）、expert 卡片轨（1 页，3 张卡跑 `rewind`，≥992 销毁后变三列网格）。
- **提交历史（2026-08-31 全部已推送）**：`59ad586`（第三十八～五十五轮，59 files /
  +16740 −4801）→ `5daa99a`（补记推送状态）→ `7e08ff6`（第五十六轮 r58）。工作区干净。
- git 远端 `github.com/luyouse-luka/Gumi-Brand--Temporary`（private，临时同步仓库），分支 `main`。
  推送走 SSH 别名 **`github-luyouse-user`** —— 裸用 `github.com` 会走 devmtc-1 那把 key 认证失败。
- **推送等明确指令**，共用环境绝不全量、绝不 `--delete`。

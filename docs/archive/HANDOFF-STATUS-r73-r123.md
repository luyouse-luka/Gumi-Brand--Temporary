# Gumi Brand — HANDOFF 状态段归档（第七十三～一二三轮）

> 2026-09-09 从 [../HANDOFF.md](../HANDOFF.md) 分卷而来，**原文未改一字**。
> HANDOFF 顶部只保留最近 3 轮的状态段；每轮的推送清单 / 三方对比 / 判据数字另见
> [../PUSH-LOG.md](../PUSH-LOG.md)（覆盖第一〇四轮起）。
> ⚠ 各轮的「不要报成 bug」已原文沉淀进 HANDOFF 第一节的 `### 4`，**那里才是现行清单**，
> 本文件只作原始出处备查。

---

> 状态：**第一二三轮（2026-09-09）—— reel 就地播放、弹窗整套删除，`$build` = `20260909-r123`，已推 live**。
> 推 `main.js` + `customstyle.scss` / `.css` + **`sections/gb-reviews.liquid`（对方的文件，经授权）**。
> 新基线 **`baseline-20260909-r123`**（624 文件）。三方对比 ours 4 / **theirs 0** / CONFLICT 0。
>
> 判据：`tools/reelplay.py` 静态 **23/0** / `--live` **20/0** / `--strip` **8 red**；
> 回读 4 个逐字节一致 + 620 个清单外零附带改动；
> 回归 `r67reel` 26/0、`rwd` 全绿、`heroseq` / `r121check` 全绿、`menutab` 58/0、`crevcheck` 全绿。
>
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

---

> 状态：**第一二二轮（2026-09-09）—— hero 入场改成一条时间线，`$build` = `20260909-r122`，已推 live**。
> 推 `assets/main.js` + `customstyle.scss` + `.css`。新基线 **`baseline-20260909-r122`**（624 文件）。
> 三方对比 ours 3 / **theirs 0** / CONFLICT 0。
>
> 判据：`tools/heroseq.py` 静态 **10/0**（390 档 11/0）/ `--live` **10/0** / `--strip` **6 red**；
> 回读 3 个逐字节一致 + 621 个清单外零附带改动；
> 回归 `refocusring` 静态+线上各 24/0、`r121check` 15/0、`menutab` 58/0（复跑）。
>
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

---

> 状态：**第一二一轮（2026-09-09）—— Escape 归还焦点不再画 focus 样式 + 居中 hero 标题封顶，
> `$build` = `20260909-r121`，已推 live**。推 `assets/main.js` + `customstyle.scss` + `.css`。
> 新基线 **`baseline-20260909-r121`**（624 文件）。三方对比 ours 3 / theirs 5 / CONFLICT 0。
>
> 判据：`tools/refocusring.py` 静态 **24/0** / `--live` **24/0** / `--strip` 反向 **4 red**；
> `tools/r121check.py` 静态 **15/0** / `--live` **15/0**；
> 回读 3 个逐字节一致 + 621 个清单外零附带改动；
> 回归 `menutab` 58/0、`scrolllock` 44 条 0 failed、`placeholderbg` 50/0、`r119check` 13/0、`crevcheck` 全绿。
>
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

---

> 状态：**第一二〇轮（2026-09-09）—— 占位图灰底全部去掉，`$build` = `20260909-r120`，已推 live**。
> 只推 `assets/customstyle.scss` + `.css` 两个 asset。
> 新基线 **`baseline-20260909-r120`**（624 文件）。三方对比 ours 2 / **theirs 7** / CONFLICT 0。
>
> 判据：静态站 `tools/placeholderbg.py` **50/0**、线上 `--live --password 1234` **40/0**、
> 反向 `--strip` **33 red**（注入灰底后确实转红）；
> 回读 2 个逐字节一致 + 622 个清单外文件零附带改动；
> 回归 `crevcheck` all green、`crevlive` 30/0、`r119check` 13/0、`r119live` 8/0、
> `rwd` 全绿、`scrolllock` 44 条 0 failed、`r117check` 15/0。
>
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

---

> 状态：**第一一九轮（2026-09-08）—— 需求方三条：collection 页字体 / gift 媒体圆角 /
> `?type=` 预填，`$build` = `20260908-r119`，已推 live**。
> 只推 `assets/customstyle.css` + `.scss` + `main.js` 三个 asset。
> 新基线 **`baseline-20260908-r119`**（624 文件）。三方对比 ours 3 / **theirs 12** / CONFLICT 0
> （theirs 全是红线的 templates + settings_data，本轮零 template 推送）。
>
> 判据：静态站 `tools/r119check.py` **13/0**（旧产物上 7 red）；
> 线上 `tools/r119live.py --password 1234` **8/0**（推前 `--preflight` 12/0，含两条反向守卫）；
> 回读 3 个逐字节一致 + 621 个清单外文件零附带改动；
> 回归 `r117check` **15/0**、`r117live --cart` **11/0**、`menutab --live` **58/0**、`rwd` 全绿。
>
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

---

> 状态：**第一一八轮（2026-09-08）—— 预开状态的弹窗关不掉，`$build` 不变，已推 live**。
> 只推 `assets/main.js` 一个文件。新基线 **`baseline-20260908-r118`**（624 文件）。
> 三方对比 ours 1 / theirs 0 / CONFLICT 0。
> 判据 `tools/modalpreopen.py` 静态站 **17/0**、`--live` **20/0**（旧 JS 上 3 red）；
> 回归 `scrolllock` 44 条 0 failed、`menutab` 58/0、`r117check` 15/0。
>
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

---

> 状态：**第一一七轮（2026-09-08）—— 需求方八条（一条当场撤销、一条只能走后台），
> `$build` = `20260908-r117`，已推 live**。改 `customstyle.scss` + `.css` + `main.js`
> + **`sections/gb-reviews.liquid`**（经授权）+ 12 个静态 HTML（只进 git）。
> 新基线 **`baseline-20260908-r117`**（624 文件）。三方对比 ours 4 / **theirs 1** / CONFLICT 0。
>
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

---

> 状态：**第一一六轮（2026-09-08）—— 需求方三条：science CTA 填值 / Tab 走完菜单再走 bar /
> highlight-card 白线，`$build` = `20260908-r116`，已推 live**。
> 改 `customstyle.scss` + `.css` + `main.js` + **`templates/page.science.json`**（红线例外，经授权）。
> 新基线 **`baseline-20260908-r116`**（624 文件）。三方对比 ours 4 / theirs 0 / **CONFLICT 0**，
> 回读 4 个逐字节一致 + 620 个零附带改动。
>
> 判据：线上 `tools/r116live.py` **12/0** + `tools/menutab.py --live` **58/0**；
> 静态站 `tools/r116check.py` **9/0**（旧 CSS 上 3 red）、`tools/menutab.py` **58/0**
> （旧 JS 上 5 red，全在新增的 I 段）；回归 `scrolllock.py` 44 条 0 failed、`rwd.py` 全绿。
>
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

---

> 状态：**第一一五轮（2026-09-08）—— 需求方四条，`$build` = `20260908-r115`，已推 live**。
> 改 `customstyle.scss` + `.css` + `main.js` + **`liquid/sections/gb-science.liquid`**（新建，
> 取自 `baseline-20260908-1000` 的线上版）+ 静态站 `science.html`。
> 新基线 **`baseline-20260908-r115`**（624 文件）。**清单外零附带改动。**
> 判据：线上 `tools/r115live.py` **25/0** + `tools/menutab.py --live` **45/0**；
> 静态站 `tools/r115check.py` **30/0**（旧 CSS 上 10 red）、`tools/menutab.py` **45/0**
> （旧 JS 上 3 red，全在新增的 H 段）；回归 `scrolllock.py` 44 条 0 failed、`rwd.py` 全绿。
>
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

---

> 状态：**第一一四轮（2026-09-08）—— footer `title` 补回 + reviews 两处断行，已推 live**。
> 推 `sections/gb-footer.liquid` + `templates/page.reviews.json`，**零 asset、`$build` 不变**。
> 新基线 **`baseline-20260908-1000`**（624 文件）。实测 **7 ok / 0 red**。
>
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

---

> 状态：**第一一三轮（2026-09-08）—— 菜单键盘路径 + footer 链接 hover + 两处换行标记，
> `$build` = `20260908-r113`，已推 live**。改 `customstyle.scss` + `.css` + `main.js`
> + **`templates/index.json`** + **`templates/page.our-story.json`**。
> 新基线 **`baseline-20260908-0953`**（624 文件）。
>
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

---

> 状态：**第一一二轮（2026-09-08）—— promo 弹窗三条，`$build` = `20260908-r112`，已推 live**。
> 只推 3 个 asset（`customstyle.scss` + `.css` + **`main.js`**），零 liquid、零 template。
> 三方对比 ours 3 / theirs 1（`templates/index.json`，红线）/ **CONFLICT 0**。
> 新基线 **`baseline-20260908-0919`**（624 文件）。
>
> 1. `.gb-promo-panel__logo` 补 `img` —— 线上 `settings.logo` 已上传，`gb-logo.liquid`
>    渲染的是 `<img width=124 height=32>`，只写 `svg` 的规则管不到，把 24 高的行撑出 8px。
>    ⚠ **凡 `render 'gb-logo'` 处，选择器必须 `svg, img` 两个都写**（header / footer 早就这么写）。
> 2. `.h-captcha[data-size="invisible"] { position: absolute; }` —— 见下方「不要报成 bug」第 2 条。
> 3. 手机档 `.gb-promo-panel` 改 `overflow: hidden auto`，内容列的滚动收进 `panel-wide`。
>
> 判据：`tools/r112check.py` **49 ok / 0 red**（旧 CSS 上跑 **18 red**，不是恒真）；
> `tools/r112live.py --password 1234` 改前 **21 red**（三条 bug 线上全部复现）、推后 **75 ok / 0 red**；
> 回归 `r110check` 0 red、`r107check` 82/0、`r110live` 13/0、`r107live` 31/0。
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

---

> 状态：**第一一一轮（2026-09-08）—— footer social icons 补 `title`，`$build` 不变**。
> 只推 `sections/gb-footer.liquid` 一个文件，零 scss / 零 css / 零 js / 零 template。
> 新基线 **`baseline-20260908-0900`**（624 个文件）。
> 判据 `tools/socialtitle.py`（新）：静态站 36 + liquid 3 = **39 ok / 0 red**；
> 加 `--password 1234` 连线上渲染一起验 **42 ok / 0 red**；
> 负向对照（未改的 liquid）**36 ok / 3 red**，判据不是恒真。
>
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

---

> 状态：`$build` = **`20260908-r110`**（**第一一〇轮**，2026-09-08）—— 需求方七条，六条落地：
> 星星墨迹回到换图前 / `/collections/all` 手机端沟槽 / `.card-gallery` 去掉箭头与快加 /
> 口味列 370 以下一列 / 评论标题手机端单行省略 / 手风琴 0.3s→0.45s。
> **只推 2 个 asset**（`customstyle.scss`+`.css`），零 liquid、零 template、零 `main.js`。
> 已推 live，三方对比 **theirs 0 / CONFLICT 0**。
>
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

---

> 状态：`$build` = **`20260908-r108`**（**第一〇九轮**，2026-09-08）—— 需求方五条：
> 标题入场时序 1.4s→0.7s / 触摸端不再出焦点环 / 九处按压缩放全删 /
> 手机端 hero 波浪与 banner 重新贴合（线上专有）/ Shopify captcha 占位不再吃 gap。
> **只推 2 个 asset**（`customstyle.scss`+`.css`），零 liquid、零 template、零 `main.js`。
> 已推 live，新基线 **`baseline-r108/`**（**624** 个文件 —— 比下面那条的 623 新，
> 含并行会话的 JSON + 主题团队新加的 `gb-promo-modal.liquid`）。
>
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

---

> 状态：**第一〇八轮（2026-09-08）—— JSON 数据轮，`$build` 不变**。补齐线上全部缺失的波浪
> + `star.svg` 换设计稿图。**零 css / 零 js / 零 liquid**（同时段并行会话在做 r107 的 scss）。
> 已推 live，14 个文件，新基线 **`baseline-20260908-0800`**（623 个文件）。
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

---

> 状态：`$build` = **`20260908-r107`**（第一〇七轮，2026-09-08）—— 需求方四条：
> `gb-form__check` 去掉 hover 变色 / `gb-page-hero--center` 顶距回稿的 64 /
> `gb-product__tag` 收缩到文字宽 / `/404` 的 product-list 接入站点沟槽。
> **只推 2 个 asset**（`customstyle.scss`+`.css`），零 liquid、零 template、零 `main.js`。
> 已推 live，新基线 **`baseline-r107/`**（623 个文件）。
> 判据 `tools/r107check.py` 82/0（静态）+ `tools/r107live.py --password 1234` 31/0（线上）。
>
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

---

> 状态：`$build` = **`20260908-r106`**（第一〇六轮，2026-09-08）—— 需求方十条：
> hero padding / 留言框滚轮 / 表单三处颜色 / 下拉补勾 / 导航卡插画回稿 / 购物车缩略图 /
> `/collections/all` 接入站点风格 / **`--edge-top` 波浪的预留补洞**。
> 只推了 3 个 asset（`customstyle.scss`+`.css`+`main.js`），零 liquid、零 template。
> 已推 live，新基线 **`baseline-r106/`**（623 个文件）。
>
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

---

> 状态：`$build` = **`20260908-r97`**（第九十八轮，2026-09-08）—— 评论分页交给线上。
> **已推 live**（三个文件：`assets/customstyle.css` / `.scss` / **`main.js`**）。**没推任何 liquid。**
> 回读 **617 → 617**、三个逐字节相同、**614 个清单外文件零改动**。新基线 **`baseline-r97`**。
> 判据 **`tools/r96live.py --password 1234`**：推前 **101 ok / 1 red** → 推后 **107 ok / 0 red**，
> `--strip` 41 红。静态 `r96check` 136 ok、`crevcheck` 全绿、`crevlive` 30 ok，其余回归全绿。
>
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

---

> 状态：`$build` = **`20260908-r96`**（第九十七轮，2026-09-08）—— 对话 7 条 + tight 卡片 margin-top。
> **已推 live**（2026-09-08，两个文件：`assets/customstyle.css` / `.scss`）。
> **`main.js` 按需求方指示不推；本轮没有推任何 liquid。**
> 回读 **617 → 617**、我推的两个逐字节相同、线上 `--build` 已是 `20260908-r96`。
> 新基线 **`baseline-r96`（617 文件）**。
> 判据 **`tools/r96live.py --password 1234`**：推前 **63 ok / 39 red** → 推后 **102 ok / 0 red**，
> `--strip` 反向 41 红。静态 `tools/r96check.py` **141 ok / 0 red**、`--strip` 64 红。
> 回归 `crevlive`(30) / `rwd` / `r86check` / `r87check` / `r89check` / `crevcheck` / `r94check`(42) 全绿。
>
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

---

> 状态：`$build` = **`20260908-r95`**（第九十六轮，2026-09-08）—— 线上星星被撑成 1500px。
> **已推 live**（2026-09-08，两个文件：`assets/customstyle.css` / `.scss`）。
> 回读 **617 → 617**、逐字节相同、**615 个清单外文件零改动**。新基线 **`baseline-r95`（617 文件）**。
> 判据 **`tools/crevlive.py --password 1234`**：推前 **9 ok / 21 red**、推后 **30 ok / 0 red**、
> `--strip` 反向 21 红。回归 `crevcheck` / `r94check`(42) / `rwd.py` 全绿。
>
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

---

> 状态：`$build` = **`20260908-r94`**（第九十五轮，2026-09-08）—— product 顶距反转、
> vs 卡片底距下限、header 两菜单上线。
> **已推 live**（2026-09-08，三个文件：`assets/customstyle.css` / `.scss` /
> `sections/gb-header.liquid`；liquid 经需求方明确授权，分两步推、先 CSS 后 liquid）。
> 回读 **617 → 617**、三个文件逐字节相同、**614 个清单外文件零改动**。新基线 **`baseline-r94`（617 文件）**。
> 判据 **`tools/r94check.py`**：静态 **42 ok / 0 red**，`--as-served` 线上 **20 ok / 0 red**；
> `--strip` 反向 **21 红**且精确落在两处修复各自的档内。
> 回归 `rwd.py` / `r91` / `r92` / `r93`(81) / `crevcheck` / `r52`(385) / `r53`(249) 全绿。
>
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

---

> 状态：`$build` = **`20260907-r93`**（第九十四轮，2026-09-07）—— compare 头像/图标对齐、
> expert 卡等高、hero media 淡入（只改 live）。
> **已推 live**（2026-09-07，三个文件：`assets/customstyle.css` / `.scss` /
> `sections/gb-page-hero.liquid`；liquid 经需求方明确授权，分两步推、先 CSS 后 liquid）。
> 推前 `prepush-20260907-1623` 与 `baseline-r92` **零差异**；回读 **616 → 616**、
> 三个文件逐字节相同、**613 个清单外文件零改动**。新基线 **`baseline-r93`（616 文件）**。
> 判据 **`tools/r93check.py`**：静态 **81 ok / 0 red**，`--as-served` 线上 **76 ok / 0 red**；
> `--strip` 反向 **22 红**且精确落在两个修复各自的档内。
> 回归 `rwd.py` 全绿 / `r52`(385) / `r53`(249) / `crevcheck` 全绿。
>
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

---

> 状态：`$build` = **`20260907-r92`**（第九十三轮，2026-09-07）—— vs 品牌行美术件不再压文字、
> `/404` 换主题字体、`product-list` 底距。
> **已推 live**（2026-09-07，三个文件：`assets/customstyle.css` / `.scss` / `sections/main-404.liquid`）。
> 回读 **616 → 616**、三个文件逐字节相同、613 个清单外文件零改动。新基线 **`baseline-r92`**。
> 判据 **`tools/r92check.py`**：静态 14 档全绿；`--as-served` 推前 17 红、推后**全绿**。
>
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

---

> 状态：`$build` = **`20260907-r91`**（第九十二轮，2026-09-07）—— promo 还原静态站 + vs 表格对齐。
> **已推 live**（2026-09-07，三个文件：`assets/customstyle.css` / `.scss` / `sections/gb-promo.liquid`）。
> 回读 **616 → 616**、三个文件逐字节相同、613 个清单外文件零改动。新基线 **`baseline-r91`**。
> 判据 **`tools/r91check.py`**（静态 11 档 / 线上 5 档）：`--as-served` 推前 33 红、推后**全绿**。
> 六件事：`__media` 图 `cover`→`contain`、绿卡的弧隐藏、绿卡 `__main` restate `__stack` 的节奏、
> 手机端横向波浪用 `::after` + `$mask-promo-lip-h` 重建、`--vs-label-w` 给 label 列一个 floor、
> 浅绿卡与 logo 的 `left` 改从 label 列推导、pile 的手机值从 `stack` 搬回 `narrow`。
>
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

---

> 状态：`$build` = **`20260907-r90`**（第九十轮，2026-09-07）—— 评论卡四处改造：
> 星级拆成 `<img>`、附件放小熊占位、More/Less 分页、4.76 补上 r89 漏掉的 `$c-lime` 描边。
> **未推 live**（`gb-app-section` 线上仍没有 liquid，推 css 也渲染不出来）。
> 判据 **`tools/crevcheck.py`**：正向全绿、`--strip` 反向 68 红；`rwd.py` 两页全绿。
> 逐条与「别报成 bug」在 **1u**。
> ⚠ **判据从 `r89check.py` 改名成 `crevcheck.py`** —— 另一个会话同日也做了 r89 并
> **覆盖了那个文件**。gb-crev 的判据从此按模块命名、不带轮次号，别再改回去。
> ⚠ **`$build` 一天之内被两个会话各推进过一次**（我 r88 → 它 r89 → 我 r90）。
> 动 token 前先 `grep '\$build' assets/customstyle.scss`，别按记忆推断。

---

> 状态：`$build` = **`20260907-r89`**（第八十八～八十九轮，2026-09-07，**已推 live**）。
> 推的是 `assets/customstyle.css` / `.scss` 两个。回读 **616 → 616**、逐字节相同、
> **614 个清单外文件零改动**。新基线 **`baseline-r89`（616 文件）**。
> `r88check` / `r89check` 的 `--as-served` 推前 12 红 / 6 红，推后**全部全绿**。
> 四件事：collection 页底距 32→120/64（照 `.gb-rich-page`，顺带解决小熊压产品名）、
> `.gb-product` 顶距三档拉平到 32、`--lg` 显式写回 96/52/fluid、
> promo 绿卡的波浪咬痕改用 `__body::before` + mask 重建。
>
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

---

> 状态：`$build` = **`20260904-r68`**（第六十八轮：板底波浪的 0.5px 舍入），
> 已编译，**已推上 live**（2026-09-04 推的 css / scss / main.js 三个文件；
> 回读逐字节相同、`fill/59px`+`fill/40px` 各 1 处、文件数 586 → 586 零误伤）。
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

---

> 状态：`$build` = **`20260907-r76`**（第七十六轮，2026-09-07），**已推 live**：
> 订阅下拉**退回原生控件**（需求方要求，只 restyle 闭合态，下拉列表交回浏览器）；
> **faq 与 footer 交界那条波浪补回 mint 顶**（线上 setting 填的是 `to-lime`，上半透明，
> mint 在波浪处断成白色）。回读 590 → 590、逐字节相同、587 个未推文件零改动；
> `tools/r73check.py --password 1234 --as-served` **54 ok / 0 FAIL**。
> 新基线 `baseline-r76/`。
> ✅ **对方已经把购物车抽屉做完了**（`snippets/gb-cart-drawer.liquid` +
> `gb-cart-line-item.liquid` + `gb-cart-scripts.liquid`，2026-09-07 加的）——
> Gumi 的整套 `.gb-cart*` 类名原样搬进了 Horizon 的
> `<theme-drawer>` → `<dialog>` → `cart-drawer-component` → `cart-items-component`，
> 所以我们的样式够得着。**[LIVE-GAP.md](LIVE-GAP.md) 第四节的「购物车没做」已过时。**

---

> 状态：`$build` = **`20260907-r88`** —— 第八十八轮（collection 页底距）与**第八十九轮
> （Real Customer Reviews）共用同一个 token**：两轮由两个并行会话同时在做，r88 先提的 token。
> **两轮都还没推 live。**
> ✅ **Real Customer Reviews 做成了真前端**（`reviews.html` + `pdp.html`）——
> 原本划归评论 app 的「实现边界」按需求方要求推翻，四份稿（reviews / pdp 各两档）是
> 同一个组件，两页共用一份实现。判据 `tools/crevcheck.py`（r90 改名，原名被并行会话占了）：正向 **68 绿**、
> `--strip` 反向 **60 红**（把 `.gb-crev` 规则剥掉再注入，证明判据读的是本轮的规则）；
> `tools/rwd.py` 两页全绿。逐条与「别报成 bug」在 **1t**。
> ⚠ **线上没有 `gb-app-section` 的 liquid** —— 这块目前只活在静态站，上线要对方补 section。
> ⚠ **同目录另有一个 Claude 会话在做 r88**（`tools/r88check.py`，以及 scss 末尾的
> `.gb-page-wrapper .product-grid-container`）。两边的改动都在，但**推送前必须重跑三方对比**。

---

> 状态：`$build` = **`20260907-r87`**（第八十七轮，2026-09-07，**已推 live**）。
> 推的是 `assets/customstyle.css` / `.scss` + **`snippets/gb-logo.liquid`**（r85 欠的那条）。
> 回读 **616 → 616**、三个文件逐字节相同、613 个清单外文件零改动。
> 新基线 **`baseline-r87/`（616 文件）**。`r85check` / `r86check` / `r87check` 三份
> `--as-served` **全部全绿** —— logo 那 18 条 `PEND` 随本次推送转绿，2x 屏碎图已修。
> ⚠ **对方把 PDP 拆成了 9 个 block**（608 → 616：`gb-atc` / `gb-feature` / `gb-guarantee-note` /
> `gb-lead` / `gb-price` / `gb-rating` / `gb-subscription` / `gb-title` / `gb-variants`），
> 并重写了 `gb-features.liquid` / `gb-product.liquid` 与两个 template。
> **PDP 的卖点列表到这一刻仍然是空的**（`<ul class="gb-product__features"></ul>`）——
> 是对方的文件，我们没动。改 PDP 样式前**先看线上真实层级**。

---

> 状态：`$build` = **`20260907-r86`**（第八十六轮，2026-09-07，**已推 live**）。
> 需求方点名五处：features 位置 / 手机菜单开合时 header 消失 / 跑马灯 logo 再小 /
> 链接 hover 去下划线改变色 / 面板上边框只在打开时显示。**全部 CSS**，`main.js` 未动。
> 推的是 `assets/customstyle.css` / `.scss` 两个；回读逐字节相同。
> 新基线 **`baseline-r86/`（608 文件）**。判据 `r86check.py --as-served` 线上**全绿**（推前 30 红）。
> ✅ **锁滚动让 sticky header 消失的三处锁全部修完**（菜单 / 弹窗 / 购物车抽屉）：
> 锁只压 `html`，`body` 半边一律 `overflow-x: clip; overflow-y: visible`。
> ⚠ **不要"顺手统一"回 `overflow: hidden`** —— 那会让 body 变成 sticky 的 scrollport。
> ⚠ **PDP 卖点列表线上目前是空的**：对方在推送当天把 features 改成
> `{% content_for 'block', type: '_gb-features', id: 'features' %}`，父块渲染了、
> 内部的 `{% content_for 'blocks' %}` 没带出来。**是对方的文件，我们没动。**
> ⚠ **`div.shopify-block` 在 PDP 上回来了**（`{% content_for 'blocks' %}` 给每个 block
> 套一层），下面那句「全站 0 处」对 PDP 已过时 —— 写 `>` 选择器前先看线上真实层级。
> ⚠ 跑马灯的 **88×36 是我们选的数，不是稿上的**（这块只有桌面稿），且这一档因此比原来慢约 13%。

---

> 状态：`$build` = **`20260907-r85`**（第八十五轮，2026-09-07，**已推 live**）。
> 需求方点名九处：thumb 焦点态 / guarantee 图标 / 订阅卡描边 / footer 分隔线 /
> 面板上边框 / 面板列对齐 / logo 换 `<img>` / 抽屉卡插画宽 / reels 装得下就居中不滚。
> 推的是 `assets/customstyle.css` / `.scss` / `main.js` 三个；回读 607 → 607、逐字节相同、
> 604 个清单外文件零改动。新基线 **`baseline-r85/`（607 文件）**。
> 判据 `tools/r85check.py --as-served` 线上**全绿**（推之前同一判据 66 红）。
> ⚠ **`snippets/gb-logo.liquid` 仍未推**（需单独授权，改法在 `liquid/` + `work-r85/`）——
> 线上三处 logo 还是 `src="0"`，**1x 屏能看、2x 屏碎图**；判据里那 18 条 `PEND` 就是它。
> ⚠ 三方对比：线上自 r84 起只有对方改的 `sections/gb-nutrition.liquid`
> （加了 `scallop_variant` 下拉 = STYLE-GAP 的 **C5**，对方自行落地），**我们的 3 个文件零冲突**。
> ⚠ **本轮同目录还有另一个 Claude 会话在跑 account 页**（提交 `29a7638`、
> `account.html` + `assets/account.*` + `tools/acct*.py`）。`account.scss` 是独立入口、
> 自带 `?v=…-a1`，不依赖 `customstyle.scss`；我的 `?v=` 批量替换顺带把 `account.html`
> 的 4 处 r84 换成了 r85（那页确实加载 `customstyle.css`）。**推送前必须重跑三方对比。**

---

> 状态：`$build` = **`20260907-r84`**（第八十四轮，2026-09-07，**已推 live**）。
> 推的是 `assets/customstyle.css` / `.scss` 两个文件；回读 607 → 607、逐字节相同、
> 605 个清单外文件零改动；`r84check.py --as-served` 线上两档全绿（推之前同一判据 19 红）。
> 新基线 **`baseline-r84/`（607 文件）**。
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

---

> 状态：`$build` = **`20260907-r83`**（第八十三轮，2026-09-07，**已推 live**）。
> `.gb-science__title` 收窄到 660 并居中、`.gb-science-card__text` 去掉 6px 顶距。
> ⚠ **`margin: 0 auto` 会压过手机端的 `align-items: flex-start`** —— narrow 块里那句
> `margin: 0` 是承重的，删了手机端标题就会居中，而稿里（`228:8166`）是左对齐。
> ℹ `max-width: 660` **只在首页咬得住**：`/pages/science` 的标题在所有档都填满 `__head`，
> 原值 1072 同理也从未生效过。
> 判据 `tools/r83check.py`：线上 `--as-served` 全过 + 2 条明确跳过。
> 新基线 **`baseline-r83/`（607 文件）**。

---

> 状态：`$build` = **`20260907-r82`**（第八十二轮，2026-09-07，**已推 live**）。
> 本次推送**同时带上了 r81 与 r82 两轮** —— 线上此前停在 r80（r81 改完等指令时未推）。
> **r81**：`.gb-product__image` / `__thumb` 的图改 `object-fit: contain`（**推翻 r64 的 cover**，
> 灰底会露成 letterbox，是有意的）；并查清了 nutrition/product 交界波浪的消失原因。
> **r82**：reel 的 focus 环撤掉、改为镜像 hover 的 `scale(1.06)`（**推翻 r78 的 `::after` 环**）；
> `gb-stats__title` / `gb-nutrition__title` 里 richtext 带来的 `<p>` 补上 `font: inherit`。
> ⚠ **本轮未推任何 liquid**（需求方明确「先不推 liquid」）。
> ⚠ **波浪仍未修**：`gb-nutrition → gb-product` 交界的那条**线上从来没有输出过**，
> 是结构缺失不是配色错，**CSS 补不出来**，逐条证据见 CHANGELOG 第八十一轮第 2 节。
> 判据 `tools/r82check.py` / `r81check.py`：线上 `--as-served` 双双全过。
> 新基线 **`baseline-r82/`（607 文件）**。

---

> 状态：`$build` = **`20260907-r80`**（第八十轮，2026-09-07，**已推 live**）。
> `.gb-product__packed-item` 与 `.gb-product__taste-item` 的图标规则从 `svg` 扩到 `svg, img`：
> 对方把占位圆圈换成了 `image_picker`，而 **HTML 的 width/height 属性只给宽高比不给尺寸**，
> 线上图标因此按固有尺寸渲染 —— packed **171×161**（板 34×32）、taste **106×100**（板 51×48）。
> ⚠ **`.gb-product__guarantee` 是同一个病，本轮未修**（需求方只点名了 packed 与 taste）——
> 它在 **5 个页面**上（`index` / `pdp` / `our-story` / `how-gumi-works` / `reviews`），
> 影响面比这两个都大。`r80check.py` 每轮打印它的尺寸但不断言。
> ⚠ 它不在 PDP 的 packed 区域内，**线上探针在 PDP 上测不到它**，要验得换页面。
> 判据 `tools/r80check.py`：线上 `--as-served` 全过；推送前同一判据 4 红（双向）。
> 回读 607 → 607、逐字节相同、605 个清单外文件零改动。新基线 **`baseline-r80/`**。
> 探针 `tools/r80probe.py` 可复跑，一次量出三处图标行的静态站 / 线上对照。

---

> 状态：`$build` = **`20260907-r79`**（第七十九轮，2026-09-07，**已推 live**）。
> 关掉了第七十七轮登记的两条待裁决 **BH / BI**：购物车抽屉的退场跑满稿的 0.7s
> （原来被 Horizon 切在 0.125s）、桌面端打开抽屉锁住背后的页面（原来 ≥990 不锁）。
> **两条是耦合的**：退场拉长后，Horizon 提前解锁造成的横向跳从看不见变成必然可见。
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

---

> 状态：`$build` = **`20260907-r78`**（第七十八轮，2026-09-07，**已推 live**）：
> reel 的 focus 环改用 `::after` 画在卡内（原来被 swiper 裁掉上下两条）、
> footer 的 focus 环改跟文字色（原来深绿描深绿等于没有）、
> header CTA padding 42 → 40（**只改 `.gb-header__cta`，基类不动**）。
> 判据 `tools/r78check.py` 32 条全过。
> 推送含第七十七轮的 cart-drawer 改动（2 个 css 文件）；回读逐字节相同、零删除；
> 线上实测 12 条新选择器全部解析、reel 环四边像素命中。新基线 `baseline-r78/`（603 文件）。
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

---

> 状态：`$build` = `20260907-r73`（第七十三轮，2026-09-07），**CSS 已推 live**：
> header 吸顶在线上被 Shopify 包裹层吃掉（`display: contents` 撤掉两层 wrapper 盒）、
> PDP gallery 贴合 header（104→80）、cta 补 20px 间距、去掉全站按钮的按压下沉。
> 回读 587 → 587、逐字节相同、585 个未推文件零改动；
> **线上真实效果 `tools/r73check.py --password 1234 --as-served` 30 条全过**。
> 新基线 `Gumi-Brand-shopify/baseline-r73/`。
> ⚠ **`main.js` 本轮没改也没推** —— 三方对比里本地/线上/基线逐字节相同，不是漏推。
> ⚠ **第 3 条 `gb-sub__select` 的 liquid 按需求方指示未推**：`snippets/gb-sub.liquid`
> 补 `data-select` 已改好验过，在 `liquid/snippets/` 与 `liquid/r73.patch`，
> 工作副本 `work-r73/`。**在推之前线上那个下拉一直是原生控件，别报成 bug。**
> ⚠ **对方 2026-09-04 之后启用了 Horizon 原生购物车抽屉**（`theme.liquid` 放开
> `{% render 'cart-drawer' %}`、`settings_data.json` 加 `auto_open_cart_drawer: true`）——
> 与我们的 `.gb-cart` 是两条路线。这是三方对比里唯一的线上改动，我方三个 assets 未被动过。

---

## 过期的工作区状态（第七十七～八十三轮末）

## 八、工作区状态（第八十三轮末，2026-09-07 更新）

- **第八十三轮已推**（2026-09-07，2 个文件：`customstyle.css` / `.scss`）。
  **新基线 `baseline-r83/`（607 文件）**，push/prepush 快照已删。
  回读 607 → 607、两个文件逐字节相同。
- ⚠ **回读时清单外有 2 个 JSON 变动，是对方同期在后台改的，不是误伤**：
  `templates/index.json`（文案补空格 + 一个 section 设 `disabled: true`）、
  `sections/header-group.json`（格式化后语义零差异）。
  **归属判据**：这类改动只有 Online Store Editor 能做，而我方推送清单里从来没有任何 JSON。
  下次再看到 JSON 出现在回读差异里，先按这条判，别怀疑推送。
- ⚠ **判据的"期望值"要断言机制，不要硬编码结论**。本轮 `r83check` 连错两次：
  先是用「左右空隙相等」判居中，而满宽的标题 `gapL == gapR == 0` 也满足；
  再是给每个页面硬编码了该居中还是该左对齐。
  改成：手机档验三个锚点（`gapL < 2` + `margin-left: 0px` + `align-items: flex-start`），
  桌面档若标题本来就满宽则**明确 SKIP 并打印原因**。
- ⚠ **仍未处理**：`.gb-product__guarantee` 的图标尺寸（5 个页面）、
  `gb-nutrition → gb-product` 的交界波浪（需对方加 liquid，且要支持 `--bleed`）。
  `docs/LIVE-GAP.md` 仍是过时的。

## 八之二、第八十二轮末的工作区状态

- **第八十一 + 八十二轮已推**（2026-09-07，2 个文件：`customstyle.css` / `.scss`）。
  **新基线 `baseline-r82/`（607 文件）**，`push-r82/` 与 prepush 快照已删。
  回读 607 → 607、逐字节相同、605 个清单外文件零改动。`main.js` 三方一致，未列清单。
- ⚠ **推之前一定要看线上的 build token 是哪一轮**：本次就发现线上停在 r80
  （r81 改完等指令时没推），于是一次推送带了两轮的改动。
  **「上一轮推过了」不能凭记忆断定**，`diff` 里的 build token 就是答案。
- ⚠ **判据绑死具体取值已经坑了五次**（r77check 绑 `--animation-speed`、
  r78check / r73check 绑 `$build`、r64check 绑 `object-fit: cover`、r78check 绑 reel 环）。
  **写判据时凡是"客户可能反转的取值"，都按 key 区分或只断言不变契约**，
  把具体形式交给当轮的判据。
- ⚠ **仍未处理**：`.gb-product__guarantee` 的图标尺寸（同 packed/taste 的病，在 5 个页面上）、
  `gb-nutrition → gb-product` 的交界波浪（需对方加 liquid）。
  两条都在「不要报成 bug」的 1m / 1n 里登记着，判据会打印但不断言。
- ⚠ **`docs/LIVE-GAP.md` 仍是过时的** —— 对方在 r79 之后陆续补了
  `gb-promo` / `gb-vs` / `gb-app-section` / `gb-nl-modal` 四个 liquid，还在给
  `gb-product` 加营养标签的 metaobject fallback。**需要重新核一遍。**

## 八之二、第八十轮末的工作区状态

- **第八十轮已推**（2026-09-07，2 个文件：`customstyle.css` / `.scss`）。
  **新基线 `baseline-r80/`（607 文件）**，`push-r80/` 与 prepush 快照已删。
  `main.js` 本轮未改，三方逐字节相同，未列进清单。
  ⚠ 对方这期间只改了 `templates/index.json`（Online Store Editor 托管，**绝不推**）。
- ⚠ **对方在 r79 推送当天补了 4 个 liquid**（`sections/gb-promo` / `gb-vs` /
  `gb-app-section`、`snippets/gb-nl-modal`）并改了 `sections/gb-product.liquid` ——
  **`docs/LIVE-GAP.md` 已经过时，需要重新核一遍**。
- ⚠ **图标从占位 `<svg>` 换成 `<img>` 这件事还没做完**：`packed` 本轮修了，
  **`taste` 与 `guarantee` 仍是坏的**（线上 taste 实测 106×100，板值 51×48）。
  需求只点名 packed，按铁律 20 没有擅自动 —— 等需求方拍板。
- ⚠ **别再把「liquid 里写了 `image_url: width: 80` / `width="34"`」当成尺寸约束**：
  前者不决定固有尺寸（实测出图 171 宽），后者只声明宽高比。**CSS 必须自己给宽高。**

## 八之二、第七十九轮末的工作区状态

- **第七十九轮已推**（2026-09-07，3 个文件：`customstyle.css` / `.scss` / **`main.js`**）。
  **新基线 `baseline-r79/`（607 文件）**，`push-r79/` 与 prepush 快照已删。
  回读 607 → 607、逐字节相同、604 个清单外文件零改动。
  ⚠ **`main.js` 这轮真的改了**（新增 `scrollbarProbe`）—— r73/r77 那句「main.js 与线上
  逐字节相同、不用列进清单」**对这一轮不适用**。
  ⚠ **对方同期推了 7 项**（4 个新 liquid + `gb-product.liquid` + 两个 templates json），
  没有一项在我们的清单里。那 4 个新 section 正是 LIVE-GAP 登记的缺口，
  **该文档需要重新核一遍**。
- **BH / BI 已关闭**，PROJECT-STATUS 里两条对应条目已标结案。剩下 **BJ / BK** 仍待裁决。
- **判据 `tools/r79check.py`** —— 离线 39 条（产物 23 + main.js 7 + 静态站 9）+ 线上 16 条。
  `--password 1234` 全过、1 条明确跳过；**`--as-served` 应 8 红**，那是"线上还没推"的正确答案，
  也是这个判据不恒真的证明。
- ⚠ **三个旧判据本轮修过，都是判据自己的毛病不是实现回归**：
  `r78check` / `r73check` 把 `$build` 断言写成 `==` 当轮 token（每轮必假红，改成 `>=`，
  r77check 早就是这个写法了）；`r77check` 的四条动画断言绑死了
  `var(--animation-speed`，本轮时长换成 `$t-drawer` 后报红 ——
  改成只验「相位类驱动我们的关键帧」，**时长归 r79check 管**。
- ⚠ **写线上探针时两个必踩的坑**（本轮都栽过一次）：
  ① **测点要落在变化区间内** —— `animationDuration` 在 open 后等 1000ms 才读，
  那时动画早跑完、`--opening` 已被摘掉，读到的是 `0s`。要在 rAF 双帧内采样，
  并加一条「采样时相位类还在」的锚点断言。
  ② **顶替 css 时 `main.js` 也要一起顶替** —— 只顶 css 的话，线上跑的还是没有
  `scrollbarProbe` 的旧 js，`--scrollbar-w` 两侧都缺席，**断言自洽地绿着却什么都没验**。
  现在有 `scrollbarProbe is live (anchor)` 兜底。
- ⚠ **`--scrollbar-w` 的真实补偿本机验不了**：headless chromium 没有屏幕滚动条，
  `innerWidth - clientWidth` 恒 0。判据把这条 **SKIP 并打印**，改用**合成 15px**
  验 CSS 机制是否响应。**真实宽度下的效果须真机 / 真浏览器确认。**

## 八之二、上一轮的工作区状态（第七十七轮末）

- **第七十七 + 七十八轮已推**（2026-09-07，`assets/customstyle.css` / `.scss` 两个文件）。
  **新基线 `baseline-r78/`（603 文件）**，`push-r78/` 已删。
  ⚠ 回读时文件数 593 → 603、清单外 12 个文件变动 —— **对方同期推的，不是误伤**。
  归属判据：新文件在**基线和推送前快照里都不存在**，而 `--only` 推送不可能创建文件。
  ⚠ **验线上别用非指纹的 `/cdn/shop/t/2/assets/customstyle.css`** —— 实测它回的是
  `20260907-r73` 的旧缓存，跟主题里的实际文件差了好几轮。要么走页面引用的 `?v=<digest>`
  指纹 URL，要么直接在浏览器里读已解析的规则与计算值。
  ⚠ **CSSOM 遍历别写 `if (r.cssRules) { walk(...); continue; }`** ——
  Chrome 的 `CSSStyleRule` 也带 `cssRules`（嵌套 CSS），这么写会把每条样式规则当容器跳过，
  命中数恒 0。见 memory `cssom-stylerule-has-cssrules`。
- ⚠ **（历史）线上曾走在 `baseline-r76` 前面**（2026-09-07 05:02 拉的
  `live-20260907-r77check/`，593 文件 vs 基线 590）：新增
  `snippets/gb-cart-empty.liquid` + `assets/nav-card-bear.png/.webp`，改动
  `gb-cart-drawer` / `gb-cart-line-item` / `gb-cart-scripts` / `gb-head` /
  `sections/gb-product.liquid` / `config/settings_data.json` / `settings_schema.json`。
  **`assets/customstyle.*` 零差异**（线上仍是 r76），本轮推送清单不冲突 ——
  但**推之前仍要重拉一次做三方对比**，这个店一天能变四五次。
  逐条 diff 与对 r77 的影响分析见 CHANGELOG 第七十七轮「复查」。
- **第七十七轮（cart-drawer）—— 需求方当时说「暂不先修改 cart 相关的样式，只做记录，稍后推」，
  随后在第七十八轮一并推出。已上线。**
  **推送前核算过一次**（对 `live-20260907-r77check/`）：
  `assets/main.js` 与线上**逐字节相同**（不列进清单）；
  `customstyle.css` 差 103 行，剔掉 30 行 build token 后剩 **73 行，全部是新增**，
  `diff` 里**没有一条 `<`** —— 即没有误删线上任何既有规则。
  新增部分正好是 8 条规则 + 2 组 keyframes：`#cart-drawer .theme-drawer__dialog`
  （含 `::backdrop` / `--opening` / `--closing`）、`gb-cart-scrim` / `gb-cart-slide`、
  `.gb-cart-item__stepper input.gb-cart-item__count`（含 spin-button 伪元素）、
  `select.gb-cart-item__interval:not(.gb-select__native)`（含 hover）。
  ⚠ 真推的时候**仍要重拉一次做三方对比**，这个快照是 05:02 的。
- **第七十七轮（cart-drawer）已随第七十八轮推出**（`assets/customstyle.css` / `.scss`）。
  判据 `tools/r77check.py`
  （55 过 / 0 红 / **7 条明确跳过**；线上半段要 `--password 1234`，加 `--as-served` 才是真状态。
  跳过的 7 条全是需要购物车有货的行项目尺寸，见下面 Cloudflare 那条）。
  线上半段用 **`page.route` 顶替 `customstyle.css`**，不是 `add_style_tag` 追加 ——
  追加的规则在同权重时凭顺序必胜，会把判据打得比浏览器实际更宽松。
- ⚠⚠ **`gumi.com.au` 在 Cloudflare 托管挑战后面，触发器是 `/cart/*` 这个路径本身**。
  首页 200 一切正常，一请求 `/cart/<variant>:<qty>` 或 `/cart/add.js` 就跳
  `?__cf_chl_rt_tk=…` +「Verifying your connection...」，**之后连首页都变成
  「Just a moment...」，整个会话报废**，退避半小时也不一定解。
  `/products.json` 和 `/password` 打多了同样会累积到 429 / 503。
  **写线上探针一律不要碰 `/cart/*`** —— 新开 context 本来就是空车，
  空车态足够验 dialog 几何 / 层级 / 遮罩 / `::backdrop` / 关闭路径 / 空态文案 / 手机档模态性。
  真要有货用 `r77check.py --fill`，**它会踩挑战，跑完这个 IP 得歇一阵**。
- ⚠ **429/503 不等于密码错**。`r77check.py` 起初把它报成
  「storefront password rejected」，第二处又报成「variant may be gone」——
  **两个都是假诊断，会把人支去查密码和商品目录**。现已分开识别。
  `/products.json` 也不再每轮去打，variant id 写死在判据里。
- **判据自己会挑错测点**：390 档「点遮罩关闭」曾报红，真因是
  **那档面板满宽、根本没有露出来的遮罩**，坐标落在面板上。
  改成点关闭按钮，遮罩点击移到 900 档验。**报红先怀疑判据**。
- **线上探针的三条写法**：`page.route` 顶替 css 而不是 `add_style_tag` 追加
  （追加的规则同权重必胜，判得比浏览器宽松）；一个 context + 一个页面 +
  `set_viewport_size` 走三档（少一次导航就少一次挑战掷骰，还顺带跑了
  Horizon 的 `#onModalBreakpointChange`）；`skip()` 单独计数并在结尾列名，
  **跳过必须响**，`sys.exit` 只看 FAIL。
- ⚠ **`cd <目录> && cmd` 会一直留在那个目录里**（Bash 工具跨调用保留 cwd）。
  本轮 `cd .../baseline-r76 && grep ...` 之后，随后几条命令的 `assets/customstyle.scss`
  全落在**基线目录**上：先是 grep 报「改动没了」，接着 `npx sass` 把基线的 scss
  重编译进了**基线的 css**。这次没造成损坏（产出字节与 `live-20260907-0224-after-r76/`
  的独立快照一致，md5 `6d7f4f3a…`），但换个场景就是把快照写坏。
  **进快照/基线目录一律用绝对路径，别用裸 `cd`。**

- **第七十六轮已推**（`customstyle.css` / `.scss` / `main.js`），新基线 `baseline-r76/`（590 文件）。
  ⚠ **对方 2026-09-07 当天改过线上四次**（启用原生 cart-drawer → 改 `gb-header.liquid`
  接上触发器 → 新增三个 `gb-cart-*.liquid` → 改 `gb-product.liquid` 的加购逻辑）。
  **每次推送前都必须重新 `theme pull` 做三方对比**，这一天里没有一次快照能重用。
- ⚠ **验证线上 CSS 的判据必须用压缩形式，而且「压缩」不是全局的**：
  选择器里的空格会被去掉（`:has(>.shopify-section...)`），
  但**自定义属性的值保留空格**（`--wave-bg: #e7f8d0`）。这一天在这上面栽了两次。
  更稳的写法是**比对「线上命中数 == 本地源命中数」**，不写死期望字符串。
- **第七十三轮：CSS 已推（2 个文件），liquid 未推（需求方指示）**。
  `$build` = **`20260907-r73`**（两次 md5 `676fba65…`）。新基线 `baseline-r73/`（587 文件）。
  待推的只剩 `snippets/gb-sub.liquid`（补 `data-select`），推它需逐次授权。
- ⚠ **`main.js` 已经和线上一致**（本地/线上/基线逐字节相同），除非真改了它，否则不用列进推送清单。
- **推送副本的做法值得沿用**：当只推部分改动时，从推送前快照复制一份干净副本、
  只放入要推的文件（本轮 `push-r73/`），与线上的差异应恰好等于推送清单 ——
  这样命令写错也推不出清单外的东西。推完即删。
- **本轮两条规则只在线上有匹配**（`#header-group` / `.gb-product__form`），
  静态站上零效果，见「一·1g」。
- **线上 header 吸顶失效的根因**是 sticky 被两层 Shopify 包裹盒约束（父盒高度 = header 高度）。
  诊断脚本 `tools/r73probe.py --password 1234 --url <page>` 打印任意元素的祖先链
  （position / top / overflow / 高度）+ 滚动前后的 rect，以后再遇到"本地对线上不对"的
  定位类问题先跑它。

- **第七十一轮已推 7 个 liquid**（5 个 section 走新 snippet 剥 richtext 外层 `<p>`、
  `gb-scripts` 三个脚本加 `defer`、新增 `snippets/gb-rich-inline.liquid`）。
  当前线上基线 `Gumi-Brand-shopify/baseline-r71/`（587 文件），判据 `tools/r71check.py` 21 条。
- ⚠ **线上探针可用了**：`python3 tools/liveprobe70.py --password 1234 --throttle`
  测 CLS、`.wowo` 与 `[data-line-reveal]` 的时序、`fonts.ready` / `window.gumi` 时刻。
  **密码不进仓库，走 CLI 参数。**
- ⚠ **`[data-line-reveal]` 与 `.wowo` 现在共用同一道 `html.js` 门**（第七十二轮补齐，
  此前只有 wowo 有门，这是两套机制长期不一致）。门脚本的兜底是 **10000ms**，
  **不要再调回 4000** —— main.js 在慢网络下要 3.6~4.3s 才 boot，4s 会提前误判成「脚本挂了」
  并摘掉门，文字于是先裸露再被拆行推走。
  放宽定时之所以安全，是因为 `defer` 保证 main.js 在 `load` 之前执行，
  `addEventListener("load", u)` 才是主信号，定时只防 load 永不触发。
  **改动这里必须重验降级路径**：`route('**/main.js*', abort)` 之后文字要仍然可见
  （实测 load 后 1.5s 就恢复，不用等 10s）。

- **`liquid/` 是第七十轮新建的目录**，放我们改过的线上 section（完整文件 + patch）。
  线上 liquid 由对方维护、本地没有源，改动只留在 `Gumi-Brand-shopify/` 的工作副本里
  会被下次 `theme pull` 冲掉 —— 所以进仓库留一份。约定见 `liquid/README.md`。
  ⚠ **绝不推 `templates/*.json` / `sections/*-group.json` / `config/settings_data.json`**：
  Online Store Editor 托管，推它们会覆盖对方在后台调的一切。第七十轮因此把
  footer 换行、page-hero 标题换行、四页挂 `gb-product` 全部推给了后台去做。
- **第七十轮推了 `gb-stats.liquid` + `gb-expert.liquid` 两个 liquid 到 live**，
  `gb-reviews.liquid`（法务免责声明）**改好了但未推**，在 `liquid/sections/` 与
  `work-r70/` 各一份。当前线上基线 `Gumi-Brand-shopify/baseline-r70/`。
  判据 `python3 tools/r70check.py <theme-dir>`，24 条：对 `work-r70` 应全过，
  对**线上**应 18 过 6 红（红的全是 disclaimer），对未改动的旧快照应有 16 条 FAIL。
- ⚠ **推 liquid 时日志会打 `Cleaning your remote theme`** —— 带 `--nodelete` 时它不删东西，
  第七十轮实测文件数 586 → 586、584 个未推文件零改动。**别被这句话吓到回滚**，
  但每次仍要回读比对，这句话本身不是证据。


- `$build` 历史（**跳过 r61**：那个号从没作为 token 存在过，
  而 `tools/r61check.py` 早被第五十九轮占用了这个名字。**r64 也从没被线上服务过** ——
  推上去当天就被第三方的 r58 覆盖了，见 CHANGELOG 第六十四轮）。全站 **129** 处 `?v=`（实测）：有轮播的 5 页各 12、
  其余 6 个交付页各 11、`font-check.html` 4。一条 `sed` 全换掉。
- ⚠ **验证仍不完整**：第五十五轮欠的那批里，`rwd.py` / `scrolllock` / `r53check`
  在第五十八、五十九轮都跑过（全绿）。**仍欠 `revealcheck` / `hardbreaks` /
  `platecheck` / `seamcheck` / `font-check.html` / 全站矩形波及比对** ——
  第五十八轮需求方明确说先不做。
- **`.gb-promo-panel` 从 768 起是双栏**，768–1109 靠 `zoom: var(--pp-k)` 整块等比缩
  （1110 是第一个能把 1062 塞进两个 24 gutter 的宽度）。`@include panel-wide` 块里的
  数**全是板值**，调这一档只能调 --pp-k。待决 AT 已关闭。
- **`selectBox` 现在有三个变体**：默认（询问类型，自带 44 高白盒）、`bare`（国家码，
  无盒子）、`inline`（cart 的 delivery interval，句子里的一段文字）。
  **列表放不下会加 `.is-up` 往上开**，判断在 `wouldOverflow()` 里 ——
  ⚠ 它刻意不读 list 自己的 rect（入场位移正在跑，会读到过渡起始值），
  也刻意排在 `move()` 之后（`scrollIntoView` 会滚动祖先）。
- **购物车抽屉 `.gb-cart`** 挂在 **11 个交付页**，靠 header 那个 `data-modal="gb-cart"`
  的图标打开。`font-check.html` 没有 header，因此也没有抽屉。
  两个状态由根元素的类切：没有 `.is-empty` = 有货，加上 `.is-empty` = 空车
  （与 `.is-open` 同为 0-2-0 状态类，两者可叠）。
  **预览空态就是在 devtools 里给 `#gb-cart` 加这个类**，没有 JS 会自己切。
- `assets/main.js` 仍是 **15 个模块**。⚠ **再加任何 `overflow-y:auto` 的容器都必须登记进
  `smoothScroll.PREVENT`**，否则 Lenis 吃掉滚轮、那个容器再也滚不动
  （`rwd.py` 的第 3 条判据会抓，`font-check.html` 里也有探针）。
- **`assets/bear-icon.png` / `.webp` 不在 `images/`**（第六十一轮移过去的）：
  `.gb-bear-meter__bear` 是全站唯一一处 CSS 写死的图片引用，原来写 `url("../images/…")`，
  在 `file://` 与静态主机上都对，但 Shopify 从 CDN 扁平地服务 `assets/`，
  样式表旁边没有 `images/` 可以 `../` 上去 —— 一上主题就 404，且是静默的（背景空掉不报错）。
  现在与字体同写法：裸文件名 + `?v=#{$build}`。
  **以后往 scss 里加任何 `url()` 都必须是 assets/ 内的裸文件名**，判据 `tools/assetpath.py`。
- `images/pay-*.svg` 五个是**导出件的原件**（与 `figma/assets-raw/icons/desktop-cart-payment-method-*.svg`
  逐字节相同），`r60check` 会验这一点。cart 的其余图标是内联 SVG，`d` 也逐字节来自导出件；
  interval 的箭头例外 —— 那是 `selectBox` 画的（与板上的 16 chevron 是同一个 vee）。
- **reels 的视频**（第六十二轮）：`.gb-reel` 上的 `data-video` 是行内属性，
  `modal.open(el, trigger)` 把它写进弹窗里的 `[data-modal-video]`。
  没有 `data-video` 的触发元素照旧显示灰底 + play 图标（靠弹窗上的 `has-video` 类）。
  ⚠ **`stopVideo` 必须留在 `close()` 开头**，挪进 `unlockAfter` 声音会多响一个淡出的时间；
  ⚠ **`playVideo` 必须在 `is-open` 之前**，否则先淡入一个空画面。
  `data-video` 既吃直链文件也吃 YouTube／Vimeo 链接：`playVideo()` 判断类型后
  **当场建节点**进 `[data-modal-media]`，HTML 里两个播放器一个都没有。
  ⚠ **关闭时节点整个移除** —— 对 iframe 这是唯一能停下第三方播放器的办法；
  ⚠ **状态类要等淡出结束才清**（`unlockAfter(ms, el)`）；
  ⚠ **`.has-video/.has-embed` 时容器底色压成 `$c-ink`** —— 节点在关闭瞬间就没了，
  不压底色那 0.28s 淡出里会闪出灰色占位底。三条互相牵制，改一条要一起看。
  `images/reel-1..4.mp4`、`reel-poster-1..5.jpg` 与卡 5 的 YouTube 链接
  **全是占位**，见「不要报成 bug」1c。
- ⚠ **Playwright 的 chromium 是靠一条符号链接找到的**：装到的是 `chromium-1208`，
  而 `tools/` 下 15 个脚本写死 `chromium-1217`，用
  `ln -sfn ~/.cache/ms-playwright/chromium-1208 ~/.cache/ms-playwright/chromium-1217` 对上。
  **这条链接不在仓库里，换机器要重建**，否则所有判据脚本一起失效。
  ⚠ 别把 `/snap/bin/chromium` 链过去 —— 那是 snap wrapper，不认 playwright 传的
  `--disable-field-trial-config`，会以 exit 64 失败。
- ⚠ **`<head>` 里那段内联脚本不能挪进 `main.js`**：它是 `.wowo{opacity:0}` 的存活门，
  一要在首帧之前挂上 `html.js`（否则 FOUC），二要在 `main.js` 死掉时撤门 ——
  而 `main.js` 死了就跑不到自己。见 [[reveal-gate-must-track-module-liveness]]。
- 五个页面**运行时**会多出 DOM 节点（`selectBox` 建出来的下拉）：11 个交付页各有 cart 的
  两个，`get-in-touch` 另加两个、`referral` 另加一个。
  `cssnap.py diff` 对这些页无效，用 `r42rect.py`。
- `images/favicon.svg` 是**生成物**（footer logo 的四条 path + 实测底色），
  **改 logo 就要重跑生成**（`r59check` 的「逐字节相同」会报红提醒）。
- `assets/swiper-bundle.min.js` 是 vendor 原件（Swiper 11.2.6，MIT，154KB），**不要改它**。
- **两条推送线互不相干，别互相推断**：
  - **git**：最后提交 `d6aec8c`（2026-08-31，第五十七轮 favicon），`origin/main` 与 HEAD 一致
    —— 已提交的都推过了。**第五十八～六十八轮共 11 轮尚未提交**
    （26 个已跟踪改动 + 42 个未跟踪新增，含 `docs/account/`、`docs/LIQUID-TODO-*.md`、
    `images/reel-*.mp4` 与 `pay-*.svg`）。
  - **Shopify live**：r61 / r62 / r63 / r64+r65 / r66 / r67 / **r68** 都已推。
    每次都是 `--only` 逐个列出 + `--nodelete` + `--allow-live`。
  ⚠ **liquid 从未推过，推 liquid 需逐次授权**；线上的 liquid 是别人在维护的。
- **Shopify 推送**：店铺 `je1ka9-er.myshopify.com`，CLI 账号 **john@mockuptocode.com**
  （⚠ 不是 johnz0385@gmail.com，那个账号对这个店无权限；CLI 单 session，
  换账号会踢掉 funkyfood2 / global-cke 的登录态）。
  主题 **`Dev` (#180348977399) role = live** —— 名字骗人，改它就是改线上；
  `Horizon` (#179976765687) 是 unpublished。
  **一律 `--only <file>` 逐个列出 + `--nodelete`，绝不裸跑 push。**
  基线在 `/home/ly/project/Gumi-Brand-shopify/`（不在静态站仓库里）。
  ⚠ **线上 45 个 SVG 与本地只差 CRLF/LF，不是改动，别推**；
  ⚠ **`customstyle.scss` 与 `.css` 都在主题 assets/ 里，必须双写**。
- git 远端 `github.com/luyouse-luka/Gumi-Brand--Temporary`（private，临时同步仓库），分支 `main`。
  推送走 SSH 别名 **`github-luyouse-user`** —— 裸用 `github.com` 会走 devmtc-1 那把 key 认证失败。
- **推送等明确指令**，共用环境绝不全量、绝不 `--delete`。

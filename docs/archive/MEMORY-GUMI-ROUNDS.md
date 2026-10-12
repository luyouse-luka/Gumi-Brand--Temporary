# Gumi Brand — memory 里的逐轮进度原文（r116–r126）

> 2026-09-09 从 memory `project-gumi-brand.md` 移出，**原文未改一字**。
> memory 里留的是从这些段落提炼出的长期规则；基线目录名 / 文件数 / `$build` 具体值会过期，
> 以 `grep '$build' assets/customstyle.scss` 与 `docs/HANDOFF.md` 顶部为准。

---

**2026-09-09 进度（r126）：线上基线 `baseline-20260909-r126/` 624 个文件，
`$build` 仍是 `20260909-r124`（r125/r126 都没动 css/js）。当天连推七轮 r120–r126。**
⚠ **reel 卡是竖版 9:16（桌面 304×540 / 手机 228×405），但占位视频 `video-07.mp4` 是
1276×720 横版** —— `object-fit: contain` 之下视频只占卡片高度 **32%**，上下各留约 184px 深色。
**这是素材问题不是样式问题**，r126 已在 schema 里加了竖版提示（`paragraph` + 三个字段的
label/info），等需求方按 9:16 重新上传。**不要改成 `cover`**：那会把横版裁成中间一条。
⚠ **改 schema 时只动 `label` / `info` / 新增 `paragraph`，`id` 一个都别动** ——
动 `id` 才会让已存的值失联。r126 改完回读复核 36 个视频值全部保留。

**2026-09-09 进度（r125）：线上基线 `baseline-20260909-r125/` 624 个文件。
`$build` 仍是 `20260909-r124`（r125 只改 liquid 与模板数据，css/js 未动）—— 又一次轮次号≠build 号。**
⚠ **r125 首次按需求方指示推了 3 个 `templates/*.json`**（product / page.our-story /
page.how-gumi-works，各补 10 个 reel 的 `"video"`）。**这是红线例外，没有明确指示仍然绝不推。**
降低风险的做法：**当场 pull → 正则只插入一行（不要用 `json.dump`，会重排格式产生几百行无关 diff）
→ 立刻推 → 回读逐字节核对**。三个文件 diff 各只有 10 行新增，同时反证对方窗口内没碰过。
⚠ **需求方说「video 已填入」，拉下来实测三页各 0 个** —— 如实告知后需求方才指示由我们填。
**先拉再信**（同 [[feedback_honest-recall-no-appeasement]]）。
⚠ **`gb-reviews.liquid` 有两层守卫**：单卡 `{% if video_url != '' %}` + 外层「一张可播的都没有
就整条 `.gb-reviews__reels` 轨道不渲染」。只留单卡守卫的话空 swiper 轨道照样占位画翻页按钮。
外层那段解析必须与渲染循环里的完全一致。
⚠ **守卫做过破坏性真实验证** —— 卡片全填上视频后这条分支就测不到了，所以临时摘掉 our-story
一个 video 推上去实测 9 张卡（对照组 10 张），再推回原数据复核 10 张。
**改这类"缺数据时降级"的逻辑，不构造缺数据就等于没验。**
⚠ **30 张卡 + 首页 6 张都是同一段 `video-07.mp4`**，需求方指定的占位，**上线前必须替换**。

**2026-09-09 进度（r124）：`$build` = `20260909-r124`，线上基线 `baseline-20260909-r124/` 624 个文件。
当天连推五轮 r120–r124。**
⚠ **r124 修的是「`[hidden]` 属性设了但元素没消失」** —— UA 的 `[hidden]{display:none}` 特异性
**0-0-0**，输给元素自己的作者 `display`。r123 新写的 `.gb-reel__trigger{display:flex}` 漏了重申，
播放中的按钮仍在绘制（304×540）、仍在 tab 序里，只是被后 append 的 video 盖住看不见。
**项目里这条重申一共五处**（nl-panel pane / promo panel / `.gb-btn` / `.gb-crev-card` /
`.gb-reel__trigger`）—— **新写任何"带作者 display 又要用 hidden"的元素都要补 `&[hidden]{display:none}`**。
见 [[hidden-attr-vs-author-display]]。
⚠ **判据教训：断言"属性设没设" ≠ 断言"它起没起作用"** —— `reelplay.py` 原来只读 `t.hidden`，
那个在 bug 下一直是 `true`，全绿。真正抓到它的是 `getComputedStyle(t).display === 'none'`
与 `getBoundingClientRect() === [0,0]`。**凡是"某元素被隐藏/禁用/移除"的断言，都要读效果不读属性。**

**2026-09-09 进度（r123）：`$build` = `20260909-r123`，线上基线 `baseline-20260909-r123/` 624 个文件。
当天连推四轮 r120–r123。**
⚠ **r123：reel 改成「就地播放」，`.gb-rv-modal` 弹窗整套删除** —— 客户原话「不是点击出现弹窗
而是只可以播放的视频」，选 A 方案（点击卡片就地播放带控件）。**这推翻了 r11/r66/r81/r117
一路做的 reel 弹窗**，别当成"漏掉弹窗"补回来。
- `.gb-reel` 从 `<button>` 变 `<div data-reel>`，内层 `.gb-reel__trigger` 承载交互
  （`<button>` 里不能放 `<video controls>`：无效 HTML，控件点击还冒泡回按钮）
- 删掉：scss 的 `.gb-rv-*` 171 行、main.js 的 `playVideo/stopVideo/embedUrl` 98 行、
  liquid 的弹窗块、4 个静态页各 19 行、**r121 给 `.gb-reel` 加的 `.is-refocused` opt-out**（已成死规则）
- 新增 `main.js` 的 `reelPlayer` 模块（mp4→`<video>`、YouTube→`<iframe>`、file://→说明块，一次只播一个）
- **推了对方的 `sections/gb-reviews.liquid`**（经逐次授权），完整文件+patch 在 `liquid/`
- 判据 `tools/reelplay.py`（静态 23/0、`--live` 20/0、`--strip` 8 red）
⚠ **线上 reel 视频填写状况（推翻旧记录「线上还没填值」）**：首页 6 张**已填**
（都是 `shopify://files/videos/video-07.mp4`，同一个文件）；**product / our-story /
how-gumi-works 三页各 10 张、一个都没填 → 那 30 张卡点了没反应**。
在 `docs/LIVE-BACKLOG.md` 第〇之三条，判据单列成 backlog 汇总不计 red。
⚠ **写反向验证（`--strip`）要先确认它真的会红** —— `reelplay.py` 第一版只删 hook 属性，
可事件早已绑定、选择器还有 class 兜底，反向跑照样全绿 = 等于没写。
改成删数据源（让函数早退）+ 植入被删掉的东西，才真正反向。
⚠ **锚点随功能消失时，判据会以「存活守卫报 0」的形式转红，那是守卫在工作** ——
本轮 `placeholderbg` / `scrolllock` / `refocusring` / `font-check.html` 四份都因此改过，
都不是回归。

**r122：hero 入场改成一条时间线** —— title 行 → lead 行 → 按钮 → USP 依次登场。
两套动画系统（lineReveal 150ms/行、wowo `delay-in-N`）用一个 `--line-base` 计数器串起来；
hook 由 `lineReveal.wireHero()` **运行时注入**（hero 标记在对方 liquid 里，不越界改）；
CSS 用 `[data-seq-step].wowo.animated`（0-3-0）压过 markup 里删不掉的 `delay-in-N`（0-1-0）。
⚠ **`wowo.play()` 的剥类时机从固定 1500ms 改成 `1500 + 自身 delay`** —— 这是**对 Terra 移植的
有意偏离**：390 档 USP 延迟 900ms + 700ms 动画 = 1600ms，原版会在淡入 86% 时让元素跳终态。
别"改回 Terra 一致"。判据 `tools/heroseq.py`。

**r121：Escape 关闭弹窗后，触发按钮不再显示 focus 样式** —— 程序化 `.focus()` 会**保留调用前的
`:focus-visible` 状态**，于是触发按钮画出焦点环。共享 `returnFocus(el)`（main.js 顶层）打
`.is-refocused` 标记，CSS 撤掉焦点样式，下次真实按键或失焦清除。三处共用：header / modal / dropdown。
⚠ **一条全局 `outline:none` 不够** —— 各组件的焦点样式属性不同（reel 是子元素 scale、
表单是 border-color），要逐个 opt-out，**靠实测发现不是靠读层叠**。
⚠ **别用 `mouseenter` 清标记** —— 弹窗关闭时布局变化会把元素滑到静止光标下，Chrome 补发
`mouseenter`，标记在设上的同一瞬间被清掉。hover 用 CSS `:not(:hover)`。
另加 `.gb-page-hero--center .gb-page-hero__title { max-width: 990px }`（**7 个页面在用，
不是 scss 注释写的 5 个**）。判据 `tools/refocusring.py` / `tools/r121check.py`。

**2026-09-09 进度（r120）：`$build` = `20260909-r120`，线上基线 `baseline-20260909-r120/` 624 个文件。**
⚠ **r120 把全站占位图的灰底全部去掉了（15 处）** —— 13 个 `$c-gray-200` 媒体盒底
+ `.gb-crev-card__image` 的 `#d5d4d4` + `.gb-scallop-box` 的 `--box-bg` 默认值。
**需求方在两个口径里明确选了 B「一律去掉，含尚无摄影素材的纯占位块」**，
这**推翻了** `PROJECT-STATUS.md`「内容真实性」里「占位保持占位」的旧规则 ——
**下一轮别按 Figma 稿把 `#d9d9d9` 补回来**，那些盒子现在就该是纯空白。
保留三处不是漏改：`$c-gray-200` 变量本身（`$color-border` 指着它）、
`.gb-ingredients__disc` 的 `--box-bg: $c-sand`（真实设计色）、
`has-video` 时的 `$c-ink`。判据 `tools/placeholderbg.py`（静态 50/0、`--live` 40/0、
`--strip` 反向 33 red），**按模块命名不带轮次号**。
⚠ **HTML 里还有 58 处 `TODO client image: … grey placeholder` 故意没动** —— TODO 本身仍成立。
⚠ **「See More Reviews 一次加载 6 个」是对方做完的，我方零改动** ——
那个步长是 `gb-app-section.liquid` 的 schema setting `step`，**存值在
`templates/page.reviews.json` + `product.json` 两个红线 JSON 里，liquid 的 default 改了不生效**
（同 r117 `link_4_url` 的坑）。r120 回读时发现对方把 default 与两处存值都 4 → 6 了，
线上实测 `step=6`、点一次 5 → 11。**别记成我方成果，也别再推一遍。**
⚠ **待办（只记录未动手）**：客户提「`gb-science-card__value` 数字不要单独放 p 里，没有任何的语意」
—— 语义化改造，两种改法与三条约束（`data-count-up` 的 hook 不能留在合并后的 `<p>` 上，
否则 `countUp.run()` 的正则匹配不上、动画静默失效；nutrient 变体的 value 与 text 不相邻做不到合并；
要授权推对方的 `sections/gb-science.liquid`）逐条在 `docs/PROJECT-STATUS.md`「第一二〇轮新开的」。
⚠ `r119check.py` 又踩了写死 `$build` 的坑（HANDOFF r119 自己刚记过），已改成「≥」。

**2026-09-08 进度（r118）：`$build` 仍是 `20260908-r117`（r118 只改 main.js，scss 未动），
线上基线 `baseline-20260908-r118/` 624 个文件。**
r118 修「预开状态的弹窗关不掉」：`gb-cart-drawer.liquid` 三个分支的 `.gb-cart` 都写死 `is-open`，
其中 `empty-cart-template`（删掉最后一件商品时回放）用我们的 `[data-modal-close]`，
另两个用主题的 `on:click` —— 我们的 `modal.close()` 守卫在只有 `open()` 才设的 `current` 上，
于是那一个分支三条关闭路径全 no-op。详见 [[custom-element-open-attr-vs-inner-dialog]]。
⚠ **r117 实测「遮罩能关」没有错，只是撞上了接线不同的另外两个分支** ——
**一个 snippet 多分支时，验证要把每个分支都走一遍。**

**上一轮进度：`$build` = `20260908-r117`（第一一七轮已推，标题号与 build 号从 r112 起
对齐 —— r109 被跳过一次专门为了对齐），线上基线 `baseline-20260908-r117/` 624 个文件。**
r117 需求方八条（一条当场撤销、一条只能走后台）：
⚠ **`--page-width` 含两侧 margin** —— Horizon 自身值是 `calc(90rem + margin*2)`。给
collection / 404 对齐版心时按「内容宽」填 `$w-container` 会让三档各多缩进 80，正确值是
`$w-container + $pad-x-desktop*2`（= container mixin 的 max-width）。**本轮为此推错一次**，
`r117live` 6 red 抓到才修。教训：**线上专有规则（静态站零匹配）推前必须用 `add_style_tag` 注入预演**。
⚠ `/cart` 购物车关不掉的真因是 [[custom-element-open-attr-vs-inner-dialog]]，已在 main.js 兜。
⚠ **`docs/LIQUID-TODO-reels.md` 整份作废** —— 三处 hook 对方做了两处、第三处 r66 被
「play 图标完全不显示」取代。reel 的真缺口是 schema 只有 `{"type":"video"}`（只吃 Files 上传），
r117 补了 `video_embed`（**必须 `text` 不能 `url`**，url 类型不收 YouTube watch 链接）+ `poster`。
线上仍播不了是因为还没填值，不是没生效。
⚠ **Contact 两处链接改不了** —— header 那条在 Shopify 导航菜单（不在主题文件里）、
footer 那条在 `footer-group.json`（红线）；`gb-footer.liquid` 的 `link_4_url` 只是 schema default，
已有存值时改了不生效。见 `docs/LIVE-BACKLOG.md` 第 0 条。
⚠ **单轮判据里别写死 `$build`** —— `r116check` 因此在 r117 必然转红、像回归失败，已改成「≥」；
`r115check` 同样的写法还留着。
⚠ **对方会在后台重编排页面**：r116 后把 science 页我们填的 CTA 改成 `Shop now`/`shopify://collections`，
4 个 `wave_*` 并成 1 个 `gb_wave_8wJQLE`。三方对比每轮都要跑。
r116 三条：① science 的 Shop Now **不是新做的**，按钮与 6 条断点差额 r115 就推过，本轮只是
经授权填了 `templates/page.science.json` 的 `cta_label`/`cta_url`（值取自同页 `ingredients`
那颗，不是自拟）—— 净距 48 **只能量不能读规则**（`margin-top` 是差额，`__inner` 的 gap 垫在上面）；
② 桌面 Tab 重排成 `toggle → 整个菜单 → bar 剩余 → 页面`，**三个接缝，第三个（走出 header）
漏了就是死循环** —— `.gb-header__panel` 是 `<header>` 最后一个子元素，走完 cart 的默认下一站
正是菜单第一个；③ `.gb-highlight-card__media` 白线见 [[rounded-clip-box-bleeds-its-own-background]]。
⚠ `menutab.py` 的 `WHERE` 现在多返回 `aria` —— 线上 cart 链接带角标 `0`，`textContent` 非空、
回退不到 `aria-label`，静态站没角标所以**这个假信号只在线上转红**。
⚠ **git 工作区从 r99 起又攒了 90+ 项未提交**（最新 commit 停在 r98 `e45f34a`），
「每轮及时提交」的约定**已经第二次失效**。
r115 起 `.gb-br-wide` 不再隐藏，`gb-lines` 的 `^^` 与 `//` **渲染结果相同**，
全站没有「只在桌面断」的能力了。`sections/gb-science.liquid` 有了 `cta_label`/`cta_url`
两个 setting，**留空不渲染** —— 线上那颗 Shop Now 还没值，等需求方在主题编辑器里填。
⚠ 弹窗表单缺 `data-promo-form`，`main.js` 的 `promoModal.bindForm` 因此接不上，
线上提交邮箱不会切到「复制优惠码」那屏而是整页 POST `/contact`（liquid 是对方的，未动）。
hCaptcha 吃 gap 的坑见 [[shopify-hcaptcha-eats-a-flex-gap]]。 期间主题团队上线了首单折扣弹窗
（`snippets/gb-promo-modal.liquid`，用我们全套 `.gb-promo-panel__*` 类名，但自带内联
`<script>`、不走 `main.js` 的 modal 模块）。⚠ **线上 hero 的内建波浪 r105 起已换成流内的
Gumi Wave section**，`.gb-hero` 手机端那个给小熊留的 496 margin 因此会把波浪一起推走 ——
已用两条 `.shopify-section:has()` 修（静态站恒不匹配）。

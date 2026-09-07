# Gumi Brand — 交接

> 一份文档管三种会话：**接手做需求** / **对稿复查** / **做审计**。
> 项目定位与已确立的规范在 [PROJECT-STATUS.md](PROJECT-STATUS.md)；
> 改动史在 [CHANGELOG.md](CHANGELOG.md)（近 10 轮）+ [CHANGELOG-ARCHIVE.md](CHANGELOG-ARCHIVE.md)（第一～三十轮），**两份一起 grep**。
>
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

> 状态：`$build` = **`20260907-r90`**（第九十轮，2026-09-07）—— 评论卡四处改造：
> 星级拆成 `<img>`、附件放小熊占位、More/Less 分页、4.76 补上 r89 漏掉的 `$c-lime` 描边。
> **未推 live**（`gb-app-section` 线上仍没有 liquid，推 css 也渲染不出来）。
> 判据 **`tools/crevcheck.py`**：正向全绿、`--strip` 反向 68 红；`rwd.py` 两页全绿。
> 逐条与「别报成 bug」在 **1u**。
> ⚠ **判据从 `r89check.py` 改名成 `crevcheck.py`** —— 另一个会话同日也做了 r89 并
> **覆盖了那个文件**。gb-crev 的判据从此按模块命名、不带轮次号，别再改回去。
> ⚠ **`$build` 一天之内被两个会话各推进过一次**（我 r88 → 它 r89 → 我 r90）。
> 动 token 前先 `grep '\$build' assets/customstyle.scss`，别按记忆推断。

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
>
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
>
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
>
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
>
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
>
> 状态：`$build` = **`20260907-r83`**（第八十三轮，2026-09-07，**已推 live**）。
> `.gb-science__title` 收窄到 660 并居中、`.gb-science-card__text` 去掉 6px 顶距。
> ⚠ **`margin: 0 auto` 会压过手机端的 `align-items: flex-start`** —— narrow 块里那句
> `margin: 0` 是承重的，删了手机端标题就会居中，而稿里（`228:8166`）是左对齐。
> ℹ `max-width: 660` **只在首页咬得住**：`/pages/science` 的标题在所有档都填满 `__head`，
> 原值 1072 同理也从未生效过。
> 判据 `tools/r83check.py`：线上 `--as-served` 全过 + 2 条明确跳过。
> 新基线 **`baseline-r83/`（607 文件）**。
>
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
>
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
>
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
>
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
>
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

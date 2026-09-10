# 推送记录

> 每次 `shopify theme push` 一行。**详情看 [CHANGELOG.md](CHANGELOG.md) 对应轮次**，
> 这里只回答「什么时候推了哪些文件、验了没有、基线滚到哪」。
>
> 店铺 `je1ka9-er.myshopify.com`，主题 **Dev #180348977399（role = live）**。
> 一律 `--only <file>` 逐个列出 + `--nodelete` + `--allow-live`，**绝不裸跑 push**。

## 流程（每次都走完）

```
1  theme pull → prepush-rNN          拉线上最新
2  三方对比   baseline / prepush / work
     local ≠ baseline → 我改的，进推送清单
     remote ≠ baseline → 别人改的，拉回来不覆盖
     两边都改        → 冲突，中止
3  分步推送   依赖在前（snippet → section；css → 用它的 section）
4  theme pull → verify-rNN           全量回读
5  回读判据   推的文件逐字节一致 + 其余文件零附带改动 + 文件数没掉
6  滚基线     verify-rNN → baseline-rNN，清掉 prepush 与旧基线
```

⚠ **回读判据必须有 liveness 守卫**：拉取没跑完时大部分文件不存在，
「其余文件零附带改动」会在空集上恒真（2026-09-08 实际踩到过）。

⚠ **CDN 直读核对必须带 `?v=` 指纹** —— 不带指纹的
`https://gumi.com.au/cdn/shop/t/2/assets/customstyle.css` 回来的是**任意旧的缓存副本**
（r91 与 r119 两次实测都是 `20260907-r73`，落后几十轮），HTTP 200 只证明「有东西」、
不证明「是新的」。**看着像「推了没生效」，其实是 URL 用错了。**
正确判据两条，本流程第 5 步的回读用第一条即可：
① `theme pull` 回来逐字节比对；② 渲染后的页面里读
`getComputedStyle(document.documentElement).getPropertyValue('--build')`
（同时证明「文件是新的」和「浏览器真用上了」）。见 memory
`verify-shopify-live-css-minified`。

## 2026-09-08

| 轮次 | 推了什么 | 文件数 | 回读 | 基线 |
|---|---|---|---|---|
| **第一百轮** | `snippets/gb-lines.liquid`（新）+ 10 个 gb-section | 11 | 13 ok / 0 red | 618 → 619 |
| **第一〇一轮** | `sections/gb-wave.liquid`（新）+ `customstyle.css`/`.scss` | 3 | 5 ok / 0 red | 619 → 620 |
| **第一〇二轮** | 11 个 `templates/*.json` + `customstyle.css`/`.scss` | 13 | 15 ok / 0 red | 620 → 620 |
| **第一〇三轮** | `sections/gb-wave.liquid` + 11 个 `templates/*.json` | 12 | 3 ok / 11 red（良性，见下） | 620 → 620 |
| **第一〇四轮 a** | `sections/gb-footer.liquid`（合并重传） | 1 | 5 ok / 1 red（对方并发改动，见下） | 620 → 620 |
| **第一〇四轮 b** | `customstyle.css`/`.scss` + `sections/gb-wave.liquid` + 11 个 `templates/*.json` | 14 | 27 ok / 0 red | 620 → **`baseline-r104`** |
| **第一〇五轮** | `customstyle.css`/`.scss` + `sections/gb-wave.liquid` + 11 个 `templates/*.json` | 14 | 我方改动全部落地；2 处对方 schema 变更导致的数据剔除，见下 | 623 → **`baseline-r105`** |
| **第一〇六轮** | `customstyle.css`/`.scss` + `assets/main.js` | 3 | 3 个文件逐字节一致；1 处附带差异是对方并发改动 | 623 → **`baseline-r106`** |
| **第一〇八轮** | `assets/star.svg` + 13 个 `templates/*.json` | 14 | 12 逐字节一致；9 个 CTA 模板 18 处良性剔除，**真实数据差异 0** | 623 → **`baseline-20260908-0800`** |
| **第一一一轮** | `sections/gb-footer.liquid` | 1 | 逐字节一致；623 个清单外文件零改动 | 624 → **`baseline-20260908-0900`** |
| **第一一六轮** | `customstyle.css`/`.scss` + `assets/main.js` + `templates/page.science.json`（授权） | 4 | 4 个逐字节一致；620 个清单外文件零改动 | 624 → **`baseline-20260908-r116`** |
| **第一一七轮** | `customstyle.css`/`.scss` + `assets/main.js` + `sections/gb-reviews.liquid`（授权）<br>⚠ css/scss 因 `--page-width` 填错重推过一次 | 4 | 4 个逐字节一致；620 个清单外文件零改动 | 624 → **`baseline-20260908-r117`** |
| **第一一八轮** | `assets/main.js` | 1 | 逐字节一致；623 个清单外文件零改动 | 624 → **`baseline-20260908-r118`** |
| **第一一九轮** | `customstyle.css`/`.scss` + `assets/main.js` | 3 | 3 个逐字节一致；621 个清单外文件零改动 | 624 → **`baseline-20260908-r119`** |

**第一一九轮**：三方对比 ours 3 / **theirs 12** / CONFLICT 0。theirs 全是红线文件
（`config/settings_data.json` + 11 个 `templates/*.json`），本轮零 template 推送、未覆盖。
逐条看过：`settings_data` 只差两项（promo 弹窗标题、免运费门槛 100 → 10900，对方后台改的），
`collection.json` 的差异是 **Shopify 保存时补全 schema 默认值**（`font_size` / `text_color` 等空值）
+ 新增 `wave_footer_cta_before` 与分页设置 —— **主题的 Typography 设置没有变**，
本轮「15 个字体变量还是 Inter」的判断在推送前后都成立。
线上实测 `tools/r119live.py --password 1234` **8 ok / 0 red**（无 CDN 滞后，推完即读到）；
回归 `r117live --cart` **11/0**、`menutab --live` **58/0**。
⚠ `r117live.py` 也写死了 `$build`（推完必然假性转红），已同 `r117check.py` 一起改成「≥」——
**这个坑 check 侧和 live 侧是两份，修一边不够。**

**第一〇三轮那 11 red**：Shopify 自己把过渡用的 `pair` 键剔掉了（schema 没声明的 setting
保存时会被丢弃）。逐字段核对过 25/25 个实例色值都在、`count`/`direction` 完好、`order` 未动。

⚠ **第一〇二轮是本项目第一次推 `templates/*.json`** —— 此前是明令红线（Online Store Editor
托管，推它 = 覆盖别人在后台调的所有设置）。当次经用户明确授权，做法是
**读线上最新 → 只插入需要的条目 + 只改目标 setting → 写回**，且推前逐文件核对了改动面。
**红线没有取消，下次仍需逐次授权。**

**第一〇四轮 a 那 1 red**：回读发现 2 个附带差异 —— **对方在我方拉取（05:12）与推送之间改的**，
不是本次推送造成的（推的文件逐字节一致、文件数 620 未变、`--only` 只含一个文件）。
详见下表。⚠ 其中 `templates/page.get-in-touch.json` 正是本轮待推清单里的一个 ——
已**以回读的最新树为基底重建**了 11 个 templates，对方的 `form_type` 修复完好保留。

⚠ **教训：templates 的改动必须在推送前的最后一刻、以最新拉取为基底重建**。
`tools/_apply_r104_tpl.py` 因此改成必须传 `--src <最新拉取目录>`，不再硬编码快照。

### 第一〇四轮 b（已推，经用户授权）

14 个文件，**分两条命令按依赖序推**（一条命令里 `--only` 的先后 Shopify 不保证执行序）：

```
1  assets/customstyle.css / .scss + sections/gb-wave.liquid     实现先落地
2  templates/*.json × 11                                        再让实例指名尺寸
```

⚠ 顺序反了不会报错，只会渲染错：templates 先落地时线上还没有 `.gb-wave--sm/--lg` 的实现，
每条波浪都会退回默认弧数。

**推前**重新 `theme pull` 为 `prepush-r104b`，与上次回读逐字节零差异（对方那段时间没再动）；
templates **以这份最新拉取重建**，三方对比 ours 14 / theirs 0 / **冲突 0**。

**回读** `verify-r104b`：14 个文件逐字节一致、其余 606 个零附带改动、文件数 620 未掉。
落地核对：24 处 `count` 全是 board size（sm 12 / lg 12），2 处 `color_below` 到位，
对方的 `form_type: contact` 完好。**27 ok / 0 red**。

⚠ **1 处 `count` 有意保持 `'3'`**：`page.reviews.json` 的 `wave_gb_product_tj33wK_after`——
线上这页没有 `app-section`，这条边界在稿上没有对应物。判据把它列为 exempt 并断言它**没被改动**。

**线上实测** `tools/r104map.py --password 1234`：边界差异 **32 → 11**，
所有尺寸与间距差异归零（每条 ok 的 `padding-bottom` 与静态站逐字节相同）。
剩下的 11 处全是已登记的模块缺口（线上缺 `logo-scroll` / `app-section` / `cta-band` /
两处 `gb-product`）与 index 那处 `--bleed` 机制差异，**没有一处是波浪本身的问题**。

**基线滚动**：`verify-r104b` → **`baseline-r104`**（620 个文件）；
`prepush-r104b` / `verify-r104` / `live-20260908-0512` 已清掉。

### 第一〇五轮（已推，经用户授权）

推前拉取比对，对方**又新增 3 个 blocks 并改了 `sections/gb-rich-page.liquid`**（在做 shipping 的表格模块），
与我方 14 个文件零重叠，三方对比**冲突 0**。分两步按依赖序推。

回读：14 个文件中 5 个逐字节一致；**9 个 `page.*.json` 不一致，全部是 Shopify 剔除废弃键**——
`show_scallop` / `bg_variant` / `scallop_variant` 的 schema 已被对方删掉，保存即丢（同第一〇三轮的 `pair`）。
逐叶子核对：**33 处良性剔除**，我方目标改动 100% 落地。

线上实测 `tools/r104map.py --password 1234 --all`：
`gb-nutrition -> gb-product` 的 bleed 边界 **ok**（`transparent -> #ffffff`，h=129，与稿逐项一致）；
**11 页的 CTA 波浪全部 ok**。

## ⚠⚠ 本轮的事故：两页正文被剔除（数据已抢救）

`page.privacy-policy.json` / `page.shipping.json` 的 `body.settings.content`（整页正文）
在推送后**从 template 里消失**。责任要分清：

| 事实 | 谁造成的 |
|---|---|
| 线上两页正文**空白** | **对方**。他们把 `gb-rich-page.liquid` 从 `{{ section.settings.content }}` 改成 `{% content_for 'blocks' %}` 却没迁内容，我方推送**之前**页面就已经是空的（推前快照里 `body` 无 blocks） |
| template 里的正文**数据消失** | **我方推送触发**。那个键已不在 schema 里，Shopify 一保存就丢 |

**数据已抢救**，两次独立拉取的值一致，存放在：

```
docs/rescue/page.privacy-policy-body-content.html   3826 字符
docs/rescue/page.shipping-body-content.html         1277 字符
```

恢复路径：对方的新 `blocks/gb-rich-text.liquid` 就是同构的 `richtext` `content`，
把这两份内容各建一个 `gb-rich-text` block 即可。**本轮未做** —— 需求方的指示是
「只管自己修改的数据」，这属于对方正在进行的迁移。⚠ 但**必须告知对方内容在哪**，
否则他们未必有备份。

⚠ **教训：推 template 会连带清掉「schema 已删但 template 里还留着」的键。**
对方正在重构 section schema 时，推他们负责的 template 之前要先看那个 section 的 schema 有没有变。

## 期间对方（WP/主题团队）的改动

| 时间点 | 文件 | 内容 | 我方处置 |
|---|---|---|---|
| 第一百轮前 | 13 个（`gb-lead` / `gb-subscription` / 各 section 的 `arc_text` info 等） | 订阅模块 + 提示文案 | 未覆盖 |
| 第一〇三轮前 | `sections/gb-footer.liquid` | **回退了第一百轮的 `gb-lines`**，`tagline` 改回 `richtext` + `gb-rich-inline`；另加了 newsletter 成功/失败提示 | **未擅自改回**（改回会覆盖他们的新功能），已登记待裁决 |
| 第一〇四轮 a 期间 | `sections/gb-form-section.liquid` | privacy policy 链接加 `target="_blank" rel="noopener noreferrer"` | 未覆盖 |
| 第一〇四轮 a 期间 | `templates/page.get-in-touch.json` | `form_type` `referral` → `contact`（修表单类型用错） | 未覆盖，已并入本轮重建的基底 |
| 第一〇五轮前 | 11 个 `sections/gb-*.liquid` | **删掉全部内建波浪输出与 `scallop_variant` schema**（含 `gb-nutrition` 的 `--bleed`、`gb-footer-cta` 的那条），`gb-footer-cta` 另删 `bg_variant` | 未覆盖；⚠ 回退路径就此消失 |
| 第一〇五轮前 | `templates/index.json` / `product.json` | 各插一条 Gumi Wave 在 CTA 前（只迁了 2/22 个模板） | 保留，并补齐其余 9 页 + 改正 product 的目测配色 |
| 第一〇五轮推送前 | `sections/gb-rich-page.liquid` + 3 个新 blocks | 正文改由 blocks 承载（`gb-rich-text` / `gb-rich-table` / `_gb-rich-row`） | 未覆盖；⚠ 连带导致上面那起正文剔除 |


### 第一〇六轮（已推，经用户授权）

需求方十条，**只推 3 个 asset，零 liquid、零 template**（红线未触碰）。

推前 `theme pull` 两次：06:22 与推送前 07:08。两次之间对方改了
`config/settings_data.json`、`config/settings_schema.json`、`snippets/gb-cart-drawer.liquid`、
`snippets/gb-cart-empty.liquid`、`templates/page.shipping.json` —— **与我方 3 个文件零重叠，冲突 0**。

回读：3 个文件**逐字节一致**，文件数 623 未变。1 处附带差异
`sections/gb-app-section.liquid`（评论时间改成「X ago」相对时间）——
是对方在我方 prepush 拉取（07:08）与 verify 拉取（07:09）之间推的，`--only` 里根本没有它。

线上实测 `tools/r106live.py --password 1234` **28 ok / 0 red**。

⚠ **`assets/main.js` 连带推上了第九十六轮那 5 行**（Swiper `transitionEnd`），
此前一直未推，本轮随 Lenis 那条一起上线。

**基线滚动**：`verify-r106` → **`baseline-r106`**（623 个文件）；
`pull-r106` / `prepush-r106` / `baseline-r103` / `baseline-r104` 已清掉。

⚠ **验证成本的说明**：本轮判据里真正必须读线上的只有 `/collections/all`（Horizon 自己的模板，
静态站没有对应页，钩子 `data-template` 也只在线上存在）。其余九条全部跑在本地静态站，
全站 computed-style 快照也是本地 `file://`。这一轮拉线上拉得多，是因为需求方点名要
「查原因、是否和静态站一致」（第 5/7/8 条）—— 那是**一次性诊断**，不是每轮推送的必需流程。

### 第一〇七轮（2026-09-08，已推，经用户授权）

需求方四条，**只推 2 个 asset**（`assets/customstyle.css` + `.scss`），
零 liquid、零 template、零 `main.js`（红线未触碰）。

⚠ **需求方同期在另一会话改线上 json**（模块与配色），所以本轮的三方对比不是走过场：

| | 数量 | 内容 |
|---|---|---|
| ours | 2 | `assets/customstyle.css` / `.scss` |
| theirs | 7 | `sections/footer-group.json`、`sections/gb-app-section.liquid`、`sections/gb-page-hero.liquid`、`templates/index.json`、`templates/page.faq.json`、`templates/page.how-gumi-works.json`、`templates/page.reviews.json` |
| **CONFLICT** | **0** | — |

⚠ `sections/gb-page-hero.liquid` 与本轮第 2 条（`--center` 顶距）**同模块，逐行看过 diff**：
对方加的是 overline（小字 + 五星 SVG）与两个 setting，**没动 section 根类**，我方规则照常命中。

推送前验产物新鲜度：重编译 scss 与仓库里的 css **逐字节相同**。

回读：2 个文件逐字节一致，文件数 **623 未变**，与 prepush 的差异**只有这 2 个文件**。
CDN 带指纹回读（241523 字节）：`20260908-r107` × 16 / `r106` × 0 /
`.gb-product__tag{…inline-flex}` × 1 / `[data-testid=product-list]{--page-margin` × 1 /
`padding:64px 0 calc` × 1 / `padding:80px` 残留 0 / `.gb-form__check:hover` 残留 **0**。

线上实测 `tools/r107live.py --password 1234` **31 ok / 0 red**。

**基线滚动**：`verify-r107` → **`baseline-r107`**（623 文件）；
清掉 `prepush-r107` / `work-r107` / `baseline-r105`。
⚠ `work-r70` … `work-r105` 共 12 个旧工作副本仍在，各 600+ 文件，可清（未动）。


### 第一〇八轮（已推，经用户授权）

**JSON 数据轮**：九个无稿模板补 CTA 波浪 + 四处页面内缺失波浪 + 两处改根因，另换 `star.svg`。
**零 css / 零 js / 零 liquid** —— 同时段并行会话在推 r107 的 `customstyle.scss`，两条线不重叠。

```
shopify theme push --store je1ka9-er.myshopify.com --theme 180348977399 \
  --path <work> --nodelete --allow-live \
  --only assets/star.svg --only templates/{404,article,blog,collection,list-collections,\
         page.contact,page,password,search,index,page.how-gumi-works,page.our-story,page.reviews}.json
```

⚠ **推送前最后一刻重拉发现并发改动**：后台有人把 CTA `button_url` 改成
`shopify://products/superfood-greens-gummies`（index / page.faq 两处），
以及 Shopify 保存触发的规范化。**以最新拉取为基底重建**后推送，对方改动完好保留。

**回读** `verify` 623 个文件：14 个推送文件中 5 个逐字节一致，9 个 CTA 模板各差 2 个键 ——
`bg_variant` / `scallop_variant` 被 Shopify 剔除（schema 早已没有它们，同第一〇三 / 一〇五轮）。
**逐叶子比对 18 处良性剔除 / 0 处真实差异**；609 个清单外文件零附带改动。

**线上实测**：`tools/wavelive.py --password 1234` **6 ok / 0 red**、
`tools/wavemap.py --password 1234` 11 个设计页波浪全部渲染、新增 4 条高度正确。

**基线滚动**：`verify-wavefill` → **`baseline-20260908-0800`**（623 个文件）。
⚠ **基线名用时间戳不用轮次号** —— 并行会话同日在推 r107，轮次号撞过三次。
旧的 `baseline-r106` **未删**，因为另一条线可能仍在用它做三方对比。

### 第一〇九轮（2026-09-08，已推，经用户授权）

⚠ **标题号是一〇九，`$build` 是 `r108`** —— 并行会话把「第一〇八轮」用在它那条 JSON 轮上
（`$build` 不变），我这批推出去时 token 已写成 `20260908-r108`。**认 `$build` 不认标题号。**

需求方五条，**只推 2 个 asset**（`assets/customstyle.css` + `.scss`），
零 liquid、零 template、零 `main.js`（红线未触碰）。

**三方对比**：ours 2 / theirs **18** / **CONFLICT 0**。theirs 分两拨：

| 来源 | 文件 | 内容 |
|---|---|---|
| **并行会话**（同一天另一个窗口） | `assets/star.svg` + 10 个 `templates/*.json` | 补齐线上缺失的波浪、星星换设计稿图（它的第一〇八轮） |
| **主题团队** | `snippets/gb-promo-modal.liquid`（新）、`layout/theme.liquid`、`config/settings_*.json` | 首单折扣弹窗上线 |

⚠ 两处与本轮改动同区，**都逐条核对过**：

- `templates/index.json` 新增 `wave_logos_after` —— 前驱是 logo section，
  不满足本轮第 4 条的 `:has(> .gb-hero)`，零冲突。`overlap: false` 也不触发 `--sc-res`。
- 新增的 `gb-promo-modal.liquid` 用的正是 `.gb-promo-panel__*` 全套类名，我们的样式覆盖得到；
  本轮第 2 条给 `.gb-promo-panel__close` 加的规则正好赶上它上线。
  ⚠ 它自带内联 `<script>`，**不走我们 `main.js` 的 modal 模块**。

推送前验产物新鲜度：重编译 scss 与仓库里的 css **逐字节相同**。

回读：2 个文件逐字节一致，文件数 **624 未变**，与 prepush 的差异**只有这 2 个文件**。

CDN 带指纹回读（241248 字节）：`20260908-r108` × 16 / `r107` × 0 /
`gm-line-up .7s` × 1 / `gm-halo-up .7s` × 1 / `1.4s` 残留 **0** /
`@media(pointer:coarse)` 块在（六个选择器齐全）/ `:active{transform:scale` 残留 **0** /
hero wave 两条各 × 1 / captcha 折叠 × 1。

⚠ **压缩形式又坑了两次**：`@media(pointer:coarse)` 与 `:has(+.gb-wave-section)` 线上都无空格，
按源码形式 grep 全部报 0。**判据一律用压缩形式写**（[[verify-shopify-live-css-minified]]）。

线上实测：`herobear.py --live` 波浪回到 573–609、下游 1069（稿 572–608 / 1068）；
`revealrace.py --live` 四页时序三页领先；上一轮 `r107live.py` **31 ok / 0 red** 无回归。

**基线滚动**：`verify-r108` → **`baseline-r108`**（624 文件）；
清掉 `prepush-r108` / `work-r108` / `baseline-r106`。
⚠ 并行会话建议**基线名改用时间戳**（轮次号已撞四次），本轮推完才看到，**下轮起照办**。

### 第一一〇轮（2026-09-08，已推，经用户授权）

需求方七条，**六条落地**（第 7 条垃圾桶实测已等于稿，未改、等裁决）。
**只推 2 个 asset**（`assets/customstyle.css` + `.scss`），零 liquid、零 template、零 `main.js`。

⚠ **`$build` 从 r108 跳到 `20260908-r110`**，`r109` 未使用 —— 上一批标题「第一〇九轮」
配的是 build r108（并行会话占号造成的分叉）。这轮起标题号与 build 号对齐。

**三方对比**：ours 2 / **theirs 0** / **CONFLICT 0** —— 这一轮线上没有别人的改动
（上一轮是 18 个）。

推送前验产物新鲜度：重编译 scss 与仓库里的 css **逐字节相同**。

回读：2 个文件逐字节一致，文件数 **624 未变**，与 prepush 的差异**只有这 2 个文件**。

CDN 带指纹回读（241774 字节）：`20260908-r110` × 16 / `r108` × 0 /
星星两条 padding 各 × 1 / collection gutter × 1 / `.card-gallery slideshow-arrows` × 1 /
`max-width:370px` × 1 / 评论标题 `text-overflow:ellipsis` × 1 /
`block-size .45s` × 1、**`block-size .3s` 残留 0**。
⚠ 这次 grep **一次命中** —— 判据直接按压缩形式写的（上一轮为此返工两次）。

线上实测 `tools/r110live.py --password 1234` **13 ok / 0 red**；
上两轮回归 `r107live.py` **31 ok / 0 red**、`r107check.py` 82/0、`r107states.py` 0 red。

**基线滚动**：⚠ **从这轮起改用时间戳命名**（轮次号已撞四次）——
`verify-r110` → **`baseline-20260908-0851/`**（624 文件）；
清掉 `prepush-r110` / `work-r110` / `baseline-r107`。


### 第一一一轮（已推，经用户授权）

**单文件轮**：footer 三个 social link 补 `title` 属性。零 asset、零 template。

```
shopify theme push --store je1ka9-er.myshopify.com --theme 180348977399 \
  --path <work> --nodelete --allow-live --only sections/gb-footer.liquid
```

⚠ **`gb-footer.liquid` 需要单独盯** —— 第一〇三轮对方在这个文件里回退过我们的
`gb-lines` 改动。本轮推送前拉了两次（间隔约 10 分钟），两次都确认对方没动它。

**回读** 624 个文件：推的文件逐字节一致，623 个清单外文件零附带改动。
**线上实测** `tools/socialtitle.py --password 1234` **42 ok / 0 red**
（静态站 36 + liquid 3 + 线上渲染 3）。

**基线滚动**：`verify-social` → **`baseline-20260908-0900`**（624 个文件）。
⚠ 并行会话另有一套 `baseline-r108` 等轮次号基线，**两套并存互不覆盖**，别删对方的。


### 第一一二轮（已推，经用户授权）

**三个 asset**：`assets/customstyle.css` + `.scss` + **`assets/main.js`**。
零 liquid、零 template、零 `settings_data.json`。`$build` = `20260908-r112`。

```
shopify theme push --store je1ka9-er.myshopify.com --theme 180348977399 \
  --path work-r112 --nodelete --allow-live \
  --only assets/customstyle.css --only assets/customstyle.scss --only assets/main.js
```

**三方对比**（baseline `baseline-20260908-0900` / remote `prepush-r112` / local `work-r112`）：
ours 3 / **theirs 1**（`templates/index.json`，红线文件，从不推）/ **CONFLICT 0**。

推送前验产物新鲜度：重编译 scss 与仓库里的 css **逐字节相同**；
`work-r112` 与基线的文件清单**完全一致**（无新增无删除），`main.js` 的 diff **正好一行**。

**回读** 624 个文件：推的 3 个逐字节一致，**清单外 0 个附带改动**。

**CDN 带指纹回读**（css 239846 字节 / js 30167 字节）：

| 判据（压缩形式） | 命中 |
|---|---|
| `20260908-r112` / `20260908-r110` | **16 / 0** |
| `.gb-promo-panel__logo svg,.gb-promo-panel__logo img{...}` | 1 |
| `h-captcha[data-size=invisible]{position:absolute}` | 1 |
| `shopify-challenge__container`（第一〇九轮那条的残留） | **0** |
| `.gb-promo-panel{overflow:hidden auto}` | 1 |
| `max-height:100%;overflow-y:auto}`（内容列收进 panel-wide） | 1 |
| `main.js` 的 `.gb-field__input--area, .gb-promo-panel` | 1 |

⚠ CDN 交付的 css/js **不与仓库逐字节相同**（Shopify 还会再压一道，243606 → 239846），
所以逐字节判据只能用在 `theme pull` 回读上，**CDN 一侧只能按压缩形式 grep**。

**线上实测**

| 判据 | 结果 |
|---|---|
| `tools/r112live.py --password 1234` | **75 ok / 0 red**（改前同判据 21 red） |
| `tools/r110live.py --password 1234` | 13 ok / 0 red |
| `tools/r107live.py --password 1234` | 31 ok / 0 red |
| `.gb-promo-panel` 线上带 `data-lenis-prevent` | ✅ —— 反证 `smoothScroll.init()` 用的是新 PREVENT 串 |

**基线滚动**：`verify-r112` → **`baseline-20260908-0919`**（624 文件）；
清掉 `prepush-r112` / `work-r112` / `baseline-20260908-0800`。


### 第一一三轮（已推，经用户授权，**含 2 个 `templates/*.json`**）

**5 个文件**：`assets/customstyle.css` + `.scss` + `main.js` + **`templates/index.json`** +
**`templates/page.our-story.json`**。`$build` = `20260908-r113`。

⚠ **本轮是红线例外**：`templates/*.json` 平时绝不推（Online Store Editor 托管），
本轮需求方明确授权「可以修改 json 然后推送」。**只改了每个文件里的一个字符串**，
且**基于当轮 pull 下来的线上最新版**改，不是基于基线 —— 否则会把对方的改动一起回滚。

```
shopify theme push --store je1ka9-er.myshopify.com --theme 180348977399 \
  --path work-r113 --nodelete --allow-live \
  --only assets/customstyle.css --only assets/customstyle.scss --only assets/main.js \
  --only templates/index.json --only templates/page.our-story.json
```

**改的两个值**（把「普通回车 = 只在手机断」改成「`//` + 回车 = 所有宽度都断」）：

| 文件 | 改前 | 改后 |
|---|---|---|
| `templates/index.json` | `"<p>60+ whole foods.<br>No juicer, no fuss.</p>"` | `"60+ whole foods.//\n No juicer, no fuss."`（无空格） |
| `templates/page.our-story.json` | `"Aussies are obsessed.\nHere's why."` | `"Aussies are obsessed.//\nHere's why."` |

⚠ index 那个是**遗留 richtext 值**。`gb-lines.liquid` 的 `</` 分支会拆包 `<p>`，
但**不保护里面已有的 `<br>`** —— 随后那道 `replace: '<br>', '<br class="gb-br-narrow">'`
把它降级成了「只在手机断」。**所有带 `<br>` 的遗留 richtext 值都有这个问题**，
不只是这一处（见「顺带发现」）。

**安全措施**：改完 `diff` 对线上最新版**每个文件正好 1 行**；改后仍能 JSON 解析
（先剥掉 Shopify 的 `/* */` 注释再 parse）；推送前**又单拉了一次这两个文件**确认没被人改。

**三方对比**（基线 `baseline-20260908-0919`）：对方自基线以来改了 4 个文件
（`sections/footer-group.json`、`sections/gb-footer.liquid`、`templates/page.reviews.json`、
`templates/product.json`），**与推送清单零交集**，CONFLICT 0。

**回读** 624 个文件：推的 5 个逐字节一致。清单外有 2 个文件变了
（`templates/page.how-gumi-works.json` / `page.reviews.json`）——
**是对方在推送窗口内于后台编辑器改的，不是本次推送的附带影响**（用了 `--only`，且这 5 个逐字节吻合）。

**CDN 回读**：`20260908-r113` × 16 / `r112` × 0 / `gb-footer__link:hover{color:#b5ed61}` × 1；
`main.js` 里 `focusin` × 1、`inert` × 2、`expand:` × 1、状态守卫被压成 `if(open!==wasOpen)` × 1。
⚠ **CDN 的 JS 也会被再压一道**（79458 → 31067 字节，参数名都被改短），
所以 `open === wasOpen` 这种源码形态 grep 一定落空 —— 判据要么按压缩形态写，要么只信 `theme pull` 的逐字节。

**线上实测**

| 判据 | 结果 |
|---|---|
| `tools/menutab.py --live --password 1234` | **32 ok / 0 red**（改前 12 red） |
| `tools/footerhover.py --live --password 1234` | **64 ok / 0 red**（改前 26 red） |
| 首页 / our-story 标题回读 | 都渲染成裸 `<br>`，与静态站一致 |
| `tools/r112live.py` / `r110live.py` | 75/0 · 13/0 |

**基线滚动**：`verify-r113` → **`baseline-20260908-0953`**（624 文件）；
清掉 `prepush-r113` / `work-r113` / `recheck` / `baseline-20260908-0851`。

### ⚠ 推送窗口内发现的两件事（都不是本次推送造成的）

1. **`/pages/reviews` 的 H1 现在页面上有字面 `^^`** —— 对方把值填成了
   `"Aussies are obsessed. ^^Here's why."`。`gb-lines.liquid` 的标记**只认「行尾 `^^` + 真回车」**
   （`^^<br>`），这个值里根本没有换行，于是 `^^` 原样打到页面上。
   正确写法：`"Aussies are obsessed.^^\nHere's why."`。**没动** —— 对方正在编辑器里改这个文件。
2. **`sections/gb-footer.liquid` 里第一一一轮加的 `title` 属性被对方回退了**（同时加了 Snapchat 链接）。
   **这是第二次**（第一〇三轮回退过 `gb-lines`）。本轮没推 liquid，未处理。


### 第一一四轮（已推，经用户授权）—— footer title 补回 + reviews 两处断行

**2 个文件**：`sections/gb-footer.liquid` + `templates/page.reviews.json`。
**零 asset、`$build` 不变**（仍 `20260908-r113`）。

#### 1. `gb-footer.liquid`：把第一一一轮的 `title` 属性补回来

对方在第一一三轮窗口内回退了它、同时新增了 Snapchat 链接。按需求方指示
**拉取对方的最新版、在其上补回我们的改动**（而不是推回我们的旧版本）——
所以 Snapchat 链接**原样保留**，`title` 从 3 个变成 **4 个**，值仍与各自 `aria-label` 相同。

⚠ **这是这个文件第二次被回退**（第一〇三轮回退过 `gb-lines`）。**每次推它之前都要单独确认。**

#### 2. `page.reviews.json`：两个 title

| 字段 | 改前 | 改后 | 为什么 |
|---|---|---|---|
| `gb-page-hero.title` | `"Aussies are obsessed. ^^Here's why."` | `"Aussies are obsessed.^^\nHere's why."` | **标记只认「行尾 + 真回车」**，写在行中间时 `^^` 会原样印到页面上（线上当时就印着） |
| `gb-expert.title` | `"Recommended\nby experts"` | `"Recommended//\nby experts"` | **需求方取值**：桌面稿这句是**一行**（1072×48），需求方两次要求桌面也断，按客户取值处理 |

⚠ **`gb-expert__title` 现在偏离桌面稿，是有意的**，别按稿改回去 —— 与第五十九轮那批
「client override」同一性质。手机稿本来就有硬断，所以只有桌面档是新增的。

#### 验证

| 判据 | 结果 |
|---|---|
| 回读逐字节（2 个文件） | 一致 |
| 清单外附带改动 | 1 个 `templates/page.our-story.json` —— **对方同时在后台加手风琴**，非本次推送影响；已确认我们第一一三轮写进去的 `//` 仍在 |
| 线上渲染 `/pages/reviews` | h1 `<br class="gb-br-wide">`、expert `<br>`，**字面 `^^` 已消失** |
| 1440 / 390 实测 | h1 **192px = 3 行**（等于桌面稿的 192）/ expert **两档都是 2 行**；`gb-br-wide` 桌面显形、手机 `display:none`（**全站第一次真正用到这个类**） |
| footer 四个 social link | `title == aria-label` 四个全中 |
| 合计 | **7 ok / 0 red** |

⚠ **reviews 的 h1 在 390 是 3 行、手机稿是 2 行** —— 与本轮无关：该页 hero 线上多带
`--lg`（静态站没有），是 HANDOFF 里早已登记为「忽略」的线上/静态差异。改前那版还多两个
`^^` 字符，只会更长，不是本轮引入的。

**基线滚动**：`verify-r114` → **`baseline-20260908-1000`**（624 文件）。

### 第一一五轮（2026-09-08，已推，经用户授权）—— 需求方四条

**4 个文件**：`assets/customstyle.scss` + `assets/customstyle.css` + `assets/main.js`
+ **`sections/gb-science.liquid`**。`$build` = `20260908-r115`。**零 template JSON。**

| 文件 | 改了什么 |
|---|---|
| `customstyle.scss` / `.css` | `$build` → r115；删掉 `.gb-br-wide` 的 narrow 隐藏；`.gb-rich-table th:first-child` 88 → 124；新增 `.gb-science__cta`（基础档 + `--tight` 档共 6 条 margin） |
| `main.js` | header：焦点落到 toggle 就开菜单（`:focus-visible` 判别）+ `skipFocusOpen` 守卫 + `refocus()` |
| `sections/gb-science.liquid` | 新增 `cta_label` / `cta_url` 两个 setting + 卡片下方的 CTA 标记。**这是对方的文件**，本轮以当轮 pull 的线上版为基底改（与基线一致，没被人动过） |

#### 三方对比

`ours` 4、`CONFLICT` **0**、`theirs` 1（`config/settings_data.json` —— 主题编辑器托管，
**从不推**，不在清单里）。四个目标文件 baseline == remote，对方一个都没碰。

#### 验证

| 判据 | 结果 |
|---|---|
| 回读逐字节（4 个文件） | **全部一致**（含 `customstyle.css`） |
| 清单外附带改动 | **0** |
| 文件数 | 624 → 624 |
| `tools/r115live.py`（新） | **25 ok / 0 red** |
| `tools/menutab.py --live` | **45 ok / 0 red**（A–G 回归段全绿，新增的 H 段线上也全过） |

线上实测要点：`--build` 已是 `"20260908-r115"`；shipping 两张表在 1440 / 390
都是 **124 / opts-out**；reviews h1 的 `br.gb-br-wide` 在 **390 也 `display != none`**；
science 两个 section 正常渲染、6 张卡都在、**无 Liquid error**。

⚠ **`.gb-science__cta` 线上计数为 0 是预期状态，不是没生效** —— `cta_label` 留空就不渲染。
需求方本轮**没有授权推 `templates/page.science.json`**，所以那颗 Shop Now 要么由需求方
在主题编辑器里填（Science 第二个区块 → Button label / Button link），要么下一轮单独授权推一次 JSON。

⚠ **reviews h1 在 390 仍是 3 行，但断行确实生效了** —— 判据不能用行数，要读**行内容**：
现在的三行是「Aussies are / obsessed. / **Here's why.**」，改前是「Aussies are /
obsessed. Here's / why.」。第三行整句归位就是这次要的效果。行数不变是因为该页 hero
线上多带 `--lg`（HANDOFF 早已登记为「忽略」），30px 字在 350 的版心里放不下第一句。

⚠ **本轮 `customstyle.css` 回读是展开格式、与本地逐字节一致** —— 与 HANDOFF 第 915 行
记的「pull 回来是 Shopify 压缩过的单行」不同。压缩是**间歇性的**，写线上判据时
两种形式都要能匹配，别把某一次的形态当成常态。

**基线滚动**：`verify-r115` → **`baseline-20260908-r115`**（624 文件）。

---

### 第一二〇轮（2026-09-09，已推，经用户授权）—— 占位图灰底全部去掉

`$build` = `20260909-r120`。

#### 推送清单（2 个）

```
shopify theme push --store je1ka9-er.myshopify.com --theme 180348977399 \
  --path work-20260909-0129 \
  --only assets/customstyle.scss --only assets/customstyle.css \
  --nodelete --allow-live
```

| 文件 | 改了什么 |
|---|---|
| `customstyle.scss` / `.css` | 15 处占位媒体盒的灰底（13 × `$c-gray-200` + `.gb-crev-card__image` 的 `#d5d4d4` + `.gb-scallop-box` 的 `--box-bg` 默认值）全部去掉；`$build` → r120；清掉 8 段会诱导下一轮补回灰底的注释 |

静态站 3 个 HTML 的注释、新判据 `tools/placeholderbg.py`、`crevcheck.py` 与 `r119check.py`
的断言修正**只进 git，不推**。

#### 三方对比

`ours` 2、`CONFLICT` **0**、`theirs` 7（`blocks/_gb-guarantee.liquid` /
`sections/gb-form-section.liquid` / `gb-ingredients.liquid` / `gb-rich-page.liquid` /
`snippets/gb-promo-modal.liquid` / `templates/index.json` / `page.privacy-policy.json`
—— 逐个 diff 过，全与灰底无关：表单校验、schema 类型、页面内容开关、隐私链接）。
两个目标文件 baseline == remote，对方没碰。

#### 验证

| 判据 | 结果 |
|---|---|
| 编译器新鲜度 | 用 r119 源重编译与仓库 `customstyle.css` **逐字节一致** → 配置正确、产物不过期 |
| 产物 diff | **正好 46 行**，全部是 `$build` 版本号与 14 处 `background: #d9d9d9` / `#d5d4d4` 的删除 + `--box-bg` |
| 回读逐字节（2 个文件） | **全部一致** |
| 清单外附带改动 | **0**（624 → 624） |
| `tools/placeholderbg.py`（新） | 静态站 **50 ok / 0 red** |
| `tools/placeholderbg.py --live` | **40 ok / 0 red** |
| `tools/placeholderbg.py --strip` | **33 red** —— 反向注入灰底后判据确实转红，证明它在测东西 |
| 回归 | `crevcheck` all green / `crevlive` 30/0 / `r119check` 13/0 / `r119live` 8/0 / `rwd` 全绿 / `scrolllock` 44 条 0 failed / `r117check` 15/0 |

⚠ **回读时发现对方在推送窗口内改了 16 个文件** —— 不是本次推送造成的（我们只推 2 个 asset，
回读逐字节一致、清单外 0 改动）。其中一项直接关掉了本会话的第一条需求：
**`gb-app-section.liquid` 的 `step` default 4 → 6，两个 template JSON 的存值也 4 → 6**，
线上实测 `step=6`、点一次 5 → 11。**See More Reviews 那条对方自己做完了，我方零改动。**

**基线滚动**：`verify-r120` → **`baseline-20260909-r120`**（624 文件）。

---

### 第一二一轮（2026-09-09，已推，经用户授权）—— Escape 归还焦点不画 focus 样式 + 居中 hero 标题封顶

`$build` = `20260909-r121`。

```
shopify theme push --store je1ka9-er.myshopify.com --theme 180348977399 --path work-XXXX \
  --only assets/customstyle.scss --only assets/customstyle.css --only assets/main.js \
  --nodelete --allow-live
```

| 文件 | 改了什么 |
|---|---|
| `main.js` | 新增顶层 `returnFocus()`；header / modal / dropdown 三处归还焦点改用它 |
| `customstyle.scss` / `.css` | 全局 `.is-refocused:focus-visible{outline:none}`；`.gb-reel` 的 transform opt-out；`.gb-page-hero--center .gb-page-hero__title{max-width:990px}`；`$build` → r121 |

判据 `tools/refocusring.py`、`tools/r121check.py` 只进 git，不推。

#### 三方对比

`ours` 3、`CONFLICT` **0**、`theirs` 5（`sections/gb-ingredients.liquid` /
`gb-science.liquid` / `templates/index.json` / `page.our-story.json` / `page.science.json`）。
三个目标文件 baseline == remote，对方没碰。
⚠ 对方在动 `sections/gb-science.liquid` —— 正是 r120 记下的 science-card 语义化待决所在的文件，
下轮做那条前先重新 pull。

#### 验证

| 判据 | 结果 |
|---|---|
| 回读逐字节（3 个文件） | **全部一致** |
| 清单外附带改动 | **0**（624 → 624） |
| `tools/refocusring.py` | 静态 **24/0**、`--live` **24/0** |
| `tools/refocusring.py --strip` | **4 red**（反向注入焦点样式，4 个 case 全转红） |
| `tools/r121check.py` | 静态 **15/0**、`--live` **15/0** |
| 回归 | `menutab` 58/0 / `scrolllock` 44 条 0 failed / `placeholderbg` 50/0 / `r119check` 13/0 / `crevcheck` 全绿 |

⚠ **线上第一次 `r121check` 报 1 red，是判据 URL 写错**（`/pages/faqs` 是 404，线上为 `/pages/faq`），
**存活守卫抓住的**。修 URL 时行尾注释又吃掉了同一行的下一个列表项，项数从 15 掉到 13 ——
**计数暴露的，不是报错**。两处都已修，复跑 15/0。

**基线滚动**：`verify-r121` → **`baseline-20260909-r121`**（624 文件）。

---

### 第一二二轮（2026-09-09，已推，经用户授权）—— hero 入场改成一条时间线

`$build` = `20260909-r122`。推 `assets/main.js` + `customstyle.scss` + `.css`，
`--only` × 3 + `--nodelete` + `--allow-live`。

| 文件 | 改了什么 |
|---|---|
| `main.js` | `lineReveal.wireHero()`（运行时给 hero 注入 sequence hook）；`sequence()` 认 `[data-seq-step]`；`wowo.play()` 剥类时机改为 `1500 + 自身 delay` |
| `customstyle.scss` / `.css` | `[data-seq-step].wowo.animated` 的节拍延迟（0-3-0 压过 markup 里的 delay-in-N）；`$build` → r122 |

#### 三方对比

`ours` 3、`CONFLICT` **0**、`theirs` **0**（本轮窗口内对方没动手）。

#### 验证

| 判据 | 结果 |
|---|---|
| 回读逐字节（3 个） | **全部一致**，清单外 **0**，624 → 624 |
| `tools/heroseq.py` | 静态 **10/0**、390 档 **11/0**、`--live` **10/0** |
| `tools/heroseq.py --strip` | **6 red** |
| 回归 | `refocusring` 静态/线上各 24/0、`r121check` 15/0、`menutab` 58/0（复跑） |

⚠ **线上首跑 1 red 是判据采样时机**，不是没推上去：wowo 播完就剥 `.wowo`/`.animated`，
被测规则只在这两个类在时生效。判据已改成读之前临时加回再还原。
⚠ **别用 `/cdn/shop/t/2/assets/*` 查线上产物** —— 那是旧主题，css 停在 `20260907-r73`。

**基线滚动**：`verify-r122` → **`baseline-20260909-r122`**（624 文件）。

---

### 第一二三轮（2026-09-09，已推，经用户授权）—— reel 就地播放 + 删弹窗

`$build` = `20260909-r123`。**含一个对方的 liquid，用户逐次授权。**

```
shopify theme push --store je1ka9-er.myshopify.com --theme 180348977399 --path work-XXXX \
  --only assets/customstyle.scss --only assets/customstyle.css --only assets/main.js \
  --only sections/gb-reviews.liquid --nodelete --allow-live
```

| 文件 | 改了什么 |
|---|---|
| `main.js` | 删 `modal.playVideo/stopVideo/embedUrl`（98 行）与三处调用；新增 `reelPlayer` 模块（就地播放、一次只播一个） |
| `customstyle.scss` / `.css` | 删 `.gb-rv-*` 整块（171 行）+ 共享 focus 列表里的 `__close` + r121 的 reel opt-out；新增 `.gb-reel__trigger` / `__video` / `__embed` / `__offline`；`$build` → r123 |
| **`sections/gb-reviews.liquid`** | reel 卡片 `<button>` → `<div data-reel>` + 内层 `.gb-reel__trigger`；删整个 `.gb-rv-modal` 块。完整文件与 patch 存进 `liquid/` |

#### 三方对比

`ours` 4、`CONFLICT` **0**、`theirs` **0**。四个目标文件 baseline == remote —— 
**改 liquid 的基底与线上一致**，这点在推对方文件前必须先确认。

#### 验证

| 判据 | 结果 |
|---|---|
| 回读逐字节（4 个，含 liquid） | **全部一致**，清单外 **0**，624 → 624 |
| `tools/reelplay.py` | 静态 **23/0**、`--live` **20/0** |
| `tools/reelplay.py --strip` | **8 red** |
| 回归 | `r67reel` 26/0 / `rwd` 全绿 / `heroseq` / `r121check` 全绿 / `menutab` 58/0 / `crevcheck` 全绿 / `scrolllock` 36 条 0 failed |

⚠ **线上 3 red 已查明是内容不是代码**：product / our-story / how-gumi-works 三页
**各 10 张 reel 一个视频都没填**（首页 6 张填了）。判据已改成把它单列成
“theme-editor backlog” 汇总，不计 red。待办在 `docs/LIVE-BACKLOG.md` 第〇之三条。

**基线滚动**：`verify-r123` → **`baseline-20260909-r123`**（624 文件）。

---

### 第一二四轮（2026-09-09，已推，经用户授权）—— 修 r123 的 `[hidden]` 失效

`$build` = `20260909-r124`。只推 `assets/customstyle.scss` + `.css`，`main.js` 未改。

| 文件 | 改了什么 |
|---|---|
| `customstyle.scss` / `.css` | `.gb-reel__trigger` 补 `&[hidden] { display: none; }`（UA 的 `[hidden]` 是 0-0-0，输给它自己的 `display:flex`，r123 的播放按钮因此没真被收起）；`$build` → r124 |

#### 三方对比

`ours` 2、`CONFLICT` **0**、`theirs` **0**。两个目标文件 baseline == remote。

#### 验证

| 判据 | 结果 |
|---|---|
| 回读逐字节（2 个） | **一致**，清单外 **0**，624 → 624 |
| `tools/reelplay.py` | 静态 **25/0**、`--live` **22/0** |
| 反向（临时移除新规则再跑） | 新增的两条转红、旧断言仍绿 —— 证明补的正是缺口 |
| 回归 | `refocusring` / `heroseq` / `placeholderbg` / `r121check` 全绿 |

⚠ **判据补强**：原来只断言 `t.hidden`（属性值），那个在 bug 下一直是 `true`。
新增 `getComputedStyle(t).display === "none"` 与 `getBoundingClientRect() === [0,0]` 两条读**效果**。

**基线滚动**：`verify-r124` → **`baseline-20260909-r124`**（624 文件）。

---

### 第一二五轮（2026-09-09，已推，经用户明确指示）—— 无视频 reel 不渲染 + 填入视频

`$build` **不变**（仍 `20260909-r124`，css/js 未动）。

⚠⚠ **本轮推了 3 个 `templates/*.json`** —— 「绝不推」的红线文件，**需求方明确指示**才做。

```
shopify theme push --store je1ka9-er.myshopify.com --theme 180348977399 --path work-XXXX \
  --only sections/gb-reviews.liquid \
  --only templates/product.json --only templates/page.our-story.json \
  --only templates/page.how-gumi-works.json \
  --nodelete --allow-live
```

| 文件 | 改了什么 |
|---|---|
| `sections/gb-reviews.liquid` | 单卡守卫 `{% if video_url != '' %}` + 外层「一张可播的都没有就整条轨道不渲染」 |
| 三个 `templates/*.json` | 各 10 个 reel block 补 `"video": "shopify://files/videos/video-07.mp4"` |

**降低红线风险的做法**：当场 `theme pull` → 正则**只插入一行**（不用 `json.dump`，否则重排格式产生几百行无关 diff）→ 立刻推 → 回读逐字节核对。
三个文件的 diff **各只有 10 行新增**，这同时反证对方在窗口内没碰过它们。

#### 验证

| 判据 | 结果 |
|---|---|
| 回读逐字节（4 个） | **全部一致**，清单外 **0**，624 → 624 |
| `tools/reelplay.py --live` | **25/0**，theme-editor backlog 汇总**已消失** |
| **守卫真实验证** | 临时摘掉 our-story 一个 video → 推 → 线上实测 **9 张卡**（对照组 how-gumi-works 仍 10 张、轨道仍在）→ 推回原数据 → 复核 **10 张** |
| `theme check` | 我改的文件无 offense |

⚠ **需求方说「video 已填入」，但拉下来实测三页各 0 个** —— 已如实告知并说明后果，
需求方随即指示由我们直接填入。**先拉再信。**

**基线滚动**：新拉 → **`baseline-20260909-r125`**（624 文件）。

---

### 第一二六轮（2026-09-09，已推，经用户授权）—— reel 后台补竖版比例提示

`$build` **不变**（仍 `20260909-r124`）。只推 `sections/gb-reviews.liquid`。

| 文件 | 改了什么 |
|---|---|
| `sections/gb-reviews.liquid` | reel block schema：新增 `paragraph` 说明竖版 9:16 / 卡片 304×540 / 建议 1080×1920 / 横版会留黑边；`video`、`video_embed`、`poster` 三个字段 label 加「— portrait 9:16」并补 info。**`id` 一个都没改**，已存值不受影响 |

#### 三方对比

`ours` 1、`CONFLICT` **0**、`theirs` **0**。

#### 验证

| 判据 | 结果 |
|---|---|
| schema JSON | 提取 `{% schema %}` 段 `json.loads` 通过 |
| `theme check` | 我改的文件 **0 offense** |
| 回读逐字节 | **一致**，清单外 **0**，624 → 624 |
| 已存值 | `product.json` 回读仍 reel 10 / 已填 10 |
| `tools/reelplay.py --live` | **25/0** |

⚠ **实测记录**：占位视频 `video-07.mp4` 原始 **1276×720（16:9 横版）**，卡片 **304×540（9:16 竖版）**，
`contain` 下视频只占卡片高度 **32%**，上下各留约 184px 深色。**这是素材问题不是样式问题**，
提示已加在后台，等需求方按 9:16 重新上传。

**基线滚动**：`verify-r126` → **`baseline-20260909-r126`**（624 文件）。

## 2026-09-09（续）

| 轮次 | 推了什么 | 文件数 | 回读 | 基线 |
|---|---|---|---|---|
| **第一二七轮** | `assets/customstyle.css` / `.scss` / `main.js` | 3 | 4 ok / 0 red | 624 → **`baseline-20260909-r127`** |

#### 三方对比

`ours` **3**、`theirs` **5**、`CONFLICT` **0**。

⚠ **theirs 这次不是 0** —— 自 `baseline-20260909-r126` 起对方改了
`sections/gb-reviews.liquid`（`<figcaption>` → `<cite>`，就是需求方报的「斜体」真因）、
`sections/gb-header.liquid`（Shop now href 写死）、`snippets/gb-cart-drawer.liquid`、
`snippets/gb-cart-line-item.liquid`、`templates/page.reviews.json`。
**全部原样保留，一个都没覆盖** —— work 目录是从 prepush 拷的，推送清单按
`local != remote` 算而不是 `local != baseline`（后者会把对方的 5 个文件一起算进来推回去）。

#### 验证

| 判据 | 结果 |
|---|---|
| 产物新鲜度 | 重编译 scss 与仓库 css **逐字节相同** |
| 推前注入预演（线上专有的两条） | **8 ok / 0 red**，注入前 `CITE:italic` / `names=[null×5]`，注入后 `CITE:normal` / `gb-acc-0×5` |
| 回读逐字节 | 3 个**一致**，清单外 **0**，624 → 624 |
| 渲染版本 | `--build = "20260909-r127"`（证明浏览器真用上了，不是 CDN 旧副本） |
| `tools/clientlive5.py --live` | **13 / 0** |
| `tools/herousp.py --live` | **5 / 0**（全档 20px，板值 18.7） |

**基线滚动**：`verify-20260909-r127` → **`baseline-20260909-r127`**（624 文件）；
顺手清掉 `baseline-20260909-r120`～`r123` 四个旧快照。

| 轮次 | 推了什么 | 文件数 | 回读 | 基线 |
|---|---|---|---|---|
| **第一二八轮** | `assets/customstyle.css` / `.scss` / `main.js` | 3 | 4 ok / 0 red | 624 → **`baseline-20260909-r128`** |

三方对比 `ours` **3** / `theirs` **1**（`templates/page.how-gumi-works.json`，原样保留）/ `CONFLICT` **0**。
判据：`clientlive5.py --live` **20/0**、兜底守卫 **5/0**、渲染 `--build = "20260909-r128"`。
顺手清掉 `baseline-20260909-r124` / `r125` 两个旧快照。

| 轮次 | 推了什么 | 文件数 | 回读 | 基线 |
|---|---|---|---|---|
| **第一二九轮** | `assets/customstyle.css` / `.scss` / `main.js` | 3 | 4 ok / 0 red | 624 → **`baseline-20260909-r129`** |

三方对比 `ours` **3** / `theirs` **0** / `CONFLICT` **0**。
判据：`uifixes.py --live` **6/0**、`scallopedge.py --live` **3/0**（推送前对旧 PNG 跑是 **2 红**，
反向验证成立）、渲染 `--build = "20260909-r129"`。
顺手清掉 `baseline-20260909-r126` / `r127`。

| 轮次 | 推了什么 | 文件数 | 回读 | 基线 |
|---|---|---|---|---|
| **第一三〇轮** | `assets/customstyle.css` / `.scss` / `main.js` | 3 | 4 ok / 0 red | 624 → **`baseline-20260909-r130`** |

三方对比 `ours` **3** / `theirs` **1**（`sections/gb-app-section.liquid`，原样保留）/ `CONFLICT` **0**。
判据：`drawernav.py` 静态 **11/0** + 线上复跑 **11/0**、`menutab.py` **58/0**
（补 `scroll-padding-bottom` 前是 57/1，是本轮 sticky 引入的回归）、渲染 `--build = "20260909-r130"`。
顺手清掉 `baseline-20260909-r128`。

| 轮次 | 推了什么 | 文件数 | 回读 | 基线 |
|---|---|---|---|---|
| **第一三一轮** | `assets/customstyle.css` / `.scss` | 2 | 2 ok / 0 red | 624 → **`baseline-20260909-r131`** |

三方对比 `ours` **2** / `theirs` **0** / `CONFLICT` **0**（`main.js` 本轮没改，与线上逐字节相同）。
⚠ **本轮推了两次**：第一次推完线上判据 **25/3** —— 把 `padding-bottom` 从 `.gb-*__acc-row`
的基础规则里删掉后，**Horizon 给展开态的 `<summary>` 补了 11.2px**，位置被主题接管
（静态站测不出，只有线上 `open geometry` 判据看得见）。补回 `[open] > & { padding-bottom: 0 }`
再推，线上 **28/0**。
判据：`drawernav.py` 静态 **28/0** + 线上 **28/0** + `--reverse` **6 红**、
`menutab.py` **58/0**（删掉 r130 的 `scroll-padding-bottom` 后没有回归）、
线上回归 `clientlive5` 20/0 / `uifixes` 6/0 / `herousp` 5/0、渲染 `--build = "20260909-r131"`。
顺手清掉 `baseline-20260909-r129`。

| 轮次 | 推了什么 | 文件数 | 回读 | 基线 |
|---|---|---|---|---|
| **第一三二轮** | `assets/customstyle.css` / `.scss` / `main.js` | 3 | 3 ok / 0 red | 624 → **`baseline-20260909-r132`** |

三方对比 `ours` **3** / `theirs` **0** / `CONFLICT` **0**。
判据：`drawernav.py` 静态与线上各 **35/0**（`--reverse` 8 红）、`linereveal.py`（新，字体竞态）
静态四档 delay 全绿 + 线上 **5/0**、`menutab.py` 静态与线上各 **58/0**（注释掉
`scroll-padding-bottom` 仍 57/1，判据未削弱）、`uifixes.py` 静态与线上各 **10/0**、
`wraptruth.py` 120 次读数 **0 失配**、回归 `scrolllock` 36/0 / `rwd` 全绿 /
`clientlive5` 20/0 / `herousp` 5/0、渲染 `--build = "20260909-r132"`。
⚠ `revealcheck.py` **FAIL 12 是既有欠账**：用 r131 基线的 `main.js` 复跑，
逐条相同的 12 条 `ink-halo opacity 0`（同页、同档）。顺手清掉 `baseline-20260909-r130`。

| 轮次 | 推了什么 | 文件数 | 回读 | 基线 |
|---|---|---|---|---|
| **第一三三轮** | `assets/customstyle.css` / `.scss` | 2 | 2 ok / 0 red | 624 → **`baseline-20260909-r133`** |

三方对比 `ours` **2** / `theirs` **0** / `CONFLICT` **0**。
判据：`drawernav.py` 静态与线上各 **35/0**、`menutab.py` **58/0**。
顺手清掉 `baseline-20260909-r131`。

| 轮次 | 推了什么 | 文件数 | 回读 | 基线 |
|---|---|---|---|---|
| **第一三四轮** | `assets/customstyle.css` / `.scss` / **`sections/gb-header.liquid`** | 3 | 3 ok / 0 red | 624 → **`baseline-20260909-r134`** |

三方对比 `ours` **3** / `theirs` **0** / `CONFLICT` **0**。
⚠ **本轮推了 liquid**（加容器必然改 markup）。改的是从线上拉下来的那份，不是仓库副本。
判据：`drawernav.py` 静态与线上各 **39/0**、`menutab.py` **58/0**、`clientlive5.py` **20/0**、
`rwd` 全绿 / `scrolllock` 36/0。顺手清掉 `baseline-20260909-r132`。

## 2026-09-10

| 轮次 | 推了什么 | 文件数 | 回读 | 基线 |
|---|---|---|---|---|
| **第一三五轮** | `assets/customstyle.css` / `.scss` / `main.js` | 3 | 3 ok / 0 red | 624 → **`baseline-20260909-r135`** |

三方对比 `ours` **3** / `theirs` **0** / `CONFLICT` **0**。**本轮没有 liquid。**
判据：`cartfocus.py` **5/0**（`--strip` 转红 2 条）、`promotitle.py` **12/0**（摘掉 `inkSplit`
复跑 7 红）、`inkringlive.py --password 1234` **9/0**；回归 `refocusring` 18/0 / `rwd` 全绿 /
`scrolllock` 36/0 / `drawernav` 39/0 / `menutab` 58/0。顺手清掉 `baseline-20260909-r133`。

⚠ **线上回读没有碰 `/cart`** —— 那条路径挂着 Cloudflare 托管挑战，一碰会污染整个会话
（连首页一起挂住）。`inkringlive.py` 改为在**首页**注入一个带 `.gb-cart__close` 类的
夹具 `<dialog>` 并无手势 `showModal()`，与 `/cart` 落地页同形：同一份线上 main.js、
同一份线上样式表、同一套 `:focus-visible` 判定。真实抽屉的 dialog 也没开
（Horizon 打开时可能去取 cart section，那同样会碰 `/cart`）。

| 轮次 | 推了什么 | 文件数 | 回读 | 基线 |
|---|---|---|---|---|
| **第一三六轮** | `assets/customstyle.css` / `.scss` / `main.js` | 3 | 3 ok / 0 red | 624 → **`baseline-20260910-r136`** |

三方对比 `ours` **3** / `theirs` **0** / `CONFLICT` **0**。**本轮没有 liquid。**
`customstyle.scss` 本轮**只动了 `$build`** —— 样式零改动，升它是为了给 `main.js` 的 `?v=` 破缓存。
判据：`cartsplit.py --password 1234` **推送前 3 红 / 推送后 5 全绿**（同一判据、同一线上环境，
唯一变量是这次推送，这就是它的反向验证）；端到端走真实 `/cart`，1440 与 390 两档
「落地展开 → 点 close 关掉了」；`inkringlive.py` **9/0**；回归 `refocusring` 18/0 /
`cartfocus` 5/0 / `promotitle` 12/0。顺手清掉 `baseline-20260909-r134`。

⚠ **`tools/r135live.py` 改名为 `tools/inkringlive.py`** —— 原判据把 `$build` 写死成
`'r135' in build`，推完 r136 当场变红而站点无恙。改用 `>= 135` 比较。
**单轮判据别写死 `$build`、判据文件名别带轮次号**，这两条项目里早就写着，本轮又踩了一次。

| 轮次 | 推了什么 | 文件数 | 回读 | 基线 |
|---|---|---|---|---|
| **第一三七轮** | `assets/customstyle.css` / `.scss` / `main.js` / **`sections/gb-form-section.liquid`** | 4 | 4 ok / 0 red | 624 → **`baseline-20260910-r137`** |

三方对比 `ours` **4** / `theirs` **0** / `CONFLICT` **0**。
⚠ **本轮推了 liquid**（六个 `<option>` 写在 liquid 里，不推线上就还是只有 AU）。
**改的是从线上拉下来的那份，不是仓库副本** —— 两者有历史差异（privacy policy 链接的写法），
用锚点只替换 select 那三行，`diff` 核对过只有 select 变动。
判据：`phonecode.py` 本地与线上各 **22/0**（`--strip` 反向 10 红）；
回归 `rwd` 全绿 / `cartsplit` 5-0 / `inkringlive` 9-0。顺手清掉 `baseline-20260909-r135`。

⚠ **线上跑判据要先摘掉 `#promo-modal`** —— 它 4 秒自动弹出、遮罩拦截点击，
判据跑到第四个国家就超时。只设我们的 `sessionStorage['gb-promo-seen']` **不管用**：
线上开它的不是我们的 `promoModal`，是按 `data-promo-delay` 走的另一套。

| 轮次 | 推了什么 | 文件数 | 回读 | 基线 |
|---|---|---|---|---|
| **第一三八轮** | `assets/customstyle.css` / `.scss` / `main.js` / **`sections/gb-form-section.liquid`** | 4 | 4 ok / 0 red | 624 → **`baseline-20260910-r138`** |

三方对比 `ours` **4** / `theirs` **0** / `CONFLICT` **0**。
⚠ **又推了 liquid**（各国号码样例写在 option 的 `data-example` 上）。
**改的仍是从线上拉下来的那份**，用六个锚点逐个替换 option 行，`diff` 核对过只有这六行。
`customstyle.scss` 本轮**只动了 `$build`** —— 样式零改动，升它是给 `main.js` 破缓存。
判据：`phonecode.py` 本地与线上各 **34/0**（比 r137 多 12 条位数断言，`--strip` 反向 20 红）；
回归 `cartsplit` 5-0 / `inkringlive` 9-0。顺手清掉 `baseline-20260910-r136`。

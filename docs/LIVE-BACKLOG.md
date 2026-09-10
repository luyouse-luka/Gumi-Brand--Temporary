# 线上剩余项 —— 后台待填 与 待加通道

> 2026-09-04 第七十轮生成，承接 [LIVE-GAP.md](LIVE-GAP.md)。
> 第七十轮的决定：**只改 liquid，不碰 Online Store Editor 托管的 JSON**
> （`templates/*.json`、`sections/footer-group.json`、`config/settings_data.json`）。
> 推它们会覆盖对方在后台调过的一切。剩下的落在这里。

## 〇之前、提给对方：`gb-cart-scripts.liquid` 的降级打开会让抽屉关不掉（r136，2026-09-10）

**这一条我们已经在 `main.js` 里兜住了**（`cartDrawer.watchSplit()`），登记在此是因为
**根子在对方的文件里**，不改的话任何绕过组件的打开都还会分裂一次。

`snippets/gb-cart-scripts.liquid` 的 `openCartIfHash()`：

```js
if (typeof drawer.showDialog === 'function') { drawer.showDialog(); return true; }
var d = drawer.querySelector('dialog');
if (d && typeof d.showModal === 'function') { d.showModal(); return true; }   // ← 问题在这
```

`<theme-drawer>` 还没 upgrade 时 `showDialog` 不是函数，于是立刻走第二条、
用原生 `showModal()` 把 dialog 开了 —— 而原生方法永远存在，所以 `return true`，
下面那句 `setTimeout(tryOpen, 100)` 永远用不上。结果 `<dialog>` 开着而组件读作关闭，
`on:click="#cart-drawer/close"` 在 close 按钮和遮罩上双双 no-op，只有 Escape 能关。

**建议改法**（等组件就绪再决定走哪条）：

```js
var open = function () {
  var d = drawer.querySelector('dialog');
  if (typeof drawer.showDialog === 'function') { drawer.showDialog(); }
  else if (d && d.showModal) { d.showModal(); drawer.setAttribute('open', ''); }
};
if (window.customElements && customElements.whenDefined) {
  customElements.whenDefined('theme-drawer').then(open, open);
} else { open(); }
```

关键是**降级分支要把 `open` 属性一起设上**，让组件与 dialog 两半同步。

## 〇、⚠⚠ 手机菜单现在就缺三项 —— 后台补齐即恢复（r94 已推 liquid，2026-09-08）

`sections/gb-header.liquid` 从「一个菜单 + 用 `.gb-header__links-item--mobile` 隐藏桌面项」
改成了**两个独立菜单**（桌面一个、手机一个，CSS 各显其一）。原因：
**Shopify 的 link list 无法给单个菜单项加类名**，所以旧结构下手机端的顺序被钉死成
「先全部 mobile 项、再全部 desktop 项」，而稿上两者是交错的。

推送后手机端只会渲染 **Mobile menu** 这一个 link list，所以后台必须把它补成完整的六项：

| 顺序 | 条目 | 类型 |
|---|---|---|
| 1 | Shop | 普通链接 |
| 2 | How Gumi Works | 普通链接 |
| 3 | Science | 普通链接 |
| 4 | Reviews | 普通链接 |
| 5 | Learn more | **带子项**：Our Story / FAQs / Shipping / Referral Program |
| 6 | Get in Touch | **带子项**：Partners & Influencers / Press Inquiries / Careers |

Desktop menu 保持现在的三项（How Gumi Works / Science / Reviews）不变。

⚠ **已经在缺了，不是预警**：r94（2026-09-08）按需求方要求推了这个 liquid，而后台
Mobile menu 至今仍是 Shop / Learn more / Get in Touch 三项 —— 线上手机端**当前就少了
How Gumi Works / Science / Reviews**（1440 桌面端不受影响，仍是三项 Desktop menu）。
补齐上表六项即刻恢复，无需再推任何文件。

## 〇之四、⚠ 36 张 reel 卡等 9:16 竖版素材（r126）

r125 把三页 30 张卡的视频按需求方指示填成了与首页相同的 `video-07.mp4`（首页 6 张本来就是它），
**但那是 1276×720 的横版**，而 reel 卡片是 304×540 的竖版 —— `contain` 之下视频只占卡片
高度的 **32%**，上下各留约 184px 深色。

**要做的**：客户提供 **9:16 竖版**素材（建议 1080×1920），在主题编辑器逐张替换。
r126 已把这个要求写进后台 schema：区块顶部有一条说明，`Video` / `Or a hosted video URL` /
`Poster` 三个字段的名字后面都带「— portrait 9:16」。

⚠ **上传 hosted URL（YouTube/Vimeo）时要一并给 Poster**，且 poster 也要 9:16 —— 上传的 mp4
会自动取首帧，hosted 链接不会。

⚠ **判据不会因为这条转红** —— 它是素材不是代码。代码侧的取舍（要不要改成 `cover`）
在 `docs/PROJECT-STATUS.md`「第一二六轮新开的」，**未动，等拍板**。

## 〇之三、⚠⚠ 三个页面的 30 张 reel 卡没有视频，点了不动（r123 起暴露）

r123 把 reel 从「点开弹窗」改成「就地播放」。没有填视频的卡片**点击完全没有反应**
（在此之前是打开一个空弹窗，同样没用，只是看起来像在做事）。

| 页面 | reel 卡 | 已填视频 |
|---|---|---|
| 首页 `templates/index.json` | 6 | **6** ✅ |
| 产品页 `templates/product.json` | 10 | **0** ❌ |
| Our Story `templates/page.our-story.json` | 10 | **0** ❌ |
| How Gumi Works `templates/page.how-gumi-works.json` | 10 | **0** ❌ |

**怎么填**：主题编辑器 → 对应页面 → Customer Reviews（`gb-reviews`）→ 每个 Reel 区块 →
**Video**（上传 Files 里的 mp4）或 **Or a hosted video URL**（YouTube / Vimeo，纯文本不是链接字段）。
填了 hosted URL 的还要给 **Poster**，上传的 mp4 会自动取首帧。

⚠ **首页那 6 张现在全指向同一个文件** `shopify://files/videos/video-07.mp4` ——
能播，但 6 张卡放的是同一段视频。客户给到真素材后要逐张换掉。

⚠ **判据不会因为这条转红** —— `tools/reelplay.py` 把它单列成 backlog 汇总，
因为这是内容不是代码。跑完看输出末尾的 “theme-editor backlog” 一段。

## 〇之二、promo 绿卡的 Arc text 请在后台清空（r91）

`templates/product.json` → `promo` → 第一张卡（`variant: green`）的 **Arc text** 现在是
schema 默认值 `"OUR PROMISE"`。稿里绿卡**没有弧**，而 `gb-promo.liquid` 不分 variant 都画，
于是线上多了一条绿底绿字的隐形弧 —— 它是个 452px 宽的盒子，把 copy 半边顶宽了
（768 档实测两个半边变成 364 / 395，卡片不再 50/50，1024 / 768 两档整卡还高出 62 / 66px）。

r91 的 CSS 已经 `display: none` 挡住它，功能上没问题。**更干净的做法**是在主题编辑器里
把绿卡的 Arc text 清空 —— 那样内容与稿一致，不靠样式兜底。
⚠ **r91 已把 `variant == 'white'` 判断推上线**，所以绿卡现在无论后台填什么都不会画弧了 ——
这一条降级成「后台数据整洁度」，不再是视觉问题。

## 一、现在就能在后台做完的（不需要我们再改代码）

### 0 之二、主题字体设置全都还是 Inter（r119 查到的根因）⚠ 决定要不要全站统一

后台 **Online Store → 主题 → Typography** 的字体没有指向 PP Palma —— 它是自定义字重文件，
Shopify 的字体选择器里选不到，所以主题的 **15 个字体族变量全是 `Inter, sans-serif`**：

```
--font-body--family        --font-heading--family     --font-paragraph--family
--font-subheading--family  --font-accent--family      --font-h1..h6--family
--button-font-family-primary / -secondary
--cart-primary-font-family / --cart-secondary-font-family
```

后果：**靠继承拿字体的元素**（`body` 被我们写死了品牌栈）看着正常，
**点名字体变量的 Horizon 原生组件**一律退回 Inter —— 价格、`Sale` 角标、
skip link、`Filter` 按钮都属于后者。

- **r119 已修 `/collections/all`**：在 `#MainContent[data-template^="collection"]` 上
  整组重声明这 15 个变量。
- **仍是 Inter 的地方**：`/404` 的商品列表（价格 + 角标；标题与按钮 r107 已单独写死）、
  `<body>` 顶部的全站 skip link，以及将来任何跑 Horizon 原生组件的模板。
- ⚠ **后台改不了这一条** —— Typography 选不到自定义字体。真正的两条路：
  ① 需求方拍板「全站统一」，我们把这 15 个变量提到 `:root`/`body` 一层（一条改动、影响全站，
  需要一轮完整回归）；② 维持现状，逐模板钩子覆盖（每加一个 Horizon 模板就要补一次）。
  **等需求方选。**

### 0. Contact 两处链接指错页（r117 需求方提出）⚠ 代码里改不了

需求方要求 Contact 指向 **`/pages/contact`**，线上两处现在都指向 `/pages/get-in-touch?type=contact`。
**两处都是后台数据，主题文件里没有可改的地方**：

| 位置 | 数据在哪 | 怎么改 |
|---|---|---|
| header 菜单 | `section.settings.desktop_menu` / `mobile_menu` = Shopify **导航菜单** | 后台 → 网店 → 导航 → 改那一项的网址 |
| footer 链接区 | `sections/footer-group.json` 的 `link_4_url` | 主题编辑器 → Footer → 第 4 条链接 |

⚠ `sections/gb-footer.liquid` 里那个 `"link_4_url": "/pages/get-in-touch?type=contact"` 只是
**schema 的 default**，`footer-group.json` 里已有存值，**改 default 不生效**，别去推它。
要我们代推只能推 `footer-group.json`（红线，需逐次授权）。

⚠ 顺带：静态站两处写的是 `get-in-touch.html?type=contact`，静态站**没有 contact.html**。
改线上之前先确认 `/pages/contact` 是不是真要用的那一页 —— 当初「预填咨询类型」那套
（`?type=contact` 传参 → `enquiryPrefill` 读取）是照搬 Funky 站点的做法，换页会让这条链路失效。


### 1. 首页评价区标题少了换行 ⚠ 这是线上的真 bug

`templates/index.json` → `reviews` → Title 当前值：

```
Aussies are obsessed.Here's why.
```

两句直接粘在一起，中间既没有空格也没有换行。`page.how-gumi-works.json` 的同一 section
是对的（`Aussies are obsessed.\nHere's why.`）。

**怎么改**：后台 → 首页 → Gumi Reviews → Title，在 `obsessed.` 与 `Here's` 之间换行。
`gb-reviews.liquid` 已经是 `escape | newline_to_br`，填了就会断行。
静态站这一处是**裸 `<br>`（桌面端也断行）**，所以这里保持现状即可，不需要窄屏专用换行。

### 2. 四个模板没挂 `gb-product`

`sections/gb-product.liquid` 只挂在 `product.json`。静态站另有 4 页带这个区块：

| 页面 | 静态站的形态 | live 模板 |
|---|---|---|
| 首页 | `gb-product gb-product--lg` | `index.json` 无 |
| Reviews | `gb-product` | `page.reviews.json` 无 |
| How Gumi Works | `gb-product` | `page.how-gumi-works.json` 无 |
| Our Story | `gb-product` | `page.our-story.json` 无 |

**怎么改**：后台对应页面 → 添加区块 → Gumi Product，拖到静态站里的位置。
⚠ **这是直接改线上外观**，加之前先确认位置与要绑定的产品。首页那个还要选 `--lg` 变体
（如果 section 有对应 setting；没有的话需要我们加，见下）。

### 3. 店名还是 Shopify 默认占位 ⚠ 第七十一轮线上实测发现

footer 版权行渲染出来是 `© 2026 My Store` —— `{{ shop.name }}` 取的是店铺设置里的名字，
现在还是 Shopify 建店时的默认值 `My Store`。

**怎么改**：Shopify 后台 → Settings → Store details → Store name 填成 Gumi 的正式名称。
不是代码问题，改完全站 footer 一起生效。

## 二、需要我们先加「通道」，之后才能后台填的

这些不是后台填不填的问题 —— **liquid 现在根本没有接收口**，填了也不会生效。
第七十轮按需求方决定没做（只做了确定无疑的三条），要做的话是下一轮的事。

| # | 想要的效果 | 卡在哪 | 要加什么 |
|---|---|---|---|
| 1 | footer tagline 的 2 处窄屏换行（11 页共 22 处） | tagline 是 richtext，后台按 shift+enter 产出的是**裸 `<br>`**，全断点都断；静态站要的是仅 ≤767 断 | `gb-footer.liquid` 加 `replace: '<br>', '<br class="gb-br-narrow">'` |
| 2 | page-hero 标题换行（faq、how-gumi-works） | `title` 是 `text` 类型 + `| escape`：单行输入框**输不进换行**，HTML 也会被转义成字面文字 | schema 的 `title` 改成 `textarea`，输出加 `newline_to_br` + `replace` |
| 3 | Reviews 页 hero 顶部的 overline（星级 + `123,456+ happy customers`） | `gb-page-hero.liquid` 完全没有这个节点 | 加 `overline` text setting（default 留空，否则用到 page-hero 的 7 个页面会全都冒出来）+ 星级 SVG |
| 4 | faq 的 `--lh-24`、privacy 的 `--privacy-mobile` 行高微调 | 逐页修饰类，liquid 里没有开关 | 加 `lead_style` select setting（default 空） |

⚠ 第 1、2 项会**改变对方 section 的输入契约**（原本是纯单行文本），
且在他们真去后台填之前，线上看不出任何变化。

## 三、不用做的（查证过，别再列进来）

| 条目 | 为什么不用做 |
|---|---|
| `gb-acc-body__media` | 对方 2026-09-04 早上补的 `gb-product.liquid` 里已经有了 |
| `gb-logo-scroll__img--abc` / `--vogue` / `--wellbeing` | 线上有 `class_suffix` setting，`index.json` 三个 block 的值也都填好了。类名由 `{% assign %}` 拼出，literal 搜不到而已 |
| `gb-stats.title` 的换行 | 静态站本来就是裸 `<br>`（全断点断行），线上写法**正确** |
| `gb-rv-panel__glyph` | 第六十六轮已适配：`customstyle.scss:1888` 特意把规则挂在 `svg` 而不是这个 wrapper 上，就因为线上是裸的。补上 wrapper 反而破坏那条假设 |
| 52 个本地图不在线上 `assets/` | 线上走 `image_picker` + `image_url`（Files/CDN），15 个已绑定的图片设置全部非空 |

## 四、六个模块级缺口（不在本轮范围，仍未做）

营养标签弹窗 `gb-nl-*` / 首单 promo 弹窗 / PDP promo 卡 / PDP 对比表 `gb-vs` /
testimonial 卡 / shipping 表格 `gb-rich-table`。逐条在 [LIVE-GAP.md](LIVE-GAP.md) 第一节。
这些要新写 section 或 snippet，工作量与风险都比本轮大一个量级。

## 五、横在所有验收前面的一件事

**店铺开着 storefront 密码保护**，外部访问渲染 `layout/password.liquid`。
第七十轮那三处改动**视觉上一条都没验过** —— 判据只能证明 liquid 的结构与 token 正确。
⚠ **密码是 `1234`**，第六十四轮就拿到过（见 CHANGELOG 第六十四轮），当时误记为
「需向需求方要」，白等了两轮。第七十一轮起用 `tools/liveprobe70.py --password 1234`
可直接对线上做时序与 DOM 探测。

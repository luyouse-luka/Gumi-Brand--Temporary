# 线上剩余项 —— 后台待填 与 待加通道

> 2026-09-04 第七十轮生成，承接 [LIVE-GAP.md](LIVE-GAP.md)。
> 第七十轮的决定：**只改 liquid，不碰 Online Store Editor 托管的 JSON**
> （`templates/*.json`、`sections/footer-group.json`、`config/settings_data.json`）。
> 推它们会覆盖对方在后台调过的一切。剩下的落在这里。

## 一、现在就能在后台做完的（不需要我们再改代码）

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

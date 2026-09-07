# 静态站 ↔ live 主题 差距报告

> 2026-09-04 生成。live 快照 `Gumi-Brand-shopify/live-20260904-1134/`（`theme pull` 自
> `Dev #180348977399`，role = live）。判据脚本 `tools/livediff.py` / `livepages.py` / `livesect.py`，
> 三个都接受 live 目录作参数，随时可复跑。

## 结论

**「除了购物车其他都完成了」不成立**。除 cart drawer 外，还有 **6 个模块 + 2 类挂载点**
线上没有 liquid。已完成的部分覆盖了 11 页的主干区块，缺的集中在**弹窗、PDP 下半页、
以及 `gb-reviews` 内部的 testimonial 卡**。

另有一项与本次比对无关但当场发现的：**`$build` r68 从未推上 live**，线上停在 r67。

## 一、模块级缺口（线上全文搜不到这些类名）

| 模块 | 静态站位置 | 说明 |
|---|---|---|
| `gb-cart` / `gb-cart-item` | 11 页（header 图标触发） | 购物车抽屉，54 个 token。⚠ 见下方「购物车的实际状态」 |
| `gb-nl-*`（12 个块） | index / pdp / reviews / our-story / how-gumi-works | **营养标签弹窗**，26 个 token。`gb-nutrition` section 本身在线上，点开的弹窗没有 |
| `gb-promo-modal` / `gb-promo-panel` | index | 首单 20% off 邮箱换码弹窗，24 个 token |
| `gb-promo` / `gb-promo-card` | pdp | PDP 的两张 promo 卡（绿卡 / 白卡），22 个 token |
| `gb-vs` | pdp | Gumi vs Others 对比表，18 个 token |
| `gb-rich-table` | shipping | 配送表格，3 个 token。`gb-rich-page` 在线上，表格没有 |
| `gb-testimonial` / `gb-testimonials` | index / our-story / how-gumi-works | 评价卡片，在 `gb-reviews` **内部**。section 在线上，这块内容没有 |
| `gb-app-section` / `gb-product__app-slot` | pdp / reviews / 另 3 页 | 评论 app 的挂载点。空容器 + 标题，app 接进来时才用得上 |

## 二、模板挂载缺口（section 文件存在，但没挂进模板）

`sections/gb-product.liquid` 只挂在 `product.json`。静态站另有 4 页带这个区块：

| 页面 | 静态站 | live 模板 |
|---|---|---|
| index | `gb-product gb-product--lg` | `index.json` 无 |
| reviews | `gb-product` | `page.reviews.json` 无 |
| how-gumi-works | `gb-product` | `page.how-gumi-works.json` 无 |
| our-story | `gb-product` | `page.our-story.json` 无 |

这类缺口只需在模板 JSON 里加一条 section 记录，不用写新 liquid。

## 三、零碎缺口

> ⚠ **第七十轮逐条查证过这一节，10 条里只有 3 条是真的**（已做），
> 4 条是假信号或已适配，3 条需要先加 liquid 通道。
> **动手前先读 [LIVE-BACKLOG.md](LIVE-BACKLOG.md)**，别照着下面这张表直接修。

- **`gb-br-narrow` / `gb-br-wide` 全站缺失** —— 这是响应式强制换行的辅助类
  （`<br class="gb-br-narrow">`），静态站 11 页都在用。线上文案由 schema setting 填，
  换行点因此丢失，**手机端折行会与稿不一致**。
- `gb-page-hero__lead--lh-24`（faq）/ `gb-page-hero__lead--privacy-mobile`（privacy）/
  `gb-page-hero__overline` —— page-hero 的三个逐页微调修饰类线上没有。
- `gb-logo-scroll__img--abc/--vogue/--wellbeing` —— 三个媒体 logo 的逐个尺寸修饰类。
- `gb-stats__arrow--1..4` —— stats 区块的四个装饰箭头。
- `gb-acc-body__media`（faq 手风琴内的图）/ `gb-reviews__disclaimer` / `gb-rv-panel__glyph`。

## 三之二、缺一个 section = 连带缺一条波浪 ⚠（2026-09-07 第七十四轮补）

**波浪是上方 section 的最后一个子元素**，不是独立兄弟。所以上表里任何一个「线上没有」的
section，都会连带让**下一个区块的上边缘波浪一起消失**，视觉症状是那条边变成直的。

已确认两处（用户报的「gb-faq 波浪消失」就是这个）：

| 页面 | 静态站 faq 上方 | 线上 faq 上方 | 缺的是 |
|---|---|---|---|
| pdp | `.gb-app-section`（含 `--edge --cream-to-mint`） | `.gb-reviews` | `gb-app-section` 没有 liquid |
| how-gumi-works | `.gb-product`（含 `--edge --white-to-mint`） | `.gb-reviews` | `gb-product` 没挂进模板 |

⚠ **不要给 `.gb-faq` 补一个自己的波浪** —— 区块补回来时会变成两个。
正解是补回上方的 section（how-gumi-works 在后台加 `gb-product` 即可，见 LIVE-BACKLOG 一·2）。

判据：按**几何相邻**判断归属（波浪底边 ≈ 目标区块顶边，容差 6px），
不能按 DOM 兄弟找 —— 线上隔着 Shopify 的 section 包裹层。

## 四、购物车的实际状态（比「没做」更需要注意）

> ✅ **2026-09-07 已完成，本节整段作废**。对方当天分两步做完了购物车：
> 先把图标改成原生抽屉的触发器（`<cart-icon class="gb-header__icon-wrap">` +
> `<button on:click="#cart-drawer/toggle">` + `{% render 'cart-bubble' %}`，
> `theme.liquid` 放开 `cart-drawer`、`settings_data.json` 开 `auto_open_cart_drawer`）；
> 随后新增 `snippets/gb-cart-drawer.liquid` + `gb-cart-line-item.liquid` +
> `gb-cart-scripts.liquid`，**把 Gumi 的整套 `.gb-cart*` 结构原样搬进 Horizon 的
> `<theme-drawer>` → `<dialog>` → `cart-drawer-component` → `cart-items-component`**，
> 自动开启、数量增减、`/cart/change.js` 的 morph 全部保留。
> 所以第一节表里「`gb-cart` / `gb-cart-item` 线上没有」也已作废。
>
> 第七十七轮用纯 CSS 把它还原成静态站的外观并抬到 header 之上，
> 逐条与「别报成 bug」在 [HANDOFF.md](HANDOFF.md) 1j。
> 角标的定位问题与修法见 CHANGELOG 第七十五轮。
>
> **下面这段是历史记录，描述的是 2026-09-07 之前的状态。**

线上不是简单地缺购物车，而是**装了另一套**：

- `layout/theme.liquid:172` 渲染了 Horizon 原生 `{% render 'cart-drawer' %}`，
  `settings_data.json` 里 `cart_type: "drawer"`
- 但 `sections/gb-header.liquid:18` 的购物车图标写的是 `<a href="{{ routes.cart_url }}">`,
  **不是原生抽屉的触发器**，也不是静态站的 `data-modal="gb-cart"`

源码上看，点图标会跳转到 `/cart` 页面，原生抽屉不会打开。⚠ 店铺有 storefront 密码保护，
**这一条没能实测确认**，只是读源码的推断。要落地 `.gb-cart` 的话，图标那行也要一起改。

## 五、不是差距的（别报成 bug）

- **52 个本地图片 / 视频不在线上 `assets/`** —— 线上走 `image_picker` + `image_url`
  （Files/CDN），19 个 image_picker、80 处 `image_url`。**15 个已绑定的图片设置全部非空**，
  没有「模块在、图没传」的情况。
- **`gb-scallop--*` / `gb-stat--*` / `gb-reviews--*` 等修饰类"缺失"** —— 线上写成
  `gb-scallop--{{ s.trailing_scallop }}`、`gb-stat--{{ b.variant }}`，由 schema setting 拼出来，
  literal 搜不到。`livesect.py` 已抑制这类前缀，但抑制不彻底的仍会露头。
- **波浪归属看起来对不上** —— 线上把波浪做成了 section 的 `leading_scallop` /
  `trailing_scallop` setting，静态站是写死的。**架构差异，不是缺口**。
- **`blocks/` 下 0 个 `gb-*`** —— 对方早先把 25 个 gb block 搬进了 `sections/`，见 HANDOFF 头部。
- **119 个线上独有 assets** —— Horizon 4.1.5 基底自带。
- **45 个 SVG 的 CRLF/LF 差异** —— 判据脚本已按 `\r\n → \n` 归一，不再报。

## 六、判据怎么跑

```bash
cd /home/ly/project/Gumi-Brand
LIVE=/home/ly/project/Gumi-Brand-shopify/live-20260904-1134

python3 tools/livediff.py  "$LIVE"   # 类名集合差集，块级缺口
python3 tools/livepages.py "$LIVE"   # 11 页 <main> 区块序列 vs 模板 section 序列
python3 tools/livesect.py  "$LIVE"   # 两边都有的 section，内部 token 差异
```

⚠ 三个脚本的已知局限，写判据时要知道：

1. **live 侧扫全文而非 `class="..."`** —— Liquid 用 `{% assign classes = 'gb-x' %}` 和
   `{% form class: 'gb-form' %}` 造类名。只扫 class 属性会虚报一堆基础块缺失
   （第一版就是这么错的）。代价是注释里的类名也会算作"存在"。
2. **`livepages.py` 靠缩进找 `<main>` 直接子**，不是 HTML 解析 ——
   SVG 的自闭合标签会把解析器的深度计数搞乱，`<path>` 会被当成 main 的直接子。
   页面重新格式化后这个探针会失效，脚本里有断言会当场报错，不会静默出错结果。
3. **`livesect.py` 会跟进 `{% render %}`** —— 不跟进的话 `gb-sub__*`（在
   `snippets/gb-sub.liquid` 里）会虚报 26 条缺失。
4. **三个脚本都只比源码，不比渲染结果** —— 店铺有 storefront 密码保护，
   外部访问渲染 `layout/password.liquid`。**这份报告生成时视觉层一条都没验过。**
⚠ **密码是 `1234`**（第六十四轮就拿到过，见 CHANGELOG）—— 当时误记为「需向需求方要」，
第七十一轮起已能用 `tools/liveprobe70.py --password` 直接验线上。

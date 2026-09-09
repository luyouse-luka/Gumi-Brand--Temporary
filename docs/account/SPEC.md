# Gumi Account — 设计文档

2026-09-04 立项。Gumi Brand 的账户中心，**独立开发**（客户要求以后能整块复用结构），
引用已开发站的公共组件与视觉体系。

## 1. 定位与边界

- 设计源 SECTION **`2284:27077`**「✅Account Section Mobile (21/08/26)」，
  在页面 `401:29271`「Website - Desktop & Mobile MVP ✅」下 —— **READY FOR DEV**，正式交付稿
- 全量落盘在 `figma/account/`，**开发期间不需要再调 Figma API**（索引见该目录 README.md）
- 与 MVP 11 页共用 header / footer / 色板 / 字体 / 断点体系，但**代码独立**

**不做的**（沿用现站已确立的边界 + 本轮新增）：

| 不做 | 原因 |
|---|---|
| 真实订阅数据、真取消 / 跳过 / 改期的后端调用 | Shopify + 订阅 app 的职责，前端只做壳与交互 |
| 稿里的 `Chrome browser` INSTANCE（手机浏览器栏、home indicator） | 假舞台，不是页面的一部分 |
| 左侧导航的灰色圆点图标 | 便签 `27602` 原话：待设计图标的**占位**，不是最终件 |
| `400:18907`「Account Wire Frame」里的任何东西 | 竞品调研板（Grüns / Athletic Greens / HiSmile / Huel），不是 Gumi 的稿 |
| `2121:17567`「OLD - Account Section Mobile」 | 旧版，14 条评论标的增删是相对它说的 |

## 2. 已定决策（2026-09-04 用户拍板）

| # | 决策 | 取舍 |
|---|---|---|
| 1 | **公共 header 不动**，account 页单独覆盖 | 稿里的 header（logo 左 + 人形 + 汉堡、浅绿底）与现站不同，是**功能性差异**：便签 `34518` 说汉堡打开的是 **account 菜单**，不是站点菜单 |
| 2 | **公共 footer 不动**，account 页跟现站一致 | 稿的 footer 内容不同（两栏平铺、多 Snapchat、按钮文案 `Subscribe now`），差异登记待裁决 |
| 3 | 桌面弹窗**沿用站内既有机制，居中卡片** | 21 类动作弹窗只有手机稿，桌面无稿 |
| 4 | **静态页 + 独立 `account.css` / `account.js`**，与现站同仓 | — |
| 5 | `account.scss` **自带一份变量副本** | 不动 `customstyle.scss`。代价是漂移风险，以 `tools/acctvars.py` 判据兜底 |
| 6 | `account.js` **自包含**，不调 `window.gumi` | 见 §4 的并存说明 |
| 7 | **单页多视图**（照搬 funkyfood） | 客户要复用结构，整块搬走最方便 |
| 8 | Log in / Sign up **独立两页**，共用 account 的 css/js | 未登录态 header 不同（多 `Shop now` 按钮），且对得上 Shopify `customers/login` 路由 |

## 3. 交付物

```
account.html                单页多视图：Overview / Subscriptions / Subscription Detail
account-login.html          未登录态
account-signup.html
assets/account.scss         样式源，自带变量副本
assets/account.css          编译产物（双写，勿手改）
assets/account.js           自包含 IIFE
tools/acctvars.py           变量漂移判据
docs/account/SPEC.md        本文
docs/account/CHANGELOG.md   变更记录（约 10 项一条）
docs/account/HANDOFF.md     交接（含「不要报成 bug 的清单」）
```

- 类名前缀 **`.gb-acct-`** —— 与现站 39 个分区隔开，便于整块拆走
- 编译：`npx sass@1.77.8 assets/account.scss assets/account.css --no-source-map`
- 破缓存：account 自己的 `$build`，与现站的 `$build` 独立

## 4. 两个 JS 并存

account 页**同时加载** `main.js` 与 `account.js`，两者不互相调用：

| 脚本 | 负责 |
|---|---|
| `main.js`（现站，15 模块） | 公共 header / footer 的**站点**交互：Menu 展开、购物车抽屉、平滑滚动 |
| `account.js`（新，自包含） | account 视图切换、account 汉堡菜单、19 类弹窗、表单校验 |

- hook 用 **`data-acct-*`**，绝不复用样式类，也不与 `main.js` 的 `data-modal` 撞名
- 结构照 `js-init-module-data-hook-convention`：IIFE + `'use strict'` + 早退守卫
- ⚠ **新增任何 `overflow-y:auto` 的容器**（弹窗内滚动、多产品列表）必须登记进
  `main.js` 的 `smoothScroll.PREVENT`，否则 Lenis 吃掉滚轮 —— 这是唯一需要碰 `main.js` 的地方，
  届时单独申请

## 5. 视图与页面

### account.html 的三个视图

| 视图 | 桌面源 | 手机源 |
|---|---|---|
| Account Overview | `2284:27678` | `2284:27604`（整页）+ `27450`/`27499`/`27548`（三种订单状态弹层） |
| My Subscriptions（列表） | `2284:28000`（同屏三态） | `2284:28305`（同屏三态）、`34046`（Cancelled + Paused 两态） |
| Subscription Detail | `2284:27792`（ACTIVE） | 见下表 11 个变体 |

**Subscription Detail 的 11 个手机变体**（状态判读见 `figma/account/PAGES.txt`）：

| 节点 | 高 | 状态 | 特征 |
|---|---|---|---|
| `2284:28330` | 2902 | ACTIVE | 基准态，Add Items + Discounts + Add a discount code |
| `2284:28478` | 2902 | ACTIVE | 已加折扣码 —— 文案变 **Edit** discount code（便签 `30921`） |
| `2284:28627` | 2834 | PAUSED | — |
| `2284:28774` | 2882 | PAUSED | 与 `28627` 差 48px，差异待逐个比对 |
| `2284:34058` | 2800 | CANCELLED | Restart Subscription |
| `2284:34352` | 2902 | ACTIVE | 由 cancelled 转回 active |
| `2284:27202` | 2701 | Cancelled | — |
| `2284:27304` | 3070 | — | 含 **Promo code discount** 行 |
| `2284:27081` · `27116` | 2206 | — | 两个等高，差异待比对 |
| `2284:27151` | 1820 | — | 最矮，疑为单产品态 |
| `2284:27170` | 2100 | — | — |

⚠ 后五个 frame **稿上没有状态标签**，归属需在实现前逐个比对确认，不靠高度猜。

- **桌面**：左侧竖导航 + 右侧内容卡
- **手机**：导航变成**页内列表卡片**（`27604`）+ 右上角汉堡下拉面板（`34757`）——
  **两套并存，不是同一套折叠**

### Overview 的三种订单状态（便签 `27600`）

| 状态 | 含义 | 稿 |
|---|---|---|
| Preparing | 已付款 | `2284:27450` |
| Shipping | 已履约发货 | `2284:27499` |
| Renewal | 仍可编辑 | `2284:27548` |

### 订阅状态

ACTIVE / PAUSED / CANCELLED 三态（`28000` 桌面列表同屏展示三张卡）。

- **PAUSED**：便签 `28321`+`34038` —— 与 active 一样，只多一个 paused 标签，
  续订日期设为暂停到期日；**Skip next order 按钮要移除**（便签 `34042`）
- **CANCELLED**：便签 `28323` —— Re-Activate 进入重启流程，**续订日期移除**；
  重启要到次日才能操作（便签 `34040`）

## 6. 弹窗清单（30 个态 / 13 类）

完整文案见 `figma/account/MODALS.txt`。⚠ 该文件列了 41 个 390x840 frame，
其中 **7 个是页面态不是弹窗**（Account Overview above-the-fold x3、My Subscriptions x2、
Navigation x1、Container x1），`Navigation Expanded` 是汉堡面板归 header。真弹窗是 30 态 / 13 类。弹窗本体是 frame 的最后一个 child，
其上的 `Rectangle` 是遮罩，`Chrome browser` 是假舞台。

| 类 | 态数 | 尺寸（手机） | 关键规则 |
|---|---|---|---|
| Cancel Subscription | 7 | 390×672 | **7 屏挽留链**，见下 |
| Edit Shipping | 4 | 254–672 | 地址表单 + Success 态 |
| Add Product | 3 | 390×672 | QTY 0 时按钮变「remove this product」（便签 `34504`） |
| Edit Product | 3 | 390×672 | 最后一个产品 QTY 不能减到 0（便签 `34502`） |
| Add A discount Code | 3 | 246–292 | 码不存在时按钮**不变绿**（便签 `30919`）；已有码时文案 add→edit（便签 `30921`） |
| Edit Name | 2 | 390×246 | — |
| Edit Date | 1 | 390×290 | 选下次续订日，其余日期按频率顺推（便签 `30911`）；**须是完整的未来一天**（便签 `30923`） |
| Edit Frequency | 1 | 390×290 | 选项：2 / 4 / 6 周（便签 `30925`） |
| Edit Payment Method | 1 | 390×256 | 发邮件改支付方式；便签 `34508` 要求发件域名不能像诈骗 |
| Skip Next Order | 1 | 390×236 | 只能跳过下一单；跳过后显示为 deactivated（便签 `30907`） |
| I need it now | 1 | 390×256 | 保持频率，按所选时间调整日期（便签 `30909`） |
| Edit Product - only one product | 1 | 390×672 | 阻止删除最后一个产品 |
| Restart subscription | 1 | 390×329 | — |

### 取消流程 7 屏（便签 `34512`·`34514`·`34516`）

```
29596  挽留：先劝跳过 1 / 2 单        → Cancel now | Continue to Skip
29767  跳过成功                        → Done
29928  原因选择（5 项）
30286  原因选择（同上，另一变体）
30107  原因选择（⚠ 稿里「I have too much product」重复了两次，是稿的 bug）
30465  选「Going away」→ 假期暂停日历，选恢复日期
30740  选「Too expensive」→ 20% off 挽留
```

- **「I have too much product」及其后的选项没有第二屏**，选完直接取消（便签 `34512`）
- 取消数据要记录：谁、为什么（便签 `34516`，「Like funky cancellation data」）
- 20% off 是在订阅折扣之上再加一档（便签 `34514`）

## 7. 待设计方裁决

| # | 项 | 冲突 |
|---|---|---|
| A | **导航条目四个版本互不一致** | 桌面 `27678` 无 Contact Preferences；桌面 `27792`/`28000` 有；手机页内列表 `27604` 无 Account Overview 也无 Contact Preferences；手机汉堡 `34757` 只有 4 条（Account / My Subscriptions / My Details / Log Out）。**r-a3 查清了规律**：差异跟着页面走 —— Overview 页 8 项，Subscriptions / Detail 页 9 项。是有意还是漏画，需设计方回答。**已暂按 9 项实现**（PLAN Task 3 定的，一处可改） |
| A2 | **桌面两栏在 1440 以下如何收敛无稿** | 三个桌面稿一致地画 nav 241 + gap 32 + 内容 **固定 571**，左右 gutter **244 / 352**（不对称，但三稿完全相同，故判定为有意）。合计 1440 恰好铺满，**照抄则 768 档横向溢出 864 > 768**（`rwd.py` 实测）。已暂用「nav 241 固定 + 内容 `minmax(0,1fr)`，gutter 从 244/352 用 `fluid()` 收到 20」，1440 与稿逐值一致 |
| B | **评论与稿矛盾** | 评论 `2284:27077`：「原来的 contact preference 以及 refer a friend 去除了」，但两处稿上仍画着 |
| C | **六项只有导航条目、没有页面稿** | Order History / My Details / Change Password / Refer a Friend / Help / Contact Preferences。构想来自 Huel 竞品板，**不可自造** |
| D | **左侧导航图标未设计** | 便签 `27602`：灰圆是占位 |
| E | **21 类弹窗的桌面稿全缺** | 已定按决策 3 做居中卡片，具体宽度/内边距需给值 |
| F | **footer 内容差异** | 稿：两栏平铺 13 条链接 + Snapchat + `Subscribe now`；现站：三栏 + FB/IG/TikTok + `Subscribe`。且 Influencers / Press Inquiries / Careers 的目标页可能不存在 |
| G | **header 差异** | 稿：logo 左 + 人形 + 汉堡、浅绿底；Log in 稿另有 `Shop now` 按钮。已定单独覆盖，但需确认这是最终态 |
| H | **Add items 是否开启** | 便签 `30905`：「can be turned off for now until other items get added」，且「Edit 跳购物车还是 PDP？」设计方自己也没定 |
| I | **Download invoice 是否做** | 便签 `27444`：「Only do if very very very cheap. Otherwise, remove.」 |
| J | **Flavour 是否可编辑** | 便签 `30913`·`30915`：「for now I don't think it's an option」 |
| K | **交互态全缺** | hover / focus / active / disabled 在稿里与便签里都没有，按现站 `.gb-btn` 的既有值走，需集中登记（全局铁律 13） |
| L | **手机波浪 36 vs 现站组件 48** | account 稿的 `Spacer Bottom`（`2284:27607`）在 390 档是 36 高，现站 `.gb-scallop` 的 390 档算出 48（`--sc-band` 13.3 + amp 34.7），注释写着 48 才是「design's own strip height」。已复用现站组件（全站一致优先），差 12 |
| N | **Detail 的 Discounts 行两稿不一致** | 桌面 `27954` 是「Automatic + `-$26.40` 标签」，手机 `28433` 只有标签、没有 `Automatic`。无便签说明。**已两套都做按 767 切换**（全局铁律 3 允许的第二种做法），需设计方确认哪边是对的 |
| M | **桌面 Renewal 态无稿** | `2284:27548` 只有手机版。桌面的 renewal 沿用了桌面的字号阶梯（20/30），只有配色与文案按 renewal 走；`It's upcoming!` 标签块在两端都锁 16/24（它是状态不是断点） |

## 8. 稿件自身的错误（不是我们做错）

- ⚠ **三个桌面稿全叫「Account Overview Desktop」，实际是三个不同页面**（复制未改名，
  与 MVP 那 5 个同名「Our Story Desktop」是同一个坑）。**别信稿名，按 24px 标题认**：

  | 节点 | 真实身份 | 24px 标题 | 导航 |
  |---|---|---|---|
  | `2284:27678` | Account Overview | `Hi, Susanna` | 8 项 |
  | `2284:28000` | My Subscriptions（列表） | `My Subscriptions` 复数 | 9 项 |
  | `2284:27792` | Subscription Detail | `My Subscription` 单数 + `Cancel Subscription` | 9 项 |

- ⚠ **三个 icon 槽在板上是 `visible=false`，不是漏画**：两个 CTA 按钮的图标
  （`191:3907` View Order / `191:3892` Manage Subscription）与手机问候区的返回箭头
  （`2284:27611`）。组件自带图标槽，板上关掉了。**判据**：Figma 导出不含隐藏节点，
  所以整块 board SVG 在那个位置没有 path —— 「裁不出来」是确认而非失败。
  加图标前先查节点 JSON 的 `visible`。
- ⚠ **手机 Overview 的问候文案与桌面不一致**：桌面 `Hi, Susanna` / `Welcome back!`
  （有逗号、有感叹号），手机 `Hi Susanna` / `Welcome Back`（无逗号、无感叹号、B 大写）。
  两套都按各自的板做了，需设计方统一。
- ⚠ **桌面 CANCELLED 卡删错了行**：`2284:28146` 删掉的是 Shipping、保留 Next renewal date；
  但便签 `28323` 明写「Renewal date removed」，手机 `28316` / `34055` 也都是删 Renewal、
  保留 Shipping。**按便签 + 手机稿实现**（隐藏续订行），桌面这块是复制时改漏的。
- ⚠ **桌面 PAUSED 卡的续订日期没跟着改**：便签 `28321` 说暂停态显示的是「暂停到期日」，
  手机 `28315` / `34056` 写 `17 Aug 2026`，桌面 `28109` 还留着 active 的 `19 Jul 2026`。
  **按手机稿实现**。
- `34192` 标题拼成「Restart **subscoption**」
- `33847` 文案「You need to **another** product in order to delete this one」语法错
- `30107` 的取消原因列表里「I have too much product」**重复两次**（`29928`/`30286` 是正常的 5 项）
- 5 个手机稿的 `Chrome browser` 显示 `gumi.com.au` + 电量 84% + 8:39 —— 假舞台

## 8b. 上线前必须替换的占位内容

混在正文里看不出来，不单独列就一定会带上线。

| 项 | 在哪 | 为什么必须换 |
|---|---|---|
| **Refer a Friend 配图** | `images/refer-friends.jpg` / `.webp`（源 `imageRef 59db3bf5…`） | 板上的图是市售摄影素材，**画面里有第三方品牌 logo（帽子上的 Prada 标）**。客户站点直接用有商标风险，且授权来源未知 |
| `Hi, Susanna` / `Welcome back!` | `account.html` | 板上的示例姓名，接后端后应取真实用户名 |
| `Preparing, Aug 13` / `It's been shipped` / `Renewal Date, Sep 13` | `account.html` 三个状态槽 | 板上的示例日期与状态 |
| `Estimated delivery 3-6 business days.` / `You can make changes up until Sep 13, 6:59 AM` | 同上 | 示例文案，实际由订单数据决定 |
| `Earn rewards and $20 for every referral.` | `account.html` | 金额待客户确认 |
| **详情页的四条产品行** | `account.html` 的 `.gb-acct-product` ×4 | 板上就是同一件商品重复四次（同名、同数量、同价），是排版占位不是真数据 |
| `$168.90` / `$121.50` / `$00.00` / `-$26.40` / `FREE` | 同上 | 板上的示例价格；小计与总计都写着 `$00.00`，显然是未填 |
| `Ships every 4 weeks` / `PayPal (reallylongemail@email.com)` / `18th Jul, 2026, 6:59 AM` / `19 Jun`·`17 Jul`·`14 Aug`·`11 Sep` | 同上 | 板上的示例订阅设置与日期 |
| `Flavour`（产品行的口味位） | `.gb-acct-product__flavour` | 板上 `27899` 的文字**就是「Flavour」这个词**，值没填。便签 `30913` 说口味暂不可编辑 |
| **订阅卡的产品缩略图** | `account.html` 的 `.gb-acct-sub__thumb`（源 `196:19033`） | 板上是 64×64 的纯 `#d9d9d9` 矩形，**设计里根本没有产品图**，不是我们漏切 |
| `Superfood Greens Gummies` / `Quantity: 1` / `+4 More Products` / `$1245.60` | `account.html` 三张订阅卡 | 板上的示例订阅数据 |
| `19 Jul 2026`（active）/ `17 Aug 2026`（paused）/ `123 Express Ln, VIC 3121` | 同上 | 板上的示例日期与地址 |
| 三处 `href="#"`（View Order / Refer a Friend / Re-Activate Subscription） | `account.html`，已标 `TODO client link` | 目标页未定 |

## 9. 验证判据

沿用现站 `tools/` 的做法，account 专用判据另立：

| 判据 | 验什么 |
|---|---|
| `tools/acctvars.py` | `account.scss` 的变量副本与 `customstyle.scss` 是否仍一致（决策 5 的兜底） |
| `tools/rwd.py` | 复用现站的，扩到 account 三页 × 14 档：横向溢出 / 文字被裁 / 滚轮黑洞 |
| `tools/scrolllock.py` | 复用现站的：弹窗开启不得让页面横向位移（全局铁律 14） |
| `tools/acctmodal.py` | 19 类弹窗逐个开合、遮罩、焦点、ESC、滚动锁 |
| `tools/assetpath.py` | 复用现站的：scss 里的 `url()` 必须是 assets/ 内裸文件名 |

⚠ 负向断言（「已无 XXX」）先验锚点存在；hover 验证须用 Playwright（直连 headless 下
`(hover:hover)` 恒 false）。

## 10. 设计源速查

| 要什么 | 去哪 |
|---|---|
| 任何数值 | `figma/account/nodes/<id>_<slug>.json`，**不看截图** |
| 便签全文 | `figma/account/NOTES.txt`（33 条） |
| 弹窗清单与文案 | `figma/account/MODALS.txt`（30 态 / 13 类，另 7 个页面态） |
| 整页状态判读 | `figma/account/PAGES.txt`（24 个整页 frame） |
| 节点索引 | `figma/account/account-nodes-index.json` |
| 视觉参考 | `figma/account/screenshots/`（98 张） |
| 图标 | 先查 `figma/assets-raw/icons/`（MVP 阶段 1286 个）；没有再从 `figma/account/svg/` 的整块 SVG 本地裁 |
| 位图 | `figma/account/image-fills/<imageRef>.<ext>`（988 个） |

⚠ 33/42 个 MVP frame 含 `characterStyleOverrides`，account 的 frame 同理，
**只取 TEXT 顶层 style 必错**。

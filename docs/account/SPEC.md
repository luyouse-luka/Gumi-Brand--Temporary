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
| 8 | ~~Log in / Sign up **独立两页**~~ → **合成一页两视图**（`account-login.html` 的 `#login` / `#signup`），共用 account 的 css/js | 原因是未登录态 header 不同（多 `Shop now` 按钮）且对得上 Shopify `customers/login` 路由。**Task 28（2026-09-15 需求方指示）反转了「两页」这半**：改为复用 `[data-acct-view]` 一页两视图、alt 链接互切。Shopify 化时仍是两个 template，各 `render` 同一个 section 并指定默认视图 |

## 3. 交付物

```
account.html                单页多视图：Overview / Subscriptions / Subscription Detail
account-login.html          未登录态一页两视图：#login / #signup（Task 28 合并）
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

### account.html 的八个视图

前三个有桌面稿；**后五个只有 390 手机稿，桌面按外推规则做**（决策 C，2026-09-10 拍板）。

| 视图 | 桌面源 | 手机源 |
|---|---|---|
| `overview` Account Overview | `2284:27678` | `2284:27604`（整页）+ `27450`/`27499`/`27548`（三种订单状态弹层） |
| `subscriptions` My Subscriptions（列表） | `2284:28000`（同屏三态） | `2284:28305`（同屏三态）、`34046`（Cancelled + Paused 两态） |
| `detail` Subscription Detail | `2284:27792`（ACTIVE） | 见下表 11 个变体 |
| `orders` Order History | **无稿，外推** | `2284:27202` |
| `order` Order Detail | **无稿，外推** | `2284:27304` |
| `details` My Details | **无稿，外推** | `2284:27081`（`27116` 逐字相同，只做一个） |
| `password` Change Password | **无稿，外推** | `2284:27151` |
| `help` Help | **无稿，外推** | `2284:27170` |

**桌面外推规则**（`27792` vs `28330` 等三对逐档比对得出，别重新推导）：
**只有页面标题一档变** —— 手机 `20/24 w800 ls-0.2` → 桌面 `24/30 w800 ls-0.24`
（`.gb-acct-intro__title` 已实现）。`16/24`、`14/20`、`12/18` 三档两端完全相同，
版心与两栏 shell 沿用 `.gb-acct__inner`。

⚠ **Refer a Friend 与 Contact Preferences 仍然没有页面** —— 这两项连手机稿都没有，
做了就是自造内容。三处导航里它们保持 `aria-disabled`，由 `tools/acctview.py` 锁住。

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
| ~~C~~ **已拍板** | **~~六项~~两项只有导航条目、没有页面稿** —— 2026-09-10 用户定：五个有手机稿的**都做，且桌面由我们外推**（Task 16-22 已完成）；无稿的两项不做 | 原列 Order History / My Details / Change Password / Refer a Friend / Help / Contact Preferences。**r-a5 逐节点比对推翻了一半**：Order History（`2284:27202`）/ My Details（`27081`·`27116`）/ Change Password（`27151`）/ Help（`27170`）**其实都有 390 手机稿**，另外还多出一个导航里没有的 **Order Detail**（`27304`）。真正无稿的只剩 **Refer a Friend** 与 **Contact Preferences**。⚠ **Task 29（2026-09-15）又反转了一半**：需求方要求把 **Refer a Friend** 按 funkyfood 的模块做出来，已建 `referral` 视图并接上三处入口。它**依然没有任何板**，整页的文案与数值都是我们定的，逐条登记在 CHANGELOG Task 29 末节。**Contact Preferences 仍然不可点**。⚠ 这五个页面**不在 PLAN 的 15 个 Task 里**，做不做、要不要补桌面稿，需拍板。比对见 `DETAIL-STATES.md` |
| D | **左侧导航图标未设计 —— 灰圆点是占位，等图标** ⚠ **答复反复过一次** | 便签 `27602` 原话：灰圆是待设计图标的占位，且 `#D9D9D9` 正是 Figma 的默认占位灰，所以 Task 34 前先停下问过一次 → 需求方 **2026-09-14**「圆点不是占位而是 css 样式」，据此做进侧栏 `.gb-acct-nav__link::before` → **2026-09-17 设计方书面澄清：“These grey circles are placeholders for Icons which have yet to be designed.”**，与便签一致、与 09-14 的答复相反。**实现不动**（占位本来就得画出来），但**性质从「已定稿的样式」改回「待替换的占位」**，已进 8b。两处同源同值：20 槽 / 16.67 点 / `#D9D9D9` / gap 12 / 文字左沿 48（侧栏 Task 34、手机卡 Task 39）。⚠ 图标到位后换的是这两条 `::before`（给它 `background-image` 或换成真元素），不是加新结构。⚠ **每行右侧那个 5×10 的 chevron 两处都还没做**，需求从未提过 |
| E | **21 类弹窗的桌面稿全缺** | 已定按决策 3 做居中卡片，具体宽度/内边距需给值。**r-a6 起面板暂用板上的 390 居中**（`--acct-modal-w`，源数据里的值、非自拟），给了宽度只改这一个变量。手机稿本身**有两种形态**：≤394 的居中卡（r12）与 672 的贴底抽屉（r12/12/0/0，内含 528 的滚动区），桌面是否也分两种一并回答。**r-a10 记一笔代价**：面板宽锁 390 而桌面内边距按卡片惯例升到 24，内容盒比手机窄 8px —— `shipping-success` 的 `Your shipping details have been updated.` 在桌面折成两行（面板 254→274）。给桌面一个更宽的面板即可消掉。**✅ r-a22 已定**：需求方 2026-09-15 指示「弹窗 pc 端的宽高参考 funkyfood 的 account 页面」——桌面 `--acct-modal-w: 520px`、`max-height: 90vh`（funkyfood `\.delivery-*-pop-up .content` 是 520，其取消流程封顶 90vh）。**这反转了 2026-09-10「桌面沿用 390」的裁决**；手机仍是 390。上面那条折行代价随之消失 |
| F | **footer 内容差异** | 稿：两栏平铺 13 条链接 + Snapchat + `Subscribe now`；现站：三栏 + FB/IG/TikTok + `Subscribe`。且 Influencers / Press Inquiries / Careers 的目标页可能不存在 |
| G | **header 差异** | 稿：logo 左 + 人形 + 汉堡、浅绿底；Log in 稿另有 `Shop now` 按钮。已定单独覆盖，但需确认这是最终态 |
| H | **Add items 是否开启** | 便签 `30905`：「can be turned off for now until other items get added」，且「Edit 跳购物车还是 PDP？」设计方自己也没定 |
| I | **Download invoice 是否做** | 便签 `27444`：「Only do if very very very cheap. Otherwise, remove.」 |
| J | **Flavour 是否可编辑** | 便签 `30913`·`30915`：「for now I don't think it's an option」 |
| K | **交互态全缺** | hover / focus / active / disabled 在稿里与便签里都没有，按现站 `.gb-btn` 的既有值走，需集中登记（全局铁律 13） |
| L | **手机波浪 36 vs 现站组件 48** | account 稿的 `Spacer Bottom`（`2284:27607`）在 390 档是 36 高，现站 `.gb-scallop` 的 390 档算出 48（`--sc-band` 13.3 + amp 34.7），注释写着 48 才是「design's own strip height」。已复用现站组件（全站一致优先），差 12 |
| N | **Detail 的 Discounts 行两稿不一致** | 桌面 `27954` 是「Automatic + `-$26.40` 标签」，手机 `28433` 只有标签、没有 `Automatic`。无便签说明。**已两套都做按 767 切换**（全局铁律 3 允许的第二种做法），需设计方确认哪边是对的 |
| M | **桌面 Renewal 态无稿** | `2284:27548` 只有手机版。桌面的 renewal 沿用了桌面的字号阶梯（20/30），只有配色与文案按 renewal 走；`It's upcoming!` 标签块在两端都锁 16/24（它是状态不是断点） |
| O | **`2284:27081` 与 `27116` 完全一样** | 两张 My Details 手机稿**文本逐字相同、高度同为 2206**。是复制未删，还是有肉眼级差异（如某个 input 的 focus 态）？属上面 C 那批页面，一并回答 |
| P | **PAUSED 的续订日期两处稿不一致** | 详情稿 `28627`/`28774` 写 `19 Jul 2026`（与 active 相同），列表稿 `28315`/`34056` 写 `17 Aug 2026`。便签 `34038` 说暂停态显示的是「暂停到期日」，**站列表那边**。已各按各自的稿实现（详情 19 Jul / 列表 17 Aug），**未擅自统一**，需给出哪个对 |
| Q | **`28774` 的折扣码链接文案疑似漏改** | 它明明显示着一段码，链接却写 `Add a discount code`；同样有码的 `28478` 写的是 `Edit discount code`，便签 `30921` 也站 Edit 这边。**已按 Edit 实现**，判为 `28774` 漏改，需确认 |
| W | **原因屏「一个都没选」的态无稿** | `29928`/`30286`/`30107` 三张各选中一项，没有一张画未选态。已实现为「CTA 灰、禁用、字面写 Continue」——按站内脏值门控惯例，需确认 |
| X | **`Cancel now` 在第一屏与后面几屏含义不同** | 挽留屏（`29596`）的 `Cancel now` 已实现为「进原因屏」（便签 `34516` 要先收原因），而原因/假期/折扣三屏的 `Cancel now` 直接结束。同一个词两种行为，需确认第一屏是不是应该直接取消 |
| Y | **`34351` 的 Save 是绿的，`31976` 的是灰的** | 两个面板都只有一个预填日期字段，重启的按钮却直接可用。已按各自的板实现（重启面板挂 `data-acct-save-ungated` 显式豁免），需给出哪个对 |
| S | **地址单选钮的未选中态无稿** | `2284:32450` 板上只画了选中态（#e9facf 填充 + 0.8 绿环 + 8.8 圆点），因为 `shipping-current` 只有一个地址且恒选中。未选中态用了字段描边同色的 1px 灰环，是自拟的，需确认 |
| T | **表单两栏行比容器宽 1px** | `2284:33094`/`33109` 是 `168 + 15 + 168 = 351`，而体的内容盒只有 `390-20-20 = 350`。已按 `1fr / 15 / 1fr` 实现（每栏 167.5），需确认 168 是不是笔误 |
| U | **`shipping-current` 只画了一个地址，却有单选钮** | 有单选就意味着可以有多个，但板上没有第二张卡、没有「新增地址」入口、`Save` 也是灰的。是「以后支持多地址」的预留，还是这一版就只有一个？影响 Save 的语义 |
| V | **State 下拉的候选项只有 VIC** | `2284:33111` 闭合态显示 `VIC`，展开态无稿。已填澳洲 8 个州的标准缩写（ACT/NSW/NT/QLD/SA/TAS/VIC/WA）—— 是标准枚举不是自拟文案，但排序与是否用全称需确认。**r-a22 补**：展开态改用站点自己的 `.gb-select`（需求方指示），所以投影是站点的 `0 4px 12px` + 1px 描边，不是 account 板上别处那种 `0 10.29px 8px`；无稿可比，按「与站内其他下拉一致」处理 |
| R | **Detail 的四个状态全无桌面稿** | PAUSED / PAUSED+超长码 / CANCELLED / 重启后，都只有 390。桌面沿用基准态 `27792` 的字号阶梯，只有结构与文案随状态走。与 M 同类 |
| Z | **Log in / Sign up 的 header 用的是站点 header，不是 account header** | 两页板上的 header instance 是 `Header Navigation Desktop/Closed` —— 与 MVP 11 页同一个组件（Menu 下拉 + logo 居中 + 绿 `Shop now` + 两个图标），**不是** account 那个（logo + 人形 + 汉堡、浅绿底）。未登录访客也确实用不上 account 菜单。**已按站点 header 实现**（直接复用 `.gb-header`，样式与交互都来自 `customstyle.css` / `main.js`，account.scss 一行没写），与 G 是同一件事的两面，请一并确认 |
| AA | **note 卡在桌面比表单窄 8** | 两个桌面板都是表单 480 / note `472`（`35205`·`35132`），两个手机板则同为 350。桌面差的这 8px 没有语义、居中后左右各差 4，~~已按 480 实现~~ → **2026-09-16 需求方拍板 472，已实现**（`__alt` 仍 480）。**AA 已解决** |
| AB | **auth 桌面板的次要文字是 `#656565`，全套其余地方是 `#666666`** | ⚠ **Task 24 的全量扫描订正：是五处不是三处** —— `35189`(login 副标题)·`35111`(signup 副标题)·`35208`/`35135`(两页 note 正文)·`35129`(`Must be at least 8 characters`)。两个手机板同位置是 `#666666`/`#808080`（全套统计：`#666666` 1022 次，`#656565` 这五处）。**已各按各自的板实现**（`$c-gray-650`；`35129` 走 `.gb-acct-auth__aside--hint`），需给出哪个对 |
| AC | **My Details 的姓名两栏在桌面无稿** | 手机板 `27081` 把 `First name*` 与 `Last name*` **上下堆叠**（两个 308×70 在同一个 gap 16 的列里）。桌面没有板。**已按 Sign up 桌面板 `35059` 的两栏实现**（≤767 塌回堆叠），因为那是全套里唯一有桌面稿的同类表单，且桌面内容列 571 宽单栏会空。要保持堆叠请回一句 |
| AD | **`Opt in to order updates via text message` 稿上没有勾选框** | 它在板 `27081` 上是一行 12/18 `#666` 的纯文本，与上一张卡的 `You will receive a confirmation email…` 同一角色（都挂在卡 body 的第二个槽）。但文案是「选择加入」的口吻，像漏画了 checkbox。**已按稿做成纯文字**，需确认 |
| AF | **signup 桌面副标题没有字距，同类的另外三处都有** | `35111` 是 18/28 w400 **`ls=0`**，而 login 桌面的同位元素 `35189` 是 18/28 **`-0.36`**，两个手机板（`35034`/`35004`）都是 16/24 `-0.32`。四处同一角色、只有一处是 0，判为稿的疏漏，**已按体系给 -0.36**。要真是 0 请回一句 |
| AG | **`My Subscription` 列表项三行颜色不一致** | 手机板 `28305` 的三行是 `#1a1a1a` / `#101828` / `#101828`（同一个列表、同一个 16/24 w500）。`#101828` 全套只有这两次，`#1a1a1a` 是通用正文色，**已统一按 `#1a1a1a`**，需确认 |
| AO | **账号菜单只剩 hover 一条路** | Task 33 按需求去掉了汉堡的点击开关，`.gb-acct-menu` 只在 `@media (hover: hover)` 下靠图标 hover 打开，触屏与键盘都打不开（承载 hover 的是个不可聚焦的 `<div>`）。**没有链接因此失联** —— 那四条在桌面 `.gb-acct-nav`、手机 `.gb-acct-list` 里全都有。要不要给触屏/键盘补一条路（tap 开关，或把图标改成 `<button>` 加 `:focus-within`）请回一句 |
| AP | **header 不再随菜单变色** | 板 `34854`（桌面展开）/ `34804`（手机展开）把整条 bar 提亮到 `#f6feec` 并加一像素内描边。Task 33 按需求整条删除，bar 只剩 `$c-lime-150`。**与稿不符是需求方的决定**，登记备查 |
| AH | **signup 的 Email 输入框占位文字与其他字段不成体系** | `35023`/`35059` 上 Email 框内写的是 **`Email`**，而同一张板的 First name / Last name / Password 分别是 `First name` / `Last name` / **`Your password`**，login 两档的 Email 框也都是 `Your email`。**已统一按 `Your email`**，要照稿写 `Email` 请回一句 |
| AL | **Edit renewal date 的日历用的是 `cancel-holiday` 那张板的组件**，⚠ **Task 38 起由 flatpickr 绘制**（需求方 2026-09-17 要 funkyfood 同款插件 + gumi 的样式）。新增待答：**年份成了可编辑的 number input**（插件结构，板上是纯文本），要不要锁成只读 | 需求方 2026-09-15 点名「查看设计 Heading away on holiday 的日历表」。`Edit Date` 板（`31976`）上确实只有输入框，日历只在 `30465` 画过一次。**已复用 `.gb-acct-cal`**（连同 `30622` 的 1px 内描边、`30623` 的 20/24 内边距、`30625` 的 32 高月份条）。这等于把一个挽留流程里的组件搬进表单弹窗 —— 若设计方认为两处应有不同样式，请给 Edit Date 的板 |
| AM | **桌面弹窗正文的宽度是外推的** | 21 类弹窗**桌面稿全缺**（待裁决 E）。`.gb-acct-modal__copy` 板上是 `320` 框在 `350` 内容盒里，本轮判定**「右侧 30 的留白」才是组件、320 不是**，改成 `calc(100% - 30px)`；520 面板下算出 442。若设计方本意是正文固定 320、右侧留白随面板变宽，请回一句 |
| AN | **弹窗内下拉的展开方向随面板会不会滚动而变** | 需求方要求「下拉应该往下」。不滚的面板（`edit-frequency` / `edit-product` 桌面）已改成往下；**内容真的要滚的面板（`add-product` / `shipping-form`、以及手机档）仍然往上** —— 往下会被滚动区裁掉半截。若要求「任何情况都往下」，需要把下拉改成脱离面板的浮层（会动到 `main.js` 的站点组件，属主站线） |
| AI | ~~**Edit Date 的日历稿里不存在**~~ **（Task 31 已反转，见 AL）** | `2284:31976` 全部内容只有标题 / `Next renewal date` / `19/07/2026` / 说明 / Cancel / Save，**没有日历**。需求方 2026-09-15 要求「采用 funkyfood 项目中日历的同样插件做法」，故用 flatpickr `inline` 并沿用 funkyfood portal 的皮肤。**日历的字号 / 行高 / 选中态配色 / 箭头全部无设计源**，需设计方给规格 |
| AJ | **加了日历后面板变高，板上是 290** ⚠ Task 31 换成 `.gb-acct-cal` 后实测 **632**（原 flatpickr 是 604） | 290 是「只有一个输入框」的面板高度。装进内联日历后必然变高；390×844 放得下，但 **390×667（iPhone SE 一代）会贴到 `max-height` 上开始滚动**。⚠ **Task 32 已消解这一条**：需求方 2026-09-16 要求日历默认收起、点 input 才展开，收起态的面板高度回到板上的值（`edit-date` 290 / `restart` 329，实测吻合），两条高度断言都已恢复。展开态 632 / 671 是瞬时状态，不再与板比 |
| AK | **Suburb 自动补全没做（需求方指示先不做）** | 需求方 2026-09-15：「可能会同 funkyfood 的地址自动补全，可以加上注释先不做」。已在 `account.html` 的 Suburb 字段上留注释。**funkyfood 那套是纯前端**：`layout/theme.liquid` 首次交互时懒加载 `maps.googleapis.com/maps/api/js?key=…&libraries=places`，`assets/customer-portal-details.js:1344` 用 `new google.maps.places.Autocomplete(input, {componentRestrictions:{country:'au'}})` 接管输入框，`place_changed` 里把 `address_components` 拆成 address1 / city(=Suburb) / provinceCode(=State) / zip 回填，再用 `common-theme.js:461` 的 `findZoneData()` 拿一份配送区 JSON 本地比对，不在派送范围就显示 `Delivery not available at this suburb`。**要做需要两样 Gumi 目前都没有的东西**：① 一个 Google Places API key（funkyfood 的 key 是硬编码在 theme.liquid 里的，不能借用）② 一份 Gumi 自己的配送区数据。请需求方决定是否提供 |
| AQ | **Refer a Friend 卡的箭头，两块板对不上** | `2284:27780`（桌面）的 `Content` 带 `counterAxisAlignItems: CENTER`，箭头 y=44=24+(80−40)/2，**居中**；`2284:27639`（手机）箭头 y=16=padding-top，**顶对齐**。需求方 2026-09-17 说「`.gb-acct-refer` 去掉 `align-item center`」，但同一条需求的另外两点都在讲手机，**故只在 ≤767 撤掉、桌面保留居中**。要桌面也顶对齐（即与 `27780` 不符）请回一句 |
| AR | **跳过下一单：便签与板互相不一致** | 便签 `2284:30908` 说改期要走「I want it now」或「edit frequency」，而板 `2284:28922` 上真正画出来的那行字是 **「To unskip this order, edit your **renewal date**」**，链接指向的是日期选择。**已按板实现**（板是画出来的，便签是随手写的 —— 同一条便签里 subscription 还拼成了 `subscripition`）。要改成便签说的两个入口请回一句 |
| AS | **`+N More products` 是后端规则，静态站做不了** | 便签 `2284:28326`：「More than one product in a subscription / +1 More products when more than one product in the subscripition」。即 `.gb-acct-sub__more` **只在订阅里多于一件商品时出现**，数字是「其余商品数」。板上六个实例渲染出来的字全是 `+4 More Products`（大写 P），**文案按板、规则待接后端**。已同时登进 8b |
| AT | **自动播放的循环视频没有暂停控件** | 便签 `2284:34511`「Video / Auto plays」，Task 40 已把 `.gb-acct-video__media` 改成 `autoplay muted loop playsinline`。⚠ WCAG 2.2.2 要求超过 5 秒的自动播放内容可暂停，而 `.gb-acct-video__play` 目前只是板上画的装饰件；⚠ `prefers-reduced-motion: reduce` 下要不要不自动播也没说。**视频源还没来**，不臆造控件，两件事一起等拍板 |
| AE | **订单状态三态没有任何视觉区分** | 板 `27202` 的 `Shipped` / `Delivered` / `Cancelled` 全是 `#1a1a1a` 14/20，与旁边的 `Date:` / `Total:` 值同一个样式，没有色块、没有徽章。订阅那边的 ACTIVE / PAUSED / CANCELLED 是有徽章的（`.gb-acct-pill`）。**已按稿实现（三者同色）**，需确认订单状态是不是也该有区分 |

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
- `33116`/`33119` 地址表单的最后一个字段拼成「Delivery **Instrctions**」（应为 `Instructions`），
  标签与占位两处都错。**已按稿照抄**，上线前需设计方改
- ⚠ **同一个地址在两张板上邮编不一样**：`shipping-current`（`32457`）写 `3182`，
  表单 `shipping-form`（`32940`）写 `3181`，其余各行相同。**已各按各自的板实现**，需给出哪个对
- ⚠ **`30465` 的 July 2026 月历不能照抄，有三处错**：① 2026-07-01 是**周三**，
  板上却排在 `Su` 列；② 第一行有一格写着 **`32`**（六月只有 30 天）；
  ③ 星期头是 `Mo Tu We Th Fr **Sat** Su` —— 只有周六是三个字母。
  **月历改成运行时生成**（Mo 起、按真实日历排），只有视觉 token 取自板；
  `Sat` 照抄。⚠ 这不是 bug，别改回板上的排法。
- ⚠ **`30465` 里被选中的那一格 `6` 用的是 Inter，其余 41 格都是 PP Palma**
  （组件默认字体漏改）。已统一用 PP Palma，字重按板取 w500。
- ⚠ **`30107` 不只是重复项**：它把第 2 行的「Too expensive right now」整个覆盖成了
  「I have too much product」，所以那一列少一项、多一项。**七项以 `29928`/`30286`
  为准**（两张逐字一致）。另外 `30107` 的 CTA 写的是 `Cancel` 不是 `Continue` ——
  那不是错，是便签 `34512` 的体现：无第二屏的原因，按钮直接说「取消」。
- ⚠ **`29596` 的视频是占位**：`29751` 是纯 `#d9d9d9` 矩形、没有 `imageRef`，
  与订阅卡缩略图同类。上线前必须换成真视频/封面，已进 §8b。
- `34192` 标题拼成「Restart **subscoption**」
- `32775` Skip 弹窗文案拼成「Are you sure you **wan** to skip…」（应为 `want`）。**已按稿照抄**
- `34079` CANCELLED 的说明文案拼成「You will be **bale** to make changes…」（应为 `able`）。**已按稿照抄**，上线前需设计方改
- `33847` 文案「You need to **another** product in order to delete this one」语法错
- `30107` 的取消原因列表里「I have too much product」**重复两次**（`29928`/`30286` 是正常的 5 项）
- 5 个手机稿的 `Chrome browser` 显示 `gumi.com.au` + 电量 84% + 8:39 —— 假舞台
- ⚠ **`2284:35059` Sign up 桌面的标题与副标题用的是 Lexend，全套只有这一处**：标题 `35110`
  是 Lexend 600 36/44 ls -0.72、副标题 `35111` 是 Lexend 400 18/28 ls 0，而同一页的手机板
  `35032` 是 PP Palma 800 24/30、同组的 Log in 桌面板 `35188`/`35189` 是 PP Palma 800 32/40
  与 PP Palma 400 18/28 ls -0.36。account 的 112 个节点里 Lexend 只出现在这一个文件。
  **已按 Log in 桌面板实现**（PP Palma 800 32/40）。Lexend 是站内确有的字体，所以不能
  当成 Figma 回退字忽略 —— 若设计方确实想让 Sign up 标题与 Log in 不同，需明说。
- ⚠ **手机 Log in 板 `2284:35015` 写的是「Forgot you password?」**（少一个 r），桌面 `35202`
  是「Forgot your password?」。**按桌面的正确拼写实现**。
- ⚠ **手机 Sign up 板 `2284:35034` 的副标题少了「your」**：手机「Sign up to edit, skip or
  manage subscription」，桌面 `35111`「…manage your subscription」。**按桌面实现**。
- ⚠ **两个 auth 桌面板的 note 卡标题是 PP Palma 500，手机板是 400**（`35207`/`35134` vs
  `35020`/`35056`），颜色也是 `#1B1C1E` vs `#011307`。**已各按各自的板实现**，与待裁决 AB 同源。

- ⚠ **`2284:27151` Change Password 的说明文案有错字**：「…we'll send you an email with
  instructions **ro** reset it.」—— `ro` 应为 `to`。**按 `to` 实现**。
- ⚠ **`2284:27081` My Details 的电话字段 label 写的是「Email*」**，应为「Phone number*」——
  上一组 Email 字段的 label 复制过来忘了改（同组内 `Your name` 的两个 label 都是对的）。
  **按 `Phone number*` 实现**。
- ⚠ **`2284:27202` Order History 的五张订单卡里有三张完全相同**（`Order #12345680` /
  `Aug 15, 2026` / `Delivered` / `$45.00`）—— 只有前三张是三种不同状态
  （Shipped / Delivered / Cancelled），后两张是复制凑数。**照稿做五张**，
  但内容属占位（见 §8b）。
- ⚠ **`2284:27081` 与 `27116` 两张 My Details 逐字相同、同高 2206**（待裁决 O）——
  **只实现一个**，不是漏了一页。
- ⚠ **`2284:27081` 的两段说明文字宽度写死 298，比它们所在的内容盒窄 10**
  （`You will receive a confirmation email…` 与 `Opt in to order updates…`，
  两者都是 `textAutoResize=HEIGHT` 的 FIXED 298，而 `Order Info` 是 308）。
  两段都**左对齐、左边缘与 label 齐平**，所以差的 10px 全在右边、没有语义。
  **已按撑满 308 实现**，与 note 卡 472 vs 480（待裁决 AA）同类。

- ⚠ **`2284:27304` 的四条商品行把「较低的价划掉」**：`$134.50` 是正常样式、
  `$133.50` 带 STRIKETHROUGH。划线价按惯例是**原价**、应当更高，这里反了。
  **已照稿实现**（划 `$133.50`），两个数都是占位（见 §8b），换真数据时一并纠正。


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
| **导航行左侧的灰圆点** ×2 | `.gb-acct-nav__link::before`（侧栏 9 行）/ `.gb-acct-list__link::before`（手机卡 6 行） | 设计方 2026-09-17：“These grey circles are placeholders for Icons which have yet to be designed.” `#D9D9D9` 是 Figma 的默认占位灰。**图标未设计，上线前必须换掉**（裁决 D）|
| **订阅卡的产品缩略图** | `account.html` 的 `.gb-acct-sub__thumb`（源 `196:19033`） | 板上是 64×64 的纯 `#d9d9d9` 矩形，**设计里根本没有产品图**，不是我们漏切。Task 30 起画的是 `images/product-placeholder.png` 而不是 CSS 底色 |
| `Superfood Greens Gummies` / `Quantity: 1` / `+4 More Products` / `$1245.60` | `account.html` 三张订阅卡 | 板上的示例订阅数据 |
| `19 Jul 2026`（active）/ `17 Aug 2026`（paused）/ `123 Express Ln, VIC 3121` | 同上 | 板上的示例日期与地址 |
| **挽留屏的视频** | `.gb-acct-video` 内的 `<video class="gb-acct-video__media">`（源 `2284:29751`） | 板上是纯 `#d9d9d9` 矩形 + 播放键，没有 imageRef。Task 36 起灰块里有一个**不带 `src`** 的 `<video>` 占位，客户已明确要留这块。⚠ 接 `src` 时要一并删掉父级的 `role="img"` / `aria-label`（`role="img"` 的子树对辅助技术是 presentational，真视频留在里面等于把播放器藏了），并决定加不加 `controls` |
| `Next order will renew on 17 July, 2026` | `cancel-skipped` 面板 | 板上的示例日期 |
| `22/07/2026` | `restart` 面板的重启日期 | 板上的示例日期 |
| 两处 `href="#"`（View Order / Refer a Friend） | `account.html`，已标 `TODO client link` | 目标页未定。⚠ **Re-Activate Subscription 已于 Task 32 接上 detail 的 cancelled 态**，不再是死链 |
| `href="#"` 的 **Forgot your password?** | `account-login.html`，已标 `TODO` | 密码找回页在稿里根本不存在，目标未定 |
| **Help 页手风琴的全部文案** | `account.html` 的 `[data-acct-view="help"]`，已标 `TODO 待客户文案` | 板 `27170` 上七行的标题就是字面的 `Accordion Open` / `Accordion Closed`，正文是 `Text here` —— 设计里根本没有 FAQ 内容，**不许自拟** |
| `email@email.com.au` / `0400 000 000` / `Mon - Fri, 6am - 11pm AEST` | `.gb-acct-help` 卡（Help 与 Order Detail 共用） | 板上的示例联系方式 |
| Order History 的五张订单卡 | `[data-acct-view="orders"]` | `Order #1234567x` / `Aug 14-16, 2026` / `$89.99`·`$45.00`·`$0.00` 全是示例，且后两张是第二张的复制（见 §8） |
| `Page 1 of 10` 与两个翻页箭头 | 同上 | 静态站只有一页，箭头做成 disabled；接后端后才有真分页 |
| Order Detail 的四条商品行缩略图 | `.gb-acct-item__thumb` ×4 | 板上是 40×40 的纯 `#d9d9d9` 矩形、**没有 imageRef** —— 与订阅卡缩略图一样，设计里根本没有产品图，不是我们漏切。Task 30 起同样是 `images/product-placeholder.png` |
| Order Detail 的四条商品行 | `[data-acct-view="order"] .gb-acct-item` ×4 | 同一件商品重复四次（同名、同口味位、同数量、同价），是排版占位不是真数据 |
| Order Detail 的订单数据 | `[data-acct-view="order"]` | `Order #12345678` / `Aug 13, 2026` / `$121.50` / `$134.50`→`$133.50` ×4 / Order Summary 的四个 `$00.00` / `Susanna Rose, 12 Charnwood Rd…` / `•••• 5467` / `Shipping & Standard: $12.98` 全是板上的示例 |
| **Refer a Friend 整页**（Task 29，无稿） | `[data-acct-view="referral"]` | `GUMI-0000` 是示例 code（没有 referral 后端）；hero 是 16/9 的 `images/product-placeholder.png`（Task 30 起；原为 `#eeeeee` 的 CSS 底色，统一到全站占位灰 `#d9d9d9`）；四个分享按钮都是 `href="#"`；`GIVE $20 / GET $20` 与说明文字沿用 overview 卡的 $20 口径。⚠ **刻意没有复用 `images/refer-friends.jpg`** —— 那张图带第三方品牌 logo，且一卡一图不允许它冒充第二处用图 |
| 改密卡的说明文案（Task 29 改写） | `[data-acct-view="password"] .gb-acct-card__text` | 板 `27151` 写的是「会发一封重置邮件」，需求方改成 funkyfood 的内联表单，文案随之改写。三个密码字段稿上完全不存在 |
| **`images/product-placeholder.png`**（14 处引用）| `.gb-acct-prod__thumb` ×6 / `.gb-acct-sub__thumb` ×3 / `.gb-acct-item__thumb` ×4 / `.gb-acct-referral__hero` ×1 | 400×400 的纯 `#d9d9d9`，**不是产品图**。接上真实商品数据时每一处都要换成各自的图，⚠ 一卡一图，不许复用同一张冒充多张 |
| 两个 auth 表单的 `action="#" method="post"` | `account-login.html` 的两个视图 | 静态壳，提交后只会跳回 `#`。接 Shopify 时换成 `customers/login` 与 `customers/register` 的真实 form |

## 8c. 弹窗几何（r-a6 起，取自 29 张弹窗板）

- 遮罩 `#000000` @ 0.6（`2284:31476`），面板满 390 宽、白底
- 居中卡：高 ≤394，`top == bottom`，圆角 12 四角
- 贴底抽屉：高 672 = 840−168，贴底，圆角 `[12,12,0,0]`，内部 `64 头 / 528 滚动体 / 80 脚`
- 头 64 高、四周 20，标题 16/24 w500 `-0.32` `#1a1a1a`，右侧 24×24 关闭叉（10×10 线条）
- ⚠ 滚动锁**复用站内 `is-modal-open`**，不另起一套：body 必须 `overflow-x:clip; overflow-y:visible`
  （用 `hidden` 会让 sticky 的 `.gb-acct-header` 当场掉出视口），补偿只落在 `html`

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

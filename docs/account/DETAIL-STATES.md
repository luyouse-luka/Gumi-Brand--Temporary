# Subscription Detail 的状态比对

> PLAN Task 7 步骤 1 的结论。**别按 frame 高度猜状态**，下面每一条都是逐个节点比对出来的。
> 比对脚本：把每个 frame 的可见 TEXT 全量抽出来横向对比，再比 `Frame 1984078229`
> （卡片正文）的直接子节点序列。

## 一、PLAN 里列的六个「未标注 frame」不是 Detail 的状态

`2284:27202` · `27304` · `27081` · `27116` · `27151` · `27170` 全部**不是订阅详情页**，
而是**账户区其他栏目的手机稿**。文本一比就分得清：

| 节点 | 真实身份 | 判据（文本里独有的东西） |
|---|---|---|
| `2284:27202` | **Order History**（订单列表） | `Order History` / `Review, track, or create a return for your orders.` / 5 张 `Order #1234567x` 卡 / `Page 1 of 10` |
| `2284:27304` | **Order Detail**（单个订单详情） | `Order Items:` / `Order Summary` / `Shipping Information` / `Payment Information` / `Download Invoice` / `Need help with your order?` |
| `2284:27081` | **My Details**（个人资料表单） | `Your details` / `First name*` / `Opt in to order updates via text message` / `Save changes` |
| `2284:27116` | **My Details** —— 与 `27081` **文本逐字相同** | 同上。两者高度都是 2206，疑似复制未改；差异需比像素或交互态才看得出 |
| `2284:27151` | **Change Password** | `Need to update your password?` / `Click the button below and we'll send you an email with instructions ro reset it.`（`ro` 是错字） |
| `2284:27170` | **Help** | `Popular Questions` / `Accordion Open` / `Accordion Closed` ×6 / `Need help with your order?` |

### ⚠ 这推翻了 SPEC 待裁决 C 的一半

待裁决 C 原话是「六项只有导航条目、没有页面稿：Order History / My Details /
Change Password / Refer a Friend / Help / Contact Preferences」。
**其中四项其实有手机稿**（Order History / My Details / Change Password / Help），
另外还多出一个导航里没有的 **Order Detail**。

仍然没有稿的只剩 **Refer a Friend** 与 **Contact Preferences** 两项。

这五个页面**不在 PLAN 的 15 个 Task 里**，属于范围变化，等用户拍板再做，本轮不动。

## 二、Detail 真正的状态（全部只有 390 手机稿，无桌面稿）

基准态 = `2284:28330` ACTIVE（Task 6 已做）。

| 节点 | 状态 | 与基准态的差 |
|---|---|---|
| `2284:28478` | **ACTIVE + 折扣码已应用** | Discounts 行多一段码文本（`DISCOUNTCODE`，12/18 `#666`，右对齐，宽 118 固定）；链接文案 `Add a discount code` → `Edit discount code`（便签 `30921`） |
| `2284:28627` | **PAUSED** | 徽章 `PAUSED`；续订行标签 `Next renewal date` → `Subscription restarts`；**日程卡里的 `Skip next order` 整个删掉**（便签 `34042`：暂停期间不许跳过下一单），日程卡因此从 228 矮到 160 |
| `2284:28774` | **PAUSED + 超长折扣码** | 同 `28627`，外加 Discounts 行里一段 51 字符的码，在 118 的固定宽里折成 4 行，小计块从 150 长到 198（便签 `34044`） |
| `2284:34058` | **CANCELLED + 可重启** | 见下表，改动最多 |
| `2284:34352` | **CANCELLED 重启后转回 ACTIVE** | 文本与 `28330` **逐字相同**。不是新状态，是重启流程的结果页 |

### `2284:34058` CANCELLED 的逐项差异

| 位置 | 基准态 | CANCELLED |
|---|---|---|
| 徽章 | `ACTIVE` | `CANCELLED` |
| 续订行 `Frame 1984078258` | 有（78 高） | **整行删除** |
| 按钮块 `Frame 1984078260` | 两个按钮 96 高（`Edit Date` / `I need it now`） | **一个按钮 44 高**：`Restart Subscription`（图标槽 `visible=false`） |
| 按钮块下方 | 无 | 多一句居中说明 `You will be bale to make changes to your subscription once restarted.`（12/18 `#666`，宽 298.5）+ 一条新分隔线 `Line 120` |
| 第一条产品行的口味位 | `Flavour` `#666` + 划线原价 + 现价 | `Out of stock` **`#dd655e`**（coral）+ 单价 `$00.00`（12/18 500 `-0.12`，无划线） |
| Discounts 行 | 有 | **删除**，小计块从 150 矮到 118 |
| `Skip next order` | 有 | **仍然有**（与 PAUSED 相反） |
| `Cancel Subscription` | 有 | **删除** —— `Frame 1984078383` 这个壳还在，里面的 TEXT 被删空了 |
| 灰化 | —— | **没有任何 opacity 变化**。列表卡的 PAUSED/CANCELLED 会压到 0.4，详情页不会 |

## 三、归属未定 / 需设计方确认

| # | 项 | 说明 |
|---|---|---|
| 1 | `2284:27081` 与 `27116` **完全一样** | 文本逐字相同、高度同为 2206。是复制未删，还是有肉眼级差异（如某个 input 的 focus 态）？ |
| 2 | `28774` 的链接文案 | 它明明显示着一段折扣码，链接却写 `Add a discount code`；`28478` 同样有码却写 `Edit discount code`。便签 `30921` 站 `28478` 这边，所以 `28774` 判为漏改 |
| 3 | PAUSED 的续订日期 | 详情稿 `28627`/`28774` 写 `19 Jul 2026`（与 active 相同），列表稿 `28315`/`34056` 写 `17 Aug 2026`。便签 `34038` 说暂停态显示的是暂停到期日，列表那边才对 |
| 4 | 这四个状态**没有桌面稿** | 与待裁决 M 同类：桌面按基准态的字号阶梯外推，只有结构与文案随状态走 |

# Gumi Account — 交接文档

> account 静态页是 Gumi-Brand 仓库里**独立的一条线**，与 MVP 11 页 + Shopify 主题化那条线
> 并行推进、互不相干。接手先读这份，再按需翻 [PLAN.md](PLAN.md) / [SPEC.md](SPEC.md) /
> [CHANGELOG.md](CHANGELOG.md)。
>
> **最重要的一节是第 5 节「不要报成 bug 的清单」** —— 里面每一条都是有意为之，
> 上一轮审计已经查过一遍。不看就修，等于把裁决过的取舍再推翻一次。

---

## 1. 边界：哪些是这条线的，哪些不是

| | account 线（这条） | 主站线（另一条） |
|---|---|---|
| 页面 | `account.html` · `account-login.html` · `account-signup.html` | `index.html` 等 11 页 |
| 样式 | `assets/account.scss` → `.css`（**自带一份变量副本**） | `assets/customstyle.scss` → `.css` |
| 脚本 | `assets/account.js`（自包含 IIFE，不调 `window.gumi`） | `assets/main.js`（`window.gumi`） |
| 版本号 | **`$build-acct`**，当前 `20260910-a12` | `$build`，当前 `r138` |
| 判据 | `tools/acct*.py` | `tools/r*check.py` 等 |
| 文档 | `docs/account/` | `docs/PROJECT-STATUS.md` 等 |

⚠ **同一个仓库里可能另有一个会话在跑主站线**。提交**一律逐个列文件路径**，
不要 `git add -A`，不要碰 `customstyle.*` / `main.js` / `liquid/` / 各 MVP 页 / `docs/` 根下的文件。

⚠ **account.scss 的变量是 customstyle 的副本**，`tools/acctvars.py` 守着它不漂移。
改颜色/断点/字体变量要两边一起改，或者确认那是 account 独有的 token（判据会把它列成
`note account-only token`，不算红）。

---

## 2. 三个页面各是什么

- **`account.html`** —— 单页三视图，`[data-acct-view]` 切换：
  `overview`（Hi Susanna + 当前订单卡 + Refer a friend）/ `subscriptions`（三张订阅卡）/
  `detail`（订阅详情 + 19 类弹窗的入口）。**三个视图都在 DOM 里，只有一个不带 `hidden`**。
- **`account-login.html`** / **`account-signup.html`** —— 未登录态两页。
  它们用的是**站点 header**（`.gb-header`，Menu / logo / Shop now / 两个图标），
  不是 account header，骨架整套取自 `faq.html`，只有 `<main class="gb-acct-auth">` 是自己的。

**桌面与手机是两套并存、不是一套折叠**：桌面左侧竖导航 9 项，手机是页内列表卡 6 项 +
右上角下拉面板 4 项，767 互斥切换。

---

## 3. 命令速查

```bash
# 编译（唯一正确的编译方式，sass 不在 PATH）
npx sass@1.77.8 --no-source-map assets/account.scss assets/account.css

# 改完必须一起 bump：源码里的 $build-acct + 三个页面各两处 ?v=
grep -rn '20260910-a12' assets/account.scss account*.html
```

⚠ **改了 scss 一定要重编译**。判据读的是 `account.css`，忘了编译会得到「改了没生效」
的假红，或者更糟 —— 假绿。

---

## 4. 判据与基线

**全绿才算完**。任何一条红就停下修，不要标「已知问题」放过。

| 判据 | 基线 | 说明 |
|---|---|---|
| `python3 tools/acctcheck.py` | **660 ok / 0 red** | 结构与数值，按 (页面, 宽度, 动作) 分组 |
| `python3 tools/acctmodal.py` | **1314 ok / 0 red / 1 aborted** | 19 类弹窗，**约 4 分钟，后台跑** |
| `python3 tools/acctvars.py` | 54 ok / 0 red | 变量副本没漂移 |
| `python3 tools/assetpath.py` | GREEN | scss 里的 `url()` 必须是 `assets/` 内裸文件名 |
| `python3 tools/acctbp.py` | 1842 declarations / 0 red | 断点值档互斥、阈值不带数值 |
| `python3 tools/accthover.py` | 30 hover properties / 0 red | 每个 hover 属性都有对应过渡 |
| `python3 tools/acctmotion.py` | 12 ok / 0 red | reduced-motion 真的覆盖到了 |
| `python3 tools/rwd.py account.html` | 全绿 | 14 档溢出扫描，三个页面各跑一次 |

**那条 abort 是预期的，不是欠验证**：`account.html@390` 的「开弹窗页面有没有横移」。
手机画的是 overlay 滚动条、不占布局宽度，锁滚动时没有宽度被释放，也就没有横移可测。
**桌面档（1440）这条是真跑了的** —— 判据启动 chromium 时去掉了 Playwright 默认的
`--hide-scrollbars`，拿到真滚动条再测。

### 写判据时会踩的坑

- ⚠ **测「页面横移」必须挑右对齐的元素**。滚动条在右边，锁滚动释放它的宽度时，
  左对齐的东西（`.gb-acct-nav`、logo）**一动不动** —— 实测：补偿开着是 0px，
  把补偿强行关掉**还是 0px**。判据因此恒真过。现在测的是 `.gb-acct-header__icons`
  的 `right`，关掉补偿会稳定报 15px。
- ⚠ **负向断言（"已无 XXX"）先验锚点**。`acctcheck.py` 的 `absent` 在元素不存在时算过，
  所以每组的第一条都是 `("vis", ".gb-acct-auth", True)` 之类的锚点。
- ⚠ **`innerText` 在 `display:none` 子树里不套 `text-transform`**（徽章会读成 `Active`
  而不是 `ACTIVE`），而且三个视图同名元素并存 —— 选择器**必须带
  `[data-acct-view='<name>'] ` 前缀**。
- ⚠ **读「状态切换后的颜色」要等够过渡（≥450ms）**，等 120ms 读到的是插值。
- ⚠ **headless 里 `(hover: hover)` 恒 false**，hover 只能用 Playwright 实测，不能靠读 CSS。
- ⚠ **活性自检要逐条突变**。「一批一起改、红了就算过」会漏掉早退分支里的死属性 ——
  Task 10 就这样漏过 10 条。
- ⚠ **探针往被测元素里塞东西，收尾只能移除自己塞的那块**，不能 `innerHTML=''`
  或整体还原：前者抹掉真内容，后者重建节点让 JS 捕获的引用失效。
- ⚠ **判据里任何"点开弹窗"的分支，末尾都要按 Escape 关掉**。`modal.open()` 不会
  把一个开着的面板换成另一个，后面的检查会全量测到 `0px`。这个 bug 在
  `acctmodal.py` 里藏了很久，因为那条分支一直在 abort、从没执行过。

---

## 5. 不要报成 bug 的清单

下面每一条都是**有意为之**或**稿件自身的问题**，已经查过、已经拍过板。
逐条的出处在 [SPEC.md](SPEC.md) 第 7 节（待裁决）与第 8 节（稿件错误）。

### 5a. 稿里就没有的东西

- **`Chrome browser` 假舞台没做**（手机稿顶上的浏览器地址栏、电量、home indicator）。
- **左侧导航的灰色圆点是待设计的图标占位**（便签 `27602`），不是漏切图标。
- **三个 icon 槽在板上是 `visible=false`**：两个 CTA 的图标（View Order / Manage
  Subscription）与手机问候区的返回箭头。**Figma 导出不含隐藏节点，所以整块 board SVG
  在那个位置没有 path —— 「裁不出来」是确认，不是失败。**
- **订阅卡的产品缩略图是 64×64 的纯 `#d9d9d9`**，设计里根本没有产品图。
- **挽留屏的"视频"是纯 `#d9d9d9` 矩形 + 播放键**，没有 imageRef。
- **登录/注册两页没有 footer CTA 区块** —— 两张桌面板的 `Footer CTA` 都是 `visible=false`。
- **无稿的两项（Refer a Friend / Contact Preferences）只在导航里、不可点**，
  渲染成 `aria-disabled` 的 `<span>`，既不是死链也不建页面（待裁决 C）。

### 5b. 稿自带的错字与自相矛盾（已按更可信的一版实现）

| 稿上写的 | 我们做的 | 出处 |
|---|---|---|
| `Sign up` 桌面标题是 **Lexend** 36/44 | PP Palma 800 32/40（同 Log in） | 全套 112 个节点只有这一处 Lexend，它自己的手机板是 PP Palma |
| 手机 `Forgot you password?`（少个 r） | `Forgot your password?` | 桌面板拼写正确 |
| 手机 Sign up 副标题少 `your` | 补上 `your` | 桌面板有 |
| 桌面 note 卡 472 宽 vs 表单 480 | 都做 480 | 两个手机板本来就同宽 |
| 桌面 auth 的次要文字 `#656565` | 照做（新增 `$c-gray-650`），手机 `#666666` 照做 | 全套 `#666666` 1022 次、`#656565` 只有 3 处 |
| `30107` 的取消原因有重复项 | 照抄 | 稿自带 |
| `34192` 把 subscription 拼成 `subscoption` | 照抄 | 稿自带 |
| `33116`/`33119` 的 `Delivery Instrctions` | 照抄 | 稿自带 |
| `30465` 的 July 2026 月历排错（1 号排在 Su 列、有一格写 `32`） | **不照抄**，日历是算出来的 | 照抄等于交一个排错的死日历 |
| 三个桌面稿全叫「Account Overview Desktop」 | 按 24px 标题认，是三个不同页面 | 复制未改名 |
| 桌面 CANCELLED 卡删的是 Shipping 行 | 按便签 + 手机稿删 Renewal 行 | 便签 `28323` 明写 |
| 桌面 PAUSED 卡日期还是 `19 Jul 2026` | 按手机稿 `17 Aug 2026` | 便签 `28321` |
| 同一地址两张板邮编 `3182` / `3181` | 各按各自的板 | 需设计方给出哪个对 |

### 5c. 有意的实现取舍

- **桌面两栏 gutter 是 244 / 352 不对称** —— 三个桌面稿完全一致，判定为有意，没改成居中。
  内容列用 `minmax(0,1fr)` 而不是稿上的固定 571：**照抄则 768 档横向溢出 864 > 768**（实测）。
- **弹窗滚动锁复用站内的 `is-modal-open`，没有另起一套**。自己写一套（html+body 都
  `overflow:hidden` + 两边都补 `padding-right`）实测坏两处：`.gb-acct-header` 是
  `position: sticky`，body 变成 scrollport 后**当场掉出视口**；补偿付了两遍滚动条宽度。
- **弹窗里的滚动区把 `data-lenis-prevent` 直接写在标签上**，没有去登记 `main.js` 的
  `smoothScroll.PREVENT`（PLAN Task 8 步骤 4 原本要求登记）。行为等价，而且不必碰主站线的文件。
  ⚠ `main.js` 的 PREVENT 扫描**只在 init 跑一次**，所以后加的容器登记了也没用。
- **account.scss 没有写 blanket 的 `prefers-reduced-motion` 规则**。
  `customstyle.scss` 顶部已经有一条 `*, *::before, *::after { ... !important }`，
  account.css 在它之后加载，所有过渡本来就被压平了 —— 再写一遍是死代码。
  `tools/acctmotion.py` 证明了它确实够得着（并且用 `no-preference` 的读数做不变量对照，
  防止「元素压根没有过渡」也算过）。
- **弹窗头脚的分隔线用 `box-shadow: inset`，不是 `border`** —— 稿上是
  `strokeAlign: INSIDE`，用 border 会让每个面板比板高 2px。
  ⚠ 但**卡片框**（地址 `32448` / 成功 `32932`）的 `strokesIncludedInLayout` 是 `true`，
  那里要写**真 `border`**。同一批板里两套规则，改之前先查这个字段。
- **弹窗的脚固定 72 高（抽屉 80）**，哪怕里面只有一个 Cancel。没按钮的面板自然高只有 52，
  所以 `min-height` 是写死的。
- **贴底抽屉是定高不是上限**：五张挽留板全是 `v:FIXE 672`，用 `max-height` 会让内容少的屉缩水。
- **登录/注册用站点 header 而不是 account header** —— 板上的 instance 就是站点那个组件，
  未登录访客也没有 account 菜单可开。
- **auth 的提交按钮没有用站点的 `.gb-btn--lg`**：那个类在 ≤767 会掉到 44 高（客户 r133 的决定），
  而稿上的手机按钮**仍是 52 高**。account 线本来也是「按钮全自写」（`account.html` 里
  `.gb-btn` 出现 0 次）。
- **手机 auth 的间距比桌面大**：按钮 ↔ alt 行 ↔ note 卡，桌面 32、手机 **48**。两套板都是这么画的。

### 5d. 预览时会以为坏了、其实没坏

- **Overview 的三种订单状态 / 订阅三态 / 详情各状态，都没有 JS 会自己切**。
  预览要在 devtools 里改属性：
  `[data-acct-order-state]` = `preparing` / `shipped` / `renewal`；
  `.gb-acct-detail[data-acct-sub-state]` = `active` / `paused` / `cancelled`；
  `.gb-acct-detail[data-acct-discount]` = `applied`。
- **`Flavour` 下拉不可交互是便签 `30913` 要求的**，不是没接上。
- **表单提交只会跳回 `#`** —— 三个页面的 form 都是 `action="#"` 的静态壳。
- **`.wowo` 入场动画在 account 页没有用**，页面不会淡入。
- **三个视图都在 DOM 里**，devtools 里能同时看到三份同名元素 —— 只有一个不带 `hidden`。

---

## 6. 上线前必须替换的占位内容

⚠ 这些混在正文里看不出来，不单独列就一定会带上线。完整表在 [SPEC.md](SPEC.md) 第 8b 节，
其中**最要紧的一条**：

- **`images/refer-friends.jpg` 画面里有第三方品牌 logo（帽子上的 Prada 标）**。
  它是设计稿用的市售摄影素材，客户站点直接用有商标风险，授权来源未知。

其余是示例姓名（`Hi, Susanna`）、示例日期、示例价格（小计与总计都写着 `$00.00`）、
示例订阅数据、四条重复的产品行、以及四处 `href="#"`
（View Order / Refer a Friend / Re-Activate Subscription / Forgot your password）。

---

## 7. 现状与遗留

**PLAN 94/95 步**，15 个 Task 只剩最后一步提交。三个页面、19 类弹窗、37 个弹窗态全部落地。

- ⚠ **`~/.cache/ms-playwright/chromium-1217` 已不存在**。playwright 1.58 装的是 **1208**，
  1217 是过时残留、被清掉了。`tools/` 下**约 150 个脚本**把 1217 写死在 `CHROME` / `EXE` 里。
  本轮把 `acctcheck.py` 与 `acctmodal.py` 改成扫 `chromium-*` 取最新，**其余脚本没动**
  （多数是主站线的）。为了让它们继续能跑，留了一条软链
  `~/.cache/ms-playwright/chromium-1217 -> chromium-1208`：在 `~/.cache` 里、不在仓库、
  不会被同步脚本推上线。**要重装 playwright 之前先 `rm` 掉它。**
- **`account.html` 的主站资源版本号还停在 `?v=20260909-r134`**，两个 auth 页写的是 `r138`
  （与 11 个 MVP 页一致）。主站线的批量替换看来不含这三个文件，需要 account 线自己跟进。
- **SPEC 第 7 节的待裁决已积到 A–AB**，全部**已按暂定方案实现、一处可改**。
  最需要设计方回话的几条：A（导航条目四个版本不一致）、E（21 类弹窗的桌面稿全缺）、
  G / Z（header 到底用哪个）、C（五个只有手机稿的页面做不做）。
- **Shopify 化还没开始**。接主题时 auth 两页要换成 `customers/login` / `customers/register`
  的真实 form；样式必须**单文件**（`assets/` 不接受子目录），图片放与 `assets/` 平级的 `images/`。

---

## 8. 接手第一件事

```bash
grep -c '^- \[x\]' docs/account/PLAN.md      # 进度
python3 tools/acctcheck.py                    # 1 分钟，拿基线
python3 tools/acctmodal.py &                  # 4 分钟，后台
```

跑出来的数字对不上第 4 节的基线，先查是不是忘了编译 scss，再查是不是另一个会话
动了共用文件（`find . -newermt "HH:MM"` + `ls -lt ~/.claude/projects/*/*.jsonl`）。

# Gumi Account — 变更记录

> account 静态页自成一条线：独立 `assets/account.scss` / `.css` / `.js`，独立版本号
> `$build-acct`（**与现站的 `$build` 无关，别混**），判据 `tools/acct*.py`。
> 计划在 [PLAN.md](PLAN.md)，设计决策与待裁决在 [SPEC.md](SPEC.md)。
>
> 约 10 项记一条，只写「改了什么 / 为什么 / 文件清单 / 遗留」。

---

## Task 5 — My Subscriptions 列表与三种订阅状态（`$build-acct` = `20260909-a3`）

**设计源**：桌面 `2284:28000`（同屏三态）；手机 `2284:28305`（同屏三态）、
`2284:34046`（Cancelled + Paused）；便签 `28321` paused / `28323` cancelled / `28325` +N。

### 做了什么

- **页头 `.gb-acct-intro`** —— 桌面是 `#daf6b0` 卡片（r14、pad 24/32、min-h 136、
  标题 800 24/30、副标 400 14/22 且 `max-width: 409`）；手机去掉卡片，改成
  白色圆形返回键（32、r40）+ 文字（20/24 与 12/18）。**返回键在 Overview 页是关掉的、
  在这页是开的**，同一个 `Account Header` 组件的两种用法。
- **订阅卡 `.gb-acct-sub`** —— 白底 + `#e6e6e6` 1px + r12，三段：head（pad 20、
  底边 1px）/ body（pad 24，手机 20）/ foot（pad 4-24-24，手机 8-16-20）。
  续订与配送两行桌面并排（gap 16）、手机上下堆叠。产品行固定 `max-width: 308`。
- **状态徽章 `.gb-acct-pill`** —— 24 高、r52、Inter 500 12/18 大写，左侧是一个
  16 的白盘套 11.74 的环（`border: 3.07px`）。三态取色全部来自节点：
  active `#cbf390`/`#005635`、paused `#ffefc3`/`#fd871a`、cancelled `#cccccc`/`#4d4d4d`。
  新增 `$c-amber-{100,300,500}` 三个 account-only 变量。
- **三态由 `[data-acct-sub-state]` 驱动**，选择器写在属性上而不是修饰类上，
  Task 6 的详情页可以直接复用同一个徽章。paused 把 `__summary` 压到 0.4；
  cancelled 把 `__meta` 与 `__summary` 都压到 0.4，并隐藏续订行。
- **卡片整块不可点**：稿上只有按钮可点，所以卡片没有 `cursor: pointer` 也没有 hover
  （全局铁律 13 的反面）。CTA 文案按状态取 `Manage Subscription` / `Re-Activate Subscription`。

### 顺带修正了 Task 4 的一处还原错误

**桌面浅绿带与波浪原来高了 73px**，波浪的扇贝直接横穿侧栏和问候卡。
原因是 `123` / `114` 这两个数是拿板坐标减错了基准算的：板 `27678` 的 `main` 起点在
`179.6`，矩形底在 `1043`、波浪顶在 `367`，相对 `main` 应该是 **196.4 / 187.4**。
已改成 `196` / `187`，手机档（176）本来就是对的、未动。判据补了
`.gb-acct__wave{top}` 两条，活性自检 C 验过。

同时把手机的起始留白拆开：外壳 `.gb-acct__inner` 只留板上 `Account Header` 自己的
`padding-top: 8`，剩下的归各视图 —— Overview 因为返回键是关的、文字从 40 起，
所以 `.gb-acct-ov` 补 `padding-top: 32`；Subscriptions 的返回键是开的，从 8 起。
两者相加与改动前一致，Overview 的渲染没有位移。

### 稿件两处自相矛盾，按便签 + 手机稿做

1. **CANCELLED 删错了行**：桌面 `28146` 删 Shipping、留 Renewal；便签 `28323` 写的是
   「Renewal date removed」，手机 `28316`/`34055` 也是删 Renewal。→ 隐藏续订行。
2. **PAUSED 的续订日期**：便签 `28321` 说显示「暂停到期日」，手机写 `17 Aug 2026`，
   桌面 `28109` 还留着 active 的 `19 Jul 2026`。→ 取 `17 Aug 2026`。

两条都记进 SPEC §8。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | subscriptions 视图填入 intro + 三张卡；`?v=` 升到 `a3` |
| `assets/account.scss` | 新增 My Subscriptions / 徽章 / 卡片正文三段；新增 `$c-amber-{100,300,500}`；修正 `.gb-acct::before` 与 `.gb-acct__wave` 的桌面值；`.gb-acct__inner` 手机 padding-top 40→8，`.gb-acct-ov` 补 32 |
| `assets/account.css` | 编译产物（双写） |
| `tools/acctcheck.py` | 追加 Task 5 断言 141 条；新增 `("account.html", 390, GOTO_SUBS)` 组；`GOTO_SUBS` 的触发元素改成按宽度选（手机档侧栏是 `display:none`，只能点页内列表卡） |
| `images/acct-{sub-renewal,sub-shipping,back-arrow}.svg` | 新增 3 个 |
| `figma/account/cut-icons.py` | JOBS 支持第 4 项「SVG 文件名」——三个同名桌面板导出时按真实页名重命名过，节点文件名与 SVG 文件名对不上。⚠ 仍在 `.gitignore` 的 `figma/` 内，不入库 |
| `docs/account/SPEC.md` | §8 新增两条稿件错误；§8b 新增缩略图占位与示例订阅数据 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctcheck.py` | **314 ok / 0 red**（Task 4 收尾是 173） |
| 活性自检 A：cancelled 的 `opacity: .4` 改成 1 | 转红 3 条 ✅ |
| 活性自检 B：删掉 cancelled 的 `[data-acct-sub-renewal]{display:none}` | 转红 2 条 ✅ |
| 活性自检 C：色带高度退回旧的 123 | 转红 1 条 ✅（证明这条断言真的在管色带） |
| 活性自检 D：徽章 r52 改 4 | 转红 1 条 ✅ |
| `tools/rwd.py account.html` | 全绿 |
| 订阅视图单独扫溢出（13 档，`#subscriptions`） | 0 溢出 |
| `tools/acctvars.py` | 54 ok / 0 red（新增三个 amber 只 note） |
| 肉眼对稿 | 1440 对 `2284-28000`、390 对 `2284-28305`，逐块一致 |

### 已知偏差（不要报成 bug）

- **徽章圆环的边框读回来是 `3px` 而不是 `3.07px`**：border-width 的 used value 取整数像素。
  源码里仍写 `3.07px`（节点值 3.0674），断言按取整后的值写。
- **圆环直径读回 `11.7344px`**：`11.74px` 落到 1/64 像素网格上的结果，节点值是 11.742387。
- **桌面 CANCELLED 卡比稿少一行**（隐藏了续订行、保留配送行）——见上文，是照便签做的，
  与桌面板不同是**有意的**。
- **PAUSED 卡的日期与桌面板不同**（`17 Aug` vs `19 Jul`）——同上。
- **产品缩略图是灰块**：`196:19033` 在所有板上都是纯 `#d9d9d9` 矩形，设计里就没有产品图。
- **CTA 的 hover 用 `opacity: .85`**，与 Task 4 的 `.gb-acct-order__cta` 同一套；
  返回键沿用 `.gb-acct-refer__action` 的位移写法（反向 `-2px`）。交互态稿里全缺，见待裁决 K。

### 遗留

- `Manage Subscription` 指向 `data-acct-goto="detail"`，详情视图 Task 6 才填内容，
  现在点过去是空壳。`Re-Activate Subscription` 是 `href="#"`（重启流程无稿）。
- `account.html` 里 `customstyle.css` / `main.js` 的 `?v=` 还停在 `20260908-r105`，
  而现站那条线已经滚到 `r124`。**没动**，那是另一条线的批量替换范围。

---

## Task 4 — Account Overview 视图与三种订单状态（`$build-acct` = `20260909-a2`）

**设计源**：桌面 `2284:27765`（在 `27678` 内）、手机 `2284:27604`；
三态 `2284:27450` preparing / `27499` shipped / `27548` renewal。

### 做了什么

- **问候块 `.gb-acct-hello`** —— 桌面是 `#daf6b0` 卡片（r14、pad 24/32、gap 8、
  `Hi, Susanna` 800 24/30、`Welcome back!` 400 14/22）；手机去掉卡片只剩文字（20/24 与 12/18）。
- **订单卡 `.gb-acct-order`** 三态，`data-acct-order-state` authored 在元素上，无 JS。
  preparing / shipped 深绿白字，**renewal 整个反过来**：卡底 `#cbf390`、标题变
  `#a7e746` 的标签块（r4、pad-inline 8）、正文与状态转深绿、CTA 变绿底白字且文案是
  `Manage Subscription`。
- **Refer a Friend 卡 `.gb-acct-refer`** —— `#f5f1e9` 底、圆形头像（桌面 80 / 手机 66）、
  `#cbf390` 标签、白色圆形箭头按钮（40 / 32）。
- **Logout 按钮 `.gb-acct-logout`** —— 手机专有（桌面的 Logout 在侧栏），52 高、r72、深绿底。
- **浅绿带 + 波浪** —— `.gb-acct::before` 把 header 的 `#e7f8d0` 往下延伸，底边接一个
  `.gb-scallop`（新变体 `--mint-to-cream`）。页面底色设成 `$c-cream`（`2284:27604` 的 fill），
  否则白色的列表卡组在 body 的纯白上完全看不出来。
- **问候区装饰小熊** —— lime 描边 + 旋转 18.47° 的小熊照片，裁在 113.9x145（桌面）框内，
  桌面允许它探出卡片右边 41.9。

### 三个把人绊住的地方

1. **三个 icon 槽在板上是 `visible=false`**：两个 CTA 按钮的图标与手机问候区的返回箭头。
   组件自带槽、节点 JSON 里结构完整，只有 `visible` 字段能分辨。
   **交叉验证**：Figma 导出不含隐藏节点，所以整块 board SVG 在那个位置没有 path ——
   `cut-icons.py` 报「no path inside」是**确认**不是失败。三个都没做。
2. **旋转节点的 bbox 不是画面**：小熊 `2284:27653` 记的 186.5x164 是旋转后的包围盒，
   真正的框是 188.9x145.7（桌面）。另外**不能把图居中于裁切框** —— 熊在自己的 PNG 里偏左，
   居中会露出空白的右半边；按节点坐标算出 `left: -33.5px` 才对。
3. **`img { max-width: 100% }` 会压垮它**：装饰图故意比裁切框宽，全局规则把它压回框宽，
   旋转后就转出一个扁盒子。判据里锁了 `max-width: none`。同族坑见
   memory `theme-img-rule-blows-up-unsized-img`。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | overview 视图填入 hello / order（三态槽）/ refer / logout + 顶部 `.gb-acct__wave` |
| `assets/account.scss` | 新增 Overview / 订单卡 / Refer / Logout / 装饰 / 波浪变体六段；新增 `$c-lime-300` `$c-lime-500` 两个 account-only 变量 |
| `assets/account.css` | 编译产物（双写） |
| `tools/acctcheck.py` | 追加 Task 4 断言 88 条；新增 `STATE_PREPARING` / `STATE_RENEWAL` 两个动作 |
| `images/refer-friends.{jpg,webp}` | 新增，Refer 卡头像 |
| `images/acct-bear-side.{png,webp}` | 新增，问候区装饰小熊 |
| `images/acct-{order-preparing,order-shipped,order-renewal,logout,action-arrow,bear-halo}.svg` | 新增 6 个 |
| `figma/account/make-images.py` | **新建**（位图派生）⚠ 在 `.gitignore` 的 `figma/` 内，不入库，与 `optimize-images.py` 同惯例 |
| `figma/account/cut-icons.py` | **新建**（从整块 board SVG 按节点 bbox 裁图标）同上不入库 |
| `docs/account/SPEC.md` | 待裁决新增 L / M；稿件错误新增两条；新增 §8b「上线前必须替换的占位内容」 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctcheck.py` | **173 ok / 0 red** |
| 活性自检 A：删掉 renewal 的整块状态覆盖 | 转红 7 条 ✅ |
| 活性自检 B：删掉 `[data-state]{display:none}` | 转红 7 条 ✅（三个文案槽同时显示） |
| `tools/rwd.py account.html` | 全绿 |
| `tools/acctvars.py` | 54 ok / 0 red（两个 account-only 变量只 note） |
| 三态肉眼对稿 | 390/1440 各三态截图逐个比对 `2284-27450/27499/27548`，一致 |
| 卡片尺寸实测 | 桌面 hello 571x136 / order 571x168 / refer 571x128，手机 refer 350x98 —— 与稿一致 |

⚠ **判据里读状态切换后的颜色必须等够过渡时间**：首跑 2 red 是 `rgb(19,99,68)`，
那是 `$t-base` 0.2s 走到一半的插值，不是样式错。等待已从 120ms 提到 450ms。

### 已知偏差（不要报成 bug）

- **手机订单卡 192 高，稿 188**。差 4 来自 label：稿的 TEXT bbox 记 20，但 style 的
  line-height 是 24，CSS 行盒取 24。属 Figma 与 CSS 的固有半行距差异
  （memory `figma-rounds-half-leading-css-does-not`），未强压。
- **手机波浪 48 高，稿的 `Spacer Bottom` 是 36**。复用了现站 `.gb-scallop`（全站一致优先），
  已登记待裁决 L。
- **桌面 hello 卡 `min-height: 136px`**：稿的 frame 固定 136 而内容只有 108，
  多出的 28 是文字下方的空白，不是 padding。
- **手机 hello 到 order 的间距是 32，稿 34**：32 是 container `2284:27615` 自己的 gap，
  34 是跨容器量出来的。取了前者。
- **桌面 renewal 态是外推的**（`27548` 只有手机稿），见待裁决 M。

### 遗留

- **`images/refer-friends.jpg` 画面里有第三方品牌 logo**（帽子上的 Prada 标）——
  已列进 SPEC §8b「上线前必须替换」。
- Subscriptions / Detail 两个视图仍是空壳（Task 5–7）。
- 导航项左侧的灰色圆点没做（便签 `27602` 说是待设计图标的占位，PLAN 明确不做）。

---

## Task 3 — 桌面竖导航、手机列表卡与视图切换（`$build-acct` = `20260909-a2`）

**设计源**：桌面 `2284:27843`（在 `27792` 内，与 `27678`/`28000` 逐值相同）、
手机 `2284:27617`（在 `27604` 内）、两栏外壳 `2284:27842`。

### 做了什么

- **桌面竖导航 `.gb-acct-nav`**（241 宽，5 组，组间 16）。组白底 `#fff` / 圆角 8 / 内边距 8；
  行 40 高、圆角 8、`padding-inline: 16`、PP Palma 400 14/20 ls −0.28 色 `#1a1a1a`；
  当前行 `#f3f3f3`。9 项：Account Overview / My Subscriptions / Order History ‖
  My Details / Change Password ‖ Refer a Friend ‖ Help / Contact Preferences ‖ Logout。
- **手机页内列表卡 `.gb-acct-list`**（4 组 6 项，组间 16）。组白底圆角 8 **内边距 0**，
  行 68 高、`padding: 24 16`（手机没有固定高压着，24 是真生效的）。
  行间分隔线取自 `Line 79`：326 宽（左右各缩 12）、1px、`#faf9f8`。
- **两栏外壳 `.gb-acct__inner`**：`241px minmax(0,1fr)`，`column-gap 32`，
  `padding: 48 352 144 244`。
- **`view` 模块**（`account.js`）：`[data-acct-goto]` 事件委托 + hash 同步 + 未知 hash 回退
  overview + `is-current` / `aria-current` 同步。header 汉堡菜单前两条也接了 `data-acct-goto`
  （保留 `<a href="#overview">` 做渐进增强）。

### 为什么这么定

- **桌面 9 项、手机 6 项，是两套并存不是一套折叠**。手机卡不含 Account Overview（你就在这页）
  与 Contact Preferences，Logout 在稿上是卡外的独立绿按钮（`2284:27648`，属 Task 4）。
  两者用 `display` 在 767 互斥切换。
- **内容列用 `minmax(0,1fr)` 而不是稿上的固定 571**。三个桌面稿一致地画
  `244 + 241 + 32 + 571 + 352 = 1440`，恰好铺满；照抄则 **768 档横向溢出 864 > 768**
  （`rwd.py` 实测，见下方判据）。1440 下 1fr 算出来正是 571，与稿逐值一致。
- **`244 / 352` 不对称但三稿完全相同**，判定为有意，未擅自改成居中。收敛方式无稿，
  已登记 SPEC 待裁决 A2。
- **六个无稿项渲染成 `aria-disabled` 的 `<span>`**，不是死链也不建页面（待裁决 C）。
  Logout 是 `<button data-acct-logout>` 空壳 —— 登出需要后端，不在 MVP。
- **禁用行与当前行不响应 hover**：前者不可点（全局铁律 13），后者已是填充态，
  hover 回 cream 会读作"离开了本区"。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | `<main>` 换成 `.gb-acct__inner` 两栏；新增 `.gb-acct-nav` 9 项、overview 视图内 `.gb-acct-list` 6 项；菜单前两条加 `data-acct-goto`；`?v=` → a2 |
| `assets/account.scss` | 新增 Shell 两栏 / 桌面 nav / 手机 list 三个分区；`$build-acct` → `20260909-a2` |
| `assets/account.css` | 编译产物（双写） |
| `assets/account.js` | 新增 `view` 模块，挂进 `modules` 与 `window.gumiAcct`（**排在 `acctNav` 之后**，它 init 里调 `closeMenu()`） |
| `tools/acctcheck.py` | 追加 Task 3 断言 45 条；新增 `GOTO_SUBS` 动作与 `shown` 检查类型 |
| `docs/account/SPEC.md` | 待裁决 A 补上真实规律、新增 A2；第 8 节新增「三个桌面稿同名」 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctcheck.py` | **82 ok / 0 red**（Task 2 的 37 条 + Task 3 的 45 条） |
| 活性自检 A：删掉 `.gb-acct-list` 的 `@include narrow` | 转红 2 条 ✅ |
| 活性自检 B：把 `view` 模块摘出 `modules` | 转红 7 条 ✅ |
| 活性自检 C：内容列改回稿上的固定 `571px` | `rwd.py` 报 `768 横向溢出 864>768` ✅ |
| `tools/rwd.py account.html` | 全绿 |
| Playwright 实测 hover（headless 直连 `(hover:hover)` 恒 false） | 可点行变色 / 禁用行不变 / 当前行不变，3/3 |

### 遗留

- **视图内容全空**，三个 `<section data-acct-view>` 只有 overview 放了列表卡，
  Subscriptions / Detail 是空壳 —— 属 Task 4–7。**因为空，视图切换只能用 `hidden` 属性
  断言**（`shown` 检查），不能用渲染尺寸：空 section 高度为 0，`vis` 分不出"切掉了"和"是空的"。
- **顺带发现未修**（超出本轮范围，等拍板）：header 汉堡菜单里 `My Details` 与 `Log Out`
  仍是 `href="#"` 死链，是 Task 2 的遗留。菜单只有 4 条而桌面导航 9 条，也属待裁决 A。
- **手机列表卡的位置**（它在 Overview 页里排第几、上下间距）取自 `2284:27615` 的
  `gap 32`，但那要连同 `Hi Susanna` 卡片一起摆，留给 Task 4。
- 交互态的 hover 底色借用了 `$c-cream`，是自定值（待裁决 K），未登记进 motion 段变量表。

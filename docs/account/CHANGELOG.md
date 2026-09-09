# Gumi Account — 变更记录

> account 静态页自成一条线：独立 `assets/account.scss` / `.css` / `.js`，独立版本号
> `$build-acct`（**与现站的 `$build` 无关，别混**），判据 `tools/acct*.py`。
> 计划在 [PLAN.md](PLAN.md)，设计决策与待裁决在 [SPEC.md](SPEC.md)。
>
> 约 10 项记一条，只写「改了什么 / 为什么 / 文件清单 / 遗留」。

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

# Gumi Account — 变更记录

> account 静态页自成一条线：独立 `assets/account.scss` / `.css` / `.js`，独立版本号
> `$build-acct`（**与现站的 `$build` 无关，别混**），判据 `tools/acct*.py`。
> 计划在 [PLAN.md](PLAN.md)，设计决策与待裁决在 [SPEC.md](SPEC.md)。
>
> 约 10 项记一条，只写「改了什么 / 为什么 / 文件清单 / 遗留」。

---

## Task 12 — 配送地址弹窗与表单校验（`$build-acct` = `20260910-a10`）

**设计源**：`2284:32294` 当前地址 / `32940`·`33161` 表单 / `32779` 成功。

### 「两个表单变体」其实是一个面板

`32940` 与 `33161` 逐节点相同，只差三行数据（`12 Charnwood Road / St Kilda / 3181`
与 `20 Park Avenue / Richmond / 3121`）。所以只做一个 `shipping-form`，
判据反过来利用这一点：**要改的值全部取自另一张板**，不自造测试串。

⚠ PLAN 里说 `2284:33129` 是表单的滚动容器，**不对** —— 它浮在板外、比弹窗里那份
少一个字段（686 vs 800），是旧草稿。真正的滚动容器是 `33092`。

### 三处把卡片撑高的地方

1. **这两张卡的描边要算进盒子**。`32448` / `32932` 是同一个框，
   `strokesIncludedInLayout: true` —— `16 + 内容 + 16 + 1 + 1` 才等于板上的 178 / 78。
   和头脚的发丝线正好相反（那两条 INSIDE 但不占高，必须写 `box-shadow: inset`）。
   两处不能互抄，已写进 [MODAL-SPECS](MODAL-SPECS.md) §7。
2. **`32458` 是这批板里唯一带 `textTruncation: ENDING` + `maxLines: 1` 的文本**。
   判据是它的 `absoluteRenderBounds` 只有 240.99，而同一串在浏览器里自然宽 278.6 ——
   其余五行两边差都 <1px，所以只有这一行是被截断的。不截断，卡片就是 198 而不是 178。
   ⚠ 光加 `white-space: nowrap` 还不够：它会变成整列的**自动最小尺寸**，
   卡片被撑宽而不是把字裁掉，得在两层 flex 上补 `min-width: 0`。
3. **`SPACE_BETWEEN` 会吞掉 `itemSpacing`**。地址卡写着 gap 24，实测两个孩子之间只剩
   9.8；把 24 当真 gap 写进 CSS，文字列窄 12px，那行照样折。

### 表单

- **校验交给浏览器**：`.gb-acct-modal__panel` 本身就是 `<form>`，
  必填用 `required`、邮编用 `pattern="\d{4}"`。板上**没有错误态**，
  自画红框/提示语等于自拟视觉；原生校验还免费带键盘与读屏。
- **链到成功页挂在 `submit` 上，不是按钮的 `click`** —— 校验不过根本不会有 `submit`。
  `e.preventDefault()`，不提交到任何后端。
- **`+61` 是 29 宽的纯文字前缀，不是国家选择器**：它旁边的 chevron（`196:17798`）
  在板上 `visible=false`。因为要待在描边里，电话这一格的边框从 input 移到了
  `.gb-acct-field__box`，input 变透明无边。
- **必填星号没有自己的颜色**：`33096` 的 Label 没有 `characterStyleOverrides`，
  `*` 与标签同为 `#666666`。判据因此改成验「标签里没有第二个元素」。
- **State 用原生 `<select>`**（同 `edit-frequency`：板上只有闭合态）。
  候选项填了澳洲 8 个州的标准缩写，登记在 SPEC 待裁决 V。

### 顺带修掉的两处旧账

- **`<select>` 上没关原生箭头** —— `edit-frequency`（Task 9）一直画着两个 chevron：
  板上的那个 + 浏览器自己的。加 `select.gb-acct-field__input { appearance: none }`，
  并给两个 `<select>` 都补了断言。
- **占位符用的是浏览器默认灰**。板上三处占位（`Discount Code` / `Company` /
  `000 000 000` / `Delivery Instrctions`）全是 `#666666`，与真实值同色，补 `::placeholder`。
- **`_snapshot` 读不出单选**：单选的 `value` 是常量，变的是 `checked`。
  地址面板是第一个用单选的脏值门控，不改就永远醒不来。

### 遗留

- **桌面的成功提示折成两行**：面板宽锁 390（用户已定）而桌面内边距按卡片惯例是 24，
  内容盒比手机窄 8px，`32937` 那句正好放不下（254 → 274）。记进 SPEC 待裁决 E。
- 板上错字 `Delivery Instrctions`、同一地址两张板邮编 `3182`/`3181` 打架，已登记 SPEC §8。
- `shipping-current` 只画了一个地址却有单选钮，Save 因此恒灰；未选中态无稿。待裁决 S / U。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | `shipping-current` 填入地址卡与脚；新增 `shipping-form`（`<form>` 面板）与 `shipping-success`；`?v=` → `a10` |
| `assets/account.scss` | 新增 `.gb-acct-addr` / `.gb-acct-form` / `.gb-acct-note` 三族与 `.gb-acct-field__box`·`__prefix`·`__bare`·`__input--area`；`select.gb-acct-field__input` 关原生箭头；两处 `::placeholder`；新增 `$c-acct-radio` |
| `assets/account.css` | 编译产物（双写） |
| `assets/account.js` | `modal.init` 加 `submit` 监听；`acctForm._snapshot` 认单选 |
| `images/acct-note-ok.svg` | 新增（绿盘 + 白勾，双色，不走 currentColor 改写） |
| `tools/acctmodal.py` | 新增 `check_shipping` 三段；主循环只枚举 detail 视图里的触发器，另加「任意触发器都要有面板」的全页扫描；`check_forms` 补 `<select>` 箭头断言 |
| `docs/account/SPEC.md` | 待裁决 S/T/U/V；E 补桌面代价；§8 补两条板错 |
| `docs/account/MODAL-SPECS.md` | §7 卡片框、§8 单行截断 |
| `figma/account/cut-icons.py` | 追加 1 条 JOBS + `KEEP_STROKE`。⚠ 不入库 |

### 判据

```
tools/acctmodal.py   1001 ok / 0 red / 2 aborted   （Task 11 收尾 834）
tools/acctcheck.py    541 ok / 0 red    rwd 全绿   acctvars 54 ok   assetpath GREEN
双写一致 IN SYNC      node --check OK
活性自检 两轮 11 处突变 → 31 红：去掉单行截断 / 压平 4·8 两层 gap /
  卡片描边改成 inset / submit 不再链 / _snapshot 只读 value /
  `<select>` 放开原生箭头 / 两栏 gap 15→24 / 去掉 textarea 的 lenis /
  提示图标 gap 12→16 / 去掉 suburb 的 required
面板高度对板：394 / 254；抽屉在 390x840 视口 672
```

---

## Task 11 — 折扣码弹窗三态（`$build-acct` = `20260910-a9`）

**设计源**：`2284:31488` 空 / `31648` 已填 / `31809` 已应用；
便签 `30919` 码不存在时按钮不变绿 / `30921` 已有码时入口文案 add→edit（Task 7 已做）。

### 「已填」不是第三份 DOM

`31648` 就是 `31488` 的输入框里有东西 —— 这是静态页**唯一判得了**的事。
所以 `data-acct-discount-state` 只有 `empty` / `applied` 两个值，
中间那态由输入框的值驱动。⚠ 便签 `30919`：**Apply 变绿不代表码有效**，
码存不存在是后端的事，前端只判「有没有输入」（`trim()` 后非空，纯空格不算）。

### 两处会让面板矮掉的地方

1. **脚在板上是固定 72，哪怕里面只有一个 Cancel**（`31646`）。
   有按钮的面板 `16 + 40 + 16` 自然就是 72，但折扣弹窗的脚没有按钮，
   自然高只有 52 —— 面板整整矮 20。补 `min-height: 72px`（抽屉那档是 80），
   对已有的六个表单面板是空操作。
2. **`31962` 是两层嵌套**：label 与输入行之间 6，整个字段组与结果条之间 **8**。
   压平成一层 `row-gap: 6` 再给结果条 `margin-top: 8`，结果条会低 6px。
   照板拆成 `.gb-acct-discount__field` 内层 6 / 外层 8。

修完两个面板高度与板逐值相等：**246 / 292**。

### 做了什么

- **输入行**（`31643`）：输入框与 Apply 共用一行、间距 8。板上是 `246 + 8 + 96 = 350`；
  实现让 **Apply 保持 96 固定、输入框弹性**，所以桌面多出来的 24 gutter 从输入框身上走，
  标签不会被挤。
- **Apply**（`31645`）：`96×44`、圆角 **8** —— 是行内字段按钮，不是脚里那个 40 高的胶囊，
  单独一个类。禁用 `#e6e6e6`/`#808080`，可用 `#005635`/白。
- **已应用的结果条**（`31969`）：`#f6feec` 底 + `#daf6b0` INSIDE 描边 + 圆角 8，
  右侧是**垃圾桶**图标（`565:46772`，不是叉）。
- **结果条文案的强调是颜色不是字重**：`31972` 的底色是 `#011307`，
  而 `Discount ` 与 ` applied $35.25 off` 两段被 override 成 `#4d4d4d` ——
  **只有 `CEO90` 是深色**。实现用 `<strong>` 但 `font-weight: 400`，只换颜色。
- 脚里**只有 Cancel**，两个面板都没有 `[data-acct-save]`（判据专门验了这条）。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | 两个折扣面板填入字段组 + 结果条 + 脚；面板加 `data-acct-discount-state`；`?v=` → `a9` |
| `assets/account.scss` | 新增 `.gb-acct-discount` 一族与 `.gb-acct-chip`；`__foot` 补 `min-height: 72px`（抽屉 80） |
| `assets/account.css` | 编译产物（双写） |
| `assets/account.js` | 新增 `acctDiscount`，挂进 `window.gumiAcct.discount` |
| `images/acct-chip-remove.svg` | 新增 |
| `tools/acctmodal.py` | 追加 `check_discount`（2 面板 × 2 断点）；chip 检查从「存在」改成「可见」 |
| `figma/account/cut-icons.py` | 追加 1 条 JOBS。⚠ 不入库 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctmodal.py` | **834 ok / 0 red / 2 aborted**（Task 10 收尾 768） |
| 活性自检：Apply 不再跟随输入 / 状态不再隐藏结果条 / 去掉脚的 72 下限 | 转红 **8** ✅ |
| `tools/acctcheck.py` / `rwd.py` / `acctvars.py` / `assetpath.py` | 未回归 |
| 双写一致 | IN SYNC |
| 面板高度对板 | 246 / 292，两个都中 |

### 遗留

- **Apply 与垃圾桶都只有前端行为**：不校验码、不真的移除折扣 —— 都要后端。
- **`31809` 的输入框在板上是空的**（占位文案 `Discount Code`），Apply 也是灰的 ——
  即「码已应用、输入框已清空」。照板实现。
- `CEO90` / `$35.25` 是板上的示例值，已在 SPEC §8b 的占位清单范围内。

---

## Task 10 — 产品编辑与新增弹窗、数量门控（`$build-acct` = `20260910-a8`）

**设计源**：`2284:30960`·`31145`·`33666` edit-product / `28942`·`29200`·`29399` add-product /
`33847` product-locked；便签 `34502` 最后一个产品不能减到 0 / `34504` 减到 0 时按钮变删除 /
`30917` 多产品滚动、按钮不动 / `30913`·`30915` Flavour 暂不可编辑（待裁决 J）。

### 三个面板都是 672 抽屉，尺寸与短弹窗不同

| 项 | 短弹窗 | 产品抽屉 |
|---|---|---|
| 体的上下内边距 | 24 / 20 | **32**（板值，两端一致） |
| 脚高 | 72（16 上下） | **80（20 上下）** |
| 左右内边距 | 24 桌面 / 20 手机 | 同 |

卡片网格取自 `29095`：两列 **168**、列距 **15**、行距 **24**。板上 `168+15+168 = 351`
装在 350 的内容框里（超 1px），实现改成 `minmax(0,1fr)` 平分而不是钉死 168 ——
只有一张卡时它仍落在左列，与 `30960` 画的一致。

### 数量门控：下限按卡声明，不按卡片数推断

PLAN 给的 `acctQty` 用 `root.querySelectorAll('[data-acct-product]').length === 1`
判断「是不是最后一个」。**这个推断在本实现里是错的** —— 便签 `34502` 说的是
「**订阅里**最后一个产品」，而面板渲染几张卡是另一回事：`30960` 只画一张卡，
但它照样能减到 0（`31145` 就是那个态），因为该订阅还有别的产品。

改成每张卡自己声明 `data-acct-qty-min`：`edit-product` / `add-product` 为 `0`，
`product-locked` 为 `1`。

### 「减到 0 = 删除」是每个面板自己选的，不是自动的

第一版按便签 `34504` 让任何卡到 0 都把 CTA 换成 `Remove this product`，**判据当场报红**：
`add-product` 的四张卡本来就都是 0，而板 `28942`/`29399` 的 CTA 仍是 `Add products` ——
**选购面板里的 0 是「没选」，不是「删掉」**。改成由 CTA 上的
`data-acct-label-zero` 显式声明，只有 `edit-product` 有（对应板 `31145`）。

### 做了什么

- **`edit-product`**：一张卡（Flavour + Size 两个下拉 + 步进器，QTY 1），CTA `Save`，
  到 0 时变 `Remove this product`。
- **`add-product`**：四张卡两列（Flavour + 步进器，QTY 全 0），CTA `Add products`；
  体是滚动区（`30917`），CTA 在脚里不随之滚动。
- **`product-locked`**：`33847` 的警示条（`#fbeae9` 底、`#f6d4d2` INSIDE 描边、coral 图标、
  `Sorry!` 深色其余 `#666`）+ 一张 QTY 1 且减号已禁用的卡。**它没有自己的触发器**，
  由 `gumiAcct.modal.open('product-locked')` 打开 —— 真实站点由订阅数据决定何时出现。
- **Flavour 下拉画出来但不可交互**（待裁决 J）：`aria-disabled="true"`、不绑事件、
  也不给 hover（铁律 13 反过来同样成立：不可点的别加 hover）。
- 步进器减号到下限时**禁用**，板 `34020` 的禁用底色就是 `#faf9f8`。

### 判据自己的两个「不可能失败」的洞（都补了）

活性自检把三处守卫全删掉后**只转红 4 条**，一查是判据的问题：

1. **禁用按钮不派发 click，程序化 `.click()` 也不派发** —— `product-laked` 的减号在标签里
   就带 `disabled`，判据的「再点一下必须被拒」永远打不出去，**那条 JS 守卫从没被测过**。
   改成先摘掉 `disabled` 再点、点完还原。
2. **`bind()` 只在 init 跑一次**，所以「重开面板会不会重复绑定」怎么测都是绿的。
   改成判据自己手动再调一次 `bind()` —— 那才是守卫存在的场景。

补完后同样的 mutation 转红 **14** 条（含 `product-locked` 下限被突破、三个面板的重复绑定），
这两类之前一条都抓不到。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | edit-product / add-product 填入网格与脚；新建 product-locked 面板（含警示条）；`?v=` → `a8` |
| `assets/account.scss` | 新增 `--sheet` 的体/脚内边距覆盖、`__alert`、`.gb-acct-prod-grid`、`.gb-acct-prod` 一族、`.gb-acct-qty` 三段式步进器 |
| `assets/account.css` | 编译产物（双写） |
| `assets/account.js` | 新增 `acctQty`，`modal.init` 里对每个面板绑一次，挂进 `window.gumiAcct.qty` |
| `images/acct-qty-minus.svg`·`acct-qty-plus.svg`·`acct-opt-chevron.svg`·`acct-alert.svg` | 新增 4 个 |
| `tools/acctmodal.py` | 追加 `check_products`（3 面板 × 2 断点）；修掉上面两个洞 |
| `figma/account/cut-icons.py` | 追加 3 条 JOBS；**bbox 有一边为 0 时自动撑开 2px**（减号是纯横线，viewBox 高度为 0 会什么都不画）；`acct-alert` 那条注释掉并说明不可自动重生。⚠ 不入库 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctmodal.py` | **768 ok / 0 red / 2 aborted**（Task 9 收尾 648） |
| 活性自检：删下限守卫 / 删禁用同步 / 删重复绑定守卫 | 转红 **14** ✅ |
| `tools/acctcheck.py` / `rwd.py` / `acctvars.py` / `assetpath.py` | 未回归 |
| 双写一致 | IN SYNC |

### 稿件不一致三处（照多数实现，已登记）

| 项 | 情况 | 取法 |
|---|---|---|
| Size 下拉 | `30960`/`31145` 有，`33666`/`33847` 没有 | edit-product 取有（自己那两张板都有），product-locked 取无（自己那张板） |
| Flavour 下拉 | `28942`（4 卡）有，`29200`/`29399`（2 卡）没有 | add-product 取有 |
| CTA 在 0 时的文案 | `31145` 换成删除，`28942`/`29399` 不换 | 按面板显式声明，见上 |

### 遗留

- **PLAN 步骤 7「把滚动容器加进 `main.js` 的 `smoothScroll.PREVENT`」未做** ——
  沿用 Task 8 的做法，`data-lenis-prevent` 直接写在 `.gb-acct-modal__body` 标签上，
  行为等价且不必碰 `main.js`；判据每个面板都验了这条。
- **`product-locked` 没有触发路径**：什么时候算「最后一个产品」取决于真实订阅数据，
  静态页判断不了。面板做好了，接后端时由数据决定何时 `open()`。
- **产品缩略图是 `#d9d9d9` 空方块** —— 板 `196:19033` 本来就没有产品图（SPEC §8b 已登记）。
- **四张卡是同一件商品重复四次**，板上就是如此，属占位数据。

---

## Task 9 — 六类表单弹窗与脏值门控的保存按钮（`$build-acct` = `20260910-a7`）

**设计源**：`2284:31330` edit-name / `31976` edit-date / `32135` edit-frequency /
`32463` edit-payment / `32621` skip-next / `33350` need-now；
便签 `27446` 脏值门控 / `27448` 预填当前值 / `30925` 频率只有 2·4·6 周。
共用组件值已抽成 **`docs/account/MODAL-SPECS.md`**，Task 10–13 直接查那份。

### 桌面怎么对齐（用户 2026-09-10 拍板）

用户定：**面板宽仍用板上的 390**，字号/间距/宽度按其他有桌面稿的部分对齐。
照这条去查，发现**字号根本不用改** —— 桌面板 `2284:27792` 与手机共用同一套阶梯：

| token | 桌面 `27792` | 手机 | |
|---|---|---|---|
| 行标签 / Cancel / Edit | `14/20 w400 -0.28` | 同 | 一致 |
| 按钮 / 总计 | `16/24 w500 -0.32` | 同 | 一致 |
| 小链接 | `12/18 w400 -0.24` | 同 | 一致 |
| 页标题 | `24/30 w800 -0.24` | 20/24 | 唯一有 ramp 的 |

Task 6 那个 `1.1554` **只作用在四个日期块上**，不是全局缩放。
所以桌面唯一真正的差异是**容器内边距**，弹窗照 account 自己的卡片惯例走：

| 元素 | 桌面 | 手机 | 中间 | 对照 |
|---|---|---|---|---|
| 头/体/脚 左右 | `24` | `20` | `fluid(20px, 24px)` | `.gb-acct-sub--detail .gb-acct-sub__head` |
| 体 上下 | `24` | `20` | `fluid(20px, 24px)` | `.gb-acct-sub__body` |
| 头 上下 | `20` | `20` | — | `.gb-acct-sub__head` 两端都是 20 |
| 脚 上下 | `16` | `16` | — | 板值 |

### 一个会让每个面板都高 2px 的坑

头的分隔线与脚的分隔线在板上是 `strokeAlign: **INSIDE**` —— 1px 画在 64 / 72 **之内**。
用 CSS `border-bottom` / `border-top` 会各加 1px，**每个面板都比板高 2px**
（判据允许 ±2，正好卡在边界上蒙混过关）。改用 `box-shadow: inset 0 ∓1px 0` 复现 INSIDE 描边，
六个面板的高度这才与板逐值相等：246 / 290 / 290 / 256 / 236 / 256。

### 做了什么

- **三个表单型**（edit-name / edit-date / edit-frequency）：标签 + 44 高控件（r8、`#cccccc`
  描边、`16/24` `#666`）+ 12/18 说明行。日期与频率各带一个尾部图标，从板 SVG 按 bbox 裁出。
- **三个确认型**（edit-payment / skip-next / need-now）：只有一段 `14/20` `#666` 正文。
  正文块是板上的 **320 固定宽**（三张板一致），左对齐、右侧留 30。
- **脏值门控**（便签 `27446`）：`acctForm.watch()` 在 init 时就给每个面板上表，
  改动任一字段解锁 Save，**改回原值再次锁上**。确认型没有 `[data-acct-field]`，不受管，
  板上它们本来就是绿的可用态。
- **`disabled` 同时写在标签里**，不只靠 JS —— 脚本没加载时按钮也不该可点，且避免
  「先亮一下再变灰」。
- **skip-next 的日期用 `<strong>` 单独描粗**：板上 `17 July, 2026` 是
  `characterStyleOverrides` 里的 w500 `#011307`，不是整句样式。
  edit-frequency 的说明行同理，`2026-07-19` 是 w800，且后面跟的是 **U+2028** 不是换行 ——
  HTML 里写成 `<br>`（memory `nl2br-blind-to-u2028`）。

### 与 PLAN 不同的一处：频率用原生 `<select>`

PLAN 步骤 3 要求「用现站 `selectBox` 的视觉规格重画一份自定下拉」。**没有照做** ——
板上 `2284:32135` **只有闭合态，展开态一张稿都没有**，自画列表等于自拟视觉（铁律 2/3）。
原生 `<select>` 与闭合态逐值一致（44 高 / r8 / `#cccccc` / `16/24` `#666` / 尾部箭头），
键盘与读屏行为免费，选项按便签 `30925` 只给 2 / 4 / 6 周。
要自定 listbox，需先拿到展开态的稿，或同意照搬现站 `.gb-select` 的规格。已登记 MODAL-SPECS §6。

### 一条自检本身是无效的，已替换

PLAN 步骤 5 让「删掉 `save.disabled = true` → 行为断言必须红」。实测**没有转红** ——
因为 `disabled` 也写在标签里，删掉 JS 那行初始态照旧。**这条自检证明不了任何事。**
换成删掉真正起作用的那部分（`input` / `change` 监听器），当场转红 6 条。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | 六个面板填入 body + foot；三个字段、两个尾部图标、三段正文；`?v=` → `a7` |
| `assets/account.scss` | 头补 INSIDE 描边与 24/20 gutter；body 补内边距与 cream 底；新增 `__foot` / `__copy` / `__hint` / `__fields` / `__save` 与 `.gb-acct-field` 一族；`$build-acct` → `20260910-a7` |
| `assets/account.css` | 编译产物（双写） |
| `assets/account.js` | 新增 `acctForm`，`modal.init` 里对每个面板上表，挂进 `window.gumiAcct.form` |
| `images/acct-field-date.svg`·`acct-field-chevron.svg` | 新增 2 个 |
| `tools/acctmodal.py` | 追加 Task 9 的 `check_forms`（6 弹窗 × 2 断点）；`<select>` 走 `select_option`；字段缺失时报红而不是崩 |
| `docs/account/MODAL-SPECS.md` | 新建 —— 弹窗共用组件规格 |
| `docs/account/SPEC.md` | §8 新增 `wan to skip` 错字 |
| `figma/account/cut-icons.py` | 追加 2 条 JOBS。⚠ 不入库 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctmodal.py` | **648 ok / 0 red / 2 aborted**（Task 8 收尾是 438） |
| 活性自检 A（PLAN 版：删 `save.disabled = true`） | **没转红 → 判定此自检无效**，已替换 |
| 活性自检 B1：删掉 `input`/`change` 监听器 | 转红 **6** ✅ |
| 活性自检 B2：桌面 gutter 退回 20 | 转红 **12** ✅（390 档保持绿，正确） |
| `tools/acctcheck.py` / `rwd.py` / `acctvars.py` / `assetpath.py` | 未回归 |
| 双写一致 | IN SYNC |
| 面板高度对板 | 246 / 290 / 290 / 256 / 236 / 256，六个全中 |

### 判据自己的一个 bug（Task 8 埋的）

Task 8 的 Lenis 滚轮探针收尾时写 `body.innerHTML = ''`，**把被测面板的内容整个抹掉**，
于是后面 Task 9 的检查量到的是空壳（`edit-name` 报「面板 178px 高」）。
改成只移除探针塞进去的那个 div —— **不能用 innerHTML 还原**，那会重建节点、
让 `acctForm` 捕获的字段引用全部失效，Save 再也醒不过来。

### 遗留

- **频率下拉的展开态无稿**（见上）。
- **正文块 320 固定宽**照板实现，右侧留 30 空；若那其实是漏改，改成 350 即可。
- **表单只有前端行为**，Save 不落任何数据 —— 决策里就没有后端。
- 板上错字两处照抄并登记：`wan to skip`（`32775`）、`Restart subscoption`（`34192`）。
- `edit-name` 另有一版 `2284:33508`（值是人名 `Susanna`），详情页用的是 `31330` 那版
  （值 `My Subscription`）。人名那版属 My Details 页，不在本计划内。

---

## Task 8 — 弹窗基础设施与滚动锁（`$build-acct` = `20260910-a6`）

**设计源**：`2284:31330`（居中卡结构）、`2284:28942`（贴底抽屉）、`MODALS.txt`（13 类 / 37 态标题）。

### 弹窗有两种形态，不是一种

把 29 个 390×840 弹窗板逐个量下来，形态**只有两类**，且判据一眼可分：

| 形态 | 高 | 位置 | 圆角 | 板 |
|---|---|---|---|---|
| **居中卡** | ≤394 | `top == bottom`，全部居中 | `12` 四角 | 17 张 |
| **贴底抽屉** | `672` = 840−168 | 贴底（`bottom == 0`） | `[12,12,0,0]` 只有上两角 | 12 张 |

抽屉那批内部固定是 `64 头 + 528 体 + 80 脚`，`528` 的体是滚动区
（`MODALS.txt` 里那个 `_Scroll bar` 16×528 就是它）。两种形态的遮罩都是
`#000000` @ **0.6**（`31476`），面板都是**满 390 宽**（板宽即面板宽，手机上左右不留边）。

### 与 PLAN 的写法不同的一处：不另起一套锁

PLAN 给的是新建 `.acct-locked`，`html` 与 `body` 都上 `overflow:hidden` + 都补
`padding-right`。**实测这在本页会坏两处**，所以改成复用站内已有的 `is-modal-open`
（`customstyle.css` 本来就加载在 account 页上）：

| PLAN 写法 | 实测后果 |
|---|---|
| `body { overflow: hidden }` | **`.gb-acct-header` 是 `position: sticky`，body 变成它的 scrollport 后当场掉出视口** —— 活性自检里读到 `headerTop = -485` |
| `html` 与 `body` 都补 `padding-right` | 让出来的滚动条宽度**付两遍**，居中布局左移半个滚动条 |

站内那份 CSS 早就解了这两个（body 用 `overflow-x:clip; overflow-y:visible`，
padding 只落在 `html`），再造一份等于把同样的坑重踩一遍。
**写同一个 class 不等于调 `main.js`** —— 两个脚本仍然互不调用，决策 6 不破。
⚠ `main.js` 的 `modal` 也用这个 class 驱动 `[data-modal]`；account 页上没有任何
`[data-modal]` 触发器，两者不会同时持锁。**以后若在此页加 `[data-modal]`，先关的那个会把另一个解锁。**

### 做了什么

- **`gumiAcct.modal`**（`account.js`）：`open(name, trigger)` / `close()` / `isOpen()`。
  委托点击 `[data-acct-modal]` 开、`[data-acct-modal-close]` 与遮罩关，ESC 关，
  Tab 在面板内循环，关闭后焦点回到触发器。**同时只允许一个面板**：开第二个会先收起第一个
  且**全程不松锁**。
- **补偿只测一次**：`is-modal-open` 已在就不再测 —— 取消流程 7 屏是同一个弹窗换内容，
  第二次测量会读到 0 并把第一次的补偿抹掉。
- **解锁等淡出结束**（`--acct-modal-exit`，随 `prefers-reduced-motion` 压到 `0.01ms`）；
  被顶掉的面板留了 token 守卫，过期回调不会去解锁顶替它的那个。
- **13 个面板壳**：遮罩 + 面板 + 头（标题 + 关闭叉）+ 可滚动 body。
  标题**逐字取自板**（`MODALS.txt`），`restart` 的 `Restart subscoption` 是板上的错字，
  照抄并已登记 SPEC §8。**body 全空**，内容是 Task 9–13。
- **关闭叉** `images/acct-modal-close.svg` 从板 SVG 按 `I2284:31481;30:887` 的 bbox 裁出，
  `figma/account/cut-icons.py` 加了一条 JOBS（该脚本在 `.gitignore` 的 `figma/` 内，不入库）。

### 两个静默坑

1. **`display:flex` 压过 UA 的 `[hidden]{display:none}`** —— 面板带着 `hidden` 仍然铺满视口、
   吞掉整页点击（判据里表现为 Playwright 报「subtree intercepts pointer events」）。
   补 `.gb-acct-modal[hidden] { display: none; }`。
2. **Lenis 吃滚轮**：`main.js` 的 `smoothScroll.PREVENT` 扫描**只在 init 时跑一次**。
   本轮**没有改 `main.js`** —— 直接把 `data-lenis-prevent` 写在 `.gb-acct-modal__body`
   标签上（Lenis 在 wheel 时自己读这个属性），行为等价。判据实测：摘掉属性后
   滚轮把面板 body 滚 **0px**，加上就正常滚。

### 文件清单

| 文件 | 改动 |
|---|---|
| `assets/account.js` | 新增 `modal` 模块（焦点陷阱 / ESC / 遮罩关 / 单面板 / 一次性补偿 / token 守卫），挂进 `modules` 与 `window.gumiAcct` |
| `assets/account.scss` | 新增 Modal 一段：外层 + 遮罩 + 面板（两形态）+ 头 + 标题 + 关闭叉 + 滚动 body + reduced-motion；`$build-acct` → `20260910-a6` |
| `assets/account.css` | 编译产物（双写） |
| `account.html` | `</footer>` 后插入 13 个面板壳；`?v=` → `a6` |
| `images/acct-modal-close.svg` | 新增 |
| `tools/acctmodal.py` | 新建判据 |
| `figma/account/cut-icons.py` | 追加 1 条 JOBS。⚠ 不入库 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctmodal.py` | **438 ok / 0 red / 2 aborted** |
| 活性自检 A：`html.is-modal-open` 的 `padding-right` 打掉 | 转红 2 ✅ |
| 活性自检 B：换成 PLAN 那份锁（两边 `overflow:hidden` + 两边补 padding） | 转红 **42** ✅，其中 `sticky header top=-485` |
| 活性自检 C：摘掉 `data-lenis-prevent` | 转红 4 ✅（滚轮滚 0px） |
| `tools/acctcheck.py` | 541 ok / 0 red（未回归） |
| `tools/rwd.py` / `acctvars.py` / `assetpath.py` | 全绿 / 54 ok / GREEN |
| 双写一致 | IN SYNC |
| 关闭叉 hover + transition（Playwright 实测） | 变色 ✅ 有过渡 ✅ |

### ⚠ 两条 ABORT，不是绿也不是红

`headless chromium 画的是 overlay 滚动条，宽度恒 0`，所以**「开弹窗页面会不会横向跳」
这条真实测试在本机跑不出来**，判据**明确 abort 而不是报绿**。
CSS 机制本身用合成的 `--scrollbar-w: 15px` 验过（`html` 补到 15px、`body` 保持 0px、
第二次开不变）。**真实位移必须在有实体滚动条的桌面浏览器上人工确认一次。**

### 遗留

- **面板 body 全空**，13 个弹窗现在点开只有标题和关闭叉 —— 内容是 Task 9–13。
- **桌面弹窗宽度仍是待裁决 E**。面板暂用板上的 390 居中，
  这是**源数据里的值**不是自拟；给了宽度后只改 `--acct-modal-w` 一个变量。
- **7 个 hook 还没有触发器**（`product-locked` / `shipping-form` / `shipping-success` /
  `cancel-skipped` / `cancel-reason` / `cancel-holiday` / `cancel-discount`），
  它们由 Task 10–13 的流程内部调起，届时补面板。
- **是否把 `.gb-acct-modal__body` 登记进 `main.js` 的 `smoothScroll.PREVENT`** ——
  行为上不需要（属性已直接写在标签上），但 `font-check.html` 有探针盯着未登记的可滚容器。
  改 `main.js` 需单独授权，**未做**。

---

## Task 7 — Detail 的 PAUSED / CANCELLED / 折扣码状态（`$build-acct` = `20260909-a5`）

**设计源**：`2284:28478`（折扣码已应用）、`28627`·`28774`（PAUSED 两版）、
`34058`（CANCELLED + Restart）、`34352`（重启后转回 ACTIVE）；
便签 `34042` 暂停期不许跳过 / `34044` 超长码 / `30921` 折扣码链接文案。

### 先查清了六个「未标注 frame」的归属

PLAN 把 `27202`·`27304`·`27081`·`27116`·`27151`·`27170` 列为「疑似 Detail 的状态」。
逐节点比对文本后**全部不是** —— 它们是账户区另外五个页面的手机稿：
Order History / Order Detail / My Details（两份逐字相同）/ Change Password / Help。
结论写进 `DETAIL-STATES.md`。

**这推翻了待裁决 C 的一半**：原以为六项无稿，实际四项有手机稿，还多出一个导航里
没有的 Order Detail；真正无稿的只剩 Refer a Friend 与 Contact Preferences。
**这五个页面不在 15 个 Task 里，属于范围变化，本轮未做，等拍板。**

### 做了什么

- **状态用两个正交属性开关表达，不复制 DOM**：`data-acct-sub-state`
  （`active` / `paused` / `cancelled`）× `data-acct-discount`（`none` / `applied`）。
  两维必须正交，因为 `28774` 是「PAUSED 且有码」。元素上挂
  `data-detail-only="active paused"` 声明自己属于哪些态，CSS 隐藏其余。
  ⚠ **判据必须写成「当前态不在这个元素的列表里」** ——
  `:not([data-detail-only~="paused"])` 那样反过来写，`"active paused"` 会在两个态里都消失。
- **PAUSED**（`28627`）：徽章换色换字；续订行标签 `Next renewal date` → `Subscription restarts`
  （日期与 Est Delivery 行不动）；**`Skip next order` 整个移除**（便签 `34042`：暂停期不许跳过）。
- **CANCELLED**（`34058`）：续订行 / 折扣行 / `Cancel Subscription` 三处删除；
  两个按钮换成单个 `Restart Subscription` + 板上 298.5 宽的居中说明 + 一条分隔线；
  第一条产品行的口味位换成 coral 的 `Out of stock` 且只留单价（无划线原价）；
  **`Skip next order` 保留**（与 PAUSED 相反）。其余入口一律画成禁用态。
- **折扣码已应用**（`28478`）：Discounts 行多一段 118 宽右对齐的码，
  链接文案 `Add a discount code` → `Edit discount code`。

### 禁用态的每个值都取自 `34058`，不是自己调的灰

| 位置 | 稿上的值 | 节点 |
|---|---|---|
| 七个 `Edit` 链接 | `#808080` **fill opacity 0.4** | `34087`/`34096`/`34108`/`34121`/`34165`/`34172` |
| `Add Items` / `Skip next order` | 底 `#e6e6e6`、字 `#808080` | `34141` / `34189` |
| 四个日期块 | 字 `#808080` | `34182` / `34184` |
| 缺货那行的品名 | coral `#dd655e` **且带删除线** | `34095` |
| `Restart Subscription` | 底 `#005635`、字白 | `34078` |
| `Add a discount code` | 仍是 `#0374a5` —— 和 Restart 是仅存的两个可用项 | `34153` |

⚠ **删除线在 `characterStyleOverrides` 里，不在顶层 `style`** —— 24 个字符全部指向带
`STRIKETHROUGH` 的 style 1。只读顶层 `style` 会判成「没有删除线」。同一行的数量 `1`
（`34094`）没有 override，所以删除线只包品名、不包数量，实现里把数量放在被划的 span 之外
（`text-decoration` 会传染给行内子元素且子元素关不掉）。

⚠ **CSS 只让它们看起来、摸起来是禁用的**。将来接真数据时，同一个条件必须一并写上
`disabled` 属性，否则它们仍可聚焦、且被读屏播报成可用。

### 判据里改掉的一个假绿

`DETAIL_LONGCODE` 与 `DETAIL_DISCOUNT` 原本做的事**完全一样**（只设
`data-acct-discount=applied`），**那段 51 字符的码从没进过 DOM**。于是「超长码在 118 里
折行、不撑破」的两条 `nofit` 实际量的是 12 字符的 `DISCOUNTCODE`，怎么写都是绿的。

把 `2284:28878` 的原文 `THISISADISAVERYVERYVERYVERYVERYLONGDISCOUNTCODE1265` 注进判据后
**当场转红**：码撑破自己的 118 达 258px，390 档整页横向溢出 135px。
真因是它是**一个没有断点的 token**，作为 flex item 的自动最小尺寸取的是整串想要的 376。
修法是 `.gb-acct-summary__code` 加 `overflow-wrap: anywhere`。

修完实测与稿逐值一致：118 宽 / 折 4 行 / 小计块 `150 → 198`。
这两个几何值已钉成断言（含 `150` 的对照不变量），不是只判「没溢出」。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | detail 卡加 `data-acct-sub-state` / `data-acct-discount` 两个开关；15 处 `data-detail-only`、3 处 `data-discount-only`；新增 Restart 按钮 + 说明 + 分隔线、`Out of stock`、`Edit discount code`、折扣码 span；品名裹进 `__label` 让数量留在删除线外；`?v=` 升到 `a5`（同一文件里主线的 `r105 → r134` 是别处那轮带过来的） |
| `assets/account.scss` | 新增两组 `@each` 状态开关、`[data-acct-sub-state="cancelled"]` 禁用段、`.gb-acct-detail__restart-note`、`.gb-acct-product__stock`、`.gb-acct-summary__code`（含 `overflow-wrap: anywhere`）；`$build-acct` → `20260909-a5` |
| `assets/account.css` | 编译产物（双写） |
| `tools/acctcheck.py` | 追加 Task 7 断言 93 条；新增 `DETAIL_PAUSED` / `DETAIL_CANCELLED` / `DETAIL_DISCOUNT` / `DETAIL_LONGCODE` 四个动作；`LONGCODE` 现在真的注入 `28878` 的原文 |
| `docs/account/DETAIL-STATES.md` | 新建 —— 六个 frame 的归属、Detail 五个状态的逐项差异、四条待确认 |
| `docs/account/SPEC.md` | §7 新增待裁决 O / P / Q / R；C 补上「四项其实有稿」 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctcheck.py` | **541 ok / 0 red**（Task 6 收尾是 448） |
| 活性自检 A：摘掉 `data-acct-sub-state` 那组 `@each` | 转红 **20** ✅ |
| 活性自检 B：摘掉 `data-acct-discount` 那组 `@each` | 转红 **3** ✅ |
| 活性自检 C：摘掉 `overflow-wrap: anywhere` | 转红 **8** ✅（含两条几何值） |
| 铁律 6 配对审计：14 条 `absent` 是否都有同名正向断言 | 14/14 有 ✅ |
| `tools/rwd.py account.html` | 全绿 |
| `tools/acctvars.py` | 54 ok / 0 red |
| `tools/assetpath.py` | GREEN（`account.scss` 无 `url()`） |
| 双写一致：重编译 scss 与 `account.css` 逐字节 diff | IN SYNC |

### 已知偏差（不要报成 bug）

- **PAUSED 的续订日期实现成 `19 Jul 2026`**（跟 active 相同），因为详情稿 `28627`/`28774`
  就是这么写的。列表卡那边是 `17 Aug 2026`。便签 `34038` 站列表那边 —— **两处不一致是稿的问题**，
  已登记待裁决 P，未擅自统一。
- **`28774` 的链接文案实现成 `Edit discount code`**，但那张稿上写的是 `Add a discount code`。
  判为漏改（便签 `30921` 与 `28478` 都站 Edit 这边），已登记待裁决 Q。
- **四个状态一个桌面稿都没有**，桌面沿用基准态的字号阶梯，只有结构与文案随状态走。
  与待裁决 M 同类，已登记待裁决 R。
- **CANCELLED 没有任何 opacity 变化** —— 列表卡的 PAUSED/CANCELLED 会压到 0.4，
  详情页不会，是稿本来就这样，不是漏做。
- 说明文案里的 `bale`（应为 `able`）是稿上的错字，按稿照抄，已在 §8 登记。

### 遗留

- **Order History / Order Detail / My Details / Change Password / Help 五个页面有手机稿但不在计划里**
  —— 范围变化，等拍板。做的话还缺桌面稿。
- **`27081` 与 `27116` 文本逐字相同、高度同为 2206**，是复制未删还是有肉眼级差异（如某个 input 的
  focus 态）？已登记待裁决 O。
- **状态目前只能由判据用脚本切**，页面上没有切换入口 —— 真实站点由模板按订阅数据渲染。
  「怎么进入 PAUSED」设计方自己回的是 *we haven't finalised this yet*（阻塞项「暂停入口」）。
- 禁用态的 `disabled` 属性未加（见上方 ⚠），接后端时补。

---

## Task 6 — Subscription Detail 的 ACTIVE 基准态（`$build-acct` = `20260909-a4`）

**设计源**：桌面 `2284:27792`、手机 `2284:28330`；便签 `30905` Add items / `30913` Flavour /
`30921` 折扣码 / `27444` Download invoice。

### 做了什么

- **页头复用 `.gb-acct-intro`**，加两个修饰：`--back`（返回键在桌面也显示，`28068` 没有）
  与 `__text--row`（铅笔按钮取代副标题，桌面 gap 8 / 手机 16）。铅笔挂
  `data-acct-modal="edit-name"`。
- **卡片外壳复用 `.gb-acct-sub`**（白底 + `#e6e6e6` + r12 + head/body），因为板上
  `27865` 与列表卡 `28072` 本来就是同一个组件。唯一差别是 head 的左右内边距
  桌面 24（列表是 20），用 `.gb-acct-sub--detail` 覆盖。
- **`.gb-acct-row`** —— 图标 + 标签/值 + 可选 Edit 的通用行，四处用它：续订日期（外加
  18/26 的大号日期与一行 Est Delivery）、Frequency、Shipping、Payment Method。
  值的颜色是 `#101828`（navy），**不是列表卡用的 `#1a1a1a`**。
- **`.gb-acct-product`** ×4 —— 62 缩略图 + 「数量 名称」+ Edit + 「Flavour + 划线原价/现价」。
- **`.gb-acct-summary`** —— 小计 / 折扣（`Automatic` + `#cbf390` 标签）/ 运费 /
  `Add a discount code` / 总计。
- **`.gb-acct-schedule`** —— 四个日期块 + `Skip next order`（全站唯一的描边按钮：无填充、
  2px 深绿边、深绿字）。
- **`.gb-acct-link`** —— 蓝色带下划线的 Edit / Add a discount code / Cancel Subscription
  （`#0374a5`，`characterStyleOverrides` 里写的 `textDecoration: UNDERLINE`）。
- **11 个 `data-acct-modal` hook 全部就位**（edit-name / edit-date / need-now /
  edit-frequency / edit-product ×4 / add-product / discount-add / shipping-current /
  edit-payment / skip-next / cancel-offer-skip），Task 8 才接 JS，现在是惰性的。
- **`.gb-acct-btn` 与 Task 5 的 `.gb-acct-sub__cta` 合成一条规则**：板上它们是同一个
  Button 组件，值一模一样。列表卡的 markup 没动。

### 三处稿上才看得出来的东西

1. **桌面的四个日期块是手机块按 1.1554 缩放的**：圆角 8→9.243、描边 1→1.155、
   内边距 24/12→27.73/13.86、字号 16/24→18.49/27.73，**每一项都乘同一个系数**。
   手机那版才是组件的原值。板上那条 316 宽的日期条塞在 308 的内容列里（溢出 8），
   也是缩放的副产品 —— 实现里让四块 `flex: 1` 平分，正好铺满。
2. **产品行的框是固定 62，里面的文字列却是 68**，所以价格那行会探进下方 24 的间距里 6px。
   照板做了（`height: 62px`），不是我们算错。
3. **Payment Method 的值里是 U+2028**（行分隔符）而不是换行，`PayPal` 与邮箱各占一行 ——
   HTML 里写成 `<br>`。这类字符肉眼与普通空格无异，见 memory `nl2br-blind-to-u2028`。

### 两稿不一致一处，两套都做

桌面 `27954` 的折扣行是「Automatic + 标签」，手机 `28433` 只有标签。无便签说明，
按全局铁律 3 的第二种做法**两套都做、767 切换**，登记为待裁决 N。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | detail 视图填入页头 / 详情卡 / 四条产品行 / 小计 / 日程卡 / 取消链接；11 个 `data-acct-modal`；`?v=` 升到 `a4` |
| `assets/account.scss` | 新增 Detail / 详情行 / 蓝链 / 产品行 / 小计 / 日程六段；`.gb-acct-sub__cta` 与新的 `.gb-acct-btn` 合并成一条规则；`.gb-acct-intro--back` 与 `__text--row` 两个修饰 |
| `assets/account.css` | 编译产物（双写） |
| `tools/acctcheck.py` | 追加 Task 6 断言 134 条；新增 `GOTO_DETAIL` 动作（**走真实路径**：先点导航进列表，再点卡片 CTA）；Task 5 的文本断言补上视图作用域 |
| `images/acct-{edit-pencil,date,frequency,plus,payment}.svg` | 新增 5 个 |
| `figma/account/cut-icons.py` | 追加 5 个 JOBS。⚠ 在 `.gitignore` 的 `figma/` 内，不入库 |
| `docs/account/SPEC.md` | §7 新增待裁决 N；§8b 新增详情页的四类占位数据 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctcheck.py` | **448 ok / 0 red**（Task 5 收尾是 314） |
| 活性自检 A：去掉 `--back` 的显示规则 | 转红 1 ✅ |
| 活性自检 B：详情卡头内边距退回 20 | 转红 1 ✅ |
| 活性自检 C：去掉产品行的固定 62 高 | 转红 1 ✅（读回 68，正好是那 6px） |
| 活性自检 D：描边按钮改 1px | 转红 1 ✅ |
| 活性自检 E：**负向断言的锚**——往详情页塞一个 `__sub` | `absent` 转红 ✅（全局铁律 6） |
| 活性自检 F：拆掉列表卡 CTA 的 `data-acct-goto` | 整组 134 条转红 ✅（证明判据走的是真实点击路径，不是 hash） |
| `tools/rwd.py account.html` | 全绿 |
| 详情视图单独扫溢出（13 档，`#detail`） | 0 溢出 |
| `tools/acctvars.py` | 54 ok / 0 red |
| 肉眼对稿 | 1440 对 `2284-27792`、390 对 `2284-28330`，逐块一致 |

### 已知偏差（不要报成 bug）

- **产品行的价格会探进下方间距 6px** —— 见上文第 2 条，板上就是这样。
- **产品名固定 `max-width: 212px`**、**Flavour 行固定 217**、**变更截止提示固定 298.5** ——
  都是板上的固定宽度，去掉它们文字会拉成一行、与稿不符。
- **日期块用 `flex: 1` 而不是板上的固定 116.3 / 73**，否则手机档溢出 8px。
- **`Flavour` 是标签不是值**：板上 `27899` 的文字就是这个词，口味按便签 `30913` 暂不做。
- **Add Items 照稿做了**：便签 `30905` 说可以先关掉，是否隐藏是待裁决 H，不自己决定。
- **`Download invoice` 没做**：便签 `27444` 说「Only do if very very very cheap，
  否则删掉」，且详情稿上本来就没有这一项，待裁决 I。
- **蓝链与铅笔的 hover 用 `opacity: .7`**，交互态稿里全缺，见待裁决 K。

### 遗留

- 11 个 `data-acct-modal` 现在点了没反应 —— Task 8 建弹窗基础设施后才接上。
- 折扣行只做了 `Add a discount code` 那一版；便签 `30921` 的「已应用折扣码 → 文案变 Edit」
  是 Task 7。
- Detail 的 PAUSED / CANCELLED / 折扣已应用等其余状态是 Task 7。

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

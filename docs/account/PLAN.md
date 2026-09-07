# Gumi Account 静态页面 实施计划

> **给执行者：** 用 `superpowers:subagent-driven-development`（推荐）或 `superpowers:executing-plans`
> 按任务逐个实施。步骤是 `- [ ]` 复选框，做完打勾。

**目标：** 把 Figma SECTION `2284:27077` 的 account 设计做成静态页面 —— `account.html`
单页三视图 + `account-login.html` + `account-signup.html`，独立 `account.scss` / `account.js`，
复用现站 header / footer 与视觉体系。

**架构：** 静态 HTML，与 MVP 11 页同仓同目录。样式源 `assets/account.scss` 自带一份变量副本，
编译成 `assets/account.css`。脚本 `assets/account.js` 是自包含 IIFE，不调 `window.gumi`；
页面同时加载 `main.js`（驱动公共 header/footer 的站点交互）与 `account.js`（account 自己的
视图切换、汉堡、19 类弹窗）。桌面左侧竖导航，手机换成页内列表卡 + 右上角下拉面板。

**技术栈：** Dart Sass 1.77.8（`npx sass@1.77.8`）、原生 JS（无框架、无 jQuery）、
Playwright（判据脚本，chromium 在 `~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome`）

**Spec：** `docs/account/SPEC.md`

---

## 全局约束

以下每条对**每个任务**都成立，任务内不再重复。

### 数值来源
- **所有数值 token（font-size / line-height / letter-spacing / 颜色 / padding / gap /
  radius / shadow）一律从 `figma/account/nodes/<id>_<slug>.json` 取**，不看截图、不目测、不"贴近视觉"
- **TEXT 节点必查 `characterStyleOverrides`** —— 只取顶层 style 必错
- 某视觉效果常由**同层兄弟节点**实现，别只盯同名组件
- 取不到值就停下向用户索取，**不许自己填**
- 该 Figma 文件**没有 shared styles**（`/v1/styles` 返回 0 条），节点里的写死属性就是全部真相

### 设计源速查
| 要什么 | 去哪 |
|---|---|
| 数值 | `figma/account/nodes/` （112 个全深度 JSON） |
| 视觉参考 | `figma/account/screenshots/` （98 张） |
| 便签规则 | `figma/account/NOTES.txt` （33 条 + John 追问全文） |
| 弹窗清单 | `figma/account/MODALS.txt` （37 态 / 19 类） |
| 整页状态 | `figma/account/PAGES.txt` （24 个整页） |
| 图标 | 先查 `figma/assets-raw/icons/`（MVP 的 1286 个），没有再从 `figma/account/svg/` 整块 SVG 里按 id 裁 |
| 位图 | `figma/account/image-fills/<imageRef>.<ext>` （988 个） |
| 索引 | `figma/account/README.md` |

**开发期间不需要调 Figma API。** 真要调：三个账号里只有 `dev@mockuptocode.com`
还有额度，且限流按账号算。

### 不做的
- 稿里的 `Chrome browser` INSTANCE（手机浏览器栏、电量、home indicator）—— 假舞台
- 左侧导航的灰色圆点 —— 便签 `27602`：待设计图标的**占位**
- 任何后端调用（真取消 / 真跳过 / 真改期 / 真支付）—— 只做壳与前端交互
- `400:18907`「Account Wire Frame」里的一切 —— 那是 Huel 等竞品的调研板
- `2121:17567`「OLD - Account Section Mobile」—— 旧版

### 目录与命名
- 页面在**根目录**，`assets/` **扁平不建子目录**（Shopify 硬约束），
  `<img src>` 的图片在**顶层 `images/`**
- ⚠ **scss 里的 `url()` 必须是 `assets/` 内的裸文件名 + `?v=#{$build}`**，
  写 `../images/…` 一上主题就静默 404。判据 `python3 tools/assetpath.py`
- ⚠ **`file://` 下 CSS mask 引用外部文件会被 CORS 拦掉**（origin=null），mask 静默变空
  并把被遮罩元素一起带走 —— 客户就是双击打开预览的。**mask 一律内联进 scss**
- 类名前缀 **`.gb-acct-`**，JS hook 用 **`data-acct-*`**（绝不复用样式类，也不与
  `main.js` 的 `data-modal` 撞名）

### 断点
account 沿用现站的两族断点，**值档必须互斥**：

```scss
$bp-mobile: 575px;   $bp-narrow: 767px;   $bp-tablet: 1280px;
@mixin mobile { @media (max-width: $bp-mobile) { @content; } }
@mixin narrow { @media (max-width: $bp-narrow) { @content; } }
@mixin tablet { @media (min-width: 768px) and (max-width: $bp-tablet) { @content; } }
@mixin pc     { @media (min-width: 1281px) { @content; } }
```
布局阈值 `mid` ≤991 / `stack` ≤1024 / `tight` ≤1200 **只准带排布、不准带数值**。
⚠ 稿只有 390 与 1440 两档，**768–1280 那一带一个板值都没有**，全是 `fluid()` 斜坡或行为约束。

### 交互态（稿里完全没有，全局铁律 13）
- 凡可点击（`a` / `button` / 卡片整块 / tab / 手风琴行 / 图标按钮 / 提交）**都要有 hover**，
  且**任何状态变化都要走 `transition`**
- 时长/曲线集中在 `account.scss` 的 motion 段变量，不要每处自己填 `0.3s ease`
- hover 规则包在 `@media (hover: hover)` 里；位移/缩放用 `transform` 不动 `width/height`
- 收尾补 `@media (prefers-reduced-motion: reduce)` 压到 `0.01ms`
- **抬起量 / 投影 / 时长 / 曲线全是自定值，逐条登记进 SPEC 的待裁决表**

### 编译与破缓存
```bash
npx sass@1.77.8 assets/account.scss assets/account.css --no-source-map
```
改完把 `account.scss` 顶部的 `$build-acct` 加一版，并同步三个页面的 `?v=`。
**account 的 `$build-acct` 与现站的 `$build` 各自独立，不要混。**

### 注释
**一律英文、极度精简**，只留"不看会改错"的那一句（顺序依赖、反直觉取值、外部约束）。
复述代码在做什么的注释、分节横幅、TODO 流水一律删。前端源码线上可直接下载。

### 提交
每个任务末尾提交一次。**不推送**（git 与 Shopify 都不推），等用户明确指令。

---
## 文件结构

| 文件 | 职责 |
|---|---|
| `account.html` | 三视图单页：Overview / Subscriptions / Detail。视图是三个 `<section data-acct-view>`，同一份 header/footer/导航 |
| `account-login.html` | 未登录态。header 带 `Shop now`，无导航 |
| `account-signup.html` | 同上 |
| `assets/account.scss` | 唯一样式源。分区顺序 = 层叠依赖：DEFINITIONS → Shell → Nav → Views → Modals → Motion |
| `assets/account.css` | 编译产物，勿手改 |
| `assets/account.js` | 自包含 IIFE。模块：`view` / `acctNav` / `acctModal` / `acctForm` / `cancelFlow` |
| `tools/acctvars.py` | 变量副本漂移判据 |
| `tools/acctcheck.py` | account 专用结构/数值判据，逐任务追加断言 |
| `tools/acctmodal.py` | 19 类弹窗开合、遮罩、焦点、ESC、滚动锁 |
| `docs/account/CHANGELOG.md` | 变更记录，约 10 项一条 |

三个页面都加载：`main.js`（公共 header/footer 的站点交互）+ `account.js`（account 自己的）。
两者不互调。

---

## Task 1：地基 —— 变量副本、编译链路、页面骨架

**文件**
- 创建：`assets/account.scss`、`assets/account.js`、`account.html`、`tools/acctvars.py`
- 产出：`assets/account.css`

**接口**
- 产出：`$build-acct`、`$c-*` 全套色板、`@mixin mobile/narrow/tablet/pc/mid/stack/tight`、
  `fluid($min,$max,$from,$to)`、根类 `.gb-acct`

- [x] **步骤 1：写漂移判据（先写，此时必红）**

创建 `tools/acctvars.py`：

```python
#!/usr/bin/env python3
"""account.scss keeps its own copy of the tokens (decision 5). This proves the
copy still matches customstyle.scss, so drift fails loudly instead of silently."""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "customstyle.scss"
DST = ROOT / "assets" / "account.scss"
# only the tokens account actually mirrors; $build is deliberately per-file
WATCH = re.compile(r'^\$(c-[\w-]+|bp-[\w-]+)\s*:\s*([^;/]+?)\s*(?://.*)?;', re.M)

def grab(p):
    return {m.group(1): m.group(2).strip() for m in WATCH.finditer(p.read_text())}

a, b = grab(SRC), grab(DST)
missing = sorted(set(a) - set(b))
drifted = sorted(k for k in set(a) & set(b) if a[k] != b[k])
extra   = sorted(set(b) - set(a))

for k in missing: print(f"RED  missing in account.scss: ${k} = {a[k]}")
for k in drifted: print(f"RED  drifted: ${k}  customstyle={a[k]}  account={b[k]}")
for k in extra:   print(f"note account-only token: ${k} = {b[k]}")
ok = len(set(a) & set(b)) - len(drifted)
print(f"\n{ok} ok / {len(missing)+len(drifted)} red")
sys.exit(1 if missing or drifted else 0)
```

- [x] **步骤 2：跑判据，确认它红**

```bash
python3 tools/acctvars.py
```
预期：`RED missing in account.scss: $c-lime = #b5ed61`（以及其余全部），退出码 1。
⚠ 若此时是绿的，说明判据没抓到东西 —— 先修判据（负向断言要先验锚点，全局铁律 6）。

- [x] **步骤 3：建 account.scss 的 DEFINITIONS 段**

从 `assets/customstyle.scss` 第 28–431 行**逐字复制**变量与 mixin（色板 `$c-*`、
断点 `$bp-*` 与七个 mixin、`fluid()`），顶部加：

```scss
// Gumi Account — account.scss
// Tokens below are a copy of customstyle.scss (spec decision 5).
// tools/acctvars.py fails if they drift.

$build-acct: "20260904-a1";
```

⚠ **不要复制 mask 常量段** —— account 稿里没有波浪，用不到；真需要时再单独内联。

- [x] **步骤 4：跑判据，确认它绿**

```bash
python3 tools/acctvars.py
```
预期：`N ok / 0 red`，退出码 0。

- [x] **步骤 5：建 account.html 骨架**

从 `index.html` 复制 `<head>`（含那段 `.wowo` 存活门内联脚本）、`<header>`、`<footer>`
三块**原样**，中间放空的三个视图容器：

```html
<main class="gb-acct">
  <section class="gb-acct__view" data-acct-view="overview" hidden></section>
  <section class="gb-acct__view" data-acct-view="subscriptions" hidden></section>
  <section class="gb-acct__view" data-acct-view="detail" hidden></section>
</main>
```

`<head>` 里在现站样式**之后**加：

```html
<link rel="stylesheet" href="assets/account.css?v=20260904-a1">
```

`</body>` 前在 `main.js` **之后**加：

```html
<script src="assets/account.js?v=20260904-a1"></script>
```

同时创建 `assets/account.js`，本任务只放骨架（Task 2 起往里加模块）：

```js
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var modules = [];
    for (var i = 0; i < modules.length; i++) {
      try { modules[i][1].init(); }
      catch (e) { if (window.console && console.error) console.error('gumiAcct:' + modules[i][0], e); }
    }
  });

  window.gumiAcct = {};
})();
```

⚠ **一个 try/catch 包一个模块** —— 一个模块炸掉不能带走其余的，
这和 `main.js` 的做法一致。

⚠ **顺序是层叠依赖**：`account.css` 必须在 `customstyle.css` 之后，否则覆盖不生效。
⚠ **用 `hidden` 属性控制视图显隐，不要 `style="display:none"`** —— 后面 `view` 模块
靠 `el.hidden` 切换。

- [x] **步骤 6：编译并肉眼确认**

```bash
npx sass@1.77.8 assets/account.scss assets/account.css --no-source-map
python3 tools/assetpath.py
```
浏览器双击打开 `account.html`：header 与 footer 与现站**完全一致**，中间空白。
⚠ 若 header 塌了，多半是复制时漏了 `<head>` 的存活门脚本 —— `.wowo{opacity:0}` 是无条件的。

- [x] **步骤 7：提交**

```bash
git add assets/account.scss assets/account.css account.html tools/acctvars.py docs/account/
git commit -m "feat(account): 地基 —— 变量副本、编译链路、页面骨架与漂移判据"
```

---

## Task 2：account 专用 header + 手机汉堡面板

**设计源**：`2284:34578`（桌面 nav 收起）、`2284:34805`（桌面 nav 展开）、
`2284:34757`（手机汉堡展开，弹窗本体是 `2284:34759` 附近的 `Component 7`）、
`2284:34529`（手机 nav 收起）

**便签 `34518` 定的行为**：Logo → 网站首页；Account icon → account 首页（本页）；
**汉堡 → 打开 account 菜单**（不是站点菜单）。

**文件**
- 修改：`account.html`（header 内增 account 专用节点）、`assets/account.scss`、`assets/account.js`
- 修改：`tools/acctcheck.py`（创建）

**接口**
- 产出：`.gb-acct-header`（覆盖层）、`.gb-acct-menu`（下拉面板）、
  hook `data-acct-menu-toggle` / `data-acct-menu`
- 产出：`account.js` 的 `acctNav` 模块，暴露 `acctNav.closeMenu()`

- [x] **步骤 1：从节点取值，写进判据**

从 `figma/account/nodes/2284-34578_desktop-navigation.json` 与
`2284-34757_navigation-expanded.json` 取：header 高度、底色、logo 尺寸与左边距、
图标尺寸与间距、下拉面板的宽/圆角/阴影/内边距/行高/字号/字距。

创建 `tools/acctcheck.py`，第一批断言写这些值（**具体数字从节点取，不要照抄本文**）：

```python
#!/usr/bin/env python3
"""account 结构/数值判据。每个任务往 CHECKS 里追加，跑全量回归。"""
import sys, json, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = pathlib.Path.home() / ".cache/ms-playwright/chromium-1217/chrome-linux64/chrome"

# (page, width, selector, css-prop, expected) — expected values come from Figma nodes
CHECKS = [
    ("account.html", 1440, ".gb-acct-header", "height", "<from 2284:34578>"),
    ("account.html", 1440, ".gb-acct-header", "background-color", "<from 2284:34578>"),
    ("account.html",  390, "[data-acct-menu]", "width", "<from 2284:34757>"),
]

def main():
    ok = red = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=str(CHROME))
        for page_name, w, sel, prop, want in CHECKS:
            pg = b.new_page(viewport={"width": w, "height": 900})
            pg.goto((ROOT / page_name).as_uri())
            pg.wait_for_timeout(300)
            el = pg.query_selector(sel)
            if el is None:
                print(f"RED  {page_name}@{w}  {sel} not found"); red += 1; pg.close(); continue
            got = pg.evaluate("([e,p])=>getComputedStyle(e).getPropertyValue(p)", [el, prop])
            if got.strip() == want:
                ok += 1
            else:
                print(f"RED  {page_name}@{w}  {sel} {prop}: want {want}, got {got}"); red += 1
            pg.close()
        b.close()
    print(f"\n{ok} ok / {red} red")
    sys.exit(1 if red else 0)

main()
```

- [x] **步骤 2：跑判据，确认它红**

```bash
python3 tools/acctcheck.py
```
预期：三条全红（`.gb-acct-header not found` 等）。

- [x] **步骤 3：写 header 覆盖样式**

在 `account.scss` 的 Shell 分区里，用 `.gb-acct-header` 作用域**覆盖**现站 header，
不改 `customstyle.scss` 一行：

```scss
.gb-acct-header {
  // account header differs by function, not by oversight: the burger opens the
  // account menu, not the site menu (Figma note 2284:34518).
}
```

⚠ **作用域选择器 0-2-0 会压过基类 0-1-0，而 `@media` 不提升特异性** ——
凡是要随断点变的值，走 custom property 覆盖（`--x: …`），不要直接写最终属性，
否则永久禁用基类的断点规则。

- [x] **步骤 4：写汉堡面板结构与 JS**

`account.html` 的 header 内加：

```html
<button class="gb-acct-header__burger" type="button"
        data-acct-menu-toggle aria-expanded="false" aria-controls="gb-acct-menu">
  <span class="visually-hidden">Account menu</span>
</button>
<nav class="gb-acct-menu" id="gb-acct-menu" data-acct-menu hidden>
  <!-- 四条，取自 2284:34757：Account / My Subscriptions / My Details / Log Out -->
</nav>
```

`account.js`：

```js
(function () {
  'use strict';

  var acctNav = {
    init: function () {
      var btn = document.querySelector('[data-acct-menu-toggle]');
      var menu = document.querySelector('[data-acct-menu]');
      if (!btn || !menu) return;              // not on this page
      btn.addEventListener('click', function () {
        var open = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', String(!open));
        menu.hidden = open;
      });
      document.addEventListener('click', function (e) {
        if (menu.hidden || btn.contains(e.target) || menu.contains(e.target)) return;
        btn.setAttribute('aria-expanded', 'false');
        menu.hidden = true;
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !menu.hidden) {
          btn.setAttribute('aria-expanded', 'false');
          menu.hidden = true;
          btn.focus();
        }
      });
    },
    closeMenu: function () {
      var btn = document.querySelector('[data-acct-menu-toggle]');
      var menu = document.querySelector('[data-acct-menu]');
      if (btn) btn.setAttribute('aria-expanded', 'false');
      if (menu) menu.hidden = true;
    }
  };

  document.addEventListener('DOMContentLoaded', function () {
    var modules = [['acctNav', acctNav]];
    for (var i = 0; i < modules.length; i++) {
      try { modules[i][1].init(); }
      catch (e) { if (window.console && console.error) console.error('gumiAcct:' + modules[i][0], e); }
    }
  });

  window.gumiAcct = { acctNav: acctNav };
})();
```

⚠ `[hidden]{display:none!important}` 在现站 reset 里已有；若 account 给
`.gb-acct-menu` 设了 `display:flex`，**作者样式会压过 UA 的 `[hidden]`** ——
必须确认 reset 里那条 `!important` 生效，否则面板关不掉。

- [x] **步骤 5：编译，跑判据，确认它绿**

```bash
npx sass@1.77.8 assets/account.scss assets/account.css --no-source-map
python3 tools/acctcheck.py
```
预期：`3 ok / 0 red`。

- [x] **步骤 6：活性自检（判据必须能抓到破坏）**

把 `.gb-acct-header` 的 `height` 临时改错一个值，重编译重跑 —— **必须转红**；
改回来再跑 —— 必须回绿。判据抓不到破坏就是假绿（全局铁律 6）。

- [x] **步骤 7：提交**

```bash
git add account.html assets/account.scss assets/account.css assets/account.js tools/acctcheck.py
git commit -m "feat(account): account 专用 header 与手机汉堡面板"
```

---
## Task 3：导航与视图切换

**设计源**：桌面左竖导航 `2284:27678`（无 Contact Preferences）/ `2284:27792`·`28000`
（有 Contact Preferences）；手机页内列表卡 `2284:27604`。

⚠ **导航条目四个版本互不一致，属待裁决 A/B。** 本任务按**桌面 `27792` 那版**实现
（条目最全），并在 `docs/account/CHANGELOG.md` 与 SPEC 待裁决表里记明这是暂定选择，
一处可改。**不要自己删掉 Contact Preferences 或 Refer a Friend** —— 评论说去除了，
但稿上画着，冲突未裁决前以稿为准。

**文件**
- 修改：`account.html`、`assets/account.scss`、`assets/account.js`、`tools/acctcheck.py`

**接口**
- 消费：Task 2 的 `acctNav.closeMenu()`
- 产出：`.gb-acct-nav`（桌面竖导航）、`.gb-acct-list`（手机列表卡）、
  hook `data-acct-goto="<view>"`；`account.js` 的 `view` 模块，暴露
  `view.show(name)`，`name ∈ {overview, subscriptions, detail}`

- [ ] **步骤 1：往 acctcheck.py 追加断言（先红）**

```python
CHECKS += [
    ("account.html", 1440, ".gb-acct-nav",  "display", "block"),
    ("account.html",  390, ".gb-acct-nav",  "display", "none"),
    ("account.html",  390, ".gb-acct-list", "display", "block"),
    ("account.html", 1440, ".gb-acct-list", "display", "none"),
]
```
桌面竖导航与手机列表卡是**两套并存**，不是同一套折叠 —— 上面四条正是在锁这一点。

- [ ] **步骤 2：跑判据确认红** → `python3 tools/acctcheck.py`

- [ ] **步骤 3：写结构**

```html
<nav class="gb-acct-nav" aria-label="Account">
  <ul class="gb-acct-nav__group">
    <li><button type="button" data-acct-goto="overview">Account Overview</button></li>
    <li><button type="button" data-acct-goto="subscriptions">My Subscriptions</button></li>
    <li><a href="#" aria-disabled="true">Order History</a></li>
  </ul>
  <!-- 其余分组按 2284:27792 的分隔，逐组取值 -->
</nav>
```

⚠ **无稿的六项**（Order History / My Details / Change Password / Refer a Friend /
Help / Contact Preferences）**只出现在导航里，不建页面**，标 `aria-disabled="true"`
且不可点。待裁决 C 解决前**不许自造页面内容**（全局铁律 3）。

- [ ] **步骤 4：写 view 模块**

```js
var view = {
  init: function () {
    var views = document.querySelectorAll('[data-acct-view]');
    if (!views.length) return;
    var self = this;
    document.addEventListener('click', function (e) {
      var t = e.target.closest('[data-acct-goto]');
      if (!t) return;
      e.preventDefault();
      self.show(t.getAttribute('data-acct-goto'));
      acctNav.closeMenu();
    });
    this.show(location.hash.slice(1) || 'overview');
  },
  show: function (name) {
    var views = document.querySelectorAll('[data-acct-view]');
    var found = false;
    for (var i = 0; i < views.length; i++) {
      var match = views[i].getAttribute('data-acct-view') === name;
      views[i].hidden = !match;
      if (match) found = true;
    }
    if (!found) { this.show('overview'); return; }   // unknown hash falls back
    var links = document.querySelectorAll('[data-acct-goto]');
    for (var j = 0; j < links.length; j++) {
      links[j].classList.toggle('is-current',
        links[j].getAttribute('data-acct-goto') === name);
    }
    if (location.hash.slice(1) !== name) history.replaceState(null, '', '#' + name);
    window.scrollTo(0, 0);
  }
};
```
把 `['view', view]` 加进 `modules` 数组与 `window.gumiAcct`。
⚠ `view` 必须排在 `acctNav` **之后** —— 它在 `init` 里调 `acctNav.closeMenu()`。

- [ ] **步骤 5：编译、跑判据确认绿、活性自检**（临时把 `.gb-acct-list` 的
      `@include narrow` 去掉 → 必须转红）

- [ ] **步骤 6：提交** — `git commit -m "feat(account): 桌面竖导航、手机列表卡与视图切换"`

---

## Task 4：Account Overview 视图

**设计源**：桌面 `2284:27678`；手机 `2284:27604`（整页）；
订单状态三态 `2284:27450`（Preparing）/ `27499`（Shipped）/ `27548`（Renewal）。

**便签 `27600` 定的语义**：Preparing = 已付款；Shipping = 已履约发货；Renewal = 仍可编辑。

**文件**
- 修改：`account.html`、`assets/account.scss`、`tools/acctcheck.py`
- 可能新增：`images/` 下的小熊图（从 `figma/account/image-fills/` 取，先查
  `figma/assets-raw/` 有没有现成的同一张）

**接口**
- 产出：`.gb-acct-hello`、`.gb-acct-order`（三态由 `data-acct-order-state` 切）、
  `.gb-acct-refer`、`.gb-acct-logout`

- [ ] **步骤 1：追加断言（先红）** —— 问候卡底色/圆角/内边距、订单卡底色、
      CTA 按钮高度与圆角，值全部从 `2284-27678_account-overview-desktop.json` 与
      `2284-27604_account-overview.json` 取。

- [ ] **步骤 2：跑判据确认红**

- [ ] **步骤 3：写结构与样式**

三种订单状态用**根节点状态类**切，不建三份 DOM：

```html
<div class="gb-acct-order" data-acct-order-state="preparing">
  <p class="gb-acct-order__label">Current order:</p>
  <p class="gb-acct-order__status">Preparing, Aug 13</p>
  <p class="gb-acct-order__note">We're preparing your order.</p>
  <a class="gb-btn gb-acct-order__cta" href="#">View Order</a>
</div>
```
```scss
.gb-acct-order {
  &[data-acct-order-state="shipped"]  { /* 取自 2284:27499 */ }
  &[data-acct-order-state="renewal"]  { /* 取自 2284:27548 */ }
}
```
⚠ 三态的**文案与图标都不同**（Preparing 是包裹图标、Shipped 是卡车、Renewal 是日期），
逐个从对应节点取，别复用。

⚠ 小熊图：先 `ls figma/assets-raw/ | grep bear` 看 MVP 阶段有没有同一张；
有就复用现有文件名，没有再从 `image-fills/` 取并 `python3 figma/optimize-images.py` 压。
**一卡一图，不复用同一张冒充多张**（全局铁律 3）。

- [ ] **步骤 4：编译、跑判据确认绿、活性自检**

- [ ] **步骤 5：三态肉眼验**

在 devtools 里把 `data-acct-order-state` 依次改成三个值，对照
`screenshots/2284-27450_*.png` / `27499` / `27548`。**没有 JS 会自己切**，
这一条写进 `docs/account/HANDOFF.md` 的「不要报成 bug」清单。

- [ ] **步骤 6：提交** — `git commit -m "feat(account): Account Overview 视图与三种订单状态"`

---

## Task 5：My Subscriptions 列表视图

**设计源**：桌面 `2284:28000`（同屏三态）；手机 `2284:28305`（同屏三态）、
`2284:34046`（Cancelled + Paused 两态）。

**便签**：`28321` PAUSED 与 active 一样，只多 paused 标签，续订日期是暂停到期日；
`28323` CANCELLED 的 Re-Activate 进重启流程、**续订日期移除**；
`28325` 多产品时显示「+N More products」。

**文件**
- 修改：`account.html`、`assets/account.scss`、`tools/acctcheck.py`

**接口**
- 产出：`.gb-acct-sub-card`（状态由 `data-acct-sub-state="active|paused|cancelled"` 切）、
  `.gb-acct-pill`（三色状态徽章）

- [ ] **步骤 1：追加断言（先红）** —— 三个徽章的底色/文字色/圆角/字号，
      卡片在三态下的透明度差异（PAUSED/CANCELLED 的产品行是灰化的），
      值从 `2284-28000_account-overview-desktop.json` 取。

- [ ] **步骤 2：跑判据确认红**

- [ ] **步骤 3：写一份卡片模板，三态用状态类切**

```html
<article class="gb-acct-sub-card" data-acct-sub-state="active">
  <header class="gb-acct-sub-card__head">
    <h3>My Subscription</h3>
    <span class="gb-acct-pill">ACTIVE</span>
  </header>
  <!-- 续订日期 / 配送地址 / 产品行 / +N More Products / Total / CTA -->
</article>
```
- CANCELLED 时**整块隐藏续订日期那一行**，CTA 文案变 `Re-Activate Subscription`
- 三态各出一张卡（稿上就是同屏三张），CTA 按状态取不同文案

⚠ 卡片整块**不可点**（稿上是 CTA 按钮才可点），所以卡片本身不要加
`cursor:pointer` 或 hover（全局铁律 13 的反面：不可点的别加 hover）。

- [ ] **步骤 4：编译、跑判据确认绿、活性自检**

- [ ] **步骤 5：提交** — `git commit -m "feat(account): My Subscriptions 列表与三种订阅状态"`

---

## Task 6：Subscription Detail —— ACTIVE 基准态

**设计源**：桌面 `2284:27792`；手机 `2284:28330`。

**内容顺序**（取自 `27792`，逐块取值）：返回箭头 + 标题 + 铅笔 → 状态徽章 →
Next renewal date + Est Delivery → `Edit Date` / `I need it now` 两个按钮 →
Frequency 行 + Edit → 产品行 ×N（缩略图 / 数量 / 名称 / Flavour / 划线原价 + 现价 / Edit）→
`+ Add Items` → 变更截止提示 → 小计 / 折扣 / 运费 / `Add a discount code` / 总计 →
Shipping + Edit → Payment Method + Edit → Renewal Schedule（四个日期块）+ `Skip next order` →
`Cancel Subscription` 链接

**文件**
- 修改：`account.html`、`assets/account.scss`、`tools/acctcheck.py`

**接口**
- 产出：`.gb-acct-detail`、`.gb-acct-row`（图标 + 标签 + 值 + Edit 的通用行）、
  `.gb-acct-product`、`.gb-acct-summary`、`.gb-acct-schedule`
- 产出：所有 Edit 入口的 hook `data-acct-modal="<name>"`，name 见 Task 8 的清单

- [ ] **步骤 1：追加断言（先红）** —— `.gb-acct-row` 的高度/分隔线颜色/图标尺寸、
      产品行的缩略图尺寸、划线价的 `text-decoration`、总计行的字重，
      值从 `2284-27792_account-overview-desktop.json` 取。

- [ ] **步骤 2：跑判据确认红**

- [ ] **步骤 3：写结构与样式**

本任务**只放静态内容与 Edit 入口的 hook，不实现弹窗**（Task 8–13 做）。
每个 Edit 按钮写成：

```html
<button class="gb-acct-row__edit" type="button" data-acct-modal="edit-date">Edit</button>
```

⚠ **Add Items 按便签 `30905` 可以先关掉**（「can be turned off for now until other
items get added」）—— 本任务**照稿做出来**，是否隐藏留待裁决 H，别自己决定。

⚠ 折扣行：便签 `30921` 说已有折扣码时文案从 `Add` 变 `Edit`，
本任务只做 `Add a discount code` 那一版，`Edit` 版在 Task 7。

- [ ] **步骤 4：编译、跑判据确认绿、活性自检**

- [ ] **步骤 5：提交** — `git commit -m "feat(account): 订阅详情 ACTIVE 基准态"`

---

## Task 7：Detail 的其余状态

**设计源**：`2284:28478`（折扣码已加）、`28627`·`28774`（PAUSED 两版）、
`34058`（CANCELLED + Restart）、`34352`（由 cancelled 转回 active）、
`27202`·`27304`·`27081`·`27116`·`27151`·`27170`（**稿上无状态标签，需逐个比对确认归属**）。

⚠ **后六个 frame 的状态归属没有定论**，第一步就是把它们比对清楚，别按高度猜。

**文件**
- 修改：`account.html`、`assets/account.scss`、`tools/acctcheck.py`
- 创建：`docs/account/DETAIL-STATES.md`（比对结论）

- [ ] **步骤 1：比对六个未标注的 frame**

```bash
python3 - <<'PY'
import json
for nid in ["2284:27202","2284:27304","2284:27081","2284:27116","2284:27151","2284:27170"]:
    f = nid.replace(':','-')
    import glob; p = glob.glob(f"figma/account/nodes/{f}_*.json")[0]
    d = json.load(open(p))["document"]
    out=[]
    def w(n):
        if n["type"]=="TEXT":
            t=" ".join((n.get("characters") or "").split())
            if t: out.append(t)
        for c in n.get("children") or []: w(c)
    w(d)
    print(f"\n=== {nid} ({len(out)} 条文本) ===")
    print(" | ".join(out))
PY
```
把结论写进 `docs/account/DETAIL-STATES.md`：每个 frame 是什么状态、与基准态差在哪。
**比对不出来的就标"归属未定"并列入待裁决**，不要硬塞一个状态。

- [ ] **步骤 2：追加断言（先红）** —— PAUSED 态下 `Skip next order` 按钮**不存在**
      （便签 `34042` 明确要求移除），CANCELLED 态下续订日期行不存在。

```python
CHECKS_ABSENT = [   # negative assertions: anchor must exist first (rule 6)
    ("account.html", 390, ".gb-acct-detail[data-acct-sub-state='paused'] [data-acct-modal='skip-next']"),
    ("account.html", 390, ".gb-acct-detail[data-acct-sub-state='cancelled'] .gb-acct-row--renewal"),
]
```
⚠ 负向断言**先验锚点存在**：先断言 `.gb-acct-detail[data-acct-sub-state='paused']`
**存在**，再断言里面那个按钮不存在。否则选错文件（空/404）会让断言恒真、报全绿。

- [ ] **步骤 3：跑判据确认红**

- [ ] **步骤 4：用状态类实现差异**，不复制整块 DOM

- [ ] **步骤 5：编译、跑判据确认绿、活性自检**

- [ ] **步骤 6：提交** — `git commit -m "feat(account): 订阅详情的 PAUSED/CANCELLED/折扣码状态"`

---
## Task 8：弹窗基础设施

**决策 3**：桌面**沿用站内既有机制、居中卡片**；手机按稿的定位与尺寸。

**13 类弹窗的 hook 名**（`data-acct-modal` 的取值）。一类可能有多个态，
多态用 panel 上的 `data-acct-*-state` 切，不建多个 panel：

```
edit-name  edit-date  edit-frequency  edit-payment  skip-next  need-now
edit-product  add-product  product-locked
discount-add  discount-applied
shipping-current  shipping-form  shipping-success
cancel-offer-skip  cancel-skipped  cancel-reason  cancel-holiday  cancel-discount
restart
```

**文件**
- 修改：`assets/account.js`、`assets/account.scss`
- 创建：`tools/acctmodal.py`

**接口**
- 产出：`acctModal.open(name, trigger)` / `acctModal.close()` / `acctModal.isOpen()`
- 产出：`.gb-acct-modal`（外层，`.is-open` 状态类）、`.gb-acct-modal__panel`、`.gb-acct-modal__backdrop`

- [ ] **步骤 1：写弹窗判据（先红）**

创建 `tools/acctmodal.py`：逐个 `data-acct-modal` 触发器点击 → 断言对应 panel 可见、
backdrop 存在、焦点落进 panel、按 ESC 关闭、关闭后焦点回到触发器。
再加一条**滚动锁不得让页面横向位移**：

```python
# Locking scroll removes the desktop scrollbar and widens the viewport, so the
# page shifts right unless the width is compensated (global rule 14).
# Headless defaults to no scrollbar (width always 0), so this check must run on a
# page that really scrolls and really has one -- abort if it does not.
def check_no_shift(pg, trigger_sel):
    pg.evaluate("document.body.style.minHeight = '4000px'")   # force a scrollbar
    sbw = pg.evaluate("window.innerWidth - document.documentElement.clientWidth")
    if sbw == 0:
        print("ABORT  no real scrollbar in this browser -- check proves nothing")
        return None
    before = pg.evaluate("document.querySelector('.gb-acct-nav').getBoundingClientRect().left")
    pg.click(trigger_sel)
    pg.wait_for_timeout(400)
    after = pg.evaluate("document.querySelector('.gb-acct-nav').getBoundingClientRect().left")
    return abs(after - before) < 0.5
```

- [ ] **步骤 2：跑判据确认红** → `python3 tools/acctmodal.py`

- [ ] **步骤 3：实现 acctModal**

```js
var acctModal = {
  _last: null,
  init: function () {
    var self = this;
    document.addEventListener('click', function (e) {
      var t = e.target.closest('[data-acct-modal]');
      if (t) { e.preventDefault(); self.open(t.getAttribute('data-acct-modal'), t); return; }
      if (e.target.closest('[data-acct-modal-close]')) { e.preventDefault(); self.close(); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && self.isOpen()) self.close();
    });
  },
  isOpen: function () { return !!document.querySelector('.gb-acct-modal.is-open'); },
  open: function (name, trigger) {
    var el = document.querySelector('.gb-acct-modal[data-acct-modal-panel="' + name + '"]');
    if (!el) return;
    this._last = trigger || null;
    // measure while the scrollbar is still there, then compensate for its loss
    if (!document.documentElement.classList.contains('acct-locked')) {
      var sbw = window.innerWidth - document.documentElement.clientWidth;
      document.documentElement.style.setProperty('--acct-sbw', sbw + 'px');
      document.documentElement.classList.add('acct-locked');
      document.body.classList.add('acct-locked');
    }
    el.hidden = false;
    void el.offsetWidth;                       // force reflow so the transition runs
    el.classList.add('is-open');
    var focusable = el.querySelector('input, select, textarea, button, [href]');
    if (focusable) focusable.focus();
  },
  close: function () {
    var el = document.querySelector('.gb-acct-modal.is-open');
    if (!el) return;
    el.classList.remove('is-open');
    var self = this;
    var ms = parseFloat(getComputedStyle(el).transitionDuration) * 1000 || 0;
    setTimeout(function () {
      el.hidden = true;
      // release only after the fade-out, or the page jumps mid-transition
      document.documentElement.classList.remove('acct-locked');
      document.body.classList.remove('acct-locked');
      if (self._last) { self._last.focus(); self._last = null; }
    }, ms);
  }
};
```

```scss
.acct-locked {
  overflow: hidden;
  padding-right: var(--acct-sbw, 0px);   // scrollbar is gone; keep the width
}
```

⚠ **补偿只能补一次** —— 上面那个 `classList.contains` 守卫就是为此：取消流程 7 屏是
**同一个弹窗换内容**，第二次测量会读到 0 并覆盖掉第一次的补偿。
⚠ **html 与 body 都设** —— overflow 传导权归属不确定，两个都补无害。
⚠ **解锁要等淡出结束**（上面的 `setTimeout`），提前解锁页面会在淡出中途跳一下。

- [ ] **步骤 4：把新增的可滚动容器登记进 main.js 的 PREVENT**

弹窗内若有 `overflow-y:auto` 的区域（多产品列表、取消原因列表、日历），
必须加进 `main.js` 的 `smoothScroll.PREVENT`，否则 Lenis 吃掉滚轮、那个容器再也滚不动。
⚠ **这是本计划唯一需要改 `main.js` 的地方**，改之前单独向用户申请，把理由与改动行数一并说明。

- [ ] **步骤 5：编译、跑判据确认绿**

- [ ] **步骤 6：活性自检** —— 把 `padding-right: var(--acct-sbw)` 临时删掉重跑，
      横向位移那条**必须转红**。若删了还是绿，说明测试环境没有真滚动条，判据无效。

- [ ] **步骤 7：提交** — `git commit -m "feat(account): 弹窗基础设施与滚动锁补偿"`

---

## Task 9：简单表单弹窗 6 类

**设计源与尺寸**（手机，取自 `MODALS.txt`）：

| hook | 节点 | 手机尺寸 | 要点 |
|---|---|---|---|
| `edit-name` | `2284:31330`·`33508` | 390x246 | 两版分别是订阅名与人名 |
| `edit-date` | `2284:31976` | 390x290 | 选下次续订日，其余按频率顺推（便签 `30911`）；必须是完整的未来一天（便签 `30923`） |
| `edit-frequency` | `2284:32135` | 390x290 | 选项只有 2 / 4 / 6 周（便签 `30925`） |
| `edit-payment` | `2284:32463` | 390x256 | 发邮件改支付方式，无表单 |
| `skip-next` | `2284:32621` | 390x236 | 确认框 |
| `need-now` | `2284:33350` | 390x256 | 确认框 |

**便签 `27446`**：保存按钮**只有在上方表单被改动过之后才变为可用态**。
**便签 `27448`**：字段预填当前值，开始编辑即生效。

**文件**：`account.html`、`assets/account.scss`、`assets/account.js`、`tools/acctmodal.py`

**接口**
- 消费：Task 8 的 `acctModal.open/close`
- 产出：`acctForm.watch(panelEl)` —— 监听 panel 内输入，脏了就解锁 Save 按钮

- [ ] **步骤 1：追加断言（先红）** —— 六个 panel 的宽/高/圆角/内边距从各自节点取；
      再加一条行为断言：**未改动时 Save 是 disabled，改动后变 enabled**。

- [ ] **步骤 2：跑判据确认红**

- [ ] **步骤 3：写六个 panel 的结构与样式**

⚠ `edit-frequency` 的下拉：**用现站 `selectBox` 的视觉规格重画一份**在 `account.js` 里
（决策 6 要求自包含），不要调 `window.gumi.selectBox`。规格从 `2284:32135` 节点取。

- [ ] **步骤 4：写 acctForm**

```js
var acctForm = {
  watch: function (panel) {
    var save = panel.querySelector('[data-acct-save]');
    if (!save || panel.dataset.acctWatched) return;
    panel.dataset.acctWatched = '1';
    var initial = this._snapshot(panel);
    save.disabled = true;                    // note 2284:27446: dirty-gated
    var self = this;
    panel.addEventListener('input', function () {
      save.disabled = self._snapshot(panel) === initial;
    });
  },
  _snapshot: function (panel) {
    var f = panel.querySelectorAll('input, select, textarea');
    var v = [];
    for (var i = 0; i < f.length; i++) v.push(f[i].value);
    return v.join(' ');
  }
};
```

⚠ `save.disabled = true` 会让按钮进入 UA 的 disabled 态；样式要显式写 `&:disabled`
的外观，且**不要给 disabled 的按钮加 hover 或 `cursor:pointer`**。

- [ ] **步骤 5：编译、跑判据确认绿、活性自检**（删掉 `save.disabled = true` → 行为断言必须红）

- [ ] **步骤 6：提交** — `git commit -m "feat(account): 六类表单弹窗与脏值门控的保存按钮"`

---

## Task 10：产品弹窗 3 类

| hook | 节点 | 尺寸 | 要点 |
|---|---|---|---|
| `edit-product` | `2284:30960`·`31145`·`33666` | 390x672 | 三个变体：默认 / 变体 / QTY=2 |
| `add-product` | `2284:28942`·`29200`·`29399` | 390x672 | 三个变体：QTY=0 / 2 / 0 |
| `product-locked` | `2284:33847` | 390x672 | 「Sorry! Subscriptions need to have at least one product.」 |

**便签**：`34502` 最后一个产品的 QTY 不能减到 0；`34504` 其余产品 QTY 减到 0 时
按钮文案变成「remove this product」；`30917` 多产品时启用滚动 + 按钮固定在视口底部；
`30913`·`30915` Flavour 暂不可编辑（待裁决 J，本任务照稿画出来但设为不可交互）；
`34500` 下拉将来接 Shopify 变体；`30927` 两个及以上变体时上下排列。

**文件**：`account.html`、`assets/account.scss`、`assets/account.js`、`tools/acctmodal.py`

**接口**
- 产出：`acctQty.bind(rootEl)` —— 加减按钮、0 时改按钮文案、最后一个产品锁定

- [ ] **步骤 1：追加断言（先红）**
  - QTY 减到 0 时按钮文案变 `Remove this product`
  - 只剩一个产品时 QTY 减不到 0（点减号后值仍为 1）
  - 多产品时 panel 内出现 `overflow-y: auto` 的容器且 CTA `position: sticky` 贴底

- [ ] **步骤 2：跑判据确认红**

- [ ] **步骤 3：写结构与样式**，Flavour 下拉标 `aria-disabled="true"` 且不绑事件

- [ ] **步骤 4：写 acctQty**

```js
var acctQty = {
  bind: function (root) {
    var self = this;
    root.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-acct-qty]');
      if (!btn) return;
      var row = btn.closest('[data-acct-product]');
      var out = row.querySelector('[data-acct-qty-value]');
      var n = parseInt(out.textContent, 10) || 0;
      var delta = btn.getAttribute('data-acct-qty') === 'up' ? 1 : -1;
      var only = root.querySelectorAll('[data-acct-product]').length === 1;
      if (n + delta < (only ? 1 : 0)) return;   // note 34502: last product cannot hit 0
      out.textContent = n + delta;
      self._sync(row, n + delta);
    });
  },
  _sync: function (row, n) {
    var cta = row.closest('.gb-acct-modal').querySelector('[data-acct-save]');
    if (!cta) return;
    // note 34504: dropping an extra product to 0 turns Save into a removal action
    cta.textContent = n === 0 ? 'Remove this product'
                              : cta.getAttribute('data-acct-label-default');
  }
};
```

- [ ] **步骤 5：把 acctQty 挂进弹窗打开流程**

`acctQty` 是委托绑定，同一个 panel 绑两次会让点一下加两次。在 `acctModal.open()`
里紧跟 `acctForm.watch(el)` 之后加：

```js
    if (window.gumiAcct && window.gumiAcct.acctQty) window.gumiAcct.acctQty.bind(el);
```
并在 `acctQty.bind()` 开头加同款守卫：

```js
    if (root.dataset.acctQtyBound) return;
    root.dataset.acctQtyBound = '1';
```

- [ ] **步骤 6：编译、跑判据确认绿、活性自检**

- [ ] **步骤 7：把 panel 内的滚动容器加进 `main.js` 的 `smoothScroll.PREVENT`**（沿用 Task 8 的授权）

- [ ] **步骤 8：提交** — `git commit -m "feat(account): 产品编辑与新增弹窗、数量门控"`

---

## Task 11：折扣码弹窗

| hook | 节点 | 尺寸 | 态 |
|---|---|---|---|
| `discount-add` | `2284:31488` | 390x246 | 空输入 |
| `discount-add` | `2284:31648` | 390x246 | 已填 `CEO90` |
| `discount-applied` | `2284:31809` | 390x292 | 成功，多一行 `Discount CEO90 applied $35.25 off` |

**便签**：`30919` 码不存在时**按钮不变绿**；`30921` 已有码时入口文案 add 变 edit；
`34044` 长码的处理方式照稿。

- [ ] **步骤 1：追加断言（先红）** —— 输入为空时 Apply 按钮的 `background-color`
      不等于主绿（值从 `31488` 取），填入后等于（值从 `31648` 取）；成功态 panel 高 292
- [ ] **步骤 2：跑判据确认红**
- [ ] **步骤 3：写三态，用 panel 上的 `data-acct-discount-state` 切**
- [ ] **步骤 4：Apply 按钮的启用只看输入非空**（前端能判的就判；码是否真实存在要后端，不做）
- [ ] **步骤 5：编译、跑判据确认绿、活性自检**
- [ ] **步骤 6：提交** — `git commit -m "feat(account): 折扣码弹窗三态"`

---

## Task 12：地址弹窗 4 类

| hook | 节点 | 尺寸 | 态 |
|---|---|---|---|
| `shipping-current` | `2284:32294` | 390x394 | 显示当前地址 |
| `shipping-form` | `2284:32940`·`33161` | 390x672 | 表单（两个变体） |
| `shipping-success` | `2284:32779` | 390x254 | 成功 |

另有 `2284:33129`「Container」390x750 —— 是**表单的滚动容器**，其最后一个 child
是 `_Scroll bar`（16x528），说明这个 panel 内部滚动。

- [ ] **步骤 1：追加断言（先红）** —— 表单 panel 内有 `overflow-y:auto` 容器、
      必填星号的颜色、电话区号 `+61` 前缀框的宽度，值从 `32940` 取
- [ ] **步骤 2：跑判据确认红**
- [ ] **步骤 3：写三态与表单校验**（必填、邮编格式；**不提交到任何后端**）
- [ ] **步骤 4：把滚动容器加进 `smoothScroll.PREVENT`**
- [ ] **步骤 5：编译、跑判据确认绿、活性自检**
- [ ] **步骤 6：提交** — `git commit -m "feat(account): 配送地址弹窗与表单校验"`

---

## Task 13：取消流程 7 屏 + 重启

**7 屏链路**（节点见 `MODALS.txt`）：

```
cancel-offer-skip   29596  劝跳过 1/2 单        -> [Cancel now] [Continue to Skip]
cancel-skipped      29767  跳过成功              -> [Done]
cancel-reason       29928  原因选择（5 项）
                    30286  同上，另一变体
                    30107  稿的 bug：I have too much product 重复两次
cancel-holiday      30465  选 Going away 后进暂停日历，选恢复日期
cancel-discount     30740  选 Too expensive 后进 20% off 挽留
restart             34192  重启订阅（标题稿上拼错成 subscoption）
```

**便签 `34512`**：「I have too much product」及其之后的选项**没有第二屏**，选完直接取消。
**便签 `34516`**：取消数据要记录（谁、为什么）—— 前端只做**采集与传参的壳**，不落库。
**便签 `34514`**：20% off 是在订阅折扣之上再加一档。
**便签 `34040`**：重启要到**次日**才能操作。

⚠ **稿的 bug 照实做，不静默修正**：`30107` 的重复项、`34192` 的拼写错误
都已登记进 SPEC 第 8 节，问过用户再改。

**文件**：`account.html`、`assets/account.scss`、`assets/account.js`、`tools/acctmodal.py`

**接口**
- 产出：`cancelFlow.start()` / `cancelFlow.goto(step)` / `cancelFlow.pick(reason)`
- ⚠ 7 屏是**同一个弹窗换内容**，不是 7 个弹窗叠加 —— 滚动锁只加一次、只补偿一次

- [ ] **步骤 1：追加断言（先红）**
  - 点 `Cancel Subscription` 后第一屏是 `cancel-offer-skip`，不是原因选择
  - 选 `Going away or on holiday` 进 `cancel-holiday`
  - 选 `Too expensive right now` 进 `cancel-discount`
  - 选 `I have too much product` **不进任何第二屏**，流程终止（便签 `34512`）
  - 全程 `document.documentElement.style.paddingRight` 只被设置一次

- [ ] **步骤 2：跑判据确认红**

- [ ] **步骤 3：写七屏内容与分支表**

```js
var cancelFlow = {
  // note 34512: only these two reasons branch to a second screen; the rest end the flow
  BRANCH: {
    'going-away': 'cancel-holiday',
    'too-expensive': 'cancel-discount'
  },
  start: function () { acctModal.open('cancel-offer-skip'); },
  goto: function (step) {
    var panels = document.querySelectorAll('[data-acct-modal-panel]');
    for (var i = 0; i < panels.length; i++) {
      var n = panels[i].getAttribute('data-acct-modal-panel');
      if (n.indexOf('cancel-') !== 0 && n !== 'restart') continue;
      panels[i].hidden = n !== step;
    }
  },
  pick: function (reason) {
    var next = this.BRANCH[reason];
    if (next) { this.goto(next); return; }
    acctModal.close();          // no second screen for the remaining reasons
  }
};
```
⚠ `goto()` **不调用 `acctModal.open()`** —— 那会重新测量滚动条并覆盖已有补偿。

接上入口。Task 6 的 `Cancel Subscription` 链接改成 `data-acct-cancel-start`，
原因按钮加 `data-acct-cancel-reason="going-away"` 之类，然后在 `cancelFlow.init()` 里：

```js
  init: function () {
    var self = this;
    document.addEventListener('click', function (e) {
      if (e.target.closest('[data-acct-cancel-start]')) { e.preventDefault(); self.start(); return; }
      var r = e.target.closest('[data-acct-cancel-reason]');
      if (r) { e.preventDefault(); self.pick(r.getAttribute('data-acct-cancel-reason')); }
    });
  },
```
把 `['cancelFlow', cancelFlow]` 加进 `modules` 与 `window.gumiAcct`。
⚠ 排在 `acctModal` **之后** —— `start()` 会调 `acctModal.open()`。

- [ ] **步骤 4：暂停日历（`30465`）**

用原生 `<table>` 画月历，规格从 `2284-30465_cancel-subscription.json` 取。
**不引第三方日历库**。可选日的规则：便签 `30923` 说必须是完整的未来一天，
所以今天与更早的日期禁用。

- [ ] **步骤 5：编译、跑判据确认绿、活性自检**（把 `BRANCH` 清空 → 分支断言必须红）

- [ ] **步骤 6：提交** — `git commit -m "feat(account): 取消流程七屏与重启订阅"`

---

## Task 14：Log in / Sign up 两页

**设计源**：桌面 `2284:35137`（Log in）· `35059`（Sign up）；
手机 `2284:34993`（Log in）· `35023`（Sign up）。

⚠ 这两页的 header **多一个绿色 `Shop now` 按钮**，且**没有左侧导航**。
⚠ 手机 frame 的顶层第一个 child 是 `Chrome browser` INSTANCE —— 假舞台，不实现。

**文件**
- 创建：`account-login.html`、`account-signup.html`
- 修改：`assets/account.scss`（新增 Auth 分区，排在 Views 之后）、`tools/acctcheck.py`

- [ ] **步骤 1：追加断言（先红）** —— 两页存在、`.gb-acct-nav` **不存在**
      （负向断言先验 `.gb-acct-auth` 存在）、`Shop now` 按钮存在且底色取自 `35137`
- [ ] **步骤 2：跑判据确认红**
- [ ] **步骤 3：写两页**，复用 Task 1 的 head/header/footer 骨架，
      表单结构与文案逐字取自节点（Log in 页底部那段
      「Ordered before but haven't set up an account?」整块也要）
- [ ] **步骤 4：两页都加载 `account.css` + `main.js` + `account.js`**
- [ ] **步骤 5：编译、跑判据确认绿、活性自检**
- [ ] **步骤 6：提交** — `git commit -m "feat(account): 登录与注册两页"`

---

## Task 15：收尾 —— 响应式、交互态、全量回归

**文件**：`assets/account.scss`、`tools/`、`docs/account/`

- [ ] **步骤 1：断点重叠扫描**

```bash
grep -n '@include \(mobile\|narrow\|tablet\|pc\)' assets/account.scss
```
逐个确认值档互斥：同一属性不得同时落在两个档内。
⚠ 重叠不会报错，只会让「同一行字的字号来自手机档、字距来自插值档」，肉眼只觉得怪。

- [ ] **步骤 2：hover / 过渡配平**

```bash
grep -c ':hover' assets/account.scss
grep -c 'transition' assets/account.scss
```
两个数差很多就是漏了过渡。逐个补齐，hover 规则包进 `@media (hover: hover)`。
⚠ 直连 headless 下 `(hover:hover)` 恒 false，**验证 hover 必须用 Playwright**。

- [ ] **步骤 3：补 reduced-motion**

```scss
@media (prefers-reduced-motion: reduce) {
  .gb-acct *, .gb-acct-modal * {
    transition-duration: .01ms !important;
    animation-duration: .01ms !important;
  }
}
```

- [ ] **步骤 4：全档溢出扫描**

```bash
python3 tools/rwd.py
```
扩到 account 三页 x 14 档。判据：无横向溢出、无文字被裁、无滚轮黑洞。

- [ ] **步骤 5：全量回归**

```bash
python3 tools/acctvars.py && python3 tools/acctcheck.py && \
python3 tools/acctmodal.py && python3 tools/assetpath.py && python3 tools/scrolllock.py
```
**全绿才算完**。任何一条红就停下修，不要标「已知问题」放过。

- [ ] **步骤 6：清掉探针临时文件**

```bash
git status --short
```
不该有未登记的新文件。
⚠ snap chromium 读不到 `/tmp`，探针临时文件只能落在项目内，**跑完必须删**，
否则会被同步脚本当成改动推上线。

- [ ] **步骤 7：写交接文档**

创建 `docs/account/HANDOFF.md`，必须包含**「不要报成 bug 的清单」**：
- 无稿的六项只在导航里、不可点，是**有意为之**（待裁决 C）
- 左侧导航的灰圆是**待设计图标占位**（便签 `27602`）
- Overview 三种订单状态、订阅三态、详情各状态**都没有 JS 会自己切**，
  预览要在 devtools 里改 `data-acct-*` 属性
- `30107` 的取消原因重复项、`34192` 的 `subscoption` 拼写**是稿自带的**
- `Chrome browser` 假舞台没做，不是漏了
- Flavour 下拉不可交互是便签 `30913` 要求的

创建 `docs/account/CHANGELOG.md`，把 15 个任务归并成若干条记录，
每条写「改了什么 / 为什么 / 文件清单 / 遗留」。

- [ ] **步骤 8：提交** — `git commit -m "docs(account): 收尾回归、交接文档与不要报成 bug 清单"`

---

## 阻塞项

不阻塞 Task 1-8，但下列几项在动到对应任务前最好先要到答案。

| # | 阻塞什么 | 内容 |
|---|---|---|
| A/B | Task 3 | 四个版本的导航条目不一致；评论说 contact preference 与 refer a friend 去除了，但稿上画着。本计划暂按桌面 `27792` 那版做，一处可改 |
| C | 不阻塞 | 六项无稿页面 —— 本计划只在导航里出条目、不建页面 |
| E | Task 8-13 | 13 类弹窗的桌面稿全缺。已定「居中卡片」，但**宽度与内边距需要给值**，否则只能自己填，那就违反「数值取自源数据」 |
| 暂停入口 | Task 5·7·13 | John 追问的答复原文：暂停订阅**没有独立入口**，是在 cancel 流程中途引导，「we haven't finalised this yet」。PAUSED 的状态页有稿，怎么进入没有 |
| H | Task 6 | Add Items 是否先关掉；Edit 跳购物车还是 PDP |
| I | Task 6 | Download invoice 做不做（「Only do if very very very cheap」） |
| J | Task 10 | Flavour 是否可编辑 |
| K | Task 15 | 交互态的抬起量 / 投影 / 时长 / 曲线全是自定值，需集中登记待裁决 |

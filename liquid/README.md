# `liquid/` — 我们改过的线上主题文件

> 2026-09-04 第七十轮建立。**这个目录不是主题**，只放我们动过的那几个文件。

## 为什么存在

线上主题的 liquid **由对方维护，本地没有源**——静态站仓库里一直只有 HTML/SCSS/JS。
第七十轮第一次改 liquid，改动如果只留在 `Gumi-Brand-shopify/` 的工作副本里，
下次 `theme pull` 就被冲掉，也查不到历史。所以改过的文件在这里留一份，进 git。

## 内容

| 文件 | 说明 |
|---|---|
| `sections/*.liquid` / `snippets/*.liquid` / `blocks/*.liquid` | 改后的**完整文件** |
| `rNN.patch` | 该轮相对当轮 live 快照的 diff，给对方合入用 |

基线快照在 `/home/ly/project/Gumi-Brand-shopify/`（不在本仓库，太大）。

## 各文件状态（⚠ 推送状态不一致，改之前先看这里）

| 文件 | 轮次 | 改了什么 | 线上 |
|---|---|---|---|
| `sections/gb-stats.liquid` | r70 | 补 4 个装饰箭头 | ✅ 已推 |
| `sections/gb-expert.liquid` | r70 | 标题只在 ≤767 断行 | ✅ 已推 |
| `sections/gb-reviews.liquid` | r70 | 补法务免责声明 + setting | ❌ 未推（需求方只点名推了另两个） |
| `snippets/gb-rich-inline.liquid` | r71 | 新增：剥掉 richtext 的外层 `<p>` | ✅ 已推 |
| `snippets/gb-scripts.liquid` | r71 | 三个脚本加 `defer` | ✅ 已推 |
| `sections/gb-footer.liquid` | r71 | tagline 走 gb-rich-inline | ✅ 已推 |
| `sections/gb-hero.liquid` | r71 | lead 走 gb-rich-inline | ✅ 已推 |
| `sections/gb-header.liquid` | r90 | 菜单拆成两个 ul（桌面/手机各一），移除 `--mobile` 单项类 | ❌ **未推**：需求方要求先在静态站落地并调完样式；推之前后台 Mobile menu 必须先补成六项，见 `docs/LIVE-BACKLOG.md` 第〇节 |
| `blocks/gb-title.liquid` | r90 | PDP 产品标题 `<h2>` → `<h1>`（整页原本 0 个 h1） | ✅ 已推 |
| `sections/main-404.liquid` | r92 | schema `class` 补 `gb-404` 钩子（`section-wrapper` 是 main-page / main-blog-post / section 共用的，不能当选择器） | ❌ **未推**：等授权。没有它，404 的标题/正文/按钮样式全部不生效 |
| `sections/gb-promo.liquid` | r91 | 补 `gb-arc-text--mob`（手机端那条弧线上一直没有）；arc 只对 `variant == 'white'` 渲染 | ✅ **已推**（r91，2026-09-07，需求方明确授权）。theme check 推前后报告逐行相同；线上手机端实测已出弧 |
| `sections/gb-nutrition.liquid` | r71 | 卡片 text 走 gb-rich-inline | ✅ 已推 |
| `sections/gb-form-section.liquid` | r71 | note 走 gb-rich-inline | ✅ 已推 |
| `sections/gb-product.liquid` | r71 | guarantee_note 走 gb-rich-inline | ✅ 已推 |
| `snippets/gb-head.liquid` | r72 | 揭示门兜底 `4000` → `10000` | ✅ 已推 |
| `snippets/gb-logo.liquid` | r85 | `image_url` 过滤器顺序：`image_url` 先出 URL，`times: 2` 再乘字符串得 `0` → 线上 `src="0"` + `0 2x` 候选，2x 屏必碎图 | ✅ **已推**（r87，2026-09-07；回读逐字节相同，线上 src 已是真实 URL） |
| `snippets/gb-sub.liquid` | r73 | 订阅下拉补 `data-select`（selectBox 的 hook） | ⛔ **不必推**：r74 改由 `main.js` 自己认领，留作备选 |

⚠ **这五个 section 与 `snippets/gb-rich-inline.liquid` 是绑在一起的** ——
它们都 `{% render %}` 它，缺了它整站这五处直接报错。r71 推送时按「先 snippet 后 section」
两步推，任何时刻线上都是自洽的；以后再动这几处照此办理。

## 用法

**改之前**：先 `theme pull` 拉最新线上到 `Gumi-Brand-shopify/live-<YYYYMMDD-HHMM>/`，
`diff -r` 比对上一次的 baseline —— 对方随时在改，**不比对就动手会覆盖别人的改动**。

**改**：`cp -a live-<stamp> work-rNN`，在 work 里改（脚本 `tools/_apply_rNN.py`），
再把动过的文件镜像回这里。

**验**：`python3 tools/rNNcheck.py <theme-dir>` +
`shopify theme check --path <theme-dir>`（对改前改后各跑一次比 offense 数）。

⚠ **推 liquid 需逐次授权**，线上 liquid 是对方在维护的。
⚠ **绝不推 `templates/*.json`、`sections/*-group.json`、`config/settings_data.json`** ——
Online Store Editor 托管，推它们会覆盖对方在后台调的一切。

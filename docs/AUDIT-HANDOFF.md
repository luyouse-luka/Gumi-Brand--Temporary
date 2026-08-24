# Gumi Brand — 审计交接文档

> 建档 2026-08-20，交接人：上一轮搭建会话（第 1~13 轮）。
> **本文件的读者是审计会话**：要做还原度核对、CSS / JS / 性能审计。
> 项目全貌见 [PROJECT-STATUS.md](PROJECT-STATUS.md)，改动史见 [CHANGELOG.md](CHANGELOG.md)，
> 设计方口头约定见 [HANDOVER-NOTES.md](HANDOVER-NOTES.md)。**本文件不重复它们，只写审计要用的东西。**

---

## 0. 先读这一段，能省掉大半误报

这个项目**处于静态 HTML 阶段**（Figma → HTML/CSS/JS），Shopify 主题化还没开始。
很多东西是**有意为之**或**等设计方裁决**，不是缺陷。开审前请把第 3.4 节
「不要报成 bug 的清单」过一遍 —— 上一轮踩过的坑里，有相当一部分是「看起来像 bug，
查了半天发现是约定」。

三条最容易误判的：

1. **字体不是最终字体。** PP Palma 无授权，现用**试用包 + 400 字重插值件**。
   字宽、字距、字形细节与设计稿天然对不齐，**不要按像素报还原度**。见第 3.4 节。
2. **只有 1440 和 390 两个断点有设计稿。** 768 / 1024 是按响应式规则推导的，
   **没有稿可比**，那两档只能审「有没有坏」，不能审「像不像稿」。
3. **`file://` 下预览有独立的坑**（mask 被 CORS 拦、CSS/JS 被缓存），
   见第 7.2 节。踩进去会得到完全错误的结论。

**审计只出报告，不改代码。** 同目录可能有并行会话（见全局 CLAUDE.md「多 Agent 并行」），
且推送/改动一律等用户明确指令。报告写到 `docs/audit/`。

---

## 1. 30 秒跑起来

```bash
cd /home/ly/project/Gumi-Brand

# 编译 SCSS（sass 不在 PATH，必须 npx 带版本）
npx sass@1.77.8 assets/customstyle.scss assets/customstyle.css --no-source-map

# 全站回归：11 页 × 5 个宽度，出截图 + 查横向溢出 + 查卡住的入场动画
python3 tools/shoot.py --all              # 截图落在 tools/shots/
python3 tools/shoot.py science.html 1440  # 单页单宽度
```

预览：浏览器直接开 `index.html`（`file://`）。**没有 dev server，也不要起** ——
客户就是双击打开预览的，起了 server 会掩盖第 7.2 节那类只在 `file://` 暴露的问题。

Playwright 的 chromium 在 `~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome`，
写脚本时要显式 `executable_path=`，不能靠默认解析。

---

## 2. 项目坐标

```
Gumi-Brand/
├── *.html                  # 11 个交付页（根目录）+ font-check.html（自检页，不交付）
├── assets/
│   ├── css/style.css       # ⚠ 编译产物，勿手改
│   ├── scss/               # 样式源码，7-1 结构
│   ├── js/main.js          # 636 行，零依赖
│   ├── fonts/              # woff2
│   └── icons/              # SVG
├── images/                 # ⚠ 图片在顶层，不在 assets 下（与 Terra/EuroCave 不同）
├── figma/                  # 设计源：节点 JSON / 截图 / build spec / 原始资产。只读，不交付
├── tools/                  # shoot.py + shots/。不交付
├── docs/                   # 本文档所在。不交付
└── PP Palma - Free For Personal Use v1.0/   # 字体试用包，不交付
```

**11 个交付页**：`index`(Homepage) / `pdp` / `science` / `reviews` / `how-gumi-works` /
`our-story` / `faq` / `get-in-touch` / `referral` / `privacy-policy` / `shipping`

### 缓存版本号机制（改代码前必看）

HTML 里对 css / js 的引用都带 `?v=20260820-r15`，字体 url 里的 `?v=#{$build}` 来自
`assets/customstyle.scss` 顶部定义段的 `$build`。
**`file://` 预览会把无版本号的资源缓存到看不出改动** —— 第九轮为此白查过一轮
「改动没落实」。改了 CSS/JS 就同步升 `$build` 和 11 个 HTML 里的 `?v=`。

`font-check.html` 是构建自检页：显示当前 `$build`、10 条功能探针、字体渲染表。
**判断"我看到的产物是不是最新的"就开它**，比肉眼比对可靠。

---

## 3. 还原度审计

### 3.1 设计源在哪

| 要什么 | 去哪 | 说明 |
|---|---|---|
| **数值**（字号/行高/字距/色/间距/圆角/阴影） | `figma/nodes/*.json` | **唯一权威**。42 个 frame 的完整节点树 |
| 视觉参考 | `figma/screenshots/*.png` | 72 张 @1x。**只用于判断「有没有、谁在谁上面」** |
| 结构速查 | `figma/parser-out/*/build.txt` | 本地 parser 产物，层级+数值的紧凑视图 |
| **长文案** | `python3 figma/dump-text.py <node-id>` | ⚠ `build.txt` 会把长字符串截成 `...`，第十二轮为此漏抄过半句 |
| 逐页文案清单 | `docs/copy/` | 71 份 |
| token 汇总 | `docs/DESIGN-TOKENS.md` | 139 种字体组合 / 95 色 / 60 圆角 / 19 阴影 |
| 页面↔节点对照 | `docs/FIGMA-NODES.md` | 见下 |

### 3.2 ⚠ 不要调 Figma API

`/v1/images` 端点**账号级 429 限流中**（2026-08-20 实测，retry-after ≈ 3.98 天 →
约 08-24 解除）。`settings.json` 里那把 PAT 已耗尽。

- **数据端点 `/v1/files/nodes` 不受影响**，需要节点数据走这条。
- 但 `figma/nodes/` 已全量落盘，正常审计**不需要发任何请求**。
- 真要发且撞到错误：**立即停下告诉用户**（① 具体错误 ② 可能原因 ③ 如何继续），
  不静默重试、不假装拿到了数据。

### 3.3 页面 ↔ 节点对照（完整表在 FIGMA-NODES.md）

file key `R6ZWkjY1VNBAbljFhLjpuH`，交付 SECTION `401:31719`。

| 页面 | Desktop 1440 | Mobile 390 |
|---|---|---|
| Homepage | `285:18162` | `228:5932` |
| PDP | `324:52658` | `324:53792` |
| Science | `324:56865` | `324:58044` |
| Reviews | `324:63924` | `324:64961` |
| How Gumi Works | `324:69636` | `324:70523` |
| Our Story | `324:72839` | `324:73673` |
| FAQ | `324:75766` | `324:76169` |
| Get in Touch | `326:79979` | `326:80318` |
| Referral | `326:81218` | `326:81540` |
| Privacy Policy | `326:82363` | `326:83399` |
| Shipping | **无 desktop 稿** | `326:83129` |

⚠ **5 个 desktop 稿在 Figma 里重名叫「Our Story Desktop」**（设计方复制后没改名），
上表归属是逐个开图按首屏标题核实过的结果，不是坐标推断。别自己重新按名字认。

⚠ **33 个 frame 含 `characterStyleOverrides`**（同一段文字里换字体/色/字号）。
核对文字样式时必须逐字符查 `characterStyleOverrides` + `styleOverrideTable`，
只取 TEXT 顶层 style 会得出错误结论。清单在 DESIGN-TOKENS.md 末尾。

### 3.4 ⚠ 不要报成 bug 的清单

#### A. 字体 —— 不是最终字体，别按像素比

PP Palma 是 Pangram Pangram 的商业字体，**手上只有 "Free For Personal Use" 试用包**：

| 设计稿字重 | 用量 | 现在用的文件 | 状态 |
|---|---|---|---|
| 300 | 249 | `pppalma-fizzy-light.woff2` | 试用包原件 |
| **400** | **1914（全站 59%）** | **`pppalma-fizzy-light.woff2`** ← 同上 | ⚠ 见下方 |
| 500 | 747 | `pppalma-fizzy-medium.woff2` | 试用包原件 |
| 800 | 366 | `pppalma-fizzy-heavy.woff2` | 试用包原件 |

#### ⚠ 400 与 300 现在是同一个文件 —— 正文字重比稿轻一档

**这是全站最大的一处已知还原度偏差，且是有意的取舍，别当 bug 报。** 来龙去脉：

1. 稿里 400 用 **PPPalma-Regular**，试用包**恰好不给这一个**（而它占全站 59% 用量）。
2. 曾用插值件顶（FizzyLight + FizzyMedium，`T_SHAPE=0.50` / `T_SPACE=0.50`，
   494/501 字形成功，脚本在 `PP Palma - Free For Personal Use v1.0/make-regular-interp.py`）。
3. **2026-08-20 客户端实测：两个插值件都渲染成 last-resort monospace** —— 字体加载成功，
   但里面没有一个可用字形，于是全站正文回退、而 300/500/800 标题正常。
   这正是客户报的「字距看着散开」。**Linux Chrome 上复现不了**，
   而且双 `src` 兜底也没用（文件被接受，只是画不出东西，fallback 永不触发）。
4. 第十一轮据此**把 400 降级到真实试用文件 `fizzy-light`**，
   代价是 **300 与 400 同款，正文比稿轻一个字重档**（色深差一级）。

切换点仍是 `_fonts.scss` 顶部一行：
`$pp-400-src: "fizzy-light" | "fizzy-medium" | "fizzy-regular-interp" | "regular-interp"`。
度量参考：hero 行行宽 稿 319.00 / fizzy-light 317.80 / 插值件 320.00 ——
**light 在度量上更近，medium 在色深上更近**。

其他系统性偏差：

- 稿的 300/500/800 全是 **Fizzy** 切（字距更紧），**plain 家族同字重宽约 4%**。
  plain 版插值件（`T_SPACE=0.31`）就是为补这 4% 做的，现已不用。
- **结论：字宽、字距、字重色深与稿存在系统性偏差，已知且当前不可消除**，
  要等客户给授权 web font 才能做像素级验收。**报还原度时请把字体度量差单独归类**，
  不要混进「实现偏差」。
- 全站只走 `$font-brand-stack`，换字体只改 `_fonts.scss` 一处。
- ⚠ 400 那条 `@font-face` **故意没有 `local()`** —— 试用包 12 个 OTF 的
  typographic family 都叫 "PP Palma"，`local()` 会在装了字体的机器上劫持整族，
  导致设计师和其他人看到不同的字。**别"顺手补上 local() 兜底"**，第七轮专门拆过。

#### B. 断点 —— 只有两档有稿

**1440 和 390 是唯二有设计稿的宽度。** 768 / 1024 / 1920 没有稿，是按响应式规则推导的
（拥挤优先收窄 gap/padding 保持原布局，不重构）。那三档只能审「有没有坏」
（溢出、重叠、断行、可读性），不能审「像不像稿」。

#### C. 桌面稿与手机稿互相冲突的四处（**等设计方裁决**）

一律取信息量更大的一版，没有自造内容：

| 位置 | 桌面稿 | 手机稿 | 现在的做法 |
|---|---|---|---|
| Science 三张 stat 卡 | 三张同一句占位 | 三段各不同的真文案 | 用手机的文案；数值取 95%（桌面+homepage 一致） |
| Science 成分区收尾 | 「Shop Now」按钮 | 四行手风琴 | 两套都做，按断点切换 |
| Science nutrient 卡 | 3 张 | 4 张 | 做 3 张，不造第 4 张 |
| How Gumi Works 副标 | `This is a placeholder subheading.` | 真文案，珊瑚红 `#dd655e` | 文案用手机的，颜色各按各稿 |

#### D. 占位内容 —— 稿里就是占位，按铁律 3 原样保留

**这些不是实现问题，是设计稿自带的，上线前必须由客户替换：**

- **Reviews 专家卡三处引用文案里有竞品名 `Grüns`**（设计师抄了参考站）
- **Shipping 全页写的是美国配送**（Alaska / Hawaii / US Territories / $65 门槛），
  而 Gumi 是澳洲品牌
- **Privacy Policy 正文全是 lorem ipsum**
- PDP 页脚 6 条 accordion 是 `Accordion Closed` / `Text here`
- PDP 退款保证下方 3 个图标 + `tastes like` 图标是占位符（批注 `401:31225`）
- Get in Touch 的 Enquiry Type 稿里只给了 `Contact Us` 一项，现有四项是按
  header/footer 指向本页的四个链接补的，**需客户确认最终列表**

#### E. 实现边界 —— 这些区块**故意只有壳**（2026-08-19 用户拍板）

由 Shopify app / metafield 产出的内容，前端不实现逻辑、不填假数据，只留结构占位：

| 页面 | 区块 | 标记 |
|---|---|---|
| PDP | 订阅选购（Autoship / Subscribe & Save / One Time） | `.product__app-slot[data-app="subscription"]` |
| PDP | 产品详情 accordion（Why Gumi / Ingredients / Science / Directions） | 只做 accordion 壳 |
| PDP | 评论区（4.76 / 123,000 reviews / 点赞点踩） | app 渲染 |
| **Reviews 页** | 整页评论列表 | app 渲染 |
| 全站 header | Trustpilot 徽章 | 第三方嵌入，现为文字占位 |

⚠ 连带作废：批注 `401:31223`（评论支持传图、点赞点踩排序）**属评论 app 能力，本次不实现**。
⚠ 仍要做的：**营养标签弹窗**（批注 `401:31227`）不是 app 内容，已实现。
⚠ **Referral 逻辑**明确不在 MVP 范围（设计方交接说明原文），只有视觉。

#### F. 稿里根本没有、由本项目自定的值

改这些不算「修还原度」，算「补设计」，要标出来让设计方给值：

- **全部 hover / active 交互态**（稿里完全没有）。抬起量、投影、时长（.15/.2/.3s）、
  曲线（easeOutCubic）都是自定值，集中在 `_variables.scss` 的 motion 段。
- 手风琴与 tab 的**展开态图标**形态。
- PDP 产品图 sticky 的**吸顶偏移**（现用 `top: 24px`，批注只说要 sticky 没给数值）。
- 营养标签弹窗**开合时长**（0.4s）与曲线。
- 表单 **focus ring**（`_form.scss` 里那圈 `0 0 0 3px rgba(0,86,53,.15)`）。

#### G. 已知的浏览器差异（有意接受）

**手风琴展开动画只在 Chrome 系有**（`::details-content` + `interpolate-size`）。
改成原生 `<details>` 是为了让开合不依赖 JS，代价是 Firefox / Safari 瞬开瞬收。
这是权衡结果，已列入「落地前需向设计方确认」。

---

## 4. CSS 审计

### 4.1 架构

单文件 `assets/customstyle.scss`（第十五轮由 36 个 partial 合并而来），块顺序写死为
**定义段 → base → components → layout → modules**（原 36 个 partial）。
产物 `assets/customstyle.css` 144KB，未压缩、无 sourcemap。

文件分两段（合并前的 partial 名保留在块注释里，方便对着历史 changelog 找）：

```
第一段 定义（无 CSS 输出，Sass 要求先定义后使用，被迫排最前）
  variables(token+motion)  mixins  masks(内联 mask)

第二段 输出（顺序 = 原 style.scss 的 @use 顺序，层叠依赖它）
  fonts  reset  [mixins 的 :root{--pad-x} 块]  typography  animation(wowo)
  accordion button modal motion scallop scallop-box arc-text
  header footer page-hero
  hero logo-scroll stats science nutrition product reviews promo vs faq
  faq-image expert dosed story cta-band form rich-text compare ingredients
```

⚠ `:root{--pad-x}` 原本住在 `_mixins.scss` 里，但它是 CSS **输出**不是定义，
所以留在第二段 reset 之后的原位，没跟着 mixin 定义提到最前 —— 合并前后产物逐字节
相同就是靠这个安排，别把它当成错误「修正」。

### 4.2 项目内的 CSS 纪律（审计时按这个判）

- **改样式前先定位真正胜出的规则**（特异性 + 加载顺序），**在原位就地改**，
  不往文件末尾堆覆盖。判据：将来调试时一条 `grep` 能不能找齐所有相关规则。
- 数值一律引用 `_variables.scss` 的 token，不散落硬编码。
- **hover 一律 `@include hover`**（内部包 `@media (hover: hover)`），
  否则触摸屏点完 hover 态会粘住。
- **任何状态变化都要有 `transition`**，时长/曲线取 motion token，不各处自己填 `0.3s ease`。
- 响应式「拥挤」默认收窄 gap/padding 保持原布局，**不重构**。

### 4.3 现状基线（截至 r15，供你对照，不是结论）

| 指标 | 值 |
|---|---|
| `!important` | 3 |
| `z-index` 声明 | 14 |
| `@media` 块 | 317 |
| `:hover` / `transition` | 41 / 53 |

`:hover` 与 `transition` 的比值是**铁律 13 的自查判据** ——
两个数差很多就说明有 hover 没配过渡。现在 41:53 是合理的（很多 transition 服务于非 hover 状态）。

### 4.4 已知的可疑点 / 技术债（我知道的，你可以直接查证）

1. **mask 全部内联成 data URI**（`helpers/_masks.scss`，**27.1 KB**：
   `$mask-scallop-box` 13.3K / `$mask-scallop-band` 11.3K / `$mask-scallop-card` 1.3K）。
   这是**被迫的**，不是体积失控 —— `file://` 下 CSS mask 引用外部文件会被 CORS 拦掉，
   mask 静默变空并把元素整块吞掉，而 computed style 一切正常。
   **不要建议改回 url() 外链**，会直接让客户预览时元素消失。
   （前两个是 PNG 阈值图，第三个是 URL-encoded SVG。）
2. **`.scallop` 波浪条**用 repeating-radial-gradient 画，几何靠节距推导
   （`r = 0.6407d`, `amp = 0.24008d`）。`_scallop.scss` 里的注释解释了为什么不能用
   固定尺寸 —— 旧的封顶写法在 ≥1920 会把弧切断。
3. **`.cta-band` 的 mask 是从画板渲染图抠的**，不是几何生成 ——
   那组弧不满足 `r = 0.6407d`（实测节距 ~88 对振幅 56，无单一半径满足）。
   代价：**低于 1280 宽时弧会略微压扁**。`_cta-band.scss` 注释里写了取舍理由。
4. **317 个 @media 块**分散在各 partial 里（每个模块自己写自己的断点），
   不是集中式。这是 7-1 的常规做法，但如果你要审重复度，这是入口。
5. `assets/customstyle.css` **未压缩**。静态阶段有意不压 —— 压了就没法在浏览器里直接对源。
   Shopify 阶段再上构建。

---

## 5. JS 审计

`assets/main.js`，**636 行，零依赖**（无 jQuery / GSAP / Swiper / AOS），
单个 IIFE 包住，页面底部 `<script>` 引入（非 defer/async —— 在 `</body>` 前）。

八个模块，按文件顺序：

| 模块 | 行 | 职责 |
|---|---|---|
| `wowo` | 5 | 滚动入场，从 Terra 主题 1:1 移植（去掉 jQuery） |
| `header` | 61 | 桌面下拉面板 / 移动全宽抽屉 |
| `bear-meter` | 107 | 按 `data-total` / `data-fill` 渲染小熊填充比例 |
| `popText` | 130 | 逐词入场，转写自 cravburgers.shop（批注 `401:29596`） |
| `modal` | 240 | 营养标签面板（批注 `401:31227`），底部上滑 |
| `slider` | 325 | 横向 snap 轨道的箭头控制 + 无限循环 |
| `gallery` | 527 | PDP 缩略图轨驱动主图 |
| `enquiryPrefill` | 587 | 联系表单按 `?type=` 预选咨询类型 |

### 关键契约（改之前必须懂）

- **`.wowo { opacity: 0 }` 是无条件的。** JS 没加载或报错 → 内容**永久不可见**。
  兜底只有 `<noscript><style>.wowo{opacity:1!important}</style></noscript>`，
  **它挡不住"JS 加载了但抛异常"这一种**。任何触碰 main.js 或加载顺序的改动，
  都必须验证首屏元素最终 `opacity` 回到 1。
- wowo 的机制：进视口加 `.animated` 播 0.7s → **1500ms 后移除两个 class**。
  **只播一次，不可重播。** 写截图脚本时必须等够 1700ms，否则拍到半播状态，
  肉眼看像"文字重影"。
- **`data-pop-text` 逐词弹出只用在首页四个 `.stat` 上**（第八轮收窄的范围）。
  其余全站文字容器一律 `wowo fadeInUp`、图片容器 `wowo fadeIn`。
  **不要"顺手给标题也加上 pop"** —— 第十二轮犯过，被 CHANGELOG 抓回来。
- 描边文字里的数字用 `data-pop-atom` 整块弹出，逐字拆会把描边拆断。

### 已知风险点

- `slider` 的拖拽会吞掉拖动结束时的那次 click（有意为之，注释在 482 行）。
- `modal` 用 `aria-hidden` + 内部可聚焦元素时有陷阱，384 行注释写了处理方式。
- 无错误边界：任一模块抛异常会中断后续模块初始化（单 IIFE，非逐模块 try）。
  **这条直接关系到上面 `.wowo` 的永久不可见风险**，值得审。

---

## 6. 性能审计

### 6.1 现状事实（已核实，直接用）

| 项 | 值 |
|---|---|
| `images/` 总计 | **5.9 MB** / 18 个文件 |
| 最大的几张 | `gumi-bear-front.png` 828K、`vs-bear-glow.png` 826K、`promo-art.png` 803K、`gumi-bear-front-glow.png` 787K、`stats-bear.png` 565K |
| 格式 | **全是 PNG**，无 webp/avif，无 `<picture>`/`srcset` |
| `<img>` 总数 / `loading="lazy"` | 87 / **10** |
| 带 `width`+`height` 属性 | 81 |
| `rel="preload"` | **0**（字体也没有） |
| `font-display` | `swap` × 16 |
| `assets/*.woff2` | 804K，13 个被引用 + 6 个未引用 |
| `assets/customstyle.css` | 144K 未压缩 |
| `assets/main.js` | 32K 未压缩，零依赖 |
| 外部请求 | **0**（无 CDN、无第三方脚本、mask 已内联） |

### 6.2 审这里之前，先分清阶段

**静态阶段做了没意义、Shopify 阶段才该做的**（列出来是让你不必花力气写建议）：

- CSS/JS 压缩与合并 → Shopify 有自己的资源管线
- 图片 CDN / 响应式尺寸 → Shopify `image_url` filter 会接管
- HTTP 缓存头 / HTTP2 push → 平台侧

**现在就值得报的**：

- 图片本身的**源体积**（5.9MB 的 PNG，进了 Shopify 也还是这么大的源）
- **透明 PNG 是否真的需要 PNG**（几张 800K 的是带 alpha 的小熊，webp 可能省 70%+）
- lazy 覆盖率 10/87
- 字体：**5 个族**同时加载（PP Palma / Inter / Lexend / Playpen Sans / Figtree），
  首屏关键字体没有 preload
- `.wowo` 的 opacity:0 与 LCP 的关系 —— 首屏元素靠 JS 显形，**这对 LCP 是实打实的影响**，
  值得实测而不是推断

### 6.3 已知待清理（我知道的，省你时间）

| 文件 | 情况 |
|---|---|
| `assets/diag-a-resave.woff2`、`diag-b-rewrite.woff2` | **诊断残留，可删**（62K） |
| `assets/pppalma-{light,medium,regular-interp,fizzy-regular-interp}.woff2` | `$pp-400-src` 的候选备件，**当前未引用但有用途**，别当垃圾删 |
| `assets/plus-jakarta-sans-*` | 第二备选字体，`customstyle.scss` 里注释着，**有意保留** |
| `images/scallop-box.png` | **已内联成 data URI**，磁盘文件不再被引用；保留为源即可 |
| `images/bear-gummy.png` | 是 `bear-gummy-glow.png` 的**生成源**（`figma/optimize-images.py`），**不是垃圾** |
| 根目录 `0e110e9b-….png`、`1e4ea5b2-….png` | 疑似对话中贴入的临时截图，**不属于项目** |

---

## 7. 验证工具与判据

### 7.1 判据纪律（全局铁律 6，本项目吃过亏的）

- **CSS 改了结构/顺序 → diff 产物无效**。判据 = 全站 computed-style 快照，
  **必须含 `::before` / `::after`**（本项目大量用伪元素画线和装饰）。
- **负向断言（"已无 XXX"）必须先验锚点存在**。取错文件（404/空）会让断言恒真、报全绿。
- **两个比对量若共享同一污染源，自洽 ≠ 正确**，须比不变量。

### 7.2 ⚠ headless / `file://` 陷阱清单（本项目实际踩过的）

1. **`file://` 下 CSS mask 引用外部文件被 CORS 拦掉**（origin null），
   mask 静默变空 → **被遮罩的元素整块消失**，而 computed style 一切正常。
   本项目所有 mask 已内联。**看到元素消失先想这条。**
2. **截图必须等 1700ms**。wowo 播 0.7s、1500ms 才卸 class，早拍会得到半播状态。
3. **断点隐藏的元素 opacity 恒 0**，别当成"卡住的 wowo"。
   `shoot.py` 用 `el.offsetParent === null` 跳过它们。
4. **headless 直连时 `(hover: hover)` 恒 false** → 全站 hover 规则一条都不生效。
   **验 hover 必须用 Playwright**（它不占这个限制）。
5. **注入 `animation: none` 会让靠入场动画显形的区块停在第 0 帧**，
   截图全白而计算样式全正常。
6. **元素截图按边界盒裁**，descender / 描边光晕本来就在盒外，会被误读成"渲染被切"。
   本项目大量用 `ink-outline()` 描边，**留白 clip 再截**。
7. **`getComputedStyle` 读 `--x` 拿到的是未求值的字符串**，不是像素。
   判据要改读吃了它的普通属性。
8. **`letter-spacing: 0` 的 computed 就是 `normal`**，与"没写"不可区分。
9. snap chromium 直连的固有局限（最小窗口 500×657、无 GPU、读不到 `/tmp`）：
   **Playwright 一条都不占**，但要自己指 `executable_path`。

### 7.3 上一轮的验证结论（可作为基线）

`python3 tools/shoot.py --all` 最近一次（r15，CTA 修复后）：
**55/55 全绿** —— 11 页 × 5 宽度，横向溢出 0、卡住的 `.wowo` 0。

Playwright 实测（第六轮）：**46 类可点击元素 hover 全部生效、cursor 全为 pointer**，
触摸端反证不粘住。**注意这是两页时的数字，现在 11 页了，交互态需要重新全量清点。**

---

## 8. 建议的审计范围与输出

四条线，互相独立，可并行：

| # | 线 | 核心问题 | 主要判据 |
|---|---|---|---|
| 1 | **还原度** | 1440 / 390 两档与稿的数值偏差 | 节点 JSON 的数值 vs computed style，**逐 token 比**，不目测 |
| 2 | **CSS 质量** | 重复/失效规则、特异性战争、断点一致性、伪元素副作用 | 全站 computed-style 快照；`grep` 可定位性 |
| 3 | **JS 质量** | 错误边界、事件解绑、重复绑定、`.wowo` 永久隐藏风险 | 实跑 + 人为注入异常看降级 |
| 4 | **性能** | 图片源体积、字体策略、LCP 与 wowo 的关系、lazy 覆盖 | 实测（Playwright + Lighthouse），不推断 |

**交互态清点是第 5 项独立工作**（铁律 13）：11 页所有 `a[href]` 与 `button`，
比对 hover 前后 computed style，找出"有 hover 没 transition"和"能点没 hover"两类。
上一轮只清点过 2 页。

### 输出要求

- 报告写到 `docs/audit/`，一条线一个文件。
- 每条发现给：**位置（`file:line`）+ 现象 + 判据（怎么验的）+ 建议**。
- **必须区分三类**：① 真缺陷 ② 第 3.4 节里的"有意为之/待裁决" ③ 需设计方给值。
  混在一起的报告没法用。
- **不改代码。** 修复是下一轮的事，且要等用户明确指令。
- 如果发现与本文档矛盾的事实，**以你实测为准并在报告里点明**，本文档可能已过时。

---

## 9. 一句话状态

11 个静态页全部落地，55/55 回归绿，**未推送任何东西**；
Shopify 主题化未开始（店铺 / 主题基底 / 接入方式三项未定）；
等设计方裁决 4 处两稿冲突，等客户替换 3 处占位文案 + PP Palma 授权字体。

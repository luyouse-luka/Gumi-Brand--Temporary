# Gumi Brand — 性能审计报告（第 4 线）

> 审计日期 2026-08-20 · 范围：`file://` 静态阶段的 11 个交付页
> 依据 [AUDIT-HANDOFF.md](../archive/AUDIT-HANDOFF.md) 第 6 节（性能）与第 7 节（判据纪律）
> **本轮只出报告，未改动任何项目文件。** 唯一新增文件是本文件。

---

## 0. 怎么跑出来的

所有探针脚本在 `/tmp/claude-1007/-home-ly/c7ffb540-53f6-4bbe-87d6-fe452694dbc5/scratchpad/`
（会话级临时目录，不进项目）。Playwright 一律显式
`executable_path=~/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome`。

| 脚本 | 做什么 | 产物 |
|---|---|---|
| `img_stats.py` | 18 张 PNG 的像素尺寸 / 磁盘体积 / alpha 通道是否真被用到 | 见 §1 |
| `probe_perf.py 1440 900` / `390 844` | 11 页 × 2 宽度：LCP（PerformanceObserver `largest-contentful-paint`）、CLS（`layout-shift`）、longtask、`document.fonts`、每个 `<img>` 的 `naturalWidth` vs `getBoundingClientRect()`、CDP `Performance.getMetrics` 取 ScriptDuration/LayoutDuration/RecalcStyleDuration | `perf-1440.json` / `perf-390.json` |
| `probe_req.py` | `page.on("request")` 抓 `file://` 请求，分「首屏加载」与「滚到底之后」两批 —— 这是**唯一能证明某张图到底下没下**的判据（ResourceTiming 在 `file://` 下恒为空） | `req-1440.json` |
| `perf_lcp2.py` | **LCP 因果 A/B**：把整站复制到 scratchpad 造 5 个变体（A 原样 / B 关掉 `.wowo` 透明门 / C 再关 `.float-art`+`.pop-word` / D 直接把 `wowo` class 从 HTML 里删掉 / E `main.js` 置空），每个变体在 t=300ms 先跑**存活性断言**（确认改动真的生效）再测 LCP | `perf_lcp2.json` |
| `perf_lazytest.py` | 变体 F（给所有无属性的 img 补 `loading="lazy"`）、G（F + 面板关闭时 `.nav-card__art{display:none}`），实测首屏请求字节数 | 见 §2 |
| `perf_thrash.py` | 同一元素集合上做 interleaved（现在的写法）vs batched（先读后写）A/B 计时；并统计整页滚动过程中 `wowo.run()` 被调用几次、累计几毫秒 | `perf_thrash.json` |
| `perf_webp.py` | 每张 PNG 转 3 种目标（同尺寸 q82 / 同尺寸 lossless / 缩到实测渲染尺寸的 2× 后 q82），只写到 scratchpad，**不碰 `images/`** | `perf_webp.json`、`perf_conv/` |
| `perf_fontshift.py` | 变体 H（PP Palma 的 url 打断）/ I（PP Palma + Figtree 都打断），比对 130 个文本块的 y 坐标与文档总高 —— 这是 FOUT 重排的**替代判据** | `perf_fontshift*.json` |
| `perf_layers.py` | 统计 `will-change != auto` 的元素数、`.pop-word` 数、`.bear-meter__bear` 数 | 见 §5 |

**项目文件未被修改**，A/B 全部在 `scratchpad/perf_var/{A..I}/` 的独立副本上做；
`assets/css/style.css` md5 `060c27f1…`、`assets/js/main.js` md5 `032b7c5e…` 审计前后一致。

---

## 1. 结论速览（按收益排序）

| # | 级别 | 发现 | 实测收益 |
|---|---|---|---|
| A-1 | **P0** | 15 张实际被引用的 PNG，源体积 5.05 MB；转 WebP 后 473 KB | **-4.60 MB / -91%** |
| A-2 | **P0** | LCP 元素被 `.wowo{opacity:0}` 挡住，11 页一律在 **DCL + ~1500ms** 才被记录 | LCP **1.55s → 0.07s**（-1.5s） |
| A-3 | **P0** | `nav-card-bear.png` 312 KB，导航面板**关着也照下**，11 页每页都下 | 每页 **-312 KB**（PNG 口径） |
| A-4 | **P1** | 62 个首屏以下的 `<img>` 没有 `loading="lazy"` | index 首屏 **-661 KB** |
| A-5 | **P1** | 3 张图的源分辨率是显示尺寸的 5.9~12.5 倍 | 3 张合计 **1.76 MB → 33 KB** |
| A-6 | **P1** | 3 个首屏关键字体文件（97.4 KB）**0 preload**；实测换字体会让 index 上 **65/130** 个文本块位移，最大 52px | 见 §4 |
| A-7 | **P1** | `main.js` 加载成功但抛异常时，index 上 **30 个元素永久 opacity:0**，`<noscript>` 挡不住 | 与 JS 审计线重叠 |
| B-1 | P2 | `wowo.run()` 读写交替（forced sync layout），同元素集合上比批处理慢 3.1~4.1× | 当前规模只值 **3.6ms**，量级不痛 |
| B-2 | P2 | `will-change` 永不释放：index 68 个元素常驻合成层；`.float-art` 挂着 5s 无限动画 | 本机无 GPU，需真机验 |
| B-3 | P2 | 首屏 hero 图桌面端**欠采样** 1.20×（源 528px 对 439 CSS px），retina 上发虚 | 与其余「过采样」正好相反 |
| B-4 | P2 | index 移动端 CLS = 0.01416，源头 `DIV.hero__cta` | 远低于 0.1 阈值 |
| C-1 | ③ | `bear-gummy-glow.png`（374 KB）**全站零引用** —— 交接文档只说了它的**生成源** `bear-gummy.png` 有用途，没说它自己也没人用 | 需确认 |
| C-2 | ③ | Inter / Lexend / Playpen Sans 三族 `@font-face` 声明齐全但**没有任何选择器引用**，一个字节都没下载 | 需设计方裁决 |
| C-3 | — | 根目录两个 UUID 命名的 PNG 确认不属于项目（只报告，未删） | 见 §7 |

---

## 2. 图片

### 2.1 逐张实测（源尺寸 / 体积 / alpha / 实际显示尺寸）

「显示尺寸」= 1440 与 390 两档里**最大**的那次 `getBoundingClientRect()`（探针 `probe_perf.py`）；
「倍率」= 源宽 ÷ 显示宽，>2.0 就说明超出 2× DPR 所需。

| 文件 | 源尺寸 | 磁盘 | alpha 真用到 | 最大显示尺寸 | 倍率 | 在哪 |
|---|---|---|---|---|---|---|
| `gumi-bear-front.png` | 1200×927 | 808 K | ✅ 不透明占比 31.6% | **96×96**（`object-fit:contain`） | **12.50×** | science 对比头像 |
| `vs-bear-glow.png` | 1200×927 | 807 K | ✅ 35.6% | **202×156** | **5.94×** | pdp `.vs__bear` |
| `bear-scatter.png` | 400×309 | 100 K | ✅ 28.7% | **76×94**（9 处，最小 46×84） | **5.26~8.70×** | index nutrition |
| `promo-art.png` | 1413×1209 | 784 K | ✅ 26.1% | 470×402 | 3.01× | pdp / science / reviews |
| `others-bottles.png` | 240×240 | 85 K | ✅ 31.8% | 112×112 | 2.14× | pdp / science |
| `media-vogue.png` | 369×106 | 16 K | ✅ 18.9% | 139×40 | 2.65× | index logo 带 |
| `media-abc-news.png` | 348×74 | 15 K | ✅ 35.7% | 160×34 | 2.18× | index logo 带 |
| `media-wellbeing.png` | 200×45 | 6 K | ✅ 27.2% | 160×36 | 1.25× | index logo 带 |
| `nav-card-bear.png` | 523×631 | 312 K | ✅ 46.4% | 261×315 | 2.00× ✔ | 全站 header 面板 |
| `stats-bear.png` | 1121×986 | 551 K | ✅ 23.7% | 560×493 | 2.00× ✔ | index stats |
| `deco-bear-md.png` | 880×774 | 355 K | ✅ 23.6% | 440×387（390 档只有 160×141） | 2.00× ✔ / 5.50×（移动） | 全站页脚 |
| `deco-bear-sm.png` | 659×580 | 206 K | ✅ 23.6% | 329×290（390 档只有 154×136） | 2.00× ✔ / 4.28×（移动） | 全站页脚 |
| `product-pack.png` | 877×1005 | 355 K | ✅ 13.0% | 493×549 | 1.78× ✔ | index pack 带 |
| `gumi-bear-front-glow.png` | 528×874 | 768 K | ✅ 82.9% | 439×727（未旋转） | **1.20×（欠采样）** | index hero |
| `bear-icon.png` | 27×44 | 3 K | ✅ 65.9% | 27×44 | 1.00× | science CSS 背景 |
| `bear-gummy.png` | 760×587 | 375 K | ✅ | — 无引用 | — | glow 生成源（保留） |
| `bear-gummy-glow.png` | 760×587 | 374 K | ✅ | — **无引用** | — | 见 C-1 |
| `scallop-box.png` | 1040×1040 | 25 K | ✅ | — 已内联为 data URI | — | 保留为源 |

18 张全部是 RGBA 且 alpha **确实在用**（透明像素占比 17%~87%），所以不能一刀切换成 JPEG；
但**WebP 完整支持 alpha**，实测 alpha 通道最大误差 = **0**（逐像素比对，`perf_webp.py`）。

### 2.2 「源体积 → 可优化到多少」

三种目标各转一份实测（不覆盖项目里的图；产物在 `scratchpad/perf_conv/`）：
① 同尺寸 WebP q82 ② 同尺寸 WebP 无损 ③ 先缩到「实测显示尺寸 × 2」再 q82。
取三者最小的一个作为目标。

| 文件 | 现在 (PNG) | 目标 | 省 | 用哪种 | 目标尺寸 |
|---|---:|---:|---:|---|---|
| `gumi-bear-front.png` | 827,691 | **7,068** | **-99%** | 缩到 2× 后 q82 | 249×192 |
| `vs-bear-glow.png` | 825,970 | **18,534** | **-98%** | 缩到 2× 后 q82 | 448×346 |
| `promo-art.png` | 802,725 | 91,016 | -89% | 缩到 2× 后 q82 | 940×804 |
| `gumi-bear-front-glow.png` | 786,604 | 76,370 | -90% | 同尺寸 q82 | 528×874（保持） |
| `stats-bear.png` | 564,650 | 58,782 | -90% | 同尺寸 q82 | 保持 |
| `product-pack.png` | 363,655 | 92,870 | -74% | 同尺寸**无损** | 保持 |
| `deco-bear-md.png` | 363,495 | 38,514 | -89% | 同尺寸 q82 | 保持 |
| `nav-card-bear.png` | 319,109 | 30,586 | -90% | 同尺寸 q82 | 保持 |
| `deco-bear-sm.png` | 211,192 | 23,116 | -89% | 同尺寸 q82 | 保持 |
| `bear-scatter.png` | 102,118 | **7,402** | **-93%** | 缩到 2× 后 q82 | 243×188 |
| `others-bottles.png` | 86,614 | 21,238 | -75% | 缩到 2× 后 q82 | 224×224 |
| `media-vogue.png` | 15,926 | 7,768 | -51% | 同尺寸**无损** | 保持 |
| `media-abc-news.png` | 15,604 | 7,632 | -51% | 同尺寸**无损** | 保持 |
| `media-wellbeing.png` | 6,139 | 2,594 | -58% | 同尺寸**无损** | 保持 |
| `bear-icon.png` | 3,250 | 1,034 | -68% | 同尺寸 q82 | 保持 |
| **被引用的 15 张合计** | **5,294,742 (5.05 MB)** | **484,524 (473 KB)** | **-91%** | | |
| 另有 3 张零引用（bear-gummy / bear-gummy-glow / scallop-box） | 792,952 | — | 从不加载，不计入 | | |
| `images/` 目录总计 | 6,087,694 (5.81 MB) | — | | | |

**质量判据**（不是「看着还行」）：把原图与 q82 解码结果**都合成到白底**（页面真实底色）后算 PSNR ——
`media-*` 三张 48~50 dB、`deco-bear-*` 40 dB、`stats-bear` 40.6 dB、`gumi-bear-front-glow` 37.0 dB、
最差的 `bear-icon` 31.5 dB / `others-bottles` 34.4 dB。**≥35 dB 视觉无损**，
所以除了这两张小图需要单独调 q 值（或直接用无损），q82 可以作为默认起点。
`media-*` 三张是平涂 logo，**无损反而更小**（7.6 K vs 8.5 K），别一律走有损。

### 2.3 逐页首屏实际下载量（实测请求，非推断）

`probe_req.py` 抓 `page.on("request")`。字体 97.4 KB / CSS 160 K / JS 24 K 每页恒定。

| 页面 | HTML | 首屏图片 (PNG) | 首屏总计 | 图片换 WebP 后 | 总计 | 降幅 |
|---|---:|---:|---:|---:|---:|---:|
| science.html | 44 K | **2,553 K** | 2,878 K | 208 K | 532 K | **-82%** |
| index.html | 91 K | **2,332 K** | 2,704 K | 248 K | 620 K | -77% |
| pdp.html | 86 K | 1,764 K | 2,131 K | 129 K | 496 K | -77% |
| reviews.html | 50 K | 1,657 K | 1,988 K | 179 K | 510 K | -74% |
| how-gumi-works / our-story / faq / get-in-touch / referral / privacy-policy / shipping | 25~64 K | **873 K**（全是 nav-card + 两只页脚熊） | ~1,180 K | 90 K | ~400 K | -66% |
| **11 页合计** | | | **17.61 MB** | | **4.89 MB** | **-72%** |

> 7 个「纯文本页」自己只有 25~64 KB 的 HTML，却每页拖着 **873 KB 的装饰性 PNG** ——
> 占首屏总量的 74%。这是最刺眼的一处。

### 2.4 建议

**现在就该做（静态阶段）**

1. **[P0]** 把 `images/` 的 15 张在用图各出一份 WebP，HTML 用 `<picture><source type="image/webp">` +
   `<img src="…png">` 兜底。PNG 源保留（Shopify 阶段 `image_url` 需要高分源）。
   → 全站 -4.6 MB。转换脚本可参考 `scratchpad/perf_webp.py`，**别直接跑它覆盖项目图**。
2. **[P1]** 三张严重超采样的图**直接重出**（`gumi-bear-front` 用于 96×96 头像时另存一份小的，
   不要与 pdp/science 的大图共用一个文件；`vs-bear-glow` 只用在 202×156；
   `bear-scatter` 最大只用到 76×94）。→ 1.76 MB → 33 KB。
3. **[P2]** `deco-bear-sm/md` 桌面 2.0×（合规）但移动端只显示 154×136 / 160×141，
   即移动端在下 4.3~5.5 倍的像素。加 `srcset` 出一份移动尺寸即可。
4. **[P2]** 反向问题：`gumi-bear-front-glow.png` 是**首屏 LCP 图**，源 528px 对应 439 CSS px
   （倍率 1.20），在 2× 屏上是放大显示 → 发虚。这张要**加大**到 ~880px 宽再压 WebP
   （加大后 WebP 体积仍远小于现在的 768 KB PNG）。

**Shopify 阶段再做**：`srcset` 断点由 `image_url` filter 接管、CDN 与格式协商由平台侧处理 ——
本节只解决「源文件本身就这么大」这一层，那一层进了 Shopify 也省不掉。

---

## 3. lazy 覆盖率

### 3.1 实测分类（84 个 `<img>`，交付 11 页）

> **纠正交接文档**：6.1 表里的 `87` 含 `font-check.html` 里 3 个 JS 模板字符串（`<img class="hero__bear">`，
> 不是真元素、也不交付）。交付页实际是 **84 个 `<img>`**。

| 类别 | 数量 | 判据 |
|---|---:|---|
| 首屏以下但**没有** `loading="lazy"` | **62** | 1440 档 `top>900` **且** 390 档 `top>844` |
| ├─ 其中显式写了 `loading="eager"` | 24 | index 的 8 组 media logo（`top≈980` / `1292`） |
| └─ 其中什么属性都没有 | 38 | `deco-bear-*`×22、`bear-scatter`×9、`vs-bear-glow`、`others-bottles`×2、`promo-art`×2、`stats-bear`、`gumi-bear-front` |
| 首屏内但**被折叠面板藏着**，仍照下 | 11 | `nav-card-bear.png`，`top=191`，每页一个 |
| `loading="lazy"` 且确实在首屏以下 ✅ | 10 | `product-pack`×9（index）、`promo-art`×1（pdp） |
| 首屏内且正确 eager ✅ | 1 | `gumi-bear-front-glow`（index hero，LCP 图） |

**「首屏的图反过来不该 lazy」这一类：0 个。** 全站没有把 `loading="lazy"` 误挂到首屏图上的情况 ——
唯一的首屏图（hero 熊）没写 loading 属性，默认 eager，是对的。

### 3.2 补 lazy 到底能省多少 —— 实测，不是推断

`perf_lazytest.py`，三个变体各测「load 事件 +1200ms 内实际发出的 PNG 请求」：

| 变体 | index 首屏 PNG | faq 首屏 PNG |
|---|---:|---:|
| 现状 | 10 张 / **2332.1 KB** | 3 张 / **872.8 KB** |
| F：给所有无属性的 img 补 `loading="lazy"` | 7 张 / **1671.2 KB**（-661 KB） | 3 张 / **872.8 KB**（**-0**） |
| G：F + 面板关闭时 `.nav-card__art{display:none}` | 6 张 / **1359.5 KB**（-972 KB） | 2 张 / **561.2 KB**（-311 KB） |

三条必须写清楚的事实：

1. **`loading="lazy"` 对 `nav-card-bear` 完全无效。** 它在 `.header__panel`（`grid-template-rows:0fr`
   + `overflow:hidden`）里，但 `position:absolute` 的 `.nav-card__art` 仍然算出 261×315 的
   rect 且 `top=191` —— 落在视口内，浏览器判定「该加载」。变体 F 实测它照下不误。
   **正解是让它在面板关闭时没有盒子**（`display:none` / 面板加 `content-visibility:hidden` /
   或改成 `.header.is-open` 才生效的 CSS 背景图）。变体 G 实测每页省 **311 KB**。
2. **短页面上 lazy 也救不了页脚两只熊。** faq 的 `deco-bear-sm/md` 在 `top=1647/2157`，
   落在 Chrome 的 lazy 距离阈值内 → 补了属性照样下（F 变体 faq 一字节没省）。
   这两张要靠 **§2 的 WebP + 尺寸** 解决（574 KB → 61.6 KB），不是靠 lazy。
3. index 的 24 个 media logo 显式写了 `loading="eager"`，但它们在 `top≈980`（1440）/ `1292`（390），
   两档都在折线以下。三张 logo 加起来只有 37 KB，**改不改都不影响大局**，
   但如果 `eager` 是为了让跑马灯量到宽度，那属于 §5 B-1 那类隐式耦合，值得在注释里写明原因。

### 3.3 建议

- **[P0]** 面板关闭时不渲染 `.nav-card__art` —— 11 页每页 -311 KB，是**唯一一处全站通吃**的改动。
  改 `_header.scss`，不要往文件末尾堆覆盖（铁律 4）。
- **[P1]** 给 §3.1 里那 38 个「什么属性都没有」的 `<img>` 补 `loading="lazy"`。
  index 省 661 KB；短页面省不到，但不会更差。
- **[P2]** 24 个 media logo 的 `loading="eager"` 如果没有非它不可的理由（跑马灯测宽？），
  改成默认或 lazy；如果有理由，在 HTML 里留一行注释说明，否则下一轮一定有人「顺手改掉」。

---

## 4. 字体

### 4.1 ⚠ 实测推翻交接文档 6.2 的「5 个族同时加载」

`document.fonts` + 请求抓取（11 页 × 1440/390 全跑过），结论是：

```
每页实际下载的 woff2 = 恰好 3 个，全是 PP Palma：
  pppalma-fizzy-light.woff2   31.9 K   (weight 400，即正文；300 复用同一 URL)
  pppalma-fizzy-medium.woff2  32.6 K   (weight 500)
  pppalma-fizzy-heavy.woff2   32.9 K   (weight 800)
                              ------
                              97.4 K
```

`document.fonts` 的 12 个 FontFace 状态：PP Palma 400/500/800 = `loaded`，
**PP Palma 300 / Figtree×2 / Inter×2 / Lexend×2 / Playpen Sans×2 全部 `unloaded`。**

原因很直接：`assets/css/style.css` 里**只有 21 条 `font-family`**，全部是
`"PP Palma","Figtree",-apple-system,…` 这一个栈；`$font-ui-stack` / `$font-display-stack` /
`$font-hand-stack` 三个变量在 `_fonts.scss` 里定义之后**再没有任何地方引用**
（`grep -rn 'font-ui-stack' assets/scss/` 只命中定义那一行）。
所以 Inter / Lexend / Playpen Sans 的 `@font-face` 是**死声明**，浏览器一个字节都不会取。

`assets/fonts/` 19 个文件里**只有 3 个会被请求**，另外 16 个（674 KB）从不出现在网络里。
（交接文档 6.1 写的「13 个被引用」指的是 SCSS 里写了 `url()`；实际**匹配到字形**的只有 3 个。）

- ➡ **性能上这不是问题**（未匹配的 `@font-face` 不会触发下载），但
- ➡ **它是个还原度事实**：设计稿用了 Inter（409 次）/ Lexend（108）/ Playpen Sans（90），
  现在全部被 PP Palma 顶掉了。**这条归还原度审计线裁决**，本报告只提供「一个字节都没下」的证据。
- ➡ `Figtree` 是 `$font-brand-alt`，只在 PP Palma 加载失败时才下载 ——
  变体 H（把 PP Palma 的 url 打断）实测 `document.fonts` 变成 `Figtree:300 900 = loaded`，
  证明兜底链路通。**平时 0 字节，是一份免费的保险，别当成「多余的族」删掉。**

### 4.2 preload：0 个，而 3 个都够格

首屏（1440，viewport 900）实际用到的 family+weight 组合，逐页实测：

```
index / pdp / science / faq  →  ['PP Palma 400', 'PP Palma 500', 'PP Palma 800']
```

**三个文件全部是首屏关键路径**，总计 97.4 KB。它们现在的发现链是
`HTML → CSS(160 K) 下载并解析完 → 布局匹配字形 → 才发起字体请求`，
是典型的三跳。`<link rel="preload" as="font" type="font/woff2" crossorigin>` 能把这三跳压成一跳。

### 4.3 `font-display: swap` 的重排代价 —— 用替代判据量出来了

`file://` 下字体从本地磁盘秒回，first paint 之前就绪，**FOUT 根本不会发生**，
所以 §6 里实测的 CLS≈0 **不能拿来说「上线也没问题」**。
替代判据：把字体 URL 打断，比对「用 PP Palma 排版」与「用兜底栈排版」的几何差
（`perf_fontshift.py`，变体 I：PP Palma + Figtree 双双打断，`document.fonts` 空数组，存活性断言通过）。

| 页面 | 文档总高 | 位移 >1px 的文本块 | 单块最大位移 |
|---|---|---|---|
| index.html | 9471 → 9419（**-52px**） | **65 / 130** | **52.0px**（"30 Day Money Back Guar…"） |
| pdp.html | 8191 → 8169（-22px） | **56 / 86** | 34.0px（"Discount xx"） |
| science.html | 5662 → 5662（0） | 0 / 57 | 0 |
| faq.html | 3118 → 3118（0） | 0 / 25 | 0 |

结论：**长文案页（index / pdp）上线后一定会看到 swap 重排**，一半以上的文本块会跳；
短文案页（science / faq）因为标题都是单行 + 行高写死，一个像素都不动。
这不是「要不要 preload」的可选项，是 index/pdp 的实打实 CLS 来源。

### 4.4 建议

- **[P1]** 11 个 HTML 的 `<head>` 里加 3 条
  `<link rel="preload" as="font" type="font/woff2" crossorigin href="assets/fonts/pppalma-fizzy-{light,medium,heavy}.woff2?v=…">`。
  三个都是首屏必需，实测过，不是猜的。注意 **`crossorigin` 必须写**，漏了会下两遍。
- **[P2]** 若要进一步压掉 index/pdp 的 swap 重排，给 `@font-face` 补
  `size-adjust` / `ascent-override`（对齐兜底栈的度量）；但 **PP Palma 是临时字体**，
  客户给了授权文件后度量会变，**这一项建议压到拿到正式字体之后再做**，现在做等于白做。
- **[③ 需裁决]** Inter / Lexend / Playpen Sans 三族要不要真的用起来（稿里有 607 处），
  还是确认「全站统一 PP Palma」。定了之后：要用就补选择器，不用就把三组 `@font-face`
  连同 6 个 woff2 一起清掉（现在是纯死代码，但删之前必须有裁决）。
  ⚠ `pppalma-{light,medium,regular-interp,fizzy-regular-interp}` 与 `plus-jakarta-sans-*`
  是有意保留的备件（交接文档 6.3），**不在此列**。

---

## 5. `.wowo` 与 LCP —— 本轮最重要的实测

### 5.1 现象

11 页 × 2 宽度，`PerformanceObserver({type:'largest-contentful-paint', buffered:true})`：

| 页面 | FCP | 最终 LCP (1440) | 最终 LCP (390) | LCP 元素 |
|---|---:|---:|---:|---|
| index | 84 ms | **1588 ms** | 1576 ms | `H1.hero__title`（`index.html:106` 自带 `wowo fadeInUp`） |
| pdp | 40 | **1568** | 1556 | `H2.product__title`（祖先 `pdp.html:128` `.product__info wowo fadeInUp`） |
| science | 56 | **1572** | 1560 | `H1.page-hero__title`（祖先 `.page-hero__text wowo fadeInUp`） |
| reviews | 48 | 1568 | 1544 | 同上 |
| how-gumi-works | 40 | 1552 | 1552 | 同上 / 390 档是 `P.dosed__lead` |
| our-story | 44 | 1564 | 1548 | 同上 |
| faq | 40 | 1552 | 1548 | 同上 |
| get-in-touch | 48 | 1544 | 1540 | 同上 |
| referral | 48 | 1544 | 1544 | 同上 |
| privacy-policy | 32 | 1556 | 1552 | `P`（祖先 `.rich-text wowo fadeInUp`） |
| shipping | 40 | 1536 | 1560 | 同上 |

**每一页的 LCP 都 ≈ `domContentLoaded + 1500ms`，而 FCP 只有 32~84ms。**
1500 这个数字不是巧合 —— 它就是 `main.js:36-38` 里
`setTimeout(function(){ el.classList.remove("wowo","animated") }, 1500)` 的常数。

### 5.2 因果 A/B（带存活性断言，不是相关性）

`perf_lcp2.py`，5 个整站副本，每个在 t=300ms 先验条件成立再往下测：

| 变体 | 存活性断言（t=300ms） | index LCP | LCP 元素 |
|---|---|---:|---|
| **A** 原样 | 折线下 `.wowo` 的 computed opacity = **0** ✔ | **1580 ms** | `H1.hero__title` |
| **B** 只关透明门（`html .wowo{opacity:1}`） | 同一批元素 opacity = **1** ✔ | **72 ms** | `H1.hero__title` |
| **C** B + 关掉 `.float-art` / `.pop-word` 入场 | `.float-art` opacity = **1** ✔ | **64 ms** | **`IMG.hero__bear`（`gumi-bear-front-glow.png`，399,727 px²）** |
| **D** 直接把 `wowo` class 从 HTML 里删干净 | `document.querySelectorAll('.wowo').length = 0` ✔ | **84 ms** | `H1.hero__title` |
| **E** `main.js` 置空（"加载成功但什么都没干"） | `window.gumi = undefined` ✔ | 52 ms，但 LCP 元素退化成 **1580 px² 的「Shop now」按钮**；页面结束时 **30 个元素 opacity 仍为 0** | — |

pdp / science / faq 三页同样跑了全套，形态完全一致（A ≈ 1550ms，B/C/D 全部 ≤ 80ms）。

**判据说明**：B 和 D 是两条互相独立的路径（一条改 CSS、一条改 HTML），
结果一致 → 排除「只是某一种改法的副作用」。C 又在 B 的基础上多关一层，
LCP 从 72ms 微降到 64ms 但**元素换成了 hero 图** —— 说明第二层门（`.float-art` 的
`gm-art-in` 入场，`opacity:0` + `delay .5s` + `duration 1.5s`）挡住的是**真正的 LCP 元素**。

### 5.3 结论

1. **`.wowo{opacity:0}` 把 11 个页面的 LCP 从 ~70ms 推到 ~1550ms，代价 1.5 秒，约 20 倍。**
   机制：元素在 `.animated` 期间跑的是合成层上的 opacity 动画，主线程不重绘，
   Chrome 记不到新的 LCP 候选；直到 1500ms 那次 `classList.remove` 让元素**回到主线程重绘**，
   LCP 才被登记。所以缩短动画时长没用 —— 卡点是 class 移除那一刻。
2. **首页真正的 LCP 元素其实是 hero 熊图**（399,727 px² > H1 的 88,788 px²），
   被 `.float-art` 的入场动画一起挡掉了。上线到真实网络后，
   **768 KB 的 `gumi-bear-front-glow.png` 就是 LCP 资源** —— 这把 §2 的图片优化
   和 §4 的 preload 直接串成了同一条链。
3. **`<noscript>` 兜不住变体 E。** JS 加载成功但抛异常时，`<noscript>` 规则不生效，
   index 上 30 个元素永久 `opacity:0`，LCP 退化到一个 1580 px² 的按钮 ——
   即整个首屏文案都不可见。交接文档 §5「已知风险点」说的就是这个，
   本轮给出了**量化值**（index 30 / pdp 22 / science 17 / faq 3 个元素）。

### 5.4 建议

- **[P0] 首屏元素不要挂 `.wowo`。** 精确到 11 处，都在页面顶部：
  - `index.html:106` `<h1 class="hero__title wowo fadeInUp">`
  - `pdp.html:128` `<div class="product__info wowo fadeInUp delay-in-1">`
  - `science / reviews / how-gumi-works / our-story / faq / get-in-touch / referral` 的
    `<div class="page-hero__text wowo fadeInUp">`
  - `privacy-policy / shipping` 的 `<div class="rich-text wowo fadeInUp">`

  折线以下的入场动画**照留不误** —— 这次改动只针对第一屏。改完的判据：
  重跑 `perf_lcp2.py` 的 A 变体，LCP 应从 ~1550ms 落到 ~80ms；
  同时 `python3 tools/shoot.py --all` 必须仍是 55/55（首屏元素最终 opacity 回到 1）。
- **[P0] 同理，hero 图外层的 `.float-art--still` 入场也要让路**（或让它从 opacity:1 起步，
  只做 transform）。变体 C 实测这一步能让 LCP 元素回到 hero 图本身。
- **[P1] 给 `main.js` 每个模块套独立 `try/catch`**（现在是单 IIFE，任一模块抛异常
  后面全不初始化）。这条与 JS 审计线重叠，但从性能角度它决定 LCP 是 80ms 还是「永远不出现」。
- **[P2]** 更彻底的做法是让 `.wowo` 的隐藏由 JS 加类来实现（`html.js-on .wowo{opacity:0}`），
  这样 JS 挂掉时内容天然可见。但这会动到 Terra 移植过来的 1:1 契约，
  **需要用户拍板**（全局 CLAUDE.md 铁律 12 明确说这两份文件要照搬）。

---

## 6. 主线程 / CLS

### 6.1 JS 执行耗时与长任务（CDP `Performance.getMetrics`，1440）

| 页面 | ScriptDuration | LayoutDuration | RecalcStyle | LayoutCount | 长任务 (>50ms) | DOM 节点 |
|---|---:|---:|---:|---:|---:|---:|
| index | **9.1 ms** | 36.1 ms | 28.3 ms | 5 | **0** | 1209 |
| pdp | 2.6 | 14.9 | 9.9 | 4 | 0 | 842 |
| how-gumi-works | 3.0 | 12.9 | 10.1 | 4 | 0 | 536 |
| our-story | 3.1 | 12.6 | 10.7 | 4 | 0 | 488 |
| science | 1.9 | 12.6 | 9.6 | 3 | 0 | 691 |
| reviews | 2.1 | 12.7 | 11.6 | 3 | 0 | 423 |
| faq | 1.9 | 9.3 | 9.1 | 3 | 0 | 236 |
| get-in-touch | 1.8 | 14.0 | 9.5 | **21** | 0 | 214 |
| referral | 1.6 | 12.0 | 10.4 | **22** | 0 | 203 |
| privacy-policy | 1.7 | 12.4 | 7.4 | 3 | 0 | 211 |
| shipping | 1.5 | 10.8 | 10.3 | 3 | 0 | 247 |

**11 页 × 2 宽度，长任务总数 = 0。JS 执行 1.5~9.1ms。主线程不是瓶颈。**
（`get-in-touch` / `referral` 的 LayoutCount 21~22 明显高于其余的 3~5，
唯一区别是这两页有表单 / `<select>`；21 次布局在 12~14ms 内跑完，
**不构成问题，只是记一笔**，将来若这两页变卡先看这里。）

### 6.2 `wowo.run()` 的 forced synchronous layout —— 存在，但当前不值钱

`main.js:21-31` 的循环形态是
`getBoundingClientRect()` → `clientHeight` → **`classList.add("animated")`** → 下一个元素再读，
即经典的读写交替，每个元素都会强制一次同步布局。

同一元素集合上的 A/B（`perf_thrash.py`，各跑 7 次取中位数）：

| 页面 | 元素数 | interleaved（现在的写法） | batched（先全读再全写） | 倍数 |
|---|---:|---:|---:|---:|
| index | 200 | **12.20 ms** | 3.00 ms | **4.1×** |
| pdp | 200 | 5.70 ms | 1.80 ms | 3.2× |
| science | 145 | 4.60 ms | 1.50 ms | 3.1× |

**但真实规模下代价可以忽略**：整页滚到底的过程中，
index 一共调了 36 次 `run()`，累计 **3.6 ms**，`.wowo:not(.animated)` 的最大待处理数只有 **23**；
pdp 29 次 / 2.6 ms、science 21 次 / 1.7 ms。

- **[P2 · 记一笔，别急着改]** 这是个**不随规模扩展**的写法：现在 23 个元素 3.6ms，
  如果哪天某页 `.wowo` 上到 200 个，就是每帧 12ms（掉帧线以下但已经很难看）。
  改法只需把 `play()` 的调用挪到读循环之后（收集命中数组再统一 add）。
  ⚠ 但 `wowo` 是从 Terra 1:1 移植的，铁律 12 要求照搬 ——
  **要改得先跟用户确认是否接受与 Terra 版本产生分叉**。

### 6.3 CLS

| 页面 | CLS @1440 | CLS @390 | 源头 |
|---|---:|---:|---|
| index | 0.00005 | **0.01416** | `DIV.hero__cta`，t=57ms |
| pdp / reviews / how-gumi-works / our-story / faq / privacy-policy | 0.00005 | 0 | `DIV.header__actions` + 内联 svg，t≈40ms |
| science / get-in-touch / referral / shipping | 0 | 0 | — |

**全站 CLS 实测远低于 0.1 阈值，没有布局跳动问题。** 具体核过的三件事：

1. **交付 11 页的 84 个 `<img>` 全部带 `width`+`height` 属性**（`imgtags.json` 逐个解析）。
   交接文档 6.1 写的「81」是把 `font-check.html` 里 3 个模板字符串算进分母又漏算了几个，
   **实测是 84/84，一个不缺。**
2. **memory 里那个 `aspect-ratio` 陷阱不成立**：`style.css:135-136` 有全局
   `img { height: auto }`，探针读回来的每个 `<img>` 的 computed `aspect-ratio`
   都是 `auto <w> / <h>`（来自属性），**没有任何一条 CSS `aspect-ratio` 落在 `<img>` 上** ——
   13 处 `aspect-ratio` 全部挂在 `.page-hero__media` / `.product__image` / `.promo-art` 等**容器**上。
   这个坑已经被正确规避了。
3. **index @390 那 0.01416 是唯一一处真位移**，发生在 t=57ms、源头是 `.hero__cta`，
   与图片和字体都无关（那时字体已就绪）。值太小不必修，**但 §4.3 说明的 FOUT 重排
   在真实网络下会叠加上来** —— 上线后要重测。

---

## 7. `file://` 下测不出的项目

按要求单列。每条给出替代判据，**没有编造数字**。

| 测不出的 | 为什么 | 本轮用的替代判据 |
|---|---|---|
| **TTFB / 网络瀑布 / 传输体积** | `file://` 下 `performance.getEntriesByType('resource')` **恒为空数组**（11 页全测过，`resourceCount=0`） | 改用 `page.on("request")` 抓请求清单（能证明「下没下」「什么时候下」的先后），体积一律用**磁盘字节数**，并在表里标明是磁盘口径不是传输口径 |
| **`font-display: swap` 造成的 FOUT / 真实 CLS** | 字体从本地磁盘在 first paint 前就绪，swap 窗口为 0 | §4.3：打断字体 URL 后比对 130 个文本块的 y 坐标与文档总高，量出 index 65/130 块位移、最大 52px |
| **`rel="preload"` 的实际收益** | 本地磁盘读取 <5ms，三跳压成一跳看不出差别 | 只给「哪几个文件属于首屏关键路径」的实测结论（3 个，97.4 KB），收益留到有 HTTP 源之后测 |
| **压缩后的传输体积** | 没有 gzip/brotli 中间层 | 不做估算。本报告所有体积都是**未压缩磁盘字节**；WebP 已经是压缩格式，gzip 对它几乎无效，所以 §2 的图片结论**不受影响** |
| **GPU 合成 / 无限动画的真实帧成本** | snap chromium 无 GPU（SwiftShader 软件合成），帧率数据不可信 | 只给静态计数（index 68 个 `will-change` 元素、59 个 `.pop-word`、每页 2~3 个 5s 无限 `transform` 动画），**结论必须交真机复测** |
| **首屏 LCP 的绝对毫秒数** | 本机无网络延迟、无 GPU，绝对值必然乐观 | §5 的判据用的是**差值**（A 1580ms vs B 72ms）和**常数对齐**（LCP ≈ DCL+1500 = `main.js:38` 的 setTimeout），这两个都与机器无关 |
| **移动端真实触摸滚动的掉帧** | headless `mouse.wheel ≠ 真机触摸` | 未做，超出本线范围 |

---

## 8. 三类归档

### ① 真缺陷 / 真浪费（可以直接排期）

| 编号 | 位置 | 现象 | 判据 | 级别 |
|---|---|---|---|---|
| A-1 | `images/` 15 张 | 全 PNG，源 5.05 MB | 逐张转 WebP 实测 → 473 KB，alpha 误差 0，白底 PSNR 31.5~52.7 dB | **P0** |
| A-2 | 11 页首屏容器（`index.html:106`、`pdp.html:128`、7 页 `.page-hero__text`、2 页 `.rich-text`） | `.wowo` 把 LCP 推迟 ~1.5s | 5 变体 A/B 带存活性断言：1580ms → 72/64/84ms | **P0** |
| A-3 | `.nav-card__art`（11 页 `*.html:86`） | 面板关着仍下 312 KB | 变体 G 实测每页 -311 KB；变体 F 证明 `loading="lazy"` 对它无效 | **P0** |
| A-4 | 38 个无 loading 属性的 `<img>` | 首屏以下仍 eager | 变体 F 实测 index -661 KB | P1 |
| A-5 | `gumi-bear-front` 12.5× / `vs-bear-glow` 5.94× / `bear-scatter` 5.26~8.70× 超采样 | 1.76 MB 换来 96×96 / 202×156 / 76×94 的显示 | `naturalWidth` vs `getBoundingClientRect()` 双宽度取最大 | P1 |
| A-6 | 11 个 `<head>` | 3 个首屏关键字体 0 preload；index/pdp 会 FOUT 重排 | 首屏 family+weight 实测；变体 I 量出 65/130 块位移、52px | P1 |
| A-7 | `main.js` 单 IIFE 无错误边界 | 抛异常 → index 30 个元素永久不可见，`<noscript>` 不生效 | 变体 E 实测 | P1 |
| B-1 | `main.js:21-31` | forced sync layout（读写交替） | 同集合 A/B：3.1~4.1×，但真实规模只 3.6ms | P2 |
| B-2 | `_motion.scss` `.float-art` / `.pop-word` | `will-change` 永不释放 + 5s 无限动画 | index 68 个常驻合成层；**帧成本需真机验** | P2 |
| B-3 | `index.html:127` hero 图 | 反向问题：源 528px 对 439 CSS px，2× 屏发虚 | 倍率 1.20，是全站唯一一张欠采样 | P2 |

### ② 已知且有意为之 —— 本轮**没有**新证据推翻，不重复报

- mask 全部内联成 data URI（27.1 KB）：`file://` 下外链 mask 被 CORS 拦。**实测确认
  `scallop-box.png` 从未被请求过**，与文档一致，不建议改回 `url()`。
- `style.css` 163 K 未压缩、`main.js` 32 K 未压缩：静态阶段有意不压。
  **本报告不写任何压缩/合并/CDN/缓存头建议**（属 Shopify 阶段与平台侧）。
- 外部请求 0：11 页实测每页只有 `HTML + style.css + main.js + 3 woff2 + N 张 PNG`，
  **无第三方、无 CDN**，与文档一致。
- `pppalma-{light,medium,regular-interp,fizzy-regular-interp}`、`plus-jakarta-sans-*`：
  `$pp-400-src` 候选备件与第二备选，**有意保留**，本报告不建议删。
- `images/bear-gummy.png`：`bear-gummy-glow.png` 的生成源（`figma/optimize-images.py:41`），**保留**。
- `images/scallop-box.png`：已内联，**保留为源**。
- `diag-a-resave.woff2` / `diag-b-rewrite.woff2`（62 K）：文档已标「诊断残留可删」，
  实测确认从不请求，**维持文档结论，本轮不重复展开**。

**本轮实测与交接文档不一致的三处（以实测为准）：**

| 交接文档 6.1/6.2 写的 | 实测 |
|---|---|
| 「**5 个族**同时加载（PP Palma / Inter / Lexend / Playpen Sans / Figtree）」 | 每页只下 **3 个 PP Palma 文件 / 97.4 KB**；Inter / Lexend / Playpen Sans / Figtree **一个字节都没下**（`document.fonts` 全 `unloaded`），因为没有任何选择器引用它们 |
| 「`assets/fonts/` 13 个被引用」 | SCSS 里写了 `url()` 的是 13 个，但**真正被请求的只有 3 个**；另外 16 个（674 KB）从不出现在网络里 |
| 「`<img>` 总数 87 / 带 `width`+`height` 81」 | 87 含 `font-check.html` 里 3 个 JS 模板字符串；**交付 11 页是 84 个 `<img>`，84 个全部带 `width`+`height`** |

### ③ 需用户 / 设计方拍板

| 编号 | 事项 | 需要谁定 |
|---|---|---|
| C-1 | `images/bear-gummy-glow.png`（374 KB）**全站零引用**。它是 `optimize-images.py:41` 从 `bear-gummy.png` 生成的**成品**（不是中间件），说明当初有落地意图但没用上。交接文档只保了它的源，没提它本身。**只报告，未删。** | 设计方 / 用户：是漏做了某个区块，还是废弃了 |
| C-2 | Inter / Lexend / Playpen Sans 三族在稿里共 607 次用量，实现里 0 引用、0 下载。要用就补选择器（并顺带获得 preload 决策），不用就是 6 个 woff2 死代码 | 还原度审计线 + 设计方 |
| C-3 | `.wowo` 的隐藏改成「JS 加类才隐藏」能根除永久不可见风险，但会与 Terra 的 1:1 移植分叉（铁律 12） | 用户 |
| C-4 | `wowo.run()` 改成先读后写同样是与 Terra 分叉 | 用户 |
| C-5 | index 24 个 media logo 的 `loading="eager"` 是刻意的还是顺手写的？若是为了跑马灯测宽，需在 HTML 留注释 | 上一轮搭建会话 / 用户 |

---

## 9. 根目录两个临时文件（只报告，未删）

| 文件 | 尺寸 | 体积 | 判定 |
|---|---|---|---|
| `0e110e9b-1f14-4f2c-800f-2eca95554611.png` | 2285×1106，RGB（**无 alpha**） | 212 KB | 全仓 `grep` 只在 `docs/AUDIT-HANDOFF.md:390` 被提到「疑似临时截图」，**没有任何 HTML / CSS / JS / 脚本引用**。尺寸与色彩模式（无 alpha、非整数设计尺寸）都符合「屏幕截图」而非「设计资产」 |
| `1e4ea5b2-aa92-4e60-a9d4-36359d880baf.png` | 1530×1132，RGB（**无 alpha**） | 127 KB | 同上 |

两者合计 339 KB，**确认不属于项目交付物**。它们在根目录而不是 `images/`，
既不会被页面加载也不会进 Shopify 主题，**对性能零影响**；
但如果将来用 `rsync` 整目录同步会被带上。**处置等用户指令。**

---

## 10. 一句话

主线程和 CLS 都没问题（长任务 0、CLS ≤0.014）；
所有可拿的收益都在**三处**：图片源体积（5.05 MB → 473 KB，-91%）、
`.wowo` 挡住 LCP（1.55s → 0.07s）、以及导航面板那张关着也下的 312 KB 小熊（×11 页）。
字体一共只有 3 个文件 97.4 KB，加 preload 即可，
但**上线后 index/pdp 会出现 swap 重排（65/130 块、最大 52px）**，这条在 `file://` 下永远看不到。

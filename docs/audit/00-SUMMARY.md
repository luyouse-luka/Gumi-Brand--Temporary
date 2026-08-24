# Gumi Brand — 四线审计总报告（构建 r15，2026-08-20）

> 四条线并行跑完：**还原度 / CSS / JS / 性能**，外加铁律 13 要求的**交互态全量清点**。
> 本文件只做汇总与排序，**证据和判据在各条线的详报里**，不在这里重复。
>
> ⚠ **本轮只出报告，未改任何项目文件**（`assets/` / `*.html` / `images/` 全部未动，
> `style.css` 与源码 md5 与审计前一致）。修复等用户明确指令。

## 报告清单

| 文件 | 线 | 范围 |
|---|---|---|
| [`01-fidelity-cross-page.md`](01-fidelity-cross-page.md) | 还原度 | **跨页系统性偏差**（主会话）12 条 |
| [`01-fidelity-a-index.md`](01-fidelity-a-index.md) | 还原度 | Homepage 1440/390，23 条 |
| [`01-fidelity-b-pdp-science.md`](01-fidelity-b-pdp-science.md) | 还原度 | PDP / Science，18 条 |
| [`01-fidelity-c-reviews-hgw-story.md`](01-fidelity-c-reviews-hgw-story.md) | 还原度 | Reviews / How Gumi Works / Our Story，14 条 |
| [`01-fidelity-d-text-pages.md`](01-fidelity-d-text-pages.md) | 还原度 | FAQ / Get in Touch / Referral / Privacy / Shipping，28 条 |
| [`02-css.md`](02-css.md) | CSS | 17 条 + **交互态全量清点** |
| [`03-js.md`](03-js.md) | JS | 18 条 + **爆炸半径表** |
| [`04-performance.md`](04-performance.md) | 性能 | 11 条 + 3 条待确认 |

---

## 0. 一句话结论

**骨架是好的，问题集中在三处**：① 入场动画的失败模式（既是 P0 缺陷，也是 LCP 慢 1.5 秒的唯一原因）、
② 手机端大量模块只写了桌面值（偏差密度是桌面的 5.9 倍）、③ 图片源体积（5.05 MB 可压到 473 KB）。

桌面端还原度**很扎实** —— 110 个按钮实例桌面端 0 处几何偏差，区块高度逐像素级吻合，
21 组比对里桌面 token 偏差只有 38 条。**没有发现自造内容**（五组独立核查，全部通过）。

---

## 1. 建议的修复顺序

按「改动成本 ÷ 影响面」排的，前四条是上线阻断级。

| # | 事项 | 出处 | 为什么排这里 |
|---|---|---|---|
| 1 | **wowo 的 rAF `ticking` 闩锁加 `try/finally`**（`main.js:43-52`） | JS P0-2 | 一行代码。现在只要 `run()` 抛一次异常，闩锁永远锁死，实测 22/27 元素永久不可见 |
| 2 | **`.wowo{opacity:0}` 改成 `html.js` 门控** | JS P0-1 / 性能 A-7 | 同一处改动同时消掉两个 P0：JS 抛异常时内容永久不可见、`<noscript>` 挡不住这种情况 |
| 3 | **首屏 11 处容器不参与 wowo 的透明门** | 性能 A-2 | LCP 从 1.55s → 0.07s。现在 11 页的 LCP 一律卡在 DCL+1500ms，而 FCP 只有 32~84ms |
| 4 | **删掉两处会真印在页面上的开发占位** | 还原度 A / B | `Subscription options load here.` / `Customer reviews load here.` —— 交付前必须换成空壳或真 app 挂载点 |
| 5 | **`.highlight-card__lip` 波浪吃掉图片**（`_nutrition.scss:66`） | 还原度 A P0 | 波浪吃进图片 93.6px（稿 29.8px），还露出圆的下半弧成"双层波浪"，两断点都中 |
| 6 | **三条 `.scallop--lg` 的弧向反了** + **手机 CTA 扇贝板弧数 14 vs 稿 5** | 还原度 A P1 / 跨页 F7 | 扇贝是品牌标志图形。半径/节距都对，只有凹凸方向与手机断点的节距错 |
| 7 | **Privacy 正文首段丢失**（`privacy-policy.html:118`） | 还原度 D P1-5 | 漏了稿里 568 字符的首段，还把页头副标 `Subheading` 重复进正文 —— 违铁律 3 |
| 8 | **手机端"只写了桌面值"的一批模块** | 跨页 F2/F3/F4/F5 | 页脚字号、四个文本页的页头副标、CTA 按钮高度、满宽按钮 —— 一次性按手机稿补 mobile 块 |
| 9 | **图片：WebP + 补 lazy + 关掉导航面板里的图** | 性能 A-1/A-3/A-4/A-5 | -4.6 MB（-91%），index 首屏再 -661 KB，每页再 -312 KB |
| 10 | **13 个 `data-modal` 触发器指向不存在的弹窗** | JS P1-4 | our-story 6 / how-gumi-works 6 / reviews 1，点了完全没反应且不报错 |

---

## 2. 四条线各自的重点

### 2.1 还原度（95 条真偏差：P0×1 / P1×38 / P2×56）

**桌面 vs 手机是本轮最强的信号**：21 组比对里桌面 token 偏差 38 条、手机 223 条，**5.9 倍**。
且几乎全是同一种形态 —— *模块只写了桌面值、没写 `@include mobile` 块*：

- 页脚整块（11 页 × 10 条链接 + 版权行）字号大一档
- `.product__cta` / `.product__label-btn` / 表单提交按钮高 60（稿 52）、字号 18（稿 16）
- 稿里手机端设成 FILL（满宽）的按钮，实现仍按内容宽收缩
- 小熊填充条没按手机稿缩放，5×20 变成六行（B 组）
- Our Story 手机 CTA 板整体缩水 219px（C 组）

**跨页共用组件**里另有四处：全局字距 `-0.32px` 铺到了稿中字距为 0 的 71 处文字、
四个文本页误用了 Reviews 的页头副标变体、白底页面多出一条薄荷色带、手机端 header 图标顺序颠倒。

**内容完整性**：五组独立核查，**没有自造内容**。占位（Grüns 竞品名、美国配送口径、lorem ipsum、
`Text here`、`Accordion Closed`）全部原样保留 —— 这是对的，但**上线前必须由客户替换**。

**新发现 26 条桌面/手机稿互相冲突**，不在 AUDIT-HANDOFF 3.4-C 已登记的四条里，需设计方裁决。
其中最值得先问的：**两个手机稿（Privacy / Shipping）用的是另一版页脚组件**（16px/600/ls 0），
与其余 9 稿不一致 —— 不先定这个，修页脚会把这两页改得更远。

### 2.2 CSS（17 条）+ 交互态清点

- **P1-1**：`_cta-band.scss:34-35` / `_expert.scss:106-107` 把同一串 base64 各展开了两遍，
  产物里白扔 **11.6 KB**（我实测；CSS 报告按含属性前缀口径记 12.9 KB，同一处，修法一致）。
  仓库里 `_scallop-box.scss:23` 已有 `--box-mask` + `var()` 的正确写法，照抄即可，不违反"mask 必须内联"。
- **P1-2**：`.promo-card--white` 的手机 `gap` 被作用域选择器压掉，**写了不生效**（Playwright 实测）。
- **交互态清点结论（11 页 × 2 断点，2102 条记录、真鼠标到达 1368 次）**：
  `a` / `button` / `summary` **0 处**缺 hover；`:hover` **41/41 全部包在 `@media (hover:hover)` 内**，
  0 条裸写。**铁律 13 在链接与按钮上执行得很好。**
  漏的是表单侧 3 类：两个 `appearance:none` 的 `<select>` 和包 checkbox 的 `label.form__check`
  （后者连 `cursor:pointer` 都没有），以及 1 处有 hover 无过渡（`_product.scss:283` 的 `trans()` 漏了 `color`）。
- 三处 `prefers-reduced-motion` 块是**死代码**（被 reset 的 `!important` 压过）。

### 2.3 JS（18 条）

两条 P0 都指向同一个机制：**`.wowo{opacity:0}` 是无条件的，而它的复位链路没有兜底**。

**爆炸半径表推翻了交接文档的因果链**：`wowo.init()` 排在第一个且先注册监听，所以模块 2~8 任一抛异常，
`.wowo` 都照常回到 1（7 组实测 27/27）。"无错误边界 → 整页永久不可见"**不成立** ——
它的真实后果是"后半段功能静默消失"。永久不可见的入口只有 P0-1、P0-2 两条。

另有 6 条 P1/P2 值得先修：resize 把 reels 轨道甩回居中（移动端地址栏收放必触发）、
`fill()` 克隆无上界（零宽 slide 实测造出 4281 个节点）、双弹窗留下关不掉的遮罩、
`e.target.closest` 无守卫、popText 的 catch 摘掉了 CSS 兜底依赖的属性、跨断点后桌面端挂一块 259px 空面板。

### 2.4 性能（11 条）

- **图片是大头**：15 张在用 PNG 共 5.05 MB → WebP 473 KB（**-91%**，alpha 误差 0）。
  三张是严重超采样：`gumi-bear-front.png` 828 KB 只显示 96×96（**12.5×**）、`vs-bear-glow.png` 5.94×。
- **LCP 被 `.wowo` 挡住 1.5 秒**：11 页 × 2 宽度，LCP 一律落在 DCL+~1500ms（1500 就是 `main.js:38` 的常数），
  而 FCP 只有 32~84ms。5 个整站副本做 A/B 且每个都先跑存活性断言，两条独立路径互证。
- **`nav-card-bear.png` 312 KB 每页白下**：导航面板 `0fr` 折叠但图仍有 261×315 的盒，`loading` 对它无效。
  （补一句：它的源 523×631 对显示 261×315 正好是 2×，**尺寸本身是对的**，问题是"关着也下"。）
- 三处对交接文档的更正：字体**不是"5 族同时加载"**，实际只下 3 个 PP Palma 文件 97.4 KB；
  交付页是 84 个 `<img>` 且**全部**带 width+height；`img{height:auto}` 已规避 aspect-ratio 陷阱，CLS ≤0.014。
- 两张废弃图 `bear-gummy.png` + `bear-gummy-glow.png` 合计 **767 KB，HTML/CSS 引用均为 0**
  （主会话复核）。交接文档 6.3 只说了前者是后者的生成源，没说后者也没人用 —— **需确认是废弃资产还是漏接的图**。

---

## 3. 主会话独立复核过的条目

子会话的发现里，这几条主会话用自己的探针重跑过，**判据独立、结论一致**：

| 条目 | 复核方式 | 结果 |
|---|---|---|
| 55/55 回归基线 | 独立探针（不写截图，避免干扰正在读对照图的子会话） | ✅ 11 页 × 5 宽度全绿 |
| 13 个死的 `data-modal` 触发器 | grep 触发器 vs 弹窗容器 | ✅ our-story/how-gumi-works 有触发器无容器 |
| `.testimonial` 的 flex-basis 变成卡高 | Playwright 量卡高 vs 内容高 | ✅ @1024 空 80px / @768 空 116px / @390 空 92px |
| 手机 header 图标顺序颠倒 | 上下对照图 | ✅ 稿"袋→人"，实现"人→袋"；桌面两边都对 |
| 白底页面多一条薄荷色带 | FAQ@1440 竖切采样 + 整行取样 | ✅ 稿白→lime 直连，实现插 9px `#e7f8d0`（整行 24 处） |
| `.scallop--lg` 弧向反了 | 上缘剖面的上下半列数比 | ✅ 稿 935:317（上/下 2.95），实现 462:978（0.47） |
| PDP 多出 3 张 testimonial 卡 | `dom_only` 求差 | ✅ 三段文字不在任何可见节点里 |
| Privacy 正文首段丢失 | 节点 y=622 的 18px 段落 vs HTML | ✅ 实现那一行是 `<p>Subheading</p>` |
| 产物里 base64 重复 | 直接扫 `style.css` 的 data URI | ✅ 3 处 2 个唯一，重复多占 11.6 KB（7.1%） |
| 两张废弃图零引用 | grep HTML + CSS | ✅ 767 KB 无人引用 |
| 三个字体族无人使用 | grep 选择器 + 扫 42 个 frame 的 TEXT | ✅ Inter 只用于稿顶的浏览器地址栏模拟，Lexend 只在一块生鲜 App 参考稿里，Playpen Sans 0 次 |

**注意一处容易读混的**：Homepage hero 下方那条 `.scallop` 波形**是对的**（剖面偏差 3~8px），
弧向反的是 `.scallop--lg` 那三条 —— 两者不是同一个东西，别一起改。

---

## 4. 需要别人拍板的（挡住修复的）

### 4.1 需设计方裁决

1. **两个手机稿（Privacy `326:83399` / Shipping `326:83129`）的页脚是另一版组件**（16/24/600/ls 0），
   其余 9 稿是 14/20/400/-0.28。**先定这条，才能修页脚。**
2. 各组新发现的 **26 条桌面/手机稿冲突**（A 8 / B 7 / C 4 / D 7），清单在各自报告里。
3. 稿里 20 处 `#ff3b30` / `#ff2d55` 红色文字（不在品牌色板内，全落在占位内容上）——
   判断是"待定标记"还是真要红色。
4. 交互态（hover / active / focus ring）、手风琴与 tab 的展开态图标、PDP sticky 偏移、
   弹窗开合时长 —— 稿里全没有，现在都是自定值（AUDIT-HANDOFF 3.4-F）。

### 4.2 需客户提供

1. **PP Palma 授权 web font**。现在 400 字重（全站 59% 用量）用的是 300 的文件，
   **字宽/字距/换行与稿的偏差不可消除**，像素级验收要等这个。切换点仍只有 `_fonts.scss` 一处。
2. 三处占位文案：Reviews 专家卡的竞品名 `Grüns`、Shipping 的美国配送口径、Privacy 的 lorem ipsum。
3. Get in Touch 的 Enquiry Type 最终列表。

---

## 5. 基线数字（r15，供下一轮对照）

| 指标 | 值 |
|---|---|
| 回归 | 11 页 × 5 宽度 **55/55 绿**（横向溢出 0、卡住的 `.wowo` 0） |
| 稿侧可见 TEXT / 渲染文本 / 成功配对 | 1915 / 1969 / 1301 |
| token 偏差 | 桌面 **38**，手机 **223**（5.9 倍） |
| 按钮实例（稿↔实现可配） | 110，偏差 15 —— **全部在 390** |
| `!important` / `z-index` / `@media` | 3 / 14 / 317 |
| `:hover` / `transition` | 41 / 53，`:hover` **41/41** 在 `@media (hover:hover)` 内 |
| `style.css` | 163,351 B（其中重复 base64 11,566 B = 7.1%） |
| `main.js` | 636 行，零依赖 |
| `images/` 在用 PNG | 15 张 / 5.05 MB → WebP 473 KB |
| LCP（11 页 × 2 宽度） | 1536~1588 ms（FCP 32~84 ms） |
| CLS | ≤ 0.014 |

**下一轮的回归判据建议**：把"每个 `@include mobile` 块里的字号集合 vs 手机稿字号集合"做成脚本判据 ——
本轮 223 条手机偏差里绝大多数都能被这一条抓住。审计用的比对脚本在
`/tmp/claude-1007/-home-ly/c7ffb540-53f6-4bbe-87d6-fe452694dbc5/scratchpad/`
（`fig_text.py` / `batch_dom.py` / `compare2.py` / `crop_pair.py` / `btn_all.py` / `regress.py`），
要长期用就挪进 `tools/`。

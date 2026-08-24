# Gumi Brand — 项目状态

> 建档 2026-08-19。本文件记录项目定位、约定与进度；设计节点清单见 [FIGMA-NODES.md](FIGMA-NODES.md)。
>
> 🔍 **要做审计（还原度 / CSS / JS / 性能）的会话，读 [AUDIT-HANDOFF.md](AUDIT-HANDOFF.md)** ——
> 那份文档专为审计写，含「不要报成 bug 的清单」与探针陷阱，能省掉大半误报。

## 项目定位

Shopify 前端项目（Gumi Brand 官网 + 商品页）。设计交付源为 Figma
`Internal - Gumi Brand & Website` 的 SECTION `401:31719`「Desktop & Mobile MVP (14/08/26)」，
位于 **🟢 READY FOR DEV** 分组下。

**当前阶段：11 个静态页全部落地，四线审计的上线阻断级问题已修完**（Homepage / PDP / Science / Reviews / How Gumi Works /
Our Story / FAQ / Get in Touch / Referral / Privacy Policy / Shipping），
每页 5 个宽度（390/768/1024/1440/1920）无横向溢出、无卡住的入场动画。
改动记录见 [CHANGELOG.md](CHANGELOG.md)。

验证脚本 `tools/shoot.py`（全页截图 + 溢出 + 卡住的 `.wowo`），`python3 tools/shoot.py --all`。
新页面外壳由 `figma/new-page.py` 从 index.html 现切现拼，`--resync` 可把 header 改动推给所有页。
长文案一律用 `figma/dump-text.py` 从节点取全文 —— `build.txt` 会把长字符串截断成省略号。

⚠ **两端要同步做**：手机稿（390）不是桌面稿的等比缩小，数值必须各取各的。第四轮抽查发现
Homepage 有 3 处 mobile 字号是凭手感缩的（已修）。判据是把每个 `@include mobile` 块里的
字号与手机稿实际字号集合对一遍 —— 不在集合里的就是编的。

⚠ **交互态要一起做**（CLAUDE.md 铁律 13）：可点击的地方都要有 hover，状态变化都要走
`transition`。这类要求**既不在 Figma 稿里也不在 build spec 里，没人提就一定漏** —— 第五轮
清点时 19 类可点击元素只有 9 类写了 hover、其中 7 类还没过渡。时长与曲线统一在
`_variables.scss` 的 motion 段（`$t-base` / `$ease-out`），hover 一律用 `@include hover`
包 `@media (hover: hover)`，否则触摸屏点完 hover 态会粘住。
判据是 Playwright 遍历所有 `a[href]` 与 `button`，比对 hover 前后的 computed style。

## 待用户确认的事项

### 开工前必须定的
1. **店铺与主题** — Shopify 店铺域名、主题基底（Dawn？既有主题？）、是否已有 dev 主题
2. **实现形态** — 直接写 Shopify 主题（sections/snippets/liquid），还是先出静态 HTML 再套主题
3. **接入方式** — Shopify CLI（本机需走 device code 流，见 memory `shopify-cli-headless-device-code`）/ GitHub 集成 / 手工上传
4. **PP Palma 授权文件** — 三个免费字体（Inter / Lexend / Playpen Sans）已下载到位；
   **PP Palma 是 Pangram Pangram 商业字体，试用包 EULA 明确排除商业用途**。
   ⚠ **第六轮起已接入试用包**（Figtree 退为 `$font-brand-alt` 兜底，不再是主字体）：
   300/500/800 用包内 Fizzy 三个原件；**400（全站 59% 用量）试用包不提供**，
   第十一轮起指向 `fizzy-light`，即 **400 与 300 同款、正文比稿轻一个字重档**
   （插值件在客户浏览器上渲染成 last-resort monospace，已弃用；详见 CHANGELOG 第十一轮）。
   **需要客户提供授权 web font 文件**才能做像素级还原验收，切换点只有 `_fonts.scss` 一处。

### 需要设计方给数值的
- **交互态（hover / active）稿里完全没有** — 现有的抬起量（1px 按钮 / 4px 卡片）、投影、
  时长（.15 / .2 / .3s）与曲线（easeOutCubic）都是自定值，集中在 `_variables.scss` 的
  motion 段，要调改那一组即可。
- ~~手风琴与 tab 的**展开态图标**该变成什么形态~~ — 稿里仍然没有，但需求方 2026-08-24
  在任务文档里指定了：**加号的竖线旋转成横线**（即减号），且不用 SVG、用 CSS 画。已落地。
- tab（营养标签弹窗的两个页签）的选中态仍是自定值。

### 设计方在等回复的（见 HANDOVER-NOTES.md 第三节）
5. ~~**header 返工问题**~~ — 已给建议（header 独立 section + 原生 linklist + schema 设置位），**用户指示暂时搁置**
6. ~~**STATISTICS 小熊图形**~~ — ✅ **2026-08-19 已定：用代码动态表示**（按输入的百分比高亮/填充小熊图形，不用静态图）
7. ~~**PDP 占位图标格式**~~ — **用户指示暂时忽略**，等需要落地时再问设计方

### 桌面稿与手机稿对不上的地方（第十二轮发现，**需设计方裁决**）

四处两稿冲突，一律取信息量更大的一版，没有自造内容：

| 位置 | 桌面稿 | 手机稿 | 现在的做法 |
|---|---|---|---|
| Science 三张 stat 卡 | 三张同一句占位 | 三段各不相同的真文案 | 用手机的文案；数值仍取 95%（桌面 + homepage 一致，手机的 50% 判为占位残留） |
| Science 成分区收尾 | 「Shop Now」按钮，标题 Heading | 四行手风琴，标题 Just the necessities | 两套都做，按断点切换 |
| Science nutrient 卡 | 3 张 | 4 张 | 做 3 张，不造第 4 张 |
| How Gumi Works 副标 | This is a placeholder subheading. | 真文案，且是珊瑚红 #dd655e | 文案用手机的，颜色各按各稿 |

### 第十四轮新增的待决事项

- **`gumi-bear-front-glow.png` 是首页 LCP 图，源只有 528px 宽**（对 439 CSS px 是 1.20×，
  2× 屏上会发虚）。**需向设计方索取更高分辨率的源**，放大现有文件解决不了。
- **`bear-gummy-glow.png`（767 KB）全站零引用** —— 是废弃资产还是漏接的图？未删，待确认。
- **手机稿里没有白色 promo 卡**，它的手机 `gap` 取 12 还是 24 需设计方定（现按 12）。
- **Privacy / Shipping 两个手机稿的页脚是另一版组件**（16/24/600/ls 0），与其余 9 稿冲突。
  本轮按 9 稿的 14/20 做，**先定这条才能继续动页脚**。
- index 的 24 个 media logo 仍是 `loading="eager"`：怀疑跑马灯靠它测宽，改前要先确认。

### 交付前必须替换的占位内容

- **Reviews 专家卡的引用文案里有竞品名**：三张卡都写着「Grüns has everything I need…」，
  Grüns 是另一个软糖品牌，设计师直接抄了参考站文案。原样保留在 HTML 里并加了注释，
  **上线前必须换掉**。
- **Shipping 全页文案写的是美国配送**（Alaska、Hawaii、US Territories、$65 门槛），
  而 Gumi 是澳洲品牌。同样是设计稿的占位。
- **Privacy Policy 正文全是 lorem ipsum**。
- Get in Touch 的 **Enquiry Type 选项列表**稿里只给了「Contact Us」一个。现在的四项
  对应 header/footer 指向本页的四个链接（Partners & Influencers / Press Inquiries /
  Careers / Contact），并支持 `?type=` 预填（批注要求照搬 Funky 的做法）。需客户确认最终列表。

### 落地前需向设计方确认的
0. **手风琴展开动画只在 Chrome 系有**（`::details-content` + `interpolate-size`）。
   改成原生 `<details>` 是为了让开合不依赖 JS；Firefox / Safari 现在是瞬开瞬收。
8. **Shipping 桌面稿缺失** — 只有手机稿，**已按 Privacy Policy 的文本页布局实现**，需确认
9. **PDP 产品图 sticky 的吸顶偏移量** — 批注只说要 sticky，没给数值，现用 `top: 24px`
10. **营养标签弹窗开合时长**（0.4s）与曲线 — 稿中没有，是自定值（第三轮遗留）
11. **平板（576–1280）没有设计稿**（第十六轮）—— 需求方 2026-08-21 把断点定成
    手机 ≤575 / 平板 576–1280 / PC ≥1281，但 Figma 只有 390 与 1440 两张板。
    这一档现在所有数值都是两张稿之间的**线性插值**（`fluid()`，576 处等于手机值、
    1281 处等于桌面值），`nutrition__band` 的四个量取的是中点。
    栅格按需求做成 3→2→1，两列的阈值是按列宽算出来的（science 744 / nutrition 704）。
    设计方若出平板稿，改的是插值的两个锚点，不用重排布局。

## 已确立的规范（来自全局 CLAUDE.md + 既有 Shopify 项目）

### 项目文件结构（2026-08-19 用户指定，2026-08-21 第十五轮改为扁平）

```
Gumi-Brand/
├── *.html              # 页面文件放根目录（index.html / pdp.html / …）
├── assets/             # ⚠ 扁平，不建任何子目录（Shopify 主题 assets 的硬约束）
│   ├── customstyle.scss   # 样式源码，全站唯一一份
│   ├── customstyle.css    # 编译产物，勿手改
│   ├── main.js
│   ├── *.woff2            # 19 个：PP Palma / Figtree / Inter / Lexend / Playpen Sans
│   └── *.svg              # 44 个图标
├── images/             # ⚠ 图片在顶层，与 assets 平级（不是 assets/images）
├── figma/              # 设计源，只读，不进交付
├── tools/              # 验证脚本（cssnap / rwd / sect / shoot / webp），不进交付
└── docs/               # 项目文档，不进交付
```

⚠ **`assets/` 内不许建子目录**（2026-08-21 用户指定）。Shopify 主题的 `assets/`
本身就不接受子目录，现在的结构可以原样搬过去。

⚠ 与 Terra / EuroCave 的既往约定**有一处不同**：那两个项目图片在 `assets/images/`，
本项目图片提到**顶层 `images/`**。写路径时别顺手抄旧项目。
（上 Shopify 主题时 `images/` 也得进 `assets/`，届时一并处理。）

⚠ 样式**只有 `assets/customstyle.scss` 一个源文件**（原 7-1 的 36 个 partial 已合并）。
文件分「定义」「输出」两段，改之前先看文件头那段说明 —— 块的相对顺序是层叠依赖，
别随手挪动。编译：

```
npx sass@1.77.8 assets/customstyle.scss assets/customstyle.css --no-source-map
```

### 数值来源
- 所有数值 token（font-size / line-height / letter-spacing / 颜色 / padding / gap / radius / shadow）
  一律取 Figma 节点数据。截图只用于判断「有没有、谁在谁上面」。
- TEXT 节点必查 `characterStyleOverrides`；某视觉效果常由同层兄弟节点实现。

### 内容真实性
- 文本忠实设计源，占位保留占位或标 `TODO 待客户文案`，不编造。
- 图片一卡一图，不复用同一张冒充多张。

### 断点体系（2026-08-21 第十六轮定，改之前先读完这一节）

断点分成**两组**，别混着用：

| 组 | mixin | 范围 | 管什么 |
|---|---|---|---|
| 系统三档 | `@include mobile` | ≤575 | 手机。数值一律取手机稿 390 |
| | `@include tablet` | 576–1280 | 平板。没有稿，数值靠 `fluid()` 在两张稿间插值 |
| | `@include pc` | ≥1281 | PC。桌面稿 1440 的值本来就写在基础规则里 |
| 布局阈值 | `@include tight` | ≤1200 | 版心开始吃紧 |
| | `@include stack` | ≤1024 | 稿里的两栏并排放不下，改上下堆叠 |
| | `@include narrow` | ≤768 | 手机版排布 |

⚠ **布局阈值不要去对齐 575/1280**。一台 1194 宽的平板放得下稿里的两栏，硬堆成一列是把
好排版改坏；第十六轮第一版就是把 ≤1024/≤1200 全推到 1280，结果 1025–1280 从两栏变单列，
那是**改制引入的回归**。这三个阈值是既有的、验证过的，原样保留。

⚠ 平板数值一律写 `fluid($手机值, $桌面值)`，别拍脑袋填中间数。
`fluid()` 的斜率**必须无单位** —— 写成 `26px * (100vw - 576px)` 是 px×px，量纲错了，
整条声明会被静默丢弃，表现是「字号原地不动、padding 掉回 0」而 DevTools 里那行看着完全正常。

⚠ 改完**必须实测**跨宽度的计算值，不能看截图目测 —— 上面那个量纲错误就是目测判成
「已生效」、实测才抓出来的。判据脚本见下方「验证工具」。

### 类名前缀（2026-08-21 第十六轮定）

所有模块类都带 `gb-` 前缀（`.gb-hero` / `.gb-product__stage` / `.gb-btn` …），
为的是上 Shopify 主题后不跟主题自带样式和 app 注入的样式撞名。

**不带前缀的只有两类**，新增时照此办：
- 动效工具类：`wowo` / `animated` / `fadeIn*` / `zoomIn` / `zoomOut` / `bounceIn` / `delay-in-N`
  （main.js 与 Terra 的 wowo 约定挂在这些名字上）
- 状态类：`is-*` / `no-js` / `js`

### 验证工具（tools/，不进交付）

| 脚本 | 用途 | 什么时候必须跑 |
|---|---|---|
| `cssnap.py` | 全站 computed-style 快照 + diff（含伪元素，390/1440 两档） | **改选择器名、搬 @media、合并文件** —— 这类改动 diff 产物无效，只能比计算值 |
| `rwd.py` | 11 页 × 10 档宽度：横向溢出 + 文字被祖先裁切 + **可滚容器是否登记给 Lenis** | 每动一次响应式；**每新增一个 `overflow-y:auto` 的容器** |
| `shoot.py --all` | 同上 + 全页截图 + 卡住的 `.wowo` | 收尾 |
| `sect.py` | 按区块截图（整页一万像素高看不动） | 要人眼看某个模块时 |
| `r19check.py` | 第十九轮 7 条任务的专项判据（弹窗时长 / 手风琴死区 / 图标 / 焦点 / 吸顶 / 弧 / 波浪色） | 动这七处中任意一处之后 |
| `r20check.py` | 第二十轮 8 条的专项判据（hero 按钮 / 星条 / 光晕尺寸 / logo 槽位 / 弧度 / 加号 / 箭头 / stats 波浪），全部与 Figma 数值比 | 动这八处中任意一处之后 |
| `make-hero-glow.py` | 按稿重建 `images/gumi-bear-front-glow.png`（glow 是稿里一条 26.2137 的 CENTER 描边，不是照片自带的） | 换 hero 熊照片、或要改光圈粗细 / 采样率时 |

用法：`python3 tools/cssnap.py before` → 改 → `python3 tools/cssnap.py after`
→ `python3 tools/cssnap.py diff before after`。
⚠ 快照前会把 `Math.random` 钉死 —— 不钉的话 word-pop / float-art 的抖动会让同一份 CSS
连采两次就有 260+ 处「差异」，真信号全被埋掉。

### CSS / 改动纪律
- 改样式前先定位真正胜出的规则（特异性 + 加载顺序），在原位就地改，不往文件末尾堆覆盖。
- 若主题存在 SCSS 源 → CSS 产物的构建链，**必须双写**或走差分移植，绝不全量重编译
  （funkyfood 的 `custom-style.css` 与 global-cke 的 `style.css` 都因此漂移过）。
- 响应式「拥挤」默认收窄 gap / padding 保持原布局，不重构；只有用户明确说改布局才动结构。

### 推送纪律（Shopify 多方共用环境）
- 改完只汇报「改了什么 + 怎么验证」，**等用户明确说推送才执行**。
- 一律 `--only <file>` 逐个列出 + `--nodelete`，**绝不裸跑 `shopify theme push`**（= 全量覆盖）。
- 推送前必做线上快照三方对比，有交集就停下人工处理。
- `config/settings_data.json` 由主题编辑器托管，非必要不推。

### Liquid 转义
- `<script>` 内用 `{{ value | json }}`；`onclick` 属性用 `{{ value | json | escape }}`；HTML 属性用 `{{ value | escape }}`。
- `<script>` 块里写 `| json | escape` 会双重编码损坏数据。

### 平滑滚动（2026-08-21 第十七轮定）

用 **Lenis 1.3.11**（MIT），vendored 在 `assets/lenis.min.js`，无构建步骤。
驱动代码是 `assets/main.js` 的 `smoothScroll` 模块。

- **`html { scroll-behavior }` 必须保持 `auto`**。Lenis 内部靠 `window.scrollTo` 落位，
  而按 CSSOM-View，`scrollTo` 是按元素自己的 `scroll-behavior` 执行的 —— 写 `smooth`
  就成了两层平滑套在一起，页面会飘会拖尾。
  老教程里那条 `.lenis.lenis-smooth { scroll-behavior: auto !important }` **自 Lenis 1.3
  起已失效**（不再输出 `lenis-smooth` 类），指望不上。
- **每新增一个 `overflow-y: auto` 的容器，就要登记进 `smoothScroll.PREVENT`**，
  否则 Lenis 把滚轮全吃掉、那个容器再也滚不动。现有三个：
  `.gb-product__thumbs`（只在桌面可滚）/ `.gb-header__panel`（只在手机可滚）/
  `.gb-nl-panel__body`。`tools/rwd.py` 逐视口盯这条 —— **单一视口验不全**。
- 触摸不接管（`syncTouch: false`），真机原生惯性比任何模拟都好。
- 两条关闭路径：`prefers-reduced-motion: reduce` 自动不启用；`<html data-no-smooth>` 手动关。
- 弹窗打开时 `lenis.stop()`（`modal.open` 里调），页面已被 `is-modal-open` 锁住，
  弹窗正文才滚得动；关闭时 `start()`。
- 站内锚点走 `lenis.scrollTo`，**不开 Lenis 自带的 `anchors`** —— 站里有 70 个
  `href="#"` 占位链接，交给它有把页面拉回顶部的风险。

### 波浪（scallop）的归属：放在所属 section 内（2026-08-21 第十八轮定，
### 尺寸机制 2026-08-24 第二十三轮改过，下面是当前状态）

**波浪是它所分隔的「上面那个 section」自己的最后一个子元素**，不是 `<main>` 下的
独立兄弟，后台里也不该是独立的一条——这条结构性决定第十八轮定的，没有变：

```html
<section class="gb-product gb-product--lg">
  …
  <div class="gb-scallop gb-scallop--edge gb-scallop--lg gb-scallop--white-to-mint"></div>
</section>
```

- **为什么归上面而不是下面**：`.gb-scallop--bleed`（nutrition 那道）要让上方模块的内容
  穿到波浪底下，跨不过模块边界。
- **尺寸写在波浪自己身上**（第二十三轮撤掉了「section 传 `--edge-w/band/h` 给波浪」
  这层——`.gb-scallop` / `.gb-scallop--lg` 本来就自给自足，直接读 `:root` 的
  `--sc-w/h` 或 `--sc-lg-w/h`）。section 只需要做一件事：把 `var(--sc-h)` 或
  `var(--sc-lg-h)` 加进自己的 `padding-bottom`（`calc(原值 + var(--sc-h))`），
  给波浪腾出一条自己的高度。多数模块「永远大瓦片」或「永远小瓦片」，直接把变量
  写死进 `padding-bottom`；同一个 class 在不同页面要求不同瓦片的（`.gb-page-hero--center`
  / `.gb-product` / `.gb-app-section` / `.gb-ingredients`），新增了 `--lg` 正交修饰类
  （`.gb-page-hero--lg` / `.gb-product--lg` / `.gb-app-section--lg` / `.gb-ingredients--lg`，
  跟 `.gb-scallop--lg` 是同一种命名思路，只覆盖 `padding-bottom`）。
  ⚠ **`position: relative` 也要自己补**——之前是 `.gb-sec-edge` 给的，删掉那层之后
  每个用到 `.gb-scallop--edge` 的 section 都要自己有这条，否则波浪的 `position:absolute`
  飘到更外层的定位祖先上去。
- 配色约定：`--wave-bg` 恒为**上方**那块的颜色、`--wave-fg` 恒为**下方**那块；
  `--down`（弧朝下）与 `--lg`（大瓦片）是两根正交的轴。
- ⚠ **不要写 `section + .gb-scallop` 这类相邻兄弟选择器** —— Shopify 给每个 section 套的
  `<div id="shopify-section-…">` 一来就全失配。（现在波浪在 section 内部，本来也不需要。）
- 页脚两道（`.gb-footer-cta-wrap` / `.gb-footer-wrap`）是**上边缘**、在流里，
  本来就在自己模块内，没有改；要做上边缘变体再加一组 `--edge-t`。

⚠ **改波浪尺寸机制或搬波浪时，路径式的 computed-style diff 无效**（节点一移动，
后面所有兄弟的下标整体错位，diff 比的是不同元素）。判据要换成与位置无关的不变量：
「波浪顶边到上方内容底边的间距」==该模块原来的 `padding-bottom` 数值、波浪底边
贴 section 底边（像素差 ≤0.6）、波浪宽度贴 section 宽度。脚本见 CHANGELOG 第二十三轮。

### 入场动效

**除下方「特殊动效」列出的以外，所有 fadeIn / fadeInUp 一律用 `wowo`，且尽量靠 class 控制。**

- 移植 Terra 的两份文件：`project/Terra/assets/scss/helpers/_animation.scss`
  + `script.js` 的 `morph.wowoSetup()` / `morph.wowo()`。不新写 IO 观察器、不引 AOS / animate.css / WOW.js。
- 用法：元素加 `class="wowo fadeInUp"`，错峰加 `delay-in-N`（N=1~20，每级 0.1s）。
  **写 HTML 时直接把 class 挂上**，不要在 JS 里逐个查询注入 —— 只有 CMS 导出不可改的 HTML
  才走 `wowoSetup()` 的选择器映射表。
- 可用动画名：`fadeIn` / `fadeInUp` / `fadeInDown` / `fadeInLeft` / `fadeInRight` /
  `zoomIn` / `zoomOut` / `bounceIn`；时长固定 0.7s，fadeInUp 位移 30px；**只播一次不可重播**。
- ⚠ 隐藏门**不再是无条件的**（第十四轮改）：规则是 `html.js .wowo { opacity: 0 }`，`js` 类由
  `<head>` 的内联脚本加、并在 `load`（或 4s 兜底）时若 `window.gumi` 不存在就摘掉。
  **只加 `js` 类是不够的** —— 那行内联脚本在 main.js 404 / 顶层抛异常时照样执行，门照样成立；
  必须以「main.js 的收尾导出存在」为条件。改加载顺序后仍要验首屏 opacity 回到 1。
- ⚠ **动效 class 挂在包裹容器上，不挂在 `<img>` / `<picture>` 上**（第十七轮）：
  `<picture>` 当不了定位/动效元素（默认 inline，改 display 又会把 `<source>` 提升成布局项），
  且图片自己常带 `transform`（如 hero 小熊的 7.92° 倾斜），两者叠在同一个元素上会互相覆盖。
  是 `<picture>` 就用一个 `<div>` 包起来，class 挂 div。
- ⚠ **首屏元素不挂 `wowo`**（第十四轮）：合成层上的 opacity 动画不产生 LCP 候选，
  要等 1500ms 移除 class 才登记，11 页 LCP 因此卡在 ~1550ms。折线以下照常用。

### 特殊动效（不走 wowo，单独实现）

| 模块 | 效果 | 参考 |
|---|---|---|
| Homepage **「60+ whole foods. No juicer, no fuss.」** | 小熊软糖图片**浮动** + **出现**动效 | https://www.cravburgers.shop/ **首屏的图案** |
| 全站文字出现效果 | 同参考站的文字入场手感 | 同上 |

对应批注 `401:29596` / `216:5903`（设计方原话就是让参考 cravburgers.shop 的汉堡浮动 + 文字淡入）。
落地前先实地看参考站的实现（浮动是否 GSAP、是否随鼠标视差、缓动曲线与周期），
**别凭「浮动」二字自己造一个 `@keyframes float`**。文字入场若与 wowo 手感一致则仍用 wowo，
只有确认不一致才单写。

### 实现边界：Shopify app 生成的内容不做（2026-08-19 用户指定）

搭前端时**跳过会由 Shopify app / metafield 产出的内容**，只留结构占位与样式外壳，不实现逻辑、不填假数据。
已核实设计稿中受此影响的区块：

| 页面 | 区块 | 稿中表现 | 处理 |
|---|---|---|---|
| PDP `324:52658` / `324:53792` | **订阅选购** | Autoship and Save / Subscribe & Save / One Time Purchase / Delivers every 4 Weeks / How subscription works | 由订阅 app 渲染，前端不做选项逻辑与价格计算 |
| PDP | **产品详细信息 accordion** | Why Gumi / Ingredients & Allergies / Science / Directions | 内容走 metafield/app，前端只做 accordion 壳 |
| PDP | **评论区** | Real Customer Reviews 4.76 / Based on 123,000 reviews / 5 张评论卡 / 点赞点踩计数 / See More Reviews | 由评论 app 渲染，前端不做 |
| **Reviews 页** `324:63924` / `324:64961` | 整页评论列表 | 同上 | 由评论 app 渲染，前端不做 |
| 全站 header | **Trustpilot 徽章** | `Excellent` / `Truspilot` | 第三方嵌入 |

⚠ 连带作废：批注 `401:31223`（评论支持选传图、点赞点踩排序）**属于评论 app 的能力，本次不实现**。
⚠ 仍要做的：**营养标签弹窗**（`401:31227` 底部上滑）不是 app 内容，是自定义模块，照做。
⚠ PDP 页脚「And Last Questions?」的 6 条 accordion 稿中就是 `Accordion Closed` / `Text here` 占位 ——
按铁律 3 **保留占位**，不编造问答。

## 设计源现状（已全量落盘）

| 项 | 数量 |
|---|---|
| 页面稿 | 11 组（Desktop 1440 ↔ Mobile 390），Shipping 缺 desktop |
| 组件与状态稿 | 导航 4、购物车 4、弹窗 9、其他 3 |
| 完整节点树 | 42 个 frame + 30 条批注 |
| 参考截图 | 72 张 PNG @1x |
| 字体样式组合 | 139 种 |
| 颜色 | 95 种（含描边） |
| 圆角 | 60 种 |
| 阴影 | 19 种 |
| 文案条目 | 71 份逐页清单（`docs/copy/`） |
| 字体文件 | `assets/` 共 19 个 woff2（804K），其中 13 个被 `customstyle.scss` 的 `@font-face` 段引用 |

**⚠ 33 个 frame 含 `characterStyleOverrides`**（同段文字里换字体/色/字号）——
实现时必须逐字符查 `characterStyleOverrides` + `styleOverrideTable`，不能只取 TEXT 顶层 style。
清单在 [DESIGN-TOKENS.md](DESIGN-TOKENS.md) 末尾。

**品牌视觉**：字体 **PP Palma**（主，3298 次）/ **Inter**（409）/ **Lexend**（108）/ **Playpen Sans**（90）；
主色 `#B5ED61` 青柠绿、`#005635` 深绿、`#011307` 近黑绿、`#FAF9F8` 米白。

字体文件与 `@font-face` 已就位于 `assets/customstyle.scss`（原 `base/_fonts.scss` 段）：

- Inter / Lexend 是**可变字体**（一个文件覆盖全字重，md5 实测同一文件）→ `font-weight` 写范围
- Playpen Sans 是**静态实例**，只有 600 → `font-weight` 写单值，要别的字重得另外下载
- PP Palma 无授权文件，Figtree 占位；**全站走 `$font-brand-stack`，换字体只改这一处**
- 稿中的 `SF Pro Text` 不是字体需求，是 SF Symbols 图标占位（Trustpilot 星标），导 SVG

## 进度

| 日期 | 事项 |
|---|---|
| 2026-08-19 | 建项目目录；确认交付节点 `401:31719`；拉取文件结构 + SECTION 子节点清单（88 个） |
| 2026-08-19 | 首个 token 触发账号级 429（retry-after ≈ 4.6 天），拉到 4/42 中断；换 dev@mockuptocode.com 的 PAT 后一次跑完 |
| 2026-08-19 | 节点 42/42 + 截图 72/72 落盘；核实 5 个重名 desktop 稿归属；提取交接说明与 22 条批注；生成 token 与逐页文案 |
| 2026-08-19 | 定下 5 条前端规范（目录结构 / wowo 动效 / 特殊效果参考站 / app 内容边界 / STATISTICS 代码动态）；建交付目录 |
| 2026-08-19 | 补齐字体：查出稿中还有 Lexend（前次汇总漏了）；下载 Inter/Lexend/Playpen Sans；PP Palma 无授权用 Figtree 占位；写 `_fonts.scss` 并验编译 |
| 2026-08-19 | 用 `figma-parser/local-parse.js` 零 API 生成 42 个 frame 的 build spec；建 SCSS 骨架 + 移植 wowo；完成 header / footer / hero / logo scroll；下全 12 张 raster + 14 个图标 |
| 2026-08-19 | `/v1/images` 端点触发账号级 429（retry-after ≈ 4.6 天），后续 section 新图标导出受阻 |
| 2026-08-19 | 换 ly-design PAT 解除限流；Homepage 全部 section 完成，14 断点无横向溢出 |
| 2026-08-19 | 实地考察 cravburgers.shop 反查出 GSAP 参数，用原生 CSS+JS 复刻小熊浮动与文字出现；营养标签弹窗（两页签 + 27 行成分表）完成 |
| 2026-08-20 | 修 Homepage 三处 mobile 字号偏差；**PDP 整页完成**（product/reviews 复用 Homepage 模块 + promo / Us VS Them / FAQ 新建，评论区按 app 边界留壳）；新增 `ink-outline()` 圆形描边函数与圆形光晕重建 |
| 2026-08-20 | 用户追加公约（hover / 过渡 / 动效流畅）→ 建 motion token 与 `@include hover`，补齐两页全部交互态；Playwright 实测 **46 类可点击元素 hover 全部生效、cursor 全为 pointer**，触摸端反证不粘住 |
| 2026-08-20 | **客户验收 10 项全部落地**：PP Palma 试用包接入（400 字重靠 Light+Medium 插值补齐）、波浪改 gradient 平铺实现全宽响应、hero 小熊不再被裁、hover 去位移去阴影、描边统一 `ink-outline`、logo 去 cover 裁切、PDP gallery 与 reels 做成 swiper/slider。详见 CHANGELOG 第六轮 |
| 2026-08-20 | **字体解析定死 + 入场效果重排**：删掉 PP Palma 400 的 `local()`（试用包 12 个 OTF 的 typographic family 都叫 "PP Palma"，会在装了字体的机器上被整族劫持）；word-pop 收归 stats 的 `.stat`（数字用 `data-pop-atom` 整块弹出，避免描边被拆断）；全站文字容器铺 `wowo fadeInUp`、图片容器铺 `fadeIn`。新增 `font-check.html` 自检页。详见 CHANGELOG 第七轮 |
| 2026-08-20 | **字距 / 波浪几何 / hover / 手风琴**：插值字体拆成形(0.50)、距(0.31)两个系数把字距按稿收平；波浪条高改由节距推导（旧的封顶写法在 ≥1920 会把弧切断、波浪散开），节距上限收到稿值即宽屏只增多不变大；按钮 hover 统一翻 lime、链接加下划线扫入；FAQ 与 PDP 规格行做成真手风琴；reels 改全屏出血并居中。详见 CHANGELOG 第八轮 |
| 2026-08-20 | **任务文档 8 项**：logo 条真无缝循环（旧写法位移量大于余量，>1308 宽必露白）；PDP 缩略图按稿外挂到列外、顶对齐，主图回到 465；promo-art 拍平成单张 PNG（顺带修出**小熊与全部标签旋转反号**、以及 `ink-outline()` 在多行上自相遮挡两个真 bug）；手风琴改原生 `<details>`，JS 禁用下仍能开合；页脚区去 wowo；PP Palma 插值件回退字形 11→7（`j` 归位）；reels 改无限循环；hero 小熊改挂 `.hero__inner` 并补上稿里的 7.92°/−15° 倾斜。详见 CHANGELOG 第十轮 |
| 2026-08-20 | **九个内页全部搭完**（Science / Reviews / How Gumi Works / Our Story / FAQ / Get in Touch / Referral / Privacy / Shipping），全站 11 页 × 5 宽度回归 **55/55 绿**；新增 `figma/new-page.py`（页面外壳）、`figma/dump-text.py`（长文案取全文）、`tools/shoot.py`（回归）。详见 CHANGELOG 第十二、十三轮 |
| 2026-08-20 | **写审计交接文档** [AUDIT-HANDOFF.md](AUDIT-HANDOFF.md)：跑起来的命令、设计源定位、**不要报成 bug 的 7 类清单**（字体/断点/两稿冲突/占位/app 边界/自定值/浏览器差异）、CSS·JS·性能三线的现状基线与已知技术债、9 条 headless 探针陷阱、建议的审计范围与输出格式 |
| 2026-08-21 | **审计的上线阻断级修复全部落地**（第十四轮）：wowo 两个 P0（闩锁死锁 / 透明门无兜底）、首屏退出透明门使 **LCP 1550ms → 40~104ms**、7 处开发占位、Privacy 首段与两页分隔条、13 个死弹窗触发器、扇贝拆尺寸/方向两轴（22 处重指派）、CTA 板手机几何 + 两张矢量 mask、手机端「只写桌面值」一批、**图片 WebP 使首屏 17.61MB → 3.78MB**、CSS/JS 卫生 10 条。详见 CHANGELOG 第十四轮 |
| 2026-08-21 | **assets 目录扁平化 + SCSS 合并**（第十五轮）：按需求方定的交付结构，`assets/` 取消 css/js/fonts/icons/scss 五个子目录全部平铺（66 个文件、零子目录），36 个 scss partial 合并为单文件 `assets/customstyle.scss`。判据是**编译产物逐字节相同**（改路径前 md5 一致），A/B 几何 24 个页面×宽度组合的 scrollHeight 全部逐一相同、222 处矩形差异低于 237 处的噪声基线。详见 CHANGELOG 第十五轮 |
| 2026-08-21 | **任务文档 9 项**（第十六轮）：断点改制成 手机≤575 / 平板576–1280 / PC≥1281（布局阈值 768/1024/1200 原样保留，只给数值分档）、平板档 140 条 `fluid()` 插值、栅格 3→2→1；`nutrition__band` 按稿重做（旧实现把旋转转了两遍）、9 只散熊合成单图（旧实现漏了各自旋转）、产品图库改叠放淡入且一次一张、手风琴同组排他、reel hover 只放大内部图、浮动收归 stats、`bear-meter` 改 20 列 grid；全站 79 个块名加 `gb-` 前缀（3384 处，computed-style 逐项不变）。详见 CHANGELOG 第十六轮 |
| 2026-08-21 | **波浪搬进所属 section**（第十八轮）：`<main>` 下 27 个独立波浪 + hero 那个全部成为宿主 section 的最后一个子元素（`.gb-sec-edge` / `.gb-scallop--edge`），尺寸只写在 section 上、波浪继承。留白用 `::after` 占位块 —— border 会被 Chromium 取整到整数 px（每道差 ~1px），padding 得逐个 section 逐断点 calc。判据换成**与位置无关的矩形多重集**（路径式 diff 因节点移动整体错位而失效）：除宿主各自长高一个条高外所有盒子逐一不变、`body` 总高 22 个组合一位小数不差。详见 CHANGELOG 第十八轮 |
| 2026-08-21 | **任务文档 3 项**（第十七轮）：全站平滑滚动接 **Lenis 1.3.11**（手写阻尼版换掉——触控板的 wheel 已带 OS 惯性，再叠一层会拖尾）；`nutrition__band` 透到波浪底下（稿里那一个 Spacer 的 `frameFill` 本就是 `none`，旧实现把包装袋直线硬切在 section 底边）、pack 行改居中屏幕 + 始终两侧被裁 + 全面 `fluid()`；hero 小熊去掉放大改纯淡入、页脚装饰熊去 fadeIn、动效改挂包裹 div。**总高度是不变量**：nutrition +127.979 与波浪 −127.979 精确抵消，`body` 高度一位小数没动。波浪归属给出结论（做设置项不做独立 section，DOM 不用动）。详见 CHANGELOG 第十七轮 |
| 2026-08-24 | **任务文档 7 项**（第十九轮）：弹窗退场换曲线并加长（真因是 out 曲线倒放、不是时长）；手风琴行距从容器 `gap` 挪进 `summary` 的 `padding-bottom`（行间死区归零，末项要单独归零否则页面长高）；59 处加号图标改纯 CSS 两条线、展开转平、去 hover 放大；输入框焦点改 border-color（复选框留 outline）；header 吸顶 + 抽屉高度实测 + PDP sticky 避让；弧形文字两个真因（SVG `overflow:hidden` 切上缘 −11.7、文字比路径长 1.9）；页脚波浪条带改透明，5 页点名薄荷。判据 `tools/r19check.py` 全绿 + **body 总高 22 组合不变**。详见 CHANGELOG 第十九轮 |
| 2026-08-24 | **对话给的 8 项（第二十轮）**：hero 按钮满宽 + 公告条补 Trustpilot 五颗星；**hero 光晕按稿重建**（稿里 glow 是一条 26.2137 的 CENTER 描边、不是照片自带的，旧图只有约 12px 且贴着照片凹凸走）；logo 槽位 96→80 + viewport 上下 8；**`ONE HANDFUL` 的弧从正圆 `A 338 338` 改回设计的椭圆** rx118.5261/ry65.7047，框回 278×29；`60+`/`10+` 的加号缩到 0.56em 并上浮（PP Palma 试用档的 `+` 字形对不上，用排版模拟）；**四支箭头补上 Figma 组的旋转+镜像**（旧 viewBox 长宽比差 2.5 倍）并移进 `.gb-stats__bear`；补回 `.gb-stats` 从来就没有的下缘波浪（cream→sand，96）。判据 `tools/r20check.py` 全绿；10 个非首页页面除星条外逐像素不变。详见 CHANGELOG 第二十轮 |
| 2026-08-24 | **对话给的 PC 端 15 项（第二十一轮）**：science-card/bear-meter/highlight-card/product accordion·taste·packed/testimonial/reviews disclaimer/footer-cta 共 14 处间距与尺寸微调；`.gb-product__app-slot`（订阅 app 占位虚线框）整块删除；**footer-cta 弧度还原**——真因是 viewBox 一直拿椭圆本体的 289×62 当框用，Figma 里椭圆外面还套着一层 452×51 的 `Curved Text FRAME` 没找到，弧被压成近似正圆，改用椭圆左右顶点间的整段圆顶弧（`M 81 83 A 144.5 66 0 0 1 370 83`）。`tools/rwd.py` 11 页×10 档全绿。全站还剩 4 处同缺陷（promo-card / dosed×2 / cta-band）+ footer-cta 手机变体未做，详见 CHANGELOG 第二十一轮遗留 |
| 2026-08-24 | **对话追加 7 项（第二十二轮）**：`gb-stats__bear` 的浮动效果收窄到内部图片（新增 `.gb-stats__bear-art` 包裹层，四支箭头不再跟着飘）；packed 区 sub-title 补 `align-self:center`（上轮 packed 改 flex-start 连带带偏了标题）；stats__note / highlight-card__title / footer-cta 三处间距值订正。 |
| 2026-08-24 | **撤掉 gb-sec-edge 机制 + 补 stats 波浪右侧小熊（第二十三轮，用户定）**：全站 14 个模块的波浪尺寸不再靠 section 上的 `gb-sec-edge`/`gb-sec-edge--lg` 传值，改成直接把 `var(--sc-h)`/`var(--sc-lg-h)` 加进各自的 `padding-bottom`（`.gb-scallop`/`.gb-scallop--lg` 本来就自给自足）；新增 4 个正交 `--lg` 修饰类处理「同一 class 不同页面要求不同瓦片」的情况。30 处波浪逐一核对定位上下文、贴边、宽度、间距不变量全部通过；踩到并修复一个批量替换脚本的跨规则误传 bug（8 处被错误加上 `--lg`）。另外把 `.gb-stats` 波浪右侧一直缺失的小熊补上（`images/stats-bear-deco.png`，从 `bear-gummy-glow.png` 裁边而来，坐标按设计截图反推——本地没有这个节点的 Figma 数据；因 `.gb-stats` 无 overflow 保护，位置比设计稿的截图位置上移了一截以避免被下一个 section 盖住下半截）。详见 CHANGELOG 第二十三轮，含遗留的架构文档更新。 |
| 2026-08-24 | **弹窗滚动锁定横向抖动修复 + nutritional-label 数值订正（第二十四轮）**：`html/body.is-modal-open{overflow:hidden}` 关掉滚动条后视口凭空变宽、内容跟着跳一下——`main.js` 加锁前先测滚动条宽度写成 `--scrollbar-w`，CSS 补 `padding-right: var(--scrollbar-w,0px)` 吃回来，解锁自动归零；这个坑不止这一个项目踩过，已写进 `~/.claude/CLAUDE.md` 通用铁律第 14 条备用。另去掉 `.gb-nl-panel__close` hover 时的 SVG 旋转；`.gb-nl-pane`/`.gb-nl-tab::after`/`.gb-nl-table` 共 6 处数值订正。详见 CHANGELOG 第二十四轮。 |
| 2026-08-20 | **缓存版本号 + 构建自检**：反馈「改动没落实」，服务器侧查证文件全对、真因是 `file://` 预览把无版本号的 css/js/woff2 缓存住了。给引用与字体 url 加 `?v=$build`，`font-check.html` 扩成构建自检（版本号 + 10 条功能探针 + 字体表）。详见 CHANGELOG 第九轮 |
## 阻塞

1. ~~**Figma `/v1/images` 端点 429**~~ — **已解除**。`settings.json` 里的 `figd_NR7GZ…` 仍在限流
   （账号级，retry-after ≈ 4.6 天），改用 **ly-design 的 PAT**（`dev@mockuptocode.com`）后恢复，
   全站资产已一次性下全到 `figma/assets-raw/`（1286 SVG + 201 PNG，42MB）。
   ⚠ **重要发现**：429 只打在 `/v1/images`（导出端点），**`/v1/files/nodes` 数据端点不受影响**，
   带 `geometry=paths` 能拿到矢量路径自己生成 SVG。下次撞限流先试这条路，别直接等。
2. **PP Palma 仅有试用版**（`PP Palma - Free For Personal Use v1.0/`，EULA 明确排除商业用途）。
   已接入用于还原度比对：300/500/800 用包内 Fizzy 三个文件，**400 是 Light+Medium 插值的产物**
   （试用包不含 Regular，而它占全站 59% 用量）。
   **上线前必须换成客户的授权 web font**，尤其 Fizzy 那一组；切换点仍只有 `_fonts.scss`。
3. 店铺 / 主题基底 / 接入方式未定 → 只影响后续套 Shopify 主题，静态阶段不受影响。
4. **Figma `/v1/images` 又在限流**（2026-08-20 实测 429，`retry-after` ≈ 3.98 天 → 约 08-24 解除）。
   手上只有 `settings.json` 里那把已耗尽的 PAT，第十轮的 promo-art 因此是本地渲染的
   （`figma/promo-art-source.html` + `figma/render-promo-art.py`），拿到新 token 后可按
   「四周各留 5%」的约定直接覆盖 `images/promo-art.png`。

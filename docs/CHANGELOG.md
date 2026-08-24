# Gumi Brand — 前端改动记录

> 每约 10 项记一条。只写「改了什么 / 为什么 / 文件清单 / 遗留」。
> 推导过程、探针数据、失败尝试留在对话里。

## 2026-08-19 第一轮：基建 + header/footer + hero + logo scroll

### 改了什么

1. **build spec 全量生成**（42 个 frame）。复用 `figma-parser` 的 `local-parse.js`
   吃已落盘的节点 JSON，**零 API 调用**，产出与在线 parser 等价的 `.build.txt` + `.spec.json` + `asset-list.json`。
2. **SCSS 骨架**（7-1）：变量取自 `DESIGN-TOKENS.md`；`container` mixin 用 CSS 变量承载响应式内边距
   （避免每个调用点触发 Sass `mixed-decls` 弃用警告）。
3. **移植 Terra 的 `wowo`**：`_animation.scss` 整份复制；JS 按原机制原生改写（不引 jQuery，
   Shopify 主题不带它），class 契约与 1500ms 清理时序不变。`<noscript>` 兜底防 JS 挂掉后内容永久不可见。
4. **header**：桌面 dropdown（0fr→1fr 网格动画，展开高度实测 258px 与稿一致）+ 移动全宽抽屉
   （批注 401:31229）。两张 nav 卡片、Manage Account、6 个链接（Shop / Learn more / Get in Touch 三项仅移动稿有）。
5. **footer**：CTA（弧形文字用 SVG `textPath`，批注 401:31452 要求文字可编辑）+ 四段式 footer
   + 两只浮动小熊 + 扇贝分隔。
6. **扇贝分隔组件**：几何直接取自 Figma union 节点（小号 r=193.62 间距 302.19；大号 r=335.75 间距 524.74）。
   一份 SVG `fill: currentColor`，配色靠修饰类。**大号那份是从节点数据重建的**（API 限流时导不出）。
7. **hero**：标题/描述/按钮/3 个 USP（数字描边 = Figma `stroke 5px OUTSIDE` → `-webkit-text-stroke: 10px`
   + `paint-order: stroke fill`，正好对上批注 401:31482 要求描边完整包裹标点）。小熊按稿 `cover` 裁进
   568×816 框并压在扇贝之上，由 `.hero` 裁切。
8. **logo scroll**（批注 401:29602）：CSS 跑马灯，4 组重复保证无缝；`.logo-scroll--off` 对应
   「关闭时下方灰底上延」。
9. **资产**：12 张 raster 一次性下全（去重后仅 12 个 imageRef，走 image fills 端点零配额）；
   图标 14 个；原图移入 `figma/assets-raw/`，`images/` 只放优化产物（小熊 8.3MB→808K）。
10. **小熊光晕**：稿中的光晕 vector 在本地 JSON 里 `fillGeometry` 为空，API 又限流 →
    用图自身 alpha 膨胀重建（形状仍来自源图，非编造）。

### 文件清单

```
新增  assets/scss/helpers/{_variables,_mixins,_animation}.scss
新增  assets/scss/base/{_reset,_typography}.scss
改写  assets/scss/base/_fonts.scss              （注释改英文，逻辑未动）
新增  assets/scss/components/{_button,_scallop}.scss
新增  assets/scss/layout/{_header,_footer}.scss
新增  assets/scss/modules/{_hero,_logo-scroll}.scss
新增  assets/scss/style.scss                    入口
新增  assets/js/main.js                          wowo + header 交互
新增  index.html                                 header / hero / logo scroll / footer
新增  assets/icons/*.svg                         14 个
新增  images/*.png                               8 个交付图
新增  figma/fetch-assets.py                      资产下载（raster / icons / illust / raw）
新增  figma/optimize-images.py                   派生交付图 + 光晕重建
新增  figma/make-page.py                         SVG 内联工具
新增  figma/parser-out/                          42 个 frame 的 build spec
移动  figma/assets-raw/                          12 张原始导出图（不进交付）
```

### 遗留

- **Figma `/v1/images` 端点 429**，`x-figma-rate-limit-type: low`（账号级配额耗尽），
  `retry-after ≈ 4.6 天`。节点数据/截图/image fills 不受影响，已下载资产齐全。
  **后续 section 的新图标导出被卡住** —— 需换账号 PAT，或从节点数据重建（弧形文字、扇贝已这么做）。
- Homepage 还剩：60+ whole foods（含 STATISTICS 动态小熊）、packed with、nutrition、pdp、reviews。
- 特殊动效（小熊浮动 + 文字出现，参考 cravburgers.shop）**尚未实地考察参考站**，未落地。
- PP Palma 仍是 Figtree 占位，字宽与换行位置与稿有出入，此阶段不做像素级验收。

## 2026-08-19 第二轮：Homepage 全部 section 完成

### 改了什么

1. **Figma 限流解除**：`settings.json` 里的 `figd_NR7GZ…` 的 `/v1/images` 端点仍在 429
   （账号级、retry-after ≈ 4.6 天），改用 **ly-design 的 PAT**（`dev@mockuptocode.com`）后恢复。
   ⚠ 另有一个发现：**429 只打在 `/v1/images`（导出端点），`/v1/files/nodes` 数据端点不受影响**，
   带 `geometry=paths` 可以拿到矢量路径自己生成 SVG —— 下次撞限流先试这条路。
2. **全站资产已落盘**：`figma/assets-raw/icons/` 1286 个 SVG + `figma/assets-raw/illust/` 201 张 PNG@2x
   （42MB，按文件名去重后的实际数，无失败项）。交付用的再挑进 `assets/icons/` 与 `images/`。
3. **STATISTICS**（60+ whole foods）：四角统计块按 Figma 的 1193×623 画布用百分比绝对定位，
   4 个手绘箭头 + 中间小熊；tablet 起转 2 列网格。弧形文字提为 `.arc-text` 组件与 footer 共用。
4. **science cards**：**这里才是设计方问的「按百分比高亮的小熊图形」** —— 每卡 100 个小熊，
   前 95 个实心、后 5 个 `opacity: .3`（实测自节点数据）。按用户决策做成**代码动态**：
   `data-fill` / `data-total` 驱动，JS 生成，主题设置改数字即可，不用动 markup。
   图标是 14×22 的小熊照片（不是矢量），按 frame 偏移裁出 27×44。
5. **nutrition**：3 张深绿卡（图为稿中的灰色占位，底部深绿扇贝 lip）+ 产品包装带。
   包装带原是 2246px 的整帧、旋转 -6.56° —— 实测发现**父容器旋转正好抵消行内的阶梯偏移**，
   所以改成「水平排列 + 每个包装各自倾斜」，用单张包装图重复，省下 1.7MB 的整帧导出。
6. **product（Homepage 内嵌 PDP）**：图区/信息/特性/保障/accordion/Tastes Like/Packed With 全做，
   **订阅模块按 app 边界只留占位槽**（`data-app="subscription"`），不复刻选项与价格。
   稿中 guarantee / taste / packed 的图标本身就是空占位方块（150 字节），照实现不编造。
7. **reviews**：Instagram reels 区（**不是评论 app，不在排除范围**）。5 个 reel 灰色占位 + play 图标，
   横向 scroll-snap 而非引入 Swiper；3 条 testimonial 稿中文案完全相同，按铁律保留占位。
8. **响应式全断点验证**：14 个宽度（375→1920）逐个实测 `scrollWidth` 与 `canScrollX`，
   修掉 4 处横向溢出，现全部为 0。

### 修掉的坑（都是实测出来的，不是目测）

| 症状 | 根因 |
|---|---|
| header 面板收不起来（0fr 仍留 64px） | grid item 的 padding 压不掉，须再套一层无 padding 的裁剪层 |
| 扇贝弧变平 | reset 的 `svg{max-width:100%}` 把 1721px 的 SVG 压到 1440，viewBox 等比缩放 |
| 移动端小熊盖住 hero 标题 / 页面能横滚 505px | 容器写了 `position: static`，内部绝对定位的图逃到更上层 relative 祖先 |
| 1200px 处横向溢出 33px | `.deco-bear--b` 用 `left:66%` 配固定 440px 宽，改 `right` 锚定 |
| 1100px 处溢出 101px | footer 三列链接固定 194px 不换行 |

### 文件清单

```
新增  assets/scss/components/_arc-text.scss
新增  assets/scss/modules/{_stats,_science,_nutrition,_product,_reviews}.scss
改    assets/scss/modules/{_hero,_logo-scroll}.scss
改    assets/scss/components/_scallop.scss        新增 5 个配色修饰类
改    assets/scss/layout/{_header,_footer}.scss   面板裁剪层 / 小熊定位 / 三列换行
改    assets/js/main.js                            + bearMeter
改    index.html                                   Homepage 全部 section
新增  assets/icons/                                共 33 个
新增  images/                                      bear-icon / stats-bear / product-pack / bear-scatter 等
新增  figma/assets-raw/{icons,illust}/             全站资产备份，不进交付
```

### 遗留

- **特殊动效未做**：小熊浮动 + 全站文字出现（参考 cravburgers.shop，批注 401:29596）。
  常规 fadeInUp 已挂 `wowo`，但参考站的手感**尚未实地考察**，不能凭「浮动」二字自造。
- **营养标签弹窗未做**（批注 401:31227，底部上滑）。按钮已就位：
  `.product__label-btn[data-modal="nutritional-label"]`。
- Homepage 之外的 10 个页面未开工（PDP / Science / Reviews / How Gumi Works / Our Story /
  FAQ / Get in Touch / Referral / Privacy / Shipping）。
- 页面总高 9420px vs 稿 10123px，差值主要来自被排除的订阅模块，属预期。
- PP Palma 仍是 Figtree 占位，换行位置与稿有出入，此阶段不做像素级验收。

---

## 第三轮 — 特殊动效 + 营养标签弹窗（2026-08-19）

### 做了什么

1. **实地考察参考站 cravburgers.shop**（批注 401:29596 / 216:5903 指定）。
   该站是 Next.js + GSAP + ScrollTrigger + Lenis，动效不在 CSS 里，从 JS chunk 反查到确切参数：

   | 效果 | 参数（原站 GSAP 调用） |
   |---|---|
   | 图片入场 | `fromTo {scale:.5, opacity:0, y:100, rotate:-5} → {scale:1,opacity:1,y:0,rotate:0}`，`1.5s / back.out(1.5) / delay .5` |
   | 图片浮动 | `to {y:"-=15"}`，`2.5s / sine.inOut / repeat:-1 / yoyo / delay 1.7` |
   | 文字出现 | 按词拆分，`from {opacity:0, scale:0, y:random(18,40), rotate:random(-16,16)}`，`.72s / back.out(2.35) / stagger .055 / transformOrigin 50% 90%`，ScrollTrigger `top 88%` + `once` |
   | 降级 | `prefers-reduced-motion` 时只做 opacity 0→1，`.4s / stagger .02` |

2. **用原生 CSS + 60 行 JS 复刻，不引 GSAP**（会多 ~70KB gzip，两个效果不值）。
   缓动按 GSAP 源码公式 `back.out(s) = (t-1)²·((s+1)(t-1)+s)+1` 采样成 CSS `linear()`，
   前面留 `cubic-bezier` 兜底老引擎。参数与推导写在 `_motion.scss` 顶部注释。
   - `.float-art` 挂 hero / stats / footer 两只小熊；入场与浮动共用 transform，
     靠 `animation-composition: add` 叠加，不互相截断
   - `[data-pop-text]` 由 `popText` 模块拆词，随机量写进 `--pop-y/--pop-r`，错峰走 `--pop-i`
   - `data-pop-stagger="30"` 可按元素覆盖 55ms 步长（长段落 29 词要跑 2.3s）
   - HTML 里 10 个标题/引导段从 `wowo fadeInUp` 换成 `data-pop-text`；卡片/图块仍走 `wowo`

3. **营养标签弹窗**（批注 401:31227）。稿 336:31534（Nutritional Information 页签）/
   336:34120（Ingredient List 页签）/ 336:28414（手机）。两个页签 + 27 行成分表 + 2 条脚注全部照搬，
   数值维持稿中占位（`Information here` / `15 g` / `5%`），不编造。
   - 底部上滑、原路滑回：常驻 DOM，`translateY(100vh) ↔ 0`，`visibility` 延后到过渡结束再切
   - 桌面居中 845×579 / 手机贴底 `calc(100svh - 45px)`，圆角 24 / 16-16-0-0
   - 键盘可用：Escape 关闭、Tab 焦点循环、开关时焦点进出面板

### 修掉的坑

| 症状 | 根因 |
|---|---|
| 弹窗 head 高 128（稿 120） | 稿里那 8px gap 属于只有一个子节点的包裹层，实际不生效 |
| 切到 Ingredient List 面板撑到 852 | body 没设 `max-height`；稿中两个页签 body 都是 459 |
| 打开后焦点没进面板 | `querySelector` 选中了不可聚焦的遮罩 `div`，改成只查可聚焦元素 |
| 页签文字比稿高 9px | 稿中 tab 框 `primaryAxisAlignItems: CENTER`，44 高里内容垂直居中 |
| 成分表子行不缩进 | `.nl-table th` (0-1-1) 压过 `.nl-table__sub` (0-1-0) |

### 判据

- 文字拆词**零文本改动**（拆前/拆后 `textContent` 逐元素比对）、`<br>` 保留、
  三个断点盒高逐元素比对全等 → 拆词没改变任何换行
- 跳跃滚动到 0/25/50/75/90/100% 后，**视口内不得有仍不可见的入场元素**（等错峰跑完后全绿）
- 弹窗开启态 7 个断点：页面横向溢出 0、面板内横向溢出 0、几何 845×579 / head 120 / tab 44 全等稿

### 文件清单

```
新增  assets/scss/components/_motion.scss    浮动 + 文字出现（含参数出处与推导）
新增  assets/scss/components/_modal.scss     营养标签弹窗
改    assets/scss/style.scss                 + modal / motion
改    assets/js/main.js                      + popText + modal（142 → 318 行）
改    index.html                             10 处换 data-pop-text / 4 处挂 float-art / 追加弹窗
改    index.html                             6 条中文注释改英文（违反“不要中文注释”）
```

### 遗留

- **文字出现只挂了标题与引导段**，正文列表/卡片内文字仍走 `wowo`。若要真「全站文字」，
  需要逐段确认，且长段落建议改用参考站的另一套「整行上滑」变体（SplitText lines，
  `y:100%→0`、`1.4s`、`stagger .15`、`power4.out`），本轮未做。
- 弹窗滚动条只写了 `::-webkit-scrollbar`（稿中 8px 圆角灰条）。**不能同时写 `scrollbar-width`**，
  Chrome 121+ 标准属性会胜出把自定义样式顶掉；火狐因此是默认滚动条。
- 弹窗开合时长（0.4s）与曲线稿中没有，是自定值，需设计方确认。
- 手机端面板实测 657 高、稿 698，差值来自 Figtree 比 PP Palma 窄导致标签少折一行，属占位字体预期差异。

---

## 第四轮 — 手机端字号校正 + PDP 整页（2026-08-20）

### 做了什么

1. **修 Homepage 三处手机端字号**：抽查 `@include mobile` 块里的字号与手机稿 228:5932
   的实际字号集合比对，12 种里 3 种不在稿中，都是凭手感缩的：
   `.science-card__value` 44/36 → 稿本就与桌面同为 **56/44**（连带 `::before` 高亮条按 56 定的
   32px 高度不再脱钩，直接删掉 mobile 覆盖）；`.product__title` 26/34 → **30/36**；
   `.highlight-card__title` 26/32 → **24/30**。
2. **PDP 整页 `pdp.html`**（稿 324:52658 / 324:53792）。主产品区与 Homepage 的 `.product`
   **58 条文本零差异**（同一组件实例），整块复用，只加 `.product--page` 做图区 sticky；
   reviews 同样复用，加 `.reviews--sand` 换底色（稿中这页是 #f5f1e9 不是 mint）。
3. **新模块**：`_promo.scss`（discount xx 两张 1062x528 卡）、`_vs.scss`（Us VS Them）、
   `_faq.scss`（含 app 占位壳）。
4. **Us VS Them 的两端结构不同**：桌面是 924 宽三列表（标签 | Gumi | 他们），手机拆成两个
   独立块、标签各出现一次。DOM 按手机结构写（两列各带标签），桌面把 others 列的标签
   `display:none` —— 两列行高一致就自然对齐，不需要绝对定位。
5. **`ink-outline()` 函数**（`helpers/_mixins.scss`）：Figma 给文字描边用 ROUND join，
   `-webkit-text-stroke` 只会 miter，8.37px 的粗描边会长出尖刺。改用同心双环偏移副本，
   步数按环半径正比分配。单环会跳过 o/e 的内孔漏出底色，所以是两环。
6. **两处光晕改由 alpha 重建**：稿里导出的轮廓 vector 与小熊自身 bbox 对不上（promo 插画错位
   30px），改走 Homepage 已有的 GLOW 手法。给 `add_glow` 加 `round_join` 模式 ——
   PIL 的 `MaxFilter` 是方核，半径超过 ~12px 就是方角光晕，改用高斯模糊阈值化得到圆形膨胀。
7. **扇贝缝改内联 SVG**：卡片中间那道 126x764 的圆列（r 63、圆心距 106）原本导出成两张 PNG，
   改成一份 SVG 取卡片自身颜色，桌面竖版 / 手机横版。
8. 新增 3 个 scallop 配色（`--white-to-sand` / `--sand-to-white` / `--cream-to-mint`）。
   ⚠ 大小两种扇贝的配色属性**语义相反**（小的 top-anchored、大的 bottom-anchored），
   已在 `_scallop.scss` 注释里写明，加新配色前先读。
9. 资产：新增 `bear-gummy(-glow)` / `others-bottles`（原图 15MB → 84K）/ `vs-bear-glow`
   / 6 个 `promo-arrow-*.svg`（SVG 导出已含旋转，不要再 rotate）。

### 修掉的坑（都是实测出来的）

| 症状 | 根因 |
|---|---|
| vs 小熊只有一半大、位置偏 | 挂了不存在的 `float-art--xs`，落在 `gm-art-in` 的 `scale(.5)` 起始帧；稿中这只熊本就没有浮动 |
| promo 按钮文字折两行 | 误把 build spec 的 `max-width: 219px` 当按钮宽 —— 那是 347 减去两侧 64px padding 后的**内容宽** |
| 手机 others 列标签与值贴在一起 | gap 只写在 `.vs__col--gumi .vs__row`(0-2-0)，媒体查询不加特异性，压过了 `.vs__row` 的 mobile 规则 |
| 768px 处横向溢出 4px | 手机布局的百分比全按 351 宽稿算，728 容器下把小熊放大到 255px；给 `.vs__table` 加 400px 上限 |
| 标签描边长尖刺 / 字母内孔漏底色 | 见上方第 5 条 |
| OUR PROMISE 弧形文字上半被裁 | viewBox 只有路径高 132，没留 24px 字高 |

### 判据

- **文本完整性**：设计源 122 条（已排除 toolbar 与 real-customer-reviews）逐条比对，
  缺失 28 条全部有据 —— 17 条订阅模块、5 条 accordion 展开内容（均属 app 边界）、
  6 条 `visible:false` 的 "Text here"、2 条 SVG 内文字与 1 条 placeholder 属性（脚本误报）、
  1 条 FAQ 里溢出容器不可见的残留文案（截图核实稿中确实不渲染，按铁律 3 不补）。
- **横向溢出**：375→1920 共 16 个断点，`scrollWidth - clientWidth` 全为 0。
- **几何**：桌面 9 项 / 手机 5 项与稿逐一比对全等（promo card 1062x528、vs table 924x448、
  faq row 624x45、手机 vs 块 350x302 等）；两端值区起点 Gumi/Others 均与稿一致。
- 首屏 `wowo` 元素最终 opacity 全部回到 1；`.product--page` 图区 `position: sticky` 生效。

### 文件清单

```
新增  pdp.html
新增  assets/scss/modules/{_promo,_vs,_faq}.scss
改    assets/scss/helpers/_mixins.scss          + ink-outline()
改    assets/scss/components/_scallop.scss      + 3 个配色
改    assets/scss/modules/_product.scss         + .product--page sticky / mobile 字号
改    assets/scss/modules/_reviews.scss         + .reviews--sand
改    assets/scss/modules/_science.scss         mobile 字号（删覆盖）
改    assets/scss/modules/_nutrition.scss       mobile 字号
改    assets/scss/style.scss                    + promo / vs / faq
改    figma/optimize-images.py                  GLOW 改 list、+ round_join、+ 3 条 JOBS
新增  assets/icons/promo-arrow-{1..6}.svg
新增  images/{bear-gummy,bear-gummy-glow,others-bottles,vs-bear-glow}.png
```

### 遗留

- **Reviews 整页（`real-customer-reviews`）只留 `data-app="reviews"` 占位壳**，按 app 边界不做。
- 占位字体（Figtree 代 PP Palma）导致换行位置与稿不同，几处 hug 高度比稿矮 4~15px
  （手机 others 块 268.5 vs 稿 279.5，promo stack 232 vs 256），属预期，不做像素级验收。
- `ink-outline` 在字母内孔仍有约 0.5px 的残留白点，1x/2x 屏下不可见；要彻底干净需改 SVG
  `<text stroke-linejoin="round">`，成本高，暂不做。
- Homepage 的 `.usp__value` 仍用 `-webkit-text-stroke`（同样的尖角问题），未统一到
  `ink-outline` —— 那块已验收，改动需重新走一遍 Homepage 的验证。
- PDP 的 sticky 只在 tablet 以上生效；稿没给 sticky 的偏移量，现用 `top: 24px`。

---

## 第五轮 — 全站交互态：hover + 过渡（2026-08-20）

用户把三条要求写进公约（已落到 `~/.claude/CLAUDE.md` 铁律 13）：
**hover 要有过渡、按钮/link/可点击处都要有 hover、整体动效要流畅**。
交互态既不在 Figma 稿里也不在 build spec 里，前四轮全程没人提 → 全漏。

### 改动

1. **`_variables.scss` 新增 motion token**：`$t-fast .15s` / `$t-base .2s` / `$t-slow .3s`、
   `$ease-out cubic-bezier(.33,1,.68,1)`（easeOutCubic）、`$ease-in-out`。
   稿里没有 hover/active 态，**这组是自定值，可整组调**。
2. **`_mixins.scss` 新增 `@include hover` 与 `trans()`**。hover 一律包 `@media (hover: hover)`，
   否则触摸屏点完 hover 态会粘住不还原。`trans(a, b)` 把属性列表展开成统一时长/曲线。
3. `.btn` 基类：`transition` 扩到含 transform / box-shadow，加 `&:active { translateY(1px) }`；
   `--primary` / `--lg` hover 改为加深底色 + 抬起 1px + 投影。
4. **header 7 处**：toggle / logo / icon / link / sublink 补 hover；`.nav-card` 整卡上浮 4px +
   投影（走 `$t-slow`，面积大），卡内箭头圆圈同步变 lime 并右移 3px；4 处硬编码 `ease` 换成 token。
5. **footer 5 处**：`footer-cta__btn` 补 hover（`.btn` 基类没有 hover，底色又被它覆盖）、
   logo / link / social-link / submit 补过渡；`.footer__legal-links a` 是**稿里的裸 `<a>`
   没有 class**，探针才发现漏掉。
6. **product 3 处**：`label-btn` hover 灌满绿底白字、`cta` 补过渡与抬起、
   `acc-row` hover 变色且 + 号放大 1.15（展开态图标形态稿里没有，不自造）。
7. **faq / hero / promo / reviews**：`faq__row` 与 `acc-row` 同构所以反馈一致；
   `reels__btn` 的 SVG 内联写死 fill，继承色改不动，反馈只能落在 opacity / transform。
8. **modal**：`nl-panel__close` hover 转 90°、`nl-tab` 未选中时 lime 下划线半透浮现。
9. 清掉 10 处冗余 `cursor: pointer` —— reset 的 `button {}` 与 `a[href]` 的浏览器默认已覆盖，
   只在 `.btn` 保留一份（它可能挂到非交互标签上）。

### 修掉的坑

| 症状 | 根因 |
|---|---|
| 7 类元素"有 hover 但瞬间跳变" | 只写 `:hover` 没写 `transition`，是最常见的半成品写法 |
| Privacy / Cookies 两条链接完全没反馈 | 稿里是裸 `<a>` 无 class，按 class 清点时看不见，靠探针遍历 `a[href]` 才抓到 |
| `.nl-panel__close` 编译告警 mixed-decls | 声明写在 `svg {}` 嵌套规则之后，Sass 1.77 会警告 |
| 探针报 `header__link` / `sublink` scroll 超时 | 取到的是 `--mobile` 那几个实例，桌面 `display:none` → rect 0x0。改成"取第一个 rect 非零的匹配"，并另开 390 宽**非触摸**视口测抽屉内元素 |

### 判据

- **锚点先验**：hover 规则包在 `@media (hover: hover)` 里，该查询若为 false 则所有断言恒假。
  探针启动先打印 `matchMedia('(hover: hover)').matches` = **True** 才继续。
- **hover 实测**：Playwright 遍历两页全部 `a[href]` 与 `button`，对每类元素 hover 前后各读一次
  computed style，比对 color / background-color / border-color / opacity / transform / box-shadow。
  **46 类元素全部有变化，`cursor` 全为 pointer，问题项 0**。
  hover 后等 450ms 再读 —— 虚拟时间不推进过渡，立刻读会拿到起始值。
- **隐藏元素补测**：header 面板内的先点开 toggle、`wowo` 未入场的先滚到底再回顶、
  弹窗内的先开弹窗；mobile-only 元素在 390 宽**不开 `has_touch`** 的视口测（等价于缩窄的桌面窗口）。
- **触摸端反证**：390x844 + `has_touch=True` 下 `(hover:hover)=False`、`(hover:none)=True`，
  `.product__cta` hover 无任何差异 —— 证明触摸屏不会粘住 hover 态。
- **删除后回归**：清掉 10 处 `cursor: pointer` 后重跑探针，46/46 仍为 pointer。

### 文件清单

```
改  assets/scss/helpers/_variables.scss   + motion token 一组
改  assets/scss/helpers/_mixins.scss      + @mixin hover / @function trans()
改  assets/scss/base/_reset.scss          注释说明 cursor 的唯一来源
改  assets/scss/components/_button.scss   基类过渡扩展 + :active + 两个变体 hover
改  assets/scss/components/_modal.scss    nl-panel__close / nl-tab
改  assets/scss/layout/_header.scss       toggle/logo/icon/link/sublink/nav-card + 曲线 token 化
改  assets/scss/layout/_footer.scss       cta-btn/logo/link/social/submit/legal 裸 a
改  assets/scss/modules/_product.scss     label-btn / cta / acc-row
改  assets/scss/modules/_faq.scss         faq__row
改  assets/scss/modules/_hero.scss        hero__btn
改  assets/scss/modules/_promo.scss       promo-card__btn 与 --light
改  assets/scss/modules/_reviews.scss     reels__btn
改  assets/css/style.css                  重新编译，4310 行，无 Sass 告警
```

### 遗留

- **抬起量、投影、时长全是自定值**（稿中无交互态），已集中在 `_variables.scss` 的 motion 段，
  设计方要调整改那一组即可，不必逐组件改。
- `.header__panel` 的展开仍是硬编码 `0.35s`（比 `$t-slow` 略长，面板高度大），未强行统一。
- 手风琴 / tab 的**展开态**（`aria-expanded="true"` 时图标该变成什么）稿里没有，未自造。
- 触摸端只有 `:active` 反馈，没有 hover —— 这是刻意的，真机上 hover 会粘住。

---

## 第六轮 — 客户验收反馈 10 项（2026-08-20）

用户审查前两页后给出 10 条。全部落地，判据见下。

### 改了什么

1. **PP Palma 到位**（试用包 `PP Palma - Free For Personal Use v1.0/`）。稿中 4 个字重里
   300/500/800 直接对上 Fizzy 三个文件；**400（PPPalma-Regular，占全站 59% 用量）试用包不提供**，
   改为在 Light(300) 与 Medium(500) 之间**插值生成** —— 501 个字形中 490 个逐点插值，
   11 个结构不兼容的（含 `$` `j`）回退 Medium 原轮廓。脚本随包留档。
2. **Hero 小熊不再被裁 + 去掉浮动**。PNG 原带 337px 透明边距，逼出"放大再裁"的写法，结果切掉了
   熊的头顶与脚底。图裁到墨迹（1200×927 → 528×874），`.hero` 改 `overflow-x: clip`
   让熊按稿溢出到下方白色区；浮动动效换 `.float-art--still`（只保留入场）。
3. **波浪全宽响应**。原来是固定 1596px 内联 SVG 居中，2580 屏上只有中间一段有波浪。
   改为 repeating radial-gradient 平铺：`--wave-w` 用 `clamp()` 随视口变化，
   在 390 与 1440 两个基准点都落回稿值，超过 1440 后波浪变宽并增多、**条高封顶**不推动布局。
   13 处内联 SVG 全部删除。
4. **hover 去掉位移与阴影**（用户公约新增）。12 处 `translateY` + `box-shadow` 移除，
   只保留配色变化；`:active` 的按下 1px 保留（触摸端唯一反馈）。
5. **描边改用 `ink-outline()`**。稿是 OUTSIDE/ROUND 描边，`-webkit-text-stroke` 是居中描边，
   向内吃掉一半 → 0/6 的内孔留下背景色斑点；且 Chrome 的 `paint-order` 按字符生效，
   g 的描边会压住旁边的 6。text-shadow 铺在整段文字下方，一体轮廓、内孔填实、标点也被包住
   （正是批注 `401:31482` 要求的）。
6. **`.science-card__value` 补描边**。稿 56px/7px OUTSIDE；原实现是个绝对定位的 lime 矩形条，
   把 % 号漏在外面。
7. **logo-scroll 不再裁切**。`object-fit: cover` 是元凶：ABC 那张是 400×400 画布里装 348×74 的字标，
   cover 把它缩成 193×193 塞进 65px 的框，字母基线被削 7px。三张图裁到墨迹，
   改为按**设计稿实测的墨迹高度**（34/36/40）排版，槽宽 193 + gap 30 不变。
8. **PDP gallery 做成 swiper**：主图 5 张横向 snap 轨道，缩略图列作为 nav（点击切换 + 高亮），
   缩略图超出时自身纵向滚动。sticky 本已存在，保留。
9. **reels 做成 slider**：稿里左右箭头画在同一个 SVG 里，拆成两个按钮并绑定滚动，端点自动禁用。
10. 顺带修掉装饰熊入场 `rotate(-5deg)` 在窄屏造成的 3–4px 瞬时横向滚动条。

### 修掉的坑

| 症状 | 根因 |
|---|---|
| 量到的 hero 几何全不对（447×622 而非 568×816） | 探针在入场动画播放中采样，读到 `matrix(0.68…)` 中间态。等待改 2600ms |
| 回归报 12 个断点横向溢出 | 同上，1300ms 时装饰熊还在 `rotate` 中；稳态为 0 |
| 首次二分定位溢出源，所有元素都"减少 4px" | 逐个 `display:none` 会触发重排，结果失真。改注入式 A/B 才定位到 deco-bear |
| 插值字体字宽变了、轮廓没变 | 只改 `charstring.program`，保存时 `bytecode` 缓存优先。须一并清 `bytecode = None` |
| 判据"400 落在 300 与 500 之间"为假 | 300/500/800 是 Fizzy 系列、400 是非 Fizzy，跨系列比字宽无意义。改用同系列三个 master 比 |

### 判据

- 字体：fontTools 层 25/25 字宽 + 10/10 墨迹面积严格居中；浏览器层同系列实测 t=0.495（目标 0.5）。
- 波浪：1440 下 tile 302.4 / 高 96.8（稿 302.19 / 96），390 下 144.64（稿 144.64），2580 铺满全宽。
- hover：34 个可点击元素类实测，位移残留 0、阴影残留 0；先验 `(hover:hover)=true` 才断言。
- 溢出：2 页 × 16 断点 = 32 个测量点，稳态与动画期均为 0。
- gallery/slider：点第 3 个缩略图 → scrollLeft=806=2×403、高亮 index=2；手动滚到第 5 张高亮反向同步。

### 文件清单

```
改  assets/scss/base/_fonts.scss           PP Palma 四个 @font-face + $pp-400-src 开关
改  assets/scss/components/_scallop.scss   整体重写为 radial-gradient 平铺
改  assets/scss/components/_motion.scss    + .float-art--still
改  assets/scss/components/_button.scss    去 hover 位移/阴影
改  assets/scss/modules/_hero.scss         overflow-x:clip、小熊尺寸定位、usp ink-outline
改  assets/scss/modules/_stats.scss        stat__value ink-outline
改  assets/scss/modules/_science.scss      science-card__value 改描边（删矩形条）
改  assets/scss/modules/_logo-scroll.scss  去 object-fit:cover，按墨迹高度排版
改  assets/scss/modules/_product.scss      gallery swiper（stage/thumbs 双滚动）
改  assets/scss/modules/_reviews.scss      reels 平滑滚动 + 按钮 disabled 态
改  assets/scss/modules/_promo.scss        去 hover 位移/阴影
改  assets/scss/layout/_header.scss         同上（nav-card）
改  assets/scss/layout/_footer.scss         同上 + footer-cta-wrap overflow-x:clip
改  assets/js/main.js                       + slider / gallery 两个模块
改  index.html / pdp.html                   删 13 处内联 SVG、gallery 与 reels 结构、图片尺寸属性
改  images/gumi-bear-front-glow.png         裁到墨迹 528×874
改  images/media-{abc-news,vogue,wellbeing}.png  裁到墨迹
新  assets/fonts/pppalma-*.woff2            6 个（含插值 Regular）
新  PP Palma …/make-regular-interp.py       插值脚本留档
备  figma/assets-raw/*.ORIGINAL.png         四张图的裁剪前原件
```

### 遗留

- **PP Palma 是 personal-use 试用版，且 400 是插值产物，都不可商用上线** ——
  需客户提供授权 web font（尤其 Fizzy 那一组）。切换点仍只有 `_fonts.scss`。
- 小熊按**高度**匹配设计稿，宽度因此比稿窄约 4%：我们的 PNG 比例 528:874，
  而 Figma 把它塞进 1109×913 的矩形做了垂直裁剪，两者比例不同，只能二选一。
- `ink-outline` 在 4~5 倍放大下边缘有轻微锯齿（36 步副本叠加），1x/2x 屏不可见，未加密。
- 宽屏波浪取的是"既加宽也增多"的折中（2580 下小波浪 6.5 个 / 大波浪 3.7 个，稿 1440 是 4.8 / 2.7），
  上限写在 `_scallop.scss` 的两个 `clamp()` 里，设计方若有偏好改那两个值即可。
- gallery 与 reels 的主图/卡片仍是稿中的灰色占位，接 Shopify 产品图后需复测 snap 与高亮。
- hero 高度仍比稿矮（741 vs 864），熊在版面中的相对位置因此偏上，属整体还原度问题，未动。

---

## 第七轮 — 字体解析 + 入场效果重排（2026-08-20）

### 改了什么

1. **移除 PP Palma 400 的 `local()`**。原来写的是
   `src: local("PP Palma"), local("PPPalma-Regular"), url(...)`。试用包里 12 个 OTF 的
   nameID 16（typographic family）**全都是 "PP Palma"**（`fc-list` 已证实：一个 family
   别名覆盖 Light/Medium/Heavy + 六个 Fizzy 切）。装了这套试用字体的机器上，
   `local("PP Palma")` 会命中整个家族，由平台决定给哪一张脸——Chrome/Windows 的 local()
   会按 family name 解析，于是**同一个页面在设计师机器上和别人机器上是两种字**，
   而且只有 400 会这样，因为只有它带了 `local()`。现在四个字重一律走 url()。
2. **word-pop 入场只留给 stats 的 `.stat`**。index 10 处、pdp 6 处 `data-pop-text` 全撤，
   改挂到四个 `.stat` 上；数字用新的 `data-pop-atom` 整块弹出。
3. **全站按容器铺 wowo 入场**：文字容器 `fadeInUp`、图片容器 `fadeIn`
   （index 19→34 个，pdp 12→26 个）。

### 修掉的坑

| 现象 | 真因 / 判据 |
|---|---|
| 「字体跟设计完全不一样，尤其是 regular」 | 本机复现不出（见下判据）。唯一与机器相关的路径是 400 的 `local("PP Palma")`，已删；并新增 `font-check.html` 让任何一台机器能直接量出四个字重实际落到哪个文件 |
| `data-pop-atom`：拆词会把描边拆断 | `.stat__value` 的 `6<span>g</span>` 若按词拆成两个 `.pop-word`，`ink-outline` 会各画一圈、中间留缝——正是第六轮第 5 条修过的那类问题。故整块弹出，不下钻 |

### 判据

- **字体没错**：设计稿 285:18162 的 hero 正文（PPPalma-Regular / 20px / -0.4）墨迹宽 **319px**，
  我们的插值件在同参数下 **320px**；同尺放大 4 倍逐字叠比，`R a g v ,` 形态一致。
- **字重没错**：把 Figma 的「文本 → fontWeight」与页面 computed font-weight 做连接比对，
  73 条可匹配文本里 66 条一致，7 条差异逐条回查 Figma 后确认是**比对脚本把 footer 链接(400)
  匹配到了 header 链接(500)**，实现侧无误。
- **实际用字**：CDP `CSS.getPlatformFontsForNode` 全页统计 = PP Palma 2652 字形 /
  Fizzy Medium 540 / Fizzy Heavy 447，与设计的 400/500/800 分布对得上。
- **local() 劫持已排除**：把 12 个 OTF 装进 fontconfig 后重测，页面内 `"PP Palma"/400`
  实测宽 322.20 = 插值件（Light 317.80 / Medium 326.70 / FizzyLight 292.45 / FizzyMedium 304.97），
  即 Linux 侧未被劫持；Windows 侧无法在本机复现，故直接删掉这条路径。
- **入场**：先给所有 `.wowo` 打 `data-was-wowo` 标记（wowo 播完会摘 class，不打标记断言恒真），
  滚完整页后 —— index 34 / pdp 26 个元素**最终 opacity 全部 = 1，无一卡在 `.wowo`**；
  横向溢出 1440/390 四组均为 0。
- **pop 归属**：`.pop-word` 共 63 个，**落在 `.stat` 之外的 0 个**；pdp 为 0 个。
  四个 `.stat__value` 均 `isWord=true / innerWords=0`，text-shadow 描边保留。

### 文件清单

```
改  assets/scss/base/_fonts.scss     删 400 的两条 local()，补原因注释
改  assets/js/main.js                popText 增加 data-pop-atom（整块弹出）分支 + stamp()
改  index.html                       pop 收归 4 个 .stat；新增 15 处 wowo 容器
改  pdp.html                         pop 全撤；新增 14 处 wowo 容器
新  font-check.html                  开发自检页（不属于站点），量四个字重实际命中哪个文件
```

### 遗留

- 「字体不一样」在本机（Linux/Chromium）复现不出，上面所有判据都指向实现与稿一致。
  若换机后 `font-check.html` 仍报「不符」或「加载失败」，把那张表发回来即可定位。
- 图片容器的 `fadeIn` 有两处是**嵌套**在卡片自身的 `fadeInUp` 里的
  （`.highlight-card__media`、`.promo-card__media` / `.promo-card__art`），
  两层 opacity 同时起跑、观感正常，但若嫌层次多可以只留卡片那层。

---

## 第八轮 — 字距 / 波浪几何 / hover / 手风琴（2026-08-20）

### 改了什么

1. **插值字体拆成两个系数**：形 `T_SHAPE=0.50`、距 `T_SPACE=0.31`。
   轮廓仍取 Light↔Medium 中点（笔画粗细对得上），推进宽与左承改取 31%，
   轮廓按左承差整体平移 —— 字形不动，只把间距收紧。
2. **波浪条高改由节距推导**，不再单独 clamp；节距的上限收到设计稿自身的值
   （小 302.19 / 大 524.74）。宽屏从此**保持设计尺寸、只是重复更多次**。
3. **hover 统一规则**：按钮 hover 一律翻到 lime 强调色（`$c-lime` + `$c-green-900` 文字），
   唯一例外是本就坐在 lime 上的 `.footer-cta__btn`，翻成白底绿字。
   链接加 `link-underline()` 下划线扫入（伪元素 scaleX，元素本身不位移）。
4. **手风琴做成真交互**：新 `components/_accordion.scss` + `main.js` 的 `accordion` 模块，
   FAQ 6 行 + PDP 规格 5 行 × 2 页共 16 行全部可开合。
5. **reels 改全屏宽度**，并在初始化时停在中点。

### 修掉的坑

| 现象 | 真因 / 判据 |
|---|---|
| 「半圆和半圆之间要贴在一起」 | 第六轮把条高单独 `clamp(...,96.8px)` 封顶，而弧高由节距决定（`amp = 0.24008 × 节距`）。1920 下节距已长到 698.9 → 需要 167.8px，条高只有 127.6 → **弧在合拢之前就被切掉**，波浪散成一个个孤立的鼓包。现在 `height: calc(var(--wave-amp) + var(--wave-band))`，两者不可能再脱节 |
| 导航链接下划线拉满整列 | `.header__link` 基础规则是 `display:flex; width:100%`；纯链接改 `inline-flex; width:auto`，子菜单容器与 `.footer__links` 改 `align-items:flex-start` |
| 手风琴行包了一层 wrapper 后所有分隔线消失 | `.product__acc-row:first-child` 原本指"容器里的第一行"，包进 `.product__acc-item` 后每行都是自己那层的第一个子元素。改成 `.product__acc-item:first-child &` |
| 首轮拟合插值系数得出 t 在 −0.36~0.30 乱跳 | 拿**光栅墨迹宽**去比**浏览器推进宽**，两者差一个右侧承（2~8px），与 Light→Medium 的总差（~10px）同量级。改成两边都量光栅墨迹宽后，四条样本一致落在 0.29~0.36 |

### 判据

- **字距**：同一阈值（亮暗中点）下量四条 400 字重整行，稿 / 我们 =
  318/318、204/205、634/633、626/627 —— 改前一律 +2~+3px。
  **墨迹覆盖率（＝笔画粗细）比值 1.000 / 1.009**，即只动了距、没动形。
- **波浪**：390 / 1440 / 1920 / 2580 四个视口 × 7 条波浪，条高 ≥ 弧高全部成立
  （改前 1920 与 2580 下的大波浪各差 40.2 / 40.5px）。
  ≥1440 时节距与条高恒为 302.2/95.9 与 524.7/128.0，稿值是 302.19/96 与 524.74/128。
- **hover**：42 类可点击元素实测（先断言 `(hover:hover)=true`），
  **无反馈的 0 类**；位移/阴影残留仍为 0。
  单测四个此前偏弱的：footer CTA 绿→白、promo light 白→lime、导航链接绿→#47ac00 且
  `::after` 的 scaleX 0→1、reels 箭头 opacity 1→0.75。
- **手风琴**：收起 0px/`hidden` → 展开 274px/`visible` → 再收起 0px；
  加号竖笔 transform = `matrix(1,0,0,0,0,0)`（scaleY(0)）；两页四组断点一致。
- **reels**：轨道 left=0、宽=视口宽（全出血）；1440 下初始 scrollLeft=88 / 最大 176，
  正是稿里 Reels Row `x=-88 w=1617` 的两侧等量出血。
- 回归：2 页 × 1440/390 共 4 组，横向溢出 0，`.wowo` 元素最终 opacity 全 1、无卡死。

### 文件清单

```
改  assets/scss/components/_scallop.scss   条高由节距推导；节距上限收到稿值
新  assets/scss/components/_accordion.scss 面板 0fr→1fr + 加号变减号图标
改  assets/scss/style.scss                 注册 accordion
改  assets/scss/helpers/_mixins.scss       + link-underline()
改  assets/scss/components/_button.scss    hover 翻 lime
改  assets/scss/layout/_header.scss        导航链接改色 + 下划线；子菜单列对齐
改  assets/scss/layout/_footer.scss        CTA 翻白、submit 翻 lime、链接下划线
改  assets/scss/modules/_hero.scss          按钮 hover 翻 lime
改  assets/scss/modules/_promo.scss         同上（含 --light）
改  assets/scss/modules/_product.scss       同上 + acc-item 包裹后的 first-child 修正
改  assets/scss/modules/_faq.scss           faq__row 补 cursor
改  assets/scss/modules/_reviews.scss       reels 去掉居中 padding，改全出血
改  assets/js/main.js                       + accordion 模块；slider 支持 data-slider-centre
改  index.html / pdp.html                   16 行手风琴结构 + 面板；reels 加 data-slider-centre
改  assets/fonts/pppalma-regular-interp.woff2   按新系数重生成
改  PP Palma …/make-regular-interp.py       形/距双系数 + 直接输出 woff2
```

### 遗留

- 手风琴面板里的 `Text here` 与灰块，是 Figma 组件 324:53921 自带的占位，不是我写的文案。
- 多行可同时展开（设计没给规则）。要改成一次只开一行，把容器上的
  `data-accordion` 写成 `data-accordion="single"` 即可，JS 已支持。
- 字距这一项本机量到的差只有 +0.16%~+0.63%，已按稿收平；若你那边看到的差比这大得多，
  多半不是这一层的问题，`font-check.html` 的表能直接定位。

---

## 第九轮 — 缓存版本号 + 构建自检（2026-08-20）

### 背景

第八轮四项改完后，反馈是「这些修改全都没有落实」。服务器侧逐项查过：三轮 41 项标记全在、
产物与源码逐字节一致、行为冒烟全绿、06:24 之后无任何写入（含 06:35 那次 Unison 同步之后），
两个并行 Claude 会话的 jsonl 里对本项目**零写操作**。也就是说**文件是对的，问题在「加载到的是哪一版」**。

真因锁定在这一条：`index.html` / `pdp.html` 引 `assets/css/style.css` 与 `assets/js/main.js`
**没有任何版本号**，字体 url 也没有。预览走的是 `file://`，浏览器会把 css / js / woff2
缓存到下一次硬刷新为止 —— 普通 F5 拿到的还是旧文件，于是四项改动会**同时**看起来像没做，
其中手风琴这种全新交互都不出现，只有缓存能解释。

### 改了什么

1. `_variables.scss` 加 `$build`；`:root { --build: "…" }` 把它暴露给 JS。
2. 两页的 `<link>` / `<script>` 和 `_fonts.scss` 里 14 个 woff2 url 全部带上 `?v=$build`。
3. `font-check.html` 从「字体自检」扩成**构建自检**：先报版本号，再逐条探测本轮改动在不在
   （波浪 `--wave-amp`、`.acc-panel`、`link-underline`、reels padding、`ink-outline`、
   `object-fit`、`window.gumi.accordion / slider / gallery / popText`），最后才是字体表。
   顶部一条横幅直接给结论。

### 修掉的坑

| 现象 | 真因 / 判据 |
|---|---|
| 改了但页面没变 → 被判成「没改」 | `file://` 下无版本号的 css/js/woff2 被浏览器缓存。加 `?v=`；实测 `file://` 带 query 仍能取到文件（requestfailed 为空，四个字重全部 loaded） |
| 自检页报 300/400/500 三个字重「对不上任何文件」，且三个数一模一样 | `@font-face` 是惰性的，量的时候页面自己的 PP Palma 还没下载完，量到的是 fallback 宽度。补 `document.fonts.load(w + ' 40px "PP Palma"')` 后四项全过 |
| 波浪那一项在 ≤1440 看不出变化 | 第八轮那个 bug 只在 **≥1920** 才发作（1440 及以下旧写法本来就贴合）。1280/1366/1440/1536/1600/1920/2560 七个宽度实测，条高 ≥ 弧高全部成立 |

### 判据

- 自检页横幅：**全部通过**（版本 20260820-r8；10 条功能探针全「在」；4 个字重全「通过」）。
- 回归：2 页 × 1440/390，溢出 0、`.wowo` 无一不可见/卡死、波浪几何全对、
  reels 全宽且停中点、手风琴 0→274→0。
- 产物与源码逐字节一致。

### 文件清单

```
改  assets/scss/helpers/_variables.scss   + $build 构建戳
改  assets/scss/base/_reset.scss          + :root{--build}
改  assets/scss/base/_fonts.scss          14 个 woff2 url 带 ?v=；@use variables
改  index.html / pdp.html                 css/js 引用带 ?v=
改  font-check.html                       扩成构建自检（版本 + 10 条功能探针 + 字体表）
```

### 遗留

- **`$build` 要手动往前推**：改完样式/脚本后同时更新 `_variables.scss` 的 `$build`
  与两页 `?v=` 的值（三处）。没有构建流程，只能这样。

---

## 第十轮 — 任务文档 8 项（2026-08-20）

用户给了 `修改任务文档.txt`，8 条。全部落地。两条是此前没发现的真 bug（promo 小熊
与全部标签的旋转方向反了、hero 小熊漏了稿里的倾斜），一条改了实现路线（手风琴脱离 JS）。

### 改了什么

1. **logo 条真无缝**。旧写法是一条 12 项的轨道位移 `-50% - 15px`（＝ 1338px），可轨道
   总宽只有 2646 —— 位移完右边只剩 1308px 的内容，视口一超过 1308 就露白，1440 下已经
   差 132px。改成 8 组 × 3 个 logo，每组自带 `padding-right: 30px` 把接缝并进节距，
   动画位移 `translateX(-100%)` ＝ 正好一组 669px。节距固定 → 速度不随视口变，
   要保证的只是「轨道比视口多出一组」，8 组＝ 4683px 的余量，过 4K 都够。
2. **PDP 缩略图顶部 + 右侧对齐**。稿 324:52658 把缩略图列放在 465 列**外面**
   （x = 列左 − 62），主图占满 465，右边缘与下方「View Nutritional Label」齐平。
   原实现让它在流内，吃掉 62px，主图只剩 403 —— 比按钮窄一截就是看到的症状。
   改成绝对定位挂在 `right: calc(100% + 14px)`、`top: 0`（稿里两者 y 都是 922，不是原来的垂直居中）。
   ≥1120px 才外挂（低于这个宽度左边放不下 62px 的外伸），1024 及以下按手机稿
   324:53792 改成主图下方的横排 52px 缩略图带。
3. **promo-art 拍平成一张图**。`images/promo-art.png`（1413×1209，3x，带 alpha）。
   Figma 导出端点仍在账号级 429，图是本地渲染的：`figma/promo-art-source.html`
   ＋ `figma/render-promo-art.py`。四周各留 5%（标签光晕会溢出组的 bbox），页面侧
   `left/top:-5% + width/height:110%` 放回稿的 427.4×365.7 上。
4. **手风琴改原生 `<details>/<summary>`**。反馈是「根本点不开」，而本机怎么测都能开
   —— 能同时解释两者的只有「开合这件事挂在两个都可能失手的环节上」：main.js 得加载到，
   浏览器还得把 `grid-template-rows: 1fr` 在不定高容器里算成内容高。`<details>` 把两个
   环节都拿掉：开合、键盘、a11y 树都交给浏览器，动画退成纯增强
   （`::details-content` + `interpolate-size`，浏览器不支持就瞬开，不会不开）。
   16 行（FAQ 6 + PDP 规格 5 × 2 页）全部改完，JS 完全禁用下实测仍能开合。
5. **页脚区去 wowo**。`<footer>` 3 处 + 上方绿色 CTA 区 `.footer-cta` 4 处，两页共 14 处，
   全部去掉 `wowo fadeIn/fadeInUp/delay-in-N`。header 里本来就没有。
6. **PP Palma Regular 插值件修到 494/501**。原来 490 个字形插值、11 个回退成 **Medium
   原轮廓** —— 回退＝在一段 t=0.31 的文字里混进一个 t=1.0 的字，肉眼看得出来，而
   `j` 出现在 juicer / enjoy / Join 里。这 11 个里有 4 个（j / ij / uni0237 / eng）
   其实不是不兼容，只是两个 master 差一个收尾冗余点（Light 的 j 竖笔多一段
   (336,0)→(335,0)）。脚本改成「对不上时才抹掉 <3 单位的线段再比一次」，
   `j` 的推进宽从 524（Medium）回到 491（t=0.31，与 a/n/o/H 同一个 t）。
   剩 7 个是 Uogonek / ae / aeacute / ae.ss04 / cent / dollar / uni20B2，构造真的不同
   （Light 的 $ 是三条轮廓、Medium 是一条），其中只有 `$` 出现在站上，一次，占位价格里。
7. **reels 改无限循环**。克隆式而非 transform 式，为的是原生触摸滚动、惯性和 snap 全都还在：
   整组重复到两侧各有一整组余量，滚动停下 120ms 后按整组宽平移回中带。一组 1640px，
   一次甩动跑不出去；只在停下时平移，所以不会截断惯性。箭头不再有禁用态。
   居中改成「把某张卡的中心对到视口中心」再算，1440 下自动得到稿里 Reels Row
   `x=-88 w=1617` 的两侧 88px 出血，别的宽度也自洽。
8. **hero 小熊改挂 `.hero__inner` 并按稿倾斜**。两件事：
   - `.hero__inner` 补 `position: relative`。稿把画框放在 1440 宽的 Page Header 里
     （x=759.98, y=14），原来挂在全宽的 `.hero` 上，1920 屏上小熊比稿多往右跑 240px。
   - 小熊本来就是斜的：Figma 节点 332:16444 的 relativeTransform
     `[[.99046,-.13782],[.13782,.99046]]` ＝ CSS `rotate(7.92deg)`，手机稿 228:5932 是 −15deg。
     568×816 那个框其实是**倾斜后的外接盒**，不是画本身。

### 修掉的坑

| 现象 | 真因 / 判据 |
|---|---|
| promo 小熊跟稿对不上，标签也偏 | 旋转**方向反了**。节点 relativeTransform 换算成 CSS 是 `+18.52deg`（顺时针），写成了 `-18.5deg` —— 整整差 37°；6 个标签的 `--r` 也全是反号。改完与稿叠图除字距外完全重合 |
| 第六轮记的「Figma 把小熊竖向裁了、宽度只能差 4%」 | 也是同一个坑的副产品。当时把**倾斜后的外接盒** 535.8×785.6（比 0.682）当成了画本身，跟我们文件的 0.604 对不上，于是判成裁剪。反算回未旋转是 439.1×732.06 ＝ 0.5998，与我们的 528/874 差 0.7%。不是裁剪，是漏了倾斜，那 4% 随之消失 |
| promo 标签「Whole / Super / Gut health」第一行下半截被啃掉 | `ink-outline()` 在**多行**上会自相残杀：Chrome 逐行画「行 1 阴影→行 1 字→行 2 阴影→行 2 字」，18.09px 行距配 8.37px 光晕，行 2 的光晕正好压在行 1 的字上。拆成两层（元素画光晕+透明字，叠一层只画字）后干净。经验值写进 `ink-outline()` 注释了 |
| 一度以为 `.promo-card__title--outlined` 也中招 | **是我量错**：Playwright 的 `element.screenshot()` 按边界盒裁，descender 本来就在盒外。带 16px 留白重截，单层写法本来就是好的（36px 行距扛得住 11.25px 光晕），已把多余的改动撤回 |
| 首轮验 FAQ 判成「点不开」 | 也是探针写错：`document.querySelector('.acc-panel')` 在 PDP 上先命中的是规格行那一组，不是 FAQ 那一组。换成 `按钮.nextElementSibling` 后 0→274→0 正常 |

### 判据

- **logo 无缝**：390/768/1024/1440/1920/2580 六个宽度，位移一组后剩余轨道 4683px ≥ 视口，全部成立；节距 669、时长 15s 恒定。
- **缩略图**：≥1120 顶对齐 Δ=0、主图右边缘与按钮右边缘 Δ=0、缩略图列 x=180.5（稿 181）；≤1024 转横排且 `document.scrollWidth == 视口`（无外伸溢出）。
- **手风琴**：FAQ 45→319→45、PDP 规格 24→298→24；**`java_script_enabled=False` 下仍 45→319**。
- **页脚**：两页 footer 区 `.wowo` 计数 = 0，header = 0；整页其余 wowo 保留（index 27 / pdp 19）。
- **字体**：`j` 推进宽 476(L) → **491** ← 524(M)，t=0.31 与 a/n/o/H 同值；回退数 11 → 7；`font-check.html` 四个字重全部命中期望文件。
- **reels**：连点 next 14 次、prev 20 次，每步恰好一个节距、全程落在 [0.5, 1.5] 组宽的回绕带内、无一步卡住、两个按钮始终可用；1440 下卡中心对齐误差 0.00px。
- **hero**：`offsetParent` = `hero__inner`，1440/1920/2580 三档「画框右边缘距 inner 右边缘」恒为 112（稿 111.97）；小熊 computed 旋转 7.92°/手机 −15°；用**光晕左右耳尖高差**反算倾角，稿 7.39° vs 本站 8.06°，差 0.67°。
- **回归**：2 页 × 11 个宽度（375→2560）= 22 组，横向溢出全 0，滚完整页后 `.wowo` 无一卡在 opacity<1。
- 产物与源码逐字节一致（`sass` 重编后 `diff` 无输出）。

### 文件清单

```
改  assets/scss/modules/_logo-scroll.scss   改 8 组 × translateX(-100%) 无缝循环
改  assets/scss/modules/_product.scss       缩略图外挂 right:calc(100%+14px)/top:0；≤1024 转横排
改  assets/scss/modules/_promo.scss         promo-art 改单图 + .promo-art--live 保留生成源；小熊旋转改 +18.52deg
改  assets/scss/modules/_hero.scss          hero__inner 补 relative；hero__bear 加 7.92/-15deg 倾斜并重算尺寸
改  assets/scss/components/_accordion.scss  重写为原生 details/summary；acc-panel* → acc-body*
改  assets/scss/helpers/_mixins.scss        ink-outline() 补多行互相遮挡的警告与经验值
改  assets/scss/helpers/_variables.scss     $build → 20260820-r10
改  assets/scss/base/_fonts.scss            更新插值件说明（494/501、剩余 7 个、$pp-400-src 换真文件的路子）
改  assets/js/main.js                       slider 加 data-slider-loop（克隆 + 静默回绕）；删掉 accordion 模块
改  index.html                              logo 条 8 组；5 行手风琴改 details；页脚去 wowo；?v=
改  pdp.html                                promo-art 换单图；16 行手风琴改 details；标签 --r 全部改号；页脚去 wowo；?v=
改  font-check.html                         版本号 + 探针改到第十轮（details / logo 循环 / hero 倾斜 / promo 单图）
改  assets/fonts/pppalma-regular-interp.woff2   按新脚本重生成
改  PP Palma …/make-regular-interp.py       对不上时先抹冗余点再比，回退 11 → 7
新  images/promo-art.png                    1413×1209 @3x，带 alpha
新  figma/promo-art-source.html             promo-art 的导出源（不进交付）
新  figma/render-promo-art.py               上面那页的渲染脚本
```

### 遗留

- **promo-art 现在是位图**：文案不可选中、不可在主题编辑器里改、换字体要重出图。
  拿到没限流的 Figma token 后可以直接导 Group 45（`I332:20251;332:20584`）@3x 覆盖同名文件，
  约定只有一个 —— 四周各留 5%。要退回活文字也只需把 `figma/promo-art-source.html` 里那段
  markup 贴回 pdp.html 并加上 `promo-art--live`。
- **手风琴展开动画是 Chrome 路线**：`::details-content` + `interpolate-size`。Firefox / Safari
  上目前是瞬开瞬收，功能不受影响。要三家都有动画只能回到 JS 测高度那条路。
- **`$` 仍是 Medium 轮廓**（PDP 占位价格里那一个）。Light 的 `$` 是三条轮廓、Medium 是一条，
  没法插值，只能等授权字体。
- PDP 缩略图外挂的 1120px 门槛是算出来的（`.product__inner` 995 + 20 padding，
  列左 = (W−995)/2 + 20 ≥ 62 → W ≥ 1080，取 1120 留 20px 余量）。若版心改了要跟着改。
- reels 的回绕在滚动静止 120ms 后发生；克隆卡片带 `aria-hidden`，接真实视频后要确认
  克隆体里的 `<video>`/懒加载不会重复请求。

---

## 第十一轮 — 任务文档 3 项（2026-08-20）

`修改任务文档.txt` 换了新的一批，3 条改动 + 1 条「继续做页面」。三条全部落地，
其中两条查出来的真因跟报上来的现象不是一回事。

### 改了什么

1. **`6g` 的描边不再啃掉 `6`**。反馈是「g 的 text-stroke 影响 6」，实测确认：
   `6<span class="stat__unit">g</span>` 里那个 span 是**独立的绘制单元**，Chrome 按
   「6 的光晕 → 6 的字 → g 的光晕 → g 的字」这个顺序画，7.05px 的光晕于是压在
   已经画好的 6 上，把右缘和字腔各啃掉一块。跟第十轮 promo 标签**多行**互相残杀
   是同一个机制，只是从跨行换到了同一行内。
   解法同样是拆两层，新加 `ink-split()` mixin：底层整串画光晕、字透明（g 的光晕
   在那层仍盖着 6 的光晕，但同色看不出来），顶层整串只画字。
   ⚠ 光晕层必须 `z-index: -1` + 父 `isolation: isolate` —— 定位子元素默认画在父的
   在流文字**之上**，第一版没加，整个数字变成一坨浅绿。
   `.usp__value`（hero 的 6g）中的是同一个坑，一并修；`.stat__value` / `.usp__value`
   共 7 处**全部**加了 halo 层，因为 mixin 把 `text-shadow` 归零，只改带 span 的那两处
   会让 60+ / 21 / 10+ 的光晕整个消失。

2. **PP Palma 400 的「间距过大」= 全站唯一一个非 Fizzy 字面**。
   稿里 300 / 500 / 800 全是 **Fizzy** 切（FizzyLight / FizzyMedium / FizzyHeavy），
   只有 400 写的是 **PPPalma-Regular**——因为 Pangram Pangram **根本没出 Fizzy Regular**，
   设计师要 400 只能选常规那支。而常规family 比 Fizzy 宽约 4%，于是 400 成了页面上
   唯一一档松排的字，实测**比它旁边的 500 还宽**（72 字符行 617 vs 603）。
   改成用两个 **Fizzy** master 插值（t = 0.50 两轴，400 正是 300 与 500 的中点），
   落在 595 —— FizzyLight 587 < **595** < FizzyMedium 603，四个字重终于单调。
   `make-regular-interp.py` 已参数化（`PP_LIGHT` / `PP_MEDIUM` / `PP_T_SHAPE` /
   `PP_T_SPACE` / `PP_PSNAME` / `PP_SUBFAM`），旧的非 Fizzy 插值件原样保留，
   `$pp-400-src` 一行可切回。

3. **reels**：
   - **nav 还原设计**。稿 `Frame 992460` 是 **90×40、itemSpacing 10**，那个 90 是
     **整条 nav** 的宽（40 + 10 + 40），里面每个 `action` 是 40×40 的圆。第六轮把
     原本一整张 90px 的箭头图拆成两个按钮时，`svg { width: 90px }` 留在了原地 ——
     于是每个圆都被拉成 90×40 的椭圆。改成 40×40 + gap 10；手机稿是 72×32 /
     按钮 32×32 / gap 8，一并补上。
   - **reel 可点开视频弹窗**。5 个 `.reel` 由 `div` 改 `button`，挂 `data-modal="reel-video"`，
     复用既有 modal 模块（Esc / 遮罩 / 焦点陷阱全都现成）。⚠ **稿里没有这个弹窗**，
     外壳是按现有弹窗语言自造的（居中淡入 + 缩放，而非营养标签那种底部上滑），
     **待设计方确认**；里面仍是稿自己的灰底 + play 占位，不塞假视频。
   - **鼠标可拖动**。只接管 `pointerType === "mouse"`，触摸照旧走原生滚动（惯性和
     snap 都还在）。超过 5px 才算拖动，拖动期间加 `.is-dragging` 关掉 snap，松手
     还给 CSS 去归位；拖完那一下 click 被吞掉，否则每次拖动结束都会弹出弹窗。
   - 顺带修了**手机端 reel 尺寸**：稿 228×405 / gap 16，之前是 240×426 / gap 24。
   - loop 的克隆体现在会把内部可聚焦元素设 `tabIndex = -1` —— reel 变成 button 之后，
     `aria-hidden="true"` 的克隆里躺着 5 个可 Tab 到的按钮就是个 a11y 陷阱。

### 修掉的坑

| 现象 | 真因 / 判据 |
|---|---|
| 「g 的描边影响 6」 | 不是 stroke 的宽度问题，是 **inline 子元素自成绘制单元**。判据：把 `.stat__unit` 的 `text-shadow` 单独设成 none，6 立刻完整（但 g 就没描边了）—— 两张 6× 放大图并排看得一清二楚 |
| 拆两层后整个数字变成一坨浅绿 | 定位子元素画在父的在流文字**之上**。`z-index:-1` + `isolation:isolate` 才落到字下面 |
| 「PP Palma 400 间距过大」 | **不是字距做错了**。215 个单行样本比对下来我们**没有一个超过稿宽**（最大 0.996），20 个定宽段落的断行 19/20 与稿一致（剩下一个是探针没处理 U+2028）。真因是**系列混用**：稿里只有 400 落在非 Fizzy 家族，比周围宽 4% |
| 圆形箭头被压成椭圆 | 90 是**整条 nav** 的宽不是单个按钮的。判据：改完实测 `navTotal = 90`、`navGap = 10`、按钮 40×40，与稿三个数全对上 |
| 回归探针报「23 个 wowo 卡住」 | **探针写错**：一次 `scrollTo` 跳到底，中间元素从没进过视口，`wowo` 自然不会触发。改成 400px 步进滚动后 16 组全 0 |

### 判据

- **6g**：7 处数值层 `text-shadow: none` + halo 层 72 段光晕、`color` 透明、
  `z-index:-1`，halo 与父的 rect 三个方向偏差全 0.00；6× 放大图对照，右缘与字腔完整。
- **字体**：自检页四个字重全部命中期望文件；宽度序列 817.97(300) → **832.39(400)**
  → 845.86(500) → 884.67(800) 单调。切换前后 A/B：桌面 1440/1920 高度**零变化**，
  窄屏 390/768/1024 各减 22~46px（都是某个段落少一行），无破版。
- **reels**：桌面按钮 40×40 / gap 10 / 总宽 90、reel 304×540 / gap 24；
  手机按钮 32×32 / gap 8 / 总宽 72、reel 228×405 / gap 16 —— 与稿逐项一致。
  点击开弹窗、Esc 关、拖 240px 得 Δ+224 且 `is-dragging` 在、松手清除、
  拖完不误开弹窗、拖完再点击照常开、克隆体中 `tabIndex !== -1` 的数量为 0。
- **回归**：2 页 × 8 个宽度（375→2560）渐进滚动，横向溢出全 0、`.wowo` 无一卡住。
- 自检页 15 条功能探针全「在」，版本 20260820-r11。
- 产物与源码逐字节一致。

### 文件清单

```
改  assets/scss/helpers/_mixins.scss        + ink-split()（两层描边，含 z-index 的坑）
改  assets/scss/modules/_stats.scss         .stat__value 改用 ink-split
改  assets/scss/modules/_hero.scss          .usp__value 改用 ink-split
改  assets/scss/modules/_reviews.scss       nav 40/32 + gap 10/8；reel 手机 228×405；
                                            reel hover/active；.is-dragging 关 snap
改  assets/scss/components/_modal.scss      + .rv-modal 视频弹窗外壳（自造，待确认）
改  assets/scss/base/_fonts.scss            $pp-400-src → fizzy-regular-interp + 缘由
改  assets/scss/helpers/_variables.scss     $build → 20260820-r11
改  assets/js/main.js                       slider 加鼠标拖动 + 克隆体 tabIndex=-1
改  index.html / pdp.html                   7 处数值加 .ink-halo；5 个 reel 改 button；
                                            + #reel-video 弹窗；?v=
改  font-check.html                         版本 r11；探针换到第十一轮（ink-split /
                                            nav 40 / 拖动态 / rv-modal）；字体期望改 Fizzy
新  assets/fonts/pppalma-fizzy-regular-interp.woff2   Fizzy 两 master t=0.5 插值
改  PP Palma …/make-regular-interp.py       masters 与 t 改为环境变量可覆盖
```

### 遗留

- **reel 视频弹窗稿里没有**：居中淡入 + 缩放、0.28s、遮罩 `rgba(1,19,7,.78)` 全是自定值，
  待设计方确认。里面是稿自己的灰底 + play 占位，接到真视频后换掉 `.rv-panel__video`
  即可；届时要确认 loop 的克隆体里不会重复请求视频。
- **400 现在有意偏离稿的字面**：稿写 PPPalma-Regular，我们用 Fizzy 插值件。拿到客户
  授权的 web font 后，如果对方给的是真 PPPalma-Regular，要重新决定跟哪一边 ——
  跟稿就会重新出现「400 比 500 宽」。
- 非 Fizzy 的 `pppalma-regular-interp.woff2` 与两个 plain master 仍保留在 `assets/fonts/`，
  只为 `$pp-400-src` 可切回；正式交付时可删（约 100KB）。
- `$` 仍是 Medium 轮廓，且 Fizzy 版回退字形从 7 个变成 9 个
  （多了 eogonek / uni20BF，都是站上不出现的 Latin-ext 与货币符号）。

### 补记（同日，r12）— 客户端字距异常的排查与加固

反馈：首页 hero 引导段在对方浏览器里被撑成 4 行、字距极大（截图），而同屏的
标题 / 按钮 / `60+ 21 6g` 全部正常 —— 差别是那段是 **400 字重**。

**服务器端复现不了**：1440 与 1280 下都是 380px 宽、**2 行**、`letter-spacing` 计算值
`-0.4px`、`document.fonts.check('400 20px "PP Palma"')` 为 true，与稿一致。
拿对方截图里 `60+ / 21 / 6g` 的间距（稿 110+20）标定缩放后反推：容器宽约 405px（对），
字高行高都对，**只有每字符推进 ≈25px（应为 8.5px）** —— 多出的约 15px/字不可能来自
本站 CSS（那里写死 -0.4px），也不是换字体能产生的量级。

字体文件本身逐项比对过原厂 FizzyMedium：`unitsPerEm` / `hhea` / `OS/2` 全部一致，
advance 中位 1160（原厂 1176）、max 2708（原厂 2723）、cmap 389 = 389，无异常字形。

仍做了三件加固：

1. **修掉我自己引入的 name 表不规范**：`nameID 2`（subfamily）只允许
   Regular / Italic / Bold / Bold Italic，我写成了 `Fizzy Regular`。原厂的做法是
   `nameID 1 = "PP Palma Fizzy Medium"`、`2 = "Regular"`、`16 = "PP Palma"`、
   `17 = "Fizzy Medium"`，已照此重写并重新生成。
2. **400 的 `@font-face` 给两个 src**：新文件读不到时退到旧的插值件，而不是整段
   掉出 PP Palma 家族。这一条很关键 —— 标题是 500/800 照常渲染，**只有正文掉队**，
   看起来就特别像「字距 bug」而不是「字体丢了」。
3. **自检页加第 4 节「正文 400 实际排版」**：量那一句在 380px 容器里的行数与
   每字符推进，直接分流成「字体没加载」/「字体命中对了但字距被撑开」两种判定；
   样张区末尾加一行**完全不用 PP Palma 的对照** —— 两行都被撑开 = 浏览器或系统层面
   （字体/可读性设置、阅读增强类扩展），只有 400 那行被撑开 = 字体文件。

```
改  PP Palma …/make-regular-interp.py       name 表按原厂约定（nameID 2 固定 Regular）
改  assets/fonts/pppalma-fizzy-regular-interp.woff2   按上条重新生成
改  assets/scss/base/_fonts.scss            400 的 @font-face 双 src 兜底
改  font-check.html                         + 第 4 节排版探针；样张加系统字体对照行
改  assets/scss/helpers/_variables.scss     $build → 20260820-r12
改  index.html / pdp.html                   ?v=
```

**待对方回报**：自检页第 4 节的判定 + 最底下对照行的样子；以及浏览器 / 系统、
是否 `file://` 本地打开、有没有阅读增强或翻译类扩展。

### 补记二（同日，r13）— 结论反转：插值件在客户端不可用，400 降级到原厂文件

对方发回自检页截图，直接推翻上一条补记的结论：**样张里 300 / 500 / 800 与「完全不用
PP Palma」的对照行全部正常，唯独 400 那行是等宽 + 字距撑开**。按自检页自己写的判据，
这就是**字体文件的问题**，不是浏览器设置。

**为什么前面一路测都是绿的** —— 第 3 节「四个字重命中哪个文件」的判据有缺陷：它把
页面渲染出的宽度，跟**同一个文件**单独加载后的参照宽度比。文件坏了，两边一起坏，
比对当然自洽，于是报「命中正确」。正是 [[probe-must-compare-against-invariant]] 那条：
两个比对量共享同一污染源时，自洽 ≠ 正确。

**故障形态**：face 被浏览器接受（不是 404、不是解析失败），但里面一个字形都画不出来，
于是整段落回退到系统 last-resort 等宽字体；而标题是 300/500/800，用的是原厂文件，
照常渲染 —— 所以看起来像「只有正文字距坏了」。也因此**双 src 兜底无效**（文件没
「失败」，fallback 永远不会触发），上一条补记加的第二个 src 已撤回。

回头看，对方最早那句「PP Palma regular 间距过大，可能是字体原因」说的就是这件事：
**非 Fizzy 的旧插值件在他们机器上同样不可用**，一直显示的就是等宽兜底。本机 Linux
Chrome 两个插值件都能正常渲染，所以从第七轮起就没被发现。

### 改了什么

1. **400 降级到原厂真文件** `pppalma-fizzy-light.woff2`。代价是 300 与 400 同款，
   正文比稿细一个字重档；换来的是**一定画得出字**。
2. **自检页加第 5 节「生成流程诊断」**，四行一条链，把生成流程切成三刀：
   ① 原厂文件 → ② 仅用 fontTools 重存 → ③ 重存 + 用 RecordingPen/T2CharStringPen
   重写每个字形（坐标不变，本应与①一模一样）→ ④ 真正的插值件。
   对方指出从哪一行开始坏，就锁定是哪一步的问题。
   已知线索：③ 比 ② 小 4KB（12%）—— `RecordingPen` 不记录 hint 操作符，
   重写会丢掉全部 CFF hinting。

```
改  assets/scss/base/_fonts.scss      $pp-400-src → fizzy-light；撤回双 src；写清故障形态
改  font-check.html                   + 第 5 节生成流程二分；WANT 的 400 改回真文件
改  assets/scss/helpers/_variables.scss   $build → 20260820-r13
改  index.html / pdp.html             ?v=
新  assets/fonts/diag-a-resave.woff2    诊断样本（仅重存），定位后可删
新  assets/fonts/diag-b-rewrite.woff2   诊断样本（重写轮廓），定位后可删
```

### 遗留

- **插值路线待定**：等对方回报第 5 节是哪一行开始坏。若 ③ 就坏 → 不能再用
  RecordingPen → T2CharStringPen 这条路重写 charstring；若只有 ④ 坏 → 是插值逻辑。
  在定位之前**不要再生成新的插值件**，否则又是一轮盲改。
- 一个不动轮廓的备选路线：取 FizzyLight 原文件，**只改 hmtx 与 charstring 首位的
  width**，轮廓指令一字不动 —— 字形仍是 Light 的（偏细），但字距可以调到 400 的位置，
  且完全没有重写轮廓的风险。
- 根本解仍是**向客户要授权的 PP Palma Regular**。
- 两个 `diag-*.woff2` 与两个插值件都不进正式交付。

## 第十二轮 — 内页开工：Science / Reviews / How Gumi Works（2026-08-20）

任务文档第 4 条「按顺序进行接下来的页面搭建」。九个内页里先落三个，两端同步做。
开工前按 memory 的要求跑了一次跨页文本 diff，结论是内页大半由既有模块拼成：
header / footer-cta / footer / `.product` / `.reviews` / `.faq` / `.app-slot` 全部原样复用，
真正新写的只有五个模块。

### 改了什么

1. **新页面三张**：`science.html` / `reviews.html` / `how-gumi-works.html`。
   页面外壳由新脚本 `figma/new-page.py` 从 `index.html` 现切现拼 —— 静态站没有模板引擎，
   十一个页面各存一份 header/footer，手抄迟早漂移。`--resync` 可以把 header 的改动推给所有内页。

2. **新模块五个**：
   - `layout/_page-hero.scss` —— 九个内页共用的页头。桌面左文右图，手机把图挪到文字**上方**
     （`column-reverse`，不是简单堆叠）。变体：`--center`（How Gumi Works，无媒体列）、
     `--text`（后续四个文本页）、`__overline`（Reviews 的星标行）、`__lead--lg`。
   - `modules/_compare.scss` —— Science 的 us VS Them。与 PDP 的 `.vs` 不是同一个块。
   - `modules/_ingredients.scss` —— 成分辐射图。**图形与 PDP promo 卡是同一份合成图**，
     直接复用 `images/promo-art.png` + `.promo-art`，没有重做。
   - `modules/_faq-image.scss` —— 带图的手风琴区，行为复用 `components/_accordion.scss`。
   - `modules/_expert.scss` —— Reviews 的专家推荐卡；手机稿把三张排成 947px 宽，是横滑轨。
   - `modules/_dosed.scss` —— How Gumi Works 的两个图文块，弧形眉题复用 `.arc-text`。

3. **`components/_scallop-box.scss`（通用扇贝方块）**。Science 的 520 底盘与 How Gumi Works
   的 597 图框是**同一个形状**（归一化后 alpha 差异 0.0），所以一份 mask 服务全部，
   `--box-bg` 控制占位色，图片被裁成扇贝形。

4. **`.science-card` 按手机稿修正**：padding 24 → **20**，eyebrow 手机 16 → **14/0.56**，
   新增 `__body` 内层（桌面 gap 16 / 手机 12）—— 手机稿的卡内间距与卡外间距本来就不同，
   flat 结构表达不了。**index.html 的三张卡同步改了结构**。

5. **`tools/shoot.py`**：全页截图 + 横向溢出 + 卡住的 `.wowo` 两项探针，`--all` 跑全站。

6. 新增 `.btn--xl`（220x60/18px）、`.reviews--cream`、四个 scallop 配色、`$c-coral`。

### 修掉的坑

| 现象 | 真因 / 判据 |
|---|---|
| 扇贝底盘整块不见，元素还在 | **`file://` 下 CSS mask 引用文件被 CORS 拦掉**（origin 为 null），mask 静默解析成空，把被遮罩的元素一起带走。客户就是双击打开预览的，线上正常掩盖不了这点。两个 mask 全部内联进 `helpers/_masks.scss`（PNG 降到 320px 再 base64，SVG 直接 URL 编码），CSS 从 104K 到 125K |
| 对比表比稿高 7px | Figma 的 LINE 是**高度 0 的子项**，照抄成 `border-top` 会给每行加 1px。改用 `::before` 画线，行高回到 64（手机 48），面板 540 / 432 与稿逐项一致 |
| 标题、正文出现「重影」 | **探针的时序问题**，不是实现问题：`wowo` 播 0.7s、1500ms 后才卸 class，截图截在半途。滚完等 1700ms 再拍 |
| 手机端报 23 个卡住的 `.wowo` | 探针把**断点隐藏掉的元素**也算进去了（它们永远进不了视口，opacity 本就是 0）。加 `offsetParent === null` 跳过 |
| 「Shop Now」按钮 425px 宽 | Figma 里是 220 hug，作为 column flex 子项会被 stretch。`align-self: flex-start` |
| 首版给标题挂了 `data-pop-text` | **第八轮已经撤过一次**：word-pop 只留给 stats 的 `.stat`，其余一律 `wowo`。查 changelog 才发现，全部改回 |

### 两稿冲突（**待设计方确认**，见 PROJECT-STATUS）

桌面稿与手机稿在四处对不上，都取了信息量更大的一版，没有自造：

- Science 三张 stat 卡：桌面三张同一句占位，手机是**三段不同的真文案** → 用手机的；数值仍是 95%
  （桌面稿 + homepage 一致，手机稿的 50% 判为占位残留）
- Science 的成分区：桌面收尾是「Shop Now」按钮，手机是**四行手风琴**且标题不同
  （Heading / Just the necessities）→ 两套都做，按断点切换
- Science nutrient 卡：桌面 3 张 / 手机 4 张 → 做 3 张，不造第 4 张
- How Gumi Works 副标：桌面还是「This is a placeholder subheading.」，手机是真文案且**颜色是珊瑚红**
  → 文案用手机的，颜色各按各稿

### ⚠ Reviews 页的引用文案里有竞品名

三张专家卡的引用是设计稿直接从参考站抄来的占位，**文中出现 Grüns**（另一个软糖品牌）。
原样保留（不编造），但**上线前必须替换**，已在 HTML 注释与 PROJECT-STATUS 标出。

### 判据

- 5 页 x 5 个宽度（390/768/1024/1440/1920）渐进滚动：横向溢出 0、卡住的 `.wowo` 0。
- Science 桌面逐项实测 vs 稿：hero text x110/w566/h272、media x760/w570/h430、
  卡片 x80/w410.7、compare 标题 x189/w410、面板 x732/w519/h540（行 64）、
  disc x188/w520、faq 媒体 x188/w520 —— 全部与稿一致。
- 页面总高 vs 稿（扣掉稿里的浏览器 toolbar）：Science 5662/5691、
  How Gumi Works 7613/8084、Reviews 7101/9006（Reviews 的差额是评论 app 区只出外壳）。
- 扇贝方块两处同源：归一化 alpha 差异 0.0。

### 文件清单

```
新  science.html / reviews.html / how-gumi-works.html
新  figma/new-page.py                        从 index.html 现切外壳拼页（含 --resync）
新  tools/shoot.py                           截图 + 溢出 + 卡住 wowo 探针
新  assets/scss/layout/_page-hero.scss
新  assets/scss/modules/_compare.scss / _ingredients.scss / _faq-image.scss
新  assets/scss/modules/_expert.scss / _dosed.scss
新  assets/scss/components/_scallop-box.scss
新  assets/scss/helpers/_masks.scss          两个内联 mask（file:// 下唯一可行的形式）
新  images/scallop-box.png                   扇贝方块（由 science-desktop-image 优化而来）
改  assets/scss/modules/_science.scss        手机 padding/eyebrow 修正 + __body + 三个变体
改  assets/scss/modules/_reviews.scss        + .reviews--cream
改  assets/scss/modules/_faq.scss            app-section 加标题 + inner 改 flex
改  assets/scss/components/_button.scss      + .btn--xl
改  assets/scss/components/_scallop.scss     + 4 个配色
改  assets/scss/helpers/_variables.scss      + $c-coral；$build → 20260820-r14
改  assets/scss/style.scss                   注册 7 个新模块
改  index.html                               三张 science 卡加 __body 内层；?v=
改  pdp.html / font-check.html               ?v=
改  figma/optimize-images.py                 + scallop-box 一条
```

### 遗留

- 剩余六页：Our Story / FAQ / Get in Touch / Referral / Privacy / Shipping。
- Reviews 的评论 app 区只有 `.app-slot` 外壳，页面比稿短 1900px，是预期。
- `.faq__row` 也有「LINE 高 0 却写成 border」的老问题（既有实现，本轮没动）。
- Reviews 专家卡的引用文案含竞品名，见上。

## 第十三轮 — 内页收尾：Our Story / FAQ / Get in Touch / Referral / Privacy / Shipping（2026-08-20）

九个内页的后六个，连同第十二轮的三个，**11 个静态页至此全部落地**。
这六页几乎没有新版式：四个是文本/表单页，Our Story 由既有的 `.reviews` + `.product` 撑起大半。

### 改了什么

1. **六张新页面**：`our-story.html` / `faq.html` / `get-in-touch.html` / `referral.html` /
   `privacy-policy.html` / `shipping.html`。

2. **新模块四个**：
   - `modules/_story.scss` —— Our Story 的三张图文卡（手机纵向堆叠）。
   - `modules/_cta-band.scss` —— 深绿扇贝 CTA 板，Our Story 与 FAQ 共用。
   - `modules/_form.scss` —— Get in Touch 与 Referral 共用一套字段/提交样式。
   - `modules/_rich-text.scss` —— Privacy 与 Shipping 的长文页（含 Shipping 的两张费率表）。
   另加 `.faq--plain`（FAQ 页那份列表在白底、且上方没有标题）。

3. **咨询类型可预填**（批注要求「照搬 Funky 站点」）。header / footer 里指向联系页的四个链接
   现在带 `?type=partners|press|careers|contact`，`main.js` 的 `enquiryPrefill` 读它选中对应项，
   认不出的值就留在稿自己的默认值上。

4. **`figma/dump-text.py`** —— 打印一块画板全部可见 TEXT 的完整字符。
   起因是 `sections/*.build.txt` 会把长字符串截成省略号，第十二轮照抄时漏掉过半句
   （How Gumi Works 的「Built for the days you forget everything.」被写成了「…everything else.」，本轮已修）。

### 修掉的坑

| 现象 | 真因 / 判据 |
|---|---|
| FAQ 页的 CTA 板上叠着一层**别的页面的文案**（"Nutrition that fits the life you're living." / "Shop Now"），半透明 | 板的形状是从 Our Story 的**画板渲染**里抠的，阈值只认品牌绿 —— 板上的 lime 标题和白色按钮离绿很远，于是**被一起抠成了洞**，透出下面的白底。grep 证实 HTML 里根本没有那段文字。解法是二值化后 `binary_fill_holes` 把洞填回去，只保留外轮廓的抗锯齿。⚠ `PIL.ImageDraw.floodfill` 在这里静默无效（填充覆盖率 0），换 `scipy.ndimage` 才对 |
| 「Send Message」按钮没有底色 | `.btn` 基类只有布局，配色一直在修饰类里（`--primary` / `--lg`）。表单提交是全站唯一的满宽按钮，给了它自己的配色而不是再加一个修饰类 |
| CTA 板比稿矮 85px | 稿是 plate 1280x393 里居中放一个 1086x288 的内容块，而内容块自己已有 48px padding —— 差的正是上下各 52.5。另外眉题与标题在稿里是一组（gap 32），按钮离这组 40，我起初一律用了 40。补 `.cta-band__head` 并把弧形 SVG 的画布从 40 收到 28（稿里那个 132 高的框有 89 是空的），实测 392 对 393 |

### 判据

- 11 页 x 5 个宽度（390/768/1024/1440/1920）= 55 组：横向溢出 0、卡住的 `.wowo` 0。
- CTA 板：宽 1280、高 392（稿 393）、上边轮廓起伏 41px（扇贝还在），板内白色像素只剩真实的按钮。
- 页面总高 vs 稿（扣掉稿里的浏览器 toolbar）：FAQ 3034/3003、Get in Touch 2892/2803、
  Referral 2676/2587、Privacy 4040/4287、Our Story 6507/7095。
- 文案：长段落一律取自节点 dump，不用 build.txt 的截断串。

### 文件清单

```
新  our-story.html / faq.html / get-in-touch.html / referral.html
新  privacy-policy.html / shipping.html
新  figma/dump-text.py                        画板全文 dump（build.txt 会截断）
新  assets/scss/modules/_story.scss / _cta-band.scss / _form.scss / _rich-text.scss
改  assets/scss/helpers/_masks.scss           + $mask-scallop-band（已填洞）
改  assets/scss/modules/_faq.scss             + .faq--plain
改  assets/scss/style.scss                    注册 4 个新模块
改  assets/js/main.js                         + enquiryPrefill
改  how-gumi-works.html                       修「everything else.」多出的词
改  全部 *.html                               联系页链接带 ?type=；?v= → r15
改  assets/scss/helpers/_variables.scss       $build → 20260820-r15
```

### 遗留

- Privacy 正文、Shipping 全文（写的是**美国**配送）、Reviews 专家卡的**竞品名**都是稿自带的占位，
  上线前必须替换 —— 已在 PROJECT-STATUS 单列一节。
- Get in Touch 的咨询类型选项只有「Contact Us」来自稿，其余三项按 header/footer 的链接补的，需客户确认。
- CTA 扇贝板的弧不符合分隔条那套 `r = 0.6407d`（实测 pitch 88 / 振幅 56），现在用的是从稿渲染
  抠出来的位图 mask，窄屏会被压扁。设计方若能给矢量源可换成真几何。
- 表单 focus 态是自定值。

---

## 第十四轮 — 四线审计的上线阻断级修复（2026-08-21）

`docs/audit/` 那轮只出报告没动文件。本轮按 `00-SUMMARY.md` 的修复顺序做完前 10 项，
外加 CSS / JS 两条线里同级别的条目。构建号 → `20260821-r16`。

### 改了什么

**一、入场动画的失败模式（P0 ×2 + LCP）**

1. **`wowo` 的 rAF 闩锁不再会锁死**。`main.js` 里 `ticking = false` 写在 `self.run()` 之后，
   `run()` 抛一次异常就永远回不来，之后每次 scroll 都被 `if (ticking) return` 挡掉 ——
   审计实测 22/27 元素永久不可见。改成 `try { self.run(); } finally { ticking = false; }`。
   （同文件的 slider / gallery 把复位写在业务调用之前，本来就没这问题。）

2. **`.wowo{opacity:0}` 改成以「main.js 活着」为条件**。原来无条件生效，`<noscript>` 只挡
   「浏览器禁用 JS」，挡不住 404 与顶层抛异常这两种真实故障。
   ⚠ 审计建议的「head 里内联一行加 `js` 类」**单独用是不够的** —— 那行内联脚本在 404 / throw
   两种场景下照样执行，门照样成立，实测 `stuck` 仍是 29 个。现在的门是：
   内联加 `js` 类 → `load`（或 4s 兜底）时若 `window.gumi` 不存在就把类摘掉。
   `window.gumi` 是 main.js 自己的收尾导出，是唯一诚实的存活信号。
   实测：健康时 `belowOp=0`（门照常工作），404 / throw 时 `belowOp=1`、`stuck` 只剩 3 个
   本来就该隐藏的弹窗层。

3. **首屏 13 处容器移出透明门**，hero 熊图入场换成不带 opacity 的 `gm-art-in-opaque`。
   合成层上的 opacity 动画不产生 LCP 候选，要等 1500ms 那次 `classList.remove` 才登记 ——
   **11 页 LCP 1536~1588ms → 40~104ms**。首屏文案因此不再淡入（折线以下照旧），
   这是拿掉 1.5 秒换来的，把 class 加回去即可回退。

4. **八个模块各自套 try/catch**。单 IIFE 里任一模块抛异常，它后面的全部静默不初始化。

**二、内容与结构**

5. **7 处开发占位文案**（`Subscription options load here.` / `Customer reviews load here.`）
   会印在页面上，改成 HTML 注释；挂载点与预留高度保留。
6. **Privacy 正文首段补回**（568 字符两个自然段，`figma/dump-text.py` 从节点取全文），
   原来那句 `<p>Subheading</p>` 是页头副标被重复进了正文。
7. **Privacy / Shipping 补上页头下方的分隔条**。原注释写「稿里没有分隔条」，与节点数据不符：
   `326:82363` 有 `Spacer Desktop 324:46328`(h96)，手机稿有对应的未翻转 `Spacer Bottom`。
8. **13 个死的 `data-modal` 触发器**：our-story / how-gumi-works / reviews 三页缺弹窗 markup，
   从 index 整块复用补齐。实点验证 6 页触发器全部能开、0 broken。

**三、几何还原**

9. **highlight card 的波浪唇口** `bottom: -1px` → `-23.5%`。SVG 是一整排圆，稿只让顶上
   29.76/94 露出来，整块露出会把圆的下半弧也带出来，看着像两层波浪。
   百分比按容器高解析，两个断点都对。

10. **扇贝拆成「尺寸」与「方向」两根正交轴**。原来 `.scallop--lg` 同时管大瓦片和向下鼓，
    于是所有大分隔条都朝反了（只有 page-hero 下方那条碰巧对），而四个文本页要的
    「小瓦片 + 向下鼓」根本无法表达。
    判据不是像素而是**组件 id**，稿里正好是两轴相乘：

    | componentId | 高 | 弧向 | 对应 class |
    |---|---|---|---|
    | `310:8380` | 96 | 上 | `.scallop` |
    | `310:8412` | 128 | 上 | `.scallop .scallop--lg` |
    | `324:46328` | 96 | 下 | `.scallop .scallop--down` |
    | `324:46319` | 128 | 下 | `.scallop --lg --down` |

    全站 22 处按这张表重新指派。验证用两条互不相干的判据（相位采样 + 均值/中位数符号），
    11 页全部一致、零分歧。

11. **CTA 扇贝板**：手机端几何按手机稿（`padding 64/38`、内容 gap 108、head gap 39、
    标题 30/36/-0.3、板 350×507 对稿 507.5），mask 换成**两张按各自画板生成的矢量**。
    原来一张位图从 1280 画板抠出来横向拉到 390，14 个弧压成 24.5px 的锯齿。
    矢量取自节点自己的 `fillGeometry`，**不需要导出端点**（`/v1/images` 仍在限流）。
    实测：1440 = 14 弧 / 节距 91.4（稿 89.5），390 = 5 弧 / 节距 70.0（稿 68）。
    ⚠ SVG data URI **必须写 `width`/`height`**，只有 viewBox 时 Chrome 解析出的图不绘制，
    mask 全透明 → 整块元素消失。

12. **手机端「只写了桌面值」的一批**：页脚链接 14/20/-0.28（版权行的 `<p>` 要就地重述，
    全局 `p` 是直接规则、压过继承）、四个文本页页头副标（18/500/-0.36/#333333，FAQ 行高 24、
    Privacy 手机 16/24/#4d4d4d）、三处主 CTA 52/16/+0.48、手机稿设 FILL 的按钮改满宽。
    16 条 computed-style 断言全绿。

13. **`vs__bear` 的 `width`/`height` 属性比例修正**（202×173 → 202×156）。属性既不是文件比例
    也不是 CSS 要的值；`height:auto` 时属性就是加载前的 aspect-ratio，lazy 化后暴露成 17px 跳变。

**四、图片与加载（首屏 17.61 MB → 3.78 MB）**

14. **15 张在用图各出一份 WebP**，`<picture>` + PNG 兜底；三张严重超采样的先缩到 2× 显示尺寸。
    质量判据是**合成到白底后的 PSNR ≥ 35 dB**，15/15 通过（最低 35.7）。
    ⚠ 判据本身踩过一次坑：拿缩小后的 WebP 去和原尺寸 PNG 比，量的是缩放不是编码，
    会把每张缩过的图都判成质量不合格。参照物必须是「原图按同样方式缩过」。
    转换脚本 `tools/webp.py`（只写 `.webp`，从不碰 PNG）。
15. **`picture{display:contents}` + `source{display:none}`**。前者避免 `<picture>` 的行内盒
    挪动 logo 跑马灯；后者是配套的 —— `display:contents` 会把 `<source>` 提升成父级 flex 项，
    实测把 Science 的对比头像挤到第二行、整页下移 96px。
    判据是**全站几何快照**（11 页 × 2 宽度、3089 个 key）：改完只剩跑马灯的 1~2px，
    同配置连跑两次也有同样抖动，即动画相位噪声。
16. **49 处补 `loading="lazy"`**；`nav-card-bear` 用 `display:none` + `lazy` 组合 ——
    两者缺一都不行：面板折叠时它仍算出 261×315 的盒（lazy 判定「该加载」），
    而 `display:none` 单独也不阻止 `<img>` 下载。每页省 312 KB，5 个页面首屏图片降到 0。
17. `bear-icon` 的 CSS 背景走 `image-set()`，PNG 留作兜底声明。

**五、CSS / JS 卫生**

18. `.promo-card--white .promo-card__stack` 的手机 gap 在作用域内重述（媒体查询不加特异性，
    原来那条永远打不中）。
19. `.product__cta` 的 transition 补 `color`、去掉 hover 从不改的 `box-shadow`。
20. reduced-motion：reset 补 `transition-delay/animation-delay: 0s !important`
    （原来只压 duration，弹窗关闭后隐形遮罩还挡 0.4s 点击）；删掉 3 处被 `!important` 压过的
    死规则，保留 `::details-content` 与 `.rv-panel{transform:none}` 两个够不着的例外并注明原因。
21. 两个 `appearance:none` 的 `<select>` 与 `label.form__check` 补 hover 反馈与 `cursor:pointer`。
22. JS 健壮性 5 条：`open()` 先关旧弹窗、`e.target.closest` 守卫（document 上的合成 click
    会抛异常）、popText 的 catch 不再摘 `data-pop-text`（CSS 兜底正靠它）、
    `fill()` 零宽守卫 + 克隆上界 12（实测退化时能造出 4281 个节点）、
    resize 只在**宽度**变化时重排（手机地址栏收放会把 reels 甩回居中）。

### 怎么验证的

| 判据 | 结果 |
|---|---|
| `tools/shoot.py --all` | 11 页 × 5 宽度 **55/55**，横向溢出 0、卡住的 `.wowo` 0 |
| LCP（11 页 @1440） | **40~104 ms**（改前 1536~1588） |
| JS 404 / 顶层 throw 两组 | 透明门自动摘除，`stuck` 只剩 3 个本就隐藏的弹窗层 |
| 全站几何快照 diff | 3089 key，仅跑马灯 1~2px（噪声基线相同） |
| 扇贝弧向（双判据 × 11 页） | 50 条全部一致，分歧 0 |
| CTA 板弧数 | 1440 = 14、390 = 5，与两张稿一致 |
| 手机端 token（16 条 computed） | 0 失败 |
| 弹窗触发器实点（6 页） | 0 broken |
| JS 六条各自复现原故障 | 0 失败 |
| 真鼠标 hover（5 类） | 0 失败，`elementFromPoint` 先验命中 |
| WebP PSNR（合成白底） | 15/15 ≥ 35 dB |
| 首屏实际下载（11 页真实请求） | 17.61 MB → **3.78 MB** |

### 文件清单

```
改  assets/js/main.js                      闩锁 try/finally、模块 try/catch、closest 守卫、
                                           open() 关旧、popText catch、fill 上界、resize 宽度门
改  assets/scss/helpers/_animation.scss    隐藏门 → html.js
改  assets/scss/helpers/_masks.scss        scallop-band 换两张矢量（桌面 + 手机）
改  assets/scss/helpers/_variables.scss    $build → 20260821-r16
改  assets/scss/base/_reset.scss           picture/source 显示模式、reduced-motion 补 delay
改  assets/scss/components/_motion.scss    + gm-art-in-opaque（hero 熊不从 opacity 0 起步）
改  assets/scss/components/_scallop.scss   拆 --lg（尺寸）/ --down（方向）
改  assets/scss/components/_modal.scss     删 reduced-motion 死代码，保留 transform 例外
改  assets/scss/components/_accordion.scss 同上，保留 ::details-content
改  assets/scss/components/_button.scss    .btn--xl 手机 FILL + 52/16
改  assets/scss/layout/_header.scss        nav-card__art 面板关闭时 display:none
改  assets/scss/layout/_footer.scss        手机 14/20/-0.28，版权行 p 就地重述
改  assets/scss/layout/_page-hero.scss     + --text-page / --lh-24 / --privacy-mobile
改  assets/scss/modules/_nutrition.scss    唇口 bottom -23.5%
改  assets/scss/modules/_cta-band.scss     手机几何按稿 + 手机 mask
改  assets/scss/modules/_product.scss      CTA/label-btn 手机 52/16、transition 补 color
改  assets/scss/modules/_form.scss         提交按钮手机 52/16、select 与 check 的交互态
改  assets/scss/modules/_promo.scss        白卡 gap 在作用域内重述
改  assets/scss/modules/_science.scss      bear-icon 走 image-set
改  全部 *.html                            js 门控、首屏去 wowo、picture、lazy、扇贝 class、?v=
改  privacy-policy.html / shipping.html    补分隔条；privacy 补正文首段
改  our-story / how-gumi-works / reviews   补弹窗 markup
改  pdp.html                               vs__bear 属性比例
新  images/*.webp                          15 张
新  tools/webp.py                          WebP 转换 + PSNR 门禁
```

### 遗留

- **`gumi-bear-front-glow.png` 是首页 LCP 图但源只有 528px 宽**（对 439 CSS px 是 1.20×，2× 屏上发虚）。
  要加大必须有更高分源 —— **需向设计方索取**，不能靠放大。
- `bear-gummy-glow.png` 767 KB **零引用**，未删；需确认是废弃资产还是漏接的图。
- 手机稿里没有白色 promo 卡，它的手机 gap 取 12 还是 24 **待设计方定**（现在按 12）。
- Privacy / Shipping 两个手机稿用的是另一版页脚组件（16/24/600/ls 0），与其余 9 稿冲突，
  **本轮按 9 稿的 14/20 做**，待裁决。
- 审计里的 P2 长尾未做：全局字距铺到稿中字距为 0 的 71 处、手机 header 图标顺序、
  白底页面多出的薄荷色带、hero CTA 宽度、stats↔science 缺的扇贝与小熊、pack band 双重旋转、
  Shipping 费率表样式、26 条新发现的两稿冲突、20 处红色文字。
- index 的 24 个 media logo 仍是 `loading="eager"`，未动（怀疑跑马灯靠它测宽，改前要先确认）。

---

## 第十五轮 — assets 目录扁平化 + SCSS 合并为 customstyle.scss（2026-08-21）

需求方定的交付结构：**`assets/` 内不建子目录**，js / css / icon / font 一律平铺；
**SCSS 收进单文件 `customstyle.scss`**。这也正是 Shopify 主题 `assets/` 的硬约束
（不接受子目录），所以现在改比交付前改省事。顶层 `images/` 按既有约定不动。

### 结构

```
改前                              改后
assets/css/style.css              assets/customstyle.css
assets/js/main.js                 assets/main.js
assets/fonts/*.woff2   (19)       assets/*.woff2   (19)
assets/icons/*.svg     (44)       assets/*.svg     (44)
assets/scss/  36 个 partial       assets/customstyle.scss  (6266 行)
```

`assets/` 现在 66 个文件、零子目录。平铺后无文件重名（已验四类 64 个文件名互不冲突）。

### SCSS 合并怎么做的

合并不是简单拼接 —— 原来 36 个 partial 各自 `@use` 依赖，**输出顺序 ≠ 定义顺序**；
拼成单文件后两者被迫统一，而 Sass 要求变量先定义后使用。所以文件分成两段：

- **第一段「定义」**：variables / mixins / masks，不产生任何 CSS 输出，被迫排最前。
- **第二段「输出」**：顺序 = 原 `style.scss` 的 `@use` 顺序（由 sourcemap 的 `sources`
  反推得到，不是照目录名排的）。

一个例外记在文件头免得日后被当成错误「修正」：`_mixins.scss` 里那个 `:root{--pad-x}`
是 CSS 输出而非定义，所以它留在第二段 reset 之后的原位，没跟着 mixin 定义提到最前。

**判据 = 产物逐字节相同。** 合并后（尚未改路径时）编译出的 CSS 与原 `style.css`
同为 147808 B、md5 同为 `04c78d0b…`，证明合并没有改动任何一条规则或它们的层叠顺序。

### 路径改写

`customstyle.css` 从 `assets/css/` 上移到 `assets/`，深度少一层：

| 原 | 现 |
|---|---|
| `url("../fonts/x.woff2")` × 12 | `url("x.woff2")` |
| `url("../../images/bear-icon.*")` | `url("../images/bear-icon.*")` |

改完产物 diff 恰好 28 行，**全部是 url 行，无一行是别的内容**。

### 验证

| 判据 | 结果 |
|---|---|
| 合并未改 CSS（改路径前）| 与原 style.css **逐字节相同**，md5 一致 |
| 改路径后的产物 diff | 28 行，100% 是 url |
| `tools/shoot.py --all` | 55/55 ok，无 overflow、无 stuck wowo |
| CSS/JS 是否真的生效 | 12 页 `--pad-x=80px`、`--build` 正确、`window.gumi` 为 object |
| 字体路径是否解析得到 | 12 页 `document.fonts` 里 PP Palma 状态 loaded |
| HTML 引用是否都命中真实文件 | 全部命中，无 404 |
| **A/B 几何**（旧结构副本 vs 新结构，同 HTML 内容）| 11750 个几何键，**24 个页面×宽度组合的 scrollHeight 全部逐一相同** |

A/B 报了 222 处矩形差异，全部集中在 `deco-bear` / `pop-word` / `logo-scroll__item`
这些带 CSS 动画的元素上，方向还不固定。**同一份代码跑两次的噪声基线是 237 处** ——
实测低于噪声，判定为动画相位噪声而非回归。（探针已先摘 `.wowo`，但 CSS animation 没关，
所以噪声躲不掉，只能靠基线对照。）

### 文件清单

```
新  assets/customstyle.scss           36 个 partial 合并，6266 行
新  assets/customstyle.css            编译产物，147691 B
删  assets/scss/                      36 个 partial（内容已并入）
删  assets/css/style.css              由 customstyle.css 取代
移  assets/js/main.js              -> assets/main.js
移  assets/fonts/*.woff2   (19)    -> assets/
移  assets/icons/*.svg     (44)    -> assets/
改  全部 11 个页面 + font-check.html  link/script 路径；font-check 的 DIR 改 "assets/"
改  figma/promo-art-source.html       css 与 icon 路径
```

### 遗留

- 编译命令变了，两处文档已同步：
  `npx sass@1.77.8 assets/customstyle.scss assets/customstyle.css --no-source-map`
- `assets/*.svg` 44 个图标**正式页面一处都没引用**（图标都是内联 SVG 或 CSS mask 实现的），
  只有 `figma/promo-art-source.html` 和 `figma/fetch-assets.py` 引着。按需求原样搬过来了，
  没删 —— 但交付 Shopify 前值得确认这批是不是还要留。
- `font-check.html` 的 link 本来就没带 `?v=`，本轮未动（它是诊断页，走缓存也无妨）。
- 顶层 `images/` 未动（169 处引用）。上 Shopify 主题时它也得进 `assets/`，届时一并处理。

---

## 第十八轮 — 波浪真正搬进所属 section（2026-08-21）

第十七轮我给的结论是「做成 section 的设置项即可，DOM 不用动」。用户看完说
**还是要把波浪放在对应的 section 模块里** —— 那就搬。这一轮只做这一件事。

### 改了什么

`<main>` 下那 27 个独立的 `<div class="gb-scallop">` 全部搬进它所分隔的**上面那个
section**，成为它的最后一个子元素；顺带把 `.gb-hero` 里那个也统一到同一套机制
（它本来就在 section 内，但用的是「在流里」的老写法，留着会让 Liquid 移植出现两种模式）。
搬完 28 个，形态是：

```html
<section class="gb-product gb-sec-edge gb-sec-edge--lg">
  …
  <div class="gb-scallop gb-scallop--edge gb-scallop--white-to-mint"></div>
</section>
```

**为什么归上面那个 section 而不是下面**：nutrition 那道波浪要让上方模块的内容
（包装袋）穿到波浪底下（`.gb-scallop--bleed`），跨不过模块边界，只能归上面。

**尺寸只写在 section 上**（`--edge-w` / `--edge-band` / `--edge-h`），波浪从父级继承。
所以 `.gb-scallop--edge` **不再带 `--lg`**，大小由宿主的 `.gb-sec-edge--lg` 决定 ——
一份真值，不会出现「section 说大瓦片、波浪说小瓦片」这种对不上的情况。
Liquid 里一个 `{% if %}` 同时决定两边。

搬迁脚本 `tools/move-scallops.py`（一次性；它自己会从 `</section>` 往回找配对的
开标签，不靠「最近一个 `<section`」猜）。

### 形状占的高度怎么留出来 —— 前两条路都试过、都不行

| 方案 | 为什么不行 |
|---|---|
| `border-bottom: var(--edge-h) solid transparent` | **Chromium 把 border 宽度取整到整数 px**（127.979 → 127）。每道波浪差 ~1px，28 道累计能把页面缩短二十几像素，而且波浪会露出 1px 到下一个模块里。是实测 `border-bottom-width: 127px` vs 波浪高 `127.969px` 抓出来的 |
| `padding-bottom: calc(原值 + var(--edge-h))` | 精度够，但每个 section 在各断点的底内距都不一样（88 / 96 / 120 / 64…，还各有窄屏值与插值），要 calc 在原值之上就得逐条改 15 个规则 × 2~3 个断点，早晚跟基础规则漂移 |
| ✅ `::after` 占位块 | **纯增量**：section 长高 `--edge-h`，原有内距一个字都不用动；且它在 padding box 之内，`overflow:hidden` 的 section（`.gb-nutrition` / `.gb-logo-scroll`）也不会把波浪裁掉，于是连特例都不需要 |

几何上与「独立兄弟」逐像素等价：section 高度 `+--edge-h`、波浪脱离文档流，净变化为 0；
波浪顶边 = section 底边 − `--edge-h` = 原来那个兄弟所在的位置。

### 判据

路径式的 computed-style diff **这一轮无效**：波浪从 `<main>` 里拿走会让后面所有兄弟的
下标整体错位，diff 比的是不同的元素（一上来报了两千多处「差异」，全是错位）。
换成**与位置无关的不变量** —— 全站每个真实元素的**矩形多重集**：

- 22 个页面 × 宽度组合，**除宿主 section 自己长高一个条高之外，其余每一个盒子的矩形
  逐一相同**（index@1440 是 1325 个盒子不变、3 个宿主变高；science 是 693 / 3；
  faq 是 234 / 1 …），元素总数前后一致。
- 每个宿主的高度增量都**精确等于该档条高**（1440：小 95.94 / 大 127.97；
  390：小 48.02 / 大 35.27），不是「差不多」。
- **`body` 总高度 11 个页面 × 2 档全部一位小数不差**。
- `tools/rwd.py` ✅ 全绿；`tools/shoot.py --all` **110/110 ok**；
  构建自检 30 项全绿（`20260821-r19`）；产物与源码一致。
- 人眼复核四种形状：hero 的 `--down`（小熊仍压在波浪上）、nutrition 的 `--bleed`
  （包装袋仍穿到波浪底下被圆弧切）、page-hero 的 `--down --mint-to-cream`、
  `.gb-vs` 的小瓦片 —— 与搬迁前一致。

### 文件清单

```
改  assets/customstyle.scss   新增 .gb-sec-edge / --lg / .gb-scallop--edge（::after 占位）；
                             .gb-scallop--bleed 去掉负 margin；.gb-nutrition 去掉自补的
                             padding-bottom；$build → 20260821-r19
改  assets/customstyle.css    编译产物
改  index.html                4 个波浪搬进宿主 + hero 那个统一到新机制
改  pdp.html / reviews.html / how-gumi-works.html / science.html / our-story.html /
    faq.html / get-in-touch.html / referral.html / privacy-policy.html / shipping.html
                             各自的波浪搬进宿主 section
改  font-check.html           第十七轮的 --bleed / nutrition padding 两条探针换成
                             第十八轮的两条（占位块与波浪等高、裁切型宿主无需特例）
新  tools/move-scallops.py    一次性搬迁脚本
```

### 遗留

- **页脚那两道波浪没动**：`.gb-footer-cta-wrap` 与 `.gb-footer-wrap` 的波浪是**上边缘**
  （模块的第一个子元素，在流里），本来就在自己的模块内且位置正确。要做上边缘变体
  就再加一组 `--edge-t`（`::before` 占位 + `top: 0`），本轮没有需求，没做。
- `.gb-sec-edge` 目前只有下边缘。以后要给某个 section 同时加上下两道边缘，
  得把 `--edge-h` 拆成 `--edge-h-t` / `--edge-h-b`。

## 第十七轮 — 任务文档 3 项：平滑滚动 / 波浪归属 + band 透底 / 去放大（2026-08-21）

`修改任务文档.txt` 又换了一批，3 条。第 2 条里夹着一个**设计问题**（波浪该不该做成独立模块），
先给结论再动手；夹着的两个 bug 都改了。

### 改了什么

1. **全站平滑滚动**（第 1 条）。用 **Lenis 1.3.11**（MIT），文件 vendored 到
   `assets/lenis.min.js`，没有构建步骤，换版本＝换那个文件。
   先手写过一版滚轮阻尼，换掉了：**触控板**的 wheel 是操作系统已经加过惯性的高频流，
   再叠一层阻尼会糊成拖尾，而归一化不同输入源正是 Lenis 主要在解决的事 ——
   这一点在无头浏览器里根本验不出来（`mouse.wheel ≠ 真机`）。
   `main.js` 的 `smoothScroll` 模块负责三件事：登记内部可滚容器、弹窗开时 `stop()`、
   站内锚点走 `lenis.scrollTo`。触摸不接管（`syncTouch:false`），
   `prefers-reduced-motion` 与 `<html data-no-smooth>` 都能整站关掉。
2. **波浪：结论是「不要做成独立 section，做成所属模块的一个设置项」**（第 2 条的问题）。
   理由见下一节 —— 关键在于**「独立的 DOM 节点」和「后台里独立的一条」不是一回事**，
   所以本轮**一个波浪节点都没有搬**。
3. **`nutrition__band` 透到波浪底下**（第 2 条的 bug）。稿里全站每个 Spacer 的
   `frameFill` 都是「上方那块的颜色」（`#ffffff` / `#faf9f8` / `#f5f1e9`…），
   **唯独 nutrition→PDP 那一个（`310:8425`）`frameFill = none`** —— 设计师单独去掉了它的底色，
   为的就是让包装袋从圆弧缺口里继续往下露。所以这是一处特例，用
   `.gb-scallop--bleed` 表达：条带透明 + 自己往上压一个条高，`.gb-nutrition` 同步补出
   同高的 `padding-bottom`。旧实现里包装袋被**直线硬切**在 section 底边，
   底下再盖一条不透明浅绿。
4. **pack 行居中屏幕、始终两侧被裁**（第 2 条）。原来是定宽 2148px 的块 + 手机端往右偏 100，
   宽屏上会露出排头排尾。现在 `left:50%` + `width:max-content` + 两行都
   `align-items:center`，行内包装袋加到 10 / 11 个（一奇一偶保持半个节距的砖缝错位），
   `pk=1` 时行宽 4385px，4K 也铺得满。
5. **band 全部改流体**（第 2 条「始终跟随屏幕变化」）。`--pk` 这个缩放系数连同三档写死的值
   一起去掉，`--band-h` / `--band-cy` / `--pack-w` / `--pack-gap` / 散熊三个量全换 `fluid()`：
   576 处等于手机稿、1281 处等于桌面稿，中间连续，不再在两个断点处跳。
6. **hero 小熊去掉放大、改纯淡入**（第 3 条）。原来是
   `translateY(100px) scale(0.5) rotate(-5deg)` 归位、1.5s，现在只留 `opacity 0→1`、0.7s。
7. **页脚 CTA 两只装饰熊去掉 fadeIn**（第 3 条），现在是静态装饰。
8. **图片的动效/定位一律挂包裹 div**（第 3 条）。11 页的装饰熊由裸 `<img class="gb-deco-bear …">`
   改成 `<div class="gb-deco-bear …"><picture>…</picture></div>`。
   `<picture>` 自己当不了定位元素（默认 inline，改 display 又会把 `<source>` 提升成布局项，
   见 memory `picture-display-contents-promotes-source`）。

### 波浪该不该固定进模块（第 2 条的问题）

> ⚠ **本节「不需要动 DOM」的部分已被第十八轮推翻**（用户 2026-08-21 决定：还是要
> 真的放进 section 里）。下面对「后台里该是一条」的分析仍然成立，别照着「不用动 DOM」做。

**结论：波浪不要做成独立的 section，做成它所依附那个 section 的一个设置项
（「上边缘形状 / 下边缘形状 + 颜色」）。但这件事不需要动现在的 DOM。**

三条依据：

1. **Liquid 的一个 section 可以吐多个顶层节点。** `nutrition.liquid` 完全可以在
   `</section>` 之后自己再吐一个 `<div class="gb-scallop …">`。后台里它仍是**一条**，
   商家加/删/换序 nutrition 时波浪跟着走，永远不会错位或漏配色。
   「独立的 DOM 节点」不等于「后台里独立的一条」—— 后者才是麻烦的来源。
2. **现在的 DOM 已经是可以这样搬的形态。** 50 个波浪里 22 个本来就在模块内部
   （页脚 CTA 11 个、页脚 11 个），另外 27 个在 `<main>` 下、每一个都紧贴它的 section。
3. **样式表里没有任何跨 section 的组合器**。全站只有 4 处 `>` / `+` 选择器
   （`.gb-ink-halo` / `.gb-scallop-box > img` / `.gb-header__sublist > div` / `.gb-vs__row`），
   全在组件内部。所以 Shopify 给每个 section 套的 `<div id="shopify-section-…">`
   **不会打断任何一条规则** —— 这是「可以直接搬」的硬判据，不是感觉。
   ⚠ 反过来说：**以后不要写 `section + .gb-scallop` 这种相邻兄弟选择器**，
   那个包裹层一来就全失配。本轮的 `--bleed` 因此是挂在波浪自己身上的修饰类。

配色沿用现有约定即可：`--wave-bg` 恒为**上方**那块的颜色、`--wave-fg` 恒为**下方**那块，
对应两个设置项；`--down`（圆弧朝下）与 `--lg`（大瓦片）是两根正交的轴，各一个开关。

### 修掉的坑

| 现象 | 真因 / 判据 |
|---|---|
| `.gb-scallop--bleed` 写了 `--wave-bg: transparent`，条带照样是浅绿 | 修饰类排在**配色修饰之前**。两者同特异性，谁在后谁生效，于是 `--lime-to-white` 又把浅绿盖回来了。挪到配色之后即可 —— 自检探针抓到的 |
| 自检页新加的「Lenis 实例在」恒报红 | 内联自检在**解析期**就跑了，而 main.js 的模块是 `DOMContentLoaded` 才 init 的，那时实例必然还是 null。整段自检推迟到 `DOMContentLoaded` 之后 |
| 「三个可滚容器都要是 overflow-y:auto」这条断言永远不成立 | 判据本身错了：`.gb-product__thumbs` **只在桌面**可滚、`.gb-header__panel` **只在手机**可滚，同一视口下不可能同时成立。这条不变量搬到 `tools/rwd.py` 逐视口跑 |
| 全站截图里 band 一片空白 | 两件事叠加：`full_page` 截图不触发滚动 → `wowo` 没播、元素停在 `opacity:0`；我又给 pack 图加了 `decoding="async"`。改用视口截图 + 去掉那个属性 |

### 判据

- **总高度是这轮的不变量**：nutrition 补 `padding-bottom` +127.979px、波浪 `margin-top` −127.979px，
  两者必须精确抵消。实测 `body` 高度 1440 档 **9471.42px → 9471.42px**、
  390 档 **11441.9px → 11441.9px**，一位小数都没动。
- **computed-style 快照**（`tools/cssnap.py`，含伪元素，390/1440 × 12 页）：
  除 index 外的 10 个页面**全部是纯结构差异**（装饰熊多了一层 div），**属性变化 0 处**——
  也就是说把波浪几何提到 `:root` 这件事，渲染上一点没变。
  index 上有属性变化的元素只有 14/15 个，全在波浪 + nutrition + pack-band 子树内。
- **相位不变**：1440 档 row1 原来的第 1 个包装袋，现在落在第 4 个的位置上，坐标
  `[-190.5, 4295.2]` 逐位相同 —— 左右各加 3 个、居中，图案没有平移。
  row2 因为改成居中，比稿偏了 8.1px（见「遗留」）。
- **响应式**：`tools/rwd.py` 11 页 × 10 档 ✅ 全绿；新增第三条判据「滚轮黑洞」——
  任何自己能纵向滚的元素都必须带 `data-lenis-prevent`。
  `tools/shoot.py --all` **110/110 ok**（横向溢出 0、卡住的 `.wowo` 0）。
- **透底在每个视口都成立**：360/390/575/576/768/1024/1280/1281/1440/1920/2560 共 11 档，
  `.gb-nutrition` 的 `padding-bottom` 与波浪的 `margin-top` 逐档精确互为相反数，
  且行宽始终超出视口 1800px 以上（两侧一定被裁）。
- **Lenis 不破坏既有滚动**：PDP 的 sticky 图库照常黏住（滚 900px 后顶距 100→24，不是 −800）；
  滚轮压在横向轨道 `.gb-reels` 上滚的是页面（+400），轨道 `scrollLeft` 不动。
- **Lenis 行为**：滚一次有 16 个中间帧且单调不回弹（不是瞬跳）；缩略图竖轨已登记；
  弹窗打开时 `isStopped === true`、关闭后恢复；`data-no-smooth` 与
  `prefers-reduced-motion` 两条关闭路径都不建实例；无 JS 报错。
- **hero 进场**：动画中途取样 `opacity 0.73 / transform: none` —— 是淡入，不是缩放。
- 构建自检页 30 项全绿（`20260821-r18`）；产物与源码一致；`main.js` 语法自检通过。

### 文件清单

```
新  assets/lenis.min.js            Lenis 1.3.11 UMD（MIT），16.4 KB
改  assets/main.js                 smoothScroll 模块（Lenis 驱动 + 锚点 + PREVENT 名单）；
                                   modal.open/close 调 pause()/resume()；$build 相关无
改  assets/customstyle.scss        html 保持 scroll-behavior:auto（与 Lenis 互斥，写了理由）；
                                   波浪几何提到 :root（--sc-h / --sc-lg-h）供 nutrition 复用；
                                   新增 .gb-scallop--bleed；.gb-nutrition 补 padding-bottom；
                                   band 全面改 fluid()、去掉 --pk / --band-dx；
                                   hero 进场改 gm-art-fade-in；.gb-deco-bear 改包裹 div；
                                   $build → 20260821-r18
改  assets/customstyle.css         编译产物
改  index.html                     波浪加 --bleed；pack 行 4/5 → 10/11；?v=r18
改  pdp.html / reviews.html / our-story.html / how-gumi-works.html / science.html /
    faq.html / get-in-touch.html / referral.html / privacy-policy.html / shipping.html
                                   装饰熊改包裹 div 并去掉 wowo fadeIn；引入 lenis.min.js；?v=r18
改  font-check.html                整段自检推迟到 DOMContentLoaded；补 7 个第十七轮探针；
                                   EXPECT_BUILD → r18；引入 lenis.min.js
改  tools/rwd.py                   第三条判据：可滚容器必须登记给 Lenis（逐视口跑）
```

### 遗留

- **手机端散熊相对包装袋的相位偏了 0.46 个节距**。稿把整条 band 往右挪了 100.41，
  本轮按要求改成「行始终居中屏幕」，熊如果跟着往左挪就会被左边缘切掉半只，
  所以熊按**稿里的屏上位置**单独锚定（中线 −107）。要改回按相位对齐，
  把 `.gb-nutrition__bears-img` 的 `fluid(107px, 420.97px)` 换成 `fluid(-11.4px, 420.97px)`。
- **row2 比稿偏 8.1px**（桌面档）。稿里 row2 是 FILL 宽度、从左边缘排起，偏移 213.97；
  改成两行都居中后偏移是半个节距 222.05。包装袋是周期重复的，这 8px 看不出来。
- **hero 小熊是首页的 LCP 元素**（399,727 px²）。改成淡入后 LCP 会被推到淡入结束那一刻
  （时长 0.7s + 延迟 0.2s ≈ 0.9s）。要退回「不牺牲 LCP」的老做法，把
  `.gb-float-art--still` 的 `animation` 改回 `gm-art-in-opaque`（keyframes 留着没删）。
- **`.gb-expert__cards` 纵向多出 26px**（reviews 窄屏）。它只写了 `overflow-x:auto`，
  按规范另一轴的 `visible` 会被强制算成 `auto`，于是它「纵向也能滚」26px。
  有 Lenis 在，滚轮压上去滚的是页面，没有实际影响，本轮未动。
- **平板档仍然没有设计稿**（沿用第十六轮的说明）。

## 第十六轮 — 任务文档 9 项：断点改制 + band 还原 + 全站 gb- 前缀（2026-08-21）

`修改任务文档.txt` 换了新的一批，9 条，全部落地。其中 3 条查出来是**旧实现真的错了**
（band 转了两遍、散熊漏了旋转、bear-meter 每行数量不对），不是单纯的需求变更。

### 改了什么

1. **`nutrition__band` 按稿重做**（第 1 条）。稿 `341:46422`（Frame 60）是一个
   2148.494 × 977.991 的竖向 auto-layout，**整帧** rotation −6.556°；里面两行是普通的
   横向 auto-layout，行不转、pack 也不转。旧实现反过来：行平放、每个 pack 各转 −6.56°，
   于是 pack 之间仍排成水平线，稿里它们是沿对角线往右上走的。
   **第二处错更隐蔽**：`images/product-pack.png` 当初是按绝对空间导的，旋转已经烤进图里
   （877×1005 = 旋转后外接盒 438.38×502.38 的 2 倍），页面再叠一次 rotate = 转了两遍 ≈ −13.1°。
   图已由 `figma/make-pack-upright.py` 转正回 388.25×461.047 的 2 倍，旋转只由 `.gb-pack-band` 做一次。
2. **散落小熊合成单张**（第 2 条）。原来是 9 个 `<picture>` 各自引同一张
   `bear-scatter.png`，且宽高属性抄的是**旋转后外接盒**、旋转本身没实现 —— 9 只熊全被拉变形
   且方向一致。9 个节点共用同一 imageRef + imageTransform，所以零 API 本地合成即可
   （`figma/make-nutrition-bears.py`，裁 29.152%~71.002% 得单只熊，按各自 relativeTransform 摆放）。
3. **产品图库改叠放淡入、一次一张**（第 3 条）。原来是 scroll-snap 横向滚动条：一次甩动
   能跨好几张、切换是位移。现在 slide 绝对定位叠放，只有 `.is-active` 不透明；一次手势只走 ±1，
   跟拖多远无关。缩略图、键盘 ←→ 与索引同步。
4. **手风琴排他**（第 4 条）。全站 59 个 `<details>` 分 5 组加 `name=`（`gb-faq` / `gb-faq2` /
   `gb-spec`），同组只开一项走**原生**行为 —— 键盘、a11y、无 JS 全不受影响。
   `main.js` 补一个 `accordion` 模块兜老浏览器（它们把 `name` 当无关属性忽略）。
5. **reel hover 只放大内部图**（第 5 条）。卡片本身去阴影去位移，新增 `.gb-reel__media` 承载层，
   `scale(1.06)` 挂它身上，圆角与播放键不跟着变形。客户封面图来了塞进这一层即可。
6. **浮动收归 stats**（第 6 条）。11 页页脚 CTA 的两只装饰熊撤掉 `float-art`，改
   `wowo fadeIn delay-in-1 / delay-in-3` —— 不飘，一前一后依次淡入。全站现在只有
   `.gb-stats__bear` 还在飘。`.float-art--sm` / `gm-art-in-sm` / `gm-art-float-sm` /
   `.float-art--d2` 随之无使用者，一并删掉。
7. **全站 class 加 `gb-` 前缀**（第 7 条）。79 个模块块名连同它们的 `__元素` / `--修饰`
   一起改，共 3384 处（12 个页面 + SCSS 553 + JS 7）。
   **不改**动效与状态工具类（`wowo` / `fadeIn*` / `delay-in-N` / `is-*` / `no-js` / `js`）——
   main.js 与 Terra 的 wowo 约定挂在这些名字上。
8. **断点体系改成需求方口径**（第 8 条）：手机 ≤575 / 平板 576–1280 / PC ≥1281。
9. **全站响应式**（第 9 条）：平板档补数值插值 + `nutrition__cards` / `science__cards` 3→2→1。

### 断点改制怎么做的（第 8+9 条，这轮最容易踩的地方）

断点分成**两组**，别混着用：

| 组 | mixin | 范围 | 管什么 |
|---|---|---|---|
| 系统三档 | `mobile` | ≤575 | 手机稿 390 的数值 |
| | `tablet` | 576–1280 | 平板，没有稿，数值靠 `fluid()` 插值 |
| | `pc` | ≥1281 | 桌面稿 1440，值本来就在基础规则里 |
| 布局阈值 | `tight` | ≤1200 | 版心开始吃紧 |
| | `stack` | ≤1024 | 稿里的两栏并排放不下，改堆叠 |
| | `narrow` | ≤768 | 手机版排布 |

**为什么布局不跟着系统三档走**：一台 1194 宽的平板放得下稿里的两栏，硬堆成一列是把好排版
改坏。我第一版就是把 ≤1024/≤1200 全推到 1280，结果 1025–1280 从两栏变单列 —— 那是我引入的
回归，不是需求。所以布局阈值原样保留（旧代码的 768/1024/1200 是验证过的），
系统三档只负责「同一套排布下字号间距该多大」。

平板那一档的数值用 `fluid($手机值, $桌面值)`：在 576 处等于手机值、1281 处等于桌面值，
中间线性。两张稿都命中，中间那段不是拍脑袋填的。脚本 `tools/add-tablet-tier.py` 自动配对
基础规则与 `narrow` 块里的纯长度声明，生成 140 条；`stack` / `tight` 设过的属性一律跳过
（那是作者有意写给那两段的值，插了就是抹掉）。

版心 `--pad-x` 也改成插值 20→80。写死 40 会在 1280/1281 交界处让正文宽度**反向跳 79px**
（视口宽 1px，正文反而窄一截）。

### 修掉的坑

| 现象 | 真因 / 判据 |
|---|---|
| pack band 跟稿完全对不上 | 转了两遍：图里烤了 −6.556°，CSS 又转一次。转正后 9 个 pack 与稿的最大偏差 **0.26px**（手机档 0.13px） |
| 9 只散熊方向一致、被拉变形 | 宽高属性抄的是**旋转后外接盒**，旋转没实现。同一个坑第三次出现（见 memory `figma-rotated-frame-bbox-is-not-the-artwork`） |
| 平板插值写完「看着生效了」，实测字号原地不动、版心 padding 掉回 0 | `fluid()` 里斜率带了单位：`26px * (100vw - 576px)` 是 px×px，量纲错了，**整条声明被静默丢弃**，而 DevTools 里那行看着完全正常。斜率必须无单位。我一度靠截图目测判成「已生效」，是实测才抓出来的 |
| 自动生成的插值层漏了近四成规则 | 注释行没有分号，被块切分器粘在了后一个块前面，`startswith("@include narrow")` 因此失配。本文件里「上一行有注释」的块占 40% |
| bear-meter 在手机上每行 17 只、排成 7 行 | 稿里**恒定 20 只一行 × 5 行**（手机稿 300 只 / 15 行 × 20、桌面稿同理）。旧写法 flex-wrap + 写死 13.5px，列一窄就自己换行。改成 20 列 grid：列宽再小也是 20 只一行，只是按比例缩小 |
| 改名后 header 导航链接整个掉样式 | SCSS 里有一条 `a.header__link`（元素限定选择器），改名正则的 `(?<![\w-])` 把它挡掉了。判据抓到的：改名前后 computed-style 快照在这个节点上有 46 处差异 |
| 构建自检页从第十四轮起一直报「✗ 有 1 项不符」 | `EXPECT_BUILD` 停在 `20260820-r13`，而 `$build` 已经走到 r16 —— 版本号只推了一半。已同步并补 7 个本轮探针 |

### 判据

- **改名**：改名前后全站 computed-style 快照（`tools/cssnap.py`，含 `::before/::after`，
  390 与 1440 两档、11 个页面共 3.6 万项）**逐项相同**。唯一有差异的是 `font-check.html`
  —— 它本来就要随构建变。
- **断点改制**：每一步都用同一把判据卡住 390 / 1440 不变 —— 阈值搬迁 ✅、插值层 ✅、
  阈值还原 ✅ 三次都是「完全一致」。中间档（576–1280）本来就是要改的，不进不变量。
- **band 几何**：9 个 pack 与稿的绝对坐标逐个对，1440 档最大偏差 0.26px、390 档 0.13px；
  散熊位置 1440 档完全吻合，390 档 y 完全吻合、x 差 6px（设计师手工挪的，未追）。
- **响应式**：11 页 × 10 档宽度（360/390/575/576/768/1024/1280/1281/1440/1920）
  横向溢出 0、文字被祖先裁切 0、滚完整页后卡住的 `.wowo` 0。
- **插值连续性**：`.gb-science__title` 30px@576 → 40px@1281 逐档单调、两端精确落在稿值；
  `--pad-x` 20→80 同理，1280/1281 交界不跳。
- **交互**：图库淡入 0.3s、大幅左滑只走一张（3→3 不是 3→4）、缩略图与键盘同步（1440/390 两档）；
  手风琴 5 组排他在 **JS 开与关**两种情况下都只展开一项；reel hover 只有 `.gb-reel__media`
  变成 `matrix(1.06,…)`、卡片 boxShadow 恒 `none`、移开复原。
- 产物与源码一致（`sass` 重编后 `diff` 无输出）；`main.js` 语法自检通过。

### 文件清单

```
改  assets/customstyle.scss        断点两组 + fluid() + band/bears/gallery/reel 重写
                                   + 140 条平板插值 + bear-meter 改 grid + 3→2→1
                                   + 79 个块名加 gb- 前缀（553 处）+ $build → r17
改  assets/customstyle.css         编译产物
改  assets/main.js                 gallery 重写为叠放淡入；新增 accordion 模块并挂上 window.gumi；
                                   7 处类名前缀
改  index.html                     散熊收成单图；pack 图宽高属性 877x1005 → 776x922；
                                   首图 is-active；details name；reel__media；deco-bear 去浮动
改  pdp.html / reviews.html / our-story.html / how-gumi-works.html / science.html /
    faq.html / get-in-touch.html / referral.html / privacy-policy.html / shipping.html
                                   同上适用部分 + gb- 前缀 + ?v=r17
改  font-check.html                EXPECT_BUILD 同步 r17；补 7 个第十六轮探针
新  images/nutrition-bears.png     832x792 @3x，9 只熊合成一张（+ .webp 59 KB）
改  images/product-pack.png        转正 776x922（原图存 figma/assets-raw/product-pack.ROTATED-ORIGINAL.png）
删  images/bear-scatter.png/.webp  已被 nutrition-bears 取代
新  figma/make-nutrition-bears.py  散熊合成脚本（零 API）
新  figma/make-pack-upright.py     pack 图转正脚本（零 API）
新  tools/cssnap.py                全站 computed-style 快照 + diff（改 CSS 结构唯一有效的判据）
新  tools/rwd.py                   窄屏体检：横向溢出 + 内容被裁，11 页 × 10 档约两分钟
新  tools/sect.py                  按区块截图（整页一万像素高看不动）
新  tools/add-tablet-tier.py       一次性：生成平板插值层
新  tools/prefix-classes.py        一次性：加 gb- 前缀
改  tools/shoot.py                 WIDTHS 换成新断点两侧各取一格
改  tools/webp.py                  PLAN 换 nutrition-bears，去掉 bear-scatter
```

### 遗留

- **平板（576–1280）没有设计稿**，这一档的所有数值都是两张稿之间的线性插值，
  `nutrition__band` 的四个量（`--pk` / `--band-h` / `--band-cy` / `--band-dx`）是取中点算的。
  设计方若出平板稿，改的是 `fluid()` 的两个锚点和那四个量，不用重排布局。
- **3→2→1 的两列阈值是算出来的**：science 744px（一行 20 只熊需要 ~320 的列宽）、
  nutrition 704px。版心或卡片内距改了要跟着改，算式写在使用处注释里。
- `.gb-hero__title` 这类有 `stack` / `tight` 授权中间值的属性**不插值**，仍是
  36 → 48 → 60 的阶梯（769 / 1201 处跳变）。这是旧代码就有的、作者写死的中间态，本轮刻意保留。
- 产品图库改淡入后**无 JS 时缩略图点了没反应**（首图仍可见）。这是「淡入」这个要求本身
  带来的，不是漏做 —— 原来的原生滚动条在这一点上更好。
- reel 的 `.gb-reel__media` 目前是灰底占位，等客户封面图；结构与样式已就位。
- `images/product-pack.png` 是本地反转一次得到的（`/v1/images` 仍在限流）。
  拿到没限流的 token 后可直接导 `341:46424` 覆盖（导出时它本来就是正的）。

## 第十九轮 — 任务文档 7 项：手风琴死区 / header 吸顶 / 弧被裁（2026-08-24）

`修改任务文档.txt` 又换了一批，7 条。其中两条（第 6、7）在动手前先做了取证，
真因都跟表面描述不一样，记在下面。

### 改了什么

1. **弹窗关闭慢下来**（第 1 条）。真因不是时长 —— 进退场本来都是 0.4s；问题在**曲线**：
   `cubic-bezier(0.32, 0.72, 0, 1)` 是「起步快、末端缓」的 out 型，进场好看，倒过来播就是
   「一上来先冲掉大半行程」，观感即「啪」地消失。改成进退场各用各的：进场维持
   0.4s + 原曲线，退场 **0.55s + `$ease-in-out`**（前三分之一几乎不动）。
   基础规则上的 `transition` 管的就是「回到基础态」，所以退场值写在基础规则、进场值写在
   `.is-open` 里。`visibility` 的延迟同步跟到 0.55s，否则遮罩会提前吃掉点击。

2. **手风琴行间死区**（第 2 条）。行距原本是容器的 `gap`，那是**容器自己的空白**，
   点在两行之间什么都不会发生。改成把这段距离塞进 `summary` 的 `padding-bottom`
   （`--acc-gap`，product 20 / faq 24 / faq-image 16·24），**收起态几何一模一样**，
   但整段归了可点区。三处配套：
   - 展开时 `[open] > summary` 的 `padding-bottom` 收回 0，让面板自己的 16px 顶距接手
     —— 稿里 summary 与正文之间就是 16，行与行之间才是 20/24；
   - `.gb-acc-body` 补 `padding-bottom: var(--acc-gap)`，展开后到下一行的距离不塌；
   - **末项 `--acc-gap: 0`** —— 原来的 `gap` 不落在最后一项之后，不归零的话每个手风琴
     都会给页面多添一份行距（实测 faq +24、pdp/reviews/how-gumi-works +44、science@390 +48）。

3. **加号图标改纯 CSS**（第 3 条）。59 处 `<svg class="gb-acc-icon">` 换成
   `<span class="gb-acc-icon">`，两条线由 `::before` / `::after` 画（14×2、1px 圆头，
   取自原来那两条 path）。展开时**竖线转 90° 与横线重合**成减号，而不是整体转 45° 变叉
   —— 后者是「关闭」的手势。同时去掉图标的 hover 放大（`scale(1.15)` 全站清零），
   整行 hover 只换颜色。

4. **输入框焦点走边框**（第 4 条）。全局那条 `:focus-visible { outline: 2px solid }` 对
   `input`（除 checkbox/radio）/ `textarea` / `select` 关掉，改成 `border-color` 变色：
   `.gb-field__input` → 深绿（顺带去掉那圈 3px 光晕），`.gb-footer__input` → lime
   （页脚是深绿底，绿描边本来也看不清）。**复选框刻意留着 outline** —— 原生控件没有
   可控的 border，摘掉就等于键盘用户完全看不见焦点。

5. **header 吸顶**（第 5 条）。`position: sticky; top: 0`，公告条不跟着走。两处连带：
   - **手机抽屉高度**原本写死 `100svh − 公告条 − header`，只在页面停在最顶部时才成立。
     改成 `var(--drawer-h)`，由 `main.js` 的 `header.measure()` 在开抽屉与 resize 时实测
     （`视口高 − header 底边`），CSS 里那个 calc 退为回退值。
   - **PDP 的 sticky 图库** `top: 24px` 会被吸顶的 header 盖住，改成 `calc($h-header + 24px)`。
     顺手把写死的 80/64 收进 `$h-header` / `$h-header-mobile`，一处真值。

6. **弧形文字被裁**（第 6 条）。取证发现是**两个**独立原因叠在一起：
   - SVG 根元素默认 `overflow: hidden`，而 viewBox 是照「弧线」量的、没算文字的
     ascender —— 实测上缘越界 cta-band **−11.71**、stats −2.8、footer-cta −1.07。
     `.gb-arc-text { overflow: visible }` 一行解决，**盒子尺寸一个像素不动**，
     所以版面不受影响（改 viewBox 会把元素撑高、连带挪动整组间距）。
   - cta-band 那条另外还有 `textLength 163.41 > pathLength 161.53`：文字比弧还长，
     `textPath` 超出路径的部分直接不画。弦 160 → 168（R 338 不变），弧长 169.78，
     余量 6.37（3.9%）。
   全站 17 个弧逐个复核，路径余量最小的就是这条。

7. **页脚 CTA 上边缘的波浪透明**（第 7 条）。`--wave-bg` 的语义是「上方那块的颜色」，
   而这道波浪的上方是**各页最后一个 section**，模块自己不知道那是什么色。写死薄荷的结果：
   实测 11 页里 **6 页（白色收尾）多出一条薄荷带**，另 5 页恰好蒙对。
   `.gb-scallop--to-lime` 改 `transparent` 让上下文透出来；上方真是薄荷色的五页
   （index / pdp / reviews / science / how-gumi-works）改用新增的 `.gb-scallop--mint-to-lime`。
   改完 11 页逐页实测「条带色 == 上方 section 色」。

### 判据

新增 `tools/r19check.py`，7 条任务逐条给数字，**全绿**：

| 条 | 判据 |
|---|---|
| 1 | 面板退场 0.55s / 进场 0.4s，曲线不同；遮罩同步；visibility 延迟 0.55s |
| 2 | 四个手风琴容器 × 相邻两行中点做 `elementFromPoint`，**死点 0 个**（改前每个间隙都是死区） |
| 3 | 图标 `tagName === SPAN`、`svg.gb-acc-icon` 全站 0 个、收起 `rotate(90°)` → 展开 `identity`、`scale(1.15)` 规则 0 条 |
| 4 | 真点击进入 `:focus-visible` 后 outline 为 none、边框由 `#ccc → #005635`、`rgba(1,19,7,.1) → #b5ed61`、box-shadow none；复选框不在「摘 outline」名单内 |
| 5 | 1440 / 390 滚动 1500px 后 `header.top == 0`；抽屉底边贴视口底（滚动 0 与 1500 两种情形都 799 vs 800） |
| 6 | 17 个弧全部 `overflow: visible` 且**路径余量 > 0**（最小 6.37） |
| 7 | 11 页逐页「条带色 == 上方 section 色」 |

几何不变量（第 2 条是纯粹的「换个地方放同一段距离」，必须证明没挪动任何东西）：

- **`body` 总高 11 页 × 2 档 = 22 个组合逐一相同**（第一版漏了末项归零，那时 6 个页面
  各长高 20~48，就是靠这条抓出来的）。
- computed-style 全站快照：4 个不含手风琴的页面**各只有 7 处差异**
  = header sticky(4) + 波浪色(1) + arc overflow(2)，**零位移**。
- 含手风琴的页面里，所有 `#rect` 变化都是 `details` / `summary` 自身 **+20/+24 的高度**
  与展开项内部的等量下移，**每一行的 `top` 全部不变** —— 行的视觉位置没动，
  动的只是可点区的下边界。
- `<元素消失> 1062 / <元素新增> 354` 全部是图标换标签的账：
  59 图标 × 2 档 = 118，旧的 (svg + 2 path) × 3 条（含伪元素）= 1062，新的 span × 3 = 354。

回归：`tools/rwd.py` ✅ 全绿；`tools/shoot.py --all` 110/110 ok；
`font-check.html` 构建自检 **37 条全绿**（新加本轮 7 条探针）；`$build` → `20260824-r20`。

### 文件清单

```
改  assets/customstyle.scss   $nl-slide-out/$nl-ease-out；.gb-acc-icon 重写为 CSS 两条线；
                             三个手风琴容器 gap → --acc-gap；两个 row 加 padding-bottom
                             与 [open] 归零；末项 --acc-gap: 0；.gb-acc-body 收尾；
                             input/textarea/select 的 :focus-visible 摘 outline；
                             .gb-field__input / .gb-field__phone 去光晕；.gb-footer__input
                             加焦点边框；.gb-header 改 sticky；$h-header 新变量；
                             抽屉高度改 var(--drawer-h)；PDP sticky 避让 header；
                             .gb-arc-text overflow: visible；--to-lime 透明 +
                             新增 --mint-to-lime；$build → 20260824-r20
改  assets/customstyle.css    编译产物
改  assets/main.js            header.measure()：开抽屉与 resize 时实测 --drawer-h
改  index.html / pdp.html / science.html / reviews.html / how-gumi-works.html /
    our-story.html / faq.html
                             59 处 <svg class="gb-acc-icon"> → <span>
改  index.html / pdp.html / science.html / reviews.html / how-gumi-works.html
                             页脚波浪 --to-lime → --mint-to-lime
改  faq.html / our-story.html cta-band 弧的弦 160 → 168
改  全部 11 页 + font-check   ?v= → 20260824-r20
改  font-check.html           EXPECT_BUILD + 本轮 7 条探针
新  tools/r19check.py         本轮 7 条任务的专项判据
```

### 遗留

- **展开时 summary 的 `padding-bottom` 从 20/24 收到 0 是带 0.3s 过渡的**，与面板展开同时跑。
  若设计方认为展开态 summary 与正文之间不该是 16px，改 `.gb-acc-body` 的 `padding-top` 即可。
- **cta-band 弧的路径余量 6.37 是按当前占位字体（PP Palma 试用 Fizzy Light）量的**。
  换成客户授权的 PP Palma 后字宽会变，这一条要重量 —— `tools/r19check.py` 的第 6 段直接
  跑一遍就能看出来。
- 复选框仍走全局 outline（有意为之，见上）。若设计方要自定义勾选框，那时再一并改。
- 探针取样的三个坑，写在 `tools/r19check.py` 里，后来者别再踩：faq 首项在稿里**默认展开**
  （拿它测「收起态」会得到反的结论）、science 的手机手风琴在桌面宽是 `display:none`
  （rect 全 0，命中测试恒假）、**`el.focus()` 不触发 `:focus-visible`**（那是给真实交互的
  启发式，必须用 `page.click`）。

---

## 第二十轮 — 对话给的 8 条：hero 光晕重建 / 弧度还原 / 箭头旋转 / 补回缺失的波浪（2026-08-24）

本轮任务由对话直接给出（不是 `修改任务文档.txt`，那份是第十九轮的，未改动）。
原文 8 条，第 8 条是问「`gb-sec-edge gb-sec-edge--lg` 是干嘛的」，答在最后。

所有数值一律取自 Figma 节点数据（`figma/nodes/285-18162_homepage-desktop.json`
= 1440 桌面首页、`228-5932_homepage-mobile.json` = 390 手机首页），
判据脚本 `tools/r20check.py`。

### 改了什么

**1a `.gb-hero__btn` 满宽** — 稿 `332:16424` 宽 380 = 所在列 `Frame 427319663` 的整宽，
不是 shrink-to-fit。`align-self: flex-start` → `stretch`。

**1b 公告条补上 Trustpilot 五颗星** — 之前只有 `Excellent` 和 `Truspilot` 两个词，
中间什么都没有。稿 `332:16402`「stars」= 77×14，五个 14×14 的方板（`#b5ed61`）
横排、间距 1.75，每块中间嵌 10.5×10.5 的深绿五角星（内缩 1.75，几何直接取
`fillGeometry`）。做成**一整条 77×14 的 SVG** 而不是五个 flex 项：间距在稿里是死值，
一条 SVG 就把「方板 + 星 + 间距」全锁进 viewBox，桌面手机同一套（手机稿同尺寸）。
官方 embed 上线前这条会被整体换掉。

**2 hero 的 `gumi-bear-front-glow` 按稿重建** —— 「外轮廓大小宽度不对」的真因：
**光晕不是照片自带的，是稿里单独一条描边**。`332:16445` 是一条 439.066×732.078 的
路径，`fillGeometry` 是空的，只有 `strokeWeight 26.2137` / **CENTER** / `#b5ed61`，
所以光圈向外扩 13.107、向内压 13.107。旧文件是照着照片 alpha 描出来的一圈
**约 12px**（换算到屏幕只有 10.4px，不到设计的 40%），而且贴着照片每个凹凸走 ——
腿缝那种窄口在设计里被 26px 的粗描边直接糊平，旧图却老实地凹进去。
新图 `tools/make-hero-glow.py` 按稿重建：glow 路径的 `strokeGeometry` 填 `#b5ed61` 打底，
照片（`332:16446`，rect 1010.919×780.649 @ (−271.928, −13.757)，`scaleMode FILL`，
源图 `images/gumi-bear-front.png` 1200×927 比例一致所以等于直接拉伸）盖在上面，
一起被 Background 的 467.886×759.180 裁一刀（实测没裁到任何墨迹），再裁到墨迹。
尺寸因此从「路径宽 439.1」变成「路径 + 描边 = 466.0」，槽位占比 77.3% → **82.04%**，
手机 67.7% → **71.39%**（292.95 + 16 描边，手机稿描边是 16 不是 26.2）。
输出 559×910，与旧文件同采样率，**LCP 字节数基本不变**（787K/76K → 760K/79K，PSNR 38.2 dB）。

**3 logo 轨道：槽位 80 + viewport 上下各 8** — 稿 `341:47385` 行高 96，里面的
`Logo` 框是 **79.88 高、上下各留 8.06**。两者相加仍是 96，section 总高一个像素没变。

**4 `ONE HANDFUL` 的弧改成设计的椭圆** — 稿里的弧字 `341:47318` 是一段**椭圆**弧：
`rx 118.5261 / ry 65.7047`，圆心 (139, 82.073)，基线走椭圆顶点 (139, 16.368)。
之前写的是 `A 338 338`（正圆），同样半跨 85.5 只落 **11.0px**，设计落 **20.2px** —— 弧度太平。
框也回到稿的 `Curved Text` = **278×29**（之前 237×50）。
**head gap 保持稿的 48，没有改成 30**：30 是在旧的 50px 弧框上量出来的补偿值；
框改回 29 之后，48 得到的「弧字墨迹底 → 标题墨迹顶」正好是设计的 **52px**（旧的是 58）。
若仍想更紧，`.gb-stats__head` 的 gap 改 30 得到墨迹 34px，一行的事。

**5 `60+` / `10+` 的加号缩小上浮** — 设计稿实测三处：hero 12/25、stats `60+` 17/35.5、
stats `10+` 17/36 —— 加号墨迹一律是数字的 **47.9%** 高、顶边与数字顶边齐平。
而我们这份 PP Palma **试用档**的 `+` 字形是 85.7% 高且垂直居中（`plus` 轮廓
y 136..1364 / 数字 −32..1500，upm 2000），**字形本身对不上**，只能用排版还原：
`font-size: 0.56em` 把墨迹压到 47.9%，`top: -0.6em` 抬到顶边对齐。
光晕不用管 —— `.gb-ink-halo` 的 `0.15em` 在父级就算成了绝对 px 再继承，
加号周围仍是 7px，与设计实测一致。
`.gb-stat--ingredients` / `--fibre` 的 `top` 按任务文档给的 **5.5%**（Figma 原值 5.099%）：
稿里 `Ingredients Item Container` 高 56、里面的 TEXT 从 +1.957 开始，我们的行盒 51 高
且文字贴块顶，同样的 top 我们的墨迹高约 1.96px，5.5% 正好补回来（推导值 5.41%）。

**6 四支箭头补上组的旋转，并移进 `.gb-stats__bear`** —— 「位置没还原」的真因不是位置：
`341:47322/25/28/31` 四个组的 `relativeTransform` **行列式是 −1**（旋转 + 镜像），
旧实现导出的是**未旋转**的原始矢量，viewBox 长宽比 1.70 / 2.83 / 2.67 / 3.03，
而设计里的外接盒是 1.16 / 1.08 / 1.07 / 1.11 —— **差 2.5 倍**，形状和高度全错。
新 SVG 把「组变换 × 子变换」烘进 `<path transform>`，viewBox 直接取合成后的墨迹盒。
描边：Figma 是 OUTSIDE 1.78036，SVG 只有居中描边，宽度取两倍 **3.56071** 才等外扩量。
四支现在是 `.gb-stats__bear` 的子元素（任务文档要求），百分比改成相对熊框
302.797×375.016 算，超出 0~100% 是正常的。**副作用：熊带着 `.gb-float-art--d1`
的漂浮，箭头现在跟着一起飘**（不想要就把 `gb-float-art gb-float-art--d1` 从熊上摘掉）。

**7 `.gb-science` 上方的波浪补回来** — 不是「看不到了」，是**从来就没有**：
`.gb-stats` 没带 `gb-sec-edge`，也没有 `.gb-scallop--edge` 子元素。稿里
`341:47307`「Spacer Desktop」高 96、底色 `#faf9f8`（= 上方 stats 的 cream），
下一段 `341:46641` 是 `#f5f1e9`（sand）。补 `gb-sec-edge`（不带 `--lg`，96 而非 128）
+ 新配色类 `.gb-scallop--cream-to-sand`。science.html 的两个 `.gb-science` 上下同色，
本来就不需要波浪，没动。

**8「`gb-sec-edge gb-sec-edge--lg` 是干嘛的」** —— 让 section **自带它自己的下边缘波浪**：
- `.gb-sec-edge` 做两件事：① 用 `::after` 占位块留出波浪的高度（`--edge-h`），
  ② 把 `--edge-w / --edge-band / --edge-h` 声明在 section 上，让绝对定位的
  `.gb-scallop--edge` 子元素继承 —— **尺寸只有一份真值**，不会出现「section 说大瓦片、
  波浪说小瓦片」。
- `--lg` 只是换一套更大的瓦片：普通 `--sc-*` 在 1440 下是 302 宽 / **96 高**，
  `--sc-lg-*` 是 524 宽 / **128 高**，正好对上稿里两种 Spacer 的高度。
- 波浪归**上面**那个 section 而不是下面，是因为 nutrition 那道要让包装袋穿到波浪底下
  （`.gb-scallop--bleed`），跨不过模块边界。搬迁脚本 `tools/move-scallops.py`。

### 判据（`tools/r20check.py`，全部通过）

| 条 | 判据 |
|---|---|
| 1a | 按钮宽 == `.gb-hero__cta` 宽 == 稿的 380 |
| 1b | 星条 77×14、五颗、方板 `rgb(181,237,97)`、星形 `rgb(0,86,53)`、夹在两段文案中间 |
| 2 | 熊图占槽位 **82.04%**；资源比例 559:910 = 0.6143 == 设计墨迹 466.0:758.5 |
| 3 | 槽位 80 / viewport `padding-top: 8px` / 行总高仍 96 |
| 4 | `viewBox == "0 0 278 29"`；路径含 `118.5261 65.7047`；半跨 85.5 落差 **20.20**（旧 11.0）；弧长 227.0 > 文字长 171.8；head gap 48.00 |
| 5 | 加号墨迹 / 数字墨迹 = **48.6%**（hero 50.0%），顶边差 +1.21px / +0.25px |
| 6 | 四支都在 `.gb-stats__bear` 里；四支位置与设计误差 **≤0.02%**；长宽比 1.1650 / 1.0778 / 1.0737 / 1.1081 对设计 1.1649 / 1.0777 / 1.0736 / 1.1080 |
| 7 | `.gb-stats` 带 `gb-sec-edge` + `.gb-scallop--edge`；`--wave-bg #faf9f8` / `--wave-fg #f5f1e9`；高 95.9 |
| 手机 | 弧字字号 20（手机稿 `236:12453`）、弧框仍 278、星条 77×14 |

几何不变量（本轮在 11 页的公告条里插了节点，路径式快照会整体错位，
判据换成「**body 总高 + 排除公告条子树后的矩形多重集**」，见 memory
`css-refactor-computed-style-judge`）：

- **10 个非首页的页面 × 2 档 = 20 个组合，body 总高与非公告条矩形逐一全同** ——
  本轮除星条外没碰过它们。
- index 的差异逐条对得上账（忽略 y 只比 (x, w, h)）：
  24 个 logo 槽 96→80、新增 1440×95.9 的波浪、`.gb-stats__head` 226→**205**（= 稿的 205）、
  hero 按钮 204→380、hero 熊 535×780.3→566.1×815.6、四个箭头盒换形状、
  弧框 237×50→278×29、USP 数值 66.8→56.4 宽（高仍 37）。
- index body 总高 9471.4 → 9546.4，**+74.96 = 新波浪 +95.94 − 弧框 −21.0**，无残差。

回归：`tools/rwd.py` ✅ 全绿；`tools/shoot.py --all` **110/110 ok**；
`tools/r19check.py`（第十九轮判据）全部通过；`$build` → `20260824-r21`。

### 途中抓到的一个副作用（已修）

加号 `font-size: 0.56em` 之后，`.gb-usp__value` 从 37 长到 **42**，
`.gb-hero` 连带长高 5px。原因是父级 `line-height` 是**长度**（37px），
原样继承给这个小字号行内盒；它的内容区只有 22.6px，`(37−22.6)/2 = 7.2` 的
半行距落在基线**下方**，比 32px 的 strut 还低 5.3px，行盒被撑高。
补 `line-height: 0` 后行内盒不参与行盒高度计算，字形照画。
**这条是靠 body 总高不变量抓出来的，肉眼完全看不出来。**

### 文件清单

```
改  assets/customstyle.scss   .gb-hero__btn align-self: stretch；新增 .gb-announcement__stars
                             （+ __star-plate / __star-pt）；.gb-logo-scroll__viewport
                             padding 8px 0、__item 高 80；.gb-stats__arc 278 宽 + narrow 字号 20；
                             新增 .gb-stat__plus / .gb-usp__plus（0.56em / line-height 0 / top -0.6em）；
                             .gb-stat--ingredients / --fibre top 5.5%；.gb-stats__arrow 四条
                             百分比改为相对熊框；新增 .gb-scallop--cream-to-sand；
                             .gb-hero__bear 宽 82.04% / narrow 71.39% + 注释重写；
                             $build → 20260824-r21
改  assets/customstyle.css    编译产物
改  全部 11 页                公告条插入 <svg class="gb-announcement__stars">；?v= → 20260824-r21
改  index.html                stats 弧 viewBox/path；三处 60+/10+ 加号包 span（含 halo 副本）；
                             四支箭头换新 SVG 并移进 .gb-stats__bear；.gb-stats 加 gb-sec-edge
                             + .gb-scallop--cream-to-sand 子元素；hero 熊图 width/height 559x910
改  font-check.html           EXPECT_BUILD → 20260824-r21
改  images/gumi-bear-front-glow.png / .webp    按稿重建，528x874 → 559x910
新  tools/make-hero-glow.py   hero 光晕合成图的生成脚本（可复跑）
新  tools/r20check.py         本轮 8 条的专项判据
```

### 遗留

- **全站其余 5 处弧形文字用的还是 `A 338 338` 正圆，同一个缺陷。**
  稿里只有两种椭圆：桌面 **289×132**（rx 144.5 / ry 66，footer-cta ×10、promo-card、
  dosed ×2、cta-band）和手机 / 桌面-stats **237.05×131.41**（rx 118.5261 / ry 65.7047）。
  各自的 `Curved Text` 框在稿里是 452×51 / 452×28 / 452×34 / 231×31 / 278×29 /
  278.28×46.38 / 229×29 / 274×46，父级 gap 32 / 40 / 24 / 39。
  另外 `.gb-arc-text text` 全站写死 24px，**手机稿是 20px**，所有实例在窄屏都偏大一号。
  本轮只按任务文档改了 `gb-stats__arc`，其余要不要一起扫等指示 —— 那会动到 11 页的竖向节奏，
  得单开一轮并重跑全部不变量。
- `.gb-stat--vitamins` / `--benefits` 的 `top` 仍是 Figma 原值，与上面两个一样高约 1.96px。
  要对齐按 **+0.31%** 算：vitamins 56.93% / benefits 53.72%。
- `.gb-stat__value` 在桌面继承了 `letter-spacing: -0.32px`，稿里是 **0**。影响不到 1px，本轮没动。
- 加号是**排版模拟**，不是字形。换成客户授权的 PP Palma 后，如果那一版的 `+` 本身就是
  小号上浮的字形（设计稿的表现更像是这样），这两条规则要撤掉 —— `tools/r20check.py`
  第 5 段会直接报出来（比例会变成 ~24%）。
- hero 光晕图仍是 1.2× 采样（`docs/audit/04-performance` 的 P2「欠采样」那条没动）。
  要提到 2× 把 `tools/make-hero-glow.py` 的 `OUT_W` 改成 932，webp 从 79K 涨到约 123K。

## 第二十一轮 — 对话给的 PC 端 15 项数值 + footer-cta 弧度还原（2026-08-24）

本轮由对话直接给出（不是 `修改任务文档.txt`），数值全部是需求方指定的具体值，直接照改；
只有 footer-cta 的弧度是需求方报的 bug，按 Figma 节点数据查证后修。

### 数值类（14 项，均为 PC/基础规则，未动 mobile 专属值）

`.gb-science-card__body` gap 16→22（tablet fluid 上限同步改 22）、`.gb-bear-meter`
max-width 346→347 / gap 4px→**8px 4px**（行距单独拉开，列距不变）、`.gb-highlight-card__title`
补 margin-bottom 14px、`.gb-highlight-card__text` 补 max-width 300px、`.gb-product__accordion`
补 margin-top 8px 且 `--acc-gap` 20→24（连带改了 `.gb-product__acc-row` 的 padding-bottom，
两处共用一个变量，见第十九轮）、`.gb-product__taste` / `.gb-product__packed` 共享规则补
margin-top 24px，`.gb-product__packed` 单独拆出 `align-items: flex-start`（taste 仍是 center —
两者以前共用一条规则，现在拆成「共享块 + packed 单独覆盖」，taste 不受影响）、
`.gb-testimonial__body` gap 8→10、`.gb-testimonial__name` 补 margin-top -8px、
`.gb-reviews__disclaimer` max-width 1100→626 + 补 margin-top 48px、`.gb-footer-cta__inner`
gap 32→30、`.gb-footer-cta__text` 补 margin-top -6px、`.gb-footer__link-groups` gap 24→22。

`.gb-product__app-slot`（订阅 app 占位的虚线框）按需求整个删掉：`pdp.html` 里的
`<div class="gb-product__app-slot">` 与 scss 里对应的规则块一起移除，CTA 按钮直接跟在
产品信息后面。app 接入后会在按钮前挂载自己的内容，这块不需要预留占位壳。

### footer-cta 弧度还原

**bug 是框选小了，不是曲率算错。** `.gb-footer-cta__arc` 之前直接把椭圆本体的
289×62 当 viewBox 用，而 Figma 里椭圆本体（`313:9711`「YOUR GREENS CALLED」，size
289×132，rx144.5/ry66）外面还套着一层「Curved Text FRAME」（`313:9710`，size
**452×51**，椭圆在其中左右各留 81px 居中），这层框此前一直没找到，只能拿椭圆自己
的窄边凑合，弧于是被硬压成 `A 338 338` 的近似正圆（第二十轮遗留清单里已经把这层框的
尺寸列出来了，本轮只是把 footer-cta 这一处按图施工）。

新参数：viewBox `0 0 452 51`，椭圆中心 (225.5, 83)，`M 81 83 A 144.5 66 0 0 1 370 83`
—— 取的是椭圆左右两个顶点之间的整段圆顶弧（不是像 `gb-stats__arc` 那样只取中间一小段），
弧长 342.3 比「YOUR GREENS CALLED」的渲染文字长 267.9 富余约 28%，不会被 `textPath` 截断。
CSS 宽度同步 289px → 452px（`@include tablet` 的 `fluid()` 上限跟着改，`@include narrow`
的 237px 未动——mobile 用的是另一种椭圆 237.05×131.41，这条留在下面遗留里）。

### 判据

`tools/r22check.py`（临时脚本，未入库）逐项核对上面 14 处 computed style 数值、
app-slot 已从 DOM 消失、弧形 viewBox/path/弧长富余量/CSS 宽度；`tools/rwd.py`
11 页 × 10 档宽度全绿，本轮的 margin/max-width 改动没有引入横向溢出。

### 遗留

- **弧形文字还剩 4 处同一缺陷**（promo-card、dosed ×2、cta-band，各自的 Curved Text
  框 452×28 / 452×34 / 231×31，尺寸见上一轮遗留清单）；footer-cta 的 mobile 变体
  （237.05×131.41 那个真正的手机椭圆）也还没单独做，现在 mobile 只是把这次改对的
  桌面路径等比缩窄，弧的曲率对但椭圆的长宽比不是手机稿本来的比例。全站扫描仍按
  上一轮说的单开一轮处理，会动 11 页竖向节奏。

### 文件清单

```
改  assets/customstyle.scss    本轮 14 处数值 + .gb-product__app-slot 规则删除 +
                               .gb-footer-cta__arc 宽度/fluid 上限；$build → 20260824-r22
改  assets/customstyle.css     编译产物
改  pdp.html                   删 .gb-product__app-slot 占位 div
改  全部 11 页                  footer-cta 弧形 SVG 的 viewBox/path；?v= → 20260824-r22
```

## 第二十二轮 — 对话追加的 7 项（stats 熊浮动范围 / 间距修正）（2026-08-24）

对话在第二十一轮报告之后又追加了几条，内容仍是直接给值，唯一需要判断的是「浮动效果
只给内部图片」——把 `gb-stats__bear` 上的 `gb-float-art gb-float-art--d1` 移到新加的
`.gb-stats__bear-art`（包 `<picture>` 的内层 div），四支箭头作为 `.gb-stats__bear` 的
直接子元素留在外层，不再跟着一起飘。⚠ `.gb-float-art` 的 `will-change: transform`
会让承载它的元素变成新的包含块，`.gb-stats__bear-img` 的定位是按熊框
302.797×375.016 算的百分比，wrapper 必须 `inset: 0` 撑满整个熊框，尺寸差一点这些
百分比就全错——判据是两者 `getBoundingClientRect()` 逐一相等（entry 动画播完之后测，
播放中间量会因为 `scale(0.5)` 的过渡值直接量出腰斩的宽高，是本轮踩过的一个假阳性）。

### 改了什么

- `.gb-product__packed .gb-product__sub-title` 补 `align-self: center`——上一轮把
  `.gb-product__packed` 改成 `align-items: flex-start` 让列表左对齐，连带把标题也带偏了。
- `gb-stats__bear` 浮动范围收窄到内部图片（见上）。
- `.gb-stats__note` 补 `margin-top: -30px`。
- `.gb-highlight-card__title` 的 `margin-bottom` 14px 改 12px（上一轮给错了）。
- `.gb-footer-cta__inner` 的 `gap` 30px 改 0；间距改成分别写在 `.gb-footer-cta__title`
  （`margin-top: 38px; margin-bottom: 30px`）与 `.gb-footer-cta__text`
  （`margin-bottom: 32px`，`margin-top: -6px` 保留）上，不再靠容器 `gap` 统一控制。

### 判据

临时脚本核对以上 computed style；`tools/rwd.py` 11 页 × 10 档全绿。`$build` → `20260824-r23`。

### 文件清单

```
改  assets/customstyle.scss    本轮 6 处 + 新增 .gb-stats__bear-art；$build → 20260824-r23
改  assets/customstyle.css     编译产物
改  index.html                 gb-stats__bear 内插入 .gb-stats__bear-art 包裹 <picture>
改  全部 11 页                  ?v= → 20260824-r23
```

## 第二十三轮 — 撤掉 gb-sec-edge 机制 + 补 stats 波浪右侧小熊（2026-08-24）

用户对第十八轮定下的「尺寸写在 section 上、`.gb-scallop--edge` 靠 class 继承」这套
机制不满意，明确要求**全站撤掉**，波浪自己的尺寸固定写在波浪自己身上，不要 section
配合。另外指出 `.gb-stats` 的 `gb-scallop--cream-to-sand` 波浪右侧一直缺一只小熊
（对照设计截图核实过，本地 `figma/nodes/` 里确实没有这个节点——大概率设计稿在
首次拉取之后又单独改过这一处，没能补拉到）。

### gb-sec-edge / gb-sec-edge--lg 撤掉

**原理**：`.gb-scallop` / `.gb-scallop--lg` 本来就是自给自足的（直接读 `:root` 的
`--sc-w/h` 或 `--sc-lg-w/h`，不需要任何人传值）；section 唯一真正需要外部配合的
是「多留出一条波浪高的空间」——现在直接把 `var(--sc-h)` / `var(--sc-lg-h)` 加进
各模块自己 `padding-bottom` 的数值里（`calc(既有值 + var(--sc-h))`，两个变量本身
是 `clamp()` 算出来的，天然跟着视口连续变化，不需要再对齐断点），不再需要
`::after` 占位块，`.gb-scallop--edge` 也不再从 section 继承 `--wave-w/band/h`，
只剩定位这一件事。

**14 个模块逐一顺过一遍**：多数模块「永远是大瓦片」或「永远是小瓦片」，直接把
对应变量加进自己的 `padding-bottom`（`.gb-hero`/`.gb-nutrition`/`.gb-science`/
`.gb-science--tight`/`.gb-dosed`/`.gb-cta-band` 永远大瓦片；`.gb-logo-scroll`/
`.gb-stats`/`.gb-vs`/`.gb-expert` 永远小瓦片）。四个模块是**同一个 class 在不同页
面要求不同瓦片**（`.gb-page-hero--center`、`.gb-product`、`.gb-app-section`、
`.gb-ingredients`），新增四个正交修饰类（跟 `.gb-scallop--lg` 是同一种命名思路，
只做「把 padding-bottom 覆盖成大瓦片版本」这一件事，不做别的）：
`.gb-page-hero--lg`（how-gumi-works / our-story 的 `--center` 页头）、
`.gb-product--lg`（index / font-check 的产品区）、`.gb-app-section--lg`
（reviews.html）、`.gb-ingredients--lg`（science.html）。pdp 的 `.gb-product--page`
原来没有自己的 padding 规则，新开一条。`.gb-reviews--cream` / `--sand` 两个颜色
修饰符恰好各自唯一对应大 / 小瓦片，直接把 padding-bottom 加在颜色类自己身上。

⚠ **12 个模块的 `position: relative` 之前是 `.gb-sec-edge` 给的，删掉那层之后
必须逐一补回自己身上**——`.gb-scallop--edge` 的 `position: absolute` 没有落点会
飘到更外层的定位祖先上去，量出来的第一版就是漏了这一步，30 处波浪里有一部分
直接飘走。

### 踩到的一个脚本 bug（已修）

批量替换用的是「(section 原 class 字符串, 波浪原 class 字符串)」成对匹配的脚本，
但**波浪的颜色配对 class 字符串在不同 section 之间会撞车**（比如
`gb-scallop--edge gb-scallop--down gb-scallop--to-white` 全站 7 个页头一字不差），
脚本按文件处理时波浪替换这一半没有绑定「本文件这条规则的 section 是否真的匹配」，
导致 8 处被跨规则误传了 `gb-scallop--lg`（5 个小页头 + how-gumi-works 的
`.gb-product` + reviews.html 的 `.gb-expert` / `.gb-ingredients`）。**判据是按
「当前 section 的 class 列表」重新推一遍该不该有 `--lg`，逐一比对**，不是靠脚本
本身的执行日志——日志显示"成功替换"不代表替换对了地方。

### 判据

- 全站 30 处波浪逐一核对：`position` 不是 `static`、波浪底边与 section 底边的
  像素差 ≤0.6、波浪宽度与 section 宽度的像素差 ≤1（1440 与 390 两档，共 60 组）。
- 29 处（不含 font-check）核对「波浪顶边到上方内容底边的间距」== 改前源码里那个
  模块的 `padding-bottom` 原值（96 / 120 / 88 / 0 ……逐一列出的具体数），
  证明改动没有让任何一处的总高度多算或漏算——**这条判据独立于本轮同时在做的
  其余间距类改动**（footer-cta 那些 margin/gap 是故意变的，不在这条不变量里）。
- `tools/rwd.py` 11 页 × 10 档全绿。

### stats 波浪右侧的小熊

素材用 `images/bear-gummy-glow.png`（原本只是 `promo-art.png` 的合成源，这次
另外裁掉透明边距存成 `images/stats-bear-deco.png/.webp`，直接单独展示）。坐标
按设计截图反推（本地没有这个节点的 Figma 数据），`.gb-stats` 相对定位、熊用
`translate(-50%,-50%)` 钉中心点。

⚠ **中心点的 y 没有照抄截图反推的位置**：`.gb-stats` 自己没有 `overflow`
属性，熊只要探出 section 底边，就会被下一个 section（`.gb-science`，不透明底色，
后画）按正常层叠盖住下半截——截图量出来的中心本来在 103%（相对 `.gb-stats`
自身高度），收到 89.5%（手机同理，100.3%→91.5%）才能让熊全须全尾留在
`.gb-stats` 自己的画面里。代价是熊比设计稿里更往上一点，没有整个压在波浪上，
这是「不動 DOM 结构、不建跨 section 的 z-index/负 margin 特例」这个约束换来的；
真要做到跟设计稿分毫不差需要重新设计层叠关系，本轮没有做。

### 遗留

- **弧形文字仍有 4 处 `A 338 338` 正圆未修**（同第二十一轮遗留，未动）。
- stats 小熊装饰的坐标是反推的，等设计方给回这个节点的真实数据后需要用真实
  尺寸/位置核对一遍。

### 文件清单

```
改  assets/customstyle.scss    删 .gb-sec-edge/.gb-sec-edge--lg；.gb-scallop--edge 精简为纯定位；
                               14 个模块的 padding-bottom + position:relative；新增
                               .gb-page-hero--lg / .gb-product--lg / .gb-app-section--lg /
                               .gb-ingredients--lg / .gb-stats__deco-bear；$build → 20260824-r24
改  assets/customstyle.css     编译产物
改  全部 11 页 + font-check     30 处 section/波浪 class 改写（去 gb-sec-edge，按需补 --lg /
                               新修饰类）；index.html 追加 .gb-stats__deco-bear；?v() → r24
新  images/stats-bear-deco.png/.webp   bear-gummy-glow.png 裁边后的独立展示版
```

## 第二十四轮 — 弹窗滚动锁定的横向抖动 + nutritional-label 数值修正（2026-08-24）

### 弹窗锁滚动时页面横向跳一下（已修，写进公约）

`html.is-modal-open, body.is-modal-open { overflow:hidden; }` 关掉滚动条后，视口
在桌面非 overlay 滚动条（Windows/Linux 常见）下会瞬间宽出滚动条那几 px，内容跟着
右移/重新居中，肉眼是「开弹窗屏幕跳一下」。这个问题不是本项目独有，之前别的项目
也遇到过，这次一并把修法记进了 `~/.claude/CLAUDE.md` 通用铁律第 14 条，供以后的
项目直接复用，不用每次重新推导。

修法：`assets/main.js` 的 `modal.open()` 在**加锁定 class 之前**（此时真实滚动条
还在，测得出宽度）用 `window.innerWidth - document.documentElement.clientWidth`
量出滚动条宽度，写成 `--scrollbar-w` 这个 CSS 变量；`assets/customstyle.scss` 里
原来的锁定规则补一行 `padding-right: var(--scrollbar-w, 0px)` 把这段宽度吃回去。
关闭弹窗时锁定 class 一并移除，`padding-right` 自动跟着归零，不需要额外复位逻辑。

验证：headless 环境原生滚动条宽度恒为 0（见 memory headless-chromium-probe-limits），
真机上跳动量测不出来，改用 Playwright 直接把 `--scrollbar-w` 覆写成合成值 `17px`，
确认 `html`/`body` 的 computed `padding-right` 都正确跟到 `17px`，关闭后归零——
这样验证的是「CSS 机制本身对这个变量的响应是否正确」这条不变量，不依赖 headless
测不出的真实滚动条宽度。

### gb-nl-panel__close 去掉 hover 时的 SVG 旋转

`@include hover { background: $c-lime-100; transform: rotate(90deg); }` 里的
`transform: rotate(90deg)` 删掉，`transition` 也把已经用不上的 `transform` 参数
一并摘掉（`trans(background-color, transform)` → `trans(background-color)`），
只保留背景色过渡。

### nutritional-label 弹窗数值修正（对话给的 7 项）

```
.gb-nl-pane                 padding: 20px 24px 24px  →  18px 10px 24px 24px
.gb-nl-tab::after            bottom: 8px  →  10px
.gb-nl-table caption        padding: 3px 0  →  8px 0 6px
.gb-nl-table th, td         padding: 6px 0  →  7px 0
.gb-nl-table td             width: 100px  →  72px
.gb-nl-table td:last-child  width: 60px  →  128px
```

Playwright 逐一读 computed style 核对，`.gb-nl-pane` 的 padding 合成后是
`18px 10px 24px 24px`（4 值写法，因为 top 和 right 各自单独指定，与原来 left/right
共用一个值的 3 值写法不再等价），表格宽度/间距全部通过。

### 文件清单

```
改  assets/customstyle.scss   .gb-nl-panel__close 去 hover 旋转；.gb-nl-tab::after /
                              .gb-nl-pane / .gb-nl-table 的 7 处数值修正；modal 锁定
                              规则补 padding-right: var(--scrollbar-w, 0px)；
                              $build → 20260824-r25
改  assets/customstyle.css   编译产物
改  assets/main.js           modal.open() 加锁前测滚动条宽度写入 --scrollbar-w
改  全部 11 页 + font-check   ?v() → r25
改  ~/.claude/CLAUDE.md      通用铁律新增第 14 条：锁滚动条要补偿滚动条宽度
```
```

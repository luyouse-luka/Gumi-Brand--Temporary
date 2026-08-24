# Gumi Brand — 设计方交接说明与画布批注

> 来源：Figma `402:31998`「Handover Notes For Dev:」+ 散落在各页面稿旁的 30 个 `note` frame。
> 截图见 `figma/screenshots/402-31998_*.png` 与 `figma/screenshots/*_note_*.png`。
> **动手前必读。** 这些是设计方对开发的口头约定，节点数据里不体现。

## 一、交接说明原文（402:31998）

> Hi John,
>
> This is the MVP for desktop and mobile.
> It does not include the referral logic or the account section. We are still finalising those.
> We made it quickly. If something is unclear, use your judgement. If you are unsure how something should work, please ask.
> **Copy and images are not final yet.**
>
> One note: **the header may change later**, depending on the account section design. Changes could be small (layout) or bigger (new dropdown, links, or logo position).
> I don't know the best way to handle this from a dev side. If we build a basic header now and change it later, will that mean extra rework for you?
> What would you suggest? For example, is it possible to build a simple working header now and finish the final navigation design later? Without causing rework?
> Let me know your recommended approach.

### 由此推出的三条硬约束

1. **范围**：MVP 只含 desktop + mobile 页面。**referral 逻辑**与 **account 区块**不在本次范围（设计方仍在敲定）。Referral 页面**视觉稿**有，但其**逻辑**明确排除。
2. **文案与图片都不是最终版** → 按全局铁律 3，占位保留占位或标 `TODO 待客户文案`，**不编造像真的内容**，图片一卡一图不复用。
3. **header 会变** → 设计方在问「现在建基础 header、之后改，会不会造成返工」。**这是一个等着回复的问题**，见文末「待回复设计方」。

## 二、画布批注（22 条实质内容）

按主题归类。原文为中文，此处保留原意并补上节点号，便于回查。

### 交互与动效

| 节点 | 主题 | 要求 |
|---|---|---|
| `401:29596` `216:5903` | 交互效果 | 小熊软糖图形要有**浮动效果**，文字要有**淡入效果**。动画风格参考 https://www.cravburgers.shop/（汉堡图片的浮动 + 文字淡入） |
| `326:84892` | PRODUCT PAGE SCROLL | 产品图片**粘性定位固定不动**，页面其余内容正常滚动 |
| `401:31227` | NUTRITIONAL LABEL | 做成**从屏幕底部上滑**的面板；关闭时按原路径反向滑回 |

### 主题编辑器可编辑性（Shopify schema 需求）

| 节点 | 主题 | 要求 |
|---|---|---|
| `401:31444` | TEXT | 所有介绍性文字模块，编辑器里要有开关，**独立于主标题显示/隐藏副标题** |
| `401:31442` | CARD | 编辑器加切换开关，**独立显示/隐藏卡片的标题、副标题、描述** |
| `401:31994` | CTA BLOCKS | 所有**文字内容和链接**都必须编辑器可编辑 |
| `401:31219` | DESKTOP CARDS | 每张卡片的**跳转链接**、**按钮文字/标签**必须编辑器可编辑 |
| `401:31440` | IMAGE & TEXT | 图片区域做成**灵活的图片框架/占位**，方便编辑器换图或加图 |
| `401:29602` | LOGO SCROLL | 编辑器加开关控制该元素开/关。**开启时背景白色；关闭时下方区块的灰色背景向上延伸填充该区域** |
| `401:31225` | PDP 占位内容 | 退款保证下方的三个图标、以及 'tastes like' 的图标都是**占位符**，需编辑器可编辑/可替换 |

### 链接与跳转

| 节点 | 主题 | 要求 |
|---|---|---|
| `401:31217` | START YOUR GREENS 按钮 | 链接到 **PDP** |
| `401:31215` | DARK GREEN CARDS | **暂时不做点击跳转**（先不加链接） |
| `401:29598` | FOOTER LINKS | 手机端**同桌面端** |
| `326:79393` | 联系表单预填咨询类型 | 按钮功能与 **Funky 站点**类似 —— 点击跳转到联系我们页面并**自动预填相应咨询类别** |

### 布局与样式修复

| 节点 | 主题 | 要求 |
|---|---|---|
| `401:31229` | NAVIGATION | 移动端**全宽**显示 |
| `401:31717` | CART | 移动端**全宽**显示 |
| `401:31482` | HIGHLIGHTED TEXT | 现用描边样式**没完整包住所有字符**（句号被切）。需修复，确保描边一致包裹所有字符含标点 |
| `401:31452` | TEXT ON CURVED PATH | 文字变长时，容器/框架必须**动态扩展**，避免与下方内容重叠 |
| `401:31996` | BACK PAGES | 用**标准 Shopify 文本页面布局** + 品牌风格 header（指 FAQ / Shipping / Privacy Policy 这类页） |

### 功能性需求

| 节点 | 主题 | 要求 |
|---|---|---|
| `401:31223` | REVIEWS | ~~评论组件支持选传图片；点赞/点踩，赞多排前踩多排后~~ → **❌ 本次不实现**：评论由 Shopify 评论 app 产出（2026-08-19 用户定的边界，见 PROJECT-STATUS.md「实现边界」） |
| `401:31715` | REFERRAL PROGRAM LOGIC | **仍在确认中**（且 MVP 明确排除 referral 逻辑） |

### 空批注（占位，无内容）

`324:55034`、`324:61872`、`324:67971`、`324:71473`、`324:74462`、`326:80721`、`326:81918`
—— 内容均为 "Note information here"，是设计方留的空模板，**不是遗漏的需求**，不要照着猜。

## 三、待回复设计方 / 待用户拍板

| # | 事项 | 状态（2026-08-19） |
|---|---|---|
| 1 | **header 返工问题**（设计方直接问的） | 已给出建议方案；**用户指示暂时搁置**，不阻塞开工 |
| 2 | **STATISTICS 小熊图形**（`401:31213`） | ✅ **已定：用代码动态表示** |
| 3 | **PDP 占位图标格式**（`401:31225`） | **暂时忽略**，落地时再问 |

### 2 的决策详情

设计方原问题：**「每个百分比应使用静态图片，还是将小熊软糖图形通过代码动态高亮，以匹配输入的百分比数值？」**

**决策：代码动态高亮。** 即小熊软糖图形只有一份资源，按传入的百分比数值动态填充/高亮相应比例，
不为每个百分比各切一张静态图。

落地要点（写代码时回看这里）：

- 小熊图形导 **SVG**（按全局规范：icon / 图形类一律 SVG），填充比例靠**遮罩/裁切**控制，
  不要靠叠两张不同颜色的位图。
- 百分比是**输入值**（Shopify 阶段来自 schema setting，静态阶段先写死在 HTML 的 `data-*` 上），
  CSS 变量承载填充比例，便于主题编辑器改数值时无需改代码。
- ⚠ 全局记忆 [[cover-crop-breaks-percent-hotspots]]：若图形容器用了 `object-fit:cover`，
  按容器百分比定位的填充线会漂。填充比例必须相对**图形自身的 viewBox**算，不是相对容器盒。
- 对应稿件节点：`401:29604`（Homepage STATISTICS 数据块 60+ / 21 / 6g / 10+）。

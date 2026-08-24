# Gumi Brand — Figma 设计节点索引

> 数据来源：Figma REST API 直连（非 MCP）。所有数值以此处节点数据为准，不目测截图。

## 文件

| 项 | 值 |
|---|---|
| 文件名 | `Internal - Gumi Brand & Website` |
| File key | `R6ZWkjY1VNBAbljFhLjpuH` |
| URL | https://www.figma.com/design/R6ZWkjY1VNBAbljFhLjpuH/Internal---Gumi-Brand---Website |
| 最后修改 | 2026-08-19T05:48:26Z |
| version | `2389304678804694814` |
| 交付节点 | `401:31719` — SECTION **「Desktop & Mobile MVP (14/08/26)」** |
| 所属页面 | `-> Website - Desktop & Mobile MVP ✅`（`401:29271`），位于 **🟢 READY FOR DEV** 分组下 |

文件共 26 个 Figma 页面，分组：READY FOR DEV / WIP / BRANDING / IMAGES / SOCIAL MEDIA / Archive。
**本次交付范围只有 READY FOR DEV 下的 `401:31719`**，其余（WIP、Account Wire Frame、Flow Mapping、Archive）不在范围内。

SECTION `401:31719` 直接子节点共 88 个：70 FRAME + 15 GROUP + 2 INSTANCE + 1 RECTANGLE。
其中 30 个 FRAME 名为 `note`（画布批注），15 个 GROUP 为页面标题装饰条。

## ⚠ 必读：开发交接说明

| 节点 | 名称 | 尺寸 |
|---|---|---|
| `402:31998` | **Handover Notes For Dev:** | 1440×960 |

外加 30 个 `note` 批注 frame（337×68 ~ 337×320），散落在各页面稿旁。
**动手前必须先读这两类内容**，它们承载设计方对开发的口头约定。

## 页面稿（Desktop ↔ Mobile 配对）

配对依据：画布 x 坐标相邻成对（desktop 在左、mobile 在右），归属已逐个用首屏文案核实。

| # | 页面 | Desktop 节点 | 尺寸 | Mobile 节点 | 尺寸 | 归属确认 |
|---|---|---|---|---|---|---|
| 1 | Homepage | `285:18162` | 1440×10123 | `228:5932` | 390×11543 | ✅ 名称明确 |
| 2 | Product Page (PDP) | `324:52658` | 1440×9934 | `324:53792` | 390×10534 | ✅ 名称明确 |
| 3 | Science | `324:56865` | 1440×5750 | `324:58044` | 390×7352 | ✅ 名称明确 |
| 4 | Reviews | `324:63924` | 1440×9066 | `324:64961` | 390×9182 | ✅ 名称明确 |
| 5 | How Gumi Works | `324:69636` | 1440×8144 | `324:70523` | 390×8613 | ✅ 名称明确 |
| 6 | Our Story | `324:72839` | 1440×7155 | `324:73673` | 390×8468 | ✅ 名称明确 |
| 7 | FAQ | `324:75766`（稿名 Our Story Desktop） | 1440×3063 | `324:76169` | 390×3184 | ✅ 已核实（首屏 "Frequently asked questions"） |
| 8 | Get in Touch | `326:79979`（稿名 Our Story Desktop） | 1440×2863 | `326:80318` | 390×2848 | ✅ 已核实（首屏 "Let's talk gummies"） |
| 9 | Referral | `326:81218`（稿名 Our Story Desktop） | 1440×2647 | `326:81540` | 390×2790 | ✅ 已核实（首屏 "Join the Gumi movement"） |
| 10 | Privacy Policy | `326:82363`（稿名 Our Story Desktop） | 1440×4347 | `326:83399` | 390×4864 | ✅ 已核实（首屏 "Privacy Policy"） |
| 11 | Shipping | **无独立 desktop 稿** | — | `326:83129` | 390×3352 | ⚠ 见下方说明 |

⚠ 上述 4 个 desktop 稿在 Figma 里都叫「Our Story Desktop」（复制后未改名），已按首屏标题逐个开图核实，
上表归属为**核实结果**而非坐标推断。

**Shipping 没有 desktop 稿** —— 按批注 `401:31996`「BACK PAGES 使用标准的 Shopify 文本页面布局，
并应用品牌风格 header」，FAQ / Shipping / Privacy Policy 属同一类文本页，Shipping 桌面端可复用
Privacy Policy 的布局。**这是推断，落地前需向设计方确认。**

**断点基准：Desktop 1440px / Mobile 390px。** 无 tablet 稿 —— 中间区间的行为需按响应式规则自行推导（拥挤优先缩间距，见全局铁律 10）。

## 组件与状态稿

### 导航
| 节点 | 名称 | 尺寸 | 说明 |
|---|---|---|---|
| `401:31720` | Header Navigation Desktop/Closed | 1440×80 | INSTANCE，桌面导航收起态 |
| `401:31721` | Header Navigation Desktop/Open | 1440×80 | INSTANCE，桌面导航展开态 |
| `283:15014` | Nav Collapsed | 391×840 | 手机导航收起 |
| `283:14915` | Nav Expanded | 391×1224 | 手机导航展开 |

### 购物车
| 节点 | 名称 | 尺寸 |
|---|---|---|
| `341:42573` | Desktop Cart | 1440×768 |
| `341:42749` | Desktop Cart Empty | 1440×768 |
| `336:36516` | Mobile Cart | 390×1272 |
| `336:34942` | Mobile Cart - Empty | 390×844 |

### 弹窗
| 节点 | 名称 | 尺寸 | 端 |
|---|---|---|---|
| `336:31534` | Desktop Nutritional Label Pop up | 1440×768 | 桌面 |
| `336:34120` | Desktop Nutritional Label Pop up | 1440×768 | 桌面（第二态） |
| `336:28414` | Nutritional Label Pop up | 390×839 | 手机 |
| `336:29511` | Nutritional Label Pop up | 390×839 | 手机 |
| `336:31949` | Nutritional Label Pop up | 390×839 | 手机 |
| `336:32296` | Nutritional Label Pop up | 390×839 | 手机 |
| `285:18988` | Pop up | 390×840 | 手机 |
| `285:19179` | Pop up | 390×840 | 手机 |
| `285:19373` | 首单折扣弹窗（桌面） | 1440×768 | 稿名叫 Homepage Desktop，实为 "Get 20% off your first order!" 邮箱换码弹窗 |

营养标签弹窗有 4 个手机版 + 2 个桌面版，互为不同状态或不同产品 —— 需开图区分，不可假设重复。

### 其他
| 节点 | 名称 | 尺寸 | 说明 |
|---|---|---|---|
| `196:18017` | Input Drop Down | 320×44 | 表单下拉，对应批注 `326:79393` 联系表单预填咨询类型 |
| `401:29604` | Homepage Desktop（局部） | 557×541 | Homepage 的 STATISTICS 数据块（60+ / 21 / 6g / 10+），对应批注 `401:31213` |
| `341:47527` | Frame 1984078220 | 790×136 | 媒体背书 logo 滚动条（ABC NEWS / WellBeing / VOGUE），对应批注 `401:29602` LOGO SCROLL |

## 落盘位置

```
figma/
├── raw/
│   ├── file-depth1.json              # 文件顶层结构（26 页面）
│   └── node-401-31719-d1.json        # 交付 SECTION 一层子节点清单
├── nodes/                            # 42 个 frame 完整节点树 + notes-batch-1~3.json（geometry=paths）
├── screenshots/                      # 72 张参考截图（PNG @1x）
├── fetch-nodes.py                    # 节点拉取（断点续传：已落盘的自动跳过）
├── fetch-shots.py                    # 截图拉取
├── extract-tokens.py                 # 生成 DESIGN-TOKENS.md + docs/copy/
├── run-all.sh                        # 串行跑 fetch-nodes → fetch-shots（token 走 FIGMA_TOKEN 环境变量）
├── nodes-index.json                  # 节点文件索引
└── screenshots-manifest.json         # 截图清单
docs/
├── PROJECT-STATUS.md                 # 项目定位、规范、进度、待确认事项
├── FIGMA-NODES.md                    # 本文件
├── HANDOVER-NOTES.md                 # ⚠ 设计方交接说明 + 22 条画布批注
├── DESIGN-TOKENS.md                  # 字体/颜色/圆角/阴影汇总 + 字符级覆盖清单
└── copy/                             # 71 份逐页文案清单

交付目录（2026-08-19 建，规范见 PROJECT-STATUS.md「项目文件结构」）：
*.html                                # 页面放根目录
assets/{css,scss,js,fonts,icons}/
images/                               # ⚠ 顶层，不在 assets 下
```

重跑：`bash figma/run-all.sh`（设计更新后先删掉 `figma/nodes/` 里要重拉的文件，脚本会跳过已存在的）。

## 拉取进度

| 项 | 状态 |
|---|---|
| 文件结构 | ✅ 完成 |
| SECTION 子节点清单 | ✅ 完成（88 个） |
| 完整节点树 | ✅ **42/42** frame + 30 条 note（3 个批次文件） |
| 截图 | ✅ **72/72** 张 PNG @1x |
| Handover Notes / note 批注 | ✅ 已提取成文 → [HANDOVER-NOTES.md](HANDOVER-NOTES.md) |
| 设计 token | ✅ 已汇总 → [DESIGN-TOKENS.md](DESIGN-TOKENS.md) |
| 逐页文案 | ✅ 71 份 → `docs/copy/` |

### 限流记录

**2026-08-19 06:27 UTC — token `figd_bT5R…vjyT`（john@olivergrace.com.au, pro）配额耗尽：**

| 端点 | 状态 |
|---|---|
| `/v1/me` | 200 |
| `/v1/files/{key}?depth=1` | 200（浅层，成本低） |
| `/v1/files/{key}/nodes?ids=…` | **429**，`retry-after: 399832`（≈4.6 天） |
| `/v1/images/{key}?ids=…` | **429**，`retry-after: 398958`（≈4.6 天） |

`x-figma-rate-limit-type: low` = 账号级成本配额耗尽，非瞬时突发限流。
**诱因**：起初用 figma-parser 的 `--scan` 走全量 `/v1/files`，在这个 26 页的大文件上挂了 10 分钟没返回，
很可能就是它吃光了配额。**这个文件不要再跑 `--scan`。**

**2026-08-19 07:0x — 换 token `figd_jf9y…MOiWc`（dev@mockuptocode.com）后三个端点全部 200，拉取一次跑完。**

按 [[figma-bbox-unreliable-and-429-per-account]]：429 按账号计，换其他账号的 PAT 即可绕开；
同账号再建新 token 无效；`/v1/me` 返回 200 不代表没限流。

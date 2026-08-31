# Gumi Brand — 静态站

Shopify 前端项目（gumi.com.au）的静态实现阶段：**11 个页面全部落地**，
设计源为 Figma `Internal - Gumi Brand & Website` 的 SECTION `401:31719`
「Desktop & Mobile MVP (14/08/26)」。当前 `$build` = `20260828-r54`（第五十二轮）。

> ⚠ **这是临时同步仓库**。设计源（`figma/`）与验证产物（`tools/snap`、`tools/shots`）
> 不在这里，它们留在服务器上的 `/home/ly/project/Gumi-Brand/`。

## 先读这三份

| 文档 | 内容 |
|---|---|
| [docs/HANDOFF.md](docs/HANDOFF.md) | **接手先读**：不要报成 bug 的清单 / 验证怎么跑 / 对稿方法 / 历轮踩到的坑 / 待决索引 |
| [docs/PROJECT-STATUS.md](docs/PROJECT-STATUS.md) | 项目定位、断点体系、目录约定、仍未关闭的待决事项 |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | 改动记录（近 10 轮）。第一～三十轮在 [CHANGELOG-ARCHIVE.md](docs/CHANGELOG-ARCHIVE.md)，**查历史两份一起 grep** |

另有 [docs/DESIGN-TOKENS.md](docs/DESIGN-TOKENS.md)、[docs/FIGMA-NODES.md](docs/FIGMA-NODES.md)、
[docs/HANDOVER-NOTES.md](docs/HANDOVER-NOTES.md)（设计方的 22 条批注）；
逐轮进度与已关闭的待决在 [docs/PROJECT-STATUS-ARCHIVE.md](docs/PROJECT-STATUS-ARCHIVE.md)，
三份旧交接文档的原文在 [docs/archive/](docs/archive/)。

## 目录

```
*.html          11 个页面（index / pdp / science / reviews / how-gumi-works /
                our-story / faq / get-in-touch / referral / privacy-policy / shipping）
                + font-check.html（构建自检：版本号 + 功能探针 + 字体表）
assets/         ⚠ 扁平，不建任何子目录（Shopify 主题 assets 的硬约束）
                customstyle.scss  样式源码，全站唯一一份
                customstyle.css   编译产物，勿手改
                main.js  /  woff2  /  svg
                lenis.min.js / swiper-bundle.min.js  vendor 原件，勿手改；
                  Swiper 用到的样式摘进了 customstyle.scss 的「Vendor」分区，
                  没有第二个样式表
images/         ⚠ 图片在顶层，与 assets 平级（不是 assets/images）
tools/          验证脚本，不进交付
docs/           项目文档，不进交付
```

## 改样式

```bash
npx sass@1.77.8 assets/customstyle.scss assets/customstyle.css --no-source-map
```

改完把 `customstyle.scss` 顶部的 `$build` 加一版，并同步全站 `?v=`：

```bash
sed -i 's/20260828-r54/20260828-r55/g' *.html   # ?v= 38 处 + font-check 的 EXPECT_BUILD 1 处
```

反馈「改了没生效」时，先让对方硬刷新，再看 `font-check.html` 顶部的版本横幅。

## 验证

```bash
python3 tools/rwd.py            # 12 页 × 14 档宽度：横向溢出 / 文字被裁 / 滚轮黑洞
python3 tools/revealcheck.py    # 入场动效收尾
python3 tools/cssnap.py before  # 改选择器名、搬 @media、合并文件时唯一有效的判据
python3 tools/r53check.py       # 最近一轮的专项判据（r31/r32/r36/r39～r45/r48/r50/r52 同理）
python3 tools/emptyline.py      # 全站行盒数 == 视觉行数（动 <br> 或 lineReveal 后必跑）
python3 tools/platecheck.py     # CTA 板圆瓣几何（像素级，动 scallop-tile 后必跑）
python3 tools/seamcheck.py      # CTA 板接缝（8 档 DPR 含分数缩放；与 platecheck 成对）
python3 tools/scrolllock.py     # 弹窗/抽屉锁滚动不得让页面横向位移（判据自带真实滚动条，缺则 abort）
python3 tools/r42rect.py r41 1440   # 不变量档矩形比对（cssnap 跑不动时用）
```

完整跑法与判据纪律见 [docs/HANDOFF.md](docs/HANDOFF.md) 第二节。

## 上线前必须替换的占位内容

- **Reviews 专家卡引用里有竞品名 Grüns**（设计师抄的参考站文案）
- **Shipping 全页写的是美国配送**（Alaska / Hawaii / US Territories / $65 门槛），而 Gumi 是澳洲品牌
- **Privacy Policy 正文是 lorem ipsum**
- **PP Palma 300（FizzyLight）仍是试用包**，EULA 排除商业用途。400/500/800 已是客户授权文件；
  切换点是 `customstyle.scss` 的四条 `@font-face`，只改 `src`

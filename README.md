# Gumi Brand — 静态站

Shopify 前端项目（gumi.com.au）的静态实现阶段：**11 个页面全部落地**，
设计源为 Figma `Internal - Gumi Brand & Website` 的 SECTION `401:31719`
「Desktop & Mobile MVP (14/08/26)」。

> ⚠ **这是临时同步仓库**。设计源（`figma/`）与验证产物（`tools/snap`、`tools/shots`）
> 不在这里，它们留在服务器上的 `/home/ly/project/Gumi-Brand/`。

## 先读这两份

| 文档 | 内容 |
|---|---|
| [docs/PROJECT-STATUS.md](docs/PROJECT-STATUS.md) | 项目定位、断点体系、目录约定、待决事项、进度 |
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | 十九轮改动记录：改了什么 / 为什么 / 文件清单 / 遗留 |

另有 [docs/AUDIT-HANDOFF.md](docs/AUDIT-HANDOFF.md)（要做审计的会话读这份，含「不要报成 bug 的清单」）、
[docs/DESIGN-TOKENS.md](docs/DESIGN-TOKENS.md)、[docs/FIGMA-NODES.md](docs/FIGMA-NODES.md)、
[docs/HANDOVER-NOTES.md](docs/HANDOVER-NOTES.md)（设计方的 22 条批注）。

## 目录

```
*.html          11 个页面（index / pdp / science / reviews / how-gumi-works /
                our-story / faq / get-in-touch / referral / privacy-policy / shipping）
                + font-check.html（构建自检：版本号 + 37 条功能探针 + 字体表）
assets/         ⚠ 扁平，不建任何子目录（Shopify 主题 assets 的硬约束）
                customstyle.scss  样式源码，全站唯一一份
                customstyle.css   编译产物，勿手改
                main.js  /  lenis.min.js  /  19 个 woff2  /  44 个 svg
images/         ⚠ 图片在顶层，与 assets 平级（不是 assets/images）
tools/          验证脚本，不进交付
docs/           项目文档，不进交付
```

## 改样式

```bash
npx sass@1.77.8 assets/customstyle.scss assets/customstyle.css --no-source-map
```

改完把 `customstyle.scss` 里的 `$build` 加一版，并同步全站 `?v=`：

```bash
sed -i 's/?v=20260824-r20/?v=20260824-r21/g' *.html
```

反馈「改了没生效」时，先让对方硬刷新，再看 `font-check.html` 顶部的版本横幅。

## 验证

```bash
python3 tools/rwd.py           # 11 页 × 10 档宽度：横向溢出 / 文字被裁 / 滚轮黑洞
python3 tools/shoot.py --all   # 同上 + 全页截图 + 卡住的入场动画
python3 tools/cssnap.py before # 改选择器名、搬 @media、合并文件时唯一有效的判据
python3 tools/r19check.py      # 第十九轮 7 条任务的专项判据
```

## 上线前必须替换的占位内容

- **Reviews 专家卡引用里有竞品名 Grüns**（设计师抄的参考站文案）
- **Shipping 全页写的是美国配送**（Alaska / Hawaii / US Territories / $65 门槛），而 Gumi 是澳洲品牌
- **Privacy Policy 正文是 lorem ipsum**
- **PP Palma 是商业字体，目前用试用包占位**，400 字重（全站 59% 用量）试用包不提供、
  现指向 Fizzy Light。上线前需要客户的授权 web font，切换点只有 `customstyle.scss`
  的 `$font-brand-stack` 一处。

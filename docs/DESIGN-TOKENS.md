# Gumi Brand — 设计 token 汇总

> 来源：`figma/nodes/` 共 45 个节点文件（SECTION `401:31719` 全部 frame）。
> 由 `figma/extract-tokens.py` 生成，改动设计后重跑即可。

## 字体族与文件状态

⚠ 本节手写，`extract-tokens.py` 重跑不会覆盖。字重统计已含 `styleOverrideTable` 里的字符级覆盖。

| 字体 | 出现 | 需要字重 | 授权 | 本地文件 |
|---|---|---|---|---|
| **PP Palma** | 3298 | 300 / 400 / 500 / 800 | Pangram Pangram **商业字体** | ❌ 无 → 暂用 Figtree 占位 |
| **Inter** | 409 | 400 / 500 / 600 / 700 / 800 | OFL 免费 | ✅ 可变字体，1 文件覆盖全字重 |
| **Lexend** | 108 | 400 / 600 / 700 | OFL 免费 | ✅ 可变字体 |
| **Playpen Sans** | 90 | 600 | OFL 免费 | ✅ **静态实例**，只有 600 |
| ~~SF Pro Text~~ | 11 | — | — | ❌ **不是字体需求**，见下 |

**SF Pro Text 的 11 处全是同一个字符 `U+100668`**（Unicode 私有区），是设计师用 **SF Symbols
打的图标占位**，出现在每个 desktop 稿顶部紧挨 "Excellent / Truspilot" —— 即 **Trustpilot 星标**。
实现时导 SVG，不要去找 SF Pro 字体。且该徽章已按「Shopify app 生成内容」边界排除。

### PP Palma 现状

官方 FAQ 原文：**"All of our fonts are free to try for personal use as long as it is not used in
a commercial project."** 试用文件**通过邮箱订阅发放**（提交邮箱后邮件收取），不能直链下载；
且试用授权**明确排除商业项目** —— Gumi 是商业站，试用版只能用于本地还原比对，不能上线。

**当前处理**：`assets/customstyle.scss` 的 `@font-face` 段里 PP Palma 只声明 `local()`，
装了正版的机器直接命中，没装则落到占位字体。**占位 = Figtree**（OFL 可变字体，
geo-humanist，与 Palma 官方描述的 "inspired by Antique Olive / Johnston / Avenir" 同一谱系）。
第二候选 **Plus Jakarta Sans** 也已下载，切换只需改 `$font-brand-alt` 一处 + 解开两块注释。

⚠ **拿到正版 woff2 后**：放进 `assets/`（平铺，无子目录），在 PP Palma 那条 `@font-face` 的
`src: local(...)` 后面补 `url(...)`。**不要去各组件里改 `font-family`** ——
全站都走 `$font-brand-stack`。

⚠ 占位字体与 PP Palma 的**字宽度量不同**，`letter-spacing`（稿中多为 -0.02em）
和换行位置会有出入。**换字体前不要做像素级还原验收**，那时的偏差不代表实现错了。

### 可变字体 vs 静态实例（md5 实测）

| 字体 | 各字重文件 md5 | 结论 | `@font-face` 写法 |
|---|---|---|---|
| Inter | 5 个字重 **同一 md5** | 可变字体 | `font-weight: 100 900` 范围 |
| Lexend | 3 个字重 **同一 md5** | 可变字体 | `font-weight: 100 900` 范围 |
| Playpen Sans | 100/600/800 **三个不同 md5** | 静态实例 | `font-weight: 600` 单值 |

⚠ 这个区别不能想当然：**可变字体若写单个 `font-weight` 值，浏览器会按默认 instance 渲染**
（通常 400），Medium/Bold 就静默失效了。反过来静态实例写范围也不对。判据是 md5 比对，不是猜。

## 字体样式（139 种组合）

| family | weight | size | line-height | letter-spacing | case | align | 出现 |
|---|---|---|---|---|---|---|---|
| PP Palma | 400 | 16.0px | 24.0px | -0.32px |  | LEFT | 762 |
| PP Palma | 400 | 14.0px | 20.0px | -0.28px |  | LEFT | 383 |
| Inter | 600 | 16.0px | 24.0px | 0.0px |  | LEFT | 286 |
| PP Palma | 500 | 16.0px | 24.0px | -0.32px |  | LEFT | 174 |
| PP Palma | 400 | 16.0px | 24.0px | -0.32px |  | CENTER | 163 |
| PP Palma | 300 | 9.5px | 12.0px | 0.0px |  | LEFT | 162 |
| PP Palma | 500 | 16.0px | 28.0px | 0.48px | TITLE | LEFT | 118 |
| PP Palma | 400 | 18.0px | 28.0px | -0.36px |  | LEFT | 89 |
| PP Palma | 400 | 14.0px | 20.0px | -0.28px |  | RIGHT | 82 |
| PP Palma | 300 | 12.9px | 16.2px | 0.0px |  | LEFT | 81 |
| PP Palma | 500 | 16.0px | 24.0px | -0.32px |  | CENTER | 64 |
| PP Palma | 800 | 32.2px | 37.2px | -0.32px |  | CENTER | 57 |
| Playpen Sans | 600 | 1.5px | 2.1px | -0.03px |  | LEFT | 54 |
| PP Palma | 500 | 16.0px | 20.0px | 0.0px |  | CENTER | 51 |
| PP Palma | 400 | 14.0px | 20.0px | -0.28px |  | CENTER | 48 |
| PP Palma | 400 | 12.0px | 18.0px | -0.24px |  | LEFT | 47 |
| PP Palma | 500 | 16.0px | 24.0px | 0.0px |  | LEFT | 41 |
| PP Palma | 400 | 18.0px | 28.0px | -0.36px |  | CENTER | 41 |
| PP Palma | 400 | 12.0px | 18.0px | -0.24px |  | RIGHT | 40 |
| PP Palma | 400 | 6.2px | 9.3px | -0.12px |  | LEFT | 39 |
| PP Palma | 500 | 14.0px | 20.0px | 0.0px |  | LEFT | 38 |
| Lexend | 600 | 10.0px | 18.0px | -0.2px |  | CENTER | 32 |
| PP Palma | 800 | 36.0px | 40.0px | -0.36px |  | CENTER | 31 |
| PP Palma | 500 | 17.6px | 18.1px | 0.0px |  | CENTER | 30 |
| PP Palma | 800 | 30.0px | 36.0px | -0.3px |  | LEFT | 26 |
| Lexend | 600 | 12.0px | 18.0px | 0.0px |  | LEFT | 26 |
| Playpen Sans | 600 | 1.3px | 1.8px | -0.03px |  | LEFT | 25 |
| PP Palma | 400 | 16.0px | 24.0px | 0.0px |  | LEFT | 25 |
| PP Palma | 400 | 16.0px | 24.0px | 0.0px |  | CENTER | 24 |
| PP Palma | 400 | 14.0px | 22.0px | -0.28px |  | CENTER | 24 |
| Inter | 400 | 16.0px | 19.4px | 0.0px |  | CENTER | 21 |
| PP Palma | 500 | 18.0px | 26.0px | -0.36px |  | CENTER | 21 |
| PP Palma | 400 | 14.0px | 22.0px | -0.28px |  | RIGHT | 20 |
| PP Palma | 500 | 15.3px | 21.8px | 0.0px |  | CENTER | 20 |
| PP Palma | 800 | 40.0px | 48.0px | -0.4px |  | CENTER | 19 |
| Inter | 500 | 20.0px | 28.0px | 0.0px |  | LEFT | 19 |
| PP Palma | 400 | 16.0px | 24.0px | -0.32px |  | RIGHT | 18 |
| PP Palma | 500 | 12.0px | 20.0px | 0.0px |  | LEFT | 18 |
| PP Palma | 800 | 30.0px | 36.0px | -0.3px |  | CENTER | 17 |
| PP Palma | 500 | 18.0px | 28.0px | 0.0px | TITLE | LEFT | 17 |
| PP Palma | 800 | 24.0px | 30.0px | -0.24px |  | LEFT | 16 |
| PP Palma | 400 | 6.2px | 9.3px | -0.12px |  | CENTER | 16 |
| PP Palma | 500 | 14.0px | 20.0px | 0.56px | UPPER | LEFT | 15 |
| PP Palma | 800 | 56.0px | 44.0px | 0.0px |  | LEFT | 15 |
| Inter | 600 | 6.2px | 9.3px | 0.0px |  | LEFT | 15 |
| PP Palma | 800 | 24.0px | 30.0px | -0.24px |  | CENTER | 14 |
| PP Palma | 800 | 32.0px | 40.0px | -0.32px |  | LEFT | 14 |
| PP Palma | 500 | 18.0px | 24.0px | -0.36px |  | CENTER | 14 |
| Lexend | 600 | 14.0px | 18.0px | 0.0px |  | LEFT | 12 |
| Lexend | 600 | 16.0px | 24.0px | 0.0px |  | LEFT | 12 |
| Lexend | 400 | 12.0px | 18.0px | 0.0px |  | LEFT | 12 |
| PP Palma | 500 | 11.9px | 12.2px | 0.0px |  | CENTER | 12 |
| PP Palma | 800 | 32.0px | 40.0px | -0.32px |  | CENTER | 11 |
| SF Pro Text | 400 | 19.1px | 22.8px | 0.0px |  | CENTER | 11 |
| Inter | 800 | 20.0px | 28.0px | 0.0px |  | LEFT | 11 |
| Inter | 400 | 14.6px | 17.7px | -0.06px |  | LEFT | 10 |
| PP Palma | 500 | 12.0px | 15.5px | -0.12px |  | LEFT | 10 |
| PP Palma | 400 | 12.0px | 15.5px | -0.12px |  | LEFT | 10 |
| PP Palma | 500 | 6.2px | 9.3px | -0.12px |  | LEFT | 10 |
| PP Palma | 400 | 18.0px | 26.0px | -0.36px |  | CENTER | 9 |
| PP Palma | 800 | 16.1px | 18.9px | 0.0px |  | LEFT | 9 |
| PP Palma | 500 | 9.1px | 11.4px | 0.0px |  | LEFT | 9 |
| PP Palma | 500 | 12.0px | 12.0px | 0.48px | UPPER | LEFT | 9 |
| PP Palma | 500 | 16.0px | 20.0px | 0.64px | UPPER | LEFT | 9 |
| PP Palma | 800 | 32.6px | 38.3px | 0.0px |  | LEFT | 9 |
| PP Palma | 500 | 18.4px | 23.2px | 0.0px |  | LEFT | 9 |
| PP Palma | 800 | 20.0px | 24.0px | -0.2px |  | LEFT | 9 |
| PP Palma | 800 | 12.6px | 14.8px | 0.0px |  | LEFT | 9 |
| PP Palma | 500 | 7.1px | 9.0px | 0.0px |  | LEFT | 9 |
| PP Palma | 400 | 14.0px | 20.0px | 0.0px |  | LEFT | 8 |
| PP Palma | 500 | 6.2px | 9.3px | -0.12px |  | CENTER | 8 |
| PP Palma | 800 | 56.0px | 64.0px | -0.56px |  | CENTER | 7 |
| PP Palma | 800 | 40.0px | 48.0px | -0.4px |  | LEFT | 6 |
| PP Palma | 500 | 12.5px | 12.8px | 0.0px |  | CENTER | 6 |
| PP Palma | 400 | 12.0px | 20.0px | 0.0px |  | RIGHT | 6 |
| PP Palma | 400 | 14.0px | 20.0px | 0.0px |  | RIGHT | 6 |
| PP Palma | 400 | 7.0px | 10.8px | -0.14px |  | CENTER | 6 |
| PP Palma | 400 | 7.0px | 10.8px | -0.14px |  | LEFT | 6 |
| Playpen Sans | 600 | 12.5px | 17.9px | -0.25px |  | LEFT | 5 |
| PP Palma | 400 | 14.0px | 22.0px | -0.28px |  | LEFT | 5 |
| Playpen Sans | 600 | 0.5px | 0.7px | -0.01px |  | LEFT | 5 |
| PP Palma | 400 | 5.4px | 8.5px | -0.11px |  | CENTER | 5 |
| PP Palma | 500 | 7.0px | 9.3px | -0.14px |  | CENTER | 5 |
| PP Palma | 800 | 20.0px | 24.0px | -0.2px |  | CENTER | 4 |
| PP Palma | 400 | 12.0px | 18.0px | -0.24px |  | CENTER | 4 |
| PP Palma | 800 | 46.7px | 51.3px | 0.0px |  | CENTER | 4 |
| PP Palma | 500 | 18.0px | 26.0px | -0.36px |  | LEFT | 4 |
| PP Palma | 800 | 36.0px | 40.0px | -0.36px |  | LEFT | 4 |
| Inter | 400 | 14.0px | 20.0px | 0.0px |  | LEFT | 4 |
| PP Palma | 300 | 9.7px | 12.6px | 0.0px |  | LEFT | 4 |
| PP Palma | 800 | 18.0px | 19.9px | 0.0px |  | CENTER | 4 |
| PP Palma | 800 | 9.3px | 11.6px | -0.09px |  | CENTER | 4 |
| PP Palma | 400 | 5.4px | 8.5px | -0.11px |  | RIGHT | 4 |
| PP Palma | 400 | 5.4px | 7.7px | -0.11px |  | LEFT | 4 |
| PP Palma | 400 | 16.0px | 22.0px | 0.0px |  | CENTER | 3 |
| PP Palma | 800 | 40.0px | 44.0px | -0.4px |  | CENTER | 3 |
| PP Palma | 500 | 16.0px | 20.0px | 0.64px | UPPER | CENTER | 3 |
| PP Palma | 500 | 14.0px | 20.0px | 0.56px | UPPER | CENTER | 3 |
| PP Palma | 800 | 15.5px | 18.6px | -0.15px |  | CENTER | 3 |
| PP Palma | 500 | 6.2px | 7.7px | 0.25px | UPPER | LEFT | 3 |
| PP Palma | 800 | 21.7px | 17.0px | 0.0px |  | LEFT | 3 |
| PP Palma | 800 | 12.4px | 15.5px | -0.12px |  | CENTER | 3 |
| PP Palma | 500 | 7.0px | 10.8px | 0.0px | TITLE | LEFT | 3 |
| PP Palma | 500 | 6.2px | 10.8px | 0.19px | TITLE | LEFT | 3 |
| PP Palma | 800 | 12.5px | 14.4px | -0.12px |  | CENTER | 3 |
| PP Palma | 400 | 20.0px | 30.0px | -0.4px |  | CENTER | 2 |
| PP Palma | 400 | 20.0px | 30.0px | -0.4px |  | LEFT | 2 |
| Lexend | 600 | 18.0px | 22.0px | 0.0px |  | LEFT | 2 |
| PP Palma | 800 | 66.2px | 52.0px | 0.0px |  | CENTER | 2 |
| PP Palma | 800 | 56.0px | 44.0px | 0.0px |  | CENTER | 2 |
| PP Palma | 800 | 56.0px | 64.0px | -0.56px |  | LEFT | 2 |
| PP Palma | 500 | 9.5px | 12.0px | 0.0px |  | LEFT | 2 |
| PP Palma | 300 | 13.1px | 17.0px | 0.0px |  | LEFT | 2 |
| PP Palma | 500 | 20.0px | 24.0px | 0.0px |  | CENTER | 2 |
| PP Palma | 400 | 12.0px | 18.0px | 0.0px |  | LEFT | 2 |
| PP Palma | 400 | 4.6px | 7.0px | -0.09px |  | LEFT | 2 |
| PP Palma | 500 | 5.4px | 7.7px | 0.0px |  | LEFT | 2 |
| PP Palma | 400 | 13.7px | 20.6px | -0.27px |  | LEFT | 2 |
| PP Palma | 800 | 40.0px | 44.0px | 0.0px |  | CENTER | 1 |
| PP Palma | 800 | 60.0px | 72.0px | -0.6px |  | LEFT | 1 |
| PP Palma | 800 | 24.5px | 32.7px | 0.49px |  | LEFT | 1 |
| PP Palma | 800 | 15.8px | 21.1px | 0.32px |  | LEFT | 1 |
| PP Palma | 400 | 18.0px | 26.0px | -0.36px |  | LEFT | 1 |
| PP Palma | 800 | 30.0px | 38.0px | 0.0px |  | LEFT | 1 |
| PP Palma | 500 | 12.9px | 16.2px | 0.0px |  | LEFT | 1 |
| PP Palma | 800 | 21.7px | 24.7px | -0.22px |  | CENTER | 1 |
| PP Palma | 400 | 7.7px | 11.6px | -0.15px |  | CENTER | 1 |
| Playpen Sans | 600 | 4.9px | 6.9px | -0.1px |  | LEFT | 1 |
| PP Palma | 800 | 12.4px | 15.5px | -0.12px |  | LEFT | 1 |
| PP Palma | 400 | 5.4px | 7.7px | -0.11px |  | RIGHT | 1 |
| PP Palma | 500 | 5.4px | 7.7px | 0.22px | UPPER | LEFT | 1 |
| PP Palma | 400 | 5.4px | 8.5px | -0.11px |  | LEFT | 1 |
| PP Palma | 400 | 6.2px | 9.3px | 0.0px |  | CENTER | 1 |
| PP Palma | 800 | 13.9px | 15.5px | -0.14px |  | CENTER | 1 |
| Inter | 400 | 5.7px | 6.8px | -0.02px |  | LEFT | 1 |
| PP Palma | 500 | 6.2px | 9.3px | 0.0px |  | LEFT | 1 |
| PP Palma | 800 | 23.2px | 27.8px | -0.23px |  | LEFT | 1 |
| PP Palma | 400 | 7.7px | 11.6px | -0.15px |  | LEFT | 1 |
| PP Palma | 400 | 13.7px | 20.6px | -0.27px |  | RIGHT | 1 |

## 颜色（95 种）

| 值 | 出现 |
|---|---|
| `#D9D9D9` | 1303 |
| `#B5ED61` | 1110 |
| `#005635` | 1066 |
| `#011307` | 713 |
| `#FFFFFF` | 661 |
| `#4D4D4D` | 556 |
| `#005635 (stroke)` | 520 |
| `#B5ED61 (stroke)` | 420 |
| `#85C947` | 330 |
| `#004128` | 324 |
| `#F4FCE7` | 275 |
| `#E9D7FE` | 275 |
| `#1B1C1E` | 250 |
| `#666666` | 249 |
| `#FFFFFF (stroke)` | 235 |
| `#DAF6B0` | 206 |
| `#333333` | 188 |
| `#FAF9F8` | 175 |
| `#E7F8D0` | 168 |
| `#EEEEEE` | 143 |
| `#011307 @0.05` | 141 |
| `#47AC00 (stroke)` | 105 |
| `#EEC644` | 104 |
| `#737373` | 88 |
| `#101828` | 82 |
| `#F5F1E9` | 60 |
| `#000000 (stroke)` | 56 |
| `#000000` | 55 |
| `#666666 (stroke)` | 54 |
| `#CCCCCC (stroke)` | 53 |
| `#F9FFF1` | 53 |
| `#1A1A1A` | 49 |
| `#4D4D4D (stroke)` | 47 |
| `#667085 (stroke)` | 46 |
| `#98A2B3 (stroke)` | 46 |
| `#DAF6B0 (stroke)` | 40 |
| `#011307 (stroke)` | 38 |
| `#FF3B30` | 37 |
| `#DD655E` | 35 |
| `#D9D9D9 (stroke)` | 31 |
| `#808080` | 31 |
| `#D154ED` | 30 |
| `#011307 @0.1 (stroke)` | 25 |
| `#808080 (stroke)` | 24 |
| `#E7EAED` | 21 |
| `#CBF390` | 20 |
| `#011307 @0.05 (stroke)` | 20 |
| `#D5D4D4` | 20 |
| `#DD655E (stroke)` | 20 |
| `#656565` | 19 |
| `#F6FEEC (stroke)` | 18 |
| `#DDEADD` | 16 |
| `#F5DAD8` | 16 |
| `#EEC644 @0.3` | 16 |
| `#B3B3B3 (stroke)` | 15 |
| `#F5F1E9 (stroke)` | 14 |
| `#9B9A97` | 14 |
| `#1B1C1E (stroke)` | 12 |
| `#172B85` | 12 |
| `#BFBFBF` | 11 |
| `#EE6A5F` | 11 |
| `#CE5347 (stroke)` | 11 |
| `#F5BD4F` | 11 |
| `#D6A243 (stroke)` | 11 |
| `#61C454` | 11 |
| `#58A942 (stroke)` | 11 |
| `#000000 @0.05` | 11 |
| `#9E9E9E` | 11 |
| `#4C4C4C` | 11 |
| `#797979` | 11 |
| `#F3F3F3` | 10 |
| `#FF2D55` | 9 |
| `#DADADA` | 8 |
| `#E6E6E6 (stroke)` | 6 |
| `#0374A5` | 6 |
| `#253B80` | 6 |
| `#CBF390 (stroke)` | 5 |
| `#000000 @0.5` | 5 |
| `#E6E6E6` | 5 |
| `#D2D2D2 (stroke)` | 4 |
| `#667085` | 4 |
| `#000000 @0.4` | 4 |
| `#0374A5 (stroke)` | 4 |
| `#F9A000` | 4 |
| `#179BD7` | 4 |
| `#F6FEEC` | 2 |
| `#D0D5DD (stroke)` | 2 |
| `#F3F3F3 (stroke)` | 2 |
| `#ED0006` | 2 |
| `#6D6DBB` | 2 |
| `#FF5E00` | 2 |
| `#1F72CD` | 2 |
| `#222D65` | 2 |
| `#F2F4F7 (stroke)` | 1 |
| `#F9FAFB` | 1 |

## 圆角（60 种）

| radius | 出现 |
|---|---|
| 8.0 | 279 |
| (0.0, 0.0, 0.0, 0.0) | 234 |
| 0.8 | 209 |
| 0.9 | 185 |
| 72.0 | 176 |
| 1.8 | 129 |
| 16.0 | 117 |
| 6.7 | 101 |
| 1.0 | 94 |
| 4.0 | 86 |
| 4.7 | 54 |
| (1.7, 1.7, 0.0, 0.0) | 54 |
| 100.0 | 39 |
| 6.5 | 30 |
| 10.0 | 28 |
| (1.5, 1.5, 0.0, 0.0) | 25 |
| 21.3 | 20 |
| 10.7 | 20 |
| 1.3 | 20 |
| 0.4 | 20 |
| 2.6 | 19 |
| 44.0 | 18 |
| 40.0 | 18 |
| 24.0 | 16 |
| 0.3 | 15 |
| 10000.0 | 12 |
| 1.9 | 11 |
| 3.1 | 11 |
| 60.0 | 9 |
| 7.8 | 8 |
| 50.0 | 8 |
| 27.8 | 7 |
| (8.0, 8.0, 0.0, 0.0) | 6 |
| (16.0, 16.0, 8.0, 8.0) | 6 |
| 1.5 | 6 |
| (14.3, 14.3, 0.0, 0.0) | 5 |
| (0.6, 0.6, 0.0, 0.0) | 5 |
| 8.3 | 5 |
| 4.1 | 5 |
| 0.7 | 5 |
| 23.8 | 4 |
| 27.3 | 4 |
| (16.0, 16.0, 0.0, 0.0) | 4 |
| 9.3 | 4 |
| 6.2 | 4 |
| (6.2, 6.2, 3.1, 3.1) | 3 |
| 32.0 | 2 |
| 15.7 | 2 |
| 26.0 | 2 |
| 6.0 | 2 |
| 3.4 | 2 |
| 3.9 | 2 |
| 19.3 | 2 |
| 8.9 | 2 |
| 45.7 | 2 |
| 15.5 | 1 |
| (5.5, 5.5, 0.0, 0.0) | 1 |
| 3867.0 | 1 |
| (0.0, 0.0, 32.0, 32.0) | 1 |
| 4.6 | 1 |

## 阴影（19 种）

| effect | 出现 |
|---|---|
| `DROP_SHADOW 0.0,1.3 blur 12.9 spread 0 #000000 @0.08` | 17 |
| `DROP_SHADOW 0.0,1.0 blur 2.0 spread 0 #101828 @0.05` | 14 |
| `DROP_SHADOW 0.0,1.5 blur 15.0 spread 0 #000000 @0.25` | 12 |
| `DROP_SHADOW 0.0,0.6 blur 0.0 spread 0 #000000 @0.15` | 10 |
| `INNER_SHADOW 0.0,-0.6 blur 0.0 spread 0 #000000 @0.05` | 10 |
| `INNER_SHADOW 0.0,0.0 blur 6.7 spread 0 #EC6D62` | 10 |
| `INNER_SHADOW 0.0,0.0 blur 6.7 spread 0 #F5C451` | 10 |
| `INNER_SHADOW 0.0,0.0 blur 6.7 spread 0 #68CC58` | 10 |
| `DROP_SHADOW 0.0,-4.0 blur 28.0 spread 0 #333131 @0.05` | 5 |
| `DROP_SHADOW 0.0,-4.0 blur 10.0 spread 0 #333131 @0.01` | 5 |
| `DROP_SHADOW 0.0,4.0 blur 6.0 spread -2.0 #101828 @0.03` | 1 |
| `DROP_SHADOW 0.0,12.0 blur 16.0 spread -4.0 #101828 @0.08` | 1 |
| `DROP_SHADOW 0.0,0.5 blur 5.0 spread 0 #000000 @0.08` | 1 |
| `DROP_SHADOW 0.0,0.4 blur 0.8 spread 0 #101828 @0.05` | 1 |
| `DROP_SHADOW 0.0,0.2 blur 0.0 spread 0 #000000 @0.15` | 1 |
| `INNER_SHADOW 0.0,-0.2 blur 0.0 spread 0 #000000 @0.05` | 1 |
| `INNER_SHADOW 0.0,0.0 blur 2.6 spread 0 #EC6D62` | 1 |
| `INNER_SHADOW 0.0,0.0 blur 2.6 spread 0 #F5C451` | 1 |
| `INNER_SHADOW 0.0,0.0 blur 2.6 spread 0 #68CC58` | 1 |

## ⚠ 含 characterStyleOverrides 的 frame（33 个）

这些 frame 里有 TEXT 节点做了字符级样式覆盖（同一段文字里某些字换了字体/颜色/字号）。
实现时必须逐字符查 `characterStyleOverrides` + `styleOverrideTable`，不能只取 TEXT 的顶层 style。

- `228-5932_homepage-mobile`
- `285-18162_homepage-desktop`
- `285-18988_pop-up`
- `285-19179_pop-up`
- `285-19373_homepage-desktop`
- `324-52658_product-page-desktop`
- `324-53792_pdp-mobile`
- `324-56865_science-desktop`
- `324-58044_science-moble`
- `324-63924_reviews-desktop`
- `324-64961_reviews`
- `324-69636_how-gumi-works-desktop`
- `324-70523_how-gumi-works`
- `324-72839_our-story-desktop`
- `324-73673_our-story`
- `324-75766_our-story-desktop`
- `324-76169_faq`
- `326-79979_our-story-desktop`
- `326-80318_get-in-touch`
- `326-81218_our-story-desktop`
- `326-81540_referral`
- `326-82363_our-story-desktop`
- `326-83129_shipping`
- `326-83399_privacy-policy`
- `336-28414_nutritional-label-pop-up`
- `336-29511_nutritional-label-pop-up`
- `336-31949_nutritional-label-pop-up`
- `336-32296_nutritional-label-pop-up`
- `401-29604_homepage-desktop`
- `402-31998_handover-notes-for-dev`
- `notes-batch-1`
- `notes-batch-2`
- `notes-batch-3`

## 逐页文案

见 `docs/copy/`，共 71 份：

| 文件 | frame | 节点 | 条数 |
|---|---|---|---|
| [324-52658_Product-Page-Desktop.md](copy/324-52658_Product-Page-Desktop.md) | Product Page Desktop | `324:52658` | 220 |
| [324-53792_PDP-Mobile.md](copy/324-53792_PDP-Mobile.md) | PDP Mobile | `324:53792` | 215 |
| [324-63924_Reviews-Desktop.md](copy/324-63924_Reviews-Desktop.md) | Reviews Desktop | `324:63924` | 215 |
| [324-64961_Reviews.md](copy/324-64961_Reviews.md) | Reviews | `324:64961` | 194 |
| [285-18162_Homepage-Desktop.md](copy/285-18162_Homepage-Desktop.md) | Homepage Desktop | `285:18162` | 188 |
| [401-29604_Homepage-Desktop.md](copy/401-29604_Homepage-Desktop.md) | Homepage Desktop | `401:29604` | 188 |
| [228-5932_Homepage-Mobile.md](copy/228-5932_Homepage-Mobile.md) | Homepage Mobile | `228:5932` | 177 |
| [324-69636_How-Gumi-Works-Desktop.md](copy/324-69636_How-Gumi-Works-Desktop.md) | How Gumi Works Desktop | `324:69636` | 155 |
| [336-29511_Nutritional-Label-Pop-up.md](copy/336-29511_Nutritional-Label-Pop-up.md) | Nutritional Label Pop up | `336:29511` | 152 |
| [336-32296_Nutritional-Label-Pop-up.md](copy/336-32296_Nutritional-Label-Pop-up.md) | Nutritional Label Pop up | `336:32296` | 152 |
| [324-72839_Our-Story-Desktop.md](copy/324-72839_Our-Story-Desktop.md) | Our Story Desktop | `324:72839` | 144 |
| [324-70523_How-Gumi-Works.md](copy/324-70523_How-Gumi-Works.md) | How Gumi Works | `324:70523` | 142 |
| [324-73673_Our-Story.md](copy/324-73673_Our-Story.md) | Our Story | `324:73673` | 135 |
| [324-56865_Science-Desktop.md](copy/324-56865_Science-Desktop.md) | Science Desktop | `324:56865` | 125 |
| [324-58044_Science-Moble.md](copy/324-58044_Science-Moble.md) | Science Moble | `324:58044` | 116 |
| [336-28414_Nutritional-Label-Pop-up.md](copy/336-28414_Nutritional-Label-Pop-up.md) | Nutritional Label Pop up | `336:28414` | 96 |
| [336-31949_Nutritional-Label-Pop-up.md](copy/336-31949_Nutritional-Label-Pop-up.md) | Nutritional Label Pop up | `336:31949` | 96 |
| [336-34120_Desktop-Nutritional-Label-Pop-up.md](copy/336-34120_Desktop-Nutritional-Label-Pop-up.md) | Desktop Nutritional Label Pop up | `336:34120` | 87 |
| [326-83129_Shipping.md](copy/326-83129_Shipping.md) | Shipping | `326:83129` | 85 |
| [326-79979_Our-Story-Desktop.md](copy/326-79979_Our-Story-Desktop.md) | Our Story Desktop | `326:79979` | 81 |
| [324-75766_Our-Story-Desktop.md](copy/324-75766_Our-Story-Desktop.md) | Our Story Desktop | `324:75766` | 80 |
| [326-81218_Our-Story-Desktop.md](copy/326-81218_Our-Story-Desktop.md) | Our Story Desktop | `326:81218` | 78 |
| [326-82363_Our-Story-Desktop.md](copy/326-82363_Our-Story-Desktop.md) | Our Story Desktop | `326:82363` | 78 |
| [324-76169_FAQ.md](copy/324-76169_FAQ.md) | FAQ | `324:76169` | 68 |
| [326-80318_Get-in-Touch.md](copy/326-80318_Get-in-Touch.md) | Get in Touch | `326:80318` | 66 |
| [326-81540_Referral.md](copy/326-81540_Referral.md) | Referral | `326:81540` | 63 |
| [326-83399_Privacy-Policy.md](copy/326-83399_Privacy-Policy.md) | Privacy Policy | `326:83399` | 62 |
| [285-18988_Pop-up.md](copy/285-18988_Pop-up.md) | Pop up | `285:18988` | 58 |
| [285-19179_Pop-up.md](copy/285-19179_Pop-up.md) | Pop up | `285:19179` | 57 |
| [341-42573_Desktop-Cart.md](copy/341-42573_Desktop-Cart.md) | Desktop Cart | `341:42573` | 40 |
| [336-36516_Mobile-Cart.md](copy/336-36516_Mobile-Cart.md) | Mobile Cart  | `336:36516` | 37 |
| [336-31534_Desktop-Nutritional-Label-Pop-up.md](copy/336-31534_Desktop-Nutritional-Label-Pop-up.md) | Desktop Nutritional Label Pop up | `336:31534` | 31 |
| [283-14915_Nav-Expanded.md](copy/283-14915_Nav-Expanded.md) | Nav Expanded | `283:14915` | 19 |
| [283-15014_Nav-Collapsed.md](copy/283-15014_Nav-Collapsed.md) | Nav Collapsed | `283:15014` | 19 |
| [401-31721_Header-Navigation-Desktop-Open.md](copy/401-31721_Header-Navigation-Desktop-Open.md) | Header Navigation Desktop/Open | `401:31721` | 9 |
| [336-34942_Mobile-Cart---Empty.md](copy/336-34942_Mobile-Cart---Empty.md) | Mobile Cart - Empty | `336:34942` | 8 |
| [341-42749_Desktop-Cart-Empty.md](copy/341-42749_Desktop-Cart-Empty.md) | Desktop Cart Empty | `341:42749` | 7 |
| [401-31720_Header-Navigation-Desktop-Closed.md](copy/401-31720_Header-Navigation-Desktop-Closed.md) | Header Navigation Desktop/Closed | `401:31720` | 6 |
| [196-18017_Input-Drop-Down.md](copy/196-18017_Input-Drop-Down.md) | Input Drop Down | `196:18017` | 5 |
| [285-19373_Homepage-Desktop.md](copy/285-19373_Homepage-Desktop.md) | Homepage Desktop | `285:19373` | 5 |
| [402-31998_Handover-Notes-For-Dev.md](copy/402-31998_Handover-Notes-For-Dev.md) | Handover Notes For Dev: | `402:31998` | 2 |
| [216-5903_note.md](copy/216-5903_note.md) | note | `216:5903` | 1 |
| [401-29596_note.md](copy/401-29596_note.md) | note | `401:29596` | 1 |
| [401-31213_note.md](copy/401-31213_note.md) | note | `401:31213` | 1 |
| [401-31444_note.md](copy/401-31444_note.md) | note | `401:31444` | 1 |
| [401-31215_note.md](copy/401-31215_note.md) | note | `401:31215` | 1 |
| [401-31217_note.md](copy/401-31217_note.md) | note | `401:31217` | 1 |
| [401-29598_note.md](copy/401-29598_note.md) | note | `401:29598` | 1 |
| [324-55034_note.md](copy/324-55034_note.md) | note | `324:55034` | 1 |
| [324-61872_note.md](copy/324-61872_note.md) | note | `324:61872` | 1 |
| [401-31482_note.md](copy/401-31482_note.md) | note | `401:31482` | 1 |
| [401-31996_note.md](copy/401-31996_note.md) | note | `401:31996` | 1 |
| [401-31994_note.md](copy/401-31994_note.md) | note | `401:31994` | 1 |
| [326-84892_note.md](copy/326-84892_note.md) | note | `326:84892` | 1 |
| [324-67971_note.md](copy/324-67971_note.md) | note | `324:67971` | 1 |
| [324-71473_note.md](copy/324-71473_note.md) | note | `324:71473` | 1 |
| [324-74462_note.md](copy/324-74462_note.md) | note | `324:74462` | 1 |
| [326-79393_note.md](copy/326-79393_note.md) | note | `326:79393` | 1 |
| [326-80721_note.md](copy/326-80721_note.md) | note | `326:80721` | 1 |
| [401-31715_note.md](copy/401-31715_note.md) | note | `401:31715` | 1 |
| [326-81918_note.md](copy/326-81918_note.md) | note | `326:81918` | 1 |
| [401-31219_note.md](copy/401-31219_note.md) | note | `401:31219` | 1 |
| [401-31225_note.md](copy/401-31225_note.md) | note | `401:31225` | 1 |
| [401-31227_note.md](copy/401-31227_note.md) | note | `401:31227` | 1 |
| [401-31229_note.md](copy/401-31229_note.md) | note | `401:31229` | 1 |
| [401-31717_note.md](copy/401-31717_note.md) | note | `401:31717` | 1 |
| [401-31223_note.md](copy/401-31223_note.md) | note | `401:31223` | 1 |
| [401-31440_note.md](copy/401-31440_note.md) | note | `401:31440` | 1 |
| [401-31442_note.md](copy/401-31442_note.md) | note | `401:31442` | 1 |
| [401-29602_note.md](copy/401-29602_note.md) | note | `401:29602` | 1 |
| [401-31452_note.md](copy/401-31452_note.md) | note | `401:31452` | 1 |

# 交接：第三十九 / 四十轮（手机菜单改版 + 1280 以下响应式）

> 状态：`$build` = **`20260827-r41`**，全部改动**已编译、已验证、未推送**。
> 起点读这份，细节在 [CHANGELOG.md](../CHANGELOG.md) 第三十八～四十轮，
> 待决事项在 [PROJECT-STATUS.md](../PROJECT-STATUS.md)。
> 上一份交接（第三十六/三十七轮的对稿方法）仍然有效：[R37-HANDOFF.md](R37-HANDOFF.md)。

## 一、这三轮做了什么

| 轮次 | build | 主题 | 入口 |
|---|---|---|---|
| 三十八 | r39 | 任务文档 8 项（响应式为主）+ 全站条件换行粘连 | CHANGELOG 第三十八轮 |
| 三十九 | r40 | 任务文档 5 项：手机菜单照 funkyfood 重做 + PDP 手机值 | CHANGELOG 第三十九轮 |
| 四十 | r41 | 任务文档第二组 3 项：1280 以下的响应式 | CHANGELOG 第四十轮 |

需求来源都是项目根目录的 `修改任务文档.txt`。⚠ **那个文件会被就地覆写**，
接手第一件事是 `md5sum` 一下，跟 CHANGELOG 里记的条数核对，确认拿到的是哪一版。

三轮里挖出来的**既有 bug**（不是需求，是顺带发现并修掉的）：

1. **手机端三个 logo 互相压住 23.95px**（r39）—— 槽早已收成 106×44，图片仍按各自墨迹高度
2. **全站 11 页 24 处条件换行粘连**（r39）—— `word<br class="gb-br-narrow">word`，768 以上 br 隐藏后两词贴死
3. **promo 卡的扇贝一直被 reset 压小 30%**（r40）—— `svg { max-width: 100% }` 把 492px 和 143% 都截回卡片宽
4. **`.gb-page-hero__media` 在 1024 处只剩 119.8×90.3**（r41）—— 图片基本消失

## 二、不要报成 bug 的清单 ⚠

下面全是**有意为之**的，下一轮审计/对稿看到不要当回归修掉。

### 设计决策类

- **手机菜单的两个折叠组默认是收起的**。稿（`283:14915`）画的是 Learn more / Get in Touch
  **都展开**的展示态，实现是可点开的手风琴。收起时面板底部会空一段，与稿的"刚好填满"不同。
- **`.gb-header__panel-bar` 的 `padding: 12px 0` 是反推值**，不是板上的直读数。板把 64 全给了
  顶栏，而需求方把 `padding-top: 9` 给了 `panel-inner`。9 + 12 + 24 + 12 = 57 ≠ 64，
  差的 7 落在卡片上方的 gap 里（板 8，需求方给 15）。**结果 nav 卡片起点仍是板的 72**，
  所以没有再往回调。
- **`.gb-promo-card__list` 的 `margin-right: 15px` 效果是靠右，不是"居中后左移 15"**。
  base 是 `margin: 0 auto`，右边一固定，左边的 auto 就吃掉全部余量（实测 390 下左 24.39 / 右 15）。
  按需求方给的字面落的，已列为待决 I。
- **`.gb-compare__heading` / `__panel` 堆叠后跑满版心**（991 处 898.8 宽），比原来的 560 上限松。
  需求方点名要去掉那个 `max-width`，是有意的。
- **两个正方形图块（`.gb-ingredients__disc` / `.gb-faq-image__media`）堆叠时仍有 `max-width: 520px`**。
  需求方说的"不应该固定宽"指的是 row 里那个不可压缩的 `flex: 0 0 520px`（它会饿死另一栏），
  **不是堆叠后的上限** —— 去掉上限它们会撑成 898×898 的巨图。
- **`.gb-deco-bear--b` 的 `top` 仍是 px，只有 `right` 改成了百分比**（r39）。top 解析的是
  CTA 文案块的高度，不是设计常量：文案多一行、或换上比试用宽 4.7% 的授权 PP Palma，
  百分比定位的熊会跟着下滑。
- **`.gb-vs__value` 等 13 个 PDP 手机值**（r40）没有板上出处，是需求方对着截图给的，已照落。
- **reviews.html 还留着一个 `.gb-app-slot`**，pdp 的那个删了。需求那条整段都是 PDP 的选择器，
  而 reviews 页那个 slot 是整页主体（评论 app 挂载点）。待决 H。

### 探针假信号类（这些是工具的毛病，不是页面的）

- **`hardbreaks.py` 恒定 6 条 MISSING** —— 是图片里的文字，误报，三轮同数。
- **`font-check.html` 有两条断言恒假**：「波浪归属：section 自带下边缘形状」与
  「裁切型宿主也不用特例」。第十九轮把占位方案从 `::after` 换成了
  `padding-bottom: calc(… + var(--sc-h))`，`::after` 的 `content` 现在读回 `none`。
  **从第十九轮起就一直红**，不是这三轮引入的。待决 G。
- **截图脚本的 SETTLE 只写 `.wowo` 会切掉半截标题**。必须带上 reveal 那一组：
  ```
  .wowo,.gb-float-art,[data-line-reveal],.gb-line-mask__inner,.gb-ink-halo{
    opacity:1!important;transform:none!important;animation:none!important}
  ```
  漏了它，行遮罩停在第 0 帧，看起来像页面溢出。`r41check.py` 里已经是全的，
  自己新写脚本时别抄旧的短版本。见 memory `kill-animations-blanks-reveal-blocks`。
- **borders 的 computed 值会被取整**：390 档 `border-bottom-width: 0.48px` 读回 `1px`，
  `1.43px` 也读回 `1px`。DPR=1 下的既有行为，不是没生效。

## 三、这三轮踩到的坑（新写代码前看一眼）

**1. `column-reverse` 下 `flex-basis` 是高度。**
把两栏改成可伸缩 basis（`flex: 1 1 566px`）时，容器在窄档转了 `column-reverse`，
566 被当成**最小高度**，hero 凭空高了约 390px。给那一档补 `flex: none`。
症状在快照里很好认：**大量元素只有 y 变、x/w/h 全不变**。
memory: `flex-basis-is-height-in-column-direction`。

**2. 活性自检要破坏"真正负责的那条规则"。**
验「落单卡片居中」时破坏了 `> * { grid-column: span 2 }`，**只有 768 报红** ——
因为 `:last-child:nth-child(odd)` 那条独立生效，居中照样成立。
**判据：报红的档位数应当与断言覆盖的档位数相符**，只红一部分就是破坏点选错了。
memory: `negative-assert-needs-liveness-guard` 第五种。

**3. 改堆叠阈值时，同组配套规则必须一起搬。**
r41 把三个模块的 `flex-direction: column` 从 `stack`(1024) 移到 `mid`(991)，
`__heading` / `__panel` / `__body` / `__disc` / `__media` 六条 `@include stack` 全部要跟到 `mid`，
否则 992–1024 会拿堆叠态的规则去排一个 row。`padding-inline` 留在 `tight` 没动 ——
版心内距和堆叠是两件事。

**4. `fluid()` 只能用于 px。**
r40 一度写了 `top: fluid(-8%, -5%)`，百分比不能用 `calc()` 随视口插值。
那一档直接不做斜坡。memory: `percent-cannot-ramp-with-calc`。

**5. Figma 的 `line-height: 100%` 是 auto，不是字号的 100%。**
成分表节点自报 `12.0163px`（PP Palma 自然行距 1.26），写 9.54 会挤成一团。
`leading-trim: CAP_HEIGHT` CSS 没有等价物，它只解释了为什么稿里单行 box 高 7 而非 12.02。

**6. 等比缩放的例外要查，不能默认。**
成分表整表按 0.741529 缩放（字号 + 三条线宽四处独立印证），**唯独两个数值列不行** ——
手机稿的行 Frame 是 427.72 宽装在 350 容器里，SPACE_BETWEEN 在超宽盒子里排。

## 四、验证怎么跑

```bash
cd /home/ly/project/Gumi-Brand

# 编译（源在 assets/customstyle.scss，产物 customstyle.css）
npx sass@1.77.8 assets/customstyle.scss assets/customstyle.css --no-source-map

# 逐轮定向断言（全部应通过）
for s in r31check r32check r36check r39check r40check r41check; do
  python3 tools/$s.py; done

# 全站响应式（12 页 × 14 档，无横向溢出/文字被裁）
python3 tools/rwd.py

# 入场动效收尾 / 硬换行
python3 tools/revealcheck.py
python3 tools/hardbreaks.py        # 恒定 34 ok / 6 MISSING

# 全站 computed-style 快照（改结构时唯一有效的判据）
python3 tools/cssnap.py <tag> --widths 1440
python3 tools/cssnap.py diff r41 <tag>
```

**快照基线**（`tools/snap/`，共约 800M，磁盘余量 7.7G）：

| 目录 | 内容 | 用途 |
|---|---|---|
| `r38` | 全档（547M） | 两轮前，**可清** |
| `r39` / `r40` / `r41` | 仅 1440 | 桌面不变量基线 |
| `r40m` / `r41m` | 仅 390 | 手机不变量基线 |

下一轮的判据取 **`r41`（1440）与 `r41m`（390）** 作基线。两个都是设计稿宽度，
**出现 `#rect` 变化就是回归，必须查清**；纯声明变化（flex-grow / min-width 之类）无妨。

⚠ 服务器是多用户共享的，内存经常只剩 2–3G（别人的进程占着 25G，`pgrep chrome` 能看到
99 个都不是 `ly` 的）。playwright 脚本被 OOM kill（exit 137）时重跑即可，**不要去杀别人的进程**。

## 五、待决事项索引（全部在 PROJECT-STATUS.md）

| | 事项 | 轮次 |
|---|---|---|
| A–D | 桌面/手机稿冲突、稿自身 WIP 痕迹、两端同源不敢动的 | 三十七 |
| E | footer 链接区结构分歧（+116 高） | 三十八 |
| F | `.gb-footer` padding-bottom 24 vs 板的 48 | 三十八 |
| G | font-check 两条断言从第十九轮起恒假 | 三十九 |
| H | reviews.html 还留着一个 `.gb-app-slot` | 三十九 |
| I | `.gb-promo-card__list` 的 margin 语义 | 三十九 |
| **J** | **堆叠阈值 991 与第二十九轮的「推到 1200」方向相反** | 四十 |

**J 最需要先问清楚** —— 两条不能同时成立。当前按 991 落地（更晚堆叠），
若 1200 那条仍作数，把三处 `@include mid` 换成 `tight` 即可，同组六条配套规则一起换。

## 六、常驻遗留（跨轮次，不属于任何一轮）

- **768–1280 这一档始终没有设计稿**。所有值要么是 390→1281 的 `fluid()` 斜坡，
  要么是行为约束（比例、不塌陷），**没有一个是板值**。
- **小波浪手机端仍高 12px**（`--sc-band` clamp 下界，第三十五轮起）。已经有四处 padding
  靠它换算（CTA 52、footer 52、`.gb-vs` 52、`.gb-faq` 52），波浪修好后这些要回到板的 64。
- **PP Palma 300（FizzyLight）仍是试用包**，EULA 排除商业用途、不随仓库分发。
  400 是本地插值生成的。
- **上线前必须替换的占位内容**：Reviews 专家卡的竞品名 Grüns、Shipping 全页美国配送文案、
  Privacy 的 lorem ipsum。详见 PROJECT-STATUS「交付前必须替换的占位内容」。
- **Shopify 主题化尚未开始**，当前是 11 页静态站。

## 七、下一步

按优先级：

1. **问清待决 J**（堆叠阈值方向），它会影响三个模块六条规则
2. 待决 G / H / I 也是一句话就能定的，一起问
3. 需求方给新一版 `修改任务文档.txt` → 照老流程：先 `md5sum` 核对版本，
   再 `grep` CHANGELOG 查同模块历史（多数需求是既往条目的延续），再动手
4. 推送要等明确指令，且共用环境**绝不全量、绝不 `--delete`**

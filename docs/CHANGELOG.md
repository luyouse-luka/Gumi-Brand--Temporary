# Gumi Brand — 前端改动记录

> 每约 10 项记一条。只写「改了什么 / 为什么 / 文件清单 / 遗留」。
> 推导过程、探针数据、失败尝试留在对话里。

> ⚠ **第一～三十轮已分卷到 [CHANGELOG-ARCHIVE.md](CHANGELOG-ARCHIVE.md)**（2026-08-27，原文未改）。
> **查历史两份一起 grep**：`grep -n <关键词> docs/CHANGELOG*.md`。

<details><summary>归档卷的轮次索引（第一～三十轮）</summary>

- 2026-08-19 第一轮：基建 + header/footer + hero + logo scroll
- 2026-08-19 第二轮：Homepage 全部 section 完成
- 第三轮 — 特殊动效 + 营养标签弹窗（2026-08-19）
- 第四轮 — 手机端字号校正 + PDP 整页（2026-08-20）
- 第五轮 — 全站交互态：hover + 过渡（2026-08-20）
- 第六轮 — 客户验收反馈 10 项（2026-08-20）
- 第七轮 — 字体解析 + 入场效果重排（2026-08-20）
- 第八轮 — 字距 / 波浪几何 / hover / 手风琴（2026-08-20）
- 第九轮 — 缓存版本号 + 构建自检（2026-08-20）
- 第十轮 — 任务文档 8 项（2026-08-20）
- 第十一轮 — 任务文档 3 项（2026-08-20）
- 第十二轮 — 内页开工：Science / Reviews / How Gumi Works（2026-08-20）
- 第十三轮 — 内页收尾：Our Story / FAQ / Get in Touch / Referral / Privacy / Shipping（2026-08-20）
- 第十四轮 — 四线审计的上线阻断级修复（2026-08-21）
- 第十五轮 — assets 目录扁平化 + SCSS 合并为 customstyle.scss（2026-08-21）
- 第十八轮 — 波浪真正搬进所属 section（2026-08-21）
- 第十七轮 — 任务文档 3 项：平滑滚动 / 波浪归属 + band 透底 / 去放大（2026-08-21）
- 第十六轮 — 任务文档 9 项：断点改制 + band 还原 + 全站 gb- 前缀（2026-08-21）
- 第十九轮 — 任务文档 7 项：手风琴死区 / header 吸顶 / 弧被裁（2026-08-24）
- 第二十轮 — 对话给的 8 条：hero 光晕重建 / 弧度还原 / 箭头旋转 / 补回缺失的波浪（2026-08-24）
- 第二十一轮 — 对话给的 PC 端 15 项数值 + footer-cta 弧度还原（2026-08-24）
- 第二十二轮 — 对话追加的 7 项（stats 熊浮动范围 / 间距修正）（2026-08-24）
- 第二十三轮 — 撤掉 gb-sec-edge 机制 + 补 stats 波浪右侧小熊（2026-08-24）
- 第二十四轮 — 弹窗滚动锁定的横向抖动 + nutritional-label 数值修正（2026-08-24）
- 第二十五轮 — 小熊浮动范围恢复 + 补全「正文文字上滑」效果（2026-08-25）
- 第二十六轮 — PP Palma 400/500/800 换上客户授权文件（2026-08-25）
- 第二十七轮 — 补上一直没做的首单折扣弹窗（2026-08-25）
- 2026-08-25 第二十八轮：弹窗改淡入淡出 + 字体 layout shift + 标题入场 + 一批间距（`$build` = `20260825-r29`）
- 2026-08-25 第二十九轮：断点体系改制（`$build` = `20260825-r30`）
- 2026-08-25 第三十轮：任务文档两批共 24 项（`$build` = `20260825-r31`）

</details>

## 2026-08-26 第三十一轮：promo-modal 按稿重做 + 小熊改整体导出（`$build` = `20260825-r32`）

反馈「`gb-promo-modal` 的样式没有还原设计包括内部的元素，小熊图片的导出也错误，
需要整体导出一张图」。逐节点比对 336:27146（桌面）/ 285:19012（手机 email 态）/
285:19204（手机 code 态）后确认两件事都成立，本轮全部做掉。

### 改了什么

**小熊：四张拼图 → 一张整体导出**

1. **旧实现是把「旋转后的外接盒」当画框、图正着放**，所以两只熊都不倾斜、
   两团光晕跟熊完全分家飘在旁边。Figma 里这两组各自带变换：
   | 节点 | 变换 | 旧实现取的值 |
   |---|---|---|
   | Group 38585（大熊组） | 旋转 7.163° | 只取了组内两个子节点的 bbox |
   | └ Gumi Bear Side 1 | det = −1，**镜像**+旋转 | 457.76×385.51（旋转后外接盒） |
   | └ Vector（光晕） | 水平镜像 | 282.09×340.93（同上） |
   | Group 38584（小熊组） | 无旋转 | — |
   | └ Gumi Bear Side 1 | 旋转 18.484° | 369.74×325.16（旋转后外接盒） |
   同一个坑第二十轮的四支箭头踩过一次（见 CHANGELOG 第二十轮）。
2. **改成一张 `images/promo-bears.png` / `.webp`**，画框 = 两个组的**并集 bbox**
   624.54×481.17（Image frame 自己的坐标系）。桌面按 `left:-86.84 top:13` 原尺寸摆，
   手机是**同一个框 ×0.61618**——这个比例不是我定的，是稿子自己的：两组的尺寸比
   （327.58/531.64）与两组之间的位移比（157/254.8）都是 0.6162，所以一张图两端通用。
3. **图是本地复现的，不是 Figma 渲染端点导出的** —— `/v1/images` 在第一次请求后
   就 429 了（账号级，`retry-after` 241986s ≈ 2.8 天）。改走 memory 里记的那条路：
   `/v1/files/:key/images` 拿 image fill 原图（不受渲染端点限流）+ 节点的
   `fillGeometry` / `strokeGeometry` 路径，拼成 SVG 用 Chromium 渲染成透明 PNG。
   光晕的 OUTSIDE 描边直接画 `strokeGeometry`（与 fill 同色），SVG 的 stroke 是
   center 对齐、表达不了 OUTSIDE。
   ⚠ **判据是限流前抢到的那一张**：桌面 Image frame（336:27147）的官方导出图还在手上，
   把本地渲染结果按同样坐标合成到 cream 底上逐像素比 ——
   光晕纯色掩膜的 bbox **逐位相同**（x[75.5,441.0] y[97.5,443.5]）、质心差 0.06px、
   IoU 0.978，残差全在抗锯齿边缘（>64 的像素占 0.02%）。
4. 手机版的水平锚点写成 `left: calc(50% - 212px)` 而不是稿里的 `-17px` ——
   在 390 上两者等价，但这套堆叠布局一直用到 1280，锚左边缘会让两只熊在平板上
   全堆到屏幕最左侧。改成锚中心后偏移量恒为稿里的 −19.6。

**弹窗内部：逐节点对齐**

5. **`__head` 56 → 64**。稿里这一行的高度由 32 的关闭按钮 + 16 padding 决定，
   而 logo 是 `layoutPositioning: ABSOLUTE`（居中，y 20），根本不参与撑高。
   旧实现拿 logo 的 24 去撑，整行矮 8px，下面所有东西跟着上移。
6. **补上 head 与正文之间的 64 gap**（336:27155 / 285:19013 都是 `VERTICAL gap=64`）。
   旧实现没有这个 gap，靠桌面 `justify-content:center` 把正文推回大致位置，
   手机则直接紧贴。加上之后桌面 `body` 正好是稿里的 400（528 − 64 − 64），
   内部 96+32+56+32+152+32 = 400 一格不差；手机正好 332。
7. **手机 `__body` 去掉 `padding-bottom: 40`** —— 285:19021 的 padding 只有左右 40，
   底部那 40 是多加的，把正文块顶高了。
8. **`__lead` 去掉 `margin-top: -8px`**：稿里 title→lead 就是 body 自己的 gap 32，
   那个负 margin 把它压成了 24。
9. **补上 form 与「No thanks」之间的 20px**（Frame 427319585 的 `gap=20`）。
   旧标记里这两个是同一个无样式 `div` 的兄弟，中间没有任何间距，而 `__stage`
   身上的 gap:20 落在了两个互斥（`hidden`）的状态容器之间，等于空转。
   新增 `.gb-promo-panel__state` 承接这个 20。
   ⚠ 它必须自己写 `&[hidden]{display:none}` —— `[hidden]` 是 UA 的 display:none，
   作者写的任何 display 都压得过它（见 memory `hidden-attr-vs-author-display`）。
10. **删掉输入框里的信封图标**：336:27169 与 285:19028 的 `icon` / `mail` / `Help icon`
    三个实例 `visible` 全是 **false**，稿上根本没有图标（Content 宽 375 = 403−28，
    正好只有左右各 14 的 padding）。截图上也看得出来，是当初照着组件默认态补的。
11. **`__input` 补自己的 reset**：全局那条只管 `font/color/margin`，所以浏览器默认的
    边框和白底一直露在 `__field` 里面，看起来像框里又套了一个框。

### 判据

- **`tools/r32check.py`（新）42 条断言全过**：桌面 email + 手机 email + 手机 code
  三张稿逐元素比 x/y/w/h（容差 1px），另含 logo 居中、图标数为 0、input 无边框无底色、
  art 区只有一张 `promo-bears.*`、分隔线只在 ≥1281 出现。
  ⚠ **判据本身做过破坏性自检**：把 head 改回 56、把熊的锚点挪 38px，22 条断言变红；
  还原后全绿。第一次自检时替换字符串没匹配上编译产物的格式（expanded 不是压缩），
  破坏根本没注入却报了全绿 —— 锚点断言是后补的。
- **`tools/r32diff.py`（新）把 390 的实现叠在自己的稿子上逐行比**（email 比 285:18988、
  code 比 285:19179，两张 390×840 导出裁掉顶部 96 的假浏览器栏）。结构断言与它不能互相顶替 ——
  第二十七轮那只跑到面板另一头的手机小熊，当时所有结构断言都是绿的。
  结果：**除标题/副标各自的第一行外，每一行的墨迹左右边缘都是 0 偏差**
  （title l2 x[52,335]、lead l2 x[87,302] 逐位相同），全panel 平均差 4.95（抗锯齿量级）。
  ⚠ **写这个脚本时踩了两个探针坑，都写进它的文件头了**：
  ① `.click()` 之后指针停在按钮上，而 code 态的 Copy 按钮正好继承同一个位置 →
  整颗药丸拍成了 lime 的 hover 态（那一带平均差 141）；
  ② 弹窗切态时会把焦点移进新状态，键盘/脚本提交会画出一圈 `:focus-visible` 轮廓，
  稿上没有。实测：鼠标点击 `fv=false` 无环、键盘 Enter `fv=true` 有环 —— 后者是对的
  无障碍行为，不是 bug。改成鼠标提交 + 移开指针 + blur 后，那两带的差异全部消失。
- **标题第一行比稿子偏右 5px、副标第一行偏右 2px，是稿子的问题不是实现的**：
  两处 TEXT 的换行前都多了一个空格（`'Get 20% off '` / `'Enter your email address below '`，
  U+2028 之前）。Figma 居中时把它算进行宽、把可见文字往左推，CSS 则会折叠行尾空格。
  36px 的空格半宽正好 5px、16px 的正好 2px，与实测偏移逐一对上。**没有复现这个空格**——
  它是不可见字符的副作用，不是像 compare 那 3px 一样看得出来的手摆。要照抄的话
  在 `<br>` 前加一个 `&nbsp;` 即可。⚠ **第三十二轮按用户要求改成复现了**。
- **`dismiss` 那行右边缘窄 3px（199→196，1.5%）**：它是弹窗里唯一的 14px 文本，
  Figma 与 Chromium 对这个字号的字距舍入不同并在 30 个字形上累积；36 和 16 两个字号
  都是 0 偏差。r32diff 对这一行的容差因此是 ±4 而不是 ±2。
  ⚠ **这条第三十二轮证伪了：字距没有差，是探针容差取错造成的假象，见下一轮。**
- 熊图几何见上面第 3 条的像素比对。
- `tools/rwd.py` 全站 12 页 × 14 档宽度：✅ 全绿。
- **narrow 档 7 档视口**（360×640 / 360×744 / 390×744 / 414×896 / 575 / 767 / 768）：
  无页面横向溢出、熊的**墨迹**始终在 art 内且左右留白对称（360 时 67.8/66.1、
  414 时 94.8/93.1）、正文不压到熊区。⚠ 探针一开始把 `__bears` 的**盒子**
  左边缘为负（390 时 −17，正是稿值）报成越界 —— 盒子含透明边距且被 `overflow:hidden`
  裁掉，要判的是墨迹不是盒子。
- 平板档（768 / 1024 / 1280）与 1440 各截图核对，两态都拍了。

### 遗留

- **手机端在比 744 更高的视口上，正文与小熊之间会空出一大块**。稿子 285:19012 是
  390×744（浏览器栏之下的整块可用高度），content 460 + gap 32 + art 252 = 744 严丝合缝；
  视口更高时 `space-between` 把余量全给了中间那个 gap。真机（iPhone 15 Pro 约 744）
  不会出现，但 headless 840 的截图里很显眼。要改成「正文吸收余量」得先定一条稿里没有的规则。
- **平板档（768–1280）走的是手机那套全屏堆叠布局**，是第二十七轮定的（双栏只在 ≥1281）。
  1062 的双栏其实塞得进 1280，若要改是独立一轮的事。
- 桌面 code 态（揭码后）稿子里没有，仍是拿手机 code 态往 531 的列宽上套；
  `__body` 的 `justify-content:center` 只在这个态里起作用（email 态内容正好 400，是空操作）。
- 折扣码仍是稿里的占位符 `12345678CODE`，邮箱收集没有真后端（MVP 边界）。

### 文件清单

```
改  assets/customstyle.scss   promo-panel：art 四图规则 → 单张 __bears；head 高 64；
                              logo 改绝对居中；content 补 gap 64；body 去手机底 padding
                              并恢复桌面 center；lead 去负 margin；新增 __state（gap 20
                              + [hidden] 自防）；删 __field-icon；__input 补 reset；
                              $build → 20260825-r32
改  assets/customstyle.css    编译产物
改  index.html                art 区四个 <picture> → 一个；删输入框信封 svg；
                              两个状态容器加 .gb-promo-panel__state；?v= → r32
改  *.html（其余 10 页）       ?v= → r32
改  font-check.html           EXPECT_BUILD → r32
新  images/promo-bears.png    两组小熊的整体导出，624.54×481.17 @2x（1249×962）
新  images/promo-bears.webp   同上，102KB（旧的三张 webp 合计 120KB）
删  images/promo-bear.png / .webp
删  images/promo-bear-glow-lg.png / .webp
删  images/promo-bear-glow-sm.png / .webp
新  tools/r32check.py         本轮 42 条定向断言（比 Figma 数值）
新  tools/r32diff.py          390 两态叠在设计稿上逐行比墨迹（比实际绘制结果）
```

---

## 2026-08-26 第三十二轮：390 弹窗按稿逐像素对齐（`$build` = `20260825-r33`）

需求：「需要对齐 390 的设计进行设计稿还原」。上一轮已把结构做对，这一轮只处理
**叠在设计稿上还看得见的偏差**，判据全部是墨迹逐行比对，不是元素盒。

### 改了什么

1. **标题、副标各自的第一行补回稿里的尾随空格**（`<br>` 前加 `&nbsp;`）。
   上一轮查明稿子在 U+2028 之前多打了一个空格、Figma 居中时把它算进行宽，当时判定
   「不复现」；本轮按要求复现。普通空格会被 CSS 折叠，必须用 `&nbsp;`。
   结果：title l1 由 dx+5/+5 → **+0/+1**，lead l1 由 +2/+3 → **+1/+1**。

2. **标题补 0.5px 半行距修正**（`padding-top: .5px` + `margin-bottom: -.5px`）。
   PP Palma 的 ascent+descent 恰是 **1.25em**，手机端 `line-height:40 / font-size:36`
   于是半行距 = (40−45)/2 = **−2.5px**；Figma 把它取整成 −2 再排版，墨迹因此比
   Chromium 低 1px —— **盒子 y=128、高 80 完全正确，错的只是盒内文字的位置**。
   负 margin 抵掉 padding，flow 高度仍是稿子给的 80，`r32check` 无需改。
   桌面 `48 / 40` 的半行距 = −1 本来就是整数，`@include pc` 里显式归零。
   结果：title l1/l2 由 dy−2/−1 → **dy−1/+0**，标题带 `>32` 像素数 3558 → 1401。

3. **`tools/r32diff.py` 重写**：从「5 条只比 x 的文字带」扩成 **10 条带、x/y 双轴、
   两态各跑一遍**，容差统一 ±1px（Figma 与 Skia 对抗锯齿边缘的分歧上限）。
   新增 logo / 输入框占位符 / 按钮药丸 / 按钮文字 / dismiss / 下划线六条带 ——
   本轮的标题 bug 正是**盒子全对、墨迹偏 1px**，只比 x 的旧脚本抓不到。

### 判据

| | 上一轮 | 本轮 |
|---|---|---|
| email 态整面板平均差 | 4.95 | **2.05** |
| code 态整面板平均差 | 4.83 | **1.93** |
| `>32` 像素占比 | 3.65% / 3.44% | **1.55% / 1.34%** |
| 超 ±1px 的带 | title l1 +5、lead l1 +2、dismiss −3 | **无** |

- `tools/r32diff.py` 10 条带 × 2 态：全部 |dx|,|dy| ≤ 1。
- `tools/r32check.py` 42 条数值断言：绿（标题盒高 80.5，TOL 1.0 内）。
- 桌面 1440 单独核对：标题 rect 仍 y=248 h=96，墨迹与青柠贴纸逐位相同，面板平均差 2.15。
- `tools/rwd.py` 全站 12 页 × 14 档：✅ 全绿。
- **破坏性自检两次**：抽掉 `padding-top` → 4 条红；抽掉 `&nbsp;` → 2 条红。
  两次都先 `assert` 锚点串存在再替换，避免「没改到却报绿」。

### 两条上一轮结论的更正

- **`dismiss` 窄 3px 是假的**。真因是探针拿 `(77,77,77)` 容差 30 去量 **#666** 的文字，
  两边抗锯齿边缘被非对称地切掉。放宽到 `(102,102,102)` 容差 45 后，稿与实现
  同为 x[95,295]、y[444,455]，**逐位相同**。上一轮为它放宽到 ±4 的容差已收回。
- **差点误删 dismiss 的下划线**。节点自身 `style.textDecoration` 是 `None`，
  照着读会判定「稿里没有下划线」；实际它在 `characterStyleOverrides` →
  `styleOverrideTable["3"].textDecoration = "UNDERLINE"` 里。稿子那条线是
  0.755px 的软线（两行灰阶合成），Chromium 只能画整像素，实测
  `text-underline-offset: 2px` 落在 y457、`1px` 落在 y456，而稿子的重心在 457.17 ——
  **现行的 2px 就是最优解**，`text-decoration-thickness` 给小数也不会变（dsf=1 下会吸附）。
  改动已全部回退，这一条**没有产生任何代码变更**。

### 遗留

- 上一轮的四条遗留（>744 高视口的留白、平板走手机布局、桌面 code 态无稿、占位折扣码）原样保留。
- **半行距修正只做了这一个标题**。全站凡 `line-height < 1.25em` 的标题都有同样的 1px，
  要不要统一处理是独立一轮的事 —— 会牵动多个模块的视觉基线。
- ⚠ **0.5px 这个值绑在「ascent+descent = 1.25em」上**，换成客户授权的 PP Palma 后
  必须重量一次（canvas `fontBoundingBoxAscent/Descent`）：度量一变，该补的就不是 0.5 了。

### 文件清单

```
改  index.html                 promo 标题/副标 <br> 前补 &nbsp;；?v= → r33
改  assets/customstyle.scss    .gb-promo-panel__title 补 padding-top .5px / margin-bottom -.5px
                               （pc 内归零）；$build → 20260825-r33
改  assets/customstyle.css     编译产物
改  *.html（其余 10 页）        ?v= → r33
改  font-check.html            EXPECT_BUILD → r33
改  tools/r32diff.py           重写：10 条带、x/y 双轴、±1px、两态
改  docs/CHANGELOG.md          本条 + 第三十一轮两处结论标注
改  docs/PROJECT-STATUS.md     进度行
```

---

## 2026-08-26 第三十三轮：任务文档 5 项 + 对话追加 2 项（`$build` = `20260825-r34`）

### 改了什么

1. **`.gb-promo-panel__divider` `top` 50% → 52%**（任务 1，直接给值）。

2. **privacy-policy 末尾三段改成列表**（任务 2）。
   ⚠ **需求说的是 `ul`，稿子里是 `ol`** —— 326:83399 渲染出来是 `1. 2. 3.`，
   按 铁律「数值以源数据为准」落成 `<ol>`。要真的改成圆点，把标签换掉即可。
   稿里这段是**一个** TEXT 节点（326:83429）用 `\n` 分四段，`style` 里没有任何列表标记 ——
   **是从截图像素认出来的**，节点数据认不出来。
   几何逐条对上：序号墨迹 x=23/24、续行 x=44/45（= `padding-left: 24px`），
   **列表内行距恒 24px（= line-height），项间没有额外间隔** ——
   `li + li` 的 `margin-top` 因此由第三十轮凭空补的 8px 改成 **0**。

3. **波浪在 Windows 分数缩放下的发丝缝**（任务 3）。**只在 dsf 1.25/1.5/1.75 出现，
   1.0 和 2.0 干净** —— 所以之前整数缩放的全站扫描一条都扫不出来。
   两个成因叠在一起，缺一不可（实测：只修一个残留 18~45，两个都修才归零）：
   - **背景图会比盒子矮不到一个设备像素**，垫在下面的 `background-color`（上方色块）
     漏出来成一条亮线。改成**用 `background-color` 预铺下方色**（`--wave-under`），
     上方色改由一条高 `--wave-amp` 的 `linear-gradient` 显式画到圆弧闭合线为止。
     `background-color` 没有这个缺口，圆弧几何一点没动。
   - **盒子与下一区块要多叠一个像素**：`height: calc(var(--wave-h) + 1px)` +
     `margin-bottom: -1px`。那一像素处本来就是实心 `--wave-fg`，负 margin 把布局拉回去。
     `--down` 的圆弧锚在底边，多出来的像素会拖着整条波浪下移，所以它的圆心改钉在
     `calc(100% - 1px - var(--wave-r))`。
   ⚠ **`--wave-bg` 是透明的三种（`--to-lime` ×7 / `--bleed` ×2 / 裸类）不能预铺**，
   否则会在波浪上方糊一条整色带（第二十七轮踩过）；它们显式设 `--wave-under: transparent`，
   保留原状。这三种的配色对比都低，看不出来。

4. **banner 小熊去掉放大入场与上下浮动，改纯淡入**（任务 4）：
   `gb-float-art` → `gb-float-art gb-float-art--still`（`gm-art-fade-in 0.7s`，只动 opacity）。
   ⚠ **这是对第二十五轮「全站小熊恢复浮动，波浪上的除外」的反转**，也是这只熊的第三次翻转。
   回退办法：把 `gb-float-art--still` 去掉即可。附带好处是 LCP —— 这只熊是首页 LCP 元素
   （399,727 px²），透明元素不算 LCP 候选，淡入 0.7s+0.2s 比原来 1.5s+0.5s 早约 1.1s。

5. **nutrition 散熊去掉浮动**（任务 5）：直接摘掉 `gb-float-art`。
   它的入场动画本来就看不见（CSS 在页面加载即播，2.0s 播完，而这个模块在首屏之下），
   所以只留下无限浮动那一项可见效果，整类摘掉等价于「只去掉浮动」。
   ⚠ 同样是第二十五轮那条规则的反转（那轮才给它加上）。

6. **`.gb-stat` 的文字动效由词语弹跳改为行揭示**（对话追加）：
   `data-pop-text` / `data-pop-atom` 全部撤掉，四张卡的三个 `<p>` 各挂 `data-line-reveal`。
   ⚠ **参考站笔记（401:29596 / 216:5903）明写词语弹跳是留给统计数字的**，
   这条是对笔记的偏离，不是还原。撤掉后 `popText` 与 `.gb-pop-word` **全站零使用者**，
   代码保留没删，两处注释已改成「当前无使用者」。
   ⚠ **`.gb-ink-halo` 需要单独处理**：它是绝对定位的副本，行揭示的切分不会把它收进遮罩，
   于是数字还在遮罩里往上滑、青柠光晕已经整块杵在那儿。改成**等滑完再贴上**
   （`gm-fade-in .35s`，延迟 1.05s）。已验证首帧只有数字在滑、收尾光晕在位。

7. **`gb-product__title` / `gb-product__lead` 去掉行揭示**（对话追加）：
   两页各两处 `data-line-reveal` 摘掉。它们的父级 `.gb-product__info` 本来就有
   `wowo fadeInUp delay-in-1`，去掉后仍有整栏淡入，不会变成硬切。

### 判据

- **波浪**：`306` 个波浪实例（11 页 × 2 宽 × dsf 1.25/1.5/1.75）**残留 0 条**。
  破坏性自检：把 `--wave-under` 改回 `var(--wave-bg)` → 立刻报出 8 条（先 `assert` 锚点串存在）。
- **波浪没改几何**：改前改后整页截图逐页比（4 页 × 3 宽 × dsf 1/2）——
  **页高全部不变**，像素差 4~84，且每一项都落在「同代码连拍两次」的噪声基线之内
  （噪声源是还在浮动的 `.gb-stats__bear-art` 和跑马灯，最大 176,566 px）。
  ⚠ 一开始拿「改前 vs 改后有差异」当结论是错的，必须先量同代码噪声。
- **入场动效收尾**：11 页 × 2 档，滚完全页再等 2.6s，`[data-line-reveal]` 宿主 /
  `.gb-line-mask__inner` / `.gb-ink-halo` / `.wowo` / `.gb-float-art` **全部 opacity=1、
  transform 归位**。破坏性自检：停掉光晕规则 → 报 8 条。
  ⚠ 探针第一版把 `display:none` 的元素也算进去，`.gb-ingredients__desktop-only`
  在 390 恒为 opacity 0 被误报 —— 隐藏元素上的负向断言恒真，已加 `offsetParent` 过滤。
- `tools/rwd.py` 全站 12 页 × 14 档、`tools/r32check.py` 42 条、`tools/r32diff.py` 10 条带：见下方运行结果。
- privacy 列表：与稿逐行比，序号 x、续行 x、行距 24 全对；唯一差 4px 见遗留第 1 条。

### 遗留

1. **富文本段间距实现是 20px，稿子是 16px**。privacy + shipping 两页 **103 个** 16/24 正文
   节点的 `paragraphSpacing` 全是 16，实现里 `.gb-rich-text p` 的 `margin-bottom` 是
   第三十轮定的 20 —— 段落之间、以及本轮新列表与上一段之间都因此多 4px。
   **本轮没动**（需求只点名那三段改列表，改这个会动两整页的纵向节奏）。改法是一个数。
2. **`--to-lime`（7 处）/ `--bleed`（2 处）保留发丝缝**，原因见上；配色对比低，肉眼看不出。
3. **`--down`（10 处）的顶边同理未处理** —— 它的错配边在上方，现有 10 处配色
   （mint→white / mint→cream）都是低对比。要修就是把 3 的两招在顶边镜像一遍。
4. **1440 档两个 case 残留 R≈10**（满值 181，约 4%），已在肉眼阈下，没有继续追。
5. 词语弹跳（`popText` + `.gb-pop-word` + `gm-pop`）成为**零使用者的死代码**，按笔记保留。

### 文件清单

```
改  assets/customstyle.scss    .gb-promo-panel__divider top 52%；.gb-rich-text li+li margin 0；
                               .gb-scallop 改 --wave-under 预铺 + 显式上方色条 + 多 1px 叠边；
                               .gb-scallop--lg 高度同步；--down 圆心钉 -1px；
                               --to-lime / --bleed 补 --wave-under: transparent；
                               [data-line-reveal] > .gb-ink-halo 三条（含 no-js 兜底）；
                               word-pop 注释标注「无使用者」；$build → 20260825-r34
改  assets/customstyle.css     编译产物
改  assets/main.js             lineReveal 头部注释同步（popText 当前无宿主）
改  index.html                 hero 熊 → gb-float-art--still；nutrition 熊摘掉 gb-float-art；
                               4 张 gb-stat 由 data-pop-text/atom 改 3×data-line-reveal；
                               gb-product__title/__lead 去 data-line-reveal；?v= → r34
改  pdp.html                   gb-product__title/__lead 去 data-line-reveal；?v= → r34
改  privacy-policy.html        末三段 <p> → <ol><li>；?v= → r34
改  *.html（其余 8 页）         ?v= → r34
改  font-check.html            EXPECT_BUILD → r34
改  docs/CHANGELOG.md          本条
改  docs/PROJECT-STATUS.md     进度行
新  tools/revealcheck.py       11 页 × 2 档：所有入场效果收尾必须回到 opacity 1
```

## 2026-08-26 第三十四轮：index 手机端对照 228:5932 全面还原（`$build` = `20260826-r35`）

任务文档给了三条 hero 数值，外加一句「先对照 index 主页的手机端设计，检查还原」。
三条数值按源数据落地（其中两条与给的数不同，见下），检查部分把整页 144 个 TEXT 节点
与实现逐一对齐，另找出 20 处偏差。

### 先建对照工具（`tools/`，不进交付）

手上原有的脚本都是「专项断言」（r19/r20/r31/r32check），一轮一份、写死数值。这轮要的是
**全页扫描**，所以新写四支通用的：

- `figmob.py` — dump 一块 board 的可见流内节点树，坐标换算成 board 相对。丢掉
  `visible:false`（228:5932 留着整套没用上的变体：第二个 CTA 按钮、一行 overline 星标）。
- `mobgeo.py` — 同一页在某个宽度下的实际布局树。入场动效先钉到终态再量：`.wowo` /
  `[data-line-reveal]` / `.gb-float-art` 都带 transform，而 `getBoundingClientRect` 报的是
  变换后的盒子，不钉就是量在动画的随机一帧上。（只对量几何安全，截图不能这么干，
  见 `kill-animations-blanks-reveal-blocks`。）
- `mobdiff.py` — 把两边按**文档顺序做 LCS 对齐**后比 type token / 宽 / 高。
  ⚠ 不能按文本查字典：这页同一个字符串出现很多次（三条一模一样的 testimonial、三个
  `95%`），字典匹配会把它们随机配对，然后报出属于另一个元素的差异 —— 第一版就是这么
  把 stats 的 `60+`（fs 40）配到了 hero USP 的 `60+`（fs 32.24）上。
  另外两处必须先折叠，否则两边根本对不齐：`[data-line-reveal]` 宿主要吸收整棵子树
  （lineReveal 把文案拆成逐词 span，最内层文本宿主是词不是行）；`aria-hidden` 的
  ink-halo 副本要丢掉（它把每个标题的文本翻倍，`.gb-usp__value` 会读成 `60+60+`）。
- `resizeline.py` / `masktrap.py` — 见下方「关于 `<br>` 与整行揭示」。

### 任务文档三条：两条按源数据落成了别的值

1. **`.gb-hero__text` gap 24 → 16**（narrow，tablet 配 `fluid(16px, 24px)`）。
   任务给的是 15。稿里 237:14468 是一个 **gap 16** 的 Text frame（标题+副标），
   外层 237:15247 的 24 是 section 自己在 Text / Buttons / USPs 之间的节奏 —— 实现把
   两个 gap 都写成了 24，副标以下整块低 8px。**按 16 落地**：改完 lead / btn / USPs
   的 y 与稿逐位相同（264 / 340 / 416）。
   ⚠ tablet 必须同步补 gap 的 `fluid`，否则 767→768 会从 16 直跳 24。
2. **`.gb-usp__value` 的 `margin-left: 7px` 从 `@include pc` 提到基础规则**。
   原来标着「desktop only」，但 332:16427（桌面）与 237:14948（手机）是**同一个组件
   的两个实例**，尺寸逐位相同 —— 不是桌面专属，是手机漏了。7px 加在居中的 flex 项上
   实际位移 3.5px，稿里的偏移是 +2.83（21 / 6g）与 +5.01（60+ 的框更宽），7 是覆盖两者
   的折中值，沿用桌面既有取值不另算。
3. **`.gb-usps` 不加 `margin-top: 2px`，改成把数字框撑到稿的高度**。
   任务给的是给 `.gb-usps` 加 2px。但 USPs 与上方按钮的间距**本来就已经是稿的 24**，
   加 2 会变成 26。真正短的是数字那一格：稿 237:14948 是一个 **40 高的 frame** 套着
   37.2 的行盒，实现只有行盒的 37 —— 于是 label 高了 3px、整个 USP 89 而不是 92，
   数字墨迹也比稿高约 2.4px（这 2.4 就是任务里那个「2」的来源）。
   改法是 `line-height: 37px → 40px`（全档，桌面同样短 3）。
   ⚠ **不能用 padding 撑**：`ink-split()` 的 halo 是 `position:absolute; top:0`，
   对的是 padding box，加 padding 会让青柠描边和数字分家。
   ⚠ 连带 `.gb-usp__unit` 补 `line-height: 0` —— 不补的话 `6g` 的 `g` 会把行盒再撑高
   4px（`small-inline-grows-line-box-downward` 那个坑，第二十轮给 `+` 补过一次）。
   改完三列 value 齐 40、USPs 390 档 92 / 1440 档 96，与两块稿逐位相同。

### 手机档漏写：桌面值直接渗过来（7 处）

都是同一个病因 —— 值写在基础规则里，narrow 没覆盖，于是手机拿的是桌面稿的数：

| 选择器 | 手机稿 | 实现（=桌面稿） |
|---|---|---|
| `.gb-testimonial__text` | ls **0** | -0.32 |
| `.gb-highlight-card__text` | ls **0**、measure **294** | -0.32、271 |
| `.gb-product__guarantee-note` / `__guarantee` | lh **20** | 22 |
| `.gb-product__sub-title` | lh **26**（比桌面**大**） | 24 |
| `.gb-reviews__rating` | fs **12** / lh **18** | 14 / 22 |
| `.gb-reviews__disclaimer` | fs **12** / lh **18** | 14 / 22 |
| `.gb-product__guarantees` / `__guarantee` | gap **16** / 宽 **106** | 30 / 120 |

最后一条不只是数值不对：桌面的 `120×3 + 30×2 = 420` 塞不进 350 的版心，flex 把每项
压到约 96，`span { max-width: 86% }` 再砍一刀到 83 —— 「Aussie Based Support Team」
因此比稿多断一行。改回 106/16 后行数与稿一致。

另外 **`.gb-science-card__value` 补 `letter-spacing: 0`**（两块稿都是 0）。它自己没写
字距，被基础层那条裸 `p { letter-spacing: -0.32px }` 命中了 —— 在 56px 上很明显。

### 几何（6 处）

- `.gb-stats__grid` 删掉 narrow 的 `gap: 24`，回到 stack 档的 **32**（稿 243:28609 是
  158+32+158 铺满 350）。
- `.gb-stat__value` narrow lh 44 → **48**（稿 243:28613 同样是「框比行盒高」），
  `.gb-stat__unit` narrow 补 `line-height: 0`，`.gb-stat__label` narrow 补 `margin-top: -2px`
  —— 稿里「数字→label」是 10 而列本身是 12，-2 买回差额，不必为此把列拆成两层嵌套 flex。
  ⚠ **桌面档没动**：那里 `.gb-stat` 是绝对定位，`top%` 里带着客户点名的手工补偿
  （见 `.gb-stat--ingredients` 上方注释），改行高要连带重算那几个百分比，留作遗留。
- `.gb-nutrition__top` narrow gap 32 → **48**、padding-bottom 48 → **64**（稿 236:10399）。
- `.gb-nutrition__cards` narrow gap 24 → **32**（稿 236:10404；桌面横排才是 24）。
- `.gb-highlight-card` narrow padding `24/24/36` → **`20/20/32`**（稿 236:10405）。
- `.gb-highlight-card__body` 新增 `padding-inline: 8px`（**全档**）。稿 228:8955 / 285:21047
  两端都把文字块再往里收 8，实现一直没有 —— 补上之后桌面标题宽度也从 362.66 落到
  稿的 346.67，是顺带修好的。

### 换行：新增 `.gb-br-narrow`（4 处）

稿里有几处是 **U+2028 硬换行**，而桌面稿同一句是连排的。宽度做不到这件事：
`.gb-nutrition__title` 就算按稿限到 350 的 measure，「in」照样挤得进第一行（自然换行
4/2，稿是 3/3）。所以加一个只在 ≤767 显形的 `<br class="gb-br-narrow">`：

- `.gb-nutrition__title`（236:10402）
- `.gb-stat__label` 的「Green / benefits」（243:28662；桌面 341:47367 是一行）
- `.gb-footer__tagline` 两处（**11 页**都改；桌面 313:9427 是两行，手机稿是三行）

### 内容：science 卡 2 / 3 的正文照稿改回

实现里三张卡都用第一张的长文案，注释写着「设计里三张卡文案相同」——**这句是错的**。
稿里只有 eyebrow（都是没改过的组件默认值 `Easy Habit`）和 `95%` 是重复的，正文
第二张是 `No Fillers, No Nasties`、第三张是 `Made for Aussies`。已按稿落回。

### 关于 `<br>` 与整行揭示（用户中途提的疑问，实测未复现）

疑问是：换行不对可能不是缺 `<br>`，而是 resize 时宽度变了、而文案是整行揭示的，
所以分行被冻结。查证结果是 **lineReveal 本来就带 resize 重分行**（200ms debounce，
`groupLines` 会先把旧 mask 拆平再按当前 `offsetTop` 重新分组），三支探针都没复现：

- `resizeline.py`：「直接以 390 打开」对「1440 打开→滚完全页→resize 到 390」，
  20 个 `[data-line-reveal]` 宿主的行数、mask 数、每行文本**逐一相同**。
  先滚完全页是必要的 —— `groupLines` 对已揭示的宿主走 `is-settled` 另一条分支，
  不滚的话首屏以下根本走不到那条路径。
- `masktrap.py`：1200/900/700/500/390 五档，各在 **debounce 未到的 80ms** 和重建后
  各测一次 `scrollHeight > clientHeight`，**0 条被 mask 裁掉**。
- `<br class="gb-br-narrow">` 与遮罩不冲突：`wrapWords` 只处理文本节点，`<br>` 原样留在
  DOM 里，`groupLines` 按 `offsetTop` 分组时它自然落在两个 mask 之间。

拖拽过程中那 200ms 内看到的仍是旧分行，这是 debounce 的固有取舍，停下即纠正。
如果实际看到的是别的现象（具体哪个模块、什么宽度），按这三支探针的口径再复现一次即可。

### 判据

- `tools/mobdiff.py`：type-token 差异 **18 → 2**，剩的两条正是本轮有意改的 40 / 48 框高
  （`gb-usp__value` lh 37.2→40、`gb-stat__value` lh 44→48）；高度差异 21 → 17，
  两条 `HARD-BREAK-IN-BOARD` 清零，其余 17 条是量测口径差（稿是 TEXT 节点，实现元素带
  padding 或就是按钮本身）。
- `tools/rwd.py` 12 页 × 14 档：✅ 全绿。
- `tools/revealcheck.py`：11 页 × 2 档，入场动效收尾全部 opacity=1、transform 归位。
- `tools/r32check.py`：42 条断言全过（promo 弹窗本轮没碰，确认没被基础规则改动波及）。
- 桌面未退化：1440 下 hero USPs 96（稿 96）、highlight-card 410.66/362.66/346.66
  （稿 410.67/362.67/346.67）。

### 遗留

1. **stats 桌面档的数字框仍是 51（稿 56）、gap 12（稿 10）**。手机已改。桌面要动就得
   连带重算 `.gb-stat--*` 的 `top%` —— 那几个百分比里含客户点名的 5.5%，不是随手改的数。
2. **稿自身不一致**：stats 四个数字里只有 `21`（243:28628）是 ls 0，另外三个都是 -0.4。
   实现统一用 -0.4，没为单个节点开特例。
3. **science 三张卡的 eyebrow 都是 `Easy Habit`**，是组件默认值没改过的痕迹，属 WIP 占位，
   未动（正文已按稿落回，见上）。
4. `.gb-product__guarantee span { max-width: 86% }` 是第二十八轮桌面档的要求，手机沿用；
   宽度改回 106 后行数已与稿一致，故未在 narrow 覆盖它。

### 文件清单

```
改  assets/customstyle.scss    hero__text gap；usp__value lh 40 + margin-left 全档；usp__unit lh 0；
                               testimonial__text / highlight-card__text 的 narrow 字距与 measure；
                               product__guarantee-note / __guarantee / __sub-title / __guarantees 的 narrow；
                               reviews__rating / __disclaimer 的 narrow 字号行高；
                               science-card__value 补 ls 0；stats__grid 删 narrow gap；
                               stat__value / __unit / __label 的 narrow；nutrition__top / __cards 的 narrow；
                               highlight-card padding + 新增 __body padding-inline；
                               footer-cta__text narrow padding；新增 .gb-br-narrow；$build → 20260826-r35
改  assets/customstyle.css     编译产物
改  index.html                 nutrition__title / stat__label 补 gb-br-narrow；science 卡 2/3 正文；?v= → r35
改  *.html（其余 10 页）        footer__tagline 补两处 gb-br-narrow；?v= → r35
改  font-check.html            EXPECT_BUILD → 20260826-r35
新  tools/figmob.py            dump board 的可见流内节点树
新  tools/mobgeo.py            某宽度下的实际布局树（入场动效先钉终态）
新  tools/mobdiff.py           board ↔ 页面按文档顺序 LCS 对齐后比 token / 宽 / 高
新  tools/resizeline.py        「直接打开」对「resize 过来」的分行一致性
新  tools/masktrap.py          resize debounce 窗口内 line-mask 是否裁掉文字
改  docs/CHANGELOG.md          本条
改  docs/PROJECT-STATUS.md     进度行
```

## 2026-08-26 第三十五轮：任务文档 8 项（`$build` = `20260826-r36`）

需求方换了一份 8 条的手机端清单，其中两条是结构质疑（波浪该归谁）、一条是上一轮我判
「没复现」的入场折行问题被重申。先说这一条。

### 1. `is-word-split` / `is-split` 的折行确实是坏的，上一轮的验证方法有缺陷

需求方原话：「换行不对不一定是 br 的原因，是因为 resize 屏幕的时候宽度不够了，目前文本
采用的整行出现，所以出现了这个情况」。

上一轮我拿「直接以 390 打开」对「1440 打开→resize 到 390」比，20 个宿主 0 差异，据此
判为只有 debounce 窗口的瞬时现象。**这个判据本身是错的**：两边都已经被 lineReveal 拆过，
是同一个污染源的两次读数，自洽 ≠ 正确（[[probe-must-compare-against-invariant]]）。

换成真正的不变量——**同一页面关掉 JavaScript**，此时每个 `[data-line-reveal]` 都是未拆分
的普通段落，按整段自然折行。`tools/wraptruth.py` 三读对比（自然 / 稳定态 / debounce 窗口内），
6 档宽度 × 20 个宿主：

| | 修复前 | 修复后 |
|---|---|---|
| 稳定态不一致 | 0 | 0 |
| **resize 期间不一致** | **70 / 120** | **0 / 120** |

机制：`.gb-line-mask` 是 `display: block`。旧遮罩还在时，每一行是一个独立的块，**块内部
各自折行，而不是整段重折**。1440 拉窄再拉回，`Eating your greens / never felt this good.`
会变成 `… / never felt this / good.`——决定断点的是上一个宽度留下的遮罩。这个状态持续到
debounce 结束，而连续拖拽会一直把计时器重置。

修法：把 `groupLines` 开头那段拆平循环提成 `lineReveal.flatten()`，resize 时**立刻**对已播过
的宿主调用它（不 debounce），重组仍然延后。只处理 `is-revealed` / `is-settled` 的宿主——
未播的还藏在遮罩里，折行看不见，拆平反而会让文案抢在入场前闪出来。

### 2. 波浪与装饰熊改归下面那个 section（第 4、8 条）

第十八轮定的约定是「波浪归上面那个 section」。稿里不是这样：波浪是 section 之间的独立节点，
组件名就叫 **`Spacer Top`**，而 `Review Section`（236:11294）和 `PDP`（243:22224 / 316:27135）
干脆把自己那道包在了内部——**归下面**。桌面稿同构（`Spacer Desktop` 341:47307 在 science 前，
310:8425 是 PDP 的首个子节点）。

- `--cream-to-sand` + `.gb-stats__deco-bear`：`.gb-stats` → `.gb-science`
- `--lime-to-white --bleed`：`.gb-nutrition` → `.gb-product--lg`
- 新增 `.gb-scallop--edge-top`（`bottom: 100%`），绘制矩形与 `--edge` 在上一节里时**逐像素相同**
- **`.gb-stats` 的 `z-index: $z-base` 可以删了**：第二十八轮加它是为了让熊探出 stats 底边后
  不被 `.gb-science` 的不透明底盖住；熊现在本来就是 `.gb-science` 的孩子，天然画在后面

⚠ **占位空间没有跟着搬**，仍留在上一节的 `padding-bottom`。`--sc-h` 与 `--sc-lg-h` 因边界而异，
而 `.gb-science` / `.gb-product` 被多页复用、上游波浪尺寸不同，一刀切地加顶部预留会重复占位。

第 8 条的另一问：**`.gb-product--lg` 是波浪尺寸轴的修饰类**（第十九轮引入的四个正交修饰之一）。
section 自己负责给波浪留出高度，`--lg` 表示「我底下那道是大瓦片」，所以 `padding-bottom` 读
`--sc-lg-h` 而不是 `--sc-h`。它说的是下边那道，与这轮搬进来的上边那道无关。

### 3. 两只熊：稿在手机端都加了一层镜像（第 3、4 条）

肉眼判断软糖熊朝向不可靠，Figma 的 `absoluteBoundingBox` 对旋转节点又会说谎
（[[figma-rotated-frame-bbox-is-not-the-artwork]]）。判据用 `tools/bearmatch.py`：从设计截图
抠出轮廓，与素材做 IoU。

| | 原样 | 镜像 | 结论 |
|---|---|---|---|
| 中央熊 稿桌面 vs `stats-bear.png` | **0.750** | 0.484 | 桌面对，实现没错 |
| 中央熊 稿手机 vs `stats-bear.png` | 0.476 | **0.695** | **手机要镜像** |
| 装饰熊 稿手机 vs 稿桌面 | 0.467 | **0.944** | **手机要镜像** |
| 装饰熊 稿桌面 vs `stats-bear-deco.png` | 0.658 | 0.601 | 最佳 **0.841 @ +18°** |

对应稿里的 `332:16221` 与 `243:28564`——两个矩阵都是 `[-1,0;0,1]`，桌面没有对应层。
装饰熊的 `+18.52°`（243:28567 / 341:47524）实现里一直没做，素材本身是未旋转态。

装饰熊同时改了尺寸与定位：渲染光晕稿里是 1440 的 146×186、390 的 96×123，实现原来是
145×219 / 100×150（既往遗留「熊偏瘦长」就是这个）。现在 151×185 / 99.7×122。
中心锚在 **section 分界线**而不是波浪顶边——两块稿和实现只有这条线是一致的。

### 4. stats 网格的四条箭头（第 3 条）

`.gb-stats__arrow` 在 `@include stack` 里被 `display: none`，手机端整组消失；连带**手机网格比稿
矮 128px**（717.42 vs 稿 845.34），因为稿里那块空白正是箭头占的。

手机稿的四条箭头旋转角与桌面不同（+95.71 / +75 镜像 / −135 镜像 / −60，桌面是 −19.19 /
−51.05 / +127.29 / +141.03），且**其中两条带镜像，不只是转角**。SVG 里烘焙的是桌面变换，
所以在 `<span>` 上叠 `matrix = M_手机 × M_桌面⁻¹`。left/top 用墨迹中心
（`translate(-50%,-50%)` 在矩阵之后跑，所以它们就是中心），width 反解自
`aabb_w = |a|W + |c|H`、`aabb_h = |b|W + |d|H`——两式各自解出的宽度相差 4% 以内，这是自检。

`overflow: hidden` 从 `.gb-stats__bear` 移到 `.gb-stats__bear-art`：箭头是前者的另一批孩子，
挂在前者上会把它们一起裁掉；挂在后者上照样拦住 184.8% 宽的画面越出 390 视口。

### 5. 数值项（第 1、2、6、7 条）

需求方给的值先与稿核对，作用域按稿判定——**有三条如果照字面落到基础规则会砸掉桌面**：

| 项 | 稿桌面 | 稿手机 | 处理 |
|---|---|---|---|
| `.gb-highlight-card` 圆角 | 24（341:46409） | 16（236:10405） | narrow only |
| `__media` 圆角 | `[16,16,8,8]`（285:21045） | `[8,8,0,0]`（228:8968） | narrow only |
| `__lip` 宽 | 573/362.67 = **158%** | 444.41/310 = **143.36%** | narrow only |
| `.gb-pack-band` left | **50.00%**（341:46422） | **75.75%**（228:9018） | narrow only |

与稿不同、按需求方的数落的，逐条记下原因：

- **`.gb-science` padding-top 53**（稿 64）。稿的 64 是从一道 **36 高**的 Spacer Top 底下起算的，
  而实现的小波浪在 390 下渲染成 **48.03**（见「遗留」）。53 是对着这道更高的波浪配的。
- **`.gb-science-card__body` gap 19**（稿盒间距 12）。稿的 `427319601` 是 **56 高的帧包着 44 的
  行盒**，实现只有裸 44，所以实际显示出来的是 12 + 6 的半行距 = 18。与上一轮 USP 37→40 同源。
- **`.gb-science__inner` gap 46 / `__cards` gap 31**（稿 48 / 32）。原实现是 32 / 24——**手机档
  从来没给过自己的值**，拿的是桌面数，两个都错。需求方的数比稿小 1~2。
- **`.gb-highlight-card__text` max-width 283**（稿 294）。三段手机文案最宽的墨迹 270.91，
  283 与 294 折行完全相同。
- **`.gb-logo-scroll__item` 106×44 / viewport padding 4**。`Social Proof`（341:47384）**只存在于
  桌面稿**，手机端没有设计源，这两个数是需求方定的（正好是桌面 193×80 的 55%）。
  ⚠ 循环速度是「节距 / 15s」，节距从 669 缩到 408 后条带会明显变慢，需要的话要一起调时长。

对上稿的：`.gb-science__head` gap 16 + 左对齐（228:8166 itemSpacing 16、两个 TEXT 都是
`textAlignHorizontal: LEFT`；桌面靠对称 padding 居中，所以只给 narrow）、
`.gb-highlight-card` 圆角 16、`__media` `[8,8,0,0]`、`__lip` 143.36%、`.gb-pack-band` 75.75%。

顺带：`228:8167` 有**两个 U+2028**（`Lab-tested. ⏎Aussie approved. ⏎No funny business.`），
桌面只有一个，补了一处 `gb-br-narrow`。

### 判据

- `tools/wraptruth.py`：120 次读数，稳定态 0 不一致、**resize 期间 70 → 0**
- `tools/r36check.py`（新）：8 条任务 50+ 条 computed-style / 几何断言，390 + 1440 全过，
  含「桌面必须没变」的反向断言（圆角 24、lip 158%、pack 50%、标题仍居中、`gb-br-narrow` 不显形）
- `tools/bearmatch.py`（新）：轮廓 IoU，见上表
- `tools/rwd.py` 12 页 × 14 档：✅ 全绿；`revealcheck.py`：入场全部 opacity=1、transform 归位
- `tools/r31check.py` 51 条、`tools/r32check.py` 42 条全过
- `resizeline.py` 0/20、`masktrap.py` 5 档 0 裁切
- 几何：手机 stats 网格 **845.4**（稿 845.34）；装饰熊 390 **99.7×122**（稿 96×123）、
  1440 **151×185**（稿 146×186）；两档 `scrollWidth - clientWidth` **= 0**
- `r19check` 8 条、`r20check` 1 条失败——**在 HEAD 基线上同样失败**，是既往遗留
  （`gb-sec-edge` 第十九轮就删了），本轮没引入新失败

### 遗留

- **小波浪在手机端高了 12px。** 所有稿的手机 Spacer 一律 **36** 且 `clipsContent: true`；
  设计截图实测振幅 35、节距 145、槽底正好落在 section 分界，几乎没有实心带。
  实现 `--sc-band: clamp(13.3px, 1.63vw, 23.4px)` 在 390 被钉在 13.3，`--sc-h` 算出 **48.03**。
  桌面 23.4 是对的（96 = 72.55 + 23.45），大波浪手机也是对的（35.27 ≈ 36），**只有小波浪的
  clamp 下界错**。正确的下界约 1.2，但 390→1.2 / 1440→23.4 不是一条 vw 直线，改它等于重设
  波浪的断点体系，会动全站 11 页每个 section 的 `padding-bottom` 与页面总高——本轮没动。
  这也是第 6 条 `padding-t 53`（≈ 64 − 12）的由来：波浪修好后 53 应改回稿的 64。
- **`images/stats-bear-deco.png` 与中央熊素材不是同一份导出。** 墨迹比 0.654，中央熊 0.787；
  IoU 最佳 0.841（+18°），而中央熊素材镜像后能到 0.861。需求方这次只点了旋转，没换素材。
- **手机稿的 science lead 比实现多一句**：`228:8168` 结尾是 `… to prove it. Based on similar
  studies on this type of formulation.`，桌面稿（I341:46642;316:29451）没有这句。看着像
  和 95% 那组数字配套的免责说明。只有一块稿有的文案属于内容决定，没擅自补，请需求方确认。
- 768–1024 那一段仍然没有箭头：那里跑的是手机两列网格但列宽接近桌面，熊槽固定 208，
  箭头挂在熊上会离它指的文案很远，而没有任何一块稿覆盖这个区间。
- 上一轮的 stats 桌面档数字框 51（稿 56）/ gap 12（稿 10）、稿自身 `21` 字距不一致、
  science 三卡 eyebrow 都是 `Easy Habit`，均沿用未动。

### 文件清单

```
改  assets/customstyle.scss    scallop 新增 --edge-top；stats 去 z-index；stats__note narrow；
                               stats__arrow narrow 四条 matrix + 位置；stats__bear narrow 留白；
                               bear-art 接管 overflow；bear-img narrow 镜像；
                               stats__deco-bear 重写（迁 gb-science / 旋转 / 镜像 / 尺寸 / 锚点）；
                               hero__title narrow padding；hero__bear narrow left+width；
                               logo-scroll__item / __viewport narrow；
                               science padding-top / __head / __inner / __cards / card__body narrow；
                               highlight-card 圆角 + __media 圆角 + __lip 宽 + __text measure（均 narrow）；
                               nutrition__bears-img left 51.5%；pack-band narrow left；
                               $build → 20260826-r36
改  assets/customstyle.css     编译产物
改  assets/main.js             lineReveal 抽出 flatten()；resize 先拆平再 debounce 重组
改  index.html                 两道波浪 + 装饰熊迁入下方 section 并改 --edge-top；
                               science 标题补 gb-br-narrow；?v= → r36
改  *.html（其余 10 页）        ?v= → r36
改  font-check.html            EXPECT_BUILD → 20260826-r36
新  tools/fignode.py           按 id dump 节点子树（绝对几何 + 变换矩阵）
新  tools/bearmatch.py         设计截图轮廓 vs 素材的 IoU（镜像 / 逐角度）
新  tools/wraptruth.py         折行不变量：JS 关闭的自然折行 vs 遮罩折行
新  tools/r36check.py          本轮 8 条任务的定向断言
改  docs/CHANGELOG.md          本条
改  docs/PROJECT-STATUS.md     进度行
```

## 2026-08-26 第三十六轮：任务文档 21 项 + 全站手机端对稿复查（`$build` = `20260826-r37`）

需求方给了一份 21 条的手机端清单，外加一句总要求：「虽然检查过几轮还原检查但仍不理想，
我需要你对照手机端设计再次检查全站设计还原，不仅对照节点数据，而且仍需对照截图」。
21 条全部落地，其中三条的**做法**与字面给的不同（下面逐条记原因）；总要求那部分把
11 页都对了一遍稿，另找出 6 类偏差。

### 0. 先说清一件事：这轮有两处判据本身是坏的，修完才看见问题

**箭头「大小没还原」是真的，而上一轮的判据看不出来。** 第三十五轮把四条箭头的元素盒
solve 到与 `absoluteRenderBounds` 一致（59.5×65.3 对稿 60.1×64.7，±2px），据此判为已还原。
但把设计导出与实现截图并排放大后，箭头明显更短更细——**renderBounds 不是画出来的墨迹**：
它带着 OUTSIDE 描边的斜接外扩，比导出里真正的墨迹大 9~55%（逐条不同）。元素盒对上了，
盒子里画的东西没对上。

改判据：`tools/arrowfit.py` 直接在两张 PNG 上量青柠墨迹，从每条箭头自己的中心做**连通域
洪泛**（熊的光晕也是青柠，且伸进每个箭头的窗口，不隔离就是在量光晕），按比值反解 width。
left/top 两侧都锚在**熊槽**上（板 `332:16221` 207.82×254 @ (90.64,1854)，实现 208×257.42），
否则 stats 区在页面上的整体下移会被算进箭头自己的偏移里。迭代一轮后收敛：

| 箭头 | 稿墨迹 | 修前 | 修后 | width |
|---|---|---|---|---|
| --1 | 52×64 | 39×48 | 53×63 | 26.79% → 35.72% |
| --2 | 46×70 | 30×45 | 45×68 | 24.82% → 38.33% |
| --3 | 24×75 | 22×69 | 24×74 | 35.48% → 38.63% |
| --4 | 32×75 | 28×66 | 32×75 | 34.25% → 39.03% |

描边另算：SVG 里烘的是**桌面**的 OUTSIDE 1.78036（居中化 3.56071），跟着缩到手机尺寸就成了
1.70px，而手机板自己是 OUTSIDE **1.1499**（居中化 2.2998），细 26%——看起来像"小一号"而不是
"细一点"。narrow 下给 path 加 `vector-effect: non-scaling-stroke` + `stroke-width: 2.2998px`，
把线宽从变换里摘出来。

**`tools/hardbreaks.py` 第一版恒报全绿。** 它把 `<br>` 换成 U+2028 当标记，再把两边正规化后
比较——而 Python 的 `\s` **包含 U+2028**，`WS.sub(" ", s)` 把标记连同硬换行一起压成空格，
硬断和软断变成同一个字符串。换成 `\x00` 后，立刻报出 **18 处**该断没断的地方。
（`[[negative-assert-needs-liveness-guard]]` 的教科书案例：修之前的"全绿"是假的。）

### 1. 任务文档：三条没有照字面做

- **`.gb-hero__lead padding: 0 10px`** → 改成 `<br class="gb-br-narrow">` + `&nbsp;`。
  给的 padding 是在逼折行：稿 `237:14478` 是 U+2028 硬断成
  `Real fruit, real veg, real vitamins,` / `hiding in a gumi bear.`，而实现在 350 的量里
  `hiding` 挤得进第一行（实测）。padding 能挤出同样的结果，但盒子从稿的 350.26 变成 330.26，
  且折行点靠字体度量——换上授权版 PP Palma（比试用宽 4.7%）就可能再变。第三十四轮已经为
  同类问题立了 `.gb-br-narrow`，这里照用。U+2028 前稿里多打了一个空格且这行居中，所以带
  `&nbsp;`（见 `[[figma-centred-text-counts-trailing-space]]`）。
- **`.gb-testimonial svg 103×20`** → 落 **100×20**。103×20.6 是 `.gb-reviews__rating` 和
  PDP 星条的尺寸（`191:2387` / `187:12721`），testimonial 里那条是
  `187:12732;183:4814`，**100×20**（5×20，itemSpacing 0）。两处都改了，各按各的数。
- **`.gb-nutrition padding-b 27px`** → 写成 `calc(var(--sc-lg-h) - 9px)`。27 这个数是对的，
  来路是稿 `Frame 992568` 的 **itemSpacing -9**：波浪 36 高但上压 9px 到 pack band 上，
  只有 36-9=27 露在这一节下面。但写成定值会在 767/768 断点上从 27 跳到 68——波浪本身
  是跟着视口长的。改成相对波浪高度表达后交接连续，代价是 390 处 26.27 而非 27（0.73px）。

### 2. 任务文档：其余 18 条

`.gb-stats__deco-bear` top -22.34 / width 钉成 **81.6px**（需求方点名「百分比在 767 以下太大」——
20.92% 到 767 就是 160px，而这只熊只画在 390 板上）；`.gb-product` padding-top **52**
（= `243:22226` paddingTop 32 + `191:2214` paddingTop 20，实现没有内层那个 frame，两者并成一个）；
`__stage` radius 16、`__gallery` / `__media` gap 16（`191:2214` itemSpacing）、`__inner` gap 32、
`__guarantee-note` radius 8 + padding 8/20、`--lg` padding-bottom `calc(50px + --sc-lg-h)`；
`.gb-reviews` padding `64 0 78`、`__inner` gap **48**（板上手机也是 48，narrow 的 32 是错的，
连 tablet 插值一起删）、`__rating svg` 103×20、`__disclaimer` padding 0 20；`.gb-reel__play`
**64×40**（`183:5446`，原来是桌面的 85×53）；`.gb-testimonials` padding-top 0 / gap 30 /
margin-bottom **0**（那 48 与 `__inner` 的 gap 重复计一次）；`.gb-deco-bear--a` 154 / -60 / 11%。

**`.gb-testimonial` 的 `flex: 1 1 300px` 是个真 bug**：`@include stack` 把这一列改成 column
之后，flex-basis 就是**高度**，于是每张卡被撑到 300 高而板上是 196，文案浮在一个空盒子里。
narrow 只是最明显的一档，768–1024 同样中招，所以改在 `stack` 上（`flex: auto`）。
桌面 >1024 仍是 row，300px 是宽度，不动。

**`.gb-footer-cta__arc` 改双 viewBox（11 页）**，遗留清掉。板上 `236:11723` 是 278.28×46.38 的框，
里面是手机椭圆（237.05×131.41 → rx 118.525 / ry 65.705），左内缩 20.61、上内缩 17.13。
原来是把桌面的 452×51 整体缩到 237，弧被压成近正圆、字号一起缩水。做法照
`.gb-promo-card__arc` / `.gb-dosed__arc`：markup 出两份，`--pc` / `--mob` 切。

### 3. 对稿复查另找出的 6 类

- **`.gb-deco-bear--b` 停在 CTA 按钮上。** 板 `313:10011` 把这只熊放在 **Footer** 上而不是
  CTA 上：墨迹 188.34×165.68、离右缘 28.28、顶边在 wrapper 顶下方 472（即挂出这一块的底）。
  实现是 160 宽 / right 0 / top 300，正好横在 "Start Your Greens" 上。
- **our-story 与 how-gumi-works 少一条 testimonial。** 两块板的 `187:12731` 都是 **880 高
  = 4 条**；index 的是 652 = 3 条，因为它的第 4 条 `visible: false`。**是设计师逐页定的，
  不是 WIP 残留**，所以补齐（文案照抄，四条本来就同文）。补完 `gb-reviews--cream` 1828.3
  对板 1827.6。
- **18 处该硬断没断的行**（见第 0 节）。桌面板同一句也断的走普通 `<br>`（hero USP
  `Vitamins ⏎ & Minerals`、两条 `.gb-highlight-card__text`、五页的 `30 Day ⏎ Money Back
  Guarantee`）；桌面是平的走 `gb-br-narrow`（pdp `Quality you ⏎ can trust`、reviews
  `Recommended ⏎ by experts`、faq / how-gumi-works 的页头标题、shipping 第一个表头）。
  居中且 U+2028 前有空格的都带 `&nbsp;`。
- **`.gb-dosed__title` 两块板断在不同位置**（桌面 2 行、手机 3 行，断点不重合），单靠
  `gb-br-narrow` 表达不了，新增反向的 **`.gb-br-wide`**（narrow 下隐藏）。
- **shipping 两个表的列宽都不对。** 板 `326:83143` 是 88/262、`326:83187` 是 203/147，
  实现是内容自适应，量出来 60/289 和 260/90。第一个表头加 `<br>` 之后第一列塌到 60、
  正文行跟着断成两行，整表从 397 涨到 584（板 376）——所以列宽和 `<br>` 必须一起做：
  narrow 下 `table-layout: fixed` + 百分比列宽 + `th/td` padding 10（10+24+10 = 板的 44 行高），
  第二个表用新修饰类 `.gb-rich-table--even`。改完 384 / 360 对板 376 / 352（差的 8 是 8 条
  1px 分隔线——板上那是 RECTANGLE，不占布局高度）。
- **767/768 交接上有三处跳变**（`.gb-testimonials` gap 30→24、`.gb-reviews__disclaimer`
  padding 20→0、`.gb-nutrition` padding-bottom 27→68），都是只改了 narrow 没配 tablet 斜坡。
  补 `fluid()` 后连续。

### 判据

- **桌面没被动到**（需求方明确「只改手机端」）：1440 快照按**矩形多重集 + body 总高**比
  （新增了 svg / br / 一条 testimonial，路径式 diff 的兄弟下标会整体错位，见
  `[[css-refactor-computed-style-judge]]`）。**9 页 0 处矩形消失、body 高不变**；
  index 唯一 1 处是 hero USP label 盒宽 110→90.3（加 `<br>` 后收成最长行的宽度，
  中心 300.0→300.05 不变）；our-story / how-gumi-works +28 是补第 4 条 testimonial
  在 1440 挤窄了每张卡。
- `tools/arrowfit.py`：四条箭头墨迹比值收敛到 1.00±0.03
- `tools/hardbreaks.py`：11 页 34 ok / 6 missing（6 条全是成分辐射图 PNG **图片内**的
  文字，非 DOM，误报）
- `tools/pagefit.py`（新）：分段高度对稿，faq -6.2 / get-in-touch -10 / science -212 …
- `tools/rwd.py` 12 页 × 14 档 ✅ 全绿；`revealcheck.py` 入场全部 opacity=1、transform 归位
- `r31check` 51 条、`r32check` 42 条、`r36check` 全过（r36 的 `390 deco centre above seam`
  基线 9.34 → 22.34，需求方这轮点名改的）
- 767/768 逐属性对读：14 项 0 跳变

### 遗留

- **shipping / privacy-policy 两页的板上没有 footer CTA**（另外 9 页都有 1504/1564 的
  `Footer Section CTA`），实现两页都有。删一个 CTA 是内容决策不是还原，**未动，请需求方定**。
  这两页的页脚本来就有一条挂着的冲突（第十四轮：它们用的是另一版页脚组件 16/24/600/ls 0）。
- **`.gb-product__app-slot` 高 0**，板上 `Quantity` 84 + `Subscription` 512 共约 596 在这里
  —— 第二十二轮有意删掉的订阅 app 占位框，`pagefit` 里 index/pdp/our-story/how-gumi-works
  约 -400 的缺口都是它，**不是还原问题**。
- **小波浪在手机端仍高 12px**（`--sc-band` clamp 下界，第三十五轮记的那条），`.gb-stats`
  的 12.1 和 `.gb-science` padding-top 53（本该是板的 64）都还挂在这条上。
- index hero 标题与 `Clean ⏎ Ingredients` 靠宽度折出了与板相同的行数，没有硬断兜底；
  前者的 3 行来自 `padding: 0 25px`，换授权字体后要重验。
- `images/stats-bear-deco.png` 与中央熊不是同一份导出（第三十五轮遗留，未动）。
- 中央熊墨迹看着比板上大一圈（槽 208×257.42 对板 207.82×254 是对的），素材本身的问题，未查。

### 文件清单

```
改  assets/customstyle.scss    stats__arrow narrow 描边 + 四条 width/left/top 重解；
                               stats__deco-bear narrow top/width（改定值 px）；
                               nutrition padding-bottom narrow+tablet；
                               product padding-top 52 + tablet 起点；product--lg padding-bottom；
                               product__stage/​__gallery/​__media/​__inner/​__guarantee-note 的 narrow+tablet；
                               reviews padding-bottom；reviews__inner 去 narrow/tablet；
                               reviews__rating svg；reviews__disclaimer padding；
                               reel__play 64×40；testimonials padding/gap/margin；
                               testimonial stack flex:auto + svg 100×20；
                               deco-bear--a / --b 的 narrow；footer-cta__arc 改 --pc/--mob；
                               新增 .gb-br-wide；rich-table narrow 列宽/行高 + .gb-rich-table--even；
                               $build → 20260826-r37
改  assets/customstyle.css     编译产物
改  index.html                 hero__lead 硬断；usp__label / highlight-card ×2 / 30 Day 硬断；
                               footer-cta arc 双 svg；?v= → r37
改  pdp.html                   promo-card__title / 30 Day 硬断；arc 双 svg
改  reviews.html               expert__title / 30 Day 硬断；arc 双 svg
改  faq.html                   page-hero__title 硬断；arc 双 svg
改  how-gumi-works.html        page-hero__title / dosed__title（双向断点）/ 30 Day 硬断；
                               补第 4 条 testimonial；arc 双 svg
改  our-story.html             30 Day 硬断；补第 4 条 testimonial；arc 双 svg
改  shipping.html              第一个表头硬断；第二个表加 .gb-rich-table--even；arc 双 svg
改  science / get-in-touch / referral / privacy-policy.html   arc 双 svg；?v= → r37
改  font-check.html            EXPECT_BUILD → 20260826-r37
改  tools/r36check.py          deco 基线 9.34 → 22.34
新  tools/fq.py                任意 board 按 name/text/id 查节点（含旋转/描边/override）
新  tools/shotcmp.py           设计导出与实现截图分段并排（先走一遍页面再截，否则 wowo 不播）
新  tools/arrowfit.py          箭头墨迹连通域反解 width/left/top
新  tools/pagefit.py           11 页分段高度对稿
新  tools/hardbreaks.py        全站 U+2028 是否落地（⚠ 标记不能用 U+2028，\s 会吃掉）
改  docs/CHANGELOG.md          本条
改  docs/PROJECT-STATUS.md     进度行 + 待决事项
```

---

## 2026-08-26 第三十七轮：其余 10 页的截图逐区块对稿（`$build` = `20260826-r38`）

第三十六轮把需求方任务文档的 21 条做完了，但他同时要的「对照手机端设计再次检查全站还原，
不仅对照节点数据，而且仍需对照截图」只做了数值层，**截图逐区块比对仅覆盖 index**。
这一轮把剩下 10 页做完，共改 16 处 —— 其中 6 处是数值层根本发现不了的
（描边被啃、整块缩 15%、组件整个缺失），另有 11 处判定为桌面/手机稿冲突或稿自身痕迹，
只记录不改，见 `PROJECT-STATUS.md`「第三十七轮新增的待决事项」。

### 0. 工具：`pagescan.py` 重写成显式锚点

上一轮留下的版本按文档顺序把 build 的 `<section>` 和 board 的顶层帧配对，**结果全是错位的**：
board 的 children 不按 y 排序（index 上 `Frame 992545@2442` 排在 `Footer@10040` 后面），
而且板子里夹着 build 折进上一个 section 的 `Spacer Top`（波浪）。改成：

```bash
python3 tools/pagescan.py science.html --list --depth 2          # 两侧块各自排序打印，人工读出配对
python3 tools/pagescan.py science.html --pairs ".gb-compare=3162" --h 900
```

`--pairs` 一次启动浏览器跑完一页的所有锚点，超过 `--h` 的区块自动切成多片。board 的 y 直接
取自 `absoluteBoundingBox.y − root.y`，**已经含了那 96px 的假浏览器栏，不要再加**。

### 1. 数值层查不出、只有看图才发现的六处

- **`.gb-vs__table` 整块缩了 15%（PDP）**。narrow 下它有 `margin-inline: auto`，而
  auto margin 会让 flex 子项退出交叉轴 stretch → 表格 shrink-to-fit 成 298.8，而不是可用的 350。
  下面所有 `/351` 的百分比（青柠卡、GUMI logo、小熊、THE OTHERS、抹茶堆）跟着一起缩，
  值列窄到「60+ ingredients, dosed to matter」和「Often padded, rarely disclosed」都折行。
  补一行 `width: 100%` 就全对上了：表格 x=20 w=350，两列 87 + 22 + 241。
- **`.gb-dosed__title` 的青柠描边被自己的入场动效啃出洞（how-gumi-works）**。它同时有
  `ink-outline()` 和 `data-line-reveal`，而 `lineReveal` 的 `wrapWords` 把每个词包成 span，
  **inline 子元素是独立的绘制单位** —— 后一个词的字形压在前一个词的光晕上。改用
  `ink-split()`（整串的光晕画在一个绝对定位副本上）。这里有个恰好成立的巧合：`wrapWords`
  只处理直接文本节点，所以 `.gb-ink-halo` 里的文案不会被拆词，光晕天然是一整条。
  与 `.gb-stat__value` 是同一套组合。
- **Reviews 专家卡轮播没有导航箭头**。稿 `324:64961` 的 `Frame 992460` 是两个 32px 青柠圆
  （`#b5ed61` 底 + `#005635` 2px 箭头），桌面板没有（三张卡并排放得下）。补 `.gb-expert__nav`，
  接现成的 `slider` 模块（`data-slider` / `data-slider-track` / `data-slider-prev|next`），
  桌面 `display: none`。
- **Reviews 页头的五颗星是灰的**。`.gb-page-hero__overline` 的 SVG 用 `currentColor`，
  继承了那行小字的 `$c-gray-700`。两块板的星都是 `#85c947`，只有那行字是灰的。
- **PDP 上多出三条 testimonial**。稿里 `Container 187:12730` 在**手机和桌面两块板上都是
  `visible: false`**（PDP 下面另有评论 app 区），实例高度 863.6 正好等于去掉它之后的和。
  删掉后 `.gb-reviews` 内容 736 对稿 735.6。桌面同步少 358（板上那块是 308 + 48 的 gap）。
- **`.gb-science-card--nutrient` 的 `50%` 没有描边**。上一轮的注释写着「桌面板有、手机板
  没有」——**查反了**：`324:58062` 和桌面的 `316:29208` 都是 `#b5ed61 7px OUTSIDE`。
  半径是绝对值，不能跟着字号的 em 走（narrow 是 36px 面），narrow / tablet 都显式写 7px。

### 2. 间距与几何（都是 narrow 档，桌面未动）

| 位置 | 原 | 稿 | 后果 |
|---|---|---|---|
| `.gb-promo-card__body` gap | 8 | **32** | 稿把 Content / Footer 拆成两帧、中间无 gap，按钮上方的空隙是 Content 自己的 padding-bottom；错当成 Footer 的 gap 8 |
| `.gb-promo-card--white .gb-promo-card__stack` gap | 12 | **32** | 旧注释写「手机板根本没有白卡」，实际 `324:53799` 的第二张就是 |
| `.gb-promo-card__main` gap | 24 | **32** | 同上，arc / 标题 / 引导句 / 列表在手机板上是一帧里的四个同级项 |
| `.gb-dosed__text` gap | 24 | **32** | — |
| `.gb-dosed__block` gap | 32（写在 `@include stack` 里） | **48** | 顺手把数值从布局阈值挪进值档 + tablet 斜坡 |
| `.gb-cta-band__plate` padding-block | 24 | **3.75** | 板 507.5 裹着 500 的内容帧，只露 3.75 |
| `.gb-cta-band__content` | 内容撑开 464 | **min-height 500 + space-between** | `Frame 992591` 是 FIXED 500，itemSpacing 108 是下限、实际间距 144 |
| `.gb-science-card--nutrient .gb-science-card__body` gap | 19 | **12** | 19 是为 stat 卡那个 56 高的数字帧补的半行距，nutrient 卡没有那个帧 |
| `.gb-ingredients__body > * + *` | gap 16 | **+16 = 32** | 稿把文案和「后面那个东西」（science 是手风琴、reviews 是按钮）分成两个 Container |
| `.gb-form__disclaimer`（referral） | 14/20/-0.28 | **16/24/-0.32** | 用了桌面板的字号，手机板是正文号，四行 24 |

改完的逐像素结果：promo 两张卡 **755 / 848** 对稿 755 / 848；dosed 的 arc/标题/引导句/图
**64 / 125 / 229 / 421** 对稿 64 / 125 / 229 / 421；cta-band 的板/内容/弧/标题/按钮
**507.5 / 500 / 2122 / 2190 / 2442** 对稿 507.5 / 500 / 2121.8 / 2189.8 / 2441.8。

### 3. Shipping 的表格原来是一张真网格

`326:83143` 每个单元格都是 `#cccccc 0.5 CENTER` 描边 + `10/12` 内边距，表头单元格填
`#f3f3f3`，**第 2/4/6 行整行也填 `#f3f3f3`**。实现只有一条 `border-bottom`，没有竖线、
没有斑马、没有左右内边距。补齐后两张表 **377 / 353** 对稿 376 / 352（差的 1px 是外框）。
padding 取 **9.5** 不是 10：描边是 CENTER，占在 44 的行高之内，`(44 − 24 − 1) / 2 = 9.5`。
新增 `$c-gray-050: #f3f3f3`。桌面没有 shipping 稿，那边的单线样式原样留着。

### 4. 一处文案范围

get-in-touch 的同意行，稿 `326:80318` 的 `characterStyleOverrides` 只给
**`privacy policy`** 这 14 个字符加了下划线，实现把 `friendly` 也包进 `<a>` 了。

### 判据

- `tools/rwd.py` 12 页 × 14 档 ✅ 全绿
- `tools/revealcheck.py` ✅ 全部 opacity=1、transform 归位
- `tools/r31check.py` ✅ 52 条（`.gb-dosed__title` 那条改判 `> .gb-ink-halo`，
  并补一条 `text-shadow: none` 钉住 ink-split 的分层 —— 直接删掉旧断言就是把判据改松了）
- `tools/r32check.py` ✅ 42 条 / `tools/r36check.py` ✅ / `tools/hardbreaks.py` 34 ok，
  6 条 MISSING 仍是成分辐射图 PNG 里的文字，误报
- **桌面 1440 矩形多重集 + body 总高**（基线 `tools/snap/r37`，本轮 `tools/snap/r38`）：
  9 页 0 处矩形消失、body 高不变；三页有变化且都可解释 ——
  how-gumi-works **+5**（两个 `.gb-ink-halo` 副本）、reviews **+9**（expert 导航，桌面隐藏）、
  get-in-touch **1 换 1**（`<a>` 的宽度随文字范围变）、pdp **body 8192.7 → 7834.7**
  （删掉两块板都隐藏的 testimonial，−358 = 308 + 48）
- `tools/pagefit.py`：referral −42 → −26、how-gumi-works −476 → −428、shipping +546 → +532。
  ⚠ **pdp 从 −1509 变成 −2157 是对的**：原来的「接近」是两个错误在互相抵消 —— 评论 app 空槽
  少 1800，而多出来的三条 testimonial 又补回 749。逐块看，`.gb-reviews` 从超出 749 变成超出 47。

### 遗留

11 条判定为**桌面稿与手机稿冲突**或**稿自身的 WIP 痕迹**，一条没改，全部列进
`PROJECT-STATUS.md`「第三十七轮新增的待决事项」A~D 四组。要点：

- **六处文案两块板不一样**，实现一律取的桌面版（PDP promo 卡、science compare 引导句、
  FAQ 页 CTA 整块、referral 按钮、referral `Sign in`、reviews 页 FAQ 标题）。其中
  **referral 的 `Send Message` 大概率是复制未改**（同一块里就写着「Already have an
  account? Sign in」，桌面那句还和 get-in-touch 的按钮一字不差），建议改成 `Sign up`；
  **FAQ 页那处还有副作用** —— `Start Your Greens` 在手机 270 宽的按钮里折成两行。
- **两处占位数量不一样**：产品图缩略图手机 6 / 桌面 5（实现 5，补到 6 要连 `gallery` 的
  `slides.length` 一起改，否则桌面能滑到一张看不见的第六张）、FAQ 手风琴手机 8 / 桌面 6。
- **`.gb-vs__row` 每行多 2px**：稿是 12 + 0 高的 Line + 12 = 24，实现是 12 + 1 + 13 = 26。
  两块板都是 24，桌面同样偏，改了会动桌面，未改。
- **Reviews 专家卡轮播的初始位置**：稿画的是第二张居中，实现从第一张开始，没启用
  `data-slider-centre`。

### 文件清单

```
改  assets/customstyle.scss    新增 $c-gray-050；
                               page-hero__overline svg 补 color；
                               promo-card__body / --white stack / __main 的 narrow+tablet gap；
                               vs__table narrow 补 width:100%；
                               science-card--nutrient 新增 __body gap + __value 补 ink-outline(7px)；
                               ingredients__body > * + * 的 narrow margin-top；
                               新增 .gb-expert__nav；
                               dosed__title 改 ink-split；dosed__text / dosed__block 的 gap；
                               cta-band__plate padding-block / cta-band__content min-height+space-between；
                               form__disclaimer narrow+tablet；
                               rich-table narrow 全边框 + 表头/斑马底色 + 9.5/12 内边距；
                               $build → 20260826-r38
改  assets/customstyle.css     编译产物
改  pdp.html                   删掉三条 testimonial（两块板都 visible:false）
改  reviews.html               expert 接 slider（inner + track）+ 补两个导航按钮
改  how-gumi-works.html        两处 dosed__title 加 .gb-ink-halo 副本
改  get-in-touch.html          同意行的 <a> 缩到只包 privacy policy
改  全部 11 页 + font-check.html   ?v= / EXPECT_BUILD → r38
改  tools/pagescan.py          重写：--list 两侧块排序打印 / --pairs 显式锚点批量出图
改  tools/r31check.py          dosed__title 的描边断言改判 .gb-ink-halo（52 条）
改  docs/CHANGELOG.md          本条
改  docs/PROJECT-STATUS.md     第三十七轮待决事项 A~D
```

---

## 2026-08-27 第三十八轮：任务文档 8 项（响应式为主）+ 全站条件换行粘连（`$build` = `20260827-r39`）

需求方换了一份 8 条的清单，重心从「390 逐像素」转到**响应式行为**：三条是断点区间的
决策反转（箭头该从 1024 出现、footer 链接列该一直靠右、testimonial 该跟卡片一样 3→2→1），
一条是真 bug（手机端 logo 重叠），其余是 footer 一族的间距。8 条全部落地。

顺带在 1024 的对稿图上撞见一个**桌面端一直存在、11 页共 24 处**的文字粘连，一并修了。

### 0. 先说那处粘连：`gb-br-narrow` 隐藏之后，两个词贴在了一起

第三十六轮补了 18 处硬换行，写法是 `word<br class="gb-br-narrow">word`。这个 br 在 768 以上
是 `display:none`，**而 HTML 里两侧没有空白**，于是桌面渲染成：

```
Made with more care than avitamin gummy probably needs.That's on purpose.
Greenbenefits
Nutrition that fitsin your pocket
```

11 页全中（footer tagline 每页 2 处），390 下看不出来 —— br 显形时本来就该换行。
`tools/hardbreaks.py` 也看不出来：它只验「narrow 下断了没有」，没验「不断的时候接不接得上」。

修法是在 br 前补一个空格：narrow 下它落在行尾、被 CSS 折叠，不影响那一行的居中
（[[figma-centred-text-counts-trailing-space]] 说的是稿里的尾随空格，与此相反）；768 以上 br
消失，空格留下来把两个词分开。

判据放进 `r39check` 时**先写错了一版**：拿渲染出来的 innerText 找 `[a-z][A-Z]|[.,][A-Za-z]`
—— 这抓得到 `needs.That`，抓不到 `avitamin` / `Greenbenefits`，全小写的粘连和一个普通长单词
在文本层没有区别。改成在**源码**上查 `\w<br class="gb-br-(narrow|wide)">\w`，两侧写的是什么
markup 说了算。造一处粘连自检，立刻变红。

### 1. 四条箭头改成从 1024 起就出现（第 1 条，决策反转）

第三十五轮把它们放进 narrow、并在 `@include stack` 里显式 `display:none`，理由记在注释里：
「768–1024 跑手机两列网格但列宽接近桌面，熊槽固定 208，箭头挂在熊上会离它指的文案很远，
而没有任何一块稿覆盖这个区间」。需求方看过之后要求 1024 以下都要有。

做法是把整组 narrow 规则（`display` + 描边 + 四条 `matrix`/`left`/`top`/`width`）平移到
`@include stack`。**几何不用重算**：这些百分比锚的是熊槽，而熊槽在整个 stack 档都是同一个
208 × 257.42 的盒（`width: 208px` + `aspect-ratio: 303/375`），列宽变宽只是让箭头两侧的空当变大。
`r39check` 对 390 / 768 / 1024 三档都验了槽尺寸和「每条箭头的中心仍落在熊槽的一个身位内」。

连带 `.gb-stats__bear` 的上下留白也要跟着搬到 stack —— 箭头就挂在那两段空白里，
768–1024 原来是 `margin: 0 auto`，不搬的话箭头会压进相邻的网格行。

### 2. `.gb-nutrition__cards` 两列时，落单的第三张要居中（第 2 条）

grid 没有「最后一行居中」这回事。用**四轨、每张跨两轨**代替 `repeat(2, 1fr)`：
跨两轨的卡宽 `2c + g = (100% − g) / 2`，与两列写法**逐像素相同**，而多出来的半轨给落单的
那张当左右余量，`:last-child:nth-child(odd)` 落在 `grid-column: 2 / span 2` 上正好居中。

`.gb-science__cards` 是同构的（注释里就写着「same reasoning」），但需求方只点了 nutrition，
**没动**。science 那边卡数不同，落单的情况要单独看。

### 3. `.gb-testimonials` 改成 3 → 2 → 1（第 3 条）

原来是 `flex-wrap` + `@include stack { flex-direction: column }`，即 >1024 一行、≤1024 一列，
中间没有两列这一档。改成与 `.gb-nutrition__cards` 同一条阶梯：pc 三列 / tablet 两列 / narrow 一列，
`stack` 那条 column 改挂在 `narrow` 上。

**桌面因此变了，而且是变对**。`flex: 1 1 300px` 让四张卡挤进同一行（4 × 300 + 3 × 24 = 1272 < 1280），
每张压到 302；桌面稿 `I324:69755;313:11103` 是一条 **212 高的单行，1280 = 3 × 411 + 2 × 24**。
把 basis 提到 **340px** 之后，四张的第四张换行、三张的仍是一行 —— 340 不是宽度而是**换行阈值**：
pc 档的行宽在 1121（1281 处）到 1281（`max-width: 1441` 减两侧 80）之间，basis 只要
> 302.25 就能把四张拆成两行、≤ 357.67 就能让三张留在一行，`flex-grow` 随后把每张拉回
410.67 —— **和 300px 时算出来的完全一样**，所以 index 这类三张卡的页面渲染逐位不变。

⚠ 一开始写的是 `calc((100% - var(--gb-testi-gap) * 2) / 3)`。它表达得更清楚，但浏览器把百分比
夹成 `33.3333%`，算出来 410.656 而不是 410.672 —— 0.016px，够在往后每一次快照 diff 里留一行噪声。
tablet 的两列仍用 calc（那一档没有不变量基线要守）。

两列档的卡宽是 `min(411, (行宽 − gap) / 2)`：411 是稿的卡宽、留作 `max-width`，1024 处
(864 − 24) / 2 = 420 比它宽，所以卡停在 411、多出来的由 `justify-content: center` 平分。

### 4. `.gb-footer__link-groups` 1280 以下也靠右（第 4 条，决策反转）

基础规则本来就是 `flex-end`，`@include stack` 把它翻成 `flex-start`，注释写的是
「1024 以下 `.gb-footer__middle` 换行、这一块独占一行，flex-end 会把它推到右边、左边留个
约 260 的洞」。需求方要靠右，所以**删掉那条覆盖**（不是新增规则）——1024–1280 本来就走基础规则，
删掉之后 1280 以下全档一致。回退方法写在原处的注释里。

`r31check` 那条 `@900 = flex-start` 的断言改成 `flex-end` 并注明是本轮反转的，没有删断言。

### 5. 手机端三个 logo 互相压住（第 5 条，真 bug）

第三十五轮按需求方给的数把 `.gb-logo-scroll__item` 收成 106 × 44，但 `.gb-logo-scroll__img`
仍是「各自的墨迹高度 + `width: auto`」（34 / 36 / 40，桌面稿量的）。ABC 那张的墨迹是 166 × 34，
高度给 34 时宽度就是 166，**比槽宽出 60，而槽间的缝只有 30** —— 实测相邻两张重叠 **23.95px**，
最宽的一张溢出槽 54px。

按需求方说的「不需要每个图片单独设置高度，统一 106 × 44」落，另加 `object-fit: contain`：
三张的墨迹比例是 4.88 / 4.39 / 3.58，直接拉满 106 × 44 会各自变形。contain 之后三张都是
106 宽、各保各的高、共享中线（和桌面的做法一致）。修前修后各截一张图存在 `tools/shots/`。

### 6. stats 的三处数值（第 6 条）

`.gb-stats__bear-img` narrow `left: -39.2%`（原 -46.2%，桌面值）—— 镜像之后画面要往右挪
7% × 208 = 14.6px 才回到槽中央；`.gb-stats__bear` 的留白 65/63 → **78/48**（需求方重新量的，
总量紧 2px，而且把空当往上挪）；`.gb-stat--fibre` narrow `margin-top: 24px`，网格是
`align-items: start`，只动 6g 这一列。

网格高度随之 845.4 → **843.4**（板 845.34），`r36check` 里那条基线连同 bear margin 一起更新。

### 7 & 8. footer 一族（第 7、8 条）

需求方给的这一批**几乎全部能在手机板上找到出处**，落之前逐条核过：

| 项 | 需求方 | 板 | 落地 |
|---|---|---|---|
| `.gb-footer-cta` padding | 52 / 78 | `236:11720` 是 **64 / 64** | 52 = 64 − 12（小波浪超出量，见遗留），78 照给的 |
| `.gb-footer-cta__title` margin-bottom | 32 | `236:11722` itemSpacing **32** ✅ | 原来的 23 是桌面值，手机档从来没写过 |
| `.gb-footer` padding-top | 52 | `187:3984` paddingTop **64** | 同上，64 − 12 |
| `.gb-footer` padding-bottom | 24 | `187:3984` paddingBottom **48** | ⚠ 与板冲突，照给的落，记进 PROJECT-STATUS |
| `.gb-footer__middle` gap | 48 | 板顶层 itemSpacing **48** ✅ | 原 32 |
| `newsletter` / `social` / `bottom` margin-top | 16 | — | `.gb-footer__inner` 的 32 + 16 = 板的 **48** |
| `.gb-footer__link-group` gap | 12 | `187:4014` itemSpacing **12** ✅ | 板的手机链接列没有小标题，所以 `187:4012` 的 16 挂在独子上、从不渲染 |
| `.gb-deco-bear--b` top | 457 | — | 原 472 |

改完在 390 量 footer 的五个块，**四个逐像素对上板**：brand 139.00 / 139.04、newsletter
140 / 140、social 68 / 68、bottom 89 / 89，四个块间距全是 **48.00**。第五个见遗留。

**`.gb-deco-bear--b` 的 right 按需求方的想法改成百分比**（28 / 390 = 7.18%，和 `--a` 的 11%
与基础的 3.41% 一致）。**top 没改成百分比**，理由写在注释里：它解析的是 `.gb-footer-cta-wrap`
的高度，而那是 CTA 文案块的高度、不是设计常量 —— 文案多一行、或者换上比试用宽 4.7% 的授权
PP Palma，百分比定位的熊就会跟着往下滑。

tablet 斜坡按公约补齐（CTA padding / title margin / footer padding / link-group gap /
social + bottom 的 margin-top），767 与 768 逐属性连续。**`.gb-footer__newsletter` 的
margin-top 例外，只给 narrow**：768 以上 `.gb-footer__middle` 是换行的 ROW，那个 margin 会把
newsletter 压到旁边的链接列下面 16px，而不是撑开它上方的间距。

### 判据

- `tools/r39check.py`（新）：8 条任务 + 粘连，跨 **390 / 768 / 1024 / 1280 / 1440** 五档，
  每条反转都配一条「桌面必须没变」的反向断言。三条断言先写错、被真实数据纠正后才通过
  （桌面 logo 的 computed width 不是 `auto`；两列卡宽被 `max-width: 411` 截住；
  `.gb-footer__inner` 要取内容区右缘而不是边框盒）。
- **桌面 1440 快照**（`tools/snap/r38` → `r39`，本轮没动 DOM 结构，路径式 diff 可用）：
  **8 页零差异**；index 29 处 = 3 处 `flex-basis` 声明（渲染逐位相同）+ 26 处补空格后文字变宽
  （`Green benefits` +6.7、`Nutrition that fits in your pocket` +11.1，**中心 x 都不变**，
  没有折行或高度变化）；our-story / how-gumi-works 各 ~355 处 = testimonial 由
  4 × 302 一行改成 3 × 410.7 + 1 × 411 两行（对上桌面板的 1280 = 3 × 411 + 2 × 24），
  区块 +210，其下所有元素纯下移 210。
- `tools/rwd.py` 12 页 × 14 档 ✅ 全绿；`revealcheck.py` ✅ 全部 opacity=1、transform 归位
- `r31check` 52 条 ✅（footer 那条基线本轮反转）/ `r32check` 42 条 ✅ / `r36check` ✅
  （bear margin 基线本轮更新）
- `hardbreaks.py` 34 ok / 6 MISSING —— 与上轮同数，6 条仍是成分辐射图 PNG **图片内**的文字
- 对稿图 `tools/shots/scanr39-index-*`：stats 两段、CTA、footer 两段
- 负向断言的活性都验过：logo 不重叠（旧规则下重叠 23.95px 会报红）、
  条件 br 不粘连（造一处立刻报红）

### 遗留

- **footer 链接区是本轮唯一没对上板的块**：板 `187:4010` 是 **两列、无小标题、13 个链接**
  （159 宽，6 + 7 条，columns 之间 32），实现是 **三组带小标题（Why Gumi / Learn more /
  Get in touch）、每组 4 条**，narrow 下排成 2 × 2 网格 —— 328 高对板的 212，**多 116**，
  下面的 Follow us 与版权行跟着整体下移。桌面板的链接列同样是分组的，所以这是
  **两块板之间的结构分歧**，改成两列会丢掉分组语义。已记进 PROJECT-STATUS 待决。
- **`.gb-footer` padding-bottom 24 与板的 48 冲突**（需求方给的数），同上。
- **768–1024 这一档仍然没有任何设计稿**。本轮往这一档加了两样东西（四条箭头、两列
  testimonial），都是从 390 的几何外推的。
- **`.gb-stat--fibre` 的 24px 只给了 narrow**：768–1024 同样是两列网格，理应同步，但 tablet
  mixin 覆盖到 1280、而 1025–1280 是绝对定位布局（margin-top 会真的把它挪位），要单独写
  `(min-width:768px) and (max-width:1024px)` 才安全。本轮按需求方的字面「手机端」只落 narrow。
- **小波浪在手机端仍高 12px**（`--sc-band` clamp 下界，第三十五轮起的常驻项）。本轮又有
  两处 padding 靠它换算（CTA 的 52、footer 的 52），波浪修好后这两个数要跟着回到板的 64。
- `.gb-science__cards` 没跟着做「落单居中」，需求方只点了 nutrition。

### 文件清单

```
改  assets/customstyle.scss    stats__arrow narrow→stack（display/描边/四条 matrix）；
                               stats__bear 留白 78/48 并入 stack 块；
                               stats__bear-img narrow left -39.2%；stat--fibre narrow margin-top；
                               logo-scroll__img narrow 106x44 + object-fit:contain；
                               nutrition__cards tablet 改四轨跨二 + 落单居中；
                               testimonials 新增 --gb-testi-gap，stack→narrow 的 column；
                               testimonial basis 300→340 + tablet 两列 basis；
                               footer__link-groups 删掉 stack 的 flex-start；
                               footer-cta padding / title margin-bottom（narrow+tablet）；
                               footer padding（narrow+tablet）；deco-bear--b top 457 + right 7.18%；
                               footer__middle gap 48；newsletter margin-top（仅 narrow）；
                               footer__link-group gap 12；social / bottom margin-top（narrow+tablet）；
                               $build → 20260827-r39
改  assets/customstyle.css     编译产物
改  全部 11 页 + font-check.html   条件 <br> 前补空格（共 24 处）；?v= / EXPECT_BUILD → r39
新  tools/r39check.py          本轮 8 条 + 粘连的定向断言，五档
改  tools/r31check.py          footer__link-groups @900 基线 flex-start → flex-end
改  tools/r36check.py          bear margin 基线 65/63 → 78/48
改  docs/CHANGELOG.md          本条
改  docs/PROJECT-STATUS.md     进度行 + 第三十八轮新增待决事项
```

---

## 2026-08-27 第三十九轮：任务文档 5 项（手机菜单改版 + PDP 手机值）（`$build` = `20260827-r40`）

需求方给了 5 条。第 1 条是**交互改版**（手机菜单参考 funkyfood 重做），其余是数值。
5 条全部落地。过程中查出两个既有 bug：**promo 卡的扇贝一直被 reset 压小 30%**（第 5 条
带出来的），以及 **font-check 有两条断言从第十九轮起就恒假**（见遗留）。

### 1. 手机菜单：从「挂在 bar 下面的抽屉」改成「盖住整个视口的面板」

需求方点名参考 funkyfood 的出现方式与曲线。去 `funkyfood2-git-newflow` 翻了
`custom-style.scss` 的 `.header-mobile-menu`：`position:fixed; top:0`、`left:-100vw → 0`、
`transition: all 0.7s cubic-bezier(0.77, 0, 0.175, 1)`，面板自带 close 与 logo。

Gumi 自己也有这张稿 —— **`283:14915` Nav Expanded**，之前没被用上：

| | 稿 | 实现前 | 实现后 |
|---|---|---|---|
| 面板起点 | 视口顶（盖住公告条 + bar） | `top:100%`，挂在 bar 下 | `position:fixed; top:0` |
| 高度 | 1050（内容撑满可用高） | `var(--drawer-h)` 实测 | `100svh` |
| 关闭键 | 面板自带，左 gutter 20 | 无（靠 bar 上的 toggle） | `.gb-header__panel-close` |
| logo | 面板自带，居中 92.88×24 | 无 | `.gb-header__panel-logo` 93×24 |
| 曲线 | — | `0.3s` easeOutCubic | `0.7s cubic-bezier(.77,0,.175,1)` |

**位移仍走 `transform`，不是 funkyfood 的 `left`** —— `left` 动画每帧重排，`translateX` 只
合成。曲线与时长照搬。

盖住 bar 之后 toggle 不再可点，所以关闭只剩面板自己那颗按钮，`main.js` 里单独绑定；
`--drawer-h` 连同 `header.measure()` 一起删掉（面板不再需要知道 bar 在哪）。
resize 监听也删了 —— 它唯一的工作就是重新 measure，而手机端 toolbar 收放会触发 resize
（[[mobile-toolbar-resize-rebuild]]），留着反而有误关抽屉的风险。

**锁滚动补了滚动条宽度**（[[project-gumi-brand]] 的常规项）：面板满屏后页面必须锁，
而锁掉 `overflow` 会让视口凭空宽出滚动条那几 px。`header.set()` 现在跟 `modal.open()` 一样，
在锁之前实测 `--scrollbar-w`，`html` 与 `body` 两个都加 `is-menu-open`、两个都补 padding。

### 2. 面板内距：需求方的 9 / 15 正好把 nav 卡片落回稿位

`.gb-header__panel-inner` `padding-top: 24 → 9`、`gap: 32 → 15`。面板顶栏（新增）
给了 `padding: 12px 0`，是从稿反推的：稿的顶栏 64 高、close 图标中心距面板顶 32，
9 + 12 + 24 + 12 = 57，nav 卡片起点 9 + 48 + 15 = **72，与稿的 72 逐像素相同**。

实测 390：close `x=20 y=21`（稿 20/20），logo 中心 195（稿 195.5），卡片 `20,72 350×169`
（稿 20.5,72 350×169）。

### 3. hero 小熊：浮动加回来

第八轮加过（参考 cravburgers.shop，`y -15px / 2.5s each way / sine.inOut`），
第十七轮去掉，第三十三轮又把入场砍成纯淡入。需求方知道这段来回，本轮明确要加回。

写成**两条独立动画**而不是一套 keyframes：

```scss
.gb-float-art--hero {
  animation:
    gm-art-fade-in 0.7s #{$ease-out} 0.2s both,
    gm-art-float 5s var(--e-sine-io) 0.9s infinite;
  animation-composition: replace, add;
}
```

这样第三十三轮那条 LCP 注记仍然成立 —— 熊是首页 LCP 元素（399,727 px²），
opacity 在 0.9s 落定，浮动跑多久都不影响。浮动的起点就接在淡入的终点。

`--still`（只淡入）留着没删，现在没有用户，是需求再反转时的回头路。

实测 travel 15.00px、5s 循环；熊自己的 `rotate(7.92deg)` 没被吃掉（浮动挂在包裹 div 上）；
`prefers-reduced-motion` 下退回纯 `gm-fade-in`。

### 4. 成分表还原手机稿：一个等比缩放，外加一个**不能**等比缩放的例外

需求方给的规格是 `PP Palma / 300 / 9.54px / line-height 100% / letter-spacing 0%`。

两处要按源数据校正：

- **`line-height: 100%` 是 Figma 的 auto**，不是字号的 100%。节点 `336:31184` 自报
  `lineHeightPx = 12.0163`（PP Palma 的自然行距 1.26）。写 `9.54px` 会挤成一团。
  桌面节点同样是 `12.861 → 16.2049`，同一个 1.26，互相印证。
- **`leading-trim: CAP_HEIGHT`** CSS 没有等价物（`text-box-trim` 支持面还不够）。
  它解释了为什么稿里单行文本的 box 高只有 7 而不是 12.02，本身不用还原。

整表的缩放因子 **0.741529**，由四处独立印证：字号 9.5368/12.861、三条线宽
3/4.0457、1.4305/1.9292、0.4768/0.6431 —— 四个数一致到小数点后六位。padding 与缩进
按这个因子换算。

**唯一不跟这个因子走的是两个数值列。** 手机稿的行 Frame（`336:31186`）是 **427.72 宽、
装在 350 的容器里**，SPACE_BETWEEN 在那个超宽盒子里排，于是数值组落在 **278.95**，
而不是 `350 − 148.77 = 201.23`。照因子缩放桌面的 72/128 会让两列都偏左约 77px。
按板量出来是 52.33 + 18.72：实测 "15 g" 起于 278.95、"5%" 起于 331.28，与板同值。

`.gb-nl-pane--info` gap 20 → 24（需求方给的）。

### 5. PDP 手机值 —— 顺带修了一个一直存在的扇贝 bug

13 个数值照做（清单见文件列表）。其中 `.gb-promo-card__lip--h` 改百分比时撞出了真问题：

> reset 里有 `img, svg, video, canvas { max-width: 100% }`。lip 是 `<svg>`，
> **`width: 143%` 被压回 100%** —— 而它原来的 `width: 492px` 同样被压回了卡片的 343。

也就是说这道扇贝**从来没有按设计尺寸画过**。判据在板上量（`324:53792`，图片与卡片的接缝）：

| | 弧数 | 节距 |
|---|---|---|
| 板 | 5 | 69.0 / 68.0 / 69.0 / 68.0 |
| 压制版（143% → 100%） | — | 弧小到扫不出，节距 47.5 |
| 放开版（`max-width: none`） | 5 | 68.0 / 68.0 / 68.0 / 67.5 |

加了 `max-width: none`，高度改由 `aspect-ratio: 492/81` 跟着 viewBox 走，不再写死 81。

`.gb-app-slot` 只从 **pdp.html** 删（那条需求整条都是 PDP 的选择器）。
**reviews.html 上还有一个**，那是该页的主体内容区，没动 —— 见遗留。

### 判据

`tools/r40check.py`，390 / 768 / 1024 / 1440 四档。抽屉那条是**真的点开再点关**：
点 toggle → 等 0.7s → 量几何 + 命中测试 → 点面板自己的关闭键 → 验状态与锁都回到原样。

每条手机改动都配一条「桌面必须没变」的反向断言。三条负向断言做了活性自检：

| 断言 | 破坏方式 | 结果 |
|---|---|---|
| 图标被面板盖住 | 把面板改回 `position:absolute` | 报 `BAR`，红 |
| app-slot 已删 | 把 div 加回 pdp | 报 `got 1`，红 |
| lip 没被 reset 压制 | `max-width` 改回 `100%` | 报 `100%` + 宽度 100，红 |

**桌面 1440 快照 r39 → r40**：

- 10 页 + font-check：header 子树之外**零新增、零值变化**
- header 子树内 171 处「只在 r40」，全部是新增的面板顶栏（手机才 `display:block`）及其
  后代 —— 桌面 `display:none`，各页 body 高度一字未变即为证
- pdp 139 处值变化：**133 个元素纯下移 240、4 个容器高度 −240**（删掉的 app-slot 占位框
  正是 `min-height: 240px`），另 2 个是 lip 的声明变化且 `#rect` 完全不动（桌面不画它）
- 没有任何宽度变化或水平位移

断点边界 767 / 768 单独验过：767 是 fixed 全屏 + 锁定 + 0.7s，768 是 absolute dropdown +
不锁 + 0.35s。抽屉开着 resize 到 1100 会自动退回 dropdown 并解锁，页面可滚，不会卡死。

既有脚本：`r31check` 52 条、`r32check` 42 条、`r36check`、`r39check` 全过；
`rwd.py` 12×14 全绿；`revealcheck` OK；`hardbreaks` 34 ok / 6 MISSING（与上轮同数，
是图片内文字的既有误报）。`font-check.html` 版本三处一致，字重四个文件全部命中。

对稿图在 `tools/shots/`：`r40-drawer-open.png`、`r40-nl-390.png`、`r40-lip-capped|uncapped.png`、
`r40-pdp-promo|vs|product.png`。

### 遗留

- **`font-check.html` 有两条断言从第十九轮起就恒假**：「波浪归属：section 自带下边缘形状」
  与「裁切型宿主也不用特例：占位块在 padding box 内」，两条都在探 `.gb-product::after`
  占位块。第十九轮把占位方案从 `::after` 换成了 `padding-bottom: calc(… + var(--sc-h))`，
  `::after` 随之不存在，`content` 现在是 `none`。**不是本轮引入的**（本轮只给
  `.gb-product--page` 加了 padding-top）。一个恒假的断言和恒真的一样有害，等价的新判据
  是「padding-bottom 里含 `var(--sc-lg-h)`」，五行就能改写 —— 但与本轮任务无关，未动。
- **reviews.html 还留着一个 `.gb-app-slot`**：需求那条整段都是 PDP 的选择器，而 reviews
  页那个 slot 是整页的主体（评论 app 挂载点），删掉页面会空一大块。等需求方确认。
- **`.gb-header__panel-bar` 的 12px 上下内距是反推值**，不是板上的直读数：板把 64 全给了
  顶栏，而需求方把 9 给了 `panel-inner`。9 + 12 + 24 + 12 = 57 ≠ 64，差的 7 落在卡片
  上方的 gap 里（板 8，需求方给 15）。结果 nav 卡片起点仍是板的 72，所以没有再往回调。
- **手机稿里两个折叠组是展开的**（Learn more / Get in Touch 的子项都露着），实现是收起
  可点开。那是稿的展示态，未改。收起状态下面板底部会空出一段，与稿的「刚好填满」不同。
- **`.gb-promo-card__list` 的 `margin-right: 15px` 会让它靠右**，不是「居中后左移 15」——
  base 是 `margin: 0 auto`，右边固定之后左边的 auto 吃掉全部余量。实测 390 下左 24.39 /
  右 15。按需求方给的字面落的，视觉上是略偏左于版心，看着合理。
- **768–1024 仍无设计稿**（沿用上轮说明）。本轮给这一档的所有值都是 390 → 1281 的
  `fluid()` 斜坡，不是稿。
- **小波浪手机端仍高 12px**（常驻项）。本轮 `.gb-vs` 与 `.gb-faq` 的 52 又是靠它换算的。

### 文件清单

```
改  assets/customstyle.scss    新增 $t-drawer / $ease-drawer；
                               header__panel narrow 改 fixed 全屏 + 0.7s 曲线 + overscroll;
                               新增 header__panel-bar / __panel-close / __panel-logo；
                               header__panel-inner narrow padding-top 9 / gap 15；
                               is-menu-open 锁加 html + --scrollbar-w 补偿；
                               新增 .gb-float-art--hero（淡入 + 浮动），--still 留作回头路；
                               nl-pane--info gap 24；nl-table 整表 narrow/tablet 档
                                 （9.54/12.02、线宽 3/1.43/0.48、padding 5.19、列 52.33+18.72）；
                               nl-table__sub 8.16；nl-notes 9.71/12.61/5.93；
                               product--page padding-top 20；product__image radius 16；
                               promo-card__lip--h 改百分比 + max-width:none + aspect-ratio；
                               promo-art__img narrow top -8%；promo-card__list margin-right 15；
                               promo-card__list-item svg 20；reviews__disclaimer margin-top 2；
                               vs padding-top 52；vs__row 规则间距 11；vs__value padding-right 15；
                               vs__others top 46.25；faq padding 52/80；
                               $build → 20260827-r40
改  assets/customstyle.css     编译产物
改  assets/main.js             header：绑定面板关闭键；删 measure() 与 --drawer-h；
                               删 resize 监听；set() 测 --scrollbar-w 并锁 html + body
改  全部 11 页                 panel-inner 内新增 .gb-header__panel-bar（close + logo）；?v= → r40
改  index.html                 hero 熊 .gb-float-art--still → --hero
改  pdp.html                   删 .gb-app-slot 占位框
改  font-check.html            EXPECT_BUILD → r40；hero 熊断言基线改为 fade + float
新  tools/r40check.py          本轮 5 条的定向断言，四档，抽屉真开真关
新  tools/snap/r40  r40m       1440 与 390 两档快照（下一轮的基线）
改  docs/CHANGELOG.md          本条
改  docs/PROJECT-STATUS.md     进度行 + 第三十九轮新增待决事项
```

---

## 2026-08-27 第四十轮：任务文档第二组 3 项（1280 以下的响应式）（`$build` = `20260827-r41`）

需求方追加了 3 条，全部指向 **768–1280 这个没有设计稿的带宽**。三条都是真问题，
其中 `.gb-page-hero` 那条实测比描述更严重：**图片在 1024 处只剩 119.8 × 90.3**，
基本消失了。

### 1. page hero:两根柱子都是刚性的,只是刚性的方向相反

需求方说「1280 以下过于拥挤」「`__media` 不应该固定宽度」。实测下来是同一处写法在
断点两侧各犯一次错:

| 视口 | `__text` | `__media` | 标题行数 |
|---|---|---|---|
| 1440 | 566 | 570 | 3（稿值） |
| 1280 | 406 | **570** | 5 |
| 1200 | 326 | **570** | 5 |
| 1100 | **243.8** | **570** | **6** |
| 1024 | 756.4 | **119.8**（高 90.3） | 3 |

- **1025–1440**:`media` 是 `flex: 0 0 570px`,**完全不可压缩**,于是所有的短缺全由
  text 承担 —— 1100 处 text 只剩 243.8,标题排成 6 行。
- **≤1024**:`media` 翻成 `flex: 1 1 0`,basis 变 0,而 text 是 `flex: 1 1 auto`
  （basis = 内容宽 ≈ 741）。basis 先把空间分完,media 只捡到零头,**图片塌成 119.8**。

改成**一对共享的可伸缩 basis**,比例就取稿的 566 : 570:

```scss
.gb-page-hero__text  { flex: 1 1 566px; min-width: 0; }
.gb-page-hero__media { flex: 1 1 570px; }
```

1440 处 `566 + 84 + 570 = 1220` 正好等于内容盒,grow / shrink 都无空间可分,**稿值一字不动**;
更窄时两栏按同一比例让步。两处 `width` 一并删掉 —— 宽度和可伸缩的 basis 写在一起,
正是当初把它写死的原因。

同时把 `gap` 与 `padding-inline` 的交接点从 `stack`(1024) 移到 `tablet`(768–1280) 的斜坡:
旧写法在 1025 处把 gutter 从 110 直接摔到 49.9(跳 60),而 1025–1280 整段仍按桌面的
110 + 84 吃掉 194px 的横向空间 —— 那正是需求方说的拥挤带。新斜坡在 768 接上手机值、
在 1281 接上稿值,两个边界都不跳。

改后:1100 标题回到 **3 行**,1024 的图片回到 **436.6**。

> ⚠ 中途踩了一脚:`.gb-page-hero__inner` 在 narrow 是 **`column-reverse`**,主轴是纵向,
> 于是 `flex: 1 1 566px` 的 566 被当成**高度**基准,science / reviews 的 hero 凭空高了
> ~390px。手机快照一比就露出来了(387 / 700 处元素全部下移)。narrow 档补 `flex: none`
> ——`__media` 早就为同一个理由写了这一句。

### 2. `.gb-science__cards`:落单的第三张要居中

第三十八轮给 `.gb-nutrition__cards` 做过,当时需求方只点了 nutrition,science 留在遗留里;
这轮补上,用的是同一个装置 —— **四轨、每张跨两轨**。跨两轨的宽 `2c + g = (100% − g) / 2`
与 `repeat(2, 1fr)` 逐像素相同,多出的半轨给落单那张当余量:

```scss
> * { grid-column: span 2; }
> :last-child:nth-child(odd) { grid-column: 2 / span 2; }
```

全站三个 `.gb-science__cards`(science 两个、index 一个)都正好 3 张卡。

### 3. 三个两栏区块:两列撑到 991,不是 1024

`flex-direction: column` 从 `stack`(≤1024) 移到 `mid`(≤991),涉及 `.gb-compare__inner` /
`.gb-ingredients__inner` / `.gb-faq-image__inner`。

⚠ **同组的配套规则必须一起搬**,否则 992–1024 会拿到堆叠态的规则去排一个 row。
`.gb-compare__heading` / `__panel` / `.gb-ingredients__body` / `.gb-faq-image__body` /
`.gb-ingredients__disc` / `.gb-faq-image__media` 的 `@include stack` 全部跟到 `mid`。
`padding-inline` 留在 `tight`(1200) 没动 —— 版心内距和堆叠是两件事。

两个正方形图块(`__disc` / `__media`)按需求方「不应该固定宽」去掉了
`flex: 0 0 520px` + `width: 520px`,改成 `flex: 0 1 520px`。

> ⚠ 但**堆叠时的 `max-width: 520px` 必须留着**。第一版把它一并删了,结果 991 处
> 正方形撑满版心变成 **898 × 898** 的巨图 —— 那是回归,不是需求。需求方说的「固定宽」
> 指的是 row 里那个不可压缩的 basis(它会饿死另一栏),不是堆叠后的上限。
> `.gb-compare__heading` / `__panel` 的 `max-width: 560px` 则是需求方**点名要去掉**的,
> 已去掉,堆叠后跑满版心(991 处 898.8)。

### 判据

`tools/r41check.py`,**10 个宽度**:1440 / 1280 / 1200 / 1100 / 1024 / 992 / 991 / 900 /
768 / 390,跑 science(三个模块全在这一页)、reviews、index。

因为这一带没有稿,判据取的是**行为**而不是板值:

- 整条带宽上两栏必须**同步让步**:`media / text` 恒等于板的 `570 / 566`(±0.02),
  且 `text + media + gap` 恰好等于内容盒(±1.5) —— 既不留空当也不溢出
- 两个具体回归各自钉死一条:「1100 标题不得再是 6 行」「1024 图片不得再是 119.8」
- 落单卡片的中心必须与网格中心重合(±1),外加一条「它确实离开了左边缘」——
  否则「居中」在两列变一列时会假通过

四条关键断言都做了活性自检:

| 断言 | 破坏方式 | 结果 |
|---|---|---|
| 图片不塌 | media 改回 `flex: 1 1 0` | 1280→900 每档报红,媒体宽 235→111 |
| 落单居中 | `:last-child:nth-child(odd)` 退回普通 `span 2` | 每个两列档报红,第三张贴回左边缘 |
| 方形留上限 | 去掉 `max-width: 520px` | 991/900 报 898.84 |
| 两列撑到 991 | 阈值改回 1024 | 992/1024 报 `column`,共 7 条 |

> 第一次破坏「落单居中」时只改了 `> * { grid-column: span 2 }`,结果**只有 768 报红** ——
> 因为 `:last-child:nth-child(odd)` 那条独立生效,居中仍然成立。换成直接破坏那一条才
> 抓全 32 处。这是个提醒:一条断言能被两条规则中的任一条满足时,活性自检必须破坏**真正
> 负责的那一条**。

**两个不变量档的快照(r40 → r41)**:

- **1440:14 处差异,全部是声明变化,`#rect` 零变化** —— `min-width: auto→0px`、
  `flex-grow/shrink: 0→1`。1440 处 basis 之和正好等于内容宽,所以渲染逐像素不变。
- **390:11 处差异,同样零 `#rect`。** 本轮只动 tablet / mid 两个布局档。

`rwd.py` 12×14 全绿;`r31`(52)/`r32`(42)/`r36`/`r39`/`r40` 全过。

> ⚠ 探针自身的坑:截图脚本的 SETTLE 只写了 `.wowo`,漏了 reveal 那一组,于是
> 行遮罩停在第 0 帧、把标题和 lead 切掉半截 —— 看起来像是本轮改出的溢出。
> 实测 `overflow: visible`、lead 底部离 section 底还有 220px,**页面本身没问题**。
> `r41check.py` 的 SETTLE 已补全(见 memory `kill-animations-blanks-reveal-blocks`)。

### 遗留

- **堆叠阈值的方向与第二十九轮的记录相反**。那一轮的遗留写的是「两栏堆叠阈值仍是 1024,
  **没有按需求方说的推到 1200**」——推到 1200 是**更早**堆叠;这轮要的 991 是**更晚**堆叠。
  两者不能同时成立。本轮按最新的 991 落地,配合去掉宽度上限、放开 basis,992–1024
  的两栏是撑得住的(compare 368.8 / 466.8,ingredients 437.8 / 421.8)。
  **如果 1200 那条仍然有效,请需求方明确哪一条作数。**
- **768–1280 依旧没有设计稿**。本轮所有值都是行为约束(比例、不塌陷),不是板值。
- `.gb-compare__heading` / `__panel` 堆叠后跑满版心,991 处是 898.8 宽的单行标题,
  比 560 时的观感松。这是需求方点名要的,记录备查。
- 上一轮的待决 G / H / I(font-check 两条陈旧断言、reviews 的 app-slot、promo list
  的 margin 语义)本轮未动,仍待需求方裁决。

### 文件清单

```
改  assets/customstyle.scss    page-hero__inner:gap / padding-inline 从 stack 改 tablet 斜坡;
                               page-hero__text:flex 1 1 566px + min-width 0,删 width,
                                 narrow 补 flex:none(column-reverse 下 basis 是高度);
                               page-hero__media:flex 1 1 570px,删 width 与 stack 档;
                               science__cards tablet 改四轨跨二 + 落单居中;
                               compare__inner / ingredients__inner / faq-image__inner:
                                 flex-direction 从 stack 移到 mid;
                               compare__heading / __panel:stack→mid,去掉 max-width 560;
                               ingredients__disc / faq-image__media:flex 0 1 520px、删 width,
                                 stack→mid 并保留 max-width 520;
                               ingredients__body / faq-image__body:stack→mid;
                               $build → 20260827-r41
改  assets/customstyle.css     编译产物
改  全部 11 页 + font-check.html   ?v= / EXPECT_BUILD → r41
新  tools/r41check.py          本轮 3 条的定向断言,10 个宽度,四条活性自检
新  tools/snap/r41  r41m       1440 与 390 两档快照(下一轮的基线)
改  docs/CHANGELOG.md          本条
改  docs/PROJECT-STATUS.md     进度行 + 待决 J(堆叠阈值方向冲突)
```

---

## 2026-08-27 第四十一轮：任务文档第二组第 4 条 + 对话追加 3 项（`$build` = `20260827-r42`）

任务文档第二组的第 4 条上一轮漏了（那轮标题写的「3 项」），本轮补上；对话另追加了
expert 卡片轨道的三条。四条里有两条牵出了比需求本身更要紧的机制问题，都在下面各自那节。

### 1. `.gb-footer__link-groups` 1280 以下改回 flex-start（第二组第 4 条，**第二次反转**）

同一处第三次改动，方向来回：

| 轮次 | 落法 | 谁提的 |
|---|---|---|
| 第二十轮 | `@include stack { justify-content: flex-start }` | 我们（换行后左边空 260 的洞） |
| 第三十八轮 | 删掉那条覆盖，1280 以下全部 flex-end | 需求方点名 |
| **第四十一轮** | 1280 以下回到 flex-start | 需求方点名 |

⚠ **不是简单地把第二十轮那条加回来**：那条挂在 `stack`(≤1024)，而需求方两次说的都是
**1280**。项目的布局阈值到 `tight`(1200) 为止，PROJECT-STATUS「断点体系」里还有一条
明确的 ⚠ ——「布局阈值不要去对齐 767/1280」，第十六轮把 ≤1024/≤1200 全推到 1280
造成过回归。所以这条落在**值档 `tablet`(768–1280)**，上界正好是需求方说的数字：

```scss
@include tablet { justify-content: flex-start; gap: fluid(32px, 24px); }
```

`narrow`(≤767) 不需要配一条：那一档这块是 `grid repeat(2, 1fr)`，两条 1fr 轨道把余量
吃干净，`justify-content` 没有东西可分配（已写成断言，见「判据」）。

### 2. `.gb-expert__cards` 991 以下变轨道 + 无限循环

原来的阶梯是「三列 → 两列(≤991) → 轨道(≤767)」，需求方要 991 以下直接就是轨道，
所以两列那一档整个去掉，`narrow` 那整块 rail 规则升到 `mid`(≤991)。搬动时两处必须跟着改：

- **出血量从写死的 `$pad-x-mobile` 换成 `var(--pad-x)`**。这块原来只在 ≤767 生效，
  那一档 `--pad-x` 恒等于 20，写死没问题；升到 991 之后它跨过了 768，而 768–1280
  的 `--pad-x` 是 `fluid(20px, 80px)` 的斜坡（991 处 46.08）。不换就会左右各差 26px。
- **`.gb-expert__nav`（两颗箭头）也要跟到 `mid`**，否则 768–991 有轨道没箭头。
- 卡片的 `flex: 0 0 305px` + `scroll-snap-align` 跟到 `mid`，而 `padding` / `border-radius`
  这两个**手机稿数值**留在 `narrow` —— 布局阈值只搬排布，数值归值档（铁律 18）。
  305 一路用到 991（那里可见 3.1 张），与上面的三列网格衔接得上，没有跳。

无限循环用的是既有的 `data-slider-loop`（`.gb-reels` 一直在用），HTML 只加这一个属性。
但这是**第一个「只在某个断点以下才是轨道」的 slider**，于是暴露了三个 loop 从没遇到过的问题：

- **克隆会被灌进 grid**。`fill()` 在 `relayout()` 里无条件跑，992 以上这块是三列网格，
  9 个克隆会排成**多出来的三行**。加 `isRail()` 守卫 —— 判据取 `overflowX` 是不是
  `auto|scroll`，**让断点留在 CSS 里，JS 不写死 991**。
- **跨过断点要把克隆收回去**。只是「不再新增」不够：从轨道 resize 回网格时，之前克隆的
  9 张还在 DOM 里。补 `unfill()`。
- **克隆继承了 `.wowo`**。`.gb-expert-card` 每张自己带 `wowo fadeInUp`，而 `fill()`
  发生在 `wowo.init()` 之后。实测下来**不是**「永久不可见」——本项目的 wowo 是
  `scroll` 驱动、每次重新 `querySelectorAll('.wowo:not(.animated)')`，所以克隆会在
  下一次滚动时自己补播一次，效果是副本比旁边的原件晚一拍淡入。克隆时剥掉
  `wowo` / `animated`，副本直接以最终态出场。
  （`.gb-reels` 的 slide 不带 wowo，所以三个既有 loop 都碰不到这条。）

另外补了 `home()`：loop 轨道初始 `scrollLeft` 是 0，也就是第一份拷贝的左缘，
**第一次点「上一张」滑不动**，要等用户先自己滑一次、`wrap()` 跑过才正常。
现在开场就停在第二套（`wrap()` 稳定区间 [0.5, 1.5] 的正中）。
`.gb-reels` 靠 `data-slider-centre` 里的 `target = loop ? setWidth() : …` 已经在做同一件事，
所以那三个不受影响。

### 3. 去掉 `.gb-app-slot`（关闭待决 H）

pdp 那个第三十九轮删了，reviews 这个留着是因为它是评论 app 的挂载点、删了页面会空一块，
当时列为待决 H。需求方本轮点名去掉，照办：删的是那个**虚线占位框**，
`.gb-app-section` 与标题都留着（app 接进来时挂在这一节里）。
`.gb-app-slot` 的两条 scss 规则随之零引用，一并删掉，原位留了三行说明去向。
⚠ `.gb-product__app-slot` 是**另一个类**，四个页面还在用，没动。

### 判据

`tools/r42check.py`：footer 跑 index + faq 共 11 档，expert 轨道跑 reviews 共 9 档，
外加三组跨断点 resize。两条判据设计上的取舍写在文件头：

- **computed 值不能单独当判据**。`justify-content` 在没有余量的行里也读作 `flex-start`，
  所以每档都配一条几何断言，而**没有余量的档位单独报成 vacuous**，不混进「通过」里。
- **克隆可见性不能在 SETTLE 下测**。那张注入表里有 `.wowo{opacity:1!important}`，
  正是要抓的失败本身 —— 第一版就这么写的，破坏 `classList.remove` 之后**全绿**。
  改成 class 检查（`cloneKeptWowo`）+ 一张不注入 SETTLE、也不滚动的 7000 高页面读 opacity。

六条活性自检，报红范围与断言覆盖范围逐条核对：

| 断言 | 破坏方式 | 结果 |
|---|---|---|
| 桌面不被克隆 | 去掉 `isRail()` 守卫 | **先是全绿** —— `relayout()` 里还有一层守卫兜着。两处一起破坏后 4 个网格档全红，12 张卡（3+9） |
| loop 停在第二套 | 去掉 `home()` | 5 档里 4 档红。900 那档被 `wrap()` 的 120ms idle 兜住了 —— 说明 `home()` 消掉的正是这种不确定性 |
| 克隆不带 wowo | 注释掉 `classList.remove` | 5 个轨道档全红（改判据之前是全绿，见上） |
| resize 收回克隆 | 去掉 `unfill()` | 2 个 resize-up 用例全红，12 张 |
| 轨道阈值 991 | 改回 `narrow` | 991/900/768 三档共 27 条红，767/390 仍是轨道 ✓ |
| footer 靠左 | 删掉 tablet 那条覆盖 | tablet 全档红，且报出各档空洞宽度（1280 处 490） |

**不变量档**用 `tools/r42rect.py`（本轮新增）比 r41 / r41m：

`cssnap.py diff` 是**路径键**的，增删一个 DOM 节点会让后面所有兄弟的下标整体错位，
比的是不同元素 —— 而本轮既删了一个节点又加了九个，只能按矩形多重集比（HANDOFF
「桌面绝不能被动到」写的就是这个形状）。cssnap 本身也跑不动：它每个元素采 340 项 × 3
个伪态，在这台机器上被 OOM kill（12 份只写出 2 份）；只采矩形小两个数量级。

- **1440：11 页里 10 页矩形逐个吻合**，reviews 的差异全部可解释 ——
  body / main / `.gb-app-section` / `__inner` 四个容器各矮 288（= 240 占位框 + 48 gap），
  外加 `(80,1992.7,1280,240)` 这一个矩形消失（占位框本体）。把 288 的位移还原后
  没有一个矩形对不上。
- **390：同样 10 页零差异**，reviews 少 228（= 180 + 48），多出 46 个 x 为负的矩形 ——
  克隆卡片被 `home()` 停在视口左外，宽度 305 正是板值。**原件的旧位置全部仍被占用**
  （第二套正好落在第一套原来的位置），也就是说可见画面与 r41 逐像素相同。

回归：`rwd.py` 12×14 全绿、`revealcheck.py` 全绿、`hardbreaks.py` 恒定 34 ok / 6 MISSING、
`r31`(52) / `r32`(42) / `r36` / `r39` / `r40` / `r41` 全过。

### 4. `rwd.py` 的一个判据盲点（本轮触发，顺手补掉）

改完之后 `rwd.py` 报了 7 处「被裁」，全是 `.gb-expert-card`，全在轨道档。查下来是判据自己的洞：
`clipperOf()` 找「最近一个真的会裁的祖先」时跳过 `auto|scroll`，于是一路找到 `body`
（它是 `overflow-x: hidden`），把**横向轨道里待滑入的卡片**判成被 body 裁掉。

r41 之所以没报，是因为那些卡片带着 `.wowo` 停在 `opacity: 0`，被前面的过滤挡掉了；
克隆剥掉 wowo 之后就现形了。**轨道外的卡片是轨道的本意**，补一条豁免：元素与 clipper
之间隔着一个真的能横向滚的祖先就跳过。

⚠ 只认 x 轴。第一版把 y 也算进去，结果把「轨道 `overflow-x` 改 hidden」这个人为破坏
放过了 —— `overflow-x: hidden` 会把另一轴强制算成 `auto`，纵向溢出几像素就被当成
「能滚到」。收紧成只看 x 之后，那次破坏同时报出「被裁」（clipper 正确认成
`div.gb-expert__cards`）与「滚轮黑洞」。全站复跑仍是全绿，说明豁免只吃掉了那 7 条。

### 遗留

- **`r42rect.py` 只比矩形，不比声明**。它是 cssnap 在这台机器上跑不动时的替代，
  抓得住几何回归，抓不住「颜色变了但盒子没动」这类。内存宽松时补一份
  `cssnap.py r42 --widths 1440` / `r42m --widths 390` 存成下一轮基线；
  **在那之前下一轮的基线仍是 r41 / r41m**。
- **`tools/snap/` 已占 799M，磁盘 97%**。HANDOFF 标注 `r38`（547M）可清，本轮没动它。
- **reviews 的 `pagefit` 缺口从 −1942.8 扩大到 −2230.8**，就是本轮删掉的那 288。
  与 index / pdp / our-story / how-gumi-works 那几个 −400 同源，都是「app 产出的内容
  只做壳」这条边界，不是还原度问题。
- 待决 **G / I / J 本轮未动**，仍等需求方裁决。H 已关闭。
- 768–1280 依旧没有设计稿，本轮 expert 轨道在这一带的表现同样是行为约束、不是板值。

### 文件清单

```
改  assets/customstyle.scss    footer__link-groups: tablet 档补 justify-content: flex-start
                                 （注释重写，标明这是第二次反转）;
                               expert__cards: 删两列档, rail 规则 narrow→mid,
                                 出血量 $pad-x-mobile → var(--pad-x), gap 留 narrow;
                               expert__nav: narrow→mid;
                               expert-card: flex/scroll-snap-align → mid, padding/radius 留 narrow;
                               删 .gb-app-slot 两条规则（零引用后）, 原位留去向说明;
                               $build → 20260827-r42
改  assets/customstyle.css     编译产物
改  assets/main.js             slider: 新增 isRail() 守卫 / unfill() / home();
                                 fill() 与 wrap() 加守卫; 克隆剥掉 wowo|animated class
改  reviews.html               gb-expert__inner 加 data-slider-loop; 删 .gb-app-slot 及其注释
改  全部 11 页 + font-check.html   ?v= / EXPECT_BUILD → r42
新  tools/r42check.py          本轮四条的定向断言 + 六条活性自检
新  tools/r42rect.py           矩形多重集比对（cssnap 跑不动时的不变量判据，含位移还原）
改  tools/rwd.py               clipperOf 补横向轨道豁免（只认 x 轴）
改  tools/r31check.py          footer @900 断言 flex-end → flex-start
改  tools/r39check.py          第 4 节整节随反转更新; 探针补 footerInnerContentLeft;
                                 1024 移出几何断言（那一档 middle 还没换行，参照系不同）
改  docs/CHANGELOG.md          本条
改  docs/PROJECT-STATUS.md     待决 H 关闭 + 进度行
改  docs/HANDOFF.md            状态 / 不要报成 bug 的清单 / 验证跑法
改  README.md                  build 号
```

---

## 2026-08-27 第四十二轮：任务文档换版后的第 5–8 条（`$build` = `20260827-r43`）

⚠ **`修改任务文档.txt` 被就地覆写过**（md5 `b90f702c` → `467df0c8`）：上一轮做的那版里
第一组 5 条已经不见，改成 8 条，其中 5/6/7/8 是新的。第八条里需求方自己点名了
「gb-ingredients__inner … **发现没有修改成功**」「gb-compare__inner 也是如此没修改成功」——
指的正是第 5 条那批（我上一轮读到的还是旧版，那时没有这四条）。

### 1. 堆叠阈值 991/1024 → 767（第 5 条 + 第 8 条，**第三次改动**）

| 轮次 | 阈值 | 方向 |
|---|---|---|
| 第二十九轮遗留 | 1024，记录写着「没有按需求方说的推到 1200」 | 更早堆叠 |
| 第四十轮 | 991 | 更晚 |
| **本轮** | **767** | **更晚** |

需求方三次都在往「更晚堆叠、两栏保持更久」推，本轮直接落到值档 `narrow`。涉及
`.gb-compare__inner` / `.gb-ingredients__inner` / `.gb-faq-image__inner` / `.gb-product__inner`。
**待决 J 就此有了确定方向**（第二十九轮那条「推到 1200」彻底作废）。

⚠ **真正咬人的不是阈值本身，是它把两栏推进了一个放不下的带宽**：
`.gb-product__media` 是 `width: 465px` + `flex-shrink: 0`，`__info` 同样写死 465。
两栏 465 + 24 + 465 = 954，而 768 视口的内容盒只有 728 —— **实测横向溢出 163px**
（900 处 47px）。这是第四十轮 `.gb-page-hero`「两根柱子都是刚性的」的同一个病，
按同样的解法改成一对可伸缩 basis：

```scss
.gb-product__media { flex: 0 1 465px; min-width: 0; }
.gb-product__info  { flex: 0 1 465px; min-width: 0; }
```

1440 处 `465 + 24 + 465` 正好填满内容盒，无空可缩，**桌面一字未动**；768 处两栏
各让到 339.4 / 356.6。溢出归零。

⚠ **同组配套规则一起搬**（第四十轮的教训）：`.gb-product__media` / `__gallery` /
`__thumbs` / `__thumb` / `__info` 的 `@include stack` 五处全部跟到 `narrow`，
否则 768–1024 会拿堆叠态的规则去排一个 row。compare / ingredients / faq-image 的
`__heading` / `__panel` / `__body` / `__disc` / `__media` 同理。

**副作用，已实测并接受**：缩略图导轨的绝对定位挂在 `@include pc`，它的旧注释写着
「1280 以下反正都堆叠了」——这个前提本轮被推翻。768–1280 现在两栏并排，导轨落回
基础的竖排、待在 media 盒**内部**，代价是主图从 465 缩到 403（1280 处）。注释已改写。

### 2. 去掉 767 以下的宽度上限（第 5 条）

`.gb-faq-image__media` / `__body` / `.gb-ingredients__disc` / `__body` 四处的
`max-width` 在堆叠档全部去掉。第四十轮我保留过 520 的上限并写进「不要报成 bug」，
需求方本轮点名说那不算改成功，所以这次按字面落。

⚠ **实测后果，需要裁决（待决 M）**：正方形现在跑满容器宽 ——
**390 处 390×390**（此前 350×350，左右各有 20px 版心留白，现在贴边）、
**767 处 767×767**（占满整屏）。`.gb-ingredients__inner` 在 narrow 档是
`padding-inline: 0`（出血由 `__body` 自己补回来的设计），所以去掉上限就等于贴边。
若原意是「不要固定像素、但保留版心」，一行就能改回：inner 的 narrow 档
`padding-inline: var(--pad-x)`，`__body` 的补偿相应去掉。

### 3. 卡片网格 2→1 从 767 下移到 575（第 5 条）

`.gb-science__cards` 与 `.gb-nutrition__cards`（需求说「像 gb-science__cards 这种」，
全站就这两个）。两列的四轨跨二装置从 `tablet` 扩到 `narrow`，单列放进 `mobile`(≤575)。

⚠ **单列档必须重置 `grid-column: span 2`**：对着一条轨道，隐式网格会拿 span 再造出
第二列来，卡片依旧两列排。活性自检里删掉那两行，575 立刻报 2 列。

### 4. 六个手机端数值（第 6 条）

| 选择器 | 改动 | 备注 |
|---|---|---|
| `.gb-science--cream` | 补 `padding-top: 64px` | **覆盖掉 `.gb-science` 自己的 53** —— 那个 53 是板的 64 减去本站波浪多出来的 11 |
| `.gb-science-card__value` | 手机 56/44 → **36/40** | 「由 95→50」= 让 95% 那组用 50% 那组的规格。**推翻板值**（228:5932 写的就是 56/44）。`--nutrient` 的同名覆盖随之删除，两组现在同源 |
| `.gb-science--tight .gb-science__inner` | gap 32 → 48 | |
| `.gb-compare__inner` | 堆叠 gap 32 → 46 | |
| `.gb-promo-art__img` | 手机 top −8% → **−5%** | **反转第四十轮第 5 条**（那轮需求方给的正是 −8%）。现在与基础值同值 |
| `.gb-faq-image` | 手机 `64px 0` → `64px 0 80px` | |

### 5. 数字增长动画（第 7 条）

新模块 `countUp`（`main.js`，IIFE 内第 14 个模块），hook 是 `data-count-up`：

- **标记里带着最终值**，模块只是把它从 0 数上来。JS 关掉、`prefers-reduced-motion`、
  或模块自己抛异常，数字都原样在那里 —— 所以它可以在任何一步早退。
- 元素的 `innerHTML` 原样存下、最后一帧原样放回，**计数不可能留下一个四舍五入的值
  或者把 `<span>` 包裹层吃掉**。
- 计数前把盒子宽度钉死：`0%` 比 `95%` 窄，不钉的话每一帧都在重排卡片。
- 缓动是 easeOutCubic，与 motion token 里的 `$ease-out` 同形；时长 1400ms。
- IntersectionObserver 触发、`unobserve` 之后只播一次。

**挂在哪**：只挂了 `.gb-science-card__value`（9 处：science 6 + index 3），需求点名的就是它。
⚠ **`.gb-stat__value` 没挂**（首页四个大数字 60+/6g/21/10+）：它是 `.gb-ink-halo` 描边
复制层 + 真实内容的**双层结构**，且已经挂着 `data-line-reveal`，两套动画叠在同一个节点上
要先定谁先谁后。**待决 N**。`.gb-vs__value` 是文字不是数字，不适用。

### 6. 轨道每次只滚一张（第 8 条）

- **触摸/惯性**：`.gb-expert-card` 加 `scroll-snap-stop: always`，一次滑动只停到下一张，
  不让动量跨过好几张。这是原生解法，不需要 JS。
- **鼠标拖拽**：走的是 slider 自己的 pointer 处理（触摸根本不进那个分支），
  新增 `[data-slider-step]`，松手时从**拖拽起点**而不是终点走一张 —— 指针可能已经
  拖过三张了，只看终点的话 CSS snap 会就近停在那里。

### 判据

`tools/r43check.py`，四页 × 最多 11 档。两条判据写法上的坑，都是先写错再改对的：

- **「两列」不能用不同的 x 位置个数来数**。三张卡跨两轨、落单那张居中，它与前两张
  谁的 x 都不同 —— 一个正常的两列网格会被数成 3 列。判据换成**行数**（3 张卡：
  三列 1 行 / 两列 2 行 / 单列 3 行），单列档另配一条「x 只有一个值」证明 span 真被重置了。
- **countUp 只验终值等于原值是恒真的** —— 模块压根没跑也满足。改成中途取样：
  滚入视口 180ms 时的文本必须与静止后不同。

三条活性自检，报红范围逐条核对：

| 断言 | 破坏方式 | 结果 |
|---|---|---|
| 两栏不溢出 | product 改回 `width: 465 + flex-shrink: 0` | 768 三页全红，且报出 info 被挤到 231 |
| 单列档重置 span | 删掉 `grid-column: auto` 那两行 | 575 报 2 列 —— 隐式网格确实把第二列造回来了 |
| countUp 真的在跑 | 从模块注册表里摘掉 | 中途取样断言红（终值断言仍绿，正如预期） |

**回归**：`r31`(52) / `r32`(42) / `r36` / `r39` / `r40` / `r41` / `r42` 全过，
`rwd.py` 12×14 全绿，`revealcheck` 全绿。
`r42rect.py r41 1440`：**11 页里 10 页矩形逐个吻合**，唯一有差异的 reviews 是上一轮
删 app-slot 留下的（四个容器各矮 288 + 占位框消失），**本轮改动在 1440 上零影响**。

⚠ **r40 / r41 的断言随反转同步更新**（照 r39 的先例，改不删）：r40 的 promo top
`-8` → `-5`；r41 第 3 节整节从「两列撑到 991」改成「撑到 767」，两个正方形的
「保留 520 上限」改成「跑满宽度」。两处都在原地注明了是哪一轮反转的。

### 遗留

- **待决 M（正方形贴边）与 N（`.gb-stat__value` 要不要加计数）见上**，都要需求方一句话。
- **`.gb-science-card__value` 与 `.gb-science--cream` 的手机值都推翻了板值**，
  不是还原度问题，别在下一轮对稿时改回去。
- 768–1280 依旧没有设计稿。本轮把两栏一路推到 768，这一带的所有表现都是行为约束。
- `r43` / `r43m` 快照仍未存（cssnap 在这台机器上 OOM），**下一轮基线仍是 r41 / r41m**。

### 文件清单

```
改  assets/customstyle.scss    compare/ingredients/faq-image/product 四个 __inner:
                                 堆叠阈值 mid|stack → narrow, 配套规则共 11 处同步;
                               product__media / __info: 刚性 465 → flex 0 1 465px + min-width 0;
                               product__thumbs: pc 档注释改写（768–1280 已不再堆叠）;
                               faq-image__media/__body、ingredients__disc/__body: 去掉堆叠档 max-width;
                               science__cards / nutrition__cards: 两列扩到 narrow, 单列进 mobile
                                 并重置 grid-column;
                               science--cream padding-top 64; science-card__value 手机 36/40
                                 (并删掉 --nutrient 的同名覆盖); science--tight inner gap 48;
                               compare__inner 堆叠 gap 46; promo-art__img 手机 top -5%;
                               faq-image padding 64/80; expert-card 加 scroll-snap-stop: always;
                               $build → 20260827-r43
改  assets/customstyle.css     编译产物
改  assets/main.js             新增 countUp 模块（+ 注册表 + window.gumi 导出）;
                               slider: dragEnd 支持 [data-slider-step] 一次一张
改  reviews.html               gb-expert__inner 加 data-slider-step
改  science.html index.html    9 处 .gb-science-card__value 加 data-count-up
改  全部 11 页 + font-check.html   ?v= / EXPECT_BUILD → r43
新  tools/r43check.py          本轮四条的定向断言 + 三条活性自检
改  tools/r40check.py          promo top 断言随反转更新 -8 → -5
改  tools/r41check.py          第 3 节整节随反转更新（991 → 767, 上限去除）
改  docs/CHANGELOG.md          本条
改  docs/PROJECT-STATUS.md     待决 J 定向 + 新增 M / N
改  docs/HANDOFF.md            状态 / 不要报成 bug 的清单 / 验证跑法
改  README.md                  build 号
```

---

## 2026-08-27 第四十三轮：任务文档第三批 9 条（`$build` = `20260827-r44`）

⚠ **`修改任务文档.txt` 又被整批换版**（md5 `467df0c8` → `845dff6e`，881 字节，08:16 写入）：
上一批 8 条整组不见，换成 9 条新的。**第 8/9 条正是上一轮待决 M 的裁决**，落法与上一轮
记录里写的那行预案（「inner 的 narrow 档 `padding-inline: var(--pad-x)`，`__body` 的
补偿相应去掉」）逐字一致。文档结尾还留着一个只有编号、正文为空的**第 10 条**，未做。

### 1. 正方形不再贴边：版心从 `__body` 搬回 `__inner`（第 8/9 条）

上一轮按字面去掉 767 以下的宽度上限，结果 390 处 390×390、767 处 767×767 —— 记进了待决 M。
本轮的解法不是把上限加回原位，而是**把版心的责任从子元素挪回容器**：

| 元素 | 上一轮 | 本轮 |
|---|---|---|
| `.gb-ingredients__inner` / `.gb-faq-image__inner` | `padding-inline: 0` | `var(--pad-x)` |
| `.gb-ingredients__body` / `.gb-faq-image__body` | `padding-inline: 20px` | `0` |
| `.gb-ingredients__disc` / `.gb-faq-image__media` | `max-width: none` | `520px` |

净效果：**正文起点一动不动**（仍是 20），正方形从贴边回到 390 处 350×350、767 处 520×520 居中。
居中不用额外写 —— 两个 `__inner` 在堆叠档本来就带 `align-items: center`。
`.gb-compare__inner` 早就是「gutter 留在容器上」的写法，这一改正好三者归一。

### 2. expert 轨道手机端居中，前后各露一张（第 2 条）

`.gb-expert-card` 在 `narrow` 档加 `scroll-snap-align: center`（`mid` 档仍是 `start`）。
390 处静止时**前后各露 26.5px**，几何对称。

- **只落到 767 以下**，768–991 保持 start —— 那一带 start 对齐本来就露 2.3 张，提示已经够了。
  ⚠ 这是我按「手机端」字面定的范围，需求方若要整条轨道都居中，把这行从 `narrow` 挪到 `mid` 即可。
- **没动 JS**。`scroll-padding` 默认 0，所以「居中」是相对**滚动口**而非内容盒，
  轨道自己的 `padding-inline` 不参与，不需要 `data-slider-centre`（它的算式没算 padding，
  是给 reels 那条无 padding 的轨道写的）。`wrap()` 每次平移正好一个整集 = 3 个 pitch，
  居中偏移量是常数，**循环不会把居中滚丢**。
- 左侧那张之所以露得出来，靠的是第四十一轮的克隆循环；无克隆时首张左边没有东西，
  判据里的 `leftPeek` 会读到 0。

### 3. gb-dosed 堆叠点 1024 → 767（第 5 条）

与上一轮那四个 `__inner` 同样的搬法，**同样的病也在**：`.gb-dosed__media` 是
`flex: 0 0 598px` + `width: 598px`，两栏 598+54+598 = 1250 塞进 768 的 728 内容盒。
改成 `flex: 0 1 598px; min-width: 0`（`__body` 补 `min-width: 0`）。

⚠ 这个刚性 basis **在它本来就覆盖的带宽里已经在伤人**，不是本轮新引入的：活性自检把它改回去，
900 处正文列只剩 **192px**、768 处 **169.3px**，768 还横向溢出 24px。所以这条既是搬迁也是修复。

配套：`__block` / `__block--flip` 的方向切换 `stack` → `narrow`；`__body` 去掉堆叠档
`max-width: 598px`（第 5 条明写）；`__inner` 的 gap 从 `stack` 这个**布局阈值**挪回值档
（旧写法 48/64/96 三段里 `stack` 与 `narrow` 重叠，靠源码顺序分胜负，违反断点铁律），
改成 `narrow: 48` + `tablet: fluid(48, 96)`，768 与 1281 两个缝都不跳。
`__body` 的 `padding-inline` 也改成 `fluid(0, 40px)` —— 768 处该列只有约 340 宽，
平铺 40+40 会只剩 260 装 30px 的标题。

### 4. product 的上限从容器挪到 media（第 6 条）

`.gb-product__inner` 去掉堆叠档 `max-width: 560px`，`.gb-product__media` 改为
`max-width: 520px; margin-inline: auto`。**520 = 旧的 560 减去 inner 自己的 20+20 padding**，
所以画廊在任何宽度下都和改前一模一样，被放开的只有正文列（767 处从 520 → 727）。
数值取自被移除的那条规则，不是新拟的。

### 5. 其余四条

| 条 | 落点 | 备注 |
|---|---|---|
| 1 | `.gb-page-hero__media` narrow 加 `max-width: 570px` + `margin-inline: auto` | 390 处无变化（本来就 350），只在 571–767 生效。inner 在该档是 `align-items: stretch`，定宽后不居中就会硬贴左，故补 auto 边距 |
| 3 | `.gb-app-section--lg` narrow `padding-top: 52px` | 只落在 reviews（唯一带这两个类的元素）；pdp 的裸 `.gb-app-section` 仍是 64，判据里专门反证 |
| 4 | `.gb-product` narrow `padding-bottom` 64 → **46** | `--lg` / `--page` 在同档各自重述过 padding-bottom，源码顺序天然实现了需求里的 `:not()`，不需要真写 `:not()`。生效页 = reviews / our-story / how-gumi-works |
| 4 | `.gb-promo-art__img` narrow `top` −5% → **−4%** | **第三次改动**：−8%（第四十轮）→ −5%（第四十二轮）→ −4% |
| 7 | 删掉 `.gb-page-hero__lead--coral-mobile` | 规则与 how-gumi-works 上的类名一并删除。原注释写着「等设计方定夺」，本轮定了 |

⚠ **第 3、第 4 两条都同步改了 `tablet` 斜坡的手机端点**（`fluid(52px, 96px)` /
`fluid(46px, 96px)`），否则 767 → 768 会跳一档。判据里有专门的「无缝」断言。

### 验证

`r44check.py` 全过，**改前 CSS 下 72 条报红、改后 0 条**（双向判据）。
三条活性自检各自在正确范围内报红：撤掉居中吸附 → 8 条（390 偏心 42.5、左侧露出 −16）；
dosed media 改回刚性 → 3 条（900 正文 192、768 正文 169.3、768 溢出 24）；
disc 去掉 520 上限 → 5 条（767 处 727 宽）。

`r31`(52) / `r32`(42) / `r36` / `r39` / `r40` / `r41` / `r42` / `r43` 全过，
`rwd.py` 12×14 全绿，`revealcheck` 全绿，`hardbreaks` 恒定 34 ok / 6 MISSING。
`customstyle.css` 两次编译 md5 一致（`6e98d060…`）。

**桌面**：`r42rect.py r41 1440` 结果与上一轮**逐字相同**（11 页吻合，reviews 的差仍是
上一轮删 app-slot 的 −288），本轮在 1440 上零影响。

**手机**：改本轮前后各采一次 390 矩形并按模块归因 —— 唯二「未归因」的是 `body` / `main`
两个高度，是模块变化上浮的结果；其余变动全部落在本轮点名过的模块内。各页高度差与预期精确对上：
how-gumi-works / our-story **−18**（product 底 padding）、reviews **−70**（−18 −12 −40）、
science **−80**（两个正方形各 −40）、pdp **0**（promo-art 是绝对定位）、index **0**
（390 处 560 上限本来就不生效）。

### 遗留

- **第 10 条正文是空的**，只有编号。
- **`.gb-dosed__media` 手机端仍是 `max-width: 350px`**（稿在 390 的值）。767 处正文已放开到 727，
  而正方形还停在 350，视觉偏小。本轮没动它 —— 第 5 条只说「去掉固定宽度」，没给新上限，
  而第 9 条点名的两个模块里不含 dosed。**要不要比照 520 处理，等一句话**（待决 O）。
- **第 2 条只落到 767 以下**（待决 P）；**第 6 条的 520 是推算值**（待决 Q）——两条都在上面写了依据。
- 待决 **G / I / K / L / N** 仍未决；**M 本轮已由第 8/9 条裁决关闭**。
- `r44` / `r44m` 快照仍未存（cssnap 在这台机器上 OOM），**下一轮基线仍是 r41 / r41m**。
  本轮改用「反解改动 → 生成改前 CSS → 前后对采」的临时办法，判据更准但不落盘。

### 文件清单

```
改  assets/customstyle.scss    page-hero__media: narrow 加 max-width 570 + margin auto;
                               expert-card: narrow 加 scroll-snap-align: center;
                               app-section--lg: narrow padding-top 52 + tablet 斜坡;
                               product: narrow padding-bottom 64 → 46 + tablet 斜坡;
                               promo-art__img: narrow top -5% → -4%;
                               dosed__inner: gap 从 stack 挪回值档 (narrow 48 + tablet 斜坡);
                               dosed__block / __block--flip: 堆叠 stack → narrow;
                               dosed__media: 去 width 598 → flex 0 1 598px + min-width 0;
                               dosed__body: 去堆叠档 max-width, 加 min-width 0 与 padding 斜坡;
                               product__inner: 去堆叠档 max-width 560;
                               product__media: narrow 加 max-width 520 + margin auto;
                               删除 .gb-page-hero__lead--coral-mobile 整条规则;
                               ingredients/faq-image __inner: narrow padding-inline 0 → var(--pad-x);
                               ingredients/faq-image __body: narrow padding-inline 20 → 0;
                               ingredients__disc / faq-image__media: narrow max-width none → 520px;
                               $build → 20260827-r44
改  assets/customstyle.css     编译产物
改  how-gumi-works.html        移除 gb-page-hero__lead--coral-mobile 类
改  全部 11 页 + font-check.html   ?v= / EXPECT_BUILD → r44（33 + 1 处）
新  tools/r44check.py          本轮九条的定向断言 + 三条活性自检 + 双向判据
改  tools/r40check.py          promo top 断言随反转更新 -5 → -4
改  tools/r41check.py          两个正方形的断言从「跑满宽度」改回「保留 20 版心」
改  tools/r43check.py          两个正方形的上限断言 none → 520px；promo top -5% → -4%
```

---

## 2026-08-27 第四十四轮：任务文档第 10–12 条（`$build` = `20260827-r45`）

⚠ 这次是**追加**不是换版（md5 `845dff6e` → `b4e03e6c`，881 → 1131 字节）：1–9 条逐字未动、
上一轮已完成，**第 10 条补上了正文**，并新增 11/12/13。**第 13 条本轮未做**，
量化结果与三条可选方案见待决 S。

### 1. 第 10 条：dosed 标题多出一整行空行 —— 行尾的 `&nbsp;` 不会悬挂

需求方的原话是「样式不对，似乎多了很多空格」。实测：1440 处
`.gb-dosed__title`（"One pouch. Once a day. That's the whole ritual."）**占 3 个行盒
却只有 2 行文字**（h2 高 144，行高 48），两行之间浮着一团青柠色块。

病因链：

1. 稿里每个 `<br>` 前都写了 `&nbsp;`（全站 19 处），用意是「br 被 `display:none` 时
   这个空格顶上，且此处不许断行」。
2. 但 **U+00A0 在行末不像普通空格那样悬挂/折叠**。1440 处第一行墨迹 475.4 + nbsp 11.1
   = **486.5，比 mask 的 486 宽 0.5px** —— nbsp 自己折到了下一行。
3. `data-line-reveal` 的 `groupLines()` 按 `offsetTop` 把节点分行包进块级
   `.gb-line-mask`，那个孤零零的 nbsp 于是在 mask 1 内部撑出第二个行盒
   （mask 1 高 100.8 而不是 48）。
4. `.gb-ink-halo` 那层同样多出一行，`ink-outline()` 的描边就在这条空行上画出了那团色块。

**改法**：全站 19 处 `&nbsp;<br` 改成普通空格。

⚠ **先验证了 `&nbsp;` 兼着的「不许断行」职责用不上**：拿改前 / 改后两套页面，
6 页 × 11 档 × 全部 `[data-line-reveal]` 元素比断行点，**只有一处不同** ——
正是 `gb-dosed__title` 在 1440 从 144 高回到 96。其余断点一处未动。

### 2. 第 11 条：`.gb-dosed__inner` gap 96 → 80

需求写的是不带档位的 `gap: 80px`，按「规则自身的值」理解 = 基础档（板是 96）。
`tablet` 斜坡上端同步改成 `fluid(48px, 80px)`，下端仍接 48，两个缝都不跳。
手机档 48 未动。**若原意是别的档位，见待决 T。**

### 3. 第 12 条：`.gb-story__inner` 改成与卡片网格同一套 3 → 2 → 1

从 flex 行改成 grid，套用 `.gb-science__cards` 的整套装置：

| 档 | 排布 |
|---|---|
| ≥1281 | 三列一行 |
| 576–1280 | **四轨、每张跨两轨**，落单的第三张 `grid-column: 2 / span 2` 居中 |
| ≤575 | 单列，且**必须重置 span**（否则隐式网格把第二列造回来） |

实测：1280 处三张卡 x = 79.9 / 652 / **365.9**（第三张居中）；575 处三张同 x、真单列。
手机档几何与改前逐像素相同（原本就是 column + gap 48）。

### 验证

`r45check.py` 全过；改前 CSS 下 13 条报红、改后 0 条。三条活性自检各自报红：
还原 `&nbsp;` → 1440 标题回到「3 行盒 / 2 行文字」；删 story 单列档的 span 重置 →
575/390 变 2 列；gap 改回 96 → 3 条。

`r31`(52) / `r32`(42) / `r36` / `r39` / `r40` / `r41` / `r42` / `r43` / `r44` 全过，
`rwd.py` 12×14 全绿。

**新判据 `tools/emptyline.py`**（落盘复用）：全站任何 `[data-line-reveal]` 元素的
**行盒数必须等于视觉行数**，多出的行盒就是这个病。它比「HTML 里有没有 `&nbsp;`」强得多 ——
后者既不解释病因也抓不住复发。⚠ 这条判据写错过两次，两次都记进了 HANDOFF：
数 `.gb-line-word` 的 `offsetTop` 会漏（词是 `inline-block`，自己内部折行仍只有一个 top），
改数整元素的 Range 行盒又会翻倍（`.gb-ink-halo` 是同一份文案的描边副本）。
最终取「内容层词的 Range 行盒 + 3px 容差聚类」。

**前后对照**（反解本轮 SCSS 改动生成改前 CSS）：1440 只有 how-gumi-works（dosed gap，
−16 = 两个 gap 各 −8）与 our-story 变动，未归因的只有 `body` / `main` 两个高度。
⚠ our-story 报了 147 处矩形变动，看着吓人，**实测全站最大偏差 0.0156px** ——
是 flex `1 1 0` 与 grid `1fr` 两种算法的轨道舍入差，超过 0.1px 的一处也没有，肉眼无差。
390 档 **十二页全部无变化**（唯一的 0.4px 差是 countUp 动画中途取样的字宽抖动，不是布局）。

### 顺带发现（未修，等裁决）

- **`.gb-page-hero__title` 在 1281 附近会折成 5 行**（science / reviews / our-story）。
  1281 处文字列只有 486.8 宽而字号是 64，"Aussie-approved." 这个词自己在连字符处断开。
  1440 处列宽 566 就放得下。是 `flex: 1 1 566px` 与 `1 1 570px` 两栏在 1281 同时收缩所致，
  与本轮无关，也不是第 10 条那个病。**待决 U。**

### 文件清单

```
改  assets/customstyle.scss    dosed__inner: gap 96 → 80（基础 + tablet 斜坡上端）;
                               story__inner: flex 行 → 3->2->1 网格（含单列档 span 重置）;
                               story-card: 去掉 flex 基/宽度（网格轨道接管）;
                               $build → 20260827-r45
改  assets/customstyle.css     编译产物
改  faq/how-gumi-works/index/our-story/pdp/reviews  19 处 &nbsp;<br → 普通空格
改  全部 11 页 + font-check.html   ?v= / EXPECT_BUILD → r45（33 + 1 处）
新  tools/r45check.py          第 10/11/12 条的定向断言 + 三条活性自检
新  tools/emptyline.py         全站空行盒判据（可复跑，带活性自检说明）
```

---

## 2026-08-27 第四十五轮：第 13 条 —— CTA 板的圆瓣不再被拉伸（`$build` = `20260827-r46`）

上一轮把这条记成了待决 S（三条改法都是设计决策）。需求方回「想办法解决，不行就换 svg 图
或者其他办法」，于是本轮解掉了 —— **不用换图，也不用 JS**。

### 病因（上一轮已量化，这里只记结论）

`.gb-cta-band__plate` 用 `mask-size: 100% 100%` 把**一整条固定轮廓**拉到盒子上。
板的宽高比从 0.69（390）连续变到 3.26（1440），而每块稿只是一张固定的画，
于是 767 处把手机稿的圆瓣横向拉了 **2.07 倍**、768 处把桌面稿的压到 **0.44 倍**。

### 关键发现：两块稿是同一种构造

把 Figma 导出的两条 `fillGeometry` 路径解开（取路径上的 on-curve 点、按贴边筛出尖点），
两块稿都是「**半径固定的圆瓣，圆心落在距边 r 的线上，按固定间距排开，与内矩形取并集**」，
只是数不同：

| 稿 | r | 水平间距 | 垂直间距 | 顶边瓣数 | 侧边瓣数 |
|---|---|---|---|---|---|
| 1280 × 392.957 | 58.8848 | 89.4023 | 91.7291 | 14 | 4 |
| 350.852 × 507.512 | 39.9189 | 67.7535 | 61.0963 | 5 | 8 |

既然是这个构造，正确的响应式行为就不是「瓣形跟着盒子变」，而是「**瓣数**跟着盒子变」——
和站内波浪 `--sc-w`（画法固定、宽了就多重复几个）同一原则。

### 改法：九宫格 `border-image`，纯 CSS

源图不再是整块板，而是一个 **2×2 瓣的迷你板**（`2r+间距` 见方），由 `scallop-tile()`
按 r / 间距生成；`border-image-slice: r fill`、`border-image-width: r`、
`border-image-repeat: round`：

- **四角**按原尺寸绘制，永不缩放；
- **四边**各平铺**一个瓣周期**，`round` 只把瓦片缩到刚好放下整数个周期；
- **中间**是纯色，`fill` 拉伸它没有任何可见影响。

```scss
border: 0 solid transparent;   // border-width 保持 0，盒子不长大；
                               // 但 border-style 不能是 none，否则图根本不画
border-image: scallop-tile($plate-r-pc, $plate-px-pc, $plate-py-pc)
              $plate-r-pc fill / #{$plate-r-pc}px / 0 round;
```

颜色被烤进了源图 —— `border-image` 取代背景，底下再留 `background` 会从瓣的谷里透出来。
所以颜色由 Sass 从 `$c-green` 插值进 data URI，仍然跟着变量走。

### 效果（`tools/platecheck.py` 从像素量的，14 档）

| | 旧 | 新 |
|---|---|---|
| 390 / 1440 顶边瓣数 | 稿上的 5 / 14 | **5 / 14，完全复现** |
| 390 / 1440 侧边瓣数 | 稿上的 8 / 4 | **8 / 4，完全复现** |
| 767 横向畸变 | **2.07×** | **0.959×** |
| 768 横向畸变 | **0.44×** | **0.979×** |
| 全档横向畸变 | 0.44 – 2.07 | **0.94 – 1.02** |
| 全档纵向畸变 | 同上 | **0.87 – 1.07** |

纵向那 ±13% 是 `round` 在周期数只有 3–4 个时的**固有粒度**，不是实现缺陷（截图看不出来）。

### 验证

**新判据 `tools/platecheck.py`**（落盘复用）：截图、按颜色抠轮廓、逐列取边缘，验四条
**与实现无关**的不变量 —— 谷深符合解析式（瓣形）、间距均匀（无拉伸梯度）、
边段是整数次平铺、两块稿的瓣数复现。

⚠ **判据刻意不预测浏览器的取整**：实测 Chrome 的 `round` 落点与 `round()` / `ceil()` 都对不上
（1100 处 3.43 个周期它取了 4 个）。把实现细节写进断言，浏览器改版就会误报。
谷深之所以是好判据，是因为它**与平铺缩放无关** —— 瓣被缩放 s 时间距也是 p·s，
在 `d = r − r√(1 − (p/2r)²)` 里约掉了；而旧的拉伸实现会改变它。

活性自检：改回 `mask-size: 100% 100%` → **谷深、缩放、整数平铺、两块稿瓣数四项全部报红**
（1440 顶边谷深 38.50 vs 解析 20.55、缩放 6.18、瓣数 2 vs 14）。

`r31`(52) / `r32`(42) / `r36` / `r39` / `r40` / `r41` / `r42` / `r43` / `r44` / `r45` 全过，
`rwd.py` 12×14 全绿，`platecheck` 14 档全过。

**布局零影响**（`border-image` 在 `border-width: 0` 下不参与布局）：拿「板改回
`background` + `mask`」的一份 CSS 做对照，1440 与 390 两档 **12 页全部 0.0000px 位移**。
对照本身非自洽 —— 两份 CSS 差 864 字节、`border-image` 出现次数 0 vs 2。

**内容没有被圆瓣吃到**：`mask` 会裁剪内容而 `border-image` 不会，这是行为差异。
实测 8 档，内容离板四边的最小间距在任何档位都 ≥ 谷深，所以去掉裁剪没有可见影响。

### 文件清单

```
改  assets/customstyle.scss    删掉 $mask-scallop-band / $mask-scallop-band-mobile
                                 两条被拉伸的整轮廓;
                               新增 $plate-r/px/py-pc|mob 六个构造参数 +
                                 scallop-tile() 生成 2×2 瓣的九宫格源图;
                               cta-band__plate: background+mask → border-image ... round;
                               顶部 @use "sass:string";
                               $build → 20260827-r46
改  assets/customstyle.css     编译产物
改  全部 11 页 + font-check.html   ?v= / EXPECT_BUILD → r46（33 + 1 处）
新  tools/platecheck.py        圆瓣几何的像素级判据（14 档 + 活性自检说明）
```

---

## 2026-08-27 第四十六轮：修掉九宫格的区块接缝（`$build` = `20260827-r47`）

需求方反馈「可能由于渲染的原因交界处出现了很多细线」。**是真的，而且我上一轮的判据漏了它** ——
`platecheck.py` 只验几何（瓣形 / 间距 / 平铺 / 瓣数），验不了「有没有多余的浅色线」。

### 病因：九宫格的区块交界在某些 DPR 下渲染出发丝线

`border-image` 的四个区块（角 / 边 / 中）各自光栅化并抗锯齿，两条相邻的半透明边加起来
凑不满一格不透明度，于是在**离边 r 的那个矩形**上留下一条比板色浅的线。

⚠ **只在某些设备像素比下出现**，实测 1100 处：

| DPR | 1 | 1.25 | 1.5 | 1.75 | 2 | 2.25 | 2.5 | 3 |
|---|---|---|---|---|---|---|---|---|
| 发丝线 | 无 | **有** | 无 | **有** | 无 | **有** | 无 | 无 |

有的那几档正是 Windows 的 125% / 150% / 175% 缩放。最明显的一处：DPR 1.75 下
y = 57.1（r = 58.88 的那条边）上一条 1515px 长、比板色浅 63 的线。
**只测整数 DPR 会全绿**，这也是上一轮没抓到的原因。

### 改法：图下面垫一层同色实底

```scss
@mixin plate-pad($r, $px, $py) {
  background: linear-gradient($c-green, $c-green) no-repeat center /
              calc(100% - #{(scallop-valley($r, $py) + 1) * 2}px)
              calc(100% - #{(scallop-valley($r, $px) + 1) * 2}px);
}
```

关键是**内缩量**：实底必须待在瓣的**谷线**以内，否则会从谷里透出来把轮廓填平
（就变成一个圆角矩形了）。谷深 `d = r − r√(1 − (p/2r)²)` **与平铺缩放无关**
（瓣被缩放 s 时间距也是 p·s，两者约掉），所以每档是常数：桌面 20.56（顶底）/ 21.96（左右）、
手机 18.80 / 14.22，各留 1px 余量 → 内缩 43.11 / 45.91px。接缝在 r = 58.88 处，被稳稳盖住。

### 验证

**新判据 `tools/seamcheck.py`**（落盘复用）：5 档宽 × **8 档 DPR（含 1.25 / 1.75 / 2.25）**，
找板内比板色浅的贯穿发丝线。**40 组全清**。

⚠ **两条判据互为守卫，必须都跑**：
- `seamcheck` 管「有没有多余的浅色线」—— 删掉 `plate-pad` 两处，1100 的
  DPR 1.25 / 1.75 / 2.25 立刻报红（各一条 Δ63 的线）。
- `platecheck` 管「实底有没有透出来把瓣形填平」—— 把实底放大 8px 越过谷线，
  6 条谷深断言立刻报红（390 顶边 10.50 vs 解析 18.80）。

`r31`(52) / `r32`(42) / `r36` / `r39` / `r40` / `r41` / `r42` / `r43` / `r44` / `r45` 全过，
`platecheck` 14 档全过，`rwd.py` 12×14 全绿，两次编译 md5 一致（`14432f00…`）。

### 文件清单

```
改  assets/customstyle.scss    新增 scallop-valley() 与 plate-pad() mixin;
                               cta-band__plate 的两档各加一层内缩同色实底;
                               $build → 20260827-r47
改  assets/customstyle.css     编译产物
改  全部 11 页 + font-check.html   ?v= / EXPECT_BUILD → r47（33 + 1 处）
新  tools/seamcheck.py         九宫格接缝判据（8 档 DPR，含分数缩放）
```

---

## 2026-08-28 第四十七轮：任务文档第 14–19 条（`$build` = `20260828-r48`）

⚠ `修改任务文档.txt` 又是**追加**（md5 `b4e03e6c` → `364ac2b4`，1131 → 1953 字节）：
1–13 条逐字未动、r44/r45/r46 已做完，新增 14–19 六条。其中两条是既有挂账的裁决 ——
第 15 条后半对应 r38 遗留「`--center` 改了 70、`--lg` 仍是 96，两个变体不再一致」，
第 18 条对应 r34 遗留第 1 条「富文本段距实现 20、稿子 16」。

### 1. 第 14 条：手风琴正文与 FAQ 页留白的手机值

`.gb-acc-body__text` 只有一档 18/28/−0.36（r31 按桌面定的），手机板是正文号
16/24/−0.32；补 `narrow` + `tablet` 斜坡。
`.gb-faq--plain` 的 `narrow` 之前只覆盖了 `padding-top: 64`，底边继承基类的 80。
需求给的 `52px 0 64px` 两个数都落在 `narrow` 档（桌面基类是 96/120、`--plain` 是 94），
所以 top 回到基类的 52、bottom 收到 64，`tablet` 两条斜坡跟着改起点。

### 2. 第 15 条前半：CTA 按钮的标签本来就在折行

需求写的是「`padding: 0 64px` 需要加响应式」，实测**标签在 320/360/375/390 全部折成两行**。
病因不是 64 太大，而是按钮比板窄：板 `I324:53922;236:11728` 的按钮是 350 宽的 STRETCH，
64 的内缩留 222 给内容；实现里 `.gb-cta-band__content` 的 38 gutter 把按钮压到 274，
64 只剩 **146**，而标签墨迹 **146.34** —— 差 0.34px 就换行。`narrow` 档收到 24px，
390 处留 226，与板的 222 几乎一致。

⚠ **真因是那个 38 的 gutter，不是按钮自己的内缩**，见待决 V。

### 3. 第 15 条后半：页头的 padding 值统一到 `--center`

`--center` 与 `--lg` 的差别有两个轴，只有一个能合并：

| | 净留白（1440 / 390） | 波浪 |
|---|---|---|
| `--center`（faq / get-in-touch / privacy / referral / shipping） | 70 / 64 | 小瓦片 `--sc-h` |
| `--center --lg`（how-gumi-works / our-story） | **96** / 64 | **大瓦片** `--sc-lg-h` |

净留白按需求统一成 70/64。**波浪那一轴不能合并**：两页 hero 里挂的是
`gb-scallop--lg`，1440 处实测高 128.97 对小瓦片的 96.94，真把 class 删掉、
padding 退回 `--sc-h`，内容到波浪的距离会从 96 掉到 **37.97**。
所以改成 `--center` 声明 `--hero-wave: var(--sc-h)` 并独占全部 padding 值，
`.gb-page-hero--lg` 缩成**一行变量覆盖**、不再携带任何数值 ——
三条 `@media` 覆盖从它身上消失，class 只剩「告诉容器波浪多大」这一件事
（section 读不到自己子元素的波浪尺寸，这个方向的信息只能由 class 传）。

代价：how-gumi-works / our-story 桌面各矮 **26px**，见待决 W。

### 4. 第 16–18 条：表单与富文本的手机值

- `.gb-form-section` `narrow` 从 `64px 0` 改成 `64px 0 84px`，`tablet` 底边补 `fluid(84, 96)`。
- `.gb-form__disclaimer` `narrow` 补 `margin: 16px 0`，`tablet` 走 `fluid(16px, 0px)`（桌面无 margin）。
- `.gb-rich-text` 的六个块级子元素 `narrow` 段距 20 → 16。板上 privacy + shipping
  **103 个** 16/24 正文节点的 `paragraphSpacing` 全是 16 —— 桌面那一档仍是 20，
  需求只点名手机端，见待决 X。

### 5. 第 19 条：shipping 表格在 768 处整张网格消失

r37 定了列宽/行高、r38 补了边框/表头/斑马，**但两轮都只写在 `@include narrow` 里**。
768 一过，表格掉回自造的桌面 fallback：`table-layout: auto`、`padding: 12px 0`、
只有一条 `border-bottom`、无填充 —— 行高 49、列宽 181/547，跟板毫无关系。
shipping **没有桌面板**，唯一画出来的表就是手机那张，所以把整套网格提升为基础规则（待决 Y）。

列宽同时从百分比换成 px：板里一列 HUG、一列 FILL（表 1 是 88 HUG / 262 FILL，
表 2 反过来 203 FILL / 147 HUG），百分比会在表变宽时把两列一起拉。改成固定列写 px
之后，350 板宽处仍精确落在 88/262 与 203/147，更宽的视口只长 FILL 那一侧。

### 验证

**新判据 `tools/r48check.py`（193 条断言，全过）**，每条需求都跨 390/767/768/1440 验值档交接：

- 第 15 条前半不断言 padding 等于某个数，断言**标签占一行且墨迹 ≤ 可用宽**，9 档全过。
- 第 15 条后半不断言 class 不存在，断言**内容底到波浪顶的距离**两组页头同档相等，
  且大瓦片仍在 section 内。
- 第 19 条跨四档验同一组不变量（fixed 布局 / 表头填充 / 单元格描边 / 9.5-12 内边距 /
  44 行高 / 斑马 / 无横向滚动），并锁死 350 板宽下的两组列宽。

⚠ 判据自身踩到三个假信号，已在脚本里注掉原因：波浪**有意**比 `--wave-h` 高 1px
（r34 的发丝缝修法）、`.gb-form__disclaimer` 只在 referral 页、`border-collapse`
把外边框折进表框所以两列和是 349 不是 350。

**回归**：`rwd.py` 12×14 全绿；`revealcheck` 入场全部归位；`emptyline` 462 组无空行盒；
`platecheck` 14 档、`seamcheck` 40 组（8 档 DPR）全清；
`r31`(52) / `r32`(42) / `r36` / `r39` / `r40` / `r41` / `r42` / `r43` / `r44` / `r45` 全过；
两次编译 md5 一致（`dcdf8be2…`）。

**桌面没被动到**：r47 与 r48 的矩形多重集 + body 高逐页比（12 页 × 390/1440）。
1440 处只有三页有差，全部是本轮有意改的 —— how-gumi-works / our-story **−26**（第 15 条）、
shipping **−54**（第 19 条），**其余 9 页 0 处矩形变化、body 高不变**。
390 处的差也逐项归了因：faq −32 = padding −28 + 手风琴正文行高 −4，
get-in-touch **+20**、referral **+52**（+20 padding +32 margin）、privacy −24（6 段 × −4）、
shipping −16、其余各页只有折叠态 `.gb-acc-body__text` 的 28 → 24，不进文档流。

### 文件清单

```
改  assets/customstyle.scss    acc-body__text 补 narrow+tablet；faq--plain narrow 改 padding
                               简写 + tablet 双边斜坡；cta-band__btn narrow padding-inline 24；
                               page-hero--center 引入 --hero-wave 并独占 padding，
                               page-hero--lg 缩成一行变量；form-section narrow/tablet 底边；
                               form__disclaimer narrow/tablet margin；rich-text 六选择器
                               narrow/tablet 段距；rich-table 整块提升为基础规则 + 列宽改 px；
                               $build → 20260828-r48
改  assets/customstyle.css     编译产物
改  全部 11 页 + font-check.html   ?v= / EXPECT_BUILD → r48（33 + 1 处）
新  tools/r48check.py          本轮 193 条断言
```

### 遗留

- **第 15 条的真因没动**（待决 V）：`.gb-cta-band__content` 手机端 gutter 38，板上是 0
  （内层文字帧才有 8）。除了按钮，标题与引导句的可用宽也是 274 对板的 334。
- **表格描边**：板是 0.5 CENTER，实现写 `0.5px`，headless DPR1 上舍入成 1px；
  DPR2 真机会按 0.5 画。既有行为，本轮未动。
- 常驻那几条（768–1280 无板、小波浪手机端高 12px、PP Palma 300 试用装、三套零引用字体栈）不变。

---

## 2026-08-28 第四十八轮：弹窗锁滚动仍然横向抖动 —— 补偿被算了两次（`$build` = `20260828-r49`）

需求方反馈「点击出现弹窗禁止屏幕滚动，会让浏览器因为滚动条消失导致屏幕抖动，这个问题之前也有碰到过」。
**之前确实修过**：第二十四轮加了 `--scrollbar-w` 实测 + `padding-right` 补偿，第三十九轮
给手机抽屉补了同一套。**但补偿写在了两个元素上，滚动条只消失一次，宽度却被吃掉两次。**

### 病因

```scss
html.is-modal-open,
body.is-modal-open { overflow: hidden; padding-right: var(--scrollbar-w, 0px); }
```

`html` 的 `padding-right` 已经把 `body` 的可用宽收窄了一次，`body` 再收一次：

| 1440 视口，滚动条 15 | 锁定前 | 锁定后（旧） | 锁定后（新） |
|---|---|---|---|
| `documentElement.clientWidth` | 1425 | 1440 | 1440 |
| 内容可用宽 | 1425 | **1410** | 1425 |
| 版心中心 | 712.5 | **705** | 712.5 |

**方向还反了**：内容不是右移而是左移 7.5px（补过头），所以第二十四轮那次「视口变宽、
内容右移」的直觉判断在现场对不上号，一直没被认出来。

第二十四轮的验证只把 `--scrollbar-w` 覆写成 17px 检查「CSS 机制有没有响应」，
**没有验补偿量对不对** —— 典型的自洽但不正确（[[probe-must-compare-against-invariant]]）。

`is-menu-open` 那条同样是两个都补，但它整块包在 `@include narrow` 里，
手机端 overlay 滚动条不占布局宽（实测 `innerWidth - clientWidth == 0`），补偿量恒为 0，
所以从来没暴露过 —— 直到有人用 767 以下的**桌面**窗口开菜单。一并修了。

### 改法

补偿只留在滚动元素上，`overflow` 仍两个都锁：

```scss
html.is-modal-open,
body.is-modal-open { overflow: hidden; }

html.is-modal-open { padding-right: var(--scrollbar-w, 0px); }
```

`main.js` 没动 —— 测量时机（加 class 之前、滚动条还在）本来就是对的。

### 验证

**新判据 `tools/scrolllock.py`（落盘复用，8 个用例 × 32 条断言，全过）**：
三个弹窗 × 五页 + 手机抽屉，逐个点开，比对**可见元素**在锁定前后的 x 与 width。

⚠ **这条判据必须保留真实滚动条**。Playwright 启动 headless chromium 时默认带
`--hide-scrollbars`，`innerWidth - clientWidth` 恒为 0 —— 没有宽度可失去，
任何写法都不会位移，**判据会全绿地放过一个坏页面**。脚本用
`ignore_default_args=["--hide-scrollbars"]` 拿回滚动条，并在测到 gap 为 0 时
**直接 abort 而不是通过**（[[negative-assert-needs-liveness-guard]]）。

**活性自检**：把 `body` 那条 `padding-right` 加回去重编译，判据立刻报红 ——
index 1440 处 **281 个可见元素位移**、`.gb-announcement` 宽 1425 → 1410。
`index@700` 的抽屉那两例仍是 0，正好交叉证明两条锁定规则各自独立生效。

判据自身踩了三个假信号，已在脚本注释里写明：跑马灯 `.gb-logo-scroll__track` 两次采样之间
自己在动（改用 `animation-play-state: paused` 冻结，不用 `animation:none` ——
那会把入场区块打回第 0 帧，见 [[kill-animations-blanks-reveal-blocks]]）；
页面里**另一个没打开的弹窗**也是 `fixed`，会跟着视口合法变宽；
所以采样加了 `checkVisibility({checkOpacity, checkVisibilityCSS})`，只验看得见的东西。

**回归**：`rwd.py` 12×14 全绿；`r31`(52) / `r32`(42) / `r36` / `r39` / `r40`（真的点开再点关抽屉）/
`r41` / `r42` / `r43` / `r44` / `r45` / `r48`(193) 全过；`revealcheck` 入场全部归位。
**非锁定态零影响**：r48 与 r49 逐页比矩形多重集 + body 高，12 页 × 390/1440
**24 个组合 0 处差异** —— 规则只挂在 `.is-modal-open` / `.is-menu-open` 上，正常浏览时不存在。

### 文件清单

```
改  assets/customstyle.scss    is-modal-open / is-menu-open 的 padding-right 从
                               「html + body 各一次」改成只在 html 上；$build → 20260828-r49
改  assets/customstyle.css     编译产物
改  全部 11 页 + font-check.html   ?v= / EXPECT_BUILD → r49（33 + 1 处）
新  tools/scrolllock.py        滚动锁定判据（必须保留真实滚动条，gap=0 时 abort）
```

### 不要报成 bug

**锁定时 `position: fixed` 的覆盖层宽度会长 15px（1425 → 1440），这是对的**：
fixed 的包含块是视口，滚动条消失后可视区真的变宽了。它们此时要么正在打开（用户看不到
"变宽"，只看到它出现）、要么还关着不可见。判据用 `checkVisibility` 把它们排除，
**不要试图给 fixed 覆盖层也补 padding** —— 那会让遮罩盖不满右边 15px。

---

## 第四十九轮（2026-08-28）— 修改任务文档第 1–8 条

任务文档整份换新（md5 `72ef4f10…`，8 条），全部落地。`$build` → `20260828-r50`。

### 1. `.gb-stats__note` 桌面 margin-top −30 → **−34**

需求给的是裸值，按基础档落，768 以上生效；手机的 `−16`（第三十六轮需求方定的）不动。
⚠ 这两档之间原本就有 −16 → −30 的跳档（`margin-top` 从来没有 tablet 斜坡），
本轮只是把落差从 14 变成 18，**没有顺手补斜坡**（那是新决策，不是还原）。

`tools/r36check.py` 里「1440 保持 −30」那条守卫被本轮推翻，已就地改成 −34 并注明来由 ——
留着不改，下一轮回归会把它当 bug 修回去。

### 2. `.gb-stats__deco-bear` pc 端固定宽高

原来是 `width: 7.36%` + `aspect-ratio`，宽度跟着视口一路长（1920 处 140px）。
改成 `106px × 159.68px`（106 = 板宽 1440 上的槽位，比例仍是 387/583，所以 `aspect-ratio` 撤了）。

**钉死 pc 会在 1280/1281 处造出 94 → 106 的跳档**，所以 768–1280 补了
`fluid(81.6px, 106px)` 的斜坡接住两头 —— 两端都成了 px，这一档才第一次有条件插值
（源码里那句「fluid() is px-only, so percentages get no tablet tier」随之作废）。

判据不只量 1440：**1920 / 1441 / 1440 三处宽度必须完全相同**（「固定」的意思就是不再长大，
只量 1440 等于没量），外加 767/768、1280/1281 两个接缝断言。

### 3. `.gb-product__gallery` 改用 Swiper 11.2.6

`assets/swiper-bundle.min.js`（MIT，154KB）落进 `assets/`，挂在 5 个有图廊的页面上。
CSS **不引第二个样式表** —— 从 `swiper-bundle.css` 里摘出真正用到的 12 条规则，
以「Vendor — Swiper」分区写进 `customstyle.scss`（`assets/` 不收子目录，铁律 15）。
分区放在组件之前：`.gb-product__stage` 用同特异性重申了 `overflow` / `border-radius`，得让它赢。

**「效果不变」是逐条对齐出来的，不是靠感觉**：

| 原来的手写行为 | Swiper 里对应的写法 |
|---|---|
| 绝对堆叠 + `opacity` 交叉淡入 | `effect: "fade"` + `fadeEffect.crossFade` |
| `transition: opacity .3s $ease-out` | `speed: 300` + 分区里给 slide 写死本站曲线 |
| 拖动时画面不跟手 | `followFinger: false` |
| 位移 < 40px 不算滑动 | `threshold: 40` |
| 竖向为主的手势是在滚页面 | `touchAngle: 45` |
| 一次手势只走一张、到头不循环 | fade + `loop: false`（默认） |
| `prefers-reduced-motion` 归零 | `speed: 0`（Swiper 把时长写成行内样式，reset 的 `!important` 够不着） |

**两处刻意不用 Swiper**：

- **缩略图轨不接 thumbs 模块** —— 那会把它变成 transform 轨，丢掉 `scroll-snap`、
  `overflow` 滚动和它在 Lenis `PREVENT` 名单里的位置。它仍是普通按钮条，点了调 `slideTo`，
  `slideChange` 再把 `is-active` / `aria-current` 写回来。
- **键盘不接 keyboard 模块** —— 那个模块挂在 `document` 上，读者用方向键翻页时会被抢走。
  原来的 `keydown` 监听留在 stage 上，只在它有焦点时响应。

`a11y: false`：markup 已经带了 `role` / `aria-label` / `aria-current`，a11y 模块会再加一套打架的。

`.gb-product__image` 加 `cursor: grab` + `:active { cursor: grabbing }`（需求点名）。

⚠ `.swiper-backface-hidden .swiper-slide` 那条也摘了进来 —— Swiper 默认就给容器挂这个类，
漏掉它类名会变成空转，构建与 vendor 样式表**静默分叉**。

### 4. 弹窗关闭时内部内容横跳

第四十八轮修的是**页面**在锁滚动时不横移。这一条是同一个机制在**弹窗内部**的另一半：

`close()` 里 `is-modal-open` 是**立刻**摘掉的，而弹窗的淡出还要跑 0.28s（reel）/ 0.55s（营养表）。
摘掉的那一帧滚动条就回来了，`position: fixed` 的弹窗盒子（包含块是视口）当场从 1440 缩回 1425，
里面居中的 panel 跟着**左跳 7.5px** —— 而此刻它 `opacity` 还是 1，看得清清楚楚。

实测（index.html @1440，滚动条 15px）：

| 时刻 | panel x | 视口 clientWidth | panel opacity |
|---|---|---|---|
| 打开后 | 517.33 | 1440 | 1 |
| 点关闭 +120ms | **509.83** | **1425** | **1** |

改法是**把解锁推迟到淡出结束**，时长由弹窗自己在 CSS 里声明：

```scss
.gb-rv-modal {
  transition: visibility 0s linear $rv-in;
  --modal-exit: #{$rv-in};        // main.js 读这个
}
```

```js
this.unlockAfter(modalExitMs(el));   // 0 when prefers-reduced-motion
```

`unlockAfter` 用**令牌**而不是存 timer id：淡出途中重新打开弹窗时，上一次关闭挂起的回调
不许把新弹窗的锁解掉（判据里有这一条）。`prefers-reduced-motion` 下 reset 已经把时长和延迟
都归零，所以直接返回 0、立即解锁，不会白锁半秒。

三个弹窗（nl / rv / promo）都挂了 `--modal-exit`，一处修法覆盖全部。

### 5–8

- **5** `.gb-rv-panel__video` 加 hover 变色（`$c-ink` → `$c-green`）+ `trans(color)`。
  颜色是自定值，这个 lightbox 本来就是稿里没有的自建件 → PROJECT-STATUS 待决 AC。
- **6** `.gb-footer-cta__btn` 的 hover 换成 `.gb-btn--primary` 那套（lime 底 + green-900 字）。
  ⚠ 它脚下的 `.gb-footer-cta` 底板就是 lime，hover 后按钮形状只剩 1px 绿边框 → 待决 Z。
  `.gb-header__logo` 去掉 hover，连那条已无用武之地的 `transition: trans(opacity)` 一起删 → 待决 AA。
- **7** `.gb-highlight-card__text` 加 `margin: 0 auto`（卡片是 `text-align: center`，
  但那个 271/283 的盒子原来贴着左边，短行看起来和标题不对中）。
  `.gb-product--page .gb-product__media` 的 sticky **从 1281+ 铺到 768+** ——
  两栏布局从 768 就开始了，原来 1280 及以下的笔记本上图片根本不钉。
  偏移量 `calc(表头高 + 24)`，表头高在这一档是插值的，所以偏移也跟着插 → 待决 AF。
- **8** `.gb-science-card__value` 手机端的 36/40/−0.36 **移到 `.gb-science-card--nutrient`
  上而不是删掉**：直接删会把 50% 那组也一起带回 56/44，而它的板 324:58044 写的就是 36/40。
  95% 组回到板值 56/44 → 待决 AB。`tools/r43check.py` 里钉着 36/40 的两条断言同样就地改注。

### 验证

**新判据 `tools/r50check.py`（8 节，全过）**。取法上刻意避开三类恒真：

- **第 2 条**断言 1920/1441/1440 三处**完全相同**，而不是「1440 等于 106」——
  后者对一个还在随视口长大的元素也成立。
- **第 3 条**的核心断言是 **slide 矩形 == stage 矩形**。原来的 slide 是 `position:absolute; inset:0`，
  现在靠 wrapper 的 `height:100%` 一路传下来；这条链断了页面看着还在，只是图塌成 0 高，
  而任何「有没有 `swiper-initialized`」的断言照样全绿。另加 liveness：
  `typeof Swiper !== "function"` 时**直接 abort**（脚本 404 → gallery 安静早退 → 下面全部恒真）。
- **第 4 条**在**淡出中途**采样，并同时断言那一刻 `opacity` 仍是 1 —— 量一个已经看不见的
  元素有没有位移是没有意义的。另加两条反向断言：锁最终必须解开（否则「没位移」可以靠
  永不解锁作弊）、淡出途中重开时锁不许被旧定时器解掉。

**活性自检**（四项逐个撤销，判据都报红）：

| 撤销 | 判据反应 |
|---|---|
| `close()` 改回立即解锁 | 6 条红，三个弹窗各自量出 517.33 → 509.83 的 7.5px 横跳 |
| 抽掉 pdp 的 swiper `<script>` | ABORT，指名脚本没加载 |
| 删掉 `.swiper-wrapper` 的 `height: 100%` | 18 条红，5 页的 slide 高度全变 0 |
| 撤销 sticky 的 tablet 档 + bear 钉死 | 12 条红，含 1920 处 bear 涨到 140.2 |

**回归**：`rwd.py` 12×14 全绿；`r31`(52) / `r32`(42) / `r36` / `r39` / `r40` / `r41` / `r42` /
`r43` / `r44` / `r45` / `r48`(193) / `scrolllock`(32) 全过；`revealcheck` 入场归位；
`emptyline` 462 组合无空行盒；`platecheck` 瓣形全符。
`swiper` 类名在 HTML 里只出现在 5 个图廊页（其余 7 页 0 处），编译两次 md5 一致
`95aaa44b170ba2df4269f6e0adb8d1a5`。

### 文件清单

```
改  assets/customstyle.scss    1 stats__note −34；2 deco-bear 106×159.68 + tablet 斜坡；
                               3 新增 Vendor — Swiper 分区 + gb-product__image 重写；
                               4 三个弹窗加 --modal-exit；5 rv-panel__video hover；
                               6 footer-cta__btn hover / header__logo 去 hover；
                               7 highlight-card__text margin auto + PDP media sticky 768+；
                               8 science-card__value 手机档移去 --nutrient；
                               $build → 20260828-r50
改  assets/customstyle.css     编译产物
改  assets/main.js             gallery 模块改用 Swiper；modal 延迟解锁（modalExitMs / unlockAfter）
新  assets/swiper-bundle.min.js  Swiper 11.2.6（MIT）154KB
改  index / pdp / reviews / how-gumi-works / our-story.html
                               图廊加 .swiper / .swiper-wrapper / .swiper-slide + script 标签
改  全部 11 页 + font-check.html   ?v= / EXPECT_BUILD → r50（38 + 1 处）
新  tools/r50check.py          本轮 8 条的判据
改  tools/r36check.py          「1440 note margin-top 保持 −30」→ −34（本轮推翻，就地改注）
改  tools/r43check.py          「390 science value 36/40」→ 56/44（本轮撤回，就地改注）
```

### 遗留

- 待决 **Z / AA / AB / AC / AD / AE / AF** 见 PROJECT-STATUS。
- **顺带发现未修**：手机抽屉关闭时有和第 4 条一模一样的抖动（767 以下桌面窗口，
  实测 700 → 685）。修法同形，等授权。

---

## 第五十轮（2026-08-28）— 需求方对第四十九轮的四条回复

需求方逐条回了第四十九轮的交付：**第 6 条撤回**、**第 7 条改口径**、**第 8 条给了裁决**、
**第 3 条扩大范围到全站轮播**。`$build` → `20260828-r51`。

### 1. 第 6 条：footer CTA 的 hover 改回去

「第六条不改 footer cta」。恢复成翻白底（`background: $c-white; border-color: $c-white;
color: $c-green`），第四十九轮那次「照抄 `.gb-btn--primary`」作废。待决 **Z 关闭**。
`.gb-header__logo` 去 hover 不在撤回范围内，保持不变（待决 AA 仍开着）。

### 2. 第 7 条：sticky 不是 PDP 专属，767 以上每一页都钉

「gb-product__media 767 以上需要 sticky 在左边」。第四十九轮把 sticky 铺到了 768+，
但仍锁在 `.gb-product--page`（只有 PDP）。本轮**去掉 `--page` 限定**，
`.gb-product__media` 在所有五个有产品区块的页面（index / pdp / reviews / our-story /
how-gumi-works）都从 768 起吸顶，偏移量仍是 `calc(表头高 + 24)`。
判据把「图在左、信息在右」也钉了，且只在两栏并排时断言 —— 767 以下是上下堆叠的，
那里没有左右可言。待决 **AF 关闭**。

### 3. 第 8 条：手机与桌面同一套规格

「目前 gb-science-card 的 gb-science-card__value 的样式设计在手机上和 pc 端是一样的」。
第四十九轮把 36/40 挪到了 `.gb-science-card--nutrient` 上（为了保住 50% 组的板值），
本轮**连那份也删掉**：两组卡片、所有宽度都是 56/44、字距 0。
`.gb-science-card--nutrient` 现在只剩 `__body` 的 gap 覆盖。待决 **AB 关闭**。

⚠ 这一条**推翻了 50% 组自己的板值**（324:58044 画的是 36/40），已在源码注释里写明。

### 4. 第 3 条扩大：全站轮播都改 Swiper

「我发现其他轮播图都没有采用 swiper，轮播图都需要改为 swiper，原生处理后续可能会有
功能上的变化，swiper 的插件的开销值得用」。待决 **AE 关闭**（开销认了）。

除产品图廊外还有 **5 个 `[data-slider]`**，全部转过来了：

| 轮播 | 页面 | 卡数 | 形态 |
|---|---|---|---|
| reels 横轨 `.gb-reels` | index / pdp / our-story / how-gumi-works | 5 | 全出血，居中 |
| expert 卡片轨 `.gb-expert__cards` | reviews | 3 | ≤991 是轨，≥992 是三列网格 |

**原来是什么**：CSS 的 `overflow-x: auto` + `scroll-snap`，加约 270 行脚本做
克隆式无限循环、鼠标拖拽、拖后吞掉 click、居中停靠、箭头步进、跨断点拆装克隆。
**现在**：Swiper 拿走了平移、拖拽、惯性与防误点（`preventClicks` 默认开），
克隆机器、`wrap()`、`fill()`/`unfill()`、`_noClick` 全部删掉。

**配置写在 markup 上**，一个属性对一个 Swiper 选项，不看 JS 也知道这条轨在干什么：

```
[data-slider-rewind]         箭头到头绕回，不置灰
[data-slider-centre]         每个宽度都居中
[data-slider-centre-narrow]  只有 768 以下居中
[data-slider-step]           一次手势只走一张（longSwipes: false）
[data-slider-until="991"]    只在 ≤991 是轨；以上销毁 Swiper，CSS 另行排版
```

**`spaceBetween` 从 CSS 读**，不写死在 JS 里：轨道自己声明 `column-gap`（`.swiper` 是
`display:block`，这个属性在那儿不排任何版），脚本 `getComputedStyle` 拿到解析后的 px 交给
Swiper —— 间距的响应式斜坡仍然只有 SCSS 一个出处。**不能用自定义属性**：
`getComputedStyle` 读自定义属性拿到的是未求值的 `clamp(...)` 字符串
（[[custom-prop-computed-is-unevaluated]]）。

**⚠ 没有用 Swiper 的 `loop`**，原因见 PROJECT-STATUS 待决 AG：Swiper 11 是重排现有
slide 而不是复制 DOM，5 张卡填不满 1440 处 4.3 个可见位，右边空 232.5px。
改用「居中 + 从中间那张起步 + `rewind`」，这也正是板上的排布
（Reels Row 1617 宽、x = −88 = 五张卡居中两侧各探 88）。

**两处 Swiper 用不上、刻意保留原样**：

- **expert 轨 ≥992 不是「禁用 Swiper」而是销毁**。`breakpoints: {992: {enabled: false}}`
  只停交互，重排过的 slide 顺序留在 DOM 里，三列网格会照着那个顺序渲染。
  改用 `matchMedia` 建/毁，`destroy(true, true)` 连行内样式一起清掉。
  三列网格因此挂在 `.swiper-wrapper` 上（卡片真正的父元素），不在 `.gb-expert__cards` 上。
- **expert 轨容器的 `padding-inline` 删了**。Swiper 用 `clientWidth`（含 padding）量容器，
  带 padding 会让它以为地方比实际多，991 处整组左移 24px、第三张被切。
  那圈 padding 原本也没对齐任何东西 —— `scroll-padding` 是 0，旧轨道是贴视口边吸附的。

**键盘仍是自己的**：Swiper 的 keyboard 模块挂在 `document` 上，读者用方向键翻页时会被
抢走。监听留在轨道元素上，只在它有焦点时响应（reels 轨有 `tabindex="0"`）。

### 验证

**`tools/r50check.py` 加了第 9 节（全过）**。轮播的判据不是「有没有 `swiper-initialized`」——
那对一个塌成 0 高、或者右边空一大片的轨道照样成立。钉的是几何不变量：

- `spaceBetween` **等于 CSS 里声明的 `column-gap`**（防的是有人把数字写死进 JS）
- 卡片步距 == 卡宽 + gap
- **轨道两侧都不许留空**（这条正是 `loop` 踩的坑）；卡片装得下时改断言靠左排齐 ——
  991 处 3 × 305 + 2 × 19.5 = 954 装得进 976，剩下的 22 是本来就有的，不是空档
- expert 轨：≤991 Swiper 活着 + wrapper 是 flex + 导航可见；≥992 Swiper 销毁 +
  wrapper 是 grid + 导航隐藏
- 交互：箭头走一张、rewind 到头绕回且两个箭头都不置灰、轨道有焦点时方向键能翻、
  **点卡片开 reel 弹窗、拖一下不许把弹窗一起点开**

**几何回归**：改造前后各采一份 5 页 × 10 档的轨道几何（`.gb-reels` / `.gb-expert__cards`
的盒子、每张卡的 x/宽/高、gap、导航 display、横向溢出），
**50 个组合 0 处差异**（容差 0.7px，只比双方都可见的公共部分 —— 旧基线里有克隆）。

**活性自检**（两项，判据都报红）：

| 撤销 | 判据反应 |
|---|---|
| 改回 Swiper 的 `loop` + 从第一张起步 | 71 条红，index@1440 正好量出 232.5px 的右侧空档 |
| 把三列网格从 `.swiper-wrapper` 挪回容器 | 4 条红，992 以上 wrapper 仍是 flex |

**回归**：`rwd.py` 12×14 全绿；`r31`/`r32`/`r36`/`r39`/`r40`/`r41`/`r42`/`r43`/`r44`/`r45`/
`r48`/`scrolllock` 全过；`revealcheck` 入场归位。

### 文件清单

```
改  assets/customstyle.scss    6 footer-cta__btn hover 改回白底翻转；
                               7 sticky 去掉 --page 限定；
                               8 删掉 --nutrient 的图号覆盖，两组统一 56/44；
                               3 .gb-reels 去掉 overflow/snap/is-dragging，只留 column-gap；
                                 .gb-reel 改 width；.gb-expert__cards 网格移到 .swiper-wrapper、
                                 去掉 padding-inline；.gb-expert-card 去掉 scroll-snap；
                               $build → 20260828-r51
改  assets/customstyle.css     编译产物
改  assets/main.js             slider 模块整体重写在 Swiper 上（约 270 行 → 约 120 行）
改  index / pdp / our-story / how-gumi-works.html
                               reels 轨加 .swiper / .swiper-wrapper / .swiper-slide；
                               data-slider-loop → data-slider-rewind
改  reviews.html               expert 轨同上 + data-slider-until="991" data-slider-centre-narrow
改  全部 11 页 + font-check.html   ?v= / EXPECT_BUILD → r51（38 + 1 处）
改  tools/r50check.py          第 6/7/8 条按本轮口径改断言；新增第 9 节（全站轮播）
```

### 遗留

- 待决 **Z / AB / AE / AF 已关闭**；**AA / AC / AD** 仍开着；新增 **AG / AH**。
- **顺带发现未修（第四十九轮那条仍在）**：手机抽屉关闭时有和弹窗一样的抖动。

---

## 第五十一轮（2026-08-28）— 修改任务文档第二组 7 条

任务文档**追加**了第二组（md5 `72ef4f10…` → `85e228b6…`：第一组 1–8 条逐字未动，
末尾新增 7 条），全部落地。`$build` → `20260828-r52`。

### 1. 卡片阶梯的两个阈值：两列提前到 1200，一列统一到 575

「类似 gb-nutrition__cards 的 card 从 3→2→1 的 breakpoint，1200 以下变 2 个，
575 以下变 1 个，比如还有 gb-testimonials」。

站上跑这个阶梯的一共 **4 个组件、8 处**：

| 组件 | 页面 | 卡数 | 装置 |
|---|---|---|---|
| `.gb-science__cards` | index ×1、science ×2 | 3 | 网格：4 轨 + 每张 span 2 |
| `.gb-nutrition__cards` | index | 3 | 同上 |
| `.gb-story__inner` | our-story | 3 | 同上 |
| `.gb-testimonials` | index(3) / our-story(4) / how-gumi-works(4) | 3–4 | flex-wrap + basis |

**改的是阈值挂在哪，不是装置**。列数是排布，从值档 `tablet`(768–1280) / `narrow`(≤767)
搬到布局阈值 `tight`(≤1200)；gap 是数值，留在原来的值档上（铁律 18）。

⚠ **`tight` 块必须排在 `mobile` 块之前** —— 两个都是 `max-width` 查询、特异性相同，
唯一让 ≤575 保住单列的就是源码顺序。活性自检把两块对调，575/390 立刻退回两列。

⚠ **`max-width: 848px` 跟着两列态走**（science / nutrition）。它只约束两列态，
不是随视口变化的斜坡，所以和列数写在一起；单列档不需要重置（575 < 848）。

**testimonials 多改了一处**：三列态的下界从 1281 降到 1201 后，那里的行只有约 1060 宽，
装不下 `3 × 340 + 2 × 25`，第三张会被挤到第二行。基础的 `flex: 1 1 340px` 是**桌面值，
一个字都不能动**，所以在 `tablet` 档补了一个按容器解的 basis
`calc((100% - 2 * var(--gb-testi-gap)) / 3)`，并让它排在 `tight` 之前 ——
768–1200 由 `tight` 接管回两列，1281 以上两个都不匹配，桌面原样。

### 2. `.gb-product__info` 1200 以下去掉侧边 padding；`.gb-product__cta` 手机端加上限

- `padding: 0 32px` → `@include tight { padding: 0 }`。原来 `narrow` 里那条 `padding: 0`
  被 `tight` 完全覆盖，一并收掉，免得同一个属性散在两处。
- `.gb-product__cta` **需求没给数值** → 取 **520**，与 `.gb-product__media` 手机端的上限
  同值，按钮因此和它上方的产品图同宽（390 处列宽 350 < 520，稿上一字不变）。
  另配 `margin-inline: auto` —— 不居中的话它会贴着左边，而整列内容是居中的。
  → 待决 **AJ**。

### 3–7. promo 卡（只在 pdp.html，两张：green / white）

| 条 | 改动 | 备注 |
|---|---|---|
| 3 | `.gb-promo-card` narrow `max-width: 343` → **575** | 推翻板值 343（324:53792）|
| 4 | `.gb-promo-card--green .gb-promo-card__lip--v` `right: -63` → **-95** | 白卡的 `left: -63` 不动，从此不对称 |
| 5 | `.gb-promo-card__stack` narrow `max-width: 100%`；`.gb-promo-card__lip--h` `left: 53.5%` → **50.5%** | `__btn` 仍是 347（两者原来共用一条声明）|
| 6 | 白卡的 `.gb-promo-art__img` narrow `top` → **-8%** | 第四次改这个值 |
| 7 | `.gb-promo-card__list` narrow 去掉 `margin: 0 auto` | 关闭待决 I |

**第 5 条的 stack 与第 3 条是耦合的**：改前卡片只有 343 宽、body 内容宽 295，
`max-width: 347` 从来没生效过。是第 3 条把卡片放宽到 575（内容宽 527）之后，
那条 347 才开始真正掐住 stack。

**第 6 条必须写在 `.gb-promo-card--white` 作用域里**，不能直接改 `narrow` 的 -4%：
`.gb-promo-art` 还被 science / reviews 的 `.gb-ingredients__disc` 复用，
直接改会把 -8% 泼到那两页上。活性自检撤掉作用域，那两页立刻报红。
（顺带核实：绿卡根本没有 artwork 半边，promo 卡里的 `.gb-promo-art` 只有白卡一处。）

**第 7 条的实际效果不是「贴左」，是「居中后左移 7.5」**，这点值得写清楚：
去掉 `margin-left: auto` 之后没有 auto 外边距了，父容器的 `align-items: center` 接管，
右边那 15 把盒子推到中心偏左 7.5 —— 正是板上「hangs slightly left of centre」的样子。
**改前是反的**：唯一的 auto 左边距吃掉全部余量，把列表挂到了最**右**（390 实测左 24.39 / 右 15）。
待决 I 记的就是这个反向，本轮关闭。

### 验证

**新判据 `tools/r52check.py`（7 节，385 条断言，全过）**。取法上刻意避开三类恒真：

- **列数按行分组数，不数 x 的取值个数**。三张卡两列时落单那张是居中的，它与前两张
  谁的 x 都不同 —— 数 x 会把两列数成三列（第四十二轮踩过，坑 13）。
- **单列档的真正风险不是 `grid-template-columns`，是 span 没重置**：对着一条轨道，
  隐式网格会拿 `span 2` 再造出第二列，而属性读回来仍是 `1fr`，属性断言全绿。
  行数判据抓得住，活性自检也证实了（把 `tight` 挪到 `mobile` 后面，575/390 立刻退回两列）。
- **cta 的上限取盒子实际宽度**，不读 `max-width` 属性：它基础就有 `width: 100%`，
  属性断言分不清「上限生效了」和「容器本来就更窄」（第四十三轮坑 16）。
  另断言 768 处**不**受限，否则一条泼到全站的 `max-width` 也会全绿。

**双向验证**：同一份判据对着**改前的 CSS** 跑 —— **47 条红**，七条需求逐条都有对应的红
（1201 处 4 个组件 14 条 / testimonials 单列阈值 6 条 / info padding 6 条 / cta 5 条 /
promo-card 宽 7 条 / lip--v 3 条 / lip--h 3 条 / art top 3 条 / list 6 条）。

**活性自检**（四项逐个撤销，判据都报红）：

| 撤销 | 判据反应 |
|---|---|
| stack 的 `max-width: 100%`（卡片仍是 575） | 2 条红，767/576 处 stack 停在 347 |
| 把 science 的 `tight` 块挪到 `mobile` 之后 | 6 条红 = science 的 3 处 × 575/390 两档，与覆盖档位数精确相符 |
| testimonial 的 1201–1280 basis 回到 340 | 3 条红，三处 testimonials 在 1201 全部折成两列 |
| 第 6 条不加 `--white` 作用域 | 2 条红，science / reviews 的 ingredients 被泼成 -8% |

⚠ **第一项自检暴露了一条原本恒真的断言**：改前卡片只有 343 宽、body 内容宽 295，
`max-width: 347` 从来没生效过，所以「stack 铺满 body 内容宽」在改前也成立。
它只有在第 3 条把卡片放宽之后才有判别力 —— 双向验证里那 47 条红不含这一条，
是活性自检把它补上的。

**回归**：`rwd.py` 12 × 14 **全绿**；`revealcheck` 入场归位；`emptyline` 539 组合无空行盒；
`r32` / `r36` / `r42` / `r48`(193) / `r50`(612) 未受影响直接全过。

**本轮推翻的旧断言（7 个脚本 12 条，全部就地改注，没有一条是真回归）**：

| 脚本 | 原断言 | 现在 |
|---|---|---|
| `r31check` | science@700 `max-width: none` | `848px`（848 跟着两列态挂到了 `tight`；700 处仍然不构成约束）|
| `r39check` | 1280 nutrition 两列 | 档位换成 1200；plan 补采 1200 |
| `r40check` | 390 lip--h `183.5px` / art top −4% | `176.75px` / −8% |
| `r41check` | 1280 science 跑 4 轨 | 档位表去掉 1280 |
| `r43check` | 1280 grids 2 行 / art top −4% | 1 行 / −8% |
| `r44check` | 三页 art top 一律 −4% | pdp −8%、science / reviews 仍 −4%（同一块里对照，正好验作用域）|
| `r45check` | 1280 story 2 行 + 落单居中 | 1 行；居中档位换成 1200，plan 补采 1200 |

### 文件清单

```
改  assets/customstyle.scss    1 四个卡片组的阶梯阈值搬到 tight/mobile（science /
                                 nutrition / story / testimonials），testimonials 另加
                                 1201-1280 的三列 basis；
                               2 product__info padding → tight；product__cta 520 + 居中；
                               3 promo-card narrow max-width 343 → 575；
                               4 绿卡 lip--v right -63 → -95；
                               5 stack narrow max-width 100%；lip--h left 53.5% → 50.5%；
                               6 .gb-promo-card--white 作用域下 art__img top -8%；
                               7 promo-card__list narrow margin-left: 0；
                               $build → 20260828-r52
改  assets/customstyle.css     编译产物
改  全部 11 页 + font-check.html   ?v= / EXPECT_BUILD → r52（38 + 1 处，HTML 结构未动）
新  tools/r52check.py          本轮 7 条的判据（7 节 385 条）
改  tools/r31check.py          science@700 max-width none → 848px（本轮推翻，就地改注）
改  tools/r39check.py          nutrition 两列档 1280 → 1200；plan 补采 1200
改  tools/r40check.py          390 lip--h left → 176.75px；art top → -8%
改  tools/r41check.py          science 4 轨档位表去掉 1280
改  tools/r43check.py          1280 grids 2 行 → 1 行；art top → -8%
改  tools/r44check.py          art top 按页分档：pdp -8%，science/reviews 仍 -4%
改  tools/r45check.py          1280 story 2 行 → 1 行；居中档 1280 → 1200；plan 补采 1200
```

### 遗留

- 新增待决 **AI**（1201–1280 的三列比组件想要的窄）与 **AJ**（cta 上限 520 是推算值）。
- 待决 **I 关闭**（promo 列表的 margin 语义，本轮第 7 条给了裁决）。
- **顺带发现未修（第四十九轮起仍在）**：手机抽屉关闭时有和弹窗一样的横向抖动。

---

## 第五十二轮（2026-08-28）— 任务文档逐条复查 + 抽屉抖动 + 清掉四条恒假断言

任务文档**没有换版**（md5 仍是 `85e228b6…`）。本轮做三件事：把 15 条需求逐条对着实现复查一遍、
修掉第四十九轮起挂着的「顺带发现」、清掉 `font-check.html` 里的恒假断言。
`$build` → `20260828-r53`。

### 1. 15 条逐条复查 —— 全部按字面落实，没有「没修改成功」的

第四十二轮出现过需求方写「发现没有修改成功」，所以这次逐条实测，
重点看**判据可能取错量**的地方，而不是重跑一遍已经全绿的判据。

| 条 | 复查取的量 | 实测 |
|---|---|---|
| 一·5 | svg 里 `path` 真正渲染出来的 `fill`，不只是父元素的 `color` | 静止 `rgb(1,19,7)` → hover `rgb(0,86,53)`；底板 `rect` 恒为白 |
| 一·6 | hover 前后两次快照逐属性比对 | footer CTA 翻白底（第五十轮撤回后的口径）；`.gb-header__logo` 五个属性**一个都没变** |
| 一·7 | `__text` 与父盒的左右间隙；media 的 `position` 与「图在左」 | 左右各 45.8 对称；768/1024/1440 都是 `sticky` 且图在左，767 堆叠后转 `static` |
| 一·8 | 六张卡的 `font-size/line-height/letter-spacing` | 1440 与 390 全部 `56px/44px/normal`，两组一致 |
| 二·5 | `lip--h` 的 `left` 落在哪一档 | 只在 ≤767 `display:block`，`left: 50.5%` |

**一·5 的判据当时取弱了**：`r50check` 只读了 `.gb-rv-panel__video` 的 `color`。
glyph 用的是 `fill="currentColor"` 所以必然跟随，不算恒真，但需求写的是「hover svg 需要变色」，
断言就该落在 svg 上。已加强成两条：三角变绿 + 白色底板不跟着变（`r50check` 612 → 614 条）。

### 2. 手机抽屉关闭时的横向抖动（第四十九轮的「顺带发现」，本轮授权修）

与弹窗同形同病：`is-menu-open` 从前是在摘掉 `is-open` 的同一帧摘掉的，滚动条当场回来，
抽屉的包含块随之变窄，而它此刻还在滑出、完全看得见 —— 用户看到它横跳一个滚动条的宽度。

修法照 `modal.close()`：解锁推迟到滑出结束，时长由抽屉自己在 CSS 里用 `--modal-exit` 声明，
`main.js` 复用现成的 `modalExitMs()` 读它；令牌而不是 timer id，
滑出途中重新打开时上一次挂起的回调不许把新抽屉的锁解掉。

⚠ **判据抓出了第一版实现的错**：我先把 `--modal-exit: #{$t-panel}` 写在了
`.gb-header__panel` 的基础规则上。但**手机档的抽屉是另一套实现** ——
桌面是 `grid-template-rows` 收起的下拉（`$t-panel` 0.35s），
手机是 `position: fixed` + `translateX(-100%)` 滑出的抽屉（**`$t-drawer` 0.7s**），
而锁本身只在 `narrow` 生效。声明挂错了档、时长差一倍。
现在写在 `narrow` 档里，并在注释里点名「不是 $t-panel」。

### 3. `font-check.html` 四条恒假断言（待决 G 记了两条，实际是四条）

**「一个恒假的断言和恒真的一样有害：它训练人忽略那张表上的红色。」** 全部改写：

| 断言 | 为什么假 | 改成验什么 |
|---|---|---|
| 波浪归属（第十八轮） | 第十九轮把留高度的方案从 `::after` 换成 `padding-bottom: calc(… + var(--sc-lg-h))`，`::after` 的 `content` 读回 `none` | section 的 `padding-bottom` 覆盖了波浪高度（容差 1.2 吸收 `--wave-under` 的 1px 叠边） |
| 裁切型宿主（第十八轮） | **和 `::after` 无关**，待决 G 的归因不全：它要求 `padding-bottom` 恰好是 0，而 `.gb-nutrition` 实测是 **127.979** —— 裁切型宿主走的正是同一套 padding 机制 | 同上，外加 `--bleed` 的条带透明 |
| reels 拖动态关掉 snap（第十一轮） | **第五十轮引入、没人登记**：全站轮播改 Swiper 后 `.gb-reels` 的 `overflow` / `scroll-snap` / `is-dragging` 全撤了 | 轨道不再 snap、`overflow` 由 `.swiper` 提供、`column-gap` 仍在（它是 `main.js` 读 `spaceBetween` 的唯一出处）|
| 产品图库改叠放淡入（第十六轮） | **第四十九轮引入、没人登记**：堆叠与淡入交给 Swiper，slide 上再也看不到 `opacity` 规则 | vendor 分区真正提供的那部分：`transition-property: opacity` + 只有 active 那张接收指针事件 + `cursor: grab` |

改完 65 行的自检表**一条红都没有**。

### 4. AG 裁决落地：reels 换回无缝循环（加卡），expert 保持 rewind

需求方裁决「要无缝循环，得加卡」。**两条轨道的代价不一样，只做了一条**：

| 轨道 | 页 | 卡数 | 能不能加卡 |
|---|---|---|---|
| `.gb-reels` | index / pdp / our-story / how-gumi-works | 5 → **10** | 能。全断点都是轨道，加卡只是轨道上多几张，**不动布局** |
| `.gb-expert__cards` | reviews | 3，**未动** | 不能。**≥992 是三列网格**，补到 loop 需要的 9 张会把一行三张变成三行 —— 那是改桌面 |

Swiper 11 的 `loop` 是**重排**现有 slide 而不是复制 DOM，所以卡数必须超过可见张数的两倍
（1440 处可见 4.3 张 → 至少 9 张）。10 张是 5 的两倍，余量够且整齐。

**新增的 5 张是第 1 张的副本**（灰占位，`<!-- TODO client asset -->` 原样带着），
HTML 里加了注释说明它们**不是内容、是为了让 loop 有料可推**，
并登记进「交付前必须替换的占位内容」—— 真实 reels 到位后整组替换，张数由客户内容决定。

配置仍然写在 markup 上：`data-slider-rewind` → **`data-slider-loop`**。
`main.js` 里 loop 与 rewind 互斥（loop 优先），`initialSlide` 在 loop 下回到 0
（无限轨道没有「整组居中」可言），箭头的置灰逻辑对 loop 同样早退。

⚠ **代价（已知并接受）**：板上的排布是「五张卡居中、两侧各探出 88」
（Reels Row 1617 宽 / x = −88），那是**没有循环**时的取景。改成 loop 之后两侧永远盖满卡，
1440 静止时左侧探出 416 —— **和稿的取景不再一致**，这是无缝循环的固有代价。

### 验证

- **新判据 `tools/r53check.py` §1（抽屉，30 条）**，与 `r50check` 第 4 条同构：
  在滑出**中途**采样并同时断言那一刻抽屉还看得见；两条反向断言（锁最终必须解开、
  滑出途中重开时锁不许被旧定时器解掉）；**拿回真实滚动条**，gap 仍为 0 就 abort。
  ⚠ 只量抽屉**宽度**不量 x —— 手机档抽屉是 translateX 滑出的，x 在那段时间本来就在动。
- **活性自检（抽屉，两条路径各撤一次，都报红 9 条 = 3 页 × 3 条）**：
  改回同一帧立即解锁 / 撤掉 `--modal-exit` 声明，实测都量出 **700 → 685** 的 15px 横跳，
  与第四十九轮记录的数字一致。
- **活性自检（font-check 四条，逐条破坏对应机制，四条各自且只有自己报红）**：
  去掉 `.gb-product--lg` 的波浪高 / 把 `.gb-nutrition` 的 padding 归零 /
  抹掉 `.gb-reels` 的 `column-gap` / 把 `.swiper-fade` 的过渡属性换成 transform。
  **把恒假改成恒真同样有害，这一步是必须的。**
- **`tools/r53check.py` 加了 §2（reels 的无缝循环），全文件 249 条全过**。
  判据不取「两侧不留空」而取「两侧都**真的溢出**」：留空是正数、贴边是 0、盖满是负数，
  前两者对一个刚好排满的轨道也成立，只有负数才说明两头都还有卡可推。
  而且**走 8 张之后再量一次** —— 静止那一帧排得满，不代表推几张之后还满。
  另有一条前提断言「卡数 > 2 倍可见张数」：卡数掉到线下时 Swiper 会静默不循环，
  而 `params.loop` 照样报 `true`，只断言 loop 开着是抓不到的。
- **活性自检（AG，两项）**：
  - 撤掉 `data-slider-loop` 回到 rewind → **72 条红**；
  - **卡数减回 5、loop 仍开着 → 40 条红，实测右侧空 `232.5px`** ——
    与第五十轮记录的数字**一模一样**，等于把当时踩的那个坑原样复现了一遍。
- ⚠ **改注时踩到一个探针坑**：「走满一圈回到起点」这条断言，点击间隔原本沿用旧的
  260ms，而 Swiper 的 `speed` 是 **400ms** —— 动画途中的点击会被吞掉，
  点 10 次实际只走到第 6 张，断言报红但**页面是对的**。间隔改成 500ms 后通过。
  驱动轮播的判据，**点击间隔必须大于 `speed`**，否则量到的是探针自己的节奏。
- **本轮推翻的旧断言**：`r50check` 第 9 节 **91 / 614 条**（reels 的 5 张卡 / 不用 loop /
  用 rewind / 从中间起步 × 4 页 × 6 档，外加 3 条交互），全部就地改注 ——
  没有一条是真回归，都是 AG 裁决的直接结果。
- **回归**：`scrolllock`(32) / `r50check`(614) / `r52`(385) / `r39` / `r40` 全过；
  `rwd.py` 12 × 14 全绿（本轮动过 HTML 结构，必须重跑）；两次编译 md5 一致。

### 文件清单

```
改  assets/customstyle.scss    .gb-header__panel 的 narrow 档加 --modal-exit: $t-drawer；
                               $build → 20260828-r54
改  assets/customstyle.css     编译产物
改  assets/main.js             header.set() 关闭时推迟解锁 + lockToken（复用 modalExitMs）；
                               slider 支持 data-slider-loop —— 与 rewind 互斥、loop 下
                               initialSlide 归 0、箭头置灰逻辑一并早退
改  font-check.html            四条恒假断言改写（波浪归属 / 裁切型宿主 / reels / 产品图库）
改  index / pdp / our-story / how-gumi-works.html
                               reels 轨加第 6-10 张占位卡（第 1 张的副本 + 说明注释）；
                               data-slider-rewind → data-slider-loop
改  全部 11 页 + font-check.html   ?v= / EXPECT_BUILD → r54（38 + 1 处）
新  tools/r53check.py          §1 抽屉关闭不横跳（30 条）+ §2 reels 无缝循环（249 条）
改  tools/r50check.py          第 5 条加强：断言落到 svg 的 path/rect 上（612 → 614 条）；
                               第 9 节按 loop 口径改注（10 张 / loop / 非 rewind /
                               realIndex 起步 / 走满一圈回起点；pitch 改成按 x 排序算）
```

### 遗留

- 待决 **G / AA / AG / AI / AJ 关闭**（G 连带清掉两条没人登记的恒假断言；
  AA / AI / AJ 是需求方裁决「保持现状」；AG 裁决「加卡换回 loop」—— 见下）。
- 第四十九轮的「顺带发现未修」**已修完**。
- ⚠ **AG 只落地了 reels 那一半**：`.gb-expert__cards` 仍是 3 张卡 + `rewind`，
  因为它 ≥992 是三列网格，补到 loop 需要的 9 张会把一行三张变成三行 —— 那是改桌面，
  超出「加卡」这条授权。要不要一并做需要单独定。
- ⚠ **reels 的第 6–10 张是占位副本**，已登记进「交付前必须替换的占位内容」。
  真实内容替换时**不能少于 9 张**，否则 loop 会在一侧留空。
- 仍开着：A–D（稿冲突登记）/ E / F / K / L / N / O / P / Q / T / U / V / W / X / Y /
  AC / AD / AH。

## 第五十三轮（2026-08-30）— 任务文档换版后的第二、三组 13 条

任务文档**整份换版**（md5 `85e228b6…` → `2d70c334…`）：旧的第一组 1–8 条（stats note −34 /
deco-bear 钉死 / Swiper 图廊 …）整组消失，**现在的第一组 7 条就是第五十一轮做过的那批**
（逐条比对，一字未改）。真正的新需求是**第二组 8 条 + 第三组 8 条**。
其中 3 条挂起等裁决（见「待裁决」），其余 13 条全部落地。`$build` → `20260828-r55`。

### 二·1 promo 图片不再压到波浪上

`.gb-promo-art` 的手机宽度是写死的 `303px`（390 板值），而它所在的 `.gb-promo-card__art`
是 `aspect-ratio: 1`、跟着卡片一起缩。卡片越窄，方形的 art 半越矮，图却不动 ——
`.gb-promo-art__img` 还要 `height: 110%` 且 `top: -8%`，于是从 **~380 起就压到
`.gb-promo-card__lip--h` 上**。实测图与波浪的净距：767 → 65.3，575 → 54.8，390 → **5.8**，
360 → **−2.1**，320 → **−2.5**。

改成 `min(303px, 86.571%)`（86.571% = 303/350，即 390 板上的比例）：
**390 及以上一字不变**，390 以下图随卡片同步缩，间距按比例保住（360 → 9.5，320 → 14.2）。

⚠ 不能直接改 `narrow` 那条给 `.gb-promo-art` 加百分比就完事 —— `.gb-ingredients__disc
.gb-promo-art` 已经覆盖成 `82.19%`，science / reviews 两页走的是它，不受本条影响。

### 二·3 对比表在手机端占满宽度

`.gb-vs__table` 的 `narrow` 档有 `max-width: 400px`，575 处只占 400、两侧空 67.5。
需求要全宽，**但不能一路放到 767**：`.gb-vs__bear` 是这个盒子的百分比，右缘落在它的
**103.2%** 处，去掉 cap 后 767 实测文档宽 **771 > 视口 767**（700 也溢出 1.3）。
解方程 `20 + 1.0323T ≤ V` 得全宽只在 **V ≤ 659** 安全。

所以落在值档 `mobile`（≤575）上，写在 `narrow` 块**之后**（同为 `max-width` 查询、
特异性相同，源码顺序是唯一的胜负依据）。576–767 保留 400 的 cap。
→ 要不要连熊一起重排以便一路全宽，登记待决 **AL**。

### 二·4 弹窗一出现，关闭按钮就描一圈深色边

不是 border（全局 reset 早就 `button { border: 0 }`），是 **focus ring**。
`modal.open()` 里 `el.querySelector(FOCUSABLE).focus()` 取到的第一个可聚焦元素**就是**
`.gb-promo-panel__close`；这个弹窗是定时自动弹出的，脚本 focus 之前没有任何指针输入，
Chrome 因此判定为 `:focus-visible`，画出全局的 `outline: 2px solid $c-green`
（实测 `rgb(0,86,53)` solid 2px + offset 2px）—— 正是需求方看到的深色边。

改成 ARIA 对话框的标准做法：三个 `role="dialog"` 容器加 `tabindex="-1"`，
`open()` 改为 `el.focus()`。容器不是交互控件，所以给它关掉 ring。
Tab 陷阱不受影响 —— `FOCUSABLE` 里的 `[tabindex]:not([tabindex="-1"])` 本来就排除了它。

### 二·6 / 二·7 四个上限与一个百分比

| 条 | 改动 | 备注 |
|---|---|---|
| 6a | `.gb-bear-meter` narrow `max-width: 100%`（原 347） | 575 处实测由 347 放开 |
| 6b | `.gb-header__nav .gb-btn--lg` `max-width: 520px` | **需求没给数值**，取 520 = `.gb-product__cta` 的同值（第五十一轮）。767 处原本 727 宽。左对齐不居中——auto 外边距会把它推离左对齐的链接 → 待决 **AM** |
| 7a | `.gb-footer__newsletter` narrow `max-width: 340px` | 与 `stack` 档同值 |
| 7b | `.gb-deco-bear--b` `top` 改百分比 | 见下 |

**7b 推翻了源码里一条写明理由的决策**。原注释：「top stays in px on purpose: it resolves
against `.gb-footer-cta-wrap`, whose height is the CTA's copy block, not a design constant」。
需求方明确要百分比，照做，两档各自按**自己的板**换算，板上分毫不差：

- pc：`408 / 573.94 = 71.087%`（1440 实测偏移 408.0）
- narrow：`457 / 524.02 = 87.211%`（390 实测偏移 457.0）
- **tablet 档只能留 px** —— `fluid()` 用 calc 插值，百分比没法这么斜坡（铁律 18）

⚠ **代价已量化**：wrap 的高度本身随宽度变（1440/1600/1920 都是 573.94，1281 是 563.45；
390 是 524.02，767 是 463.97，320 是 588.02）。离开板宽后熊会漂：
**1281 处 −7.4px，767 处 −52.4px，320 处 +55.8px**。文案多一行也会带着它走。
→ 待决 **AK**，登记进「不要报成 bug」。

### 二·8 数字描边里的白斑

`50%` 的 `0` 字怀中间有一道白缝，`50` 与 `%` 之间也有一小块 —— `ink-outline()` 是把
字形按半径做圆盘膨胀，字怀的内切圆半径比 **7px（0.125em @56）** 大，中心就填不满，
露出的是卡片的白底。95% 那组同样有（需求方举的是 50% 这一例）。

判据不靠眼睛：把卡片背景换成哨兵色 `#ff00ff`，截 4× 图，**从图像边界做 flood fill，
数「填不到的洋红像素」= 封闭的洞**。逐档试半径：

| 半径 | 洞像素 |
|---|---|
| 0.125em（原值） | **272** |
| 0.135em | 61 |
| **0.145em** | **0** |
| 0.155em / 0.17em / 0.19em | 0 |

取**恰好归零**的 0.145em。外轮廓因此粗 1.1px（7 → 8.12 @56），偏离 Figma 的 7px 板值 ——
这是「白斑必须消失」的最小代价。单位是 em，所以三·1 把手机端降到 36px 之后描边同步缩。

### 三·1 tight 那组的间距与手机端数字

- `.gb-science--tight .gb-science__cards { margin-top: 26px }` —— **叠在既有的 gap 上**，
  不是替换：桌面 22 + 26，手机 48 + 26。需求给的是裸值，照落。
- `.gb-science-card__text { margin-top: 6px }` —— 需求这一句**没写作用域**，而上一句
  明明白白写了完整类链，差别是有意的，所以落在全局：index 3 张 + science 6 张都吃到。
  → 待决 **AN**（如果只想要 tight 那组，把它挪进作用域即可）。
- 手机端 `.gb-science-card__value` **36 / 40 / −0.36px**。需求写的 `letter-spacing: -1%`
  CSS 没有这个单位，−1% @36 就是 −0.36px；`font-style: Fizzy Heavy` 不是合法的
  `font-style` 值（Fizzy Heavy 是 PP Palma 的一个裁切，靠 family + weight 选，已经在用），跳过。

⚠ **这条第二次反转**：第四十九轮刚把手机端从 36/40 拉回板值 56/44，本轮又改回去。
`tools/r50check.py` 第 8 节（30 条）、`r43check` 2 条随之改注 —— 留着不动，
下一轮回归会把需求方的裁决当 bug 修掉。
需求里没提 768–1280，但**不补斜坡 767/768 就会跳 20px**，所以补了 `fluid(36px, 56px)` 等，
并在 `r50check` 里加了三条新断言钉住这个斜坡（落在 36–56 之间、单调不倒挂、767/768 连续）。

### 三·2 FAQ 图文块的侧边槽是桌面独有的

`.gb-faq-image__body` 的 `padding-inline: 32px` 基础值在 768–1280 仍然生效，
而 `narrow` 早就归零了。基础值不能删（那是桌面板值，桌面一个字不能动），
所以在 `tablet` 档补 `padding-inline: 0` —— **≤1280 全是 0，≥1281 保持 32**，两档一致。

### 三·5 / 6 / 7 表单三条

- **勾选框改成画的**：原生 `input[type=checkbox]` 靠 `accent-color` 上色，**它不参与过渡**
  （需求说的「点击没有过渡效果」根因就在这里）。改为 input 走 `visually-hidden`、
  `.gb-form__check::before` 画方框、`:has(input:checked)::before` 切绿底 + 勾。
  ⚠ **不是 `display: none`** —— 那会把控件移出 Tab 顺序，连浏览器的 required 提示气泡
  一起弄丢。判据里两条都钉了：input 仍可聚焦、`display != none`。
  ⚠ 判据用**真实鼠标点在画出来的方框上**，不是 `input.checked = true`：用户能点到的
  只有伪元素，只有真实点击才验得到「label 仍把点击转发给隐藏的控件」。
- `.gb-form__note a` 加下划线（referral 页）。
- `.gb-form__disclaimer` 手机端 `margin: 16px 0 -2px`，并补了 tablet 斜坡把 −2 收回 0。
  `r48check` 第 17 条随之改注（它原本假定上下 margin 共用一个数）。

### 三·8 长文页的入场

`.gb-rich-page__inner` 加 `wowo fadeInUp`（privacy-policy / shipping）。

⚠ **挂在 `__inner` 上而不是需求写的 `.gb-rich-page` 本身**：那是整块白底 section，
`.wowo{opacity:0}` 会把**背景一起吃掉**，进视口前露出 body 底色
（[[reveal-opacity-exposes-body-bg]]）。判据里钉了 section 的 `opacity` 恒为 1、
背景恒为白，以及内容最终回到 `opacity: 1`。

### 验证

- **新判据 `tools/r55check.py`，95 条全过**，覆盖落地的 13 条。
- **双向判据**：`tools/_reverse_r55.py` 用 `ast` 解出 `_apply_r55.py` 里的 `(old, new)` 对
  **逆序**套回（顺序很重要——二·8 改过的那行是三·1c 的上下文，正序撤销会匹配不上），
  重建改前的 scss/js/html，重编译后 `r55check` **报 50 条红**，13 条改动每一条都有对应的红。
  改后恢复，`customstyle.css` 与反向前**字节一致**。
- **「有没有波及别处」**：改前 / 改后各采一次全站 11 页 × (1440, 390) 的元素矩形，按 DOM
  路径配对（本轮不增删节点，路径是稳定键）。
  ⚠ **先测了探针自己的噪声地板**：同一状态连采两次，15 个页-档、1724 个矩形有差，
  最大 **2.60px**（lineReveal 分行 + Swiper + 字体加载竞态）。低于这个数的差异一律不算信号。
  地板之上的差异**全部归因**，且数值精确对上：
  - `index` **+6**（3 张卡 × text margin 6；390 是 +18 − value 行高 −12 = +6）
  - `science` **+38**（1440：两组各 +6 = 12，加 tight 的 26；390：6 张 +36 − 行高 −24 + 26）
  - `referral` **−18**（disclaimer 下边距 16 → −2）
  - checkbox 20×20 → 1×1、newsletter 350 → 340、`gb-promo-art`、`gb-deco-bear--b`
  - 各页下游 section 的整块位移量**与上游变化量完全相等**（6 / 38 / 18），是结果不是新问题
  - `gb-logo-scroll__track`（每 400ms 走 ~18px）与 `gb-stats__bear-art`（浮动 + 缩放）
    是**持续动画的采样相位差**，同一状态连采 5 次逐次都在动，与本轮无关
- **回归**：`r31/r32/r36/r39/r40/r41/r42/r43/r44/r45/r48/r50/r52/r53` 全过
  （`r39` / `r43` / `r48` / `r50` 四份就地改注，见下）；
  `rwd.py` 12 × 14 **全绿**（本轮动过 HTML，必跑）；`revealcheck.py` 全部 opacity=1；
  `scrolllock.py` 32 条全过；两次编译 md5 一致（`f7c81a99…`）。
- **本轮推翻的旧断言**（都不是回归，全是需求方裁决的直接结果）：
  - `r50check` 第 8 节：「所有档 56/44/normal」→ 按档分（≥1281 板值 / ≤767 客户值 /
    768–1280 斜坡），并**新增三条**钉住斜坡本身
  - `r43check` 2 条：390 的 56/44 → 36/40
  - `r48check` 第 17 条：disclaimer 上下 margin 不再同值
  - `r39check` 2 条：`.gb-deco-bear--b` 的 top 现在是百分比，**永远读不回字符串 `"408px"`**
    —— 改成比数值（容差 0.6）

### 文件清单

```
改  assets/customstyle.scss    17 处（见 tools/_apply_r55.py 的 EDITS）；$build → 20260828-r55
改  assets/customstyle.css     编译产物
改  assets/main.js             modal.open() 改为 el.focus()（对话框自己接焦点）
改  全部 11 页                 role="dialog" 加 tabindex="-1"（10 处）；?v= → r55
改  privacy-policy / shipping.html   .gb-rich-page__inner 加 wowo fadeInUp
改  font-check.html            EXPECT_BUILD → r55
新  tools/r55check.py          本轮 13 条的定向判据（95 条）
新  tools/_apply_r55.py        本轮 SCSS 改动的 (old, new) 对，双向判据靠它重放
新  tools/_reverse_r55.py      逆序套回，重建改前状态
改  tools/r39check.py          2 条改注（bear 的 top 是百分比）
改  tools/r43check.py          2 条改注（390 数字回 36/40）
改  tools/r48check.py          第 17 条改注（disclaimer 上下 margin 不同值）
改  tools/r50check.py          第 8 节按档重写 + 新增 3 条斜坡断言（614 → 608 条）
```

### 逐条复查（换角度取量，不重跑已全绿的判据）

13 条对着实现逐条实测，**全部按字面落实，没有「没修改成功」的**。补了三个 `r55check`
从没覆盖到的真空档，另有三条换了取量角度：

| 条 | 复查取的量（与 r55check 不同的角度） | 实测 |
|---|---|---|
| 二·8 | **手机档 36px 下的描边**（r55check 只验过 1440/56px） | 390 / 575 / 767 / 768 / 1024 五档、两组卡，洞像素**全为 0** —— `em` 单位让半径随字号缩，字怀也同步缩 |
| 三·8 | **真实滚动路径**的入场（r55check 是手动加 `animated`） | 两页首屏内，`ready` 兜底那一次就跑掉了，首帧 `opacity` 已是 1；1.5s 后 `wowo` / `animated` 都已自清，只剩 `fadeInUp` |
| 二·4 | 走**真实 `data-modal` 点击**开弹窗，读焦点落点 | 焦点在 `DIV.gb-nl-modal is-open`，关闭按钮 `:focus-visible=false`、`outline: none` |
| 二·1 | **图片墨迹**而不是边界盒（留白取自 PNG 的 alpha 通道，实测下缘 2.65%） | 320→20.3 / 360→16.3 / 375→14.8 / **390→13.4（最紧）** / 414→19.7 / 575→62.3 / 767→72.9，全部为正 |
| 三·5 | **键盘 Space** 切换（r55check 用的是鼠标） | 切换成功，方框转绿，且 ring 画在**画出来的方框**上而不是消失 |
| 三·1 | **视觉间距**而不是 `margin-top` | tight 组 head→cards = **48** = gap 22 + margin 26 ✓ |

⚠ **复查里报红的三次全是探针自己的毛病，不是页面的** —— 已写进 HANDOFF「三、探针假信号类」：
两个元素共享一张截图时量到了另一个（波浪盖过图片）、圆角污染了 ink bbox 的基准色、
`animated` 加上就立刻取量读到 `fadeInUp` 30px 位移的中途值（48 − 30 = 18）。

⚠ `r55check.py` 会在 `tools/` 下生成一张临时截图，**已改成退出前自删** ——
snap chromium 读不到 `/tmp`，探针文件只能落项目内，留着会被同步脚本当成本轮改动推上线。

### 待裁决（本轮未动手的 3 条 + 5 个新待决）

**未动手，等回复**：

1. **第二组·2 与第一组·7 直接对撞**。第一组·7（= 第五十一轮已落地）要求
   `.gb-promo-card__list` 在 767 以下**去掉** `margin: 0 auto`，据此关闭了待决 I；
   第二组·2 要求**保持** `margin: 0 auto`。去掉之后的实际效果是「居中后左移 7.5」，
   正是板上 *hangs slightly left of centre* 的样子；加回去会变成正居中。
   **需要确认是要正居中，还是这条只是没看到上一轮的结果。**
2. **第二组·5「promo-modal 到手机端才全屏」**与第二十七轮的决策冲突 ——
   平板档（768–1280）走手机那套全屏堆叠布局是那一轮定的，双栏只在 ≥1281。
   稿上**只有 1440 和 390 两档、没有 tablet 稿**，中间那一带要改成什么形态没有板可依。
3. **第三组·4「select 改成 ul 点击下拉」**。这是把原生 `<select>` 换成自定义控件，
   牵涉键盘导航、`aria-expanded`、表单提交值三块，比其余条目大一个量级；
   而且 Shopify 主题化之后表单很可能由 app 接管（联系表单的预填逻辑是照搬 Funky 站点的）。
   **要不要现在做，需要先定。**

**已落地但需要过目**：**AK**（bear 百分比的漂移量）/ **AL**（vs 表能否一路全宽）/
**AM**（抽屉按钮 520 是取的值不是板值）/ **AN**（card text 的 6px 该不该限定在 tight 组）/
**AO**（数字描边 0.145em 偏离板值 1.1px）。

### 遗留

- **第三组·3 语义不明，未动手**：「`gb-reviews gb-reviews--cream` 多了一个 `gb-testimonial`
  文本内容对齐 pc 端」。实测 our-story / how-gumi-works 的 `--cream` 版确实是 **4 张**
  （index 是 3 张），第 4 张单独落到第二行居中；但**四张卡在 1440 / 1024 / 768 / 390
  四档下的 `text-align` 全是 `center`，子元素也全是 center，与 pc 端没有任何差别**。
  需要需求方说清是「第 4 张要对齐到第一列而不是居中」，还是别的意思。→ 待决 **AP**
- 上一轮的遗留照旧：`.gb-expert__cards` 仍是 3 张 + rewind（AG 只落地了 reels 那一半）；
  reels 第 6–10 张是占位副本。
- 仍开着：A–D / E / F / K / L / N / O / P / Q / T / U / V / W / X / Y / AC / AD / AH，
  本轮新增 AK / AL / AM / AN / AO / AP。

---

## 第五十四轮（2026-08-31）— 三条挂起的需求按最新任务文档落地

任务文档**未换版**（md5 仍是 `2d70c334…`，与第五十三轮记录的同一份）。本轮做的是
第五十三轮挂起等裁决的三条 —— 需求方指示「按最新需求」，即以任务文档字面为准。
`$build` → `20260831-r56`。

### AQ 第二组·2 —— promo 列表回到正居中（**反转第五十一轮**）

第一组·7（第五十一轮落地）要求 `.gb-promo-card__list` 在 ≤767 **去掉** `margin: 0 auto`，
第二组·2 要求**保持**它。第二组是较新的一批，按它落。

要真正做到「保持 `margin: 0 auto`」，那条 `margin-right: 15px` 必须一起去掉 ——
**一个 auto 边距对上一个固定边距，盒子会被推到最右**，正是第五十一轮之前的样子
（390 实测左 24.4 / 右 15）。所以 `narrow` 与 `tablet` 两条覆盖整块删除，只留基础的
`margin: 0 auto`。

实测中心偏移（相对 `.gb-promo-card__stack` 内容盒中心，正数为偏右）：

| 视口 | 改前 | 改后 |
|---|---|---|
| 320 / 390 / 575 / 767 | −7.50 | **0.00** |
| 768 | +30.70 | **0.00** |
| 1024 | +37.20 | **0.00** |
| 1280 | +43.69 | **0.00** |
| 1440 | 0.00 | 0.00（本来就居中） |

⚠ 板上这份列表本来就是 *hangs slightly left of centre*，第五十一轮复刻的就是那个。
现在是正居中，**与板不一致，是需求方裁决**。→ 待决 **I 重新打开**。

### AR 第二组·5 —— 弹窗只在手机端全屏

「手机端」按本项目一贯口径取 **≤767**（值档 `narrow`，与第五十三轮三·1 同）。
768–1280 **没有板**，两条路都试过判据：

- 让桌面的双栏卡片提前到 768 —— 桌面卡是 1062 = 531 + 531，768 视口减去 24 的沟槽只剩
  720，两栏必须缩；而 `.gb-promo-panel__bears` 的 `left: -86.84px / width: 624.54px`
  是按 531 那一栏解出来的 px，栏一窄熊就被 `overflow: hidden` 切掉。**等于自造数值**。
- **落地的是这条**：这一档显示**手机板自己的尺寸** —— `285:19373` 是 **390×744**，
  堆叠布局里每一个值（art 252、熊的偏移、波浪的 71 内缩）都已经解在 390 上，
  `justify-content: space-between` 也照旧落在板的 32 间距上（744 − 460 − 252）。
  **一个自造数值都没有。**

同时给 `.gb-promo-modal__wrap` 的 `tablet` 档补上和 pc 一样的 24 沟槽。

⚠ **连带修掉一处会漏的**：`.gb-promo-panel__art` 的波浪读的是站点变量
`--sc-w`（`clamp(144.64px, 21vw, 302.19px)`，跟视口走）。卡片钉在 390 而波浪不钉，
就会在一张手机尺寸的卡里画一条桌面尺寸的波浪 —— 实测 1280 处节距 **268.8**，
板是 144.85。所以 `tablet` 档把 `--sc-w` 钉回 **144.64px**（就是这条斜坡自己的下界，
也就是任何手机宽度都会解到的值）。截图肉眼确认过 768 / 1024 两档。

| 视口 | 面板 | 圆角 | 沟槽 | 波浪节距 |
|---|---|---|---|---|
| 320–767 | 视口满屏 | 0 | 0 | 随视口（不变） |
| 768 / 900 / 1024 / 1280 | **390×744** | 24 | 24 | **144.63**（板值） |
| 1281 / 1440 | 1062×528 双栏（不动） | 24 | 24 | 桌面栏无波浪 |

短视口 1024×600 实测面板高 552 = 600 − 48，`max-height` 让位而不是撑破沟槽。

### AS 第三组·4 —— 询问类型改成按钮 + ul 下拉

**做法是渐进增强，不是替换**：原生 `<select>` 留在 DOM 里，既是选项的唯一来源，
也是表单的取值载体 —— 提交照旧 post `enquiry`，`enquiryPrefill` 的 `?type=` 照旧生效，
脚本挂了用户看到的就是原生控件（没有任何门控 class 去藏它）。
`main.js` 新增 `selectBox` 模块，`data-select` 是 hook（铁律 17），注册在
`enquiryPrefill` **之后**，这样按钮打开时显示的是已经预选好的那一项。

- 结构：`div.gb-select` >（被 `visually-hidden` 的原生 select）+ `button` + `ul[role=listbox]`。
  **不是 `display: none`** —— 那会把控件移出 Tab 顺序，连浏览器的必填提示气泡一起弄丢
  （与第五十三轮的勾选框同一条理由）。
- 箭头**必须是元素**才能转：背景图 `background-image` 无法 `transform`。
  改成内联 SVG（同一条 path），`.gb-select.is-open` 时 `rotate(180deg)`，走 `trans(transform)`。
- 标签：`<label for="enquiry">` 原本指向现在已经离屏的控件。`button` 不是可被 label
  标注的元素，所以 JS 摘掉 `for`、给 label 一个 id、按钮走 `aria-labelledby`，
  并补一条点击 label 聚焦按钮的监听。
- 键盘走 ARIA listbox 模式：**ul 自己拿焦点、移动 `aria-activedescendant`**，
  任何一个 `li` 都不带 tabindex。按钮上 ↓/↑/Enter/Space 开；列表里 ↑↓/Home/End 移动、
  Enter/Space 选定并回焦按钮、Esc 关闭并回焦、Tab 关闭；点击列表外关闭。
  **首字母 typeahead 没做**（原生 select 有）→ 待决 **AW**。
- 选定时写回 `native.selectedIndex` 并 `dispatchEvent(new Event('change'))`，
  后续接 Shopify app / 校验的代码听的是真控件。
- 列表 `overflow-y: auto`（上限 224），**建出来时自己挂 `data-lenis-prevent`** ——
  它是在 `smoothScroll.init()` 扫过 DOM 之后才存在的；`PREVENT` 名单里也补了一条。
- **电话里的国家码 `<select>` 没动** —— 需求只点名 `gb-field__input--select`（铁律 20）。
  → 待决 **AV**。

### 验证

- **新判据 `tools/r56check.py`，140 条全过**。
- **双向判据**：`tools/_reverse_r56.py` 用 `ast` 解出 `_apply_r56.py`（SCSS 6 对）与
  `_apply_r56_js.py`（JS 4 对）的 `(old, new)` **逆序**套回、并撤掉 HTML 的 `data-select`，
  重建改前状态 → `r56check` 报 **65 条红**，三条需求每一条都有对应的红；
  恢复后 `customstyle.css` 与反向前 **md5 一致**（`ca9ad7ec…`）。
  ⚠ 脚本里加了一道守卫：改前状态下整个下拉控件不存在，没有守卫会在第一个缺失节点上
  **抛异常中断**而不是把剩下的判据报成红。
- **「有没有波及别处」**：改前 / 改后各采一次全站 11 页 ×（1440, 390）的元素矩形，按 DOM
  路径配对。
  - 先测噪声地板：同一状态连采两次，18 个页-档有差，最大 **4.13px**（logo 跑马灯 +
    stats 小熊浮动的采样相位差）。低于这个数不算信号。
  - 地板之上只有 `pdp.html@390` 的 **16 处 × 7.50px** —— 就是 AQ 那一列，
    **只有 x 变，w/h/y 全不动**；`index.html` 那两处 4.30 / 11.40 落在
    `gb-stats__bear-art` 上，与噪声同源。
  - 新增 / 消失路径 30 / 10 个，**全部在 get-in-touch 的第 5 个字段内部**：
    `SELECT` 换成 `DIV.gb-select`（占同一个子槽位），后面的兄弟下标一个没错位。
    **字段盒 1440 处 624×70、390 处 350×70，改前改后逐位相同；其后的字段与提交按钮差 0。**
  - 弹窗是 `position: fixed`，AR 对页面流零影响。
- **回归**：`r31/r32/r36/r39/r40/r41/r42/r43/r44/r45/r48/r50/r52/r53/r55` 全过
  （`r40` / `r52` 两份就地改注，见下）；`rwd.py` 12 × 14 **全绿**（动过 HTML，必跑）；
  `revealcheck` 全部 opacity=1；`scrolllock` 32 条全过；`hardbreaks` 恒定 34 ok / 6 MISSING；
  `platecheck` / `seamcheck`（0 条发丝线）全过；两次编译 md5 一致。
- **本轮推翻的旧断言**（不是回归，是需求方裁决的直接结果）：
  - `r40check` 1 条：`390 promo list margin-right == 15px` → 改成**两侧 margin 对称**
    （auto 边距的 used value 是像素，390 处两侧各 23.19）
  - `r52check` 3 组 6 条：「右侧空隙比左侧多 15 / `margin-left == 0px`」→ 改成
    **两侧空隙相等 / 两侧 margin 相等**
- **肉眼复核**：768 / 1024 / 390 三档弹窗 + 下拉的收起 / 展开 / 键盘态各出一张图，
  确认圆角、居中、波浪节距、箭头朝向、活动项高亮。⚠ 图与临时截图脚本**已按铁律 21 删除**
  （落在项目内会被同步脚本当成本轮改动推上线）。

### 文件清单

```
改  assets/customstyle.scss      6 处（见 tools/_apply_r56.py 的 EDITS）；$build → 20260831-r56
改  assets/customstyle.css       编译产物
改  assets/main.js               新增 selectBox 模块；PREVENT 补 .gb-select__list；模块表 + window.gumi 各注册一次
改  get-in-touch.html            enquiry 的 <select> 加 data-select
改  全部 11 页 + font-check.html  ?v= / EXPECT_BUILD → 20260831-r56（39 处）
新  tools/r56check.py            本轮三条的定向判据（140 条）
新  tools/_apply_r56.py          SCSS 改动的 (old, new) 对
新  tools/_apply_r56_js.py       main.js 改动的 (old, new) 对
新  tools/_reverse_r56.py        逆序套回 scss + js + html，重建改前状态
改  tools/r40check.py            1 条改注（promo 列表两侧对称）
改  tools/r52check.py            3 条改注（同上）
```

### 待裁决（本轮新开）

- **I（重新打开）** —— promo 列表现在是正居中，板上是「居中后左移 7.5」。
  两次反转都由需求方点名，需要确认这次是终版。
- **AT** —— 768–1280 的弹窗形态取的是「手机板 390×744 居中」。**这一档没有板**，
  取值有依据（每个数都是手机板的）但不是板给的这一档。要不要改成别的形态（例如让桌面
  双栏提前，代价是熊被裁）需要拍板；1280 处这张卡只占视口的 30%。
- **AU** —— 「手机端」判成 ≤767。需求原话没给阈值，本项目一贯是这个口径。
- **AV** —— 电话里的国家码 `<select>` 仍是原生的（需求只点名了询问类型那一个）。要不要一起改。
- **AW** —— 自定义下拉没做首字母 typeahead，原生 `<select>` 是有的。
  另外主题化之后这个表单很可能由 app 接管，这个控件届时可能作废。

### 遗留

- 上一轮的遗留照旧：**AP**（第三组·3 语义不明，未动手）、`.gb-expert__cards` 仍是 3 张 +
  rewind、reels 第 6–10 张是占位副本。
- 仍开着：A–F / **I** / J–L / N–Q / T–Y / AA / AC / AD / AG / AH / AI / AJ / AK–AP，
  本轮新增 **AT / AU / AV / AW**。

---

## 第五十五轮（2026-08-31）— 需求方对第五十四轮五条待决的回复

第五十四轮把五条待决摆给需求方，回复是：
**1 = pc 端居中、手机端去掉居中；2 = 我把 AT 说糊了（待重问）；3 忽略；4 一起改；5 忽略。**
落地两条（撤回 + AV），两条按「忽略」保持现状，一条待重问。`$build` → `20260831-r57`。

### I（关闭）—— 撤回第五十四轮的居中，回到第五十一轮

需求方最终裁决：**pc 端居中，手机端去掉居中**。第五十四轮那次「全档正居中」撤回。

⚠ **这条已经反转三次，判据里三处都钉了「这是终版」**：
r40（固定 `margin-right: 15px`）→ r51（`narrow` 补 `margin-left: 0`，成为板上的「居中后左移 7.5」）
→ r56（两条覆盖全删，正居中）→ **r57 回到 r51**。

**顺带把 r51 漏掉的一处补上**：r51 只在 `narrow` 档补了 `margin-left: 0`，
`tablet`（768–1280）那条 `margin-right: fluid(15px, 0px)` 的 `margin-left` 仍然是基础的
`auto` —— **一个 auto 边距对上一个固定边距会把盒子吸到另一边**，实测这一档一直在
**往右挂**：768 处 **+30.7**、1024 **+37.2**、1280 **+43.7**，夹在一个往左挂 7.5 的手机档
和一个正居中的 pc 档中间。`tablet` 也补 `margin-left: 0` 之后，15 顺着斜坡收到 0，
两端连续（767/768 与 1280/1281 各自实测连续），全程没有任何一档往右挂。

### AV —— 国家码 select 一起改（`get-in-touch` + `referral` 两页）

同一个 `selectBox` 模块加一个 **`bare` 变体**（`data-select="bare"`）：
`.gb-field__phone` 本身已经画了边框，所以这个触发器**不带自己的盒子**，只继承原生
select 那套排版（16 / 24 / −0.32 / `$c-gray-700`）。

- 触发器只挂 `gb-select__button`，**不挂** `gb-field__input --select`（挂了会在电话框里再
  画一个 44 高的白盒）。
- 原生的 `padding-right: 23px` = 20 的箭头 + 3 的空隙 → 变体写成 `padding-right: 0` + `gap: 3`。
- 这个控件**没有 `<label for>`**，只有 `aria-label="Country code"` → JS 把它转写到按钮和列表上
  （有 label 的走 `aria-labelledby`，两条路互斥）。
- 列表挂在**电话框的下边缘**而不是触发器下边缘：触发器是 22 内容盒里的一个 24 行盒，
  它自己的 `100%` 比框底短 10px，所以 `top: calc(100% + 14px)`（10 + 默认的 4）。
  实测两页都是**离框底正好 4**。左对齐触发器、`width: max-content`（触发器只有 "AU" 那么宽）。
- ⚠ **一处会漏的**：`.gb-field__phone select`（0-1-1）压过 `.gb-select__native`（0-1-0），
  隐藏起来的原生控件**仍然拿着 23 的 padding-right**，实测宽 23px 而不是 `visually-hidden`
  的 1px。改成 `select:not(.gb-select__native)` —— 脚本没跑时没有这个 class，回退路径不受影响。
- 焦点在按钮上时 `.gb-field__phone:focus-within` 照常把框描成绿色（实测 `rgb(0,86,53)`）。
- 一页两个控件互不干扰：开国家码不会开询问类型；点询问类型会把国家码当「外部点击」关掉。

### 未动的三条

- **AU（3 忽略）** —— 「手机端」继续按 ≤767。
- **AW（5 忽略）** —— 自定义下拉不做首字母 typeahead。
- **AT（2）** —— 需求方说「糊了」，即第五十四轮那条我没讲清楚。**待重问，本轮未动**，
  768–1280 的弹窗仍是手机板的 390×744 居中卡片。

### 验证

⚠ **本轮验证不完整，是需求方叫停的** —— 下一轮接手请先补跑下面「未跑」那几项。

**已跑，全过：**

- `tools/r57check.py` **93 条全过**（AV 的结构 / 排版 / ARIA / 几何 / 层叠 / focus-within /
  键盘 / 表单取值 / 六档无横向溢出 / 两控件互不干扰）
- `tools/r56check.py` **149 条全过** —— AQ 段已按终版重写（≤767 挂左 7.5、768–1280 的
  `−mr/2` 斜坡且单调、≥1281 居中、两个档界连续、**没有任何一档往右挂**）
- **双向判据**：`tools/_reverse_r57.py` 逆序套回 scss(4 对) + js(4 对) + 两页 html，
  重建改前状态 → `r57check` **0 ok / 29 红**、`r56check` 的 AQ 段 **19 红**；
  恢复后 `customstyle.css` md5 与反向前**一致**（`66d1b6a5…`）
- 回归：`r31`（1 条改注后全过）/ `r32` / `r36` / `r39` / `r40`（已还原）/ `r41` /
  `r42` / `r43` / `r44` / `r45` / `r48` / `r50` / `r52`（已还原）全过

**未跑（下一轮必补）：**

- `rwd.py` —— **本轮动过两页 HTML，按规矩必跑**
- `r53check` / `r55check`
- `scrolllock` / `revealcheck` / `hardbreaks` / `platecheck` / `seamcheck` —— 这几份最后一次
  跑是第五十四轮，本轮的改动不涉及它们的对象，但没有复跑过
- `font-check.html` 自检页
- 「有没有波及别处」的全站矩形比对（第五十四轮做过一次，本轮没做）
- ⚠ `r52check` 最后一次跑是在本轮后两处 SCSS 改动（列表间距 13→14、
  `select:not(.gb-select__native)`）**之前**，两处都只作用于电话字段，但没有复跑过

**本轮推翻的旧断言**（都是需求方裁决的直接结果）：

- `r40check` 1 条、`r52check` 3 组 6 条 —— 第五十四轮改成的「两侧对称」**全部还原**成
  r51 的「右侧比左侧多 15 / `margin-left: 0`」，并在注释里写明**这是终版**
- `r31check` 1 条 —— `.gb-field__phone select {padding-right} == 23px` 现在读到的是隐藏的
  原生控件（0px）。改成读**画出来的触发器**的排版两条；23 的去处在 `r57check` 的
  「padding-right 0 / gap 3」一对里

### 文件清单

```
改  assets/customstyle.scss   4 处（见 tools/_apply_r57.py 的 EDITS）；$build → 20260831-r57
改  assets/customstyle.css    编译产物
改  assets/main.js            selectBox 加 bare 变体 + aria-label 兜底（4 处）
改  get-in-touch.html         国家码 <select> 加 data-select="bare"
改  referral.html             同上
改  全部 11 页 + font-check.html  ?v= / EXPECT_BUILD → 20260831-r57（39 处）
新  tools/r57check.py         本轮判据（93 条）
新  tools/_apply_r57.py       SCSS 改动的 (old, new) 对
新  tools/_apply_r57_js.py    main.js 改动的 (old, new) 对
新  tools/_reverse_r57.py     逆序套回 scss + js + html
改  tools/r56check.py         AQ 段按终版重写；AS 段的选择器收紧到 #enquiry-*（一页现在有两个控件）
改  tools/r31check.py         1 条改注
改  tools/r40check.py         1 条还原
改  tools/r52check.py         3 组 6 条还原
```

### 待裁决

- **AT（重问）** —— 第五十四轮我没把这条讲清楚。要问的其实只有一句：
  **768–1280 这一档（平板 / 小笔记本）的邮件弹窗，你想看到什么形态？**
  现在是「手机板原尺寸 390×744 的居中卡片」，1280 处约占视口 30%。
- 仍开着：A–F / J–L / N–Q / T–Y / AA / AC / AD / AG / AH / AI / AJ / AK–AP / **AT**。
  **I 本轮关闭**（终版：pc 居中、手机端不居中）；**AU / AV / AW 本轮关闭**
  （AU、AW 需求方选择忽略，AV 已落地）。

---

## 第五十六轮（2026-08-31）— 白卡的竖向波浪也往外挂

需求（对话追加，任务文档未换版，md5 仍 `2d70c334…`）：
**`.gb-promo-card--white .gb-promo-card__lip--v` `left: -100px`，响应式同步修改。**
`$build` → `20260831-r58`。

### 这是第五十一轮那条的延续

第五十一轮（第二组第 4 条）把**绿卡**的 `lip--v` 从对称的 `right: -63` 推到 `-95`，
当时白卡没动、从此不对称。本轮把白卡也推出去：

| | 声明 | 咬进相邻半边 | 占 126 盒子 |
|---|---|---|---|
| 绿卡（第五十一轮） | `right: -95px` | 31 | 24.6% |
| 白卡（改前） | `left: -63px` | 63 | 50%（对称骑缝） |
| **白卡（本轮）** | **`left: -100px`** | **26** | **20.6%** |

`lip--v` 是 126×764 的一列圆（r 63、圆心间距 106），挂在图片半边上、用**卡片自己的底色**
去咬相邻那半边。所以「探出多少」= 那一半的边缘之外有多少，剩下的才是看得见的咬痕。

### 「响应式同步修改」落在哪里

`.gb-promo-card__lip--v` **在 ≤767 是 `display: none`**（手机端改画横向的 `lip--h`），
而白卡这条声明**本来就没有分档** —— 也就是说，768 以上每一档都吃这一条，改一处即全档同步。
实测 768 / 900 / 1024 / 1200 / 1280 / 1440 六档咬痕**恒为 26**，卡片自己从 728 缩到 1062
的过程中不漂；判据里另加一条「768 与 1440 的咬痕不得有差」钉住「它确实是一个值、不是斜坡」。

⚠ **唯一没有跟着动的是手机档**（≤767 的 `lip--h`，`bottom: -48px`，咬痕 34.4 / 占 41.7%）。
需求点名的是 `lip--v`，按铁律 20 没有顺手改，且把手机档按新比例换算出来的数（−65）
是自造值。→ 待决 **AX**，见下。

### 验证

- **新判据 `tools/r58check.py`，44 条全过**：六档咬痕 26 / 盒子仍是板上的 126 /
  波浪不越出 `overflow:hidden` 的卡片 / **绿卡作为对照组仍是 31、位置不动** /
  四个手机档 `lip--v` 不画且 `lip--h` 仍在 −48 / 390 手机咬痕仍是 34.4。
- **双向判据**：`tools/_reverse_r58.py` 套回后 `r58check` **报 6 条红**（正好六档的白卡咬痕），
  恢复后 css md5 一致（`13e7107…`）。
- **回归**：`r31` / `r40` / `r44` / `r52` / `r55` / `r56` / `r57` 全过
  （`r52check` 1 条就地改注，见下）。
- **肉眼复核**：白卡 768 / 1024 / 1440、绿卡三档各出一张图，确认波浪仍读得出是波浪、
  与绿卡观感一致。⚠ 图与临时截图脚本**已按铁律 21 删除**。
- ⚠ **未跑**：`rwd.py`（本轮只改一个 `left` 且卡片是 `overflow:hidden`，不可能产生横向溢出，
  HTML 除 `?v=` 外未动）、`r53check` / `r55check` 之外的其余通用脚本
  （`scrolllock` / `revealcheck` / `hardbreaks` / `platecheck` / `seamcheck` / `font-check` /
  矩形波及比对）—— 与第五十五轮欠的是同一批，**下一轮一并补跑**。

**本轮推翻的旧断言**：`r52check` 1 条 —— 「白卡 lip--v 左探出**仍是 63**」（第五十一轮把白卡
当对照组钉住的）改成 100，并在注释里写明是需求方本轮的裁决；同节表头一并改。

### 文件清单

```
改  assets/customstyle.scss   2 处（见 tools/_apply_r58.py 的 EDITS）；$build → 20260831-r58
改  assets/customstyle.css    编译产物
改  全部 11 页 + font-check.html  ?v= / EXPECT_BUILD → 20260831-r58（39 处）
新  tools/r58check.py         本轮判据（44 条）
新  tools/_apply_r58.py       SCSS 改动的 (old, new) 对
新  tools/_reverse_r58.py     逆序套回
改  tools/r52check.py         1 条改注 + 同节表头
```

### 待裁决

- **AX. 手机端的波浪要不要跟着变浅** —— 本轮只动了 768 以上的竖向波浪（咬痕 63 → 26，
  占 50% → 20.6%）。手机端画的是另一个元素 `lip--h`（`bottom: -48px`，咬痕 34.4，占 41.7%），
  **没动**。要按同一比例跟过去的话是 `bottom: -65px` 左右，但那是**换算出来的数、不是稿上的**，
  且需求只点名了 `lip--v`。**要不要一起变浅？要的话给个数还是按比例换算？**
- **AT** 仍待重问（768–1280 的邮件弹窗形态）。

---

## 第五十七轮（2026-08-31）— 全站补上 favicon

需求（对话追加）：**网站的 favicon 换成设计里的 GUMI logo。**
改前**全站 12 页一个 `rel="icon"` 都没有**，浏览器标签页只有默认的空白图标。

### 素材不是我画的，是站上现成的锁定组合

设计源里**没有 favicon 帧**（`figma/assets-raw/` 与 `figma/nodes/` 都搜不到 logo / favicon /
mark 命名的素材，只有 `Logo` 这种字标帧，比例 2.4:1 不是方的）。所以问题变成
「用哪一套现成的组合」，而不是「画一个」。

站上有两套 GUMI 字标：header 的 `#005635` 绿字（浅底），footer 的 **`#B5ED61` 青柠字**。
后者背后的底色**是实测出来的**（顺着 `.gb-footer__logo` 往上找第一个非透明背景）：
`rgb(0, 65, 40)` = **`#004128`** = `$c-green-900`，**不是** `$c-green` 的 `#005635` ——
第一版按 `#005635` 做了，判据当场报红，改成实测值。

于是 favicon = **`#004128` 方底 + footer 那四条 path 原封不动的青柠字标**。
颜色和字形全部来自稿，唯一由我定的是版式：64 的方画布、字标占 78% 宽居中
（给 iOS 的圆角遮罩留安全区）、**不做圆角**（iOS / Android 自己会遮，浏览器标签页不需要）。

### 产出三个文件（`images/`，与本项目「图片放顶层 images/」的约定一致）

| 文件 | 用途 |
|---|---|
| `images/favicon.svg` | 现代浏览器标签页，矢量 |
| `images/favicon.ico` | 老浏览器与「保存到桌面」，内含 16 / 32 / 48 三档 |
| `images/favicon-180.png` | iOS 主屏图标（`apple-touch-icon`，**必须不透明**，iOS 会把它合成到底色上） |

PNG / ICO 都是**从这份 SVG 渲染出来的**（headless chromium 截图 → Pillow 写多档 ico），
不是另画一份，改 SVG 重跑即可同步。

### 挂载

12 页（11 个交付页 + `font-check.html`）的 `<head>` 里、`customstyle.css` 那条之前插入三行：

```html
<link rel="icon" href="images/favicon.ico?v=20260831-r58" sizes="32x32">
<link rel="icon" href="images/favicon.svg?v=20260831-r58" type="image/svg+xml">
<link rel="apple-touch-icon" href="images/favicon-180.png?v=20260831-r58">
```

⚠ **顺序有意义**：浏览器取**最后一条它认得的 `rel="icon"`**，所以 `.ico` 在前、`.svg` 在后，
认得 SVG 的（现在所有主流浏览器）拿矢量，不认得的退回 `.ico`。

⚠ **`$build` 没有升**：`customstyle.scss` 与 `main.js` 一个字没动，破缓存那条规矩针对的是
CSS/JS。三条链接带上当前的 `?v=20260831-r58`，下次升版时会跟着一起被 `sed` 替换掉。

### 验证

- **新判据 `tools/r59check.py`，96 条全过**，分六节：
  - **文件**：三个都在、非空、`apple-touch-icon` 是 180×180 **且完全不透明**、
    `.ico` 里确实有 16/32/48 三档
  - **出处**（这节是重点）：favicon 里的四条 `d` 与 `index.html` 里
    `.gb-footer__logo` 的四条**逐字节相同** —— 证明是搬过来的不是重画的。
    ⚠ 先断言「footer logo 还在」，否则选择器取空会让比对恒真
  - **配色**：底色取 footer logo 背后**实测**的 `rgb(0, 65, 40)`，不是 grep CSS 文本
    （第一版就是 grep 错了规则，把 `.gb-footer` 当成了上色的那一层）
  - **渲染**：角落像素等于底色、青柠像素占比落在合理区间（**空方块会被抓出来**）、
    iOS 圆角会遮掉的那 12×12 角落里没有画东西
  - **挂载**：12 页各三条、`.ico` 在 `.svg` 前、每个 href 在盘上都找得到、三条都在样式表之前
  - **浏览器**：三个文件都能在 chromium 里解码，SVG 的 viewBox 是正方（否则标签页图标会被压扁）
- **活性自检跑了四组，每组都报红**（判据不是恒真的）：
  删掉 svg → 2 红；改一条 path 里的一个数 → 「逐字节相同」报红；
  某页漏挂一条 → 该页两条断言报红；底色换成 `#005635` → 配色那条报红。
- **没跑别的**：本轮只往 `<head>` 加了三行 `<link>` 和三个新图片文件，
  CSS / JS / DOM 结构一个字没动，不影响任何布局判据。
  第五十五轮欠的那批（`rwd.py` / `r53check` / `scrolllock` / `revealcheck` / `hardbreaks` /
  `platecheck` / `seamcheck` / `font-check` / 矩形波及比对）**仍然欠着**。

### 文件清单

```
新  images/favicon.svg          64x64，#004128 底 + footer 那四条 path 的青柠字标
新  images/favicon.ico          从 svg 渲染，含 16/32/48
新  images/favicon-180.png      从 svg 渲染，apple-touch-icon，不透明
改  全部 12 页（11 交付页 + font-check）  <head> 里加三条 <link>
新  tools/r59check.py           本轮判据（96 条）
新  tools/_apply_r59_html.py    挂载脚本（幂等：已挂过的页会跳过）
```

### 待裁决

- **AY. favicon 的版式是我定的** —— 稿里没有 favicon 帧。字形与两个颜色都来自 footer 的
  现成锁定组合，但**方底、78% 的字标宽、不做圆角**这三项没有稿背书。
  另外**四个字母在 16px 的标签页上基本读不出来**（只看得出是一块深绿底 + 一抹青柠），
  这是所有多字母字标做 favicon 的通病。**要不要改成只取一个 `G`？** 那样 16px 下认得出，
  但不再是完整字标。
- **AX**（手机端 `lip--h` 要不要跟着变浅）与 **AT**（768–1280 的弹窗形态）仍待回复。

---

## 第五十八轮（2026-09-01）— 购物车抽屉

需求（对话，任务文档未换版，md5 仍 `2d70c334…`）：**把 cart 对照设计做出来。**
`$build` → `20260901-r59`。

### 先纠正了前提：这四个 frame 不是页面，是抽屉

`341:42573` / `336:36516`（有货）+ `341:42749` / `336:34942`（空车）四个 frame，
之前 57 轮从没动过。桌面那两个是 **1440×768 的画布上放一层 `rgba(0,0,0,.5)` 遮罩
加一个 391 宽的右侧面板**，不是 1440 宽的页面内容。手机那两个顶部 96 高的
`chrome-browser`（`gumi.com.au` + 一张截图）和末尾 78 高的 home indicator 是
**mockup 假舞台**，按 [[figma-modal-mockup-includes-fake-staging]] 不做。

三项由需求方当场拍板：**① 做成全站 drawer 挂 header 购物车图标**（不新建页面）；
**② 两个状态都做**；**③ 视觉壳 + 开关抽屉**，购物车数据归 Shopify。

### 没写一行新 JS：`modal` 模块本来就是通用的

`modal` 是事件委托 + `data-modal="id"`，滚动锁补偿、focus trap、Esc、Lenis 暂停全都现成。
header 那个 `aria-label="Cart"` 的 `<a>` 加一个 `data-modal="gb-cart"` 就接上了。
**唯一必须记得的是给根元素写 `--modal-exit`** —— 漏了会退回立即解锁，
panel 在滑出途中横跳一个滚动条宽（第四十九轮修过的那个）。本轮值取 `$t-drawer`。

⚠ **滑入不是淡入**：稿画的是侧滑，且它与手机菜单同族（`$t-drawer` 0.7s + `$ease-drawer`）。
第二十八轮「全站弹窗改纯淡入淡出」针对的是**居中弹窗**，不含侧边抽屉。**这条是我定的，
需求方只说了「可以」**，要推翻随时说 → 待决 BC。

### 空态的两张卡直接复用 `.gb-nav-card`

稿里空态那两张 169×169 的卡（Shop Gumi / Refer a Friend）与 header 导航卡**是同一个组件**，
而 `.gb-nav-card` 的 `narrow` 档逐值就是稿上的样子（169 / pad 16 / r8 / 12·18·−0.24 / action 32）。
所以没有重造，只在 cart 作用域里把它锁到那一档 —— 面板恒 391 宽，视口在桌面档时
卡片不能跟着长到 193。

⚠ **`.gb-nav-card__art` 有一道门**：它 `display:none` 直到 `.gb-header.is-open`，
这一对（加 `loading="lazy"`）才是把 312KB 小熊挡在网络之外的东西。cart 是这张卡的
**第二个宿主**，得有自己的门：`.gb-cart.is-open .gb-nav-card__art { display: block }`。
漏了这条，空态两张卡永远是空的底色。

### 稿自身的三处，没有照做

- **桌面稿有两个 total 块**：一个在流里（被面板 768 高裁掉，看不见），一个
  `position:absolute at 0,648`（648+120=768，钉底）。手机稿只有一个 —— 它的面板是
  hug 到 1100，`48+48+602+278+120+4×1` 正好。**实现成一个 sticky 底栏**。
- **`totals` 的 344 与 bar 的 343**：两个块的父级都是 auto-layout（可用 351），
  子块却是 fixed 宽，而且**两个值还不一样**。判定是手拖的残留不是设计语言，
  按 fill 351 做 —— 否则 Subtotal 的 `$60` 和 Total 的 `$45` 会互相错开 1px。→ 待决 BA
- **产品缩略图 56×56 与礼物图 47×47 在稿里是 `#D9D9D9` 实心占位**。
  按铁律 3 保留占位色块，没拿 `product-pack.png` 顶上去。→ 待决 AZ

### 过程中揪出来的三个真问题

1. **全局 `p{letter-spacing:-0.32px}` 漏进了六个 `<p>`**（ship / sum / grand-row /
   pay-note / bar-total / empty-title）。稿上这些文本一个都没有字距。
   六处显式补 `letter-spacing: normal`。
2. **Figma 的描边是 `strokeAlign: INSIDE`** —— 稿上的 184（item）/ 102×40（步进器）/
   114（礼物卡）**已经含了那 1px**，而 CSS 的 border 在 padding 盒之外。
   三处把 padding 各减 1（`23px 0 24px` / `9px 11px` / `15px`），几何才逐位对上。
   步进器的 count 因此是 `min-width: 30px`（2 border + 22 pad + 32 icon + 16 gap = 72，102−72）。
3. **`.gb-cart__body` / `__empty` 没登记进 `smoothScroll.PREVENT`** ——
   `rwd.py` 11 页 × 14 档全红「滚轮黑洞」。Lenis 会把滚轮全吃掉，抽屉内容根本滚不动。
   `main.js` 里那份清单的注释写着 REGISTER EVERY NEW overflow-y:auto CONTAINER，
   就地补上，这是本轮唯一动过的 JS。

### 判据自己的两个空洞（都补上了）

- **`backgroundColor` 是恒真的量**：遮罩的 `rgba(0,0,0,.5)` 无论 opacity 是 0 还是 1
  都读得到。截图复看时才发现这条什么都没验。改成**读实际画出来的像素**：
  打开前 `(26,26,26)` → 打开后 `(13,13,13)`，正好是 50% 叠加。
- **`scrolllock.py` 的采样盲区**：它的文档假设「闲置覆盖层靠 `checkVisibility()` 自动排除」，
  但**手机抽屉是用 `translateX(-100%)` 停在画外的**，`checkVisibility()` 仍为 true。
  以前 8 个用例里它要么是被测的 overlay 本身、要么在桌面档 `display:none`，一直没露出来；
  本轮加的 `get-in-touch@700` 第一次让它和另一个覆盖层同框，报了 53 处「移位」。
  那是 HANDOFF 2b 明确豁免的行为（fixed 盒子的包含块是视口）且在画外没人看得见 ——
  判据改成**只判视口内的元素**。

### 验证

- **`tools/r60check.py` 242 条全过**，八节：挂载（11 页 + font-check 反证）/
  出处（内联图标的 `d` 与导出件逐字节相同，5 个支付图标整文件逐字节相同，先断言源文件只有一条 path
  否则计数恒真）/ 几何 / 排版与颜色 / 文案 / 行为 / 空态 / 响应式八档
- **双向判据 `tools/_reverse_r60.py`**：抽掉 drawer + scss 分区 + 三个色值 →
  `r60check` **25 ok / 226 红**；恢复后 `customstyle.css` md5 与反向前**一致**（`df7a0c69…`）
- **`scrolllock.py` 加了 3 个 cart 用例**，44 条 / 11 用例全过。
  **活性自检**：把 `html.is-modal-open` 的 `padding-right` 打掉 → **11 个用例全红**
  （cart 三个各报 281 / 185 / 146 处移位），还原后回到 44/0
- **`rwd.py` 11 页 × 14 档全绿**（本轮动过 11 页 HTML 结构，按规矩必跑）
- **回归**：`r31` / `r32` / `r36` / `r39` / `r40` / `r41` / `r42` / `r43` / `r44` /
  `r45` / `r48` / `r50` / `r52` / `r53` / `r55` / `r56` / `r57` 全过。
  `r19check` 8 条、`r20check` 1 条仍红 —— **是既往遗留**，本文第 662 行记过，与本轮无关
- **对稿**：四个状态各截一张与 Figma 截图逐块比对，含空态小熊的裁切位置、
  礼物卡被 sticky 底栏裁掉的位置
- 两次编译 md5 一致（`df7a0c69…`）

**没跑**：第五十五轮欠的那批（`r53check` 本轮跑了，其余 `revealcheck` / `hardbreaks` /
`platecheck` / `seamcheck` / `font-check.html` / 全站矩形波及比对）—— **需求方明确说先不做**。

### 文件清单

```
改  assets/customstyle.scss   新增 Cart drawer 分区（Modals 与 Motion 之间）+ 三个色值
                             （$c-blue / $c-gray-400 / $c-gray-150）；$build → 20260901-r59
改  assets/customstyle.css    编译产物
改  assets/main.js            smoothScroll.PREVENT 补 .gb-cart__body, .gb-cart__empty（唯一一处）
改  11 个交付页               header cart 链接加 data-modal；</body> 前插 drawer 标记
改  全部 12 页                ?v= / EXPECT_BUILD → 20260901-r59
新  images/pay-{visa,mastercard,applepay,amex,paypal}.svg   与导出件逐字节相同
新  tools/r60check.py         本轮判据（242 条）
新  tools/_apply_r60_html.py  挂载脚本（幂等，图标 path 运行时从 figma 源读）
新  tools/_reverse_r60.py     反向套回 + --restore
改  tools/scrolllock.py       加 3 个 cart 用例；采样排除画外元素
```

### 待裁决

- **AZ. 产品缩略图与礼物图是稿里的 `#D9D9D9` 占位** —— 现在照样是灰块。
  要用 `product-pack.png` 吗？礼物那张 47×47 站上没有对应素材。
- **BA. `totals` 的 344 / bar 的 343 我按 fill 351 做了** —— 两个值不一致，判定是手拖残留。
  要按稿钉死就说一声。
- **BB. 空态的 Secure Checkout 只有视觉禁用**（`pointer-events:none`），没有 `aria-disabled` ——
  静态站里状态是手改属性，没有 JS 同步；真实状态以后由 Shopify 给。
- **BC. 抽屉用滑入不是淡入** —— 见上文，这条是我定的。
- 仍开着：A–F / J–L / N–Q / T–Y / AA / AC / AD / AG / AH / AI / AJ / AK–AP / AT / AX / AY。

---

## 第五十九轮（2026-09-01）— 弹窗改双栏 + 购物车下拉与五处取值

需求（对话，任务文档未换版，md5 仍 `2d70c334…`）五条：
**① `.gb-promo-panel` 767 以上一直用 row；② `.gb-cart-item__interval` 点击出下拉；
③ `__remove` 18×20；④ `__price` gap 6；⑤ `__gift-body` gap 10；⑥ `__lines` 手机端 padding 26/20。**
`$build` → `20260901-r60`。

### ① 这条就是待决 AT 的答案，AT 关闭

AT 问的是「768–1280 这一档的弹窗想要什么形态」。旧答案是**手机板 390×744 的居中卡片**
（好处是每个数都停在自己的板宽上，零自造）；AT 里也写明了另一条路的代价：
「1062 = 531 + 531 在 720 的可用宽里必须缩栏，而熊的偏移是解在 531 上的 px，
缩栏就被 `overflow: hidden` 切掉 —— 那才是自造数值」。**需求方选了另一条路。**

**做法是缩放，不是重排** —— 于是那个代价不成立：

```scss
--pp-k: calc(min(1062px, 100vw - 48px) / 1062px);   // 1 at >=1110
@include panel-wide { ... width: 1062px; height: 528px; zoom: var(--pp-k); }
```

`zoom` 而不是 `transform`：transform 会把原尺寸的盒子留在布局里，居中就废了。
`@include pc` 的 9 个块整体改成 `@include panel-wide`（`min-width: 768`），
**块里一个数都没动** —— 531 / -86.84 / 624.54 / 126 / 764 / 63 / 106.36 / 403 / 40
全是板值，由 --pp-k 统一缩。768 处整张卡是 720×358、两栏各 360；1110 起回到 1062×528。
自造的只有 --pp-k 这一个式子，48 是 wrap 自己的两个 24 gutter。

⚠ 顺带清掉两处死代码：`@include tablet { --sc-w: 144.64px }`（那一档不再画手机波浪）
和 panel 的 390×744 块。

### ② 下拉复用 `selectBox`，加第三个变体

interval 从 `<button>` 换成真的 `<select data-select="inline">`，模块照旧在它上面画控件 ——
**没有为 cart 写第二套下拉**。模块的三元判断改成变体名驱动：

```js
var variant = native.getAttribute("data-select") || "";     // "" | "bare" | "inline"
var boxless = variant === "bare" || variant === "inline";
```

⚠ 箭头的 `stroke` 由写死的 `#4d4d4d` 改成 `currentColor` —— 既有两个触发器的 color
本来就是 `$c-gray-700`（`.gb-field__input` 与 `--bare` 都是），**实测改后仍是
`rgb(77,77,77)`，等价**；cart 这个要跟着自己的蓝。
板上 cart 的 16 chevron 与模块的 20 chevron **是同一个 vee**（都在视口的一半上，
相对描边也一致），所以直接用模块的、CSS 设 16 ——`desktop-cart-icon-6` 不再内联。

**列表放不下就往上开**（新能力，对三个变体都生效）：

```js
if (this.wouldOverflow(box)) { box.wrap.classList.add("is-up"); }
```

两个坑都是实测抓出来的：

- **判断不能读 list 自己的 rect** —— 入场的 4px 位移正在跑，`getBoundingClientRect()`
  拿到的是过渡的起始值，差的那点正好让 640 高的视口漏判（实测溢出 2px 却没翻）。
  改成 `wrap.top + computed(top) + offsetHeight`，三个量都不受 transform 影响。
- **判断要放在 `move()` 之后** —— `move()` 里的 `scrollIntoView` 会滚动祖先，
  把先前测好的位置挪走。
- 镜像偏移一开始写成 12，**是我算错了**（以为触发器上下不对称）。`.gb-field__input`
  上下 padding 都是 10，所以向上也是 10 + 4 = **14**；改后两页实测都是离字段边缘正好 4。

⚠ 这个翻转**改变了既有控件的行为**：`get-in-touch` / `referral` 的国家码字段在页面靠底，
实测向下展开会到 909 而视口只有 900 —— 以前有 9px 在视口外，现在往上开。
`r57check` 那条「离框底 4」改成「离框边 4，向下或向上」。

### ③–⑥ 四处取值，全部推翻板值

| 位置 | 板 | 客户 |
|---|---|---|
| `.gb-cart-item__remove` | 16×20 | **18×20** |
| `.gb-cart-item__price` gap | 4 | **6** |
| `.gb-cart__gift-body` gap | 8 | **10** |
| `.gb-cart__lines` padding（≤767） | 24/20 | **26/20** |

四处都在注释里标了 `client r59, board says N`，`r60check` 的对应断言就地改掉并注明。

### 验证

- **`tools/r61check.py` 151 条全过**：promo 面板 11 档（方向 / zoom / 盒子 / 两栏 /
  塞得进 gutter / 竖缝 / 手机波浪开关）、下拉（结构 / 5 个选项 / 默认选中 / ARIA /
  lenis-prevent / 排版 / 箭头 / 选中写回 native / 键盘 / Esc 不关抽屉）、
  六档视口高的翻转（**每档都断言上下都没被裁**）、既有两个控件未受影响、手机端 padding
- **双向判据 `tools/_reverse_r61.py`**（scss + js + 11 页三处一起套回）：
  `r61check` **60 ok / 91 红**；恢复后 `customstyle.css` md5 与反向前**一致**（`75bc87d8…`）
- **回归全过**：`r31` / `r32` / `r36` / `r39` / `r40` / `r41` / `r42` / `r43` / `r44` /
  `r45` / `r48` / `r50` / `r52` / `r53` / `r55` / `r58` / `r59` / `r60`（240 条）；
  `rwd.py` 11 页 × 14 档全绿；`scrolllock` 44 条 / 11 用例全过
- 两次编译 md5 一致（`c396aa43…`）

**本轮推翻的旧断言**（都是需求的直接结果，不是修 bug）：

- `r56check` **21 条** —— 「768–1280 是手机板 390×744 的堆叠卡」整段改写成
  「缩放的双栏」；波浪那段从 5 档收到 ≤575（`--sc-w` 是视口斜坡，767 处本来就爬到 161，
  改前也一样，是我加测试宽度时加错了档）；1024×600 那条从「被 gutter 削顶」
  改成「485 高，本来就塞得下」
- `r57check` **2 条** —— 翻转（见上）+ 「两个独立控件」收紧到表单内
  （这页现在也挂着 cart，它的两个 interval 同样是注册过的 box）
- `r60check` **6 条** —— 四处取值 + interval 改测画出来的触发器 + chevron 不再内联

### 文件清单

```
改  assets/customstyle.scss   panel-wide mixin；--pp-k + zoom；9 个 pc 块改 panel-wide；
                             删两处死代码；.gb-select--inline + is-up；四处取值；
                             $build → 20260901-r60
改  assets/customstyle.css    编译产物
改  assets/main.js            selectBox：变体名驱动 / 箭头 currentColor / wouldOverflow +
                             clipBottom + show() 里的翻转
改  11 个交付页               两处 interval 由 <button> 换成 <select data-select="inline">
改  全部 12 页                ?v= → 20260901-r60
新  tools/r61check.py         本轮判据（151 条）
新  tools/_reverse_r61.py     反向套回 + --restore
改  tools/_apply_r60_html.py  模板出下拉；加 --remount
改  tools/r56check.py         21 条按新形态改写
改  tools/r57check.py         2 条（翻转 / 作用域）
改  tools/r60check.py         6 条按本轮取值改写
```

### 待裁决

- **BD. 下拉的五个档位里有三个是我编的** —— 稿里全站只出现过 `One Time Purchase`
  与 `4 Weeks`（PDP 的订阅区也只有单值，且那块归 app）。需求方选择「补成常见订阅档位」，
  于是有了 `2 Weeks` / `6 Weeks` / `8 Weeks`。**上线前要拿真实档位替换。**
- ~~**AT**~~ — **本轮关闭**：768 以上一律双栏，缩放而非重排。
- 仍开着：A–F / J–L / N–Q / T–Y / AA / AC / AD / AG / AH / AI / AJ / AK–AP / AX / AY /
  AZ / BA / BB / BC。

---

## 第六十轮（2026-09-01）— 空车状态改用 `is-empty` 状态类

需求方要求 `gb-cart` 的空态用 `class="is-empty"` 表达，不再用属性。

### 改了什么

`.gb-cart[data-cart="empty"]` → `.gb-cart.is-empty`，
`.gb-cart:not([data-cart="empty"])` → `.gb-cart:not(.is-empty)`。

两者都是 0-2-0，层叠权重不变；`is-empty` 与抽屉本来就有的 `is-open` 同为状态类，
可以叠在一起，命名也一致。全站没有别的地方用过 `is-empty`（改前 grep 过）。

`$build` **不动**，仍是 `20260901-r60`：这个 token 从没被服务过（线上还停在
`20260831-r58`），r58 → r60 的破缓存已经覆盖本次改动。

### 验证

- **`r60check` 242 条全过**（新增 2 条把钩子名钉死：CSS 里必须有 `.gb-cart.is-empty`、
  必须**不再**出现 `data-cart`）
- **活性自检**：把判据里注入的钩子换回已废弃的 `data-cart="empty"`，
  空态相关 **12 条当场转红**（禁用底色 / 字色 / 描边 / 不可点 / shop 按钮 44 高与 fill /
  卡片 169 高 / 卡片 action 32），说明这些断言真的挂在这个钩子上，不是空转
- **回归全过**：`r56`（149）/ `r57`（93）/ `r58`（44）/ `r59`（96）/ `r61`（151）；
  `rwd.py` 11 页 × 14 档全绿；`scrolllock` 44 条 / 11 用例全过
- 两次编译 md5 一致（`d00f77ce…`）

### 文件清单

```
改  assets/customstyle.scss   两条选择器 + 两处注释
改  assets/customstyle.css    编译产物
改  tools/r60check.py         注入改 classList.add；新增 2 条钩子名断言
改  docs/HANDOFF.md           2 处（不要报成 bug 的清单 1b、第八节用法说明）
改  docs/PROJECT-STATUS.md    1 处（待决 BB 的描述）
```

无新增待决。

---

## 第六十一轮（2026-09-03）— CSS 写死的图片移进 `assets/`

需求方指出 `.gb-bear-meter__bear` 的图片路径不对：CSS 里写死引用的图片应该在
官方 `assets/` 目录。

### 为什么这是真 bug（不只是整洁问题）

`assets/customstyle.scss` 里除字体外只有一处非 `data:` 的 `url()`：

```scss
background: url("../images/bear-icon.png") center / contain no-repeat;
```

样式表在 `assets/`，`../images/` 指到顶层 `images/` —— 在 `file://` 双击预览、
在静态主机上都解析得到，所以一直没暴露。但 Shopify 把 `assets/` **扁平地**从 CDN
服务出去（`cdn.shopify.com/s/files/…/t/1/assets/customstyle.css`），
那里根本没有 `images/` 兄弟目录可以 `../` 上去 —— **主题一上线就 404，而且是静默的**：
背景图空掉，控制台之外没有任何提示，500 个小熊（首页 3 组 + science 页 3 组各 100）
一起消失。

同一份文件里 14 处字体早就是裸文件名（第十五轮合并时改的，文件头注释也写了
「url()s are bare filenames — assets/ is flat and has no subdirectories」），
`bear-icon` 是唯一漏网的一处 —— 第十五轮那次只把它从 `../../images/` 改成 `../images/`，
少改了一层。

`<img src="images/…">` 那 21 处**不受影响**，没动：主题化时它们走 Liquid filter 改写。

### 改了什么

```scss
// Bare filename like the fonts above: assets/ is flat, and on Shopify the css
// is served from the CDN's assets/ with no images/ sibling to walk up into.
background: url("bear-icon.png?v=#{$build}") center / contain no-repeat;
background: image-set(url("bear-icon.webp?v=#{$build}") type("image/webp"),
                      url("bear-icon.png?v=#{$build}")  type("image/png"))
            center / contain no-repeat;
```

`git mv images/bear-icon.{png,webp} assets/`，并跟字体一样带上 `?v=#{$build}` 破缓存。

`$build` **不动**，仍是 `20260901-r60` —— 与第六十轮同理：这个 token 从没被服务过
（线上停在 `20260831-r58`），r58 → r60 的破缓存已经覆盖本次改动；何况图片换了 URL，
本来就不存在旧缓存。

### 验证

- **产物 diff 恰好 2 行**（3 处 url），无一行是别的内容
- **浏览器实测**：index / science 两页各 300 个 `.gb-bear-meter__bear`，
  computed `background-image` 解析到 `assets/bear-icon.webp|png`，
  用 `new Image()` 回读**两个文件都是 27×44 真加载成功**，`requestfailed` 为空
- **活性自检**：把两个文件临时挪走，同一探针 4 条全部转红
  （`0x0` + `net::ERR_FILE_NOT_FOUND`），证明判据挂在文件上不是空转
- **新判据 `tools/assetpath.py`**：扫 scss 与产物 css 的每一条 `url()`，
  断言是裸文件名且文件真在 `assets/` 里（`data:` 跳过 —— 三个 mask 是故意内联的）。
  scss 16 条 / css 14 条全绿（差的 2 条是注释掉的 Plus Jakarta `@font-face`）。
  活性自检：注入一条 `url("../images/…")` 当场报红，撤回后回绿
- `python3 tools/webp.py --check` 15 个图全绿，`bear-icon.png` 在新位置照样被找到

### 文件清单

```
移  images/bear-icon.png  → assets/bear-icon.png     git mv，内容未动
移  images/bear-icon.webp → assets/bear-icon.webp    git mv，内容未动
改  assets/customstyle.scss   3 处 url + 2 行注释
改  assets/customstyle.css    编译产物（diff 2 行）
改  tools/webp.py             加 DIR 映射，bear-icon 去 assets/ 找
新  tools/assetpath.py        url() 路径判据（通用，非单轮）
改  docs/PROJECT-STATUS.md    目录树 + 目录约定补「CSS url() 引用的图片是例外」
改  docs/HANDOFF.md           架构段计数、第八节新增一条、标题改第六十一轮末
改  docs/CHANGELOG.md         本条
```

### 推送（2026-09-03，本轮已推 live）

**这一条修的是线上此刻正在生效的 bug，不是预防性改动。** 拉下 live 主题一看：

```
线上 assets/customstyle.css   url("../images/bear-icon.png")
线上 assets/                  没有 bear-icon.png / .webp
线上主题                      没有也不可能有 images/ 目录
snippets/gb-head.liquid       <link href="{{ 'customstyle.css' | asset_url }}">
```

→ 线上 600 个小熊（index 3 组 + science 3 组各 100）**一直是空的**。
线上模板里图片走 `shopify://shop_images/…`（Shopify Files），唯独 CSS 里 `url()`
写死的这一个必须进 `assets/` —— 正是本轮修的。

**店铺 / 主题**：`je1ka9-er.myshopify.com`，主题 **`Dev` (#180348977399)，role = live**
（⚠ 名字叫 Dev 但它就是线上，看角色不看名字）。另有 `Horizon` (#179976765687) unpublished。
主题基底是 Shopify **Horizon 4.1.5**，已含 5 个 `gb-` section + 21 个 `gb-` block。
CLI 账号 **john@mockuptocode.com**（原先登录的 johnz0385@gmail.com 对这个店无权限）。

**三方对比**（推送前）：线上 = `20260831-r58`，本地 = r60 + 本轮。
本地 `assets/` 76 个文件里 48 个与线上不同 —— 但**其中 45 个只是 CRLF vs LF**
（线上是 `\r\n`），去掉空白后逐字节相同，**一律不推**。
真内容差异只有 `customstyle.css` / `customstyle.scss` / `main.js` 三个。

**实推 4 个文件**（`--only` 逐个列出 + `--nodelete`）：

```
assets/customstyle.css     产物
assets/customstyle.scss    源，双写 —— 不推它，下次谁从线上 scss 编译就把改动抹掉了
assets/bear-icon.png       新增
assets/bear-icon.webp      新增
```

`main.js` **没推**：它的 r58→r60 差异是 cart drawer / selectBox，而线上主题里
没有 `gb-cart` / `gb-promo-modal` 的 liquid，推上去只是空转，不修任何已知问题。
同理 `customstyle.css` 里 r59/r60 的 cart / promo 样式在主题里也没有对应 DOM，是空转。

**回读验证**（推完重新 `theme pull` 到 `verify/`）：

- **线上现状 vs 推送前基线的差异恰好是这 4 个**，其余 584 个文件一字未动
- 4 个文件与本地**逐字节一致**（LF 也保住了，没被转成 CRLF）
- 线上 css 里现在是 `url("bear-icon.png?v=20260901-r60")`，`../images/` 残留 **0 处**
- 线上 `assets/bear-icon.png` / `.webp` 确实存在

工作目录 `/home/ly/project/Gumi-Brand-shopify/`（**不在静态站仓库里**，静态站仓库只放交付物）：
`baseline-pre-r61/` 推送前快照 · `baseline-dev-live/` 推送后的新基线 · `push-work/` 推送用工作副本。

### 顺带发现（未修）

- **Playwright 的 chromium 没了**（`~/.cache/ms-playwright/` 整个目录不存在），
  `tools/` 下所有判据脚本写死的 `EXE`/`CHROME` 路径全部失效，现在只能用
  `/snap/bin/chromium`。本轮探针临时改了路径跑通，**但 tools 里的脚本没动** ——
  要么重装 playwright chromium，要么把 15 个脚本的路径改成带回退。等裁决。
- `images/` 里另外 41 个文件（`<img src>` 与 favicon）**没动**，主题化时再一并处理。

---

## 第六十二轮（2026-09-03）— reels 接上真视频（`$build` = `20260903-r62`）

需求四条：`gb-reviews__reels` 补上视频与截图；`.gb-reel`／`swiper-slide` 上加一个
**行内属性**填视频链接或路径，点击时传给弹窗；`.gb-reel__media` 用视频第一帧；
视频素材随便找一个短的。追加一条：`.gb-rv-panel__video` 改 16:9 并加宽。

### 改之前是什么样

三段占位，一段都没接上：

```
.gb-reel__media   空 <span>            <!-- TODO client asset: reel poster… -->
.gb-rv-panel__video 只有一个 play 图标  <!-- TODO client asset: reel video -->
modal.open(el)    只按 id 开窗，不接受任何来自触发元素的数据
```

**传参链路整条不存在**，不是接一下的事。

### 素材

`w3schools` 与 Google 的 `gtv-videos-bucket` 两个常用样片源现在都返回 **403**，
实测可用的是 `test-videos.co.uk`（Big Buck Bunny / Jellyfish / Sintel，各 10s 1MB）
与 MDN 的 `cc0-videos`（flower / friday）。**五个不同的片子**，不是同一个用五遍 ——
十张卡若都指向同一个源，「点击传参」这件事就无法证伪，判据会恒真。

下载到 `images/reel-1..5.mp4`（共 4.7MB）而不是写远程链接：刚刚两个源当场挂掉，
把交付物绑在第三方存活上不合适；属性本身写路径写链接都行，主题化时换成
Shopify Files 的 URL 即可。

**第一帧**：本机没有 ffmpeg，帧是从 chromium 里取的 —— `<video>` 画进 `<canvas>`
再读回 JPEG（`tools/_reelposter.py`）。走 http 而不是 `file://`：每个 `file://`
文档各自一个 origin，会污染 canvas 让 `toDataURL` 抛异常。
脚本同时算每帧平均亮度，五张 luma 49–130，没有开场黑帧。

### 传参怎么做的

行内属性用 `data-video`（铁律 17：hook 用 `data-*`，不复用样式类）：

```html
<button class="gb-reel swiper-slide" data-modal="reel-video"
        data-video="images/reel-3.mp4" …>
  <span class="gb-reel__media"><img class="gb-reel__media-img" src="images/reel-poster-3.jpg" …></span>
```

`modal` 侧只加了两个方法与四处接线：`open(el, trigger)` 多收一个触发元素，
在 `is-open` **之前**调 `playVideo()`（放之后会先淡入一个空画面）；
`close()` **开头**调 `stopVideo()`（放进 `unlockAfter` 里声音会多响 0.28s 的淡出时间）。
`stopVideo` 除了 `pause()` 还 `removeAttribute("src") + load()` —— 只 pause 不清源，
弹窗关掉后那 1MB 还在继续下。

没有 `data-video` 的触发元素照旧显示灰底 + play 图标（`has-video` 类控制），
所以这套改动对另外两个弹窗（营养标签、cart）完全无感。

卡 6–10 复用卡 1–5 的五个源 —— 它们本来就是「loop 需要超过可见数两倍」而复制出来的，
不是额外内容。

### 16:9

形状的源头是 `.gb-rv-panel` 的 `aspect-ratio`（不是 `__video`，那层是 100%/100%），
所以就地改的是它：`304/540` → `16/9`，`width: min(100%, 960px)`。
高度不再主导 —— 16:9 先撞到左右边，`max-width: calc((100svh - 80px) * 16 / 9)`
让短视口整体缩小而不是把比例压扁（80 = `__wrap` 自己的上下 padding，`svh` 跟随本项目既有用法）。
播放器用 `object-fit: contain` 而非 cover：占位片是横版，但**真实竖版 reel 不能被裁**。

### 验证

- **`tools/r62check.py` 94 条全过**。核心是**用三张不同的卡各点一次**
  （1→reel-1、3→reel-3、7→reel-2），断言拿到的源**互不相同**（`sources differ == 3`），
  外加 `videoWidth > 0` 证明帧真的解码了，不是只把字符串写进属性
- **活性自检**：`tools/_reverse_r62.py` 撤回本轮改动后，**94 条里 74 条转红**
  （`sources differ 1 == 3`、面板比例 `0.56 vs 1.78`），`--restore` 后回到 94/0
- ⚠ 判据第一版在撤回后是**崩溃**而不是报红（播放器不存在，`v.getAttribute` 抛异常）。
  已修：读不到播放器时返回哨兵值。**崩溃的判据分不清是页面坏了还是判据坏了**
- **回归全过**：`rwd.py` 11 页 × 14 档全绿；`scrolllock` 44 条 / 11 用例（含 reel 弹窗）；
  `r56`(149) / `r57`(93) / `r58`(44) / `r59`(96) / `r60`(242) / `r61`(151)
- `assetpath.py` 仍绿；`?v=` 全站 130 处 + scss 1 处，无旧 token 残留

**`$build` 跳过 r61**：r61 从来没有作为 token 存在过（第六十一轮沿用了 r60），
而 `tools/r61check.py` 早被第五十九轮占用了这个名字。本轮是 `20260903-r62`，
判据 `r62check.py`，两边对齐。

### 环境（顺带修好的）

Playwright 的 chromium 上一轮发现整个没了，`tools/` 下 15 个脚本的写死路径全失效。
本轮装回 `python3 -m playwright install chromium` —— 装到的是 **chromium-1208**，
脚本要的是 **1217**，用一条符号链接对上（`chromium-1217 -> chromium-1208`），
15 个脚本一个字没改。⚠ **这条链接不在仓库里，换机器要重建**。
（先试过把 `/snap/bin/chromium` 链过去，不行：那是 snap wrapper，
不认 playwright 传的 `--disable-field-trial-config`。）
顺带装上了 playwright 自带的 ffmpeg，下次抽帧不必再绕 canvas。

### 文件清单

```
改  index / pdp / our-story / how-gumi-works.html   40 张卡加 data-video + poster img；
                                                    弹窗加 <video data-modal-video>
改  assets/main.js          modal: open 收 trigger、close 先停播、playVideo/stopVideo
改  assets/customstyle.scss .gb-rv-panel 16/9 + 960 宽；.gb-rv-panel__player / __glyph
改  assets/customstyle.css  编译产物
改  11 页 + font-check.html $build 20260901-r60 → 20260903-r62（?v= 130 处）
新  images/reel-1..5.mp4    占位视频 4.7MB
新  images/reel-poster-1..5.jpg  各自的第 0 帧
新  tools/_reelposter.py    canvas 抽帧（换素材时重跑）
新  tools/_apply_r62_html.py / _reverse_r62.py / r62check.py
改  4 页弹窗            播放器全部撤掉，只留 <div data-modal-media>；卡 5/10 改 YouTube 链接
改  assets/main.js      modal.embedUrl()；playVideo 按类型建节点；stopVideo 移除节点；
                        unlockAfter(ms, el) 淡出后再清状态类；EMBED_ALLOW 常量
改  assets/customstyle.scss  __player/__embed 合并（不再需要 display 切换）；
                        has-* 时容器底色压深，避免淡出闪灰
删  images/reel-5.mp4    卡 5 改用托管链接后不再被引用
换  images/reel-poster-5.jpg  改为该 YouTube 视频的缩略图
```

### 追加：`data-video` 也吃 YouTube / Vimeo 链接

需求方补充：视频要支持 YouTube 之类的链接，不只是 mp4 文件。

`<video src="https://www.youtube.com/watch?v=…">` 会去取一个 **HTML 页面**当媒体流，
**静默失败** —— 黑帧、没有报错。托管平台只能用 iframe 嵌入。

**结构上只留一个容器**（需求方指定）：`.gb-rv-panel__video` 挂 `data-modal-media`，
里面除了 fallback 的 play 图标什么都没有；`modal.playVideo()` 判断 `data-video` 是哪一种，
**当场建出对应的那一个节点**。HTML 里因此既没有 `<video>` 也没有 `<iframe>` —— 判据把这条
钉死（`no <video> in markup` / `no <iframe> in markup`）。

| 输入 | 去向 |
|---|---|
| `images/reel-1.mp4`、`https://cdn…/x.mp4` | `<video>`，`has-video` |
| `youtube.com/watch?v=` / `youtu.be/` / `/shorts/` / `/embed/` / `/live/`（可带 `&t=`） | `<iframe>`，`has-embed` |
| `vimeo.com/123` / `player.vimeo.com/video/123` | `<iframe>`，`has-embed` |
| 没有 `data-video` | 灰底 + play 图标（原占位） |

- 嵌入走 **`youtube-nocookie.com`**（YouTube 官方的隐私增强域），`&t=42` 转成 `&start=42`
- `allow` 与 `referrerpolicy` **必须在 `src` 之前设**：权限是在 frame 开始加载时读的
- **关闭时把节点整个移除** —— 对 iframe 这是唯一能停下第三方播放器的办法，
  只清 `src` 不够干净；`<video>` 则先 `pause()` 再移除，声音和节点同一帧消失
- **状态类改到淡出之后才移除**（`unlockAfter(ms, el)`）。这是判据抓出来的：
  原来关掉弹窗后 `has-embed` 一直留着
- **`.has-video / .has-embed` 时容器底色压成 `$c-ink`**：节点在 `close()` 的瞬间就没了，
  而面板还要再淡出 `--modal-exit`，不压底色的话那 0.28s 里会闪出灰色的占位底

**演示**：卡 5/10 改成一个真实的 YouTube 链接（Blender 的 Big Buck Bunny，CC-BY），
poster 换成该片的 YouTube 缩略图，`images/reel-5.mp4` 随之删除。
现在页面上两种类型同时活着，四张本地文件 + 一张托管链接。

### ⚠ YouTube 卡在 `file://` 预览下打不开（Error 153）

实测：
- **`file://` 双击预览 → YouTube 报 `Error 153`**。`file://` 的 origin 是 `null`，
  YouTube 拒绝这种来源的嵌入。**客户就是双击预览的**，这一条一定会被当成 bug 报回来
- **`http://127.0.0.1` + headless → 「Sign in to confirm you're not a bot」**，
  这是 YouTube 对无头浏览器 + 机房 IP 的反自动化拦截，与代码无关
- 两次失败的原因都已定位，**都不是实现问题**；但**真机 + 真实域名下能不能播，本机验证不了**，
  要人工在浏览器里确认。本地 mp4 那四张不受影响，`file://` 下照播

因此判据只断言「建出了正确的节点、`src` 被写对」，**不断言第三方播放器加载成功** ——
把判据绑在 YouTube 的可用性上，它迟早会因为对方的策略变化而变红。

⚠ **判据必须每个用例重新加载页面**：`promoModal` 在 5000ms 自动弹出，而 modal 是单例，
会关掉当时开着的 reel 弹窗。第一版判据让用例累积着跑，跑到第三个卡时正好越过 5 秒，
`card 7 closed: no has-video` 无端变红 —— **红的原因与本轮毫无关系**。
现在每个用例 `fresh()` 一次，各自远在 5 秒以内。

### `file://` 下的降级（需求方报了 153 之后加的）

对照实验先把根因钉死（`tools/` 外的一次性探针，跑完已删）：

| | `file://` | `http://` |
|---|---|---|
| Big Buck Bunny | **Error 153** | 无 153 |
| 换一个视频 | **Error 153** | 无 153 |
| 去掉 `referrerpolicy` | **Error 153** | 无 153 |

**153 只由 `file://` 触发**，与视频、与 referrerpolicy 都无关 —— `file://` 页面的 origin
是 `null`，YouTube 拒绝为 null origin 配置播放器。**改代码绕不过去**，是对方的策略。

客户就是双击预览的，让他们读到一个红色 `Error 153` 等于收一张误报的 bug 单。
所以 `playVideo()` 在 `location.protocol === "file:"` 时不建 iframe，改建一段说明
（`.gb-rv-panel__offline`）+ 一个「在新标签打开」的链接。**上真实域名这个分支永不触发。**

- 链接色用 `$c-lime` 不用 `$c-green`：后者压在 `$c-ink` 上只有 **2.17:1**，低于 AA 的 4.5；
  lime 是 13.9:1，且 footer 本来就是这个搭配
- 三种节点（video / iframe / offline）**统一挂 `data-modal-node`**，
  `stopVideo()` 按 hook 拆而不是按标签名 —— 否则那个 `<div>` 会被漏掉留在弹窗里

判据因此覆盖两条路：`file://` 下建 offline 说明，**另起一个本地 http server** 验同一张卡
在有 origin 时确实建出 iframe。共 133 条。

### 推送到 Shopify live（2026-09-03 第二次）

需求方指定**只推 `customstyle.css` / `customstyle.scss` / `main.js`**，liquid 不碰
（liquid 推送需逐次授权）。

⚠ **推送前的三方对比抓到别人的改动**：上一次推送之后，线上多了
`sections/gb-reviews.liquid`（reels + `#reel-video` 弹窗）与 `blocks/gb-ingredients.liquid`，
`templates/index.json` 也变了。**assets/ 下没有别人的改动**，所以这三个文件不冲突。

**回读验证**：线上差异恰好是这 3 个，与本地逐字节一致，别人的 liquid 与 json 一个都没动。

⚠ **视频功能在线上还不会工作**，需求方已知情并接受：

| 缺口 | 位置 |
|---|---|
| 弹窗没有容器 hook | `sections/gb-reviews.liquid` 的 `.gb-rv-panel__video` 缺 `data-modal-media` |
| 属性名不一致 | liquid 写 `data-video-url`，JS 读 `data-video`（**已定：以 `data-video` 为准**） |
| 图标没有类名 | 弹窗里的 play `<svg>` 需要包一层 `.gb-rv-panel__glyph`，否则有媒体时盖不掉 |

推上去之后线上的可见变化只有一个：**reel 弹窗从 304×540 竖版变成 960×540 横版**，
里面仍是居中的 play 图标。JS 的新模块（cart drawer / selectBox / playVideo）在线上
**全部早退** —— `data-modal-media` / `gb-cart` / `data-select` / `data-gallery`
在主题的 liquid 里命中都是 0。

### 顺带发现 / 待决（未动手）

- **reel 播放会被 promo 弹窗打断** —— `promoModal.DELAY = 5000`，页面加载 5 秒后自动弹出，
  而 modal 是单例，会 `close()` 掉正在播放的 reel。这是既有行为（弹窗一直是这样），
  但**本轮之前 reel 弹窗里是静态占位，被顶掉无所谓，现在是正在播的视频**。
  修法是 promo 弹出前检查 `modal.current`，但「promo 要不要给正在看视频的人让路」是决策，
  **未动手，等裁决**。
- **AD′ 面板 16:9 与真实竖版 reel 冲突** —— reel 本来是竖版短视频（稿里的卡就是 304×540
  的 9:16）。16:9 是需求方本轮点名要的，占位片也确实是横版；但**真实竖版素材进来后，
  contain 会在左右留大片黑边**。需要裁决：面板跟素材走（竖版回 9:16），还是素材裁成横版。
- **Sintel 那张卡上下有黑边** —— 是素材自带的宽银幕 letterbox 编码在帧里，
  `cover` 在 540/360 = 1.5 的缩放下垂直方向正好完整显示，所以黑边留下了。不是 CSS 问题。
- **占位视频 4.7MB 进了仓库** —— 若不想要，改成远程链接只需替换 `data-video` 的值。
- `.gb-rv-panel__video` 的 `@include hover { color: $c-green }` 现在只对 fallback 图标有意义
  （有视频时图标是隐藏的）。无害，没动。

---

## 第九十轮（2026-09-07）— 评论卡四处改造：img 星级 / 小熊占位 / More-Less 分页 / 评分描边（`$build` = `20260907-r90`）

需求方点名四条，全部落在 r89 建的 `gb-crev` 上。

⚠ **轮次号在并行下乱过一次**：另一个会话同日做了第八十八轮（collection 底距）与
第八十八～八十九轮（product 顶距 + promo 波浪，已推 live），并**用它自己的判据覆盖了
`tools/r89check.py`**。本轮起 gb-crev 的判据改名 **`tools/crevcheck.py`** ——
按模块命名、不带轮次号，永不撞；内容从 git `79611e2` 恢复后扩写。

### 1. 星级拆成五个 `<img>`

`images/star.svg`（单颗，取自 `reviews-desktop-reviews-2.svg` 的第一个 path —— 它的坐标
本来就在 0–20 盒里，不用改）。容器改 flex 并给 `img { flex: none }`，否则窄屏下 summary
那一列会把星压扁。标题那组是同一个文件按 32 渲染（5 × 32 = 板上的 160×32）。

⚠ **4.5 星的暗点从 `path:last-of-type { fill-opacity }` 挪到了
`.gb-crev-card__star--dim { opacity: 0.3 }`** —— 拆成 `<img>` 之后 CSS 够不着内部的 path。

### 2. 评论配图放小熊占位

`images/review-bear.png` / `.webp`，128×128，从 `gumi-bear-front.png` 居中补方后缩下来的
（**不是新画的素材**）。灰底 `#d5d4d4` 留在下面，`object-fit: contain` —— 让灰块仍读作
「空槽位」，而不是图片铺满到角。

### 3. More / Less 分页（`crevPager`）

`assets/main.js` 新增模块，IIFE + `data-*` hook + 早退守卫（铁律 17）。默认 5 条，每次 +4，
全出来后按钮文字翻成 "See Less Reviews"，再点收回 5 条。`data-crev-start` /
`data-crev-step` 挂在列表上，将来主题 setting 能直接驱动。

⚠ **`[hidden]` 输给作者的 `display`**：`.gb-crev-card` 是 flex、`.gb-btn` 是 inline-flex，
而 UA 的 `[hidden]{display:none}` 只有 0-0-0 —— 两处都必须重述，否则「隐藏」的行照样在屏幕上。
⚠ **收起时列表顶会跑到视口上方**（消失的是按钮上方的行），所以收起后只在 `top < 0` 时滚回。
⚠ **总数 ≤ 起始数时按钮自我隐藏** —— 看得见却什么都不做的控件比没有更糟。

⚠ **板上只有 5 条评论，第 6 条起是那 5 条的复制件**（需求方定的方案），HTML 里有注释标着。
接评论 app 时**删掉后 5 条**。

### 4. 评分数字补上描边 —— r89 漏了

`324:64038` 给 4.76 挂了 `$c-lime` 的 **OUTSIDE 0.25em** stroke（桌面 16.55 @ 66.18、
手机 14 @ 56，两档同一个 em）。r89 当时只读了 `effects`（空的）**没读 `strokes`**，所以漏掉。

⚠ **这是 `.gb-science-card__value` 那条的两倍粗**（那边 0.125em、实现里调到 0.145em），
而 `ink-outline` 的环间隙随半径变大，所以 steps 也得翻倍：
`ink-outline(0.25em, $c-lime, $steps: 72)` → 24 + 48 + 72 = 144 个副本。
**36 steps 在这个半径下会画成虚线。**
⚠ **相邻字形的描边合并成一个「气泡」是对的** —— 已与 `figma/screenshots/` 的稿图对照过，
板上就是这样，不要当成描边过粗去调细。

### 文件清单

- `assets/customstyle.scss` / `assets/customstyle.css` — 星级容器改 flex、`--dim`、附件图、
  评分描边、`.gb-crev-card[hidden]` 与 `.gb-crev__more[hidden]` 两处重述
- `assets/main.js` — 新增 `crevPager`，注册进 modules 与 `window.gumi`
- `reviews.html` / `pdp.html` — 星级 img、附件 img、10 张卡、按钮 data-*
- `images/star.svg` / `images/review-bear.png` / `images/review-bear.webp` — 新增
- `tools/crevcheck.py` — 判据（由 `r89check.py` 改名并扩写）
- 全站 13 页的 `?v=` 与 `$build` → `20260907-r90`（245 处）

### 判据

`python3 tools/crevcheck.py` —— 两页 × 1440/390 + 分页交互，**全绿**；
`--strip` 反向 **68 红**。`tools/rwd.py` 两页全绿。
分页那组验的是 `5 → 9 → 10 → 5`、文案翻转、`aria-expanded` 跟随、按钮始终可见。

⚠ 判据一开始把 `naturalWidth === 0` 报成红 —— 那是 `loading="lazy"` 在视口外没解码，
**不是路径坏了**。探针改成先把列表滚进视口再读。

### 遗留

1. **"See Less Reviews" 是自造文案** —— 板上没有收起态。待设计方裁决。
2. 后 5 条评论是复制件，接 app 时删掉。
3. 第八十九轮那三条仍未决：第 1 条标题断句、按钮文字色（板 `#F5F1E9` vs 基类白）、
   手机端 `--lg` 只在本模块改 44。

## 第八十九轮（2026-09-07）— Real Customer Reviews 静态实现（`$build` 与 r88 共用 `20260907-r88`）

需求：把 reviews / pdp 两页的 Real Customer Reviews 从 app 挂载壳做成真的前端，对照设计还原。

⚠ **本轮推翻了 `PROJECT-STATUS.md` 的「实现边界」** —— 评论区原本划归 Shopify 评论 app、
前端只出壳。需求方明确要求做成静态前端，两页都做。

⚠ **`$build` 与第八十八轮共用 `20260907-r88`**：同一时段另一个会话在做 r88（collection 页
底距 + `tools/r88check.py`），它先把 token 提到 r88 并编译过，本轮改动搭在同一个 token 上，
**不是漏改**。判据另起 `r89check.py` 以免撞名。轮次编号是否要重排，待需求方定。

### 1. 数值与内容的来源

全部取自 Figma 节点，桌面 `324:64032`（1440）/ 手机 `324:64978`（390）。四份稿
（reviews 与 pdp 的桌面 + 手机）是同一个组件，所以两页共用一份实现。

- 5 条评论的姓名、首字母、星级、时间、标题、正文、赞踩数都是板上原值
- **只有第 1 条是 5 星，其余 4 条是 4.5**。板上的画法是把第五颗**整颗**降到 30% 透明
  （`191:5463` fill a0.30），**不是半填充**
- **图片只挂在第 1、3 条**：另外三条的 `Image` 节点 `visible: false`，卡高 324 与 240
  差的 84 就是它（64 + 20 gap）。build.txt 看不出来，只有节点数据能证
- 「See More Reviews」按钮里那个 24×24 icon 在板上 `visible: false` —— 按钮宽 280
  = 64 + 152 + 64 正好不含它。**不要照 build.txt 的轮廓补图标**

### 2. 两档只有这四处不同

| 项 | 1440 | 390 |
|---|---|---|
| 4.76 | 66.18 / 52 | 56 / 44 |
| Based on… | 16 / 24 / -0.32 | 14 / 20 / -0.28 |
| 星 + 文案 | 一行，gap 12 | 上下两行，gap 16 |
| 按钮 | 52 高 / 0 64 / 28 / .48 | 44 高 / 0 40 / 24 / -.32 |

板上 heading 的 272、列表的 112 侧内距**改写成 max-width 736 / 1056**：手机档两个上限
都大于它画的 350，于是手机端不需要任何覆盖，平板档也自然过渡。

### 3. 结构上的两个决定

- **外壳沿用 `.gb-app-section`**（padding、cream 底、48 gap 本来就对），新内容用
  `gb-crev` 前缀。**不是 `gb-reviews`** —— 那是另外四页的 testimonial 轮播
- **按钮复用 `.gb-btn--lg`**，手机档的 44/40 写在 `.gb-btn.gb-crev__more` 上（双类，
  两个选择器都是 0-1-0）。**没有动基类** —— 它在 11 个页面上各用 2 处

### 文件清单

- `assets/customstyle.scss` / `assets/customstyle.css` — 新增 `gb-crev` / `gb-crev-card` 块
- `reviews.html` — 壳换成完整实现，原来的 `<h2>` 移进 `.gb-crev__head`
- `pdp.html` — 同上；这页原本连标题都没有，按板补上
- `tools/r89check.py` — 判据（新增；r90 改名为 `tools/crevcheck.py`）

### 判据

`python3 tools/crevcheck.py`（r90 由 `r89check.py` 改名，那个名字被并行会话占了）
—— 两页 × 1440/390，68 条断言全绿。
`--strip`（把 `.gb-crev` 规则从 css 里剥掉再注入）应报 **60 红** ——
证明判据读的是本轮加的规则，而不是页面本来就有的东西。
`tools/rwd.py reviews.html` / `pdp.html` 两页全绿。
line-reveal 在新父层级下仍正常：`is-split` 生效、标题两档都是 1 行（48 / 36）。

### 遗留

1. **第 1 条评论的标题在板上就是断的** —— 「Great tasting, and super healthy product
   that would」，「would」之后没有了。照原样保留（铁律 3），**待设计方裁决**。
2. **赞踩不计数、See More 不展开**：板上只有 5 条，第 6 条不存在，编出来就是造假数据。
   两者都只做 hover / press 态，点击行为留给 app。需求方已确认这样做。
3. **按钮文字色**：板上 `#F5F1E9`，`.gb-btn--lg` 用的是白色。没有为这一个按钮改基类。
4. **手机端按钮 44 高只在本模块作用域内**；`.gb-btn--lg` 基类手机端仍是 52。
   其它页面的手机稿是否也该 44，**没查，待裁决**。
5. 线上没有 `gb-app-section` 的 liquid，这块**目前只活在静态站**。要上线得对方补 section。

## 第八十八～八十九轮（2026-09-07）— collection 页底距 + product 顶距改档 + promo 波浪重建（`$build` = `20260907-r89`）

两批需求一次推送。第一批一条（collection 页底部间距），第二批三条（两个 padding-top、promo 还原）。

### 1. `/collections/all` 底部留白 32 → 120 / 64

线上 collection 用的是 Horizon 自己的模板，**没有静态站对应页、也没有稿**。
它的 section padding 来自 theme editor 的 setting（inline `--padding-block-end: 32px`），
32 太紧：`.gb-deco-bear--a` 相对波浪固定上溢 196（桌面）/ 108（手机），
在 32 的留白下直接骑在产品名上。

取值照 `.gb-rich-page`（全站「内容 + 波浪」结构的既有定义）：**120 / 64 / `fluid` 插值**。
套用后小熊相对产品名的富余量是桌面 20px、手机 4px，**与静态站每一页实测完全一致**。

⚠ **覆盖的是 longhand 不是变量**：inline style 设的是 `--padding-block-end`，
改变量得用 `!important`；`.product-grid-container` 自己那条规则只有 0-1-0，所以 0-2-0 就够。
⚠ **代价**：对方以后在后台调这个 section 的 bottom padding 不再生效。
选 CSS 是因为 editor 的 padding setting 只有单值，做不出桌面/手机两档。

### 2. `.gb-product` 顶距三档拉平到 32

基类原来是 `96 / 52 / fluid(52,96)`。现在三档都是 32。
⚠ **线上没有匹配** —— `sections/gb-product.liquid` 只输出 `gb-product gb-product--lg`
或 `gb-product gb-product--page` 两种，**没有裸 `.gb-product` 的通道**。
这一条只影响静态站的 how-gumi-works / reviews / our-story 三页。

### 3. `--lg` 显式写回原来的斜坡，`--page` 补上它一直在继承的 96

`--lg` 之前不写 padding-top、直接吃基类的 96。基类降到 32 后必须显式restate：
`96 / 52 / fluid(52,96)`（52 = 稿 243:22226 的 paddingTop 32 加上内层 frame 的 20）。

⚠ **`--page` 是顺带必须做的防护**：它同样只在 narrow/tablet 写了 padding-top，
pc 档一直吃基类的 96。不补这一行，PDP 桌面顶距会跟着掉到 32 —— 需求没点名 PDP。

### 4. promo 绿卡的波浪咬痕：从 SVG 元素改成 mask

静态站的咬痕是 `.gb-promo-card__lip--v`（126×764 的 SVG，7 个 r=63 的圆），
**线上 `sections/gb-promo.liquid` 根本不渲染这个元素**（实测线上 0 个、静态站 4 个），
所以线上是直线分界。两边的 computed style 其实完全一致，差的只是这个元素。

不改对方的 liquid，改用 `.gb-promo-card__body::before` + `$mask-promo-lip` 重建：
同样的盒子、同样七个圆，`left: -31px` 让露出来的正好是原来那 31px。
绿色随之从 `.gb-promo-card--green` 移到 `.gb-promo-card__body`。

- ⚠ **`z-index: -1` 是承重的**：`__body` 带 `z-index: 1`、自开层叠上下文，
  负值子元素画在它自己的背景之上、正文之下 —— 正是原来 SVG 靠 body 的 z-index 白拿的顺序。
  不写就盖住首字（r? 那次 "We got sick" 被画成 "Ve got sick" 是同一个机制）。
- ⚠ **≤767 卡片仍要留绿底**：手机端两个半边堆叠、`__media` 拿到自己的圆角，
  绿色若只在 body 上，media 圆角外那一圈会露出页面底色。所以 narrow 档把绿还给卡片。
- 静态站不受影响：实测伪元素落在绝对位置 689，**与真 SVG 的 689 完全重合**。

### 文件清单

| 文件 | 改动 |
|---|---|
| `assets/customstyle.scss` | 新增 `// Collection` 分区；`.gb-product` / `--lg` / `--page` 的 padding-top；`$mask-promo-lip` + `.gb-promo-card--green` 重写；`$build` → `20260907-r89` |
| `assets/customstyle.css` | 重编译（双写） |
| `tools/r88check.py` / `tools/r89check.py` | 两轮判据（新增） |

### 推送

`--only assets/customstyle.css --only assets/customstyle.scss --nodelete --allow-live`。
三方对比：我们要推的两个文件线上 = `baseline-r87`，无第三方改动；
产物新鲜度验过（重编译 scss 与仓库 css 逐字节相同）。
回读 **616 → 616**、两个文件逐字节相同、**614 个清单外文件零改动**。
新基线 **`baseline-r89`**。`r88check` / `r89check` 的 `--as-served` 推前分别 12 红 / 6 红，
推后**全部全绿**。

### 对方同期在动的（三方对比抓到，我们没碰）

- 10:44 改 5 个 PDP block：`gb-features` 换成 `{% content_for 'blocks' %}`（**卖点列表终于不空了**，
  线上实测 4 条，代价是每个 `<li>` 外多一层 `div.shopify-block`）；
  `gb-price` / `gb-title` / `gb-variants` / `gb-subscription` 加 `| default: product` 容错。
- 11:19 `gb-footer.liquid` 三个社交链接加 `target="_blank" rel="noopener noreferrer"`。
- 推送前又抓到 `gb-header.liquid` / `footer-group.json` / `templates/product.json` 也动过。

### 遗留

- **PDP 右栏间距塌陷（未修，未登记）**：r87 那波重构把 `.gb-product__head` 删了、
  所有 block 塞进 `<form>`，于是 `.gb-product__info` 的 `gap: 24` 和 head 的 `gap: 16` 双双失配。
  实测 1440 与 390 两档下 rating→title→tag→lead→features 每一处间距都是 **0**（应为 16），
  cta→guarantee-note 也是 0（应为 24）。等需求方定用 CSS 补还是让对方改回结构。
- **promo 白卡的咬痕没做**：本轮只点名了绿卡。白卡的 `lip--v`（`left: -100px`，咬 26）线上同样缺。
- **手机端的 `lip--h` 没做**：静态站 ≤767 画的是卡片底部的水平波浪，线上也没有这个元素。
- collection 页是自定值、无稿，需登记进「待设计方裁决」。

## 第八十七轮（2026-09-07）— 需求方点名的六处 + logo liquid 落地（`$build` = `20260907-r87`）

需求（对话）七条：reviews 标题版心、面板边框、guarantees 窄屏堆叠、stats 说明的负外边距、
science 数字的手机字号、弹窗 pane 右内距，外加**「更改 gb-logo.liquid 推送」** —— r85 欠着的那条。

### 1 / 6. 两条纯数值

- `.gb-reviews__title { max-width: 570px }`。`.gb-reviews__head` 本来就是
  `align-items: center` 的列，所以不需要再补 `margin-inline: auto`。
- `.gb-nl-pane` 右内距 10 → 24。⚠ **副作用已实测**：`.gb-nl-panel__body` 的滚动条是 16px 宽，
  原来的 10 + 16 = 26 与左侧 24 视觉等宽；改成 24 之后，**pane 滚动时右侧留白是 40 对左侧 24**。
  不滚动的 pane 则从「左 24 右 10」变成两边都 24。要哪一种由需求方定。

### 2. 面板边框：上边框之外，下边框也一起藏

r86 只处理了 `border-top`。关着时面板是 0fr 行，**两条发丝都叠在 bar 自己的边框下面**，
所以 `border-bottom` 同样改成 `transparent`，`.is-open` 时给回 `$c-sand`，
两个 `*-color` 都进了面板原有的 `transition`。

### 3. `.gb-product__guarantees` 窄于 370 时一行一个

`@media (max-width: 369.98px) { flex-direction: column; align-items: center; }`。
按铁律 18 这是**布局阈值**：只有排列，不带任何数值 —— 间距仍由上面那三档 `gap` 负责。
`369.98` 而不是 `369`，是为了让 369 和 370 之间的小数视口也算「小于 370」。

### 4. `.gb-stats__note` 992 以下不再上提

把手机档里的 `margin-top: -16px` **删掉**，改成 `@include mid { margin-top: 0 }`。
⚠ **`mid`（≤991）与 `narrow`（≤767）是重叠的两档，只有源码顺序决定胜负**，所以这条
必须排在 `narrow` / `tablet` 之后（铁律 18 说的「值档互斥」在这里做不到互斥，
就必须把顺序写进注释）。基础值 −34 因此只活在 992–1280，**991/992 会有 34px 的台阶**。

### 5. ⚠ science 数字的手机字号 —— 同一组数字的**第三次反转**，这次带作用域

历史（先 grep 再动手，铁律 1）：
r43 手机 36/40 → r49 挪到 `--nutrient` 上、95% 组回板值 56/44 → r50 连那份也删（**全宽 56/44**）
→ 后来又全局改回 36/40 并补了 768–1280 的斜坡 → **r87：只有 `.gb-science--tight` 保留 36/40，
其余全部在所有宽度都用 56/44/0**。

做法是把 `@include narrow` / `@include tablet` 两块从 `.gb-science-card__value` 搬到
`.gb-science--tight .gb-science-card__value`（0-2-0）。**非 tight 的卡片因此不再需要平板斜坡** ——
767/768 两侧都是 56，本来就没有台阶可补。

⚠ 影响面：`gb-science--tight` **全站只有 science.html 的第二个 section**；
index 的 3 张、science 第一个 section 的 3 张手机端全部变回 56/44。
`text-shadow` 是 `em` 单位，描边跟着字号自己缩放，不用动。
`rwd.py` 全站全绿 —— 56px 的数字在 360 档没有撑破任何容器。

### 7. `snippets/gb-logo.liquid` —— r85 那条终于推了

`{{ logo_img | image_url: width: w | times: 2 }}` **过滤器顺序错**：`image_url` 先出 URL，
`times: 2` 乘的是字符串、返回 `0`，于是线上 `src="0"` 加一个 `0 2x` 候选 —— 1x 屏靠 srcset
侥幸能看，**2x 屏必碎图**。改成先 `assign w2 = w | times: 2` 再进过滤器。

**推完线上实测**：`src` 与 `2x` 候选都变成了真实的 `…Group_38203.svg?…&width=248`，
`r85check` 里那 **18 条 `PEND` 全部转绿**。

### 新增判据

`tools/r87check.py` —— 离线 6 条 + 静态/线上各 **四档（1440 / 900 / 390 / 360）** × 3 页
（index / science / pdp）。360 是为了第 3 条，900 是为了第 4 条的 768–991 带。
第 5 条同页取 `.gb-science:not(.gb-science--tight)` 与 `.gb-science--tight` **两个样本对比**，
单取一个证明不了「只有 tight 变」。第 2 条读边框颜色**必须等 500ms**（过渡起始值，第三次踩）。

**双向**：`--as-served` **56 红** → 换本地 css **只剩 logo 那 6 条**（那是 liquid，路由换不到）
→ 推完 liquid 后 `--as-served` **全绿**。`r85check` / `r86check` 复跑同样全绿。

### ⚠ 对方把 PDP 拆成了 9 个 block

推送前拉取（10:27）比 `baseline-r86` 多了 8 个文件（**608 → 616**）：新增
`blocks/gb-atc` / `gb-feature` / `gb-guarantee-note` / `gb-lead` / `gb-price` / `gb-rating` /
`gb-subscription` / `gb-title` / `gb-variants`，删掉 `_gb-features.liquid`，
改写 `gb-features.liquid` / `gb-product.liquid` 与两个 template。
**清单内 3 个文件线上都 = 基线，零冲突**，且 `theme check` 改前改后同为 29 offenses / 8 errors。

⚠ **PDP 的卖点列表到这一刻仍然是空的**（`<ul class="gb-product__features"></ul>`），
拆 block 之后也没恢复。是对方的文件，我们没动。

### 文件清单

```
改  assets/customstyle.scss     六处 + $build → r87
改  assets/customstyle.css      重新编译（与基线 diff = 40 行，正好是这六处）
改  全部 13 个 html             ?v= r86 → r87
推  liquid/snippets/gb-logo.liquid   （r85 就改好的那份，本轮才授权推）
新  tools/_apply_r87.py / tools/r87check.py
```

### 推送（2026-09-07，已上线）

**3 个文件**：`assets/customstyle.css` / `assets/customstyle.scss` / `snippets/gb-logo.liquid`。
三方对比零冲突。推送前 diff：css 删 21 / 增 34（剔 30 行 token 后 **40 行**）、
scss 删 10 / 增 39、gb-logo 删 2 / 增 6。
**回读 616 → 616、3 个文件逐字节相同、613 个清单外文件零改动。**
线上 `r87check --as-served` **全绿**，`r85check` / `r86check` 也全绿。
新基线 **`baseline-r87/`（616 文件）**。

### 遗留

- ⚠ **PDP 卖点列表线上是空的**（对方的 `content_for 'block'` 改造，r86 起）。
- `.gb-nl-pane` 右侧在滚动态是 40 对 24，见第 6 条，等需求方定。
- 跑马灯 88×36 的减速（r86）与「要不要收 duration」仍未定。
- STYLE-GAP：**C11 关闭**（logo 已推）。

---

## 第八十六轮（2026-09-07）— 需求方点名的五处（`$build` = `20260907-r86`）

需求（对话）五条：features 位置、手机菜单开合时 header 消失、手机跑马灯 logo 再小些、
链接 hover 由下划线改为变色、面板上边框只在菜单打开时显示。**全部 CSS，未动 JS 与 liquid。**

### 1. `.gb-product__features` 移到 `.gb-product__head` 下面

**线上它在最底下**：这个 `<ul>` 是编辑器 block，`{% content_for 'blocks' %}` 在
`.gb-product__info` 的**末尾**统一输出五个 block，所以它排在 CTA 和 guarantee-note 之后。
静态站里它是 `.gb-product__head` 的子元素，位置本来就对。

用 flex `order` 拉回来（`.gb-product__info` 本来就是 `flex-direction: column`）：
head `-2`、features `-1`，其余默认 `0`。**静态站上两条选择器都匹配不到那个 `<ul>`
（它不是 `info` 的子元素），是彻底的空转。**

⚠ **第一版只写了 `.gb-product__info > .gb-product__features`，线上完全没生效** ——
`content_for 'blocks'` 给每个 block 套了一层 `div.shopify-block`，`<ul>` 是**孙子**不是儿子
（[[render-block-wrapper-breaks-child-selector]]）。判据当场测出 `order` 仍是 `0` 才发现。
补了 `:has(> .gb-product__features)` 打在包裹层上，两条并存。
⚠ HANDOFF 里「`div.shopify-block` 现在全站 0 处」这句**对 PDP 已经过时**。

⚠ 两点取舍：`order` 只改**视觉**顺序，读屏与 Tab 仍按 DOM；features 上方的间距是
`.gb-product__info` 的 24 而不是 head 内部的 16。要真正搬 DOM 得动
`sections/gb-product.liquid`，登记为 STYLE-GAP **C12**。

### 2. ⚠ 锁滚动把 sticky header 一起弄没了 —— 三处锁都有，本轮只修了菜单那处

**实测**（390，页面滚到 900）：菜单一开，`.gb-header` 的 `top` 从 **0 跳到 −868**，
直到锁解开（关闭后约 900ms，抽屉滑出的时长）才回来。**整个开着的期间 header 都不在**，
关闭时又「啪」地跳回来 —— 这就是需求方说的「一下子消失」。

**机制**（逐条实测，不是推断）：
reset 里 `body { overflow-x: hidden }`。**只要 html 的 overflow 是 `visible`，body 的
overflow 就被提升给视口**，body 自己仍是 `visible`；一旦锁把 html 设成 `overflow: hidden`，
提升停止，那条 `overflow-x: hidden` 开始作用在 body 自己身上 —— body 成了 sticky 的
scrollport，而 body 从不滚动，于是 header 落回静态位置（即文档顶部，视口外）。

| 试法 | header top |
|---|---|
| 不锁 | 0 |
| 只锁 html | **−868** |
| html + body 都锁（现状） | **−868** |
| 锁 html，body 强制 `overflow: visible` | 0 |
| 锁 html，body `overflow-x: clip; overflow-y: visible` | **0，且横向裁切还在** |

改成最后一行：`clip` **不建立滚动容器**，所以横向裁切保住了、sticky 也活着。
判据里有一条守着锁没被削弱（锁上之后滚轮不能推动页面）。

### ⚠ 顺带发现，**未修**（同一个病，另外两处）

`html.is-modal-open, body.is-modal-open { overflow: hidden }`（弹窗）与
`html:has(#cart-drawer …), … body { overflow: hidden }`（Horizon 购物车抽屉）
**是同一条形状、同一个病**。实测 `is-modal-open` 下 header top：**390 档 −868、1440 档 −860**。

- 弹窗是全屏遮罩，header 没了看不出来；**但购物车是侧边抽屉，header 露在旁边，桌面端一定看得见**。
- 改法与本轮完全相同（那两处的 `body` 半边换成 `overflow-x: clip; overflow-y: visible`）。
- 按铁律 20 **没动**，等需求方一句话。

### 3. 手机跑马灯 slot 106×44 → **88×36**

`.gb-logo-scroll__item` 与 `.gb-logo-scroll__img` 的 narrow 档同步改。
⚠ **88×36 是我们选的数，不是稿上的** —— 这块 Social Proof 只有桌面稿（341:47384），
106×44 本身就是第三十五轮需求方口头给的。要别的数说一声。
⚠ **副作用**：速度 = 一组间距 / 15s，间距从 408 缩到 354，**这一档比原来慢约 13%**。
没有改 duration（那是决策不是还原）；要维持原速就在 narrow 里加 `animation-duration: 13s`，一行。

### 4. 链接 hover：去掉下划线，只变色

`@mixin link-underline`（伪元素 + `scaleX`）**四个用户全部摘掉，mixin 一并删除**：
`.gb-header__link` / `.gb-header__sublink` / `.gb-footer__link` / `.gb-footer__legal-links a`。
**四个本来就各自带 hover 变色**（`#47ac00` / `$c-green` / `$c-white` ×2），所以摘掉下划线之后
反馈没有变弱 —— 判据逐个强制 hover 实测颜色确实在动。

⚠ 「统一变色」按**统一改用变色**理解，**不是四处都改成同一个颜色** ——
header 在奶油底、footer 在深绿底，同色必然有一边看不见。
⚠ **常驻下划线不在此列**：`text-decoration: underline` 那六处（rich-text 链接、
法务小字、cart continue、promo dismiss 等）是行内链接的常态样式，不是 hover 效果，原样保留。

### 5. `.gb-header__panel` 的上边框只在菜单打开时显示

`border-top: 1px solid transparent` + `.gb-header.is-open & { border-top-color: $c-sand }`，
并把 `border-top-color` 加进面板原有的 `transition`，跟着行高一起淡入。

⚠ **用 transparent 不用 0 宽**：关着时面板是 0fr 行，宽度一变盒子会跳 1px；透明既不跳、
颜色又能过渡。手机档那句 `border-top: 0` 保留 —— 宽度是 0，`is-open` 给的颜色画不出东西。

### 新增判据

`tools/r86check.py` —— 离线（8 条选择器/源码断言）+ 静态 1440/390 + 线上 1440/390。
特别的三条：① 第 2 条**开菜单后读 header 位置，再补一次滚轮确认锁没被削弱**；
② 第 4 条用 CDP 强制 hover **比对颜色前后**（`(hover:hover)` 在裸 headless 恒 false，
拿不到就 SKIP 不是默默通过）；③ 第 5 条读 `is-open` 后的颜色**必须等 500ms**
（又是 [[headless-transition-reads-start-value]]，本轮第二次踩）。

**双向**：`--as-served` **30 红** → 换本地 css **全绿**。
`tools/r85check.py` 同步改了一条（面板上边框的颜色断言移交给 r86check），复跑全绿。
`tools/rwd.py` 全站全绿。

### 文件清单

```
改  assets/customstyle.scss     五处 + $build → r86（删 @mixin link-underline）
改  assets/customstyle.css      重新编译（与基线 diff = 108 行，正好是这五处）
改  全部 13 个 html             ?v= r85 → r86（135 处）
改  tools/r85check.py           面板上边框颜色断言移交 r86check
新  tools/_apply_r86.py / tools/r86check.py
```

### 2b/2c. 追加 —— 另外两处锁一起修了（需求方「修复推送」）

`html.is-modal-open, body.is-modal-open` 与 `html:has(#cart-drawer …), … body`
两条各拆成两行，`body` 半边同样换成 `overflow-x: clip; overflow-y: visible`，
锁仍然只压在 `html` 上（[[overflow-clip-breaks-scroll-lock]]：**Gecko 只认 html 那一半**，
所以这个方向是安全的）。`padding-right` 的滚动条补偿**依旧只在 html**
（[[scroll-lock-compensation-once-only]]）。

**线上实测（改前）**：`is-modal-open` 下 header top **1440 档 −860 / 390 档 −868**；
购物车抽屉（把 `dialog` 的 `open` 属性直接置上，**不碰 `/cart/*`**）**1440 档 −860** ——
这一处是侧边抽屉，header 就在旁边，**桌面端一直看得见**。

⚠ **判据自己先测错了一次**：只加 class 不走 `modal.open()`，Lenis 还在跑，
滚轮经由它的 `scrollTo` 推动了 `overflow: hidden` 的 html（900 → 1467）。
拿 r85 基线 CSS 跑同一段，**两个宽度上数字完全一样**，证明与本轮改动无关；
`modal.open()` 的生产路径会 `smoothScroll.pause()`，暂停后 1492 → 1492 锁得住。
判据已改成走生产路径。（菜单那处不受影响：`.gb-header__panel` 在 Lenis 的 `PREVENT` 名单里。）

### ⚠ 对方同时在改 PDP —— 第 1 条已由对方在 liquid 落地，但**列表现在是空的**

推送当天 10:01 / 10:03 两次拉取之间，对方给 `sections/gb-product.liquid` 加了
`{% content_for 'block', type: '_gb-features', id: 'features' %}`（放在 `.gb-product__head` 里，
位置与静态站一致），把 `features` 从 `templates/product.json` 的 `block_order` 里摘掉，
并新建 `blocks/_gb-features.liquid`。**方向和我们要的一样，所以本轮那两条 `order` 规则在线上已成空转**
（留着无害，是对方万一回滚时的兜底）。

⚠ **但线上渲染出来的 `<ul class="gb-product__features">` 是空的** ——
`templates/product.json` 里 4 个 `_gb-feature` 子块都还在，
`{% content_for 'block', type:…, id:… %}` 渲染了父块却**没有带出它内部的
`{% content_for 'blocks' %}`**；改名成 `_gb-features` 之后仍然是空的。
**PDP 上那四行卖点目前不显示。** 是对方的文件、对方正在改，我们没动。

### 推送（2026-09-07，已上线）

**2 个文件**：`assets/customstyle.css` / `assets/customstyle.scss`（`main.js` 本轮未动）。

三方对比（`live-prepush-r86/` 对 `baseline-r85/`）：**两个文件线上都 = 基线，零冲突**。
对方这期间改的是 `sections/gb-product.liquid` + `templates/index.json` + `templates/product.json`
（后两个是 Online Store Editor 托管，**我们绝不推**）。

推送前 diff 核算：css **删 103 / 增 51**，剔掉 30 行 build token 后 **124 行**，
与本地对基线的 diff 逐行相同。

**回读**：2 个文件**逐字节相同**。⚠ 文件数 **607 → 608，不是误伤** ——
对方在我们推送的那两分钟里又提交了 `blocks/_gb-features.liquid`（新增）并再改了
`gb-product.liquid` 与两个 template。我们用的是 `--only` 两个文件 + `--nodelete`，没碰他们任何东西。

**线上实测**：`tools/r86check.py --password 1234 --as-served` **全绿**（推之前 30 红）；
`tools/r85check.py --as-served` 也**全绿**（logo 那 18 条 `PEND` 除外）。

新基线 **`Gumi-Brand-shopify/baseline-r86/`（608 文件）**。

### 遗留

- ⚠ **PDP 卖点列表线上是空的**（对方本轮引入，见上）。
- ⚠ **`snippets/gb-logo.liquid` 仍未推**（r85 遗留，需授权）—— 线上三处 logo 在 2x 屏仍是碎图。
- ⚠ **`snippets/gb-logo.liquid` 仍未推**（r85 遗留，需授权）。
- 跑马灯 88×36 与「要不要一起把 duration 收到 13s」都等需求方确认。
- STYLE-GAP 新增 **C12**（features 的 DOM 位置）。

---

## 第八十五轮（2026-09-07）— 需求方点名的九处（`$build` = `20260907-r85`）

需求（对话）九条，逐条对号：thumb 焦点态、guarantee 图标尺寸、订阅卡描边、
footer 分隔线透明度、面板上边框、面板列对齐、logo 换 `<img>`、抽屉卡插画宽度、
reels 数量不足时居中不滚。**七条纯 CSS，一条 CSS+JS，一条 CSS+liquid。**

### 1. `.gb-product__thumb:focus-visible` = `.is-active`

`outline: none` + `border-color: $c-green`。理由和 r81 的 `.gb-reel` 一样：
`.gb-product__thumbs` 是可滚容器（一个轴设了 `overflow`，另一个轴被强制成 `auto`），
全局 `:focus-visible` 的 `2px/offset 2px` 环**四边全被裁**，键盘用户看不到焦点在哪。

⚠ 判据踩了老坑：`border-color` 挂着 `0.2s` 过渡，强制伪类后立刻读 = 读到起始值，
**会把一条好规则判成坏的**。`r85check` 里补了 400ms 等待（见 [[headless-transition-reads-start-value]]）。

### 2. `.gb-product__guarantee` 图标 —— 第八十轮登记的那条

`svg` → `svg, img` + `object-fit: contain`。`blocks/_gb-guarantee.liquid` 早在 r80 那次
就换成了 `<img>`，只写 `svg` 的规则从此不生效。**实测线上 106×100，应为 34×32** ——
5 个页面（index / pdp / our-story / how-gumi-works / reviews）都在放大近三倍的图标。
写法照抄 `.gb-product__taste-item` 的同一处修复。

### 3. `.gb-sub__plan` 描边从 inset 阴影改成 `::after` 覆盖环

**这是画法错，不是数值错**：inset 阴影画在**子元素下面**，而 `--sub` 的
`.gb-sub__panel` 是满宽实底，把左右下三边的描边整条盖住 —— 所以只有 `--once`
（背景在卡片自己身上）看得见。r65 起就是这样，一直没人发现。

```scss
.gb-sub__plan {
  position: relative;                 // 就这一条是新增的布局影响，且不建立层叠上下文
  &::after { position: absolute; inset: 0; border: 1px solid $c-green; border-radius: inherit; }
}
```

⚠ **仍然不能改回 `border`** —— 稿上 strokeAlign 是 INSIDE，真 border 会把 banner 顶进 1px、
把 popular 卡片从 334 撑到 336（r65 的原话保留在注释里）。
⚠ 也**没有用 `outline: 1px; outline-offset: -1px`**（写法更短、也画在子元素上面）：
Safari 16.4 以下的 outline 不跟随 `border-radius`，会在圆角卡上画出一个直角绿框。
⚠ `position: relative` 不影响下拉：`.gb-select` 自己就是 `position: relative`，
弹层锚在它身上，不在卡片上。

判据带**像素级**一条：截图取卡片左边缘第 0 列，改前是 lime-150（被盖住），改后是 #005635。

### 4~6. footer 分隔线 / 面板上边框 / 面板列对齐

- `.gb-footer__divider` 加 `opacity: 0.2`
- `.gb-header__panel` 加 `border-top: 1px solid $c-sand`
- `.gb-header__panel-inner` `align-items: center` → `flex-start`

⚠ **面板上边框在手机档关掉了**（和既有的 `border-bottom: 0` 并排）：手机是整屏抽屉、
从 y=0 起，那条发丝会落在状态栏下沿，稿里两条边都没有。**这一条是我的判断，不是需求方说的**，
不要就说一声，改回来是一行。

### 7. logo 换成了 `<img>` —— CSS 与 liquid 各坏一半

**CSS 一半（本地已改）**：三处 logo 规则都只写了 `svg`，
`snippets/gb-logo.liquid` 一旦 `settings.logo` 上传就渲染 `<img>`，规则全部落空。
实测线上：**footer logo 1440 档 411×106（应 193×50）、390 档 350×91（应 167×43）；
手机抽屉 logo 124×32（应 93×24）** —— 属性上的 width/height 只带了桌面一档，
且被主题的 `img` 规则改写。三处都补成 `svg, img` + `object-fit: contain`。

**liquid 一半（已改，未推）**：`{{ logo_img | image_url: width: w | times: 2 }}`
**过滤器顺序错了** —— `image_url` 先跑，`times: 2` 作用在**字符串**上返回 `0`，
于是线上是 `src="0"` 加一个 `0 2x` 候选。1x 屏靠 srcset 侥幸还能显示，**2x 屏必碎图**。
改成先 `assign w2 = w | times: 2` 再进过滤器；两个 URL 都手工 curl 过 200。

### 8. `.gb-nav-card__art` 手机档 `width: 100%`

桌面卡片宽、插画按 `135.2%` 外溢是稿上的做法；手机抽屉里的卡片窄得多，
同一个百分比把插画甩出了卡片。**实测 390：228 → 169（= 卡片宽）**。

### 9. reels 卡片装不满轨道时居中且不滚（CSS + JS）

`main.js` 的 `slider` 加 `fits()`：**量**所有 slide 的宽 + gap 之和，
`<= track.clientWidth` 就不建 Swiper（已建的销毁），并在 `[data-slider]` 上挂 `.is-static`；
CSS 让 `.swiper-wrapper` `justify-content: center` + `column-gap: inherit`，并隐藏箭头。

- **是量不是数**：卡片宽是 `max(304px, 21.1111vw)` 的 vw 斜坡，
  「几张算够」每个视口都不一样 —— 1440 是 4 张，**390 一张都算装得下、两张就不够**。
  需求方猜的「小于 5 个」正好是 1440 档的准确答案。
- ⚠ **只对 `loop` 轨道生效**（`if (!loop) return false`）。`rewind` 轨道（reviews 的
  expert 卡）本来就设计成到头即停，且它三张卡在 963~991 这 28px 里**正好装得下** ——
  不设门会把一个没人点名的布局改掉。判据专门有一条守着它。
- ⚠ resize 监听**只认宽度变化**（`innerWidth === lastW` 就早退）：手机地址栏收起会以
  同宽触发 resize，在那上面拆装轨道是肉眼可见的跳（[[mobile-toolbar-resize-rebuild]]）。
- 遗留：静态状态下 `.gb-reels` 仍带 `tabindex="0"`，Tab 会停在一个不能动的框上。

### 顺带查清，未修

- **线上首页 reels 只剩 6 张**（our-story / how-gumi-works 仍是 10）。6 张在 1440
  **仍然满得下**（1944 > 1440），逐格推进 8 次实测轨道无空洞，所以**不是 bug，不用管**；
  记下来是因为再少两张就会触发本轮的 static 分支。
- 静态状态下箭头是**隐藏**而不是 `disabled`。两种都合理，选了隐藏（桌面稿在卡片全排开时本来就没有 nav）。

### 新增判据

`tools/r85check.py` —— 三段：编译产物（9 条选择器 + `$build` + JS 里的 loop 门与 resize 守卫）、
静态站 1440/390、线上 1440/390（`page.route` 换 **css 和 js 两个**，或 `--as-served`）。
特别的两条：
1. **CDP `CSS.forcePseudoState`** 强制 `:focus-visible`，不靠 Tab 走 40 站；
2. **像素判据**给订阅卡描边（结构判据在改前也可能是绿的，只有取色能证明它被盖住了）。

**双向**：`--as-served` **66 红 / 18 pending**，换成本地 css+js **全绿**（pending 那 18 条是 liquid，见下）。

### 文件清单

```
改  assets/customstyle.scss     九处 + $build → r85
改  assets/customstyle.css      重新编译（与基线 diff = 54 行，正好是这九处）
改  assets/main.js              slider: fits() + is-static + 宽度触发的 apply()
改  全部 13 个 html             ?v= r84 → r85（140 处；含另一会话新建的 account.html）
新  liquid/snippets/gb-logo.liquid   image_url 过滤器顺序（未推）
新  liquid/r85.patch
新  tools/_apply_r85.py / tools/r85check.py
```

### 验证

- `tools/r85check.py --skip-live` 全绿；`--password 1234 --as-served` 66 红；`--password 1234` 全绿
- `tools/rwd.py` 全站 11 页 × 10 档 **全绿**（面板加边框、列改 flex-start 都没撑破）
- `shopify theme check` 改前改后同为 **28 offenses / 8 errors**

### ⚠ 三方对比 + 并行会话

- 线上自 r84 起只动了 `sections/gb-nutrition.liquid`（对方给它加了 `scallop_variant` 下拉，
  即 STYLE-GAP 的 **C5**，已由对方自行落地）。**清单内 3 个文件线上都 = 基线，零冲突。**
- ⚠ **同目录有另一个 Claude 会话在跑**（`80bab8cd-…`，09:18 仍在写），正在做 account 页
  （新提交 `29a7638`、新建 `account.html` / `assets/account.*` / `tools/acct*.py`）。
  `assets/account.scss` 是独立入口、自带 `?v=…-a1`，**不依赖 `customstyle.scss`**，两边不冲突；
  我的 `?v=` 批量替换**顺带把 account.html 的 4 处 r84 也换成了 r85**（那页确实加载
  `customstyle.css`，不换就吃旧样式，属于必要的一步）。

### 推送（2026-09-07，已上线）

**3 个文件**：`assets/customstyle.css` / `assets/customstyle.scss` / `assets/main.js`。
需求方先说「先推 css 和 scss」，随后补「和 js」——**liquid 那一条没在授权范围内**。

三方对比（`live-prepush-r85/` 对 `baseline-r84/`）：**三个文件线上都 = 基线，零冲突**。
对方这期间只改了 `sections/gb-nutrition.liquid`（不在清单内）。

推送前 diff 核算：css **删 24 / 增 60**，剔掉 30 行 build token 后正好 **54 行**，
与本地对基线的 diff 逐行相同；scss 删 10 / 增 59（含 1 行 token）；main.js 删 5 / 增 38，
**全部落在 `slider.bind` 一段**。

**回读**（`live-after-r85/`）：文件数 **607 → 607 零增删**、3 个文件**逐字节相同**、
**604 个清单外文件零改动**。

**线上实测**：`tools/r85check.py --password 1234 --as-served` —— **全绿**
（推之前同一判据 66 红）。18 条 `PEND` 仍在，那是 logo 的 `src`，见下。

新基线 **`Gumi-Brand-shopify/baseline-r85/`（607 文件）**。

### 遗留

- ⚠ **`snippets/gb-logo.liquid` 未推**（需单独授权）。改后的文件在
  `liquid/snippets/gb-logo.liquid` + `liquid/r85.patch`，工作副本 `Gumi-Brand-shopify/work-r85/`。
  在推之前，线上三处 logo 仍是 `src="0"` + `0 2x` 候选 —— **1x 屏能看，2x 屏碎图**。
  `r85check` 的 18 条 `PEND` 就是它，推完才会转绿。
- STYLE-GAP 的 §二（后台 9 条）/ §三（liquid，C5 已由对方完成、C11 是本轮新增的 logo）仍未动。

---

## 第八十四轮（2026-09-07）— 静态站 ↔ live 全站样式比对 + 四处输给主题 CSS 的声明（`$build` = `20260907-r84`）

需求方要求「检查网站和静态站的样式差别，再尽可能不改结构的情况下（需要个清单）修复一些样式 bug」。
全站 11 页 × 390/768/1440 三档比对，产出 [STYLE-GAP.md](STYLE-GAP.md) 一份清单，
**只修其中 CSS 能改的四条**，其余（后台设置 9 条、liquid 10 条）逐条登记等裁决。

### 改了什么

四条症状不同，真因是同一件事：**我们的选择器只有 0-1-0，被 Horizon 自己的 0-1-1 压掉**。

1. **`.gb-footer__input`（11 页）** — 边框算出来是 `#dfdfdf`，稿是 `rgba(1,19,7,.1)`。
   凶手是 base.css 的 `textarea, input:not([type="checkbox"], [type="radio"])`：
   `:not()` 取参数里最高的那一档，`[type=...]` 是 0-1-0，加上 `input` 的 0-0-1 = **0-1-1**。
   底色一起被它的 `var(--color-input-background)` 接管（当前恰好也是白，是**潜伏**不是没发生）。
2. **`.gb-field__input` / `.gb-field__control`（get-in-touch / referral）** — 同一条规则，
   边框 `#cccccc` 变 `#dfdfdf`。
3. **`.gb-form__disclaimer`（referral，≤1280）** — 底部 `-2px` 被 Horizon 的
   `:last-child:is(p,h1..h6)`（同样 0-1-1）清成 0，免责声明与提交按钮之间多出一截。
4. **`.gb-promo` / `.gb-vs` / `.gb-app-section`（pdp）** — 整块窄一圈：1440 档 **1360**、
   390 档 **358**。三个 section 的 schema 写了 `"class": "section"`，
   Horizon 的 `.section > * { grid-column-start: 2 }` 把它们塞进栅格的居中列。

前三条的改法是把**被压掉的那两三条声明**在 0-2-0 重述一遍（`.x.x`），第四条是
`.section > .gb-promo, … { grid-column: 1/-1; }`。

### 为什么这么改

- **不直接把原规则的选择器加粗成 `.x.x`** —— `.gb-field__input--select` 只有 0-1-0，
  整条加粗会连它的 `padding-right` 和箭头背景一起压死。只重述输掉的那几条。
- **重述块排在被修规则之前** —— 那两条规则里的 `:focus-visible` 与
  `.gb-field__input--select:hover` 同样是 0-2-0，靠源码顺序赢；排到后面会把焦点态和
  hover 一起压死。`r84check.py` 里有两条断言盯着这个顺序。
- **不去喂 Horizon 的变量**（`--color-input-border`）—— 那样看着更省事，但主题升级改了
  变量名就会静默失效，而我们自己的规则还是输的，等于回到原点。特异性是版本无关的。
- **第 4 条只是补偿** —— 根治是把三个 section 的 `"class": "section"` 去掉（liquid），
  去掉后这条 CSS 变成空转，可以一并删。已登记进 STYLE-GAP C6。

### 顺带查清、**未修**（等裁决，全在 STYLE-GAP.md）

- **后台就能改 9 条**：reviews 的 hero 勾了 Center layout（稿是左对齐+配图）；
  5 个文字页 hero 的 Size 填了 Large，按大波浪预留、却画小波浪 —— 1440 档空出 31px，
  390 档反过来波浪压进下一区块 13px；`gb-product` 没挂进 4 个模板；
  science/reviews 的 hero 图没传；footer 社交链接是空的。
- **需要 liquid 10 条**：`gb-page-hero.liquid` 把副标题修饰类和尾部波浪**写死**了 ——
  science 的 hero 波浪是白色压在奶油色区块上（实测 `fg=#ffffff` / 下方地色 `#faf9f8`），
  四页的大波浪画成了小的，faq 少 `--lh-24`、privacy 少 `--privacy-mobile`；
  `gb-promo.liquid` 没有 scallop setting、也没输出卡片中缝的 `__lip`；
  `gb-nutrition → gb-product` 的交界波浪仍然没有（第八十一轮的遗留）。

### 新增的判据（三个都可复跑）

| 脚本 | 回答什么 |
|---|---|
| `tools/gapstyle.py` + `gapreport.py` | 同一个类，两边算出来的样式差在哪；几何单列不作判据 |
| `tools/losers.py` | live 上哪条声明输给了主题自己的 CSS（走 CDP `CSS.getMatchedStylesForNode` 读真层叠） |
| `tools/wavecheck.py` | 每条波浪的尺寸 / 配色 / 它下面**真正的地色** |
| `tools/gapwhy.py` | 单个选择器的追因：真实 class 属性 + 祖先链 + 命中的规则 |
| `tools/r84check.py` | 本轮四项，`--as-served` 必须全红 |

⚠ **`losers.py` 写了三遍才不撒谎**，三个坑都值得记：
① 只看有 `text` 的声明会漏掉简写 —— `border: 1px solid #ccc` 与
`border-color: var(--color-input-border)` 属性名根本对不上，必须展开成 longhand；
② 含 `var()` 的简写 Chrome **展不开**（pending substitution），得手写一张简写表补；
③ 逻辑属性要归一到物理属性，否则 `summary { padding-block }` 和我们的 `padding-top`
看起来像两件事，清单里全是假警报（`.gb-faq__row` 就这么误报过一次）。
④ 节点 id 是**按文档**发的，跨页缓存 class 会张冠李戴（`.gb-dosed__lead` 一度被报成 `<select>`）。
⑤ **必须逐宽度跑** —— `.gb-form__disclaimer` 的负边距只写在 `@include narrow` / `tablet` 里，
只跑 1440 一档完全看不见。

### 文件清单

- `assets/customstyle.scss` — 四处修复 + `$build` → `20260907-r84`
- `assets/customstyle.css` — 重新编译
- `*.html`（11 页 + font-check）— `?v=` 129 处
- `docs/STYLE-GAP.md` — **新增**，本轮清单
- `tools/gapstyle.py` / `gapreport.py` / `gapwhy.py` / `losers.py` / `wavecheck.py` / `r84check.py` — 新增
- `docs/CHANGELOG.md` / `docs/HANDOFF.md`

### 验证

- `r84check.py --skip-live`：编译产物 8 条 + 静态站 30 条全绿（静态站必须**零变化**，
  `.section` 在那边不存在，两条重述块的值与原值相同）
- `r84check.py --password 1234 --as-served`：**19 红**（就是这四条缺陷）
- `r84check.py --password 1234`（把本地 css 用 `page.route` 换进 live）：**全绿**，两档都过
- 回归：`r83`/`r82`/`r81`/`r80`/`r79`/`r78` 全绿，`r64check` 1528 ok / 0 red，`rwd.py` 全绿

### 推送（2026-09-07，已上线）

需求方「先 scss 和 css，其余记录」—— **2 个文件**：`assets/customstyle.css` /
`assets/customstyle.scss`。`main.js` 本轮未改，不在清单。

⚠ **三方对比抓到对方当天改了 6 个 section**：正在把写死的波浪逐个换成 `scallop_variant`
下拉（`gb-vs` / `gb-app-section` / `gb-product` / `gb-footer-cta` / `gb-reviews`），
默认值等于原来的写死值，**渲染结果没变** —— 推完重跑 `wavecheck` 仍是同样 24 行。
`config/settings_data.json` 与 14 个 `templates/*.json` 也变了。
**清单内两个文件线上 = 基线，零冲突。**

推送前 diff：**删 15 / 增 43**。删的 15 行全是 `?v=` 版本号从 r83 换到 r84，
增的除同样 15 行外就是四条新规则的 28 行。**恰好等于本轮改动，零多余。**

回读：**607 → 607**，`live-after-r84` 对 `live-prepush-r84` 只有清单内两个文件不同，
且与本地逐字节相同 —— 605 个清单外文件零改动。
线上 `r84check.py --password 1234 --as-served` **全绿**（推之前同一判据 19 红，判据是双向的）。
新基线 **`baseline-r84/`（607 文件）**；push 副本与推送前快照已删。

### 遗留

- STYLE-GAP 的第二、三节（后台 9 条 / liquid 10 条）一条没动，等裁决。
  ⚠ 对方的 `scallop_variant` 重构**没有覆盖 `gb-page-hero.liquid` 与 `gb-promo.liquid`**，
  C1 / C2 / C3 仍然成立；且新下拉**只选颜色不选尺寸**，C2 的「大波浪画成小波浪」那一半
  在任何 section 上都还不是 setting。
- `.gb-product__guarantee` 的图标尺寸（5 页）仍未修 —— 第八十轮就登记了，不在点名范围内。

## 第八十三轮（2026-09-07）— science 标题收窄居中 + 卡片正文去掉顶距（`$build` = `20260907-r83`）

需求（对话）：`.gb-science__title` 加 `max-width: 660px; margin: 0 auto;`；
`.gb-science-card__text` 的 `margin-top` 改 0。然后推送。

### 1. ⚠ `margin: 0 auto` 会压过手机端的 `align-items: flex-start`

`.gb-science__head` 是 `flex-direction: column`，桌面 `align-items: center`，
**但 `@include narrow` 里是 `align-items: flex-start` + `text-align: left`** ——
手机稿就是左对齐的（`228:8166`，两个 TEXT 节点都是 `textAlignHorizontal: LEFT`）。

**flex 项目上的 auto margin 优先级高于 `align-items`**，所以直接加 `margin: 0 auto`
会把手机端的标题也居中。**改前实测（静态站 index）**：

| 档 | `align-items` | 左空隙 | 右空隙 | 结果 |
|---|---|---|---|---|
| 1440 | center | 10 | 10 | 居中 ✓ |
| **390** | **flex-start** | **28** | **28** | **被 auto margin 强制居中** ✗ |

需求没提手机端，而手机端左对齐是稿里定的 —— 按「只点名 A 就只改 A」保持原样，
在既有的 narrow 块里补一句 `margin: 0`：

```scss
.gb-science__title {
  max-width: 660px;
  margin: 0 auto;
  // ⚠ margin:0 here is load-bearing -- an auto margin outranks align-items.
  @include narrow { margin: 0; font-size: 30px; … }
}
```

**改后四档实测**：1440 / 1024 居中，767 / 390 左对齐（`margin-left: 0px`）。

ℹ **`max-width: 660` 只在首页咬得住**：`/pages/science` 的两块 science 在所有档位下
标题都填满了 `__head`（`gapL == gapR == 0`），`max-width` 与 auto margin 都无从发挥。
原值 `1072px` 同理也从未生效过。

### 2. `card__text` 的顶距

`margin-top: 6px` 是**任务文档第三组第 1 条**点名要的（第五十三轮落地，
当时还专门记过「这一句没写作用域，所以六张卡全都吃到」）。本轮反转回 0。

`.gb-science-card__text` 是 `<p>`，reset 的 `h1…p { margin: 0 }` 已经保证 0，
所以**直接删掉那条声明**而不是写 `margin-top: 0` —— 少一条声明，也不会让人误以为在覆盖什么。

### 文件清单

```
assets/customstyle.scss   .gb-science__title max-width 1072 → 660 + margin: 0 auto
                          + narrow 补 margin: 0；.gb-science-card__text 删 margin-top；
                          $build → r83
assets/customstyle.css    重新编译
*.html                    129 处 ?v= → 20260907-r83（12 个文件）
tools/r83check.py         新增，本轮判据（离线 + 静态站 2 页 × 4 档 + 线上 2 页 × 4 档）
```

### 验证

`python3 tools/r83check.py --password 1234 --as-served` —— **全过，2 条明确跳过**。
线上首页 1440 / 1024 居中、767 / 390 左对齐且 `margin-left: 0px`；两页所有档
`card__text` 的 `margin-top` 都是 `0px`。

⚠ **判据自己错了两次，都是"测点/期望值"的问题**：

1. **满宽被误判成居中**。第一版用 `abs(gapL - gapR) < 2` 判居中，
   而 `/pages/science` 的标题填满了 `__head`，`gapL == gapR == 0` ——
   满宽和居中在几何上不可区分，判据把它当成了居中。
2. **给每个页面硬编码了期望对齐**。改成断言**机制**而不是结论：
   手机档验 `gapL < 2` + `margin-left: 0px` + `align-items: flex-start` 三个锚点；
   桌面档若标题本来就满宽（没有空间可分配），**明确 SKIP 并打印原因**，不硬编码。

回归：`r82check` / `r81check` / `r80check` / `r79check` 全过，`r64check` 1528 ok / 0 red。

### 推送（2026-09-07，已上线）

**2 个文件**：`assets/customstyle.css` / `assets/customstyle.scss`。`main.js` 三方一致，未列清单。

三方对比（`live-prepush-r83/` 对 `baseline-r82/`）：**两个文件线上都 = 基线，零冲突**。
对方这期间改了 `sections/gb-reviews.liquid` 与 `templates/product.json`，都不在清单里。

推送前 diff：**删 17 / 增 18**，剔掉 build token 后删的是 `max-width: 1072px` 与
`margin-top: 6px`，增的是 `max-width: 660px` / `margin: 0 auto` / narrow 的 `margin: 0`。
**恰好等于本轮三处改动。**

**回读**：文件数 **607 → 607**、2 个文件**逐字节相同**。
⚠ **清单外有 2 个文件变动**：`templates/index.json` 与 `sections/header-group.json`。
**证实是对方同期在后台改的，不是误伤** —— index.json 的改动是**文案补空格**
（`"30 DayMoney Back Guarantee"` → `"30 Day Money Back Guarantee"` 等三处）
外加给一个 section 设 `"disabled": true`，**只有 Online Store Editor 能做这种改动**；
header-group.json 格式化后语义零差异（仅空白/键序）。我方推送清单里从来没有任何 JSON
（铁律：绝不推 `templates/*.json` / `*-group.json` / `settings_data.json`）。

新基线 **`Gumi-Brand-shopify/baseline-r83/`（607 文件）**。

---

## 第八十二轮（2026-09-07）— reel focus 改为镜像 hover + richtext 的 `<p>` 继承标题（`$build` = `20260907-r82`）

需求（对话）两条：① **去掉 `.gb-reel:focus-visible::after`，focus-visible 改为和 hover 效果相同**；
② **`.gb-stats__title` / `gb-nutrition__title` 等内部的 `<p>` 需要继承 title 的样式**。
③ 推送，**但先不推 liquid**。

### 1. reel focus：推翻第七十八轮的 `::after` 环

r78 用 `::after` 画环是有原因的（rail 的裁切框就是卡片盒，真 outline 会丢掉上下两条；
负 `outline-offset` 会被 `.gb-reel__media` 盖掉，三个候选都实测过）。
本轮需求方改为**和 hover 一样**，环整个撤掉：

```scss
&:focus-visible {
  outline: none;
  .gb-reel__media { transform: scale(1.06); }
}
```

⚠ **这条不能放进 `@include hover`** —— 那个 gate 是 `(hover: hover)`，
触摸设备上接键盘的用户会完全看不到焦点在哪。hover 那条仍单独留在 gate 里。

ℹ **可访问性上这是降级**（缩放比描边弱），但需求方明确要求，已记进「不要报成 bug」。

### 2. richtext 的 `<p>`：标题塌成正文大小

**根因**：Shopify 的 `richtext` setting **强制**把值包进 `<p>`，
而 `gb-stats.liquid` / `gb-nutrition.liquid` 把它直接印进 `<h2>`：

```liquid
<h2 class="gb-stats__title" data-line-reveal>{{ s.title }}</h2>
```

base 的 `p { font-size: 16px; line-height: 24px; letter-spacing: -0.32px; }`（0-0-1）
直接命中那个 `<p>`，而 `.gb-stats__title` 的规则命中的是 `<h2>` —— **子元素有自己的规则就不再继承**。

**改前线上实测**：

| 宿主 | `<h2>` 计算值 | 内部 `<p>` | 宿主实高 |
|---|---|---|---|
| `.gb-stats__title` | 56px / lh 64 / ls -0.56 | **16px / lh 24 / ls -0.32** | 48（两行 56px 本该 128） |
| `.gb-nutrition__title` | 40px / lh 48 / ls -0.4 | **16px / lh 24 / ls -0.32** | 24 |

```scss
.gb-stats__title p,
.gb-nutrition__title p {
  font: inherit;              // size, line-height, family, weight in one
  letter-spacing: inherit;    // not part of the font shorthand
}
```

**放在 base 的 `p` 规则正下方**，因为它就是来抵消那一条的 —— 因果关系一目了然，
`grep '__title p'` 一次找齐（铁律 4）。

⚠ **范围判定写进了注释**：宿主是 `*__title` 且 setting 是 `"type": "richtext"` 且**没走
`gb-rich-inline`**（r71 那个服务端剥壳 snippet）。全主题扫下来只有这两个符合：

| section | title 的 setting 类型 | 会不会带 `<p>` |
|---|---|---|
| `gb-stats` / `gb-nutrition` | **`richtext`** | **会** ← 本轮修的 |
| `gb-science` | `inline_richtext` | 不会（只允许行内标签） |
| `gb-expert` | `text` + `escape` | 不会 |
| `gb-hero` / `gb-product` / `gb-footer` / `gb-form-section` | `richtext` 但走 `gb-rich-inline` | 服务端已剥壳 |

静态站的 title 是纯文本 + `<br>`，**这条规则在那边零匹配**。

### 文件清单

```
assets/customstyle.scss   .gb-reel:focus-visible 换成 media scale（删 ::after 块）；
                          base p 规则下方新增 title <p> 继承块；$build → r82
assets/customstyle.css    重新编译
*.html                    129 处 ?v= → 20260907-r82（12 个文件）
tools/r82check.py         新增，本轮判据（离线 20 + 静态站 7 + 线上 13）
tools/r78check.py         改：reel 环的断言交给 r82check，保留「outline 被压掉 +
                          focus 仍有可见反馈」这个不变契约；像素扫描换成读 transform
```

### 验证

`python3 tools/r82check.py --password 1234` —— **全过**。
线上实测两个 title 的 `<p>` 三项（font-size / line-height / letter-spacing）**全部等于宿主**，
reel 的 `::after` 为 `none`、focus 时 media 是 `matrix(1.06, …)`。

⚠ **`r78check` 报了 5+4 红，全是 reel 环** —— 判据绑死了本轮推翻的实现，不是回归。
**这是本项目第五次**（前四次：r77check 绑 `--animation-speed`、r78/r73check 绑 `$build`、
r64check 绑 `object-fit: cover`）。已改成断言不变契约。

⚠ **改 `r78check` 时自己踩了 headless 的老坑**：Tab 之后立刻读 `.gb-reel__media` 的
transform，拿到的是**过渡起始值** `matrix(1,0,0,1,0,0)`，报红。
`:focus-visible` 的锚点是绿的，所以一眼能看出「匹配上了但值没动」＝ 时序问题。
补 400ms 等待后全过。见 memory `headless-transition-reads-start-value`。

回归：`r81check` / `r80check` / `r79check` / `r77check` 全过，`r64check` 1528 ok / 0 red。

### 推送（2026-09-07，已上线）

**2 个文件**：`assets/customstyle.css` / `assets/customstyle.scss`。
⚠ **线上此前停在 r80**（r81 改完等指令时未推），所以这次推送**同时带上了 r81 与 r82 两轮**。
`main.js` 三方逐字节相同，未列进清单。**本轮未推任何 liquid**（需求方明确「先不推 liquid」）。

三方对比（`live-prepush-r82/` 对 `baseline-r80/`）：**两个文件线上都 = 基线，零冲突**。
对方这期间改了 5 个文件（`config/settings_data.json` / `sections/gb-product.liquid` /
`snippets/gb-nl-modal.liquid` / `templates/index.json` / `templates/product.json`），
**都不在清单里**。逐条看过 `gb-product.liquid` 的 diff —— 只是给营养标签弹窗加了
`default_nutrition` 的 metaobject fallback，**scallop 部分一字未动**，
第八十一轮的波浪结论不受影响。

推送前 diff 核算：**删 25 / 增 25**，剔掉 30 行 build token 后 ——
删的是 2 条 `object-fit: cover`（r81 改的）+ 8 行 `::after` 环（r82 删的），
增的是 2 条 `object-fit: contain` + 5 行 title `<p>` 块 + 2 行 focus scale。
**没有一条误删的既有规则。**

**回读**：文件数 **607 → 607 零增删**、2 个文件**逐字节相同**、**605 个清单外文件零改动**。

**线上实测**：`r82check` / `r81check` 的 `--as-served` **双双全过**。

新基线 **`Gumi-Brand-shopify/baseline-r82/`（607 文件）**。

---

## 第八十一轮（2026-09-07）— 产品图改 `contain` + 查 nutrition/product 交界波浪消失（`$build` = `20260907-r81`）

需求（对话）两条：① `.gb-product__image` 与 `.gb-product__thumb` 下的 `img/video/picture`
改为 `object-fit: contain`；② **查 `gb-nutrition` 与 `gb-product` 交界处的波浪形状为什么没了**。

### 1. `contain`：这是对第六十四轮的反转

⚠ **第六十四轮第 5 条是需求方点名的**：「占位图容器只有灰底，内部要给 `img` / `video`
加 100% + **`object-fit: cover`**」，当时 9 个容器一起补的 `@include cover-img`。
本轮把其中**两个**改成 `contain` —— 产品图不能被裁。
**代价是灰底 `$c-gray-200` 会在图片周围露成 letterbox**，这是 `contain` 的必然结果，
不是没盖住。**别按 r64 改回去。**

**做法：给 mixin 加参数，不在调用处叠第二条 `object-fit`。**

```scss
@mixin cover-img($fit: cover) { width: 100%; height: 100%; object-fit: $fit; display: block; }

.gb-product__image img, video, picture { @include cover-img(contain); }   // 同 __thumb
```

⚠ 第一版写的是 `@include cover-img; object-fit: contain;` —— **能工作但脏**：
产物里同一个块出现两条 `object-fit`，靠源码顺序决胜，而且会让**任何「数 cover 用量」的判据虚高**
（`r64check` 就有这么一条）。加参数后产物里每块只有一条。
**mixin 的默认值必须留在 `cover`** —— 另外 11 个调用点都读它。

⚠ 注释里原本写了 `@include cover-img` 这个词，导致 `grep -c 'include cover-img'` 从 13 变 14。
**这正是 `r63check` 踩过的坑**（注释里的词被判据数进去）。措辞已改，
`r81check` 的对应断言也**先剥 `//` 注释再数**。

ℹ `picture` 那一档实际不起作用（reset 里 `picture { display: contents }`，
不是替换元素，`object-fit` 对它无意义），但 13 处调用一直是这个三元组，保持一致没有拆。

### 2. 波浪查因：**不是"没了"，是线上从来没有输出过**

`gb-nutrition → gb-product` 的交界**只在首页**。静态站 `index.html` 里，波浪是
**`gb-product` 的第一个子元素**（第四十几轮把归属从"上面那个 section"反转成"下面那个"）：

```html
<section class="gb-product gb-product--lg">
  <div class="gb-scallop gb-scallop--edge-top gb-scallop--lg gb-scallop--lime-to-white gb-scallop--bleed"></div>
```

**线上三条独立证据都指向同一个结论 —— 那个节点根本不存在：**

| 证据 | 实测 |
|---|---|
| `sections/gb-nutrition.liquid` | `scallop` 命中 **0** |
| `sections/gb-product.liquid` | 只有一处，在 `{% content_for 'blocks' %}` **之后**（section 尾部），class 是 `--edge` 不是 `--edge-top`；setting 只有 `show_scallop`（trailing） |
| `templates/index.json` | `gb-product` 的 settings 只有 `{"show_scallop": true}`，没有 leading |

**线上首页 DOM 实测**：`gb-nutrition` 与 `gb-product` 之间一条 `.gb-scallop` 都没有，
`nutrition.bottom == product.top == 4791`（严丝合缝，中间零像素，
而这条波浪本该占 `--sc-lg-h` ≈ 128px）；`gb-product` 的第一个子元素直接是 `gb-product__inner`。

⚠ **排除了三种猜测**：不是配色填错（r76 那次的病）、不是 setting 被关掉、
不是本轮或对方最近的改动引起 —— 对方这两天对 `templates/index.json` 的唯一改动是
**文案**（标题多了空格、`<br>` → `<br/>`），与波浪无关。

**这是结构缺失，CSS 补不出来**（`.gb-scallop` 虽是纯 CSS 画的，但需要一个占位节点）。

**建议的修法：让对方给 `gb-product.liquid` 加 leading scallop —— 他们已有现成范式。**
线上 `gb-science` 就有 `leading_scallop` / `trailing_scallop` 两个 setting，
DOM 里实测输出了 `gb-scallop gb-scallop--edge-top gb-scallop--cream-to-sand`。
`gb-product` 照抄即可。

⚠ **但照抄不够，还要支持 `--bleed`**：静态站这条同时带 `--lime-to-white` **和** `--bleed`，
而 `--bleed` 在源码里更靠后，会把 `--wave-bg` / `--wave-under` 双双压成 `transparent` ——
**波浪上半是透明的，让 nutrition 的包装袋从缺口继续往下露**。
这是设计的有意为之（Figma 里那个 Spacer 的 `frameFill` 是 `none`，全站独一份，
见 memory `figma-render-locally-from-image-fills` 一族的项目笔记）。
`gb-science` 的 `cream-to-sand` 是不透明档，直接套过来会**把缺口填实**。

**本轮未动 liquid**（改 liquid 需逐次授权），只出结论。

### 文件清单

```
assets/customstyle.scss   cover-img mixin 加 $fit 参数；.gb-product__image / __thumb
                          改 @include cover-img(contain)；$build → r81
assets/customstyle.css    重新编译
*.html                    129 处 ?v= → 20260907-r81（12 个文件）
tools/r81check.py         新增，本轮判据
tools/r64check.py         改：object-fit 断言从「一律 cover」改成按选择器区分（见下）
```

### 验证

`python3 tools/r81check.py --password 1234` —— 离线 17 条 + 线上 4 条**全过**。
线上 PDP 实测两个容器的 `object-fit` 都是 `contain`。

⚠ **`r64check` 报了 72 red，全部是这两个容器的 `object-fit=contain`** ——
**判据绑死了被本轮推翻的取值**，不是回归。已改成按选择器区分
（`CONTAIN_BOXES = {".gb-product__image", ".gb-product__thumb"}`，其余 7 个仍断言 cover），
改后 **1528 ok / 0 red**，总条数不变。
这是本项目第四次遇到「判据绑死了某一轮的具体取值」——
前三次是 `r77check` 绑 `--animation-speed`、`r78check` / `r73check` 绑 `$build`。
**写判据时凡是"客户可能反转的取值"，都应该按 key 区分而不是写死一个常数。**

⚠ **`r81check` 的静态站断言第一版方向写反了**：我断言两个容器里**有** `img`，
结果 2 红 —— 静态站上它们是**空的灰占位**（scss 注释就写着
"Grey boxes are the design's own placeholders — no product photos exist yet"）。
真正该断言的是「盒子在、内容不在」，真实测量只能在线上做。改后全过。

回归：`r80check` / `r79check` / `r77check` 全过。

### 推送

**未单独推，随第八十二轮一并推出**（2026-09-07）。线上此前停在 r80，
所以那次推送的 2 个文件同时带上了 r81 与 r82 两轮的改动。
线上实测 `tools/r81check.py --password 1234 --as-served` 全过。

---

## 第八十轮（2026-09-07）— `packed-item` / `taste-item` 的图标：线上换成 `<img>` 后失去尺寸约束（`$build` = `20260907-r80`）

需求（对话）两步：① **「`gb-product__packed` 下面的 `gb-product__packed-item` 需要修改成静态站，
原来的圆圈换成了图片」**；② 报告了同病的 taste / guarantee 之后，
需求方点名 **「`gb-product__taste-item` 同样修改」**（guarantee 未点名，未动）。

⚠ **taste 合并进本轮而不是另开 r81** —— r80 当时还没推过 live，
另开一号会让线上出现一个从未被服务过的 build token（r61 / r64 有过这个教训）。

### 1. 根因：样式只认 `svg`，而 width/height 属性只给比例不给尺寸

对方把 `blocks/_gb-packed.liquid` 的占位圆圈换成了 `image_picker`：

```liquid
<img src="{{ block.settings.image | image_url: width: 80 }}" width="34" height="32" ...>
```

我们的规则写的是 `svg { width: 34px; height: 32px; flex-shrink: 0; ... }` —— **`<img>` 一条都不匹配**。
而 HTML 的 `width` / `height` 属性**只声明宽高比，不是尺寸**（memory
`img-dims-attrs-give-ratio-not-size`），reset 里的 `img { height: auto }` 又把高度交还给比例，
于是图片按**固有尺寸**渲染。

**实测（`tools/r80probe.py`，线上 PDP 1440 档）**：

| | 静态站（目标） | 线上（改前） |
|---|---|---|
| 图标 | `<svg>` **34×32**，`flex-shrink: 0` | `<img>` **171×161**，`flex-shrink: 1` |
| 行高 | 32 | **161** |

⚠ 171 而不是 `image_url: width: 80` 请求的 80 —— **固有尺寸不受那个参数控制**，
所以「liquid 里已经写了尺寸」不能当作约束，CSS 必须自己给。

### 2. 改法

```scss
.gb-product__packed-item {
  ...
  svg, img { width: 34px; height: 32px; flex-shrink: 0; object-fit: contain; color: $c-cream; }
}
```

- **`svg, img` 而不是只换成 `img`** —— 静态站与设计稿仍是占位圆圈，两边都要覆盖。
  静态站上 `img` 那一半零匹配。
- **特异性 0-1-1** 压过 reset 的 `img { height: auto }`（0-0-1），否则高度会被悄悄丢掉。
- **`object-fit: contain`** —— 图片未必正好是 34:32，`fill`（默认）会拉变形。
- `color: $c-cream` 对 `<img>` 无意义，但 svg 那一半需要，保留。

### 文件清单

```
assets/customstyle.scss   .gb-product__packed-item + .gb-product__taste-item 的图标规则
                          svg → svg, img（各加 object-fit: contain）；$build → r80
assets/customstyle.css    重新编译
*.html                    129 处 ?v= → 20260907-r80（12 个文件）
tools/r80check.py         新增，本轮判据（离线 22 + 线上 10）
tools/r80probe.py         新增，量三处图标行的尺寸（静态站 vs 线上对照），可复跑
```

### 验证

`python3 tools/r80check.py --password 1234` —— **全过**。
线上 packed 图标 **171×161 → 34×32**、行高 **161 → 32**、`object-fit` 生效。

**判据是双向的**：`--as-served`（线上还没推）**4 红**，
而锚点 `live icon is an <img>` 仍绿 —— 证明测的是对的元素，红的是尺寸本身。

回归：`r79check` / `r78check` / `r77check` / `r73check` 全过。

### 3. taste：同一处方，但**不加** `flex-shrink`

```scss
.gb-product__taste-item {
  ...
  svg, img { width: 51px; height: 48px; object-fit: contain; color: $c-cream; }
}
```

⚠ **和 packed 的差别不是漏写**：`.gb-product__taste-item` 是 `flex-direction: column`，
图标在列方向上，`flex-shrink` 作用在高度而非宽度；板上没有它，静态站的 svg 也没有。
**加上去是偏离静态站，不是修得更稳。** 判据专门有一条
`taste carries no flex-shrink (matches static)` 守着这一点。

**实测线上 taste 图标 `<img> 106×100 → 51×48`**（106 是被 `.gb-product__taste-item`
自己的 `width: 106px` 卡出来的，不是图的原始尺寸）。

### ⚠ 顺带发现，未修（需求方未点名）

**`.gb-product__guarantee` 是同一个病、同一次改动引入的**：
`blocks/_gb-guarantee.liquid` 也换成了 `<img>`（`width: 80`，属性 34×32），
而 `.gb-product__guarantee` 的规则同样只写了 `svg { width: 34px; height: 32px; ... }`。

⚠ **它的影响面比 packed / taste 都大 —— 在 5 个页面上**：
`index` / `pdp` / `our-story` / `how-gumi-works` / `reviews`（实测 grep）。
按铁律 20 未动。判据 `r80check.py` 每轮把它的实测尺寸**打印出来但不断言**，
下一轮能直接看到有没有被处理。
⚠ 它不在 PDP 页的 `.gb-product__packed` 区域内，**线上探针在 PDP 上测不到它**，
要验得换一个有它的页面。

### 推送（2026-09-07，已上线）

**2 个文件**：`assets/customstyle.css` / `assets/customstyle.scss`。
`main.js` 本轮未改 —— 三方对比里本地 / 线上 / 基线**逐字节相同**，不列进清单。

三方对比（`live-20260907-prepush-r80/` 对 `baseline-r79/`）：**两个文件线上都 = 基线，零冲突**。
对方这期间只改了 `templates/index.json`（Online Store Editor 托管，**我们绝不推**）。

推送前 diff 核算：**删 17 行 / 增 19 行**，剔掉 15 行 build token 后 ——
**删的 2 行正是被改写的那两条选择器**（`.gb-product__taste-item svg` /
`.gb-product__packed-item svg`），增的 4 行是新选择器 + 两条 `object-fit`。
`diff` 里没有一条误删的既有规则。

**回读**（`live-20260907-after-r80/`）：文件数 **607 → 607 零增删**、
2 个文件**逐字节相同**、**605 个清单外文件零改动**。

**线上实测**：`tools/r80check.py --password 1234 --as-served` **全过**
（packed 171×161 → 34×32、行高 161 → 32；taste 106×100 → 51×48）。

新基线 **`Gumi-Brand-shopify/baseline-r80/`（607 文件）**。

---

## 第七十九轮（2026-09-07）— 购物车抽屉的退场时长与桌面端滚动锁（`$build` = `20260907-r79`）

需求（对话）：**「先改 BH 和 BI 还原静态站的效果」** —— 第七十七轮登记的两条待裁决。

⚠ **两条改动是耦合的，不能只做一条**：把退场从 0.125s 拉到 0.7s 之后，
Horizon 提前解锁造成的横向跳（BI 的一部分）从「看不见」变成「一定看得见」。见第 3 点。

### 1. BH —— r77 记的「必须让对方调慢全站 `--animation-speed`」不成立

**改前实测**（`r79check.py --as-served`）：`animationDuration` = `0.125s`，
关闭后 `dialog[open]` 在 **145ms** 就消失 —— 0.7s 的面板滑出被切在 1/6 处。

r77 的结论是「时长只能是 `var(--animation-speed)`，要还原 0.7s 得让对方调慢全站参数」。
**重查后不成立。** Horizon 的相位动画写在 dialog 元素上：

```css
.theme-drawer__dialog--closing { animation: drawer-slide-out var(--animation-speed) ... forwards; }
```

`--animation-speed` 是**继承的自定义属性**（定义在 `theme-styles-variables.liquid` 的 `:root`），
但真正决定退场长度的是**这条规则的 `animation-duration`**。改后者只影响 dialog 自己，
改前者会把抽屉子树里所有 Horizon 组件（按钮 transition、loading 转圈）一起拖慢。

```scss
#cart-drawer .theme-drawer__dialog--opening,
#cart-drawer .theme-drawer__dialog--closing { animation-duration: $t-drawer; }
```

特异性 1-2-0 压过 Horizon 的 0-1-0，**不依赖 `{% stylesheet %}` 与 `customstyle.css` 的加载先后**。
同时把 overlay / panel 四条动画的 `var(--animation-speed, #{$t-drawer})` 换成直接的 `$t-drawer`。

⚠ **Horizon 那条 `drawer-slide-out` 动的是 dialog 的 `right`**，
拉长到 0.7s 后它会让 dialog 盒子变形 0.7s —— **视觉上没有任何影响**，
因为 `.gb-cart` 是 `position: fixed; inset: 0`，包含块是视口不是 dialog，
`.gb-cart__panel` 又 pin 在 `.gb-cart` 上。所以没有去替换它的动画名，
留着它正好继续给 `onAnimationEnd` 提供计时。

**改后实测**：`animationDuration` = `0.7s`，`dialog[open]` 在 **717～749ms** 才消失。

### 2. BI —— 桌面端不锁滚动，且锁必须键在 `dialog[open]` 上

Horizon 只在 <990 锁（`theme-drawer.js` 的 `#modalQuery.matches` 分支里 `lockScroll(panel)`），
≥990 走 `panel.show()`。**改前实测桌面 1440 档 `html` 的 `overflow` 是 `visible`。**

```scss
html:has(#cart-drawer .theme-drawer__dialog[open]),
html:has(#cart-drawer .theme-drawer__dialog[open]) body { overflow: hidden; }

html:has(#cart-drawer .theme-drawer__dialog[open]) { padding-right: var(--scrollbar-w, 0px); }
```

形状照静态站的 `is-modal-open`：**锁加在 html 与 body 两个元素上**（html 扛滚动，
但 reset 把 `overflow-x` 放在它上面），**补偿只加在 html 上**（padding 已经收窄 body，
两个都补会把居中布局往左拉半个滚动条，见 memory `scroll-lock-compensation-once-only`）。

### 3. ⚠ 为什么锚点必须是 `dialog[open]`，不是 `theme-drawer[open]` 也不是 `html[scroll-lock]`

`theme-drawer.js` 的 `close()`：

```js
this.removeAttribute('open');        // theme-drawer[open] 立刻没
unlockScroll(panel);                 // html[scroll-lock] 立刻没
if (panel.open) { ...
  panel.classList.add('--closing');
  await onAnimationEnd(panel, ...);  // ← 退场动画在这之后才跑
}
panel.close();                       // dialog[open] 到这里才没
```

**两个直觉锚点都在退场动画开始之前就掉了。** 键在它们上面，滚动条会在面板还在滑出时被还回来，
视口凭空变宽，而 `.gb-cart` 是包含块为视口的 fixed 盒 —— 右贴边的面板会在滑到一半时横向跳。
`.gb-cart` 自己的 `--modal-exit` 注释里记的就是这个坑，静态站早就踩过。

**实测证据**（`--as-served`，线上仍是 r78）：`lockGone = 10ms`，`openGone = 145ms` ——
Horizon 确实在动画开始前 135ms 就解了锁。0.125s 下看不出来，0.7s 下必然可见。
**改后：`lockGone == openGone == 717ms`，锁一直held到面板消失。**

### 4. `--scrollbar-w` 谁来测：新增 `scrollbarProbe` 模块

`modal.open()` 与 `header.set()` 都是自己锁之前当场测。**线上这个抽屉是 Horizon 打开的**，
而它的 `lockScroll()` 与 `showModal()` 在同一个同步块里 ——
我们挂任何 observer 都在页面**已经锁上之后**才触发，那时读到的是 0。

所以改成反过来：**在页面明确没锁的时候持续缓存**。

```js
measure: function () {
  var de = document.documentElement;
  if (de.hasAttribute("scroll-lock")) { return; }              // Horizon 的锁
  if (getComputedStyle(de).overflowY === "hidden") { return; } // 我们自己的锁
  de.style.setProperty("--scrollbar-w", (window.innerWidth - de.clientWidth) + "px");
}
```

`init` + `resize` 各测一次，两道守卫缺一不可（两种锁的实现方式不同）。
排在 `modules` 列表**第一位** —— 读这个值的锁可能在 init 之后的任何时刻落下。
静态站上它写的是 `modal.open()` 会写的同一个值，无冲突。

### 文件清单

```
assets/customstyle.scss   BH 4+1 条规则改时长；BI 新增 2 条锁规则；$build → r79
assets/customstyle.css    重新编译
assets/main.js            新增 scrollbarProbe 模块（+27 行），注册进 modules 与 window.gumi
*.html                    129 处 ?v= → 20260907-r79（12 个文件）
tools/r79check.py         新增，本轮判据（离线 39 + 线上 16，1 条明确跳过）
tools/r77check.py         改：四条动画断言不再绑定时长，只验「相位类驱动我们的关键帧」
tools/r78check.py         改：$build 断言 == → >=
tools/r73check.py         改：$build 断言 == → >=
```

### 验证

`python3 tools/r79check.py --password 1234` —— **全过，1 条明确跳过**。

**判据是双向的**（对线上真实状态 `--as-served` 跑应 8 红）：

| 断言 | 改后（本地 css/js） | 改前（线上 r78） |
|---|---|---|
| `animationDuration` | `0.7s` | `0.125s` |
| `openGone`（dialog[open] 消失） | 717ms | 145ms |
| `lockGone`（锁解除） | 717ms | **10ms** |
| 桌面 `html.overflow` | `hidden` | `visible` |

⚠ **两处判据毛病，都在本轮修掉**：

1. **测点落在变化区间之外**：`animationDuration` 原本在 open 后等 1000ms 才读，
   而动画 700ms 就结束、`--opening` 已被 `onAnimationEnd` 摘掉 ——
   读到的是「没有动画的元素」的 `0s`。改成 `requestAnimationFrame` 双帧内采样，
   并加一条 `sampled while --opening was on` 的锚点断言。
2. **自洽陷阱**：线上探针原本只顶替 `customstyle.css`，`main.js` 仍是线上的旧版、
   没有 `scrollbarProbe`，于是 `--scrollbar-w` 缺席 —— **期望值与实测值都是 `0px`，
   断言自洽地绿着，却什么都没补偿**。现在 `main.js` 一起顶替，
   并补 `scrollbarProbe is live (anchor)` 证明跑的是我们那份。

⚠ **`--scrollbar-w` 的真实补偿本机验不了** —— headless chromium 没有屏幕滚动条，
`innerWidth - clientWidth` 恒 0（铁律 14 / memory `headless-chromium-probe-limits`）。
判据把这条**明确 SKIP 并打印**，改用**合成 15px** 验 CSS 机制是否响应（`padding-right` → `15px`）。
**真实宽度下的补偿需要真机 / 真浏览器确认**，本机测不出。

### 顺带发现，未修

- **<990 档 Horizon 自己的锁也没有滚动条补偿**（`base.css` 的 `html[scroll-lock]` 只有
  `overflow: hidden`）。本轮的规则键在 `dialog[open]` 上，两档都命中，
  所以这个洞**顺带被补上了** —— 但那是我们的规则在兜，对方的实现没改。
- **`.gb-cart-item__error`**（`gb-cart-line-item.liquid:83`）我方零样式，
  出错时会以主题默认外观出现。纯 CSS 可补，不在本轮需求内。
- **`.gb-cart__gift` 与 `.gb-cart__pay-marks` 线上完全没有输出**（全主题 grep 零命中），
  样式都是现成的，缺的是宿主节点，**需要对方补 liquid**。见 LIVE-GAP。

### 推送（2026-09-07，已上线）

**3 个文件**：`assets/customstyle.css` / `assets/customstyle.scss` / **`assets/main.js`**。
⚠ `main.js` 这一轮真的改了，不像 r73/r77 那样可以不列。

三方对比（`live-20260907-prepush-r79/` 对 `baseline-r78/`）：**三个文件线上都 = 基线，零冲突**。
对方在这期间推了 7 项，**没有一项在我们的清单里**：新增
`sections/gb-promo.liquid` / `gb-vs.liquid` / `gb-app-section.liquid` / `snippets/gb-nl-modal.liquid`，
改动 `sections/gb-product.liquid` / `templates/index.json` / `templates/product.json`。
⚠ **这四个新 section 正是 LIVE-GAP 里登记的缺口**（PDP promo 卡 / PDP 对比表 / 营养标签弹窗
/ app 挂载点）—— 对方在补 liquid，**LIVE-GAP.md 需要重新核一遍**。
它们用的类（`gb-promo*` / `gb-vs*` / `gb-nl-*` / `gb-scallop*`）我们都有样式，
与本轮改动零交集（BH/BI 全部作用在 `#cart-drawer` 内）。

推送前 diff 核算：`customstyle.css` **删 19 行 / 增 33 行**，剔掉 30 行 build token 后
**删的 4 行全是被改写的旧动画行、增的 14 行全是本轮规则** —— 没有误删任何既有规则。
`main.js` 只删 2 行（modules 列表首行与 export 尾行，都是被改写的那两行）。

沿用 r73 的推送副本做法：从推送前快照复制 `push-r79/`，只放入 3 个文件，
与线上的差异恰好等于推送清单，命令写错也推不出清单外的东西。推完即删。

**回读**（`live-20260907-after-r79/`）：文件数 **607 → 607 零增删**、
3 个文件**逐字节相同**、**604 个清单外文件零改动**。
⚠ 日志照例打了 `Cleaning your remote theme` —— 带 `--nodelete` 它不删东西，回读才是证据。

**线上实测**：`tools/r79check.py --password 1234 --as-served` **全过、1 条明确跳过**。
`scrollbarProbe is live` 证明线上跑的是新推的 `main.js`；
`openGone = lockGone = 752ms`（推送前的同一判据是 145ms / 10ms）。

新基线 **`Gumi-Brand-shopify/baseline-r79/`（607 文件）**。

---

## 第七十八轮（2026-09-07）— reel focus 环被裁 + footer focus 描不出来 + header CTA 收回 40（`$build` = `20260907-r78`）

需求（对话）三条：① `gb-reel` 视频位 Tab 的 focus 样式被切了；
② footer 位置的 focus 边框不显眼，需换个同字体颜色；③ header `.gb-btn--primary` padding `0 40px`。

⚠ **本轮 cart 样式冻结**（需求方上一条指示），三处都在别的模块，且专门验过没波及购物车。

### 1. reel 的 focus 环：先是被裁，改完发现根本画不出来

**改前实测**：环是全局的 `outline: 2px solid $c-green` + `outline-offset: 2px`，
而 `.gb-reels.swiper{overflow:hidden}` 的裁切框是 `[0,180,1440,540]`，
**与卡片盒的上下边完全重合** —— 画在盒外那 2px 的上下两条正好落在框外，
只剩左右两条竖线，看着就是「样式被切了」。

**第一版改法（`outline-offset: -3px`）不成立。** 像素扫描显示卡内 3~5px 处仍是照片颜色：

> ⚠ **Chrome 把元素的 outline 画在它自己的盒之后、后代之前**，
> 所以内缩的环会被绝对定位的 `.gb-reel__media`（`inset:0`）盖掉。
> 加 `isolation: isolate` 不行，加 `position:relative; z-index:1` 也不行 ——
> **三个候选逐一实测，四条边全都扫不到绿色**。

**最终改法**：换成真元素。

```scss
&:focus-visible {
  outline: none;
  &::after {
    content: ""; position: absolute; inset: 3px; z-index: 2;
    border: 2px solid $c-green; border-radius: 18px;   // 21 less the 3 inset
    pointer-events: none;
  }
}
```

`inset: 3px` 让它离裁切框（＝卡片盒）有 1px 余量，`z-index: 2` 压过 `__media` 与播放图标。
判据是**四条边各扫 8 个像素找 `#005635`**，改后上/左/右/下全部命中。

### 2. footer 的 focus 环：深绿描在深绿上

**改前实测**：环 `rgb(0,86,53)`（`$c-green`），footer 底 `rgb(0,65,40)`（`$c-green-900`）——
两个深绿，等于没有环。全局 reset 的注释里其实早就写着这件事
（「dark green outline on the footer's dark green ground is invisible anyway」），
但当时只针对输入框做了边框方案，链接这些一直没管。

```scss
.gb-footer :focus-visible { outline-color: currentColor; }
.gb-footer__submit:focus-visible { outline-color: $c-lime-200; }
```

`currentColor` 就是需求说的「同字体颜色」，逐元素跟各自的文字走：
logo `#daf6b0`、链接 `#f4fce7`、社媒 `#b5ed61`，都是浅色，在深绿底上清楚。

⚠ **`.gb-footer__submit` 必须单列出来**：它是白底药丸、自己的字色是 `$c-green-900`，
而环画在按钮**外面**、落在深绿底上 —— 用 `currentColor` 会**又一次变成深绿描深绿**。
给它 footer 自己的文字色 `$c-lime-200`。**这条别当成多余的例外删掉。**

输入框 `.gb-footer__input` 不受影响：它在 reset 里就是 `outline: none` 走边框变色。
`.gb-footer-cta` 不在 `<footer>` 里（实测），本轮选择器碰不到它，也不需要 —— 它是浅色底。

### 3. header CTA padding 42 → 40

```scss
.gb-header__cta { padding: 0 40px; }
```

⚠ **这是把稿值改回去。** `.gb-btn--primary` 的 `0 40px → 0 42px` 是第四十五轮
「一批间距/尺寸」里按 Figma 改的（同一批还有 header toggle gap 16→18、hero padding 88→91 等）。
本轮需求方要 40，按指示执行，**记在这里以免下一轮对稿审计又把它改回 42**。

⚠ **作用域挂在 `.gb-header__cta`，不是基类**：`.gb-btn--primary` 全站 22 处，
其中一处是**购物车抽屉的 Shop Now**，而 cart 本轮冻结。
判据里有一条负向断言守着基类仍是 `0 42px`。

顺带查到：`.gb-cart__shop` **本来就自带 `padding: 0 40px`**（与线上快照逐字相同），
不走基类的 42。所以本轮实际效果是**把 header 那颗对齐到了购物车那颗**。

### 文件清单

```
assets/customstyle.scss     +23 / -1（.gb-reel focus 段、.gb-footer 两条、.gb-header__cta；$build → r78）
assets/customstyle.css      重新编译
*.html                      129 处 ?v= → 20260907-r78（12 个文件）
tools/r78check.py           新增，本轮判据（32 条，全过）
tools/r78probe.py           新增，focus 环 / 裁切祖先 / 按钮盒探针（真 Tab，非 el.focus()）
tools/r73shots/reel-focus-{before,after}.png
```

### 判据要点

- **focus 环只能用真键盘 Tab 取到** —— `el.focus()` 不触发 `:focus-visible`
  （memory `script-focus-does-not-trigger-focus-visible`）。
- **拍 reel 之前必须先摘掉 `.wowo`** —— 它停在 `opacity:0`、靠滚动才播，
  headless 驱动不了，不摘的话截图整张发白，肉眼会误判成「环没画出来」。
- **负向断言先验锚点**：`.gb-btn--primary` 与 `.gb-cart__shop` 两条都先断言元素/规则存在再比值。
  ⚠ 判据自己错过一次：预期 `.gb-cart__shop` 是继承来的 42，实际它自带 40 ——
  **报红的是判据不是实现**，核对线上快照后改正。

### 推送（2026-09-07）

推了 **2 个文件**到 live 主题 `Dev (#180348977399)`，`--only` 逐个 + `--nodelete` + `--allow-live`：

```
assets/customstyle.css
assets/customstyle.scss
```

本次一并带上第七十七轮（cart-drawer）的改动 —— 那一轮编译后按需求方指示压着没推。
`main.js` 与线上逐字节相同，不进清单。

**三方对比**（基线 `baseline-r76` / 本地 / 推送前快照 `live-20260907-prepush-r78`）：
两个 css 都是「我改的 → 推」，`main.js`「一致，不推」，无冲突。
线上相对基线另有 **12 个对方的变动**（10 个新 `blocks/*.liquid` 之外还有
`sections/gb-product.liquid` / `templates/product.json` 等），本次一律不碰。

**干净副本**：从推送前快照复制一份 `push-r78/`，只覆盖这 2 个文件，
`diff -rq` 对线上差异**恰好 2 个**，命令写错也推不出清单外的东西。推完即删。

**回读验证**（`theme pull` 到 `live-20260907-after-r78`）：

- 清单内 2 个文件与推送副本**逐字节相同**；**被删除的文件 0 个**。
- css 差异 126 行，其中 30 行 build token，**`<` 侧（线上有而本地没有的行）为空** ——
  没有覆盖掉线上任何既有规则。

⚠ **文件数 593 → 603，且清单外有 12 个文件变动 —— 是对方同期推的，不是我们误伤。**
证据：那 10 个 `blocks/*.liquid` 在**基线和我们推送前的快照里都不存在**，
而 `--only` 推送不可能创建文件；`sections/gb-product.liquid` 的变动是把内联
`section.blocks` 循环拆成独立 block 文件，与 CSS 无关。
**这个店一天能被对方推四五次，回读时先按「基线和推送前快照里有没有」判断归属，再下结论。**

**线上实测**（storefront 密码走 CLI 参数）：

- 12 条新选择器全部在页面已解析的样式表里
  （`.gb-reel:focus-visible` + `::after`、`.gb-footer :focus-visible`、
  `.gb-footer__submit:focus-visible`、6 条 `#cart-drawer .theme-drawer__dialog*`、`.gb-header__cta`）。
- 计算值：`.gb-header__cta` padding `0px 40px`、`.gb-footer__link` 环 `rgb(244,252,231)`、
  `@keyframes gb-cart-scrim` 存在。
- **端到端按真 Tab 走到 reel**：`outline: none`、`::after` 的 `inset:3px` /
  `2px rgb(0,86,53)` / `z-index:2`，四条边像素扫描**全部命中**。

⚠ **两个验证陷阱，都栽了一次**：

1. **非指纹的 `/cdn/shop/t/2/assets/customstyle.css` 回的是 `20260907-r73` 的旧缓存**。
   页面真正引用的是带 `?v=<digest>` 的指纹 URL。
   **别拿那个裸路径当判据** —— 它跟主题里的实际文件可以差好几轮。
2. **CSSOM 遍历一开始命中数全 0，是判据自己的 bug**：
   `if (r.cssRules) { walk(r.cssRules); continue; }` —— Chrome 的
   **`CSSStyleRule` 也带 `cssRules` 属性**（嵌套 CSS），于是每条样式规则都被当成容器跳过，
   一条都没数到。这条早就记在 memory `cssom-stylerule-has-cssrules` 里。
   ⚠ **当时另外三个直接读数（keyframes 在、padding 对、环色对）与它矛盾** ——
   矛盾时先查判据，别急着下「没生效」的结论。

新基线 `Gumi-Brand-shopify/baseline-r78/`（603 文件）。

### 顺带发现，**未修**

- **reel 的环画在海报图上，对比度随图而变**。现在是 `$c-green` 内缩环，
  测试那张（浅绿树叶 + 白兔）很清楚，但深色海报上会弱。
  稿里根本没有 focus 态设计，全站 focus 都是我们自定的。
  要保证对比度得加一圈浅色外描（如 `box-shadow: 0 0 0 1px rgba(255,255,255,.6)`），
  **那是新增视觉设计，没做**，登记为待决 BL。

## 第七十七轮（2026-09-07）— cart-drawer 还原静态站外观 + 抬到 header 之上（`$build` = `20260907-r77`）

需求（对话）：「点击 header 购物车按钮出现的 cart-drawer 弹窗的样式能否在**不改变结构和 js**
的情况下尽量还原静态站时的样式，并且需要**提高弹窗的层级**」。

**前提：对方已经把这个抽屉做好了**（第七十六轮推送当天新增的
`snippets/gb-cart-drawer.liquid` / `gb-cart-line-item.liquid` / `gb-cart-scripts.liquid`）。
他们把 Gumi 的整套类名原样搬进了 Horizon 的 `<theme-drawer>` → `<dialog>` →
`cart-drawer-component` → `cart-items-component` 里，所以 `.gb-cart*` 的样式本来就够得着。
本轮**一行 liquid、一行 js 都没动**，全部是 CSS。

### 1. 层级：Horizon 把抽屉排在 8，我们的 header 是 100

`.theme-drawer__dialog { z-index: calc(var(--layer-sticky) + var(--drawer-stack-order,0)) }`，
而 `--layer-sticky: 8`。`.gb-header` 是 `$z-header: 100` ——
**header 连同 "Shop now" 按钮整条画在打开的购物车上面**，遮掉了免运费提示条那一行。
改前实测：header 区域取色 `(231,248,208)` 原色未被压暗；改后 `(115,124,104)`，
与静态站同点**完全相同**。

`.gb-cart` 自己的 `z-index: $z-modal` 救不了 —— dialog 是 `position:fixed` + `z-index`，
它开了自己的层叠上下文，里面的 1000 出不去。所以要抬的是 **dialog**，不是 `.gb-cart`。

```scss
#cart-drawer .theme-drawer__dialog { z-index: calc(#{$z-modal} + var(--drawer-stack-order, 0)); }
```

用 id 选择器（1-1-0）压 Horizon 的 `.theme-drawer__dialog`（0-1-0），
不依赖 `{% stylesheet %}` 与 `customstyle.css` 的加载先后。`--drawer-stack-order` 保留，
两个抽屉同开时仍按各自顺序排。**只针对购物车抽屉**，chat-drawer 不动。

### 2. dialog 本身是个 480 的白侧栏，得把它的盒子拆掉

`.theme-drawer__dialog` 不是个透明容器 —— 它就是 Horizon 的抽屉面板：
`width: var(--sidebar-width)`（实测 480）、右贴边、`background-color: var(--color-background)`、
`border-left`、safe-area padding。我们的 `.gb-cart` 是 `position:fixed; inset:0`，
画在它上面，两者**只在面板左侧那 89px 上不一致** —— 那里 dialog 的白底透过 50% 黑遮罩
显成一条浅灰竖带（改前截图 x=960..1049，取色 `(127,127,127)`，改后 `(33,46,42)`，
静态站同点 `(30,43,41)`）。

```scss
inset: 0; width: auto; max-width: none; height: auto;
padding: 0; border: 0; background: transparent; color: inherit;
```

`color: inherit` 是第三处：dialog 断言 `--color-foreground`（纯黑），
而面板里的文字本该从 body 继承 `$c-ink`。改前 `.gb-cart__totals` 是 `rgb(0,0,0)`，
改后 `rgb(1,19,7)`，与静态站一致。

### 3. 数量输入框：`<input>` 的固有宽度把 stepper 撑成 272

静态站与设计稿都是 `<span class="gb-cart-item__count">`，线上换成了
`<input type="number">`（Horizon 的 `/cart/change.js` 要它）。
`<input>` 的固有宽度约 20 个字符，于是 **stepper 从 102×40 变成 272×46**，价格被挤出面板。

```scss
.gb-cart-item__stepper input.gb-cart-item__count { width:30px; height:20px; padding:0; border:0; … }
```

⚠ 选择器**必须挂在 stepper 下**：base.css 的
`input:not([type='checkbox'], [type='radio'])` 是 0-1-1，
裸写 `input.gb-cart-item__count` 也是 0-1-1 —— **平手时靠加载顺序定胜负**，赌不得。
挂上 `.gb-cart-item__stepper` 后是 0-2-1，稳赢。
另外补了 `::-webkit-inner/outer-spin-button { appearance: none }` 去掉上下箭头。

改后实测 stepper `102×40`、count `30×20`，与静态站**逐像素相同**。

### 4. 配送周期下拉：沿用第七十六轮的判决，只画闭合态

线上的 `.gb-cart-item__interval` 是裸 `<select>`（没有 `data-select`，`selectBox` 不接管），
所以带着浏览器默认的边框和箭头。**没有去让 main.js 认领它** —— 第七十六轮需求方
已经就订阅下拉做过一次判决（「不用改点击出来的 drop box 样式」），同一个理由适用，
何况本轮明写「不改变结构和 js」。

改法与 `.gb-sub__select` 同一套：`select.gb-cart-item__interval:not(.gb-select__native)`，
`appearance:none` + 去边框 + 蓝色 vee 背景图，`:not(.gb-select__native)` 保证静态站零匹配。

⚠ 两处已知代价，**别报成 bug**：
① 箭头是背景图，跟不了 `currentColor`，hover 用整图替换 —— **颜色能过渡，箭头是瞬切**；
② 原生 `<select>` 的宽度取**最长选项**而非选中项，所以它比静态站的 `.gb-select--inline`
（只有选中项那么宽）宽一些。实测 151 vs 77，差值全部来自 "One Time Purchase" 这一串。

### 5. 空购物车：查的时候是坏的，做完复查时对方已自己修好

**发现时**：线上画空抽屉不加 `is-empty`，而是干脆不输出 `__ship`/`__body`/`__bar`。
我们的状态开关 `.gb-cart:not(.is-empty) .gb-cart__empty{display:none}` 于是恒真，
**空态文案被藏死，空购物车打开是一块纯白面板**。当时加了一条按「填充态标志物缺席」判定的救援规则。

**复查时（同日 05:02 的线上快照）对方已经补上 `is-empty`**，并把空态抽成
`snippets/gb-cart-empty.liquid`：多了两张 `.gb-nav-card`（Shop Gumi 熊图卡 + Refer a Friend 卡）
和 4 个后台 setting（`gb_empty_cart_card1_*` / `card2_*`）。我们静态站早就有
`.gb-cart__cards` 那套样式，**一行没改就对上了**。

**所以那条救援规则已删。** 实测依据：在线上把它的 `display` 摘掉，
`.gb-cart__empty` 仍是 `flex`。

⚠ **没有把它留作"保险"是有理由的** —— 它键在代理信号（没有 `__body`）上，
万一将来有货的抽屉也不输出 `__body`，它会在**有货时显示空态文案**。
守卫改放进判据：`live empty drawer carries is-empty`，
对方哪天再把这个类丢了，判据当场报红并点名，而不是靠一条可能误伤的 CSS 兜着。

线上空态实测与静态站**逐像素相同**：empty-head `1069,80,351,92`、Shop Now `1069,128,351,44`、
cards `1069,216,351,169`、单卡 `170×169`、熊图 `1106,250,229,276`、tag `1267,232,93,22`。

⚠ **唯一的差异：线上空态没有底部那条置灰的 Secure Checkout 栏**（`__bar` 整个不输出），
静态站有。这是内容取舍不是还原，**没动**，见「顺带发现」。

### 6. 铺满视口带来的两个连带项

**① `::backdrop` 要压掉。** <990 时 Horizon 走 `showModal()`，dialog 进 top layer，
浏览器会画它自己的 `::backdrop`（`rgb(--backdrop-color-rgb / 0.15)`）。
它在我们的 `.gb-cart__overlay`（0.5 黑）**下面**，两层叠起来约 0.575，比稿子深。
`#cart-drawer .theme-drawer__dialog::backdrop { background: transparent; }`，
遮罩只留 `.gb-cart__overlay` 一层。

**② Horizon 的「点背景关闭」失效了，但关闭路径没断。**
`#onBackdropClick` 的判据是 `isClickedOutside(event, panel)` —— 按 dialog 的矩形算「外部」。
dialog 一铺满视口就**没有外部了**，这个 handler 变成空转。

好在**对方已经在 `.gb-cart__overlay` 上写了 `on:click="#cart-drawer/close"`**，
真正生效的一直是那条。判据里加了两条实点：桌面 (120,500)、手机 (30,700) 各点一次遮罩，
断言 `dialog.open` 与 `theme-drawer[open]` 都回到 false。
**别把 `#onBackdropClick` 空转当成 bug 去"修"。**

### 7. 入场 / 退场：面板是服务端就带 `is-open` 的，原本直接弹出来

`.gb-cart__panel` 的 `transform: translateX(100%)` → `.is-open` 的 `none` 需要一次状态变化才跑，
而线上的 `is-open` 是 liquid 直接写死的，dialog 一 `[open]` 就已是终态 —— **没有滑入、没有淡入**，
违反「状态变化必有过渡」。借 Horizon 打在 dialog 上的两个相位类驱动我们自己的关键帧：

```scss
#cart-drawer .theme-drawer__dialog--opening .gb-cart__panel { animation: gb-cart-slide …; }
#cart-drawer .theme-drawer__dialog--closing .gb-cart__panel { animation: … reverse forwards; }
```

⚠ **时长只能是 `var(--animation-speed)`（0.125s），不是我们的 `$t-drawer`（0.7s）**：
dialog 什么时候 `display:none` 是 Horizon 用**它自己那条动画**的 `animationend` 决定的
（`onAnimationEnd(panel, …, {subtree:false})`，只看 panel 自身的动画，不看子元素），
写 0.7s 的话退场会在 0.125s 处被硬切。要还原稿子的 0.7s 得让对方调慢主题的
`--animation-speed`，那是全站参数 —— **列入待裁决，没动**。

### 复查：对方在本轮期间又改了 7 个文件

需求方要求「查看 cart 的结构和样式有没有改动」。重新 `theme pull`
（`live-20260907-r77check/`，593 文件）对 `baseline-r76/`（590）比：

| 变化 | 文件 |
|---|---|
| 新增 3 | `snippets/gb-cart-empty.liquid`、`assets/nav-card-bear.png` / `.webp` |
| 改动 7 | `snippets/gb-cart-drawer.liquid` / `gb-cart-line-item.liquid` / `gb-cart-scripts.liquid` / `gb-head.liquid`、`sections/gb-product.liquid`、`config/settings_data.json` / `settings_schema.json` |

**`assets/customstyle.css` / `.scss` 零差异** —— 线上仍是 r76，本轮推送清单不冲突。

购物车这边具体改了什么：

- `gb-cart-drawer.liquid`：空态加 `is-empty`（见上第 5 点）、根节点加
  `data-hydration-key="gb-cart-root"`、空态内容抽成 `gb-cart-empty` snippet。
- `gb-cart-line-item.liquid`：删除按钮从 Horizon 的 `on:click="/onLineItemRemove/N"`
  换成 `data-gb-remove` + 自写 handler（等服务端确认再移除行）。**类名没动，样式不受影响。**
- `gb-cart-scripts.liquid`：**新增一个内联 `<style>`** —— 行级 loading 遮罩
  （`.gb-cart-item{position:relative}` + `.gb-cart-item__loading` + `@keyframes gb-cart-spin`），
  另加「改配送周期时合并同变体同周期的重复行」逻辑。
- `sections/gb-product.liquid`：`{% form 'product' %}` 换成裸 `<form class="gb-product__form">`，
  加购按钮加 `is-loading` 并自带内联 `<style>`（`color: transparent !important` + 转圈）。
- `snippets/gb-head.liquid`：加了一段剥掉 URL 里 `?variant=` 的脚本（Appstle 应用会写）。
  **`<link rel="stylesheet" href="customstyle.css">` 的位置没动**，我们的加载次序不变。

**对 r77 的影响：一条都没打破。** 在新结构上重跑判据 **55 过 / 0 红 / 7 明确跳过**。
逐条核过的三处潜在冲突：

1. `@keyframes gb-cart-spin`（对方）vs `gb-cart-scrim` / `gb-cart-slide`（我们）—— **不同名**。
2. `.gb-cart-item{position:relative}`（对方，内联 `<style>` 在 `<body>` 里、比我们的
   `<head>` 样式表晚）—— 同权重时它赢，但**我们没设 `position`**，无冲突。
3. 裸 `<form>` 仍带 `class="gb-product__form"`，加购按钮仍是直接子 ——
   第七十三轮那条 `.gb-product__form > .gb-product__cta { margin-top:20px }` **照常命中**。

⚠ **对方开始往 liquid 里内联 `<style>` 了**（`gb-cart-scripts` 与 `gb-product` 各一处）。
这两块不归我们管、目前也不冲突，但**样式源从此不止 `customstyle.scss` 一处** ——
以后查「这条规则从哪来」要连 `snippets/*.liquid` 一起 grep。

### 文件清单

```
assets/customstyle.scss     +106 （.gb-cart 模块尾部新增 live-only 段；$build → r77）
assets/customstyle.css      重新编译
*.html                      129 处 ?v= → 20260907-r77（12 个文件）
tools/r77check.py           新增，本轮判据（55 过 / 0 红 / 7 明确跳过）
tools/r77probe.py           新增，线上抽屉几何/层叠探针
tools/r77static.py          新增，静态站抽屉基准截图
tools/r73shots/cart-*.png   改前 / 改后 / 静态站基准 / 空态线上与静态各一张
```

### 线上验证：53 过 / 0 红 / **7 条明确跳过**

`python3 tools/r77check.py --password 1234` —— 离线 33 条（产物 22 + 静态站 11）
+ 线上 20 条，全过；**7 条跳过并逐条打印在结果里**，不是静默略过。

线上半段的三个写法值得沿用：

1. **顶替而不是追加 `customstyle.css`**（`page.route` fulfill）。`add_style_tag` 追加的规则
   在同权重时凭顺序必胜，会把判据打得比浏览器实际更宽松。
2. **一个 context、一个页面、三档视口**（1440 → 390 → 900，靠 `set_viewport_size`）。
   顺带真跑了一遍 Horizon 的 `#onModalBreakpointChange`。
3. **跳过要响**：`skip()` 单独计数并在结尾列名，`sys.exit` 只看 FAIL。

⚠ **这家店在 Cloudflare 托管挑战后面，触发器是 `/cart/*` 这个路径本身**：

| 请求 | 结果 |
|---|---|
| `/`（首页） | 200，`#cart-drawer` 在 |
| `/cart/<variant>:<qty>` | **429 + `?__cf_chl_rt_tk=…`，标题 `Verifying your connection...`** |
| 之后的任何 `/` | 同样被挂住，标题 `Just a moment...` |
| 反复打 `/products.json`、`/cart/add.js`、甚至 `/password` | 也会累积到 429 / 503 |

**一旦踩中，整个浏览会话（含首页）都废掉**，退避半小时也不一定解。
所以判据默认**完全不碰 `/cart/*`**：新开 context 本来就是空车，
空车态足够验完 dialog 几何、层级、遮罩压住 header、`::backdrop`、遮罩点击关闭、
空态文案、手机档模态性与满宽。**只有行项目的尺寸需要有货**，
那 7 条走 `--fill` 开关（会踩挑战，实测确实踩），默认跳过。

**那 7 条的证据来自本轮更早的线上实测**（Cloudflare 还没被激怒时，真加了 2 件货跑的）：
stepper `102×40`、count `30×20`、interval `rgb(3,116,165)` / `appearance:none` / 边框 0，
截图 `tools/r73shots/cart-live-desktop-{before,after}.png`。
后来补的 `::backdrop` 一条不影响它们（桌面非模态根本没有 backdrop）。

⚠ **判据自己也错过一条**：390 档原本断言「点遮罩能关」，红了 ——
**那个宽度下面板是满宽的（`@include narrow { width: 100% }`），根本没有露出来的遮罩**，
我点的坐标落在面板上。改成点关闭按钮，遮罩点击移到 900 档（仍是模态、但遮罩露着）去验。
**报红的是判据不是实现**，这类"测点落在错误区域"的假红见铁律 6。

### 顺带发现，**未修**

- **线上空态没有底部那条置灰的 Secure Checkout 栏**，静态站有（`.gb-cart.is-empty`
  把它做成禁用态）。线上是整个 `__bar` 不输出，CSS 补不出来，也是**内容取舍不是还原**。
- **加购按钮的 `is-loading` 由对方内联 `<style>` 提供**，不在我们的 scss 里。
- **购物车行的图是灰占位块** —— 线上 `item.image` 为空（liquid 里 `{%- if item.image != blank -%}`
  才输出 `<img>`）。这是商品数据没图，不是样式。静态站同样是灰块（稿里就是占位）。
- **桌面端打开抽屉后，背后的页面仍可滚动**。Horizon 在 ≥990 走 `dialog.show()`（非模态，
  不锁滚动），<990 才 `showModal()`。静态站两档都锁。CSS 能做
  `html:has(#cart-drawer[open]){overflow:hidden}`，但**锁滚动必须同时补偿滚动条宽度**，
  而宽度只能 JS 实测 —— 本轮说好不改 js，所以没做。
- **`--animation-speed` 0.125s vs 稿的 0.7s**（见上第 7 点）。

### 待推送

尚未推 live。推送清单预计 2 个文件：`assets/customstyle.css` / `assets/customstyle.scss`。
`main.js` 本轮未改。

## 第七十六轮（2026-09-07）— 订阅下拉退回原生（只改闭合态）+ faq/footer 交界波浪的配色（`$build` = `20260907-r76`）

需求（对话）两条，**都推翻了前面轮次的做法**：
① 「只需改 `gb-sub__select` 的表单样式就行，不用改点击出来的 drop box 样式，因为这样改可能会有一些问题」；
② 「修复 gb-faq 缺少波浪的形状的效果」→ 追加澄清：**「是和 footer 交界处缺少波浪形状」**。

### 1. 撤回 selectBox 接管，改纯 CSS 只管闭合态

第七十四轮让 `main.js` 认领线上的订阅下拉（`selectBox` 接管成按钮 + ul），**第七十五轮已推上线**。
需求方本轮明确要求退回原生控件 —— 顾虑是接管会改 DOM 结构与交互，
而它正好和对方新装的 cart-drawer、价格逻辑挤在同一块。

- `main.js` 的 adopt 循环整段删除，**回退后与 `baseline-r73/assets/main.js` 逐字节相同**（干净回退）。
- 新增 `.gb-sub__select:not(.gb-select__native)`：40 高 / 8 圆角 / `$c-gray-350` 边框 /
  `0 1px 2px $c-ink-05` / 14px·400·-0.28 / `$c-gray-700`，箭头复用
  **`.gb-field__input--select` 里现成的那个 data URI**（同一个 vee `M5 7.5L10 12.5L15 7.5`，
  同样 `right 14px center`）—— 不是新画的。
- `:not(.gb-select__native)` 让它在静态站零匹配（那边 `selectBox` 已接管并隐藏原生控件），
  同时**顺带成了静态站的降级外观**：脚本万一死了，露出来的原生控件也是这个样子。

⚠ **代价（需求方已知并接受）**：箭头不能旋转（`background-image` 不可 `transform`），
下拉列表是浏览器/OS 画的、样式够不到。这正是 `selectBox` 当初存在的理由，现在按要求让回去。

线上实测（把 r75 main.js 已做的接管在探针里还原，等价于推 r76 之后的状态）：
`40/8px/14px/arrow`、`wrapped: False`、原生 select 仍带 `data-gb-plan-select`、
`change` 事件照常触发。

### 2. faq 与 footer 交界处的波浪：变体用错，上半条透明了

⚠ **第一版修错了位置** —— 需求「修复 gb-faq 缺少波浪的形状」被理解成上边缘，
做了一套「从 faq 这一侧补画顶部波浪」的方案。需求方澄清是**下边缘（与 footer 交界处）**，
那套补画已整段撤回，`.gb-scallop` / `--edge-top` 的选择器也还原成单选择器。

**真正的根因**：线上把这条波浪的配色对填成了 `to-lime`，静态站用的是 `mint-to-lime`。

| | `--wave-bg`（上方色） | `--wave-under` | `--wave-fg` |
|---|---|---|---|
| 静态站 `--mint-to-lime` | `#e7f8d0` mint | `#b5ed61`（默认取 fg） | `#b5ed61` |
| 线上 `--to-lime` | **transparent** | **transparent** | `#b5ed61` |

上半条透明 → `.gb-faq` 的 mint 到波浪处**断成白色**，弧形与上方失去分界，
看上去就是「波浪形状没了」。修前截图里弧形之间的间隙是白的，修后是 mint。

`to-lime` 本身没错 —— **faq 页**的这条波浪上方是白色的 `.gb-cta-band`，透明顶正合适。
错只错在 `.gb-faq` 直接接 footer 的那三页。

**改法**（纯 CSS，不碰对方的 setting）：

```scss
#MainContent:has(> .shopify-section:last-child > .gb-faq) + footer .gb-scallop--to-lime {
  --wave-bg: #{$c-lime-150};
  --wave-under: var(--wave-fg);
}
```

⚠ **`.gb-faq` 和这条波浪不是兄弟** —— 一个在 `#MainContent`，一个在 `<footer>`；
但那两个容器是兄弟，而且「faq 是 main 的最后一个 section」正好等价于「faq 直接接 footer」。
实测：pdp / how-gumi-works / reviews 该条为 true，faq 页为 false。
只用一层 `:has()`，内部是普通选择器 —— **`:has()` 不能嵌套**（第一版的 `@extend` 正是
把选择器塞进了 `:has()` 里面，判据里现在有一条 `no nested :has()` 常驻盯着）。
静态站没有 `#MainContent`，规则零匹配。

⚠ **`--wave-under` 必须一起改**：`to-lime` 把它显式设成了 transparent，
只改 `--wave-bg` 会在分数缩放下露出发丝缝（见 `.gb-scallop` 那段注释）。实测修后为 `#b5ed61`。

### 顺带发现（未修，等需求方拍板）

同一个根因**还影响另外两页**，需求方只点名了 faq，本轮按公约没动：

| 页面 | footer 波浪上方 | 该块背景 | 现状 |
|---|---|---|---|
| **index** | `.gb-reviews` | mint `#e7f8d0` | `--wave-bg: transparent` ← 同样断色 |
| **science** | `.gb-faq-image` | mint `#e7f8d0` | 同上 |
| our-story | `.gb-reviews` | cream `#faf9f8` | transparent 露出白色，大致对 |

要一并修的话，把上面那个选择器扩成三条（或请对方把这几页的 section setting
从 `to-lime` 改成 `mint-to-lime`，那是更正的路子）。

### 验证

`tools/r73check.py --password 1234` —— **52 ok / 0 FAIL**，本轮新增：

- `main.js no longer adopts the live select` / `native select restyled for the live theme`
- `faq stand-in wave spliced into .gb-scallop (not @extend)` /
  `faq wave withdrawal rule has no nested :has`（**专门盯上面那个坑**）
- 波浪四页 × 两条：`stand-in drawn/withdrawn` + **`exactly one wave at the edge`**
  —— 后者同时防住「零条」和「两条」，是这条修复的核心不变量
- 静态站四页 `rule inert, real wave intact`

另跑：11 页回归全清（波浪数量与改前一致，静态站 select 仍是 40 高的 selectBox 按钮）、
编译幂等（两次 md5 `f0737ed7…`）。
截图 `tools/r73shots/`：`faq-edge-static.png` vs `faq-edge-after.png` 形状一致、
`select-native-r76.png`。

### 文件清单

```
改  assets/main.js            删除 adopt 循环（回退到 baseline-r73 的状态）
改  assets/customstyle.scss   .gb-sub__select 原生控件样式；faq→footer 波浪的 --wave-bg/-under
                              覆盖（live-only，一层 :has）；$build → 20260907-r76
改  assets/customstyle.css    编译产物（双写）
改  *.html（12 个）            129 处 ?v= 升到 r76
改  tools/r73check.py         +15 条；$build 判据改为按声明锚定（插变量时被行号偏移坑过一次）；
                              新增常驻判据 no nested :has()
新增 tools/r73shots/footerwave-{before,after,static}.png、select-native-r76.png
                              （faq-edge-*.png 是第一版改错位置时的，留作对照）
改  docs/CHANGELOG.md、docs/HANDOFF.md
```

### 推送（2026-09-07）

推了 **3 个文件**：`assets/customstyle.css` / `.scss` / `main.js`
（`--only` 逐个 + `--nodelete` + `--allow-live`，副本 `push-r76/` 与线上差异恰好 3 个、liquid 混入 0）。

三方对比：我们的三个文件线上未被动过。**对方同期在改** `gb-product.liquid`
（加购从 FormData 换成 JSON payload）与三个 `gb-cart-*.liquid`（在做购物车抽屉）——
都不触及 select 的 DOM 或样式，`gb-sub.liquid` 的 select 仍是纯 `data-gb-plan-select`。

回读：**590 → 590**、三个文件逐字节相同、未推的 587 个文件零改动、
线上 `main.js` 里 `data-gb-plan-select` 残留 **0 处**（回退确实生效）。

**线上真实状态 `--as-served` 54 条全过**：select 是原生控件且外观为 `40/8px/14px/arrow`、
footer 波浪三页 `--wave-bg: #e7f8d0`、faq 页仍 `transparent`、角标与 gallery 保持 r75 的结果。

CDN 指纹 URL 回读交叉验证：`#MainContent:has(>.shopify-section:last-child>.gb-faq)+footer
.gb-scallop--to-lime{--wave-bg: #e7f8d0;--wave-under: var(--wave-fg)}` 完整上线。
⚠ **判据两次栽在压缩形式上** —— 线上 css 是 minified（`:has(` 里的空格被去掉），
但**自定义属性的值保留空格**（`--wave-bg: #e7f8d0`）。现在改用
**「线上命中数 == 本地源命中数」**做判据，不再写死期望值。

新基线 `Gumi-Brand-shopify/baseline-r76/`（590 文件）。
截图 `tools/r73shots/footerwave-live-r76.png` / `select-live-r76.png`。

### 遗留
- `liquid/snippets/gb-sub.liquid`（r73 那份加 `data-select` 的）**更不该推了**，
  它会让线上重新变成接管状态。已在 `liquid/README.md` 标注。
- **index / science 的同类断色未修**（见上「顺带发现」），等需求方拍板。
- ⚠ **faq 的上边缘波浪确实也缺**（pdp / how-gumi-works，因为上方的 `gb-app-section` /
  `gb-product` 线上没有），那是第七十四轮查到的另一回事，本轮的补画方案已撤回。
  逐条仍在 [LIVE-GAP.md](LIVE-GAP.md) 三之二。

---

## 第七十五轮（2026-09-07）— 购物车角标归位 + gallery 顶距二次反转（`$build` = `20260907-r75`）

需求（对话）两条：① `gb-header__icon` 的 cart-bubble 要定位到右上角、`background: #005635`、
略缩小；② `.gb-product__media` 的 top 改为 **100px**。

### 1. cart-bubble：Horizon 的定位规则一条都没匹配上

⚠ **对方在第七十四轮之后又改了线上**（`gb-header.liquid` + `gb-product.liquid`）：
购物车图标从 `<a href="{{ routes.cart_url }}">` 换成了原生抽屉的触发器 ——
`<cart-icon class="gb-header__icon-wrap …">` 包 `<button on:click="#cart-drawer/toggle">`，
里面 `{% render 'cart-bubble', limit: 100 %}`。这与第七十三轮记的
「图标指向 /cart，原生抽屉打不开」已经不同了，LIVE-GAP 第四节需要更新。

**根因**：Horizon 给角标的定位规则**全部挂在基类 `.header-actions__cart-icon` 上**
（`snippets/header-actions.liquid` 的 stylesheet 块）：

```css
.header-actions__cart-icon { --cart-bubble-size:20px; --cart-bubble-top:4.5px;
                             --cart-bubble-right:2.5px; position: relative; }
.header-actions__cart-icon .cart-bubble { position:absolute; width:var(--cart-bubble-size);
                                          top:var(--cart-bubble-top); right:var(--cart-bubble-right); }
```

而对方的 liquid 只写了 `header-actions__cart-icon--has-cart`（**修饰类**，还只在非空车时加），
**基类从未出现**。于是角标既没有定位祖先、也没有偏移量，`.cart-bubble` 退回 snippet 自带的
`position: relative` —— **参与流布局**，掉到图标正下方。
线上实测（模拟 3 件商品）：角标在图标下方 24px、背景 `rgb(0,0,0)`（Horizon 的
`settings.page_text_color` fallback），**图标盒被撑成 24×44**。

**改法**（纯 CSS，在我们的 `customstyle.scss` 里，不碰对方 liquid）：

```scss
.gb-header__icon-wrap {
  --cart-bubble-size: 16px;   --cart-bubble-top: -3px;  --cart-bubble-right: -3px;
  --cart-bubble-background: #{$c-green};   --cart-bubble-text: #{$c-white};
  position: relative;  display: inline-flex;
}
.gb-header__icon-wrap .cart-bubble {
  position: absolute; top: var(--cart-bubble-top); right: var(--cart-bubble-right);
  left: auto; bottom: auto; width: var(--cart-bubble-size); font-size: 10px; font-weight: 500;
}
```

取色走 Horizon 自己的 `--cart-bubble-background` 变量，不去改 `.cart-bubble__background`
的 `background-color` —— 变量是它 doc 注释里明写的对外接口。

| 指标 | 修前 | 修后 |
|---|---|---|
| 角标相对图标右上角 | 下方 24px | **右上 (+3, −3)** |
| 尺寸 | 20×20 | **16×16** |
| 背景 | `rgb(0,0,0)` | **`rgb(0,86,53)` = #005635** |
| 图标盒 | 24×**44**（被撑高） | 24×**24** |

⚠ **Horizon 的 donut mask 没有被修好，也修不了** —— 那条规则
（`.header-actions__cart-icon.header-actions__cart-icon--has-cart svg`，在角标处挖个透明环）
要求**基类和修饰类同时存在**，基类既然没加就不匹配。实测 `mask-image: none`，修前修后都一样。
角标直接盖在图标上，没有那圈透明间隙。要那个效果得让对方在 liquid 里补上基类。

### 2. gallery 顶距：104 → 80 → **100**，第二次反转

板上是 `header + 24`（24 量到视口顶）= 104。第七十三轮客户要求贴合改 80，本轮改 **100**。
pc 档 `calc($h-header + 20px)`；**tablet 档写成 `calc(fluid($h-header-mobile, $h-header) + 20px)`**
而不是写死 100 —— 该档 header 高度是斜坡，写死会让 768 端的净距变成 36。

⚠ **这个值已经改过两次，别按板或按上一轮改回去**，三次分别是 r53 起的 104 / r73 的 80 / r75 的 100。

### 验证

`tools/r73check.py`（已扩到覆盖 r73–r75）：

- 注入模式 **37 ok / 0 FAIL** —— 含角标四条（位置 (3,−3)、16×16、`rgb(0,86,53)`、图标盒 24）
- `--as-served` **34 ok / 0 FAIL** —— 线上仍是 r73，角标与 select 都是未修状态，**这是预期**
- 11 页静态站回归全清：header 全部粘 0、无水平溢出、`media.top` 都是 100px、
  **`.cart-bubble` / `.gb-header__icon-wrap` 本地零匹配**（live-only 规则不影响静态站）
- 编译幂等（两次 md5 `6966c831…`）

截图 `tools/r73shots/bubble-before.png` / `bubble-after.png`。

### 文件清单

```
改  assets/customstyle.scss   cart-bubble 定位/配色/尺寸（live-only）；gallery top → header+20；
                              $build → 20260907-r75
改  assets/customstyle.css    编译产物（双写）
改  *.html（12 个）            129 处 ?v= 升到 r75
改  tools/r73check.py         +6 条（角标四条、gallery 100、静态站零匹配）；修 check() 对元组的格式化
新增 tools/r73shots/bubble-*.png
改  docs/CHANGELOG.md、docs/HANDOFF.md、docs/LIVE-GAP.md
```

### 遗留 / 待推

- **r74 + r75 一起待推**：`assets/customstyle.css` / `.scss` / `main.js` 三个文件。
- **角标的透明环（donut mask）没做** —— 需要对方在 `gb-header.liquid` 给 `<cart-icon>`
  补上基类 `header-actions__cart-icon`。已进后台/对方待办。
- 空车时角标是 `visually-hidden`，本轮所有角标判据都靠**模拟非空车**（加 `--has-cart`、
  去 `visually-hidden`、填数字）才测得到 —— 直接打开页面看不到角标不是 bug。

---

## 第七十四轮（2026-09-07）— faq 波浪消失查因（非本轮引起）+ 订阅下拉改用 main.js 认领（`$build` = `20260907-r74`）

需求（对话）两条：① 查 live 的 `gb-faq` 波浪为什么没了；
② `gb-sub__select` 能否**不改结构只改样式**调回原样。

### 1. faq 上边缘的波浪：section 缺失带走的，不是波浪本身出问题

**先排除本轮嫌疑**：用推送前的 r72 CSS 注入线上同一页再测，波浪同样缺失 → **与 r73 推送无关**。

根因是波浪的归属方式：**波浪是上方 section 的最后一个子元素**（不是独立兄弟，见
PROJECT-STATUS「波浪」一节）。上方那个 section 在线上不存在，波浪就跟着一起没了。

| 页面 | 静态站 faq 上方 | 线上 faq 上方 | 判定 |
|---|---|---|---|
| **pdp** | `.gb-app-section`（含 `--edge --cream-to-mint`） | `.gb-reviews` | `gb-app-section` 线上**没有 liquid** |
| **how-gumi-works** | `.gb-product`（含 `--edge --white-to-mint`） | `.gb-reviews` | `gb-product` **没挂进该页模板** |
| reviews | `.gb-ingredients` | `.gb-ingredients` ✓ | 在（高度 129 vs 97，`--lg` 变体差异） |
| faq | `.gb-page-hero` | `.gb-page-hero` ✓ | 三个波浪全一致 |

两条缺口本身早有记录（[LIVE-GAP.md](LIVE-GAP.md) 第一节的 `gb-app-section`、
[LIVE-BACKLOG.md](LIVE-BACKLOG.md) 一·2 的「4 个模板没挂 gb-product」），
**但此前只当成"少一个区块"，没意识到它同时带走了下一区块的上边缘波浪** ——
视觉症状是 faq 上沿变成一条直边。已把这层因果补进两份文档。

⚠ **修法不是给 `.gb-faq` 补一个波浪** —— 那会在区块补回来时变成两个。
正解是补回上方的 section（how-gumi-works 在后台加 `gb-product` 即可；
pdp 要新写 `gb-app-section` 的 liquid）。

判据：`tools/r73shots/` 下线上/静态站的逐个波浪截图；比对脚本见本轮对话，
核心是按**几何相邻**（波浪底边 ≈ faq 顶边，容差 6px）判断归属，
不能按 DOM 兄弟找 —— 线上隔着 Shopify 的 section 包裹层。

### 2. 订阅下拉：纯 CSS 做不到，改用 main.js 认领（仍然不碰对方的 liquid）

**纯 CSS 的天花板**（这是 `selectBox` 当初存在的原因，注释里就写着）：
原生 `<select>` 的**下拉列表是浏览器/OS 画的**，CSS 够不到（选项字体、圆角、hover、动画全改不了）；
箭头若用 `background-image` 画则**不能 `transform` 旋转**。
能做的只有闭合态那个盒子。线上现状实测：361×26、浏览器默认 `1px solid rgb(118,118,118)`、圆角 4。

**改用 `main.js` 认领**——第七十三轮原本要改 `snippets/gb-sub.liquid` 加 `data-select`，
现在改成 `selectBox.init()` 自己去认，一条循环：

```js
var adopt = document.querySelectorAll("select[data-gb-plan-select]:not([data-select])");
for (var j = 0; j < adopt.length; j++) { adopt[j].setAttribute("data-select", ""); }
```

- **hook 用对方的 `data-gb-plan-select`，不是 `.gb-sub__select` 类** —— 类名是我们的、随时可能改名，
  那个 data 属性是他们价格逻辑的命脉，比类稳。符合铁律 17。
- **静态站零变化**：`:not([data-select])` 在本地不匹配（markup 里已经有），实测
  `hasVendorHook: False`、按钮仍 40 高、`selectBox.boxes` 仍 3 个、无 JS 报错。
- **线上实测认领后**：40 高 / 8 圆角 / `rgb(179,179,179)`（`$c-gray-350`）/ 阴影 / 14px
  —— 与静态站规格逐项一致；箭头存在且展开时旋转；原生 select 与
  `data-gb-plan-select` 都保留，**change 事件照常触发**（对方价格逻辑不受影响）。

⚠ **`liquid/snippets/gb-sub.liquid` 那份改动因此不必推了**，留作备选并已在
`liquid/README.md` 标注。要推的变成 `assets/main.js`——**那是我们自己的文件，不需要 liquid 授权**。

### 验证

`tools/r73check.py` 扩到覆盖本轮，两个模式都全绿：

- `--password 1234`（注入模式，验 r74 改动）：**32 ok / 0 FAIL**
- `--password 1234 --as-served`（线上真实状态）：**33 ok / 0 FAIL**
  —— select 那条断言为 `False`（仍是原生），**这是预期**：main.js 尚未推。

⚠ 判据里 `BEFORE fix: header scrolls away` 那条**改成了信息输出，不再是断言** ——
r73 的 CSS 已上线，线上不再复现该 bug，它继续当断言就会永远报红。

### 文件清单

```
改  assets/main.js                   selectBox.init() 认领线上订阅下拉（一条循环）
改  assets/customstyle.scss          $build → 20260907-r74
改  assets/customstyle.css           编译产物（双写）
改  *.html（12 个）                   129 处 ?v= 升到 r74
改  tools/r73check.py                +4 条（main.js 认领、静态站零变化、按钮规格）；
                                     BEFORE 那条降级为信息输出
新增 tools/r73shots/                  线上/静态站波浪截图各 3 张
改  docs/CHANGELOG.md、docs/HANDOFF.md、docs/LIVE-GAP.md、docs/LIVE-BACKLOG.md、liquid/README.md
```

### 遗留 / 待推

- **`assets/main.js` + `customstyle.css` + `.scss` 待推**（升了 `$build` 所以 CSS 也要跟着走）。
- **faq 波浪要真正修好，得补回上方的 section**：how-gumi-works 后台加 `gb-product`（一步操作），
  pdp 要新写 `gb-app-section` 的 liquid（工作量大，见 LIVE-GAP 第一节）。**本轮都没做**。
- reviews 页 faq 上方那个波浪线上是 `--lg`（129 高）、静态站是 97 —— 未查，不在本轮范围。

---

## 第七十三轮（2026-09-07）— live 站五条：header 吸顶失效、gallery 贴合、订阅下拉、按压下沉（`$build` = `20260907-r73`）

需求（对话，任务文档未换版，md5 仍 `2d70c334…`）五条，全部针对**线上**：
header 缺 sticky / `.gb-product__media` top 改 80 / `gb-sub__select` 调回原样 /
`.gb-product__cta` margin-top 20 / 按钮点击去掉下沉。

### 1. header 吸顶：规则一直在，是被 Shopify 的包裹层吃掉的

`.gb-header { position: sticky; top: 0 }` 第十四轮就写了，静态站正常。线上实测祖先链：

```
header#site-header            pos=sticky top=0px  h=81   ← 规则在
section#shopify-section-...   pos=static          h=81   ← 父盒 = header 自身高度
div#header-group              pos=static          h=121  ← 40(公告) + 81
div.gb-page-wrapper           pos=static          h=5409
```

**sticky 只在父盒内粘**，而父盒高度正好等于 header —— 滚一下就到底。
实测滚 900：`top 40 → -860`。这正是那条注释预告的情况
（"A sticky element has to sit directly in `<body>`; inside any wrapper it only sticks
within that wrapper"），只是当时没有线上环境可验。

**三个候选在线上逐个注入实测**，选 A：

| 方案 | header | 公告条 | 布局 |
|---|---|---|---|
| **A `#header-group` + 其直接子都 `display: contents`** | **粘在 0 ✓** | 正常滚走 ✓ | 不变 ✓ |
| B 只让 section wrapper `contents` | 仍滚走 ✗ | — | — |
| C sticky 挂 `#header-group` | 粘在 40 | **公告条也粘住 ✗** | 不变 |

B 无效是因为 `#header-group` 自己那 121px 的盒子还在约束；C 违反"公告条不跟着走"的设计。
A 把两层包裹盒都撤掉，`.gb-header` 的包含块回到 `.gb-page-wrapper`（整页高）。

⚠ **`display: contents` 安全的前提已验**：`theme.liquid` 里读 `headerGroup.children`
的测量脚本第一行就是 `if (!header || !headerGroup) return`，而它找的 `#header-component`
是 Horizon 原生 header —— **这个店用的是 `gb-header`，线上实测该节点不存在**，脚本本来就早退。

**静态站零视觉变化**（没有 `#header-group`），与第六十四轮那三处包裹层规则同类。

### 2. PDP gallery 贴合 header（104 → 80）

`top: calc($h-header + 24px)` = 104 改成 `top: $h-header` = 80。板上那 24 是量到视口顶的，
header 吸顶后这 24 变成了 header 下方的额外空隙，客户要去掉。
**tablet 档跟着改成 `fluid($h-header-mobile, $h-header)`** —— 该档 header 高度本身是斜坡，
写死 80 会在 768 端多出 16px 空隙。实测五档全部紧贴：

| 视口 | 768 | 1024 | 1280 | 1281 | 1440 |
|---|---|---|---|---|---|
| media.top | 64 | 71.98 | 79.97 | 80 | 80 |
| header 高 | 64 | 72 | 80 | 80 | 80 |

### 3. `gb-sub__select` 退回了原生下拉：少一个 `data-select`

静态站 `<select class="gb-sub__select" data-select>` → `selectBox` 接管成按钮 + ul（箭头可旋转）。
**线上是 `data-gb-plan-select`，没有 `data-select`** → `selectBox` 不认，渲染的是原生 `<select>`。
线上实测 `wrapped: False, button: False`。

改 `snippets/gb-sub.liquid`，**两个属性并存**：`data-select data-gb-plan-select`。

⚠ **不冲突已验**：`selectBox` 是增强不是替换 —— 原生 select 留在 DOM 当值载体，
选中后 `dispatchEvent(new Event("change", {bubbles: true}))`；对方 `gb-product.liquid:274`
正是 `planSelect.addEventListener('change', …)` 读 `this.value`。
线上注入后实测**点选项确实触发了 change**，价格逻辑不受影响。

### 4. `.gb-product__cta` 的 20px：两边结构不同，选择器必须能区分

| | cta 的父 | 与订阅框间距 |
|---|---|---|
| 静态站 | `.gb-sub` 内（最后一个孩子） | `.gb-sub` 的 `gap: 20px` → **20** |
| 线上 | `.gb-product__form` 直接子（它是 submit，必须在 form 里） | **0** |

客户要的 20 正是静态站本来就有的。直接写 `.gb-product__cta { margin-top: 20px }` 会让
**静态站变成 40**（flex 里 margin 与 gap 叠加不折叠）。
改用 `.gb-product__form > .gb-product__cta` —— `.gb-product__form` **只存在于线上**
（静态站 11 页与 scss 里都搜不到），子组合器天然把静态站排除在外。

### 5. 去掉按压下沉

5 处 `&:active { transform: translateY(1px) }` 删除：`.gb-btn` / `.gb-promo-panel__copy` /
`.gb-footer__submit` / `.gb-product__label-btn` / `.gb-product__cta`。
这 5 个块里 `transform` 的唯一用途就是这个下沉，所以 `transition` 列表里的 `transform` 一并删掉
（否则是死代码），`.gb-btn` 上那段讲 press state 的注释也跟着改。

⚠ **8 处 `:active { transform: scale(…) }` 保留** —— 那是缩放不是下沉
（`.gb-rv-panel__close` / `.gb-cart__close` / `.gb-cart-item__remove` / `.gb-cart-item__step` /
`.gb-header__icon` / `.gb-header__panel-close` / `.gb-reel` / `.gb-reels__btn`），
判据里逐个验过它们的 `transition` 仍带 `transform`，没被连带删掉。
⚠ **代价**：hover 规则都在 `@media (hover: hover)` 后面，下沉原本是触摸端**唯一**的按压反馈，
现在触摸端点按钮没有任何视觉回应。这是客户明确要求，登记在 HANDOFF「不要报成 bug」。

### 验证

`tools/r73check.py`，**29 条全过**（`--password 1234` 跑线上那段）：

- CSS 文本 15 条：下沉 0 处、scale 8 处仍在、5 个块的 transition 不再带 transform
  （⚠ 每条负向断言前都先验锚点，第一版正则按压缩形式写、又把 `text-transform` 算成命中，
  假绿过一次）
- 静态站 5 条：gallery top=80、cta margin 仍 0 且与上方仍 20、cta 父仍是 `.gb-sub`、header 仍粘 0
- **线上 9 条**（注入新 css + `data-select`，不推送）：**先复现 bug**（BEFORE header 滚走）
  → 修后 header 粘 0、公告条仍滚走、gallery 粘 80、cta 20、select 被接管、
  原生 select 仍在、**点选项触发 change**

另跑：11 页 header 全部粘 0、无水平溢出、按钮数与零宽数正常、无 JS 报错；编译幂等
（两次 md5 `676fba65…`）。

### 三方对比（推送前）

`theme pull` 到 `live-20260907-0121`（587 文件），与 `baseline-r72` 只差 2 个文件，
**都是对方改的、不是我们的**：

- `layout/theme.liquid` — 把 `{% render 'cart-drawer' %}` 从注释里放了出来
- `config/settings_data.json` — 新增 `auto_open_cart_drawer: true`

即**对方启用了 Horizon 原生购物车抽屉**（与我们的 `.gb-cart` 是两条路线，见 LIVE-GAP 第四节）。
我方三个 assets（`customstyle.css` / `.scss` / `main.js`）线上与基线逐字节相同，基线干净。

### 文件清单

```
改  assets/customstyle.scss          header 包裹层 contents；gallery top 80；cta 20（live-only）；
                                     删 5 处按压下沉 + 对应 transition 的 transform；$build → 20260907-r73
改  assets/customstyle.css           编译产物（双写）
改  *.html（12 个）                   129 处 ?v= 升到 r73
改  liquid/snippets/gb-sub.liquid    补 data-select（仓库镜像，未推）
新增 liquid/r73.patch
改  liquid/README.md                 状态表加一行
新增 tools/r73check.py               本轮 29 条判据（含线上注入）
新增 tools/r73probe.py               sticky 祖先链诊断探针
改  docs/CHANGELOG.md、docs/HANDOFF.md
```

### 推送（2026-09-07，需求方指示「liquid 暂先不改，推送样式和 js」）

推了 **2 个文件**：`assets/customstyle.css` + `assets/customstyle.scss`
（`--only` 逐个 + `--nodelete` + `--allow-live`）。

⚠ **`main.js` 没推，因为本轮根本没改它** —— 三方对比里本地 / 线上 / 基线三者逐字节相同。
「推送样式和 js」里的 js 这一轮是空集，不是漏推。

推送前建了**不含 liquid 改动的干净副本** `push-r73/`（从推送前快照复制 + 只放入两个 CSS），
与线上差异恰好 2 个文件、liquid 差异 0 处 —— 这样即使命令写错也推不到 liquid。推完已删。

回读：**587 → 587 文件数不变**，两个文件与推送副本逐字节相同、md5 与本地源一致
（`676fba65…`），**未推的 585 个文件零改动**。
CDN 层交叉验证（`https://gumi.com.au/cdn/shop/t/2/assets/customstyle.css`，不受密码保护）：
服务的是压缩形式，`display:contents` 1 处、`margin-top:20px` 1 处、`translateY(1px)` **0 处**。

**线上真实效果（`--as-served`，不注入任何东西）30 条全过**：header 粘 0、公告条仍滚走、
gallery 粘 80、cta 20px、`.gb-btn` 的 transition 不再含 transform；
select 仍是原生控件 —— **这是预期的**，liquid 按指示没推。

新基线 `Gumi-Brand-shopify/baseline-r73/`（587 文件）。

### 遗留 / 待推

- **第 3 条（`gb-sub__select`）未推**：`snippets/gb-sub.liquid` 补 `data-select` 已改好并验过
  （注入模式下 selectBox 接管且 change 正常派发），存在 `liquid/snippets/` 与 `liquid/r73.patch`，
  工作副本 `Gumi-Brand-shopify/work-r73/`。⚠ 推 liquid 需逐次授权。
  **在推之前，线上这个下拉一直是原生控件**，别再报一次。
- 静态站的 `.gb-product__form` 规则与 `#header-group` 规则在本地是**零匹配**的，
  静态站上看不出效果，只有线上能验 —— 别当成没生效。

---

## 第七十二轮（2026-09-04）— 「文字先出现」真正修好：行揭示补上 `html.js` 门（`$build` = `20260904-r72`）

需求：第七十一轮推完后**现象仍在**。第七十一轮的 `defer` 只把窗口从 4029ms 压到 3350ms，
判断「瓶颈是 HTML 体积不是 parser blocking」是对的，但**没解决问题**。

### 根因：两套入场效果只有一套挂了门

`.wowo` 有 `html.js .wowo { opacity: 0 }`（第十四轮建立），`[data-line-reveal]` **没有** ——
它只有「脚本没跑完就让文字可见」的兜底。所以 main.js 慢多久，文字就裸露多久。
**这是两套机制长期不一致，不是新引入的 bug。**

### 改动两处，缺一不可

1. **CSS 补门**（`customstyle.scss`）：

```scss
html.js [data-line-reveal]:not(.is-split) { opacity: 0; }        // 0-3-1
html.js [data-line-reveal]:not(.is-split) > .gb-ink-halo { opacity: 0; }
```

压过原有的 `[data-line-reveal]:not(.is-split){opacity:1}`（0-2-0）；`js` 类被摘掉时自动落回它。

2. **门脚本兜底 `4000` → `10000`**（`snippets/gb-head.liquid` + 静态站 12 个 HTML）。

⚠ **只加 CSS 门是无效的，本地实测证明了这一点**：门确实生效（t=4127 opacity=0），
但 **t=4257 又被摘掉** —— `setTimeout(u, 4000)` 在 4s 时武断判定「脚本挂了」，
而 main.js 限速下 4.25s 才跑起来，**兜底比脚本早 250ms 误判**。

**为什么可以放心放宽定时**：第七十一轮加的 `defer` 保证 main.js 在 `load` **之前**执行
（defer 在 DOMContentLoaded 前，load 在其后）。所以门脚本里 `addEventListener("load", u)`
那条是**完全可靠的主信号**，10s 定时只防 `load` 永不触发的极端情况。
—— 第七十一轮的 defer 因此不是白做的，它是这一轮能成立的前提。

### 验证（线上实测，跑两次）

| 指标 | r70 前 | r71 后 | **r72 后** |
|---|---|---|---|
| CLS | 0.00354 | 0.00000 | **0.00000** |
| 文字可见窗口 | 4029 ms | 3350 ms | **0 ms** |

线上时序：`t=360 opacity=0 is-split=False` → `t=3815 is-split=True` 才揭示，
探针不再报 `sat FULLY VISIBLE`。

**降级路径也验了**（这条必须验，否则就是拿铁律 12 的教训换闪烁）：
`route('**/main.js*', abort)` 拦掉主脚本后 —— `html.class` 里 **`js` 已被摘掉**，
文字 `opacity=1`、高度 >0 正常可见，而且**在 load 后 1.5s 就恢复，不用等那 10s**。

其余：编译幂等（两次 md5 `eefe6f1a…`）、`theme check` 15 vs 15 无新增、
回读三个文件逐字节相同、587 → 587 零误伤、线上 CSS 压缩形式里确认到门规则各 1 处。

### 文件清单

```
改  assets/customstyle.scss          补 html.js 行揭示门；$build → 20260904-r72
改  assets/customstyle.css           编译产物（双写）
改  snippets/gb-head.liquid          门脚本兜底 4000 → 10000（线上，已推）
改  liquid/snippets/gb-head.liquid   仓库镜像
新增 liquid/r72.patch
改  *.html（12 个）                   门脚本兜底 4000 → 10000；129 处 ?v= 升到 r72
改  docs/CHANGELOG.md、docs/HANDOFF.md
```

推送 `--only` 三个（`customstyle.css` / `.scss` / `gb-head.liquid`）+ `--nodelete` + `--allow-live`。
新基线 `baseline-r72/`。

### 遗留

- 静态站 12 个 HTML 的兜底也改了，但**静态站尚未有推送目标**（它只是设计基准）。
- `<h2>`/`<h3>` 宿主装 richtext 4 处仍未动（DOM 不拆，不紧急）。
- 「swiper 全站无条件加载 154KB」这个优化点仍在，但**窗口已归零，不再是必需**。

---

## 第七十一轮（2026-09-04）— 线上 layout shift 与「文字先出现」：查出 richtext 嵌套 `<p>`

需求：「当前网站出现了 layout shift；wowo 效果刷新时先出现文字然后才执行」。
需求方给了 storefront 密码（`1234`）。
⚠ **这个密码第六十四轮就拿到过并用于线上实测**（见本文件第六十四轮「贯穿本轮的根因」段），
但第六十九、七十轮的记录写成了「密码保护挡住了实测，需向需求方要密码」——
**信息在轮次之间丢了，白等了两轮**。密码就写在 CHANGELOG 里，以后先 grep 再说没有。

### 先纠正现象归属

**出问题的不是 wowo。** 实测 `.wowo` 门全程 `opacity=0`，工作正常。
用户看到的是 `[data-line-reveal]` 行揭示。

### 根因一：main.js 太晚 → 行揭示的兜底窗口被拉长到 4 秒

`customstyle.scss:3321` 有一条**故意的**兜底：

```scss
// Script off or still parsing: text must never be stuck invisible
[data-line-reveal]:not(.is-split) { opacity: 1; }
```

main.js 拆行（加 `.is-split`）之前文字必须可见 —— 免得 JS 挂掉时文字永久不可见
（这正是 [[reveal-gate-must-track-module-liveness]] 那条教训）。问题在窗口长度：

| | 文字完全可见的时长（同样 4x CPU + Fast 3G） |
|---|---|
| 静态站 | **657 ms** |
| 线上 | **4029 ms** |

线上 `main.js` 在 **body 172KB 处、裸 `<script src>` 无 defer**，要等 HTML 解析到那里，
再等 `lenis.min.js` 与 154KB 的 `swiper-bundle.min.js` 依次下载执行。
实测 `window.gumi` t=3597 才出现，拆行 t=4603。

### 根因二：CLS 不是字体，是 richtext 嵌套 `<p>` 把 DOM 拆坏

CLS 0.00354 发生在 t=4607，与拆行时刻（t=4603）重合，与 `fonts.ready`（t=3746）无关。
追下去发现线上真实 HTML 是：

```html
<p class="gb-hero__lead" data-line-reveal><p>Real fruit, real veg…</p></p>
```

`gb-hero.liquid` 写 `<p class="gb-hero__lead">{{ s.lead }}</p>`，而 `s.lead` 是 **richtext，
自带 `<p>` 包裹**。HTML 规范下解析器遇到内层 `<p>` 会**强制关闭外层**，DOM 被拆成三个兄弟。
浏览器里实测：

- `.gb-hero__lead` **textContent 为空、高度 0**
- 文字落在一个无 class 的裸 `<p>` 里，**字号 16px（浏览器默认），不是设计的 20px**
- `data-line-reveal` 挂在空元素上 → 这段文字的行揭示**根本没生效**

全站扫描命中 **5 处**（`<p>` 宿主 + richtext 值）：`gb-footer.tagline`（11 页全部）/
`gb-hero.lead` / `gb-nutrition` 卡片 `text`（5 页 × 3）/ `gb-form-section.note` /
`gb-product.guarantee_note`。
⚠ `<h2>`/`<h3>` 宿主装 richtext 也是无效 HTML，但解析器不像 `<p>` 那样自动闭合，DOM 不拆，本轮未动。

### 改法（需求方两处拍板）

1. **剥掉外层 `<p>`**，不改宿主标签也不动 setting 值 —— 新增
   `snippets/gb-rich-inline.liquid`，五处改成 `{% render 'gb-rich-inline', html: … %}`。
   剥离链是 `strip_newlines | replace: '</p><p>', '<br>' | replace: '<p>','' | replace: '</p>','' | strip`，
   **多段落降级成 `<br>` 而不是粘连**。线上 DOM 因此与静态站一致，行揭示能正常挂在宿主上。
   （另一个选项是宿主改 `<div>`，没选：那样内部多一层块级 `<p>`，行揭示的拆行逻辑要另外处理。）
2. **三个脚本加 `defer`** —— defer 保证按文档顺序执行且在 DOMContentLoaded 之前，
   而 `main.js` 的启动是 `readyState !== "loading" ? fn() : addEventListener(...)`，
   defer 下 readyState 已是 `interactive`，**行为不变**。

### 验证

- `tools/liveprobe70.py` 是本轮新写的线上探针（storefront 密码走 CLI 参数，**不进仓库**）：
  逐帧采 `html.className` / 样式表到位情况 / `.wowo` 与 `[data-line-reveal]` 的 opacity 与
  `is-split`，并用 PerformanceObserver 收 CLS 明细与 `fonts.ready` / `window.gumi` 时刻。
  静态站与线上跑同一份，**657ms vs 4029ms 的对照就是它测出来的**。
- `tools/r71check.py` **21 条全过**；对未改动的 `baseline-r70` 跑 **16 条 FAIL**（判据非恒真）。
- `tools/_apply_r71.py` **可复跑**：从干净副本重跑，产物与 `work-r71` 逐字节相同。
- `shopify theme check`：**18 → 15 条 offense，无新增** ——
  消失的正是 `gb-scripts.liquid` 的 3 条 `ParserBlockingScript` error。
  **Shopify 自己的检查早就在报这个问题**，本轮修复正好消掉它。

⚠ **渲染结果未验**：`shopify theme dev` 起不来，上传阶段就失败 ——
报错全是 Horizon 基底自带的 `blocks/*.liquid`（`Invalid schema: setting with id=… default
must be a color or dynamic source access path`），**与本轮改动无交集**（本轮没碰任何 `blocks/`）。
临时开发主题 `#180447248631` 已 `theme delete`，店里恢复为 `Dev` + `Horizon` 两个。

### 文件清单

```
新增  liquid/snippets/gb-rich-inline.liquid   剥掉 richtext 外层 <p> 的 snippet
新增  liquid/r71.patch                        相对 baseline-r70 的 diff
改    liquid/snippets/gb-scripts.liquid       三个脚本加 defer
改    liquid/sections/gb-footer.liquid        tagline 走 gb-rich-inline
改    liquid/sections/gb-hero.liquid          lead 走 gb-rich-inline
改    liquid/sections/gb-nutrition.liquid     卡片 text 走 gb-rich-inline
改    liquid/sections/gb-form-section.liquid  note 走 gb-rich-inline
改    liquid/sections/gb-product.liquid       guarantee_note 走 gb-rich-inline
改    liquid/README.md                        加各文件推送状态表（两轮混在一起了）
新增  tools/liveprobe70.py                    线上 CLS / 揭示时序探针
新增  tools/_apply_r71.py、tools/r71check.py  应用脚本与判据
改    docs/CHANGELOG.md、docs/HANDOFF.md
```

工作副本 `Gumi-Brand-shopify/work-r71/`（基于 `baseline-r70` = 当前线上）。

### 推送与实测结果（**一半达标，defer 基本没用**）

分两步推，消除「section 引用了还不存在的 snippet」的窗口：先单推
`snippets/gb-rich-inline.liquid`（没人引用它，先到无害），再推其余 6 个。
两步都是 `--only` 逐个列出 + `--nodelete` + `--allow-live`。

回读：7 个文件与本地**逐字节相同**，其余 580 个零误伤，文件数 586 → **587**（新增那个 snippet）。
`r71check.py` 对线上快照 **21 条全过**。新基线 `baseline-r71/`。

线上实测（`liveprobe70.py --throttle`，跑三次）：

| 指标 | 修复前 | 修复后 |
|---|---|---|
| CLS | 0.00354 | **0.00000** ✅ |
| `[data-line-reveal]` 文字可见窗口 | 4029 ms | 3350 ms ⚠ 只降 17% |
| `window.gumi` 执行时刻 | t=3597 | t=3634 **几乎没变** |

DOM 侧确认修好：`.gb-hero__lead` 从「空、高度 0」变成**有文字、高度 60、字号 20px**
（此前文字落在裸 `<p>` 里用浏览器默认 16px），`gb-footer__tagline` / `gb-highlight-card__text`
同样，全部 `innerP: false`。三个脚本都带 `[defer]`。

⚠ **`defer` 对执行时机几乎没有帮助，之前「窗口降到几百 ms」的预期是错的。**
原因：脚本本来就在 body 末尾（172KB 处），解析到那里时 HTML 已快下载完、脚本也早被
preload scanner 取回了 —— **真正的瓶颈是 259KB HTML 的下载与解析**（限速下约 3.5s），
不是 parser blocking。defer 仍然保留（消掉了 theme check 的 3 条 error，无副作用），
但它解决不了这个窗口。

**CLS 归零是嵌套 `<p>` 修复的功劳**，与 defer 无关。

### 遗留

- **「文字先出现」仍未解决**，窗口 3350ms。要真正压掉得换手段，三条路：
  ① 把 `[data-line-reveal]` 纳入 `html.js` 门（像 `.wowo` 那样），窗口 → 0，
     但门脚本的 4s 兜底 vs main.js 3.6s 执行**余量只有 400ms**，更慢的网络会让兜底先触发；
  ② 配合 ① 把兜底从 4s 放宽，代价是 JS 真挂时文字要等更久才出现；
  ③ 减体积 —— `gb-scripts.liquid` 的注释写着「Swiper is loaded only where a carousel
     exists」，但**实际是全站无条件加载 154KB**，这是注释与实现不符，且是真实的优化点。
- `<h2>`/`<h3>` 宿主装 richtext 共 4 处未动（`gb-stats.title` / `gb-nutrition.title` ×2）——
  线上实测 DOM **没有被拆**（`<p>` 老实待在 `<h2>` 里），所以不紧急，但仍是无效 HTML。
- **顺带发现**：footer 版权行是 `© 2026 My Store` —— `{{ shop.name }}` 还是 Shopify
  默认占位，店铺设置里没填店名。属于后台设置，已记入 LIVE-BACKLOG。
- `<h2>`/`<h3>` 宿主装 richtext 共 4 处（`gb-stats.title` / `gb-nutrition.title` ×2）未动 ——
  DOM 不会被拆，但仍是无效 HTML，且 `<p>` 是块级，可能影响行揭示的拆行。待查。

---

## 第七十轮（2026-09-04）— 线上零碎缺口：10 条查证后只剩 3 条，首次改 liquid

需求：「修复 live 站上的问题」，范围定为 LIVE-GAP 第三节的零碎缺口 + 模板挂载。
需求方两处拍板：**不碰 Online Store Editor 托管的 JSON**（推它们会覆盖对方后台的设置）、
**改过的 liquid 进仓库 `liquid/`**。

### 先拉最新线上再动手

`theme pull` 拉 `Dev #180348977399` 为 `live-20260904-1251/`，与 `baseline-r68`
**逐字节完全一致**（586 vs 586，`diff -r` 无输出）—— 对方那段时间没动过。

### 10 条「缺口」查证后只剩 3 条

判据报的缺失里有 5 条是假信号或已处理，逐条写进了 `docs/LIVE-BACKLOG.md` 第三节：

| 条目 | 真相 |
|---|---|
| `gb-acc-body__media` | 对方当天早上补的 `gb-product.liquid` 里已有 |
| `gb-logo-scroll__img--abc/vogue/wellbeing` | 线上有 `class_suffix` setting，`index.json` 三个 block 的值也填好了，类名由 `{% assign %}` 拼出 |
| `gb-stats.title` 的换行 | 静态站本就是裸 `<br>`（全断点断行），线上写法正确 |
| `gb-rv-panel__glyph` | 第六十六轮已适配 —— `customstyle.scss:1888` 特意把规则挂在 `svg` 上，就因为线上是裸的 |
| overline / lead 两个微调类 | liquid 没有接收口，需先加通道 + 后台填值 → BACKLOG 第二节 |

### 实做的三条

1. **`gb-stats.liquid`** — `.gb-stats__bear` 里补 4 个 `gb-stats__arrow--1..4`。
   SVG 由脚本从 `index.html` 正则提取**逐字节搬运**，不手抄。位置必须是 bear 的直接子：
   CSS 的 `left/top` 是百分比，锚在 `.gb-stats__bear`（它 `position: absolute`，
   stack 档转 `relative`）。
2. **`gb-reviews.liquid`** — 补法务免责声明 `gb-reviews__disclaimer`，
   加 `textarea` setting **带 default**。JSON 里没有这个 key 时 `section.settings`
   取 schema default，所以 index / pdp / how-gumi-works 三个实例都会生效，**不用碰模板 JSON**。
3. **`gb-expert.liquid`** — `newline_to_br` 产出裸 `<br>`，桌面端也断行；稿上这个标题
   只在 ≤767 断。改成先备好 `title_html` 再输出，**两种拼写都 replace**
   （`<br />` 与 `<br>`）——storefront 密码保护读不回渲染结果，无法实测是哪一种，
   两条互为 no-op，留着都安全。

### 验证

- `tools/_apply_r70.py` **可复跑**：从干净副本重跑，产物与 `work-r70` 逐字节相同。
- `tools/r70check.py` **24 条全过**。活性自检做了两层：对**未改动的 live 快照**跑
  → 16 条 FAIL（证明判据测的是本轮改动，不是恒真）；逐处破坏（改 arrow 编号 /
  改 disclaimer 文案 / 删一条 replace）→ 各自被抓到。
- `shopify theme check` 对改前改后各跑一次：**18 vs 18 条 offense，逐条相同**
  （差异全是路径前缀），三个 section 一条都没引入。

⚠ **视觉层一条都没验过** —— 店铺开着 storefront 密码保护，外部访问渲染
`layout/password.liquid`。判据只能证明结构与 token 正确，证不了渲染对。

### 推送（2026-09-04，**这是我们第一次推 liquid**）

需求方点名只推**两个**：`sections/gb-stats.liquid` + `sections/gb-expert.liquid`。
`gb-reviews.liquid`（法务免责声明）**留在本地未推**。

```
--only sections/gb-stats.liquid --only sections/gb-expert.liquid --nodelete --allow-live
```

三方对比：推前重新 `theme pull` 为 `_precheck`，与 `live-20260904-1251` **无任何差异**
（586 vs 586）—— 对方没动过，无冲突；`work-r70` 与远端的差异正好是我改的那 3 个文件，无多余。

回读验证（推完再 `theme pull`）：

- 推的两个文件与本地**逐字节相同**
- **没推的 `gb-reviews.liquid` 与推送前一致**，没被顺手带上去
- 全主题**只有这两个文件变了**，其余 584 个零误伤；文件数 586 → 586（`--nodelete` 生效）
- `r70check.py` 对线上回读快照跑：24 条中 18 过 6 红，**红的全部且仅仅是 disclaimer**
  ——判据精确区分了推了的与没推的

⚠ 推送日志里的 `Cleaning your remote theme` 会吓人，但带了 `--nodelete`，
**文件数与逐文件比对都证明没删任何东西**。

新基线 `Gumi-Brand-shopify/baseline-r70/`（= 当前线上）。临时目录 `_precheck` / `_verify` 已删。

### 文件清单

```
新增  liquid/README.md                    新目录的约定：为什么存在、改之前先 pull 比对
新增  liquid/sections/gb-stats.liquid     改后完整文件（与将推上 live 的逐字节相同）
新增  liquid/sections/gb-reviews.liquid   同上
新增  liquid/sections/gb-expert.liquid    同上
新增  liquid/r70.patch                    相对 live-20260904-1251 的 diff，给对方合入用
新增  tools/_apply_r70.py                 三处改动的应用脚本，锚点唯一性自检
新增  tools/r70check.py                   本轮判据，接受 theme 目录作参数
新增  docs/LIVE-BACKLOG.md                后台待填 / 待加通道 / 不用做的，三节
改    docs/CHANGELOG.md                   本轮
改    docs/HANDOFF.md                     头部状态 + 不要报成 bug 清单 + 工作区状态
```

线上快照：`live-20260904-1251`（推送前证据）→ `work-r70`（工作副本，改动在这里）。

### 遗留

- **`gb-reviews.liquid` 未推**（需求方本轮只点名推另外两个）。改动与判据都在本地，
  `liquid/sections/gb-reviews.liquid` 与 `work-r70` 里各有一份，随时可推。
  推之前照例重新 `theme pull` 做三方对比。
- **B 组一条没做**：footer 22 处换行、page-hero 标题换行、overline、两个 lead 微调类
  都需要先加 liquid 通道（需求方本轮选了只做 A 组），四页挂 `gb-product` 属于托管 JSON。
  全部逐条在 `docs/LIVE-BACKLOG.md`。
- **顺带发现一个线上真 bug，未修**（属于托管 JSON，按纪律不碰）：
  `index.json` 的 `reviews.title` = `"Aussies are obsessed.Here's why."` —— 少了 `\n`，
  两句会直接粘连。`page.how-gumi-works.json` 的同一 section 是对的。
  已写进 BACKLOG 第一节，后台改一下即可。

---

## 第六十九轮（2026-09-04）— 静态站 ↔ live 差距比对 + 补推 r68

需求：「shopify 站除了购物车其他已经完成，检查静态站和 live 的差距」。
**前提不成立** —— 除购物车外还有 6 个模块线上没有 liquid。全程只读比对，
`theme pull` 拉 `Dev #180348977399` 全量 586 文件为 `live-20260904-1134/`。

### 三层判据（新增，都接受 live 目录作参数）

| 脚本 | 比什么 | 结论 |
|---|---|---|
| `tools/livediff.py` | 两侧 `gb-*` 类名集合差集 | 27 个块静态站有、线上全文搜不到 |
| `tools/livepages.py` | 11 页 `<main>` 区块序列 vs 模板 section 序列 | 8 处页面级缺口 |
| `tools/livesect.py` | 两边都有的 section，内部 token 差异 | 81 个 token 缺在 section 内部 |

**写判据时踩的两个假信号**（都改掉了，方法写进 `LIVE-GAP.md` 第六节）：

1. **只扫 `class="..."` 会虚报一堆基础块缺失** —— Liquid 用
   `{% assign classes = 'gb-ingredients' %}` 和 `{% form class: 'gb-form' %}` 造类名。
   改成 live 侧扫全文：**全文搜不到才是确凿缺口**。
2. **HTML 解析器的深度计数被 SVG 自闭合标签搞乱** —— `<path>` 被当成 `<main>` 的直接子，
   `gb-expert-card` 因此虚报 6 次。改用缩进定位（页面是两空格一级），
   并加断言：匹配不到就当场报错，不静默出错结果。

`gb-scallop--{{ s.trailing_scallop }}` / `gb-stat--{{ b.variant }}` 这类 setting 拼接
已在 `livesect.py` 里按前缀抑制；`{% render %}` 会跟进（否则 `gb-sub__*` 虚报 26 条）。

### 比对结论

- **模块级缺口 6 个**：营养标签弹窗 `gb-nl-*`（5 页）/ 首单 promo 弹窗 `gb-promo-modal|panel`
  （index）/ PDP promo 卡 `gb-promo-card` / PDP 对比表 `gb-vs` / testimonial 卡
  `gb-testimonial(s)`（在 `gb-reviews` 内部）/ shipping 表格 `gb-rich-table`。
  另有 app 挂载点 `gb-app-section` 与 `gb-product__app-slot`。
- **模板挂载缺口**：`gb-product.liquid` 只挂在 `product.json`，静态站另有 4 页带这个区块
  （index / reviews / how-gumi-works / our-story）—— 只需在模板 JSON 加记录，不用写 liquid。
- **`gb-br-narrow` 全站缺失**：响应式强制换行辅助类，11 页都在用 → 手机端折行会与稿不一致。
- **购物车不是「没做」，是装了另一套**：`layout/theme.liquid:172` 渲染 Horizon 原生
  `cart-drawer`、`cart_type: "drawer"`，但 `gb-header.liquid:18` 的图标是
  `<a href="{{ routes.cart_url }}">`，既不是原生抽屉的触发器也不是 `data-modal="gb-cart"`。
  源码上看点图标会跳 `/cart` 页。⚠ **密码保护挡住了实测，这条只是读源码的推断。**
- **对方在今早 08:30 之后补上了 PDP 订阅模块的 liquid**（新增 `sections/gb-product.liquid` +
  `snippets/gb-sub.liquid`，改 `templates/product.json`）—— `LIQUID-TODO-subscription.md` 可归档。
- **52 个本地图不在线上 `assets/` 不是缺口**：线上走 `image_picker` + `image_url`（Files/CDN），
  19 个 picker、80 处 `image_url`，**15 个已绑定的图片设置全部非空**。

### 顺带发现并处理：r68 从未推上 live

`HANDOFF.md` 头部写着「已推上 live」，实测线上停在 r67。diff 正好只等于第六十八轮那一轮的
改动（build 号 + 注释 + 两处 `math.round`），无第三方内容混入 → **是没推，不是被覆盖**。
经需求方指示已补推，详见第六十八轮的「推送」段。

### 文件清单

```
新增  tools/livediff.py            类名集合差集
新增  tools/livepages.py           页面级 section 序列对照
新增  tools/livesect.py            section 内部 token 差异
新增  docs/LIVE-GAP.md             差距报告（含「不是差距的」一节 + 判据局限）
改    docs/CHANGELOG.md            本轮 + 第六十八轮补「推送」段
改    docs/HANDOFF.md              头部 build 状态 / 第八节标题与 $build（停在 r65）/
                                   提交历史改成 git 与 Shopify 两条线分开 / 挂上 LIVE-GAP
推    assets/customstyle.css|.scss|main.js   r67 → r68（见第六十八轮「推送」段）
```

线上主题快照落在 `Gumi-Brand-shopify/`：`live-20260904-1134`（推送前 r67，证据）→
`baseline-r68`（当前线上）。临时目录 `_precheck` / `_verify` / `push-r68` 跑完已删。

### 遗留

- **视觉层一条都没验过** —— storefront 密码保护，外部访问渲染 `layout/password.liquid`。
  要验渲染结果得向需求方要密码。购物车那条推断也卡在这里。
- **git 落后 11 轮**：第五十八～六十八轮未提交（26 个已跟踪改动 + 42 个未跟踪新增，
  含 `docs/account/`、`images/reel-*.mp4`）。
- `livesect.py` 报的 81 个 token 里，波浪相关的多数是**架构差异**（线上把波浪做成
  `leading_scallop` / `trailing_scallop` setting，静态站写死），不是缺口，未逐条清理。

---

## 第六十八轮（2026-09-04）— 板底波浪比顶边浅 0.5px：分数绘制宽度（`$build` = `20260904-r68`）

接第六十七轮补记。上一轮「未复现」，需求方追问「就目前属性来看能否修复」，
于是不再靠截图，改从属性推 —— **找到了，并修了**。

### 推导

`.gb-cta-band__plate` 的圆瓣是 `border-image` 九宫格：

```scss
border-image: scallop-tile($r, $px, $py) $r fill / #{$r}px / 0 round;
//                                       ↑slice      ↑paint width
```

`$plate-r-pc` = **58.8848**，同时用作 slice（源图坐标）与 paint width（绘制尺寸）。
**paint width 是分数**：58.8848px 落在半个设备像素上，顶、底两个切片因此朝**相反方向**舍入。

实测（DPR 2，1440）：**顶瓣 20.5 / 底瓣 20.0**。板的理论谷深是 **20.55**，
所以浅的那一边是底边。差值只有 0.5px，但它是**恒定的、每一档都在**，
在深色大色块上就是「底边的波浪比上面浅一点」。

### 排除掉的（都做了实验，不是推断）

- **规范压缩**（盒高 < 上下 paint width 之和时切片等比缩小，CSS Backgrounds 3 §6.3）：
  把板高从 392 一路压到 70（阈值 117.77），波浪**始终上下对称** —— 压缩是等比压两边，
  不会只削底边。假设证伪。
- 祖先 `overflow` 裁切、scallop 遮挡、内容溢出、线上 8 页 × 5 档、6 档 DPR：全部排除。

### 改了什么

```scss
- $plate-r-pc fill / #{$plate-r-pc}px / 0 round
+ $plate-r-pc fill / #{math.round($plate-r-pc)}px / 0 round
```

⚠ **只动 paint width，slice 保持精确值**。slice 索引源图，动它会切错位置；
paint width 是渲染尺寸，取整是渲染层的决定，不改设计几何。
两档都改（pc 58.8848 → 59，mob 39.9189 → 40）。

| 视口 | 改前 顶/底 | 改后 顶/底 |
|---|---|---|
| 1440 | 20.5 / **20.0** | 20.5 / **20.5** ✅ |
| 1280 | 20.5 / **20.0** | 20.5 / **20.5** ✅ |
| 1024 | 20.5 / **20.0** | 20.5 / **20.5** ✅ |
| 390 | 18.0 / 18.0 | **18.5 / 18.5** ✅（理论 18.81，更接近） |

取整后不仅对称，**谷深也更接近板的理论值** —— 20.55 对 20.5 比对 20.25 近。
⚠ DPR 1 下顶底仍差 1px，那是设备像素网格的固有限制，取整与否都一样。

### 文件清单

```
改  assets/customstyle.scss   两处 border-image paint width 取整 + $build → 20260904-r68
改  assets/customstyle.css    编译产物（双写）
改  *.html                    129 处 ?v= r67 → r68
改  tools/platecheck.py       补底/右两条边 + 顶底谷深容差 2.0 → 0.6 + paint width 整数断言
```

### 判据

`tools/platecheck.py` 这一轮补了三层，全部通过（14 档）：

1. **四条边一起量**（第六十七轮补记时加的）。此前**只量顶边与左边** ——
   底边被裁平或九宫格最后一行没画出来，历轮全绿也照样漏过。
2. **顶底谷深容差 2.0 → 0.6**。2px 的窗口正好放过了这次的 0.5px。
   ⚠ 768 档实测差 0.6，卡在边界上（`padding-block: fluid(3.75px, 52px)` 给出分数板高），
   所以容差不能再收。
3. **直接断言 paint width 是整数** —— 因为 0.5px 仍在上面那条容差之下，
   守结果不够，得守成因。

**活性自检**：把产物里的 `fill/59px` / `fill/40px` 改回分数 → **16 条 FAIL**，
每一档都报「border-image-width 是分数——顶/底切片会朝相反方向舍入」。

**回归**：`rwd` 全绿 / `assetpath` GREEN / `r63` 158 / `r64` 1528 / `r65` 122 /
`r66` 36 / `r67` 169 / `r67reel` 26，均 0 red。

### 过程里的两次自我纠正

- **一度把动画中间态当成 bug**：第一版截图只等了 700ms，而行揭示是 1.4s，
  截出来的标题最后一行底部平切。等到 3500ms 完全正常。
- **一度靠肉眼下结论**：把顶边和翻转后的底边并排看，觉得底边「明显更扁」，
  量出来只差 0.5px —— 眼睛把 0.5px 放大了。**铁律 2 不只对设计稿适用，对自查同样适用。**

### 顺带发现 / 未修

- **左/右边谷深仍差 0.5**（如 1440：左 22.0 / 右 21.5）。同一个舍入机制，
  但发生在宽度方向；paint width 已经取整，剩下的来自板宽本身的分数（如 350×508 的 508）。
  容差内，**未动**。
- **768 档顶底差 0.6**，来自 tablet 的 `fluid()` 分数板高，不是这次的成因。

### 推送（2026-09-04，晚于本轮改动，与第六十九轮的比对同一次会话）

本轮改完当时**没有推**，线上停在 r67 —— 是第六十九轮做静态站↔live 比对时发现的
（`HANDOFF.md` 头部当时写着「已推上 live」，与实测冲突）。

**推送前三方对比**（baseline = `baseline-dev-live`，即推完 r67 的线上快照）：

| 文件 | local≠base | remote≠base | 结论 |
|---|---|---|---|
| `assets/customstyle.css` | DIFF | same | 只有我改了，推 |
| `assets/customstyle.scss` | DIFF | same | 只有我改了，推 |
| `assets/main.js` | same | same | 本轮没改，一并推（幂等） |

对方在这期间改的是 liquid（新增 `sections/gb-product.liquid`、`snippets/gb-sub.liquid`，
改 `templates/product.json`），**与推送清单不冲突**。

**产物新鲜度**：`npx sass@1.77.8` 重编译 `customstyle.scss`，与仓库里的 `customstyle.css`
**逐字节相同** —— 推的不是过期产物（铁律 16 的双写判据）。

**推送清单（3 个文件）**：`assets/customstyle.css` + `assets/customstyle.scss` +
`assets/main.js`（`--only` 逐个列出 + `--nodelete` + `--allow-live`，
`--path` 指向线上快照的工作副本，不是静态站根目录 —— 静态站没有主题目录结构）。

**回读验证（三道，全过）**：

1. **CLI 拉回三个文件**：逐字节与本地相同。
2. **build token**：线上 `customstyle.css` 与 `.scss` 都是 `20260904-r68`（双写都到位）。
3. **关键改动**：线上压缩产物里 `fill/59px` × 1 + `fill/40px` × 1，
   分数形式 `fill/58.8848px` / `fill/39.9189px` **0 处**。
4. **零误伤**：全量拉回，文件数 **586 → 586**，除这三个文件外 `diff -rq` 无输出。

**基线滚动**：`live-20260904-1134`（推送前的线上证据，r67）→ `baseline-r68`（当前线上）。

## 第六十七轮补记（2026-09-04）— 查 `.gb-cta-band__plate` 底部被裁：未复现，补上判据盲点

需求方报「`.gb-cta-band__plate` 底部出现了被裁掉的情况」。**查完没能复现，没有改任何样式。**
下面是查了什么、排除了什么，以及顺带补上的判据。

### 排除的

| 怀疑 | 实测 |
|---|---|
| 祖先 `overflow` 裁掉板底 | 两个页面 × 4 档，plate 到文档根的整条祖先链 `overflow-y` 全是 `visible`，无一裁切 |
| 下方 scallop 盖住板底 | 与 plate 矩形相交的 `.gb-scallop` **0 个**；plate 完全在 `.gb-cta-band` 之内（板底距 band 底还有 98–247px） |
| 板底圆瓣画不全 | 逐列扫像素：**26 个档位**（2 页 × 13 档，390–2560）顶/底起伏差 ≤1.5px，底边一直在起伏 |
| 内容溢出板底 | 内容底始终在瓣谷之内（我第一版的"溢出"判定用错了基准 —— `border-image-width` 是九宫格切片的绘制宽度，不是内容禁区） |
| 线上结构不同 | 线上 faq / our-story 的 plate 几何与本地一致，祖先链同样无裁切 |

### 唯一能做出「底部被裁」的情形

**入场动画播放中**。`.gb-cta-band__title` 带 `data-line-reveal`，文字从
`.gb-line-mask`（`overflow: hidden`）里升起，升到一半时最后一行的下半截确实是被切平的；
`.gb-cta-band__plate` 自己还带 `wowo fadeInUp`（30px 位移，0.7s）。
⚠ **我第一次截图就踩了这个坑** —— 只等了 700ms（行揭示是 1.4s），
截出来的 "sufficient" 底部平切，一度当成了 bug。等到 3500ms 再截完全正常。

### 补上的判据盲点

`tools/platecheck.py` **只量顶边和左边**，底边和右边从来没进过判据 ——
**板底若被裁平或九宫格最后一行没画出来，历轮全绿也照样漏过**。
本轮补齐四条边：底/右的瓣数必须等于顶/左，谷深差不得超过 2px。

实测四边一致（如 1440：顶 14 瓣谷深 20.5 / 底 14 瓣谷深 20.0 / 左 4 瓣 21.5 / 右 4 瓣 21.5）。
**活性自检**：把底边剖面强制成常量（模拟削平）→ 立刻报 5 条，含
「底边 1 瓣 != 顶边 14 瓣——底边被裁或没画全」。

### 结果：第六十八轮找到了

需求方追问「就目前属性来看能否修复」，于是从属性本身推，**找到了**：
`border-image` 的**绘制宽度是分数**（58.8848px），顶、底两个切片因此朝相反方向舍入，
底边谷深比顶边浅 0.5px。见下一轮。

⚠ 本节「未复现」的结论是**在把容差放宽到 2px 的判据下得出的** —— 偏差真实存在，
只是当时的判据和我的肉眼都没分辨出 0.5px。

---

## 第六十七轮（2026-09-04）— halo 逐行化 + reel 在 1440 以上随视口缩放（`$build` = `20260904-r67`）

需求：
1. 「`gb-ink-halo` 能否由下往上出现和文字同步」
2. 「`gb-reel` 1440 及上能否始终保持设计显示的那种状态，中间显示三张、两端显示被裁掉一点的一张，
   类似静态站，并且 1440 以上卡片的宽度需要跟随屏幕宽度变化，高度跟随宽度比例变化」

---

### 一、halo 与文字同步 —— 第六十四轮只修对了一半

第六十四轮把 halo 从「等文字升完再淡入」改成了 `gm-halo-up`（clip 窗口 + 位移）。
**单行宿主确实同步了，多行的没有**，而当时的判据看不出来。

**实测（线上 + 本地，逐帧截图）**：`.gb-dosed__title` 在 1440 是 2 行，
mask 的 delay 是 `['0s', '0.15s']`，halo 的 delay 是 `0s` ——
第 80ms 那一帧，**光晕已经是完整两行的一整条，文字才露出第一行**。

**根因**：halo 是**整块**副本，只有一个 clip 窗口；文字是**逐行**揭示、每行错峰 150ms。
一个刚性移动的整块，其揭示前沿必然在第 2 行的 mask 启动之前就越过了第 2 行 ——
**整块 halo 与逐行揭示在原理上就无法对齐**，与参数无关。

**改法**：`main.js` 的 `groupLines()` 在拆完行之后，**为每一行克隆一份 halo**
（`.gb-ink-halo--line`），偏移到该行的 `offsetTop`，并把该行的 `--line-i` 写在上面。
于是每份光晕走自己那一行的 delay，和它背后的字一起升。

⚠ **halo 不能放进 mask 里**（第一版就是这么写的，随即推翻）：`.gb-line-mask` 要
`overflow: hidden` 才能裁住文字的滑动，而描边是 15px 的 `text-shadow` ——
放进去会被行盒**切平**。所以每份 halo 都停在 mask 外面，各自带一个 clip 窗口。

⚠ **`.gb-ink-halo--line` 必须补 `padding-bottom: $line-descend`**。
`translateY(100%)` 是相对元素**自身高度**解析的，而 `.gb-line-mask__inner` 带着
0.12em 的降部余量。不补的话 halo 的行程比文字短 0.12em，**中途快约 2px、提前到位**。
判据的 mid-flight 断言就是抓这个的（截图上看不出来）。

原来那份整块副本**留在 markup 里当无 JS 兜底**，拆行后 `display: none`。

### 二、reel 在 1440 以上随视口缩放

板上（1440）：卡片 304×540、gap 24，**三张完整 + 两端各一张被裁**。
1440 以上原本卡片钉死在 304，屏幕越宽挤进来的卡越多（2560 实测 7.8 张），取景就散了。

```scss
.gb-reel {
  width:  max(304px, 21.1111vw);   // 304/1440
  height: max(540px, 37.5vw);      // 540/1440
}
```

两条腿取的是**同一个 1440 分数**，所以 304:540 被锁死、高度跟着宽度走。
用 `max()` 而不是媒体查询：它在 1440 及以下正好回到 304/540，**边界不跳变**，
也不用新开断点（铁律 18 的值档不受影响）。

⚠ **gap 刻意不缩放**。`main.js` 的 `options()` 只在 `create()` 时读一次 `column-gap`，
而 resize 不会重建 Swiper —— 响应式的 gap 一动窗口就过期。
钉在 24 的代价只是可见张数从 4.39（1440）走到 4.54（2560），取景不变。

| 视口 | 卡片 | 比例 | 可见槽位 | 完整/触边 |
|---|---|---|---|---|
| 1280 | 304 × 539.7 | 0.5632 | 3.90 | 3 / 5 |
| **1440** | **304 × 540** | 0.5630 | 4.39 | 3 / 5 |
| 1600 | 337.8 × 600 | 0.5629 | 4.42 | 3 / 5 |
| 1920 | 405.3 × 720 | 0.5630 | 4.47 | 3 / 5 |
| 2560 | 540.4 × 960 | 0.5630 | 4.54 | 3 / 5 |

### 文件清单

```
改  assets/main.js             groupLines() 每行克隆一份 halo；flatten() 负责清理
改  assets/customstyle.scss    .gb-ink-halo--line 一族 + .gb-reel 改 max()
                               + $build → 20260904-r67
改  assets/customstyle.css     编译产物（双写）
改  *.html                     129 处 ?v= r66 → r67
新  tools/r67check.py          169 条，halo 逐行同步
新  tools/r67reel.py           26 条，reel 取景与比例
改  tools/r64check.py          halo 断言移交 r67（见下）
```

### 判据

- `tools/r67check.py` **169 ok / 0 red**：2 个宿主 × 多档宽度，逐行断言
  halo 数 == 行数、halo top == mask offsetTop、`--line-i` 递增、
  **每行 halo 的 delay == 同一行 mask 的 delay**、动画名对，
  外加一条 **mid-flight**：触发后 260ms 读两层的 `transform.m42`，差值须 ≤1px。
  还有一条 resize 后 halo 不累积（`flatten` 有没有清干净）。
  三处**活性守卫**：没有 mask、没有 halo、260ms 时没有东西在动，都直接判红 ——
  否则「都同步」会是个空命题。
- `tools/r67reel.py` **26 ok / 0 red**：5 档宽度的卡片尺寸、比例、可见槽位、
  完整/触边张数。
- **活性自检**（逐项反向改回产物）：
  | 改回 | 转红 |
  |---|---|
  | halo 去掉 `padding-bottom` | 8（全是 mid-flight 的 2~3px 提前） |
  | halo delay 去掉 `--line-i`（回到 r64 的整块时序） | 9（含 delay 不匹配、mid-flight 13.8 vs 25.7） |
  | reel 去掉 `max()` 缩放 | 6（2560 挤进 7.80 张） |

⚠ **`tools/r64check.py` 的 halo 断言已移除**，改由 r67 接管，并在原处写明了原因：
它**只把 halo 和 line 0 比**，所以整块 halo 在多行标题上出问题时它照样全绿 ——
这正是本轮要修的盲点。移除后 r64 仍是 **1528 ok / 0 red**（包裹层那部分不受影响）。

**回归**（全部 0 red）：

```
rwd 全绿   assetpath GREEN
r58 44   r59 96   r60 242  r61 151  r62 133  r63 158
r64 1528 r65 122  r66 36   r65interact 36
r67 169  r67reel 26                          合计 2741 条
```

### 推送（2026-09-04）

**推送前三方对比**：`assets/` **零差异**。对方改了三个文件，都不在推送清单：
`config/settings_data.json`（主题编辑器设置，**永远不推**）、`templates/index.json`（后台配区块）、
以及 `sections/gb-reviews.liquid` —— 后者是好消息：**他们补上了 `data-modal-media`**
（`docs/LIQUID-TODO-reels.md` 第 1 条的一半），reel 视频的播放器终于建得出来了。
⚠ 但 `.gb-rv-panel__glyph` 包裹层仍然没有，**这正好印证第六十六轮把 play 图标的隐藏规则
挂在 `svg` 而不是 `.gb-rv-panel__glyph` 上是对的** —— 挂在包裹层上到今天都不会生效。

**差异核对**：css 56 行（剔除 build token 后 26 行）、`main.js` 40 行，逐条都是本轮改动。
⚠ 核对时发现 `main.js` 里一句注释是旧的（第一版写的「放进 mask 里」，改成放在 mask 外后
没跟着更新）。**注释会误导下一个人**，先修了再推。

**推送清单（3 个文件）**：`assets/customstyle.css` + `assets/customstyle.scss` +
`assets/main.js`（`--only` 逐个列出 + `--nodelete` + `--allow-live`）。

**回读验证（三道）**：

1. **CLI 拉回**：3 个文件逐字节与本地相同，**零误伤**，文件数 584 → 584。
2. **线上 halo**（how-gumi-works，1440）：2 行 → **2 份 `.gb-ink-halo--line`**，
   `top` `['0px','48px']` 与 mask 的 offsetTop 一致，整块副本 `display: none`，
   `padding-bottom` 解析为 4.8px（0.12em × 40 行高）。
   **mid-flight：`mask=[19.9, 36.6]` / `halo=[19.9, 36.6]` —— 逐行完全相同。**
   这是最强的一条：两层在动画中途的 `transform.m42` 一致，才说明光晕真的贴着它那一行的字在走。
3. **线上 reel**：

| 视口 | 卡片 | 比例 | 完整 / 触边 |
|---|---|---|---|
| 1440 | 304.0 × 540.0 | 0.5630 | 3 / 5 |
| 1920 | 405.3 × 720.0 | 0.5630 | 3 / 5 |
| 2560 | 540.4 × 960.0 | 0.5630 | 3 / 5 |

线上实测 **22 ok / 0 red**（含三条活性守卫：dosed 必须多行、260ms 时必须有东西在动、
reel 必须存在，否则判红而不是静默通过）。

**基线滚动**：`baseline-pre-r67`（推送前，r66）/ `baseline-dev-live`（当前线上，r67）。

### 顺带发现 / 未修

- ⚠ **第六十四轮的记录里有一句是错的**：那里写「单行宿主（每个 `.gb-stat__value` 和
  `.gb-usp__value`）」。实测 **`.gb-usp__value` 根本没有 `data-line-reveal`** ——
  它带 halo 但从不参与拆行，那份光晕是静态显示的整块副本。
  本轮判据据此把它排除在外，已在 r67check 里注明。
- **play 图标不跟着卡片缩放**（`.gb-reel__play` 固定 85×53）。2560 时卡片 540 宽，
  图标相对更小。稿里没有 1440 以上的规格，**需求也只点了卡片**，没动。
- **2560 时卡片高 960px**，比多数笔记本视口还高。这是「高度跟随宽度比例」的直接结果，
  是需求指定的，不是 bug。若要封顶，给 `height` 再套一层 `min()` 即可，一处回退。
- **`.gb-ink-halo--line` 是运行时生成的节点**，页面 DOM 数会随行数增加
  （`cssnap.py diff` 对这些页本来就无效，见「不要报成 bug」三·3）。

## 第六十六轮（2026-09-04）— reel 弹窗的 play 图标隐藏（`$build` = `20260904-r66`）

需求：「`gb-rv-panel__video` 的 svg 隐藏起来」+「只推送修改的文件」。

### 改之前先看了线上是什么样

线上首页有 **10 个 `.gb-reel`，但带 `data-video` 的是 0 个** —— 对方按
`docs/LIQUID-TODO-reels.md` 第 2 条把属性名从 `data-video-url` 改成了 `data-video`，
**但后台还没填视频 URL**。所以点开任何一个 reel 都不会加 `.has-video`，
弹窗里就是稿的 fallback：灰底 + 一个 play 图标（实测 `svgVisible: true`）。需求指的就是这个图标。

### 改了什么

```scss
.gb-rv-panel__video {
  svg { display: none; }        // was: width: 85px; height: 53px
}
```

⚠ **选择器落在 `svg` 上，不是 `.gb-rv-panel__glyph` 上**。两边的 markup 不一样：

| | 结构 |
|---|---|
| 静态站（r62 起） | `<div class="gb-rv-panel__video" data-modal-media><span class="gb-rv-panel__glyph"><svg>…` |
| 线上 liquid | `<div class="gb-rv-panel__video"><svg>…`（裸的，LIQUID-TODO 第 1 条仍未做） |

挂在 `.gb-rv-panel__glyph` 上的规则在静态站会通过、**在线上会静默失配** ——
这正是第六十二轮那条 `.gb-rv-modal.has-video .gb-rv-panel__glyph { display: none }`
今天在线上不生效的原因。

### 文件清单

```
改  assets/customstyle.scss   1 条规则 + $build → 20260904-r66
改  assets/customstyle.css    编译产物（双写）
改  *.html                    129 处 ?v= r65 → r66
新  tools/r66check.py         36 条
```

### 判据

`tools/r66check.py` **36 ok / 0 red**，4 个页面 × 两种 markup：
`wrapped`（原样）与 **`bare`（JS 剥掉 `.gb-rv-panel__glyph`，复现线上的裸 svg）**。
每一遍都断言 `display: none` **且** 盒宽为 0，并带**活性守卫**——
先断言 `svg` 至少有 1 个，否则「它被隐藏了」是个空命题。

**活性自检**：把产物里的 `display: none` 改成 `block` → **12 red**，
`wrapped` 与 `bare` 两遍各 6 条，两种结构都被覆盖到。

**回归**（全部 0 red）：

```
rwd.py 全绿   assetpath.py GREEN
r58 44  r59 96  r60 242  r61 151  r62 133  r63 158
r64 1744  r65 122  r65interact 36  r66 36        合计 2762 条
```

### 推送（2026-09-04）

**推送前三方对比**：`assets/` **零差异**；对方在改 `templates/`（8 个 json 有变化，
另新增 `page.get-in-touch.json` / `page.referral.json`），与推送清单不冲突。
css diff 剔除 build token 后**恰好 3 行** —— `-width:85px` `-height:53px` `+display:none`。

**推送清单（2 个文件）**：`assets/customstyle.css` + `assets/customstyle.scss`
（`--only` 逐个列出 + `--nodelete` + `--allow-live`）。`main.js` 本轮没改，未推。

**回读验证**：

1. **CLI 拉回**：两个文件逐字节与本地相同。⚠ 另有 `templates/index.json` 变化 ——
   **不是本次推送造成的**（清单里没有 templates），是对方在后台配 usp 区块的 settings，
   推送前的对比里就已经在改这批文件了。
2. **CDN**：裸路径 `…/assets/customstyle.css` 一开始仍返回旧版（208144 字节）——
   **是边缘缓存滞后，不是没推上去**。带随机查询参数取回即为新版：214796 字节、
   build `20260904-r66`、压缩形式 `gb-rv-panel__video svg{display:none}` 1 处。
3. **线上浏览器实测**（首页）：`.gb-rv-panel__video` 内 svg **1 个**（非空断言），
   `display: none`、盒宽 `0` ✅。

⚠ **顺带修正一条对 CDN 滞后的理解**：页面里引用的样式表 URL 是
`…/customstyle.css?v=4420320884865616021788508178` —— **Shopify 的 `asset_url` 自带指纹**，
所以裸路径的边缘缓存滞后**不影响用户实际拿到的版本**。
以后验证「线上有没有生效」应当以**浏览器里页面实际加载的那个 URL** 为准，
拿裸路径 curl 出来的旧内容会误判成「没推上去」。

**基线滚动**：`baseline-pre-r66`（推送前）/ `baseline-dev-live`（当前线上）。

### 顺带发现 / 未修

- **`.gb-rv-panel__video` 的 `@include hover { color: $c-green }` 现在没有视觉效果了**。
  那个 hover 是给 svg 的 `currentColor` 用的，svg 一隐藏就没有承载者了。
  规则留着无害（第五十轮需求方点名加的），**没删**，但下轮如果看到它「不生效」，
  这就是原因，不是 bug。
- **第六十二轮的 `.gb-rv-modal.has-video/.has-embed .gb-rv-panel__glyph { display: none }`
  现在是冗余的**（svg 已无条件隐藏）。它是当时的既有设计，且真接上视频后仍是正确的语义，
  **没删**。
- ⚠ **如果本意是「只在有视频时隐藏、没视频时仍显示 play 图标」**，把这条规则包进
  `.gb-rv-modal.has-video, .gb-rv-modal.has-embed` 里即可，一处回退。
  现在的写法是**无条件隐藏**，所以没有视频的 reel 点开是纯灰底空弹窗。

## 第六十五轮（2026-09-04）— PDP 订阅模块（`$build` = `20260904-r65`）

需求：「之前 pdp 没有做订阅相关的东西（Autoship and Save 以及下面的模块），现在需要补上」
+「加上 `Delivers every:` 的点击交互效果」。

⚠ **这一轮推翻了既有的实现边界。** `docs/PROJECT-STATUS.md`「实现边界：Shopify app 生成的
内容不做」把 PDP 订阅选购列为「由订阅 app 渲染，前端不做」，第一轮只留了占位槽
`data-app="subscription"`，第二十二轮把那个虚线占位框也删了。需求方本轮明确要求补上，
所以**视觉与交互都做，价格/折扣/档位仍归 app**。边界表已更新。

### 数据来源

桌面 `I324:52733;316:18227`（401 宽）/ 手机 `I324:53797;191:2419`（350 宽），
两块稿的节点数据全量落盘，**没有一个数取自截图**。三处只有节点数据才看得出来的：

| 项 | 节点字段 | 若照截图做会怎样 |
|---|---|---|
| `$79.99` 是**删除线** | `textDecoration: STRIKETHROUGH` | 小字灰色，截图上像普通副标 |
| banner **全大写** | `textCase: UPPER`（`characters` 本身是混合大小写 `MOST POPULAR: get 49% off`） | 照 `characters` 写就是小写，**第一版就漏了，靠对稿图才发现** |
| 卡片描边**画在盒内** | `strokeAlign: INSIDE`（bbox == renderBounds） | 用 `border` 会让卡片高 336/306，稿是 334/304 |

第三条决定了写法：`.gb-sub__plan` 用 `box-shadow: inset 0 0 0 1px`，**不是 `border`**。
border 除了撑高 2px，还会把顶部 banner 往里推 1px，而稿里 banner 是齐着卡片边的
（Most popular 334 = Banner 36 + option 298，没有给边框留位置）。

### 结构

```
.gb-sub                       gap 20（= 稿 Subscription frame）
├ .gb-sub__heading            "Autoship and Save" 16/500
├ .gb-sub__plans              gap 16
│ ├ .gb-sub__plan--sub        radius 16/8，inset 1px 描边
│ │ ├ .gb-sub__banner         绿底 lime 字，uppercase
│ │ └ .gb-sub__panel          lime-150 底，pad 20/16，gap 16
│ │   ├ label.gb-sub__pick    radio + 名称/价格/份数/日均
│ │   ├ .gb-sub__works        "How subscription works:" + 三条对勾
│ │   └ .gb-sub__every        "Delivers every:" + 下拉
│ └ label.gb-sub__plan--once  一次性档，同一套 radio
└ .gb-product__cta            "Start Now"
```

⚠ **CTA 移进了 `.gb-sub` 里**。稿里 Start Now 就是 Subscription frame 的第三个孩子，
而 `Product Details` 的 gap 24 正好等于现有 `.gb-product__info` 的 gap —— 结构对上了，
`.gb-product__cta` 的样式不依赖父级，移动后 narrow 的 `max-width:520 + margin-inline:auto`
照常居中。

### 交互

- **`Delivers every:` 下拉**复用 `main.js` 的 `selectBox` 默认变体：HTML 里只是
  `<select data-select>`，JS 自动换成 button + ul，箭头能转、能键盘操作、原生 select 同步提交。
  稿的盒子比表单字段矮（40 vs 44），所以 `.gb-sub__every .gb-select__button` 就地覆盖
  高度/圆角/边框色/阴影 —— 0-2-0 压过 `.gb-field__input` 的 0-1-0。
- **单选没有写 JS**。`:has(.gb-sub__radio:checked)::before` 纯 CSS 就能画选中态，
  两张卡本身都是 `<label>`，点整块即选中。第一版 HTML 里写了个 `is-selected` 类，
  没有任何东西维护它 —— **死类会误导下一轮**，已删。
- radio 走 `.gb-form__check` 同一路子（原生控件 visually-hidden，圆点画在 label 的
  `::before`）：选中时底色填绿，再用**卡片自己的底色**做 3.5px inset 环，把稿的 11px 芯
  从 18px 内容区里切出来 —— 稿里 Checkbox 的 fill 正是卡片底色 `#E7F8D0`，印证了这个画法。

### 文件清单

```
改  pdp.html                  订阅模块 HTML（替换掉 app 占位注释，CTA 移入）
改  assets/customstyle.scss   .gb-sub 全套 + $c-gray-350（#b3b3b3，稿的下拉边框色）
                              + $build → 20260904-r65
改  assets/customstyle.css    编译产物（双写）
改  *.html                    129 处 ?v= r64 → r65
新  tools/r65node.py          通用节点 dump（几何/样式/填充/描边/特效），可查任意 board
新  tools/r65check.py         122 条：逐项比对两块稿的字号/行高/字距/间距/颜色/高度
新  tools/r65interact.py      36 条：真点击驱动的下拉与单选行为
```

### 判据

- `tools/r65check.py` **122 ok / 0 red** — 20 个选择器 × 2 档的 computed 值直接对节点数据，
  外加 banner 36/28、下拉 40、一次性卡 90/76、popular 卡 334/304 四个盒高。
- `tools/r65interact.py` **36 ok / 0 red** — 点开列表 → 断言 `is-open`/`visibility`/
  `aria-expanded`/箭头 transform 变化 → 选第 4 项 → 断言值与**原生 select 同步**、列表收起 →
  断言**用下拉不会改动套餐选择** → 点一次性卡 → 断言两个圆点的填充互斥 → 点回订阅行。
- **活性自检**：把 `inset` 描边改回 `border` → **8 red**，转红的正是四个盒高与描边写法两条。
- **视觉**：`figma/screenshots/` 的两张整页稿按节点坐标裁出订阅区，与 DPR2 元素截图并排。
  桌面 402×564 vs 稿 401×564、手机 350×513 vs 稿 350×512。
  banner 大小写就是这一步看出来的 —— **122 条 computed 判据当时全绿，因为我根本没想到去断言
  `text-transform`**。补进判据后才有覆盖。

**回归**（全部 0 red）：

```
rwd.py      全绿      assetpath.py  GREEN
r58    44   r59    96   r60   242   r61   151
r62   133   r63   158   r64  1744
r65   122   r65interact 36            合计 2726 条
```

### ⚠ 交付前必须替换的占位内容（本轮新增）

| 内容 | 现值 | 说明 |
|---|---|---|
| 订阅价 / 原价 / 日均 | `$40.40` `$79.99` `$1.46/day` | 稿上的占位数字，须由订阅 app 输出 |
| 一次性价 / 原价 / 日均 | `$54.40` `$79.99` `$1.94/day` | 同上 |
| 折扣幅度 | `MOST POPULAR: get 49% off` | 同上 |
| 配送档位 | `2 / 4 / 6 / 8 Weeks` | **稿上只有 `4 Weeks` 一个值**。第五十九轮需求方对 cart 的同类下拉裁决过「补成常见订阅档位」，这里沿用同一套，见待决 BD |

### 推送（2026-09-04）— r64 + r65 一并推上 live，并修好线上被回退的 JS

需求方指令：「关于上述的样式传到 live 上去」+「还有相关 js」。

**推送前取证**：线上 `assets/main.js` 与本地整份不同（65493 vs 70995 字节）。
逐一比对历史快照后确认它**逐字节等于我们自己的 `baseline-r61`** —— 是我们的旧版本被推回去了，
不是别人写的新代码（缺 `playVideo` / `data-video` / `wouldOverflow` 等第五十九～六十二轮的功能）。
**所以推本地新版是恢复 + 更新，不覆盖任何人的新工作。**

**顺带发现 `assets/bear-icon.png` / `.webp` 在线上缺失**，而 `customstyle.css` 里
`url("bear-icon.webp?v=…")` 引用它们 —— 不补就是静默 404（正是第六十一轮修过的病）。
它们是样式的直接依赖，一并推。css 里所有 `url()` 目标都扫过，其余 10 个字体都在。

**推送清单（5 个文件，`--only` 逐个列出 + `--nodelete` + `--allow-live`）**：

```
assets/customstyle.css     244540 → 257296   (r58 → r65)
assets/customstyle.scss    329614 → 348003
assets/main.js              65493 →  70995   (r61 版 → r65)
assets/bear-icon.png       新增（线上缺失）
assets/bear-icon.webp      新增（线上缺失）
```

推送前 `diff -rq` 确认推送源与线上的差异**恰好是这 5 个**，无夹带。

**回读验证（四道）**：

1. **CLI 拉回**：5 个文件逐字节与本地相同，除它们之外**零误伤**，文件数 580 → 582。
2. **CDN**：build token = `20260904-r65`；`gb-sub__plan` 11 处 / `gm-halo-up` 2 处 /
   `gb-dosed__inner>*` 1 处 / `grid-auto-rows:1fr` 2 处；`main.js` 的 `playVideo`、
   `wouldOverflow` 各 2 处；`bear-icon.webp` 200。**这次 CDN 没有滞后。**
3. **`r64check.py --live` 2056 ok / 0 red**（比本地多的 312 条即 live 那一遍）。
   ⚠ 该判据在元素缺失时会静默跳过，所以另跑了**锚点存活检查**：
   `gb-dosed__inner` 1 / `gb-dosed__block` 2 / `gb-faq__item` 6·4·10 /
   `gb-science-card` 3·6 / `gb-highlight-card` 3 —— 元素都在，0 red 不是空转。
4. **逐条需求的线上实测**：

| 需求 | 改前线上 | 改后线上 |
|---|---|---|
| 3 FAQ 行距 | 6 行 `padding-bottom` **全 0px** | `[0, 16, 16, 16, 16, 0]` ✅ |
| 3 分隔线 | 每行都丢 `border-top` | 除首行外都是 1px ✅ |
| 4 `.gb-dosed__block` | 391.8（媒体图 138） | **1250**（媒体图 598），与静态站一致 ✅ |
| 2 卡片等高 | — | science `[384.3×3]` / highlight `[457.7×3]` ✅ |
| — bear-icon | 404 | 背景指向 CDN 的 `assets/bear-icon` ✅ |

**⚠ 线上结构已被对方重构**：`div.shopify-block` 现在**全站 0 处**（blocks 搬进了 sections）。
第六十四轮那三处「锚到列表直接子元素」的修复因此从"必需"变成"防御性" —— 新结构下与原写法等价，
**不要因为「包裹层没了」就改回 `:first-child` / `:last-child`**，下次再有人用 block 就又会坏。

**⚠ 订阅模块（r65）的样式推上去了，但线上不会显示** —— 线上 PDP 没有 `.gb-sub` 的 liquid
结构（实测 `.gb-sub` 0 处）。需要 liquid 那边照 `pdp.html` 加 HTML，
交接见 `docs/LIQUID-TODO-subscription.md`。

**基线滚动**：`baseline-pre-r65`（推送前线上，r58）/ `baseline-dev-live`（当前线上，r65）。


### 顺带发现 / 未修

- **稿里 `Subscribe & Save` 的份数说明与 `One Time Purchase` 一模一样，都是
  `28 Packs delivered once`**。订阅档写 "delivered once"（只送一次）讲不通，
  两块稿都是这样，不是导出问题。**按铁律 3 照抄了稿，没有自己改写**，需设计方裁决 → 待决 BF。
- **一次性档没有 `MOST POPULAR` 之外的任何折扣说明**，但它也有划线原价 `$79.99` 和
  `$54.40` 的现价 —— 稿如此，未加旁注。
- **`Frame 992437`（Product Details 的第三个孩子）在稿里是 radius 16 + `#E7F8D0` 底的盒子**，
  对应现有 `.gb-product__guarantee-note`，实现一致，本轮核对时顺带确认，无需改。
- 手机稿 `$40.40` 与 `$79.99` 之间的视觉间隙看起来比 `itemSpacing: 2` 宽一点点（约 2px），
  疑似 Figma 文本框的 trailing space（见 [[figma-centred-text-counts-trailing-space]]）。
  **按节点数据取 2，没有目测调整。**

## 第六十四轮（2026-09-04）— 任务文档 5 条 + 三处 Shopify 包裹层结构病（`$build` = `20260904-r64`）

需求（对话给出，5 条）：

1. `.gb-stat` 的第一个 `.gb-stat__value` 出现之后 `.gb-ink-halo` 才出现，希望与 `.gb-line-mask` 同步
2. `.gb-science-card` / `.gb-highlight-card` `height: 100%`
3. `.gb-faq__row` `padding-bottom: 16px`
4. `.gb-dosed__inner` 线上与静态站不一致，查原因；若是结构问题，以线上结构为准改样式还原静态站效果
5. 占位图容器只有灰底，内部要给 `img` / `video` 加 100% + `object-fit: cover`

### 贯穿本轮的根因：Shopify 给每个 block 套一层 `div.shopify-block`

线上（storefront password `1234`，本轮首次拿到）实测，三处独立需求是同一个病：
`.gb-dosed__block` / `.gb-faq__item` / `.gb-product__acc-item` 在线上各自被包进一层
**裸 `div.shopify-block`**，于是

- `:first-child` / `:last-child` 判的是**那层包裹**，每个 item 都同时是首也是末；
- `width: 100%` / `height: 100%` 的百分比参照的是**包裹层**，不是原来的容器。

`tools/r64wrap.py` 扫了 8 个线上页面，16 处选择器/页面对失配，全部集中在这两族选择器上。

| 症状 | 实测 |
|---|---|
| `.gb-dosed__block` 塌宽 | 1440 档 **391.8** vs 静态站 **1250**；媒体图 138 vs 598。`align-items:center` 让包裹层 shrink-to-fit，块的 `width:100%` 于是参照塌掉的盒子 |
| FAQ 行距全没了 | `.gb-faq__item:last-child{--acc-gap:0}` 命中**每一个** item → 线上 6 行的 `padding-bottom` 全是 **0px**（静态站 24px） |
| FAQ 手机端分隔线全没了 | `.gb-faq__item:first-child .gb-faq__row{border-top:0}` 同理命中每一行 |

⚠ `.gb-product__acc-row` 的注释里已经记过一次同形的坑（"rows now wrapped in
.gb-product__acc-item → first child of EVERY item"）。**这是第二次，包裹层又多了一层。**
以后写结构选择器一律锚在**列表容器的直接子元素**上，别锚在 item 上。

### 改了什么

```scss
// 位置判定锚到列表的直接子元素，穿透任意深度的包裹层
.gb-faq__list > :last-child,
.gb-faq-image__list > :last-child,
.gb-product__accordion > :last-child { --acc-gap: 0px; }        // was .gb-faq__item:last-child

.gb-faq--plain .gb-faq__list > :first-child .gb-faq__row { … }  // 三处 :first-child 同办法
.gb-dosed__inner > * { width: 100%; }                            // 抵消 align-items:center 的 shrink
```

- **第 1 条**：`.gb-ink-halo` 改走新的 `gm-halo-up`，与 `.gb-line-mask__inner` **同起点、同时长、同曲线**
  （`1.4s var(--e-power4-out)`，delay 由 `base*150ms + 1.05s` 改为 `base*150ms`）。
  halo 是绝对定位副本、进不了遮罩，所以给它自己的窗口：`clip-path` 的 bottom 从
  `100%` 走到 `-20px`，与位移同一条插值 —— 等价于一个**停在文字终位的窗口**，
  正是 `.gb-line-mask` 的 `overflow` 对真实文字做的事。
  收尾 `-20px` 而不是 0，是因为描边是 15px 的 `text-shadow`，窗口齐平行盒会削掉它。
- **第 2 条**：两个卡片加 `height: 100%`。当前线上这两组**没有**包裹层，所以视觉零变化；
  加了之后即使将来做成独立 block 也不会塌（判据里用注入包裹层的方式验过）。
- **第 3 条**：`.gb-faq__list` 的 `--acc-gap` 24 → 16。⚠ 改的是变量不是 `padding-bottom`：
  面板尾部读同一个变量，写死属性会让两者脱钩。`.gb-faq-image__list` 保持自己的 16/24 斜坡。
- **第 5 条**：9 个占位容器补 `img, video, picture { @include cover-img; }`。
  其中 4 个（`.gb-acc-body__media` / `.gb-product__thumb` / `.gb-product__image` /
  `.gb-promo-card__media`）有圆角却没有 `overflow: hidden`，一并补上 —— 不补的话图片会顶掉圆角。

### 文件清单

```
改  assets/customstyle.scss   6 组改动 + $build → 20260904-r64
改  assets/customstyle.css    编译产物（双写）
改  *.html                    129 处 ?v= token r63 → r64（12 个页面）
新  tools/r64check.py         本轮判据，1744 条
新  tools/r64wrap.py          扫线上 8 页，找被 shopify-block 打断的选择器
新  tools/r64dosed.py         dosed 塌宽的线上/静态站几何对比
新  tools/r64probe.py         卡片高度与 faq padding 的线上基线
改  tools/r63check.py         修假阳性（见下）
```

### 判据

`tools/r64check.py` **1744 ok / 0 red**。它跑三遍：
`plain`（原样）/ `wrapped`（**JS 注入 shopify-block 包裹，在本地复现线上 DOM**）/ `live`（`--live`）。
wrapped 这一遍是本轮的核心 —— 没有它，所有修复都只能推上线才知道对不对。

**活性自检**（逐项反向改回产物，判据必须转红）：

| 项 | 转红数 |
|---|---|
| A `.gb-dosed__inner > *` → `width:auto` | 11 |
| B `--acc-gap` 锚点改回 `.gb-faq__item:last-child` | 132 |
| D `--acc-gap` 16 → 24 | 184 |
| E 两个 `height: 100%` 删掉 | 33 |
| F halo 改回 `gm-fade-in` | 144 |
| 第 5 条 `object-fit: cover` → `fill` | 276 |

⚠ **E 项第一次自检是 0 red —— 判据当时漏了这两个网格**（`WRAP` 的注入清单里没有
`.gb-science__cards > *` / `.gb-nutrition__cards > *`）。补进去后才转红 33。
**活性自检抓到的是判据的洞，不是代码的洞**；没跑这一步就会把"冗余改动"当成"已验证"。

**回归**：`r58` 44 / `r59` 96 / `r60` 242 / `r61` 151 / `r62` 133 / `r63` 158、
`assetpath` GREEN、`rwd.py` 全绿，均 0 red。

`tools/r63check.py` 修了一处假阳性：它用 `findall(r"grid-auto-rows:\s*1fr")` 数 scss 应为 2 处，
而本轮在 `.gb-science-card` 的注释里写了这个词 → 数成 3 → 报红。改成先剥 `//` 注释再数；
剥完仍能抓真缺失（把一处规则改成 `auto`，照样 1 red）。

### 推送（2026-09-04）⚠ 推上去了，但随即被第三方覆盖

推送本身成功：`--only assets/customstyle.css --only assets/customstyle.scss --nodelete --allow-live`
→ `The theme 'Dev' (#180348977399) was pushed successfully.`

**推送前**三方对比干净：线上 596 文件 / 120 blocks / css 是 r63，
唯一的他方改动是 `sections/gb-reviews.liquid`（他们按 `docs/LIQUID-TODO-reels.md`
把 `data-video-url` 改成了 `data-video`，还改用了 Shopify 的 video 对象 —— TODO 第 2 条已完成，
第 1 条 `data-modal-media` 仍未做），与推送清单不冲突。
差异核对：线上→本地 css diff 共 128 行，剔除 build token 后 98 行，**逐行都是本轮六项改动，无一行多余**。

**推送后回读，线上变成了另一个版本**：

| | 文件数 | blocks | `assets/customstyle.css` | `assets/main.js` |
|---|---|---|---|---|
| 推送前（我拉的） | 596 | 120 | `20260903-r63` 249137B | `5f89a00b` |
| 我推的 | — | — | `20260904-r64` 251156B | 未推 |
| 推送后（回读） | **571** | **96** | **`20260831-r58`** 244540B | **`c9133d61`** |

- 24 个 `blocks/gb-*.liquid` 与 `sections/gb-page.liquid` 不在了；
  线上 how-gumi-works 的 `gb-dosed` 由 20 处变成 **0 处**，`shopify-block` 也变成 0 处。
- `assets/main.js` 变了 —— **本轮从未推过它**，本地/基线/推送前三者的 md5 都是 `5f89a00b`。
- `config` 之外还有 `sections/footer-group.json` 变化。

**判断**：这不是本次推送造成的，理由是 ① 只推了 2 个文件且带 `--nodelete`；
② 线上现在的 css **不是我推的内容**（是 r58），说明我推之后另有写入；
③ `main.js` 这个我从未碰过的文件也变了；④ 被删的 blocks 与推送清单毫无关系。
**确定性边界**：能确认"线上当前内容不是我推的、且含我从未推过的文件的改动"；
不能从客户端证明对方的具体操作（Shopify 无法从 CLI 查文件级操作日志）。

⚠ **2026-09-04 第六十五轮推送时更正**：上面说的「24 个 blocks 被删」**不准确** ——
它们是被**搬进了 `sections/`**（blocks 120→95、sections 49→63），是一次
block → section 的重构，不是删除。当时的 `diff -rq` 输出被 `head -15` 截断，
只看到 `Only in baseline/blocks:` 那半边，漏了 `Only in remote/sections:` 那半边。
**`assets/customstyle.css`（r63→r58）与 `assets/main.js`（r62 版→r61 版）确实被回退到旧版**，
这一条不变 —— `main.js` 经比对逐字节等于我们自己的 `baseline-r61` 快照。


**当前状态：已停手，等需求方裁决，未做任何恢复动作。** CDN 仍在服务 r63（滞后，实测过 20 分钟）。

恢复源俱全（`/home/ly/project/Gumi-Brand-shopify/`）：

```
baseline-dev-live                          596 文件 120 blocks  r63  ← 完整的推送前线上快照
remote-pre-r64                             596 文件 120 blocks  r64  ← 上面那份 + 本轮两个文件
remote-post-r64                            571 文件  96 blocks  r58  ← 现在的线上
evidence-20260904-0656-live-after-r64-push 571 文件  96 blocks  r58  ← 证据留存
```

### 顺带发现 / 未修

- **`.gb-faq-image__list` 的 narrow 首行规则与 `.gb-faq__row` 里的那条重复**
  （8130 与 7953 同值，后者已覆盖前者）。既有冗余，非本轮引入，没动。
- **`.gb-rv-panel__video` 没有跟着改** —— 它刻意是 `contain` 不是 `cover`（16:9 占位片），
  见「不要报成 bug」1c。第 5 条不适用于它。
- **稿里 `Subscribe & Save` 的说明文案与 `One Time Purchase` 一样是 `28 Packs delivered once`**
  （订阅档写 "delivered once" 讲不通），做 PDP 订阅模块时需要设计方裁决。
- 静态站没有 `.shopify-block`，所以本轮三处结构修复**在静态站上是零视觉变化**；
  它们的价值只在线上，判据靠注入包裹层来覆盖。

## 第六十三轮（2026-09-03）— 两组卡片全档等高（`$build` = `20260903-r63`）

需求：「`gb-science__cards` 内部的 card 的高度应该保持一致，还有 `gb-nutrition__cards` 的 card」。

### 现状（实测，不是目测）

两个容器都是 grid，item 默认 `align-self: stretch`，所以**同一行内**本来就等高 ——
1201 以上三列一行时三张齐平，需求里说的不齐**只发生在换行之后**：

| 视口 | 布局 | 改前高度（index） |
|---|---|---|
| 1440 | 三列一行 | `[384.3, 384.3, 384.3]` ✅ |
| 1199 | 两列两行 | `[379, 379, 355]` ← 第三张自己一行，行高由它自己的内容定 |
| 576 | 两列两行 | `[319.6, 319.6, 271.6]` |
| 575 | 一列三行 | `[410.7, 386.7, 386.7]` ← 每张各自一行，三个高度 |

差值来自文案行数：index 的第一张 science 卡是两行正文，另两张一行；
nutrition 的前两张两行，第三张一行。

### 改了什么

两个容器各加一行：

```scss
grid-auto-rows: 1fr;
```

`stretch` 只拉平**同一行**，要跨行拉平得让所有行本身等高。这里所有行都是隐式行，
而在**高度为 auto 的 grid 容器**里，`fr` 轨道会全部解到最高那一行的内容高
（CSS Grid §12.7，可用空间无限时的 fr 求解），正好就是「所有卡等于最高的那张」。

改后每一档都是三个相同值，且**没有把整体抬高** —— 1199 档从 `[379, 379, 355]`
变成 `[379, 379, 379]`，取的是原本的最大值，不是新算出来的更大值。

### 文件清单

```
改  assets/customstyle.scss   2 处 grid-auto-rows: 1fr（+ $build → 20260903-r63）
改  assets/customstyle.css    编译产物（双写）
新  tools/r63check.py         158 条判据
```

### 判据

`tools/r63check.py`：2 页 × 13 档，断言每个容器内所有直接子元素高度极差 ≤ 0.5px，
外加无横向溢出、scss 与 css 双写各 2 处。**158 ok / 0 red**。

活性自检：把产物里的 `grid-auto-rows:1fr` 改成 `auto` 重跑 → **20 red**，
且转红的**全部**是 1200 及以下的档（1201 以上本来就等高，不该红，也确实没红）。

回归：`rwd.py` 全绿、`assetpath.py` GREEN、`scrolllock` 44、`r58`–`r62` 共 666 条全绿。

### 顺带发现 / 未修

- **拉高出来的空间落在卡片底部**。卡是 `flex-direction: column`，内容顶对齐，
  所以矮卡被拉平后是下方留白（science 卡表现为 bear meter 之下多 24px，
  nutrition 卡是正文之下）。要让内容跟着分布得另加 `justify-content: space-between`
  或给某个子元素 `margin-top: auto` —— 那是版式决策不是还原，**没动**。
- **`.gb-story__inner` 没跟着改**。它是同一套 3→2→1 装置，但注释里写着
  `align-items: start` 是有意的：稿 324:72839 的三张卡就是 538/510/538 不等高。
  需求只点了 science 与 nutrition，按「点名 A 就只改 A」没动。
  ⚠ **这条别当 bug 报**。
- **`.gb-testimonials` 也没动** —— 它是 flex-wrap 不是 grid，同一句改法不适用，
  需求也没点它。
- 单列档（575 以下）等高意味着三张卡都等于最高那张，手机上是纯留白。
  需求原话没有限定断点，所以全档一致；若只想在多列档等高，
  把这行包进 `@media (min-width: 576px)` 即可，一处回退。

### 推送（2026-09-03）

推了**两个文件**到 live 主题 `Dev (#180348977399)`，`--only` 逐个列出 + `--nodelete`：

```
assets/customstyle.css
assets/customstyle.scss
```

`main.js` 本轮没改（线上与本地逐字节相同），未推。HTML 只改了 `?v=` token，
它们不是主题文件，不进推送清单。

**三方对比**（推送前）：线上比上次基线多出别人的 4 个文件
（`blocks/gb-compare.liquid` / `blocks/_gb-compare-row.liquid` / `blocks/gb-faq-image.liquid` /
`sections/gb-expert.liquid`）并改了 4 个 `templates/page.*.json`。
**`assets/` 目录零差异** —— 与本轮推送清单不冲突。

**差异核对**：线上 → 本地的 css diff 共 32 行，剔除 build token 后
**恰好剩两行 `grid-auto-rows: 1fr`**，没有一行多余。

**回读验证**（两道）：

1. CLI 拉回：线上差异恰好是这 2 个文件、与本地逐字节一致；别人的 4 个新文件、
   `sections/gb-reviews.liquid`、`blocks/gb-ingredients.liquid`、5 个 templates json、
   `config/settings_data.json` **全部未动**。文件数 596 → 596。
2. CDN 回读 `https://gumi.com.au/cdn/shop/t/2/assets/customstyle.css`：
   `grid-auto-rows:1fr` 出现 **2 次**，分别落在 `.gb-science__cards{…}` 与
   `.gb-nutrition__cards{…}` 里；build token 是 `20260903-r63`。

⚠ **CDN 上的 css 是 Shopify 压缩过的**（249137 → 208144 字节，9998 行 → 2 行），
所以它与本地的 md5 **本来就不同**，别拿 md5 当判据。
判据要用压缩形式（`grid-auto-rows:1fr` 而不是 `grid-auto-rows: 1fr`），
且 **`grep -c` 在单行文件上恒返回 1**，必须 `grep -o … | wc -l`。

基线滚动：`baseline-r62`（上一版线上）/ `baseline-pre-r63`（本次推送前）/
`baseline-dev-live`（当前线上）。

### ⚠ 店铺开着密码保护

`https://gumi.com.au/` 外部访问返回的是 **`layout/password.liquid` 渲染的密码页**
（section 只有 `template--…__main` 与 `password-footer`，页面里 **0 个 `gb-` 类、
0 处 `customstyle`**）。`Shopify.theme` 确认就是 `Dev #180348977399`、role main，
所以不是主题选错了 —— **是密码墙**。

因此**线上视觉验证做不了**（没有店铺密码），只能验到 CDN 上的 asset 层：
`/cdn/shop/t/2/assets/` 不受密码保护，可以直接 curl。
下次要在浏览器里看线上效果，需要向需求方要 storefront password。

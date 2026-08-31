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

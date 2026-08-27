# 手机端对稿复查：方法与结论（第三十六 / 三十七轮）

> 原为第三十六轮的「还剩 10 页没做」交接单，**第三十七轮已全部做完**
> （`$build` = `20260826-r38`，见 [CHANGELOG.md](CHANGELOG.md) 第三十七轮）。
> 保留这份是因为下面三节仍然要用：**坐标对齐规则**、**判据**、**不要当 bug 修的清单**。

## 一、覆盖情况

| 层面 | 覆盖 | 工具 / 判据 |
|---|---|---|
| 任务文档 21 条 | ✅ 11 页 | 逐条 computed-style 实测，CHANGELOG 第三十六轮 |
| 分段高度对稿 | ✅ 11 页 | `tools/pagefit.py` |
| 硬换行（U+2028）落地 | ✅ 11 页 | `tools/hardbreaks.py`（6 条 MISSING 是图片里的字，误报） |
| 横向溢出 / 文字被裁 | ✅ 12 页 × 14 档 | `tools/rwd.py` |
| 入场动效收尾 | ✅ | `tools/revealcheck.py` |
| 桌面 1440 未退化 | ✅ 11 页 | 矩形多重集 + body 总高，见下方「四」 |
| 既有专项断言 | ✅ | `r31check` 52 条 / `r32check` 42 条 / `r36check` |
| **截图逐区块比对** | ✅ **11 页**（第三十七轮补齐后 10 页） | `tools/pagescan.py` |

**为什么非看图不可**：第三十五轮把四条箭头的元素盒 solve 到与 `absoluteRenderBounds` 一致
（±2px），断言全绿，需求方仍说「箭头没还原」——并排放大一看短了 25~35%，
因为 renderBounds 含 OUTSIDE 描边的斜接外扩，不是画出来的墨迹。第三十七轮又验证了一次：
`.gb-vs__table` 整块缩 15%、`.gb-dosed__title` 的描边被入场动效啃出洞、Reviews 缺整个导航
组件、五颗星是灰的 —— **没有一条是数值断言查得出来的**。

## 二、怎么再跑一遍

```bash
python3 tools/pagescan.py science.html --list --depth 2       # 两侧块各自排序打印
python3 tools/pagescan.py science.html --pairs ".gb-page-hero=192,.gb-compare=3162" --h 900
```

输出在 `tools/shots/`，**左＝设计导出，右＝实现**，中间一条品红分隔线，用 Read 工具直接看图。
`--pairs` 一次启动浏览器跑完一页所有锚点，超过 `--h` 的区块自动切片。

⚠ **不要按文档顺序自动配对**：board 的 children 不按 y 排序（index 上 `Frame 992545@2442`
排在 `Footer@10040` 后面），而且板子里夹着 build 折进上一个 section 的 `Spacer Top`（波浪）。
第一版 `pagescan.py` 就是这么写的，出的图全是错位的。

查稿节点用 `tools/fq.py`：

```bash
python3 tools/fq.py 324-58044 'Compare' --depth=2      # 按名字/文案搜
python3 tools/fq.py 324-58044 '324:58125'              # 按 id（支持实例复合 id 的末段）
```
它打印 box / ink / 旋转矩阵 / 布局属性 / 填充 / 描边 / 字号行高字距 / characterStyleOverrides。
⚠ **描边和可见性都要看**：nutrient 卡的 `50%` 漏描边、PDP 多出的 testimonial，
都是只有翻 `strokes` / `visible` 才发现的。

## 三、坐标对齐（做之前必须先懂这个，否则出的图全是错位的）

设计导出的 y **不等于** 节点 JSON 里的 y。转换规则：

```
截图 y = 节点的 absoluteBoundingBox.y − board 的 absoluteBoundingBox.y
```

多数 board 在页面内容上方还有一条 96px 的假浏览器栏（节点名 `Chrome browser`），
所以对这些 board：`截图 y = 内容帧相对 y + 96`。**逐页不同，别套用**：

| 页 | node 文件 | 内容帧 id | 假浏览器栏 |
|---|---|---|---|
| index | `228-5932_homepage-mobile` | `237:13125` | 有（96） |
| pdp | `324-53792_pdp-mobile` | 无（顶层就是内容） | 有（96） |
| science | `324-58044_science-moble` | `324:58047` | 有（96） |
| reviews | `324-64961_reviews` | `324:64962` | **无** |
| how-gumi-works | `324-70523_how-gumi-works` | `326:89662` | **无** |
| our-story | `324-73673_our-story` | `324:73675` | 有（96） |
| faq | `324-76169_faq` | `326:93671` | 有（96） |
| get-in-touch | `326-80318_get-in-touch` | 无 | 有（96） |
| referral | `326-81540_referral` | `326:90991` | **无** |
| shipping | `326-83129_shipping` | `326:83131` | 有（96） |
| privacy-policy | `326-83399_privacy-policy` | `326:83401` | 有（96） |

⚠ **不要用页面顶部的单一偏移量贯穿全页**。实现与稿会一路漂开（波浪渲染高 12px、订阅框
是空的），到页脚能差几百 px。每个区块**各自重新锚定**：拿该区块在实现里的 y 和在稿里的 y，
分别作为两侧的切片起点。

---

## 四、判据（发现问题后，改完要按这个验）

### 桌面绝不能被动到

需求方明确「只改手机端，如遇到不得不改电脑端结构的地方再改」。这轮的做法：

```bash
python3 tools/cssnap.py <tag>                  # 存快照
```
然后**按矩形多重集 + body 总高比 1440**，不要用 cssnap 自带的路径式 diff ——
只要新增了 DOM 节点（这轮加了 svg / br / 一条 testimonial），后面兄弟的下标就整体错位，
比的是不同元素，会报出几千处假差异。第三十七轮 1440 的结论是 **9 页 0 处矩形消失、body 高不变**；另三页有变化且都可解释
（新增 DOM 的 ink-halo / expert 导航、`<a>` 宽度随文字范围变、PDP 删掉两块板都隐藏的
testimonial 使 body 少 358）。

比对脚本（临时写的，需要时照抄）：

```python
import json, glob, os, collections
A, B = "tools/snap/r38", "tools/snap/<new>"
for fa in sorted(glob.glob(f"{A}/*.1440.json")):
    name = os.path.basename(fa); fb = os.path.join(B, name)
    a, b = json.load(open(fa)), json.load(open(fb))
    ra = collections.Counter(tuple(round(x,1) for x in s["#rect"]) for _, s in a if "#rect" in s)
    rb = collections.Counter(tuple(round(x,1) for x in s["#rect"]) for _, s in b if "#rect" in s)
    ha = next(s["#rect"][3] for p, s in a if p == "/html[0]/body[1]")
    hb = next(s["#rect"][3] for p, s in b if p == "/html[0]/body[1]")
    print(name, "only-in-old:", sum((ra-rb).values()), "bodyh:", ha, "->", hb)
```
基线在 `tools/snap/r37/`（第三十六轮末）与 `tools/snap/r38/`（第三十七轮末），都已存好。

### 断点交接

改了 narrow 的值就要配 tablet 斜坡，否则 767→768 跳变。这轮补了三处才干净。
逐属性对读 767 / 768 的 computed 值，差 >1px 就是断层。
⚠ `fluid()` **只能用于 px**，且起点必须等于 narrow 的值；百分比量不能用它。

### 其他

```bash
python3 tools/rwd.py          # 12 页 × 14 档，约五分钟，必跑
python3 tools/revealcheck.py  # 入场动效收尾，约两分钟
python3 tools/r31check.py     # 52 条
python3 tools/r32check.py     # 42 条（promo 弹窗）
python3 tools/r36check.py     # 第三十五/三十六轮的专项
python3 tools/hardbreaks.py   # U+2028 落地；当前 34 ok / 6 missing
python3 tools/pagefit.py      # 分段高度对稿
```
`hardbreaks` 剩的 6 条 MISSING 全是**成分辐射图 PNG 里的文字**（`Super Mushrooms` /
`Vitamins & Minerals` 等，图片不是 DOM），是误报，别去"修"。

---

## 五、已知差异，**不要当 bug 修**

1. **`.gb-product__app-slot` 高 0**。稿里这里是 `Quantity` 84 + `Subscription` 512 ≈ 596，
   第二十二轮**有意删掉**的订阅 app 占位框，留空槽给 Shopify app。`pagefit` 里 index /
   pdp / our-story / how-gumi-works 约 −400 的缺口都是它。
2. **小波浪在手机端高 12px**（`--sc-band` 的 clamp 下界，第三十五轮遗留）。`.gb-stats`
   多出的 12.1、`.gb-science` padding-top 用 53 而非稿的 64，都挂在这条上。修它等于重设
   波浪的断点体系，会动全站 11 页每个 section 的 padding-bottom 与页面总高。
3. ~~**shipping 表格行高差 8px**~~ —— **第三十七轮已修**。稿里那不是不占高度的 RECTANGLE，
   是每个单元格 `#cccccc 0.5 CENTER` 的描边（外加表头与 2/4/6 行的 `#f3f3f3` 底色）。
   补齐网格并把 padding 从 10 改成 `(44 − 24 − 1) / 2 = 9.5` 后，两张表 377 / 353 对稿 376 / 352。
4. **`.gb-arc-text` 其余几处仍是单 viewBox**：这轮只把 `.gb-footer-cta__arc` 改成了双
   viewBox（11 页）。`.gb-promo-card__arc` / `.gb-dosed__arc` / `.gb-cta-band__arc` 早已是
   双份，`.gb-stats__arc` 两块板共用同一个 278×29 框、只换字号，都是对的。
5. **Reviews 专家卡有竞品名 Grüns、Shipping 全页写美国配送、Privacy 正文是 lorem ipsum**——
   稿自带的占位，上线前必换，不是还原问题。
6. **science 三张卡的 eyebrow 都是 `Easy Habit`**、稿里 stats 四个数字只有 `21` 字距为 0——
   稿自身的 WIP 痕迹，历轮已判定不追。

---

## 六、需要需求方裁决的

⚠ 第三十七轮又新增 11 条（六处桌面/手机文案冲突、两处占位数量冲突、
两处稿自身 WIP 痕迹、一处两端同源偏差），**全部列在 `PROJECT-STATUS.md`
「第三十七轮新增的待决事项」A~D 四组**，这里不重复。以下是第三十六轮留下的：

1. **shipping / privacy-policy 两页的稿里没有 footer CTA 区块**，另外 9 页都有
   （`Footer Section CTA` 1504 / 1564）。实现这两页都挂了 CTA。删一个 CTA 是内容与转化
   决策，**未动**。这两页的页脚本来就有一条挂着的冲突（第十四轮：它们用的是另一版页脚
   组件 16/24/600/ls 0），大概率是同一批稿的模板差异，建议一并问。
2. **小波浪高 12px 要不要修**（见「五」第 2 条）——影响面是全站页高。
3. 第三十五轮遗留的两条仍未定：`images/stats-bear-deco.png` 与中央熊不是同一份导出；
   手机稿的 science lead 比桌面稿多一句免责说明（只有一块稿有的文案，属内容决定）。

---

## 七、这轮踩到的两个坑（已写进 memory，这里留个指针）

- **`absoluteRenderBounds` ≠ 画出来的墨迹**：带 OUTSIDE 描边的矢量组，renderBounds 含
  斜接外扩，比导出墨迹大 9~55% 且逐条不同。判据要在两张 PNG 上量墨迹，且**从图形自己的
  中心做连通域洪泛**（邻近同色元素会伸进任何合理窗口）。
  memory: `figma-renderbounds-inflated-by-outside-stroke`
- **Python 的 `\s` 匹配 U+2028**：拿 U+2028 当 `<br>` 的标记做换行断言，正规化时标记会被
  连同硬换行一起压成空格，**断言恒真报全绿**。换 `\x00`。
  memory: `regex-s-eats-u2028-marker`

---

## 八、工作区状态（第三十七轮末）

- `$build` = `20260826-r38`，全站 33 处 `?v=` 与 `font-check.html` 的 `EXPECT_BUILD` 一致
- `assets/customstyle.css` 是最新编译产物（`npx sass@1.77.8 assets/customstyle.scss
  assets/customstyle.css --no-source-map`，无警告）
- **未 commit、未推送**。上一次提交是 `b397b0d`（r31→r34），第三十四 / 三十五 / 三十六 /
  三十七四轮都还在工作区
- 工具（都不进交付）：`fq.py` / `shotcmp.py` / `pagescan.py`（第三十七轮重写成显式锚点，
  已验证）/ `arrowfit.py` / `pagefit.py` / `hardbreaks.py`
- 基线快照 `tools/snap/r36base`（第三十五轮前）/ `r37`（第三十六轮末）/ `r38`（第三十七轮末）

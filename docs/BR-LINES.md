# 换行补录清单（第一百轮）

> `snippets/gb-lines.liquid` 让 setting 能带换行，但**存量 section 的值不会自动更新** ——
> schema 里的 `default` 只对新添加的 section 生效，已经放在页面上的那些读的是
> `templates/*.json` 里存着的旧值。所以代码推上去之后，还需要有人到后台把下面 18 个
> 字段重新录一遍。

## 怎么输入

| 想要的效果 | 在输入框里怎么打 |
|---|---|
| 只在手机端（≤767）断行 | 直接按回车 |
| 所有宽度都断行 | 该行结尾打 `//` 再回车 |
| 只在桌面端（≥768）断行 | 该行结尾打 `^^` 再回车 |

标记本身不会显示出来。字段类型已从 `text`/`richtext` 改成 `textarea`，所以后台的输入框
现在是多行的、能打回车。

⚠ **原来是 `richtext` 的四个字段**（`gb-footer.tagline` / `gb-hero.lead` /
`gb-nutrition.title` / `gb-stats.title`）存量值还带着 `<p>` 包裹。snippet 认得这种旧值、
会正确拆包，所以**不补录也不会出错**，只是换行仍然缺。补录时把下面的纯文本整段贴进去即可。

## 清单

### 1. `gb-dosed` → **block row > title**

页面：how-gumi-works　　断行：3 处

```
One pouch.
Once a day. ^^
That's
the whole ritual.
```

### 2. `gb-expert` → **title**

页面：reviews　　断行：1 处

```
Recommended
by experts
```

### 3. `gb-footer` → **tagline**

页面：account, faq, get-in-touch, how-gumi-works, index, our-story, pdp, privacy-policy, referral, reviews, science, shipping　　断行：2 处

```
Made with more care than a
vitamin gummy probably needs.
That's on purpose.
```

### 4. `gb-hero` → **block usp > label**

页面：index　　断行：1 处

```
Vitamins//
& Minerals
```

### 5. `gb-hero` → **lead**

页面：index　　断行：1 处

```
Real fruit, real veg, real vitamins,
hiding in a gumi bear.
```

### 6. `gb-nutrition` → **block card > text**

页面：index　　断行：1 处

```
Toss a pack in with your pocket, //
no fridge, no mess, no excuses
```

### 7. `gb-nutrition` → **block card > text**

页面：index　　断行：1 处

```
Because self care shouldn't //
feel like a chore
```

### 8. `gb-nutrition` → **title**

页面：index　　断行：1 处

```
Nutrition that fits
in your pocket
```

### 9. `gb-page-hero` → **title**

页面：faq　　断行：1 处

```
Frequently
asked questions
```

### 10. `gb-page-hero` → **title**

页面：how-gumi-works　　断行：1 处

```
How Gumi
Works
```

### 11. `gb-page-hero` → **title**

页面：our-story　　断行：1 处

```
Our mission is to make daily//
nutrition simple and enjoyable.
```

### 12. `gb-page-hero` → **title**

页面：reviews　　断行：1 处

```
Aussies are obsessed.//
Here's why.
```

### 13. `gb-page-hero` → **title**

页面：science　　断行：2 处

```
Lab-tested.//
Aussie-approved.//
No funny business.
```

### 14. `gb-promo` → **block card > title**

页面：pdp　　断行：1 处

```
Quality you
can trust
```

### 15. `gb-reviews` → **title**

页面：how-gumi-works, index, our-story, pdp　　断行：1 处

```
Aussies are obsessed.//
Here's why.
```

### 16. `gb-science` → **title**

页面：index　　断行：2 处

```
Lab-tested.
Aussie approved.//
No funny business.
```

### 17. `gb-stats` → **block stat > label**

页面：index　　断行：1 处

```
Green
benefits
```

### 18. `gb-stats` → **title**

页面：index　　断行：1 处

```
60+ whole foods.//
No juicer, no fuss.
```

## 代码改完但不在这份清单里的

- **`gb-rich-page`（shipping 页表格里的 `<th>`）** —— 走 richtext 字段，商家可以直接在
  富文本里写 `<br class="gb-br-narrow">`，不需要改代码，也不走 `gb-lines`。
- **`gb-testimonial__lead`（5 处）/ `gb-promo-panel__title`·`lead`（2 处）** —— 这两个模块
  线上根本没有，是**内容缺口不是换行缺口**，别当换行 bug 报。
- **静态站里硬编码的 5 个 `<span>`（“30 Day Money Back Guarantee”）** —— 不是 setting。

## 验收判据

```bash
python3 tools/brdiff.py --password 1234
```

推送前是 **27 lost**。代码推上去后仍是 **27 lost** —— 因为值还没录；
**补录完成后应为 0 lost**。那 7 个 `NO NODE` 不会变，它们不是换行问题。

⚠ 判据跑在 390 宽，只验 `gb-br-narrow` 与裸 `<br>`。`gb-br-wide`（只有 `gb-dosed`
那一处）在 390 是隐藏的，要验它得另跑 768 以上。

## 波浪改造的已定决策（2026-09-08）

- **形状**：用 Gumi 现有的半圆弧（`radial-gradient` 三段 + `linear-gradient`），
  **不**改用 FunkyFood 的平滑曲线 SVG。
- **颜色**：保留现有 **15 组预设**配对，**不**开放任意 color picker。
- 仍未定：新增独立 section，还是替换现有 58 处实例。

---

## 补记（第一一三轮，2026-09-08）：线上有两处**打错了标记**

线上全站只剩 **3 个** `br.gb-br-narrow`（静态站有 37 个 —— 上面 18 个字段仍未补录）。
把这 3 个逐一对了两块板，**两个是错的**：

| 位置 | 桌面稿 | 手机稿 | 线上现状 | 结论 |
|---|---|---|---|---|
| index `gb-stats__title`「60+ whole foods. / No juicer, no fuss.」 | **有 U+2028**（高 128 = 2 行 @lh64） | 有 U+2028（高 72） | `gb-br-narrow`，桌面连排 | ❌ 后台行尾要打 **`//`** |
| our-story `gb-reviews__title`「Aussies are obsessed. / Here's why.」 | **有 U+2028**（高 96 = 2 行 @lh48） | 无，自然折行成 2 行 | `gb-br-narrow`，桌面连排 | ❌ 后台行尾要打 **`//`** |
| reviews `gb-expert__title`「Recommended / by experts」 | 无，一行（高 48） | 有 U+2028（高 72） | `gb-br-narrow` | ✅ **正确，别动** |

⚠ **静态站这两处本来就是裸 `<br>`**（`index.html:329` / `our-story.html:190`），
是后台录入时**按了普通回车**而不是 `//` 回车，才降级成了「只在手机断」。
**不是 CSS 的问题** —— `.gb-br-narrow { @media (min-width: 768px) { display: none } }`
正是它该做的事，reviews 那处就依赖它。

改法（后台 → 对应 section 的 title 字段）：

```
60+ whole foods.//
No juicer, no fuss.
```

```
Aussies are obsessed.//
Here's why.
```

⚠ 这两个值存在 `templates/index.json` / `templates/page.our-story.json` 里，**红线文件，我们不推**，
只能在后台改。

---

## 补记（第一一四轮）：标记写在行中间不生效，会原样印到页面上

`gb-lines.liquid` 只认 **`//<br>` / `^^<br>`**，也就是「标记贴在**行尾**、后面跟一个**真回车**」。
写成 `"Aussies are obsessed. ^^Here's why."`（行中间、没有回车）时：

- `newline_to_br` 找不到换行 → 不产生 `<br>` → `^^<br>` 这条 replace 不匹配
- 结果 **`^^` 原样打到页面上**，且当然也没有换行

线上出现过一次（`/pages/reviews` 的 h1），第一一四轮改回了正确写法。**正确输入**：

```
Aussies are obsessed.^^
Here's why.
```

⚠ 相关字段都是 `textarea`（可以按回车），不是 `text` —— 输入框本身没有限制。

### 另一个坑：遗留 richtext 值里已有的 `<br>` 会被降级

`</` 分支拆 `<p>` 包裹时**不保护里面已有的 `<br>`**，随后统一那道
`replace: '<br>', '<br class="gb-br-narrow">'` 会把它变成「只在手机断」。
`templates/index.json` 的 `<p>60+ whole foods.<br>No juicer, no fuss.</p>` 就是这么坏的
（第一一三轮改成了纯文本 + `//`）。**所有带 `<br>` 的遗留 richtext 值都有这个问题**，
要么逐个补录成纯文本，要么改 snippet 在 `</` 分支里先把 `<br>` 换成 `@@B@@` 保护起来。**snippet 未改。**

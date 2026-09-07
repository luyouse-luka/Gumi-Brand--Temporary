# 交给做 liquid 的人：PDP 订阅模块

静态站第六十五轮做完了 `Autoship and Save` 整块（视觉 + 单选 + 配送周期下拉），
`assets/customstyle.css` / `.scss` / `main.js` **已经推上 live 主题
`Dev (#180348977399)`**（`$build` = `20260904-r65`）。

**但线上 PDP 没有这块的 HTML，所以现在什么都看不到**（实测线上 `.gb-sub` 0 处）。
把下面的结构放进 PDP 模板就能显示，JS 和 CSS 都不用再动。

## 放在哪

`.gb-product__info` 里，**紧跟在 `.gb-product__head` 之后**，
并且**把现有的 `.gb-product__cta`（Start Now）搬进 `.gb-sub` 里当最后一个孩子** ——
设计稿里 Start Now 就属于 Subscription frame，`.gb-product__info` 的 24 gap
正好是稿里 Product Details 的 gap。CTA 的样式不依赖父级，搬过去不用改 CSS。

## 结构（照抄，类名一个都不能改）

```html
<div class="gb-sub" data-sub>
  <p class="gb-sub__heading">Autoship and Save</p>

  <div class="gb-sub__plans">
    <div class="gb-sub__plan gb-sub__plan--sub" data-sub-plan>
      <p class="gb-sub__banner">MOST POPULAR: get 49% off</p>

      <div class="gb-sub__panel">
        <label class="gb-sub__pick">
          <input class="gb-sub__radio" type="radio" name="gb-sub-plan" value="subscribe" checked>
          <span class="gb-sub__info">
            <span class="gb-sub__line">
              <span class="gb-sub__name">Subscribe &amp; Save</span>
              <span class="gb-sub__price"><span class="gb-sub__price-now">$40.40</span><span class="gb-sub__price-was">$79.99</span></span>
            </span>
            <span class="gb-sub__line gb-sub__line--meta">
              <span class="gb-sub__packs">28 Packs delivered once</span>
              <span class="gb-sub__rate">$1.46/day</span>
            </span>
          </span>
        </label>

        <div class="gb-sub__works">
          <p class="gb-sub__works-title">How subscription works:</p>
          <ul class="gb-sub__points">
  <li class="gb-sub__point"><svg class="gb-sub__tick" aria-hidden="true" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M16.6673 5.4165L7.50065 14.5832L3.33398 10.4165" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span>Locked in pricing, every delivery.</span></li>
  <li class="gb-sub__point"><svg class="gb-sub__tick" aria-hidden="true" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M16.6673 5.4165L7.50065 14.5832L3.33398 10.4165" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span>Skip, pause or cancel any time.</span></li>
  <li class="gb-sub__point"><svg class="gb-sub__tick" aria-hidden="true" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M16.6673 5.4165L7.50065 14.5832L3.33398 10.4165" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span>Delivered before you run out.</span></li>
          </ul>
        </div>

        <div class="gb-sub__every">
          <p class="gb-sub__every-label">Delivers every:</p>
          <select class="gb-sub__select" data-select aria-label="Delivery interval">
            <option>2 Weeks</option>
            <option selected>4 Weeks</option>
            <option>6 Weeks</option>
            <option>8 Weeks</option>
          </select>
        </div>
      </div>
    </div>

    <label class="gb-sub__plan gb-sub__plan--once" data-sub-plan>
      <input class="gb-sub__radio" type="radio" name="gb-sub-plan" value="once">
      <span class="gb-sub__info">
        <span class="gb-sub__line">
          <span class="gb-sub__name">One Time Purchase</span>
          <span class="gb-sub__price"><span class="gb-sub__price-now">$54.40</span><span class="gb-sub__price-was">$79.99</span></span>
        </span>
        <span class="gb-sub__line gb-sub__line--meta">
          <span class="gb-sub__packs">28 Packs delivered once</span>
          <span class="gb-sub__rate">$1.94/day</span>
        </span>
      </span>
    </label>
  </div>

  <button class="gb-product__cta" type="button">Start Now</button>
</div>
```

## 契约

| 东西 | 说明 |
|---|---|
| `data-select` | **必须留着**。`main.js` 的 `selectBox` 靠它把原生 `<select>` 换成 button + ul，箭头才会转、才能键盘操作。原生 select 仍在（visually-hidden），照常提交。 |
| `name="gb-sub-plan"` | 两个 radio 必须同名，否则不互斥。 |
| `.gb-sub__radio` | 别删、别换成 `<button>`。选中态是 `:has(.gb-sub__radio:checked)::before` 画的，**没有 JS**。 |
| 两张卡都是 `<label>` | 点整块即选中，靠的就是 label。改成 `<div>` 就点不动了。 |
| `.gb-sub__tick` 的 svg | 与 `.gb-product__feature` 用的是同一个对勾 path。 |

⚠ **`<label>` 里只能放行内元素** —— 现在里面是 `input` + `span`。
换成 `<p>` / `<div>` 会让 HTML 不合法，浏览器会把标签重排，布局直接散。

## 哪些要接后台 / app

前端只把稿上的字摆到位，**下面这些全是占位，必须由订阅 app 或 schema 提供真值**：

| 位置 | 现在写死的 |
|---|---|
| 折扣徽章 | `MOST POPULAR: get 49% off` |
| 订阅价 / 原价 / 日均 | `$40.40` / `$79.99` / `$1.46/day` |
| 一次性价 / 原价 / 日均 | `$54.40` / `$79.99` / `$1.94/day` |
| 份数说明 | `28 Packs delivered once` |
| 配送档位 | `2 / 4 / 6 / 8 Weeks` |

⚠ **配送档位是补的** —— 设计稿里只有 `4 Weeks` 一个值。第五十九轮需求方对购物车的同类下拉
裁决过「补成常见订阅档位」，这里沿用同一套。真实档位由订阅 app 决定。

⚠ **`Subscribe & Save` 和 `One Time Purchase` 的份数说明在稿里是同一句
`28 Packs delivered once`**。订阅档写「只送一次」讲不通，两块稿都这样，
**已登记待决 BF，等设计方给正确文案**，先别自己改。

## 做成 section 还是 block

线上正在把 `blocks/` 往 `sections/` 搬，这块跟着走就行。
⚠ 如果做成 block（每个 block 一层包裹），注意 **`.gb-sub__plans` 的两个 `.gb-sub__plan`
必须是它的直接子元素** —— 中间多一层裸 `div` 不会破坏这块的样式（这里没有用
`:first-child` / `:last-child`），但 gap 16 会作用在包裹层上，视觉一致。

## 验证

静态站的判据可以直接对着线上跑（改 `URL` 常量即可）：

```bash
python3 tools/r65check.py      # 122 条：字号/行高/字距/间距/颜色/四个盒高，对 Figma 节点
python3 tools/r65interact.py   # 36 条：真点击驱动的下拉与单选
```

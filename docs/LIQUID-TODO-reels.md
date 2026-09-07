# 交给做 liquid 的人：reels 视频要跑起来还差三处

静态站（`/home/ly/project/Gumi-Brand/`）第六十二轮已经把 reel 视频做完并推了
`assets/customstyle.css` / `.scss` / `main.js` 到 live 主题 `Dev (#180348977399)`。
**JS 已经在线上了，但主题的 liquid 还差三处 hook，功能因此不工作。**

改完这三处，视频（本地 mp4 与 YouTube／Vimeo 链接）就都能播，JS 不用再动。

## 1. 弹窗容器缺 `data-modal-media`

`sections/gb-reviews.liquid`，`.gb-rv-panel__video` 那一行：

```diff
-      <div class="gb-rv-panel__video"><svg aria-hidden="true" viewBox="0 0 86 54" …></svg></div>
+      <div class="gb-rv-panel__video" data-modal-media>
+        <span class="gb-rv-panel__glyph" aria-hidden="true"><svg aria-hidden="true" viewBox="0 0 86 54" …></svg></span>
+      </div>
```

两件事：**容器加 `data-modal-media`**（`main.js` 靠它找地方建播放器），
**play 图标包一层 `.gb-rv-panel__glyph`**（有媒体时靠这个类把图标盖掉；
现在 svg 裸着，盖不掉会压在视频上）。

⚠ 播放器**不要**写进 liquid。`<video>` 还是 `<iframe>` 由 `main.js` 按链接类型当场建，
写死一个反而会两个都在。

## 2. 属性名要统一成 `data-video`

liquid 现在写的是 `data-video-url`，`main.js` 读的是 `data-video`。**已定以 `data-video` 为准。**

`sections/gb-reviews.liquid`：

```diff
-      <button class="gb-reel swiper-slide" type="button" data-modal="reel-video"{% if b.video_url != blank %} data-video-url="{{ b.video_url }}"{% endif %} …>
+      <button class="gb-reel swiper-slide" type="button" data-modal="reel-video"{% if b.video_url != blank %} data-video="{{ b.video_url }}"{% endif %} …>
```

`blocks/_gb-reel.liquid` 里有同样一行，一起改。

## 3. `video_url` 字段填什么

`data-video` 三种输入都吃，不用分字段：

| 填什么 | JS 建出什么 |
|---|---|
| Shopify Files 的 `.mp4` 直链 | `<video controls>` |
| `youtube.com/watch?v=` / `youtu.be/` / `/shorts/` / `/embed/` / `/live/`（可带 `&t=`） | `<iframe>`（走 `youtube-nocookie.com`） |
| `vimeo.com/123` / `player.vimeo.com/video/123` | `<iframe>` |
| 留空 | 灰底 + play 图标，点开是空弹窗 |

⚠ schema 里 `video_url` 是 `"type": "url"`。Shopify 的 url 类型**不一定接受
YouTube 的 watch 链接**（它主要给站内链接用）。如果后台填不进去，把它改成
`"type": "text"` 即可，JS 那边不挑。

## 现在线上是什么样

只推了 css/js 之后，唯一的可见变化是**弹窗从 304×540 竖版变成了 960×540 横版**
（16:9 是需求方本轮点名要的），里面仍是居中的 play 图标，点卡片没有视频。
这是预期状态，不是坏了。

## 顺带一提，两件待需求方裁决的事

- **16:9 与竖版 reel 冲突**：reel 本该是竖版 9:16（稿里的卡就是 304×540）。16:9 是本轮
  点名要的，占位片也是横版；真实竖版素材进来后 `object-fit: contain` 会左右留大片黑边。
- **promo 弹窗会打断正在播的 reel**：`promoModal.DELAY = 5000`，而 modal 是单例。
  以前弹窗里是静态占位无所谓，现在是视频。

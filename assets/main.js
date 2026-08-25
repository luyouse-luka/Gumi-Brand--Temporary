/* Gumi Brand — site scripts. No dependencies. */
(function () {
  "use strict";

  /* ---------------------------------------------------------------------
   * wowo — scroll reveal, ported 1:1 from the Terra theme (jQuery dropped).
   * Contract: markup carries `class="wowo fadeInUp"`, optional `delay-in-N`
   * (N = 1..20, 0.1s steps). Plays once; both classes are stripped after
   * 1500ms so the element keeps no animation state.
   *
   * The hiding rule is gated on `html.js` (set by an inline <script> in <head>),
   * so a JS file that never loads or throws at parse time leaves content visible.
   * The <noscript> override in each page stays as a second net.
   * ------------------------------------------------------------------- */
  var wowo = {
    run: function () {
      var wTop = window.pageYOffset || document.documentElement.scrollTop;
      var wHeight = window.innerHeight;
      var wBottom = wTop + wHeight;
      var els = document.querySelectorAll(".wowo:not(.animated)");

      for (var i = 0; i < els.length; i++) {
        var el = els[i];
        var rect = el.getBoundingClientRect();
        var meHeight = el.clientHeight;
        var meTop = rect.top + wTop;
        var meBottom = meTop + meHeight;

        if (meTop > wTop - meHeight && meBottom < wBottom + meHeight) {
          this.play(el);
        }
      }
    },

    play: function (el) {
      el.classList.add("animated");
      setTimeout(function () {
        el.classList.remove("wowo", "animated");
      }, 1500);
    },

    init: function () {
      var self = this;
      var ticking = false;

      var onScroll = function () {
        if (ticking) return;
        ticking = true;
        window.requestAnimationFrame(function () {
          try { self.run(); } finally { ticking = false; }
        });
      };

      window.addEventListener("scroll", onScroll, { passive: true });
      window.addEventListener("resize", onScroll, { passive: true });
      self.run(); // catch whatever is above the fold
    }
  };


  /* ---------------------------------------------------------------------
   * Header — dropdown panel on desktop, full-width drawer on mobile.
   * ------------------------------------------------------------------- */
  var header = {
    init: function () {
      var el = document.getElementById("site-header");
      if (!el) return;
      var toggle = el.querySelector(".gb-header__toggle");
      if (!toggle) return;

      var self = this;
      this.el = el;

      toggle.addEventListener("click", function () {
        self.set(!el.classList.contains("is-open"));
      });

      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") self.set(false);
      });

      document.addEventListener("click", function (e) {
        if (el.classList.contains("is-open") && !el.contains(e.target)) self.set(false);
      });

      // header 吸顶后，它到视口顶的距离随滚动变化（公告条滚走就归零），
      // 手机抽屉「从 header 底一直到视口底」这个高度只能实测。CSS 里的
      // calc(100svh - 公告条 - header) 只在页面停在最顶部时才成立。
      window.addEventListener("resize", function () {
        if (el.classList.contains("is-open")) self.measure();
      }, { passive: true });

      var items = el.querySelectorAll("[data-collapsible]");
      for (var i = 0; i < items.length; i++) {
        (function (item) {
          var btn = item.querySelector(".gb-header__link");
          if (!btn) return;
          btn.addEventListener("click", function () {
            var open = item.classList.toggle("is-open");
            btn.setAttribute("aria-expanded", open ? "true" : "false");
          });
        })(items[i]);
      }
    },

    // 抽屉可用高度 = 视口高 − header 底边所在的位置
    measure: function () {
      var bottom = this.el.getBoundingClientRect().bottom;
      this.el.style.setProperty("--drawer-h", (window.innerHeight - bottom) + "px");
    },

    set: function (open) {
      if (open) this.measure();
      this.el.classList.toggle("is-open", open);
      var toggle = this.el.querySelector(".gb-header__toggle");
      if (toggle) toggle.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.classList.toggle("is-menu-open", open);
    }
  };

  /* ---------------------------------------------------------------------
   * bear-meter — renders data-total bears, the first data-fill of them solid.
   * Built in JS so a theme setting can change the number without new markup.
   * ------------------------------------------------------------------- */
  var bearMeter = {
    init: function () {
      var meters = document.querySelectorAll(".gb-bear-meter");
      for (var i = 0; i < meters.length; i++) {
        var el = meters[i];
        if (el.children.length) continue;
        var total = parseInt(el.getAttribute("data-total"), 10) || 100;
        var fill = parseInt(el.getAttribute("data-fill"), 10) || 0;
        var frag = document.createDocumentFragment();
        for (var j = 0; j < total; j++) {
          var s = document.createElement("span");
          s.className = "gb-bear-meter__bear" + (j < fill ? "" : " is-off");
          frag.appendChild(s);
        }
        el.appendChild(frag);
      }
    }
  };

  /* ---------------------------------------------------------------------
   * popText — per-word entrance, transcribed from the reference the design
   * notes name (cravburgers.shop, notes 401:29596 / 216:5903). Their build
   * splits on /(\s+)/, wraps each word in an inline-block span and runs
   * from {opacity 0, scale 0, y random(18,40), rotate random(-16,16)}
   * with duration .72, ease back.out(2.35), stagger .055, once, at top 88%.
   * Timing and easing live in _motion.scss; this only builds the spans and
   * stamps the per-word randoms.
   *
   * Text stays readable if this never runs: the spans that carry opacity 0
   * are the ones this creates.
   * ------------------------------------------------------------------- */
  var POP_START = "-12%";          /* ScrollTrigger "top 88%" */
  var POP_Y_MIN = 18, POP_Y_MAX = 40;
  var POP_ROT = 16;

  var popText = {
    init: function () {
      var els = document.querySelectorAll("[data-pop-text]");
      if (!els.length) return;

      for (var i = 0; i < els.length; i++) {
        // Do NOT drop data-pop-text here: the CSS fallback keys off it
        // ([data-pop-text]:not(.is-split) .gb-pop-word { opacity: 1 }), so removing
        // it would hide the words that split() had already created.
        try { this.split(els[i]); } catch (e) { els[i].setAttribute("data-pop-failed", ""); }
      }

      if (!("IntersectionObserver" in window)) {
        for (var j = 0; j < els.length; j++) els[j].classList.add("is-popped");
        return;
      }

      var io = new IntersectionObserver(function (entries, obs) {
        for (var k = 0; k < entries.length; k++) {
          if (!entries[k].isIntersecting) continue;
          entries[k].target.classList.add("is-popped");
          obs.unobserve(entries[k].target);
        }
      }, { rootMargin: "0px 0px " + POP_START + " 0px", threshold: 0 });

      for (var m = 0; m < els.length; m++) io.observe(els[m]);
    },

    /* Replaces text nodes with .gb-pop-word spans; whitespace stays a real text
       node so line breaking is unchanged, and element children are left be. */
    split: function (root) {
      if (root.classList.contains("is-split")) return;
      /* Per-element override of the reference's 0.055 stagger, in ms */
      var step = parseFloat(root.getAttribute("data-pop-stagger"));
      if (step > 0) root.style.setProperty("--pop-step", step + "ms");
      var n = { i: 0 };
      this.walk(root, n);
      root.classList.add("is-split");
    },

    walk: function (node, n) {
      var kids = Array.prototype.slice.call(node.childNodes);

      for (var i = 0; i < kids.length; i++) {
        var child = kids[i];

        if (child.nodeType === 1) {
          /* [data-pop-atom] pops as ONE piece instead of word by word. The
             stat figures need it: their outline is a text-shadow silhouette,
             and splitting "6g" into two spans would draw two silhouettes and
             put a seam through the number. */
          if (child.hasAttribute && child.hasAttribute("data-pop-atom")) {
            this.stamp(child, n);
            continue;
          }
          this.walk(child, n);
          continue;
        }
        if (child.nodeType !== 3 || !child.nodeValue.trim()) continue;

        var parts = child.nodeValue.split(/(\s+)/);
        var frag = document.createDocumentFragment();

        for (var p = 0; p < parts.length; p++) {
          if (!parts[p]) continue;
          if (/^\s+$/.test(parts[p])) {
            frag.appendChild(document.createTextNode(parts[p]));
            continue;
          }
          var span = document.createElement("span");
          span.className = "gb-pop-word";
          span.textContent = parts[p];
          span.style.setProperty("--pop-i", n.i);
          span.style.setProperty("--pop-y", rand(POP_Y_MIN, POP_Y_MAX).toFixed(1) + "px");
          span.style.setProperty("--pop-r", rand(-POP_ROT, POP_ROT).toFixed(1) + "deg");
          frag.appendChild(span);
          n.i++;
        }

        node.replaceChild(frag, child);
      }
    },

    /* Turns an existing element into a single pop unit. .gb-pop-word is
       inline-block, but every current host is a flex item, where display is
       blockified — so this does not change the layout it is applied to. */
    stamp: function (el, n) {
      el.classList.add("gb-pop-word");
      el.style.setProperty("--pop-i", n.i);
      el.style.setProperty("--pop-y", rand(POP_Y_MIN, POP_Y_MAX).toFixed(1) + "px");
      el.style.setProperty("--pop-r", rand(-POP_ROT, POP_ROT).toFixed(1) + "deg");
      n.i++;
    }
  };

  function rand(min, max) { return min + Math.random() * (max - min); }

  /* ---------------------------------------------------------------------
   * lineReveal — per-line entrance for running copy, the other half of the
   * cravburgers.shop reference (notes 401:29596 / 216:5903). popText above is
   * the word-scatter pop, reserved for the STATISTICS numbers; this is their
   * GSAP SplitText {type:"lines", mask:"lines"} used everywhere else: each
   * visual line gets its own overflow:hidden mask and slides up inside it
   * (y:100%→0%, once revealed the mask never plays again). Timing lives in
   * customstyle.scss; this only measures lines and builds the mask spans.
   *
   * Text stays readable if this never runs: [data-line-reveal] falls back to
   * opacity:1 in CSS when .is-split never gets added.
   * ------------------------------------------------------------------- */
  var LINE_ROOT_MARGIN = "0px 0px -5% 0px"; /* ScrollTrigger "top 95%" */
  var LINE_RESIZE_DEBOUNCE = 200;

  var lineReveal = {
    init: function () {
      var els = document.querySelectorAll("[data-line-reveal]");
      if (!els.length) return;
      this.els = els;
      var self = this;

      /* Splitting into lines measures offsetTop, which depends on the real
         brand font's metrics. Running before the webfont has swapped in
         measures the fallback font instead and bakes in the wrong wrap
         points -- above-the-fold text (the hero lead) is revealed almost
         immediately, so it never gets a later resize to self-correct. Wait
         for the swap, but never block longer than one frame's worth of
         patience: a font that never resolves must not leave the page unsplit.

         而 500ms 这个兜底超时在慢网络上是**一定**会先跑的，所以光有它不够：
         第二十八轮实测（字体响应压后 1500ms）里 .gb-hero__lead / .gb-science__lead /
         .gb-product__lead 三段都是按兜底字体的换行点分了 2 行，真字体一到位每行
         变宽、每个遮罩里挤进两行，元素高度从 60 涨到 90 —— 一次凭空的 30px 位移，
         而且遮罩数还停在 2，动画会两行一起滑。所以字体到位后必须**重新分行**一次。
         groupLines 本来就是幂等的（先把旧遮罩拆回去再按当前换行点重建），已经
         揭示过的段落会走 is-settled 直接落终态，不会把入场动画重播一遍。 */
      var started = false;
      var refined = false;

      var start = function () {
        if (started) return;
        started = true;
        self.runInitialSplit();
      };

      var refine = function () {
        if (refined) return;
        refined = true;
        if (!started) { start(); return; }   // 字体够快，第一次就是拿真字体量的
        for (var n = 0; n < self.els.length; n++) {
          try { self.split(self.els[n]); } catch (e) { /* leave last-good state */ }
        }
      };

      if (document.fonts && document.fonts.ready && typeof document.fonts.ready.then === "function") {
        document.fonts.ready.then(refine, refine);
        window.setTimeout(start, 500);
      } else {
        start();
      }

      /* Wrap points move with viewport width, so a resize has to re-group
         words into fresh lines. split() itself skips already-revealed
         elements straight to the settled end state -- see groupLines(). */
      var timer;
      window.addEventListener("resize", function () {
        window.clearTimeout(timer);
        timer = window.setTimeout(function () {
          for (var n = 0; n < self.els.length; n++) {
            try { self.split(self.els[n]); } catch (e) { /* leave last-good state */ }
          }
        }, LINE_RESIZE_DEBOUNCE);
      });
    },

    runInitialSplit: function () {
      var els = this.els;
      for (var i = 0; i < els.length; i++) {
        try { this.split(els[i]); } catch (e) { els[i].setAttribute("data-line-failed", ""); }
      }

      if (!("IntersectionObserver" in window)) {
        for (var j = 0; j < els.length; j++) els[j].classList.add("is-revealed");
        return;
      }

      var io = new IntersectionObserver(function (entries, obs) {
        for (var k = 0; k < entries.length; k++) {
          if (!entries[k].isIntersecting) continue;
          entries[k].target.classList.add("is-revealed");
          obs.unobserve(entries[k].target);
        }
      }, { rootMargin: LINE_ROOT_MARGIN, threshold: 0 });

      for (var m = 0; m < els.length; m++) io.observe(els[m]);
    },

    split: function (root) {
      if (!root.classList.contains("is-word-split")) {
        this.wrapWords(root);
        root.classList.add("is-word-split");
      }
      this.groupLines(root);
      root.classList.add("is-split");
    },

    /* Same discipline as popText.walk: only text nodes become spans,
       whitespace stays a real text node, element children are left alone.
       [data-line-reveal] hosts are plain-copy <p> elements with no nested
       markup, so this only needs to look at root's direct children. */
    wrapWords: function (root) {
      var kids = Array.prototype.slice.call(root.childNodes);
      for (var i = 0; i < kids.length; i++) {
        var child = kids[i];
        if (child.nodeType !== 3 || !child.nodeValue.trim()) continue;
        var parts = child.nodeValue.split(/(\s+)/);
        var frag = document.createDocumentFragment();
        for (var p = 0; p < parts.length; p++) {
          if (!parts[p]) continue;
          if (/^\s+$/.test(parts[p])) { frag.appendChild(document.createTextNode(parts[p])); continue; }
          var span = document.createElement("span");
          span.className = "gb-line-word";
          span.style.display = "inline-block";
          span.textContent = parts[p];
          frag.appendChild(span);
        }
        root.replaceChild(frag, child);
      }
    },

    /* Unwraps any existing .gb-line-mask back to its flat children, measures
       each .gb-line-word's offsetTop to find the current wrap points, then
       re-wraps each run of same-top nodes in a fresh mask. Safe to call
       repeatedly -- every resize does. */
    groupLines: function (root) {
      var wasRevealed = root.classList.contains("is-revealed") || root.classList.contains("is-settled");

      var masks = root.querySelectorAll(".gb-line-mask");
      for (var u = 0; u < masks.length; u++) {
        var mask = masks[u];
        var inner = mask.firstChild;
        while (inner && inner.firstChild) mask.parentNode.insertBefore(inner.firstChild, mask);
        mask.parentNode.removeChild(mask);
      }

      var nodes = Array.prototype.slice.call(root.childNodes);
      var lines = [];
      var current = null;
      var lastTop = null;

      for (var i = 0; i < nodes.length; i++) {
        var node = nodes[i];
        var isWord = node.nodeType === 1 && node.classList.contains("gb-line-word");
        if (!isWord) {
          if (current) current.push(node);
          continue;
        }
        var top = node.offsetTop;
        if (lastTop === null || Math.abs(top - lastTop) > 1) {
          current = [];
          lines.push(current);
          lastTop = top;
        }
        current.push(node);
      }

      for (var l = 0; l < lines.length; l++) {
        var maskEl = document.createElement("span");
        maskEl.className = "gb-line-mask";
        var innerEl = document.createElement("span");
        innerEl.className = "gb-line-mask__inner";
        innerEl.style.setProperty("--line-i", l);
        for (var n = 0; n < lines[l].length; n++) innerEl.appendChild(lines[l][n]);
        maskEl.appendChild(innerEl);
        root.appendChild(maskEl);
      }

      if (wasRevealed) {
        root.classList.remove("is-revealed");
        root.classList.add("is-settled");
      }
    }
  };

  /* ---------------------------------------------------------------------
   * packBand — 营养区那条斜着铺过去的包装袋。
   *
   * 标记里每行只留两个 <picture>（任务文档第 5 条：DOM 里写 21 个同样的
   * <picture> 太呆板），铺满屏幕要几个由这里按当前节距算出来再克隆补齐 ——
   * 跟 .gb-bear-meter 用 JS 生成 100 个小熊是同一个路子。
   *
   * 原来两行写死 10 / 11 个，是照最宽的情况配的：桌面要铺 4385px、手机 2160px，
   * 而视口分别只有 1440 / 390，两端都大幅过量。节距 --pack-w / --pack-gap 都是
   * fluid()，随视口连续变化，个数本来就该跟着算。
   *
   * ⚠ 量宽度只能用 offsetWidth：.gb-pack-band 整条转了 -6.556°，
   *   getBoundingClientRect() 给的是旋转后的外接盒，拿它算节距会偏大
   *   （同一类坑见 memory figma-rotated-frame-bbox-is-not-the-artwork）。
   * ⚠ 两行个数必须一奇一偶：稿里的砖缝错位就是靠行宽差一个节距、
   *   再由 align-items:center 各自居中得来的，两行一样多就对齐了。
   * ------------------------------------------------------------------- */
  var PACK_BAND_TILT = 6.556;   // deg，与 .gb-pack-band 的 rotate 保持一致

  var packBand = {
    init: function () {
      var band = document.querySelector("[data-pack-band]");
      if (!band) return;
      var rows = band.querySelectorAll(".gb-pack-band__row");
      if (!rows.length) return;
      this.rows = rows;

      var self = this;
      this.fill();

      var timer;
      window.addEventListener("resize", function () {
        window.clearTimeout(timer);
        timer = window.setTimeout(function () { self.fill(); }, 200);
      }, { passive: true });
    },

    fill: function () {
      var seed = this.rows[0].firstElementChild;
      if (!seed) return;
      /* ⚠ 量的必须是 <img> 不是 <picture>：站里 picture 一律 display:contents
         （见 helpers 里那条规则），它自己没有盒子，offsetWidth 恒为 0，真正的
         flex 项是里面那个 img。computed width 是求值后的 used value，比
         offsetWidth 多带小数（388.25 vs 388），累到十几个袋子上差得出来。
         也不能去读 --pack-w：自定义属性的 computed 是没求值的 clamp() 串。 */
      var probe = (seed.querySelector && seed.querySelector("img")) || seed;
      var packW = parseFloat(window.getComputedStyle(probe).width) || probe.offsetWidth;
      if (!packW) return;                    // 还没布局出来，等 resize 再来
      var gap = parseFloat(window.getComputedStyle(this.rows[0]).columnGap) || 0;
      var pitch = packW + gap;
      if (pitch <= 0) return;

      // 斜着铺，水平方向要多盖住转过去的那两角；+2 保证两侧一定被裁掉、
      // 不会露出排头排尾（稿里就是被裁的）
      var span = window.innerWidth / Math.cos(PACK_BAND_TILT * Math.PI / 180);
      var base = Math.ceil(span / pitch) + 2;
      /* 第一行钉成偶数，跟原来写死的 10 / 11 相位一致：两行都靠 align-items:center
         居中，偶数行的中线落在两个袋子中间那道缝上、奇数行落在正中那个袋子上，
         错开的正好是半个节距。只保证「一奇一偶」是不够的 —— 若算出 5 / 6，
         错位量虽然还是半个节距，但两行的角色对调了，砖缝跟稿里反过来。 */
      if (base % 2) base++;

      for (var i = 0; i < this.rows.length; i++) this.setCount(this.rows[i], base + i);
    },

    setCount: function (row, n) {
      var seed = row.firstElementChild;
      if (!seed) return;
      while (row.children.length > n) row.removeChild(row.lastElementChild);
      while (row.children.length < n) row.appendChild(seed.cloneNode(true));
    }
  };

  /* ---------------------------------------------------------------------
   * accordion — 同组只开一项（任务文档第 4 条）。
   *
   * 主力是原生的 <details name="…">：同名的一组里，浏览器自己保证只有一项展开，
   * 键盘、a11y 树、无 JS 都不受影响（Chrome 120+ / Safari 17.2+ / Firefox 130+）。
   * 这里只补老浏览器 —— 它们把 name 当无关属性忽略，于是能同时展开好几项。
   *
   * 不做特性检测：支持的浏览器里别的项早已被自己关掉，这段循环等于空转；
   * 而 `'name' in HTMLDetailsElement.prototype` 在部分版本上会误判成支持。
   * ------------------------------------------------------------------- */
  var accordion = {
    init: function () {
      var all = document.querySelectorAll("details[name]");
      for (var i = 0; i < all.length; i++) {
        (function (d) {
          d.addEventListener("toggle", function () {
            if (!d.open) { return; }
            var group = document.querySelectorAll('details[name="' + d.getAttribute("name") + '"]');
            for (var j = 0; j < group.length; j++) {
              if (group[j] !== d && group[j].open) { group[j].open = false; }
            }
          });
        })(all[i]);
      }
    }
  };

  /* ---------------------------------------------------------------------
   * modal — the nutritional label panel (note 401:31227). Opened by any
   * [data-modal="<id>"], closed by [data-modal-close], the overlay or Escape.
   * The element stays in the DOM so the closing fade plays out (round 28
   * dropped the slide-up in favour of a plain cross-fade); visibility is
   * delayed in CSS rather than switched to display: none.
   * ------------------------------------------------------------------- */
  var FOCUSABLE = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';

  var modal = {
    current: null,
    lastFocus: null,

    init: function () {
      var self = this;

      document.addEventListener("click", function (e) {
        var t = e.target;
        if (!t || !t.closest) { return; }
        var open = t.closest("[data-modal]");
        if (open) {
          e.preventDefault();
          self.open(document.getElementById(open.getAttribute("data-modal")));
          return;
        }
        if (t.closest("[data-modal-close]")) self.close();
      });

      document.addEventListener("keydown", function (e) {
        if (!self.current) return;
        if (e.key === "Escape") { self.close(); return; }
        if (e.key === "Tab") self.trap(e);
      });

      this.tabs();
    },

    open: function (el) {
      if (!el || this.current === el) return;
      // Only one at a time: close() tracks a single `current`, so a stacked
      // dialog would be orphaned on screen with its overlay still hit-testable.
      if (this.current) { this.close(); }
      this.lastFocus = document.activeElement;
      this.current = el;
      el.classList.add("is-open");
      el.setAttribute("aria-hidden", "false");
      /* html carries the scroll, body does not: the reset sets overflow-x on
         html, which makes it the scrolling element */
      // Measure the real scrollbar width before locking (it's still on screen
      // here) so the CSS lock can pad the freed space back in and stop the
      // page jumping sideways when the scrollbar disappears.
      var scrollbarW = window.innerWidth - document.documentElement.clientWidth;
      document.documentElement.style.setProperty("--scrollbar-w", scrollbarW + "px");
      document.documentElement.classList.add("is-modal-open");
      document.body.classList.add("is-modal-open");
      // 页面已被锁住，Lenis 再跑就是空转；停掉它弹窗正文才滚得动
      smoothScroll.pause();
      var first = el.querySelector(FOCUSABLE);
      if (first) first.focus();
    },

    close: function () {
      var el = this.current;
      if (!el) return;
      this.current = null;
      el.classList.remove("is-open");
      el.setAttribute("aria-hidden", "true");
      document.documentElement.classList.remove("is-modal-open");
      document.body.classList.remove("is-modal-open");
      smoothScroll.resume();
      if (this.lastFocus) this.lastFocus.focus();
    },

    trap: function (e) {
      var f = this.current.querySelectorAll(FOCUSABLE);
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    },

    tabs: function () {
      var lists = document.querySelectorAll('[role="tablist"]');
      for (var i = 0; i < lists.length; i++) {
        lists[i].addEventListener("click", function (e) {
          var tab = e.target.closest('[role="tab"]');
          if (!tab) return;
          var all = this.querySelectorAll('[role="tab"]');
          for (var j = 0; j < all.length; j++) {
            var on = all[j] === tab;
            all[j].setAttribute("aria-selected", on ? "true" : "false");
            var pane = document.getElementById(all[j].getAttribute("aria-controls"));
            if (pane) pane.hidden = !on;
          }
        });
      }
    }
  };

  /* ---------------------------------------------------------------------
   * promoModal — "Get 20% off your first order" (Figma 285:18988/19373,
   * both mislabelled — see round 26 changelog). Markup only exists on
   * index.html, so "does #promo-modal exist" already scopes this to the
   * homepage; no page-detection needed. Auto-opens once per tab session —
   * the delay and the once-per-session rule are house choices, the design
   * carries no trigger spec at all.
   * ------------------------------------------------------------------- */
  var promoModal = {
    DELAY: 5000,
    SEEN_KEY: "gb-promo-seen",

    init: function () {
      var el = document.getElementById("promo-modal");
      if (!el) return;
      this.bindForm(el);
      this.bindCopy(el);

      var seen;
      try { seen = sessionStorage.getItem(this.SEEN_KEY); } catch (e) { seen = null; }
      if (seen) return;

      var self = this;
      window.setTimeout(function () {
        modal.open(el);
        try { sessionStorage.setItem(self.SEEN_KEY, "1"); } catch (e) {}
      }, this.DELAY);
    },

    bindForm: function (el) {
      var form = el.querySelector("[data-promo-form]");
      if (!form) return;
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        // No app wired up to send this to yet (MVP boundary: email-capture
        // popups like this are normally a Klaviyo/Justuno-style app) — this
        // just plays the design's second state so the interaction is real.
        el.querySelector('[data-promo-panel="email"]').hidden = true;
        var code = el.querySelector('[data-promo-panel="code"]');
        code.hidden = false;
        var first = code.querySelector("button, [href], input, [tabindex]");
        if (first) first.focus();
      });
    },

    bindCopy: function (el) {
      var btn = el.querySelector("[data-promo-copy]");
      var codeEl = el.querySelector("[data-promo-code]");
      if (!btn || !codeEl) return;
      btn.addEventListener("click", function () {
        var text = codeEl.textContent;
        var flash = function () {
          var was = btn.textContent;
          btn.textContent = "Copied!";
          window.setTimeout(function () { btn.textContent = was; }, 2000);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(flash, flash);
          return;
        }
        // Fallback for contexts without the async Clipboard API (older
        // Safari, non-secure origins): a temporary offscreen textarea.
        var ta = document.createElement("textarea");
        ta.value = text;
        ta.style.cssText = "position:fixed;top:-9999px;left:-9999px";
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); } catch (e) {}
        ta.remove();
        flash();
      });
    }
  };

  /* ---------------------------------------------------------------------
   * slider — arrow controls for a horizontal snap track, with an optional
   * endless loop.
   *
   * The track already scrolls and snaps in CSS, so this only adds the arrows
   * and, for [data-slider-loop], the wrap-around; with JS off the strip is
   * still swipeable, just finite and without buttons. One step = one slide
   * plus the gap, read from the DOM rather than hard-coded, so it survives the
   * responsive gap changes.
   *
   *   [data-slider]  wrapper
   *     [data-slider-track]  the scroller
   *     [data-slider-prev] / [data-slider-next]  buttons
   *     [data-slider-loop]   clone the set and wrap around
   *     [data-slider-centre] park a slide's centre on the viewport centre
   *
   * The loop is clone-based rather than transform-based so that native touch
   * scrolling, momentum and snapping all keep working: the set is repeated
   * until there is at least one full set of runway on each side, and once the
   * scroll goes idle the position is shifted by exactly one set width. A whole
   * set is 1640px on the reels row, so a single fling cannot outrun it, and
   * shifting only when idle means the jump never cuts a momentum scroll short.
   * ------------------------------------------------------------------- */
  var slider = {
    init: function () {
      var roots = document.querySelectorAll("[data-slider]");
      for (var i = 0; i < roots.length; i++) { this.bind(roots[i]); }
    },

    bind: function (root) {
      var track = root.querySelector("[data-slider-track]");
      var prev = root.querySelector("[data-slider-prev]");
      var next = root.querySelector("[data-slider-next]");
      if (!track) { return; }

      var loop = root.hasAttribute("data-slider-loop");
      var originals = [];
      var i;
      for (i = 0; i < track.children.length; i++) { originals.push(track.children[i]); }
      var setCount = originals.length;

      var pitch = function () {
        var first = track.firstElementChild;
        if (!first) { return track.clientWidth; }
        var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
        return first.getBoundingClientRect().width + gap;
      };
      var setWidth = function () { return pitch() * setCount; };

      // Enough copies that a full set of runway sits on each side of the
      // viewport: 1.5 sets of travel plus whatever the viewport itself covers.
      var fill = function () {
        if (!loop || !setCount) { return; }
        // A set that measures 0 (images not yet decoded, display:none ancestor)
        // used to fall back to 1px and ask for one clone per viewport pixel --
        // measured at 4281 nodes. Wait for a real measurement instead.
        var w = setWidth();
        if (w <= 1) { return; }
        var need = Math.min(12, Math.ceil(2.5 + track.clientWidth / w));
        var have = Math.round(track.children.length / setCount);
        while (have < need) {
          for (i = 0; i < setCount; i++) {
            var clone = originals[i].cloneNode(true);
            clone.setAttribute("aria-hidden", "true");
            /* aria-hidden with a focusable inside is a trap: the reader skips
               the node but Tab still lands in it. Take the copies out of the
               tab order — the originals are still reachable. */
            if (clone.matches && clone.matches(FOCUSABLE)) { clone.tabIndex = -1; }
            var inner = clone.querySelectorAll ? clone.querySelectorAll(FOCUSABLE) : [];
            for (var c = 0; c < inner.length; c++) { inner[c].tabIndex = -1; }
            track.appendChild(clone);
          }
          have++;
        }
      };

      var jump = function (to) {
        var prevBehavior = track.style.scrollBehavior;
        track.style.scrollBehavior = "auto";
        track.scrollLeft = to;
        track.style.scrollBehavior = prevBehavior;
      };

      // Keep the position inside the second set, so there is always a set of
      // content to scroll into on either side.
      var wrap = function () {
        if (!loop) { return; }
        var w = setWidth();
        if (w <= 0) { return; }
        var s = track.scrollLeft;
        if (s < w * 0.5) { jump(s + w); }
        else if (s > w * 1.5) { jump(s - w); }
      };

      var sync = function () {
        if (loop) { return; }          // no ends to reach
        // 1px of slack: sub-pixel scroll positions would otherwise never
        // satisfy an exact comparison and the end button would stay live.
        var max = track.scrollWidth - track.clientWidth;
        if (prev) { prev.disabled = track.scrollLeft <= 1; }
        if (next) { next.disabled = track.scrollLeft >= max - 1; }
      };

      if (prev) {
        prev.addEventListener("click", function () {
          track.scrollBy({ left: -pitch(), behavior: "smooth" });
        });
      }
      if (next) {
        next.addEventListener("click", function () {
          track.scrollBy({ left: pitch(), behavior: "smooth" });
        });
      }

      track.addEventListener("scroll", function () {
        if (!track._t) {
          track._t = window.requestAnimationFrame(function () {
            track._t = 0;
            sync();
            if (root._onScroll) { root._onScroll(); }
          });
        }
        // Wrap only once the scroll has settled, so a jump can never cut a
        // momentum scroll or a smooth scrollBy short.
        window.clearTimeout(track._idle);
        track._idle = window.setTimeout(wrap, 120);
      }, { passive: true });

      /* Drag to scroll, mouse only. Touch already scrolls this rail natively
         with momentum and snapping; taking over its pointer events would cost
         both. The rail keeps its own scrollLeft, so this is just a nudge —
         release hands straight back to the CSS snap. */
      var drag = null;
      var DRAG_SLOP = 5;      // below this it is a click, not a drag

      track.addEventListener("pointerdown", function (e) {
        track._noClick = false;
        if (e.pointerType !== "mouse" || e.button !== 0) { return; }
        drag = { x: e.clientX, left: track.scrollLeft, moved: 0, held: false };
      });

      track.addEventListener("pointermove", function (e) {
        if (!drag) { return; }
        var dx = e.clientX - drag.x;
        if (Math.abs(dx) > drag.moved) { drag.moved = Math.abs(dx); }
        if (!drag.held && drag.moved > DRAG_SLOP) {
          drag.held = true;
          track.classList.add("is-dragging");
          try { track.setPointerCapture(e.pointerId); } catch (err) {}
        }
        if (drag.held) {
          track.scrollLeft = drag.left - dx;
          e.preventDefault();
        }
      });

      var dragEnd = function (e) {
        if (!drag) { return; }
        var held = drag.held;
        if (held) {
          try { track.releasePointerCapture(e.pointerId); } catch (err) {}
          track.classList.remove("is-dragging");
          /* Swallow the click this drag would otherwise fire: the pointer went
             down on a reel, so letting it through would open the lightbox at
             the end of every drag. */
          track._noClick = true;
        }
        drag = null;
      };
      track.addEventListener("pointerup", dragEnd);
      track.addEventListener("pointercancel", dragEnd);

      track.addEventListener("click", function (e) {
        if (!track._noClick) { return; }
        track._noClick = false;
        e.preventDefault();
        e.stopPropagation();
      }, true);

      // The reels row is full-bleed and wider than the viewport; the design
      // frames it by centring the window on a card's centre (Reels Row
      // x=-88 w=1617 on a 1440 frame — 88px of overhang on each side, which is
      // exactly what "middle card centred" produces at that width). Recompute
      // it rather than hard-coding 88 so the framing survives any viewport.
      var centre = function () {
        if (!root.hasAttribute("data-slider-centre")) { return; }
        var p = pitch();
        var slide = track.firstElementChild;
        if (!p || !slide) { return; }
        var half = slide.getBoundingClientRect().width / 2;
        var target = loop ? setWidth() : (track.scrollWidth - track.clientWidth) / 2;
        var k = Math.round((target + track.clientWidth / 2 - half) / p);
        var to = k * p + half - track.clientWidth / 2;
        var max = track.scrollWidth - track.clientWidth;
        jump(Math.max(0, Math.min(max, to)));
      };

      // Only width matters here. Mobile browsers fire resize when the address
      // bar shows/hides, which changes height alone -- rebuilding on that threw
      // the track back to centre while the user was mid-swipe.
      var lastW = window.innerWidth;
      var relayout = function () { fill(); centre(); sync(); };

      window.addEventListener("resize", function () {
        if (window.innerWidth === lastW) { return; }
        lastW = window.innerWidth;
        relayout();
      }, { passive: true });
      relayout();
      root._sync = sync;
      root._wrap = wrap;
      root._centre = centre;
    }
  };

  /* ---------------------------------------------------------------------
   * gallery — thumbnail rail driving the main stage.
   *
   * 一次只出一张，切换是淡入（任务文档第 3 条）。原来是 scroll-snap 滚动条，
   * 一次甩动能跨好几张、切换是位移。现在 slide 全部叠放，只有 .is-active
   * 那张不透明；索引是这里的一个变量，不再从 scrollLeft 反推。
   *
   * 「每次只能滑动一张」= 一次手势只走 ±1，跟拖了多远无关 —— 拖 40px 和拖
   * 400px 都只翻一张。到头就停，不回绕（这是产品图库不是轮播）。
   *
   *   [data-gallery]        外壳
   *     [data-gallery-thumbs] 缩略图列
   *       [data-gallery-go="N"] 跳到第 N 张
   *     [data-gallery-track]  舞台
   *       [data-gallery-slide]  每一张
   * ------------------------------------------------------------------- */
  var gallery = {
    init: function () {
      var roots = document.querySelectorAll("[data-gallery]");
      for (var i = 0; i < roots.length; i++) { this.bind(roots[i]); }
    },

    bind: function (root) {
      var stage = root.querySelector("[data-gallery-track]");
      var thumbs = root.querySelectorAll("[data-gallery-go]");
      if (!stage || !thumbs.length) { return; }
      var slides = stage.querySelectorAll("[data-gallery-slide]");
      if (!slides.length) { return; }

      var idx = 0;
      for (var k = 0; k < slides.length; k++) {
        if (slides[k].classList.contains("is-active")) { idx = k; }
      }

      var show = function (next) {
        next = Math.max(0, Math.min(slides.length - 1, next));
        if (next === idx) { return; }
        idx = next;
        for (var i = 0; i < slides.length; i++) {
          slides[i].classList.toggle("is-active", i === idx);
        }
        for (var j = 0; j < thumbs.length; j++) {
          var on = j === idx;
          thumbs[j].classList.toggle("is-active", on);
          if (on) { thumbs[j].setAttribute("aria-current", "true"); }
          else { thumbs[j].removeAttribute("aria-current"); }
        }
        // 缩略图列自己也会滚（桌面竖向、窄屏横向），把当前那张带进视野
        if (thumbs[idx] && thumbs[idx].scrollIntoView) {
          try { thumbs[idx].scrollIntoView({ block: "nearest", inline: "nearest" }); } catch (e) {}
        }
      };

      for (var i = 0; i < thumbs.length; i++) {
        (function (btn) {
          btn.addEventListener("click", function () {
            show(parseInt(btn.getAttribute("data-gallery-go"), 10) || 0);
          });
        })(thumbs[i]);
      }

      // 手势：一次只走一张。用 pointer 事件而不是 touch —— 触控板和鼠标拖动
      // 也要能翻，而 pointerType 在这里不需要区分。
      var x0 = null, y0 = null;
      stage.addEventListener("pointerdown", function (e) {
        x0 = e.clientX; y0 = e.clientY;
      }, { passive: true });
      stage.addEventListener("pointerup", function (e) {
        if (x0 === null) { return; }
        var dx = e.clientX - x0, dy = e.clientY - y0;
        x0 = y0 = null;
        // 纵向为主的手势是在滚页面，不是在翻图
        if (Math.abs(dx) < 40 || Math.abs(dx) < Math.abs(dy)) { return; }
        show(idx + (dx < 0 ? 1 : -1));
      }, { passive: true });
      stage.addEventListener("pointercancel", function () { x0 = y0 = null; }, { passive: true });

      stage.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight") { show(idx + 1); e.preventDefault(); }
        else if (e.key === "ArrowLeft") { show(idx - 1); e.preventDefault(); }
      });

      // 首屏对齐：HTML 里首张已带 is-active，这里只把缩略图的高亮补上
      for (var m = 0; m < thumbs.length; m++) {
        var on2 = m === idx;
        thumbs[m].classList.toggle("is-active", on2);
        if (on2) { thumbs[m].setAttribute("aria-current", "true"); }
        else { thumbs[m].removeAttribute("aria-current"); }
      }
    }
  };

  /* ---------------------------------------------------------------------
   * enquiryPrefill — the contact form's "Enquiry Type" can be preselected
   * from the link that led here, so the four footer links (Partners, Press,
   * Careers, Contact) all point at the one page and land on the right option.
   * Figma's handover note asks for the Funky site's behaviour; that site
   * carries the choice in the query string, which is what this reads.
   *
   *   get-in-touch.html?type=press
   *
   * An unknown value is ignored, leaving the design's own default selected.
   * ------------------------------------------------------------------- */
  var enquiryPrefill = {
    init: function () {
      var form = document.querySelector("[data-prefill-enquiry]");
      if (!form) return;
      var select = form.querySelector("#enquiry");
      if (!select) return;

      var want = (new URLSearchParams(window.location.search).get("type") || "").toLowerCase();
      if (!want) return;

      for (var i = 0; i < select.options.length; i++) {
        if (select.options[i].value.toLowerCase() === want) {
          select.selectedIndex = i;
          return;
        }
      }
    }
  };

  /* ---------------------------------------------------------------------
   * smoothScroll — 全站平滑滚动（任务文档第 1 条）。用 Lenis 1.3.11（MIT），
   * 文件已 vendored 到 assets/lenis.min.js，没有构建步骤，改版本＝换那个文件。
   *
   * 为什么用插件而不是自己写阻尼：手写那版在鼠标滚轮下没问题，但**触控板**
   * 的 wheel 事件是操作系统已经加过惯性的高频流，再叠一层阻尼会糊成拖尾。
   * 归一化不同输入源（滚轮 / 触控板 / 精密滚轮 / deltaMode 三种单位）正是
   * Lenis 主要在解决的事，而这一点在无头浏览器里验不出来
   * （见 memory headless-chromium-probe-limits：mouse.wheel ≠ 真机）。
   *
   * ⚠ 必须配 html{scroll-behavior:auto}。Lenis 内部靠 window.scrollTo 落位，
   *   而按 CSSOM-View，scrollTo 是按元素的 scroll-behavior 执行的 —— CSS 那边
   *   若是 smooth，就变成「平滑里再套一层平滑」，页面会飘。
   *   老教程里那条 `.lenis.lenis-smooth{scroll-behavior:auto!important}` 保险丝
   *   **自 Lenis 1.3 起已失效**（不再输出 lenis-smooth 类），指望不上。
   *   见 memory scroll-behavior-smooth-vs-scrolltrigger。
   *
   * 三个必须处理的边界：
   *   1. 自己能滚的容器（缩略图竖轨、导航抽屉、营养表弹窗正文）要挂
   *      data-lenis-prevent，否则滚轮会穿透去滚页面。**每加一个
   *      overflow-y:auto 的容器就要在 PREVENT 里登记**，font-check.html
   *      有一条自检在盯这件事。
   *   2. 弹窗打开时 lenis.stop()，交还原生 —— 页面已被 is-modal-open 锁住，
   *      弹窗正文才滚得动。modal.open/close 里调 pause()/resume()。
   *   3. 触摸不接管（syncTouch 默认 false）：真机原生惯性比任何模拟都好，
   *      接管 touch 是无障碍上的倒退。
   *
   * 关掉：给 <html> 加 data-no-smooth；prefers-reduced-motion 下自动不启用。
   * ------------------------------------------------------------------- */
  var smoothScroll = {
    // 站内每一个 overflow-y:auto 的容器都要在这里登记
    PREVENT: ".gb-product__thumbs, .gb-header__panel, .gb-nl-panel__body",

    lenis: null,

    init: function () {
      var root = document.documentElement;
      if (root.hasAttribute("data-no-smooth")) { return; }
      if (typeof Lenis !== "function") { return; }   // 插件没加载就走原生，不报错
      if (window.matchMedia &&
          window.matchMedia("(prefers-reduced-motion: reduce)").matches) { return; }

      var els = document.querySelectorAll(this.PREVENT);
      for (var i = 0; i < els.length; i++) {
        els[i].setAttribute("data-lenis-prevent", "");
      }

      this.lenis = new Lenis({
        duration: 1,
        // easeOutExpo：起步快、尾巴长，是「顺滑」而不是「粘手」的关键
        easing: function (t) { return t === 1 ? 1 : 1 - Math.pow(2, -10 * t); },
        smoothWheel: true,
        syncTouch: false,
        autoRaf: true
      });

      this.anchors();
    },

    /* 站内锚点。不开 Lenis 自带的 anchors：本站有 70 个 href="#" 的占位链接，
       交给它有把页面拉回顶部的风险。这里逐条守卫后再自己送进 lenis.scrollTo。 */
    anchors: function () {
      var self = this;
      document.addEventListener("click", function (e) {
        var a = e.target.closest && e.target.closest('a[href^="#"]');
        if (!a) { return; }
        var hash = a.getAttribute("href");
        if (!hash || hash === "#") { return; }              // 占位链接
        if (a.pathname !== location.pathname || a.origin !== location.origin) { return; }
        var t;
        try { t = document.querySelector(hash); }           // hash 是数据不是选择器
        catch (err) { return; }
        if (!t) { return; }
        e.preventDefault();
        self.lenis.scrollTo(t, { offset: 0 });
        if (history.pushState) { history.pushState(null, "", hash); }
      });
    },

    pause: function () { if (this.lenis) { this.lenis.stop(); } },
    resume: function () { if (this.lenis) { this.lenis.start(); } }
  };

  function ready(fn) {
    if (document.readyState !== "loading") { fn(); }
    else { document.addEventListener("DOMContentLoaded", fn); }
  }

  ready(function () {
    // One IIFE, ten modules: without a boundary the first throw takes every
    // module after it with it, silently -- the page renders and simply stops
    // responding from that point on. Failing one module is the smaller loss.
    var modules = [["wowo", wowo], ["header", header], ["bearMeter", bearMeter],
                   ["packBand", packBand],
                   ["popText", popText], ["lineReveal", lineReveal], ["modal", modal], ["promoModal", promoModal],
                   ["slider", slider], ["gallery", gallery], ["accordion", accordion],
                   ["smoothScroll", smoothScroll], ["enquiryPrefill", enquiryPrefill]];
    for (var i = 0; i < modules.length; i++) {
      try {
        modules[i][1].init();
      } catch (e) {
        if (window.console && console.error) { console.error("gumi:" + modules[i][0], e); }
      }
    }
  });

  window.gumi = { wowo: wowo, header: header, bearMeter: bearMeter, packBand: packBand,
                  popText: popText,
                  lineReveal: lineReveal, modal: modal, promoModal: promoModal, slider: slider,
                  gallery: gallery, accordion: accordion,
                  smoothScroll: smoothScroll, enquiryPrefill: enquiryPrefill };
})();

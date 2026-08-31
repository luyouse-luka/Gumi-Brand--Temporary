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
    lockToken: 0,

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

      // On mobile the drawer covers the whole viewport, bar included, so the
      // toggle underneath it is not hit-testable and there is nothing "outside"
      // the panel to click. Its own close button is the only way back out.
      var close = el.querySelector(".gb-header__panel-close");
      if (close) {
        close.addEventListener("click", function () { self.set(false); });
      }

      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") self.set(false);
      });

      document.addEventListener("click", function (e) {
        if (el.classList.contains("is-open") && !el.contains(e.target)) self.set(false);
      });

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

    set: function (open) {
      // Measure the real scrollbar width while it is still on screen: the lock
      // below removes it and the viewport would widen by that much, shunting the
      // page sideways. The is-menu-open rule pads the freed width back in.
      if (open) {
        var scrollbarW = window.innerWidth - document.documentElement.clientWidth;
        document.documentElement.style.setProperty("--scrollbar-w", scrollbarW + "px");
      }
      var wasOpen = this.el.classList.contains("is-open");
      this.el.classList.toggle("is-open", open);
      var toggle = this.el.querySelector(".gb-header__toggle");
      if (toggle) toggle.setAttribute("aria-expanded", open ? "true" : "false");
      // html carries the scroll (the reset puts overflow-x on it), so the lock
      // has to sit on both. The rule itself is scoped to the phone tier.
      var token = ++this.lockToken;
      if (open) {
        document.documentElement.classList.add("is-menu-open");
        document.body.classList.add("is-menu-open");
        return;
      }
      // Same shape as modal.close(): dropping the lock in this frame hands the
      // scrollbar back while the drawer is still sliding shut, and the drawer's
      // containing block narrows by that width -- it steps 15px sideways in full
      // view. Hold the lock for the slide-out, which the panel declares itself.
      // Token, not a stored timer id: reopening mid-exit must not let the stale
      // callback unlock the drawer that replaced this one.
      var panel = this.el.querySelector(".gb-header__panel");
      var ms = (wasOpen && panel) ? modalExitMs(panel) : 0;
      var self = this;
      var run = function () {
        if (self.lockToken !== token) { return; }
        document.documentElement.classList.remove("is-menu-open");
        document.body.classList.remove("is-menu-open");
      };
      if (ms > 0) { setTimeout(run, ms); } else { run(); }
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
   * countUp — [data-count-up] counts a figure up from zero the first time it
   * enters the viewport.
   *
   * The markup ships the FINAL value; nothing here writes the number into an
   * empty element. So with JS off, with reduced motion, or if this throws, the
   * figure is simply there — which is why it can afford to bail early anywhere.
   *
   * The element keeps its authored innerHTML (the figures are wrapped in a
   * span) and gets it back verbatim on the last frame, so the count can never
   * leave a rounded value or a stripped wrapper behind.
   * ------------------------------------------------------------------- */
  var COUNT_MS = 1400;

  var countUp = {
    init: function () {
      var els = document.querySelectorAll("[data-count-up]");
      if (!els.length) return;
      // Reduced motion: leave the authored figure exactly as it is.
      if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
      if (!("IntersectionObserver" in window)) return;

      var self = this;
      var io = new IntersectionObserver(function (entries, obs) {
        for (var i = 0; i < entries.length; i++) {
          if (!entries[i].isIntersecting) continue;
          obs.unobserve(entries[i].target);      // once only
          self.run(entries[i].target);
        }
      }, { rootMargin: "0px 0px -12% 0px" });

      for (var j = 0; j < els.length; j++) { io.observe(els[j]); }
    },

    run: function (el) {
      var html = el.innerHTML;
      var text = el.textContent.trim();
      // prefix / digits / suffix — "95%" and "6g" both land here, "Actually
      // good" does not and is left alone.
      var m = text.match(/^(\D*?)(\d+(?:\.\d+)?)(\D*)$/);
      if (!m) return;
      var head = m[1], target = parseFloat(m[2]), tail = m[3];
      var decimals = (m[2].split(".")[1] || "").length;

      /* Freeze the box at its final width first: "0%" is narrower than "95%",
         and the figure sits in a flex column, so without this every frame
         relayouts the card. */
      el.style.minWidth = el.getBoundingClientRect().width + "px";

      var t0 = 0;
      var step = function (now) {
        if (!t0) { t0 = now; }
        var p = Math.min(1, (now - t0) / COUNT_MS);
        if (p < 1) {
          // easeOutCubic — the same shape as $ease-out in the motion tokens
          var v = target * (1 - Math.pow(1 - p, 3));
          el.textContent = head + v.toFixed(decimals) + tail;
          window.requestAnimationFrame(step);
        } else {
          el.innerHTML = html;
          el.style.minWidth = "";
        }
      };
      window.requestAnimationFrame(step);
    }
  };

  /* ---------------------------------------------------------------------
   * lineReveal — per-line entrance for running copy, the other half of the
   * cravburgers.shop reference (notes 401:29596 / 216:5903). popText above is
   * the word-scatter pop the notes reserve for the STATISTICS numbers; round 33
   * moved those here as well, so popText currently has no hosts. This is their
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

         The 500ms fallback always fires first on a slow connection, so it is not
         enough on its own: measured with the font response held back 1500ms, three
         leads split into 2 lines against the fallback font, then each line grew
         and every mask held two lines — the element went 60 -> 90, a 30px shift,
         with the mask count still at 2 so the animation slid two lines at once.
         So re-split once the font lands. groupLines is idempotent (it unwraps the
         old masks and rebuilds against the current wrap points) and paragraphs
         that already revealed go through is-settled straight to the end state. */
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
        if (!started) { start(); return; }   // font was fast; the first split already used it
        for (var n = 0; n < self.els.length; n++) {
          try { self.split(self.els[n]); } catch (e) { /* leave last-good state */ }
        }
        self.sequence();
      };

      if (document.fonts && document.fonts.ready && typeof document.fonts.ready.then === "function") {
        document.fonts.ready.then(refine, refine);
        window.setTimeout(start, 500);
      } else {
        start();
      }

      /* Wrap points move with viewport width, so a resize has to re-group
         words into fresh lines. split() itself skips already-revealed
         elements straight to the settled end state -- see groupLines().
 
         Re-grouping is debounced, but UNMASKING cannot be: .gb-line-mask is
         display:block, so while the old masks stand each line is its own block
         and re-wraps inside itself instead of the paragraph re-wrapping as a
         whole. Drag a window narrower and "never felt this good." breaks after
         "this" and leaves "good." stranded on a third line, because the mask
         from the old width is still there deciding where the line ends. That
         lasts as long as the debounce, and a continuous drag keeps resetting it.
         So: flatten now, re-group when the drag stops.
         tools/wraptruth.py is the check — it reads the same page with JS off as
         the invariant, because comparing one split state against another split
         state is two readings of the same fault.
 
         Only hosts that have already played: an unrevealed one is hidden inside
         its masks, so its wrap points are not visible anyway, and dropping the
         masks would flash the copy in ahead of its own entrance. */
      var timer;
      window.addEventListener("resize", function () {
        for (var f = 0; f < self.els.length; f++) {
          var el = self.els[f];
          if (!el.classList.contains("is-revealed") && !el.classList.contains("is-settled")) continue;
          try { self.flatten(el); } catch (e) { /* leave last-good state */ }
        }
        window.clearTimeout(timer);
        timer = window.setTimeout(function () {
          for (var n = 0; n < self.els.length; n++) {
            try { self.split(self.els[n]); } catch (e) { /* leave last-good state */ }
          }
          self.sequence();
        }, LINE_RESIZE_DEBOUNCE);
      });
    },

    runInitialSplit: function () {
      var els = this.els;
      for (var i = 0; i < els.length; i++) {
        try { this.split(els[i]); } catch (e) { els[i].setAttribute("data-line-failed", ""); }
      }
      this.sequence();

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
    /* Drops the per-line masks and puts the words back as flat children, which
       is the only state in which the browser wraps the paragraph AS A PARAGRAPH.
       groupLines() starts with this; resize calls it on its own — see init(). */
    flatten: function (root) {
      var masks = root.querySelectorAll(".gb-line-mask");
      for (var u = 0; u < masks.length; u++) {
        var mask = masks[u];
        var inner = mask.firstChild;
        while (inner && inner.firstChild) mask.parentNode.insertBefore(inner.firstChild, mask);
        mask.parentNode.removeChild(mask);
      }
    },

    groupLines: function (root) {
      var wasRevealed = root.classList.contains("is-revealed") || root.classList.contains("is-settled");

      this.flatten(root);

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
    },

    /* Hosts inside [data-line-sequence] play one after another instead of all
       at once: --line-base continues the line index across siblings, so the
       150ms per-line stagger carries straight on into the next block. Has to
       re-run after every split pass -- the line counts move with the width. */
    sequence: function () {
      var groups = document.querySelectorAll("[data-line-sequence]");
      for (var g = 0; g < groups.length; g++) {
        var hosts = groups[g].querySelectorAll("[data-line-reveal]");
        var base = 0;
        for (var h = 0; h < hosts.length; h++) {
          hosts[h].style.setProperty("--line-base", base);
          base += hosts[h].querySelectorAll(".gb-line-mask").length || 1;
        }
      }
    }
  };

  /* ---------------------------------------------------------------------
   * packBand — the diagonal run of packs in the nutrition block.
   *
   * The markup carries two <picture> per row; how many are needed to fill the
   * screen is computed here and cloned in — the same approach .gb-bear-meter uses
   * to generate its 100 bears.
   *
   * The rows used to be a hard-coded 10 / 11, sized for the widest case: desktop
   * needs 4385px of run and mobile 2160px, against viewports of 1440 / 390. The
   * pitch (--pack-w / --pack-gap) is fluid, so the count has to follow.
   *
   * ⚠ Measure with offsetWidth only: .gb-pack-band is rotated -6.556°, so
   *   getBoundingClientRect() returns the rotated bounding box and the pitch comes
   *   out too large.
   * ⚠ The two counts must be one odd, one even: the board's brickwork offset comes
   *   from the rows differing by one pitch and each centring itself.
   * ------------------------------------------------------------------- */
  var PACK_BAND_TILT = 6.556;   // deg, must match .gb-pack-band's rotate

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
      /* ⚠ Measure the <img>, not the <picture>: picture is display:contents
         site-wide, so it has no box and offsetWidth is always 0 — the flex item is
         the img inside. computed width is the used value and carries the fraction
         (388.25 vs 388), which adds up over a dozen packs. Reading --pack-w does
         not work either: a custom property's computed value is the unevaluated
         clamp() string. */
      var probe = (seed.querySelector && seed.querySelector("img")) || seed;
      var packW = parseFloat(window.getComputedStyle(probe).width) || probe.offsetWidth;
      if (!packW) return;                    // not laid out yet; the resize pass will catch it
      var gap = parseFloat(window.getComputedStyle(this.rows[0]).columnGap) || 0;
      var pitch = packW + gap;
      if (pitch <= 0) return;

      // Running diagonally, the horizontal run has to cover the rotated corners;
      // +2 guarantees both ends stay clipped, as the board has them
      var span = window.innerWidth / Math.cos(PACK_BAND_TILT * Math.PI / 180);
      var base = Math.ceil(span / pitch) + 2;
      /* Row one is pinned to an even count, matching the old hard-coded 10 / 11
         phase: both rows centre, so an even row's centre line lands on the seam
         between two packs and an odd row's on a pack. "One odd, one even" alone is
         not enough — 5 / 6 keeps the half-pitch offset but swaps the roles and the
         brickwork comes out mirrored. */
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
   * accordion — one open item per group.
   *
   * Native <details name="…"> does the work: the browser keeps one item open per
   * name, and keyboard, the a11y tree and the no-JS case are unaffected
   * (Chrome 120+ / Safari 17.2+ / Firefox 130+). This only covers older browsers,
   * which ignore name as an unknown attribute and open several at once.
   *
   * No feature detection: where it is supported the others are already closed and
   * this loop is a no-op, while `'name' in HTMLDetailsElement.prototype` reports
   * support on some versions that do not have it.
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

  // Exit length, declared by the modal itself in CSS next to the transition that
  // uses it. Reduced motion zeroes every duration and delay, so the exit is over
  // before the next frame and there is nothing to wait for.
  function modalExitMs(el) {
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) { return 0; }
    var v = getComputedStyle(el).getPropertyValue("--modal-exit").trim();
    if (!v) { return 0; }
    return v.slice(-2) === "ms" ? parseFloat(v) : parseFloat(v) * 1000;
  }

  var modal = {
    current: null,
    lastFocus: null,
    unlockToken: 0,

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
      // The page is locked, so Lenis has nothing to do; stopping it lets the modal body scroll
      smoothScroll.pause();
      // Focus the dialog, not its first control. FOCUSABLE lands on the close
      // button, and a script focus with no pointer input before it still counts
      // as :focus-visible -- the ring painted itself the moment the modal
      // appeared. The container carries tabindex="-1" and has rings turned off.
      el.focus();
    },

    close: function () {
      var el = this.current;
      if (!el) return;
      this.current = null;
      el.classList.remove("is-open");
      el.setAttribute("aria-hidden", "true");
      // The lock stays on until the exit has played. Dropping it here hands the
      // scrollbar back while the panel is still fully opaque, and this modal is
      // position:fixed -- its containing block is the viewport, which narrows by
      // the scrollbar width -- so the centred panel jumps sideways mid-fade.
      this.unlockAfter(modalExitMs(el));
      if (this.lastFocus) this.lastFocus.focus();
    },

    // A token rather than a stored timer id: open() can land inside the wait, and
    // the stale callback must not unlock the modal that replaced this one.
    unlockAfter: function (ms) {
      var self = this;
      var token = ++this.unlockToken;
      var run = function () {
        if (self.unlockToken !== token || self.current) { return; }
        document.documentElement.classList.remove("is-modal-open");
        document.body.classList.remove("is-modal-open");
        smoothScroll.resume();
      };
      if (ms > 0) { setTimeout(run, ms); } else { run(); }
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
   * slider — horizontal card rails, driven by Swiper.
   *
   * Client-set: every carousel on the site runs on Swiper, not just the product
   * gallery. This was a native overflow-x scroller with scroll-snap and a
   * clone-based endless loop; Swiper owns the translate, the loop, the drag and
   * the momentum now, so the clone bookkeeping, the wrap-around, the pointer
   * drag and the click-swallowing are all gone.
   *
   *   [data-slider]  wrapper
   *     [data-slider-track]  the .swiper container
   *       .swiper-wrapper > [.swiper-slide]
   *     [data-slider-prev] / [data-slider-next]  buttons
   *
   * Config rides on the wrapper, one attribute per Swiper option, so the markup
   * still says what a rail does without reading this file:
   *   [data-slider-loop]           endless wrap (needs > 2x the visible count)
   *   [data-slider-rewind]         arrows wrap round instead of dead-ending
   *   [data-slider-centre]         centeredSlides at every width
   *   [data-slider-centre-narrow]  centeredSlides below 768 only
   *   [data-slider-step]           one slide per gesture (longSwipes: false)
   *   [data-slider-until="N"]      only a rail at or below N px wide; above that
   *                                Swiper is destroyed and CSS lays the track out
   *                                some other way (the expert cards become a grid)
   *
   * `spaceBetween` is read off the track's own `column-gap` rather than written
   * here: the gap is responsive and lives in the SCSS, and Swiper needs the
   * resolved number in JS because it writes the spacing as slide margins.
   *
   * ⚠ `loop` has a hard prerequisite. Swiper 11 loops by REORDERING the slides it
   * has rather than cloning, so a rail can never show more cards than exist:
   * with the 5 cards the reels row used to carry, 1440 (which fits 4.3) left
   * 232px of empty track on the right. Client-set: the reels rows now carry 10
   * placeholder cards so the loop has more than twice the visible count, and
   * they run `loop`. The expert rail on reviews stays on `rewind` -- above 991
   * it is a three-column GRID, so padding it out to loop size would turn one row
   * of three into three rows and change the desktop layout.
   * `rewind` (arrows wrap, nothing dead-ends) remains the fallback for any rail
   * that cannot be padded out.
   * ------------------------------------------------------------------- */
  var slider = {
    init: function () {
      var roots = document.querySelectorAll("[data-slider]");
      for (var i = 0; i < roots.length; i++) { this.bind(roots[i]); }
    },

    bind: function (root) {
      var track = root.querySelector("[data-slider-track]");
      if (!track || !track.querySelector(".swiper-slide")) { return; }
      // Vendor script missing or blocked: the wrapper is still a flex row of
      // cards, so the first few show and the arrows do nothing.
      if (typeof Swiper !== "function") { return; }

      var prev = root.querySelector("[data-slider-prev]");
      var next = root.querySelector("[data-slider-next]");
      var loop = root.hasAttribute("data-slider-loop");
      // Swiper treats them as alternatives; loop wins where both are present.
      var rewind = !loop && root.hasAttribute("data-slider-rewind");
      var until = parseFloat(root.getAttribute("data-slider-until"));
      var centreNarrow = root.hasAttribute("data-slider-centre-narrow");
      var centre = root.hasAttribute("data-slider-centre") || centreNarrow;
      // Whether centring is in force RIGHT NOW, which is what decides where the
      // rail opens. Only initialSlide may read this: `centeredSlides` itself has
      // to stay true in the base params or the 768 breakpoint below has nothing
      // to fall back to on the way down.
      var centredNow = function () {
        return root.hasAttribute("data-slider-centre")
            || (centreNarrow && matchMedia("(max-width: 767px)").matches);
      };
      var sw = null;

      var options = function () {
        var o = {
          slidesPerView: "auto",
          spaceBetween: parseFloat(getComputedStyle(track).columnGap) || 0,
          loop: loop,
          rewind: rewind,
          grabCursor: true,
          speed: matchMedia("(prefers-reduced-motion: reduce)").matches ? 0 : 400,
          centeredSlides: centre,
          // A centred rail opens on its MIDDLE card, which is what puts the set
          // symmetrically across the viewport -- the board's own framing. Opening
          // on the first card would centre that one and leave the whole left half
          // of the track empty.
          // A centred rail opens on its MIDDLE card so the set sits symmetrically
          // across the viewport. Under `loop` there is no "whole set" to centre --
          // the rail is endless in both directions -- so the first card is fine.
          initialSlide: (!loop && centredNow())
            ? Math.floor((track.querySelectorAll(".swiper-slide").length - 1) / 2)
            : 0,
          // One slide per gesture: without this a long drag hands over to the
          // long-swipe rule and crosses as many cards as it travelled.
          longSwipes: !root.hasAttribute("data-slider-step"),
          // The markup carries role / aria-label already; the a11y module would
          // add a second, conflicting set.
          a11y: false,
          keyboard: false
        };
        if (centreNarrow) {
          o.breakpoints = { 768: { centeredSlides: false } };
        }
        return o;
      };

      var sync = function () {
        if (!sw || rewind || loop) { return; }   // neither one ever dead-ends
        if (prev) { prev.disabled = sw.isBeginning; }
        if (next) { next.disabled = sw.isEnd; }
      };

      var create = function () {
        if (sw) { return; }
        sw = new Swiper(track, options());
        sw.on("slideChange", sync);
        sync();
      };

      var destroy = function () {
        if (!sw) { return; }
        sw.destroy(true, true);           // also strips the inline styles it wrote
        sw = null;
        if (prev) { prev.disabled = false; }
        if (next) { next.disabled = false; }
      };

      if (prev) { prev.addEventListener("click", function () { if (sw) sw.slidePrev(); }); }
      if (next) { next.addEventListener("click", function () { if (sw) sw.slideNext(); }); }

      // The rail is focusable (tabindex on the track), and a native scroller
      // answered the arrow keys for free. Bound to the track, not the document:
      // a reader arrowing down the page must not be paging a carousel.
      if (track.hasAttribute("tabindex")) {
        track.addEventListener("keydown", function (e) {
          if (!sw) { return; }
          if (e.key === "ArrowRight") { sw.slideNext(); e.preventDefault(); }
          else if (e.key === "ArrowLeft") { sw.slidePrev(); e.preventDefault(); }
        });
      }

      if (!(until > 0)) { create(); return; }

      // Rails that only exist below a breakpoint. matchMedia rather than
      // Swiper's own `breakpoints: {enabled: false}`: disabling leaves the loop
      // duplicates in the DOM, and above the threshold those show up as extra
      // grid cells.
      var mq = matchMedia("(max-width: " + until + "px)");
      var apply = function () { if (mq.matches) { create(); } else { destroy(); } };
      if (mq.addEventListener) { mq.addEventListener("change", apply); }
      else if (mq.addListener) { mq.addListener(apply); }
      apply();
    }
  };

  /* ---------------------------------------------------------------------
   * gallery — thumbnail rail driving a Swiper stage.
   *
   * Client-set: the stage is Swiper (assets/swiper-bundle.min.js), configured to
   * behave exactly as the hand-rolled version did — cross-fade, one slide per
   * gesture, no wrap, stops at the ends.
   *
   * The rail is deliberately NOT Swiper's thumbs module: that would turn it into
   * a transform track and cost it its scroll-snap, its overflow scrolling and its
   * place in the Lenis PREVENT list. It stays a plain button strip calling
   * slideTo, with slideChange writing the active state back.
   *
   * Keyboard is ours too. Swiper's module listens on the document, so ArrowLeft /
   * ArrowRight would change slides while the reader is arrowing down the page;
   * this stays bound to the focused stage.
   *
   *   [data-gallery]        shell
   *     [data-gallery-thumbs] thumbnail column
   *       [data-gallery-go="N"] jump to slide N
   *     [data-gallery-track]  stage (.swiper)
   *       [data-gallery-slide]  one slide (.swiper-slide)
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
      if (!stage.querySelector("[data-gallery-slide]")) { return; }
      // Vendor script missing or blocked: the CSS leaves slide one showing, which
      // is the same state this had with JS off.
      if (typeof Swiper !== "function") { return; }

      var sw = new Swiper(stage, {
        effect: "fade",
        fadeEffect: { crossFade: true },
        // Was `transition: opacity .3s` on the slide; Swiper writes the duration
        // inline, so the reduced-motion reset cannot reach it and it is set here.
        speed: matchMedia("(prefers-reduced-motion: reduce)").matches ? 0 : 300,
        // The old gesture, restated as options: nothing moves under the finger,
        // a drag shorter than 40px is not a swipe, and a mostly-vertical one is
        // the page scrolling.
        followFinger: false,
        threshold: 40,
        touchAngle: 45,
        // The markup already carries role / aria-label / aria-current; the a11y
        // module would add a second, conflicting set.
        a11y: false,
        keyboard: false
      });

      var sync = function (scroll) {
        var idx = sw.activeIndex;
        for (var j = 0; j < thumbs.length; j++) {
          var on = j === idx;
          thumbs[j].classList.toggle("is-active", on);
          if (on) { thumbs[j].setAttribute("aria-current", "true"); }
          else { thumbs[j].removeAttribute("aria-current"); }
        }
        // The rail scrolls too (vertical on desktop, horizontal when narrow).
        // Not on first paint: nothing has been chosen yet, and scrollIntoView
        // would drag the page down to the gallery on load.
        if (scroll && thumbs[idx] && thumbs[idx].scrollIntoView) {
          try { thumbs[idx].scrollIntoView({ block: "nearest", inline: "nearest" }); } catch (e) {}
        }
      };

      sw.on("slideChange", function () { sync(true); });
      sync(false);

      for (var i = 0; i < thumbs.length; i++) {
        (function (btn) {
          btn.addEventListener("click", function () {
            sw.slideTo(parseInt(btn.getAttribute("data-gallery-go"), 10) || 0);
          });
        })(thumbs[i]);
      }

      stage.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight") { sw.slideNext(); e.preventDefault(); }
        else if (e.key === "ArrowLeft") { sw.slidePrev(); e.preventDefault(); }
      });
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
   * selectBox — client-set: the enquiry select is presented as a button and a
   * ul listbox so the chevron can rotate. A native <select> paints its own
   * popup, and the background-image arrow it used before cannot be transformed.
   *
   * An enhancement, not a replacement. The native control stays in the DOM as
   * the single source of the options AND as the form's value carrier, so submit
   * still posts `enquiry`, enquiryPrefill still works, and if this module ever
   * throws the user is left with the native control rather than nothing.
   * It runs after enquiryPrefill so the button opens on the preselected option.
   *
   * ARIA listbox pattern: the ul takes focus and moves aria-activedescendant,
   * so no option ever holds a tabindex. Typeahead is not implemented.
   * ------------------------------------------------------------------- */
  var selectBox = {
    boxes: [],

    init: function () {
      var self = this;
      var all = document.querySelectorAll("select[data-select]");
      for (var i = 0; i < all.length; i++) { this.build(all[i]); }
      if (!this.boxes.length) { return; }

      document.addEventListener("click", function (e) {
        for (var i = 0; i < self.boxes.length; i++) {
          var b = self.boxes[i];
          if (b.open && !b.wrap.contains(e.target)) { self.close(b, false); }
        }
      });
    },

    build: function (native) {
      if (!native.options.length) { return; }
      var self = this;
      var id = native.id || ("gb-select-" + this.boxes.length);
      // "bare" = the phone field's country code: same widget with no box of its
      // own, because .gb-field__phone already draws the border around it.
      var bare = native.getAttribute("data-select") === "bare";
      var aria = native.getAttribute("aria-label");

      var wrap = document.createElement("div");
      wrap.className = bare ? "gb-select gb-select--bare" : "gb-select";
      native.parentNode.insertBefore(wrap, native);
      wrap.appendChild(native);
      native.classList.add("gb-select__native");
      native.setAttribute("tabindex", "-1");
      native.setAttribute("aria-hidden", "true");

      var btn = document.createElement("button");
      btn.type = "button";
      btn.id = id + "-button";
      btn.className = bare ? "gb-select__button"
                           : "gb-field__input gb-field__input--select gb-select__button";
      btn.setAttribute("aria-haspopup", "listbox");
      btn.setAttribute("aria-expanded", "false");
      btn.setAttribute("aria-controls", id + "-list");
      btn.innerHTML =
        '<span class="gb-select__value"></span>' +
        '<svg class="gb-select__arrow" viewBox="0 0 20 20" fill="none" aria-hidden="true">' +
        '<path d="M5 7.5L10 12.5L15 7.5" stroke="#4d4d4d" stroke-width="1.667" ' +
        'stroke-linecap="round" stroke-linejoin="round"/></svg>';

      // The label pointed at a control that is now off-screen. A button is not a
      // labelable element, so the association has to move to aria-labelledby.
      var label = document.querySelector('label[for="' + id + '"]');
      if (label) {
        if (!label.id) { label.id = id + "-label"; }
        label.removeAttribute("for");
        label.addEventListener("click", function () { btn.focus(); });
        btn.setAttribute("aria-labelledby", label.id + " " + btn.id);
      } else if (aria) {
        btn.setAttribute("aria-label", aria);
      }

      var list = document.createElement("ul");
      list.className = "gb-select__list";
      list.id = id + "-list";
      list.setAttribute("role", "listbox");
      list.setAttribute("tabindex", "-1");
      if (label) { list.setAttribute("aria-labelledby", label.id); }
      else if (aria) { list.setAttribute("aria-label", aria); }
      // Built after smoothScroll.init has swept the DOM for PREVENT, so it has to
      // opt out of Lenis itself.
      list.setAttribute("data-lenis-prevent", "");

      for (var i = 0; i < native.options.length; i++) {
        var li = document.createElement("li");
        li.className = "gb-select__option";
        li.id = id + "-opt-" + i;
        li.setAttribute("role", "option");
        li.textContent = native.options[i].text;
        list.appendChild(li);
      }

      wrap.appendChild(btn);
      wrap.appendChild(list);

      var box = { wrap: wrap, native: native, btn: btn, list: list,
                  value: btn.firstChild, open: false, active: -1 };
      this.boxes.push(box);
      this.sync(box);

      btn.addEventListener("click", function () {
        if (box.open) { self.close(box, true); } else { self.show(box); }
      });

      btn.addEventListener("keydown", function (e) {
        var k = e.key;
        if (k === "ArrowDown" || k === "ArrowUp" || k === "Enter" || k === " ") {
          e.preventDefault();          // also stops Enter/Space firing click twice
          self.show(box);
        }
      });

      list.addEventListener("click", function (e) {
        var li = e.target.closest && e.target.closest(".gb-select__option");
        if (!li) { return; }
        self.choose(box, Array.prototype.indexOf.call(list.children, li));
        self.close(box, true);
      });

      list.addEventListener("keydown", function (e) {
        var k = e.key, last = list.children.length - 1;
        if (k === "Escape") { e.stopPropagation(); self.close(box, true); }
        else if (k === "Tab") { self.close(box, false); }
        else if (k === "ArrowDown") { e.preventDefault(); self.move(box, box.active + 1); }
        else if (k === "ArrowUp") { e.preventDefault(); self.move(box, box.active - 1); }
        else if (k === "Home") { e.preventDefault(); self.move(box, 0); }
        else if (k === "End") { e.preventDefault(); self.move(box, last); }
        else if (k === "Enter" || k === " ") {
          e.preventDefault();
          self.choose(box, box.active);
          self.close(box, true);
        }
      });

      // Anything that drives the real control (enquiryPrefill, a Shopify app,
      // a form reset) is mirrored back into the drawn one.
      native.addEventListener("change", function () { self.sync(box); });
    },

    show: function (box) {
      if (box.open) { return; }
      box.open = true;
      box.wrap.classList.add("is-open");
      box.btn.setAttribute("aria-expanded", "true");
      this.move(box, box.native.selectedIndex);
      box.list.focus();
    },

    close: function (box, refocus) {
      if (!box.open) { return; }
      box.open = false;
      box.wrap.classList.remove("is-open");
      box.btn.setAttribute("aria-expanded", "false");
      box.list.removeAttribute("aria-activedescendant");
      if (refocus) { box.btn.focus(); }
    },

    move: function (box, i) {
      var kids = box.list.children;
      if (!kids.length) { return; }
      i = Math.max(0, Math.min(kids.length - 1, i));
      for (var j = 0; j < kids.length; j++) {
        kids[j].classList.toggle("is-active", j === i);
      }
      box.active = i;
      box.list.setAttribute("aria-activedescendant", kids[i].id);
      kids[i].scrollIntoView({ block: "nearest" });
    },

    choose: function (box, i) {
      if (i < 0 || i >= box.native.options.length) { return; }
      if (box.native.selectedIndex !== i) {
        box.native.selectedIndex = i;
        box.native.dispatchEvent(new Event("change", { bubbles: true }));
      }
      this.sync(box);
    },

    sync: function (box) {
      var i = box.native.selectedIndex;
      box.value.textContent = i < 0 ? "" : box.native.options[i].text;
      var kids = box.list.children;
      for (var j = 0; j < kids.length; j++) {
        kids[j].setAttribute("aria-selected", j === i ? "true" : "false");
      }
    }
  };

  /* ---------------------------------------------------------------------
   * smoothScroll — site-wide smooth scrolling on Lenis 1.3.11 (MIT), vendored to
   * assets/lenis.min.js. No build step; changing version = replacing that file.
   *
   * Why a library rather than hand-rolled damping: the hand-rolled version was
   * fine under a mouse wheel, but a TRACKPAD's wheel events are a high-frequency
   * stream the OS has already added inertia to, and a second layer of damping
   * smears into a trail. Normalising input sources (wheel / trackpad / precision
   * wheel / three deltaMode units) is most of what Lenis does, and none of it can
   * be verified headless (mouse.wheel is not a real device).
   *
   * ⚠ Requires html{scroll-behavior:auto}. Lenis lands with window.scrollTo, and
   *   per CSSOM-View scrollTo obeys the element's scroll-behavior — smooth in CSS
   *   makes it smooth inside smooth and the page drifts. The old
   *   `.lenis.lenis-smooth{scroll-behavior:auto!important}` fuse stopped working in
   *   Lenis 1.3 (the class is no longer emitted).
   *
   * Three edges that have to be handled:
   *   1. Anything that scrolls itself (thumbnail rail, nav drawer, the nutrition
   *      table's body) needs data-lenis-prevent, or the wheel falls through to the
   *      page. REGISTER EVERY NEW overflow-y:auto CONTAINER IN PREVENT —
   *      font-check.html has a probe watching for this.
   *   2. lenis.stop() while a modal is open, handing back to native — the page is
   *      already locked by is-modal-open and the modal body has to scroll.
   *      modal.open/close call pause()/resume().
   *   3. Touch is left alone (syncTouch defaults to false): native inertia beats
   *      any simulation and taking it over is an accessibility regression.
   *
   * To disable: data-no-smooth on <html>; prefers-reduced-motion skips it.
   * ------------------------------------------------------------------- */
  var smoothScroll = {
    // Every overflow-y:auto container on the site has to be registered here
    PREVENT: ".gb-product__thumbs, .gb-header__panel, .gb-nl-panel__body, .gb-select__list",

    lenis: null,

    init: function () {
      var root = document.documentElement;
      if (root.hasAttribute("data-no-smooth")) { return; }
      if (typeof Lenis !== "function") { return; }   // library absent: native scrolling, no error
      if (window.matchMedia &&
          window.matchMedia("(prefers-reduced-motion: reduce)").matches) { return; }

      var els = document.querySelectorAll(this.PREVENT);
      for (var i = 0; i < els.length; i++) {
        els[i].setAttribute("data-lenis-prevent", "");
      }

      this.lenis = new Lenis({
        duration: 1,
        // easeOutExpo: quick start, long tail — the difference between smooth and sticky
        easing: function (t) { return t === 1 ? 1 : 1 - Math.pow(2, -10 * t); },
        smoothWheel: true,
        syncTouch: false,
        autoRaf: true
      });

      this.anchors();
    },

    /* In-page anchors. Lenis's own anchor handling is off: the site has 70
       href="#" placeholders and it could pull the page back to the top. Guarded
       here, then handed to lenis.scrollTo. */
    anchors: function () {
      var self = this;
      document.addEventListener("click", function (e) {
        var a = e.target.closest && e.target.closest('a[href^="#"]');
        if (!a) { return; }
        var hash = a.getAttribute("href");
        if (!hash || hash === "#") { return; }              // placeholder link
        if (a.pathname !== location.pathname || a.origin !== location.origin) { return; }
        var t;
        try { t = document.querySelector(hash); }           // hash is data, not a selector
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
                   ["popText", popText], ["countUp", countUp], ["lineReveal", lineReveal], ["modal", modal], ["promoModal", promoModal],
                   ["slider", slider], ["gallery", gallery], ["accordion", accordion],
                   ["smoothScroll", smoothScroll], ["enquiryPrefill", enquiryPrefill],
                   ["selectBox", selectBox]];
    for (var i = 0; i < modules.length; i++) {
      try {
        modules[i][1].init();
      } catch (e) {
        if (window.console && console.error) { console.error("gumi:" + modules[i][0], e); }
      }
    }
  });

  window.gumi = { wowo: wowo, header: header, bearMeter: bearMeter, packBand: packBand,
                  popText: popText, countUp: countUp,
                  lineReveal: lineReveal, modal: modal, promoModal: promoModal, slider: slider,
                  gallery: gallery, accordion: accordion,
                  smoothScroll: smoothScroll, enquiryPrefill: enquiryPrefill,
                  selectBox: selectBox };
})();

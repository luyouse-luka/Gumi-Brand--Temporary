/* Gumi Brand — site scripts. No dependencies. */
(function () {
  "use strict";

  /* Focus handed back by script -- Escape, a close button, a closing dropdown --
     keeps whatever :focus-visible state came before it, so the trigger paints a
     ring as if the user had tabbed to it (client r121). Mark it instead; CSS drops
     the ring, and the next real key or blur clears the mark so a genuine Tab rings. */
  function markRefocused(el) {
    if (!el) { return; }
    el.classList.add("is-refocused");
    var clear = function () {
      el.classList.remove("is-refocused");
      el.removeEventListener("blur", clear);
      el.removeEventListener("keydown", clear);
    };
    el.addEventListener("blur", clear);
    el.addEventListener("keydown", clear);
  }

  function returnFocus(el) {
    if (!el || !el.focus) { return; }
    markRefocused(el);
    el.focus();
  }

  /* An outline drawn with text-shadow is painted per line, so on a wrapping
     heading the next line's halo covers the previous line's descenders. CSS
     ink-split() fixes that by moving the halo to an absolutely positioned copy
     underneath -- the copy has to exist in the DOM. Where the markup carries it
     (.gb-stat__value, .gb-usp__value) nothing to do; where the text comes from a
     theme setting, build it here. innerHTML is read before the copy is inserted,
     so it never nests; aria-hidden keeps it out of the accessible name. */
  function inkSplit(el) {
    if (!el || el.querySelector(".gb-ink-halo")) { return; }
    var halo = document.createElement("span");
    halo.className = "gb-ink-halo";
    halo.setAttribute("aria-hidden", "true");
    halo.innerHTML = el.innerHTML;
    el.insertBefore(halo, el.firstChild);
  }

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
    // Client r117: on the first pass the banner and the modules under it are
    // both in view, so they start together -- and the banner loses, because its
    // media carries delay-in-1 while the modules below it usually carry none.
    // The phone then reads bottom-up. Hold the rest back by one beat so the
    // banner lands first. 700 measured, not guessed: at 400 the gap was 66ms
    // (still reads as simultaneous), at 900 the modules below arrive at 1.5s
    // and the page feels held back. Self-chosen either way, no board backing --
    // see the "awaiting design sign-off" list.
    FIRST_HOLD: 700,
    BANNER: ".gb-hero, .gb-page-hero",
    firstRun: true,

    run: function () {
      var wTop = window.pageYOffset || document.documentElement.scrollTop;
      var wHeight = window.innerHeight;
      var wBottom = wTop + wHeight;
      // Held elements are excluded so a scroll landing mid-hold cannot start
      // the same reveal a second time.
      var els = document.querySelectorAll(".wowo:not(.animated):not([data-wowo-hold])");
      var first = this.firstRun;
      this.firstRun = false;

      for (var i = 0; i < els.length; i++) {
        var el = els[i];
        var rect = el.getBoundingClientRect();
        var meHeight = el.clientHeight;
        var meTop = rect.top + wTop;
        var meBottom = meTop + meHeight;

        if (meTop > wTop - meHeight && meBottom < wBottom + meHeight) {
          if (first && el.closest && !el.closest(this.BANNER)) {
            this.hold(el, this.FIRST_HOLD);
          } else {
            this.play(el);
          }
        }
      }
    },

    play: function (el) {
      el.classList.add("animated");
      // Terra strips at a flat 1500, which assumes the delay is one of the small
      // delay-in-N steps. A sequenced step (r122) can start at 900ms, and stripping
      // mid-fade drops it straight to its end state. Wait out its own delay too.
      var d = parseFloat(getComputedStyle(el).animationDelay) * 1000;
      setTimeout(function () {
        el.classList.remove("wowo", "animated");
      }, 1500 + (d > 0 ? d : 0));
    },

    hold: function (el, ms) {
      var self = this;
      el.setAttribute("data-wowo-hold", "");
      setTimeout(function () {
        el.removeAttribute("data-wowo-hold");
        self.play(el);
      }, ms);
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
    skipFocusOpen: false,

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

      // Tab landing on the toggle opens the menu, so the next Tab walks its
      // links instead of a shut panel. Pointer focus must NOT open it: focus
      // fires before click, and the click would toggle it straight back shut.
      // :focus-visible is the only thing that tells the two apart.
      toggle.addEventListener("focus", function () {
        if (self.skipFocusOpen) { return; }
        if (toggle.matches && toggle.matches(":focus-visible")) { self.set(true); }
      });

      // .focus() dispatches synchronously, so the flag needs no timer. Without
      // it every close that hands focus back to the toggle reopens the menu --
      // programmatic focus keeps whatever :focus-visible state came before it.
      var refocus = function () {
        self.skipFocusOpen = true;
        returnFocus(toggle);
        self.skipFocusOpen = false;
      };

      // On mobile the drawer covers the whole viewport, bar included, so the
      // toggle underneath it is not hit-testable and there is nothing "outside"
      // the panel to click. Its own close button is the only way back out.
      var close = el.querySelector(".gb-header__panel-close");
      if (close) {
        close.addEventListener("click", function () { self.set(false); refocus(); });
      }

      document.addEventListener("keydown", function (e) {
        if (e.key !== "Escape" || !el.classList.contains("is-open")) { return; }
        self.set(false);
        refocus();           // else focus is stranded on what just slid away
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
            self.expand(item, !item.classList.contains("is-open"));
          });
        })(items[i]);
      }

      // Keyboard reveal. The panel and each sublist are shut by geometry (a 0fr
      // grid row, translateX on the drawer), never by display, so everything
      // inside keeps its place in the tab order while invisible -- measured 6
      // dead stops on desktop, 19 in the phone drawer. Open what the focus lands
      // in rather than skipping it: the menu is meant to be reachable by Tab.
      var panel = el.querySelector(".gb-header__panel");
      el.addEventListener("focusin", function (e) {
        var sub = e.target.closest && e.target.closest(".gb-header__sublist");
        var item = sub && sub.closest("[data-collapsible]");
        if (item) {
          self.expand(item, true);
          // The sublist opens on a 0fr -> 1fr row, so the browser's own focus
          // scroll has already run against the collapsed geometry -- and while
          // the row is still 0fr there is nothing to scroll. Re-run it once the
          // row has grown, or the last links land under the drawer's fixed CTA
          // (tools/menutab.py reads that as a blind stop).
          (function (target, row) {
            var again = function () {
              row.removeEventListener("transitionend", again);
              if (document.activeElement === target && target.scrollIntoView) {
                target.scrollIntoView({ block: "nearest" });
              }
            };
            row.addEventListener("transitionend", again);
          })(e.target, sub);
        }
        if (panel && panel.contains(e.target)) { self.set(true); }
      });
      el.addEventListener("focusout", function (e) {
        // A null relatedTarget is the browser chrome, or a click on dead space
        // inside the panel; neither means the user has left the menu.
        if (e.relatedTarget && !el.contains(e.relatedTarget)) { self.set(false); }
      });

      // The panel is the last child of <header>, so in source order the bar's
      // own controls (logo, Shop now, account, cart) sit between the toggle and
      // the menu. Reroute the two seams so Tab runs
      //   toggle -> menu -> rest of the bar -> page.
      // Only rendered stops count: the other breakpoint's list is display:none
      // on an ancestor, which leaves each link's own computed display intact --
      // getClientRects() is the one test that sees through that.
      var bar = el.querySelector(".gb-header__bar");
      var shown = function (root, skip) {
        var all = root.querySelectorAll(FOCUSABLE), out = [];
        for (var i = 0; i < all.length; i++) {
          if (all[i] !== skip && all[i].getClientRects().length) { out.push(all[i]); }
        }
        return out;
      };
      // First rendered stop after the whole header. DOCUMENT_POSITION_PRECEDING
      // (2) reads "el comes before this node", i.e. the node is past the header.
      var past = function () {
        var all = document.querySelectorAll(FOCUSABLE);
        for (var i = 0; i < all.length; i++) {
          if (!el.contains(all[i]) && (all[i].compareDocumentPosition(el) & 2)
              && all[i].getClientRects().length) { return all[i]; }
        }
        return null;
      };
      el.addEventListener("keydown", function (e) {
        if (e.key !== "Tab" || !el.classList.contains("is-open")) { return; }
        // The phone drawer covers the bar and inerts it: there is no second
        // group to interleave, and the panel already holds every stop.
        if (!panel || !bar || bar.hasAttribute("inert")) { return; }
        var inPanel = shown(panel), inBar = shown(bar, toggle);
        if (!inPanel.length || !inBar.length) { return; }
        var last = inPanel[inPanel.length - 1], a = document.activeElement;
        // toggle.focus() re-enters the focus handler, but set() early-returns
        // on an unchanged state, so reopening here is a no-op.
        if (!e.shiftKey && a === toggle) { e.preventDefault(); inPanel[0].focus(); }
        else if (!e.shiftKey && a === last) { e.preventDefault(); inBar[0].focus(); }
        else if (!e.shiftKey && a === inBar[inBar.length - 1]) {
          // Third seam, and the one that makes the path terminate: the panel is
          // the header's LAST child, so a plain Tab off the end of the bar walks
          // back into the menu and loops forever. Jump past the header instead;
          // focusout closes the menu on the way out.
          var nxt = past();
          if (nxt) { e.preventDefault(); nxt.focus(); }
        }
        else if (e.shiftKey && a === inPanel[0]) { e.preventDefault(); toggle.focus(); }
        else if (e.shiftKey && a === inBar[0]) { e.preventDefault(); last.focus(); }
      });
    },

    expand: function (item, open) {
      item.classList.toggle("is-open", open);
      var btn = item.querySelector(".gb-header__link");
      if (btn) { btn.setAttribute("aria-expanded", open ? "true" : "false"); }
    },

    set: function (open) {
      var wasOpen = this.el.classList.contains("is-open");
      // focusin fires on every Tab step inside an open panel. Re-running the
      // open path would remeasure --scrollbar-w with the bar already locked --
      // it reads 0 there, the compensation padding drops and the page steps
      // sideways.
      if (open === wasOpen) { return; }
      // Measure the real scrollbar width while it is still on screen: the lock
      // below removes it and the viewport would widen by that much, shunting the
      // page sideways. The is-menu-open rule pads the freed width back in.
      if (open) {
        var scrollbarW = window.innerWidth - document.documentElement.clientWidth;
        document.documentElement.style.setProperty("--scrollbar-w", scrollbarW + "px");
      }
      this.el.classList.toggle("is-open", open);
      var toggle = this.el.querySelector(".gb-header__toggle");
      if (toggle) toggle.setAttribute("aria-expanded", open ? "true" : "false");
      // html carries the scroll (the reset puts overflow-x on it), so the lock
      // has to sit on both. The rule itself is scoped to the phone tier.
      // The phone drawer is fixed and full-viewport, so it covers the bar while
      // the bar's own links stay tabbable behind it -- 4 more dead stops. Read
      // the panel's used position rather than repeat the breakpoint here.
      var panel = this.el.querySelector(".gb-header__panel");
      var bar = this.el.querySelector(".gb-header__bar");
      var covered = !!(panel && getComputedStyle(panel).position === "fixed");
      var token = ++this.lockToken;
      if (open) {
        if (bar && covered) {
          // Opened from the bar (a click on the toggle): hand focus to the
          // drawer BEFORE inerting the bar, or the browser drops it to <body>.
          if (bar.contains(document.activeElement)) {
            var into = panel.querySelector(".gb-header__panel-close");
            if (into) { into.focus(); }
          }
          bar.setAttribute("inert", "");
        }
        document.documentElement.classList.add("is-menu-open");
        document.body.classList.add("is-menu-open");
        return;
      }
      if (bar) { bar.removeAttribute("inert"); }
      // Same shape as modal.close(): dropping the lock in this frame hands the
      // scrollbar back while the drawer is still sliding shut, and the drawer's
      // containing block narrows by that width -- it steps 15px sideways in full
      // view. Hold the lock for the slide-out, which the panel declares itself.
      // Token, not a stored timer id: reopening mid-exit must not let the stale
      // callback unlock the drawer that replaced this one.
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
  /* Hard cap on waiting for the brand font before revealing. Only a font that
     is still unresolved this late gets the fallback metrics. */
  var LINE_FONT_WAIT = 1500;

  var lineReveal = {
    /* The hero plays as one run: the title's lines first, then each item in the CTA
       block a beat behind the last (client r122). The hooks are set here instead of
       authored because that markup is the theme's gb-hero.liquid. */
    wireHero: function () {
      var text = document.querySelector(".gb-hero__text");
      if (!text || !text.querySelector(".gb-hero__cta")) { return; }
      text.setAttribute("data-line-sequence", "");
      var steps = text.querySelectorAll(".gb-hero__cta > .wowo");
      for (var i = 0; i < steps.length; i++) { steps[i].setAttribute("data-seq-step", ""); }
    },

    init: function () {
      this.wireHero();
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
         that already revealed go through is-settled straight to the end state.

         ⚠ r132: that end-state shortcut is why the reveal must NOT start before
         the font is in. Measured cold: split at 490ms, hero revealed at 492ms,
         font landed at 824ms -- the re-split caught both hero blocks mid-run and
         settled them, so the entrance played half way and then every line
         appeared at once. Warm loads never showed it because fonts.ready beats
         the timer. So the wait below gates the REVEAL, not just the split, and
         a host that is still animating when the font lands is re-split after its
         own run ends rather than during it. */
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
        for (var n = 0; n < self.els.length; n++) { self.resplitWhenIdle(self.els[n]); }
      };

      if (document.fonts && document.fonts.ready && typeof document.fonts.ready.then === "function") {
        document.fonts.ready.then(refine, refine);
        window.setTimeout(start, LINE_FONT_WAIT);
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

    /* Re-split against the font that just landed, but never on top of a running
       entrance: groupLines sends a revealing host straight to its end state, so
       doing it mid-run stops the animation dead. Wait out whatever is left of
       this host's own lines first -- by then the shortcut is a no-op. */
    resplitWhenIdle: function (el) {
      var self = this;
      var wait = 0;
      if (el.getAnimations) {
        var anims = el.getAnimations({ subtree: true });
        for (var i = 0; i < anims.length; i++) {
          if (anims[i].playState !== "running" || !anims[i].effect) continue;
          var end = anims[i].effect.getComputedTiming().endTime || 0;
          var left = end - (anims[i].currentTime || 0);
          if (left > wait) wait = left;
        }
      }
      var run = function () {
        try { self.split(el); } catch (e) { /* leave last-good state */ }
        self.sequence();
      };
      if (wait > 0) { window.setTimeout(run, wait + 50); } else { run(); }
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
      /* Per-line halo copies are rebuilt on every pass; leaving them in would
         make each resize add another layer. */
      var stale = root.querySelectorAll(".gb-ink-halo--line");
      for (var d = 0; d < stale.length; d++) stale[d].parentNode.removeChild(stale[d]);

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

      /* The halo is one absolutely positioned copy of the WHOLE string, so it
         cannot ride a per-line reveal: a single clip window crosses line 2
         before line 2's own mask has started, and the outline lands ahead of
         its glyphs. It is kept out of the grouping here and re-created per line
         below — parked OUTSIDE the masks, see the second pass. */
      var halo = null;
      for (var h0 = 0; h0 < nodes.length; h0++) {
        if (nodes[h0].nodeType === 1 && nodes[h0].classList.contains("gb-ink-halo")) {
          halo = nodes[h0];
          break;
        }
      }

      for (var i = 0; i < nodes.length; i++) {
        var node = nodes[i];
        if (node === halo) continue;
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

      /* One halo per line, parked OUTSIDE the masks. It cannot go inside: the
         mask clips to the line box and the outline is a 15px text-shadow, so it
         would come out sliced flat. Each copy is offset onto its own line and
         carries that line's --line-i, so it rides the same 150ms stagger as the
         glyphs it sits behind. Read the offsets after every mask exists —
         reading them inside the loop above would measure a half-built column. */
      if (halo) {
        var built = root.querySelectorAll(".gb-line-mask");
        for (var m = 0; m < built.length; m++) {
          var lineHalo = halo.cloneNode(false);
          lineHalo.classList.add("gb-ink-halo--line");
          lineHalo.style.top = built[m].offsetTop + "px";
          lineHalo.style.setProperty("--line-i", m);
          var srcInner = built[m].firstChild;
          for (var q = 0; q < srcInner.childNodes.length; q++) {
            lineHalo.appendChild(srcInner.childNodes[q].cloneNode(true));
          }
          root.appendChild(lineHalo);
        }
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
        // [data-seq-step] is a whole element (a button, a list) rather than text,
        // so it takes one beat; a line host takes as many as it has lines.
        var hosts = groups[g].querySelectorAll("[data-line-reveal], [data-seq-step]");
        var base = 0;
        for (var h = 0; h < hosts.length; h++) {
          hosts[h].style.setProperty("--line-base", base);
          base += hosts[h].hasAttribute("data-line-reveal")
            ? (hosts[h].querySelectorAll(".gb-line-mask").length || 1)
            : 1;
        }
      }
    }
  };

  /* ---------------------------------------------------------------------
   * reelPlayer — a reel card plays where it stands (client r123). It used to open
   * the shared lightbox; that dialog and its styles are gone.
   *
   * data-video takes either a media file or a hosted page (YouTube, Vimeo). Only a
   * file can go in <video>: given a watch URL it fetches an HTML page and fails
   * silently, black frame and no error. A hosted page is embedded instead.
   * ------------------------------------------------------------------- */
  var reelPlayer = {
    init: function () {
      var cards = document.querySelectorAll("[data-reel]");
      if (!cards.length) return;
      var self = this;
      for (var i = 0; i < cards.length; i++) {
        (function (card) {
          var trigger = card.querySelector("[data-reel-play]");
          if (!trigger) return;
          trigger.addEventListener("click", function () { self.play(card, trigger); });
        })(cards[i]);
      }
    },

    // youtube-nocookie is YouTube's own privacy-enhanced host.
    embedUrl: function (src) {
      var m = src.match(/(?:youtube(?:-nocookie)?\.com\/(?:watch\?(?:[^#]*&)?v=|embed\/|shorts\/|live\/)|youtu\.be\/)([\w-]{6,})/);
      if (m) {
        var t = src.match(/[?&#]t=(\d+)/);
        return "https://www.youtube-nocookie.com/embed/" + m[1] +
               "?autoplay=1&rel=0&playsinline=1" + (t ? "&start=" + t[1] : "");
      }
      m = src.match(/(?:player\.)?vimeo\.com\/(?:video\/)?(\d+)/);
      if (m) { return "https://player.vimeo.com/video/" + m[1] + "?autoplay=1"; }
      return null;
    },

    play: function (card, trigger) {
      if (card.querySelector("[data-reel-node]")) { return; }   // already playing
      var src = trigger.getAttribute("data-video");
      if (!src) { return; }
      this.stopAll(card);
      var embed = this.embedUrl(src);
      var node;

      // YouTube and Vimeo refuse a null origin, which is exactly what a file://
      // page has, and render their own error in place of the video. The client
      // previews by double-clicking, so say why. Never runs off file://.
      if (embed && location.protocol === "file:") {
        node = document.createElement("div");
        node.className = "gb-reel__offline";
        node.setAttribute("data-reel-node", "");
        var msg = document.createElement("span");
        msg.textContent = "Hosted video cannot play from a local file.";
        var link = document.createElement("a");
        link.className = "gb-reel__offline-link";
        link.href = src;
        link.target = "_blank";
        link.rel = "noopener";
        link.textContent = "Open it in a new tab";
        node.appendChild(msg);
        node.appendChild(link);
      } else if (embed) {
        node = document.createElement("iframe");
        node.className = "gb-reel__embed";
        node.setAttribute("data-reel-node", "");
        node.title = "Customer reel";
        node.allow = "autoplay; encrypted-media; picture-in-picture";
        node.setAttribute("allowfullscreen", "");
        node.src = embed;
      } else {
        node = document.createElement("video");
        node.className = "gb-reel__video";
        node.setAttribute("data-reel-node", "");
        node.playsInline = true;
        node.controls = true;
        node.setAttribute("aria-label", trigger.getAttribute("aria-label") || "Customer reel");
        node.src = src;
      }

      trigger.hidden = true;
      card.classList.add("is-playing");
      card.appendChild(node);
      if (node.tagName === "VIDEO") {
        // Inside the click's gesture, so audio is allowed; a refusal still rejects
        // and must not surface as an unhandled rejection.
        var pr = node.play();
        if (pr && pr.catch) { pr.catch(function () {}); }
      }
    },

    // One at a time: ten cards playing at once is ten audio tracks.
    stopAll: function (except) {
      var open = document.querySelectorAll("[data-reel].is-playing");
      for (var i = 0; i < open.length; i++) {
        if (open[i] === except) { continue; }
        this.stop(open[i]);
      }
    },

    stop: function (card) {
      var node = card.querySelector("[data-reel-node]");
      if (!node) { return; }
      // Pausing first stops the audio in the same frame the node goes away; for the
      // iframe, removing it is the only way to stop a third-party player.
      if (node.tagName === "VIDEO") {
        node.pause();
        node.removeAttribute("src");
        node.load();
      }
      card.removeChild(node);
      card.classList.remove("is-playing");
      var trigger = card.querySelector("[data-reel-play]");
      if (trigger) { trigger.hidden = false; }
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
   * accordion — jQuery-style slideUp/slideDown, one open row per group.
   *
   * The element stays a native <details>: open/close, keyboard and the a11y tree
   * are the browser's, and a dead main.js still opens rows (round 13 shipped a
   * JS+grid version that reported as "does not open at all" when the script did
   * not land). This module only replaces the ANIMATION and the exclusivity.
   *
   * Why not ::details-content: Safari < 18.4 has no such pseudo-element, so the
   * CSS slide simply does not run there. Animating .gb-acc-body's own box gives
   * every browser the same motion. The stylesheet keeps the CSS slide behind
   * `html:not(.js-acc)` -- this module sets .js-acc, so if it never runs the CSS
   * one is still there.
   * ------------------------------------------------------------------- */
  /* Live renders these rows from blocks/_gb-accordion-row.liquid, which emits no
   * name=, so nothing there is exclusive. One group per accordion container; the
   * static build already ships the attribute and never enters this branch. */
  var ACC_HOSTS = ".gb-product__accordion, .gb-faq__list, .gb-faq-image__list";
  var ACC_MS = 400;                                  // jQuery's slideUp/slideDown default
  var ACC_EASE = "cubic-bezier(0.42, 0, 0.58, 1)";   // approximates jQuery's `swing`

  function nameAccordionGroups() {
    var hosts = document.querySelectorAll(ACC_HOSTS);
    for (var i = 0; i < hosts.length; i++) {
      var rows = hosts[i].querySelectorAll("details:not([name])");
      for (var j = 0; j < rows.length; j++) {
        rows[j].setAttribute("name", "gb-acc-" + i);
      }
    }
  }

  /* Height only. jQuery also animates the vertical padding, but here that moves
   * the copy DOWN as the row opens -- the box grows from the top while the text
   * is being pushed off the padding, which reads as a wobble. ::details-content
   * is already clipping, so a padding that never animates is never visible.
   * ⚠ Reads offsetHeight while open: the row must already be open when this is
   * called for a slideDown, or the target height is 0. */
  function accSlide(item, open) {
    var body = item.querySelector(".gb-acc-body");
    if (!body || !body.animate) { item.open = open; return; }
    if (item.gbAccAnim) { item.gbAccAnim.cancel(); }
    if (open) { item.open = true; }

    var end = body.offsetHeight + "px";
    body.style.overflow = "hidden";

    /* fill: forwards, and the row is shut BEFORE the fill is dropped. Without it
     * the closing animation ends, height falls back to auto for one frame while
     * ::details-content is still open, and the panel flashes back to full height
     * on its way out. */
    var anim = body.animate(
      [{ height: open ? "0px" : end }, { height: open ? end : "0px" }],
      { duration: prefersReduced() ? 0 : ACC_MS, easing: ACC_EASE, fill: "forwards" });
    item.gbAccAnim = anim;
    anim.onfinish = function () {
      if (!open) { item.open = false; }
      anim.cancel();
      body.style.overflow = "";
      item.gbAccAnim = null;
    };
  }

  function prefersReduced() {
    return matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  var accordion = {
    init: function () {
      nameAccordionGroups();
      var items = document.querySelectorAll(".gb-faq__item, .gb-product__acc-item");
      if (!items.length) { return; }
      document.documentElement.classList.add("js-acc");

      for (var i = 0; i < items.length; i++) {
        (function (d) {
          var row = d.querySelector("summary");
          if (!row) { return; }
          /* Park the group on a data attribute: with name= still on the element
           * the browser closes its siblings the instant `open` is set, which cuts
           * their slideUp off mid-flight. Without JS the attribute stays put and
           * native exclusivity keeps working. */
          var group = d.getAttribute("name");
          if (group) {
            d.setAttribute("data-acc-group", group);
            d.removeAttribute("name");
          }

          row.addEventListener("click", function (e) {
            e.preventDefault();
            var opening = !d.open;
            if (opening && group) {
              var sib = document.querySelectorAll('[data-acc-group="' + group + '"]');
              for (var j = 0; j < sib.length; j++) {
                if (sib[j] !== d && sib[j].open) { accSlide(sib[j], false); }
              }
            }
            accSlide(d, opening);
          });
        })(items[i]);
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
  var EMBED_ALLOW = "accelerometer; autoplay; clipboard-write; encrypted-media; " +
                    "gyroscope; picture-in-picture; web-share";

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
          self.open(document.getElementById(open.getAttribute("data-modal")), open);
          return;
        }
        if (t.closest("[data-modal-close]")) self.close();
      });

      document.addEventListener("keydown", function (e) {
        if (e.key !== "Escape" && e.key !== "Tab") { return; }
        // Not `current` alone: a dialog that arrived already open never set it.
        var el = self.current || self.showing();
        if (!el) { return; }
        if (e.key === "Escape") { self.close(); return; }
        self.trap(e, el);
      });

      this.tabs();
    },

    open: function (el, trigger) {
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
      var el = this.current || this.showing();
      if (!el) return;
      this.current = null;
      el.classList.remove("is-open");
      el.setAttribute("aria-hidden", "true");
      // The lock stays on until the exit has played. Dropping it here hands the
      // scrollbar back while the panel is still fully opaque, and this modal is
      // position:fixed -- its containing block is the viewport, which narrows by
      // the scrollbar width -- so the centred panel jumps sideways mid-fade.
      this.unlockAfter(modalExitMs(el), el);
      returnFocus(this.lastFocus);
    },

    // A dialog of ours that is on screen without having gone through open().
    // Two conditions, both load-bearing:
    //   [data-modal-close] inside -- the test for "ours to drive". The live cart
    //     drawer also ships is-open, but two of its three branches wire the
    //     overlay to the theme's own close command; adopting those would have us
    //     fight Horizon over the same drawer.
    //   getClientRects()          -- it has to actually be on screen. That same
    //     drawer sits inside a <dialog> that decides whether it shows, so the
    //     class alone would match a shut drawer and close something invisible.
    showing: function () {
      var all = document.querySelectorAll('[role="dialog"].is-open');
      for (var i = 0; i < all.length; i++) {
        if (all[i].querySelector("[data-modal-close]") && all[i].getClientRects().length) {
          return all[i];
        }
      }
      return null;
    },

    // A token rather than a stored timer id: open() can land inside the wait, and
    // the stale callback must not unlock the modal that replaced this one.
    unlockAfter: function (ms, el) {
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

    trap: function (e, el) {
      var f = (el || this.current).querySelectorAll(FOCUSABLE);
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
      // Runs before the open timer below, so the halo is in place the first
      // time the panel is painted -- inserting it later reflows the heading.
      inkSplit(el.querySelector(".gb-promo-panel__title"));
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
          // Client r96: with three cards a centred rail parks the first (and
          // the last) in the middle, leaving a card's worth of empty track at
          // one edge -- most visible right after `rewind` wraps round. This
          // pins the end slides to the track edges and leaves every interior
          // position centred, so the board's peek-each-side is unchanged.
          // Ignored above 767 where the breakpoint turns centring off.
          // ⚠ `&& !loop` keeps the four reels rails untouched: an endless rail
          // has no first or last slide, so the option only has side effects there.
          centeredSlidesBounds: centre && !loop,
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
        // ⚠ slideChange is not enough. Where the track holds only a little more
        // than fits -- the expert rail at 767, three 305px cards in 768 -- the
        // rail still moves but activeIndex never leaves 1, so the arrows stayed
        // live at both ends. transitionEnd fires on every settle, edge or not.
        sw.on("transitionEnd", sync);
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

      // Client r85: a rail whose cards already fit the track has nothing to
      // scroll, and `loop` has no room to wrap -- Swiper parks the set against
      // the left edge instead of centring it. Measured, not counted: the card
      // width is a vw ramp, so "enough cards" is a different number at every
      // viewport (four fit at 1440, no count fits at 390).
      // ⚠ loop rails only. `rewind` is built to dead-end at any count, and the
      // expert rail's three cards fit their track in the last 30px before it
      // becomes a grid -- going static there is a layout nobody asked for.
      var fits = function () {
        if (!loop) { return false; }
        var sl = track.querySelectorAll(".swiper-slide");
        if (!sl.length) { return false; }
        var total = 0;
        for (var i = 0; i < sl.length; i++) {
          total += sl[i].getBoundingClientRect().width;
        }
        var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
        return total + gap * (sl.length - 1) <= track.clientWidth;
      };

      // Rails that only exist below a breakpoint. matchMedia rather than
      // Swiper's own `breakpoints: {enabled: false}`: disabling leaves the loop
      // duplicates in the DOM, and above the threshold those show up as extra
      // grid cells.
      var mq = until > 0 ? matchMedia("(max-width: " + until + "px)") : null;
      var apply = function () {
        var railed = !mq || mq.matches;
        var stat = railed && fits();
        if (railed && !stat) { create(); } else { destroy(); }
        root.classList.toggle("is-static", stat);
      };
      if (mq) {
        if (mq.addEventListener) { mq.addEventListener("change", apply); }
        else if (mq.addListener) { mq.addListener(apply); }
      }
      // Width only: the mobile toolbar sliding away fires resize at the same
      // width, and tearing the rail down on that is a visible jump.
      var lastW = window.innerWidth;
      window.addEventListener("resize", function () {
        if (window.innerWidth === lastW) { return; }
        lastW = window.innerWidth;
        apply();
      });
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
      // ⚠ Not #enquiry: the theme's contact section suffixes every field id with
      // its own section id (enquiry-template--...__form), so that id only ever
      // existed on the static page. The name is the stable hook -- Shopify wraps
      // it as contact[...] and the static form posts it bare.
      var select = form.querySelector(
        'select[name="enquiry"], select[name="contact[enquiry]"]');
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
      // Variants that draw no box of their own, because something around them
      // already does: "bare" is the phone field's country code (.gb-field__phone
      // has the border), "inline" is the cart's delivery interval (it is a run of
      // text inside a sentence).
      var variant = native.getAttribute("data-select") || "";
      var boxless = variant === "bare" || variant === "inline";
      var aria = native.getAttribute("aria-label");

      var wrap = document.createElement("div");
      wrap.className = "gb-select" + (variant ? " gb-select--" + variant : "");
      native.parentNode.insertBefore(wrap, native);
      wrap.appendChild(native);
      native.classList.add("gb-select__native");
      native.setAttribute("tabindex", "-1");
      native.setAttribute("aria-hidden", "true");

      var btn = document.createElement("button");
      btn.type = "button";
      btn.id = id + "-button";
      btn.className = boxless ? "gb-select__button"
                              : "gb-field__input gb-field__input--select gb-select__button";
      btn.setAttribute("aria-haspopup", "listbox");
      btn.setAttribute("aria-expanded", "false");
      btn.setAttribute("aria-controls", id + "-list");
      btn.innerHTML =
        '<span class="gb-select__value"></span>' +
        '<svg class="gb-select__arrow" viewBox="0 0 20 20" fill="none" aria-hidden="true">' +
        // currentColor, not #4d4d4d: both existing triggers compute to that anyway
        // (.gb-field__input and --bare are both $c-gray-700), and the cart's
        // inline variant needs the chevron to follow its own blue.
        '<path d="M5 7.5L10 12.5L15 7.5" stroke="currentColor" stroke-width="1.667" ' +
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
      box.wrap.classList.remove("is-up");
      box.wrap.classList.add("is-open");
      box.btn.setAttribute("aria-expanded", "true");
      // AFTER move(): its scrollIntoView can scroll an ancestor out from under a
      // measurement taken before it. A list that would fall past whatever clips
      // it (the cart drawer's scroll area, else the viewport) opens upwards.
      this.move(box, box.native.selectedIndex);
      if (this.wouldOverflow(box)) { box.wrap.classList.add("is-up"); }
      box.list.focus();
    },

    // Where the list would end up, computed WITHOUT reading its own rect: the
    // entry transform is mid-flight at this point, so a rect here is short by
    // however much of the 4px slide is still to play. `top` resolves the
    // calc(100% + n) against the wrap, and offsetHeight ignores transforms.
    wouldOverflow: function (box) {
      var wrap = box.wrap.getBoundingClientRect();
      var top = parseFloat(getComputedStyle(box.list).top) || 0;
      return wrap.top + top + box.list.offsetHeight > this.clipBottom(box.wrap);
    },

    // Bottom edge of the nearest ancestor that actually clips, or the viewport.
    clipBottom: function (el) {
      for (var p = el.parentElement; p && p !== document.body; p = p.parentElement) {
        var o = getComputedStyle(p).overflowY;
        if (o !== "visible" && o !== "clip") {
          return Math.min(p.getBoundingClientRect().bottom, window.innerHeight);
        }
      }
      return window.innerHeight;
    },

    close: function (box, refocus) {
      if (!box.open) { return; }
      box.open = false;
      box.wrap.classList.remove("is-open");
      box.btn.setAttribute("aria-expanded", "false");
      box.list.removeAttribute("aria-activedescendant");
      if (refocus) { returnFocus(box.btn); }
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
    PREVENT: ".gb-product__thumbs, .gb-header__panel, .gb-header__panel-clip, .gb-nl-panel__body, .gb-select__list, .gb-cart__body, .gb-cart__empty, .gb-field__input--area, .gb-promo-panel",

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
        // Client r129: "weaker". easeOutExpo's long tail is what reads as drift,
        // and duration is how long that tail runs -- 1s -> 0.6s keeps the curve
        // (still smooth, not stepped) and cuts the coast. House value, no board.
        duration: 0.6,
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

  /* ---------------------------------------------------------------------
   * phoneCode — the phone placeholder's dial code follows the country select.
   *
   * Client r137: the country list grew from AU alone to six, and the placeholder
   * has to agree with whatever is picked -- dial code AND digit count.
   *
   * ⚠ Each option carries its own data-example, because the lengths genuinely
   * differ: SG is 8 digits, AU 9, US/CA/GB 10. r137 shipped with one shared tail
   * (the board's AU "400 000 000") behind every dial code, which was wrong for
   * four of the six -- US/CA/GB a digit short, SG a digit over, and NZ has no
   * 400 range at all. Numbers are real prefixes with zeroed tails, the way the
   * board writes AU; US/CA use 555, the North American range reserved for
   * fiction, so no placeholder points at a live line.
   *
   * ⚠ Bound to the NATIVE select, not to our widget: selectBox syncs
   * native.selectedIndex and fires a bubbling change on every pick, so this one
   * hook covers the custom list, the native fallback when JS builds no widget,
   * and browser autofill.
   * ⚠ US and CA are both +1. That is correct, not a copy-paste slip.
   * ------------------------------------------------------------------- */
  var phoneCode = {
    init: function () {
      var selects = document.querySelectorAll("[data-phone-code]");
      for (var i = 0; i < selects.length; i++) { this.bind(selects[i]); }
    },

    bind: function (select) {
      var field = select.closest(".gb-field__phone");
      var input = field && field.querySelector('input[type="tel"]');
      if (!input) { return; }
      // Captured once, before anything rewrites it: the number pattern the board
      // drew, minus its dial code. Only a fallback now -- an option without its
      // own data-example keeps whatever the markup shipped with.
      var rest = (input.getAttribute("placeholder") || "").replace(/^\+\d+\s*/, "");
      var apply = function () {
        var opt = select.options[select.selectedIndex];
        var dial = opt && opt.getAttribute("data-dial");
        if (!dial) { return; }
        var example = opt.getAttribute("data-example") || rest;
        input.setAttribute("placeholder", example ? dial + " " + example : dial);
      };
      select.addEventListener("change", apply);
      apply();
    }
  };

  /* ---------------------------------------------------------------------
   * scrollbarProbe — keeps --scrollbar-w current for locks we do not open.
   *
   * modal.open() and header.set() measure the bar themselves right before they
   * lock. The live cart drawer is opened by Horizon, whose lockScroll() lands in
   * the same synchronous block as showModal() -- any observer of ours fires
   * after the page is already locked, where the reading is 0. So cache the
   * width whenever the page is demonstrably unlocked instead.
   * Static pages: harmless, it writes the value the other two would.
   * ------------------------------------------------------------------- */
  var scrollbarProbe = {
    init: function () {
      var self = this;
      this.measure();
      window.addEventListener("resize", function () { self.measure(); });
    },

    measure: function () {
      var de = document.documentElement;
      // A locked page reports no bar; keep the last good value rather than 0.
      if (de.hasAttribute("scroll-lock")) { return; }
      if (getComputedStyle(de).overflowY === "hidden") { return; }
      de.style.setProperty("--scrollbar-w", (window.innerWidth - de.clientWidth) + "px");
    }
  };

  /* ---------------------------------------------------------------------
   * cartDrawer — resync a drawer the theme rendered already open.
   *
   * /cart ships it expanded by putting `open` on the inner <dialog>, but
   * <theme-drawer>'s own open attribute stays unset. Its close() guards on that
   * attribute, so the close button and the overlay -- both wired to
   * `#cart-drawer/close` -- do nothing until something toggles it once. Escape
   * still works because that is the dialog's native path, which skips the
   * component. Handing the component the state it is missing costs no repaint:
   * the panel does not move (measured over a full second).
   * ------------------------------------------------------------------- */
  var cartDrawer = {
    init: function () {
      var self = this;
      this.guardInitialFocus();
      this.watchSplit();
      // Attribute callbacks only exist once the element is upgraded, and the
      // theme's own setup should land first -- whenDefined resolves right away
      // if it already is, so the frame is what actually orders us after it.
      var run = function () {
        requestAnimationFrame(function () { self.resync(); });
      };
      if (window.customElements && customElements.whenDefined) {
        customElements.whenDefined("theme-drawer").then(run, run);
      } else { run(); }
    },

    /* resync() above samples ONCE, so it only ever catches a drawer that is
       already open by the time we run. The drawer can also be opened later and
       from outside the component: /cart is a redirect to /#open-cart, and
       gb-cart-scripts' handler for that hash does

         if (typeof drawer.showDialog === 'function') { drawer.showDialog(); }
         else { drawer.querySelector('dialog').showModal(); }   // always exists

       so whenever <theme-drawer> has not upgraded yet it takes the second branch,
       opens the native dialog behind the component's back and never retries. The
       panel is then visibly open while the component still reads closed, and
       on:click="#cart-drawer/close" no-ops on BOTH the close button and the
       overlay -- only Escape works, which is the signature of the split.

       ⚠ Watch the attribute, do not sample it: which branch that handler takes is
       a race against custom-element upgrade, so the split appears on some loads
       and not others. subtree covers a dialog swapped in later (the empty-cart
       template is injected at runtime). resync() is idempotent, so the write we
       trigger here settles on the next callback instead of looping. */
    watchSplit: function () {
      var host = document.getElementById("cart-drawer");
      if (!host || !window.MutationObserver) { return; }
      var self = this;
      new MutationObserver(function () { self.resync(); }).observe(host, {
        attributes: true, attributeFilter: ["open"], subtree: true
      });
    },

    /* The drawer is Horizon's <dialog>, so the [role=dialog][tabindex=-1] rule
       that keeps OUR modals from ringing their close button never reaches it:
       showModal() hands initial focus to the first focusable child, which is
       .gb-cart__close. Landing straight on /cart opens the drawer during load,
       so that focus has no user gesture behind it -- the drawer appears with its
       close control looking selected. Mark it the way returnFocus marks a
       handed-back focus (r121); a real key or blur clears the mark.
       ⚠ Armed only until the first real input. After that, focus landing there
       is the user's own doing and has to keep its ring -- a keyboard user who
       tabs to this button must still see where they are. */
    guardInitialFocus: function () {
      var armed = true;
      var types = ["keydown", "pointerdown", "touchstart"];
      var disarm = function () {
        armed = false;
        for (var j = 0; j < types.length; j++) {
          document.removeEventListener(types[j], disarm, true);
        }
      };
      for (var i = 0; i < types.length; i++) {
        document.addEventListener(types[i], disarm, true);
      }

      var mark = function (node) {
        var btn = node && node.closest ? node.closest(".gb-cart__close") : null;
        if (btn) { markRefocused(btn); }
      };
      // The theme can open and focus the drawer before this file even parses.
      mark(document.activeElement);
      document.addEventListener("focusin", function (e) {
        if (armed) { mark(e.target); }
      }, true);
    },

    resync: function () {
      var host = document.getElementById("cart-drawer");
      if (!host) return;
      var dialog = host.querySelector("dialog");
      // Act on the split state only. A drawer that starts shut, or one the
      // theme opens itself later, already has both halves in step.
      if (!dialog || !dialog.open || host.hasAttribute("open")) { return; }
      host.setAttribute("open", "");
    }
  };

  function ready(fn) {
    if (document.readyState !== "loading") { fn(); }
    else { document.addEventListener("DOMContentLoaded", fn); }
  }

  ready(function () {
    // One IIFE, ten modules: without a boundary the first throw takes every
    // module after it with it, silently -- the page renders and simply stops
    // responding from that point on. Failing one module is the smaller loss.
    var modules = [["scrollbarProbe", scrollbarProbe], ["cartDrawer", cartDrawer],
                   ["wowo", wowo], ["header", header], ["bearMeter", bearMeter],
                   ["packBand", packBand],
                   ["popText", popText], ["countUp", countUp], ["lineReveal", lineReveal], ["modal", modal], ["promoModal", promoModal],
                   ["slider", slider], ["gallery", gallery], ["accordion", accordion],
                   ["reelPlayer", reelPlayer],
                   ["smoothScroll", smoothScroll], ["enquiryPrefill", enquiryPrefill],
                   ["selectBox", selectBox], ["phoneCode", phoneCode]];
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
                  selectBox: selectBox, phoneCode: phoneCode, scrollbarProbe: scrollbarProbe,
                  cartDrawer: cartDrawer, reelPlayer: reelPlayer };
})();

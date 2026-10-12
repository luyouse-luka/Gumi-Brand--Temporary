(function () {
  'use strict';

  /* Height animation shared by the FAQ rows and the password form. 400ms and a
   * swing approximation are what main.js runs the site accordions on, so the two
   * read as the same control. The resting height stays in CSS: apply() flips the
   * class, this reads the height either side of it and animates between them.
   * ⚠ prefers-reduced-motion has to be checked here -- customstyle's blanket rule
   * flattens CSS transitions, not the Web Animations API.
   */
  var SLIDE_MS = 400;
  var SLIDE_EASE = 'cubic-bezier(0.42, 0, 0.58, 1)';

  function slideTo(el, apply) {
    var start = el.offsetHeight;
    // The shut state is visibility:hidden so it is neither read aloud nor
    // tabbable; hold it visible for the length of the animation only.
    el.style.visibility = 'visible';
    apply();
    var end = el.offsetHeight;
    var clear = function () { el.style.visibility = ''; };
    if (!el.animate || start === end) { clear(); return; }
    if (el.gbSlide) el.gbSlide.cancel();
    var ms = matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : SLIDE_MS;
    var anim = el.animate([{ height: start + 'px' }, { height: end + 'px' }],
                          { duration: ms, easing: SLIDE_EASE });
    el.gbSlide = anim;
    anim.onfinish = function () { clear(); el.gbSlide = null; };
  }

  var accountList = {
    init: function () {
      document.querySelectorAll('.gb-acct-list__link').forEach(function (link) {
        if (link.querySelector('.gb-acct-list__arrow')) return;
        link.insertAdjacentHTML('beforeend', '<svg class="gb-acct-list__arrow" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M8.33398 15L13.334 10L8.33398 5" stroke="#1A1A1A" stroke-width="1.66667" stroke-linecap="round" stroke-linejoin="round"/></svg>');
      });
    }
  };

  var accountVideo = {
    init: function () {
      document.querySelectorAll('.gb-acct-video').forEach(function (root) {
        var video = root.querySelector('video');
        if (!video) return;
        video.controls = false;
        root.removeAttribute('role');
        var old = root.querySelector('.gb-acct-video__play');
        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'gb-acct-video__play';
        button.setAttribute('data-acct-video-toggle', '');
        button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="188.869 426.914 13.7434 15.4545" fill="none" aria-hidden="true"><path d="M201.935 433.469C202.838 433.99 202.838 435.293 201.935 435.814L190.9 442.185C189.998 442.706 188.869 442.055 188.869 441.012L188.869 428.27C188.869 427.228 189.998 426.576 190.9 427.097L201.935 433.469Z" fill="#011307"/></svg>';
        if (old) old.replaceWith(button);
        else root.appendChild(button);
        function sync() {
          var playing = !video.paused && !video.ended;
          root.classList.toggle('is-playing', playing);
          button.setAttribute('aria-label', playing ? 'Pause video' : 'Play video');
        }
        function toggle() {
          if (!video.paused) video.pause();
          else {
            var pending = video.play();
            if (pending && pending.catch) pending.catch(sync);
          }
        }
        button.addEventListener('click', toggle);
        video.addEventListener('click', toggle);
        ['play', 'pause', 'ended', 'error'].forEach(function (event) { video.addEventListener(event, sync); });
        sync();
      });
    }
  };

  var accountMenu = {
    init: function () {
      var menu = document.querySelector('[data-acct-menu]');
      if (!menu) return;
      var root = menu.parentElement;
      var icon = root.querySelector('svg');
      if (!icon) return;
      menu.hidden = false;
      var button = document.createElement('button');
      button.type = 'button';
      button.setAttribute('data-acct-menu-toggle', '');
      button.setAttribute('aria-label', 'Account menu');
      button.setAttribute('aria-expanded', 'false');
      menu.id = menu.id || 'acct-menu';
      button.setAttribute('aria-controls', menu.id);
      root.insertBefore(button, icon);
      button.appendChild(icon);
      function closeSiteMenu() {
        var header = window.gumi && window.gumi.header;
        if (header && header.el) header.set(false);
      }
      root.addEventListener('mouseenter', closeSiteMenu);
      function setOpen(open) {
        if (open) closeSiteMenu();
        root.toggleAttribute('data-acct-menu-open', open);
        button.setAttribute('aria-expanded', String(open));
      }
      button.addEventListener('click', function () {
        setOpen(!root.hasAttribute('data-acct-menu-open'));
      });
      document.addEventListener('click', function (e) {
        if (!root.contains(e.target) || e.target.closest('[data-acct-goto]')) setOpen(false);
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && root.hasAttribute('data-acct-menu-open')) {
          setOpen(false);
          button.focus();
        }
      });
      document.addEventListener('focusin', function (e) {
        if (!root.contains(e.target)) setOpen(false);
      });
    }
  };

  var view = {
    init: function () {
      if (!document.querySelector('[data-acct-view]')) return;   // not on this page
      // Live Liquid has the structural class but may omit the static-page hook.
      // Register it before the first swap so both JS and CSS use the same shell.
      var shell = document.querySelector('.gb-acct .gb-acct__views');
      if (shell) shell.setAttribute('data-acct-views', '');
      var self = this;

      document.addEventListener('click', function (e) {
        var t = e.target.closest && e.target.closest('[data-acct-goto]');
        if (!t || t.getAttribute('aria-disabled') === 'true') return;
        e.preventDefault();
        self._subState(t);
        self.show(t.getAttribute('data-acct-goto'), true);
      });

      window.addEventListener('hashchange', function () {
        self.show(location.hash.slice(1), true);
      });
      window.addEventListener('resize', function () { self._endLeave(); });

      // first paint must not animate -- the page has no entry motion otherwise
      this.show(location.hash.slice(1));
    },

    show: function (name, animate) {
      var views = document.querySelectorAll('[data-acct-view]');
      var found = false;
      var shown = null;
      var prev = null;
      var i;
      var shell = document.querySelector('[data-acct-views]');
      var swapHeight = shell ? shell.getBoundingClientRect().height : 0;
      // a second click during an exit must not leave two views on screen
      this._endLeave();
      for (i = 0; i < views.length; i++) {
        if (!views[i].hidden) prev = views[i];
      }
      for (i = 0; i < views.length; i++) {
        var match = views[i].getAttribute('data-acct-view') === name;
        views[i].hidden = !match;
        views[i].inert = !match;
        if (match) { found = true; shown = views[i]; }
      }
      // Unknown hash falls back to the first view in the DOM, not a hard-coded
      // name: the auth page has no 'overview' and would recurse until the stack blew.
      if (!views.length) return;
      if (!found) { this.show(views[0].getAttribute('data-acct-view'), animate); return; }
      // Phone account views cover the old content before the shell changes
      // height. Desktop/auth retain their existing one-shot entry animation.
      if (animate && shown && prev !== shown) {
        if (prev && shell && shown.parentElement === shell &&
            matchMedia('(max-width: 767px)').matches &&
            !matchMedia('(prefers-reduced-motion: reduce)').matches) {
          this._cover(prev, shown, shell, swapHeight);
        } else {
          if (prev) this._leave(prev);
          this._enter(shown);
        }
      }

      var links = document.querySelectorAll('[data-acct-goto]');
      for (i = 0; i < links.length; i++) {
        var on = links[i].getAttribute('data-acct-goto') === name;
        links[i].classList.toggle('is-current', on);
        if (on) links[i].setAttribute('aria-current', 'page');
        else links[i].removeAttribute('aria-current');
      }

      if (location.hash.slice(1) !== name) {
        history.replaceState(null, '', '#' + name);
      }
      window.scrollTo(0, 0);
    },

    // note 28323: the three list cards share one detail view, so the card that
    // was clicked is what decides which state that view opens in.
    _subState: function (trigger) {
      var card = trigger.closest('.gb-acct-sub[data-acct-sub-state]');
      var detail = document.querySelector('.gb-acct-detail');
      if (!card || !detail) return;
      detail.setAttribute('data-acct-sub-state', card.getAttribute('data-acct-sub-state'));
    },

    // display:none cannot transition, so the outgoing view is unhidden again for
    // the length of one exit animation. CSS takes it out of flow, but only inside
    // [data-acct-views] -- the auth page's two <main>s sit above a footer that
    // would jump, so there the plain hide above is the whole swap.
    _leave: function (el) {
      var self = this;
      if (!el.closest('[data-acct-views]')) return;
      el.hidden = false;
      el.classList.add('is-leaving');
      var stop = function (e) {
        if (e && e.target !== el) return;       // animationend bubbles
        clearTimeout(timer);
        el.removeEventListener('animationend', stop);
        el.classList.remove('is-leaving');
        el.hidden = true;
        if (self._leaving === stop) self._leaving = null;
      };
      // a dropped animation never fires animationend, and a stranded view would
      // cover the page for good
      var timer = setTimeout(stop, 1000);
      el.addEventListener('animationend', stop);
      this._leaving = stop;
    },

    _endLeave: function () { if (this._leaving) this._leaving(); },

    _cover: function (old, next, shell, previousHeight) {
      var self = this;
      var targetHeight = next.getBoundingClientRect().height;
      var height = Math.max(previousHeight, targetHeight);
      var shrink = null;
      var timer;
      var revealed = false;
      old.hidden = false;
      old.classList.add('is-leaving');
      shell.style.height = height + 'px';
      next.style.minHeight = '100%';
      next.classList.add('is-covering');
      void next.offsetWidth;
      next.classList.add('is-entering');
      var style = getComputedStyle(next);
      var duration = parseFloat(style.animationDuration) * 1000;
      var easing = style.animationTimingFunction;

      function finish() {
        clearTimeout(timer);
        next.removeEventListener('animationend', reveal);
        if (shrink) shrink.cancel();
        old.hidden = true;
        old.classList.remove('is-leaving');
        next.classList.remove('is-entering', 'is-covering');
        next.style.minHeight = '';
        shell.style.height = '';
        if (self._leaving === finish) self._leaving = null;
      }

      function reveal(e) {
        if (e && e.target !== next) return;
        if (revealed) return;
        revealed = true;
        clearTimeout(timer);
        old.hidden = true;
        old.classList.remove('is-leaving');
        next.classList.remove('is-entering');
        // The full-height cover remains opaque while the shell settles.
        if (height > targetHeight + 1 && shell.animate) {
          shrink = shell.animate([{ height: height + 'px' }, { height: targetHeight + 'px' }],
                                 { duration: duration, easing: easing, fill: 'forwards' });
          shrink.onfinish = finish;
          timer = setTimeout(finish, duration + 200);
        } else finish();
      }

      next.addEventListener('animationend', reveal);
      timer = setTimeout(reveal, duration + 200);
      this._leaving = finish;
    },

    _enter: function (el) {
      el.classList.remove('is-entering');
      void el.offsetWidth;                       // restart, or a fast re-click plays nothing
      el.classList.add('is-entering');
      var done = function () {
        el.classList.remove('is-entering');
        el.removeEventListener('animationend', done);
      };
      el.addEventListener('animationend', done);
    }
  };

  /* acctForm — note 2284:27446: Save stays asleep until the form above it has
   * actually been changed. Panels with nothing to change (the confirm-only ones)
   * have no [data-acct-field] and are left alone, which is also how their boards
   * draw them: green, not #e6e6e6.
   */
  var acctForm = {
    // Panels are armed by modal.open(); a form living straight on a page has
    // nobody to arm it, so it is picked up here instead.
    init: function () {
      var forms = document.querySelectorAll('[data-acct-form]');
      if (!forms.length) return;                 // not on this page
      for (var i = 0; i < forms.length; i++) this.watch(forms[i]);
    },

    watch: function (panel) {
      var save = panel.querySelector('[data-acct-save]');
      var fields = panel.querySelectorAll('[data-acct-field]');
      // 34351 draws restart's Save green while 31976's identical-looking one is
      // grey, so the exception is spelled out on the panel rather than hidden in
      // a missing data-acct-field.
      if (panel.hasAttribute('data-acct-save-ungated')) return;
      // ⚠ The once-only flag is a property, never an attribute: the Shopify
      // templates are transcribed from rendered DOM, and an attribute written
      // here comes back in the markup and turns this guard into a hard return.
      if (!save || !fields.length || panel._acctQtyOwned) return;
      panel._acctInitial = this._snapshot(fields, panel);
      save.disabled = true;
      if (panel._acctWatched) return;
      panel._acctWatched = true;
      var self = this;
      function sync(e) {
        if (panel._acctQtyOwned) return;
        var currentFields = panel.querySelectorAll('[data-acct-field]');
        var quantities = panel.querySelectorAll('input[data-acct-qty-value]');
        var valid = true;
        for (var i = 0; i < quantities.length; i++) {
          if (!quantities[i].value || !quantities[i].checkValidity()) valid = false;
        }
        save.disabled = !valid || self._snapshot(currentFields, panel) === panel._acctInitial;
      }
      panel.addEventListener('input', sync);
      // A <select> fires change, not input, in older engines; listening to both
      // costs nothing and the comparison is idempotent.
      panel.addEventListener('change', sync);
    },

    _snapshot: function (fields, panel) {
      var v = [];
      for (var i = 0; i < fields.length; i++) {
        var f = fields[i];
        // A radio's value is a constant; what changes is which one is picked.
        v.push(f.type === 'radio' || f.type === 'checkbox' ? (f.checked ? '1' : '0') : f.value);
      }
      // Quantity controls also participate in dirty checking.
      var q = panel ? panel.querySelectorAll('[data-acct-qty-value]') : [];
      for (var k = 0; k < q.length; k++) v.push(q[k].value == null ? q[k].textContent : q[k].value);
      return v.join('\u0000');
    }
  };

  /* acctDiscount — Apply follows the field and nothing else.
   *
   * ⚠ note 30919: a green Apply is not a claim that the code exists. Whether it
   * does is the back end's answer; all this decides is that something was typed.
   */
  var acctDiscount = {
    bind: function (panel) {
      var input = panel.querySelector('[data-acct-discount-input]');
      var apply = panel.querySelector('[data-acct-apply]');
      if (!input || !apply || panel._acctDiscountBound) return;   // property, see acctForm.watch
      panel._acctDiscountBound = true;
      function sync() { apply.disabled = !input.value.trim(); }
      input.addEventListener('input', sync);
      sync();

      // Applied state and success chips belong to the server response.
    }
  };

  /* cancelFlow — the reason screen is the only branching one (note 34512).
   *
   * Boards 29928 and 30286 pick the two reasons that have a second screen and
   * draw the CTA "Continue"; 30107 picks a terminal one and draws it "Cancel".
   * So the button says what pressing it will do, and BRANCH is the whole rule.
   */
  var cancelFlow = {
    BRANCH: {
      'going-away': 'cancel-holiday',
      'too-expensive': 'cancel-discount'
    },

    init: function () {
      var root = document.querySelector('[data-acct-reasons]');
      if (!root) return;
      var cta = root.closest('.gb-acct-modal').querySelector('[data-acct-cta]');
      if (!cta) return;
      var self = this;
      root.addEventListener('change', function () { self.sync(root, cta); });
      this.sync(root, cta);
    },

    sync: function (root, cta) {
      var picked = root.querySelector('[data-acct-reason]:checked');
      cta.disabled = !picked;
      var next = picked ? this.BRANCH[picked.value] : null;
      cta.textContent = next || !picked ? 'Continue' : 'Cancel';
      if (next) {
        cta.setAttribute('data-acct-modal', next);
        cta.removeAttribute('data-acct-modal-close');
      } else {
        cta.removeAttribute('data-acct-modal');
        // note 34516 is the back end's job; here the flow simply ends
        if (picked) cta.setAttribute('data-acct-modal-close', '');
        else cta.removeAttribute('data-acct-modal-close');
      }
    }
  };

  /* acctCal — 30465's date picker, drawn by flatpickr (the same plugin the
   * funkyfood portal uses) and skinned to the board in account.scss.
   *
   * ⚠ The board's own grid cannot be copied: 1 July 2026 is a Wednesday but the
   * board puts it under Su, and one cell reads "32". Only the tokens are the
   * board's; the month comes from the plugin.
   *
   * note 30923: the resume day has to be a whole future day, so today and
   * everything before it is out and the first selectable day is tomorrow.
   */
  var acctCal = {
    // flatpickr indexes weekdays from Sunday and firstDayOfWeek only rotates
    // what is shown, so this list has to start at Su to come out Mo..Su.
    // 'Sat' is the board's own odd spelling.
    DAYS: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sat'],
    MONTHS: ['January', 'February', 'March', 'April', 'May', 'June', 'July',
             'August', 'September', 'October', 'November', 'December'],
    MONTHS_SHORT: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                   'Sep', 'Oct', 'Nov', 'Dec'],
    PREV: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="54 402 20 20" fill="none" aria-hidden="true"><path d="M66.5 417L61.5 412L66.5 407" stroke="currentColor" stroke-width="1.67" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    NEXT: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="316 402 20 20" fill="none" aria-hidden="true"><path d="M323.5 417L328.5 412L323.5 407" stroke="currentColor" stroke-width="1.67" stroke-linecap="round" stroke-linejoin="round"/></svg>',

    init: function () {
      var roots = document.querySelectorAll('[data-acct-cal]');
      if (!roots.length) return;                          // not on this page
      if (typeof flatpickr !== 'function') return;        // plugin did not load
      var today = new Date();
      today.setHours(0, 0, 0, 0);
      var min = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1);
      for (var i = 0; i < roots.length; i++) this._arm(roots[i], min);
    },

    _arm: function (root, min) {
      var self = this;
      // ⚠ The Shopify template pre-renders a calendar shell for the paint before
      // the plugin loads. flatpickr appends its own instead of adopting it, so
      // without this the modal shows two.
      var shell = root.querySelector('.flatpickr-calendar');
      if (shell) shell.remove();
      // data-acct-cal-for names the input this calendar fills. The holiday panel
      // drives no field, so it carries an input of its own for flatpickr to bind.
      var input = this._field(root) || root.querySelector('[data-acct-cal-input]');
      if (!input) return;
      var from = this._parse(input.value);
      // ⚠ A field whose date has already passed (the boards ship 19/07/2026)
      // selects nothing; minDate then opens the view on the first month that
      // has a live day. Clamping the selection to tomorrow instead would show a
      // highlighted day the field disagrees with. A calendar with no field of
      // its own (the holiday panel) has nothing to disagree with, so it opens
      // on the first selectable day -- board 30669 fills exactly one.
      var picked = from ? (from >= min ? from : null) : new Date(min.getTime());

      root._fp = flatpickr(input, {
        inline: true,
        appendTo: root,
        // ⚠ flatpickr sets readonly on the input without this, and anything that
        // fills the field -- a probe, autofill -- hangs on it.
        allowInput: true,
        dateFormat: 'd/m/Y',
        minDate: min,
        defaultDate: picked,
        // a <select> here would not read as the board's one-line "July 2026"
        monthSelectorType: 'static',
        prevArrow: this.PREV,
        nextArrow: this.NEXT,
        locale: {
          firstDayOfWeek: 1,
          weekdays: { shorthand: this.DAYS, longhand: this.DAYS },
          months: { shorthand: this.MONTHS_SHORT, longhand: this.MONTHS }
        },
        // ⚠ Save is gated on a value snapshot; the plugin fires input and
        // change on the field itself, which acctForm already listens for, so
        // nothing needs re-dispatching here. acct38check pins that it still does.
        onReady: function (dates, str, fp) {
          // Month navigation updates the year without opening a mobile keyboard.
          fp.currentYearElement.readOnly = true;
          fp.currentYearElement.setAttribute('inputmode', 'none');
          fp.currentYearElement.tabIndex = -1;
          // The plugin draws its month arrows as bare spans.
          self._label(fp.prevMonthNav, 'Previous month');
          self._label(fp.nextMonthNav, 'Next month');
        }
      });

      // The calendar drops out of the field on click; the shut state is CSS
      // behind .acct-live, so this only flips the class.
      if (root.classList.contains('gb-acct-cal--field')) {
        input.addEventListener('click', function () {
          slideTo(root, function () { root.classList.toggle('is-open'); });
        });
      }
    },

    _label: function (el, text) {
      if (!el) return;
      el.setAttribute('role', 'button');
      el.setAttribute('tabindex', '0');
      el.setAttribute('aria-label', text);
      el.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
      });
    },

    _field: function (root) {
      var id = root.getAttribute('data-acct-cal-for');
      return id ? document.getElementById(id) : null;
    },

    _parse: function (value) {
      var m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/.exec((value || '').trim());
      return m ? new Date(+m[3], +m[2] - 1, +m[1]) : null;
    }
  };

  /* modal — every [data-acct-modal] opens the panel of the same name.
   *
   * The lock reuses the site's own is-modal-open rather than a second class of
   * ours. customstyle.scss already solves two traps here and a parallel lock
   * would have to solve them again: body must get overflow-x:clip /
   * overflow-y:visible (hidden makes body the sticky header's scrollport and
   * .gb-acct-header drops out of view), and the freed scrollbar width must be
   * padded back on html ONLY (paying it on both spends it twice).
   *
   * ⚠ The class alone does NOT lock the page. Lenis owns the wheel site-wide and
   * scrolls by calling window.scrollTo, which overflow:hidden does not stop --
   * so it has to be handed back to native for as long as a panel is open, the
   * same call main.js makes for its own modals. Probing this needs
   * prefers-reduced-motion at no-preference: under `reduce` smoothScroll.init()
   * returns early, Lenis never runs and the missing pause reads green.
   *
   * ⚠ main.js also drives is-modal-open for [data-modal]. account.html has no
   * [data-modal] trigger, so the two never hold the lock at once; if one is ever
   * added here, whichever closes first would unlock the other.
   */
  // main.js may be absent or may have thrown before its export landed.
  function smoothScroll(method) {
    var s = window.gumi && window.gumi.smoothScroll;
    if (s && typeof s[method] === 'function') s[method]();
  }

  var modal = {
    _last: null,

    init: function () {
      var self = this;
      // Armed up front, not on first open: the board ships Save greyed out, so
      // it has to be disabled before the panel is ever shown.
      var panels = document.querySelectorAll('.gb-acct-modal');
      for (var i = 0; i < panels.length; i++) {
        acctForm.watch(panels[i]);
        acctDiscount.bind(panels[i]);
      }
      window.addEventListener('resize', function () {
        var open = document.querySelector('.gb-acct-modal.is-open');
        if (open) self._fit(open);
      });
      document.addEventListener('click', function (e) {
        if (!e.target.closest) return;
        if (e.target.closest('[data-acct-apply]')) return;
        var open = e.target.closest('[data-acct-modal]');
        if (open) {
          e.preventDefault();
          self.open(open.getAttribute('data-acct-modal'), open);
          return;
        }
        if (e.target.closest('[data-acct-modal-close]')) { e.preventDefault(); self.close(); }
      });
      // Nothing here posts anywhere. A panel is a <form> so that Save runs the
      // browser's own required/pattern checks first -- submit is the only event
      // that fires after they pass, which is why the chain hangs off it and not
      // off the button's click.
      document.addEventListener('submit', function (e) {
        e.preventDefault();
        var next = e.target.getAttribute('data-acct-modal-next');
        if (next) self.open(next);
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && self.isOpen()) { e.preventDefault(); self.close(); }
        else if (e.key === 'Tab' && self.isOpen()) self._trap(e);
      });
    },

    isOpen: function () { return !!document.querySelector('.gb-acct-modal.is-open'); },

    panel: function (name) {
      return document.querySelector('.gb-acct-modal[data-acct-modal-panel="' + name + '"]');
    },

    open: function (name, trigger) {
      var el = this.panel(name);
      if (!el) return;                                  // panel not built yet
      clearTimeout(el._acctHideTimer);
      if (el.classList.contains('is-open')) return;
      acctForm.watch(el);
      var already = this.isOpen();
      if (already) this._hide(document.querySelector('.gb-acct-modal.is-open'));
      this._last = trigger || this._last;
      // Measure while the scrollbar is still on screen, and only the first time:
      // the cancel flow swaps content inside one open panel, and a second
      // measurement would read 0 and wipe the compensation already applied.
      if (!document.documentElement.classList.contains('is-modal-open')) {
        var sbw = window.innerWidth - document.documentElement.clientWidth;
        document.documentElement.style.setProperty('--scrollbar-w', sbw + 'px');
        document.documentElement.classList.add('is-modal-open');
        document.body.classList.add('is-modal-open');
        smoothScroll('pause');
      }
      el.hidden = false;
      this._fit(el);
      void el.offsetWidth;                              // reflow, or the entry has nothing to run from
      el.classList.add('is-open');
      el.setAttribute('aria-hidden', 'false');
      // The dialog itself takes focus, not its first control: a scripted focus
      // with no pointer input before it still counts as :focus-visible, so the
      // ring would be painted the moment the panel appears.
      el.querySelector('.gb-acct-modal__panel').focus({ preventScroll: true });
    },

    // ⚠ A body that does not actually overflow has to stop being a clip box.
    // main.js's selectBox opens a dropdown upwards when it would fall past the
    // nearest clipping ancestor, and overflow-y:auto clips whether or not it
    // scrolls -- so every select in a short panel flipped up against its own
    // label. A body that really does scroll keeps auto and its dropdowns keep
    // flipping, which is right: down would be clipped.
    _fit: function (el) {
      var body = el.querySelector('.gb-acct-modal__body');
      if (!body) return;
      body.setAttribute('data-lenis-prevent', '');
      body.style.overflowY = '';        // measure as authored, not as last set
      // ⚠ Not scrollHeight: every closed .gb-select keeps its absolutely
      // positioned list in that number, so a panel with no visible overflow
      // reports some and latches itself shut. The static flow is what decides.
      var flow = 0;
      for (var k = 0; k < body.children.length; k++) {
        var kid = body.children[k];
        if (getComputedStyle(kid).position === 'absolute') continue;
        flow = Math.max(flow, kid.getBoundingClientRect().bottom);
      }
      var pad = parseFloat(getComputedStyle(body).paddingBottom) || 0;
      if (flow && flow + pad <= body.getBoundingClientRect().bottom + 1) {
        body.style.overflowY = 'visible';
      }
      // A classic scrollbar coming in (the calendar opening) narrows the
      // content; pay its width out of the right padding so nothing shifts.
      body.style.paddingRight = '';
      var sbw = body.offsetWidth - body.clientWidth;
      if (sbw > 0) {
        var side = parseFloat(getComputedStyle(body).paddingLeft) || 0;
        body.style.paddingRight = Math.max(0, side - sbw) + 'px';
      }
      // ⚠ Content can still grow after the panel opens -- an async list once
      // this is on a store, or anything injected into it. A body left at
      // `visible` cannot be scrolled, so the overflow would be unreachable
      // behind the panel's clip. Height only: our own scrollbar coming and
      // going changes their width and would loop this straight back.
      if (window.ResizeObserver && !el._acctRO) {
        var self = this;
        var last = -1;
        el._acctRO = new ResizeObserver(function (entries) {
          var h = 0;
          for (var i = 0; i < entries.length; i++) h += entries[i].contentRect.height;
          if (Math.abs(h - last) < 1) return;
          last = h;
          self._fit(el);
        });
        el._acctROTargets = [];
      }
      if (el._acctRO) {
        var targets = el._acctROTargets;
        for (var t = targets.length - 1; t >= 0; t--) {
          if (targets[t].parentElement !== body) {
            el._acctRO.unobserve(targets[t]);
            targets.splice(t, 1);
          }
        }
        for (var c = 0; c < body.children.length; c++) {
          if (targets.indexOf(body.children[c]) !== -1) continue;
          targets.push(body.children[c]);
          el._acctRO.observe(body.children[c]);
        }
      }
      if (window.MutationObserver && !el._acctMO) {
        var modalSelf = this;
        el._acctMO = new MutationObserver(function () {
          if (!el.hidden) modalSelf._fit(el);
        });
        el._acctMO.observe(body, { childList: true });
      }
    },

    close: function () {
      var el = document.querySelector('.gb-acct-modal.is-open');
      if (!el) return;
      var self = this;
      var back = this._last;
      this._last = null;
      this._hide(el, function () {
        // Released only after the exit has played: handing the scrollbar back
        // while the panel is still opaque makes the centred panel jump sideways.
        document.documentElement.classList.remove('is-modal-open');
        document.body.classList.remove('is-modal-open');
        smoothScroll('resume');
        // ⚠ preventScroll, or the browser scrolls the trigger back into view the
        // instant the lock comes off: the page jumps under the panel's fade-out
        // and the sticky nav and header move with it. Nothing needs scrolling --
        // the page never moved while the panel was open.
        if (back && document.contains(back)) back.focus({ preventScroll: true });
        self._token = null;
      });
    },

    // Shared by close() and by open()-over-an-open-panel, which must not drop
    // the lock at all.
    _hide: function (el, done) {
      el.querySelectorAll('.gb-acct-video__media').forEach(function (video) { video.pause(); });
      el.classList.remove('is-open');
      el.setAttribute('aria-hidden', 'true');
      var ms = this._exitMs(el);
      var token = this._token = {};
      clearTimeout(el._acctHideTimer);
      el._acctHideTimer = setTimeout(function () {
        el.hidden = true;
        // A panel that was replaced mid-exit must not run the stale callback:
        // it would unlock the page under the panel that replaced it.
        if (done && token === this._token) done();
      }.bind(this), ms);
    },

    _exitMs: function (el) {
      var v = getComputedStyle(el).getPropertyValue('--acct-modal-exit').trim();
      var n = parseFloat(v);
      if (!n) return 0;
      return v.indexOf('ms') > -1 ? n : n * 1000;
    },

    // Focus stays inside the dialog while it is open.
    _trap: function (e) {
      var el = document.querySelector('.gb-acct-modal.is-open');
      var f = el.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]),'
                                  + ' select:not([disabled]), textarea:not([disabled]),'
                                  + ' [tabindex]:not([tabindex="-1"])');
      if (!f.length) { e.preventDefault(); return; }
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  };

  /* acctFaq — 2284:27170. One row open at a time, which is the only shape the
   * board draws; clicking the open row closes it.
   */
  var acctFaq = {
    init: function () {
      var roots = document.querySelectorAll('[data-acct-accordion]');
      if (!roots.length) return;                 // not on this page
      for (var i = 0; i < roots.length; i++) this.bind(roots[i]);
    },

    bind: function (root) {
      if (root._acctBound) return;   // property, see acctForm.watch
      root._acctBound = true;
      var self = this;
      root.addEventListener('click', function (e) {
        var q = e.target.closest && e.target.closest('[data-acct-q]');
        if (!q || !root.contains(q)) return;
        var item = q.parentNode;
        var wasOpen = item.classList.contains('is-open');
        self._closeAll(root);
        if (!wasOpen) self._set(item, true);
      });
    },

    _closeAll: function (root) {
      var items = root.querySelectorAll('.gb-acct-faq__item');
      for (var i = 0; i < items.length; i++) this._set(items[i], false);
    },

    _set: function (item, open) {
      var panel = item.querySelector('.gb-acct-faq__panel');
      var q = item.querySelector('[data-acct-q]');
      var flip = function () {
        item.classList.toggle('is-open', open);
        if (q) q.setAttribute('aria-expanded', open ? 'true' : 'false');
      };
      if (panel) slideTo(panel, flip); else flip();
    }
  };

  /* acctPw — the 2026-09-15 brief asks for funkyfood's Reset Password behaviour:
   * the form slides out under the button rather than the board's reset email.
   * Collapsed state lives in CSS behind .acct-live, so without this script the
   * form is simply open and usable.
   */
  var acctPw = {
    init: function () {
      var btn = document.querySelector('[data-acct-pw-toggle]');
      var wrap = document.querySelector('[data-acct-pw-wrap]');
      if (!btn || !wrap) return;                 // not on this page
      var self = this;
      btn.addEventListener('click', function () {
        self.set(btn, wrap, !wrap.classList.contains('is-open'));
      });
      var cancel = wrap.querySelector('[data-acct-pw-cancel]');
      if (cancel) {
        cancel.addEventListener('click', function () {
          self.set(btn, wrap, false);
          btn.focus();
        });
      }
    },

    set: function (btn, wrap, open) {
      slideTo(wrap, function () {
        wrap.classList.toggle('is-open', open);
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      if (!open) return;
      var first = wrap.querySelector('input');
      // preventScroll: otherwise the browser scrolls the still-collapsed wrapper
      // into view and the content slides back up as it grows.
      if (first) first.focus({ preventScroll: true });
    }
  };

  /* acctCopy — the referral code. navigator.clipboard needs a secure context and
   * this build is opened over file://, so execCommand stays as the fallback
   * instead of the button quietly doing nothing.
   */
  /* acctSelectFit — the shared selectBox decides whether to drop its list
   * upwards by walking up to the nearest ancestor that clips, but its
   * clipBottom() treats overflow:clip as "does not clip". A modal panel is
   * exactly that (clip, NOT hidden -- hidden turns the panel into a scrollport
   * and its fields stop being reachable), so the list never flipped: past three
   * options it was cut off at the panel edge, and below six it has no scrollbar
   * of its own, which left the cut part unreachable.
   *
   * ⚠ Patched here, not in main.js: that file belongs to the marketing pages'
   * line, and only these two pages load this one. If the shared widget ever
   * stops exposing these methods this module no-ops -- acct44check pins that
   * the patch is live, so the no-op cannot pass silently.
   */
  var acctSelectFit = {
    GAP: 8,       // breathing room against the panel edge
    MIN: 96,      // below this a clamped list is not worth showing; flip instead

    init: function () {
      var sb = window.gumi && window.gumi.selectBox;
      if (!sb || typeof sb.show !== 'function' || typeof sb.close !== 'function') return;
      var self = this;

      var show = sb.show, close = sb.close;
      sb.show = function (box) { show.call(sb, box); self._fit(box); };
      sb.close = function (box, refocus) {
        if (box && box.list) box.list.style.maxHeight = '';
        return close.call(sb, box, refocus);
      };
    },

    _fit: function (box) {
      if (!box || !box.open || !box.list) return;
      var clip = this._clipper(box.wrap);
      if (!clip) return;                       // nothing clips it: leave it alone
      var list = box.list;
      // Measured with the clamp off, so this is the height CSS would give it.
      list.style.maxHeight = '';
      var natural = list.offsetHeight;
      if (!natural) return;                    // closed or detached
      var wr = box.wrap.getBoundingClientRect();
      var cr = clip.getBoundingClientRect();
      var below = Math.min(cr.bottom, window.innerHeight) - wr.bottom - this.GAP;
      var above = wr.top - Math.max(cr.top, 0) - this.GAP;
      // ⚠ Takes over the side from selectBox, which flips on one side's room
      // alone: in a short panel both sides can be too small and the bigger one
      // is what keeps the most options reachable.
      var up = below < natural && above > below;
      box.wrap.classList.toggle('is-up', up);
      var room = up ? above : below;
      if (room < natural) {
        list.style.maxHeight = Math.max(this.MIN, Math.round(room)) + 'px';
      }
    },

    _clipper: function (el) {
      for (var p = el.parentElement; p && p !== document.body; p = p.parentElement) {
        if (getComputedStyle(p).overflowY !== 'visible') return p;
      }
      return null;
    }
  };

  var acctCopy = {
    init: function () {
      var btns = document.querySelectorAll('[data-acct-copy]');
      if (!btns.length) return;                  // not on this page
      for (var i = 0; i < btns.length; i++) this.bind(btns[i]);
    },

    bind: function (btn) {
      var self = this;
      btn.addEventListener('click', function () {
        var input = document.getElementById(btn.getAttribute('data-acct-copy'));
        if (!input) return;
        input.select();
        input.setSelectionRange(0, 99999);        // iOS ignores select() alone
        var legacy = function () {
          try { return document.execCommand('copy'); } catch (e) { return false; }
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(input.value).then(
            function () { self.flash(btn); },
            function () { if (legacy()) self.flash(btn); });
          return;
        }
        if (legacy()) self.flash(btn);
      });
    },

    flash: function (btn) {
      if (btn.gbCopyTimer) clearTimeout(btn.gbCopyTimer);
      else btn.setAttribute('data-acct-copy-label', btn.textContent);
      btn.textContent = 'Copied';
      btn.gbCopyTimer = setTimeout(function () {
        btn.textContent = btn.getAttribute('data-acct-copy-label');
        btn.gbCopyTimer = null;
      }, 1500);
    }
  };

  document.addEventListener('DOMContentLoaded', function () {
    // cancelFlow and acctCal run after modal: modal arms the panels, and both of
    // these read controls inside them.
    var modules = [['accountList', accountList], ['accountVideo', accountVideo],
                   ['accountMenu', accountMenu], ['view', view], ['modal', modal],
                   ['acctForm', acctForm], ['acctFaq', acctFaq],
                   ['cancelFlow', cancelFlow], ['acctCal', acctCal],
                   ['acctPw', acctPw], ['acctCopy', acctCopy],
                   ['acctSelectFit', acctSelectFit]];
    for (var i = 0; i < modules.length; i++) {
      try { modules[i][1].init(); }
      catch (e) { if (window.console && console.error) console.error('gumiAcct:' + modules[i][0], e); }
    }
  });

  // Liveness flag, not a feature flag: account.scss hides the auth page's inactive
  // view only under .acct-live, so this line running is what makes hiding safe.
  document.documentElement.classList.add('acct-live');

  window.gumiAcct = { view: view, modal: modal, form: acctForm,
                      faq: acctFaq,
                      discount: acctDiscount, cancelFlow: cancelFlow,
                      selectFit: acctSelectFit,
                      cal: acctCal, pw: acctPw, copy: acctCopy };
})();

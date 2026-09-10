(function () {
  'use strict';

  var acctNav = {
    init: function () {
      var btn = document.querySelector('[data-acct-menu-toggle]');
      var menu = document.querySelector('[data-acct-menu]');
      if (!btn || !menu) return;              // not on this page

      var header = btn.closest('.gb-acct-header');

      function setOpen(open) {
        btn.setAttribute('aria-expanded', String(open));
        menu.hidden = !open;
        if (header) header.classList.toggle('is-open', open);
      }

      btn.addEventListener('click', function () {
        setOpen(btn.getAttribute('aria-expanded') !== 'true');
      });
      document.addEventListener('click', function (e) {
        if (menu.hidden || btn.contains(e.target) || menu.contains(e.target)) return;
        setOpen(false);
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !menu.hidden) {
          setOpen(false);
          btn.focus();
        }
      });

      acctNav._setOpen = setOpen;
    },
    closeMenu: function () {
      if (acctNav._setOpen) acctNav._setOpen(false);
    }
  };

  var view = {
    init: function () {
      if (!document.querySelector('[data-acct-view]')) return;   // not on this page
      var self = this;

      document.addEventListener('click', function (e) {
        var t = e.target.closest && e.target.closest('[data-acct-goto]');
        if (!t || t.getAttribute('aria-disabled') === 'true') return;
        e.preventDefault();
        self.show(t.getAttribute('data-acct-goto'));
        acctNav.closeMenu();
      });

      window.addEventListener('hashchange', function () {
        self.show(location.hash.slice(1));
      });

      this.show(location.hash.slice(1));
    },

    show: function (name) {
      var views = document.querySelectorAll('[data-acct-view]');
      var found = false;
      var i;
      for (i = 0; i < views.length; i++) {
        var match = views[i].getAttribute('data-acct-view') === name;
        views[i].hidden = !match;
        if (match) found = true;
      }
      if (!found) { this.show('overview'); return; }             // unknown hash

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
    }
  };

  /* acctForm — note 2284:27446: Save stays asleep until the form above it has
   * actually been changed. Panels with nothing to change (the confirm-only ones)
   * have no [data-acct-field] and are left alone, which is also how their boards
   * draw them: green, not #e6e6e6.
   */
  var acctForm = {
    watch: function (panel) {
      var save = panel.querySelector('[data-acct-save]');
      var fields = panel.querySelectorAll('[data-acct-field]');
      // 34351 draws restart's Save green while 31976's identical-looking one is
      // grey, so the exception is spelled out on the panel rather than hidden in
      // a missing data-acct-field.
      if (panel.hasAttribute('data-acct-save-ungated')) return;
      if (!save || !fields.length || panel.getAttribute('data-acct-watched')) return;
      panel.setAttribute('data-acct-watched', '1');
      var initial = this._snapshot(fields);
      save.disabled = true;
      var self = this;
      panel.addEventListener('input', function () {
        save.disabled = self._snapshot(fields) === initial;
      });
      // A <select> fires change, not input, in older engines; listening to both
      // costs nothing and the comparison is idempotent.
      panel.addEventListener('change', function () {
        save.disabled = self._snapshot(fields) === initial;
      });
    },

    _snapshot: function (fields) {
      var v = [];
      for (var i = 0; i < fields.length; i++) {
        var f = fields[i];
        // A radio's value is a constant; what changes is which one is picked.
        v.push(f.type === 'radio' || f.type === 'checkbox' ? (f.checked ? '1' : '0') : f.value);
      }
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
      if (!input || !apply || panel.getAttribute('data-acct-discount-bound')) return;
      panel.setAttribute('data-acct-discount-bound', '1');
      function sync() { apply.disabled = !input.value.trim(); }
      input.addEventListener('input', sync);
      sync();
    }
  };

  /* acctQty — the product card stepper.
   *
   * ⚠ The floor is declared per card (data-acct-qty-min), not inferred from how
   * many cards are on screen. Note 34502 is about the subscription's last
   * product, and how many of its products a panel happens to render is not the
   * same question -- 30960 draws one card that may still go to 0 because the
   * subscription has others.
   */
  var acctQty = {
    bind: function (root) {
      if (root.getAttribute('data-acct-qty-bound')) return;   // delegated: once only
      root.setAttribute('data-acct-qty-bound', '1');
      var self = this;
      root.addEventListener('click', function (e) {
        var btn = e.target.closest && e.target.closest('[data-acct-qty]');
        if (!btn || btn.disabled) return;
        var row = btn.closest('[data-acct-product]');
        var out = row && row.querySelector('[data-acct-qty-value]');
        if (!out) return;
        var n = parseInt(out.textContent, 10) || 0;
        var min = parseInt(row.getAttribute('data-acct-qty-min'), 10) || 0;
        var next = n + (btn.getAttribute('data-acct-qty') === 'up' ? 1 : -1);
        if (next < min) return;
        out.textContent = next;
        self._sync(root, row, next, min);
      });
      var rows = root.querySelectorAll('[data-acct-product]');
      for (var i = 0; i < rows.length; i++) {
        var v = rows[i].querySelector('[data-acct-qty-value]');
        var m = parseInt(rows[i].getAttribute('data-acct-qty-min'), 10) || 0;
        this._sync(root, rows[i], parseInt(v ? v.textContent : '0', 10) || 0, m);
      }
    },

    _sync: function (root, row, n, min) {
      var down = row.querySelector('[data-acct-qty="down"]');
      if (down) down.disabled = n <= min;
      var cta = root.querySelector('[data-acct-save]');
      if (!cta) return;
      // note 34504: a product stepped down to nothing turns the action into a
      // removal -- but only where 0 means "take it out". In the picker 0 just
      // means "not chosen", and 28942/29399 keep the CTA at "Add products", so
      // the swap is opt-in per panel rather than automatic.
      var zeroLabel = cta.getAttribute('data-acct-label-zero');
      if (!zeroLabel) return;
      var zero = false;
      var rows = root.querySelectorAll('[data-acct-product]');
      for (var i = 0; i < rows.length; i++) {
        var v = rows[i].querySelector('[data-acct-qty-value]');
        var m = parseInt(rows[i].getAttribute('data-acct-qty-min'), 10) || 0;
        if (m === 0 && parseInt(v ? v.textContent : '1', 10) === 0) { zero = true; break; }
      }
      cta.textContent = zero ? zeroLabel : cta.getAttribute('data-acct-label-default');
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

  /* acctCal — 30465's date picker.
   *
   * ⚠ The board's own grid cannot be copied: 1 July 2026 is a Wednesday but the
   * board puts it under Su, and one cell reads "32". Only the tokens come from
   * the board; the month is generated.
   *
   * note 30923: the resume day has to be a whole future day, so today and
   * everything before it is out and the first selectable day is tomorrow.
   */
  var acctCal = {
    DAYS: ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sat', 'Su'],   // 'Sat' is the board's own
    MONTHS: ['January', 'February', 'March', 'April', 'May', 'June', 'July',
             'August', 'September', 'October', 'November', 'December'],

    init: function () {
      var root = document.querySelector('[data-acct-cal]');
      if (!root) return;
      var today = new Date();
      today.setHours(0, 0, 0, 0);
      this.min = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1);
      this.picked = new Date(this.min.getTime());
      this.view = new Date(this.min.getFullYear(), this.min.getMonth(), 1);
      var self = this;
      root.addEventListener('click', function (e) {
        if (!e.target.closest) return;
        if (e.target.closest('[data-acct-cal-prev]')) { self._step(root, -1); return; }
        if (e.target.closest('[data-acct-cal-next]')) { self._step(root, 1); return; }
        var day = e.target.closest('[data-acct-cal-day]');
        if (day && !day.disabled) {
          self.picked = self._parse(day.getAttribute('data-acct-cal-day'));
          self.render(root);
        }
      });
      this.render(root);
    },

    _step: function (root, by) {
      this.view = new Date(this.view.getFullYear(), this.view.getMonth() + by, 1);
      this.render(root);
    },

    _iso: function (d) {
      var m = d.getMonth() + 1, day = d.getDate();
      return d.getFullYear() + '-' + (m < 10 ? '0' : '') + m + '-' + (day < 10 ? '0' : '') + day;
    },

    _parse: function (iso) {
      var p = iso.split('-');
      return new Date(+p[0], +p[1] - 1, +p[2]);
    },

    render: function (root) {
      var title = root.querySelector('[data-acct-cal-title]');
      if (title) title.textContent = this.MONTHS[this.view.getMonth()] + ' ' + this.view.getFullYear();
      var table = root.querySelector('table');
      if (!table) return;

      var head = '<thead><tr>';
      for (var i = 0; i < this.DAYS.length; i++) head += '<th scope="col">' + this.DAYS[i] + '</th>';
      head += '</tr></thead>';

      // Monday-first, whole weeks only: back up to the Monday on or before the
      // 1st and run to the Sunday on or after the last day.
      var first = new Date(this.view.getFullYear(), this.view.getMonth(), 1);
      var start = new Date(first.getTime());
      start.setDate(1 - ((first.getDay() + 6) % 7));
      var last = new Date(this.view.getFullYear(), this.view.getMonth() + 1, 0);
      var end = new Date(last.getTime());
      end.setDate(last.getDate() + 6 - ((last.getDay() + 6) % 7));

      var body = '<tbody>';
      var cur = new Date(start.getTime());
      var pickedIso = this._iso(this.picked);
      while (cur <= end) {
        body += '<tr>';
        for (var c = 0; c < 7; c++) {
          var iso = this._iso(cur);
          var out = cur.getMonth() !== this.view.getMonth();
          var off = out || cur < this.min;
          body += '<td><button class="gb-acct-cal__day" type="button"'
               + ' data-acct-cal-day="' + iso + '"'
               + (out ? ' data-acct-cal-out' : '')
               + (off ? ' disabled' : '')
               + ' aria-pressed="' + (iso === pickedIso ? 'true' : 'false') + '">'
               + cur.getDate() + '</button></td>';
          cur.setDate(cur.getDate() + 1);
        }
        body += '</tr>';
      }
      body += '</tbody>';

      var caption = table.querySelector('caption');
      table.innerHTML = (caption ? caption.outerHTML : '') + head + body;
    }
  };

  /* modal — every [data-acct-modal] opens the panel of the same name.
   *
   * The lock reuses the site's own is-modal-open rather than a second class of
   * ours. customstyle.scss already solves two traps here and a parallel lock
   * would have to solve them again: body must get overflow-x:clip /
   * overflow-y:visible (hidden makes body the sticky header's scrollport and
   * .gb-acct-header drops out of view), and the freed scrollbar width must be
   * padded back on html ONLY (paying it on both spends it twice). Setting the
   * class is not calling main.js -- the two scripts still do not talk.
   *
   * ⚠ main.js also drives is-modal-open for [data-modal]. account.html has no
   * [data-modal] trigger, so the two never hold the lock at once; if one is ever
   * added here, whichever closes first would unlock the other.
   */
  var modal = {
    _last: null,

    init: function () {
      var self = this;
      // Armed up front, not on first open: the board ships Save greyed out, so
      // it has to be disabled before the panel is ever shown.
      var panels = document.querySelectorAll('.gb-acct-modal');
      for (var i = 0; i < panels.length; i++) {
        acctForm.watch(panels[i]);
        acctQty.bind(panels[i]);
        acctDiscount.bind(panels[i]);
      }
      document.addEventListener('click', function (e) {
        if (!e.target.closest) return;
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
      }
      el.hidden = false;
      void el.offsetWidth;                              // reflow, or the entry has nothing to run from
      el.classList.add('is-open');
      el.setAttribute('aria-hidden', 'false');
      // The dialog itself takes focus, not its first control: a scripted focus
      // with no pointer input before it still counts as :focus-visible, so the
      // ring would be painted the moment the panel appears.
      el.querySelector('.gb-acct-modal__panel').focus();
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
        if (back && document.contains(back)) back.focus();
        self._token = null;
      });
    },

    // Shared by close() and by open()-over-an-open-panel, which must not drop
    // the lock at all.
    _hide: function (el, done) {
      el.classList.remove('is-open');
      el.setAttribute('aria-hidden', 'true');
      var ms = this._exitMs(el);
      var token = this._token = {};
      setTimeout(function () {
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

  document.addEventListener('DOMContentLoaded', function () {
    // view runs after acctNav: its init calls acctNav.closeMenu().
    // cancelFlow and acctCal run after modal: modal arms the panels, and both of
    // these read controls inside them.
    var modules = [['acctNav', acctNav], ['view', view], ['modal', modal],
                   ['cancelFlow', cancelFlow], ['acctCal', acctCal]];
    for (var i = 0; i < modules.length; i++) {
      try { modules[i][1].init(); }
      catch (e) { if (window.console && console.error) console.error('gumiAcct:' + modules[i][0], e); }
    }
  });

  window.gumiAcct = { acctNav: acctNav, view: view, modal: modal, form: acctForm,
                      qty: acctQty, discount: acctDiscount, cancelFlow: cancelFlow,
                      cal: acctCal };
})();

#!/usr/bin/env python3
"""Mount the cart drawer on the 11 delivery pages (idempotent).

Two edits per page: the header's cart icon gains data-modal, and the drawer
markup goes in just before the scripts, next to the other modals.

font-check.html is skipped -- it has no header, so nothing can open the drawer.

Every path in the drawer's inline icons is read out of figma/assets-raw/icons at
run time, so the markup cannot drift from the board without this failing.
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = os.path.join(ROOT, "figma", "assets-raw", "icons")

PAGES = ["index.html", "pdp.html", "science.html", "reviews.html",
         "how-gumi-works.html", "our-story.html", "faq.html",
         "get-in-touch.html", "referral.html", "privacy-policy.html",
         "shipping.html"]


def paths(stem):
    """Every path `d` in a source icon, in document order."""
    svg = io.open(os.path.join(ICONS, stem + ".svg"), encoding="utf-8").read()
    return re.findall(r'<path d="([^"]+)"', svg)


def icon(stem, w, h, sw, cls=""):
    d = paths(stem)
    assert len(d) == 1, "%s has %d paths" % (stem, len(d))
    c = ' class="%s"' % cls if cls else ""
    return ('<svg%s aria-hidden="true" viewBox="0 0 %d %d" fill="none" '
            'xmlns="http://www.w3.org/2000/svg"><path d="%s" stroke="currentColor" '
            'stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            % (c, w, h, d[0], sw))


# The bin icon ships wrapped in a clipPath; its rect covers y 2..18 and the path
# runs 3.33..16.67, so the clip cuts nothing and is dropped rather than repeated
# with a duplicate id on every page.
CLOSE = icon("desktop-cart-icon", 24, 24, "2")
TRUCK = icon("desktop-cart-icon-2", 24, 24, "2")
CYCLE = icon("desktop-cart-icon-3", 24, 24, "2")
MINUS = icon("desktop-cart-icon-4", 16, 16, "1.33333")
PLUS = icon("desktop-cart-icon-5", 16, 16, "1.33333")
LOCK = icon("desktop-cart-icon-10", 24, 24, "2")
BIN = icon("desktop-cart-frame-1984078213", 16, 20, "1.33333")

MARKS = ["visa", "mastercard", "applepay", "amex", "paypal"]   # board order, 341:42573


INTERVALS = ["One Time Purchase", "2 Weeks", "4 Weeks", "6 Weeks", "8 Weeks"]


def item(name, variant, count, was, now, plan_label, plan_value):
    opts = "\n".join(
        '                  <option%s>%s</option>' % (' selected' if o == plan_value else '', o)
        for o in INTERVALS)
    return """          <li class="gb-cart-item">
            <span class="gb-cart-item__media" aria-hidden="true"></span>
            <div class="gb-cart-item__main">
              <div class="gb-cart-item__head">
                <div class="gb-cart-item__row">
                  <span class="gb-cart-item__name">%s</span>
                  <button class="gb-cart-item__remove" type="button" aria-label="Remove %s">%s</button>
                </div>
                <span class="gb-cart-item__variant">%s</span>
              </div>
              <div class="gb-cart-item__qty">
                <div class="gb-cart-item__stepper">
                  <button class="gb-cart-item__step" type="button" aria-label="Decrease quantity">%s</button>
                  <span class="gb-cart-item__count">%s</span>
                  <button class="gb-cart-item__step" type="button" aria-label="Increase quantity">%s</button>
                </div>
                <span class="gb-cart-item__price">
                  <s class="gb-cart-item__was">%s</s>
                  <span class="gb-cart-item__now">%s</span>
                </span>
              </div>
              <p class="gb-cart-item__plan">%s
                <select class="gb-cart-item__interval" data-select="inline" aria-label="Delivery interval for %s">
%s
                </select>
              </p>
            </div>
          </li>""" % (name, name, BIN, variant, MINUS, count, PLUS, was, now,
                      plan_label, name, opts)


NAV_CARDS = """        <div class="gb-cart__cards">
          <a class="gb-nav-card" href="pdp.html">
            <span class="gb-nav-card__title">Shop Gumi</span>
            <picture>
              <source srcset="images/nav-card-bear.webp" type="image/webp">
              <img class="gb-nav-card__art" src="images/nav-card-bear.png" alt="" width="523" height="631" loading="lazy" decoding="async">
            </picture>
            <span class="gb-nav-card__action"><svg aria-hidden="true" viewBox="0 0 23 23" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79519 11.4995H18.2114M11.5033 4.79146L18.2114 11.4995L11.5033 18.2076" stroke="currentColor" stroke-width="2.29991" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
          </a>
          <a class="gb-nav-card" href="referral.html">
            <span class="gb-nav-card__body">
              <span class="gb-nav-card__tag">Refer a Friend</span>
              <span class="gb-nav-card__text">Earn rewards and $20 for every referral.</span>
            </span>
            <span class="gb-nav-card__action"><svg aria-hidden="true" viewBox="0 0 23 23" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4.79519 11.4995H18.2114M11.5033 4.79146L18.2114 11.4995L11.5033 18.2076" stroke="currentColor" stroke-width="2.29991" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
          </a>
        </div>"""


def drawer(build):
    marks = "\n".join(
        '            <img src="images/pay-%s.svg?v=%s" alt="%s" width="35" height="24" loading="lazy" decoding="async">'
        % (m, build, m) for m in MARKS)
    return """    <div class="gb-cart" id="gb-cart" role="dialog" aria-modal="true" tabindex="-1"
         aria-labelledby="gb-cart-title" aria-hidden="true">
      <div class="gb-cart__overlay" data-modal-close></div>
      <div class="gb-cart__panel">
        <div class="gb-cart__head">
          <h2 class="gb-cart__title" id="gb-cart-title">Your Cart</h2>
          <button class="gb-cart__close" type="button" data-modal-close aria-label="Close cart">%s</button>
        </div>

        <p class="gb-cart__ship">%s Spend another $20 for FREE Delivery</p>

        <div class="gb-cart__body">
          <div class="gb-cart__lines">
            <p class="gb-cart__sub">%s Subscribe &amp; Save</p>
            <ul class="gb-cart__items">
%s
%s
            </ul>
            <div class="gb-cart__gift">
              <span class="gb-cart__gift-media" aria-hidden="true"></span>
              <div class="gb-cart__gift-body">
                <div class="gb-cart__gift-row">
                  <span class="gb-cart__gift-name">Gift Name Here</span>
                  <span class="gb-cart-item__price">
                    <s class="gb-cart-item__was">$60</s>
                    <span class="gb-cart-item__now">FREE</span>
                  </span>
                </div>
                <p class="gb-cart__gift-text">This here is a gift description that can go over two lines or even possibly three lines depending on what it says.</p>
              </div>
            </div>
          </div>

          <div class="gb-cart__totals">
            <div class="gb-cart__sums">
              <p class="gb-cart__sum">Subtotal <b>$60</b></p>
              <p class="gb-cart__sum">Discount
                <span class="gb-cart__sum-pair">Automatic <b>-$15</b></span>
              </p>
              <p class="gb-cart__sum">Shipping <b>Calculated at checkout</b></p>
            </div>
            <div class="gb-cart__grand">
              <p class="gb-cart__grand-row"><span>Total</span> <span>$45</span></p>
              <div class="gb-cart__pay">
                <p class="gb-cart__pay-note">Discount codes applied at checkout</p>
                <div class="gb-cart__pay-marks">
%s
                </div>
              </div>
              <button class="gb-cart__continue" type="button" data-modal-close>Continue Shopping</button>
            </div>
          </div>
        </div>

        <div class="gb-cart__empty">
          <div class="gb-cart__empty-head">
            <p class="gb-cart__empty-title">Oops! Your cart is empty</p>
            <a class="gb-btn gb-btn--primary gb-cart__shop" href="pdp.html">Shop Now</a>
          </div>
%s
        </div>

        <div class="gb-cart__bar">
          <p class="gb-cart__bar-total"><span>Total</span>
            <span class="gb-cart__bar-pair"><s class="gb-cart__bar-was">$60</s> <span>$45</span></span>
          </p>
          <a class="gb-btn gb-btn--lg gb-cart__checkout" href="#">%s Secure Checkout</a>
        </div>
      </div>
    </div>

""" % (CLOSE, TRUCK, CYCLE,
       item("Superfood Greens Gummies", "28 Packs", "1", "$60", "$45", "Delivers every", "4 Weeks"),
       item("Superfood Greens Gummies", "28 Packs", "1", "$60", "$45", "Delivers every", "One Time Purchase"),
       marks, NAV_CARDS, LOCK)


TRIGGER_OLD = '<a class="gb-header__icon" href="#" aria-label="Cart">'
TRIGGER_NEW = '<a class="gb-header__icon" href="#" data-modal="gb-cart" aria-label="Cart">'


def main():
    build = re.search(r'\$build:\s*"([^"]+)"',
                      io.open(os.path.join(ROOT, "assets", "customstyle.scss"),
                              encoding="utf-8").read()).group(1)
    html = drawer(build)
    for page in PAGES:
        p = os.path.join(ROOT, page)
        s = io.open(p, encoding="utf-8").read()
        before = s
        if TRIGGER_OLD in s:
            s = s.replace(TRIGGER_OLD, TRIGGER_NEW)
        if 'id="gb-cart"' in s and "--remount" in sys.argv:
            i = s.index('    <div class="gb-cart" id="gb-cart"')
            j = s.index('\n    </div>\n\n', i) + len('\n    </div>\n\n')
            s = s[:i] + s[j:]
        if 'id="gb-cart"' not in s:
            m = re.search(r'^(\s*)<script src="assets/lenis', s, re.M)
            assert m, page + ": no script block to anchor on"
            s = s[:m.start()] + html + s[m.start():]
        if s != before:
            io.open(p, "w", encoding="utf-8").write(s)
            print("mounted", page)
        else:
            print("skip   ", page, "(already mounted)")


if __name__ == "__main__":
    main()

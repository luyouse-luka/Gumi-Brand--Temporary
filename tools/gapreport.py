#!/usr/bin/env python3
"""Read gapstyle-*.json and print the static-vs-live differences as a checklist.

    python3 tools/gapreport.py tools/gapstyle-1440.json
    python3 tools/gapreport.py tools/gapstyle-1440.json --prop font-size
    python3 tools/gapreport.py tools/gapstyle-1440.json --cls gb-faq

Three buckets, in the order they matter:
  A  same class, different computed style  -> CSS bug, fixable without structure
  B  pseudo-element differs                -> scallops / arrows / rings
  C  class on static only                  -> structural gap, needs liquid (LIVE-GAP)

Geometry is printed only when the style bucket is empty for that class: a box
that is wider on live because the copy is longer is not a defect.
"""
import argparse, json, collections, sys

SKIP_GEO_ONLY = True
# background-image on live is a Shopify CDN url, on static a relative path --
# the VALUE always differs; only presence/absence is comparable.
URLISH = {'background-image', 'mask-image', '-webkit-mask-image'}


def norm(prop, v):
    if prop in URLISH:
        return 'none' if v in ('none', '') else 'url'
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('json')
    ap.add_argument('--prop'); ap.add_argument('--cls'); ap.add_argument('--page')
    ap.add_argument('--geo', action='store_true')
    a = ap.parse_args()
    data = json.loads(open(a.json, encoding='utf-8').read())

    # class -> prop -> list of (page, static, live)
    style_diff = collections.defaultdict(lambda: collections.defaultdict(list))
    pseudo_diff = collections.defaultdict(lambda: collections.defaultdict(list))
    missing = collections.defaultdict(list)
    liveonly = collections.defaultdict(list)
    tagdiff = collections.defaultdict(list)
    geo_diff = collections.defaultdict(lambda: collections.defaultdict(list))

    for page, d in data.items():
        if a.page and page != a.page: continue
        st, lv = d['static'], d['live']
        if not lv: continue
        for cls, s in st.items():
            l = lv.get(cls)
            if l is None:
                missing[cls].append(page); continue
            if s['tag'] != l['tag']:
                tagdiff[cls].append((page, s['tag'], l['tag']))
            for p, v in s['s'].items():
                lvv = l['s'].get(p)
                if norm(p, v) != norm(p, lvv):
                    style_diff[cls][p].append((page, v, lvv))
            for pseudo in ('::before', '::after'):
                sp, lp = s.get(pseudo), l.get(pseudo)
                if (sp is None) != (lp is None):
                    pseudo_diff[cls][pseudo + ' exists'].append(
                        (page, 'yes' if sp else 'no', 'yes' if lp else 'no'))
                elif sp and lp:
                    for p, v in sp.items():
                        if norm(p, v) != norm(p, lp.get(p)):
                            pseudo_diff[cls][pseudo + ' ' + p].append((page, v, lp.get(p)))
            for p, v in s['g'].items():
                if abs((v or 0) - (l['g'].get(p) or 0)) > 2:
                    geo_diff[cls][p].append((page, v, l['g'].get(p)))
        for cls in lv:
            if cls not in st: liveonly[cls].append(page)

    def show(title, bag):
        print('\n' + '=' * 72); print(title); print('=' * 72)
        rows = sorted(bag.items(), key=lambda kv: (-sum(len(x) for x in kv[1].values()), kv[0]))
        for cls, props in rows:
            if a.cls and a.cls not in cls: continue
            print('\n  .%s' % cls)
            for p, hits in sorted(props.items()):
                if a.prop and a.prop != p and not p.endswith(a.prop): continue
                pages = ', '.join(h[0] for h in hits)
                s, l = hits[0][1], hits[0][2]
                allsame = all((h[1], h[2]) == (s, l) for h in hits)
                print('      %-28s static=%-22s live=%-22s  [%s]%s'
                      % (p, str(s)[:22], str(l)[:22], pages, '' if allsame else ' *varies'))

    show('A. same class, different computed style  (CSS-fixable)', style_diff)
    show('B. pseudo-element differs  (scallops / arrows / rings)', pseudo_diff)

    if tagdiff:
        print('\n' + '=' * 72); print('A2. same class, different TAG'); print('=' * 72)
        for cls, hits in sorted(tagdiff.items()):
            print('  .%-40s static=<%s> live=<%s>  [%s]'
                  % (cls, hits[0][1], hits[0][2], ', '.join(h[0] for h in hits)))

    print('\n' + '=' * 72); print('C. class on static only  (structural gap)'); print('=' * 72)
    byblock = collections.defaultdict(list)
    for cls, pages in missing.items():
        byblock[cls.split('__')[0].split('--')[0]].append((cls, pages))
    for blk, items in sorted(byblock.items(), key=lambda kv: -len(kv[1])):
        pages = sorted({p for _, ps in items for p in ps})
        print('  %-26s %2d classes   [%s]' % (blk, len(items), ', '.join(pages)))

    if a.geo:
        show('D. geometry differs (content-driven, informational)', geo_diff)
    print('\n(totals) style=%d classes  pseudo=%d  static-only=%d  live-only=%d'
          % (len(style_diff), len(pseudo_diff), len(missing), len(liveonly)))


if __name__ == '__main__':
    main()

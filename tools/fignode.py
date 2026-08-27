#!/usr/bin/env python3
"""Dump one node subtree with absolute geometry + composed transform."""
import json,math,sys
BOARDS={'m':('figma/nodes/228-5932_homepage-mobile.json','228:5932'),
        'd':('figma/nodes/285-18162_homepage-desktop.json','285:18162')}
def load(k):
    p,r=BOARDS[k]; d=json.load(open(p)); idx={}
    def ix(n):
        idx[n['id']]=n
        for c in n.get('children') or []: ix(c)
    ix(d['nodes'][r]['document']); return idx
def dump(idx,nid,maxd=99,depth=0):
    n=idx.get(nid)
    if n is None: print('MISSING',nid); return
    def w(n,depth):
        if n.get('visible') is False or depth>maxd: return
        bb=n.get('absoluteBoundingBox') or {}; rb=n.get('absoluteRenderBounds') or {}
        rt=n.get('relativeTransform'); s=''
        if rt:
            det=rt[0][0]*rt[1][1]-rt[0][1]*rt[1][0]
            s=f" rot={math.degrees(math.atan2(rt[1][0],rt[0][0])):+.2f}° det={det:+.3f}"
        ex=''
        if n.get('type')=='TEXT':
            st=n.get('style',{})
            ex=f"  «{n['characters'][:26]}» fs={st.get('fontSize')} lh={st.get('lineHeightPx')} ls={st.get('letterSpacing')} w={st.get('fontWeight')}"
        for k in ('itemSpacing','paddingLeft','paddingRight','paddingTop','paddingBottom','layoutMode','cornerRadius','primaryAxisAlignItems','counterAxisAlignItems','clipsContent'):
            if n.get(k) not in (None,0,False): ex+=f" {k}={n[k]}"
        print('  '*depth+f"{n['type']:<9} {n.get('name','')[:30]:<30} x={bb.get('x',0):>9.2f} y={bb.get('y',0):>9.2f} w={bb.get('width',0):>7.2f} h={bb.get('height',0):>7.2f} ink=({rb.get('x',0):.1f},{rb.get('y',0):.1f},{rb.get('width',0):.1f},{rb.get('height',0):.1f}) {n['id']}{s}{ex}")
        for c in n.get('children') or []: w(c,depth+1)
    w(n,depth)
if __name__=='__main__':
    idx=load(sys.argv[1]); md=int(sys.argv[2])
    for nid in sys.argv[3:]: dump(idx,nid,md); print()

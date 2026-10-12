from pathlib import Path
import re
root = Path(__file__).resolve().parents[1]
t = root.parent/'Gumi-Brand-shopify'
pre = t/'prepush-20261007-acct-burger'
post = t/'verify-20261007-acct-burger'
fresh = t/'prework-20261007-acct-menu-restore'
work = t/'work-20261007-acct-menu-restore'
targets = {'assets/account.scss','assets/account.css','layout/account.liquid','sections/gb-account.liquid','sections/gb-header.liquid'}
files = lambda r: {p.relative_to(r).as_posix():p for p in r.rglob('*') if p.is_file() and p.name != 'AGENTS.md'}
a,b,c = map(files,[pre,post,fresh])
assert len(c)>=642
print('Previous push collateral:',[k for k in a if k not in targets and (k not in b or a[k].read_bytes()!=b[k].read_bytes())])
marker = '<main class="gb-acct">'
assert a['sections/gb-account.liquid'].read_text(encoding='utf-8').split(marker,1)[1] == b['sections/gb-account.liquid'].read_text(encoding='utf-8').split(marker,1)[1]
print('Previous push kept entire fresh Account body: True')
print('New live changes:',[k for k in b if k not in c or b[k].read_bytes()!=c[k].read_bytes()])
for rel in ['assets/account.scss','assets/account.css','assets/account.js','sections/gb-header.liquid']:
    assert b[rel].read_bytes()==c[rel].read_bytes(), 'target changed: '+rel
for rel in ['assets/account.scss','assets/account.css','assets/account.js']:
    assert (root/rel).read_bytes()==c[rel].read_bytes(), 'local differs: '+rel

old = (t/'prepush-20261007-account-header/sections/gb-account.liquid').read_text(encoding='utf-8')
account = re.search(r'      <div class="gb-acct-header__link gb-acct-header__link--account">.*?\n      </div>',old,re.S).group(0)
header = c['sections/gb-header.liquid'].read_text(encoding='utf-8')
start = header.index('    <button class="gb-header__toggle gb-acct-header__toggle"')
end = header.index('    </button>',start)+len('    </button>')
header = header[:start]+'    <div class="gb-acct-header__icons">\n'+account+'\n'+header[start:end]+'\n    </div>'+header[end:]
(work/'sections').mkdir(parents=True,exist_ok=True)
(work/'sections/gb-header.liquid').write_text(header,encoding='utf-8',newline='\n')
static = (root/'account.html').read_text(encoding='utf-8')
start = static.index('    <button class="gb-header__toggle gb-acct-header__toggle"')
end = static.index('    </button>',start)+len('    </button>')
static = static[:start]+'    <div class="gb-acct-header__icons">\n'+account+'\n'+static[start:end]+'\n    </div>'+static[end:]
static = static.replace('20261007-a68','20261007-a69')
(root/'account.html').write_text(static,encoding='utf-8',newline='\n')
p = root/'account-login.html'
p.write_text(p.read_text(encoding='utf-8').replace('20261007-a68','20261007-a69'),encoding='utf-8',newline='\n')
p = root/'assets/account.scss'
scss = p.read_text(encoding='utf-8').replace('20261007-a68','20261007-a69')
scss = scss.replace('// Account top bar: logo left, hamburger right.', '// Account top bar: logo left, account dropdown and hamburger right.')
scss = scss.replace('// ⚠ No hover of its own (Task 33). The account icon still answers the pointer\n// through its ::after rule and the panel below; the burger is inert.', '// Account icon hover and click both expose the existing account dropdown.')
scss = scss.replace('// to where the header\'s content box ends: 24 (the icons gap) + 24 (the cart)', '// to where the header\'s content box ends: 24 (the icons gap) + 24 (the burger)')
p.write_text(scss,encoding='utf-8',newline='\n')
p = root/'assets/account.js'
js = p.read_text(encoding='utf-8')
old = '      function setOpen(open) {\n        root.toggleAttribute'
new = '''      function closeSiteMenu() {
        var header = window.gumi && window.gumi.header;
        if (header && header.el) header.set(false);
      }
      root.addEventListener('mouseenter', closeSiteMenu);
      function setOpen(open) {
        if (open) closeSiteMenu();
        root.toggleAttribute'''
assert old in js
p.write_text(js.replace(old,new,1),encoding='utf-8',newline='\n')
print('Prepared Account icon/dropdown restoration, burger retained.')

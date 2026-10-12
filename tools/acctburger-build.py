from pathlib import Path
import re, hashlib

root = Path(__file__).resolve().parents[1]
theme = root.parent / 'Gumi-Brand-shopify'
fresh = theme / 'prework-20261007-acct-burger'
base = theme / 'baseline-20261007-header-original'
work = theme / 'work-20261007-acct-burger'
targets = ['assets/account.scss', 'assets/account.css', 'layout/account.liquid', 'sections/gb-account.liquid', 'sections/gb-header.liquid']
for rel in targets:
    if rel == 'sections/gb-account.liquid':
        # Reviewed concurrent edit only changes current-order loading/body.
        assert (fresh/rel).read_text(encoding='utf-8').split('<main class="gb-acct">')[0] == (base/rel).read_text(encoding='utf-8').split('<main class="gb-acct">')[0]
    else:
        assert (fresh/rel).read_bytes() == (base/rel).read_bytes(), 'live target changed: '+rel
for rel in ['assets/account.scss', 'assets/account.css']:
    assert (root/rel).read_bytes() == (fresh/rel).read_bytes(), 'local target changed: '+rel

def save(rel, value):
    dest = work/rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(value, encoding='utf-8', newline='\n')

header = (fresh/'sections/gb-header.liquid').read_text(encoding='utf-8')
original = header[:header.index('\n  <div class="gb-header__panel"')]
burger = '''<div class="gb-header__bar gb-acct-header__bar">
    <a class="gb-acct-header__logo" href="{{ routes.root_url }}" aria-label="{{ shop.name }} home">
      {% render 'gb-logo', variant: 'sm' %}
    </a>
    <button class="gb-header__toggle gb-acct-header__toggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="site-menu">
      <svg class="gb-icon-menu" aria-hidden="true" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 12H21M3 6H21M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <svg class="gb-icon-close" aria-hidden="true" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M17 7L7 17M7 7L17 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </button>
  </div>'''
conditional = '''<header class="gb-header{% if template.suffix == 'account' %} gb-acct-header{% endif %}" id="site-header">
  {% if template.suffix == 'account' %}
  '''+burger+'''
  {% else %}
'''+original[original.index('  <div'):]+'''
  {% endif %}
'''
save('sections/gb-header.liquid', conditional + header[len(original):])
assert header[len(original):] == (work/'sections/gb-header.liquid').read_text(encoding='utf-8').split('{% endif %}\n',1)[1], 'shared menu changed'
layout = (fresh/'layout/account.liquid').read_text(encoding='utf-8')
save('layout/account.liquid', layout.replace('    <main id="MainContent"', '    <div id="header-group">{% sections \'header-group\' %}</div>\n    <main id="MainContent"'))
account = (fresh/'sections/gb-account.liquid').read_text(encoding='utf-8')
start = account.index('<div class="gb-announcement">')
end = account.index('<main class="gb-acct">')
save('sections/gb-account.liquid', account[:start].replace('Independent header.', 'Account top bar with the shared site menu.')+account[end:])
assert (work/'sections/gb-account.liquid').read_text(encoding='utf-8').split('<main class="gb-acct">',1)[1] == account.split('<main class="gb-acct">',1)[1]

scss = (root/'assets/account.scss').read_text(encoding='utf-8')
scss = scss.replace('20261007-a67','20261007-a68')
scss = scss.replace('// This replaces the site header rather than restyling it: the board\'s header is\n// a different component (logo + two icons, no Menu / Shop now / cart).\n// customstyle.scss is untouched.', '// Account top bar: logo left, hamburger right. The configured site menu and\n// main.js handle the panel; customstyle.scss remains unchanged.')
scss = scss.replace('  // The rule is strokeAlign INSIDE', '  border-bottom: 0;\n\n  // The rule is strokeAlign INSIDE',1)
start = scss.index('.gb-acct-header__logo {')
end = scss.index('\n.gb-acct-header__icons {',start)
scss = scss[:start]+'''.gb-acct-header__logo {
  display: block;
  width: 123px;
  height: 32px;
  flex: none;
  color: $c-green;
  transition: trans(opacity);

  svg, img { display: block; width: 100%; height: 100%; object-fit: contain; }
  @include hover { opacity: 0.7; }
  @include narrow { width: 92px; height: 24px; }
}

.gb-acct-header__toggle {
  width: 24px;
  height: 24px;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
  gap: 0;

  .gb-icon-menu { display: block; }
  .gb-icon-close { display: none; }
  .gb-acct-header.is-open & {
    .gb-icon-menu { display: none; }
    .gb-icon-close { display: block; }
  }
}
'''+scss[end:]
(root/'assets/account.scss').write_text(scss,encoding='utf-8',newline='\n')

static = (root/'account.html').read_text(encoding='utf-8')
logo = re.search(r'<a class="gb-acct-header__logo"[^>]*>(.*?)</a>',static,re.S).group(1)
panel = (root/'index.html').read_text(encoding='utf-8')
panel = panel[panel.index('    <div class="gb-header__panel"'):panel.index('  </header>')]
staticbar = burger.replace('{{ routes.root_url }}','index.html').replace('{{ shop.name }}','Gumi').replace("{% render 'gb-logo', variant: 'sm' %}",logo.strip())
static = re.sub(r'<header class="gb-acct-header".*?</header>', '<header class="gb-header gb-acct-header" id="site-header">\n  '+staticbar+'\n'+panel+'  </header>', static,count=1,flags=re.S)
static = static.replace('20261007-a67','20261007-a68').replace('assets/main.js?v=20260909-r134','assets/main.js?v=20260910-r138')
(root/'account.html').write_text(static,encoding='utf-8',newline='\n')
login = root/'account-login.html'
login.write_text(login.read_text(encoding='utf-8').replace('20261007-a67','20261007-a68'),encoding='utf-8',newline='\n')
print('Prepared account top bar; shared menu and Account backend preserved.')

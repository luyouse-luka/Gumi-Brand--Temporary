# Gumi Account — 交接文档

## 2026-10-09 — a73：数量保存确认、取消态Edit discount hover、重复header（已上线）

用户反馈Edit Product及Add Item手动输入数量后Save关闭但未保存，并追加页面有两个header。本轮基于完整fresh live，不使用旧account-feedback数据脚本：prework相对a72已有sections/gb-account.liquid、snippets/gb-account-data.liquid、gb-account-placeholders.liquid、templates/page.account.liquid四份他人更新，全部保留其新增价格、日期、取消流程及登录保护逻辑。

数量：浏览器模拟确认输入12确实POST quantity:12，旧脚本收到API成功后立即关闭，旧快照仍显示原数量。新增confirmProductQuantity：在提交时记录每个产品目标数量，成功后使用no-store读取单个订阅，按line/variant核对数量（含移除/换variant），最多6次、间隔700ms。确认后用服务端订阅更新缓存及列表/详情/当前订单再关闭；读取失败或一直不匹配则保留弹窗并显示错误，提示刷新后再试。两个弹窗共用此确认，不做乐观伪造，也不重复POST。原库存、Save门控、步进器、最后一项不能移除等逻辑保留。

取消态：原规则仅覆盖discount-add，本轮将discount-applied一并覆盖，Edit discount code悬停保持蓝色。active/paused仍蓝→绿；真实live既有取消态折扣点击拦截原样保留，不套用旧静态页可点击说明。

重复header：layout/account.liquid已渲染header-group，但fresh sections/gb-account.liquid重新带入独立announcement和acct-header。本轮仅去掉区块里重复顶部，保留共享gb-header内Account图标/下拉和汉堡，正文从<main class="gb-acct">起与fresh逐字一致；未修改layout或主站header。

上传4文件：assets/account.scss、assets/account.css、snippets/gb-account-data.liquid、sections/gb-account.liquid。源码Liquid在liquid/account-qty-discount/；本地另更新account.html、account-login.html版本、tools/acctqtysave.cjs、acctdiscountstate.cjs、acctheadercount.cjs、acctburger.cjs及docs/account三份记录。资源版本20261009-a73；account.js未修改/上传。acctburger改为手机tap/桌面键盘并等待菜单实际可见，避免过渡刚开始时立即读visibility误报。

验证：两个旧数量确认测试分别在旧fresh脚本正确失败；修复后数量52项（精确POST一次、延迟回读、持续旧数据、API拒绝、等待中弹窗/忙态）、折扣颜色24、header组合/正文保留6、四档菜单58、logo24共164项通过；Sass编译及数据脚本语法通过。数量使用模拟API，未验证真实客户/Appstle持久化；未测iPhone Safari或真实登录线上浏览器。因此本轮确认修复的是前端保存确认缺口，若真实回读报错，需进一步查Worker/Appstle，而非声称真实数据已实测保存。

部署：用户明确授权推live；Dev #180348977399 role=live。prepush完整642主题文件相对prework零变化，目标零冲突。4个--only、--nodelete、--allow-live上传，完整回读12 ok/0 red，4目标逐字节一致，其余638主题文件无变化，无增删。备份prepush-20261009-qty-discount；回读verify-20261009-qty-discount；新基线baseline-20261009-a73（包含本轮前线上他人更新）。

不要报成bug：数量Save需等待真实回读确认才关闭；取消态Add/Edit discount都保持蓝色，真实点击限制仍由数据脚本决定；header只有共享版本一份，Account图标/下拉与汉堡保留。主站样式不改，顶栏及Account footer logo继续无hover。

---

## 2026-10-09 — a72：移除Account footer logo hover（已上线）

按用户要求，在account.scss内覆盖共享.gb-footer__logo的hover透明度0.75为1，并关闭对应transition。覆盖仅随Account样式加载，账户页及登录/注册页生效；主站共享customstyle不改。logo尺寸、颜色和首页链接保持原样，顶栏logo无hover继续保留。Account资源版本20261009-a72。

上传仅assets/account.scss、assets/account.css。本地另更新account.html、account-login.html、tools/acctlogo.cjs及docs/account三份记录。Sass 1.77.8编译通过，改前源重编译与旧CSS逐字节一致，CSS仅新增9行局部覆盖。Chrome先确认旧footer hover透明度0.75；改后390/1440两宽度的账户页和登录页footer检查、顶栏logo回归共24项通过。未验证真实登录客户/iPhone Safari，本轮未做线上浏览器验证。

用户已明确授权推live；确认Dev #180348977399为live。prework完整642主题文件与a71基线一致；prepush再次完整pull与prework零变化，目标零冲突。两个--only、--nodelete、--allow-live上传，完整回读8 ok/0 red，两目标逐字节一致，其余640主题文件无变化，无增删。备份prepush-20261009-footer-logo；回读verify-20261009-footer-logo；新基线baseline-20261009-a72。

不要报成bug：Account顶栏和footer logo无hover反馈均为用户要求；主站footer仍使用原共享样式。

---

## 2026-10-09 — a71：移除顶栏logo hover（已上线）

按用户要求，删除.gb-acct-header__logo的hover透明度0.7及对应opacity transition。logo尺寸、颜色和首页链接保留。Account资源版本20261009-a71，已按用户“拉取推送到live”授权上线。

上传仅assets/account.scss、assets/account.css。本地另更新account.html、account-login.html、tools/acctmotion.py、tools/acctlogo.cjs及docs/account三份记录。acctmotion移除logo必须有过渡的旧断言。相同Sass 1.77.8重编译改前源与原CSS逐字节一致；改后编译通过，CSS仅删除上述6行。Chrome在390/1440宽度共8项检查通过，确认真实:hover前后外观一致、尺寸和首页链接保留。判据：tools/acctlogo.cjs。

确认Dev #180348977399为live；prework完整642主题文件与a70基线一致，prepush再次完整pull与prework零变化，两个目标零冲突。使用两个--only、--nodelete、--allow-live上传；完整回读8 ok/0 red，两目标逐字节一致，其余640主题文件无变化，无增删。备份prepush-20261009-logo-hover；回读verify-20261009-logo-hover；新基线baseline-20261009-a71。未验证真实登录账户或iPhone Safari；本轮未做线上浏览器验证。

不要报成bug：Account顶栏logo无hover反馈是用户最新要求。

---

## 2026-10-07 — a70：cancelled优惠码链接不再hover变色（已上线）

按用户截图，仅.gb-acct-detail[data-acct-sub-state="cancelled"]内[data-acct-modal="discount-add"]的hover保持原$c-blue/#0374a5。active/paused仍hover绿色，点击仍能打开优惠码弹窗；其他链接无变动。CSS产物仅新增5行局部规则。资源版本20261007-a70。

上传仅assets/account.scss、assets/account.css；本地另更新account.html、account-login.html版本及docs/account三份记录。Sass编译通过，Chrome computed color实测active/paused蓝→绿、cancelled蓝→蓝，cancelled点击弹窗正常（4项）。未测真实登录客户/iPhone Safari。

prework与a69目标一致；prepush全量642主题文件相对prework无并发变化，零冲突。2个--only --nodelete --allow-live推Dev #180348977399，全量回读8 ok/0 red，2目标逐字节一致，其余640主题文件不变，无增删。备份prepush-20261007-cancel-hover；回读verify-20261007-cancel-hover；新基线baseline-20261007-a70。

不要报成bug：取消订阅的优惠码链接保持蓝色并仍可点击，仅禁用hover变色。

---

## 2026-10-07 — a69：补回Account图标及下拉菜单（已上线）

用户指出a68缺少Account入口和下拉菜单。恢复旧gb-acct-header__link--account及完整Account下拉（Overview、My Subscriptions、My Details、Refer a friend、Log Out），右侧排列Account图标+汉堡。保留a68 logo尺寸、汉堡原站菜单和之前四项修复。account.js沿用原账户菜单模块，新增打开/hover账户菜单时关闭主站菜单，避免两菜单重叠；汉堡打开时原document处理器关闭账户菜单。样式编译产物逐字节不变，不上传account.css。

用户要求再次拉取并查覆盖：prework全量642主题文件与a68回读完全一致；对照a68 prepush/verify，637清单外文件无改动，gb-account正文及他人overview loading逐字保留，因此上次未覆盖这些他人修改。Account入口缺失是本方a68对需求的错误理解导致移除，本轮已纠正，不是他人变更丢失。prepush再次全量pull与prework零变化，目标零冲突。

上传仅sections/gb-header.liquid、assets/account.js、assets/account.scss；资源版本20261007-a69（SCSS版本/注释变化，CSS无变化）。本地account.html、account-login.html、tools/acctburger.cjs、tools/acctmobilefixes.cjs、tools/acctmenurestore.py及docs/account三份记录更新。Sass/JS语法通过，四档acctburger58+acctheaderfix32+acctmobilefixes54=144项通过，含触摸/点击/hover、账户切换、Escape/键盘、菜单互斥、logo尺寸和其他四项回归。acctheaderfix恢复适用；acctsiteheader仍为历史判据。

显式3个--only --nodelete --allow-live推Dev #180348977399。全量回读10 ok/0 red，3目标逐字节一致，其余639主题文件无变化，无增删。备份prepush-20261007-acct-menu-restore；回读verify-20261007-acct-menu-restore；新基线baseline-20261007-a69。未实测真实登录客户/iPhone Safari，本轮未另行网页浏览器检查，上轮入口HTTP429。

不要报成bug：a69最新决定保留Account图标及账户下拉，并保留独立汉堡原站菜单；仅购物车图标被汉堡替换。a68关于移除Account菜单的说明已被本条取代。

---

## 2026-10-07 — a68：logo尺寸及汉堡菜单（已上线）

用户最新要求：gb-acct-header__logo PC123×32px，手机≤767为92×24px，同时约束SVG与img尺寸。顶栏左logo、右侧账户/购物车两个图标合并为24px汉堡；使用gb-acct-header布局，复用原站配置菜单和main.js（手机抽屉/子菜单/滚动锁/关闭焦点/键盘，PC展开菜单）。layout/account渲染header-group；gb-header只对Account替换顶栏，其他页面顶栏及共享菜单内容保持原样。gb-account移除重复announcement和旧header，正文/后端逐字保持fresh live，包括他人新加overview loading。其他四项a66修复保留。

仅上传5文件：assets/account.scss、assets/account.css、layout/account.liquid、sections/gb-account.liquid、sections/gb-header.liquid；不上传config、account.js或主站CSS/JS。资源版本20261007-a68。本地修改account.html、account-login.html、tools/acctmobilefixes.cjs，新增tools/acctburger.cjs、acctburger-build.py、acctburgerlive.cjs及三份Account记录。acctheaderfix/acctsiteheader是历史判据，当前不适用。

Sass编译通过；390/767/768/1440下acctburger48项+acctmobilefixes54项通过，包含精确SVG/img尺寸、汉堡、菜单、其他四项回归、无溢出/脚本错误。线上网页请求HTTP429，acctburgerlive未通过HTTP入口，不声称线上浏览器验证成功；未测真实登录客户/iPhone Safari。

prework保留他人订单加载状态更新；prepush完整642主题文件相对prework零并发变化。第一批暂存assets目录缺失，只上传3份Liquid；补齐后完整midread确认Liquid一致、CSS无冲突，再上传2份CSS。均显式--only --nodelete --allow-live。最终全量回读14 ok/0 red，5目标逐字节一致，637清单外主题文件不变，无新增/删除。备份prepush-20261007-acct-burger；回读verify-20261007-acct-burger；新基线baseline-20261007-a68。

不要报成bug：本轮要求取代原账户下拉/购物车图标；Account无Shop now、logo左/汉堡右；菜单内logo保持原站布局。主站header行为不变。

---

## 2026-10-07 — 撤回共享header结构，恢复gb-acct-header（已上线）

按用户要求，撤回最初“Account还原成主站header但去Shop now”的结构修改：layout/account.liquid不再渲染header-group；sections/gb-account.liquid恢复原独立announcement及gb-acct-header（logo、账户菜单、购物车）；sections/gb-header.liquid移除Account隐藏Shop now判断，回到原主站版本。新header逐字匹配prepush-20261007-account-header原结构；Account正文与后端内联脚本逐字保持本轮fresh live内容。其他四项a66修复及a67手机header覆盖撤回均保留，CSS/JS零上传，资源版本仍20261007-a67。

上传文件仅layout/account.liquid、sections/gb-account.liquid、sections/gb-header.liquid；本地修改account.html、tools/acctmobilefixes.cjs及docs/account三份记录。acctheaderfix在390/767/768/1440的32项检查通过（手机tap/键盘菜单、桌面hover、账户切换等），acctmobilefixes54项通过（导航箭头、报错对齐、视频播放/暂停及弹窗、溢出和错误）。tools/acctsiteheader.cjs是此前共享header阶段的历史判据，当前header已恢复独立组件，不适用。未验证真实登录账户或iPhone Safari。

安全：首次pull与a67基线的三个目标相同，推前再次全量pull642主题文件，相对prework无并发变化，目标零冲突。使用三个--only、--nodelete、--allow-live推Dev #180348977399。全量回读结果9 ok / 1 red：三个上传目标逐字节一致，无新增/删除；红项为清单外snippets/gb-account-data.liquid在推送/回读期间新增3处renderCurrentOrder调用，属于线上并发修改，本次未上传该文件，已保留。其余638个清单外主题文件无变化，不声称“全部清单外零变化”。

备份prepush-20261007-header-structure-revert；回读verify-20261007-header-structure-revert；新基线baseline-20261007-header-original（包含线上并发更新）。

不要报成bug：恢复gb-acct-header和账户图标菜单是用户最新决定；Account不再有主站Menu导航。这次是局部结构撤回，未整份恢复旧gb-account.liquid，避免回滚客户资料与后端新改动。

---

## 2026-10-07 — a67：撤回手机header位置调整（已上线）

按用户“header刚刚的修改需要撤回”，仅删除a66新增的.template-account .gb-header__bar手机覆盖：Menu恢复左侧，Logo恢复居中，购物车恢复显示。继续使用共享主站header，Account仍无Shop now。保留缺失资源、导航箭头、报错首行对齐和视频controls/图标修复。

上传仅assets/account.css、assets/account.scss；Account版本20261007-a67。本地另更新account.html、account-login.html的版本引用、tools/acctmobilefixes.cjs的header原布局断言及docs/account三份记录。源文件差异断言确认仅删header覆盖和版本更新，Sass无警告，四档54项检查通过，其他四项修复仍正常。

推前完整pull 642主题文件发现snippets/gb-account-data.liquid、gb-account-placeholders.liquid相对a66基线已有线上新改动；保留不上传，两个样式目标无冲突。使用两个--only、--nodelete、--allow-live推Dev #180348977399。全量回读8 ok / 0 red，两目标逐字节一致，其余640主题文件无变化，无新增/删除。备份prework-20261007-header-revert；回读verify-20261007-header-revert；新基线baseline-20261007-a67。未验证真实登录账户或iPhone Safari。

不要报成bug：手机header恢复主站原排列是用户最新决定，不再套a66左Logo/右Menu/隐藏购物车规则。

---

## 2026-10-07 — a66：Account手机header、缺失资源及视频修复（已上线）

按用户五项要求修改并推Dev #180348977399（live）。仅Account手机端（≤767）Logo移到左侧，Menu移到最右侧，隐藏cart-icon，保留账户图标；桌面布局不变。gb-acct-list__link添加用户提供的20×20右箭头，手机端右对齐。gb-acct-modal__alert图标与文字首行顶部对齐。

补上传两份已有本地文件：assets/flatpickr.min.css来自../funkyfood2-git/assets/flatpickr.min.css（配套JS版本4.6.13）；assets/pay-visa.svg来自images/pay-visa.svg。取消视频原生controls，使用本地设计2284:29753的播放三角图标和已有按钮外形：暂停时显示，播放时隐藏；支持点击视频暂停、按钮/键盘播放，关闭或切换弹窗时暂停视频。设计只有播放三角，不自造另一份暂停图标。

上传清单（6）：assets/account.css；assets/account.scss；assets/account.js；assets/flatpickr.min.css；assets/pay-visa.svg；snippets/gb-account-modals.liquid。本地其他修改：account.html（template-account及资源版本）；account-login.html（资源版本）；tools/acctmobilefixes.cjs；docs/account/HANDOFF.md、CHANGELOG.md、PUSH-LOG.md。Account资源版本20261007-a66。

冲突防护：首次完整pull发现上轮部署后snippets/gb-account-data.liquid和gb-account-placeholders.liquid已有线上更新；原样保留，未上传这两份。推前再次完整pull，640主题文件，与本轮prework比无新增变化、目标零冲突。只按六个--only、--nodelete、--allow-live上传，不上传config或其他文件。

验证：Sass编译无警告、JS语法通过；用同一Sass版本重编译基线得到逐字节相同CSS，本轮CSS仅52行差异。390/767/768/1440四档54项浏览器检查通过，包含实际canvas媒体流播放/暂停、overlay显隐、键盘播放、关闭弹窗暂停、header位置、箭头右对齐、报错首行对齐、菜单、无横向溢出和脚本错误。线上两份补充资源HTTP200且内容有效；未登录Account的服务端布局确认只有一个site-header且无Shop now。未测试真实登录客户/业务视频源或iPhone Safari真机。

完整回读16 ok / 0 red：六目标逐字节相同，636个清单外主题文件无变化，新增仅两份缺失资源，无删除；主题总文件640→642（另有CLI生成AGENTS.md）。备份prepush-20261007-account-fixes；回读verify-20261007-account-fixes；新基线baseline-20261007-a66。

不要报成bug：手机端cart-icon隐藏是用户要求，桌面仍显示；视频播放时中央图标隐藏，可点击画面暂停；native controls关闭是用户要求；未修改线上订阅API和他人新增后端逻辑。

---

## 2026-10-07 — Account uses the shared site header (deployed)

Replaced gb-acct-header with the configured header-group in layout/account.liquid. The Account page uses the site's existing menu, logo, navigation cards and cart trigger. sections/gb-header.liquid omits Shop now only when template.suffix == 'account'; other pages retain it. Removed the duplicate announcement/header from sections/gb-account.liquid. Account content and inline backend scripts remain identical to the fresh live snapshot. No CSS/JS or theme config uploaded; Account asset version remains 20261002-a62.

Files uploaded: layout/account.liquid; sections/gb-account.liquid; sections/gb-header.liquid. Local files: account.html; tools/acctsiteheader.cjs; docs/account/HANDOFF.md; docs/account/CHANGELOG.md; docs/account/PUSH-LOG.md. Local HTML uses the site's existing static header without Shop now.

Safety: complete prepush pull (640 theme files) matched live-20261007-latest, with zero concurrent changes and zero target conflicts. Earlier live Account/backend/config changes since baseline-20261002-no8weeks were preserved. Push used three explicit --only arguments, --nodelete and --allow-live to Dev #180348977399. Complete readback: 10 ok / 0 red, three targets byte-identical, other 637 theme files unchanged, no additions/deletions. Backup: ../Gumi-Brand-shopify/prepush-20261007-account-header; readback: verify-20261007-account-header; new baseline: baseline-20261007-account-header.

Validation: local Chrome at 390/768/1440 passed 30 checks for the shared header, absent CTA, menu open/Escape close, Account navigation/modal, overflow and script errors. Live homepage retained Shop now and passed menu open/close checks. Real signed-in Account rendering and iPhone Safari were not tested.

Do not report as a bug: the old Account icon dropdown is replaced by the site's existing Account link; Account navigation remains in the Account content. The main site retains Shop now. Existing gb-acct-header CSS/JS guards are retained for historical/local fixtures and are inactive when the old markup is absent.

---

## Task 65 — 移除8 weeks配送周期选项（2026-10-02，已上线）

按用户“没有8 weeks的选项，先去掉，然后推送live”要求，在edit-frequency动态选项生成前排除planFrequencyKey为8 week的selling plan，原生select与可见自定义列表同步移除，其他周期及真实plan ID保留。静态页面原有2/4/6 weeks无需更改。只上传snippets/gb-account-data.liquid；Account资源版本仍20261002-a62。
文件：liquid/account-feedback/snippets/gb-account-data.liquid；tools/acctfrequency.cjs。手机/桌面8项检查通过（无8 weeks、2/4/6保留、当前4 weeks选中、未修改Save禁用），修复前检查因8 weeks仍出现而失败；acctsave 22项回归通过。API数据模拟，未实测真实客户账户。
完整pull相对baseline-20261002-a62无变化、无冲突，逐个--only、--nodelete、--allow-live推Dev #180348977399。完整回读6 ok / 0 red，目标逐字节一致，其余639主题文件无变化/丢失/新增。641本地文件含CLI生成AGENTS.md。备份prepush-20261002-no8weeks；回读verify-20261002-no8weeks；新基线baseline-20261002-no8weeks。

---

## Task 64 — 日历年份禁用手动输入（2026-10-02，a62已上线）

用户反馈手机选日期时弹出键盘，截图键盘建议为2027。日历标题年份是flatpickr生成的可编辑number输入框，旧Task 38明确保留了手动改年份能力。现于acctCal onReady设置currentYearElement.readOnly、inputmode=none和tabIndex=-1；保留日期字段既有allowInput配置，左右月份箭头仍可跨年，日期选择不变。三个Account日历共用此修复。
文件：assets/account.js、account.scss、account.css；account.html、account-login.html版本20261002-a62。
验证：Chrome/WebKit手机触摸模式下三个日历共30项检查通过，确认年份只读、inputmode、tabIndex、跨年切月和选日；JS语法及Sass编译通过。未验证iPhone真机软键盘；已按用户推送live授权上线a62：完整pull相对a61基线无变化，只推三份Account assets；完整回读10 ok / 0 red，三目标逐字节一致，其余文件无变化/丢失/新增。新基线baseline-20261002-a62，备份prepush-20261002-a62，回读verify-20261002-a62。

---

## Task 63 — Safari取消/Skip圆点及统一下拉箭头（2026-10-02，a61已上线）

用户确认深色圆圈位于取消订阅/Skip选项，并提供统一下拉SVG：20×20、M5 7.5L10 12.5L15 7.5、#4D4D4D、stroke-width 2、round cap/join。
WebKit手机触摸模式已复现：hover媒体查询不匹配，但触摸保留:hover，Horizon base.css的hover:checked::after深色圆点覆盖原有绿色背景。gb-acct-reason__radio现在显式-webkit-appearance:none/accent-color，关闭checked::after，直接以现有8.8px绿色背景圆点绘制，并保持hover时浅绿底；16px尺寸和ink外圈保留。地址既有实现不改，JS/API不改。
Account页面及弹窗gb-select__arrow统一20×20、路径描边2px/#4d4d4d，移除a60只覆盖Edit Product的局部规则，原生select无JS备用SVG同步2px。共享main.js及主站样式不改。
文件：assets/account.scss、account.css；account.html、account-login.html版本a61；tools/acctradio.cjs扩展WebKit/Chrome及取消/Skip覆盖；docs/account/HANDOFF.md、CHANGELOG.md。
验证：Sass编译通过；WebKit及Chrome、390/1440、地址/取消/Skip、普通/hover状态120项通过，读取截图实际圆心绿色（允许2级合成舍入），并检查尺寸、外圈、底色及伪元素隐藏。下拉四种弹窗和无JS备用SVG36项通过。WebKit为Windows Playwright引擎，未验证用户Safari真机。已按用户“推送live”授权完整拉取Dev #180348977399；与a60基线比较无线上变更、无冲突，只推assets/account.css和account.scss（分别--only、--nodelete、--allow-live）。完整回读8 ok / 0 red，两目标逐字节一致，其余文件无变化/丢失/新增。live为20261002-a61；基线baseline-20261002-a61；备份prepush-20261002-a61；回读verify-20261002-a61。推前120项radio及36项箭头检查重新通过。

---

## Task 62 — Edit Product下拉箭头描边（2026-10-02，a60已上线）

用户澄清“箭头细了”为Edit Product选项图标。本地设计2284-30960节点I2284:31124;84:8170;30:862及另一选项对应节点strokeWeight均为2，当前main.js共享图标为1.667。仅在Edit Product内的gb-acct-prod__control覆盖SVG path stroke-width:2px，保留20x20及旋转交互；其他产品/地址下拉不改。
文件：assets/account.scss、account.css；account.html、account-login.html（a60）；docs/account/HANDOFF.md、CHANGELOG.md、PUSH-LOG.md。
验证：Sass编译通过；390/1440两档检查Edit Product描边2px和20x20，Add Product/Shipping Form仍1.667px。按此前用户推送live授权完整pull，线上相对a59基线无变化、无冲突，只推两份Account样式。
全量回读8 ok / 0 red，两目标逐字节一致，其余文件无变化。live20261002-a60；基线baseline-20261002-a60；备份prepush-20261002-a60；回读verify-20261002-a60。未实测真实客户账户。

---


## Task 61 — Save改动判定与添加产品空态（2026-10-02，a59，已上线）

编辑弹窗每次打开重新记录预填后的字段基准；input/change查询当前字段，支持正文控件被替换，回到原值则禁用Save。主题接管的产品面板由syncEditCta/syncAddCta独占门控，通用表单监听不再覆盖。异步预填frequency后刷新基准再派发change；variant ID比较统一用idOf，避免GID与数字相同variant被误判为修改。
产品网格直接子级gb-acct-empty跨全部列，No additional products available to add.独占整行，不强制nowrap，窄屏可自然换行。
文件：assets/account.js、account.scss、account.css；account.html、account-login.html（a59）；liquid/account-feedback/snippets/gb-account-data.liquid；tools/acctsave.cjs；docs/account/HANDOFF.md、CHANGELOG.md。
验证：acctsave手机/桌面22项通过（未修改、修改、改回、重新打开、动态字段、异步基准、数量/选项门控、空态满宽）；acctdiscountskip 12项及acctfeedback8 40项回归通过；Sass编译和JS语法通过。只模拟UI/API，未实测真实客户。
已按用户“推送live”授权完整pull，线上相对a58基线无变化、无冲突。只推account.css、account.scss、account.js、gb-account-data.liquid；完整回读12 ok / 0 red，四目标逐字节一致，其余文件无变化。live为20261002-a59；基线baseline-20261002-a59，备份prepush-20261002-a59。确认型无编辑内容的按钮及restart既有ungated例外保留，最后商品保护未新增。

---


## Task 60 — 商品meta间距及名称两行省略（2026-10-02，a58，已上线）

按用户要求，gb-acct-product__meta增加padding-left:24px，手机≤767px宽度改100%。gb-acct-product__label采用两行clamp、超出省略及长词换行；name设置flex:1/min-width:0，避免长名称挤占Edit元素。
文件：assets/account.scss、account.css；account.html、account-login.html（a58）；docs/account/HANDOFF.md、CHANGELOG.md。
验证：Sass编译通过；浏览器320/390/767/768/1440检查多词长标题及连续长词，确认左内边距24px、手机满宽、两行裁切、与Edit不重叠、页面无横向溢出。临时验证通过stdin执行，未新增测试文件。
已按用户“推送live”指令完整pull后只推两份Account样式，API及Skip逻辑未改。live为20261002-a58；回读8 ok / 0 red，两目标逐字节一致，其余文件无变化。基线baseline-20261002-a58；备份prepush-20261002-a58。

---


## Task 59 — 撤回Skip交互，只增加日期格样式（2026-10-02，a57，已上线）

按用户更正撤回a56新增Skip内存/sessionStorage、重复提交拦截、按钮disabled、原日期保留、动态unskip提示及改期清除状态。submit handlers已逐字比对a55基线一致，日期生成恢复upcomingDates原流程。折扣修复保留。
只增加.gb-acct-schedule__day.is-skipped及日期格自身[data-acct-skipped]样式：背景/边框#e6e6e6、文字#999，沿用设计既有token。由后台给实际跳过的日期格添加标记，不在前端判断或记忆跳过状态，不修改API交互。
文件：liquid/account-feedback/snippets/gb-account-data.liquid；assets/account.scss、account.css；account.html、account-login.html（a57）；tools/acctdiscountskip.cjs；docs/account/HANDOFF.md、CHANGELOG.md。
验证：原API提交handlers与a55一致；确认新增Skip状态函数移除；手机/桌面12项检查通过，标记只影响指定日期格，不改变按钮；折扣去重、默认隐藏、空标签回归通过。Sass编译及完整脚本语法通过。
已按用户明确指令完整pull后推送两份样式及data snippet，live为20261002-a57。线上相对a56基线无变化、无冲突；全量回读10 ok / 0 red，三文件逐字节一致，其余无改动、丢失或新增。基线baseline-20261002-a57，备份prepush-20261002-a57。

---


## Task 58 — 折扣chip与跳过状态（2026-10-02，a56，已上线）

折扣结果显式遵守hidden；模板隐藏。contractDiscounts同时按ID和大小写无关的代码去重，合并不同接口形状并避免改写原contract。重复prefill清除旧chip；旧markup首次恢复时持久保存template，避免清空后不能再次生成。自动折扣空金额/0金额标签隐藏，修复空绿色横杠；有真实金额仍正常显示。
Skip成功后保存原日期及预期下一日期，续订排期首格保留原日期并灰显、按钮原生disabled、显示To unskip this order, edit your renewal date。再次提交拦截。主题缺少unskip文字时动态补入，与静态设计已有文案一致。只有成功响应记录状态；失败不记录。成功改日期/频率或立即下单清除记录，当前billing date不匹配或原日期已过去时失效。
限制：当前主题接口没有接入服务端跳过状态字段，此次使用已成功接口操作产生的内存与sessionStorage记录，按订阅ID隔离，同一浏览器会话可恢复；跨设备/新会话已有跳过状态仍需后端返回，未伪造服务端字段。
文件：assets/account.scss、account.css；account.html、account-login.html（a56）；liquid/account-feedback/snippets/gb-account-data.liquid；tools/acctdiscountskip.cjs；docs/account/HANDOFF.md、CHANGELOG.md。
验证：acctdiscountskip手机390/桌面1440共18项通过（默认隐藏、重复渲染、ID/代码去重、自动0折扣、skip成功/失败、重复skip阻断、改期恢复）；--strip去掉代码去重后转红；acctfeedback8 40项通过；Sass编译和完整Liquid脚本去除服务端插值后的JS语法通过。模拟API，未实测真实客户账户。
已按用户“拉取推送”授权完整pull，与a55基线无线上变化。只推account.css、account.scss、gb-account-data.liquid；完整回读10 ok / 0 red，三目标逐字节一致，其余文件无变化。live为20261002-a56；基线baseline-20261002-a56，备份prepush-20261002-a56。最后商品保护保持撤回。

---


## Task 57 — 手机小熊位置（2026-10-02，a55，已上线）

手机小熊 artwork top 从24px改为-17px，上移41px。设计节点2284:27495 y=40851，标题2284:27459 y=40868；桌面和平板不变。
按用户更正撤回本轮新增的最后商品保护逻辑及对应判据，主题订阅逻辑恢复修改前状态。静态 acctQty 已于Task47删除，本轮不恢复。
文件：assets/account.scss、account.css；account.html、account-login.html（a55）；docs/account/HANDOFF.md、CHANGELOG.md。
验证：此前390/767/1440位置和页面无横向溢出检查通过；acctfeedback8 40项通过。撤回后确认主题snippet与a54基线逐字节一致。
已按用户明确指令仅推account.css、account.scss，live为20261002-a55。完整回读8 ok / 0 red，两目标逐字节一致，其余文件不变；新基线baseline-20261002-a55，备份prepush-20261002-a55。不要报成bug：静态步进器没有演示JS。

---

## Task 56 — 小熊外层裁切、输入省略号、手机账户菜单和 Safari 圆点（2026-10-01，20261001-a54 已推 live）

按用户反馈移除 [data-acct-views] 的 overflow-x:clip，改在全宽 .gb-acct 页面边界裁切，避免裁掉版心外小熊，同时不让旋转图片的透明画布造成切换期横向滚动。折扣 input 加 text-overflow:ellipsis/overflow:hidden，保留完整 value。
账户图标原先只有 hover 展开：account.js 创建实际 button 并注册点击开关、外部点击关闭、选项跳转关闭、Escape/焦点离开关闭；桌面 hover 保留。以现有 data-acct-menu 注册，无需修改线上 Liquid。
Safari 地址 radio 的绿色圆点改为 checked 背景 radial-gradient（直径8.8px），明确 -webkit-appearance:none 与 accent-color，关闭原 input::after 圆点，保持16px外圈及 ink 边框。未在用户 Safari 真机复测，不能宣称已真机验证。
文件：assets/account.scss、account.css、account.js；account.html、account-login.html 版本 a54；tools/acctheaderfix.cjs、acctradio.cjs（新增）；tools/acct40check.py、acctlayers.cjs（跟随新规则）。
验证：acctheaderfix 32、acctcover 47、acctradio 16通过。radio 判据在手机/桌面视口叠加线上 Horizon base.css，检查实际截图圆心RGB(0,86,53)，含hover；未只读伪元素。Sass编译及JS语法通过。已按用户明确指令仅推三份 Account 资源；全量回读 10 ok / 0 red，目标文件逐字节一致，其余 637 文件无改动、丢失或新增。基线 baseline-20261001-a54，备份 prepush-20261001-a54。

---

> 最新上线：20261001-a54。三文件回读 10/0，其余 637 文件不变。基线 baseline-20261001-a54。此前 a53 后端订阅周期更新与动态一次性图标保留。

## Task 55 — 八项反馈已上线（2026-10-01，20261001-a53）

已完成第 1–7 项：total/price 自动右对齐；折扣错误/成功反馈与输入框统一 44px 最小高度、8px 圆角；chip 中长代码单独省略并保留删除按钮；移除小熊 artwork 裁切。折扣接受后不再以仅代码的乐观对象提前显示成功，先等待真实订阅刷新后一起显示代码/金额；刷新未确认时明确告知已接受但数据尚未更新，不伪造金额。首页近期订单使用已有 CUSTOMER_ORDERS 在订阅接口之前渲染，无近期订单的续订卡仍需订阅接口。
第 8 项补充：复现正文子节点被替换后新内容增长，旧 ResizeObserver 仍监听已移除节点，overflow:visible 未重新计算，导致内容被裁且无法滚动。现监听正文直接子节点替换、解绑旧节点并绑定新节点，_fit 注册 data-lenis-prevent，手机 sheet 采用 dvh 可视高度（保留 vh 回退）。acctscroll 修复前在 390/add-product 转红，修复后桌面/手机 Add Product 和 Shipping Form 14 项通过，含触摸事件与滚到底部；尚未验证用户具体手机浏览器。
文件：assets/account.scss、account.css、account.js；account.html、account-login.html 资源版本 a53；liquid/account-feedback/snippets/gb-account-data.liquid（基于 baseline-20261001-icons）；tools/acctfeedback8.cjs、acctscroll.cjs。
验证：acctfeedback8 40、acctcover 47、acctlayers 21 全通过；Sass 编译与 JS 语法检查通过；390/768/1024/1440 小熊修改未造成横向溢出，手机截图已检查。模板 API 使用模拟响应，无真实账户写操作。需要推送时重新拉线上基线、保留后端变更，只推指定文件。

---

## Task 54 — Order 图标还原（2026-10-01 已推 live）

按用户提供 SVG 还原 One-off purchase 的 12px 灰色圆圈 1 图标，补 Download Invoice 的 20px 白色下载图标。线上数据层复用第一条订阅商品模板且只换标签文字，导致一次性商品沿用订阅图标；现启动时保存一次性图标，动态渲染按 is_subscription 替换。SVG 路径使用用户原值，省略无裁切作用的重复 clipPath 包装。
文件：account.html；liquid/account-order-icons/snippets/gb-account-data.liquid、gb-account-placeholders.liquid；tools/accticons.cjs。样式与资源版本 a52 不变。
验证：桌面/手机尺寸、颜色、动态商品类型、无溢出 20 项通过；模板 JS 用空 Liquid 数据解析通过。仅推两个 snippets，完整回读 8/0，其余 638 文件无改动/丢失/新增。基线 baseline-20261001-icons，备份 prepush-20261001-icons。未实测真实客户登录态及发票下载接口。

---

> **最新状态（2026-10-01）**：Task 53，20261001-a52 已推 live。手机 ≤767px 的 Account 主视图改为原位淡入淡出，去掉水平滑动；0.5s 和容器高度收拢保留。桌面与登录页不变。acctcover 47 + acctlayers 21 通过；全量回读 8/0，两份样式逐字节一致，其余 638 文件无变化。基线 baseline-20261001-a52；线上后端 data/modals Liquid 更新保留。未测试真实客户登录态。
>
> **不要报成 bug**：手机旧视图现在会逐渐透明，进入视图不再横移，这是本轮明确要求；下方 a48–a51 的覆盖式滑动描述为历史状态。

> **最新修改（2026-09-30）**：Task 52 的 `a51` 已推 live。a50 线上切换未生效的根因：sections/gb-account.liquid 的 .gb-acct__views 缺少 data-acct-views，导致 JS/CSS 覆盖逻辑均未命中。view.init 现在从现有结构类注册该属性，不修改后端 Liquid。以真实线上容器标签替换静态页标签，修复前 6 项失败，修复后 acctlayers 21 + acctcover 43 全通过。已推 account.js + account.scss（版本号）；CSS 与 a50 字节一致，静态 HTML 仅本地。

> **最新上线状态（2026-09-30）**：live 的 account 资源版本为 `20260930-a51`（CSS 内容与 a50 一致）。
> Task 52 的 JS 修复和 SCSS 版本标记已推；此前 Task 48–51 修复也已上线。推前发现线上 gb-account-data.liquid 有后端更新，已保留。
> 最新基线 `baseline-20260930-a51`（640 文件）；acctpush 回读 8/0，两个文件逐字节一致，其余 638 文件零变更、零丢失、零新增。
> 下方旧轮次版本描述保留为历史，以本段及 PUSH-LOG 最新条目为准。本次未重跑浏览器判据。


> account 静态页是 Gumi-Brand 仓库里**独立的一条线**，与 MVP 11 页 + Shopify 主题化那条线
> 并行推进、互不相干。接手先读这份，再按需翻 [PLAN.md](PLAN.md) / [SPEC.md](SPEC.md) /
> [CHANGELOG.md](CHANGELOG.md)。
>
> **最重要的一节是第 5 节「不要报成 bug 的清单」** —— 里面每一条都是有意为之，
> 上一轮审计已经查过一遍。不看就修，等于把裁决过的取舍再推翻一次。

---

## 1. 边界：哪些是这条线的，哪些不是

| | account 线（这条） | 主站线（另一条） |
|---|---|---|
| 页面 | `account.html` · `account-login.html`（Task 28 起含 Sign up 视图） | `index.html` 等 11 页 |
| 样式 | `assets/account.scss` → `.css`（**自带一份变量副本**） | `assets/customstyle.scss` → `.css` |
| 脚本 | `assets/account.js`（自包含 IIFE，不调 `window.gumi`） | `assets/main.js`（`window.gumi`） |
| 版本号 | **`$build-acct`**，当前 `20260917-a39`（live 上还是 `a29`） | `$build`，当前 `r138` |
| 判据 | `tools/acct*.py` | `tools/r*check.py` 等 |
| 文档 | `docs/account/` | `docs/PROJECT-STATUS.md` 等 |

⚠ **同一个仓库里可能另有一个会话在跑主站线**。提交**一律逐个列文件路径**，
不要 `git add -A`，不要碰 `customstyle.*` / `main.js` / `liquid/` / 各 MVP 页 / `docs/` 根下的文件。

⚠ **account.scss 的变量是 customstyle 的副本**，`tools/acctvars.py` 守着它不漂移。
改颜色/断点/字体变量要两边一起改，或者确认那是 account 独有的 token（判据会把它列成
`note account-only token`，不算红）。

---

## 2. 三个页面各是什么

- **`account.html`** —— 单页**九视图**，`[data-acct-view]` 切换、hash 驱动：
  `overview`（Hi Susanna + 当前订单卡 + Refer a friend）/ `subscriptions`（三张订阅卡）/
  `detail`（订阅详情 + 19 类弹窗的入口）/ `orders`（Order History）/ `order`（Order Detail）/
  `details`（My Details 表单）/ `password`（Change Password + 滑出的改密表单）/
  `referral`（Refer a Friend，Task 29 新增）/ `help`（手风琴 + 联系卡）。
  **九个视图都在 DOM 里，任何时刻只有一个不带 `hidden`** —— `tools/acctview.py` 锁这条。
  后五个是决策 C（2026-09-10）加的，**只有 390 手机稿，桌面按 SPEC §5 的外推规则做**。
- **`account-login.html`** —— 未登录态**一页两视图**（Task 28 合并，原
  `account-signup.html` 已删）：`login` / `signup`，同样由 `[data-acct-view]` + hash 驱动，
  两条 alt 行链接（`#signup` / `#login` + `data-acct-goto`）互相切换。
  它用的是**站点 header**（`.gb-header`，Menu / logo / Shop now / 两个图标），
  不是 account header，骨架整套取自 `faq.html`，只有两个 `<main class="gb-acct-auth">` 是自己的。
  ⚠ **`.gb-acct-auth` 有 `display:flex`，压过 UA 的 `[hidden]{display:none}`** ——
  靠 scss 里那条 `&[hidden]{display:none}` 才真的藏得住。删了它两个视图会同时显示，
  而判据**照样全绿**（`querySelector` 取第一个）。

**桌面与手机是两套并存、不是一套折叠**：桌面左侧竖导航 9 项，手机是页内列表卡 6 项 +
右上角下拉面板 4 项，767 互斥切换。

⚠ **导航要改就得同时改三处**（桌面竖导航 / 手机页内列表卡 / 手机汉堡面板），
少改一处手机就进不去那一页。`acctview.py` 会比对三处的可达集合。

⚠ **`Contact Preferences` 是有意留成不可点的** —— 它连手机稿都没有，做了就是自造内容。
别看着别人都活了就顺手把它接上。
⚠ **`Refer a Friend` 原本也在这一列，Task 29（2026-09-15 需求方指示）把它做出来了** ——
同样没有任何板，整页照 funkyfood 的模块搭，每个数值和每句文案都登记在
CHANGELOG Task 29 的末节，等设计方回话。

---

## 3. 命令速查

```bash
# 编译（唯一正确的编译方式，sass 不在 PATH）
npx sass@1.77.8 --no-source-map assets/account.scss assets/account.css

# 改完必须一起 bump：源码里的 $build-acct + 三个页面各两处 ?v=
grep -rn '20260917-a39' assets/account.scss account*.html
```

⚠ **改了 scss 一定要重编译**。判据读的是 `account.css`，忘了编译会得到「改了没生效」
的假红，或者更糟 —— 假绿。

---

## 4. 判据与基线

**全绿才算完**。任何一条红就停下修，不要标「已知问题」放过。

| 判据 | 基线 | 说明 |
|---|---|---|
| `python3 tools/acctcheck.py` | **848 ok / 0 red** | 结构与数值，按 (页面, 宽度, 动作) 分组 |
| `python3 tools/acctmodal.py` | **1321 ok / 0 red / 1 aborted** | 19 类弹窗，**约 4 分钟，后台跑** |
| `python3 tools/acctview.py` | **26 ok / 0 red** | 八视图互斥、hash 路由、三处导航的可达集合一致 |
| `python3 tools/acctvars.py` | 54 ok / 0 red | 变量副本没漂移 |
| `python3 tools/assetpath.py` | GREEN | scss 里的 `url()` 必须是 `assets/` 内裸文件名 |
| `python3 tools/acctbp.py` | **2356 declarations / 0 red** | 断点值档互斥、阈值不带数值 |
| `python3 tools/r25check.py` | **40 ok / 0 red** | Task 25 十条（链式断言已随 Task 26 撤回移除）。⚠ req 9 已随 Task 31 从 flatpickr 改写成 `.gb-acct-cal` 的五条 |
| `python3 tools/r26check.py` | **42 ok / 0 red** | Task 26 六条：下拉/图标/禁用光标/折扣码/撤回链式。⚠ 下拉那段的选择器已随 Task 27 换成 `.gb-select__*` |
| `python3 tools/r27check.py` | **29 ok / 0 red** | Task 27 三条：桌面 520/90vh、抽屉从底部滑入、State 换站点下拉 + 绿边 focus |
| `python3 tools/acctdiff.py` | **647 paired / 162 differ / 50 unmatched** | 稿 TEXT 节点 vs 页面的字号·行高·字距·字重·颜色。**162 里 156 是 footer**（SPEC F，主站线），另外 6 条是稿件自身问题（Lexend 的 Sign up ×2、Contact Preferences 的 disabled 灰 ×2、My Subscription 色 ×2），差异数不为 0 是预期 |
| `python3 tools/accthover.py` | 41 hover properties / 0 red | 每个 hover 属性都有对应过渡 |
| `python3 tools/acctmotion.py` | 10 ok / 0 red | reduced-motion 真的覆盖到了（Task 28 删掉 signup 页那项）|
| `python3 tools/r29check.py` | **44 ok / 0 red** | Task 29 五条：改密滑出、手风琴 slide、Help 链接、菜单移进图标、Refer a Friend |
| `python3 tools/r30check.py` | **53 ok / 0 red** | Task 30 四条：按钮 hover 归队、灰块换占位图、图标去位移、Copy 限宽 |
| `python3 tools/r28check.py` | **32 ok / 0 red** | Task 28：一页两视图、点链接互切、hash 路由、未知 hash 不爆栈、入场动画 |
| `python3 tools/iconclip.py` | **51 ok / 0 red** | 每个 icon 的墨迹必须落在自己的 viewBox 里（Task 31 新增）。**用画的不用算的**：`d` 里的弧参数会和坐标混在一起，数值包络会报一堆幻影溢出 |
| `python3 tools/acct32check.py` | **66 ok / 0 red** | Task 32 两条：三张订阅卡各开在自己的状态、restart 弹窗的日历。⚠ 取「只属于 paused 的元素」要用 `[data-detail-only='paused']`，`~=` 会把 `"active paused"` 那 9 个也算进来 |
| `python3 tools/acct31check.py` | **437 ok / 0 red** | Task 31 三条：日历组件、桌面内文与下拉方向、弹窗锁屏。⚠⚠ **Task 33 重写了第 3 段**（144→389），因为旧版是**假绿**：它跑在 `prefers-reduced-motion: reduce` 下，而那正是 `main.js` 里 `smoothScroll.init()` 提前 return 的条件 —— **Lenis 从来没在判据里跑起来过**，于是漏掉的 `lenis.stop()` 一路读绿，真实浏览器里弹窗照样能滚。现在这一段独立开 `no-preference` 的 context、**先断言 Lenis 真的在**，再在**遮罩上**（面板体有 `data-lenis-prevent`，那里试不出来）滚轮；另补 390 档、`rest → open → after` 三态、`PageDown`、关闭后交还滚轮。**约 6 分钟** |
| `python3 tools/acct34check.py` | **29 ok / 0 red** | Task 34 七个值 + 侧栏圆点。⚠ 其中一条**跑 `index.html`**：`.gb-header__cta` 的 32 是 account 线的作用域覆盖，必须同时证明 MVP 页仍读客户的 40，否则改 customstyle 也能读绿 |
| `python3 tools/acct33check.py` | **52 ok / 0 red** | Task 33：汉堡没有点击开关、header 不再变色、两颗图标不再 hover 淡出、汉堡换成站点购物车图标、图标 hover 面板照旧。⚠ 最后两条跑在 `has_touch=True` 的上下文里，钉的是「触屏点汉堡什么都不出」这个**有意**的结果 |
| `python3 tools/acct37check.py` | **42 ok / 0 red** | Task 37 两条：产品下拉箭头 20、成功屏 Close 退回 Current Address。⚠ 箭头那组的关键断言是**「等于普通字段的箭头」**而不是「等于 20」—— 前者才证明它不再是特例；另**必须先断言 `.gb-select` 真被 `selectBox` 画出来了**，否则整组读的是不存在的元素 |
| `python3 tools/acct38check.py` | **80 ok / 0 red** | Task 38：三个日历换 flatpickr。⚠ 皮肤那组的关键断言是**「列距 == 容器宽 ÷ 7」** —— 只验「七列等距」会假绿，`display:block` 下日格紧挨排列也是等距的（40 而非 43.14）。另⚠ **`css()` 遇元素不存在报红不抛异常**，否则删掉 `minDate` 会让脚本崩在第一条上、红数少算 |
| `python3 tools/acct40check.py` | **68 ok / 0 red** | Task 40：切换动效两段、跳过态、视频自动播放、折扣行对齐。⚠ 切换过程**只在中途存在**，探针 `click()` 之后不等就读，锚点是「此刻屏幕上有 2 个视图」；⚠ `overflow-x: clip` 用它真正防住的后果验 —— 动画中途 `scrollWidth > clientWidth` 必须为假；⚠ 跳过态配反向锚点「另外三块没变」，否则一条「所有日期块都变灰」的规则照样读绿 |
| `python3 tools/acct43check.py` | **19 ok / 0 red** | Task 43：去重标记必须是 property 不是 DOM 属性。⚠ 四段都把标记放到**模块运行之前**：能在 `modal.open` 之前打属性的就那样做，`init()` 装的（My Details 表单 / 手风琴）用 **`cloneNode(true)`**（复制属性、不复制 property）。⚠ **不能「重置 property 再手动 bind」** —— 那会装第二套监听器，第一版判据的 `+1` 读成了 `+2`。⚠ 手风琴锚点**必须点第 2 行**，第 1 行板上就是展开的，点它是收起 |
| `python3 tools/acct44check.py` | **104 ok / 0 red** | Task 44：弹窗内下拉不被面板裁。⚠ **option 从 init script 注入**（任何页面脚本之前），让 `selectBox` 从加长的 `<select>` 正常构建；手写 `.gb-select__list` 的 innerHTML 量的是组件没生成过的 DOM，读数是 `listH=0` 的假象。⚠ 断言是**「两边都没被裁 + 装不下的滚得到」**，不是「它能滚」 —— 4–5 项那档内容不到 224、列表没有滚动条，被裁的部分任何方式都到不了 |
| `python3 tools/acct45check.py` | **57 ok / 0 red** | Task 45：九处客户设定的间距值。⚠ 每条都断言两次（声明 + 它真正移动的那个像素），因为这些数**不再有板号可查**。⚠ 行距量的是**相邻的两个 `.gb-acct-row`** —— 中间隔着 `__actions` 与 `__rule`，取 `rows[0]`/`rows[1]` 会跨过它们，第一版就是这样报了两条假红。⚠ 1440 那一列是**反向锚点**（23.5 / `0 4px` / 无 strip margin），丢了 `@include narrow` 才转红。⚠ 钉了「品名仍是一行」—— `item__main` 的 12 是从名字列扣的，手机上只剩 2px 余量 |
| `python3 tools/acct42check.py` | **21 ok / 0 red / 0 skipped** | Task 42：线上预渲染的日历壳 + 不可选日期的光标。⚠ **静态页没有那个壳**，判据自己搭出线上的形状再驱动 `_arm`；锚点是「探针真的注入了壳」，少了它会在静态页本来的形状上读绿。⚠ 光标三条跑在**探针自己标记的日子**上，与「这个月有没有过期日」无关 —— 否则每月最后一天视图开在下个月，三条断言在空集上恒真。⚠ 去掉 `pointer-events` 之后「点了选不中」**只能靠行为验**（`force=True` 真点一下）。⚠ 读 computed `cursor` 判不出光标能不能用（`pointer-events:none` 时它仍是 `pointer`），所以 `pointer-events` 那条断言必须同时在 |
| `python3 tools/acct41check.py` | **16 ok / 0 red** | Task 41：390 下九视图墨迹底到波浪的留白。⚠ **必须用像素不能用 computed style** —— 盒间距本来就都是 48，读 `padding-bottom` 在改之前也全绿；差的是墨迹。⚠ 五条锚点（pager 在 / 壳还是 45 / 仍是 stack 最后一个 / 父级是 stack / 真读到 `-14px`）少一条都能让「删掉分页条」读绿。⚠ detail·details 断言的是 **51** 不是 48，那 3 是行盒半行距、有意没抹 |
| `python3 tools/acct39check.py` | **29 ok / 0 red** | Task 39：切换动效、问候语居中、手机圆点、refer 对齐。⚠ 动效读的是 **`getAnimations()`** —— `effect.getKeyframes()` 直接列出关键帧动了哪些属性，「手机去掉透明度」没有别的不靠计时的读法；⚠⚠ **context 必须显式 `reduced_motion="no-preference"`**，默认值会压平时长、在一个没跑的动画上读全绿。位移类断言全部配锚点（「盒子确实比内容高」），否则「上下相等」会恒真 |
| `python3 tools/rwd.py account.html` | 全绿 | 14 档溢出扫描。⚠ **跑四条**：`account.html` / `account.html#referral` / `account-login.html` / `account-login.html#signup` —— 首屏 `hidden` 的视图不带 `#` 那一趟扫不到。⚠ 另外七个视图（subscriptions / detail / orders / order / details / password / help）**至今没跑过**，见 CHANGELOG Task 29 顺带发现 |

⚠⚠ **`tools/rNNcheck.py` 是主站线的命名空间，account 线不要再占用它。**
本轮的判据一开始写成 `tools/r31check.py`，**当场覆盖掉了主站 Round 31 的判据**
（它在 HEAD 里，`git status` 显示成 `M` 而不是 `??` —— 这是唯一的信号）。已 `git checkout`
还原，本轮判据改名 `tools/acct31check.py`。
`r25`–`r30check.py` 侥幸没撞（主站那几轮的文件不在 HEAD 里），但 **`r31` / `r32` 都被占着**，
下一轮如果顺号写 `r32check.py` 会再撞一次。**account 线一律用 `acctNNcheck.py`。**
⚠ 新建 `tools/` 下的文件前先 `git ls-tree -r HEAD --name-only tools/ | grep <名字>`。

⚠ **Task 31 的三处计数变动**：`acctbp` 2297 → **2286**（−11 = 删掉的 flatpickr 皮肤）；
`r25check` 36 → **39**（req 9 从 flatpickr 改写成日历组件的五条）；
`acctmodal` 的三处断言改了口径（copy 宽改成「可用宽 − 板上的 30」、body 的 `overflow-y`
允许**不滚的** `visible`、Lenis 探针强制把 `overflow-y` 设回 auto 再测）。

⚠⚠ **Task 40 让四个既有判据的采样时机必须变长** —— 退出动画 500ms，旧视图在这段时间里
**还在屏幕上**，300/450ms 就读会读到两个视图、甚至读到旧视图里同一句话的那一份：

| 判据 | 改动 |
|---|---|
| `acctview` | 切视图后 300 → **700ms** |
| `acctcheck` | 三处 450 → **750ms**（⚠ `goto-detail` 走的是另一段代码，漏了只修好一半）|
| `acctdiff` | 400/500 → **750ms**（否则报出 3 条莫名其妙的颜色差异）|
| `acct39check` | 选择器 `.gb-acct__view:not([hidden])` → **`.is-entering`**，`getAnimations()[0]` 否则可能读到退出那一个 |

**断言本身一条没放宽，只动了什么时候读。**

⚠ **Task 43 / 44 的计数变动**：全部判据持平（两轮只改 JS，`account.css` 与线上逐字节相同）。
⚠⚠ **`r29check` 在 Task 43 的回归里 42/2 红**，两条都是切视图后等 500ms 读到旧视图还在流里 —— **Task 40 的回归清单里没有 r28/r29/r30，所以那轮漏检了**。本轮把切视图后的两处改成 **750**，断言没放宽，回到 **44 ok / 0 red**。⚠ 其余判据的 `wait_for_timeout(500)`（`r28`/`r30`/`acct33`/`acct34`/`acct37`）等的是面板打开不是切视图，当前全绿，没动。

⚠ **Task 45 的计数变动**：`acctbp` 2356 → **2363**（+7 = 七条新增声明：`product__now` 的 `margin-left`、`sub__body` narrow 的 `row-gap`、`.gb-acct-row` 的 `margin-top`、`schedule__days` narrow 的 `padding` 与 `margin`、`item__main` 的 `padding-right`、`.gb-acct-rule` 的 `margin-top`；另外四处是改值不是新增）。⚠ **两条既有判据的期望值跟着改了**：`acct38check` 的日历 padding `20px 24px` → `20px 22px`、`acctmodal` 的 `listGap` `12px` → `12.5px` 与 holiday 日历的 `contentPadX` `24px` → `22px`（⚠ **日历的 padding 有三处判据在钉**，改一个值要找齐：`acct38check` / `acctmodal` / 新的 `acct45check`） —— 同一处改动，不是放宽断言。其余判据全部持平。

⚠ **Task 42 的计数变动**：`acctbp` 2353 → **2356**（+3 = 日历禁用态从一条规则拆成两条，多出一组 `color`/`background`/`pointer-events`）。其余判据全部持平。

⚠ **Task 41 的计数变动**：`acctbp` 2352 → **2353**（+1 = 分页条的 narrow `margin-bottom`）。其余判据全部持平。

⚠ **Task 40 的计数变动**：`acctbp` 2327 → **2352**（+25 = 退场那组规则 + 跳过态一节 + `__unskip`）；
`acct31check` 413 → **437**（+24）。⚠ **后者不是新增覆盖** —— 它按 `data-acct-modal` 的**名字**
遍历触发器而 `querySelector` 永远返回第一个同名元素，unskip 那行又引入了一个 `edit-date`
触发器，于是同一个弹窗被重复测了一遍。别把这 24 条当成新保障。

⚠ **Task 39 的计数变动**：`acctbp` 2317 → **2327**（+10 = `justify-content` 1、
`.gb-acct-list__link` 的 `column-gap` 1 + `::before` 7、`.gb-acct-refer__text` 的 `padding-top` 1、
`.gb-acct-refer` 的 `align-items` narrow 档 1，减去 `.gb-acct-order__head` 删掉的 `row-gap` 1）。
其余判据全部持平，`acctdiff` 仍是 647/162/50。

⚠ **Task 38 的计数变动**：`acctbp` 2299 → **2317**（+18 = flatpickr 皮肤比手写结构多）；
`iconclip` 53 → **51**（−2 = 两个日历箭头从 HTML 搬进了 `account.js` 的字符串，扫不到；
**页面里那 44 条一条没少**）；`acct31check` 409+4红 → **413**（三条「没有 vendor picker」
的反向断言已反转成「插件必须在」）。`acctmodal` 仍是 1321，但**网格断言换了口径**：
flatpickr 固定画六周 42 格，自研版是按月份画（九月 35 格）。

⚠ **Task 37 的计数变动**：`acctbp` 2302 → **2299**（−3 = 删掉的 `.gb-acct-prod__control .gb-select__arrow` 三条声明）。其余判据全部持平。

⚠ **Task 36 的计数变动**：`acctmodal` 1315 → **1321**（+6 = video 段新增三条 × 两个宽度）；
`acctbp` 2298 → **2302**（+4 = `.gb-acct-video__media` 的四条声明）。

⚠ **Task 35 的计数变动**：`iconclip` 79 → **53**。它的取样是「`images/*.svg` 每个文件一条
+ 两个页面里按 `class + viewBox` 去重后的 inline svg」。删掉 26 个文件后是
**7 文件 + 46 页面 = 53**，删之前是 33 + 46 = 79。**页面那 46 条一条没少** ——
少的全是文件那一侧，图标覆盖面没有缩水。

⚠ 计数变动都是**预期的**，不是漏跑：Task 25 把 `edit-date` 的面板高度断言改成 NOTE
（稿里没有日历，290 已无可比性），`acctmodal` 1314 → 1313；Task 27 把 `shipping-current`
的截断拆成「声明」+「在 390 下真生效」两条，又回到 1314；**Task 32 让两个日历都默认收起，
面板高度回到板上的值，于是 `restart` 的高度写成真断言、`edit-date` 那条 NOTE
也恢复成断言，1314 → 1315**。
**Task 33 的两处计数变动**：`acctcheck` 849 → **848**（删掉 header 展开态那条 box-shadow
断言，另两条颜色断言改成静止色）；`acctbp` 2292 → **2286**（−4 = `.gb-acct-header.is-open` 两行 + 它专用的 `transition` 两行，
再 −2 = `__link` 的 `opacity` 与它的 `transition`）；`accthover` 42 → **41**。

`acctdiff` 的 168 → 166 是**判据修好了**：它原先没看 `visibility`，把 Task 25 那个
靠 `visibility:hidden` 淡出的账号菜单当成可见文本量了进去（多报 9 条）。

**那条 abort 是预期的，不是欠验证**：`account.html@390` 的「开弹窗页面有没有横移」。
手机画的是 overlay 滚动条、不占布局宽度，锁滚动时没有宽度被释放，也就没有横移可测。
**桌面档（1440）这条是真跑了的** —— 判据启动 chromium 时去掉了 Playwright 默认的
`--hide-scrollbars`，拿到真滚动条再测。

### 写判据时会踩的坑

- ⚠ **批量改 HTML 只能整体 `re.sub` 或从后往前替换**。`list(re.finditer(...))` 之后在循环里
  改同一个字符串，第二次起位置就是错的 —— Task 26 因此两次把标签切坏（`type=<div`、`dat<button`），
  一次还让三个面板的下拉从 7 个变成 10 个。**收尾必须跑一次 `html.parser` 的标签配对校验**，
  `grep -c` 数不出这种损坏。
- ⚠ **`max-height: min(720px, calc(...))` 会被 Sass 静默丢掉** —— Sass 有自己的 `min()`，
  参数含 `calc()` 时整条声明消失且**不报错**。用两条规则（基准值 + 高度阈值）代替。


- ⚠ **测「页面横移」必须挑右对齐的元素**。滚动条在右边，锁滚动释放它的宽度时，
  左对齐的东西（`.gb-acct-nav`、logo）**一动不动** —— 实测：补偿开着是 0px，
  把补偿强行关掉**还是 0px**。判据因此恒真过。现在测的是 `.gb-acct-header__icons`
  的 `right`，关掉补偿会稳定报 15px。
- ⚠ **负向断言（"已无 XXX"）先验锚点**。`acctcheck.py` 的 `absent` 在元素不存在时算过，
  所以每组的第一条都是 `("vis", ".gb-acct-auth", True)` 之类的锚点。
- ⚠ **`checkVisibility()` 默认不看 `visibility` 属性**。靠 `visibility: hidden` 藏起来的
  元素会被当成可见，`innerText` 给出一个空字符串混进结果。`acctdiff.py` 在 Task 27、
  `acctcheck.py` 在 Task 29 各中过一次 —— 两处现在都写 `{visibilityProperty: true}`。
- ⚠ **`height: 0` + `overflow: hidden` 不等于 `[hidden]`**（Task 29）。它只是视觉裁切：
  内容仍在无障碍树里、里面的链接和输入框**仍可 Tab 聚焦**。凡是用高度动画做折叠的，
  收起态都要再补一条 `visibility: hidden`，否则读屏会念出全部折叠内容、
  焦点会跳到看不见的输入框里。
- ⚠ **`pg.click()` 之后鼠标停在落点上，Playwright 是认 `(hover: hover)` 的**。
  切视图之后新视图往往正好在那个位置放了个按钮 —— 于是 hover 色被当成静止色量进去。
  `acctdiff.py` 因此多报过一条假差异（signup 提交按钮 `#ffffff` 读成 hover 的 `#004128`）。
  凡是 click 之后要读颜色的判据，补一句 `pg.mouse.move(0, 0)`。
  ⚠ **这个污染可以潜伏很久**：`acctmodal` 里指针不是 click 留下的当场读到的，而是
  更早一次 click 留在原地、抽屉后来开在它底下。Task 30 之前按钮 hover 只改 `opacity`、
  判据读的是 `background-color`，于是**污染一直在、判据一直绿**；本轮把 hover 改成变色，
  它当场变成 3 红，读数还是**过渡中途色**（`rgb(167, 226, 94)`，既不是绿也不是 lime）。
  见到中途色就该想到指针，而不是去调容差。修在共用的 `_open()` 里，不是三个调用点各补一次。
- ⚠ **auth 页的选择器也要带视图前缀了**（Task 28）。`.gb-acct-auth__title` 现在匹配两个元素，
  signup 组不加 `[data-acct-view="signup"] ` 前缀的话 `text` 断言读到 login 的文案，
  而 `css` 断言**会碰巧全绿** —— computed style 在 `display:none` 子树里照样返回规则值。
  ⚠ `.gb-acct-auth` 本身是视图元素，前缀要写成同元素形式（`[data-acct-view="login"].gb-acct-auth`，不带空格）。
- ⚠ **`innerText` 在 `display:none` 子树里不套 `text-transform`**（徽章会读成 `Active`
  而不是 `ACTIVE`），而且三个视图同名元素并存 —— 选择器**必须带
  `[data-acct-view='<name>'] ` 前缀**。
- ⚠ **读「状态切换后的颜色」要等够过渡（≥450ms）**，等 120ms 读到的是插值。
  ⚠ **Task 29 起手风琴与改密表单是 400ms 的高度动画**，而收起的那一段要等 `animationend`
  才退出无障碍树 —— 判据等**正好 400ms** 会读到两条答案（`acctcheck` 的 `help-open-2`
  中过，时灵时不灵）。这类等待一律给到 700ms。
- ⚠ **headless 里 `(hover: hover)` 恒 false**，hover 只能用 Playwright 实测，不能靠读 CSS。
- ⚠ **`scrollHeight` 会被关闭态的下拉列表污染**（Task 31）。每个 `.gb-select` 都把
  绝对定位的 `__list` 留在 DOM 里，它算进 `scrollHeight` —— 一个肉眼毫无溢出的面板
  报出 62px 溢出。`modal._fit()` 因此量**静态流**（body 直接子元素的 rect 底边）。
  ⚠ **判据不能照抄这个算法** —— 自洽不等于正确。`acctmodal` 改成把 `__list` 临时
  `display:none`、再读浏览器自己的 `scrollHeight`：消掉污染源，度量仍是权威的那个。
- ⚠ **从 Figma 裁出来的 viewBox 不含描边**（Task 31）。`absoluteBoundingBox` 是几何外框，
  居中对齐的描边有一半在框外 —— `absoluteRenderBounds` 才是墨迹。判 icon 有没有被裁
  **要用渲染**（`tools/iconclip.py` 画两遍比对），别去解析 `d`：弧命令的 flag 会被
  当成坐标读，误差能到几百单位。
- ⚠ **活性自检要逐条突变**。「一批一起改、红了就算过」会漏掉早退分支里的死属性 ——
  Task 10 就这样漏过 10 条。
- ⚠ **探针往被测元素里塞东西，收尾只能移除自己塞的那块**，不能 `innerHTML=''`
  或整体还原：前者抹掉真内容，后者重建节点让 JS 捕获的引用失效。
- ⚠ **`acctdiff.py` 的四个坑**（会假绿或假红）：`<input>` 的文字在 `.value`/`@placeholder`
  不在子节点；Figma 把一句拆成两个 TEXT 而 DOM 是一个元素（两个名字都要进索引）；
  桌面板的假舞台是 Figma 的 Safari 组件、手机板是 `Chrome browser`，名字不同要分别剔；
  **同串文字多次出现时两边都要按 y 排序**，否则两栏布局会把页面标题配到导航项上，
  报出一对 `24->14` / `14->24` 的假差异。
- ⚠ **判据里任何"点开弹窗"的分支，末尾都要按 Escape 关掉**。不是切不过去 ——
  `open()` 里 `if (already) this._hide(...)` 会替换当前面板（Task 37 实测连切四个正常，
  旧版这里写着「换不掉」，**已过时**）—— 而是**锁不会自己松**：`is-modal-open` 留在
  `html`/`body` 上，后面的检查会全量测到 `0px`。这个 bug 在 `acctmodal.py` 里藏了很久，
  因为那条分支一直在 abort、从没执行过。

---

## 5. 不要报成 bug 的清单

下面每一条都是**有意为之**或**稿件自身的问题**，已经查过、已经拍过板。
逐条的出处在 [SPEC.md](SPEC.md) 第 7 节（待裁决）与第 8 节（稿件错误）。

### 5a. 稿里就没有的东西

- **`Chrome browser` 假舞台没做**（手机稿顶上的浏览器地址栏、电量、home indicator）。
- **左侧导航的灰色圆点是待设计的图标占位**（便签 `27602`），不是漏切图标。
- **三个 icon 槽在板上是 `visible=false`**：两个 CTA 的图标（View Order / Manage
  Subscription）与手机问候区的返回箭头。**Figma 导出不含隐藏节点，所以整块 board SVG
  在那个位置没有 path —— 「裁不出来」是确认，不是失败。**
- **订阅卡的产品缩略图是 64×64 的纯 `#d9d9d9`**，设计里根本没有产品图。
- **挽留屏的"视频"是纯 `#d9d9d9` 矩形 + 播放键**，没有 imageRef。
- **登录/注册两页没有 footer CTA 区块** —— 两张桌面板的 `Footer CTA` 都是 `visible=false`。
- **无稿的两项（Refer a Friend / Contact Preferences）只在导航里、不可点**，
  渲染成 `aria-disabled` 的 `<span>`，既不是死链也不建页面（待裁决 C）。

### 5b. 稿自带的错字与自相矛盾（已按更可信的一版实现）

| 稿上写的 | 我们做的 | 出处 |
|---|---|---|
| `Sign up` 桌面标题是 **Lexend** 36/44 | PP Palma 800 32/40（同 Log in） | 全套 112 个节点只有这一处 Lexend，它自己的手机板是 PP Palma |
| 手机 `Forgot you password?`（少个 r） | `Forgot your password?` | 桌面板拼写正确 |
| 手机 Sign up 副标题少 `your` | 补上 `your` | 桌面板有 |
| 桌面 note 卡 472 宽 vs 表单 480 | 都做 480 | 两个手机板本来就同宽 |
| 桌面 auth 的次要文字 `#656565` | 照做（新增 `$c-gray-650`），手机 `#666666` 照做 | 全套 `#666666` 1022 次、`#656565` 只有 3 处 |
| `30107` 的取消原因有重复项 | 照抄 | 稿自带 |
| `34192` 把 subscription 拼成 `subscoption` | 照抄 | 稿自带 |
| `33116`/`33119` 的 `Delivery Instrctions` | 照抄 | 稿自带 |
| `30465` 的 July 2026 月历排错（1 号排在 Su 列、有一格写 `32`） | **不照抄**，日历是算出来的 | 照抄等于交一个排错的死日历 |
| 三个桌面稿全叫「Account Overview Desktop」 | 按 24px 标题认，是三个不同页面 | 复制未改名 |
| 桌面 CANCELLED 卡删的是 Shipping 行 | 按便签 + 手机稿删 Renewal 行 | 便签 `28323` 明写 |
| 桌面 PAUSED 卡日期还是 `19 Jul 2026` | 按手机稿 `17 Aug 2026` | 便签 `28321` |
| 同一地址两张板邮编 `3182` / `3181` | 各按各自的板 | 需设计方给出哪个对 |

- **`acctdiff.py` 报的 168 条差异里 160 条是 footer** —— 稿上的 footer 是另一个组件
  （两栏平铺、多 `Homepage`/`PDP`/`Influencers`、按钮写 `Subscribe now`、链接 16/24/600/0），
  现站是三栏。SPEC 决策 2 与待裁决 F 已登记，`customstyle.scss` 的 `.gb-footer__link`
  注释也写着 pending。**改它等于改 MVP 11 页**，等设计方回话再动。
- **字距 0 是按钮与徽章的正确值，不是漏填** —— 稿上 `ACTIVE` / `Save` / `View Order`
  这类的 `letterSpacing` 就是 0，正文才是 -0.02em。`.gb-acct-order__cta` 写 `0`、
  `.gb-acct-btn` 写 `-0.32`，各自对应它们所在的板，别统一。

### 5c. 有意的实现取舍

- ⚠ **`images/` 下不再有 `acct-*.svg`，这是有意的**（Task 35 删了 26 个）。两个页面的图标
  **全部是 inline `<svg>`**，一个外部图标文件都不引。看到「有图标却没有对应 svg 文件」
  别当资源丢了 —— 节点号与取回路径在 [NODE-MAP.md](NODE-MAP.md) 末尾。
  ⚠ 其中 `acct-qty-*` / `acct-*-chevron` 四个是**废件**（紧贴 bbox / 已换成 selectBox），
  别按对照表把它们复原回去用。
- ⚠ **挽留屏灰块里的 `<video>` 没有 `src`，这是有意的**（Task 36，需求方要的就是占位）。
  空 `<video>` 在 Chrome 里不画任何东西，所以看到的还是 `#d9d9d9` 底色 + 白色播放键 ——
  **「灰块长得和以前一样」不等于 video 没加上**，要看 `video.gb-acct-video__media` 这个元素。
  播放键是纯装饰的 `<span>`，**没有任何 handler，点不动是对的**。
  ⚠ 父级的 `role="img"` / `aria-label` 现在是对的（里面确实没有可播的东西），
  但客户一接上 `src` 就必须删 —— 细节见 CHANGELOG Task 36 的「遗留」。
- **侧栏圆点是 `::before` 画的，不是资源** —— 板上它是个填 `#D9D9D9`、frame 名叫
  `placeholder` 的空图标槽，看着像占位；**需求方 2026-09-16 明确「圆点不是占位而是 css 样式」**，
  所以九行（含两个 disabled 行）都画。别当占位删掉，也别去找 svg。
  ⚠ 16.67 读回来是 **16.6562**（Chrome 吸附到 1/64 px），判据按 16.67 断言会在正确的文件上报红。
- ⚠⚠ **`.gb-acct-menu` 的 `right` 跟着 `.gb-acct-header__icons` 的 `column-gap` 走** ——
  `calc(-48px - var(--pad-x))` 里的 48 = 24（图标间距）+ 24（第二颗图标）。
  动了 `column-gap` 不改这里，面板就离开视口右边缘。**源码看不出来**，`r25check` /
  `r29check` 的 `panel right edge flush` 是唯一信号（Task 34 当场抓到过一次）。
- ⚠ **`.gb-acct-schedule` 没有自己的规则** —— `account.html:427` 是
  `class="gb-acct-sub__body gb-acct-schedule"`，它的 gap 全部来自 `__body`。
  改 `__body` 就是同时改续订日程块，这是 Task 34 客户改 23.5 时一并动的，不是漏改。
- **`.gb-header__cta` 在 account 两页是 32、其余 11 页是 40** —— 32 写在 `account.scss`
  的 auth 段，靠 account.css 排在 customstyle.css 之后取胜。**别去改 customstyle 的 40**，
  那是主站线 r78 客户定的值。

- **锁屏是「三条 CSS 规则 + 一对 JS 调用」，四样缺一不可**：
  `customstyle.scss` 1893–1910 的三条（锁在 `html`、`body` 用 `overflow-x: clip` 而非
  `hidden`、`padding-right` 只补 `html` 一边），**加上 `account.js` 的
  `smoothScroll('pause')` / `('resume')`**。
  ⚠⚠ **少了那对调用，锁在真实浏览器里是形同虚设的** —— Lenis 用 `window.scrollTo` 落位，
  `overflow: hidden` 挡不住程序滚动。Task 33 之前一直缺，判据也一直看不见（见 §4 那条）。
- ⚠ **`shipping-success` 脚部的 `Close` 不关窗，它退回 `shipping-current`**（Task 37，
  需求方 2026-09-17）。属性是 `data-acct-modal="shipping-current"`，不是
  `data-acct-modal-close` —— **看到一颗写着「Close」却不 close 的按钮，那是有意的**。
  ⚠ **右上角的 × 与遮罩仍然是真关闭**，只有脚部那颗改了语义。别为了「统一」把三者接成一样，
  `acct37check` 把 × 的行为一并钉住了。整条链现在是个闭环：
  `shipping-current → shipping-form → shipping-success → shipping-current`，锁全程不松。
  ⚠ **退回去看到的仍是旧地址**（静态站不回写表单），这是既有行为、闭环之后才看得出来，
  已登记等拍板 —— 别顺手写个 JS 把表单值填回卡片，那是自造「已保存」的假数据。
- ⚠ **产品下拉的箭头是 20，不是板上 `84:8161` 画的 10**（Task 37，需求方 2026-09-17）。
  实现方式是**删掉 account 那条覆盖**、让它落回 `customstyle.scss` 的 `.gb-select__arrow`
  基类（那里就是 20/20/20）—— 所以在 `account.scss` 里**搜不到任何 20**，别当漏写。
  同段的 button / option 仍是 40/14 的小号档，需求只点名 arrow。
- **购物车图标不要接 `data-modal="gb-cart"`** —— 这页没有抽屉，而且 `main.js` 的 modal 与
  `account.js` 的锁会互相解锁。它现在是 `href="#"` 的死链，等客户决定跳哪。

- ⚠ **`.gb-acct-menu` 只剩 hover 一条路，触屏与键盘都打不开它** —— Task 33 按需求去掉
  汉堡的点击开关。面板写在 `@media (hover: hover)` 里，承载 hover 的
  `.gb-acct-header__link--account` 又是个不可聚焦的 `<div>`。
  `acct33check` 用 `has_touch=True` 的上下文把它钉成断言，别当 bug 修回去。
  **但没有链接因此失联**：那四条在桌面 `.gb-acct-nav`、手机 `.gb-acct-list` 里全都有，
  内层视图还有 `.gb-acct-intro__back` 回总览。丢的是面板，不是导航。
- ⚠ **header 不再随菜单变色** —— 板 `34854` / `34804` 画的是展开时整条 bar 提亮到
  `#f6feec` 加一像素描边；Task 33 按需求整条删掉，bar 只剩 `$c-lime-150` 一个颜色。
  与稿不符是**需求方的决定**。
- **汉堡按钮是惰性的** —— 板上有这颗图标所以留着，但它不再控制任何东西，
  HTML 里标了 `<!-- TODO client link -->`。它的 `gb-acct-vh` 标签「Account menu」
  已名不副实，等客户决定接什么。
- ⚠ **两颗 header 图标没有自己的 hover 了**（Task 33 第 2 条，`opacity: 0.6` 已删，
  连带那条已成死代码的 `transition`）。这是**铁律 13 的例外**：账号图标仍有反馈
  （`::after` 的 lime 下划线 + 掉出来的面板），汉堡本就是惰性的。
  `.gb-acct-header__logo` 的 `opacity: 0.7` **没动**，需求只点名 `__link`。
- **Order History 的两个翻页箭头都是 `disabled`** —— 静态站只有一页可翻。
  左箭头在第 1 页本来就该禁用；右箭头是没有第 2 页可去。接后端时才有真分页。
- ~~**Help 的手风琴展开/收起没有高度动画**~~ —— **Task 29 反转**：需求方 2026-09-15
  要求参考站内其他页面 / jQuery 的 slideUp/slideDown。答案改成
  `__panel`（跑高度）+ `__a`（富文本内容），由 `account.js` 的 `slideTo()` 以
  400ms + `cubic-bezier(0.42, 0, 0.58, 1)` 驱动 —— 那是 `main.js` 给站点手风琴用的同一组值，
  注释写明是 jQuery 默认值与 `swing` 的近似。板上仍然没画过渡，这是需求方的决定。
  ⚠ **没有复用 `main.js` 的 `accSlide`**：它一半代码在处理 `<details>` 的坑，
  而 account 这边是 `button + aria-expanded`，何况 `main.js` 是主站线的文件，这条线不碰。
- **`27116` 没有单独实现** —— 它与 `27081` 逐字相同、同高 2206（待裁决 O）。
  不是漏了一页。
- **My Details 的姓名两栏是外推的** —— 手机稿上 First/Last name 是上下堆叠，
  桌面无稿。按 Sign up 桌面板 `35059` 做成两栏、≤767 塌回堆叠（决策 AC）。
- **`Opt in to order updates via text message` 是一行说明文字、不是 checkbox** ——
  板上就没画勾选框（决策 AD）。
- **订单状态 `Shipped` / `Delivered` / `Cancelled` 三者同色** —— 板上全是 `#1a1a1a`，
  没有徽章也没有色块（决策 AE）。订阅那边的三态才有徽章，别照着改。
- **`Download Invoice` 按钮做出来了** —— 便签 `27444` 说「Only do if very very very
  cheap. Otherwise, remove.」这是**待裁决 I**，照稿实现、等回话，不是自作主张。
- **桌面两栏 gutter 是 244 / 352 不对称** —— 三个桌面稿完全一致，判定为有意，没改成居中。
  ⚠ **Task 23 起这两个数不再是 `__inner` 自己的 padding**：改成了 `max-width: 952px`
  居中 + `padding-right: 108px`，套在 `.gb-acct` 的 `--pad-x`（80/20）里，
  1440 档算出来仍是 244 / 352，但 1440 以上会锁住而不是继续撑开。
  看到 `padding-left: 0` **不是 gutter 丢了**，判据改用 `rect` 量几何。
  内容列用 `minmax(0,1fr)` 而不是稿上的固定 571：**照抄则 768 档横向溢出 864 > 768**（实测）。
- **弹窗滚动锁复用站内的 `is-modal-open`，没有另起一套**。自己写一套（html+body 都
  `overflow:hidden` + 两边都补 `padding-right`）实测坏两处：`.gb-acct-header` 是
  `position: sticky`，body 变成 scrollport 后**当场掉出视口**；补偿付了两遍滚动条宽度。
- **弹窗里的滚动区把 `data-lenis-prevent` 直接写在标签上**，没有去登记 `main.js` 的
  `smoothScroll.PREVENT`（PLAN Task 8 步骤 4 原本要求登记）。行为等价，而且不必碰主站线的文件。
  ⚠ `main.js` 的 PREVENT 扫描**只在 init 跑一次**，所以后加的容器登记了也没用。
- **account.scss 没有写 blanket 的 `prefers-reduced-motion` 规则**。
  `customstyle.scss` 顶部已经有一条 `*, *::before, *::after { ... !important }`，
  account.css 在它之后加载，所有过渡本来就被压平了 —— 再写一遍是死代码。
  `tools/acctmotion.py` 证明了它确实够得着（并且用 `no-preference` 的读数做不变量对照，
  防止「元素压根没有过渡」也算过）。
- **弹窗头脚的分隔线用 `box-shadow: inset`，不是 `border`** —— 稿上是
  `strokeAlign: INSIDE`，用 border 会让每个面板比板高 2px。
  ⚠ 但**卡片框**（地址 `32448` / 成功 `32932`）的 `strokesIncludedInLayout` 是 `true`，
  那里要写**真 `border`**。同一批板里两套规则，改之前先查这个字段。
- **弹窗的脚固定 72 高（抽屉 80）**，哪怕里面只有一个 Cancel。没按钮的面板自然高只有 52，
  所以 `min-height` 是写死的。
- **贴底抽屉是定高不是上限**：五张挽留板全是 `v:FIXE 672`，用 `max-height` 会让内容少的屉缩水。
- **登录/注册用站点 header 而不是 account header** —— 板上的 instance 就是站点那个组件，
  未登录访客也没有 account 菜单可开。
- **auth 的提交按钮没有用站点的 `.gb-btn--lg`**：那个类在 ≤767 会掉到 44 高（客户 r133 的决定），
  而稿上的手机按钮**仍是 52 高**。account 线本来也是「按钮全自写」（`account.html` 里
  `.gb-btn` 出现 0 次）。
- ⚠ **`edit-date → need-now → edit-frequency` 那条链是错的，已撤回**（需求方 2026-09-15：
  「之前的逻辑搞错了……是我看错了」）。全页只剩两条真链式：`shipping-form → shipping-success`
  与 `cancel-offer-skip → cancel-skipped`。`r26check.py` 第一段锁着，别再接回去。
- **Flavour / Size 现在是可交互下拉** —— 这**反转了便签 30913**（「flavour 暂不可编辑」），
  是需求方 2026-09-15 的指示，不是漏看便签。选项 `Flavour option 1/2/3` 是占位，板上没有。
- **`<select>` 还在 DOM 里，只是 `opacity:0`** —— `acctSelect` 只画可见层，值仍由原生控件持有
  （脏值门控、表单、判据读的都是它）。别看到"看不见的 select"就删。
- **数量变化会进脏值快照** —— `acctForm._snapshot` 除了 `[data-acct-field]` 还读
  `[data-acct-qty-value]` 的文本，否则改数量不解锁 Save。
- **最后一个产品归零 → `product-locked`** 是用既有的 `data-acct-modal` 委托接的，
  那个面板（`2284:33847`）早就实现了，这轮只是给它接上触发器。
- ⚠⚠ **日历是 flatpickr 画的，皮肤才是 gumi 的**（Task 38，需求方 2026-09-17：
  「采用和 funkyfood 一样的插件」+「样式调成 gumi 设计的这种样式」）。
  **这是第三次改主意**：Task 25 引入 flatpickr → Task 31 删掉改自研 → 本轮回到插件但留住板上的外观。
  三个实例（`edit-date` / `restart` / `cancel-holiday`）**全部**换了，自研的 `acctCal` 渲染已删。
  ⚠ **别照旧记录去找 `[data-acct-cal-day]` / `[data-acct-cal-title]` / `tbody button`** ——
  现在是 `.flatpickr-day` / `.flatpickr-current-month` / `.flatpickr-*`，映射表在 CHANGELOG Task 38。
  ⚠ **`flatpickr.min.css` 没有引入，这是有意的** —— 外观 100% 是我们的，那 16KB 每条都要被覆盖。
  代价是 `account.scss` 里 `.dayContainer` 的 grid、`.flatpickr-months` 的 flex **是承重的**，
  删了就没有网格了。`acct38check` 用「列距 == 容器宽 ÷ 7」锁着。
  ⚠ **年份是个可编辑的 `<input type=number>`**（插件结构，funkyfood 那边也一样），
  板上是纯文本。spinner 已藏、外观一致，但能打字改年 —— 稿里没有这个交互面，已登记等裁决。
- ⚠ **日历固定画六周 42 格**（Task 38）。自研版按月份画（九月只有 35 格），
  flatpickr 固定六周是为了面板高度不随月份跳动，**改不掉**。日历因此比旧版高一行 40px。
  看到「格子比板上多一行」不是 bug。
- ⚠ **没有字段的日历（`cancel-holiday`）默认选中明天，有字段的（`edit-date`）不预选** ——
  板 `30669` 填了正好一天，而 `edit-date` 的字段值 `19/07/2026` 已过期，
  预选会显示一个和输入框对不上的日子。**两者不一致是对的**，`acct38check` 两边都钉住了。
  ⚠ Task 38 第一稿把这个分支写丢了（holiday 一天都不选），是 `acctmodal` 的
  `selCount == 1` 抓出来的 —— 源码审查看不出来。
- ~~**日历图标仍被拉伸**~~ —— **Task 31 修掉**，连同另外 8 个被裁的 icon。
  ⚠ **图标比它的框小是对的**：viewBox 现在指的是 icon 在板上的**槽**（20×20 / 24×24 / 16×16），
  墨迹本来就小于槽（叉号是 12 在 24 里）。旧写法拿几何外框当 viewBox，
  居中描边的一半落在框外被裁 —— Figma 的 `absoluteRenderBounds` 就是这么说的。
  **别看到「图标变小了」就把 viewBox 改回墨迹框**，`tools/iconclip.py` 锁着这条。

- ⚠ **`.gb-acct-modal__copy` 是 `calc(100% - 30px)`，不是板上的 320**（Task 31）。
  板上画的是 `320` 在 `350` 的内容盒里 —— **30 的留白才是组件，320 不是**。
  写死 320 会让 520 宽的桌面面板按手机宽度折行、右边空 150。手机档算出来仍是 320。
- ⚠ **弹窗关闭时的 `focus()` 带着 `preventScroll: true`**（Task 31），别删。
  焦点交还发生在**锁刚松开之后**，不带这个参数浏览器会把触发按钮滚回视野 ——
  页面在面板淡出的同时跳走（实测 `edit-name` 600→0、`cancel-offer-skip` 600→1445），
  看起来就像 sticky 布局被弹窗弄坏了。**锁本身一直是对的**，这条源码审查看不出来。
- **`.gb-acct-modal__panel` 用 `overflow: clip`，不是 `hidden`** —— `hidden` 会把面板变成
  滚动容器，body 里越过折线的字段（`shipping-form` 的 suburb，y=740 vs 可视区 732）就滚不到了。
  改回 `hidden` 会让 `acctmodal.py` 报 `element is not visible`。
- **`shipping-form` 的 Save 不带 `data-acct-modal-close`** —— 它靠
  `<form data-acct-modal-next="shipping-success">` 前进，而且是全页唯一带 `required` 的面板：
  加了 close 会让 click 委托的 `preventDefault()` **绕过浏览器原生校验**，填错也关窗。
  ⚠ 判断某个 save 是不是链式，**要同时看按钮的 `data-acct-modal` 和它所在 form 的
  `data-acct-modal-next`**，只扫按钮会漏。
- **视图切换只有「进场」动画，没有出场** —— `[hidden]` 是 `display:none`，不能过渡；
  出场要等播完再切，得引入状态机。桌面淡入上移、≤767 从右滑入，**首屏不播**。
  ⚠ 动画类由 `view._enter()` 在 `animationend` 摘掉 —— 留着的话 fill 状态会**冻结该子树后续所有
  transition**，表现为「类还在、值不动」。
- **`account.html` 有 40 条注释**：Task 25 把 33 条**节点定位**注释移去了 `NODE-MAP.md`，
  Task 32 应需求方要求补回 36 条**功能**注释（每个视图、每个弹窗、每个结构块一句）。
  两者不是一回事 —— **节点号仍然不进 HTML**，要查某块对应哪张板还是翻 `NODE-MAP.md`。
  `account-login.html` 同理有 6 条。
  ⚠ 前端源码线上可直接下载，这些注释是**对外可见**的，别往里写内部状态或未决事项。
  移走的 33 条定位注释在 **`NODE-MAP.md`** —— ⚠ `27680` / `27766` / `27860` / `27980`
  这些区块级节点号**别处都没有**，要查某块对应哪张板只能翻那份。
- **Edit Date 的日历用的是 `cancel-holiday` 那张板的 `.gb-acct-cal`**（Task 31 反转）。
  `Edit Date` 那张板上确实只有输入框，但 `30465`（Heading away on holiday）画了日历，
  需求方 2026-09-15 点名要它。⚠ **Task 38 又把引擎换回了 flatpickr**（见上面那条）——
  `assets/flatpickr.min.js` 回来了，但 `.gb-acct-datepicker` 那套 funkyfood 皮肤没有回来，
  也**没有** `flatpickr.min.css`。
  ⚠ **Task 32 起日历默认收起**，点字段（`.gb-acct-field__input`，日历图标是
  `pointer-events:none` 的覆盖层，点它一样穿透到 input）才 400ms 滑出，再点收起。
  收起态挂 `:root.acct-live`，脚本挂了日历就常驻可见。`cancel-holiday` 那张板的日历
  **不受影响**（没有 `data-acct-cal-for`，绑定挂不上）。
  ⚠ **输入框的 `19/07/2026` 已经是过去的日期**，所以日历展开时**不预选任何一天**、
  月份落在第一个有可选日的月。这不是 bug：落在 July 会给一个整月点不动的日历，
  钳到明天又会高亮一个和输入框对不上的日子。上线换真实数据后这个分支自然不走。
- **订单三态有两个钩子**（`gb-acct-order--<state>` 类与 `data-acct-order-state` 属性），
  两个都会选中状态。⚠ **改一个不改另一个，两种状态会同时显示** —— `acctcheck.py` 的
  切换动作已经同步改两个，自己写探针时也要。
- **`cancelled` 态那批禁用元素没有 `not-allowed` 光标** —— 它们靠 `pointer-events: none`
  挡点击，而这与 `cursor` 互斥（元素不再是命中目标，光标解析退回父级）。不是漏写。
- ⚠ **弹窗 body 的 `overflow-y` 会被 JS 改成 `visible`**（Task 31 的 `modal._fit()`）。
  `main.js` 的 `selectBox` 让下拉避开最近的裁切祖先，而 `overflow-y: auto` **不滚也照样裁** ——
  短面板里的下拉因此一律翻上、盖住自己的 label。不需要滚的 body 就不当裁切盒。
  **看到 inline style 上的 `overflow-y: visible` 不是脏数据。**
  ⚠ **`edit-frequency` / `edit-product` 往下开、`add-product` / `shipping-form` 往上开，
  两个都是对的** —— 后两个的内容是真的要滚，往下会被滚动区裁掉。
  ⚠ 判断「这个 body 要不要滚」**不能用 `scrollHeight`**：每个关闭态的 `.gb-select`
  都把绝对定位的列表留在里面，它会被算进去，于是肉眼毫无溢出的面板报出溢出。
- **手机 auth 的间距比桌面大**：按钮 ↔ alt 行 ↔ note 卡，桌面 32、手机 **48**。两套板都是这么画的。
- **9 个下拉用的是站点的 `.gb-select`，account 自己没有下拉组件**（Task 27 起）。
  样式在 `customstyle.scss`、行为在 `main.js` 的 `selectBox`，account.scss 只有两条适配规则
  + `.gb-acct-prod__control` 的 40/14 小号档。⚠ **想改下拉外观先确认改的是不是全站**。
  Task 26 自建的 `acctSelect` 已删，别照旧记录去找。
- **`<select>` 旁边没有 chevron `<svg>`** —— `selectBox` 在自己的按钮里画。
  没有 JS 时的箭头由 `select.gb-acct-field__input` 的 `background-image` 提供，
  `.gb-select__button` 再把它关掉（照抄 `.gb-field__input--select` 的写法）。
- **8 个抽屉面板共用一个入场**：`--sheet` 在 767 以下是 `translateY(100%)`。
  需求只点名 Edit Product，但板上这 8 个是同一个 672 贴底抽屉，故一起改。
- **桌面弹窗 520 宽 / 90vh 高是 2026-09-15 的裁决，反转了 2026-09-10 的「沿用 390」**，
  来源是 funkyfood account 门户的 `.delivery-*-pop-up .content`。手机仍是 390。
- **输入框 focus 是绿描边不是蓝色 outline**（Task 27），与站点其余页面的 `.gb-field__input` 一致。
- ⚠ **`.gb-acct-sub__thumb` / `__item__thumb` / `__referral__hero` 是 `<img>`，不是带底色的空盒**
  （Task 30）。它们指向 `images/product-placeholder.png`（400×400 `#d9d9d9`，Task 26 导出）。
  别看到「一张纯灰图」就当资源丢了 —— 板上本来就是纯灰块，没有产品照。
  ⚠ hero 的 `width/height="400"` 只给比例，真正定形的是 CSS 的 `aspect-ratio: 16 / 9`。
- ⚠ **按钮 hover 一律翻 lime（`#b5ed61` + `#004128` 字），不是变暗也不是淡出**（Task 30）。
  这是 `customstyle.scss` 里 `.gb-btn` 的房规，不是 account 自选。
  `:disabled` 不参与 hover，靠 `&:not(:disabled)` 而不是靠 `opacity: 1` 抵消。
- ⚠ **账号菜单在账户图标 `<div>` 里面，图标不再是链接**（Task 29）。
  `<a>` 里不能再套 `<a>`，菜单四项都是链接，所以图标只能是 `<div>`；需求本来也要求
  去掉它的点击效果。**图标盒子 `align-self: stretch` 撑满 bar 高是功能不是排版** ——
  原来图标只有 24 高，鼠标从它走到面板的那 28px 空隙里 hover 断掉、面板会在伸手途中淡掉。
  ⚠ 菜单的 `right: calc(-40px - var(--pad-x))` 同理不能简化成 `0`：定位父级已经是那个
  24px 的盒子，`0` 会让面板差 120px（16 + 24 + gutter），判据实测过。
- **改密卡上的说明文案是我们改写的**（Task 29）。板 `27151` 写的是「会给你发一封重置邮件」，
  但需求方要的是 funkyfood 那种内联表单，两者对不上，文案已按表单改写并标 `TODO 待客户文案`。
  三个密码字段稿上**完全不存在**，是照 funkyfood 的结构搭的。
- **`Refer a Friend` 整页没有设计依据**（Task 29）。结构照 funkyfood，hero 是灰块、
  code 是 `GUMI-0000`、四个分享按钮都是 `href="#"`、金额口径沿用 overview 卡的 $20。
  ⚠ **没有复用 `images/refer-friends.jpg`** —— 那张图里有第三方品牌 logo，
  而且一卡一图的规矩不允许它冒充第二处用图。
- **改密表单与手风琴的折叠态都挂在 `:root.acct-live` 上**（Task 29，复用 Task 28 的门）。
  写死的话 `account.js` 一挂就是「七条答案里六条永久看不到、改密表单永远打不开」。
  ⚠ 但**这层门目前在 account.html 上是空转的** —— 九个视图本身仍是无条件 `[hidden]`，
  无 JS 时只有 overview 可达。已登记，等拍板。
- **合并页的 `<title>` / `<meta description>` 只有 Log in 那一份**（Task 28），切到 signup
  视图不会跟着变。静态站不值得为此加 JS；Shopify 化时 `customers/login` 与
  `customers/register` 是两个 template，各自带 title，问题自然消失。
- **`view.show()` 的未知 hash 回落是 `views[0]`，不是 `'overview'`** —— auth 页没有
  overview，硬编码会**无限递归爆栈**，而 `modules` 循环的 try/catch 把异常吞成
  一行 `console.error`，页面只是「两个视图都不显示」。别为了「读起来明确」改回去。
- **两个 auth 视图共用一套入场动画**（`.gb-acct-auth.is-entering` 加进了
  `.gb-acct__view.is-entering` 的选择器列表），没有为 auth 另写 keyframes。
- ⚠ **auth 页的 `[hidden]` 规则挂在 `:root.acct-live` 上，这不是多余的门**（Task 28）。
  `hidden` 属性写在 HTML 里是**无条件**的，而合并后 Sign up 只能靠 JS 切出来 ——
  `account.js` 404 或顶层抛异常就**永久拿不到注册表单**。`.acct-live` 由 `account.js`
  跑到最后一行时才加（挨着 `window.gumiAcct` 赋值），所以脚本挂掉时两个表单都露出来、
  都能提交。**别为了「少一层」把门去掉**，`r28check` 的 `java_script_enabled=False`
  那组锁着它。
- ⚠ **`account.html` 的八视图没有这层门**（既有行为，Task 28 只处理了 auth 页）：
  `account.js` 挂掉那边只剩 overview。已登记进 CHANGELOG Task 28 的「顺带发现 / 未修」，
  等拍板，**不要当 bug 顺手修**。

- ⚠ **视图切换 0.5s（`$t-view`）是需求方点名要的**（Task 39，2026-09-17：「切换右侧模块
  动画过渡速度太快，需放慢」）。**别把它并回 `$t-slow`** —— 那一档同时喂着弹窗淡入淡出，
  合并等于把弹窗一起拖慢。`$t-view` 目前只有 `.gb-acct__view.is-entering` 与
  `.gb-acct-auth.is-entering` 在用，这是对的。
- ⚠ **手机端从右划入的关键帧里没有 `opacity`，是故意删的**（Task 39，同一次需求）。
  桌面那条 `gb-acct-view-in` 仍然淡入。两条**共用同一个时长**，手机只换 `animation-name`
  不换 shorthand —— 要让手机比桌面更慢，必须再开一档，不是改现有的数。
- ⚠ **`.gb-acct-hello` 的 `justify-content: center` 推翻了 Task 3 的注释**
  （「板 136 而内容 108，多出来的 28 是文字**下方**的空白」）。需求方 2026-09-17 要求上下平分，
  源码注释已改写。**别照着旧 changelog 把它改回去。**
- ⚠ **`.gb-acct-refer` 桌面居中、手机顶对齐，是两块板各自的样子**（Task 39）：
  `2284:27780` 的 `counterAxisAlignItems: CENTER`（箭头 y=44=24+(80−40)/2），
  `2284:27639` 的箭头 y=16=padding-top。需求原文说「去掉 align-item center」但另外两条都在说手机，
  故只在 ≤767 撤掉。**看到桌面还居中不要当漏改。**
- ⚠ **`.gb-acct-refer__text` 手机的 `padding-top: 3px` 实际只下移 1.5px** —— 父级
  `.gb-acct-refer__body` 是 `align-items: center`，盒子高 3、居中后只走一半。需求方是在
  DevTools 里试出来的，看到的就是这个结果，**故按原值落地，别"修正"成 6px**。
- ⚠ **`.gb-acct-order__head` 手机端没有 `row-gap` 声明，不是漏写**（Task 39）——
  需求要 0，不写就是 0，少一条声明。判据按「状态行上沿 == 标签行下沿」断言，不读属性。
- ⚠⚠ **两处导航行左侧的灰圆点是占位，不是定稿的样式**。设计方 2026-09-17 书面澄清：
  “These grey circles are placeholders for Icons which have yet to be designed.”
  ⚠ 这**推翻了 2026-09-14「圆点不是占位而是 css 样式」那句答复** —— 和便签 `27602`
  原本写的一致。**代码不用改**（占位本来就得画出来），但它属于「上线前必须替换」，见 §6 与 SPEC 8b。
  图标到位后换的是 `.gb-acct-nav__link::before` / `.gb-acct-list__link::before` 这两条
  （给 `background-image` 或换成真元素），**不是加新结构** —— 20 的槽、gap 12、文字左沿 48 都留着。

- ⚠⚠ **`[data-acct-views]` 上的 `overflow-x: clip` 是承重的，不是修饰**（Task 40）。
  手机切换是整整一个容器宽的对推，不夹住就会撑出横向滚动条。
  ⚠ **不要改成 `overflow: hidden`** —— `hidden` 会建立滚动容器并把另一轴一起变成 `auto`，
  下拉和 sticky 都会受影响；`clip` 不建滚动容器，`overflow-y` 留在 `visible`。
  `acct40check` 在动画中途量 `scrollWidth > clientWidth` 钉着这条。
- ⚠ **登录页没有退出动画，是故意的**（Task 40）。它的两个 `<main>` 是 body 的直接子元素、
  下面就是 footer，把其中一个抽出流会让 footer 当场往上跳半秒。`view._leave()` 以
  `[data-acct-views]` 为门，CSS 用同一个 hook。判据反向断言了这件事，**别「顺手补上」**。
- ⚠ **`view._leave()` 里那两行守卫都踩过**（Task 40）：`animationend` **会冒泡**，
  视图里任何子元素的动画都会提前触发收尾（判 `e.target !== el`）；
  快速切走又切回来时，**上一次退出的监听器会把刚回来的视图 `hidden` 掉、整页空白**
  （`show()` 开头先 `_endLeave()`）。两条判据各钉了一个。
- ⚠ **`.gb-acct-schedule[data-acct-skipped]` 默认不挂**（Task 40）。静态站没有订单数据，
  默认挂上就是编数据。灰的只有 `:first-child` —— 便签 `30908` 说只能跳**下一单**。
- ⚠ **`+4 More Products` 的文案按板不按便签**（Task 40）。便签 `28326` 写的是后端规则
  （多于一件才出现、数字是其余商品数），正文还把 subscription 拼成了 `subscripition`；
  板上六个实例渲染出来的字全是 `+4 More Products`。规则登在 SPEC，文案别改。
- ⚠ **`.gb-acct-summary__row` 的 `align-items: flex-start` 不是手滑**（Task 40）。
  板 `28774` 里 51 字符的长码折成四行、框高 72，而 `Discounts` 与 `Tag` 的框顶仍在同一条线上。
  其余几行两边等高，`center` 与 `flex-start` 渲染完全相同。

- **`detail` 与 `details` 的底部留白是 51 不是 48**（Task 41）。九个视图的**盒**间距全是 48；
  这两个视图以纯文字收尾，多出的 3 是段落行盒的半行距。抹平它要按字体度量反向补偿，
  脆且只为两个视图存在。**看得出来的那一个是 `orders` 的 62，已拉回 48。**
  ⚠ **桌面没动** —— 需求只说手机端，1440 下这 14 落在 144 的留白里。
  `acct41check` 反向钉了「1440 下 pager 的 `margin-bottom` 仍是 0px」。

- **相邻月的补白格（`prevMonthDay` / `nextMonthDay`）点不动，是有意的**（Task 42）。
  它们保留 `pointer-events: none`，因为点一下会让 flatpickr **跳一个月**。
  ⚠ 代价：`nextMonthDay` 里晚于 minDate 的那几天**其实是可选的**，也被一起挡住了，已登记待拍板。
  ⚠ 也因此**只有「打开那个月」的禁用日有 `not-allowed` 光标** —— 补白格同时带
  `.flatpickr-disabled`，而它们自己那条规则排在后面。

- **弹窗里的下拉会自己决定向上还是向下开、并可能被限高**（Task 44 的 `acctSelectFit`）。
  矮面板（`edit-frequency`）里列表会被限到 132/128 并可滚，这是**有意的** ——
  面板 `overflow: clip` 会裁掉溢出部分，而 4–5 项那一档列表自己没有滚动条、被裁的内容够不到。
  ⚠ **`MIN: 96` 是自定值**（约两行）。⚠ 高面板（`shipping-form`）不限高，保持共享的 224。
- **Task 45 的九个间距值全是客户设定，与板上的数不一致**（原处的板号注释还在，别照板"修回去"）：
  `.gb-acct-item__names` 的 `row-gap: 0`（板上 2，品名与 Flavour 的行盒现在直接相接）、
  `.gb-acct-item__text` 的 8（板上 6）、`.gb-acct-reasons` 的 12.5（板上 12）、
  `.flatpickr-calendar` 的 `20px 22px`（板上 20/24）。
  ⚠ **`.gb-acct-row` 与 `.gb-acct-rule` 的 `margin-top: -1px` 是全宽的**，且各有一个看着像 bug 的后果：
  行的负 margin 也作用在**第一行**上（首行离卡片 `padding-top` 少 1px），
  rule 只抬自己（上 23 / 下 24，**不对称**）。
  ⚠ **`.gb-acct-schedule__days` 手机端 `margin: 0 -3px`** 让日程条探出卡片内边距 3px，是有意的。
  ⚠ **手机端 `.gb-acct-sub__body` 的 `row-gap: 24` 同时作用于续订日程块** ——
  `.gb-acct-schedule` 自己没有任何规则，它的间距一直是从 `__body` 读的（与 Task 34 同一处耦合）。
- **模板里那 9 处 `data-acct-watched="1"` 现在是无害的死属性**（Task 43）。
  JS 已改用元素 property，不再读它们；建议对方顺手清掉，但**留着也不影响**。

### 5d. 预览时会以为坏了、其实没坏

- **Overview 的三种订单状态、订阅列表的三态、详情的折扣态，都没有 JS 会自己切**。
  预览要在 devtools 里改属性：
  `[data-acct-order-state]` = `preparing` / `shipped` / `renewal`；
  `.gb-acct-detail[data-acct-discount]` = `applied`；
  **`.gb-acct-schedule[data-acct-skipped]`**（Task 40，跳过下一单：首块变灰、按钮变禁用、
  下方多出 `To unskip this order, edit your renewal date` 一行）。
  ⚠ **详情的 `data-acct-sub-state` 是例外（Task 32 起）**：点哪张订阅卡的 CTA 进来，
  detail 就开在哪个状态（`view._subState`，便签 `28323`）。手改属性仍然有效，
  但下一次从列表点进来会被覆盖。**直接开 `#detail` 时是 HTML 里写的 `active`。**
- **表单提交只会跳回 `#`** —— 三个页面的 form 都是 `action="#"` 的静态壳。
- **`.wowo` 入场动画在 account 页没有用**，页面不会淡入。
- **三个视图都在 DOM 里**，devtools 里能同时看到三份同名元素 —— 只有一个不带 `hidden`。

---

## 6. 上线前必须替换的占位内容

⚠ 这些混在正文里看不出来，不单独列就一定会带上线。完整表在 [SPEC.md](SPEC.md) 第 8b 节，
其中**最要紧的一条**：

- **`images/refer-friends.jpg` 画面里有第三方品牌 logo（帽子上的 Prada 标）**。
  它是设计稿用的市售摄影素材，客户站点直接用有商标风险，授权来源未知。

⚠ **两处导航行左侧的灰圆点也在这张表里**（`.gb-acct-nav__link::before` 9 行 +
`.gb-acct-list__link::before` 6 行）——设计方 2026-09-17：“These grey circles are
placeholders for Icons which have yet to be designed.”**图标还没设计**，`#D9D9D9`
是 Figma 的默认占位灰。别因为它是 CSS 画的就当成已定稿。

⚠ **`+4 More Products` 的 4 是示例数**（Task 40）。便签 `28326` 说这行只在订阅里多于一件
商品时出现，数字是「其余商品数」；静态站没有商品数，接后端时要一起实现。

其余是示例姓名（`Hi, Susanna`）、示例日期、示例价格（小计与总计都写着 `$00.00`）、
示例订阅数据、四条重复的产品行、以及三处 `href="#"`
（View Order / Refer a Friend / Forgot your password）。
⚠ **Task 33 把 header 的汉堡换成购物车后多了第四个 `href="#"`**，等客户决定跳购物车页还是接抽屉。
⚠ **Re-Activate Subscription 已于 Task 32 接上路由**，从这张表里移出。

---

## 7. 现状与遗留

**PLAN 136/137 步**，**Task 1–45 全部完成**（Task 16–22 是决策 C 拍板后加的五个视图，
Task 23 外壳版心化 + 波浪朝向，Task 24 全量文本对照扫描，Task 25–27 是需求方三轮交互修改，
Task 28 把登录与注册合成一页，Task 29 是需求方的交互五条，Task 30 是 hover / 占位图 / 限宽四条，
Task 31 是 icon 裁切 + Edit Date 换本站日历 + 桌面弹窗内文 + 弹窗锁屏三条，
Task 32 把 Reactivation 接上路由并给 restart 弹窗挂日历，
Task 33 header 四改：拆掉汉堡的点击菜单与 header 变色、去掉图标 hover、
补上弹窗锁屏缺的 Lenis 暂停、汉堡换成购物车图标，
Task 34 auth 链接变色 + 波浪底色 + 五处尺寸 + 侧栏圆点，
Task 35 删掉 26 个没人引用的 `images/acct-*.svg`，
Task 36 挽留屏灰块里补一个不带 `src` 的 `<video>` 占位，
Task 37 产品下拉箭头回到共享的 20 + 成功屏的 Close 退回 Current Address，
Task 38 三个日历换回 flatpickr、皮肤照 30465 重写，
Task 39 视图切换动效放慢 + 问候语居中 + 手机列表补圆点 + refer 卡对齐，
Task 40 切换改成推进/退出两段 + 跳过下一单的态 + 视频自动播放 + 折扣行顶对齐，
Task 41 手机端各视图底部间距拉齐 —— 差异只在墨迹不在盒，`orders` 结尾的分页条比别的视图低 14，
Task 42 修掉线上的双日历（模板预渲染一份壳、flatpickr 又 append 一份）+ 给不可选日期加 `cursor: not-allowed`，
Task 43 **线上九处 Save 全是死的** —— `data-acct-watched` 这个运行时去重标记被抄进了 liquid，守卫读到自己上一世的标记就 return，门控从未安装；四个同族标记一起改成元素 property，
Task 44 弹窗内的下拉选项一多就被面板 `overflow: clip` 裁掉且够不到 —— `acctSelectFit` 接管方向与高度，
Task 45 需求方的九处间距微调 —— 全是客户设定值，其中四条不只是一个数：`.gb-acct-row` 的 −1px 是全宽且会抬起首行、手机 `row-gap: 24` 连带动了日程块、`item__main` 的 12px 是从名字列扣的（手机上只剩 2px 余量）、日程条探出内边距 3px）。
⚠ **两处列表每行右侧的 5×10 chevron 都仍未实现**（侧栏板 `34631`、手机卡板 `27617`
的第二个 icon 槽），需求没提过。⚠ 左侧那个灰圆点**两处现在都有了**（侧栏 Task 34、手机卡 Task 39），但设计方 2026-09-17
已澄清**那是待设计图标的占位、不是定稿样式**，上线前要换（SPEC 裁决 D / 8b）。
**两个页面**、九视图 + auth 两视图、20 类弹窗、37 个弹窗态全部落地。

⚠ **Task 31 删掉了 flatpickr**（`assets/flatpickr.min.js` / `.css`）。这两个文件**从未提交过**
（一直是 untracked），所以删除不必进提交 —— 但拉下旧工作副本的人手上还有，别当成资源丢了。

⚠ **Task 1–24 已推送到 `origin/main`，Task 25–45 做完但未提交** —— 等推送指令。
✅ **线上 = 本地 `20260918-a44`**（2026-09-18 共推四批：a40 九个文件、a41 三个、a43 两个、a44 两个）。
⚠ **a44 只推了 `account.css` / `account.scss`** —— Task 45 一行 JS 都没改。
⚠ **a43 只推了 `account.js` / `account.scss`** —— Task 43/44 都只改 JS，`account.css` 与线上**逐字节相同**，
所以不在清单里。⚠ **两个静态页 `account.html` / `account-login.html` 永远不进推送清单**
（主题侧已用自己的 liquid 接管）。
✅ **2026-09-18 已推：`assets/account.css` / `.js` / `.scss` 与 live 主题一致，同为 `20260917-a40`**，
另补了四个模板已在引用却 404 的 asset。回读 22 ok / 0 red，见 [PUSH-LOG.md](PUSH-LOG.md)。
⚠ **两个静态页 `account.html` / `account-login.html` 不在主题里**（主题侧已用自己的 liquid 接管），
所以它们永远不进推送清单。
⚠ **提交时有 27 条删除要一起进去**：`account-signup.html`（Task 28，否则拉下来的人会同时
看到旧页面和合并页）+ `images/acct-*.svg` × 26（Task 35）。三者都已 `git rm`，在暂存区里。

⚠ **需求文档 `account修改任务文档.txt` 每轮就地改写、旧内容不留痕**，
历史三轮的原文只在 CHANGELOG 的 Task 25 / 26 / 27 条目里。
⚠ **Task 28 与 Task 29 的需求根本不在那份文档里** —— 都是 2026-09-15 对话里口头给的，
原话只在 CHANGELOG 对应条目里。

- ⚠⚠ **`figma/` 整个目录不在 git 里** —— 26 张原始节点 JSON、整板 SVG、`cut-icons.py`、
  `fetch-*.py` 全部只在这台开发机上，克隆仓库的人一份都拿不到。Task 35 只把 26 个图标的
  节点号救进了 `NODE-MAP.md`，**其余设计源仍然只有一份**。要不要入库请拍板。
- ⚠ **`~/.cache/ms-playwright/chromium-1217` 已不存在**。playwright 1.58 装的是 **1208**，
  1217 是过时残留、被清掉了。`tools/` 下**约 150 个脚本**把 1217 写死在 `CHROME` / `EXE` 里。
  本轮把 `acctcheck.py` 与 `acctmodal.py` 改成扫 `chromium-*` 取最新，**其余脚本没动**
  （多数是主站线的）。为了让它们继续能跑，留了一条软链
  `~/.cache/ms-playwright/chromium-1217 -> chromium-1208`：在 `~/.cache` 里、不在仓库、
  不会被同步脚本推上线。**要重装 playwright 之前先 `rm` 掉它。**
- **`account.html` 的主站资源版本号还停在 `?v=20260909-r134`**，两个 auth 页写的是 `r138`
  （与 11 个 MVP 页一致）。主站线的批量替换看来不含这三个文件，需要 account 线自己跟进。
- **SPEC 第 7 节的待裁决已积到 A–AP**（C 已于 2026-09-10 拍板，条目划掉保留），
  其余全部**已按暂定方案实现、一处可改**。最需要设计方回话的几条：AO（账号菜单只剩 hover 一条路，Task 33 的代价）、
  A（导航条目四个版本不一致）、E（21 类弹窗的桌面稿全缺）、G / Z（header 到底用哪个）、
  I（`Download Invoice` 做不做）、AC / AD / AE（姓名两栏外推、opt-in 没勾选框、订单三态无区分）。
- ⚠⚠ **Shopify 化已经由主题侧开始了，account 页面在 live 主题上跑着** —— 2026-09-18 的三方对比
  查出的：`templates/page.account.liquid` → `{% layout 'account' %}` → `sections/gb-account.liquid`
  + `snippets/gb-account-{modals,placeholders,flatpickr-cal}.liquid`，路由 `/pages/account`。
  **这几个 liquid 是对方的范围，account 线一个都不碰。**
  ⚠ 店铺开着 storefront 密码保护，`/pages/account` 会 301 到 `gumi.com.au/password`，
  要看渲染得有密码或走主题编辑器预览。
- **2026-09-18 推了第二批，线上与本地已对齐到 `a40`**（`account.css` / `.js` / `.scss` 覆盖，
  `flatpickr.min.js` / `acct-bear-side.webp` / `refer-friends.jpg` / `.webp` 新增，
  `product-placeholder.png` / `acct-bear-side.png` 幂等重推）。回读 **22 ok / 0 red**，
  基线 `baseline-20260918-a40`（639 文件 / 207 assets）—— 见 [PUSH-LOG.md](PUSH-LOG.md)。
  ⚠ **`refer-friends.*` 是需求方 2026-09-18 拍板推的**，商标风险已告知，
  §6 的「上线前必须替换」**仍然有效**，换图后要记得删线上旧的。
  ⚠ **线上仍缺两个模板在引用的 asset**：`flatpickr.min.css`（我们没有这个文件，皮肤手写在
  `account.scss` 里，建议对方删掉那条 `<link>`）与 `pay-visa.svg`（主站线的资源，界线在 §1）。
  ⚠ **主题里没有 `images/` 目录**（Shopify 只认标准顶层目录），本地 `images/x.png`
  推成 `assets/x.png`，模板里写 `{{ 'x.png' | asset_url }}`。
  接主题时 auth 两页要换成 `customers/login` / `customers/register`
  的真实 form；样式必须**单文件**（`assets/` 不接受子目录），图片放与 `assets/` 平级的 `images/`。

---

## 8. 接手第一件事

```bash
grep -c '^- \[x\]' docs/account/PLAN.md      # 进度
python3 tools/acctcheck.py                    # 1 分钟，拿基线
python3 tools/acctmodal.py &                  # 4 分钟，后台
python3 tools/acctview.py                     # 八视图互斥与三处导航一致
```

跑出来的数字对不上第 4 节的基线，先查是不是忘了编译 scss，再查是不是另一个会话
动了共用文件（`find . -newermt "HH:MM"` + `ls -lt ~/.claude/projects/*/*.jsonl`）。

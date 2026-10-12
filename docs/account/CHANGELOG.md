# Gumi Account — 变更记录

## 2026-10-09 — a73：数量确认、取消态Edit discount hover、header去重（已上线）

Edit Product/Add Item在API成功后核对服务端数量，确认后再更新页面和关闭；旧数据最多6次回读，失败时保留弹窗报错。取消态Edit discount code保持蓝色。gb-account移除fresh live重新带入的独立header/announcement，保留layout共享header，正文/后端逐字保持fresh。

上传assets/account.scss、account.css、snippets/gb-account-data.liquid、sections/gb-account.liquid；Liquid源码在liquid/account-qty-discount/。本地另更新account.html、account-login.html、tools/acctqtysave.cjs、acctdiscountstate.cjs、acctheadercount.cjs、acctburger.cjs及三份记录。Sass/脚本语法及164项检查通过，数量API为模拟，未实测真实客户持久化。prework保留4份线上他人更新，prepush零并发变化，完整回读12 ok/0 red，其余638主题文件不变。基线baseline-20261009-a73。

---

## 2026-10-09 — a72：移除Account footer logo hover（已上线）

Account样式覆盖footer logo的hover透明度为1并关闭对应过渡，账户页和登录/注册页生效，保留尺寸、颜色和首页链接；主站共享样式不改。上传assets/account.scss、assets/account.css；本地account.html、account-login.html版本、tools/acctlogo.cjs及三份记录更新。Sass与手机/桌面24项logo检查通过。两次完整pull无并发变化或目标冲突；完整回读8 ok/0 red，其余640主题文件不变，无增删。基线baseline-20261009-a72。

---

## 2026-10-09 — a71：移除顶栏logo hover（已上线）

按用户要求删除.gb-acct-header__logo的hover透明度及对应过渡，保留尺寸、颜色和首页链接。上传assets/account.scss、assets/account.css；本地account.html、account-login.html版本、tools/acctmotion.py、tools/acctlogo.cjs及三份记录更新。Sass与手机/桌面8项检查通过；两次完整pull无并发变化或目标冲突，完整回读8 ok/0 red，其余640主题文件不变，无增删。基线baseline-20261009-a71。

---

## 2026-10-07 — a70：cancelled优惠码hover（已上线）

取消订阅详情的Add a discount code在hover时保持蓝色，其他状态正常变绿，点击仍开弹窗。上传assets/account.scss、assets/account.css；本地account.html、account-login.html版本及三份记录更新。Sass与4项颜色/点击检查通过；全量回读8 ok/0 red，640清单外文件不变。基线baseline-20261007-a70。

---

## 2026-10-07 — a69：恢复Account下拉，保留汉堡（已上线）

补回Account图标及原下拉完整5项；右侧Account+汉堡，菜单互斥，logo尺寸及其他修复保留。核对a68 prepush/verify：637清单外文件及Account正文/他人overview loading未被覆盖；新pull与a68基线一致。

上传sections/gb-header.liquid、assets/account.js、assets/account.scss；CSS产物未变，不上传。本地account.html、account-login.html、tools/acctburger.cjs、tools/acctmobilefixes.cjs、tools/acctmenurestore.py及三份记录。四档144项通过，最终全量回读10 ok/0 red，639清单外文件不变。基线baseline-20261007-a69；未实测真实登录客户/iPhone Safari。

---

## 2026-10-07 — a68：logo尺寸及汉堡菜单（已上线）

gb-acct-header__logo PC123×32px，手机92×24px，兼容img/SVG。账户/购物车图标合并为右侧汉堡，左logo布局保留；复用配置好的主站菜单和main.js手机抽屉交互，PC用原站展开菜单，Account无Shop now。保留他人最新overview loading及Account正文/后端，其他四项a66修复保留。

上传：assets/account.scss、assets/account.css、layout/account.liquid、sections/gb-account.liquid、sections/gb-header.liquid。本地：account.html、account-login.html、tools/acctmobilefixes.cjs、tools/acctburger.cjs、tools/acctburger-build.py、tools/acctburgerlive.cjs及docs/account三份记录。Sass编译与四档102项检查通过；最终完整回读14 ok/0 red，637清单外文件无变化。真实网页HTTP429，未通过线上浏览器入口；未测登录客户/iPhone Safari。基线baseline-20261007-a68。

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

## Task 53 — 手机 Account 主视图原位淡入淡出（20261001-a52，2026-10-01 已推 live）

按用户要求，≤767px 的 gb-acct__view 从右侧滑入/旧视图保持不透明改为新视图原位淡入、旧视图原位淡出；沿用 0.5s 时长及原容器高度收拢。桌面、登录页和 reduced-motion 行为保留。
文件：assets/account.scss、account.css、account.js；account.html、account-login.html 版本标记；tools/acctcover.cjs、acct40check.py（更新旧动画期望，Python 判据未重跑）。
验证：acctcover 47 + acctlayers 21 全通过，JS 语法检查通过；CSS 对 a51 仅本次动画差异。仅推 account.css/account.scss，完整回读 8/0，其他 638 文件无变化。保留线上 data/modals Liquid 后端更新。新基线 baseline-20261001-a52；未测试真实客户登录态。

---

> account 静态页自成一条线：独立 `assets/account.scss` / `.css` / `.js`，独立版本号
> `$build-acct`（**与现站的 `$build` 无关，别混**），判据 `tools/acct*.py`。
> 计划在 [PLAN.md](PLAN.md)，设计决策与待裁决在 [SPEC.md](SPEC.md)。
>
> 约 10 项记一条，只写「改了什么 / 为什么 / 文件清单 / 遗留」。

---

## Task 52 — 兼容线上缺失的视图容器标记（`20260930-a51`，2026-09-30 已推 live）

- 用户反馈 a50 后旧视图仍瞬间隐藏。核对完整线上基线：sections/gb-account.liquid 的容器仅有 class="gb-acct__views"，没有 data-acct-views；静态 account.html 有该属性。导致 view.show 找不到 shell，_leave 提前返回，CSS 隐藏覆盖规则也未命中。此前静态测试未覆盖此差异。
- 最小修复：view.init 在首次切换前从 .gb-acct .gb-acct__views 注册 data-acct-views；无需修改线上后端模板或新增样式。
- acctlayers 直接读取线上基线的容器起始标签并替换静态测试 HTML。旧代码复现 15 通过/6 失败；修复后 21/0，加 acctcover 43 项通过，共 64 项。JS 语法检查、Sass 编译通过，CSS 对 a50 字节一致。
- 文件：assets/account.js；account.scss 及两张静态 HTML 版本号 a51；tools/acctlayers.cjs。已按用户指令部署 account.js 和 account.scss；推前保留线上 gb-account-data.liquid 更新，完整回读 8/0，其余 638 文件无变更，新基线 baseline-20260930-a51。

## Task 51 — Radio、手机完整覆盖与滚动条（`20260930-a50`，2026-09-30 已推 live）

- 地址 radio 选中边框为 #011307，圆点为 #005635，覆盖 Horizon 普通选中及 hover 规则；保持 16px 圆圈和 8.8px 圆点尺寸。
- 修复 a48 遗留：旧视图虽不横移，但受新视图高度截断。手机切换先保持最大高度，由不透明新视图完整覆盖，然后平滑收拢到自然高度。快速切换和 resize 清除临时尺寸；隐藏样式只作用于手机 Account 主视图，以 absolute + opacity:0 + visibility:hidden 保留渲染，inert 阻止焦点进入。桌面及登录页保持原动画。
- 原生滚动条采用 Figma 2284:29195–29197（add-product 本地 JSON）：16px 轨道、可见滑块 8px、#E6E6E6、8px 圆角、透明轨道。应用于 Account 页面、弹窗 body 和下拉列表；未引入 SimpleBar。
- 文件：assets/account.js、account.scss、account.css；account.html、account-login.html 版本更新；新增 tools/acctlayers.cjs，更新 acctcover 判据名称。
- 验证：先复现旧代码 4 通过/9 失败；修复后 acctlayers 20、acctcover 43、acctfeedback 5、acctfeedbackdata 14，共 82 项通过。含长 Overview、收拢期间动画、resize、手机/桌面断点、减少动态效果、真实滚动条引起的日历字段位移检查。Sass 编译及 JS 语法检查通过。
- 用户授权后重新拉取 prepush-20260930-a50（640 文件），三个目标 assets 无线上改动，保留 gb-account-data.liquid 的后端更新。仅推 account 的 CSS/SCSS/JS；完整回读 acctpush 10/0，三个文件逐字节一致，其余 637 文件无变更。新基线 baseline-20260930-a50。

## Task 50 — 七项调整与折扣码控制归属修复（`20260930-a49`，2026-09-30 已推 live）

1. FAQ 分隔线改为 `rgba(#011307, 0.05)`，即 5% 不透明度。
2. 分页数字用 strong、700 字重；本地 HTML 与主题 placeholders 都改。
3. `main.js` 的 selectBox.sync 同步 is-active、aria-selected 和打开状态下的 aria-activedescendant，解决改了选项但高亮仍留在旧项的问题。键盘浏览未提交时仍保留独立 active 游标。
4. 数量由 span 改为 number input，允许直接输入整数；主题数据层改为 value 读写，动态商品卡也同步改。输入同步 CTA、减号禁用与零数量文案；小数/空值不能提交，change 时规范为符合最小值的整数。按钮步进仍由主题脚本独占，不恢复 acctQty。
5. 折扣码问题的根因：acctDiscount 未经 API 验证就设置 applied；Apply 被 data-acct-modal 当作直接切换；modal._hide 的旧计时器会隐藏已重开的同一弹窗。去掉前两条假成功路径，并取消旧计时器、避免重开已打开的面板。主题补齐 discount-applied 的 API handler，共用输入 hook；无效响应保留弹窗并提示错误，有效响应后重新获取数据再关闭。
6. 删除本地 JS 的 applied 判定和 markup 里的 CEO90 成功占位；chip 默认隐藏、无预填文案，只由主题数据层根据真实 contract.discountCodes 等返回字段填充及显示。移除 chip 的动作仍交主题 API。
7. Account 内覆盖 Horizon 的已选 radio hover ::after，颜色 #005635，作用仅 account.css 加载的页面。

验证：修改前 acctfeedback 五条失败；修改后五条通过。acctfeedbackdata 14 项通过（模拟 API 成功/拒绝、实际主题函数的数量输入与步进、radio 叠加 Horizon CSS），acctcover 43 项回归通过。Sass 1.77.8 编译、main/account JS 与模板 JS（Liquid 数据段替换为测试空数据）的语法检查通过；CSS 与 a48 比对仅上述样式规则。没有调用真实账户的修改接口，没有实测客户登录态。Python Playwright 缺失，旧 Python 判据更新期望但未运行。

文件：`assets/account.scss` / `.css` / `.js`、`assets/main.js`、`account.html` / `account-login.html`；`liquid/account-a49/snippets/gb-account-{data,modals,placeholders}.liquid`（完整线上副本的定点改动）、`liquid/account-a49/a49.patch` / README；`tools/acctfeedback.cjs` / `acctfeedbackdata.cjs`、`tools/r26check.py` / `acctmodal.py` / `acctcheck.py`。

已推：四个 assets 与三个 snippets 已于 2026-09-30 部署。推前与 a48 比对无线上差异，回读 acctpush 18/0，基线 baseline-20260930-a49；静态 HTML 未推主题。主站 main.js 的改动仅 selectBox.sync；Account 数量及折扣码动作归主题数据脚本。

---
## Task 49 — 手机视图改为覆盖式切换（`20260930-a48`，2026-09-30 已推 live）

手机端旧视图保持原位与不透明，新视图保留从右侧整宽滑入并在上层覆盖旧视图；动画结束后隐藏旧视图。按需求撤回 Task 40 手机端旧视图向左退场的效果，桌面及登录页的切换不变。
进入态背景复用 account 外壳的浅绿顶部色带与底色，色带高度为 176 − 8 = 168px；旧视图限制在新视图容器高度内，避免短视图下露出旧内容。

验证：先用浏览器复现 Overview 中途向左位移，再修改；`tools/acctcover.cjs` 43 项通过，覆盖 390/767/768/1440、静止旧视图、覆盖层级、背景、横向溢出、快速返回、最终互斥与 reduced-motion。Sass 1.77.8 编译完成，CSS 对 a47 基线的差异仅本次切换规则。
既有 `acct40check.py` 手机退场动画期望改为 `gb-acct-view-hold`；本机缺 Python Playwright，该 Python 判据未重跑。

文件：`assets/account.scss` / `account.css`、`account.html` / `account-login.html`（版本号）、`tools/acctcover.cjs`、`tools/acct40check.py`。

---
## Task 48 — 展开字段日历时弹窗内容横移（a46 → `20260929-a47`，2026-09-30 已推 live）

**改了什么**：`modal._fit()` 末尾加滚动条补偿。body 出现经典滚动条时，把右侧 padding 设为 `左 padding − 滚动条宽`（内联，每次 `_fit` 先清掉再量）。
**为什么**：body 不溢出时 `_fit` 把它设成 `overflow-y: visible`。点 `.gb-acct-field__control` 后 `flatpickr-calendar inline` 展开，内容变高，ResizeObserver 把 body 切回 `auto`，桌面约 15px 的滚动条出现，内容区跟着变窄，输入框右边缘实测左移 15px（956 → 941）。
动手前拉了线上快照 `snap-20260929-live`：线上 `account.js` 与本地逐字节相同。与 a46 基线相比只有 `gb-account-data.liquid` 被对方改过（subscription name / attributes `key`），与本问题无关。

⚠ **不要报成 bug**：
1. **一打开就要滚动的长面板（shipping-form / add-product 等），右侧留白从 24 变成 `24 − 滚动条宽`**：这是同一条补偿的结果，内容宽度因此与不滚动时一致。如果要恢复旧观感，只对带 `.gb-acct-cal--field` 的面板生效即可。
2. 手机端和 overlay 滚动条的滚动条宽度为 0，补偿不生效，这是正常的。

**判据**：`tools/calshift.py`（1440×600 / 1440×700 两档，要求真实滚动条，先断言 body 确实出现了滚动条）**6 ok / 0 red**。`--strip` 反向跑转红 2 条。线上可用 `--url … --password 1234` 复跑。
回归：`acct44check` 104/0，`acct43check` 17/0，`acctview` 26/0，`acct38check` 80/0。`acctmodal` 是 1301 ok / 2 red / 1 aborted，两条红都是 `cancel-holiday`「fewer than two selectable days」，换回 a46 的 JS 结果一样，所以不是本轮引入的。原因是判据依赖日期：9-29 当天，日历打开的那个月只剩 30 号一天可选。**顺带发现、未修。**

**文件**：`assets/account.js` · `assets/account.scss`（只动了 `$build-acct`，`account.css` 字节不变）· `account.html` / `account-login.html`（`?v=`）· `tools/calshift.py`（新）

---

## Task 47 — 数量步进器的点击交给主题 JS（a45 → `20260928-a46`，已推 live）

**改了什么**：删掉 `account.js` 里整个 `acctQty` 模块，包括面板上的委托 click、`modal.init` 里的 bind、`window.gumiAcct.qty` 的导出。
**为什么**：线上 `gb-account-data.liquid` 的 `attachQtyControls()` 直接在每个 `+` / `−` 上绑了 click。我们的委托又绑了一次，线上点一下会 ±2。
减号禁用、CTA 文案（`data-acct-label-zero`）、Save 门控，对方的 `syncEditCta` / `syncAddCta` 都已接管。

⚠ **不要报成 bug**：
1. **静态页上点 `+` / `−` 没有反应**：这是有意的，步进由主题 JS 负责。
2. **「最后一个商品减到 0 就改开 `product-locked` 弹窗」随模块一起消失了**。对方的 JS 目前不做这个路由，而是走 `qty === 0 → remove line`。需要保留的话，应由后台实现。
3. `acctForm._snapshot` 仍会读 `[data-acct-qty-value]`：只读，用来判断 Save 该不该亮。

**判据**：`acctmodal` / `r26check` 里测「步进行为」的段落改成反向断言（点击后数量不变）；删掉 `acct43check` 的 `run_dedupe`（它只测步进器去重）。
反向：换回 a45 的 JS 后，`r26check` 转红（`1 → 2`）。

**文件**：`assets/account.js` · `assets/account.scss`（只动了 `$build-acct`）· `account.html` / `account-login.html`（`?v=`）· `tools/acctmodal.py` · `tools/r26check.py` · `tools/acct43check.py`

---

## Task 46 — 按钮 API 调用中的 loading 态（a44 → `20260928-a45`，已推 live）

**改了什么**：新增全局规则 `button.is-loading`：文字和子图标隐去，原位显示一个转圈，按钮尺寸不变，并禁用点击。
圈的颜色取按钮自己的 `currentColor`；尺寸走 `--gb-spinner-size`（默认 `1.25em`），组件要单独调就覆盖这个变量。

**为什么**：对方的 `snippets/gb-account-data.liquid`（线上 2026-09-28 版，1767 行）在 API 调用期间会给以下按钮加 `is-loading`：
弹窗的触发按钮、折扣 chip 的 ×、Download Invoice。此前这个类没有任何样式。

⚠ **不要报成 bug**：
1. **选择器限定为 `button`，不是裸 `.is-loading`**：线上 `.gb-cart-item`（div 行）也用这个类挂它自己的遮罩，而 account layout 里渲染着购物车抽屉，裸类会把整行文字藏掉。
2. **文字用 `-webkit-text-fill-color` 隐藏，不用 `color: transparent`**：转圈要靠 `currentColor` 取到按钮原本的文字色，一刀切会让圈也跟着透明。
3. **放在 `account.scss`，不放 `customstyle.scss`**：PDP 的 `.gb-product__cta.is-loading` 在 `sections/gb-product.liquid` 里有自己的内联样式，而 account.css 不在 PDP 的 layout 里加载，两者互不干扰。
4. **reduced-motion 下圈是静止的**：customstyle 的全局规则把 `animation-iteration-count` 压成 1。

**判据**：`tools/acctloading.py`，8 类按钮加 1 条负向（div），结果 57 ok / 0 red；`--strip` 反向跑 36 红。
编译产物对线上 a44 的 diff 只多出本条规则。

**文件**：`assets/account.scss` · `assets/account.css` · `account.html` / `account-login.html`（`?v=` → a45）· `tools/acctloading.py`（新）

**遗留**：无。推送记录见 PUSH-LOG a45。

---

## Task 45 — 九处间距微调（a43 → `20260918-a44`）

需求方 2026-09-18，分两条给到：

> 1. `.gb-acct-product__now` margin-left 2px
> 2. `.gb-acct-sub__body` 手机端 row-gap: 24px; `.gb-acct-row` margin-top: -1px; 手机端
>    `.gb-acct-schedule__days` padding: 0; margin: 0 -3px;
> 3. `.gb-acct-reasons` row-gap: 12.5px
> 4. `.gb-acct-cal .flatpickr-calendar` padding: 20px 22px
>
> `.gb-acct-item__main` padding-right: 12px; `.gb-acct-item__names` row-gap: 0px;
> `.gb-acct-item__text` row-gap: 8px; `gb-acct-rule` margin-t -1px

九条全部是**客户设定值**，不是板上的数 —— 原处的板号注释都还在，但已经不能再当依据，
所以每条都在源码里标了 `client-set`，数值出处以本条与 `acct45check` 为准。

### 改了什么

| 选择器 | 旧 | 新 | 断点 |
|---|---|---|---|
| `.gb-acct-product__now` | — | `margin-left: 2px` | 全宽 |
| `.gb-acct-sub__body` | `row-gap: 23.5px` | 手机 `24px`（桌面仍 23.5） | `narrow` |
| `.gb-acct-row` | — | `margin-top: -1px` | 全宽 |
| `.gb-acct-schedule__days` | `padding: 0 4px` | 手机 `padding: 0; margin: 0 -3px` | `narrow` |
| `.gb-acct-reasons` | `row-gap: 12px` | `12.5px` | 全宽 |
| `.gb-acct-cal .flatpickr-calendar` | `padding: 20px 24px` | `20px 22px` | 全宽 |
| `.gb-acct-item__main` | — | `padding-right: 12px` | 全宽 |
| `.gb-acct-item__text` | `row-gap: 6px` | `8px` | 全宽 |
| `.gb-acct-item__names` | `row-gap: 2px` | `0` | 全宽 |
| `.gb-acct-rule` | — | `margin-top: -1px` | 全宽 |

### 四条不只是「一个数」

⚠ **`.gb-acct-row` 的 −1px 是全宽，而且会把第一行也抬起 1px**。第 2 组里
`.gb-acct-sub__body` 与 `.gb-acct-schedule__days` 都写了「手机端」，夹在中间的
`.gb-acct-row` 没写 —— 按字面当全宽做了。行是 `.gb-acct-sub__body` 的直接子元素，
负 margin 对**第一行**同样生效，于是首行离卡片 padding-top 少了 1px。
两个后果都钉进了判据（`gap between rows = row-gap − 1`、`first row sits 1px above
the body's content box`）。**要改成只手机端，包一层 `@include narrow` 即可，一行可回退。**

⚠ **手机 `row-gap: 24` 连带动了续订日程块** —— 与 Task 34 同一处耦合：`account.html:427`
是 `<div class="gb-acct-sub__body gb-acct-schedule">`，`.gb-acct-schedule` **自己一条规则都没有**。
本轮是「把手机端调回板上的 24」，两处一起走正合适，判据两处都断言了。
桌面的 23.5 是 Task 34 的客户值，原样保留。

⚠ **`.gb-acct-item__main` 的 12px 是从名字列扣的，不是从行里扣的**。`.gb-acct-item` 是
`space-between`，手机上两列**本来就已经顶到 `column-gap: 2`**（实测 main 右边到价格左边正好 2），
没有空隙可占，于是 padding 压在了文字列上：文字框 389.8 → 187.8，窄了 2px。
名字「Superfood Greens Gummies」仍是一行、还剩 2px 余量 —— **判据钉住了「名字仍是一行」**，
再长一点的品名会在手机上开始折行。

⚠ **`.gb-acct-schedule__days` 的 `margin: 0 -3px` 让日程条在手机上探出卡片 padding 3px**。
四个日期块因此各宽一点（`padding: 0` 又还回来 8px），不是溢出卡片本身（body padding 20 > 3）。

### 文件清单

| 文件 | 改动 |
|---|---|
| `assets/account.scss` | 九处数值（六段就地改：product / sub body / detail row / schedule days / reasons / cal，加 item 四处）；`$build-acct` → `20260918-a44` |
| `assets/account.css` | 编译产物（双写，`npx sass@1.77.8`） |
| `account.html` / `account-login.html` | 只有 `?v=` 跟版本走（17 + 2 = 19 处） |
| `tools/acct45check.py` | 新增，57 条 |
| `tools/acct38check.py` | 日历 padding 期望 `20px 24px` → `20px 22px`（同一处改动，非放宽） |
| `tools/acctmodal.py` | `listGap` 期望 `12px` → `12.5px`、holiday 日历 `contentPadX` `24px` → `22px`（同上）⚠ 日历 padding 共三处判据在钉 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acct45check.py` | **57 ok / 0 red** |
| 其中反向锚点（1440 保持 23.5 / `0 4px` / 无 strip margin） | 9 条，丢了 `@include narrow` 就转红 |
| 其中像素断言（行距、首行抬升、strip 探出 3、价格间距 4、名字仍一行、rule 上 23 下 24） | 14 条 |

### 回归

**30 个判据 + rwd ×4 全绿**：`acct45` **57** / `acctcheck` 848 / `acctmodal` **1321 ok / 0 red / 1 aborted**
（那条 aborted 是 390 遮罩滚动条，一直是预期项）/ `acct44` 104 / `acct43` 19 / `acct42` 21 / `acct41` 16 /
`acct40` 68 / `acct38` 80 / `acct34` 29 / `acct33` 52 / `acct32` 66 / `acct31` 437 / `acctview` 26 /
`accthover` 41 / `acctmotion` 10 / `acctvars` 54 / `iconclip` 51 / `assetpath` GREEN /
`r25`–`r30` 40/42/29/32/44/53 / `rwd.py` 四条全绿。

⚠ **`acctmodal` 第一遍 1319 / 2 红** —— holiday 日历的 `contentPadX` 还钉着 24。
**日历的 side padding 有三处判据在钉**（`acct38check` / `acctmodal` / `acct45check`），
改一个值要找齐三处，第一遍只改了两处。改完回到 **1321 / 0 / 1**，与上一轮逐字相同。

✅ `rwd.py` 四条全绿也顺便证明了 `item__main` 那 12px 没在任何一档挤出横向溢出。

### 遗留

- **`.gb-acct-item__names` 的 `row-gap: 0`** 让品名与 Flavour 两行的行盒直接相接（墨迹间距只剩
  两侧 leading）。板上是 2，这是客户值 —— 若日后按板校对，这里会被当成 bug 修掉，已登记进
  HANDOFF 的「不要报成 bug」。
- **`.gb-acct-rule` 的 −1px 只抬它自己**（上 23 / 下 24，不对称），同样是客户值。
- 手机上 `.gb-acct-item` 两列已无余量（column-gap 2 顶死），再加任何右侧内边距都会开始折品名。

---

## Task 44 — 弹窗里的下拉：选项一多就被面板裁掉且够不到（a42 → `20260918-a43`）

需求方 2026-09-18（补充）：

> 补充 `.gb-select.is-open .gb-select__list` 如果 option 选项过多会被截断并且无法滚动

### 复现与量化

以 `edit-frequency`（**矮面板**，需求方点名的那个）为例，逐级加 option：

| 选项数 | 列表高 | 溢出面板底边 | 能滚吗 |
|---|---|---|---|
| 3 | 130 | −10（**刚好不超**） | 不需要 |
| **4** | 170 | **+34** | **不能** |
| **5** | 210 | **+70** | **不能** |
| 6 / 8 / 12 | 224 | +88 | 能滚，但可见窗口只剩 136 |

⚠ **最坏的是 4–5 项，不是很多项**：那里内容（168 / 208）还没到 `max-height: 224px`，
所以列表**自己没有滚动条**，被裁掉的 34–70px **用任何方式都到不了**。
项数更多反而"没那么坏"—— 列表可滚，只是窗口矮。

三个原因叠起来：

1. `customstyle.scss` 的 `.gb-select__list` 用**固定** `max-height: 224px`，不知道面板还剩多少空间
2. `.gb-acct-modal__panel` 是 `overflow-y: clip`，裁掉溢出部分 —— ⚠ **这条是承重的**，
   Task 25/26 验过改 `hidden` 会让面板变成滚动容器、折线以下的字段滚不到
3. ⚠⚠ **`main.js` 的 `clipBottom()`（1892 行）把 `overflow: clip` 当成「不裁切」跳过了**：
   `if (o !== "visible" && o !== "clip")`。函数注释写的是「最近一个**真的会裁切**的祖先」，
   而 `clip` 的唯一职责就是裁切。于是 `wouldOverflow()` 拿视口底边去比，判定「没溢出」，
   `is-up` 永远不加 —— 实测 `opensUp` 全程 false。

### 修法：account 作用域内接管定位，不动共享文件

新模块 `acctSelectFit`（`assets/account.js`），只 patch `selectBox.show` / `.close` 两个方法：

- **`show` 之后自己决定方向并限高**：算出弹窗面板内上下两侧的可用空间，
  ⚠ **选大的一侧**，再把列表限到那一侧的高度。
  selectBox 只看一侧就翻，矮面板里两侧都不够时会翻到更小的那边 ——
  第一版就是这样：列表被压到 **96–98**（约 2 行），而向下其实有 132。
- **`close` 时清掉行内 `max-height`**，否则下一次打开就是矮的。
- ⚠ **没有 patch `clipBottom`**。第一版 patch 了它（把 `clip` 算作裁切），但既然 `_fit`
  自己决定方向，改共享方法的语义就是多余的改动面。`main.js` 那一行的 bug **仍在**，
  影响主站线所有 `overflow: clip` 容器里的下拉，已写进 PUSH-LOG 给对方。
- ⚠ **模块以「共享组件还暴露这两个方法」为前提**，不满足就 no-op ——
  判据第一条钉 `window.gumiAcct.selectFit` 在，no-op 不能静默通过。

修后实测（两个面板 × 两个宽度 × 3/4/5/8/30 项）**全部不溢出、内容全部可达**：

| | 结果 |
|---|---|
| `edit-frequency`（矮） | 限高 132（1440）/ 128（390），可滚 |
| `shipping-form`（高） | 上翻后空间够，**不限高**，保持 224 全高可滚 |

### 判据

`tools/acct44check.py`。⚠ **option 从 init script 注入**，在任何页面脚本之前 ——
这样 `selectBox` 是从加长后的 `<select>` **正常构建**的。
第一版探针直接改写 `.gb-select__list` 的 innerHTML，量的是组件根本没生成过的 DOM，
读数是 `listH=0` 的假象。

断言不是「它能滚」而是**「两边都没被裁 **且** 装不下的部分滚得到」**，
并配 `boxOverflowY == 'clip'` 的锚点（面板真的在裁）、`opts == n`（注入真的生效）、
关闭后行内 clamp 被清掉。

### ⚠ 顺带修好一个 Task 40 漏掉的判据

`r29check` 在本轮回归里 **42 ok / 2 red**（基线 44/0），两条都是
`want ['referral'] got ['overview','referral']`。原因是 `wait_for_timeout(500)`
**正好等于 Task 40 的退出动画时长**，读到旧视图还在流里。

⚠ **Task 40 那轮的回归清单里有 r25/r26/r27，没有 r28/r29/r30** —— 所以漏检了。
本轮把切视图后的两处 500 改成 **750**（与 `acctview` 700 / `acctcheck` 750 同一原因），
**断言一条没放宽**，回到 44/0。
⚠ 其余判据里也有 `wait_for_timeout(500)`（`r28` / `r30` / `acct33` / `acct34` / `acct37`），
但它们等的是面板打开不是切视图，当前全绿，**没动**。

回归全绿（**22 个判据 + rwd ×4，一条红都没有**）：`acctcheck` 848 · `acctmodal` 1321/0/1 aborted ·
`acctview` 26 · `acctbp` 2356 · `accthover` 41 · `acctmotion` 10 · `acctvars` 54 · `iconclip` 51 ·
`assetpath` GREEN · `acct31` 437 · `acct32` 66 · `acct33` 52 · `acct38` 80 · `acct40` 68 ·
`acct41` 16 · `acct42` 21 · `acct43` 19 · `acct44` 104 · `r25`–`r30` 40/42/29/32/**44**/53 ·
`rwd.py` ×4 全绿。计数全部持平 —— 两轮只改 JS。

### 文件清单

- `assets/account.js` — 新增 `acctSelectFit`，接入 modules 与 `window.gumiAcct.selectFit`
- `assets/account.scss` — `$build-acct` → `20260918-a43`
- `assets/account.css` — 重编译；⚠ **与线上逐字节相同**（两轮都只改 JS），推送清单里没有它
- `account.html` / `account-login.html` — 19 处 `?v=` 同步 a43
- `tools/acct44check.py` — 新增
- `tools/r29check.py` — 两处采样时机 500 → 750

### 推送

2026-09-18 与 Task 43 一起推上 live，**只两个文件**（`account.js` / `account.scss`）——
`account.css` 与线上逐字节相同。三方对比零差异，回读 8 ok / 0 red，
基线 `baseline-20260918-a43`。详见 [PUSH-LOG.md](PUSH-LOG.md)。

### 顺带发现 / 未修

- ⚠ **`main.js:1892` 的 `clipBottom()` 仍把 `clip` 当作不裁切** —— 主站线的文件，没动。
  建议把条件改成 `if (o !== "visible")`。影响面：任何 `overflow: clip` 容器里的共享下拉。
- ⚠ **`MIN: 96` 是自定值**（约两行）。面板矮到连 96 都放不下时列表会溢出，
  目前没有这样的面板；真要处理得让下拉改成全屏抽屉，属交互决策，等拍板。

---

## Task 43 — 线上所有 Save 都点不动：运行时标记被抄进了模板（a41 → `20260918-a42`）

需求方 2026-09-18：

> 选中日期之后 `gb-acct-modal__save` 仍无法点击保存

### 根因不在日历，在一个被抄进 liquid 的 JS 内部标记

`acctForm.watch()` 装完门控后会给面板打一个去重标记。对方的模板是**从渲染后的 DOM 抄出来的**，
于是这个标记进了源码：

| 文件 | 处数 |
|---|---|
| `snippets/gb-account-modals.liquid` | **8** 个面板：`edit-name` / `edit-date` / `edit-frequency` / `shipping-current` / `shipping-form` / `edit-product` / `add-product` / `product-locked` |
| `sections/gb-account.liquid:134` | **1** 处：My Details 的页内表单 |

守卫第一句就是它：

```js
if (!save || !fields.length || panel.getAttribute('data-acct-watched')) return;
```

于是每次加载都读到自己上一世的标记、**直接 return，门控从未安装**，
`save` 保持 HTML 里的 `disabled` —— 选什么日期都不会解锁。**九处全中**，
不只是 `edit-date`：八个弹窗 + My Details 的 Save 在线上全都是死的。

⚠ **与 Task 42 无关**。那一轮修的是双日历，这条从 a29 上主题的第一天就在。

### 修法：运行时状态一律不进 DOM

三个同族模块是完全一样的写法，一起改 —— 对方下次再抄渲染结果就会再中一次，
症状会变成「数量加减不动」「折扣码不响应」「手风琴点不开」：

| 模块 | 原来 | 现在 |
|---|---|---|
| `acctForm.watch` | `data-acct-watched` | `panel._acctWatched` |
| `acctDiscount.bind` | `data-acct-discount-bound` | `panel._acctDiscountBound` |
| `acctQty.bind` | `data-acct-qty-bound` | `root._acctQtyBound` |
| `acctFaq.bind` | `data-acct-bound` | `root._acctBound` |

元素属性（property）不会被 `cloneNode`、`outerHTML` 或「抄渲染结果」带走，去重语义一点没变。
四个标记此前**只有 `account.js` 自己读写**（判据、页面、模板都没引用），所以改名零影响面。

⚠ **模板里那 9 处 `data-acct-watched="1"` 现在是无害的死属性**，不必等对方删就已恢复；
建议他们顺手清掉，已进 PUSH-LOG。

### 判据

`tools/acct43check.py` **19 ok / 0 red**。四段，每段都把标记放到**模块运行之前**，
再断言功能照常：

- `edit-date`：在 `modal.open()` **之前**给面板打上属性（`watch` 正是 open 时调的）——
  这是线上的真实时序。三条：Save 起手 disabled（锚点）→ 改日期解锁 → 改回原值**重新** disabled
  （证明门控是按值比较，不是一次性开关）。
- My Details 表单与手风琴由 `init()` 装，没法在它之前打属性，改用 **`cloneNode(true)`** ——
  ⚠ **它复制属性、不复制 property**，正好是模板的形状。
  ⚠ **不能用「重置 property 再手动 bind」** —— 那会装第二套监听器，
  本轮第一版判据就是这么写的，`+1` 读成了 `+2`。
- 去重仍然有效：连着 `qty.bind()` 两次再点一下 `+`，断言只 `+1`。
- 手风琴那条断言的是**「守卫放行了」**（`_acctBound` 为 true）而不是「行数展开」——
  clone 在外壳之外，`_set()` 的 `aria-expanded` 由 `slideTo` 的回调翻转，需要真实的高度过渡才会触发。
  修复前 `bind()` 在属性上 return、根本不会设 property，所以这条照样会红。
  ⚠ 配了一条真实手风琴的锚点，**必须点第 2 行** —— 第 1 行板上就是展开的（`is-open`），
  点它是**收起**，`aria-expanded` 会读 0。

活性自检：把 `watched` 与 `bound` 两处改回 `setAttribute` → **5 红**
（`no data-acct-watched in the DOM` 读到 9、details 表单的 Save 不解锁、手风琴守卫没放行……），
还原后 19/0。

回归见 Task 44 那一节（两轮一起跑的，22 个判据全 0 red）。
⚠ 本轮回归第一次跑时 `r29check` **42/2 红**，是 Task 40 漏检的采样时机，已在 Task 44 一节说明。

### 文件清单

- `assets/account.js` — 四个去重标记从 DOM 属性改为元素 property
- `assets/account.scss` — `$build-acct` → `20260918-a42`
- `assets/account.css` — 重编译（⚠ 产物**零差异**，本轮只改 JS）
- `account.html` / `account-login.html` — 19 处 `?v=` 同步 a42
- `tools/acct43check.py` — 新增

### 顺带发现 / 未修

- ⚠ **模板与本地的 hook 计数对不上**：`data-acct-field` 线上 24 / 本地 26。
  `gb-account-modals.liquid` 里有 2 个 `{% for %}`，静态计数本来就不可比，
  但**如果真少了 hook，那些字段改了 Save 也不会解锁**。属对方还原度，建议他们自查。
- ⚠ **`.gb-select__list` 的截断/滚动问题本地复现不出来**，见下文与 HANDOFF §7。

---

## Task 42 — 线上的双日历 + 不可选日期的光标（a40 → `20260918-a41`）

需求方 2026-09-18，三条（对话里给的，`account修改任务文档.txt` 仍停在 09-16）：

> 1. live 上 `.gb-acct-nav__link:before` 这个没改成占位的灰色 icon
> 2. Edit renewal date 内部存在 flatpickr-calendar 的两个日历是什么原因
> 3. 修复 无法选择的日期也需加上 cursor 鼠标进度的样子

### 第 1 条不是 bug，是线上版本旧

圆点是 **Task 34** 加的（`a35`），而 live 主题一直停在 **`a29`**（Task 32 那一版）：

```
a29  grep 'gb-acct-nav__link::before' → 0
a40  grep 'gb-acct-nav__link::before' → 1
```

2026-09-18 推完 a40 后线上已带上（`display:flex` + 16.67 圆 / `#d9d9d9` / 20 的槽 / 文字左沿 48）。
核验一行：`getComputedStyle(document.querySelector('.gb-acct-nav__link'),'::before').backgroundColor`
应读 `rgb(217, 217, 217)`；读到 0px 宽就是浏览器/CDN 还在用旧 CSS（Shopify 实测滞后过 20 分钟）。
**没有改任何代码。**

### 第 2 条：模板预渲染一份 + 我们 append 一份

对方的 `snippets/gb-account-flatpickr-cal.liquid` 在 `.gb-acct-cal[data-acct-cal]` 里
预渲染了一份静态 `.flatpickr-calendar`，snippet 注释写的是
「flatpickr will re-render this container once initialised」—— **这个假设不成立**。
`account.js` 的 `_arm` 用的是 `appendTo: root`，而 **flatpickr 只追加、从不清空容器、也不接管已有 DOM**。
三处全中（`gb-account-modals.liquid` 第 45 / 488 / 536 行：`edit-date` / `cancel-holiday` / `restart`）。

修在**我方**、所有日历都过的那一处（`_arm` 开头，三个实例一次修完）：

```js
var shell = root.querySelector('.flatpickr-calendar');
if (shell) shell.remove();
```

⚠ **静态页没有这个壳，所以本地三轮日历工作（Task 31/32/38）都不可能发现** ——
判据因此自己搭出线上的形状再驱动 `_arm`。

⚠ **没改对方的 liquid**（HANDOFF §1 的界线）。两条建议已进 PUSH-LOG 给对方：
`layout/account.liquid:14` 那条 `flatpickr.min.css` 的 `<link>` 建议删（我们没有这个 asset，
皮肤手写在 `account.scss` 里），而**缺了 vendor CSS，预渲染的壳本来就是无样式裸 DOM**，
pre-paint 的价值不成立；壳里还硬编码着 `September 2026`。

### 第 3 条：去掉 `pointer-events: none` 才能有光标

`account.scss` 原来那条规则自己的注释就说了这件事：
「pointer-events 和 cursor 互斥，所以这些日期没有 not-allowed 光标」（[[cursor-not-allowed-vs-pointer-events]]）。
所以本轮把一条规则拆成两条：

| 选择器 | 处理 |
|---|---|
| `.flatpickr-day.flatpickr-disabled` | 去掉 `pointer-events: none`，加 **`cursor: not-allowed`** |
| `.flatpickr-day.prevMonthDay` / `.nextMonthDay` | **保留 `pointer-events: none`** —— ⚠ 它是承重的，点相邻月的补白格会让 flatpickr **跳一个月** |

⚠ **取值按 `not-allowed`**（需求原话是「鼠标进度的样子」）。理由：全站禁用态一律 `not-allowed`
（分页箭头的 `:disabled`、侧栏 `[aria-disabled]`、Task 26 的「禁用光标」那条），
这里跟着走才一致。**要 `progress`（转圈）改一个值即可。**

⚠ **hover 不会亮**：`.flatpickr-day.flatpickr-disabled` 的 `background: none` 是 0-2-0、
排在 `@include hover` 的 0-2-0 之后，顺序胜出。**所以 hover 规则一行没动** ——
若改成 `&:not(.flatpickr-disabled) { @include hover … }`，特异性会升到 0-3-0 并**压过 `.selected`**，
选中的那天 hover 时会从绿变 lime。

⚠ **去掉 `pointer-events` 之后「点了会不会选中」只能靠行为验** ——
flatpickr 自己在 `onDayClick` 里拒绝 disabled 的天。判据用 `force=True` 真点一下，
断言字段值不变、`.selected` 为 0。**只验声明是不够的。**

⚠ **只有「打开那个月」的禁用日拿得到光标** —— `prevMonthDay`/`nextMonthDay` 同时也带
`.flatpickr-disabled`，而它们自己那条规则在后面。判据的选择器因此是
`.flatpickr-disabled:not(.prevMonthDay):not(.nextMonthDay)`。

### 判据

`tools/acct42check.py` **21 ok / 0 red / 0 skipped**（两个日历实例各跑一遍）。

- **壳那一段的锚点是「探针真的注入了壳」** —— 先读 `{cals:1, shell:1}`，再 `_arm`，
  再读 `{shell:0, cals:1}`。少了前一次读，断言会在**静态页本来的形状**上读绿。
- **光标那三条跑在探针自己标记的日子上**，与「这个月有没有过期日」无关 ——
  否则每月最后一天跑判据时视图开在下个月，一条禁用日都没有，三条断言会在空集上恒真。
- **「禁用日数量 == 今天的日期数」是算出来的**，不写死日期（minDate 是明天，所以 1..今天
  全部禁用，永远至少 1 个）。视图开在下个月时这条转 SKIP 并打印原因。
- `restart` 藏在 cancelled 详情态后面，照 `acct38check` 的办法用 `modal.open()` 直接开。

活性自检：**两处突变都当场报红**。去掉 JS 守卫 → `shell is gone` 与 `exactly one calendar`
双红（2 个日历）；把 `cursor` 换回 `pointer-events: none` → 四红，
⚠ 其中 cursor 读回的是 **`pointer`** 而不是空 —— `.flatpickr-day` 的 `cursor: pointer` 还在，
`pointer-events: none` 只是让它到不了指针。**读 computed cursor 判不出「光标能不能用」，
判得出的是「值对不对」，所以 `pointer-events` 那条断言必须同时在。**

### 文件清单

- `assets/account.js` — `acctCal._arm` 开头清掉预渲染壳
- `assets/account.scss` — 日历禁用态拆成两条规则；`$build-acct` → `20260918-a41`
- `assets/account.css` — 重编译（产物 diff 正好等于那一处拆分）
- `account.html` / `account-login.html` — 19 处 `?v=` 同步 a41
- `tools/acct42check.py` — 新增

### 顺带发现 / 未修

- ⚠ **`nextMonthDay` 里晚于 minDate 的那些日子其实是可选的**，但被 `pointer-events: none`
  一起挡住了（本轮保留，因为去掉会让点击跳月）。要让它们可点，得改成
  「允许点击 + 让 flatpickr 正常切月」，属于交互决策，等拍板。
- ⚠ **线上仍缺两个模板在引用的 asset**：`flatpickr.min.css`（我方没有这个文件）、
  `pay-visa.svg`（主站线的）。见 PUSH-LOG 2026-09-18 那条。

---

## Task 41 — 手机端各视图底部间距拉齐（a39 → `20260917-a40`）

需求方 2026-09-18，一条（**只在对话里给，`account修改任务文档.txt` 仍停在 09-16 07:06 的 Task 34 那四条**）：

> 1. `gb-acct__view` 手机端不同模块的底部间距不一样 略微调整一下

### 改了什么

先量后改。**盒模型上九个视图本来就一致** —— `.gb-acct__inner` 在 ≤767 的
`padding: 8px 0 48px` 是唯一来源，九个视图的底边到 `.gb-footer-wrap` 全是 48.0。
差的是**墨迹**（[[ink-gap-not-box-gap]]），像素法量「波浪上方第一行非底色像素」才看得见：

| 视图 | 墨迹留白 | 结尾元素 |
|---|---|---|
| overview / subscriptions / order / password / help / referral | **48** | 卡片边框或实心按钮，盒边就是墨迹边 |
| detail / details | 51 | 纯文字收尾，多出的 3 是行盒半行距 |
| **orders** | **62** | `.gb-acct-pager` |

`orders` 那 14 的来源是分页条自己的构造：45 的壳（1 border + 44）里居中一个 36 的按钮（下留 4），
按钮里是 20 的箭头（再留 8），箭头的 `d` 在 20 的 viewBox 里还有 2 的余量。**一条规则改掉**：

```scss
@include narrow {
  .gb-acct-stack > .gb-acct-pager:last-child { margin-bottom: -14px; }
}
```

写在 `.gb-acct-pager__label` 之后、同族规则原位，不堆到文件末尾。

⚠ **没有改 `.gb-acct-pager` 的 45** —— 那是板上 `layoutSizingVertical=FIXED` 锁的高度，
`acctcheck` 与 `acct41check` 两边都钉着；把它压矮会同时改掉分页条在列表里的观感。
⚠ **`:last-child` 是刻意的**：将来 orders 底部若再加一块，补偿自动失效，不需要有人记得删。

⚠ **detail / details 的 51 有意没动**。那 3 是段落行盒的半行距，全站文字收尾处处如此，
要抹平就得按字体度量反向补偿 —— 脆且会变成两条只为这两个视图存在的特例。
肉眼在 390 上分不出 48 与 51，62 才是看得出来的那一个。

⚠ **桌面没动**。需求只说手机端；1440 下这 14 落在 144 的留白里，占比看不出来。
判据反向钉了「1440 下 pager 的 `margin-bottom` 仍是 0px」。

### 判据

`tools/acct41check.py` **16 ok / 0 red**。

- **不能用 computed style 验** —— 九个视图的盒间距**本来就都是 48**，读 `padding-bottom`
  在改之前也全绿。判据因此是像素的：截波浪上方 140px 的条带，取条带左上角作底色，
  从下往上找第一行偏离底色 >24 的像素。
- **五条锚点**挡住假绿：pager 还在、壳还是 45、它仍是 stack 的最后一个、父级仍是
  `.gb-acct-stack`、`margin-bottom` 真的读到 `-14px`。少了它们，把分页条整个删掉
  或把壳压到 31，那条「orders = 48」照样读绿。
- 切视图统一等 **750ms**（Task 40 的退出动画 500ms）。

产物判据（铁律 16）：同一编译器分别编译**改前源**与**改后源**，
`diff` **正好等于**新增的那 4 行 `@media (max-width: 767px)` 块，无一行无关差异。

回归全绿：`acctcheck` 848 · `acctmodal` 1321/0/1 aborted · `acctview` 26 · `accthover` 41 ·
`acctvars` 54 · `assetpath` GREEN · `rwd.py` ×4 全绿。
计数变动一处：`acctbp` 2352 → **2353**（+1 = 新增的那条 `margin-bottom`）。

### 文件清单

- `assets/account.scss` — `.gb-acct-pager__label` 之后新增 narrow 补偿；`$build-acct` → `20260917-a40`
- `assets/account.css` — 重编译
- `account.html` / `account-login.html` — 19 处 `?v=` 同步 a40
- `tools/acct41check.py` — 新增

### 顺带发现 / 未修

- ⚠ **`.gb-acct-pager` 的 `border-top` 让「分页条」在视觉上是一条分隔线 + 一行控件**，
  所以它的底部留白读起来比卡片更空。本轮只补齐到 48，**没有动板上的构造**。
- ⚠ 手机列表每行右侧的 5×10 chevron 仍未做（侧栏 `34631` / 手机卡 `27617`），需求仍未提。

---

## Task 40 — 视图切换改成推进/退出两段、跳过态、视频自动播放（a38 → `20260917-a39`）

需求方 2026-09-17，五条：

> 1. 效果需要优化。`gb-acct__view` 采用的 display block 导致出现消失不流畅，
>    特别是手机端像是突然从右边出现滑入屏幕
> 2. `gb-acct-sub__more` 这个有一个 tips：More than one product in a subscription /
>    +1 More products when more than one product in the subscripition
> 3. Renewal Schedule 的 Skip next order 需要补充一个样式，跳过的日期 `gb-acct-schedule__day`
>    是灰色的（Can only skip their next order, when they do, it will appear deactivated.
>    If they want to change this, they can go to "I want it now" OR "edit frequency"）
> 4. `gb-acct-video__media` 这里是自动播放的（Video Auto plays）
> 5. `gb-acct-summary__code` 如果 code 过长顶部应该和 `gb-acct-tag` 对齐

⚠ 第 2·3·4 条都是**板上便签的原文**，已逐条在本地板 JSON 里核到：
`2284:28326`（sub__more）/ `2284:30908`（skip）/ `2284:34511`（video）。

### 改了什么

**1 · 切换从「换掉」变成「换出 + 换入」两段。**
诊断是对的：`[hidden]` 就是 `display:none`，不能过渡，所以旧视图**瞬间消失**、新视图**瞬间出现**
再滑一下 —— 手机上 24px 的位移又太短，读起来就是「先蹦出来再挪一下」。三处改动：

| 改动 | 为什么 |
|---|---|
| 旧视图多活一个 `$t-view`（500ms），期间 `position:absolute` + `pointer-events:none` | 不出流的话新视图会被顶到它下面半秒 |
| 手机位移 24px → **整整一个容器宽**（`translateX(100%)`），进出对推 | 从屏幕外进来才没有「出现」这一下；桌面仍是淡入 + 上移 8 |
| `[data-acct-views]` 上 `position: relative` + **`overflow-x: clip`** | 推进推出各跑一个整宽，不夹住就会撑出横向滚动条 |

⚠ **`overflow-x: clip` 不是 `hidden`** —— `hidden` 会建立滚动容器，把另一轴一起变成 `auto`，
下拉、sticky 全受影响。`clip` 不建滚动容器，`overflow-y` 留在 `visible`。
⚠ 这条规则**是承重的**：`acct40check` 直接在动画中途量 `scrollWidth > clientWidth` 钉住它。

JS 新增 `view._leave()` / `._endLeave()`。两个坑各配了一行守卫：

- **`animationend` 会冒泡** —— 视图里任何子元素的动画都会提前触发收尾。判 `e.target !== el` 才处理。
- **快速来回切会把刚回来的视图关掉** —— 走掉一半又切回来，旧的那次退出仍挂着监听器，
  它的 `animationend` 一响就把**现在这个**视图 `hidden` 掉，整页空白。
  `show()` 开头先 `_endLeave()` 收掉上一次。判据两条都钉了。

⚠ **登录页故意没有退出动画**：它的两个 `<main>` 是 body 的直接子元素、下面就是 footer，
把其中一个抽出流会让 footer 当场往上跳半秒。`_leave()` 以 `[data-acct-views]` 这个 hook 为门，
CSS 用的是同一个 hook，两边不会各说各话。判据反向断言了「auth 页不留第二个视图在流里」。

**2 · `gb-acct-sub__more`：没有改代码，登记规则。**
便签 `28326` 说的是**后端规则**不是新文案：这行只在订阅里**多于一件商品时才出现**，
数字是「其余商品数」（两件商品 → `+1 More products`）。
板上六个实例渲染出来的字**全是 `+4 More Products`**（大写 P），便签正文自己还把
subscription 拼成了 `subscripition` —— 属于稿自带的随手笔记，故**文案按板、规则进 SPEC**。
静态站没有商品数，这条无法实现，已登进「上线前/接后端必须处理」。

**3 · 跳过下一单：逐值取自板 `2284:28922`（Renewal Schedule）。**
这块板就是专门画这个态的，四项差异全在上面：

| 板 | 落地 |
|---|---|
| 第一个日期块 fill `#E6E6E6` / stroke `#E6E6E6` / 字 `#808080` | `$c-gray-150` / `$c-gray-400`，**和 cancelled 态那三条是同一组 token** |
| `Skip next order` 按钮 fill+stroke `#E6E6E6`、字 `#808080`（正常是描边 `#005635`） | 复用 cancelled 那套禁用画法，连 `cursor: not-allowed` 挂父级的写法一起 |
| 按钮下方新增一行 `To unskip this order, edit your ` + `renewal date` | 14/20 ls−0.28 `#666666` + `$c-blue` `#0374a5` 链接，居中；链接接到 `edit-date` 弹窗 |
| 只有第一块灰 | 便签 `30908`「Can only skip their **next** order」→ 用 `:first-child`，不给每块加标记 |

状态钩子是 `.gb-acct-schedule[data-acct-skipped]`，**默认不带** —— 静态站没有订单数据，
默认挂上就等于编数据。预览方式和页面上其他状态一致（devtools 里加属性），已进 HANDOFF §5d。

⚠ **便签和板不一致**：便签说改期要走「I want it now」或「edit frequency」，
板上那行字写的是「edit your **renewal date**」。**按板做**（板是画出来的、便签是随手写的），
已登进 SPEC 待裁决。

**4 · 视频自动播放**（便签 `34511`）。`preload="none"` 换成 `autoplay` ——
两者互相矛盾，留着等于写了个不会加载的自动播放。`muted playsinline loop` 本来就在
（`muted` 是浏览器允许自动播放的前提，不是装饰）。
⚠ **仍然没有 `src`**，所以现在什么都不会播，灰底照旧透出来。

**5 · 折扣行顶对齐。** 板 `2284:28774`（paused + 已用码）里那个 51 字符的长码折成四行、
框高 72，而 `Discounts` 标签和 `Tag` 的**框顶都还在同一条线上**（三者 y 全是 1179）。
所以改的是两处 `align-items: center` → `flex-start`：外层 `.gb-acct-summary__row`
（否则标签会浮在四行的正中间）和内层 `.gb-acct-summary__discount`（需求点名的那对）。
其余几行两边等高，`center` 与 `flex-start` 渲染完全相同。

### 文件清单

- `assets/account.scss` — 入场/退场两组 keyframes + `[data-acct-views]` + `.is-leaving`、
  手机位移改整宽、`.gb-acct-schedule[data-acct-skipped]` 一节 + `__unskip`、
  `.gb-acct-summary__row` / `__discount` 两处对齐、`$build-acct` → `20260917-a39`
- `assets/account.css` — 重编译产物（已验与源码全新编译逐字节一致）
- `assets/account.js` — `view.show()` 记住上一个视图；新增 `_leave()` / `_endLeave()`
- `account.html` — `data-acct-views` 钩子、unskip 一行、`<video>` 改 `autoplay`、19 处 `?v=`
- `account-login.html` — 2 处 `?v=`
- `tools/acct40check.py` — 新增
- ⚠ **四个既有判据跟着改了**（见下）

### 判据

`acct40check` **68 ok / 0 red**，两个宽度各跑一遍。方法上三点：

- **切换过程是「中途」才存在的**，所以探针在 `pg.click()` 之后**不等**就读。
  锚点是「此刻屏幕上有 2 个视图」—— 只有 1 个就说明退出压根没发生，下面的断言全是空转。
- **`overflow-x: clip` 用它真正防住的后果来验**：动画中途 `scrollWidth > clientWidth` 必须为假。
  断言属性写没写是另一回事，这条直接量「页面会不会变宽」。
- **跳过态配了反向锚点**：断言第一块变灰的同时，断言**另外三块没变**。
  少了它，一条「所有日期块都变灰」的规则会照样读绿。

活性自检：**15 处突变全部报红且无一崩溃**。有一处先崩了 ——
把 unskip 那行改回 `display:none` 后，点它的链接 30 秒超时把脚本打死、
红数反而变少；已按老办法把那次点击包进 try/except 转成红。

⚠ 判据自己还闪了一次红：设完 `data-acct-skipped` 只等 200ms 就读按钮底色，
而那个按钮带着 `$t-base` 0.2s 的颜色过渡 —— 正好卡在边界上，
Chrome 把过渡中的值序列化成 `rgba(230, 230, 230, 1)`，和任何预期字符串都不等。
等待改成 500ms，连跑四遍稳定 68/0。

⚠⚠ **四个既有判据被本轮的行为变化打红，已跟着改**（不是放宽，是采样时机）：

| 判据 | 改动 | 为什么 |
|---|---|---|
| `acctview` | 切视图后 300ms → **700ms** | 退出动画 500ms，300ms 时屏幕上确实是两个视图。断言本身（「只剩一个」）没动 |
| `acctcheck` | 三处 450ms → **750ms** | 同上；`goto-detail` 那条路径是单独一段代码，漏了会只修好一半 |
| `acctdiff` | 400/500ms → **750ms** | 它按字符串配对再读 computed style，旧视图还在时会读到**同一句话在旧视图里的那一份**，报出 3 条莫名其妙的颜色差异 |
| `acct39check` | 选择器 `.gb-acct__view:not([hidden])` → **`.gb-acct__view.is-entering`** | 现在「没隐藏」的有两个，`getAnimations()[0]` 可能读到退出那一个 |

回归全绿：`acctcheck` 848 · `acctmodal` 1321/0/1 aborted · `acctview` 26 · `acctvars` 54 ·
`accthover` 41 · `acctmotion` 10 · `iconclip` 51 · `acct32` 66 · `acct33` 52 · `acct34` 29 ·
`acct37` 42 · `acct38` 80 · `acct39` 29 · `r25` 40 · `r26` 42 · `r27` 29 · `assetpath` GREEN ·
`rwd.py` ×4 全绿 · `acctdiff` 647/162/50（与上一轮一致）。

计数变动两处：

- `acctbp` 2327 → **2352**（+25 = 退出那一组规则 + 跳过态一节 + `__unskip` 的排版）
- `acct31check` 413 → **437**（+24）。⚠ **不是新增覆盖** —— 它按 `data-acct-modal` 的**名字**
  遍历触发器，而 `querySelector` 永远返回第一个同名元素。unskip 那行又引入了一个
  `edit-date` 触发器，于是同一个弹窗被**重复测了一遍**。无害，但别把这 24 条当成新保障。

### 顺带发现 / 未修

- ⚠ **自动播放的循环视频没有暂停控件**。WCAG 2.2.2 要求超过 5 秒的自动播放内容可暂停，
  而 `.gb-acct-video__play` 目前只是板上画的装饰件。视频源还没来，先不臆造控件，登记等拍板。
- ⚠ **`prefers-reduced-motion: reduce` 下要不要不自动播**？同上，等源文件到位一起定。
- ⚠ **手机列表每行右侧的 5×10 chevron 仍未做**（侧栏 `34631` / 手机卡 `27617`），需求仍未提。

---

## Task 39 — 切换动效放慢、问候语居中、手机列表补圆点（a37 → `20260917-a38`）

需求方 2026-09-17，原文四条：

> `.gb-acct-hello     justify-content: center;`
> 1. 点击 `gb-acct-nav__item` 的 tab 切换右侧模块动画过渡速度太快，需放慢，手机端切换 tab
>    对应显示的模块从右边划入的时候需去掉透明度变化的效果，同时划入的效果放慢
> 2. `.gb-acct-order__head (max-width: 767px)  row-gap: 0px;` 手机端的 `.gb-acct-nav__link::before` 应该保留
> 3. `.gb-acct-refer__text` 手机端 padding-t 3px；`.gb-acct-refer` 去掉 `align-item center`

### 改了什么

**1 · 视图切换从 `$t-slow` 0.3s 提到新 token `$t-view` 0.5s。**
没有直接改 `$t-slow` —— 它同时喂着弹窗淡入淡出（`--acct-modal-exit`、面板 transform），
调那一个会把弹窗一起拖慢。视图切换是整根右栏在动，本来就该比卡片久，所以单开一档。
`.gb-acct__view.is-entering` 与 `.gb-acct-auth.is-entering` 共用这条，登录页的视图切换一并放慢。

**2 · 手机端 `gb-acct-view-in-right` 去掉 `opacity` 关键帧**，只剩 `translateX(24px) → none`。
⚠ 时长是和桌面**同一个** `$t-view`：手机只换 `animation-name`，不换 shorthand。
所以「划入放慢」是靠第 1 条一起实现的，手机没有第二个数字。**要让手机比桌面更慢就得再开一档，说一声。**

**3 · `.gb-acct-hello` 加 `justify-content: center`。**
⚠ 这推翻了 Task 3 写在源码里的那句注释 ——「板 136 而内容 108，多出来的 28 是文字**下方**的
空白，不是 padding」。需求方要求上下平分，注释已改写成现在的依据。手机端 `min-height: 0`，
这条在 ≤767 不起作用。

**4 · `.gb-acct-order__head` 手机端删掉 `row-gap: 4px`**（不是写成 0 —— 不写就是 0，少一条声明）。
判据按「状态行的上沿 == 标签行的下沿」断言，不读属性，写成 `normal` 还是 `0px` 都咬得住。

**5 · `.gb-acct-list__link` 补上和侧栏一模一样的圆点** —— 这是 Task 34 自己登记的遗留：

> ⚠ **手机端的 `.gb-acct-list` 没动** —— 需求点名的是 `.gb-acct-nav__item`，那是另一个组件。

**逐值回查过板 `2284:27617`**，六行全部是同一个 `Account Section List` 组件，和侧栏同源：

| 板 | 实现 |
|---|---|
| `icon` INSTANCE 20×20 | 20 的槽 = `16.67 + 1.67×2` |
| `Ellipse 216` 16.67×16.67 `#D9D9D9` | `::before` 16.67 圆 `$c-gray-200` |
| `Container` `itemSpacing` 12 | `column-gap: 12px` |
| 文本 `x = 48.0` | 判据用 `Range` 量到 48（⚠ Range 不含伪元素，量的正是文字自己的左沿）|

⚠⚠ **补记（同日，设计方书面澄清）**：

> `.gb-acct-list__link::before` Icons — These grey circles are placeholders for Icons
> which have yet to be designed.

**这推翻了 2026-09-14 的那句「圆点不是占位而是 css 样式」**，回到便签 `27602` 原本的说法。
**代码没动**——占位本来就得画出来，且 `#D9D9D9` / 16.67 / 20 槽全部照板。
变的是性质：从「已定稿的样式」改回「待替换的占位」，已登进 SPEC 裁决 D（重新打开）
与 SPEC 8b / HANDOFF §6 的「上线前必须替换」。两处 `::before` 的源码注释也补了这一句。
⚠ 图标到位后换的是这两条 `::before`（给 `background-image` 或换成真元素），**不是加新结构**——
20 的槽、gap 12、文字左沿 48 都留着。

**6 · `.gb-acct-refer` 的 `align-items: center` 只在 ≤767 撤掉，桌面保留。**
⚠ **两块板互相不一致**，这是需求原文没覆盖到的地方：

| 板 | `action` 箭头 |
|---|---|
| `2284:27780` 桌面 | `counterAxisAlignItems: CENTER`，y = 44 = 24 + (80−40)/2 —— **居中** |
| `2284:27639` 手机 | y = 16 = padding-top —— **顶对齐** |

需求的另外两条都在说手机，且手机板确实是顶对齐，所以按手机理解。
**要连桌面一起顶对齐（即与 `27780` 不符），说一声，删一行的事。**

**7 · `.gb-acct-refer__text` 手机端 `padding-top: 3px`。**
⚠ 实际位移是 **+1.5px 不是 3px**：父级 `.gb-acct-refer__body` 是 `align-items: center`，
盒子高了 3、居中后只下移一半。改前实测标签上沿在图片下方 2.0px（板 `27639` 恰好也是
18 − 16 = 2），改后 3.5px。DevTools 里试出来的就是这个结果，故按原值落地。

### 文件清单

- `assets/account.scss` — `$t-view` 新 token、两处入场动画、`.gb-acct-hello`、
  `.gb-acct-order__head` narrow、`.gb-acct-list__link` 圆点、`.gb-acct-refer` 两处对齐、
  `.gb-acct-refer__text` narrow、`$build-acct` → `20260917-a38`
- `assets/account.css` — 重编译产物（已验与源码全新编译逐字节一致）
- `account.html`（17 处 `?v=`）/ `account-login.html`（2 处）
- `tools/acct39check.py` — 新增

### 判据

`acct39check` **29 ok / 0 red**，两个宽度各跑一遍。三件事值得记：

- **动效读的是 `getAnimations()`**，不是采样某一刻的 computed style。
  `effect.getTiming().duration` 给出真时长，`effect.getKeyframes()` 直接列出关键帧里
  **到底动了哪些属性** —— 「手机去掉透明度」这条要求，除此之外没有不靠计时的读法。
- ⚠ **context 必须显式 `reduced_motion="no-preference"`**。默认值会把时长压平，
  整段会在一个根本没跑的动画上读全绿（HANDOFF §5 记的 Task 8/31/33 那次假绿就是这样）。
- `justify-content` / 少掉的 `row-gap` / 撤掉的 `align-items` **全部按位移断言，不读属性**，
  每条都配一个锚点（「盒子确实比内容高」「body 确实比箭头高」），
  否则盒子一旦不比内容高，「上下相等」会恒真。

活性自检：**11 处突变全部报红且无一崩溃**（2/1/2/1/6/1/1/1/1/1/1 红）。
第一版有一处假绿 —— 删掉 `::before` 后六行「一致」仍然成立（都一致地没有），
且 `float('auto')` 当场抛异常；已补 `num()` 兜底与「六行确实有 `::before`」的锚点。

回归全绿：`acctcheck` 848、`acctmodal` 1321/0/1 aborted、`acctvars` 54、`acctview` 26、
`accthover` 41、`acctmotion` 10、`iconclip` 51、`acct31` 413、`acct32` 66、`acct33` 52、
`acct34` 29、`acct37` 42、`acct38` 80、`r25` 40、`r26` 42、`r27` 29、`assetpath` GREEN、
`rwd.py` ×4 全绿、`acctdiff` 647/162/50（未变）。
`acctbp` 2317 → **2327**（+10：`justify-content` 1、`column-gap` 1、`::before` 7、
`padding-top` 1、`align-items` ×2 新增，`row-gap` −1、`align-items` 原地不算增）。

### 顺带发现 / 未修

- ⚠ **手机列表每行右侧那个 5×10 的 chevron 仍未做** —— 板 `27617` 的每行都有
  （`icon` INSTANCE 20×20 → `Icon` VECTOR 5×10，x=322.33）。Task 34 在侧栏那边登记过同一件事，
  两处都还欠着。需求没提，没动。
- ⚠ `$t-view` 只有视图切换在用。要是以后弹窗也嫌快，那是 `$t-slow` 的事，别把这一档拿去复用。
- ⚠ **设计方的补充只到了第 1 条，第 2 条是空的**（原文写了个「2.」就没有下文）。
  等对方补齐再处理，本轮没有据此改任何东西。

---

## Task 38 — 三个日历换回 flatpickr，皮肤照 30465 重写（a36 → `20260917-a37`）

需求方 2026-09-17，两条：

> 1. 需要采用和 funkyfood 一样的插件
> 2. 并且样式调成 gumi 设计的这种样式

### 这是第三次改主意，先把来龙去脉钉住

| 轮次 | 指示 | 当时的前提 | 结果 |
|---|---|---|---|
| Task 25（09-15 文档第 9 条） | 「采用 funkyfood 项目中日历的同样插件做法」 | Edit Date 板 `31976` 上**只有输入框，没有日历** | flatpickr + funkyfood portal 皮肤 |
| Task 31（09-15 对话） | 「日历样式和设计不一样 —— 看 `Heading away on holiday` 的日历表」 | 发现 `30465` 画过日历 | 删 flatpickr，改自研 `.gb-acct-cal` |
| **Task 38（09-17，本轮）** | **插件用 funkyfood 的，样式用 gumi 的** | —— | **flatpickr 内核 + `30465` 皮肤** |

本轮等于把前两次各取一半：**引擎回到插件，外观留在板上**。
⚠ 所以 SPEC 的 **AI** 不再是"已反转"，**AL** 也不再是"复用自研组件" —— 两条都指向本轮。

### 改了什么

**1 · 三个日历全部换掉，`acctCal` 的手写渲染整个删除。**
页面上有三个实例：`edit-date`（字段型）/ `restart`（字段型）/ `cancel-holiday`（常驻）。
只换被点名的那一个会在同一个弹窗族里留下两套实现、外观一样而代码两份，故一并换（需求方 09-17 拍板）。
`acctCal` 保留模块名与 `window.gumiAcct.cal` 导出，内部从「自己生成 `<table>`」变成「配置 flatpickr」，
约 150 行 → 约 100 行。三处 HTML 的手写外壳（`__content` / `__head` / `__title` / `__grid`）
全部清空成空容器交给插件填，`cancel-holiday` 因为没有字段可绑，补了一个视觉隐藏的
`<input data-acct-cal-input>` 承载插件并兼作无障碍名（原先那个名字挂在 `<caption>` 上）。

**2 · 不引 `flatpickr.min.css`，皮肤整套自己写。**
外观是 100% 定制的，官方那 16KB 里几乎每条都要被覆盖，留着只会打特异性架。
`assets/flatpickr.min.css` 拷进来后又删掉了 —— **只有 `.min.js` 进仓库**。
代价是 `account.scss` 里那些布局规则（`.dayContainer` 的 grid、`.flatpickr-months` 的 flex）
**是承重的，不是装饰**：删了插件的 markup 就没有网格了。`acct38check` 用「列距必须等于容器÷7」
钉住这件事。

**3 · 皮肤逐值取自被删掉的 `.gb-acct-cal`**（即板 `30621`–`30643`）：
外框 8 圆角 + `#cccccc` 1px inset ring、`20/24` 内边距、月份条 32 高 + 下方 12、
标题 16/500/24/-0.32 `#4d4d4d`、箭头 40×40 内嵌 20 图标 `#808080`、
周名行 14/500 `#4d4d4d`、日格 40×40 圆 14/400、选中 `#005635` 白字 500、
禁用 `#808080`。`acct38check` 逐条断言，不是"看着差不多"。

flatpickr 的结构与自研的映射，写皮肤和判据都要按这张表：

| 自研 | flatpickr |
|---|---|
| `.gb-acct-cal__head` | `.flatpickr-months` |
| `[data-acct-cal-title]` | `.flatpickr-current-month`（⚠ **月份是 span、年份是 `<input type=number>`**，读标题要两个拼） |
| `[data-acct-cal-prev/next]` | `.flatpickr-prev-month` / `.flatpickr-next-month`（⚠ 是 `<span>` 不是 `<button>`） |
| `thead th` | `.flatpickr-weekday` |
| `tbody button` | `.flatpickr-day` |
| `[disabled]` | `.flatpickr-disabled` 类 |
| `[data-acct-cal-out]` | `.prevMonthDay` / `.nextMonthDay` |
| `[aria-pressed=true]` | `.selected` |
| `data-acct-cal-day`（iso） | `aria-label`（`September 18, 2026`，判据里转 iso） |

### 行为：Task 31/32 定下的五条全部保住

1. **默认收起、点字段 400ms 滑出**（Task 32）—— `.gb-acct-cal--field` 的收起机制原样保留，
   插件只是填进去；`cancel-holiday` 仍是常驻
2. **最小可选日 = 明天**（便签 `30923`）→ `minDate`
3. **过期字段值不预选、月份落在第一个有可选日的月** —— `defaultDate: null` + `minDate` 自动带过去
4. **选日期写回 `dd/mm/yyyy` 并解锁 Save** → `dateFormat: 'd/m/Y'`
5. **周一开头、`Mo Tu We Th Fr Sat Su`**（'Sat' 是板上的写法）→ `firstDayOfWeek: 1`
   ⚠ flatpickr 的 `weekdays.shorthand` **从周日索引**，`firstDayOfWeek` 只旋转显示，
   所以数组要写成 `['Su','Mo',...,'Sat']` 才能显示成 `Mo..Su`

另补两条插件没给的：`monthSelectorType: 'static'`（否则月份是个 `<select>`，读不出板上那行
「July 2026」），以及给两个 `<span>` 箭头补 `role=button` / `tabindex` / `aria-label` / 回车键。

### ⚠ 活性自检揪出三件事（判据先绿了一轮，是假绿）

第一轮判据 76 条全绿，**但突变三处代码后仍然全绿** —— 逐条查下去：

1. **`onChange` 里补派的 `input` 事件是多余的**。Task 25 记的「flatpickr 直接写
   `input.value`、不派发事件」在 4.6.13 + `allowInput: true` 下**已不成立**：实测点一天
   依次派发 `input` / `change` / `input`（第三个才是我们补的），而 `acctForm`
   两个事件都听（那条 `change` 监听是 Task 27 为 `<select>` 加的）。**已删**。
2. **`onReady` 里的 `fp.jumpToDate(min)` 也是多余的** —— `minDate` 本身就把视图带过去了。**已删**。
3. **列几何断言太松**：原本只验「七列等距」，而 `display:block` 下日格紧挨排列**也是等距**的
   （40 的间距而不是列宽的 43.14）。改成验「列距 == 容器宽 ÷ 7」才咬得住。

⚠⚠ 更要紧的是**回归判据揪出一个真 bug**：自研版 `picked` 的三元是
`from ? (from >= min ? from : null) : new Date(min)` —— **没有字段的日历（holiday）
默认选中明天**（板 `30669` 填了正好一天）。新版第一稿写成 `(from && from >= min) ? from : null`，
holiday 的新 input 是空的 → 一天都不选。`acctmodal` 的 `selCount == 1` 当场报红。
已按原逻辑改回，`acct38check` 补了两条钉住。

### 两处真实行为差异（插件固有，已接受）

- ⚠ **flatpickr 固定画六周 42 格**，自研版按月份需要画（九月是五行 35 格）。
  这是插件保证「面板高度不随月份跳动」的设计，改不掉。**日历因此比旧版高一行（40px）**，
  面板高度断言没红（收起态不受影响，`cancel-holiday` 的 672 抽屉仍放得下）。
  `acctmodal` 的网格断言已从「刚好覆盖本月的整周」改成「本月第一个周一起的六个整周」。
- ⚠ **邻月日改用 `pointer-events: none` 挡点击**（自研版用 `disabled` 属性）。
  两者都不可点，但**没有 `not-allowed` 光标** —— 与 `cancelled` 态那批禁用元素同样的取舍
  （`pointer-events` 与 `cursor` 互斥）。

### 文件清单

| 文件 | 改动 |
|---|---|
| `assets/flatpickr.min.js` | **新增**（v4.6.13，50.7KB，自 funkyfood `assets/` 原样拷入）。⚠ 旧轮那两个文件从未提交过，这次要进库 |
| `account.html` | 三处日历外壳清空；`cancel-holiday` 补隐藏 input；新增 flatpickr `<script>`；16 处 `?v=` |
| `account-login.html` | 2 处 `?v=` |
| `assets/account.js` | `acctCal` 改为配置 flatpickr（约 −50 行）；新增 `_label()` 给箭头补无障碍 |
| `assets/account.scss` | `.gb-acct-cal__*` 六段手写结构 → `.flatpickr-*` 皮肤；`$build-acct` → `20260917-a37` |
| `assets/account.css` | 重新编译 |
| `tools/acct38check.py` | 新增，80 ok / 0 red |
| `tools/acctmodal.py` | 日历段的**采集**换到新结构（断言一条没改，除六周那条）；caption 断言改成验隐藏 input 的无障碍名 |
| `tools/r25check.py` · `acct31check.py` · `acct32check.py` | 日历选择器映射；⚠ **`acct31check` 的三条「没有 vendor picker」反向断言已反转成「插件必须在」** |

### 判据

| 判据 | 结果 | 说明 |
|---|---|---|
| `acct38check` | **80 ok / 0 red** | 新增：接线 / 皮肤逐值 / 行为五条 / 插件 404 时不崩 |
| `acctmodal` | **1321 ok / 0 red / 1 aborted** | 持平 |
| `acctcheck` · `acctview` · `acctvars` · `accthover` · `acctmotion` | 848 / 26 / 54 / 41 / 10 | 全持平 |
| `acctbp` | 2299 → **2317** | +18 = 皮肤声明比手写结构多 |
| `iconclip` | 53 → **51** | −2：两个日历箭头从 HTML 搬进 JS 字符串，扫不到了（**页面里那 44 条一条没少**） |
| `acct31check` | 409+4红 → **413 ok / 0 red** | 三条反向断言反转 |
| `r25check` · `acct32check` · `r26` · `r27` · `acct33` · `acct34` · `acct37` | 40 / 66 / 42 / 29 / 52 / 29 / 42 | 全 0 red |
| `assetpath` · `rwd.py` ×4 | GREEN / 全绿 | |

**活性自检**：五次突变全部报红且不崩溃（网格 grid→block 2 红、日格 40→32 1 红、
删 `minDate` 10 红、删 `firstDayOfWeek` 2 红、删箭头无障碍标注 2 红）。
⚠ 第一次做自检时用 `grep -c '^RED'` 判定，**崩溃的那次红数是 0，看起来像判据太松** ——
已给 `css()` 加了「元素不存在就报红而不是抛异常」，现在删 `minDate` 会稳定报 10 红。

### 顺带发现 / 未修

- ⚠ **年份成了可编辑的 `<input type=number>`** —— 插件的标准结构，funkyfood 那边也一样。
  用户可以打字改年份跳到任意年（`min` 是今年）。板上那行是纯文本「July 2026」，
  **这是换插件引入的新交互面，稿里没有、需求也没提**。已把 spinner 箭头藏掉、外观与纯文本一致，
  但行为仍在。要不要锁成只读请设计方/需求方回话。
- **日历箭头的两个 svg 现在是 JS 里的字符串**，`iconclip` 覆盖不到它们（−2 的来源）。
  它们的 viewBox 与原 HTML 里逐字相同，但将来改动**不会有判据兜底**。
- **flatpickr 有一批我们没用到的能力**（区间选择、多月、时间、周选）随这 50KB 一起进了包。
  按需构建能砍掉一半，但那需要 npm 构建链，account 线目前没有。

## Task 37 — 产品下拉箭头回到共享的 20、成功屏的 Close 退回 Current Address（a35 → `20260917-a36`）

需求方 2026-09-17，两条：

> `.gb-acct-prod__control .gb-select__arrow`  `flex-basis: 20px; width: 20px; height: 20px;`
>
> 2. 在 Edit Shipping Address 弹窗点击 save 之后成功点击 close 需要返回弹窗
>    Edit Shipping Address 的 Current Address 那个弹窗

### 改了什么

**1 — 箭头**。`account.scss` 里 `.gb-acct-prod__control` 那段原本把共享下拉整体拉到小一号档
（button 40/14、option 40/14、**arrow 10**），依据是板 `84:8161` 画的 10px chevron。
需求方要 20 —— 那正好是 `customstyle.scss:10510` 里 `.gb-select__arrow` 的基类值
（`flex: 0 0 20px` + 20/20）。所以**删掉那一行覆盖**、不是再写一遍 20：
写死 20 会是一条与基类逐字重复的死代码，将来基类改了这里还会拦住。
button / option 的 40/14 小号档**没动** —— 需求只点名 arrow。

段首注释同步改掉：原文写着「draws these 40/14 **with a 10px chevron**」，
现在那半句不成立了，改成写明 10 是板上的值、20 是需求方的决定，防止下一轮按稿改回去。

**2 — 成功屏的 Close**。`shipping-success` 脚部那颗 `Close` 从 `data-acct-modal-close`
换成 `data-acct-modal="shipping-current"`。委托里 `[data-acct-modal]` 的分支排在
`[data-acct-modal-close]` 之前，`modal.open()` 自己会 `_hide()` 掉当前开着的面板，
所以**一个属性换一个属性就够**，JS 一行没改。用的是 `shipping-form` 脚部
「Go Back」早就在用的同一条路。

⚠ **右上角的 × 与遮罩仍然是真关闭**，只有脚部那颗按钮改了语义。
「关掉」和「退回上一屏」是两件事，需求说的是脚部那颗（板上写着 `Close` 的那颗）。
`acct37check` 把 × 的行为一并钉住，将来把两者接成一样会当场报红。

现在这条链是 `shipping-current → shipping-form → shipping-success → shipping-current`，
**一个闭环**，锁全程不松（切面板不解锁，`open()` 只在 `is-modal-open` 不在时才量补偿）。

### 文件清单

| 文件 | 改动 |
|---|---|
| `assets/account.scss` | 删 `.gb-acct-prod__control .gb-select__arrow` 一行；段首注释改写；`$build-acct` → `20260917-a36` |
| `assets/account.css` | 重新编译（`npx sass@1.77.8`） |
| `account.html` | `shipping-success` 脚部 Close 换属性；上方注释改写；16 处 `?v=` |
| `account-login.html` | 2 处 `?v=` |
| `tools/acct37check.py` | 新增，42 ok / 0 red |
| `docs/account/CHANGELOG.md` · `HANDOFF.md` | 本条目与基线更新 |

### 判据

`tools/acct37check.py` **42 ok / 0 red**，两个宽度（1440 / 390）各一套：

- 箭头：**先断言 `.gb-select` 真的被 `selectBox` 画出来了**（没有这个锚点，后面每条读的都是
  不存在的元素），再读 computed 的 `width` / `height` / `flex-basis` 都是 20px；
  **不变量对照**是「prod 的箭头 == `shipping-form` 里普通字段的箭头」——
  断言「等于 20」只证明数字对，断言「等于通用档」才证明它不再是特例；
  同时钉住 button 仍是 40 高 / 14px，确认删的只是箭头那一行。
- Close：走完整条链（点 Edit → 点面板里的 Edit → 填 phone 解锁 Save → submit →
  点 Close），断言开着的面板名回到 `shipping-current`、**锁还在**、success 面板已 hidden、
  退回去的面板**仍可交互**（不是只剩个壳）；再断言 Escape 照常关得掉、× 照常真关闭。

**活性自检逐条做过**：把 Close 改回 `data-acct-modal-close` → 6 红；
往 `account.css` 末尾加回 10px 覆盖 → 8 红。两次突变都当场还原，
`account.css` 与源码重新编译的产物 `diff` 逐字相同。

### 回归

| 判据 | 结果 |
|---|---|
| `acctcheck` | 848 ok / 0 red（持平） |
| `acctmodal` | 1321 ok / 0 red / 1 aborted（持平） |
| `acctbp` | **2302 → 2299 declarations** / 0 red（−3 = 删掉的三条声明，预期） |
| `acctview` · `acctvars` · `accthover` · `acctmotion` | 26 / 54 / 41 / 10，全 0 red |
| `r25check` · `r26check` · `r27check` | 40 / 42 / 29，全 0 red |
| `assetpath` | GREEN |

### 顺带发现 / 未修

- ⚠ **退回 `shipping-current` 后地址卡里仍是旧地址**（`12 Charnwood Road` / `3182`）。
  静态站的表单不回写任何东西，这是既有行为、不是本轮引入 —— 但**闭环之后它才看得出来**：
  以前点 Close 直接关窗，没人会回头看那张卡。要不要在前端把表单值写回卡片是**决策**
  （等于自造一份"已保存"的假数据），已登记等拍板。接后端后这条自然消失。
- **HANDOFF §4 有一条描述过时**：「`modal.open()` 不会把一个开着的面板换成另一个」。
  `open()` 里 `if (already) this._hide(...)` 明确处理了替换，本轮判据实测连切四个面板都正常。
  已在 HANDOFF 里更正 —— 但**「判据分支末尾要按 Escape 关掉」这条建议仍然成立**，
  理由换了：不是切不过去，而是锁不会自己松，留着会污染后面的测量。

## Task 36 — 挽留屏的灰块里补一个 `<video>` 占位（a34 → a35）

需求方 2026-09-16：「`.gb-acct-video` 里面需要加上 video 标签进行占位，可以不填链接」。

### 改了什么

`cancel-offer-skip` 面板里那块 190 高的灰块，原本只有一个 `<div>` 底色 + 白色播放键
（板 `2284:29751` 是纯 `#d9d9d9`，**没有 imageRef**，见 SPEC 占位表）。现在灰块内多一个
铺满的 `<video class="gb-acct-video__media">`，**不给 `src`**。

- `preload="none"` + 无 `src` + 无 `poster` → `networkState` 读 0，**一个请求都不发**
- 不给 `controls` —— 稿上画的是自绘的播放键，浏览器控件会盖在上面
- `muted playsinline loop` 先备着，客户接上 `src` 就能自动循环，不用再改属性

⚠ **空 `<video>` 在 Chrome 里不画任何东西**（`readyState` 0），所以父级那层 `#d9d9d9`
照常透出来 —— 实测截图取四点全是 `(217,217,217)`。**这也意味着「灰块还在」不能证明
video 加上了**，判据必须单独取 `video.gb-acct-video__media` 这个元素本身。

⚠ `role="img" aria-label="Video placeholder"` **暂时留着**：现在里面确实没有可播的东西，
读屏当成一张占位图念是对的。等客户接上 `src`，这两个属性连同 `controls` 一起要改 ——
`role="img"` 的子树对辅助技术是 presentational，**真视频留在里面等于把播放器藏了**。
HTML 里已写成一行 `TODO client`。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | `.gb-acct-video` 内新增 `<video class="gb-acct-video__media">` + 一行 `TODO client`；16 处 `?v=` → a35 |
| `account-login.html` | 2 处 `?v=` → a35 |
| `assets/account.scss` | 新增 `.gb-acct-video__media`（`display:block` + 100%/100% + `object-fit:cover`）；`$build-acct` → `20260916-a35` |
| `assets/account.css` | 编译产物（双写）。⚠ `diff` **正好等于**新增的那 6 行 |
| `tools/acctmodal.py` | 原有的 video 段追加三条：元素铺满灰块、自身背景透明、`src` 为空 |
| `docs/account/SPEC.md` | 占位表的「挽留屏的视频」一行改写 |

### 判据

判据**没新开文件** —— `acctmodal.py` 原本就有 video 那一段，三条追加在那里，跟着既有回归跑。

| 判据 | 结果 |
|---|---|
| `tools/acctmodal.py` | **1321 ok / 0 red / 1 aborted**（1315 → 1321，+6 = 三条 × 1440/390 两个宽度）|
| 突变自检 A：删掉 `<video>` 元素 | 转红 **6** 条（三条全灭，两个宽度）✅ |
| 突变自检 B：填一个 `src="acct-demo.mp4"` | 转红 **2** 条，**只有 `medSrc`** —— `medFills` / `medBg` 该绿的仍绿 ✅ |
| 还原复跑 | 1321 ok / 0 red ✅ |
| `tools/acctbp.py` | **2302**（2298 → 2302，+4 = 新规则的四条声明）|
| `acctcheck` / `acctview` / `acctdiff` / `assetpath` | 848 / 26 / 647·162·50（基线不动）/ GREEN |
| 编译产物 `diff` | **正好等于**新增的那 6 行（双写没夹带）|
| Playwright 实测 | 元素 472×190 与灰块逐像素同框、`networkState` 0（零请求）、截图取四点全 `(217,217,217)` |

⚠ 突变 B 是**必要的**一条：只删元素的话 `medSrc` 会读成 `None`，也转红，
但那只证明「断言跑到了」，**证明不了它分得清空 `src` 与真 `src`**。

### 遗留

- **上线前必须替换**：`<video>` 没有 `src`，视频内容未定。SPEC 占位表里原本写的
  「要么给真视频要么整块删掉」现在只剩前一半 —— 客户已经明确要留这块。
- 接 `src` 时要一并处理的三件：删 `role="img"` + `aria-label`、决定加不加 `controls`、
  自绘播放键要不要改成真的能点（现在它是纯装饰的 `<span>`，没有任何 handler）。

## Task 35 — 删掉 26 个没人引用的 `images/acct-*.svg`（无版本号变动）

需求方 2026-09-16 问「images 内部很多关于 account 的 svg 是否都引用了」，查完确认可删后下的指令。

### 查了什么

全仓扫描 `images/` 下 33 个 svg 的真实引用方（`docs/` 与 `tools/` 里的提及不算）：

| | 数量 | 谁在用 |
|---|---|---|
| 在用 | 7 | `favicon.svg`（14 页）、`pay-*.svg` 5 个（12 页，`account.html` 只引 `pay-visa`）、`star.svg`（pdp / reviews / customstyle） |
| **无人引用** | **26** | 全部 `acct-*.svg`，116 KB，26 个都已提交进 git |

⚠ **光看「没引用」不够**，又把每个文件最长的那段 `d` 拿去两个页面里比对：

- **22 个**：图形逐字 inline 在页面里，文件是纯重复品
- **4 个**：页面里找不到，但**不是漏做，是被取代了** ——
  `acct-qty-minus` / `acct-qty-plus` 的 viewBox 是从整板裁的紧贴框（减号 16×2），
  配方形 CSS 尺寸会被拉变形，页面里是 Task 26 重画并归一到 `0 0 14 14` 的版本；
  `acct-field-chevron` / `acct-opt-chevron` 的下拉在 Task 27 换成了 `main.js` 的 `selectBox`，
  chevron 由 `customstyle.scss` 自己画。**这四个是废件，别按文件复原回去用。**

### 删之前先救出节点号

⚠⚠ **`figma/` 整个目录不在 git 里**（`git ls-files figma/` = 0）。生成脚本
`figma/account/cut-icons.py` 里存着这 26 个图标的「板 → frame → 节点 id」映射，
**删掉文件后仓库里就没有第二份了**。

所以先把 26 条映射整表搬进 `docs/account/NODE-MAP.md`（仓库内），附两条取回路径：
① 从 `account.html` 拷 inline `<svg>`（最快，且是页面在用的那一版）；
② 在开发机上按节点号重跑 `cut-icons.py`。

⚠ `acct-alert` **不可用脚本重生**（bbox 裁切会带进面板自己的矩形，珊瑚色圆盘里的叉要保持白色
不能转 `currentColor`），`cut-icons.py` 里那条本来就是注释掉的。它的成品在
`account.html` 的 `.gb-acct-modal__alert` 里，整段可拷。

### 删除

`git rm -f`，26 条路径逐个列出（不用 `git add -A`）。
⚠ 其中 **9 个带未提交的本地改动**（Task 26/31 把紧贴 bbox 撑回 20×20 槽的修正），
所以 `git rm` 会拒绝、要 `-f`。**那些改动没有丢**：页面里 inline 的就是修正后的几何，
删前的比对用的也是工作副本。

### 验证

新写的反向验证（跑完即删，落在 scratchpad）：

1. **源码残留**：`.html/.scss/.css/.js/.liquid` 全扫，26 个文件名一次都不出现 → 0
2. **真实 404**：Playwright 加载两个页面并把九个视图逐个切过去（隐藏视图里的资源才会被请求），
   监听 `requestfailed` 与 `status >= 400` → 0

⚠ 判据先验「对照表里记着 26 个」这个锚点再做负向断言 —— 名单取空会让「无残留」恒真。

### 文件清单

- `images/acct-*.svg` × 26 — **删除**（提交时这 26 条删除要一起进去）
- `docs/account/NODE-MAP.md` — 追加 26 条节点号映射表 + 取回路径

⚠ **没有改任何页面 / 样式 / 脚本**，`$build-acct` 不变（仍 `20260916-a34`），
Shopify 那边本来就没推过这些文件。

### 顺带发现 / 未修

- ⚠ **`figma/` 不在 git 里** —— 26 张原始节点 JSON、整板 SVG、`cut-icons.py`、
  `fetch-*.py` 全部只在这台开发机上。本轮只救出了图标那 26 条映射，
  **其余设计源仍然只有一份**。要不要入库（或另存一份）请拍板。

---

## Task 34 — 需求文档新一批：auth 链接变色、波浪底色、五处尺寸、侧栏圆点（`$build-acct` = `a32` → `20260916-a34`）

需求来自 `account修改任务文档.txt`，**2026-09-16 07:06:55 整份改写**（Task 27 那轮的四条已被覆盖，
原文只在 Task 27 条目里）。四条全做完。⚠ 第 4 条的圆点**先停下问过一次**（板上那是个填 `#D9D9D9`、
frame 名叫 `placeholder` 的空图标槽，像是没填的占位），需求方回「**圆点不是占位而是 css 样式**」，
按这个做了。

### 1 · 两个 auth 文字链接：hover 变色不淡出

`a.gb-acct-auth__aside`（Forgot your password?）与 `.gb-acct-auth__alt > a`（Sign up / Log in 互切）
的 `@include hover { opacity: 0.7 }` 换成 `color: $c-lime`（`#b5ed61`），`transition` 同步从
`opacity` 改成 `color`；aside 另加 `align-self: flex-start`。

✅ **这条兑现的是 Task 30 登记的「顺带发现 / 未修」** —— 当时写「同一条房规下链接应当变色，
`.gb-acct-link` 自己的注释就说 opacity alone reads as fading out；但本轮需求点名的是按钮，所以没动」。

### 2 · `.gb-scallop--to-green` 的 `--wave-bg`

`$c-white`（#ffffff）→ `$c-cream`（#faf9f8）。两个都是现成变量，一行。

### 3 · header CTA 与 note 宽度

- `.gb-header__cta` → `padding: 0 32px`
  ⚠ **这是 `customstyle.scss:4130` 的类，主站线的文件，而且那个 40px 的注释写着
  「Client-set r78」**。需求说的是「account 的 header」，所以写成 `account.scss` 里的
  同特异性覆盖（account.css 排在 customstyle.css 之后），放在 auth 段开头紧挨站点 header 注释。
  **MVP 11 页不加载 account.css，读到的仍是 40** —— `acct34check` 专门跑一趟 `index.html` 钉死这一点。
- `.gb-acct-auth__note` → `width: 472px`
  ✅ **这是 SPEC 待裁决 AA 的回答**：两个桌面板都是表单 480 / note 472，我当初按 480 建，
  文档里写着「要真是 472 请回一句」。**AA 就此拍板**。原先 `__alt` 与 `__note` 共用一条 480 的规则，
  现在给 `__note` 单开一条，`__alt` 保持 480。

### 4 · 三处间距（圆点未做）

`.gb-acct-sub__body` `row-gap: 24 → 23.5px`；`.gb-acct-header__icons` `column-gap: 16 → 24px`；
`.gb-acct-schedule__days` 加 `padding: 0 4px`。

⚠⚠ **`column-gap: 16 → 24` 打歪了账号菜单面板** —— `.gb-acct-menu` 的
`right: calc(-40px - var(--pad-x))` 里那个 40 是 **16（图标间距）+ 24（第二颗图标）** 算出来的，
间距一改面板右边就离开视口边缘 8px。`r25check` 与 `r29check` 各报一条
`panel right edge flush want 0 got 8` 抓到的。已改成 `-48px`，并在注释里写明它跟着
`__icons` 的 `column-gap` 走。**源码看不出来，只有判据能抓。**

⚠ **`.gb-acct-sub__body` 的 23.5 连带动了续订日程块** —— `account.html:427` 是
`<div class="gb-acct-sub__body gb-acct-schedule">`，`.gb-acct-schedule` **自己一条规则都没有**，
它的 24 一直是从 `__body` 读来的。需求点名的是 `__body`，所以两处一起走了。
**如果只想动订阅卡、日程块保持 24，说一声，给 schedule 单开一条即可。**

### 4b · 侧栏圆点：`::before` 画，不引资源

需求原文「`.gb-acct-nav__item` 的 button 内部的左侧缺少一个深灰色圆点，查看设计」。
板 `2284:34578` 九行结构一致：

```
icon (INSTANCE 20×20)
  └ icon/placeholder (FRAME 16.67×16.67, r=3.33)
      └ Ellipse 216 (16.67×16.67, fill #D9D9D9)
```

⚠ 我先停下问了一次：`#D9D9D9` 是 Figma 的默认占位灰（板上所有灰图占位块、我们导出的
`product-placeholder.png` 都是这个色），而那个 frame 的名字**就叫 `placeholder`** ——
看着像没填的图标槽。需求方回复：**「圆点不是占位而是 css 样式」**，据此实现。

所以**不引任何资源**，`.gb-acct-nav__link::before` 直接画：

```scss
column-gap: 12px;

&::before {
  content: "";
  flex: none;
  width: 16.67px;
  height: 16.67px;
  margin-inline: 1.67px;   // 圆点在 20 的槽里居中，两边各补 1.67
  border-radius: 50%;
  background: $c-gray-200;
}
```

几何全取自板：槽 20、点 16.67、`Container` 的 `itemSpacing` 12，
**文字左沿落在 48**（16 padding + 20 槽 + 12）—— 判据用 `Range` 量文本节点的真实左沿钉住这条。
九行**包括 disabled 的 Contact Preferences 与 Logout 都有点**，板上九个一模一样。

⚠ **手机端的 `.gb-acct-list` 没动** —— 需求点名的是 `.gb-acct-nav__item`，那是另一个组件。
⚠ **每行右侧那个 5×10 的 chevron 仍未做**，需求没提，登在下面。
⚠ **16.67 写进 CSS 读回来是 16.6562** —— Chrome 把长度吸附到 1/64 px。判据按 `16.67px` 断言会在
正确的文件上报红，已写明。

### 文件清单

- `assets/account.scss` — 两处 hover 改色 + `align-self`、`--wave-bg`、`.gb-header__cta` 覆盖、
  `__note` 宽度单开、三处间距、`.gb-acct-menu` 的 `right` 跟到 −48、
  `.gb-acct-nav__link` 的 `column-gap` + `::before` 圆点、`$build-acct`
- `assets/account.css` — 重编译产物
- `account.html` / `account-login.html` — 各处 `?v=`
- `tools/acct34check.py` — 新增
- `tools/acctcheck.py` — 四条断言跟上新值（`__icons` 24、两处 `__body` 23.5、`schedule` 23.5）

### 判据

`acct34check` **29 ok / 0 red**。两次突变自检：七项值全部退回原值 → **13 红**（每一项至少一条）；
把 `::before` 与 `column-gap` 整块拿掉 → **3 红**（含「文字左沿 48 → 16」）。还原后都回到 29 / 0。
`acctcheck` 848（四条断言改了值，总数不变）；`acctbp` 2286 → **2290**；
`r25` / `r29` 修完回到 40 / 44。

### 顺带发现 / 未修（等拍板）

- **侧栏每行右侧的 5×10 chevron 仍未实现**（板 `34631` 的第二个 icon 槽）。需求没提，没动。
- `.gb-acct-auth__aside--hint`（sign-up 那条静态帮助文字）**不是链接**，没有 hover，本轮不涉及。
- Task 33 的两条遗留原样：购物车图标的 `href="#"` 没接目标、26 个没人引用的 `acct-*.svg`。

---

## Task 33 — header 四改：去掉汉堡菜单与变色、去掉图标 hover、修好弹窗锁屏、汉堡换购物车（`$build-acct` = `a29` → `20260916-a32`）

需求来自 2026-09-16 的对话（**不在 `account修改任务文档.txt` 里**）：

> 1. 去掉点击 `gb-acct-header__link gb-acct-header__burger` 出现的 `gb-acct-menu`
>    以及 header 变色的效果
> 2. 去掉 `.gb-acct-header__link:hover` 的透明度
> 3. account 页面弹窗打开后需禁止滚动页面，而且不能影响左侧的 sticky
>    （追加）并未修改成功，`gb-acct-modal` 弹窗出现之后依然可以进行滚动屏幕
> 4. `gb-acct-header__link gb-acct-header__burger` 需要变为购物车图标的 svg，参考设计

这是 **Task 29 第 4 条的延续**。那轮把 `gb-acct-menu` 搬进
`.gb-acct-header__link--account`、做成图标的 hover 面板，但**汉堡的点击开关留着没删**，
两条路各开各的。本轮把点击这条整条去掉，面板只剩 hover 一条路。

### 1 · 去掉的东西

| 层 | 删了什么 |
|---|---|
| `account.js` | 整个 `acctNav` 模块（点击开关 + 外部点击关闭 + Escape 关闭 + `closeMenu()`），以及 `view.init` 里那句 `acctNav.closeMenu()`、`modules` 表与 `window.gumiAcct` 里的条目 |
| `account.scss` | `.gb-acct-header.is-open`（背景换 `$c-acct-menu-bg` + 整像素内描边），连同它专用的 `transition: trans(background-color, box-shadow)`；hover 段里那条 `.gb-acct-menu:not([hidden])` 选择器（再没人摘 `[hidden]`，它永不命中） |
| `account.html` | 汉堡上的 `data-acct-menu-toggle` / `aria-expanded` / `aria-controls`，以及只为 `aria-controls` 存在的 `id="gb-acct-menu"` |

⚠ **与稿有出入，是需求方的决定不是漏做**：板 `34854`（桌面展开）与 `34804`（手机展开）
都把整条 bar 提亮成 `#f6feec` 并加一像素描边。本轮按需求去掉，bar 从此只有
`$c-lime-150` 一个颜色。判据里那两条 `.gb-acct-header` 颜色断言**改成了静止色**，
不是被删掉。

### 2 · 保留的东西

`.gb-acct-menu` 本身、它的 221/164 宽、`@media (hover: hover)` 里的淡入淡出，
以及 `&[hidden] { display: block }` 那个让面板能淡出而不是直接消失的写法，全部原样。
汉堡按钮**留在页面上**（板上有它），只是变成惰性按钮，按站内既有写法标了
`<!-- TODO client link -->`。

### 3 · 代价（已登记进交接 5c，别当 bug 修）

⚠ **触摸设备与键盘从此都打不开这块面板**：hover 面板写在 `(hover: hover)` 里，
触屏读不到；承载 hover 的 `.gb-acct-header__link--account` 是个 `<div>`，不可聚焦，
所以键盘也没有路。`acct33check` 用 `has_touch=True` 的上下文把它钉成断言
（点汉堡 → 面板 `display: none`），下一轮审计就不会当 bug 修回去。

**但没有任何链接因此失联**（这点先查清楚了再写的）：面板那四条
Account Overview / My Subscriptions / My Details / Log Out，桌面在 `.gb-acct-nav`
里全有（它还多出 Order History / Change Password / Refer a Friend / Help / Logout），
手机在 overview 的 `.gb-acct-list` 里全有，且每个内层视图都带
`.gb-acct-intro__back`（`data-acct-goto="overview"`）能回到总览。
丢的是这块面板本身，不是导航。

### 4 · 第 2 条：图标的 opacity hover

`.gb-acct-header__link` 的 `@include hover { opacity: 0.6 }` 删掉，连同它那条
`transition: trans(color, opacity)` —— hover 去掉后 `color` 与 `opacity` 在这个块里
都不再变，整条过渡是死代码。

⚠ **这是全局铁律 13 的一个例外，所以在源码里留了注释**：可点击处必有 hover 反馈。
两颗图标的情况分别是 —— 账号图标**仍然有反馈**（`::after` 那条 lime 下划线 + 掉出来的面板，
都是 hover 触发的）；汉堡自 本轮第 1 条起已是惰性按钮，没有反馈也无所谓。
`.gb-acct-header__logo` 的 `opacity: 0.7` **没动**（需求只点名 `__link`）。

### 5 · 第 3 条：**锁是漏的，真凶是 Lenis**

第一轮我查了 changelog（这条与 Task 31 第 3 条逐字相同）、跑了独立探针，得出「机制已在、
实测全绿、只补判据」的结论。**这个结论是错的**，需求方一句「依然可以滚动」推翻了它。

复现：把探针的 `reduced_motion` 从默认改成 `no-preference`，开着弹窗在遮罩上滚滚轮 ——
**scrollY 600 → 1300**。

| | Lenis 状态 | 遮罩上滚轮 |
|---|---|---|
| `reduce`（判据一直用的档） | `smoothScroll.init()` 提前 return，**Lenis 根本没起** | 600 → 600 假绿 |
| `no-preference`（真实浏览器） | Lenis 接管滚轮 | **600 → 1300** |

⚠⚠ **`overflow: hidden` 挡不住程序滚动**。Lenis 是用 `window.scrollTo` 落位的，
所以类挂得再对也锁不住它。`main.js` 自己的弹窗一直是 **`smoothScroll.pause()` + `resume()`**
成对调的（`main.js:1238` / `1288`，注释写着「The page is locked, so Lenis has nothing to do」），
而 `account.js` 的注释白纸黑字写着「Setting the class is not calling main.js —— the two
scripts still do not talk」—— **那句话就是这个 bug**。

修法是补上同一对调用，加一个 `main.js` 缺席也不炸的守卫：

```js
// main.js may be absent or may have thrown before its export landed.
function smoothScroll(method) {
  var s = window.gumi && window.gumi.smoothScroll;
  if (s && typeof s[method] === 'function') s[method]();
}
```

`open()` 里挂锁那一支调 `pause()`（与测滚动条宽度同一个 `if`，取消流程换内容时不会重复调），
`close()` 里摘锁那一支调 `resume()`。修完 `no-preference` 下遮罩与面板上滚轮都是 600 → 600。

⚠ 顺带纠正我自己上一段写进文档的话：`window.scrollTo(0, 1800)` 能越过锁**确实**是浏览器行为，
但我当时把它当成「无关紧要的已知现象」记下就过去了 —— 它正是 Lenis 绕过锁的**同一个机制**。
线索在手上没接上。

### 6 · 判据为什么一路绿到现在（三个洞，全补了）

`acct31check` **144 → 389**：

| 洞 | 补法 |
|---|---|
| ⚠⚠ **整段跑在 `prefers-reduced-motion: reduce` 下** —— 那正好是 `smoothScroll.init()` 的提前 return 条件，**Lenis 从来没在判据里跑起来过**。Task 8 / 31 / 33 三轮全绿都是这么来的 | 锁的那一段独立开 context、显式 `reduced_motion="no-preference"`，并**先断言 `window.gumi.smoothScroll.lenis` 真的在**——没有这个锚点，判据会再瞎一次 |
| **只在面板上滚滚轮** | 面板体上有 `data-lenis-prevent`，恰好是 Lenis 不管的地方。补**遮罩上**再滚一次 —— 那里没有任何 prevent 属性 |
| **只跑 1440；只比「打开 vs 关掉后」** | 抽成 `lock_section()`，1440 + 390 各一遍；抓 `rest → open → after` 三态（需求原话说的是打开那一下）；补 `PageDown`；关掉后补一条「滚轮有没有还回去」（`lenis.isStopped !== true`），否则每开一次弹窗页面就死一次 |

突变自检（三次，每次跑完还原）：

| 突变 | 结果 |
|---|---|
| `body.is-modal-open` 改成 `overflow-y: hidden`（经典的踩 sticky） | **88 红**，其中 44 条是本轮新加的「静止 → 打开」与 `@390` 才抓到的 |
| `html.is-modal-open` 的锁拆掉 | **103 红** |
| **把 `smoothScroll('pause')` 拿掉**（即回到本轮修复前的状态） | **45 红** —— `holds over the backdrop too@1440` 15 条、`holds against PageDown@1440` 15 条、`leaves the scroll position@1440` 15 条 |

⚠ 第三个突变**一条 `@390` 都没红**：手机上抽屉是满宽的，遮罩根本没有露出来的地方可滚，
`data-lenis-prevent` 正好盖住了全部可点区域。所以**这个 bug 本来就只在桌面显形** ——
和需求方看到的一致。别因此以为 390 那一半白跑了：它管的是 sticky 与锁的其余部分。

还原后回到 389 / 0。

### 7 · 第 4 条：汉堡换成购物车

`gb-acct-header__burger` 整颗换掉 —— 板上它是汉堡（`NOTES.txt` 第 100 行写明
「Hamburger menu - Opens account menu」），但第 1 条已经把那个菜单的点击拆了，留个汉堡名不副实。

```html
<a class="gb-acct-header__link gb-acct-header__cart" href="#" aria-label="Cart">…</a>
```

图标**逐字取自站点 header 的购物车**（`index.html` 的 `.gb-header__icon[data-modal=gb-cart]`，
957 字节 svg，判据里做了逐字比对），不是重画一个 —— 两个 header 的图标必须是同一个。
24×24 / `currentColor` / `stroke-width: 2`，与账号图标同规格。

- **类名从 `__burger` 改成 `__cart`** —— `__burger` 在 scss 里一条样式都没有（只有 HTML 和判据在用），
  改名几乎零成本，留着就是个谎。
- ⚠ **没有接 `data-modal="gb-cart"`**：这页没有购物车抽屉，而且 `main.js` 的 modal 与
  `account.js` 的锁会互相解锁（源码里早就写着这条警告）。现在是 `href="#"` + `TODO client link`，
  **第四个待接的死链**。
- ⚠ 它**没有 hover 反馈** —— 第 2 条把 `.gb-acct-header__link` 的 hover 删了。这是那条需求的
  直接后果，登记在交接 5c。

### 文件清单

- `account.html` — header 三处注释、汉堡去属性、`nav` 去 `id`、16 处 `?v=`
- `account-login.html` — 2 处 `?v=`
- `assets/account.js` — 删 `acctNav`（约 33 行）+ 三处引用
- `assets/account.scss` — 删 `.is-open` 与 header 过渡、hover 段去一条选择器、
  删 `__link` 的 opacity hover 与它的死过渡、`$build-acct`
- `assets/account.css` — 重编译产物
- `tools/acct33check.py` — 新增
- `tools/acctcheck.py` — `OPEN_MENU` 从点汉堡改成 hover 账号图标；两组 header 颜色断言改静止色
- `tools/acct31check.py` — 第 3 段抽成 `lock_section()`，改 `no-preference` + Lenis 锚点，
  补遮罩滚轮、390 档、「静止 vs 打开」、PageDown、关闭后交还滚轮
- `tools/acct33check.py` — 跟上 `__burger` → `__cart` 改名，补购物车图标与站点逐字比对

⚠ **`customstyle.scss` 一行没动** —— 三条锁屏规则本来就是对的，缺的是 Lenis 那一对调用，
补在 `account.js` 里。

### 判据

`acct33check` **48 ok / 0 red**，两次突变自检：
把 `.is-open` 规则塞回 css + 重新绑一个汉堡点击 → **10 红**；
把 `opacity: 0.6` 的 hover 塞回 scss 重编译 → **6 红**。两次还原后都回到 48/0。
`accthover` 42 → **41**（少了这一条 hover 属性）。

### 顺带发现 / 未修（等拍板）

- 汉堡按钮现在是惰性的、且已无 hover 反馈，`<span class="gb-acct-vh">Account menu</span>`
  这个无障碍标签也名不副实。要么接真跳转，要么整颗拿掉 —— 板上有这颗图标，所以没擅自删。
- `.gb-acct-header__logo` 仍带 `@include hover { opacity: 0.7 }`。需求只点名 `__link`，
  没动；要一起去掉说一声。
- Task 32 的两条遗留原样：`images/refer-friends.jpg` 的第三方 logo、26 个没人引用的
  `images/acct-*.svg`。

---

## Task 32 — Reactivation 接上路由、Restart 弹窗挂日历（`$build-acct` = `a28` → `20260916-a29`）

需求来自 2026-09-16 的对话（**不在 `account修改任务文档.txt` 里** —— 那份文档仍停在
Task 27 那轮的四条，且已全部完成）：

> 目前 subscriptions 已经写了暂停和已经取消的订阅，需点击暂停或者取消的订阅中的按钮
> 切换到对应模块，见 reactive 设计，点击 Re-Activate Subscription 进入里面有一个
> Restart Subscription 按钮点击出现弹窗 Restart subscoption，然后选择日期保存之后
> 变成和点击 Manage Subscription 之后出现的内容一样

随后追加一句：**「save 不需要改变状态，这只是静态展示站，展示交互效果即可」**，
所以最后一段（转回 ACTIVE）没做，见下。

### 1 三张订阅卡各自打开 detail 的对应状态

便签 `28323`：「Cancelled Re-Activate goes into the reactivation flow」。改之前：

| 卡 | CTA | 点下去 |
|---|---|---|
| ACTIVE | `Manage Subscription` | detail（active 态）|
| PAUSED | `Manage Subscription` | detail，**但仍是 active 态** |
| CANCELLED | `Re-Activate Subscription` | `href="#"`，**哪都不去** |

detail 只有一份 DOM，状态挂在 `.gb-acct-detail[data-acct-sub-state]` 上、HTML 里写死 `active`，
三个状态本来只能在 devtools 里手改（HANDOFF 5d）。做法两处：

- cancelled 卡的 `<a href="#">` 换成 `<button type="button" data-acct-goto="detail">`，与另两张一致
- `view._subState(trigger)`：切视图**之前**读触发按钮所在卡的 `data-acct-sub-state`，写到 detail 上

⚠ **选择器必须是 `.gb-acct-sub[data-acct-sub-state]`，不能裸写 `[data-acct-sub-state]`** ——
detail 视图自己的外层 `.gb-acct-detail` 也带这个属性，裸选会让 detail 里那个返回按钮
把状态写成它自己的当前值（自己覆盖自己）。detail 内的 `.gb-acct-sub--detail` 没有这个属性，
所以加了 `.gb-acct-sub` 之后只有列表卡命中。

⚠ **走 hash（`#detail`）进来不经过这段**，落在 HTML 写死的 `active` 上。这是有意的：
没有触发卡就没有来源状态，猜一个只会让直接开链接的人看到一个没来由的状态。

### 2 Restart 弹窗挂上日历

板 `34192` 的 restart 面板只有一个文本框（`22/07/2026`）。需求方要「选择日期」，
所以复用 Task 31 给 Edit Date 接的那套 `.gb-acct-cal`：

- DOM 照抄 `edit-date` 那块，只改 `data-acct-cal-for="acct-f-restart"` 与 caption 文案
- `acctCal` 在 Task 31 已经改成多实例（状态在 `root._cal` 上）
- 便签 `34040`（「They cant restart until next day」）与 `30923` 是同一条规则，
  `acctCal` 的 `min = 明天` 已经覆盖，不必另写

### 2b ⚠ 反转 Task 31：日历默认收起，点 input 才展开

需求方 2026-09-16 追加：「Restart subscoption 内部的日历默认也是隐藏的，点击 input 才会出现」。

⚠ **这说明 Task 31 那句需求我读反了**。原话是「Edit renewal date 的样式没还原设计，
**下面的日历要点 input 才出现**，而且日历样式和设计不一样」—— 我当时把中间那句当成
对 flatpickr 按需加载的抱怨，改成了常驻显示；它其实是「要…才…」的**期望行为**，
和 flatpickr 本来的弹出式一致。**「也」字指的就是 Edit renewal date**，所以两个面板一起改。

做法照 FAQ 手风琴那套（`slideTo` + `.acct-live` 门控），没有新机制：

- 收起态 `height: 0` + `visibility: hidden`（**零高 + overflow:hidden 仍然可 Tab、仍被读屏念**，
  见 Task 29 的同一条教训），挂在 `:root.acct-live` 上 —— 写死的话脚本一挂日历就永久不可见
- 点 `input` 时 `slideTo(root, …)` 切 `.is-open`，400ms、与站点手风琴同一组值；再点收起
- ⚠ **收起态要写 `margin-top: -6px`**：`.gb-acct-field` 是 `row-gap: 6px` 的 flex 列，
  **零高的 flex 项照样吃这个 gap**，不抵掉的话 input 下面凭空多 6px
- `cancel-holiday` 那张板的日历不受影响 —— 它没有 `data-acct-cal-for`（display only），
  绑定挂不上去，保持常驻。板上画的就是常驻。
- 需求方 2026-09-16 追加**给 input 加 `cursor: pointer`**（它现在是开日历的按钮，
  哪怕仍是可输入的 text）。选择器用 `.gb-acct-field:has(> .gb-acct-cal--field)`，
  **不碰其余字段的 text 光标**

两条既有判据的期望值被这次需求反转，**都是改断言不是删断言**（改回原行为仍会红）：

| 判据 | 原断言 | 现在 |
|---|---|---|
| `acct31check` | `calendar is visible on open` | `calendar is shut on open` + 点字段后可见 |
| `r25check` req 9 | 直接点日期格 | 先点字段展开，再点日期格 |

⚠ **`r25check` 原本不是报红而是整个崩掉** —— 日历收起后 `Locator.click` 等 30s 超时抛异常，
脚本死在那一行。**崩了看起来像红更少，不像失败**（见
[[reverse-verification-needs-crashproof-slicing]]）。`acct32check` 里同一处点击已经
包进 try/except 并把异常名当读数报出来。

✅ **面板高度因此回到了板上的值**：收起态 `edit-date` @390 = **290**（板 `31976`）、
`restart` @390 = **329**（板 `34192`），实测逐值吻合。
所以 Task 25 把 edit-date 高度断言改成 NOTE 的那条**已经恢复成真断言**，
本轮新加的 restart 那条也直接写成断言。展开态 632 / 671 不再是常驻高度，
**待裁决 AJ（「加了日历后面板变高」）随之消解**。

⚠ **输入框里的 `22/07/2026` 已经是过去的日期**，所以日历打开时不预选任何一天、
月份落在第一个有可选日的月 —— 与 edit-date 同理，不是 bug。

### 明确不做：Save 之后转回 ACTIVE

板 `34352`（重启后转回 ACTIVE）**没有实现**，`restart` 的 Save 仍然只是 `data-acct-modal-close`。
需求方 2026-09-16 明说静态展示站不需要改状态。
⚠ 连带的结果是**列表卡的状态也不会变** —— 重启后按返回箭头回列表，那张卡仍是 CANCELLED，
再点进去还是 cancelled 态。**这是预期，不是漏改。**

### 3 HTML 里补功能注释（需求方 2026-09-16 第 3 条）

「html 结构内需补上一些注释，比如模块注释（一句介绍模块功能）弹窗注释」。
`account.html` 加 36 条、`account-login.html` 加 3 条：每个视图、每个弹窗、
每个结构块（header / 两处导航 / 汉堡面板 / 分页 / footer）各一句英文。

⚠ **这与 Task 25 移走的 33 条不是一回事**：那些是**节点定位**注释（`2284:xxxxx`），
移去了 `NODE-MAP.md`，**不再回到 HTML**。这次补的是**功能**说明。

需求方随后点名「像 `2284:28072 / 28109 / 28146 desktop…` 这种注释应该去掉」，
顺着清了 Task 25 漏网的三条，**每条都先收进 `NODE-MAP.md` 再从页面删**（节点号别处没有，
直接删就丢了）：

| 位置 | 处理 |
|---|---|
| `.gb-acct-subs__list`（三张卡的六个节点号）| 整条移入 NODE-MAP；功能已由新加的视图注释覆盖 |
| `.gb-acct-auth`（signup 的两个节点号）| 整条移入 NODE-MAP |
| `.gb-acct-order`（三个状态各一个节点号）| 节点号移入 NODE-MAP，页面留「三种状态、由修饰类挑一个、运行时不切」|

⚠ **扫节点号要扫整个注释块，不能按行 grep** —— `.gb-acct-order` 那条是多行注释，
节点号在第 3–5 行，`grep '<!--'` 只看首行，第一遍就漏了它。

⚠ **注释对外可见**（前端源码线上可直接下载）。顺带把 Suburb 那条里的
**另一个客户的项目名去掉了** —— 原文写着某站怎么做自动补全，改成「需要 Places API key
与配送区数据，本店都还没有」。写的是这块做什么，不写内部状态、待裁决或稿件错误的细节
（`restart` 那条只说「标题沿用设计的拼写」）。

### 4 五个资源上主题（需求方 2026-09-16 第 4 条）

「把 account 相关 css js 和一些相关图 svg 等通过后台 cli 传到 gumi shopify 中」（随后追加 `account.scss` 也推）。

推了 `account.css` / `account.js` / `account.scss` / `product-placeholder.png` / `acct-bear-side.png`，**全是新增、零覆盖**，回读 10 ok / 0 red，基线滚到 `baseline-20260916-a29`。逐条见 [PUSH-LOG.md](PUSH-LOG.md)。

⚠ **`refer-friends.jpg` 没推** —— 画面里有第三方品牌 logo，推上客户店铺等于把商标风险带过去。
⚠ **26 个 `acct-*.svg` 没推** —— 页面用 inline svg，一个都没引用。
⚠ **主题里没有 `images/` 目录**，本地 `images/x.png` 要推成 `assets/x.png`。
⚠ **推了资源 ≠ account 上线**：线上还没有模板引用它们。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | ① cancelled 卡的 CTA `<a href="#">` → `<button data-acct-goto="detail">`（连同那条 `TODO client link` 注释一起删）；② `restart` 面板的字段里插入 `.gb-acct-cal--field` 一块；③ **36 条功能注释**；④ 16 处 `?v=` → a29 |
| `assets/account.js` | 新增 `view._subState()`，在 goto 委托里 `show()` 之前调用 |
| `assets/account.scss` | 只有 `$build-acct` → a29（没有新样式：日历与 CTA 都用既有的类）|
| `assets/account.css` | 编译产物（双写）|
| `account-login.html` | 3 条功能注释；2 处 `?v=` → a29（它加载的是同一份 account.js/css）|
| `tools/acctmodal.py` | `restart` 的高度断言写成真断言（329）；`edit-date` 的 `None` 恢复成 290 —— 日历收起后两个面板都回到板上的几何 |
| `tools/acct31check.py` | 日历可见性断言**反转**（开面板时应收起，点字段后才可见）|
| `tools/r25check.py` | req 9 点日期前先点字段展开，否则整个脚本超时崩掉 |
| `tools/acct32check.py` | **新增**，56 条：三张卡的 CTA 形态与路由、detail 开在对应状态、状态真的换了内容、restart 的日历存在且驱动输入框、最早只能明天 |
| `docs/account/HANDOFF.md` | 5d 的「没有 JS 会自己切」加例外说明；§6 的 `href="#"` 四处 → 三处；§4 判据表加 `acct32check` |
| `docs/account/SPEC.md` | §8b 的占位表：Re-Activate 从死链清单移出；待裁决 AJ 标为已消解 |
| `docs/account/NODE-MAP.md` | **收录三条从页面清出来的节点号注释** |
| `docs/account/PUSH-LOG.md` | **新增**，account 线自己的推送记录（`docs/PUSH-LOG.md` 是主站线的，不碰）|
| `tools/acctpush.py` | **新增**，推送回读判据（含短拉守卫）|

### 判据

`tools/acct32check.py` **66 ok / 0 red**（390 与 1440 两档）。
全量回归：`acctcheck` 849 / `acctview` 26 / `accthover` 42 / `acctmotion` 10 /
`acctvars` 54 / `assetpath` GREEN / `iconclip` 79 / `r26`–`r30` 42·29·32·44·53 /
`acctdiff` 647 paired·162 differ·50 unmatched / `rwd` 四条全绿，**全部 0 red**。

四条基线上调，**都是判据变强不是实现变松**：

| 判据 | 旧 | 新 | 为什么 |
|---|---|---|---|
| `acctmodal` | 1314 | **1315** | 日历收起后面板几何回到板上：`restart` 的高度写成真断言，`edit-date` 那条 NOTE（Task 25 留的）也恢复成断言 |
| `acct31check` | 143 | **144** | 可见性断言反转，另加一条「点字段才展开」|
| `r25check` | 39 | **40** | req 9 补一条「点字段展开」|
| `acctbp` | 2286 | **2292** | 收起态与 `cursor` 共 6 条新声明 |活性自检逐条突变：
拆掉 `_subState` 调用 → 5 红；拆掉 `data-acct-cal-for` → 4 红；CTA 改回 `<a href="#">` → 5 红。

⚠ **判据第一版自己写错过一条**：用 `[data-detail-only~='paused']` 取 paused 专属元素，
结果匹配到了 `data-detail-only="active paused"` 那 9 个（active 态下它们本来就该可见），
在 active 态下报出 2 条假红。改成精确匹配 `[data-detail-only='paused']`（全页 2 个）。
**`~=` 在这套状态开关上一律读不出「只属于某态」** —— scss 里那段 `@each` 的注释早写过这件事。

### 遗留 / 顺带发现（等拍板，本轮没动）

- **板 `34352`（重启后转回 ACTIVE）没有实现** —— 需求方指示静态站不改状态，见上。
  接后端时这条要补，且列表卡的状态要跟着一起变。
- **restart 面板加日历后高约 632，板上是 329** —— 与待裁决 AJ 同源，390×667 会滚。
- **Task 29–31 的旧遗留原样保留**：九个视图仍是无条件 `[hidden]`、四处重复 SVG id、
  七个视图的 `rwd` 溢出扫描从未跑过、两个 auth 文字链接仍用 `opacity` 淡出。

---

## Task 31 — icon 裁切、Edit Date 换回本站日历、桌面弹窗内文适配、弹窗锁屏（`$build-acct` = `a27` → `20260915-a28`）

需求来自 2026-09-15 的对话（**不在 `account修改任务文档.txt` 里**），三条：

1. svg 的 icon 下面被裁（点名 `gb-acct-field__icon`）；Edit renewal date 的样式没还原设计，
   下面的日历要点 input 才出现，而且日历样式和设计不一样 —— 看 `Heading away on holiday` 的日历表
2. PC 端弹窗宽度增加了但内部内容没自适应；`gb-field__input--select` 点开的下拉应该往下；
   `gb-acct-modal__cross` 也被裁（似乎所有 icon 都被裁，应该需要重新导出 svg）
3. 检查 account 所有弹窗，出现时都要锁住屏幕不滚动，并且不影响左边 sticky 的布局

### 1 icon 被裁：不是导出的问题，是 viewBox 取错了框

`figma/account/cut-icons.py` 把 icon 的 **`absoluteBoundingBox`**（几何外框）当 viewBox。
描边是居中对齐的，一半墨迹落在几何框外 —— Figma 自己的 `absoluteRenderBounds` 就写着这件事：

| icon | vec（旧 viewBox） | render（真墨迹） | 槽（新 viewBox） |
|---|---|---|---|
| `modal-close` | 10×10 | **12×12** | 24×24 |
| `field-date` | 15×16.667 | **16.666×18.332** | 20×20 |
| `cal-prev/next` | 5×10 | **6.67×11.672** | 20×20 |

**所以不用重新导出** —— 路径数据本身是全的，被裁掉的是渲染时超出 viewBox 的那半条描边。
viewBox 改指 icon 在板上的**槽**（父 frame），墨迹有余量、位置与比例也回到设计值。
叉号最显眼：10 单位在 24px 按钮里放大 2.4 倍，裁掉的 1 单位就是 **2.4px**。

⚠ **只有 9 个 icon 真被裁**（render > vec）。其余 `vec == render` 的本来就对，
**换槽会把它们搞坏** —— 那些 icon 的父节点是整行 frame（如 `252×44`），
第一版条件写宽了，17 个 icon 的 viewBox 当场被拉成整行。现在只有被裁的才换槽。

⚠ `images/acct-*.svg` **26 个全部没有被页面引用**，页面用的是 inline svg。
两边都改了，但生效的是 inline 那份。

### 2 Edit Date 弃用 flatpickr，改用板上唯一画过的日历

需求方说的 `Heading away on holiday` 的日历表就是 `cancel-holiday` 面板的 `.gb-acct-cal`
（板 `30465`，Task 12 已按板做好、运行时生成）。Edit Date 之前用的是 flatpickr + funkyfood 皮肤，
那是**稿里没有日历**时的权宜（SPEC 待裁决），现在有了正主。

顺带解决了「要点 input 才出现」：flatpickr 是**按需加载**的（Task 10 的性能优化），
点开面板到脚本落地之间日历是空的。`.gb-acct-cal` 同步生成，面板打开就在。

> ⚠ **Task 32（2026-09-16）反转了这一段**：需求方原话里的「下面的日历要点 input 才出现」
> 是**期望行为**（「要…才…」），不是对按需加载的抱怨。日历现已改回默认收起、
> 点字段才展开。此处保留原文以存记录，行为以 Task 32 为准。

- `acctCal` 从单例改成**多实例**：状态从模块搬到 `root._cal`，
  否则两个面板共享 `picked`/`view`，动一个另一个跟着跳
- 新增 `data-acct-cal-for`：指名这个日历驱动哪个 input。选中后写回并**派发 `input` 事件** ——
  `acctForm` 的 Save 门控盯的是这个事件，静默赋值会让 Save 对一个真的改过的日期保持灰着
- ⚠ **稿上的 `19/07/2026` 已经是过去**（今天 2026-09-15）。过期值**不预选**，
  但月份落在**第一个有可选日的月**：落在 July 会得到一个整月点不动的日历，
  钳到明天又会显示一个和输入框对不上的高亮
- flatpickr 三个文件与皮肤全部删除（`assets/flatpickr.min.js|css`、scss 的 `.gb-acct-datepicker` 段、
  html 的两条 `<link>`、js 的 `acctDate` 模块 81 行）

### 3 桌面 520 的内部适配只有一处真问题

逐个量了 11 个面板的内部元素，**唯一写死的是 `.gb-acct-modal__copy` 的 `max-width: 320px`** ——
在 520 的面板里正文折三行、右边空 150。其余「看着没撑开」的都是布局算出来的：
`.gb-acct-prod` 228.5 是两列 grid 的一半，`.gb-acct-addr__lines` 278.6 是 radio 让出的宽度。

改成 `calc(100% - 30px)`：板上是 `320` 在 `350` 里，**30 的留白才是组件，320 不是**。
手机档算出来仍是 320。

### 4 下拉翻上的真因是 modal body 的 overflow，不是下拉自己

`main.js` 的 `selectBox.wouldOverflow()` 会让列表避开**最近的裁切祖先**，
而 `.gb-acct-modal__body` 是 `overflow-y: auto` —— **不滚也照样裁**，于是短面板里的下拉一律翻上、
盖住自己的 label。`modal._fit()` 在打开时量一次，body 不需要滚就把 `overflow-y` 放成 `visible`。

⚠ **不能用 `scrollHeight` 判断**：每个关闭态的 `.gb-select` 都把绝对定位的列表留在 DOM 里，
它会被算进 `scrollHeight`，于是一个肉眼毫无溢出的面板报出 62px 溢出、然后把自己锁死在 auto。
量的是**静态流**（body 直接子元素的 rect 底边）。

⚠ 内容可能在打开**之后**变高（resize、将来接店铺的异步列表），
body 停在 `visible` 就再也滚不到那部分、还会被 panel 的 `clip` 吃掉。
挂了 `ResizeObserver`（只认高度变化，宽度变化是我们自己的滚动条来回，会直接把它转成死循环）+ `resize` 重测。

结果：`edit-frequency` / `edit-product` 桌面下往下开且不被面板裁；
`add-product` / `shipping-form` 内容是真的要滚，**保持翻上是对的** —— 往下会被滚动区裁掉。

### 5 弹窗锁屏本来就是对的，跳的是关闭那一下

实测 20 个面板：`is-modal-open` 全部挂上、滚轮全部锁死、sticky nav 与 header 全程不动。
真正的毛病在 `close()`：`back.focus()` 把触发按钮滚回视野，而这一下发生在**锁刚松开之后** ——
页面在面板淡出的同时跳走（实测 `edit-name` 600→0、`cancel-offer-skip` 600→1445），
看起来就像 sticky 布局被弹窗影响了。`focus({ preventScroll: true })` 修掉，`open()` 同样补上。

⚠ 这条**源码审查看不出来**：锁的实现一直是对的，跳发生在锁的生命周期之外。

### 判据

| 判据 | 结果 | 说明 |
|---|---|---|
| `tools/iconclip.py` | **79 ok / 0 red**（新增） | 每个 icon 画两遍（原 viewBox / 四边放开），落在放开区里的墨迹就是被裁的。**用画的不用算的** —— `d` 里的弧参数会和坐标混在一起，数值包络报一堆幻影溢出 |
| `tools/acct31check.py` | **143 ok / 0 red**（新增） | 本轮三条。突变自检：去掉 `preventScroll` → 9 红，`copy` 改回 320 → 3 红，去掉 `_fit` → 4 红 |
| `acctcheck` / `acctview` / `acctvars` / `assetpath` | 849 / 26 / 54 / GREEN | 不变 |
| `accthover` / `acctmotion` / `acctdiff` | 42 / 10 / 647·162·50 | 不变 |
| `r26`–`r30check` | 42 / 29 / 32 / 44 / 53 | 不变 |
| `r25check` | **39**（原 36） | req 9 改写成日历组件的五条断言 |
| `acctbp` | **2286**（原 2297） | −11 = 删掉的 flatpickr 皮肤 |
| `rwd.py` ×4 | 全绿 | |

**`acctmodal.py` 三处断言改了口径**（都是在锁旧行为，不是放水）：

1. `copy` 宽从写死 320 改成「可用宽 − 板上的 30」，与 Task 27 把面板宽改成「手机 390 / 桌面 520」同理
2. body 的 `overflow-y` 允许 `visible`，**但仅当它真的不滚**；会滚的仍必须是 `auto`
3. Lenis 那段塞 2000px 探针之后**强制把 `overflow-y` 设回 auto**（收尾还原）——
   它测的是「谁拿着滚轮」，不是「哪些面板会滚」

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | 26 处 viewBox 换槽；Edit Date 的 host 换成 `.gb-acct-cal` 结构；去掉 `data-acct-datepicker`；删两条 flatpickr `<link>`；`?v=` → a28 |
| `account-login.html` | `?v=` → a28 |
| `assets/account.js` | `acctCal` 多实例 + `data-acct-cal-for` 写回 + 输入框反向同步；删 `acctDate`（81 行）；`modal._fit()` + `ResizeObserver` + resize 重测；两处 `focus({preventScroll:true})` |
| `assets/account.scss` | 三处 svg 框跟上新 viewBox（24/16/20）；`__cal__content:last-child` 去掉分隔线；删 `.gb-acct-datepicker` 皮肤、换成 `.gb-acct-cal--field`；`__copy` 改 `calc(100% - 30px)`；`$build-acct` → a28 |
| `assets/account.css` | 重新编译 |
| `assets/flatpickr.min.js` · `.css` | **删除** |
| `images/acct-{cal-prev,cal-next,chip-remove,field-chevron,field-date,modal-close,opt-chevron,qty-minus,qty-plus}.svg` | viewBox 换槽（9 个；页面未引用，保持素材源可信） |
| `figma/account/cut-icons.py` | 改用槽，**仅对被裁的**（`renderBounds > boundingBox`）；父框过大时退回 `renderBounds`。⚠ 不入库 |
| `tools/iconclip.py` | 新增 |
| `tools/acct31check.py` | 新增 |
| `tools/r25check.py` | req 9 改写 |
| `tools/acctmodal.py` | 三处断言口径 + 两处采集 |

### 待设计方裁决（新增三条）

`SPEC.md` §7 新增 **AL**（Edit Date 直接复用挽留流程里的日历组件，若两处应有不同样式请给板）、
**AM**（桌面正文宽度是外推：判定「右侧 30 的留白」是组件、320 不是）、
**AN**（下拉方向随面板会不会滚动而变，要「任何情况都往下」得把它改成脱离面板的浮层，动的是主站线的组件）。
旧的 **AI**（「Edit Date 的日历稿里不存在」）已被本轮反转、划掉并指向 AL；
**AJ** 的面板高度从 flatpickr 的 604 变成 `.gb-acct-cal` 的 **632**。

### ⚠ 过程事故：差点把主站的判据覆盖掉

本轮判据最初写成 `tools/r31check.py` —— **仓库里已经有一个同名文件，是主站线 Round 31 的判据**，
用 `cat >` 建文件当场把它整个覆盖。发现的唯一信号是 `git status` 把它列成 **`M` 而不是 `??`**。
已 `git checkout HEAD -- tools/r31check.py` 还原，本轮判据改名 `tools/acct31check.py`。

`r25`–`r30check.py` 是侥幸：主站那几轮的文件不在 HEAD 里。但 `r31` / `r32` 都被占着，
**account 线以后一律用 `acctNNcheck.py`**，新建 `tools/` 下的文件前先
`git ls-tree -r HEAD --name-only tools/ | grep <名字>`。

### 顺带发现 / 未修

- **`skip-next` 的正文写着 `Are you sure you wan to skip`（少个 t）** —— 未查证是不是稿自带，
  本轮需求没点名，没动。要改先比对板 `32621`
- **`.gb-acct-cal` 的表头是 `Sat` 而不是 `Sa`** —— 板上就是 `Sat`（Task 12 的注释写明），不是笔误
- **`images/acct-*.svg` 26 个全是死文件** —— 页面只用 inline svg。删不删是决策，没动
- **`acct-qty-minus.svg` 的新 viewBox 是 `49 700 16 2`（墨迹框）不是 20×20 的槽** ——
  槽比这条纯横线大 10 倍，超过了「槽不能太大」的守卫。它本来也没被裁，未引用，无影响

---

## Task 30 — 按钮 hover 归队、灰块换占位图、去掉图标位移、Copy 限宽、footer 波浪底色（`$build-acct` = `a26` → `20260915-a27`）

需求来自 2026-09-15 的对话（**不在 `account修改任务文档.txt` 里**）：

1. account 相关按钮的 hover 风格要和其他页面一致
2. `.gb-acct-sub__thumb` / `.gb-acct-item__thumb` / `.gb-acct-referral__hero` 这种灰色 CSS 背景改成灰色图片占位
3. `.gb-acct-referral__social-link` 去掉 hover 偏移
4. `.gb-acct-field__input` 太短，限制 `.gb-acct-referral__copy` 的最大宽
5. （追加）account footer 的 `.gb-scallop--to-green` 改成 `--wave-bg: #fff`

### 1 · 按钮 hover：房规不是口味，写在 `.gb-btn` 的注释里

`customstyle.scss:1363` 的 `.gb-btn` 注释已经把标准定死了：

> Hover shifts colour only — no lift, no shadow (house rule). … the button flips to
> the lime accent, because **darkening green on green (#005635 -> #004128) is
> technically a change but reads as none**.

account 有五个按钮没跟上，全部改成 `background: $c-lime; color: $c-green-900;`
（有描边的连 `border-color` 一起走，`--ghost` 因此整块填满，与 `.gb-btn--lg` 同一个动作）：

| 选择器 | 原来 | 为什么不合规 |
|---|---|---|
| `.gb-acct-order__cta` | `opacity: .85` | 淡出读作「失效」，不是 hover |
| `.gb-acct-logout` | `background/border: $c-green-900` | **正是注释点名的 green-on-green**，眼睛读不出来 |
| `.gb-acct-sub__cta` / `.gb-acct-btn`（含 `--ghost`） | `opacity: .85` | 同上 |
| `.gb-acct-modal__save` | `opacity: .85` | 同上 |
| `.gb-acct-discount__apply` | `opacity: .85` | 同上 |

⚠ **四处的 `:disabled` 里各有一条 `opacity: 1`，它只为抵消 hover 的淡出而存在**。
改成变色后它就是死代码，但**不能只删不补** —— 删掉之后禁用按钮会跟着变亮绿。
hover 因此收进 `&:not(:disabled)`，四条 `opacity: 1` 一并删除。判据补了一条
「禁用按钮对 hover 无反应」锁住这一对。

已经合规、**没动**的三个：`.gb-acct-refer__action`、`.gb-acct-intro__back`、
`.gb-acct-auth__submit`。

### 2 · 三处灰块换占位图 —— 先例在 Task 26

`images/product-placeholder.png`（400×400 `#d9d9d9`）**本轮没有新建**，
Task 26 把 `.gb-acct-prod__thumb` 从 CSS 底色换成它时就导出了，这次是把剩下三处补齐，
用同一张、同一套 `<img … width="400" height="400" alt="" loading="lazy" decoding="async">`。
主站 `$c-gray-200` 的注释写着「borders only — r120 dropped every placeholder ground」，
两条线的做法本来就该一致。

- `.gb-acct-sub__thumb` ×3：`<span aria-hidden>` → `<img>`（`alt=""` 已经等价，`aria-hidden` 不再需要）
- `.gb-acct-item__thumb` ×4：`<div>` → `<img>`
- `.gb-acct-referral__hero` ×1：`<div>` → `<img>`，⚠ 灰色从我自定的 `#eeeeee` 统一到 `#d9d9d9`

⚠ **`width="400" height="400"` 给的是比例不是尺寸**，hero 要的是 16/9 ——
CSS 的 `aspect-ratio` 压过属性比例，所以 `aspect-ratio: 16 / 9` 必须留着，
判据里直接量 `offsetWidth / offsetHeight` 锁住。

### 3 · 分享图标去掉位移

`transform: translateY(-2px)` 是我在 Task 29 自定的（稿上根本没有这个模块），
与第 1 条的房规「no lift」本来就矛盾，删掉，`transition` 同步去掉 `transform`。

### 4 · Copy 限宽 —— 输入框被按钮挤没了

真因不在输入框：`.gb-acct-btn` 是 `width: 100%`，而 `flex: none` 的 `flex-basis: auto`
**从 `width` 取值**，于是 Copy 按钮的基准尺寸就是整行宽，输入框被 `flex-shrink` 压到接近 0。
⚠ **看源码看不出来** —— 每条声明单独看都对。`max-width: 120px` 封顶后实测
行宽 529 → 输入框 **401** / 按钮 **120**；`narrow` 那档原本刻意的整行按钮用
`max-width: none` 放回去。

### 5 · footer 波浪的底色

需求方追加，**指明直接改、不跑判据**。

⚠ **真正胜出的规则在 `customstyle.scss:3637`**（`--wave-bg: $c-lime` / `--wave-fg: $c-green-900`），
那是主站线文件，这条线不碰。覆盖写进 `account.scss`，紧挨着同族的 `.gb-scallop--mint-to-cream`
（将来一条 grep 找得齐）——`account.css` 排在 `customstyle.css` 之后加载，同特异性靠顺序胜出，
和那一行是同一个写法：

```scss
.gb-scallop--to-green { --wave-bg: #{$c-white}; }
```

只改 `--wave-bg`，`--wave-fg` 原样。覆盖 `account.html` 与 `account-login.html` 两页的 footer。
⚠ **没有再 bump `$build-acct`** —— a27 还没推过，这次改动仍在同一个未发布的版本里。

### 判据

| 判据 | 结果 | 说明 |
|---|---|---|
| `tools/r30check.py`（新增） | **53 ok / 0 red** | 四条逐项，hover 全部**实测悬停后的 computed 值**，不信源码 |
| `tools/acctcheck.py` | **849 ok / 0 red** | 1 红是预期：`.gb-acct-sub__thumb` 的 `background-color` 断言随本轮作废，改断 `object-fit` |
| `tools/accthover.py` | 37 → **42 properties / 0 red** | 五个按钮各多赋 1–2 个属性（+6），social 少一个 `transform`（−1），净 **+5** |
| `tools/acctbp.py` | 2289 → **2297 decl / 0 red** | 逐条 **+8**：hover 增减净 +4、三处 thumb +4、Copy 两档 +2、四条 `opacity:1` −1、`transform` −1 |
| `tools/acctmodal.py` | **1314 ok / 0 red / 1 aborted** | 见下 |
| `tools/acctdiff.py` | 647 paired / **162 differ** / 50 unmatched | 与上轮**一字不差**（灰块无文字，不进比对） |
| `acctview` / `acctvars` / `acctmotion` / `assetpath` / `rwd`×4 | 26 / 54 / 10 / GREEN / 全绿 | 全部持平 |
| `r25` / `r26` / `r27` / `r28` / `r29` check | 36 / 42 / 29 / 32 / 44，全 0 red | |

### ⚠ acctmodal 一度 3 红，是判据被本轮改动**激活**的旧污染

三条都长这样：`CTA is 40px rgb(167, 226, 94), want rgb(0, 86, 53)` ——
`#a7e25e` / `#9eda5b` 既不是绿也不是 lime，**是两者之间的过渡中途色**。

根因是 [[playwright-click-leaves-pointer-hovering]]：更早一次 `pg.click()` 把指针留在原地，
抽屉正好开在指针底下，而 **Playwright 认 `(hover: hover)`**。
以前 hover 只改 `opacity`，判据读的 `background-color` 纹丝不动，所以这个污染**一直存在却一直显绿**。
修在共用的 `_open()` 里加一行 `pg.mouse.move(0, 0)`，不是在三个调用点各补一次
（acctdiff 在 Task 29 修的是同一个根因、同一个位置）。

### 突变自检（一次一条，四条全部被抓到）

| 突变 | 红数 | 关键一条 |
|---|---|---|
| hover 改回 `opacity: .85` | **13** | `does not fade: want '1' got '0.85'` |
| thumb 底色加回来 | **1** | `has no CSS fill left: got rgb(217, 217, 217)` |
| 位移加回来 | **1** | `no lift: got matrix(1, 0, 0, 1, 0, -2)` |
| 去掉 `max-width` | **2** | `the field now takes most of the row: got False` |

### 文件清单

- `account.html` — 8 个灰块换 `<img>`、`?v=`
- `account-login.html` — `?v=`
- `assets/account.scss` — 五个按钮 hover + 四条 `opacity:1` 清理、三处 thumb 改 img 样式、
  social 去位移、`.gb-acct-referral__copy` 限宽、`.gb-scallop--to-green` 覆盖、`$build-acct`
- `assets/account.css` — 重编译产物
- `tools/r30check.py` — 新增
- `tools/acctcheck.py` — thumb 断言随本轮更新
- `tools/acctmodal.py` — `_open()` 补指针归位

### 顺带发现 / 未修（等拍板）

- **两个 auth 文字链接仍用 `opacity` 淡出**：`a.gb-acct-auth__aside`（Forgot your password?）
  与 `.gb-acct-auth__alt > a`（Sign up / Log in 互切）。同一条房规下**链接应当变色**——
  `.gb-acct-link` 自己的注释就写着「opacity alone reads as "fading out" rather than as a hover」。
  本轮需求点名的是**按钮**，所以没动。
- `.gb-acct-referral__hero` 的 16/9、`GIVE $20 / GET $20`、`GUMI-0000`、四个 `href="#"`
  **仍然全是自定值**，Task 29 已登记在 SPEC 8b，本轮换图不构成设计依据。
- Task 29 的三条旧遗留原样保留：九个视图仍是无条件 `[hidden]`、四处既有重复 SVG id、
  七个视图的 `rwd` 溢出扫描从未跑过。

---

## Task 29 — 交互五条：改密表单、手风琴滑动、Help 链接、账号菜单、Refer a Friend（`$build-acct` = `a24` → `20260915-a26`）

需求来自 2026-09-15 的对话（**不在 `account修改任务文档.txt` 里**，那份仍停在当天 03:53）。
四条原始条目 + 一条追加：

1. 点 Change Password 出现和 funkyfood account 点 Reset Password 一样的效果
2. `gb-acct-faq__a` 用容器包裹（可能是富文本），优化手风琴，参考其他页面或 jQuery 的 slideUp/slideDown
3. `gb-acct-help` 里的链接、邮箱都要用 `<a>`，还原样式
4. `gb-acct-menu` 写进 `gb-acct-header__link` 里，去掉它的点击效果，位置参考设计
5. （追加）Refer a Friend 参考 funkyfood 的模块做一个

### 1 · Change Password：funkyfood 的滑出表单

funkyfood 的 `[data-acct-reset-password]` 点击后**向下滑出**三字段表单
（Current / New / Confirm + Update password / Cancel），300ms 高度动画跑在一个注入的
`.acct-pwwrap` 上 —— 不是发邮件。

⚠ **与稿冲突**：板 `2284:27151` 上只有卡片和按钮，文案明写
「Click the button below and we'll send you an email with instructions **ro** reset it」
（`ro` 是稿自带的错字），而且**稿上没有任何密码字段**。
需求方 2026-09-15 裁定：**做表单，文案改成匹配的**，改后的文案标 `TODO 待客户文案`。
三个字段照搬 funkyfood 的结构，样式用 Gumi 自己的 `.gb-acct-field`。

### 2 · 手风琴：`__panel` 承高度，`__a` 承内容

⚠ **这反转了 Task 15 的判定**（交接文档 5c：「Help 的手风琴展开/收起没有高度动画 ——
用 `[hidden]` 切换，display 不能过渡。板上也没画过渡」）。

`<p class="gb-acct-faq__a">` 改成
`<div class="gb-acct-faq__panel"><div class="gb-acct-faq__a"><p>…</p></div></div>`：
`__panel` 是跑高度的盒子，`__a` 是富文本内容区（`> * + * { margin-top: 12px }`）。

**时长与曲线取自站内**：`main.js` 的站点手风琴用 `400ms` +
`cubic-bezier(0.42, 0, 0.58, 1)`，注释写明那是 jQuery `slideUp/slideDown` 的默认值与
`swing` 的近似 —— 正好是需求说的「参考其他页面或者 jq 的 slide」。account 这边用同一组值。

⚠ **没有复用 `main.js` 的 `accSlide`**：它是 `<details>` 专用的，一半代码在处理
`<details>` 的坑（`name` 要挪成 `data-acc-group`、`fill: forwards`、关闭动画期间保住
`[open]`）。account 的手风琴是 `button + aria-expanded`，这些坑一个都没有。
何况 `main.js` 是主站线的共享文件，**这条线不碰**（交接文档 §1）。

account.js 里新写了一个 `slideTo(el, apply)`：读 apply 前后的 `offsetHeight`，
在两者之间跑 Web Animations。静止高度留在 CSS 里，JS 只负责翻类。
⚠ `prefers-reduced-motion` **必须在 JS 里查**：`customstyle` 顶部那条 blanket 规则压平的是
CSS transition，**压不到 Web Animations API**。

### 3 · Help 卡：稿里这几处本来就是链接

板 `27170` 的 `characterStyleOverrides`（铁律 2 说的那个字段）：

| 文本 | 前缀 `#666666` | 链接段 `#0374a5` + UNDERLINE |
|---|---|---|
| `Email: email@email.com.au` | `Email: `（0–7）| `email@email.com.au`（7–25）|
| `Texting only: 0400 000 000` | `Texting only: `（0–14）| `0400 000 000`（14–26）|
| `visit FAQ page` | — | 整串（0–14）|

所以不是「加链接」而是**补回稿上就有的**：两处换成 `<a href="mailto:…">` / `<a href="tel:…">`，
并给 `.gb-acct-help__link` 补 `text-decoration: underline` —— 它原来写的是 `none`，
`visit FAQ page` 的下划线一直是缺的。

⚠ **这张卡出现两次**：`help` 视图和 `order`（Order Detail）视图，逐字相同，两处都改了。

### 4 · 账号菜单移进图标里

`<a class="gb-acct-header__link--account" href="account.html">` → `<div>`：
需求要去掉点击效果，而且 **`<a>` 里不能再放 `<a>`**，菜单那四项都是链接，
不改标签的话浏览器会把 DOM 拆开。

**位置**：板 `34805` 上菜单 221×184、右边缘 x=1439.9（板宽 1440，即贴视口右沿）、
顶距图标底 28（= (80−24)/2，正好是 bar 高与图标高的差的一半，所以原来的 `top: 100%` 就对）。
移进图标后定位父级从 header 变成那个 24px 的盒子，`right: 0` 会**差 120px**
（16 图标间距 + 24 汉堡 + 80 gutter），所以改成 `right: calc(-40px - var(--pad-x))`，
`--pad-x` 是 `@include container` 用的那个变量，断点自己会跟上。突变自检实测：
改回 `right: 0` 判据报 `want 0 got 120`。

⚠ **真正解决的问题是 hover 够不着**。原来菜单挂在 header 上、图标只有 24 高，
鼠标从图标往下走的那 28px 空隙里两个 `:hover` 都不成立，面板会在你伸手的过程中淡掉。
现在图标盒子 `align-self: stretch` 撑满 bar 高（`__icons` 也跟着 stretch，
且要先 `height: auto` 放开基类的 24，否则 stretch 不生效），空隙落在 hover 区内。
图标仍是 24（`svg { height: 24px }` 压住基类的 `height: 100%`），
下划线 `::after` 的 `top` 从 `calc(100% + 5px)` 改成 `calc(50% + 17px)`（中心 + 12 + 5）。

### 5 · Refer a Friend（追加）

⚠ **这反转了 SPEC 决策 C 的一半**：「无稿的两项（Refer a Friend / Contact Preferences）
只在导航里、不可点」。需求方要求按 funkyfood 的模块做出来。**Contact Preferences 没动**，
仍然是 `aria-disabled`。

**稿里完全没有这一页**（连手机板都没有），所以结构照 funkyfood、数值全是我们定的：
hero 占位块（16/9，`#eeeeee`）/ GIVE $20 · GET $20 / 说明文字 / 只读 code 输入框 + Copy /
四个分享图标。**每一处都已登记**（见下）。

- 社交图标**复用 footer 那四个**，但搬进来时把 SVG 的 `id` 与 `url(#…)` 统一加了 `-refer`
  后缀 —— 两个元素同 id，第二个 `clipPath` 会解析到第一个上去
- Copy 用 `navigator.clipboard`，**回退 `execCommand`**：静态站是 `file://` 打开的，
  不是 secure context，clipboard API 在那里不可用，不回退按钮就是静默无反应
- 导航接了**三处**入口：桌面竖导航、手机页内列表卡、overview 那张卡的箭头
  （原来是 `href="#"` 的 TODO）。⚠ **汉堡面板不用改** —— 它固定四项
  （Account / Subscriptions / Details / Log Out），本来就不含 orders / password / help

### 无 JS 降级：两处新的折叠都挂在 `.acct-live` 上

密码表单和手风琴的收起状态如果直接写死，`account.js` 一挂就是「七条答案里六条永久看不到、
密码表单永远打不开」。两处的 `height: 0` 都写成 `:root.acct-live …`，
复用 Task 28 那个「脚本跑到最后一行才加的类」。判据用
`java_script_enabled=False` 锁着。

⚠ funkyfood 在同一处也是这么做的（「Collapsed state lives on the wrapper, so without
this script the form simply stays open」），不是我们自己发明的。

⚠ **但在 `account.html` 上这层门现在是空转的**：八个视图本身仍是无条件 `[hidden]`，
无 JS 时只有 overview 可达，压根走不到 help / password。这条在 Task 28 已登记为
「顺带发现 / 未修」，见下。

### 判据抓到的一个回退：`height:0` 不等于 `[hidden]`

第一轮回归 `acctcheck` 报了 7 红，其中 5 条是预期的（实现改了、判据没跟上），
**另外 2 条是真问题**：`.gb-acct-faq__a` 原本只读到 1 条文案，改造后读到 **7 条**。

原因是把 `[hidden]`（`display:none`）换成了 `height:0 + overflow:hidden` ——
后者只是**视觉上**裁掉，内容仍在无障碍树里、里面的链接仍可 Tab 到。
改密表单更严重：三个 `<input type="password">` 在表单收起时**仍能被 Tab 聚焦**，
焦点会跑到屏幕上看不见的地方。

修法：收起态补 `visibility: hidden`（它不影响 `offsetHeight`，所以 `slideTo` 照常量高），
`slideTo` 在动画期间写 inline `visibility: visible`、`onfinish` 再清掉交还给 CSS。
`r29check` 补了两条断言锁住：收起时 `visibility` 必须是 `hidden`，且
`input.focus()` 之后 `document.activeElement` **不是**它。

⚠ 顺带修掉 `acctcheck.py` 自己的一个盲点：它的 `text` 断言用
`checkVisibility()` 过滤，而**那个 API 默认不看 `visibility` 属性** ——
靠 visibility 藏起来的元素会被当成可见、贡献一个空字符串进结果。
`acctdiff.py` 在 Task 27 踩过同一个坑，`acctcheck` 一直没改。
补 `{visibilityProperty: true}` 之后回到 **849 ok / 0 red**。

### 顺带发现 / 未修（等拍板，本轮没动）

- **九个视图仍是无条件 `[hidden]`**（Task 28 就登记过）。它让本轮两处降级门形同虚设。
  要不要一并套 `.acct-live`，请示下。
- **四个重复的 SVG `id`**（`Icon_3` ×4 / `Icon_4` ×3 / `Icon_5` ×2 / `Icon_11` ×2）——
  Figma 导出残留，**本轮零新增**，且没有任何 `url(#…)` 引用它们，所以目前无害。
- **`rwd.py` 只扫得到首屏那个视图**。Task 28 给它加了 `page.html#view` 支持，本轮用上了
  （新增 `account.html#referral`），但 **subscriptions / detail / orders / order / details /
  password / help 七个视图的 14 档溢出扫描仍然从来没跑过**。要补的话把七条加进回归清单即可。
- **日历图标仍被拉伸**（Task 26 起的遗留，未点名就没动）。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | ① 改密表单 + 文案改写；② 七个 FAQ 答案套 `__panel`；③ 两个视图的 help 卡各补 mailto / tel 链接；④ 账户图标 `<a>`→`<div>`、菜单移进去；⑤ **新增 referral 视图**、两处导航激活、overview 卡箭头接上；`?v=` → a26 |
| `account-login.html` | 只有 `?v=` → a26 |
| `assets/account.scss` | `slideTo` 的两处折叠态（`.acct-live` 门控）、`.gb-acct-faq__panel`、`.gb-acct-pw*`、`.gb-acct-help__link` 补下划线、`__link--account` 撑满 bar 高 + `::after` 重定位 + 菜单 `right` 补偿、`__icons` stretch、**新增 `.gb-acct-referral__*` 一节**；`$build-acct` → a26 |
| `assets/account.css` | 编译产物（双写） |
| `assets/account.js` | **新增 `slideTo()`**（400ms/swing，reduced-motion 在 JS 里查）；`acctFaq._set` 改走 slide；**新增 `acctPw`**（滑出表单）；**新增 `acctCopy`**（clipboard + execCommand 回退）；两者进 `modules` 与 `window.gumiAcct` |
| `tools/acctview.py` | `VIEWS` +referral；`NAV_LIVE` +referral；`NAV_DEAD` 只剩 Contact Preferences，`LIST_DEAD` 清空 |
| `tools/r29check.py` | **新增**，44 条（含两条无障碍断言与一组 `java_script_enabled=False` 降级）|
| `tools/acctcheck.py` | 五处预期随实现更新（导航 dead 只剩 Contact Preferences、改密文案、help 链接）；**`text` 断言补 `checkVisibility({visibilityProperty: true})`** |

### 判据

| 判据 | 结果 | 与基线的差 |
|---|---|---|
| `tools/r29check.py`（新增） | **44 ok / 0 red** | — |
| `tools/acctview.py` | **26 ok / 0 red** | 24 → 26：新视图在 1440 / 390 各加一条路由断言 |
| `tools/acctcheck.py` | **849 ok / 0 red** | 计数与基线相同：五处预期随实现更新，增减相抵。⚠ 顺带修掉一个**竞态**——`help-open-2` 原本只等 400ms，正好等于新加的 slide 时长，收起中的那一行还没退出无障碍树就被读了，改成 700ms 后连跑三次稳定 |
| `tools/acctbp.py` | **2289 declarations / 0 red** | 2216 → 2289：referral 一节 + 两条 `visibility` |
| `tools/accthover.py` | **37 hover properties / 0 red** | 35 → 37：referral 的分享图标与 Copy 按钮 |
| `tools/acctmotion.py` | **10 ok / 0 red** | 不变 |
| `tools/acctvars.py` / `assetpath.py` | 54 ok / 0 red · GREEN | 不变 |
| `tools/r25check.py` / `r26check.py` / `r27check.py` / `r28check.py` | 36 / 42 / 29 / 32 ok，0 red | 不变 |
| `tools/acctmodal.py` | **1314 ok / 0 red / 1 aborted** | 不变 |
| `tools/acctdiff.py` | **647 paired / 162 differ / 50 unmatched** | 166 → **162**，逐条归因：`Refer a Friend` 从 `aria-disabled` 的灰 `#808080` 变回正常色，与稿一致了 —— 桌面两块板各 1 条、手机两块板各 1 条。剩下的 `Contact Preferences colour #1a1a1a->#808080` ×2 是同类差异的对照（它仍然 disabled），正好佐证这个归因。非 footer 的差异现在共 6 条，其余 156 条全是 footer（SPEC F）|
| `tools/rwd.py` ×4（新增 `account.html#referral`） | 四条全绿 | |

**活性自检**（逐条突变，每条都单独跑）：

| 突变 | 判据反应 |
|---|---|
| 去掉 `.acct-live` 门控 | 无 JS 降级 1 红 |
| 图标盒子不再撑满 bar 高 | `want 80 got 24` |
| 菜单 `right` 改回 `0` | `want 0 got 120` |
| 去掉收起态的 `visibility: hidden` | **4 红**：面板 `visible`、输入框**能被 focus**、一次读出 7 条答案 |

### 上线前必须替换 / 待设计方裁决（referral 全页）

**这一页没有任何设计依据**，下列每一项都要设计方回话：

- 占位内容：`GUMI-0000`（示例 code，没有 referral 后端）、hero 灰块、
  四个分享按钮的 `href="#"`、`GIVE $20 / GET $20` 与说明文字（沿用 overview 卡的 $20 口径）
- 自定数值：hero 16/9 与 `#eeeeee`、金额字号 20/28/800（手机 18）、
  区块间距 8、分享图标 32 与 16 间距、hover 的 `translateY(-2px)` + `$c-green-900`
- ⚠ **没有复用 `images/refer-friends.jpg`** —— 那张图里有第三方品牌 logo（SPEC 8b），
  一卡一图的规矩也不允许拿它冒充第二处用图

---

## Task 28 — 登录与注册合成一页（`$build-acct` = `a22` → `20260915-a24`）

需求来自 2026-09-15 的对话（**不在 `account修改任务文档.txt` 里**，那份仍停在当天 03:53 的
Task 27 那版）：「login 页面和 sign up 页面需要放在一个页面中，在内部点击 sign up 和 login
链接互相切换」。

### 做法：复用 account.html 的视图机制，不新写切换器

两页的 diff 只有 52 行，差异**全在** `<main class="gb-acct-auth">` 之内（标题 / 副标题 /
字段 / 提交按钮 / alt 行），header、footer、head 几乎逐字相同。所以把 signup 的 `<main>`
整块搬进 login 页，两个 `<main>` 各挂一个 `data-acct-view`，交给 `account.js` 已有的 `view`
模块管 —— hash 路由、`[hidden]` 互斥、`is-current`、入场动画全是白得的。

**保留 `account-login.html` 作为合并页**（需求方选的），`account-signup.html` 删除。
站内**没有任何其他页面链向这两页**（只有彼此互链一次），所以删掉零成本。

两条 alt 链接从 `href="account-signup.html"` / `href="account-login.html"` 改成
`href="#signup"` / `href="#login"` + `data-acct-goto`，由 `view` 的 click 委托接管。

### 三个会静默失效的地方

**1 · `.gb-acct-auth` 有 `display: flex`，压过 UA 的 `[hidden]{display:none}`**

不补 `&[hidden] { display: none; }` 的话**两个视图会同时显示**，而且所有断言照样全绿
（`querySelector` 取第一个，读到的就是 login 那份）。项目里已有三处同样的处理
（`.gb-acct-menu` / `.gb-acct-modal__panel` / customstyle 两处），照抄了它们的写法。
突变自检证实：删掉这条规则 `r28check` 报 **5 条红**，signup 的 display 读成 `flex`。

**2 · `view.show()` 的未知 hash 回落硬编码 `'overview'`**

auth 页没有 `overview` 视图 → `show('overview')` 找不到 → 再调自己 → **无限递归爆栈**。
改成回落 `views[0]` 的名字（`overview` 本来就是 `account.html` 里第一个视图，所以对那边
零行为变化），并补 `if (!views.length) return;` 守住公开 API 被空页面调用。
⚠ 爆栈在控制台**看不见** —— `modules` 循环把每个 `init()` 包在 try/catch 里，
异常被 `console.error` 吞成一行。`r28check` 因此专门监听 `pageerror` + console error。
突变自检证实：改回硬编码后首屏两个视图都留着 `hidden`，判据在点击处超时。

**3 · 判据的选择器必须带视图前缀**

合并后 `.gb-acct-auth__title` 匹配两个元素。`acctcheck.py` 的 signup 组若不加前缀，
`text` 断言会读到 login 的文案，而 `css` 断言**会碰巧全绿**（computed style 在
`display:none` 子树里照样返回规则值）。四个 auth 组各加了自己的
`[data-acct-view="login|signup"]` 前缀（`.gb-acct-auth` 本身用同元素写法、不带空格），
页面级的 `.gb-acct-nav` / `.gb-acct-header` / `.gb-header__cta` 不加。

**4 · `hidden` 写死在 HTML 里 = 把注册入口押在 JS 上**

原来是两个独立页面，`href` 指向真文件，**没有 JS 也能注册**。合并后 signup 视图靠
`hidden` 属性藏起来，而这个属性是**无条件**的 —— `account.js` 404 或顶层抛异常，
Sign up 就**永久不可达**，而这页是创建账号的唯一入口。这是本轮改动**引入的退化**，
不是既有问题。

按铁律 12 的门控写法修：`hidden` 留在 HTML（无 JS 时不生效），CSS 规则改成
`:root.acct-live .gb-acct-auth[hidden]`，`.acct-live` 由 `account.js` **跑到最后一行**
时才加（挨着 `window.gumiAcct` 的赋值，那就是「脚本还活着」的判据）。
于是脚本挂掉 → 门不开 → 两个表单**都露出来**，都能提交。有脚本 → 类在同步脚本里加上，
**不闪**。`r28check` 用 `java_script_enabled=False` 锁住这条降级。

⚠ `account.html` 的八视图有同样的无条件 `hidden`，JS 挂掉就只剩 overview。那是既有行为、
不在本轮需求内，**没有动** —— 见下面「顺带发现 / 未修」。

### 顺带处理

- `signup` 页 header 里那条 `<!-- Placeholder for the official Trustpilot embed -->`
  是 login 页没有的，一并搬了过来
- `rwd.py` 支持 `page.html#view` 形式的参数 —— 否则 signup 视图首屏 `hidden`，
  **它的 14 档溢出扫描从此无人跑**。改动向后兼容（不带 `#` 时行为不变）
- 切换动画复用 `.gb-acct__view.is-entering` 那一套（桌面淡入上移 / ≤767 从右推入），
  在选择器列表里加 `.gb-acct-auth.is-entering`，没有新写 keyframes
- **修掉 `acctdiff.py` 一个自带的污染**：它切视图用 `pg.click()`，而 click 之后
  **鼠标停在落点上**，新视图往往正好在那里放了个按钮 —— Playwright **是认
  `(hover: hover)` 的**，于是 hover 色被当成静止色量了进去。本轮第一次跑 acctdiff
  就因此多报一条假差异（signup 的提交按钮 `#ffffff` 读成 `#004128`，那是它的 hover 色）。
  切换后补一句 `pg.mouse.move(0, 0)`。⚠ 这条影响**所有靠 click 切视图的板**
  （account.html 的 subscriptions / detail / orders…），不只是 auth

### 文件清单

| 文件 | 改动 |
|---|---|
| `account-login.html` | signup 的 `<main>` 并入，两个 `<main>` 各挂 `data-acct-view`（signup 带 `hidden`）；两条 alt 链接改 `#hash` + `data-acct-goto`；补 Trustpilot 注释；`?v=` → a23 |
| `account-signup.html` | **删除**（内容已并入，站内零引用） |
| `account.html` | 只有 `?v=` → a23（`account.js` / `account.css` 都动了） |
| `assets/account.scss` | `.gb-acct-auth` 补 `:root.acct-live &[hidden]{display:none}`（门控见上文第 4 条）；`.gb-acct-auth.is-entering` 加进两处入场动画的选择器列表；`$build-acct` → `20260915-a23` |
| `assets/account.css` | 编译产物（双写） |
| `assets/account.js` | `view.show()` 未知 hash 回落 `views[0]` 而非硬编码 `'overview'`，补空集守卫；末尾加 `.acct-live` 存活标记 |
| `tools/acctcheck.py` | 两个 signup 组的 key 改成 `("account-login.html", w, GOTO_SIGNUP)`；四组选择器加视图前缀；每组补一条「另一个视图不可见」；新增 `GOTO_SIGNUP` 动作（**点 alt 链接**，不走 `location.hash` —— 「点链接能切」就是需求本身） |
| `tools/acctdiff.py` | signup 两块板改指合并页 + 复用已有的 view 列（`"signup"`）；切换 hook 在 auth 页取 `.gb-acct-auth__alt`（那页没有 `.gb-acct-nav` / `.gb-acct-list`）；**切换后 `pg.mouse.move(0, 0)`** 去掉 hover 污染 |
| `tools/acctmotion.py` | 删掉 `account-signup.html` 项 —— 它测的两个选择器 login 页本来就有，且同类同规则，覆盖没丢 |
| `tools/rwd.py` | 支持 `page.html#view` |
| `tools/r28check.py` | **新增**，32 条（含一组 `java_script_enabled=False` 的降级断言）|

### 判据

| 判据 | 结果 | 与基线的差 |
|---|---|---|
| `tools/r28check.py`（新增） | **30 ok / 0 red** | — |
| `tools/acctcheck.py` | **849 ok / 0 red** | 845 → 849：四个 auth 组各补一条「另一个视图不可见」 |
| `tools/acctmotion.py` | **10 ok / 0 red** | 12 → 10：`account-signup.html` 项删除 |
| `tools/acctbp.py` | **2216 declarations / 0 red** | 2215 → 2216：新增的 `display: none` |
| `tools/acctview.py` | 24 ok / 0 red | 不变（只跑 `account.html`）|
| `tools/acctvars.py` | 54 ok / 0 red | 不变 |
| `tools/accthover.py` | 35 hover properties / 0 red | 不变 |
| `tools/assetpath.py` | GREEN | 不变 |
| `tools/r25check.py` / `r26check.py` / `r27check.py` | 36 / 42 / 29 ok，0 red | 不变 |
| `tools/acctmodal.py` | **1314 ok / 0 red / 1 aborted** | 不变 |
| `tools/acctdiff.py` | **647 paired / 166 differ / 50 unmatched** | **回到基线 166**：mouse.move 修掉了本轮引入的那条假差异，而它没让别的板降下来 —— 说明 account.html 的板本来就没撞上 hover 污染 |
| `tools/rwd.py account.html` / `account-login.html` / `account-login.html#signup` | 三条全绿 | **新增第三条跑法** |

### 顺带发现 / 未修（等拍板，本轮没动）

- **`account.html` 的八视图也是无条件 `hidden`** —— `account.js` 挂掉就只剩 overview，
  其余七个视图（含 My Details / Change Password）不可达。与本轮修掉的 auth 退化是同一个
  机制，但那是 Task 3 起的既有行为、不在本轮需求内。要不要一并套 `.acct-live` 门控请示下。
  ⚠ 代价不对称：auth 页挂了拿不到新客，account.html 挂了只是老客户看不到子页面。
- **`acctdiff.py` 的 hover 污染修复可能让别的板的差异数下降** —— 那些假差异一直计在
  166 的基线里。本轮之后的数字以第二轮回归为准（见下表）。

### 遗留

- **`<title>` 与 `<meta description>` 只有 Log in 那一份**，切到 signup 视图不会跟着变。
  静态站没有必要为此加 JS；Shopify 化时 `customers/login` 与 `customers/register`
  是两个 template，各自带自己的 title，这个问题自然消失。
- **Shopify 化的映射**：两个 template 各 `render` 同一个 section，用参数指定默认视图
  （`view: 'login'` / `'signup'`），不要做成一个 template 带 hash。

---

## Task 27 — 弹窗桌面尺寸、手机抽屉滑入、下拉换成站点组件（`$build-acct` = `a21` → `20260915-a22`）

`account修改任务文档.txt` 当天 03:53 又换了一版，三条。⚠ **这个文件每轮就地改写、旧内容不留痕**。

### 1 · 弹窗桌面宽高改参考 funkyfood 的 account 页

**这是反转**：2026-09-10 拍板「桌面沿用板上的 390」（SPEC 待裁决 E、MODAL-SPECS 一），本轮撤销。

funkyfood 的 account 门户量下来是两族：

| 族 | `.content` |
|---|---|
| `.delivery-*-pop-up`（frequency / information / payment / code / exclude / update / household…） | `max-width: 520`，`max-height: 100%`，radius 16（<576 是 8） |
| `.cancel-subscription-*-pop-up`（挽留链 9 屏） | `max-width: 594`，`max-height: 90vh`（<576 是 85vh） |

**统一取 520 + 90vh**，没按族分两个宽度 —— Gumi 这 20 个面板的角色分布与 funkyfood 不同，
分族会让同一个流程里的面板忽宽忽窄。要逐族对齐（cancel 那 6 个走 594）说一声。

⚠ 顺带纠正一个来源错误：Task 26 写的「720 是 funkyfood 的 portal 上限」**取错了文件** ——
720 出自 `.product-pop-up`（商品弹窗），不是 account 页。手机抽屉那条 `max-height` 随之
从 `720px` 改成 `85vh`（account 门户 <576 的真实值）。

### 2 · Edit Product 手机端改成从底部滑出

`.gb-acct-modal--sheet` 的入场 `translateY(16px)` → `translateY(100%)`，即从视口底缘整块推上来。

⚠ **改的是共享修饰类，8 个抽屉面板一起变**（edit-product / add-product / product-locked /
shipping-form / cancel 链 4 个）。需求只点名 Edit Product，但这 8 个在板上是同一个 672 贴底抽屉，
只给一个做单独的入场会变成两种抽屉。不想全改说一声。

### 3 · Edit Shipping Address

**a · Suburb 自动补全：只留注释，没做**（按需求方指示）。顺带把 funkyfood 那套查清了，
结论是**纯前端，但依赖两样 Gumi 没有的东西**，完整链路记在 SPEC 待裁决 AK。

**b · State 下拉换成站点自己的 `.gb-select`** —— 需求原话是「采用网站其他部分相同下拉」。
所以**删掉 Task 26 自建的 `acctSelect`**（account.js −4159 字符、account.scss −4 个规则块），
9 个 `<select>` 一律加 `data-select` 交给 `main.js` 的 `selectBox`（account.html 本来就引了 main.js）。
连带白得的：键盘 listbox 导航、空间不够自动上翻（`is-up`）、选中行打勾、`data-lenis-prevent`。

**「优化下拉收起效果」是这次换件的真正理由**：`acctSelect` 的收起是
`max-height: 320px → 0` 再把 `[hidden]` 加回去，`.gb-select__list` 用的是
`opacity + visibility + translateY`，`visibility 0s linear $t-base` 让它在淡出跑完后才退出命中测试。

**c · 输入框 focus 改成和全站其他页一样** —— `.gb-acct-field__input`（含 `--area`）、
`.gb-acct-field__box`、`.gb-acct-discount__input` 三处的 `outline: 2px solid $c-blue`
换成 `border-color: $c-green`，与 `customstyle.scss` 的 `.gb-field__input` 一致
（全站 `input/textarea/select` 本来就统一 `outline: none`，account 这三条是当初的例外）。

### 顺带处理

- 9 个 `<select>` 旁边那个手画的 `<svg class="gb-acct-field__icon">` **删掉了** ——
  `selectBox` 自己在按钮里画箭头，不删会出现两个。没有 JS 时的箭头改由
  `select.gb-acct-field__input` 的 `background-image` 提供（照抄 `.gb-field__input--select` 的写法）
- `.gb-acct-prod__control` 上方那段注释写着「Drawn but inert：便签 30913 说 flavour 还不能编辑」，
  Task 26 已经反转了它，注释是残的，一并改掉

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | 9 个 `<select>` 加 `data-select`、去掉 `--icon` 与同级 chevron `<svg>`；Suburb 字段加一行注释；`?v=` → a22 |
| `account-login.html` / `account-signup.html` | 只有 `?v=` → a22 |
| `assets/account.scss` | 桌面 `--acct-modal-w: 520px` + `max-height: 90vh`（删掉 752 那条 media）；sheet 入场 `translateY(100%)`、cap 改 85vh；删 `[data-acct-select]` 与 4 个 `.gb-acct-select__*` 块，换成 2 条 `.gb-select` 适配规则；`select.gb-acct-field__input` 补 no-JS 箭头；3 处 focus 改绿边；`$build-acct` → `20260915-a22` |
| `assets/account.css` | 编译产物（双写） |
| `assets/account.js` | 删 `acctSelect` 模块（−4159 字符），从 `modules` 与 `window.gumiAcct` 摘掉 |
| `tools/r27check.py` | **新增**，本轮 27 条 |
| `tools/r26check.py` | 选择器 `.gb-acct-select__*` → `.gb-select__*`；「面板封顶 720」改成「手机抽屉封顶 85vh」，并注明来源被 r27 换掉 |
| `tools/acctmodal.py` | 面板宽断言改成「手机 390 / 桌面 520」；chevron 两种结构都认；`shipping-current` 的截断拆成声明 + 真生效两条；`optPicker` 选择器同步 |
| `tools/acctdiff.py` | `checkVisibility({visibilityProperty: true})` —— 修掉 Task 25 起多报的 9 条 |
| `docs/account/SPEC.md` | 待裁决 E 标记**已定**（并写明反转）；V 补展开态来源；**新增 AK**（Suburb 自动补全的完整链路与前置条件） |
| `docs/account/MODAL-SPECS.md` | 一、桌面尺寸裁决改写；抽屉行补入场方式 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/r27check.py`（新增） | **29 ok / 0 red** |
| `tools/acctmodal.py` | **1314 ok / 0 red / 1 aborted**（1313 → 1314：截断那条拆成「声明」+「在 390 下真生效」两条）|
| `tools/acctcheck.py` / `acctview.py` | 845 / 24 ok，0 red |
| `tools/r25check.py` / `r26check.py` | 36 / 42 ok，0 red |
| `tools/acctbp.py` / `accthover.py` / `acctmotion.py` / `acctvars.py` | 2215 decl · 35 hover · 12 · 54，全 0 red |
| `tools/assetpath.py` / `rwd.py` ×3 | GREEN / 全绿 |
| `tools/acctdiff.py` | **647 paired / 166 differ / 50 unmatched**（基线从 168 改成 166，见下）|

活性自检（改回去必须转红）：

| 回退 | 结果 |
|---|---|
| `--acct-modal-w` 520 → 390 | `desktop panel is 520 wide` 转红 ✅ |
| sheet `translateY(100%)` → `16px` | `phone drawer starts fully off-screen` + `it is not the old 16px nudge` 转红 ✅ |
| 输入框 focus 绿边去掉 | `input focus: green border like every other page` 转红 ✅ |

### acctmodal 的 11 红全是判据的期望值过期，不是实现 bug

- **6 条「panel 520px wide, want the board's 390」** —— 守着 2026-09-10 的裁决，本轮反转了。
  改成「≤767 要 390，≥768 要 520」，**保留断言不删**，桌面改回 390 仍会红。
- **4 条 chevron 找不到** —— 它从 `select` 的同级 `.gb-acct-field__icon` 搬进了
  `.gb-select__button` 里的 `.gb-select__arrow`。选择器改成两种都认，**「一个 chevron 都没有」仍会红**。
- **1 条 `shipping-current` 的配送行没被截断** —— 这是**面板变宽的直接结果**：520 下那行放得下了。
  拆成两条：截断**声明**（`nowrap + ellipsis`）两个宽度都查，**真的在截**只在板自己的 390 下查。

### ⚠ 顺带查出：`acctdiff` 从 Task 25 起一直多报 9 条

`checkVisibility()` **默认不看 `visibility`**，而 Task 25 的账号 hover 菜单正是靠
`visibility: hidden` + 保留 `display` 来做淡出的（[[hidden-attr-vs-author-display]] 那一招）。
于是那个对用户完全不可见的面板被当成可见文本量了进去，`My Subscriptions` / `My Details`
凭空多出 9 条差异。判据补上 `{visibilityProperty: true}` 后 **177 → 166**
（9 条是 Task 25 引入的，另有 2 条从更早就错了）。**基线改成 166。**

### 遗留

- **`.gb-select__list` 的投影是站点的**（`0 4px 12px` + 1px 描边），不是 account 板上那种
  `0 10.29px 8px` 纯投影。展开态本来就无稿（待裁决 V），按「与站内一致」处理
- **funkyfood 那两族 520 / 594 我们合并成了 520**，要逐族对齐请回一句
- **`.gb-acct-field__icon` 里的日历图标仍被拉伸**（`15×16.667` 的 art 进 20×20 的框）。
  与 Task 26 修掉的 chevron 同一个根因，两轮需求都没点名，按「顺带发现不擅自修」继续留着
- Flavour / Size 的选项仍是占位（`Flavour option 1/2/3`），板上一个都没有

---

## Task 26 — 交互六条 + 撤回 Task 25 的弹窗链（`$build-acct` = `a20` → `20260915-a21`）

`account修改任务文档.txt` 当天 03:31 又换了一版，六条。⚠ **这个文件每轮就地改写、旧内容不留痕**。

### ⚠ 第 2 条是撤回

需求方原话：「之前的逻辑搞错了……是我看错了，应该还原之前的逻辑」。撤掉 Task 25 req 9 建的
`edit-date → need-now → edit-frequency`，两个 save 回到普通 save（按仍然有效的 Task 25 req 8，
点了关闭弹窗）。**flatpickr 日历不撤** —— 第 2 条只说链式看错了，没提日历。
现在全页只剩两条真链式：`shipping-form → shipping-success`（在 form 的 `data-acct-modal-next` 上）
与 `cancel-offer-skip → cancel-skipped`。`r26check.py` 第一段锁住这个撤回，防止再被加回来。

### 其余五条

**1 · 3 下拉改 ul/li** —— 新模块 `acctSelect`：从现有 `<select>` 生成按钮 + `ul`，
原生控件留在 DOM 里继续持有值（acctForm 的脏值门控、表单、判据读的都是它），**没 JS 时原生控件照常可用**。
`.gb-acct-prod__select` 那两个 `aria-disabled` 的 div 换成真 `<select>` ——
⚠ **这反转了便签 30913「flavour 暂不可编辑」**，是需求方 2026-09-15 的指示。
选项是占位（`Flavour option 1/2/3`），板上一个都没有，已登记待裁决。

**4 两个图标都在被拉伸** —— 减号的 `viewBox` 是从整板裁下来的 `14×2`，
CSS 的 `svg{width:14px;height:14px}` 把它**纵向拉了 7 倍**；加号是 `11.6667` 见方，
两者根本不在同一坐标系。chevron 同样：`10×5` 的 art 塞进 20×20 的框，高度翻倍。
全部统一到方形 viewBox 重绘。链接 hover 从 `opacity: .7` 改成变色（与 `.gb-header__link` 一致）。

**5 禁用光标** —— 上一轮做了 9 处，剩下 5 处卡在 `pointer-events: none`（与 `cursor` 互斥）。
其中只有 2 处是真禁用控件（另 3 处是装饰层）。`pointer-events:none` 让元素不再是命中目标，
光标只能由**父级**提供，用 `:has()` 精确挂到直接父级上。

**6 折扣码** —— `discount-add` / `discount-applied` 两个面板、detail 的 `data-acct-discount`
状态钩子**本来就都在**，缺的只是串联：Apply 接 `data-acct-modal="discount-applied"`，
JS 同时把 detail 切到 `applied`。于是 `Add a discount code` 变 `Edit discount code`、
摘要长出 `DISCOUNTCODE` 行 —— 都是既有的 `data-discount-only` 在工作。

**3 其余** —— 缩略图从 CSS 底色换成导出的 `images/product-placeholder.png`（400×400 `#d9d9d9`，
板上本就是纯灰块）；面板高度对齐 funkyfood 的 720；数量归零触发 `product-locked` ——
那个面板**早就实现了**（`2284:33847`），一直没有触发器，这轮用既有的 `data-acct-modal` 委托接上。

### ⚠ 两次把 HTML 改坏，都是同一个根因

`for m in list(re.finditer(...))` 之后**在循环里修改同一个字符串**，第二次替换的位置偏移已经失效：

1. Flavour/Size 替换时 `.*?` 跨过了 qty 按钮，把加号按钮的标签内容整段吞掉 → `<button ... type=<div ...>`
2. Apply 加属性时切断了 input → `... value="" dat<button ...`

第 1 次让三个面板的下拉数从 7 变成 10（重复插入）。修法是**从 git 原版重建这三个面板**再一次性正确应用本轮改动，
第 2 次按 id 定位重建。判据抓到了第 1 处（`all qty glyphs are 14x14` 报出混入的 `0 0 20 20`），
第 2 处靠 `html.parser` 的标签配对检查抓到。

**教训：批量替换只能整体 `re.sub`，或从后往前替换。** 收尾必须跑一次标签配对校验，
`grep -c` 数不出这种损坏。

### 判据

| 判据 | 结果 |
|---|---|
| `tools/r26check.py`（新增） | **42 ok / 0 red** |
| 结构完整性（`html.parser` 标签配对） | **0 错误 / 无未闭合** |
| 三个面板的下拉·数量·缩略图计数 | 与 git 原版**逐项一致**（7 / 6 / 6） |
| `acctmodal.py` | **1313 ok / 0 red / 1 aborted** |
| `acctcheck.py` / `acctview.py` / `r25check.py` | 845 / 24 / 36，全 0 red |
| `acctbp.py` / `accthover.py` / `acctvars.py` / `acctmotion.py` | 2276 decl · 37 hover · 54 · 12，全 0 red |
| `assetpath.py` · `rwd.py` × 三页 | GREEN · 全绿 |

⚠ **`acctmodal` 一度 6 红，全是同一条**：它守着便签 30913「Flavour 不可交互」，
而本轮需求把它改成了下拉。**这是判据的期望值被需求反转，不是实现 bug** ——
断言**反转保留**而不是删掉（改回 inert 的 div 仍会红），并补了锚点：
`not optInert` 在元素整个消失时也为真，会假绿，所以先验 `.gb-acct-select__btn` 存在。

### 文件清单

- `account.html` — 撤回链式、两类图标重绘、thumb 换图、Flavour/Size 换 select、Apply 接面板、三面板重建、`?v=`
- `assets/account.scss` — `acctSelect` 全套样式、链接 hover 变色、禁用光标挂父级、thumb 改 img、
  产品下拉尺寸档、panel 720 上限、`$build-acct`
- `assets/account.js` — 新模块 `acctSelect`；`acctForm._snapshot` 纳入数量；`acctQty` 派发 input +
  接 `product-locked`；`acctDiscount` 切 detail 状态
- `assets/account.css` — 重编译产物
- `images/product-placeholder.png` — 新增
- `tools/r26check.py` — 新增；`tools/r25check.py` — 随撤回更新
- `account-login.html` / `account-signup.html` — `?v=`

### 遗留

- **`.gb-acct-field__icon` 里的日历图标仍被拉伸**（`15×16.667` 的 art 进 20×20 的框）。
  与 chevron 同一个根因，但需求只点名了箭头，按「顺带发现不擅自修」留着。
- Flavour / Size 的选项是占位，**板上没有任何选项**，需设计方给真实清单。
- `max-height: min(720px, calc(...))` 写不得：**Sass 有自己的 `min()`**，参数含 `calc()` 时
  会静默丢掉整条声明且不报错。已改成高度阈值两条规则。

---

## Task 25 — 交互与弹窗十条（`$build-acct` = `a19` → `20260915-a20`）

`account修改任务文档.txt` 2026-09-15 换了内容：原三条（Task 23/24 已做完）替换为十条。

### 做了什么

**1 · 8 hover 与禁用态统一** —— 站点基准是 `.gb-btn`：纯变色、无位移。
account 里带位移的 hover 共四处，`link-underline` 那个 mixin **无使用者**（死代码，未动），
其余三处改成变色：`refer__action` / `intro__back` 的 `translateX` → `$c-lime` 底 + `$c-green-900` 字，
`modal__close` 去掉 `scale(1.1)` 只留变色。八处 disabled 的 `cursor: default` → `not-allowed`，
分页箭头补了一条（原来只有 `:not(:disabled)` 分支）。
⚠ `cancelled` 态那批用 `pointer-events: none` 挡点击，**加 cursor 无效**（两者互斥），未动。

**7 滚动锁与 sticky** —— 站内 `is-modal-open` 早就解决了这个冲突（锁在 `html`，`body` 用
`overflow-x: clip` 而非 `hidden`，否则 body 变成 scrollport、sticky header 当场掉出视口），
所以**没动锁机制**。只给 `.gb-acct-nav` 加 `position: sticky` + `top: calc(80px + 48px)`，
并补 **`align-self: start`** —— grid item 默认 `stretch` 会让它和行等高，sticky 永远不触发。
`.gb-acct-modal__panel` 补 **`overflow: clip`**。

⚠ 一开始写的是 `hidden`，`acctmodal` 当场炸出来：**`hidden` 会让面板变成滚动容器**，
body 里越过折线的字段就滚不到了（实测 `shipping-form` 的 suburb 在 y=740，body 可视区止于 732，
Playwright 报 `element is not visible`）。`clip` 同样裁到圆角，但不建滚动容器 ——
与站内 `body.is-modal-open` 用 `clip` 是同一个道理。

**9 Edit Date 换 flatpickr** —— 与 funkyfood 同款做法：`inline: true` + `appendTo`，
日历落在面板内，`overflow: hidden` 裁不到它。
⚠ **flatpickr 直接写 `input.value`、不派发事件**，Save 的脏值门控因此不会解锁 ——
`onChange` 里补一个 `input` 事件。链式 `edit-date → need-now → edit-frequency` 用既有的
`data-acct-modal` 委托（`cancel-offer-skip` 早有先例），`modal.open()` 本就支持换面板且不释放锁。

⚠ **flatpickr 自己会给 input 加 `readonly`**（`allowInput` 默认 false），HTML 上去掉没用，
判据的 `fill()` 当场超时 30s —— 要显式 `allowInput: true`。
frequency 的 2/4/6 weeks **本来就是对的**，未改。

**2 账户图标 hover** —— 对照 `34578`(closed) 与 `34805`(open) 两张桌面板：
常态**无**下划线，hover 才出现，并落下 4 项面板。所以原来那条常驻 lime 线是错的，改成 hover 态。
面板复用现成的 `.gb-acct-menu`（汉堡那个），它的 221 宽 / `padding-block: 4px` / 44 行高 /
`#f6feec` 底**与板逐值一致**，未改样式。触发包在 `@media (hover: hover)` 里，键盘走汉堡。

**3 · 6 视图切换动效** —— `[hidden]` 是 `display:none`，**不能过渡**，所以进入的视图播一次性动画：
桌面淡入上移、≤767 从右滑入。⚠ 动画类必须在 `animationend` 摘掉，否则 fill 状态会冻结该子树
后续所有 transition。首屏不播（`show()` 多了个 `animate` 参数）。
`.gb-acct-nav__item` 是裸 `<li>` 无样式，真正的过渡在 `__link` 上，**早就有**。

**4 订单三态** —— 三种状态的文案本来就都在 DOM 里（`<span data-state>`），由容器钩子选。
按用户「用 class 控制」改成 class / 属性**双钩子**，默认 `--shipped`。
⚠ 双钩子的代价：`acctcheck.py` 只改属性时两个状态会同时显示（当场 6 红），切换动作已同步改 class。

⚠ **给 save 加 close 时漏判了一个链式**：`shipping-form` 的下一步写在
`<form data-acct-modal-next="shipping-success">` 上，**不在按钮上**，只扫按钮属性会把它当成普通
save。加了 close 之后点 Save 直接关窗，`shipping-success` 再也到不了 —— 更糟的是
click 委托的 `preventDefault()` **绕过了浏览器原生校验**，地址填错也照关。已撤回。
现在全页 `type="submit"` + `data-acct-modal-close` 的组合为 **0**，带 `required` 的面板只有
`shipping-form` 一个且不带 close。

**5 注释清理** —— 42 条 → 9 条。留下的正是用户点名的两类：模块多状态说明、`TODO` 占位。
移走的 33 条落进 **`docs/account/NODE-MAP.md`** ——
⚠ `27680` / `27766` / `27860` / `27980` 这些区块级节点号**四份文档里一个都没有**，
只存在于 HTML 注释，直接删就永久丢了数值出处。

**10 性能** —— flatpickr 49.5KB 改**按需加载**（首次点开 Edit Date 才注入 script），
CSS 走 `media="print" onload` 异步。vendor 文件不带 `?v=`：它不会变，可以永久缓存。

### 判据

| 判据 | 结果 |
|---|---|
| `tools/r25check.py`（新增） | **41 ok / 0 red** |
| `acctcheck.py` | **845 ok / 0 red**（修判据前曾 839/6，见上） |
| `acctmodal.py` | **1313 ok / 0 red / 1 aborted**（较基线少 1：`edit-date` 高度断言改成 NOTE） |
| `acctview.py` / `acctvars.py` / `acctmotion.py` | 24 / 54 / 12 ok，全 0 red |
| `acctbp.py` / `accthover.py` | 2208 declarations · 35 hover properties，全 0 red |
| `assetpath.py` | GREEN |
| `rwd.py` × 三页 × 14 档 | 全绿 |

⚠ **三个 chromium 并发会让 `acctmodal.py` 的 `timeout=2000` 假红**（共享 VPS）。
那次点击单独复现是成功的，`elementFromPoint` 也确认无遮挡 —— 判据要单独跑。

### 文件清单

- `account.html` — hover 面板/日历挂载点/三态 class/链式属性/13 个 save 加 close/注释 42→9/`?v=` ×5
- `assets/account.scss` — nav sticky、panel overflow、三处 hover、9 处 cursor、视图动画、
  datepicker 样式、账户图标 hover 面板、`$build-acct`
- `assets/account.css` — 重编译产物
- `assets/account.js` — `acctDate` 模块（按需加载 + 事件补派发）、`view.show()` 加 `animate`、`_enter()`
- `assets/flatpickr.min.js` / `.css` — 自 funkyfood 移入
- `account-login.html` / `account-signup.html` — `?v=` ×2 各
- `tools/r25check.py` — 新增；`tools/acctcheck.py` — 状态切换同步 class
- `docs/account/NODE-MAP.md` — 新增，承接移出的 33 条注释

### 遗留

- **出场动画没做**：只有进入的视图播动画。做出场要等它播完再切，得引入状态机，本轮按最小实现。
- `cancelled` 态那批禁用元素仍靠 `pointer-events: none`，**光标提示无法生效**。要改得连挡点击的方式
  一起换（CSS 归光标、标记归挡点击），属于结构改动，未动。
- Edit Date 的日历**设计稿里不存在**（板上只有输入框），样式取自 funkyfood 的 portal，
  需设计方确认。已记进待裁决。

---

## Task 24 — 全量文本对照扫描（`$build-acct` = `a18` → `20260911-a19`）

`account修改任务文档.txt` 第三条：「需对照设计，有些细节部分没有还原设计」。
用户明确要求**再扫一遍**，不是套 §5 的桌面外推规则。

### 新判据 `tools/acctdiff.py`

把 15 张整页板的每个 TEXT 节点与页面上渲染同一串文字的元素配对，比
**font-size / line-height / letter-spacing / font-weight / colour**。只管文本 token，
几何仍归 `acctcheck.py`。弹窗的 41 张板不在内 —— `acctmodal.py` 的 1314 条已经盖住了。

```bash
python3 tools/acctdiff.py          # 15 张板
python3 tools/acctdiff.py help -u  # 只扫 help，并列出配不上的板文本
```

写这个判据时踩的四件事，都会让它**假绿或假红**：

1. **`<input>` 的文字不在子节点里** —— 填了值的在 `.value`、空的在 `@placeholder`。
   只读文本节点会把 My Details 四个预填字段全报成「实现里没有」。
2. **Figma 把一句话拆成两个 TEXT，DOM 里却是一个元素** —— `To find more info
   <a>visit FAQ page</a>`。只用 `innerText` 配不上前半句，现在两个名字都进索引。
3. **稿上的假舞台要按祖先名剔除** —— 手机板是 `Chrome browser` 实例，桌面板换成了
   Figma 的 Safari 组件，名字完全不同。
4. **同一串文字出现多次时按 y 排序配对**，两边都排。不排的话两栏布局里
   「My Subscriptions」会把 24/30 的页面标题配到 14/20 的导航项上，报出一对
   `24->14` 和 `14->24` 的假差异。

### 扫出来什么

647 配对 / 168 差异 / 50 板文本未配上。**其中 160 差异 + 36 未配是 footer** ——
稿上的 footer 是另一个组件（两栏平铺、多 `Homepage`/`PDP`/`Influencers` 三条链接、
按钮写 `Subscribe now`、链接 16/24/600/0），与现站三栏 footer 不是一回事。
这件事 SPEC 决策 2 与待裁决 F 早就登记了，`customstyle.scss` 的 `.gb-footer__link`
注释也写着「pending the designer's call」—— **不是 account 线的事，没动**。

剩下 8 条非 footer 差异，6 条是 §5 已裁决的（`Refer a Friend` 的 `aria-disabled` 灰
×4、`Sign up` 标题那处唯一的 Lexend）。

### 修了三处（都是「还原」不是「决策」）

| 处 | 稿 | 原实现 |
|---|---|---|
| `.gb-acct-schedule__title`（Renewal Schedule） | 14/20 w500 **`ls=0`** | `@include font` 漏传第 5 参数，继承了卡片的 `-0.32` |
| My Details 第一张卡的说明 | 两句 | 只有第一句，少 `All emails from us will be sent to your new address.` |
| `Must be at least 8 characters` | 桌面 `#656565` | `#808080`（`.gb-acct-auth__aside` 的基色，login 两档确实是这个） |

第三处按 SPEC **AB 既定的「各按各自的板」**办，新加 `.gb-acct-auth__aside--hint`，
只在 `panel-wide` 生效；它的手机板本来就是 `#808080`，基类不动。

⚠ **字距不是一刀切**：稿上按钮与徽章的 `letterSpacing` 是 0（`ACTIVE` ×39、`Save` ×11、
`View Order` ×6…），正文才是 -0.02em。实现原本就分得对 ——
`.gb-acct-order__cta` 写 `0`、`.gb-acct-btn` 写 `-0.32`，各自对应它们所在的板。
**只有 `schedule__title` 漏了**，别顺手把按钮那批也改了。

### 新登记待裁决 AF / AG / AH，并订正 AB

- **AB 的清单本来就不全**：`#656565` 说是三处，扫出来是**五处** ——
  漏了 `35111`(signup 副标题) 与 `35129`(`Must be at least`)。已订正。
- **AF** signup 桌面副标题 `ls=0`，同角色另外三处都有字距 → 判为稿的疏漏，按体系 -0.36
- **AG** `My Subscription` 三行 `#1a1a1a`/`#101828`/`#101828` → 统一 `#1a1a1a`
- **AH** signup 的 Email 框占位写 `Email`，同板其他字段与 login 两档都是 `Your …` → 统一 `Your email`

### 判据

| 判据 | 结果 |
|---|---|
| `acctdiff.py` | 647 paired / 168 differ（**160 为 footer，SPEC F**）/ 50 unmatched |
| `acctcheck.py` | **845 ok / 0 red**（+2：schedule 字距、My Details 两句文案） |
| `acctbp.py` / `acctvars.py` / `accthover.py` | 2172 decl · 54 ok · 33 hover / 0 red |
| `acctview.py` · `rwd.py` × 三页 | 24 ok / 0 red · 全绿 |

### 文件清单

- `tools/acctdiff.py` — 新增
- `tools/acctcheck.py` — 两条断言锁住本轮修复
- `assets/account.scss` — `schedule__title` 字距；`.gb-acct-auth__aside--hint`；`$build-acct`
- `assets/account.css` — 重编译产物
- `account.html` — 补第二句；`?v=` ×2
- `account-signup.html` — hint 修饰类；`?v=` ×2
- `account-login.html` — `?v=` ×2
- `docs/account/SPEC.md` — 订正 AB，新增 AF / AG / AH

### 遗留

- **这一轮只扫了文本 token**。间距 / 尺寸 / 圆角 / 阴影 / 图标 / 图片仍只有
  `acctcheck.py` 那 845 条逐板写死的断言覆盖，没有全自动比对。要同等程度地扫几何，
  得把 AutoLayout 的 `itemSpacing` / `padding*` 与 computed 值配对，是另一轮的量。
- footer 那 160 条**等设计方回 SPEC F**；回话前动它就会改到 MVP 11 页。

---

## Task 23 — 外壳版心化 + 波浪朝向（`$build-acct` = `a17` → `20260911-a18`）

需求来自仓库根的 `account修改任务文档.txt`（2026-09-11）。三条里做了前两条，
第三条「对照设计补细节」待需求方给范围。

### 做了什么

**1. `.gb-acct__wave` 的弧朝反了** —— `account.html` 那个波浪只写了
`gb-scallop gb-scallop--mint-to-cream`，缺 `gb-scallop--down`，渲染成 cream 向上凸。
稿（`2284:27678`，截图逐像素查过）是 **lime 向下凸进 cream**。补一个类即可，
颜色对不用动：`--wave-under` 在 `.gb-scallop` 基类就默认成 `var(--wave-fg)` = cream。

⚠ `account-login/signup` 的两个 `gb-scallop--to-green` **没动** —— 那是站点 footer 的波浪，
全站 14 处同写法，改了就跟 MVP 11 页不一致。

**2. 外壳从绝对 padding 换成版心** —— `.gb-acct__inner` 原本是
`padding: 48px 352px 144px 244px`，1440 以上内容会一直跟着视口撑开。
改成 `max-width: 952px` + `margin-inline: auto` + `padding-right: 108px`，
外层 `.gb-acct` 补 `padding-inline: var(--pad-x)`（站点同款 80/20）。

1440 档与改前**逐像素等价**，差别只在 1440 以上会锁住：

| | 改前 | 改后 |
|---|---|---|
| 内容左缘距视口 | 244 | 80 + (1280−952)/2 = **244** |
| 内容右缘距视口 | 352 | 244 + 108 = **352** |
| 内容列净宽 | 1440−244−352 = 844 | 952 − 108 = **844** |
| >1440 | 无限撑开 | 锁 952 居中 |

`@include tablet` 只剩上下与 `padding-right: fluid(0px, 108px)`，左右由 max-width 接管；
`@include narrow` 的左右 20 改由 `.gb-acct` 提供，`__inner` 自己归 0。

**3. `.gb-acct-header__bar` 换成 `@include container`** —— 与站点 `.gb-header__bar` 同写法，
>1440 时锁 1280 + gutters。原来是写死的 `padding-inline: $pad-x-desktop` 三档，没有上限。

### 踩到的一件事

给 `.gb-acct` 加了 `padding-inline` 之后，顺手给 `::before`（lime 带）和 `__wave`
补了 `calc(var(--pad-x) * -1)` 想保住满幅 —— **错的**。绝对定位子元素的包含块是
**padding box**，本来就是全宽 1440，`left: 0` 已经贴视口。补偿反而让波浪反向溢出 80px，
判据当场 19 红：4 条是 `rect` 直接量到 `-80` / `-20`，另外 15 条是
`nofit` 报 `page=80` —— 同一个根因的两种表现。撤掉补偿即全绿。

### 判据

`acctcheck.py` 新增 **`("rect", sel, edge, px)`** 断言：量元素到视口左/右的距离
（或自身宽度），±1 容差。加它的原因是这次改动**换了产生 244/352 的机制** ——
再断言 `padding-left: 244px` 就绑死在旧实现上，而需求要守的是「ink 落在哪」。
1440 档验 `.gb-acct-nav` 左缘 244 / `.gb-acct__views` 右缘 352，
390 档验内容左右 20、波浪满幅 0/0。

| 判据 | 结果 |
|---|---|
| `acctcheck.py` | **843 ok / 0 red**（基线 835 + 新增 8 条 rect） |
| `acctbp.py` | 2170 declarations / 0 red |
| `acctview.py` | 24 ok / 0 red |
| `acctvars.py` / `assetpath.py` | 54 ok · GREEN |
| `accthover.py` / `acctmotion.py` | 33 hover · 12 ok / 0 red |
| `rwd.py` × 三页 × 14 档 | 全绿 |

### 文件清单

- `account.html` — 波浪加 `--down`；`?v=` ×2
- `account-login.html` / `account-signup.html` — `?v=` ×2 各
- `assets/account.scss` — `$build-acct`；`.gb-acct` 加 `padding-inline`；
  `.gb-acct__inner` 版心化；`.gb-acct-header__bar` 换 `@include container`
- `assets/account.css` — 重编译产物
- `tools/acctcheck.py` — 新增 `rect` 断言类型 + 两组几何断言

### 遗留

- **第三条需求「对照设计补细节」没做** —— 需要需求方指明页面范围。
  既有的桌面外推结论在 `SPEC.md` §5（只有页面标题一档变），若要逐页重扫是另一轮的量。
- `account.html` 的**主站**资源版本号仍停在 `?v=20260909-r134`（6 处），
  两个 auth 页已是 `r138`。主站线的批量替换不含这三个文件，仍需 account 线自己跟。

---

## Task 16-22 — 账户区其余五页（决策 C 拍板，`$build-acct` = `20260910-a13` → `a17`）

用户 2026-09-10 定了待裁决 C：「C 需要补桌面稿，如果只有手机稿也需补桌面稿，
风格与其他桌面稿类似」。`DETAIL-STATES.md` 早就查清了这批到底是什么 ——
六个「未标注 frame」里五个是**账户区其他栏目的手机稿**，不是订阅详情的状态。

### 做了什么

`account.html` 从三视图变成**八视图**，`[data-acct-view]` 不变、hash 路由不变。
`account.js` 的 `Router.show()` 本来就是遍历实现，**新增视图零 JS 改动**。

| 视图 | 源 | 内容 |
|---|---|---|
| `orders` | `2284:27202` | 五张订单卡（三种状态）+ `Page 1 of 10` 分页 |
| `order` | `2284:27304` | 订单头 + 四条商品行 + Order Summary + 收发/支付信息 + Download Invoice |
| `details` | `2284:27081` | 三张卡的表单：Email / 姓名 / 电话 + 脏值门控的 Save |
| `password` | `2284:27151` | 一张卡：一句说明 + 一个按钮 |
| `help` | `2284:27170` | 七行手风琴 + 沙色联系卡 |

**Refer a Friend 与 Contact Preferences 没做** —— 这两项连手机稿都没有，
做了就是自造内容（全局铁律 3）。三处导航里保持 `aria-disabled`。

### 桌面外推规则（做之前先量出来的）

五张稿全是 390，桌面无稿。把三张桌面稿与各自的手机稿逐档比对，结论是
**只有页面标题一档变**：手机 `20/24 w800 ls-0.2` → 桌面 `24/30 w800 ls-0.24`，
而 `16/24` / `14/20` / `12/18` 三档两端完全相同。`.gb-acct-intro__title` 早已实现这条，
两栏 shell 也现成 —— 所以「补桌面稿」实际上不需要新写任何断点逻辑。

### 踩到的四件事

1. **类名撞车**：My Details 的表单块本来叫 `.gb-acct-form`，而 3034 行早有一个同名块
   （地址弹窗的字段列，row-gap 20）。后者在源码里更靠后，直接把新定义盖掉，
   判据当场报 `row-gap want 32px, got 20px`。改名 `.gb-acct-profile`。
   同理 `.gb-acct-order` 被 Overview 占着，订单列表那块叫 `.gb-acct-hist`。
   **新建 BEM 块前先 grep 类名**（全局铁律 4）。
2. **分页高度不是 padding 撑的**：板上 `layoutSizingVertical=FIXED`、`clipsContent=false`，
   45 是锁死的，36 的按钮居中在 45-1=44 的内容区里。照 `padding: 12px 16px` 写会得到 61。
3. **规划时按截图猜错两处**，取数后推翻：First/Last name 在手机稿是**上下堆叠**不是两栏；
   `Opt in to order updates…` 是**一行说明文字**不是 checkbox。都登记成决策 AC / AD。
4. **订单三态没有任何视觉区分**：`Shipped` / `Delivered` / `Cancelled` 全是 `#1a1a1a`，
   本来打算做的 `data-acct-order-state` 用不上了。登记成待裁决 AE。

### 判据

`acctcheck.py` **660 → 835 ok / 0 red**（+175）。新增 `tools/acctview.py`（24 ok）
专管路由：八个 hash 各自只点亮一个视图、未知 hash 回落 overview、三处导航的可达集合一致。

活性自检做了三次，都不是走过场：
- `acctbp.py` 造一处 mobile/narrow 重叠 + 一处布局阈值带数值 → **2 red**，恢复后 0；
- `acctview.py` 把 `password` 改名 `passwordX` → **6 red**，涵盖三类断言；
- 门控与单开各配一条交互断言（`DETAILS_DIRTY` / `HELP_OPEN2`）——
  只验初始态的话，「永远灰的 Save」和「只会展开、从不收起前一行的手风琴」都会全绿。

`accthover.py` 30 → 33、`acctbp.py` 1842 → 2168、`acctmodal.py` / `acctvars.py` /
`acctmotion.py` / `assetpath.py` / `rwd.py` 基线不变。

### 文件

- 修改：`account.html`、`account-login.html`、`account-signup.html`（只有 `?v=`）、
  `assets/account.scss` / `.css` / `.js`、`tools/acctcheck.py`、
  `docs/account/{PLAN,SPEC,DETAIL-STATES,HANDOFF,CHANGELOG}.md`
- 新增：`tools/acctview.py`

### 遗留

- **决策 AC / AD / AE 三条新的待裁决**（姓名两栏是外推的 / opt-in 没有勾选框 /
  订单三态无区分），全部已按暂定方案实现、一处可改。
- **Help 的手风琴文案全是占位**（`Accordion Open` / `Text here`），已进 SPEC §8b。
- **`Download Invoice` 照稿做了**，但便签 `27444` 说「Only do if very very very cheap」
  —— 待裁决 I 仍未回。
- **Refer a Friend / Contact Preferences 等稿**。

---

## Task 15 — 收尾：三条新判据、一处真漏、一条久挂的 abort（`$build-acct` = `20260910-a12`）

样式只动了一行（补一条 transition），其余全是**判据**：把 PLAN 里三条靠 `grep` 数数的
收尾检查换成能复跑、能证伪的脚本，顺带发现它们各自都会骗人。

### 三条 grep 各有各的骗法

**断点重叠（步骤 1）**：`grep '@include narrow'` 看得见 `@include narrow { ... }`，
看不见里面 `@include font($f, 24px, 800, 30px, -0.24px)` 展开出的
font-size / line-height / letter-spacing / font-weight —— 而这个文件的字号**几乎全是**
那样写的。`tools/acctbp.py` 解析 scss、展开 font mixin、按「属性 × 档位区间」比对。
⚠ 第一版还漏得更狠：它按行读，于是 `@include narrow { height: 24px; }` 这种**单行**
写法里的声明一条都没进表 —— 而单行是这个文件的主要写法。改成按 token 扫描后
声明数从 1184 涨到 1841。

**hover 配平（步骤 2）**：`grep -c ':hover'` 对 `grep -c 'transition'` 只能看出数量差，
看不出配对。逐属性比对之后又发现两种误判：
- `hover { background: $c-lime }` 配 `transition: trans(background-color)` 是**对的**
  （简写改的就是 background-color），按字面比会误报 9 条；
- hover 挂在祖先、被改的属性和它的 transition 都在后代（`.gb-acct-addr__pick` 的 hover
  改 `.gb-acct-addr__radio` 的 box-shadow），按选择器路径查会误报。

两条归一之后剩下**一条真漏**：`.gb-acct-header__logo` 的 `@include hover { opacity: .7 }`
从 Task 2 起就没有过渡 —— 正是全局铁律 13 说的「最常见的漏法」。

**reduced-motion（步骤 3）**：PLAN 让写一段 blanket 规则，**没有照写**。
`customstyle.scss` 顶部已经有 `*, *::before, *::after { ... !important }`，
account.css 在它之后加载，所有过渡本来就被压平 —— 再写一遍是死代码（铁律 22）。
改成用 `tools/acctmotion.py` 证明那条够得着，**并且两次读数**：`reduce` 下必须塌到 0，
`no-preference` 下同一批选择器必须仍有真时长。只读 reduce 一次分不出
「压平了」和「这个元素压根没有过渡」。

### `acctmodal.py` 那两条 abort：一条能解，一条本就该在

「开弹窗时页面有没有横移」从 Task 8 起一直 abort，记的是「本机测不出，欠一次真桌面浏览器」。
**这个结论是错的** —— 同一台机器上的 `tools/scrolllock.py` 一直在测真滚动条，
办法是 `launch(ignore_default_args=["--hide-scrollbars"])`：Playwright 默认带这个标志，
去掉就有真滚动条。

改的时候连着踩了三个坑：

1. **不能全宽度都去掉**。手机画的是 overlay 滚动条、不占布局宽度，强行给 390 一个经典
   滚动条等于把板宽压到 375，面板直接不开了。改成按宽度分别 launch，`>767` 才去掉。
2. **那条 else 分支自己是坏的**。它点开一个弹窗测完就走，没关；后面的 `check_forms`
   于是在「已经有面板开着」的状态下跑，`modal.open()` 不会换面板，量到的全是 `0px`。
   这个 bug 藏了很久 —— 因为那条分支从来没执行过。
3. **测点选错了，判据一直恒真**。原本测 `.gb-acct-nav` 的 `left`。滚动条在**右边**，
   锁滚动释放的是右边的宽度，左对齐的元素根本不动 —— 实测：补偿开着 0px，
   把 `--scrollbar-w` 强行改成 0 **还是 0px**。换成右对齐的 `.gb-acct-header__icons`
   的 `right` 之后，关掉补偿会稳定报 **15px**，判据这才有活性。

结果：**1314 ok / 0 red / 1 aborted**。剩下那条 `@390` 的 abort 是**预期**而非欠验证，
措辞也一并改了 —— 手机没有可释放的滚动条宽度，也就没有横移可测。

### 文件清单

| 文件 | 改动 |
|---|---|
| `tools/acctbp.py` | **新增**。断点值档互斥 + 阈值不带数值，按 token 解析、展开 font mixin |
| `tools/accthover.py` | **新增**。hover 属性逐条配对 transition，含简写归一与祖先/后代归一 |
| `tools/acctmotion.py` | **新增**。reduced-motion 覆盖，两档读数互为不变量 |
| `tools/acctmodal.py` | 桌面档去掉 `--hide-scrollbars`；补 else 分支的 Escape 收尾；横移测点换成右对齐元素；`CHROME` 改为自动发现 |
| `assets/account.scss` | `.gb-acct-header__logo` 补 `transition: trans(opacity)`（放在嵌套 `svg{}` **之前**，否则 Sass 报 mixed-decls 弃用警告） |
| `assets/account.css` | 编译产物（双写） |
| `docs/account/HANDOFF.md` | **新增**。第 5 节「不要报成 bug 的清单」分四组 |
| `docs/account/PLAN.md` | Task 15 步骤 1–7 打勾，逐条记下与原文的出入 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctcheck.py` | 660 ok / 0 red |
| `tools/acctmodal.py` | **1314 ok / 0 red / 1 aborted**（原 1313 / 2 aborted） |
| `tools/acctvars.py` | 54 ok / 0 red |
| `tools/assetpath.py` | GREEN |
| `tools/acctbp.py` | 1842 declarations / 0 red |
| `tools/accthover.py` | 30 hover properties / 0 red |
| `tools/acctmotion.py` | 12 ok / 0 red |
| `tools/rwd.py` × 三页 × 14 档 | 全绿 |
| `tools/scrolllock.py`（共用，只读） | 36 assertions / 0 failed |

三条新判据都做了突变自检：`acctbp` 造一处 mobile/narrow 同属性重叠 + 一处 stack 带数值
→ 6 条红；`accthover` 摘掉三处 transition → 5 条红（含祖先/后代那条）；
`acctmotion` 靠自带的不变量对照（no-preference 必须有真时长）。

### 遗留

- **PLAN 走到 94/95**。剩的一步是 Task 8 步骤 4（登记 `main.js` 的 `smoothScroll.PREVENT`），
  **有意未做**：改用把 `data-lenis-prevent` 写在标签上，行为等价且不必碰主站线的文件。
- ⚠ **chromium 版本那件事**见 Task 14 的遗留 —— 软链还在，重装 playwright 前要先 `rm`。
- **`account.html` 的主站 `?v=` 仍是 `r134`**，两个 auth 页是 `r138`。未统一（属主站线的节奏）。
- **待裁决已积到 A–AB**（SPEC 第 7 节），全部已按暂定方案实现、一处可改。
  最要紧的四条：A 导航条目、E 弹窗桌面稿全缺、G/Z header 用哪个、C 五个只有手机稿的页面。

---

## Task 14 — 登录与注册两页（`$build-acct` = `20260910-a12`）

**设计源**：桌面 `2284:35137` Log in / `35059` Sign up；手机 `2284:34993` / `35023`。

### 这两页用的是站点 header，不是 account header

板上的 header instance 叫 `Header Navigation Desktop/Closed` —— 与 11 个 MVP 页
**同一个组件**（Menu 下拉 + logo 居中 + 绿 `Shop now` + 人形/购物车两个图标），
不是 account 那个（logo + 人形 + 汉堡、浅绿底、汉堡开的是 account 菜单）。
未登录访客本来也没有 account 菜单可开。

所以骨架整套取自 `faq.html`（head / announcement / header / footer / cart 抽屉 / 脚本），
只有 `<main>` 是新写的；`account.css` 与 `account.js` 加在原有引用之后。
两张桌面板的 `Footer CTA` 都是 `visible=false`，跟着不做，与 `account.html` 一致。
PLAN 原写「复用 Task 1 的 header 骨架」，按源数据改了，已在 PLAN 步骤 3 划掉原文并注明。

### 字段直接复用 `.gb-acct-field`

两页的输入框在稿上就是弹窗用的同一个组件 `196:17634`（44 高 / `10 14` / 1px `#CCCCCC`
INSIDE / r8 / 16-24 `-0.32` 占位）。Task 9 建的 `.gb-acct-field` 逐值对得上，
没有再写第二套。

### 按钮没有用 `.gb-btn--lg`

站点那个类在 ≤767 会掉到 44 高 / `padding 40`（客户 r133 的决定，`.gb-crev__more`
与 header/cart 共用），而 `35016` 的手机按钮**仍是 52 高 / `12 64`**。
写成 `.gb-acct-auth__submit` 自带值，与 account 线「按钮全自写」的既有惯例一致
（`account.html` 里 `.gb-btn` 出现 0 次）。

### 桌面与手机的差异不止字号

| 项 | 桌面 | 手机 |
|---|---|---|
| 标题 | PP Palma 800 32/40 `-0.32` `#1B1C1E` | 800 24/30 `-0.24` `#011307` |
| 副标题 | 400 18/28 `-0.36`，限宽 768 | 400 16/24 `-0.32`，满宽 |
| 按钮↔alt 行↔note 卡 | 32 | **48** |
| note 卡内边距 | 24 | 16 / 20 |
| note 标题 | 500 16/24 `#1B1C1E` | **400** 14/20 `#011307` |
| Sign up 的姓名两栏 | 224 + 32 + 224 | 各占一行 |

姓名两栏那条是**布局阈值**（盒子怎么排），所以只写 `grid-template-columns`、
不带任何数值；其余全是值档，桌面基础值 + `@include tablet` 插值 + `@include narrow` 手机值，
三档互斥（全局铁律 18）。

### 判据先红过

`acctcheck.py` 原本在页面不存在时会抛 `ERR_FILE_NOT_FOUND` 把整轮跑崩 —— 那样
「先写断言、跑一次确认红」根本证明不了任何事。加了一条存在性守卫，缺页记红并继续。
顺带把写死的 `chromium-1217` 换成「取实际装着的那个」：playwright 1.58 装的是 **1208**，
1217 今天被清掉了（见下方遗留）。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account-login.html` | **新增**。骨架取自 `faq.html`，`<main class="gb-acct-auth">` 新写 |
| `account-signup.html` | **新增**。同上，多姓名两栏 |
| `assets/account.scss` | 新增 Auth 分区（排在 Views 之后、Modal 之前）；新增 `$c-gray-650`；`$build-acct` → `20260910-a12` |
| `assets/account.css` | 编译产物（双写） |
| `account.html` | 只有两处 `?v=` 跟着 bump，内容未动 |
| `tools/acctcheck.py` | 追加 Task 14 断言 119 条；新增「页面不存在 = 红」守卫；`CHROME` 改为自动发现 |
| `docs/account/SPEC.md` | 待裁决新增 Z / AA / AB；第 8 节新增四条稿件错误；8b 新增两条占位 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctcheck.py` | **660 ok / 0 red**（541 既有 + 119 新） |
| 同上，写页面之前 | 541 ok / **119 red** ✅ 先红 |
| 活性自检：11 处逐条突变（含往 login 页塞一个 `.gb-acct-nav`） | 17 条红**逐条可归因**，无一处漏网 ✅ |
| `tools/rwd.py account-login.html` / `account-signup.html` | 全绿 |
| `tools/acctvars.py` | 54 ok / 0 red |
| `tools/assetpath.py` | GREEN |
| `tools/acctmodal.py` | 1313 ok / 0 red / 2 aborted（与 Task 13 基线一致） |

活性自检的 11 处：姓名行的手机单列、inner 的手机 48 间距、标题手机墨色、`a.…__aside`
的下划线、note 卡手机内边距、按钮 52 高、表单 480 宽、副标题手机字号、
`.gb-acct-nav` 负向断言、alt 行的 `<a>`、以及把 sign-up 的提示行从 `<p>` 换成 `<a>`
（验「login 有下划线 / sign-up 没有」这个区分真的被守着）。

### 遗留

- ⚠ **`~/.cache/ms-playwright/chromium-1217` 已不存在**，playwright 1.58 期待的是
  **1208**（`browsers.json` 实测），1217 是过时残留、今天被清掉了。
  `tools/` 下**约 150 个脚本**（`rwd.py` / `acctmodal.py` / 主站线的 `r*check.py` 全在内）
  把 1217 写死在 `CHROME` / `EXE` 里，现在全都跑不起来。本轮只改了 PLAN 授权的
  `acctcheck.py`（改成扫 `chromium-*` 取最新）；其余脚本**未动**，超出本轮范围。
  为了让它们继续能跑，**留了一条软链** `~/.cache/ms-playwright/chromium-1217 -> chromium-1208`
  —— 在 `~/.cache` 里，不在仓库、不会被同步脚本推上线。**这是环境层的补丁不是修复**：
  哪天要重装 playwright，先 `rm` 掉它，否则 `playwright install` 会撞上这个名字。
  真正的修法是把那 150 处一起换成自动发现，需拍板。
- **顺带发现未修**：`account.html` 的主站资源版本号还停在 `?v=20260909-r134`，
  而 11 个 MVP 页已经是 `r138`。两个新页按 `r138` 写。主站线的批量替换看来不含
  `account.html`，这三个文件的主站 `?v=` 需要 account 线自己跟进。
- **`Forgot your password?` 是 `href="#"`** —— 稿里根本没有密码找回页（已进 SPEC 8b）。
- **两个表单都是 `action="#"`**，提交只会跳回 `#`。接 Shopify 时换成
  `customers/login` / `customers/register` 的真实 form（已进 SPEC 8b）。
- **`prefers-reduced-motion` 还没补** —— 全局收尾在 Task 15 步骤 3。
- Sign up 桌面标题的 Lexend、手机的 `Forgot you password?`、手机副标题少 `your`、
  note 卡宽 472 vs 480、`#656565` vs `#666666` —— 五条都在 SPEC 第 8 节与待裁决 Z/AA/AB，
  **不要在下一轮审计里当 bug 修回去**。

---

## Task 13 — 取消流程七屏与重启订阅（`$build-acct` = `20260910-a11`）

**设计源**：`2284:29596` 挽留 / `29767` 已跳过 / `29928`·`30286`·`30107` 原因 /
`30465` 假期日历 / `30740` 20% 挽留 / `34192` 重启。
便签 `34512` 分支规则 / `34514` 折扣叠加 / `34516` 取消数据 / `30923` 恢复日必须是完整未来日。

### 三张「原因板」是同一屏的三个选中态

`29928` 选第 1 项、`30286` 选第 2 项、`30107` 选第 3 项 —— 逐节点比对下来，
差别只有哪一个圆点是实心的，以及**脚上的按钮文案**：

| 板 | 选中项 | CTA |
|---|---|---|
| `29928` | Going away or on holiday | `Continue` |
| `30286` | Too expensive right now | `Continue` |
| `30107` | I have too much product | **`Cancel`** |

便签 `34512`（「这一项及之后没有第二屏」）就画在按钮上：**有下一屏就写 Continue，
没有就写 Cancel**。所以 `cancelFlow` 只剩一张 `BRANCH` 表，选中项同时决定按钮文案、
按钮去向、以及按下去是开下一屏还是收工。

⚠ **原因是 7 项不是 5 项**（PLAN 与 SPEC 都写少了）：末两项 `Taste or texture` /
`I purchased elsewhere` 在 `MODALS.txt` 的摘要里被截断了。

⚠ `30107` 也不只是「重复一项」：它把第 2 行的标签整个覆盖成了第 3 行的，
所以那张板既少一项又多一项。七项以 `29928`/`30286` 为准。

### 日历不能照抄

`30465` 画的是 July 2026，但 **2026-07-01 是周三，板上却排在 `Su` 列**，
而且第一行有一格写着 **`32`**。照抄等于交一个排错了的、点不动的日历。
所以日历**运行时生成**（Mo 起、真实排布），只有视觉 token 取自板：
40 的圆格、格间 4、圆角 20、`#4d4d4d` 的日期、`#005635` 白字的选中格、
`#808080` 的越月格、`#eaecf0` 的底线、20/24 的内边距。
星期头 `Mo Tu We Th Fr **Sat** Su` 照抄（只有周六是三个字母）。
选中格在板上还是 Inter（组件默认字体漏改），统一回 PP Palma、字重按板取 w500。

便签 `30923` 落地成：**今天及更早不可选，首个可选日是明天，且默认就选它**。
判据按 `new Date()` 反算同一个答案，不写死日期。

### 抽屉是定高 672，不是「最多 672」

Task 8 给 `--sheet` 写的是 `max-height: calc(100vh - 168px)`，Task 10 的三个产品屉
内容够多，一直顶到上限所以看不出来。`29767` 只有两行字，板上**照样是 672**——
五张挽留板全是 `v:FIXE`。改成 `height:`，四张短屉当场从 272/296/598/636 回到 672。

### 顺带修的两处

- **`data-acct-save-ungated` 原本是死的**：重启面板的日期输入没挂 `data-acct-field`，
  `acctForm.watch` 早一行就 return 了，豁免属性怎么删都不红。补上 `data-acct-field`
  之后这条豁免才真的在承重（`34351` 的 Save 是绿的，而 `31976` 的是灰的）。
- **Task 12 的地址单选 hover 漏了 `@media (hover:hover)`** —— 触屏点完会粘住。
  一并包进 `@include hover`。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | 填 `cancel-offer-skip` / `restart` 两个空壳，新增 `cancel-skipped`·`cancel-reason`·`cancel-holiday`·`cancel-discount` 四个面板；`?v=` → `a11` |
| `assets/account.scss` | 新增 `.gb-acct-flow` / `__lead` / `__sub` / `.gb-acct-video` / `.gb-acct-reason` 一族 / `.gb-acct-cal` 一族 / `.gb-acct-sr`；`--sheet` 的 `max-height` 改 `height` |
| `assets/account.css` | 编译产物（双写） |
| `assets/account.js` | 新增 `cancelFlow` 与 `acctCal`；`acctForm.watch` 认 `data-acct-save-ungated` |
| `images/acct-cal-prev.svg`·`acct-cal-next.svg`·`acct-play.svg` | 新增 |
| `tools/acctmodal.py` | 新增 `check_cancel` 五段（屏 / 原因 / 日历 / 链路 / 重启）；加 `_click` 守卫，控件没建好时转红而不是整轮崩掉 |
| `docs/account/SPEC.md` | 待裁决 W/X/Y；§8 补日历三错、Inter 泄漏、`30107` 真相、视频占位；§8b 补三条占位 |
| `figma/account/cut-icons.py` | 追加 3 条 JOBS。⚠ 不入库 |

### 判据

```
tools/acctmodal.py   1313 ok / 0 red / 2 aborted   （Task 12 收尾 1001）
tools/acctcheck.py    541 ok / 0 red    rwd 全绿   acctvars 54 ok   assetpath GREEN
双写一致 IN SYNC      node --check OK
活性自检 两轮 13 处突变 → 82 红：清空 BRANCH（PLAN 点名的那条）/ 日历不再按时钟门控 /
  周首改成周日 / 去掉 Save 豁免 / 选中行不再变色 / 抽屉改回 max-height /
  行描边改成 inset / 视频底色 / lead 颜色 / 挽留屏 Cancel now 改成关闭 /
  滚动条补偿去掉一次性守卫 / Sat→Sa / 日历内边距
面板高度对板：672 ×5（390×840 视口）/ 329（重启）
```

### 遗留

- **挽留屏的视频是占位**（`29751` 是纯 `#d9d9d9`、无 imageRef），上线前必须换或删。
- `Cancel now` 在第一屏是「去填原因」、后面几屏是「结束」，同词两义，待裁决 X。
- 原因屏「一个都没选」的态无稿，暂做成 CTA 灰 + 禁用，待裁决 W。
- 20% off 与暂停都只有前端动作：不真的加折扣、不真的暂停，都要后端（便签 `34514`/`34516`）。

---

## Task 12 — 配送地址弹窗与表单校验（`$build-acct` = `20260910-a10`）

**设计源**：`2284:32294` 当前地址 / `32940`·`33161` 表单 / `32779` 成功。

### 「两个表单变体」其实是一个面板

`32940` 与 `33161` 逐节点相同，只差三行数据（`12 Charnwood Road / St Kilda / 3181`
与 `20 Park Avenue / Richmond / 3121`）。所以只做一个 `shipping-form`，
判据反过来利用这一点：**要改的值全部取自另一张板**，不自造测试串。

⚠ PLAN 里说 `2284:33129` 是表单的滚动容器，**不对** —— 它浮在板外、比弹窗里那份
少一个字段（686 vs 800），是旧草稿。真正的滚动容器是 `33092`。

### 三处把卡片撑高的地方

1. **这两张卡的描边要算进盒子**。`32448` / `32932` 是同一个框，
   `strokesIncludedInLayout: true` —— `16 + 内容 + 16 + 1 + 1` 才等于板上的 178 / 78。
   和头脚的发丝线正好相反（那两条 INSIDE 但不占高，必须写 `box-shadow: inset`）。
   两处不能互抄，已写进 [MODAL-SPECS](MODAL-SPECS.md) §7。
2. **`32458` 是这批板里唯一带 `textTruncation: ENDING` + `maxLines: 1` 的文本**。
   判据是它的 `absoluteRenderBounds` 只有 240.99，而同一串在浏览器里自然宽 278.6 ——
   其余五行两边差都 <1px，所以只有这一行是被截断的。不截断，卡片就是 198 而不是 178。
   ⚠ 光加 `white-space: nowrap` 还不够：它会变成整列的**自动最小尺寸**，
   卡片被撑宽而不是把字裁掉，得在两层 flex 上补 `min-width: 0`。
3. **`SPACE_BETWEEN` 会吞掉 `itemSpacing`**。地址卡写着 gap 24，实测两个孩子之间只剩
   9.8；把 24 当真 gap 写进 CSS，文字列窄 12px，那行照样折。

### 表单

- **校验交给浏览器**：`.gb-acct-modal__panel` 本身就是 `<form>`，
  必填用 `required`、邮编用 `pattern="\d{4}"`。板上**没有错误态**，
  自画红框/提示语等于自拟视觉；原生校验还免费带键盘与读屏。
- **链到成功页挂在 `submit` 上，不是按钮的 `click`** —— 校验不过根本不会有 `submit`。
  `e.preventDefault()`，不提交到任何后端。
- **`+61` 是 29 宽的纯文字前缀，不是国家选择器**：它旁边的 chevron（`196:17798`）
  在板上 `visible=false`。因为要待在描边里，电话这一格的边框从 input 移到了
  `.gb-acct-field__box`，input 变透明无边。
- **必填星号没有自己的颜色**：`33096` 的 Label 没有 `characterStyleOverrides`，
  `*` 与标签同为 `#666666`。判据因此改成验「标签里没有第二个元素」。
- **State 用原生 `<select>`**（同 `edit-frequency`：板上只有闭合态）。
  候选项填了澳洲 8 个州的标准缩写，登记在 SPEC 待裁决 V。

### 顺带修掉的两处旧账

- **`<select>` 上没关原生箭头** —— `edit-frequency`（Task 9）一直画着两个 chevron：
  板上的那个 + 浏览器自己的。加 `select.gb-acct-field__input { appearance: none }`，
  并给两个 `<select>` 都补了断言。
- **占位符用的是浏览器默认灰**。板上三处占位（`Discount Code` / `Company` /
  `000 000 000` / `Delivery Instrctions`）全是 `#666666`，与真实值同色，补 `::placeholder`。
- **`_snapshot` 读不出单选**：单选的 `value` 是常量，变的是 `checked`。
  地址面板是第一个用单选的脏值门控，不改就永远醒不来。

### 遗留

- **桌面的成功提示折成两行**：面板宽锁 390（用户已定）而桌面内边距按卡片惯例是 24，
  内容盒比手机窄 8px，`32937` 那句正好放不下（254 → 274）。记进 SPEC 待裁决 E。
- 板上错字 `Delivery Instrctions`、同一地址两张板邮编 `3182`/`3181` 打架，已登记 SPEC §8。
- `shipping-current` 只画了一个地址却有单选钮，Save 因此恒灰；未选中态无稿。待裁决 S / U。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | `shipping-current` 填入地址卡与脚；新增 `shipping-form`（`<form>` 面板）与 `shipping-success`；`?v=` → `a10` |
| `assets/account.scss` | 新增 `.gb-acct-addr` / `.gb-acct-form` / `.gb-acct-note` 三族与 `.gb-acct-field__box`·`__prefix`·`__bare`·`__input--area`；`select.gb-acct-field__input` 关原生箭头；两处 `::placeholder`；新增 `$c-acct-radio` |
| `assets/account.css` | 编译产物（双写） |
| `assets/account.js` | `modal.init` 加 `submit` 监听；`acctForm._snapshot` 认单选 |
| `images/acct-note-ok.svg` | 新增（绿盘 + 白勾，双色，不走 currentColor 改写） |
| `tools/acctmodal.py` | 新增 `check_shipping` 三段；主循环只枚举 detail 视图里的触发器，另加「任意触发器都要有面板」的全页扫描；`check_forms` 补 `<select>` 箭头断言 |
| `docs/account/SPEC.md` | 待裁决 S/T/U/V；E 补桌面代价；§8 补两条板错 |
| `docs/account/MODAL-SPECS.md` | §7 卡片框、§8 单行截断 |
| `figma/account/cut-icons.py` | 追加 1 条 JOBS + `KEEP_STROKE`。⚠ 不入库 |

### 判据

```
tools/acctmodal.py   1001 ok / 0 red / 2 aborted   （Task 11 收尾 834）
tools/acctcheck.py    541 ok / 0 red    rwd 全绿   acctvars 54 ok   assetpath GREEN
双写一致 IN SYNC      node --check OK
活性自检 两轮 11 处突变 → 31 红：去掉单行截断 / 压平 4·8 两层 gap /
  卡片描边改成 inset / submit 不再链 / _snapshot 只读 value /
  `<select>` 放开原生箭头 / 两栏 gap 15→24 / 去掉 textarea 的 lenis /
  提示图标 gap 12→16 / 去掉 suburb 的 required
面板高度对板：394 / 254；抽屉在 390x840 视口 672
```

---

## Task 11 — 折扣码弹窗三态（`$build-acct` = `20260910-a9`）

**设计源**：`2284:31488` 空 / `31648` 已填 / `31809` 已应用；
便签 `30919` 码不存在时按钮不变绿 / `30921` 已有码时入口文案 add→edit（Task 7 已做）。

### 「已填」不是第三份 DOM

`31648` 就是 `31488` 的输入框里有东西 —— 这是静态页**唯一判得了**的事。
所以 `data-acct-discount-state` 只有 `empty` / `applied` 两个值，
中间那态由输入框的值驱动。⚠ 便签 `30919`：**Apply 变绿不代表码有效**，
码存不存在是后端的事，前端只判「有没有输入」（`trim()` 后非空，纯空格不算）。

### 两处会让面板矮掉的地方

1. **脚在板上是固定 72，哪怕里面只有一个 Cancel**（`31646`）。
   有按钮的面板 `16 + 40 + 16` 自然就是 72，但折扣弹窗的脚没有按钮，
   自然高只有 52 —— 面板整整矮 20。补 `min-height: 72px`（抽屉那档是 80），
   对已有的六个表单面板是空操作。
2. **`31962` 是两层嵌套**：label 与输入行之间 6，整个字段组与结果条之间 **8**。
   压平成一层 `row-gap: 6` 再给结果条 `margin-top: 8`，结果条会低 6px。
   照板拆成 `.gb-acct-discount__field` 内层 6 / 外层 8。

修完两个面板高度与板逐值相等：**246 / 292**。

### 做了什么

- **输入行**（`31643`）：输入框与 Apply 共用一行、间距 8。板上是 `246 + 8 + 96 = 350`；
  实现让 **Apply 保持 96 固定、输入框弹性**，所以桌面多出来的 24 gutter 从输入框身上走，
  标签不会被挤。
- **Apply**（`31645`）：`96×44`、圆角 **8** —— 是行内字段按钮，不是脚里那个 40 高的胶囊，
  单独一个类。禁用 `#e6e6e6`/`#808080`，可用 `#005635`/白。
- **已应用的结果条**（`31969`）：`#f6feec` 底 + `#daf6b0` INSIDE 描边 + 圆角 8，
  右侧是**垃圾桶**图标（`565:46772`，不是叉）。
- **结果条文案的强调是颜色不是字重**：`31972` 的底色是 `#011307`，
  而 `Discount ` 与 ` applied $35.25 off` 两段被 override 成 `#4d4d4d` ——
  **只有 `CEO90` 是深色**。实现用 `<strong>` 但 `font-weight: 400`，只换颜色。
- 脚里**只有 Cancel**，两个面板都没有 `[data-acct-save]`（判据专门验了这条）。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | 两个折扣面板填入字段组 + 结果条 + 脚；面板加 `data-acct-discount-state`；`?v=` → `a9` |
| `assets/account.scss` | 新增 `.gb-acct-discount` 一族与 `.gb-acct-chip`；`__foot` 补 `min-height: 72px`（抽屉 80） |
| `assets/account.css` | 编译产物（双写） |
| `assets/account.js` | 新增 `acctDiscount`，挂进 `window.gumiAcct.discount` |
| `images/acct-chip-remove.svg` | 新增 |
| `tools/acctmodal.py` | 追加 `check_discount`（2 面板 × 2 断点）；chip 检查从「存在」改成「可见」 |
| `figma/account/cut-icons.py` | 追加 1 条 JOBS。⚠ 不入库 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctmodal.py` | **834 ok / 0 red / 2 aborted**（Task 10 收尾 768） |
| 活性自检：Apply 不再跟随输入 / 状态不再隐藏结果条 / 去掉脚的 72 下限 | 转红 **8** ✅ |
| `tools/acctcheck.py` / `rwd.py` / `acctvars.py` / `assetpath.py` | 未回归 |
| 双写一致 | IN SYNC |
| 面板高度对板 | 246 / 292，两个都中 |

### 遗留

- **Apply 与垃圾桶都只有前端行为**：不校验码、不真的移除折扣 —— 都要后端。
- **`31809` 的输入框在板上是空的**（占位文案 `Discount Code`），Apply 也是灰的 ——
  即「码已应用、输入框已清空」。照板实现。
- `CEO90` / `$35.25` 是板上的示例值，已在 SPEC §8b 的占位清单范围内。

---

## Task 10 — 产品编辑与新增弹窗、数量门控（`$build-acct` = `20260910-a8`）

**设计源**：`2284:30960`·`31145`·`33666` edit-product / `28942`·`29200`·`29399` add-product /
`33847` product-locked；便签 `34502` 最后一个产品不能减到 0 / `34504` 减到 0 时按钮变删除 /
`30917` 多产品滚动、按钮不动 / `30913`·`30915` Flavour 暂不可编辑（待裁决 J）。

### 三个面板都是 672 抽屉，尺寸与短弹窗不同

| 项 | 短弹窗 | 产品抽屉 |
|---|---|---|
| 体的上下内边距 | 24 / 20 | **32**（板值，两端一致） |
| 脚高 | 72（16 上下） | **80（20 上下）** |
| 左右内边距 | 24 桌面 / 20 手机 | 同 |

卡片网格取自 `29095`：两列 **168**、列距 **15**、行距 **24**。板上 `168+15+168 = 351`
装在 350 的内容框里（超 1px），实现改成 `minmax(0,1fr)` 平分而不是钉死 168 ——
只有一张卡时它仍落在左列，与 `30960` 画的一致。

### 数量门控：下限按卡声明，不按卡片数推断

PLAN 给的 `acctQty` 用 `root.querySelectorAll('[data-acct-product]').length === 1`
判断「是不是最后一个」。**这个推断在本实现里是错的** —— 便签 `34502` 说的是
「**订阅里**最后一个产品」，而面板渲染几张卡是另一回事：`30960` 只画一张卡，
但它照样能减到 0（`31145` 就是那个态），因为该订阅还有别的产品。

改成每张卡自己声明 `data-acct-qty-min`：`edit-product` / `add-product` 为 `0`，
`product-locked` 为 `1`。

### 「减到 0 = 删除」是每个面板自己选的，不是自动的

第一版按便签 `34504` 让任何卡到 0 都把 CTA 换成 `Remove this product`，**判据当场报红**：
`add-product` 的四张卡本来就都是 0，而板 `28942`/`29399` 的 CTA 仍是 `Add products` ——
**选购面板里的 0 是「没选」，不是「删掉」**。改成由 CTA 上的
`data-acct-label-zero` 显式声明，只有 `edit-product` 有（对应板 `31145`）。

### 做了什么

- **`edit-product`**：一张卡（Flavour + Size 两个下拉 + 步进器，QTY 1），CTA `Save`，
  到 0 时变 `Remove this product`。
- **`add-product`**：四张卡两列（Flavour + 步进器，QTY 全 0），CTA `Add products`；
  体是滚动区（`30917`），CTA 在脚里不随之滚动。
- **`product-locked`**：`33847` 的警示条（`#fbeae9` 底、`#f6d4d2` INSIDE 描边、coral 图标、
  `Sorry!` 深色其余 `#666`）+ 一张 QTY 1 且减号已禁用的卡。**它没有自己的触发器**，
  由 `gumiAcct.modal.open('product-locked')` 打开 —— 真实站点由订阅数据决定何时出现。
- **Flavour 下拉画出来但不可交互**（待裁决 J）：`aria-disabled="true"`、不绑事件、
  也不给 hover（铁律 13 反过来同样成立：不可点的别加 hover）。
- 步进器减号到下限时**禁用**，板 `34020` 的禁用底色就是 `#faf9f8`。

### 判据自己的两个「不可能失败」的洞（都补了）

活性自检把三处守卫全删掉后**只转红 4 条**，一查是判据的问题：

1. **禁用按钮不派发 click，程序化 `.click()` 也不派发** —— `product-laked` 的减号在标签里
   就带 `disabled`，判据的「再点一下必须被拒」永远打不出去，**那条 JS 守卫从没被测过**。
   改成先摘掉 `disabled` 再点、点完还原。
2. **`bind()` 只在 init 跑一次**，所以「重开面板会不会重复绑定」怎么测都是绿的。
   改成判据自己手动再调一次 `bind()` —— 那才是守卫存在的场景。

补完后同样的 mutation 转红 **14** 条（含 `product-locked` 下限被突破、三个面板的重复绑定），
这两类之前一条都抓不到。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | edit-product / add-product 填入网格与脚；新建 product-locked 面板（含警示条）；`?v=` → `a8` |
| `assets/account.scss` | 新增 `--sheet` 的体/脚内边距覆盖、`__alert`、`.gb-acct-prod-grid`、`.gb-acct-prod` 一族、`.gb-acct-qty` 三段式步进器 |
| `assets/account.css` | 编译产物（双写） |
| `assets/account.js` | 新增 `acctQty`，`modal.init` 里对每个面板绑一次，挂进 `window.gumiAcct.qty` |
| `images/acct-qty-minus.svg`·`acct-qty-plus.svg`·`acct-opt-chevron.svg`·`acct-alert.svg` | 新增 4 个 |
| `tools/acctmodal.py` | 追加 `check_products`（3 面板 × 2 断点）；修掉上面两个洞 |
| `figma/account/cut-icons.py` | 追加 3 条 JOBS；**bbox 有一边为 0 时自动撑开 2px**（减号是纯横线，viewBox 高度为 0 会什么都不画）；`acct-alert` 那条注释掉并说明不可自动重生。⚠ 不入库 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctmodal.py` | **768 ok / 0 red / 2 aborted**（Task 9 收尾 648） |
| 活性自检：删下限守卫 / 删禁用同步 / 删重复绑定守卫 | 转红 **14** ✅ |
| `tools/acctcheck.py` / `rwd.py` / `acctvars.py` / `assetpath.py` | 未回归 |
| 双写一致 | IN SYNC |

### 稿件不一致三处（照多数实现，已登记）

| 项 | 情况 | 取法 |
|---|---|---|
| Size 下拉 | `30960`/`31145` 有，`33666`/`33847` 没有 | edit-product 取有（自己那两张板都有），product-locked 取无（自己那张板） |
| Flavour 下拉 | `28942`（4 卡）有，`29200`/`29399`（2 卡）没有 | add-product 取有 |
| CTA 在 0 时的文案 | `31145` 换成删除，`28942`/`29399` 不换 | 按面板显式声明，见上 |

### 遗留

- **PLAN 步骤 7「把滚动容器加进 `main.js` 的 `smoothScroll.PREVENT`」未做** ——
  沿用 Task 8 的做法，`data-lenis-prevent` 直接写在 `.gb-acct-modal__body` 标签上，
  行为等价且不必碰 `main.js`；判据每个面板都验了这条。
- **`product-locked` 没有触发路径**：什么时候算「最后一个产品」取决于真实订阅数据，
  静态页判断不了。面板做好了，接后端时由数据决定何时 `open()`。
- **产品缩略图是 `#d9d9d9` 空方块** —— 板 `196:19033` 本来就没有产品图（SPEC §8b 已登记）。
- **四张卡是同一件商品重复四次**，板上就是如此，属占位数据。

---

## Task 9 — 六类表单弹窗与脏值门控的保存按钮（`$build-acct` = `20260910-a7`）

**设计源**：`2284:31330` edit-name / `31976` edit-date / `32135` edit-frequency /
`32463` edit-payment / `32621` skip-next / `33350` need-now；
便签 `27446` 脏值门控 / `27448` 预填当前值 / `30925` 频率只有 2·4·6 周。
共用组件值已抽成 **`docs/account/MODAL-SPECS.md`**，Task 10–13 直接查那份。

### 桌面怎么对齐（用户 2026-09-10 拍板）

用户定：**面板宽仍用板上的 390**，字号/间距/宽度按其他有桌面稿的部分对齐。
照这条去查，发现**字号根本不用改** —— 桌面板 `2284:27792` 与手机共用同一套阶梯：

| token | 桌面 `27792` | 手机 | |
|---|---|---|---|
| 行标签 / Cancel / Edit | `14/20 w400 -0.28` | 同 | 一致 |
| 按钮 / 总计 | `16/24 w500 -0.32` | 同 | 一致 |
| 小链接 | `12/18 w400 -0.24` | 同 | 一致 |
| 页标题 | `24/30 w800 -0.24` | 20/24 | 唯一有 ramp 的 |

Task 6 那个 `1.1554` **只作用在四个日期块上**，不是全局缩放。
所以桌面唯一真正的差异是**容器内边距**，弹窗照 account 自己的卡片惯例走：

| 元素 | 桌面 | 手机 | 中间 | 对照 |
|---|---|---|---|---|
| 头/体/脚 左右 | `24` | `20` | `fluid(20px, 24px)` | `.gb-acct-sub--detail .gb-acct-sub__head` |
| 体 上下 | `24` | `20` | `fluid(20px, 24px)` | `.gb-acct-sub__body` |
| 头 上下 | `20` | `20` | — | `.gb-acct-sub__head` 两端都是 20 |
| 脚 上下 | `16` | `16` | — | 板值 |

### 一个会让每个面板都高 2px 的坑

头的分隔线与脚的分隔线在板上是 `strokeAlign: **INSIDE**` —— 1px 画在 64 / 72 **之内**。
用 CSS `border-bottom` / `border-top` 会各加 1px，**每个面板都比板高 2px**
（判据允许 ±2，正好卡在边界上蒙混过关）。改用 `box-shadow: inset 0 ∓1px 0` 复现 INSIDE 描边，
六个面板的高度这才与板逐值相等：246 / 290 / 290 / 256 / 236 / 256。

### 做了什么

- **三个表单型**（edit-name / edit-date / edit-frequency）：标签 + 44 高控件（r8、`#cccccc`
  描边、`16/24` `#666`）+ 12/18 说明行。日期与频率各带一个尾部图标，从板 SVG 按 bbox 裁出。
- **三个确认型**（edit-payment / skip-next / need-now）：只有一段 `14/20` `#666` 正文。
  正文块是板上的 **320 固定宽**（三张板一致），左对齐、右侧留 30。
- **脏值门控**（便签 `27446`）：`acctForm.watch()` 在 init 时就给每个面板上表，
  改动任一字段解锁 Save，**改回原值再次锁上**。确认型没有 `[data-acct-field]`，不受管，
  板上它们本来就是绿的可用态。
- **`disabled` 同时写在标签里**，不只靠 JS —— 脚本没加载时按钮也不该可点，且避免
  「先亮一下再变灰」。
- **skip-next 的日期用 `<strong>` 单独描粗**：板上 `17 July, 2026` 是
  `characterStyleOverrides` 里的 w500 `#011307`，不是整句样式。
  edit-frequency 的说明行同理，`2026-07-19` 是 w800，且后面跟的是 **U+2028** 不是换行 ——
  HTML 里写成 `<br>`（memory `nl2br-blind-to-u2028`）。

### 与 PLAN 不同的一处：频率用原生 `<select>`

PLAN 步骤 3 要求「用现站 `selectBox` 的视觉规格重画一份自定下拉」。**没有照做** ——
板上 `2284:32135` **只有闭合态，展开态一张稿都没有**，自画列表等于自拟视觉（铁律 2/3）。
原生 `<select>` 与闭合态逐值一致（44 高 / r8 / `#cccccc` / `16/24` `#666` / 尾部箭头），
键盘与读屏行为免费，选项按便签 `30925` 只给 2 / 4 / 6 周。
要自定 listbox，需先拿到展开态的稿，或同意照搬现站 `.gb-select` 的规格。已登记 MODAL-SPECS §6。

### 一条自检本身是无效的，已替换

PLAN 步骤 5 让「删掉 `save.disabled = true` → 行为断言必须红」。实测**没有转红** ——
因为 `disabled` 也写在标签里，删掉 JS 那行初始态照旧。**这条自检证明不了任何事。**
换成删掉真正起作用的那部分（`input` / `change` 监听器），当场转红 6 条。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | 六个面板填入 body + foot；三个字段、两个尾部图标、三段正文；`?v=` → `a7` |
| `assets/account.scss` | 头补 INSIDE 描边与 24/20 gutter；body 补内边距与 cream 底；新增 `__foot` / `__copy` / `__hint` / `__fields` / `__save` 与 `.gb-acct-field` 一族；`$build-acct` → `20260910-a7` |
| `assets/account.css` | 编译产物（双写） |
| `assets/account.js` | 新增 `acctForm`，`modal.init` 里对每个面板上表，挂进 `window.gumiAcct.form` |
| `images/acct-field-date.svg`·`acct-field-chevron.svg` | 新增 2 个 |
| `tools/acctmodal.py` | 追加 Task 9 的 `check_forms`（6 弹窗 × 2 断点）；`<select>` 走 `select_option`；字段缺失时报红而不是崩 |
| `docs/account/MODAL-SPECS.md` | 新建 —— 弹窗共用组件规格 |
| `docs/account/SPEC.md` | §8 新增 `wan to skip` 错字 |
| `figma/account/cut-icons.py` | 追加 2 条 JOBS。⚠ 不入库 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctmodal.py` | **648 ok / 0 red / 2 aborted**（Task 8 收尾是 438） |
| 活性自检 A（PLAN 版：删 `save.disabled = true`） | **没转红 → 判定此自检无效**，已替换 |
| 活性自检 B1：删掉 `input`/`change` 监听器 | 转红 **6** ✅ |
| 活性自检 B2：桌面 gutter 退回 20 | 转红 **12** ✅（390 档保持绿，正确） |
| `tools/acctcheck.py` / `rwd.py` / `acctvars.py` / `assetpath.py` | 未回归 |
| 双写一致 | IN SYNC |
| 面板高度对板 | 246 / 290 / 290 / 256 / 236 / 256，六个全中 |

### 判据自己的一个 bug（Task 8 埋的）

Task 8 的 Lenis 滚轮探针收尾时写 `body.innerHTML = ''`，**把被测面板的内容整个抹掉**，
于是后面 Task 9 的检查量到的是空壳（`edit-name` 报「面板 178px 高」）。
改成只移除探针塞进去的那个 div —— **不能用 innerHTML 还原**，那会重建节点、
让 `acctForm` 捕获的字段引用全部失效，Save 再也醒不过来。

### 遗留

- **频率下拉的展开态无稿**（见上）。
- **正文块 320 固定宽**照板实现，右侧留 30 空；若那其实是漏改，改成 350 即可。
- **表单只有前端行为**，Save 不落任何数据 —— 决策里就没有后端。
- 板上错字两处照抄并登记：`wan to skip`（`32775`）、`Restart subscoption`（`34192`）。
- `edit-name` 另有一版 `2284:33508`（值是人名 `Susanna`），详情页用的是 `31330` 那版
  （值 `My Subscription`）。人名那版属 My Details 页，不在本计划内。

---

## Task 8 — 弹窗基础设施与滚动锁（`$build-acct` = `20260910-a6`）

**设计源**：`2284:31330`（居中卡结构）、`2284:28942`（贴底抽屉）、`MODALS.txt`（13 类 / 37 态标题）。

### 弹窗有两种形态，不是一种

把 29 个 390×840 弹窗板逐个量下来，形态**只有两类**，且判据一眼可分：

| 形态 | 高 | 位置 | 圆角 | 板 |
|---|---|---|---|---|
| **居中卡** | ≤394 | `top == bottom`，全部居中 | `12` 四角 | 17 张 |
| **贴底抽屉** | `672` = 840−168 | 贴底（`bottom == 0`） | `[12,12,0,0]` 只有上两角 | 12 张 |

抽屉那批内部固定是 `64 头 + 528 体 + 80 脚`，`528` 的体是滚动区
（`MODALS.txt` 里那个 `_Scroll bar` 16×528 就是它）。两种形态的遮罩都是
`#000000` @ **0.6**（`31476`），面板都是**满 390 宽**（板宽即面板宽，手机上左右不留边）。

### 与 PLAN 的写法不同的一处：不另起一套锁

PLAN 给的是新建 `.acct-locked`，`html` 与 `body` 都上 `overflow:hidden` + 都补
`padding-right`。**实测这在本页会坏两处**，所以改成复用站内已有的 `is-modal-open`
（`customstyle.css` 本来就加载在 account 页上）：

| PLAN 写法 | 实测后果 |
|---|---|
| `body { overflow: hidden }` | **`.gb-acct-header` 是 `position: sticky`，body 变成它的 scrollport 后当场掉出视口** —— 活性自检里读到 `headerTop = -485` |
| `html` 与 `body` 都补 `padding-right` | 让出来的滚动条宽度**付两遍**，居中布局左移半个滚动条 |

站内那份 CSS 早就解了这两个（body 用 `overflow-x:clip; overflow-y:visible`，
padding 只落在 `html`），再造一份等于把同样的坑重踩一遍。
**写同一个 class 不等于调 `main.js`** —— 两个脚本仍然互不调用，决策 6 不破。
⚠ `main.js` 的 `modal` 也用这个 class 驱动 `[data-modal]`；account 页上没有任何
`[data-modal]` 触发器，两者不会同时持锁。**以后若在此页加 `[data-modal]`，先关的那个会把另一个解锁。**

### 做了什么

- **`gumiAcct.modal`**（`account.js`）：`open(name, trigger)` / `close()` / `isOpen()`。
  委托点击 `[data-acct-modal]` 开、`[data-acct-modal-close]` 与遮罩关，ESC 关，
  Tab 在面板内循环，关闭后焦点回到触发器。**同时只允许一个面板**：开第二个会先收起第一个
  且**全程不松锁**。
- **补偿只测一次**：`is-modal-open` 已在就不再测 —— 取消流程 7 屏是同一个弹窗换内容，
  第二次测量会读到 0 并把第一次的补偿抹掉。
- **解锁等淡出结束**（`--acct-modal-exit`，随 `prefers-reduced-motion` 压到 `0.01ms`）；
  被顶掉的面板留了 token 守卫，过期回调不会去解锁顶替它的那个。
- **13 个面板壳**：遮罩 + 面板 + 头（标题 + 关闭叉）+ 可滚动 body。
  标题**逐字取自板**（`MODALS.txt`），`restart` 的 `Restart subscoption` 是板上的错字，
  照抄并已登记 SPEC §8。**body 全空**，内容是 Task 9–13。
- **关闭叉** `images/acct-modal-close.svg` 从板 SVG 按 `I2284:31481;30:887` 的 bbox 裁出，
  `figma/account/cut-icons.py` 加了一条 JOBS（该脚本在 `.gitignore` 的 `figma/` 内，不入库）。

### 两个静默坑

1. **`display:flex` 压过 UA 的 `[hidden]{display:none}`** —— 面板带着 `hidden` 仍然铺满视口、
   吞掉整页点击（判据里表现为 Playwright 报「subtree intercepts pointer events」）。
   补 `.gb-acct-modal[hidden] { display: none; }`。
2. **Lenis 吃滚轮**：`main.js` 的 `smoothScroll.PREVENT` 扫描**只在 init 时跑一次**。
   本轮**没有改 `main.js`** —— 直接把 `data-lenis-prevent` 写在 `.gb-acct-modal__body`
   标签上（Lenis 在 wheel 时自己读这个属性），行为等价。判据实测：摘掉属性后
   滚轮把面板 body 滚 **0px**，加上就正常滚。

### 文件清单

| 文件 | 改动 |
|---|---|
| `assets/account.js` | 新增 `modal` 模块（焦点陷阱 / ESC / 遮罩关 / 单面板 / 一次性补偿 / token 守卫），挂进 `modules` 与 `window.gumiAcct` |
| `assets/account.scss` | 新增 Modal 一段：外层 + 遮罩 + 面板（两形态）+ 头 + 标题 + 关闭叉 + 滚动 body + reduced-motion；`$build-acct` → `20260910-a6` |
| `assets/account.css` | 编译产物（双写） |
| `account.html` | `</footer>` 后插入 13 个面板壳；`?v=` → `a6` |
| `images/acct-modal-close.svg` | 新增 |
| `tools/acctmodal.py` | 新建判据 |
| `figma/account/cut-icons.py` | 追加 1 条 JOBS。⚠ 不入库 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctmodal.py` | **438 ok / 0 red / 2 aborted** |
| 活性自检 A：`html.is-modal-open` 的 `padding-right` 打掉 | 转红 2 ✅ |
| 活性自检 B：换成 PLAN 那份锁（两边 `overflow:hidden` + 两边补 padding） | 转红 **42** ✅，其中 `sticky header top=-485` |
| 活性自检 C：摘掉 `data-lenis-prevent` | 转红 4 ✅（滚轮滚 0px） |
| `tools/acctcheck.py` | 541 ok / 0 red（未回归） |
| `tools/rwd.py` / `acctvars.py` / `assetpath.py` | 全绿 / 54 ok / GREEN |
| 双写一致 | IN SYNC |
| 关闭叉 hover + transition（Playwright 实测） | 变色 ✅ 有过渡 ✅ |

### ⚠ 两条 ABORT，不是绿也不是红

`headless chromium 画的是 overlay 滚动条，宽度恒 0`，所以**「开弹窗页面会不会横向跳」
这条真实测试在本机跑不出来**，判据**明确 abort 而不是报绿**。
CSS 机制本身用合成的 `--scrollbar-w: 15px` 验过（`html` 补到 15px、`body` 保持 0px、
第二次开不变）。**真实位移必须在有实体滚动条的桌面浏览器上人工确认一次。**

### 遗留

- **面板 body 全空**，13 个弹窗现在点开只有标题和关闭叉 —— 内容是 Task 9–13。
- **桌面弹窗宽度仍是待裁决 E**。面板暂用板上的 390 居中，
  这是**源数据里的值**不是自拟；给了宽度后只改 `--acct-modal-w` 一个变量。
- **7 个 hook 还没有触发器**（`product-locked` / `shipping-form` / `shipping-success` /
  `cancel-skipped` / `cancel-reason` / `cancel-holiday` / `cancel-discount`），
  它们由 Task 10–13 的流程内部调起，届时补面板。
- **是否把 `.gb-acct-modal__body` 登记进 `main.js` 的 `smoothScroll.PREVENT`** ——
  行为上不需要（属性已直接写在标签上），但 `font-check.html` 有探针盯着未登记的可滚容器。
  改 `main.js` 需单独授权，**未做**。

---

## Task 7 — Detail 的 PAUSED / CANCELLED / 折扣码状态（`$build-acct` = `20260909-a5`）

**设计源**：`2284:28478`（折扣码已应用）、`28627`·`28774`（PAUSED 两版）、
`34058`（CANCELLED + Restart）、`34352`（重启后转回 ACTIVE）；
便签 `34042` 暂停期不许跳过 / `34044` 超长码 / `30921` 折扣码链接文案。

### 先查清了六个「未标注 frame」的归属

PLAN 把 `27202`·`27304`·`27081`·`27116`·`27151`·`27170` 列为「疑似 Detail 的状态」。
逐节点比对文本后**全部不是** —— 它们是账户区另外五个页面的手机稿：
Order History / Order Detail / My Details（两份逐字相同）/ Change Password / Help。
结论写进 `DETAIL-STATES.md`。

**这推翻了待裁决 C 的一半**：原以为六项无稿，实际四项有手机稿，还多出一个导航里
没有的 Order Detail；真正无稿的只剩 Refer a Friend 与 Contact Preferences。
**这五个页面不在 15 个 Task 里，属于范围变化，本轮未做，等拍板。**

### 做了什么

- **状态用两个正交属性开关表达，不复制 DOM**：`data-acct-sub-state`
  （`active` / `paused` / `cancelled`）× `data-acct-discount`（`none` / `applied`）。
  两维必须正交，因为 `28774` 是「PAUSED 且有码」。元素上挂
  `data-detail-only="active paused"` 声明自己属于哪些态，CSS 隐藏其余。
  ⚠ **判据必须写成「当前态不在这个元素的列表里」** ——
  `:not([data-detail-only~="paused"])` 那样反过来写，`"active paused"` 会在两个态里都消失。
- **PAUSED**（`28627`）：徽章换色换字；续订行标签 `Next renewal date` → `Subscription restarts`
  （日期与 Est Delivery 行不动）；**`Skip next order` 整个移除**（便签 `34042`：暂停期不许跳过）。
- **CANCELLED**（`34058`）：续订行 / 折扣行 / `Cancel Subscription` 三处删除；
  两个按钮换成单个 `Restart Subscription` + 板上 298.5 宽的居中说明 + 一条分隔线；
  第一条产品行的口味位换成 coral 的 `Out of stock` 且只留单价（无划线原价）；
  **`Skip next order` 保留**（与 PAUSED 相反）。其余入口一律画成禁用态。
- **折扣码已应用**（`28478`）：Discounts 行多一段 118 宽右对齐的码，
  链接文案 `Add a discount code` → `Edit discount code`。

### 禁用态的每个值都取自 `34058`，不是自己调的灰

| 位置 | 稿上的值 | 节点 |
|---|---|---|
| 七个 `Edit` 链接 | `#808080` **fill opacity 0.4** | `34087`/`34096`/`34108`/`34121`/`34165`/`34172` |
| `Add Items` / `Skip next order` | 底 `#e6e6e6`、字 `#808080` | `34141` / `34189` |
| 四个日期块 | 字 `#808080` | `34182` / `34184` |
| 缺货那行的品名 | coral `#dd655e` **且带删除线** | `34095` |
| `Restart Subscription` | 底 `#005635`、字白 | `34078` |
| `Add a discount code` | 仍是 `#0374a5` —— 和 Restart 是仅存的两个可用项 | `34153` |

⚠ **删除线在 `characterStyleOverrides` 里，不在顶层 `style`** —— 24 个字符全部指向带
`STRIKETHROUGH` 的 style 1。只读顶层 `style` 会判成「没有删除线」。同一行的数量 `1`
（`34094`）没有 override，所以删除线只包品名、不包数量，实现里把数量放在被划的 span 之外
（`text-decoration` 会传染给行内子元素且子元素关不掉）。

⚠ **CSS 只让它们看起来、摸起来是禁用的**。将来接真数据时，同一个条件必须一并写上
`disabled` 属性，否则它们仍可聚焦、且被读屏播报成可用。

### 判据里改掉的一个假绿

`DETAIL_LONGCODE` 与 `DETAIL_DISCOUNT` 原本做的事**完全一样**（只设
`data-acct-discount=applied`），**那段 51 字符的码从没进过 DOM**。于是「超长码在 118 里
折行、不撑破」的两条 `nofit` 实际量的是 12 字符的 `DISCOUNTCODE`，怎么写都是绿的。

把 `2284:28878` 的原文 `THISISADISAVERYVERYVERYVERYVERYLONGDISCOUNTCODE1265` 注进判据后
**当场转红**：码撑破自己的 118 达 258px，390 档整页横向溢出 135px。
真因是它是**一个没有断点的 token**，作为 flex item 的自动最小尺寸取的是整串想要的 376。
修法是 `.gb-acct-summary__code` 加 `overflow-wrap: anywhere`。

修完实测与稿逐值一致：118 宽 / 折 4 行 / 小计块 `150 → 198`。
这两个几何值已钉成断言（含 `150` 的对照不变量），不是只判「没溢出」。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | detail 卡加 `data-acct-sub-state` / `data-acct-discount` 两个开关；15 处 `data-detail-only`、3 处 `data-discount-only`；新增 Restart 按钮 + 说明 + 分隔线、`Out of stock`、`Edit discount code`、折扣码 span；品名裹进 `__label` 让数量留在删除线外；`?v=` 升到 `a5`（同一文件里主线的 `r105 → r134` 是别处那轮带过来的） |
| `assets/account.scss` | 新增两组 `@each` 状态开关、`[data-acct-sub-state="cancelled"]` 禁用段、`.gb-acct-detail__restart-note`、`.gb-acct-product__stock`、`.gb-acct-summary__code`（含 `overflow-wrap: anywhere`）；`$build-acct` → `20260909-a5` |
| `assets/account.css` | 编译产物（双写） |
| `tools/acctcheck.py` | 追加 Task 7 断言 93 条；新增 `DETAIL_PAUSED` / `DETAIL_CANCELLED` / `DETAIL_DISCOUNT` / `DETAIL_LONGCODE` 四个动作；`LONGCODE` 现在真的注入 `28878` 的原文 |
| `docs/account/DETAIL-STATES.md` | 新建 —— 六个 frame 的归属、Detail 五个状态的逐项差异、四条待确认 |
| `docs/account/SPEC.md` | §7 新增待裁决 O / P / Q / R；C 补上「四项其实有稿」 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctcheck.py` | **541 ok / 0 red**（Task 6 收尾是 448） |
| 活性自检 A：摘掉 `data-acct-sub-state` 那组 `@each` | 转红 **20** ✅ |
| 活性自检 B：摘掉 `data-acct-discount` 那组 `@each` | 转红 **3** ✅ |
| 活性自检 C：摘掉 `overflow-wrap: anywhere` | 转红 **8** ✅（含两条几何值） |
| 铁律 6 配对审计：14 条 `absent` 是否都有同名正向断言 | 14/14 有 ✅ |
| `tools/rwd.py account.html` | 全绿 |
| `tools/acctvars.py` | 54 ok / 0 red |
| `tools/assetpath.py` | GREEN（`account.scss` 无 `url()`） |
| 双写一致：重编译 scss 与 `account.css` 逐字节 diff | IN SYNC |

### 已知偏差（不要报成 bug）

- **PAUSED 的续订日期实现成 `19 Jul 2026`**（跟 active 相同），因为详情稿 `28627`/`28774`
  就是这么写的。列表卡那边是 `17 Aug 2026`。便签 `34038` 站列表那边 —— **两处不一致是稿的问题**，
  已登记待裁决 P，未擅自统一。
- **`28774` 的链接文案实现成 `Edit discount code`**，但那张稿上写的是 `Add a discount code`。
  判为漏改（便签 `30921` 与 `28478` 都站 Edit 这边），已登记待裁决 Q。
- **四个状态一个桌面稿都没有**，桌面沿用基准态的字号阶梯，只有结构与文案随状态走。
  与待裁决 M 同类，已登记待裁决 R。
- **CANCELLED 没有任何 opacity 变化** —— 列表卡的 PAUSED/CANCELLED 会压到 0.4，
  详情页不会，是稿本来就这样，不是漏做。
- 说明文案里的 `bale`（应为 `able`）是稿上的错字，按稿照抄，已在 §8 登记。

### 遗留

- **Order History / Order Detail / My Details / Change Password / Help 五个页面有手机稿但不在计划里**
  —— 范围变化，等拍板。做的话还缺桌面稿。
- **`27081` 与 `27116` 文本逐字相同、高度同为 2206**，是复制未删还是有肉眼级差异（如某个 input 的
  focus 态）？已登记待裁决 O。
- **状态目前只能由判据用脚本切**，页面上没有切换入口 —— 真实站点由模板按订阅数据渲染。
  「怎么进入 PAUSED」设计方自己回的是 *we haven't finalised this yet*（阻塞项「暂停入口」）。
- 禁用态的 `disabled` 属性未加（见上方 ⚠），接后端时补。

---

## Task 6 — Subscription Detail 的 ACTIVE 基准态（`$build-acct` = `20260909-a4`）

**设计源**：桌面 `2284:27792`、手机 `2284:28330`；便签 `30905` Add items / `30913` Flavour /
`30921` 折扣码 / `27444` Download invoice。

### 做了什么

- **页头复用 `.gb-acct-intro`**，加两个修饰：`--back`（返回键在桌面也显示，`28068` 没有）
  与 `__text--row`（铅笔按钮取代副标题，桌面 gap 8 / 手机 16）。铅笔挂
  `data-acct-modal="edit-name"`。
- **卡片外壳复用 `.gb-acct-sub`**（白底 + `#e6e6e6` + r12 + head/body），因为板上
  `27865` 与列表卡 `28072` 本来就是同一个组件。唯一差别是 head 的左右内边距
  桌面 24（列表是 20），用 `.gb-acct-sub--detail` 覆盖。
- **`.gb-acct-row`** —— 图标 + 标签/值 + 可选 Edit 的通用行，四处用它：续订日期（外加
  18/26 的大号日期与一行 Est Delivery）、Frequency、Shipping、Payment Method。
  值的颜色是 `#101828`（navy），**不是列表卡用的 `#1a1a1a`**。
- **`.gb-acct-product`** ×4 —— 62 缩略图 + 「数量 名称」+ Edit + 「Flavour + 划线原价/现价」。
- **`.gb-acct-summary`** —— 小计 / 折扣（`Automatic` + `#cbf390` 标签）/ 运费 /
  `Add a discount code` / 总计。
- **`.gb-acct-schedule`** —— 四个日期块 + `Skip next order`（全站唯一的描边按钮：无填充、
  2px 深绿边、深绿字）。
- **`.gb-acct-link`** —— 蓝色带下划线的 Edit / Add a discount code / Cancel Subscription
  （`#0374a5`，`characterStyleOverrides` 里写的 `textDecoration: UNDERLINE`）。
- **11 个 `data-acct-modal` hook 全部就位**（edit-name / edit-date / need-now /
  edit-frequency / edit-product ×4 / add-product / discount-add / shipping-current /
  edit-payment / skip-next / cancel-offer-skip），Task 8 才接 JS，现在是惰性的。
- **`.gb-acct-btn` 与 Task 5 的 `.gb-acct-sub__cta` 合成一条规则**：板上它们是同一个
  Button 组件，值一模一样。列表卡的 markup 没动。

### 三处稿上才看得出来的东西

1. **桌面的四个日期块是手机块按 1.1554 缩放的**：圆角 8→9.243、描边 1→1.155、
   内边距 24/12→27.73/13.86、字号 16/24→18.49/27.73，**每一项都乘同一个系数**。
   手机那版才是组件的原值。板上那条 316 宽的日期条塞在 308 的内容列里（溢出 8），
   也是缩放的副产品 —— 实现里让四块 `flex: 1` 平分，正好铺满。
2. **产品行的框是固定 62，里面的文字列却是 68**，所以价格那行会探进下方 24 的间距里 6px。
   照板做了（`height: 62px`），不是我们算错。
3. **Payment Method 的值里是 U+2028**（行分隔符）而不是换行，`PayPal` 与邮箱各占一行 ——
   HTML 里写成 `<br>`。这类字符肉眼与普通空格无异，见 memory `nl2br-blind-to-u2028`。

### 两稿不一致一处，两套都做

桌面 `27954` 的折扣行是「Automatic + 标签」，手机 `28433` 只有标签。无便签说明，
按全局铁律 3 的第二种做法**两套都做、767 切换**，登记为待裁决 N。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | detail 视图填入页头 / 详情卡 / 四条产品行 / 小计 / 日程卡 / 取消链接；11 个 `data-acct-modal`；`?v=` 升到 `a4` |
| `assets/account.scss` | 新增 Detail / 详情行 / 蓝链 / 产品行 / 小计 / 日程六段；`.gb-acct-sub__cta` 与新的 `.gb-acct-btn` 合并成一条规则；`.gb-acct-intro--back` 与 `__text--row` 两个修饰 |
| `assets/account.css` | 编译产物（双写） |
| `tools/acctcheck.py` | 追加 Task 6 断言 134 条；新增 `GOTO_DETAIL` 动作（**走真实路径**：先点导航进列表，再点卡片 CTA）；Task 5 的文本断言补上视图作用域 |
| `images/acct-{edit-pencil,date,frequency,plus,payment}.svg` | 新增 5 个 |
| `figma/account/cut-icons.py` | 追加 5 个 JOBS。⚠ 在 `.gitignore` 的 `figma/` 内，不入库 |
| `docs/account/SPEC.md` | §7 新增待裁决 N；§8b 新增详情页的四类占位数据 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctcheck.py` | **448 ok / 0 red**（Task 5 收尾是 314） |
| 活性自检 A：去掉 `--back` 的显示规则 | 转红 1 ✅ |
| 活性自检 B：详情卡头内边距退回 20 | 转红 1 ✅ |
| 活性自检 C：去掉产品行的固定 62 高 | 转红 1 ✅（读回 68，正好是那 6px） |
| 活性自检 D：描边按钮改 1px | 转红 1 ✅ |
| 活性自检 E：**负向断言的锚**——往详情页塞一个 `__sub` | `absent` 转红 ✅（全局铁律 6） |
| 活性自检 F：拆掉列表卡 CTA 的 `data-acct-goto` | 整组 134 条转红 ✅（证明判据走的是真实点击路径，不是 hash） |
| `tools/rwd.py account.html` | 全绿 |
| 详情视图单独扫溢出（13 档，`#detail`） | 0 溢出 |
| `tools/acctvars.py` | 54 ok / 0 red |
| 肉眼对稿 | 1440 对 `2284-27792`、390 对 `2284-28330`，逐块一致 |

### 已知偏差（不要报成 bug）

- **产品行的价格会探进下方间距 6px** —— 见上文第 2 条，板上就是这样。
- **产品名固定 `max-width: 212px`**、**Flavour 行固定 217**、**变更截止提示固定 298.5** ——
  都是板上的固定宽度，去掉它们文字会拉成一行、与稿不符。
- **日期块用 `flex: 1` 而不是板上的固定 116.3 / 73**，否则手机档溢出 8px。
- **`Flavour` 是标签不是值**：板上 `27899` 的文字就是这个词，口味按便签 `30913` 暂不做。
- **Add Items 照稿做了**：便签 `30905` 说可以先关掉，是否隐藏是待裁决 H，不自己决定。
- **`Download invoice` 没做**：便签 `27444` 说「Only do if very very very cheap，
  否则删掉」，且详情稿上本来就没有这一项，待裁决 I。
- **蓝链与铅笔的 hover 用 `opacity: .7`**，交互态稿里全缺，见待裁决 K。

### 遗留

- 11 个 `data-acct-modal` 现在点了没反应 —— Task 8 建弹窗基础设施后才接上。
- 折扣行只做了 `Add a discount code` 那一版；便签 `30921` 的「已应用折扣码 → 文案变 Edit」
  是 Task 7。
- Detail 的 PAUSED / CANCELLED / 折扣已应用等其余状态是 Task 7。

---

## Task 5 — My Subscriptions 列表与三种订阅状态（`$build-acct` = `20260909-a3`）

**设计源**：桌面 `2284:28000`（同屏三态）；手机 `2284:28305`（同屏三态）、
`2284:34046`（Cancelled + Paused）；便签 `28321` paused / `28323` cancelled / `28325` +N。

### 做了什么

- **页头 `.gb-acct-intro`** —— 桌面是 `#daf6b0` 卡片（r14、pad 24/32、min-h 136、
  标题 800 24/30、副标 400 14/22 且 `max-width: 409`）；手机去掉卡片，改成
  白色圆形返回键（32、r40）+ 文字（20/24 与 12/18）。**返回键在 Overview 页是关掉的、
  在这页是开的**，同一个 `Account Header` 组件的两种用法。
- **订阅卡 `.gb-acct-sub`** —— 白底 + `#e6e6e6` 1px + r12，三段：head（pad 20、
  底边 1px）/ body（pad 24，手机 20）/ foot（pad 4-24-24，手机 8-16-20）。
  续订与配送两行桌面并排（gap 16）、手机上下堆叠。产品行固定 `max-width: 308`。
- **状态徽章 `.gb-acct-pill`** —— 24 高、r52、Inter 500 12/18 大写，左侧是一个
  16 的白盘套 11.74 的环（`border: 3.07px`）。三态取色全部来自节点：
  active `#cbf390`/`#005635`、paused `#ffefc3`/`#fd871a`、cancelled `#cccccc`/`#4d4d4d`。
  新增 `$c-amber-{100,300,500}` 三个 account-only 变量。
- **三态由 `[data-acct-sub-state]` 驱动**，选择器写在属性上而不是修饰类上，
  Task 6 的详情页可以直接复用同一个徽章。paused 把 `__summary` 压到 0.4；
  cancelled 把 `__meta` 与 `__summary` 都压到 0.4，并隐藏续订行。
- **卡片整块不可点**：稿上只有按钮可点，所以卡片没有 `cursor: pointer` 也没有 hover
  （全局铁律 13 的反面）。CTA 文案按状态取 `Manage Subscription` / `Re-Activate Subscription`。

### 顺带修正了 Task 4 的一处还原错误

**桌面浅绿带与波浪原来高了 73px**，波浪的扇贝直接横穿侧栏和问候卡。
原因是 `123` / `114` 这两个数是拿板坐标减错了基准算的：板 `27678` 的 `main` 起点在
`179.6`，矩形底在 `1043`、波浪顶在 `367`，相对 `main` 应该是 **196.4 / 187.4**。
已改成 `196` / `187`，手机档（176）本来就是对的、未动。判据补了
`.gb-acct__wave{top}` 两条，活性自检 C 验过。

同时把手机的起始留白拆开：外壳 `.gb-acct__inner` 只留板上 `Account Header` 自己的
`padding-top: 8`，剩下的归各视图 —— Overview 因为返回键是关的、文字从 40 起，
所以 `.gb-acct-ov` 补 `padding-top: 32`；Subscriptions 的返回键是开的，从 8 起。
两者相加与改动前一致，Overview 的渲染没有位移。

### 稿件两处自相矛盾，按便签 + 手机稿做

1. **CANCELLED 删错了行**：桌面 `28146` 删 Shipping、留 Renewal；便签 `28323` 写的是
   「Renewal date removed」，手机 `28316`/`34055` 也是删 Renewal。→ 隐藏续订行。
2. **PAUSED 的续订日期**：便签 `28321` 说显示「暂停到期日」，手机写 `17 Aug 2026`，
   桌面 `28109` 还留着 active 的 `19 Jul 2026`。→ 取 `17 Aug 2026`。

两条都记进 SPEC §8。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | subscriptions 视图填入 intro + 三张卡；`?v=` 升到 `a3` |
| `assets/account.scss` | 新增 My Subscriptions / 徽章 / 卡片正文三段；新增 `$c-amber-{100,300,500}`；修正 `.gb-acct::before` 与 `.gb-acct__wave` 的桌面值；`.gb-acct__inner` 手机 padding-top 40→8，`.gb-acct-ov` 补 32 |
| `assets/account.css` | 编译产物（双写） |
| `tools/acctcheck.py` | 追加 Task 5 断言 141 条；新增 `("account.html", 390, GOTO_SUBS)` 组；`GOTO_SUBS` 的触发元素改成按宽度选（手机档侧栏是 `display:none`，只能点页内列表卡） |
| `images/acct-{sub-renewal,sub-shipping,back-arrow}.svg` | 新增 3 个 |
| `figma/account/cut-icons.py` | JOBS 支持第 4 项「SVG 文件名」——三个同名桌面板导出时按真实页名重命名过，节点文件名与 SVG 文件名对不上。⚠ 仍在 `.gitignore` 的 `figma/` 内，不入库 |
| `docs/account/SPEC.md` | §8 新增两条稿件错误；§8b 新增缩略图占位与示例订阅数据 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctcheck.py` | **314 ok / 0 red**（Task 4 收尾是 173） |
| 活性自检 A：cancelled 的 `opacity: .4` 改成 1 | 转红 3 条 ✅ |
| 活性自检 B：删掉 cancelled 的 `[data-acct-sub-renewal]{display:none}` | 转红 2 条 ✅ |
| 活性自检 C：色带高度退回旧的 123 | 转红 1 条 ✅（证明这条断言真的在管色带） |
| 活性自检 D：徽章 r52 改 4 | 转红 1 条 ✅ |
| `tools/rwd.py account.html` | 全绿 |
| 订阅视图单独扫溢出（13 档，`#subscriptions`） | 0 溢出 |
| `tools/acctvars.py` | 54 ok / 0 red（新增三个 amber 只 note） |
| 肉眼对稿 | 1440 对 `2284-28000`、390 对 `2284-28305`，逐块一致 |

### 已知偏差（不要报成 bug）

- **徽章圆环的边框读回来是 `3px` 而不是 `3.07px`**：border-width 的 used value 取整数像素。
  源码里仍写 `3.07px`（节点值 3.0674），断言按取整后的值写。
- **圆环直径读回 `11.7344px`**：`11.74px` 落到 1/64 像素网格上的结果，节点值是 11.742387。
- **桌面 CANCELLED 卡比稿少一行**（隐藏了续订行、保留配送行）——见上文，是照便签做的，
  与桌面板不同是**有意的**。
- **PAUSED 卡的日期与桌面板不同**（`17 Aug` vs `19 Jul`）——同上。
- **产品缩略图是灰块**：`196:19033` 在所有板上都是纯 `#d9d9d9` 矩形，设计里就没有产品图。
- **CTA 的 hover 用 `opacity: .85`**，与 Task 4 的 `.gb-acct-order__cta` 同一套；
  返回键沿用 `.gb-acct-refer__action` 的位移写法（反向 `-2px`）。交互态稿里全缺，见待裁决 K。

### 遗留

- `Manage Subscription` 指向 `data-acct-goto="detail"`，详情视图 Task 6 才填内容，
  现在点过去是空壳。`Re-Activate Subscription` 是 `href="#"`（重启流程无稿）。
- `account.html` 里 `customstyle.css` / `main.js` 的 `?v=` 还停在 `20260908-r105`，
  而现站那条线已经滚到 `r124`。**没动**，那是另一条线的批量替换范围。

---

## Task 4 — Account Overview 视图与三种订单状态（`$build-acct` = `20260909-a2`）

**设计源**：桌面 `2284:27765`（在 `27678` 内）、手机 `2284:27604`；
三态 `2284:27450` preparing / `27499` shipped / `27548` renewal。

### 做了什么

- **问候块 `.gb-acct-hello`** —— 桌面是 `#daf6b0` 卡片（r14、pad 24/32、gap 8、
  `Hi, Susanna` 800 24/30、`Welcome back!` 400 14/22）；手机去掉卡片只剩文字（20/24 与 12/18）。
- **订单卡 `.gb-acct-order`** 三态，`data-acct-order-state` authored 在元素上，无 JS。
  preparing / shipped 深绿白字，**renewal 整个反过来**：卡底 `#cbf390`、标题变
  `#a7e746` 的标签块（r4、pad-inline 8）、正文与状态转深绿、CTA 变绿底白字且文案是
  `Manage Subscription`。
- **Refer a Friend 卡 `.gb-acct-refer`** —— `#f5f1e9` 底、圆形头像（桌面 80 / 手机 66）、
  `#cbf390` 标签、白色圆形箭头按钮（40 / 32）。
- **Logout 按钮 `.gb-acct-logout`** —— 手机专有（桌面的 Logout 在侧栏），52 高、r72、深绿底。
- **浅绿带 + 波浪** —— `.gb-acct::before` 把 header 的 `#e7f8d0` 往下延伸，底边接一个
  `.gb-scallop`（新变体 `--mint-to-cream`）。页面底色设成 `$c-cream`（`2284:27604` 的 fill），
  否则白色的列表卡组在 body 的纯白上完全看不出来。
- **问候区装饰小熊** —— lime 描边 + 旋转 18.47° 的小熊照片，裁在 113.9x145（桌面）框内，
  桌面允许它探出卡片右边 41.9。

### 三个把人绊住的地方

1. **三个 icon 槽在板上是 `visible=false`**：两个 CTA 按钮的图标与手机问候区的返回箭头。
   组件自带槽、节点 JSON 里结构完整，只有 `visible` 字段能分辨。
   **交叉验证**：Figma 导出不含隐藏节点，所以整块 board SVG 在那个位置没有 path ——
   `cut-icons.py` 报「no path inside」是**确认**不是失败。三个都没做。
2. **旋转节点的 bbox 不是画面**：小熊 `2284:27653` 记的 186.5x164 是旋转后的包围盒，
   真正的框是 188.9x145.7（桌面）。另外**不能把图居中于裁切框** —— 熊在自己的 PNG 里偏左，
   居中会露出空白的右半边；按节点坐标算出 `left: -33.5px` 才对。
3. **`img { max-width: 100% }` 会压垮它**：装饰图故意比裁切框宽，全局规则把它压回框宽，
   旋转后就转出一个扁盒子。判据里锁了 `max-width: none`。同族坑见
   memory `theme-img-rule-blows-up-unsized-img`。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | overview 视图填入 hello / order（三态槽）/ refer / logout + 顶部 `.gb-acct__wave` |
| `assets/account.scss` | 新增 Overview / 订单卡 / Refer / Logout / 装饰 / 波浪变体六段；新增 `$c-lime-300` `$c-lime-500` 两个 account-only 变量 |
| `assets/account.css` | 编译产物（双写） |
| `tools/acctcheck.py` | 追加 Task 4 断言 88 条；新增 `STATE_PREPARING` / `STATE_RENEWAL` 两个动作 |
| `images/refer-friends.{jpg,webp}` | 新增，Refer 卡头像 |
| `images/acct-bear-side.{png,webp}` | 新增，问候区装饰小熊 |
| `images/acct-{order-preparing,order-shipped,order-renewal,logout,action-arrow,bear-halo}.svg` | 新增 6 个 |
| `figma/account/make-images.py` | **新建**（位图派生）⚠ 在 `.gitignore` 的 `figma/` 内，不入库，与 `optimize-images.py` 同惯例 |
| `figma/account/cut-icons.py` | **新建**（从整块 board SVG 按节点 bbox 裁图标）同上不入库 |
| `docs/account/SPEC.md` | 待裁决新增 L / M；稿件错误新增两条；新增 §8b「上线前必须替换的占位内容」 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctcheck.py` | **173 ok / 0 red** |
| 活性自检 A：删掉 renewal 的整块状态覆盖 | 转红 7 条 ✅ |
| 活性自检 B：删掉 `[data-state]{display:none}` | 转红 7 条 ✅（三个文案槽同时显示） |
| `tools/rwd.py account.html` | 全绿 |
| `tools/acctvars.py` | 54 ok / 0 red（两个 account-only 变量只 note） |
| 三态肉眼对稿 | 390/1440 各三态截图逐个比对 `2284-27450/27499/27548`，一致 |
| 卡片尺寸实测 | 桌面 hello 571x136 / order 571x168 / refer 571x128，手机 refer 350x98 —— 与稿一致 |

⚠ **判据里读状态切换后的颜色必须等够过渡时间**：首跑 2 red 是 `rgb(19,99,68)`，
那是 `$t-base` 0.2s 走到一半的插值，不是样式错。等待已从 120ms 提到 450ms。

### 已知偏差（不要报成 bug）

- **手机订单卡 192 高，稿 188**。差 4 来自 label：稿的 TEXT bbox 记 20，但 style 的
  line-height 是 24，CSS 行盒取 24。属 Figma 与 CSS 的固有半行距差异
  （memory `figma-rounds-half-leading-css-does-not`），未强压。
- **手机波浪 48 高，稿的 `Spacer Bottom` 是 36**。复用了现站 `.gb-scallop`（全站一致优先），
  已登记待裁决 L。
- **桌面 hello 卡 `min-height: 136px`**：稿的 frame 固定 136 而内容只有 108，
  多出的 28 是文字下方的空白，不是 padding。
- **手机 hello 到 order 的间距是 32，稿 34**：32 是 container `2284:27615` 自己的 gap，
  34 是跨容器量出来的。取了前者。
- **桌面 renewal 态是外推的**（`27548` 只有手机稿），见待裁决 M。

### 遗留

- **`images/refer-friends.jpg` 画面里有第三方品牌 logo**（帽子上的 Prada 标）——
  已列进 SPEC §8b「上线前必须替换」。
- Subscriptions / Detail 两个视图仍是空壳（Task 5–7）。
- 导航项左侧的灰色圆点没做（便签 `27602` 说是待设计图标的占位，PLAN 明确不做）。

---

## Task 3 — 桌面竖导航、手机列表卡与视图切换（`$build-acct` = `20260909-a2`）

**设计源**：桌面 `2284:27843`（在 `27792` 内，与 `27678`/`28000` 逐值相同）、
手机 `2284:27617`（在 `27604` 内）、两栏外壳 `2284:27842`。

### 做了什么

- **桌面竖导航 `.gb-acct-nav`**（241 宽，5 组，组间 16）。组白底 `#fff` / 圆角 8 / 内边距 8；
  行 40 高、圆角 8、`padding-inline: 16`、PP Palma 400 14/20 ls −0.28 色 `#1a1a1a`；
  当前行 `#f3f3f3`。9 项：Account Overview / My Subscriptions / Order History ‖
  My Details / Change Password ‖ Refer a Friend ‖ Help / Contact Preferences ‖ Logout。
- **手机页内列表卡 `.gb-acct-list`**（4 组 6 项，组间 16）。组白底圆角 8 **内边距 0**，
  行 68 高、`padding: 24 16`（手机没有固定高压着，24 是真生效的）。
  行间分隔线取自 `Line 79`：326 宽（左右各缩 12）、1px、`#faf9f8`。
- **两栏外壳 `.gb-acct__inner`**：`241px minmax(0,1fr)`，`column-gap 32`，
  `padding: 48 352 144 244`。
- **`view` 模块**（`account.js`）：`[data-acct-goto]` 事件委托 + hash 同步 + 未知 hash 回退
  overview + `is-current` / `aria-current` 同步。header 汉堡菜单前两条也接了 `data-acct-goto`
  （保留 `<a href="#overview">` 做渐进增强）。

### 为什么这么定

- **桌面 9 项、手机 6 项，是两套并存不是一套折叠**。手机卡不含 Account Overview（你就在这页）
  与 Contact Preferences，Logout 在稿上是卡外的独立绿按钮（`2284:27648`，属 Task 4）。
  两者用 `display` 在 767 互斥切换。
- **内容列用 `minmax(0,1fr)` 而不是稿上的固定 571**。三个桌面稿一致地画
  `244 + 241 + 32 + 571 + 352 = 1440`，恰好铺满；照抄则 **768 档横向溢出 864 > 768**
  （`rwd.py` 实测，见下方判据）。1440 下 1fr 算出来正是 571，与稿逐值一致。
- **`244 / 352` 不对称但三稿完全相同**，判定为有意，未擅自改成居中。收敛方式无稿，
  已登记 SPEC 待裁决 A2。
- **六个无稿项渲染成 `aria-disabled` 的 `<span>`**，不是死链也不建页面（待裁决 C）。
  Logout 是 `<button data-acct-logout>` 空壳 —— 登出需要后端，不在 MVP。
- **禁用行与当前行不响应 hover**：前者不可点（全局铁律 13），后者已是填充态，
  hover 回 cream 会读作"离开了本区"。

### 文件清单

| 文件 | 改动 |
|---|---|
| `account.html` | `<main>` 换成 `.gb-acct__inner` 两栏；新增 `.gb-acct-nav` 9 项、overview 视图内 `.gb-acct-list` 6 项；菜单前两条加 `data-acct-goto`；`?v=` → a2 |
| `assets/account.scss` | 新增 Shell 两栏 / 桌面 nav / 手机 list 三个分区；`$build-acct` → `20260909-a2` |
| `assets/account.css` | 编译产物（双写） |
| `assets/account.js` | 新增 `view` 模块，挂进 `modules` 与 `window.gumiAcct`（**排在 `acctNav` 之后**，它 init 里调 `closeMenu()`） |
| `tools/acctcheck.py` | 追加 Task 3 断言 45 条；新增 `GOTO_SUBS` 动作与 `shown` 检查类型 |
| `docs/account/SPEC.md` | 待裁决 A 补上真实规律、新增 A2；第 8 节新增「三个桌面稿同名」 |

### 判据

| 判据 | 结果 |
|---|---|
| `tools/acctcheck.py` | **82 ok / 0 red**（Task 2 的 37 条 + Task 3 的 45 条） |
| 活性自检 A：删掉 `.gb-acct-list` 的 `@include narrow` | 转红 2 条 ✅ |
| 活性自检 B：把 `view` 模块摘出 `modules` | 转红 7 条 ✅ |
| 活性自检 C：内容列改回稿上的固定 `571px` | `rwd.py` 报 `768 横向溢出 864>768` ✅ |
| `tools/rwd.py account.html` | 全绿 |
| Playwright 实测 hover（headless 直连 `(hover:hover)` 恒 false） | 可点行变色 / 禁用行不变 / 当前行不变，3/3 |

### 遗留

- **视图内容全空**，三个 `<section data-acct-view>` 只有 overview 放了列表卡，
  Subscriptions / Detail 是空壳 —— 属 Task 4–7。**因为空，视图切换只能用 `hidden` 属性
  断言**（`shown` 检查），不能用渲染尺寸：空 section 高度为 0，`vis` 分不出"切掉了"和"是空的"。
- **顺带发现未修**（超出本轮范围，等拍板）：header 汉堡菜单里 `My Details` 与 `Log Out`
  仍是 `href="#"` 死链，是 Task 2 的遗留。菜单只有 4 条而桌面导航 9 条，也属待裁决 A。
- **手机列表卡的位置**（它在 Overview 页里排第几、上下间距）取自 `2284:27615` 的
  `gap 32`，但那要连同 `Hi Susanna` 卡片一起摆，留给 Task 4。
- 交互态的 hover 底色借用了 `$c-cream`，是自定值（待裁决 K），未登记进 motion 段变量表。

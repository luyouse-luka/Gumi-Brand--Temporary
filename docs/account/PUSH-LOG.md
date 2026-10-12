# Gumi Account — 推送记录

## 2026-10-09 — a73：数量确认、取消态Edit discount hover、header去重（已上线）

用户明确授权修改并提交live，随后追加两个header问题。确认Dev #180348977399 role=live；上传仅assets/account.scss、assets/account.css、snippets/gb-account-data.liquid、sections/gb-account.liquid，4个--only、--nodelete、--allow-live。不上传config、layout、account.js或主站header。

prework完整642主题文件，相对a72有4份线上他人更新（gb-account、gb-account-data、gb-account-placeholders、page.account），全部基于fresh保留；prepush再次全量pull相对prework零变化/目标冲突。Sass、脚本语法及164项检查通过；数量API使用模拟，未实测真实客户持久化/登录浏览器/iPhone Safari。

完整回读12 ok/0 red，4目标逐字节一致，其余638主题文件无变化，无增删。备份prepush-20261009-qty-discount；回读verify-20261009-qty-discount；新基线baseline-20261009-a73。源码Liquid映射：liquid/account-qty-discount/snippets/gb-account-data.liquid及sections/gb-account.liquid。

---

## 2026-10-09 — a72：移除Account footer logo hover（已上线）

用户明确授权“footer的logo也去掉hover效果然后推送live”。Dev #180348977399，role=live，仅上传assets/account.scss、assets/account.css，两个--only、--nodelete、--allow-live。prework完整642主题文件与a71基线一致；prepush完整pull与prework零变化，目标零冲突。

Sass编译通过；Chrome在390/1440下的账户页、登录页footer及顶栏logo回归共24项通过。完整回读8 ok/0 red，两目标逐字节一致，其余640主题文件无变化，无增删。备份prepush-20261009-footer-logo；回读verify-20261009-footer-logo；新基线baseline-20261009-a72。未做真实登录客户/iPhone Safari或线上浏览器验证。

---

## 2026-10-09 — a71：移除顶栏logo hover（已上线）

用户明确授权“拉取推送到live”。Dev #180348977399，role=live，仅上传assets/account.scss、assets/account.css，两个--only、--nodelete、--allow-live。prework完整642主题文件与a70基线一致；prepush再次全量pull与prework零变化，目标零冲突。

Sass编译通过，Chrome在390/1440宽度的8项logo hover/尺寸/首页链接检查通过（tools/acctlogo.cjs）。完整回读8 ok/0 red，两目标逐字节一致，其余640主题文件无变化，无增删。备份prepush-20261009-logo-hover；回读verify-20261009-logo-hover；新基线baseline-20261009-a71。未做真实登录账户/iPhone Safari或线上浏览器验证。

---

## 2026-10-07 — a70：cancelled优惠码hover（已上线）

Dev #180348977399 live，仅assets/account.scss、assets/account.css；2个--only --nodelete --allow-live。prework/prepush完整642主题文件零并发变化/冲突。Sass与4项颜色/点击检查通过；全量回读8 ok/0 red，2目标逐字节一致，其余640主题文件不变，无增删。备份prepush-20261007-cancel-hover；回读verify-20261007-cancel-hover；新基线baseline-20261007-a70。

---

## 2026-10-07 — a69：Account图标/下拉恢复（已上线）

Dev #180348977399 live；仅sections/gb-header.liquid、assets/account.js、assets/account.scss，3个--only --nodelete --allow-live。prework完整642主题文件与a68回读一致；prepush再次完整pull无并发变化/冲突。Account下拉恢复，汉堡保留；CSS产物相同不重复上传。

四档144项本地检查、Sass/JS语法通过；完整回读10 ok/0 red，3目标逐字节一致，639清单外主题文件无改动/增删。备份prepush-20261007-acct-menu-restore；回读verify-20261007-acct-menu-restore；新基线baseline-20261007-a69。a68他人修改覆盖检查亦通过，详见HANDOFF同日条目。

---

## 2026-10-07 — a68：logo尺寸及汉堡菜单（已上线）

目标Dev #180348977399（live），Shopify CLI，不走Git。上传仅assets/account.scss、assets/account.css、layout/account.liquid、sections/gb-account.liquid、sections/gb-header.liquid，均--only --nodelete --allow-live。prework发现他人overview loading改动并保留；prepush完整642文件与prework零并发变化。首次因暂存assets目录缺失只上传3份Liquid；补齐后完整midread核对Liquid及CSS零冲突，再只上传2份CSS。

最终全量回读14 ok/0 red，5目标逐字节一致，637清单外主题文件无变化，无新增/删除。Sass及四档102项本地检查通过，网页请求HTTP429，未完成线上浏览器检查。备份prepush-20261007-acct-burger；回读verify-20261007-acct-burger；新基线baseline-20261007-a68。详见HANDOFF同日a68条目。

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

按用户“推送live”授权完整pull Dev #180348977399，与a61基线无变化、无冲突。只推assets/account.js、account.css、account.scss，逐个--only、--nodelete、--allow-live。日历年份只读/inputmode=none，保留箭头切月、跨年及选日。
Chrome/WebKit手机触摸模式30项检查再次通过，JS语法通过。完整回读10 ok / 0 red：三目标逐字节等于本地，其余637主题文件无变化/丢失/新增。641本地文件含CLI生成AGENTS.md。live版本20261002-a62；备份prepush-20261002-a62；回读verify-20261002-a62；新基线baseline-20261002-a62。未验证iPhone真机软键盘及真实客户账户。

---

## Task 63 — Safari取消/Skip圆点及统一下拉箭头（2026-10-02，a61已上线）

取消/Skip选中radio关闭主题深色伪元素覆盖，使用已有绿色背景圆点，触摸hover保持浅绿底；尺寸与外圈保留。Account下拉箭头统一用户SVG：20×20、描边2px、#4d4d4d，原生备用SVG同步。JS/API与主站资源不改。

已按用户“推送live”授权完整拉取Dev #180348977399；与a60基线比较无线上变更、无冲突，只推assets/account.css和account.scss（分别--only、--nodelete、--allow-live）。完整回读8 ok / 0 red，两目标逐字节一致，其余文件无变化/丢失/新增。live为20261002-a61；基线baseline-20261002-a61；备份prepush-20261002-a61；回读verify-20261002-a61。推前120项radio及36项箭头检查重新通过。 641本地文件含CLI生成AGENTS.md（主题640文件）。WebKit与Chrome手机/桌面检查通过，未验证用户Safari真机。

---

## Task 62 — Edit Product下拉箭头描边（2026-10-02，a60已上线）

用户澄清“箭头细了”为Edit Product选项图标。本地设计2284-30960节点I2284:31124;84:8170;30:862及另一选项对应节点strokeWeight均为2，当前main.js共享图标为1.667。仅在Edit Product内的gb-acct-prod__control覆盖SVG path stroke-width:2px，保留20x20及旋转交互；其他产品/地址下拉不改。
文件：assets/account.scss、account.css；account.html、account-login.html（a60）；docs/account/HANDOFF.md、CHANGELOG.md、PUSH-LOG.md。
验证：Sass编译通过；390/1440两档检查Edit Product描边2px和20x20，Add Product/Shipping Form仍1.667px。按此前用户推送live授权完整pull，线上相对a59基线无变化、无冲突，只推两份Account样式。
全量回读8 ok / 0 red，两目标逐字节一致，其余文件无变化。live20261002-a60；基线baseline-20261002-a60；备份prepush-20261002-a60；回读verify-20261002-a60。未实测真实客户账户。

---


## 2026-10-02 — a59：Save改动判定和添加产品空态上线

按用户“推送live”明确授权部署Dev #180348977399。完整pull与a58基线无变化、无冲突。只推assets/account.css、account.scss、account.js、snippets/gb-account-data.liquid，逐个--only、--nodelete、--allow-live。
编辑弹窗按预填值重建基准，主题产品Save门控不被通用监听覆盖，未改动/改回原值保持禁用；无产品可添加提示跨全部网格列。推前acctsave 22项重新通过，先前折扣/Skip12、acctfeedback8 40项通过。
完整回读12 ok / 0 red，四目标逐字节一致，其余文件无变化、丢失或新增。基线baseline-20261002-a59；备份prepush-20261002-a59；回读verify-20261002-a59。641本地文件含CLI生成AGENTS.md（主题640文件），未实测真实客户账户。
同轮“箭头细了”反馈尚缺具体图标位置，已询问，未改动箭头。

---

## 2026-10-02 — a58：商品meta间距及名称两行省略上线

按用户“推送live”明确授权部署Dev #180348977399。完整pull与a57基线无变化，无冲突。只推assets/account.css、account.scss，逐个--only、--nodelete、--allow-live。
商品meta左内边距24px，手机宽100%；名称两行clamp、长词换行，避免挤占Edit。320/390/767/768/1440两类长名称本地浏览器检查通过。API与Skip交互未改。
完整回读acctpush 8 ok / 0 red，两目标逐字节一致，其余文件无改动、丢失或新增。基线baseline-20261002-a58；备份prepush-20261002-a58；回读verify-20261002-a58。641本地文件含CLI生成AGENTS.md（主题640文件）。未实测真实客户账户。

---

## 2026-10-02 — a57：撤回新增Skip交互，只加日期格样式

按用户明确指令完整pull并推live Dev #180348977399。与a56基线无线上变化，无冲突。撤回a56新增Skip状态记忆、按钮禁用、重复提交限制、原日期生成及恢复状态逻辑，API提交handlers与a55一致；折扣修复保留。日期格自身添加is-skipped或data-acct-skipped时采用设计灰色样式，由后台标记实际跳过日期。
仅推assets/account.css、account.scss、snippets/gb-account-data.liquid，逐个--only、--nodelete、--allow-live。12项本地检查重新通过。全量回读10 ok / 0 red，三文件逐字节一致，其余文件无改动、丢失或新增。
基线baseline-20261002-a57；备份prepush-20261002-a57；回读verify-20261002-a57。641本地文件含CLI生成AGENTS.md（主题640文件）。未实测真实客户账户。

---

## 2026-10-02 — a56：折扣chip、空标签及Skip状态上线

按用户“拉取推送”明确授权推live Dev #180348977399。完整拉取641本地文件（含CLI生成AGENTS.md，主题文件640），与a55基线无变化、无目标冲突。
只推assets/account.css、account.scss、snippets/gb-account-data.liquid，逐个--only、--nodelete、--allow-live。修复折扣默认隐藏和重复chip、空金额绿色条，Skip成功后首格/按钮灰显及renewal date提示；最后商品保护不包含在本轮。
推前acctdiscountskip 18项重新通过，此前acctfeedback8 40项通过。完整回读acctpush 10 ok / 0 red，三个目标逐字节等于本地，其余文件无改动、丢失或新增。
新基线baseline-20261002-a56；备份prepush-20261002-a56；回读verify-20261002-a56。状态版本20261002-a56。
限制：Skip已确认操作保存在内存/sessionStorage，同一浏览器会话恢复；跨设备或新会话历史跳过状态需后端字段。接口验证为模拟API，未验证真实客户登录态或Safari真机。

---

## 2026-10-02 — a55：手机问候区小熊位置上线

按用户明确指令推live Dev #180348977399。手机小熊artwork top由24px改为-17px，上移41px；桌面和平板不变。最后商品保护已按用户要求撤回，不上传任何订阅JS或Liquid。
推前完整拉取，两个目标与a54基线无线上冲突。只推assets/account.css、account.scss，使用逐个--only及--nodelete、--allow-live。account.js和后端snippet保持不变。
本地acctheaderfix 32项通过；此前位置检查390/767/1440及acctfeedback8 40项通过。完整回读acctpush 8 ok / 0 red，两目标逐字节一致，其余文件无改动、丢失或新增。回读目录641文件，含CLI生成的AGENTS.md（主题文件640）。
新基线baseline-20261002-a55；备份prepush-20261002-a55；回读verify-20261002-a55。未验证真实客户登录态或Safari真机。

---

## 2026-10-01 — a54：小熊、折扣输入、手机菜单与 Safari 圆点修复上线

按用户明确指令部署 live Dev #180348977399。推前完整拉取 640 文件，与 a53 基线无变化。仅推 assets/account.css、account.scss、account.js，逐个 --only + --nodelete + --allow-live。
移除内层视图裁切、改全宽页面边界防横向溢出；长折扣输入省略；手机账户图标点击展开菜单；地址 radio 使用绿色背景圆点避免 Safari 原生黑点。
本地 acctheaderfix 32、acctcover 47、acctradio 16 共 95 项通过，Sass 编译及 JS 语法通过。全量回读 acctpush 10 ok / 0 red：三目标文件逐字节等于本地，其余 637 文件无改动、无丢失、无新增。新基线 baseline-20261001-a54；备份 prepush-20261001-a54。
资源版本 20261001-a54。未在用户 Safari 真机或真实客户账户复测。

---

## 2026-10-01 — a53：八项反馈上线

按用户明确指令部署 Dev #180348977399（role=live）。仅推 assets/account.css、account.scss、account.js 和 snippets/gb-account-data.liquid，逐个 --only + --nodelete + --allow-live。
推前完整备份 640 文件，发现 data/modals Liquid 后端更新。三方合并 data，保留订阅周期/selling plans 的新逻辑；后端上传同时移除了 Task 54 的动态一次性购买图标补丁，已恢复。modals Liquid 保留原样。三份目标 assets 对基线无线上冲突。
推前复跑 acctfeedback8 40、acctscroll 14、accticons 20 全通过；先前 acctcover 47/acctlayers 21 回归通过。全量回读 acctpush 12 ok / 0 red：四个目标文件逐字节等于本地，其余 636 文件无改动、无丢失、无新增。新基线 baseline-20261001-a53；备份 prepush-20261001-a53。
未验证真实客户账户、用户具体手机浏览器；API 验证使用模拟响应。资源版本 20261001-a53。

---

## Task 54 — Order 图标还原（2026-10-01 已推 live）

按用户提供 SVG 还原 One-off purchase 的 12px 灰色圆圈 1 图标，补 Download Invoice 的 20px 白色下载图标。线上数据层复用第一条订阅商品模板且只换标签文字，导致一次性商品沿用订阅图标；现启动时保存一次性图标，动态渲染按 is_subscription 替换。SVG 路径使用用户原值，省略无裁切作用的重复 clipPath 包装。
文件：account.html；liquid/account-order-icons/snippets/gb-account-data.liquid、gb-account-placeholders.liquid；tools/accticons.cjs。样式与资源版本 a52 不变。
验证：桌面/手机尺寸、颜色、动态商品类型、无溢出 20 项通过；模板 JS 用空 Liquid 数据解析通过。仅推两个 snippets，完整回读 8/0，其余 638 文件无改动/丢失/新增。基线 baseline-20261001-icons，备份 prepush-20261001-icons。未实测真实客户登录态及发票下载接口。

---

## 2026-10-01 — a52：手机主视图淡入淡出上线

用户明确授权推 live。确认 Dev #180348977399 role=live；推前完整拉取 640 文件，目标 account.css/account.scss 对 a51 基线无线上改动，data/modals Liquid 后端更新保留。仅推两份样式，逐个 --only + --nodelete + --allow-live。
全量回读 8 ok / 0 red：两个文件逐字节等于本地，其余 638 文件无改动、无丢失、无新增。备份 prepush-20261001-a52，新基线 baseline-20261001-a52。acctcover 47 + acctlayers 21 全通过；未实测真实客户登录态。

---

> account 线自己的推送记录。**主站线的 [`../PUSH-LOG.md`](../PUSH-LOG.md) 不要动** ——
> 那是另一条线的文件（HANDOFF §1）。两条线推的是**同一个主题**，所以推之前必须拉线上最新。
>
> 店铺 `je1ka9-er.myshopify.com`，主题 **Dev #180348977399（role = live）**。
> ⚠ **名字叫 Dev，但它就是 live 主题** —— 看角色不看名字。
> 一律 `--only <file>` 逐个列出 + `--nodelete` + `--allow-live`，**绝不裸跑 push**。
>
> 基线目录在**仓库外**：`/home/ly/project/Gumi-Brand-shopify/baseline-<date>-<tag>`。

## 流程

```
1  theme pull  → 基线目录            拉线上最新，先看要推的文件在不在
2  三方对比    baseline / remote / local
3  cp -r 基线 → push 目录，把要推的文件放进去   ⚠ 别往基线目录里放，那会毁掉对比
4  theme push  --only … --nodelete --allow-live
5  theme pull  → verify 目录
6  python3 tools/acctpush.py <baseline> <verify> <推过的路径>…
7  滚基线      verify → baseline-<date>-<tag>
```

⚠ **`theme push` 的输出里有一句 `Cleaning your remote theme`** —— 它不是在删文件，
但这句话足够吓人，所以第 6 步的「基线文件零丢失」断言必须跑，别凭这句话下结论。

## 2026-09-30 — a51：Task 52 兼容线上视图容器上线

主题 Dev #180348977399（role = live）。推前完整拉取 640 文件，三方对比 ours 2 / theirs 1 / CONFLICT 0；线上 gb-account-data.liquid 的后端更新保留。
仅推 assets/account.js（初始化时注册线上缺失的 data-acct-views）和 assets/account.scss（版本标记），逐个 --only + --nodelete + --allow-live。CSS 与线上 a50 字节一致，无需重推。
全量回读 640 文件，acctpush **8 ok / 0 red**：两个文件逐字节等于本地，其余 638 文件无改动、无丢失、无新增。
新基线 baseline-20260930-a51；推前备份 prepush-20260930-a51。修复已通过线上容器结构复现及静态回归 64 项；此次上线确认文件回读，未进行真实客户账户交互测试。

---

## 2026-09-30 — a50：Task 51 Radio、手机覆盖切换与滚动条上线

主题 Dev #180348977399（role = live）。推前重新拉取 640 文件；三方对比 ours 3 / theirs 1 / CONFLICT 0。线上 `snippets/gb-account-data.liquid` 的后端更新完整保留。

仅推 `assets/account.css`、`assets/account.scss`、`assets/account.js`，逐个 `--only` + `--nodelete` + `--allow-live`。
全量回读 640 文件，acctpush **10 ok / 0 red**：三个目标文件逐字节等于本地，其余 637 文件零改动、零丢失、零新增。
新基线 `baseline-20260930-a50`；推前备份 `prepush-20260930-a50`。本轮实现已通过 82 项本地检查；此次发布验证为完整文件回读，未进行线上真实客户账户交互测试。

---

## 2026-09-30 — a49：Task 50 七项修复上线

主题 Dev #180348977399（role = live）。推前重新拉取 640 文件，与 a48 基线零差异；三方对比 ours 7 / theirs 0 / CONFLICT 0。

推送清单：`assets/account.css`、`assets/account.scss`、`assets/account.js`、`assets/main.js`；`snippets/gb-account-data.liquid`、`snippets/gb-account-modals.liquid`、`snippets/gb-account-placeholders.liquid`。
仅上述七个文件，`--only` + `--nodelete` + `--allow-live`；未推静态 HTML、模板 JSON 或配置。

全量回读 640 文件，`tools/acctpush.py` **18 ok / 0 red**：七个文件逐字节等于本地，其他 633 文件零改动、零丢失、零新增。
新基线 `baseline-20260930-a49`；推前备份 `prepush-20260930-a49`。Account `$build-acct` = `20260930-a49`。
未执行真实客户账户的修改接口；推前的 API 行为验证为模拟响应，62 项专项与回归已通过。本次回读核验确认文件上线，不代表真实账户端到端测试。

---
## 2026-09-30 — a48：Task 49 手机视图覆盖式切换上线

仅推 `assets/account.css` + `assets/account.scss` 到 Dev #180348977399（role = live）。推前与 a47 比对两个推送文件无线上改动。
全量回读 640 文件：两个推送文件逐字节一致，其他 638 文件零改动、零丢失、零新增。
新基线 `baseline-20260930-a48`；推前快照 `prepush-20260930-a48`。专项 `acctcover.cjs` 43 项通过。

---
## 2026-09-30 — a47：Task 48 日历展开时的弹窗横移修复上线

仅推 `assets/account.js` + `assets/account.scss` 到 Dev #180348977399（role = live）；CSS 字节不变，未推。
推前拉取 640 文件，三方对比 ours 2 / theirs 1 / CONFLICT 0。对方的 `snippets/gb-account-data.liquid` 改动完整保留。
全量回读 640 文件：两个文件与本地逐字节一致，其余 638 文件零变更、零丢失、零新增。
新基线 `baseline-20260930-a47`，推前备份 `prepush-20260930-a47`。JavaScript 语法检查通过。
本次未重跑浏览器判据；Task 48 既有 `calshift` 为 6 ok / 0 red，月底日期相关回归失败仍待处理。

---
## 2026-09-28 — a46：Task 47 删掉前端的 qty 步进（js + scss）

**基线 `baseline-20260928-a46`（640 文件）。** 推前重拉的线上快照与 a45 基线零差异；三方对比 ours 2 / theirs 0 / CONFLICT 0。

| 主题内路径 | 为什么 |
|---|---|
| `assets/account.js` | 删掉 `acctQty`：线上它和 `gb-account-data.liquid` 的 `attachQtyControls()` 双绑，点一下 ±2 |
| `assets/account.scss` | 只改了 `$build-acct` → `20260928-a46`（`account.css` 字节不变，没推） |

回读 `acctpush.py` **8 ok / 0 red**。线上 `account.js` 中 `acctQty` 的出现次数为 0。
`acctmodal` 在推送后跑完：**1303 ok / 0 red / 1 aborted**（a41 时是 1321 条，少的 18 条是步进行为断言合并成了反向断言；那条 aborted 与基线一致）。推前已绿的是 `r26check` 34 / `acct43check` 17 / `acctview` 26 / `acctloading` 57，另有 `r26check` 反向验证转红。

---

## 2026-09-28 — a45：Task 46 按钮 loading 态上线（css + scss）

**基线 `baseline-20260928-a45`（640 文件）。**
推前重新拉取的线上快照与 a44 基线对比，有 6 处差异，全是对方的改动，都与本次推送无关：
`gb-account-data.liquid`（新增，1767 行）、`gb-account.liquid`、`gb-account-placeholders.liquid`、
`page.account.liquid`、`settings_schema.json`、`settings_data.json`。
本次要推的两个文件：线上与 a44 相同，本地有改动，三方对比 ours 2 / theirs 0 / CONFLICT 0。

| 主题内路径 | 为什么 |
|---|---|
| `assets/account.css` | 新增 `button.is-loading` 转圈（编译产物；diff 只多这一条规则） |
| `assets/account.scss` | 同上的源码 + `$build-acct` → `20260928-a45` |

回读 `acctpush.py` **8 ok / 0 red**。⚠ 要在**仓库根目录**跑，本地路径按 cwd 解析。
线上核验：`account.scss` 读到 `20260928-a45`，`account.css` 里 `button.is-loading` 3 处。

⚠ 上面 a43 那节列的三处「仍然要请对方改」**依旧有效**：`data-acct-watched` 9 处、`flatpickr.min.css` 与 `pay-visa.svg` 仍 404。

---

## 2026-09-18 — a44：Task 45 的九处间距上线（css + scss）

**基线 `baseline-20260918-a44`（639 文件 / 207 assets）。**
三方对比：线上与 `baseline-20260918-a43` **零差异**（`diff -rq` 全静默，没人动过）；
本地这两个文件与线上不同 —— 都是本轮改的。

| 主题内路径 | 为什么 |
|---|---|
| `assets/account.css` | Task 45 九处间距值（编译产物） |
| `assets/account.scss` | 同上的源码 + `$build-acct` → `20260918-a44` |

✅ **推之前先验了双写**：`account.css` 对线上的 `diff` **正好是这九个值、一处不多**
（11 个 hunk 全部对得上），没有 autoprefixer / browserslist 带来的无关差异。

回读 **8 ok / 0 red**：两个文件逐字节等于本地；637 个基线文件零改动零丢失；没有多出文件。
线上产物核验：`account.scss` 读到 `20260918-a44`，`account.css` 里
`margin-left: 2px` / `row-gap: 12.5px` / `padding: 20px 22px` / `padding-right: 12px` /
`margin: 0 -3px` / `row-gap: 0` 各 1 处、`margin-top: -1px` 2 处（row + rule）。

⚠ **`account.js` 不在清单里** —— Task 45 一行 JS 都没改。
⚠ 上一节的三条「仍然要请对方改」**依旧有效**，本轮没有新增请求。

---

## 2026-09-18 — a43：Task 43/44 上线（只两个文件）

**基线 `baseline-20260918-a43`（639 文件 / 207 assets）。**
三方对比：线上与 `baseline-20260918-a41` **零差异**，其余 637 个文件 `diff -rq` 证明未碰。

| 主题内路径 | 为什么 |
|---|---|
| `assets/account.js` | Task 43 四个去重标记改成元素 property + Task 44 的 `acctSelectFit` |
| `assets/account.scss` | 只有 `$build-acct` → `20260918-a43` |

⚠ **`account.css` 不在清单里** —— 两轮都只改 JS，重编译后的产物与线上**逐字节相同**
（`$build-acct` 只是 Sass 变量，不输出到 CSS）。推它没有意义。

回读 **8 ok / 0 red**：两个文件逐字节等于本地；637 个基线文件零改动零丢失；没有多出文件。
线上产物核验：`account.scss` 读到 `20260918-a43`，`account.js` 里 `_acctWatched` 在、
`acctSelectFit` 在，**`setAttribute('data-acct-watched'` 为 0 处**（不再往 DOM 写标记）。

### 仍然要请对方改的三处（都是他们的文件）

1. ⚠⚠ **`snippets/gb-account-modals.liquid` 8 处 + `sections/gb-account.liquid:134` 1 处的
   `data-acct-watched="1"`** —— JS 的运行时去重标记被从渲染结果里抄进了模板，
   Task 43 之前**这九处的 Save 全都是死的**。我方已改用元素 property，**留着不影响**，
   但它们是死属性，建议清掉，也提醒别再把 `data-acct-*-bound` 之类抄进来。
2. ⚠ **`main.js:1892` 的 `clipBottom()` 把 `overflow: clip` 当成不裁切**
   （`if (o !== "visible" && o !== "clip")`）。建议改成 `if (o !== "visible")`。
   这是主站线的文件，account 线没动；account 两页已由 `acctSelectFit` 自行接管。
   影响面：任何 `overflow: clip` 容器里的共享下拉。
3. ⚠ `layout/account.liquid:14` 的 `flatpickr.min.css` 与 `pay-visa.svg` 仍 404，见上一节。

---

## 2026-09-18 — a41：Task 42 的双日历修复上线

**基线 `baseline-20260918-a41`（639 文件 / 207 assets）。** 三方对比：线上与 `baseline-20260918-a40`
**零差异**（上一次推完对方没再动主题），其余 636 个文件 `diff -rq` 证明 push 目录未碰。

推的三个：

| 文件 | 改了什么 |
|---|---|
| `assets/account.js` | `acctCal._arm` 开头清掉模板预渲染的 `.flatpickr-calendar` —— **这条就是线上「两个日历」的修复**，本地静态页看不出差别 |
| `assets/account.scss` | 日历禁用态拆成两条规则（`.flatpickr-disabled` 加 `cursor: not-allowed`，补白格保留 `pointer-events: none`）；`$build-acct` → `20260918-a41` |
| `assets/account.css` | 重编译 |

回读 `python3 tools/acctpush.py remote-a41 verify-a41 assets/account.css=assets/account.css …`
→ **10 ok / 0 red**：三个文件逐字节等于本地；636 个基线文件零改动、零丢失；没有多出任何文件。
线上产物再核一遍：`account.scss` 读到 `20260918-a41`，`account.css` 里有
`.flatpickr-day.flatpickr-disabled { … cursor: not-allowed }`，`account.js` 里有那条清壳守卫。

⚠ **`acctmodal` 是推完之后才跑完的**（1321 ok / 0 red / 1 aborted，与基线一致）。
推的时候已绿的是九个判据，含两个日历专项（`acct38check` 80 / `acct31check` 437）与
`acct42check` 21。**回滚路径是 `baseline-20260918-a40`**，没用上。
⚠ **推之前必须重新 `theme pull`** —— 对方随时在改那五个 account liquid，
拿旧基线比会把他们的改动算成 `collateral edits`。

**给对方的两条建议**（他们的文件，我方不动）：

1. `layout/account.liquid:14` 的 `<link rel="stylesheet" href="{{ 'flatpickr.min.css' | asset_url }}">`
   **建议删掉** —— 这个 asset 我方没有（日历皮肤照 `30465` 手写在 `account.scss` 里），线上一直 404。
2. `snippets/gb-account-flatpickr-cal.liquid` 的预渲染壳**可以一起删** —— 缺了 vendor CSS 它本来就是
   无样式裸 DOM，壳里还硬编码着 `September 2026`，pre-paint 的价值不成立。
   ⚠ 即使他们不删，Task 42 的守卫也已经把它清掉了，**两边不冲突**。

---

## 2026-09-18 — a40：三个资源追平 + 补上模板已在引用的四个 404

Task 41 收工后按指令推的第二批。**基线 `baseline-20260918-a40`（639 文件 / 207 assets）。**

### ⚠ 三方对比查出：主题侧已经把 account 接上模板了

`a29` 之后**别人动过主题**，account 的 Shopify 化**已经开始并上了 live**：

| 变动 | 文件 |
|---|---|
| 新增 | `snippets/gb-account-flatpickr-cal.liquid`（预渲染的 flatpickr 日历外壳，说明对方已跟进 Task 38）|
| 改动 | `layout/account.liquid` · `sections/gb-account.liquid` · `snippets/gb-account-modals.liquid` · `snippets/gb-account-placeholders.liquid` |

路由是 **`templates/page.account.liquid` → `{% layout 'account' %}`**，即 `/pages/account`。
⚠ **HANDOFF §7 那句「线上还没有模板引用它们」已经过时**，本轮已改。
⚠ **这五个 liquid 是对方的范围，一个都没碰** —— push 目录是 `cp -r` 刚拉的线上快照再覆盖我方九个文件，
推前 `diff -rq` 证明其余 626 个文件零差异。

### 模板引用了六个线上不存在的 asset，本轮补掉四个

| 缺的 asset | 处理 |
|---|---|
| `acct-bear-side.webp` | **本轮补推**（a29 只推了 `.png`，`<source type="image/webp">` 那一半漏了）|
| `refer-friends.jpg` / `.webp` | **本轮补推** —— ⚠ **需求方 2026-09-18 拍板要推**。帽子上的 Prada 标的商标风险**已当面告知**，SPEC §8b / HANDOFF §6 的「上线前必须替换」**仍然有效**，换图后记得删旧的 |
| `flatpickr.min.js` | **本轮补推**。v4.6.13，MIT。本地一直是 untracked，Task 31 删过、Task 38 装回 |
| `flatpickr.min.css` | ❌ **没推，本地根本没有这个文件** —— 我们的日历皮肤是照 `30465` 手写在 `account.scss` 里的。`layout/account.liquid:14` 这条 `<link>` 是对方模板的多余引用，**建议对方删掉**（缺它只是少了 vendor 默认皮肤，不影响外观）|
| `pay-visa.svg` | ❌ **没推，主站线的资源**（HANDOFF §1 的界线，a29 那轮同样理由跳过）。线上 404，**要么主站线补推，要么对方模板改引用** |

### 推送清单（9 个，全部 `assets/` 顶层）

| 主题内路径 | 本地来源 | 状态 |
|---|---|---|
| `assets/account.css` | `assets/account.css` | 覆盖 a29 → **a40** |
| `assets/account.js` | `assets/account.js` | 覆盖 |
| `assets/account.scss` | `assets/account.scss` | 覆盖 |
| `assets/flatpickr.min.js` | `assets/flatpickr.min.js` | **新增** |
| `assets/acct-bear-side.webp` | `images/acct-bear-side.webp` | **新增** |
| `assets/refer-friends.jpg` | `images/refer-friends.jpg` | **新增** |
| `assets/refer-friends.webp` | `images/refer-friends.webp` | **新增** |
| `assets/product-placeholder.png` | `images/product-placeholder.png` | 内容未变，幂等重推 |
| `assets/acct-bear-side.png` | `images/acct-bear-side.png` | 内容未变，幂等重推 |

命令照旧：`--only` 逐个列 + `--nodelete` + `--allow-live`，`--path` 指向 push 目录。

### 回读

`python3 tools/acctpush.py baseline(=推前拉的线上快照) verify assets/x=本地路径 …`
→ **22 ok / 0 red**：九个文件全部落地且**逐字节等于本地**；630 个基线文件零改动、零丢失；
新增文件正好是清单里那四个。assets 计数 203 → **207**。

⚠⚠ **`acctpush.py` 本轮补了 `byte-identical` 断言** —— 旧版只验「文件存在」，
**推一个过期版本上去照样读绿**，a29 那轮的「逐字节一致」其实是手工比的。
写法 `assets/x.png=images/x.png`（主题路径=本地路径，图片两边不同名）。
活性自检：往回读的 `account.css` 末尾加一个字节，那条当场报红。

⚠ **基线必须用「推之前刚拉的线上快照」，不能用 `baseline-20260916-a29`** ——
对方那五个 liquid 的改动会被算成 `collateral edits`，五条假红。

### 线上页面没法直接验

店铺开着 **storefront 密码保护**：`https://je1ka9-er.myshopify.com/pages/account` 301 到
`gumi.com.au/password`，拿回来的是密码页（Horizon 主题的壳）。
**文件层面已验到逐字节**；要看渲染效果需要 storefront 密码，或在主题编辑器里预览。

---

## 2026-09-16 — a29：account 的资源首次上主题

Task 32 收工后推的**第一批 account 资源**。推之前线上一个 account 文件都没有，
所以这五个全是**新增，零覆盖**。

| 本地 | 主题内路径 | 大小 |
|---|---|---|
| `assets/account.css` | `assets/account.css` | 91 KB |
| `assets/account.js` | `assets/account.js` | 35 KB |
| `assets/account.scss` | `assets/account.scss` | 源码，与主站的 `customstyle.scss` 同样上主题 |
| `images/product-placeholder.png` | `assets/product-placeholder.png` | 1 KB，页面 14 处引用 |
| `images/acct-bear-side.png` | `assets/acct-bear-side.png` | 95 KB，1 处引用 |

⚠ **路径要映射**：本地静态站把图片放 `images/`，**主题里没有这个目录** ——
Shopify 只认 `assets/` 等标准顶层目录，线上 78 张图全在 `assets/` 里。
所以本地 `images/x.png` 推成 `assets/x.png`，将来模板里写 `{{ 'x.png' | asset_url }}`。

**没推，各有原因：**

- **`images/refer-friends.jpg`** —— 画面里有第三方品牌 logo（帽子上的 Prada 标），
  授权来源未知。SPEC §8b 与 HANDOFF §6 都列为「上线前必须替换」。
  **推上客户店铺等于把商标风险一起带过去**，等设计方换图。
- ~~**`images/acct-*.svg` 26 个**~~ —— 页面用的是 inline svg，一个都没引用。
  **Task 35 已把这 26 个文件从仓库删掉**（节点号存进 `NODE-MAP.md`），此条作废。
- **favicon / `pay-*.svg` / `nav-card-bear.png`** —— 主站线的资源。`nav-card-bear.png`
  线上已有；其余线上没有，但那是主站线的事，不由 account 线代推。
- **`customstyle.css` / `main.js` / `lenis.min.js`** —— 主站线的，线上已有。

回读判据 `python3 tools/acctpush.py <baseline-20260910-r138 那份> <verify> …`：
**10 ok / 0 red** —— 五个文件逐字节一致；198 个基线文件零改动、零丢失；
assets 计数 198 → **203**。基线滚到 `baseline-20260916-a29`。

⚠ **推了资源不等于 account 页面上线了**。线上还没有任何模板引用它们：
`account.html` / `account-login.html` 仍是静态页，Shopify 化（`templates/customers/*`）
还没开始，见 HANDOFF §7。

---

## ~~2026-09-16 · 线上已落后三轮（Task 33 / 34 / 36）~~ — 已于 2026-09-18 随 a40 推完

⚠ **live 主题上的是 `a29`，本地已是 `a35`**。这三个文件改了，**没有推**（推送等明确指令）：

| 文件 | 改了什么 |
|---|---|
| `assets/account.css` | 删掉 `.gb-acct-header.is-open` 与 header 的 `transition`、`__link` 的 opacity hover；Task 36 新增 `.gb-acct-video__media` |
| `assets/account.scss` | 同上 + Task 34 的七处值 + Task 34 侧栏圆点 + `$build-acct` → `20260916-a35` |
| `assets/account.js` | 删掉 `acctNav` 模块（汉堡点击开关）、**补上弹窗锁屏缺的 `smoothScroll.pause/resume`** |

⚠ **两个静态页也已改**（Task 33 购物车图标、Task 36 `<video>` 占位、18 处 `?v=` → a35），
但 `account.html` / `account-login.html` **不在主题里**（Shopify 化没开始），所以不进推送清单。
推送清单就是上面三个，命令照本文件上一节的写法（`--only` 逐个列 + `--nodelete`），
推完跑 `python3 tools/acctpush.py <baseline-20260916-a29> <verify> assets/account.css assets/account.js assets/account.scss`。

# Gumi Account — 区块 ↔ 设计板对照

> Task 25 把 `account.html` 的定位注释移到这里（需求 5：清掉页面内注释），
> Task 32 补上了当时漏网的三条（末尾三行）。
> **页面里只留功能注释**（每个视图 / 弹窗 / 结构块一句「这块做什么」）与 `TODO` 占位标记，
> **节点号一个都不留** —— 需求方 2026-09-16 点名要清。
> 数值出处仍以 Figma 节点为准（铁律 2），这张表是找回节点号的**唯一**索引。

| 锚点（紧随注释的元素） | 原注释 |
|---|---|
| `.gb-announcement__stars` | Placeholder for the official Trustpilot embed; copy is from the design |
| `.gb-scallop` | 2284:27680 desktop / 2284:27607 phone: the lime band ends in a scallop, not a straight edge. Reuses the site component; only the pair is new. |
| `.gb-acct-nav` | Six of the nine rows have no board of their own (waiting on decision C), so they render disabled rather than linking nowhere. |
| `.gb-acct-nav__item` | Shell only: signing out needs a backend that is out of MVP scope. |
| `.gb-acct-hello` | 2284:27766 desktop card / 2284:27610 phone: same block, the lime card and the bigger type are desktop only. |
| `.gb-acct-list` | The phone board reaches the other sections through this card, so it omits Account Overview (you are on it) and Contact Preferences, and keeps Logout as a separate button. It is not the desktop rail reflowed -- both exist and swap at the phone breakpoint. |
| `.gb-acct-refer` | 2284:27780 desktop / 2284:27639 phone |
| `.gb-acct-logout` | 2284:27648, phone only: on desktop Logout sits in the side rail. Shell only -- signing out needs a backend that is out of MVP scope. |
| `.gb-acct-intro` | 2284:28068 desktop / 2284:28312 phone: the lime card is desktop only, and the back button the overview keeps hidden shows here. |
| `.gb-acct-subs__list` | 2284:28072 / 28109 / 28146 desktop, 2284:28314 / 28315 / 28316 phone. The board shows all three states at once, so each card carries its own state rather than one card being switched. |
| `.gb-acct-sub__thumb` | 196:19033 is a flat #d9d9d9 rectangle on every board: the product shot is not in the design yet (see SPEC 8b). |
| `.gb-acct-sub__thumb` | 196:19033 is a flat #d9d9d9 rectangle on every board: the product shot is not in the design yet (see SPEC 8b). |
| `.gb-acct-sub__thumb` | 196:19033 is a flat #d9d9d9 rectangle on every board: the product shot is not in the design yet (see SPEC 8b). |
| `.gb-acct-intro` | 2284:27860 desktop / 2284:28337 phone. Same block as the list page's header, except the back button shows at every width and a pencil replaces the subtitle. |
| `.gb-acct-sub` | 2284:27865 desktop / 2284:28344 phone |
| `.gb-acct-btn` | 27881's icon slot is visible=false on the board |
| `.gb-acct-product__flavour` | 27899 is literally the word "Flavour": note 30913 says flavour is not editable yet, so the board never filled the value in. |
| `.gb-acct-product__flavour` | 27899 is literally the word "Flavour": note 30913 says flavour is not editable yet, so the board never filled the value in. |
| `.gb-acct-product__flavour` | 27899 is literally the word "Flavour": note 30913 says flavour is not editable yet, so the board never filled the value in. |
| `.gb-acct-product__flavour` | 27899 is literally the word "Flavour": note 30913 says flavour is not editable yet, so the board never filled the value in. |
| `.gb-acct-detail__add` | Note 30905 says Add Items can be turned off until there are other products. Built as drawn; whether it ships is decision H. |
| `.gb-acct-sub` | 2284:27980 desktop / 2284:28458 phone |
| `.gb-acct__view` | 2284:27202 phone only; the desktop layout is extrapolated from the three desktop boards (decision C, 2026-09-10). Only the heading changes size between the two: 20/24 phone, 24/30 desktop. |
| `.gb-acct-pager` | 2284:27202 Pagination. A static page has one page, so both arrows ship disabled; the left one is disabled on page 1 regardless. |
| `.gb-acct__view` | 2284:27304 phone only. Reached from a card's View Order, so it has no row of its own in the nav. |
| `.gb-acct-btn` | decision I, note 27444: "Only do if very very very cheap. Otherwise, remove." Built as drawn; say the word to drop it. |
| `.gb-acct-help` | 2284:27304 closes with the same sand card as Help (27170) |
| `.gb-acct__view` | 2284:27081 phone only. 27116 is the same board word for word at the same height, so only one is built (decision O). |
| `.gb-acct-field__label` | board 27081 labels this one "Email*" -- copy-paste slip, SPEC 8 |
| `.gb-acct-card__note` | decision AD: the board draws no checkbox here, only this line |
| `.gb-acct__view` | 2284:27151 phone only |
| `.gb-acct-card__text` | board 27151 reads "instructions ro reset it" -- typo, SPEC 8 |
| `.gb-acct__view` | 2284:27170 phone only |
| `.gb-acct-help` | 2284:27170 Frame 1984078368; Order Detail closes with the same card |
| `.gb-acct-auth` (signup, `account-login.html`) | 2284:35059 desktop / 2284:35023 phone |
| `.gb-acct-order` | Current order has three designed states, switched by the modifier class (or the data attribute): `gb-acct-order--preparing` 2284:27450 "We're preparing your order"; `--shipped` 2284:27770 "It's been shipped"; `--renewal` 2284:27548 upcoming renewal, inverted skin. Nothing switches this at runtime -- a template picks one. |

---

## 已删除的 26 个 `images/acct-*.svg`（Task 35）

这些文件**一个都没被页面引用** —— 图形全部 inline 在 `account.html` 里，
文件只是导出时留下的重复品，2026-09-16 删除。**节点号记在这里，因为**：

- 生成脚本 `figma/account/cut-icons.py` 与整个 `figma/` 目录**都不在 git 里**，只存在于开发机
- 删掉文件后，节点号在仓库里就没有第二份了

要取回某个图标：① 从 `account.html` 里把对应的 inline `<svg>` 拷出来（最快，且是页面在用的那一版）；
② 或在开发机上按下表的节点号重跑 `cut-icons.py`。

⚠ **`acct-qty-minus` / `acct-qty-plus` / `acct-field-chevron` / `acct-opt-chevron` 这四个是废件**：
前两个的 viewBox 是从整板裁的紧贴框（减号 16×2），配方形 CSS 尺寸会被拉变形 —— 页面里是
Task 26 重画并归一到 `0 0 14 14` 的版本；后两个的下拉在 Task 27 换成了 `main.js` 的 `selectBox`，
chevron 由 `customstyle.scss` 自己画。**别按这四条把文件复原回去用。**

| 图标 | 取自哪块板 | frame | 节点 id | 页面里 |
|---|---|---|---|---|
| `acct-action-arrow` | `2284-27604_account-overview` | `2284:27604` | `I2284:27646;282:12351` | 已 inline |
| `acct-alert` | `2284-33847_edit-product---only-one-product` | `2284:33847` | `2284:34001` | 已 inline |
| `acct-back-arrow` | `2284-28305_my-subscriptions` | `2284:28305` | `I2284:28312;426:43485;42:620` | 已 inline |
| `acct-bear-halo` | `2284-27604_account-overview` | `2284:27604` | `2284:27652` | 已 inline |
| `acct-cal-next` | `2284-30465_cancel-subscription` | `2284:30465` | `I2284:30628;1054:1640;1054:2006;1027:6649` | 已 inline |
| `acct-cal-prev` | `2284-30465_cancel-subscription` | `2284:30465` | `I2284:30626;1054:1640;1054:2006;1027:6973` | 已 inline |
| `acct-chip-remove` | `2284-31809_add-a-discount-code` | `2284:31809` | `I2284:31973;565:46772` | 已 inline |
| `acct-date` | `2284-27792_account-overview-desktop` | `2284:27792` | `I2284:27880;336:36087` | 已 inline |
| `acct-edit-pencil` | `2284-27792_account-overview-desktop` | `2284:27792` | `2284:27864` | 已 inline |
| `acct-field-chevron` | `2284-32135_edit-frequency` | `2284:32135` | `I2284:32289;196:17634;196:17613;30:862` | **已废弃** |
| `acct-field-date` | `2284-31976_edit-date` | `2284:31976` | `I2284:32130;196:17634;196:17613;350:19032` | 已 inline |
| `acct-frequency` | `2284-27792_account-overview-desktop` | `2284:27792` | `2284:27884` | 已 inline |
| `acct-logout` | `2284-27604_account-overview` | `2284:27604` | `I2284:27648;336:35896` | 已 inline |
| `acct-modal-close` | `2284-31330_edit-name` | `2284:31330` | `I2284:31481;30:887` | 已 inline |
| `acct-note-ok` | `2284-32779_edit-shipping` | `2284:32779` | `2284:32934` | 已 inline |
| `acct-opt-chevron` | `2284-30960_edit-product` | `2284:30960` | `I2284:31124;84:8170;30:862` | **已废弃** |
| `acct-order-preparing` | `2284-27450_account-overview---above-the-fold` | `2284:27450` | `I2284:27462;426:42846` | 已 inline |
| `acct-order-renewal` | `2284-27548_account-overview---above-the-fold` | `2284:27548` | `I2284:27560;407:39877` | 已 inline |
| `acct-order-shipped` | `2284-27499_account-overview---above-the-fold` | `2284:27499` | `I2284:27511;407:39861` | 已 inline |
| `acct-payment` | `2284-27792_account-overview-desktop` | `2284:27792` | `2284:27975` | 已 inline |
| `acct-play` | `2284-29596_cancel-subscription` | `2284:29596` | `2284:29753` | 已 inline |
| `acct-plus` | `2284-27792_account-overview-desktop` | `2284:27792` | `I2284:27943;336:36087` | 已 inline |
| `acct-qty-minus` | `2284-30960_edit-product` | `2284:30960` | `I2284:31133;181:3726` | **已废弃** |
| `acct-qty-plus` | `2284-30960_edit-product` | `2284:30960` | `I2284:31141;83:7100` | **已废弃** |
| `acct-sub-renewal` | `2284-28000_account-overview-desktop` | `2284:28000` | `2284:28080` | 已 inline |
| `acct-sub-shipping` | `2284-28000_account-overview-desktop` | `2284:28000` | `2284:28085` | 已 inline |

⚠ `acct-alert` **不可用脚本重生**（bbox 裁切会带进面板自己的矩形，且珊瑚色圆盘里的叉要保持白色，
不能转 `currentColor`）。它的成品在 `account.html` 的 `.gb-acct-modal__alert` 里，整段拷走即可。

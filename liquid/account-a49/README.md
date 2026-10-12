# Account a49 — deployed 2026-09-30

Based on live `baseline-20260930-a48` (640 files), pulled 2026-09-30. These are complete copies of the latest theme snippets with the requested changes; all three were deployed to live on 2026-09-30.

| Theme path | Change | Status |
|---|---|---|
| snippets/gb-account-data.liquid | Numeric input read/write and CTA gating; both discount forms use API validation and response-driven UI | Deployed |
| snippets/gb-account-modals.liquid | Numeric quantity fields; remove automatic applied routing and hard-coded success text | Deployed |
| snippets/gb-account-placeholders.liquid | Bold pager numbers | Deployed |

Asset changes: assets/account.scss, account.css, account.js, main.js (deployed). The main.js change synchronizes custom select active state with the selected option across the site. CSS/SCSS changes are paired.

All seven files were deployed together after a fresh pull and conflict check against a48. Do not push static HTML, templates JSON, settings data or unrelated snippets. Preserve other contributors' updates. `a49.patch` provides the targeted snippet diff.

Verification: browser reproduction failed before the fix; acctfeedback (5 checks), acctfeedbackdata (14 checks, mocked API), acctcover (43 checks). No real customer API mutations or live account end-to-end test performed. Python Playwright is unavailable locally; existing Python expectations were updated but not rerun.

Readback: acctpush.py 18 ok / 0 red; 640 files total, seven byte-identical, 633 unchanged, no additions or deletions. New baseline: baseline-20260930-a49. Pre-push backup: prepush-20260930-a49.

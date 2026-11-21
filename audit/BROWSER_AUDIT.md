# Browser Lab Audit — Executed Offline, Keyboard and Responsive QA

**Source:** `docs/index.html` / `docs/lesson-config.json` / `tests/browser/offline-e2e.mjs`.  
**Verified candidate CI:** [Hardened CI 44960081116](https://github.com/mohammadrezwankhan/battery-power-models/actions/runs/44960081116), browser artifact `14729600827`.  
**Public GitHub Pages:** https://mohammadrezwankhan.github.io/battery-power-models/

The browser lab contains four guided lessons based on an idealized directly specified thermal heat input, not the native default `I²R` current specification. The UI time unit is **minutes**; equations convert to SI seconds. An education checkpoint proves consistency with an analytical reference model, not physical device calibration.

## Independently calculated checkpoints

All four presets and eight absolute-tolerance checks were independently recomputed with `T(t)=T_a+(Q/G)(1−exp(−G×60t/C_th))`, `Q_rejected=G(T−T_a)`, `E_stored=C_th(T−T_a)/1000`. Every published tolerance is **0.02** in the stated metric units.

| Module / time | Metric | Published | Independent calculation | Decision |
|---|---|---:|---:|---|
| Heat balance / 5 min | T °C | 34.481808 | 34.4818083824 | PASS |
| Heat balance / 60 min | T °C | 39.999908 | 39.9999078368 | PASS |
| Current/heat / 60 min | T °C | 84.999631 | 84.9996313473 | PASS |
| Current/heat / 60 min | Heat removed W | 1199.992627 | 1199.9926269452 | PASS |
| Cooling / 60 min | T °C | 40.000000 | 40.0000000000 | PASS |
| Cooling / 60 min | Stored kJ | 90.000000 | 90.0000000000 | PASS |
| Transfer / 10 min | T °C | 43.260066 | 43.2600655382 | PASS |
| Transfer / 10 min | Stored kJ | 495.603932 | 495.6039322945 | PASS |

HTML-embedded lesson JSON matched `docs/lesson-config.json` on baseline source review. The active JS thermal equation uses an exact exponential, not Forward Euler.

## Actual real-browser execution

Chrome was launched by GitHub Actions with remote networking disabled and loaded `docs/index.html` as `file://` in a fresh profile. A scoped DevTools test harness uses a frozen set of authored expressions, not a general-purpose user-controlled evaluator. These assertions actually passed:

| Criterion | Observed result |
|---|---|
| Offline `file://` and no network | PASS, zero external HTTP(S) requests |
| All four module tabs, four presets | PASS |
| Eight named UI checkpoints | PASS, each module reported 2/2 |
| Keyboard module arrows, End/Home, slider ArrowRight | PASS |
| Configuration dialog open, Escape and focus restoration | PASS |
| Actual downloaded CSV *contents* | PASS, 241 samples, expected header, first time=0, end time=60 min |
| Reduced-motion media preference | PASS, computed `scroll-behavior:auto`, hero transform none |
| 320, 375, 768, 1280 px widths | PASS, no horizontal page overflow |
| Uncaught JS exceptions | PASS, zero |
| External network requests | PASS, zero |

Detailed observed widths in the JSON receipt: document/viewport 320/320, 375/375, 753/768 and 1265/1280 CSS px. The public hosted site also passed a separate interactive four-module smoke test. No changes to student/user data occurred.

## Boundaries and residual UX work

The audit is a functional and focused accessibility smoke test. It is **not** a full WCAG 2.2 or screen-reader certification: cross-platform assistive technology, zoom at 400%, every graphic's contrast and color-vision modes have not been independently certified. A targeted computed text-contrast regression is incorporated in the final QA proposal; it must pass the same GitHub Actions job before merge. Native browser tests are independent of tool-name claims and do not establish physical battery or capacitor safety.

## Run locally

Requires modern Node (tested Node 24) and Chrome/Chromium available at a standard Linux path or through `CHROME_BIN`:

`node tests/browser/offline-e2e.mjs`

The script deliberately fails if Chrome is missing, a checkpoint is wrong, a CSV row is wrong, a keyboard flow breaks, an external request occurs, a script exception is thrown or responsive overflow is detected. It saves `hardening-artifacts/browser-offline-qa.json` with pass/fail evidence. Headless test output never silently substitutes for an inaccessible browser.

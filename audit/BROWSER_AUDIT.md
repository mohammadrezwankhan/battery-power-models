# Browser Lab Audit — Four Modules, Numerical Checkpoints, and Accessibility

Reviewed sources: `docs/index.html`, `docs/lesson-config.json`, `docs/lesson-config.schema.json`, `tests/browser/csp.test.mjs`, `scripts/browser-csp.mjs`. Public Pages: https://mohammadrezwankhan.github.io/battery-power-models/. Read-only live browser test completed 2026-11-21. No user data was collected and no repository changes were made by the browser.

## Model and numerical provenance

The embedded JSON lesson config in HTML was parsed and checked for exact JSON structure equality with `docs/lesson-config.json`: **equal at baseline**. The active browser lesson uses illustrative *direct heat input* in watts, time in **minutes** with factor 60 to convert to SI seconds, fixed ambient starting temperature, and thermal capacitance in J/K. It is related to but not identical in parameter defaults or current-to-heat mapping with the native Python cell model. Browser JS thermal source includes `delta = heatW/coolingWK * (1 - Math.exp(-coolingWK*t*60/capacityJPerK))`, the exact first-order exponential prediction. This is not Forward Euler. Browser numerical code also includes additional demonstrator model families that are not the advertised two native solver families; do not misstate native model count as number of browser modules.

## Independent checkpoint reconstruction

Used `T(t)=Ta+(Q/G)(1−exp(−G×60t/C))`, `removed=G(T−Ta)`, and `stored=(T−Ta)C/1000`. Values below computed independently from each module preset; tolerance is 0.02 absolute in the individual metric units as specified in the embedded config.

| Module | Preset Q/G/C/Ta | Check at time | Metric | Published expected | Independently computed | Within tol |
|---|---|---|---|---:|---:|---|
| 1: heat balance | 300 W /20 W·K⁻¹/6000 J·K⁻¹/25°C | 5 min | temperature °C | 34.481808 | 34.4818083824 | PASS |
| 1 | same | 60 min | temperature °C | 39.999908 | 39.9999078368 | PASS |
| 2: Joule heat | 1200 W /20/6000/25 | 60 min | temperature °C | 84.999631 | 84.9996313473 | PASS |
| 2 | same | 60 min | removed W | 1199.992627 | 1199.9926269452 | PASS |
| 3: cooling | 1200 W /80/6000/25 | 60 min | temperature °C | 40.000000 | 40.0000000000 | PASS |
| 3 | same | 60 min | stored kJ | 90.000000 | 90.0000000000 | PASS |
| 4: transfer to DC | 1200 W /80/60000/35 | 10 min | temperature °C | 43.260066 | 43.2600655382 | PASS |
| 4 | same | 10 min | stored kJ | 495.603932 | 495.6039322945 | PASS |

All eight numerical checkpoint values agree; no tolerance was widened.

## Read-only interactive browser QA

A separate live browser session loaded the public GitHub Pages site and interacted with the interface. Confirmed: all four modules selectable; each module's `Load lesson preset` responds and updates the heat, cooling, capacity and ambient controls; `Check outcomes` is responsive; chart and axis labels render; metric tabs switch; model assumptions disclosure opens; source-oriented actions and desktop layout show no obvious clipping. This is a smoke test, not a full Playwright axe-core audit. It did not inspect every checkpoint verdict from DOM assertions or export each CSV payload.

| Check | Status | Evidence and limitations |
|---|---|---|
| Four module tabs | PASS | individually clicked in browser |
| Four preset buttons | PASS | each clicked, controls update |
| Outcome-check action | PASS functional | click responds; full per-checkpoint UI assertion not performed |
| Chart visibility / desktop spacing | PASS smoke | chart labels/axes and panel visible, no observed overflow |
| Source JS math parity | PASS source | closed-form thermal source inspected |
| Source JSON parity | PASS source | embedded vs external JSON structurally equal |
| Live-file `file://` offline / no network | BLOCKED | not performed; site badge "offline ready" is a claim, not evidence |
| GitHub Pages relative assets | PARTIAL | public deployed site renders; full case-sensitive link crawler not performed |
| Keyboard navigation and sliders | PARTIAL | one Tab pressed, no complete focus traversal |
| Mobile viewport | BLOCKED | no mobile resize exercised |
| Reduced motion | PARTIAL | CSS `@media(prefers-reduced-motion: reduce)` found and anim suppression present; preference emulation and actual computed-style assertion not run |
| Exported CSV schema and values | PARTIAL | export control visible, downloaded bytes not independently checked |
| Console errors | PARTIAL | no visible page exceptions, browser console API inspection not performed |
| External CDN dependencies | PARTIAL | source architecture appears inline/offline-first; real network trace not captured |

## Recommended machine-executable checks

1. Open `docs/index.html` from a clean checkout as file:// with network fully disabled, load all four presets, check checkpoints and exports.
2. Repeat under GitHub Pages relative directory hosting and exercise all intra-site links.
3. Run keyboard-only tab order, Enter/Space activation, slider arrow keys and dialog Escape.
4. At viewport widths 320, 375, 768 and 1280 px, capture chart and control overlap.
5. Emulate `prefers-reduced-motion: reduce` and inspect computed animation/transition durations; require static engineering quantities to remain visible.
6. Parse exported CSV rows, units, sample count, timestamp semantics and JSON export values.
7. Record failed network requests, console exceptions and WCAG contrast/focus evidence.

**Claim boundary:** Passing educational checkpoints validates consistency with a synthetic model; it is not field calibration, thermal safety evidence or power-electronics hardware certification.

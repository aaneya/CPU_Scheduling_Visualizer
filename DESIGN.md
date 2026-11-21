# Design System: CPU Scheduling Studio

**Project:** CPU Scheduling Visualizer & Performance Analyzer
**Aesthetic direction:** Technical / Academic — "a well-set lab handout, not a SaaS landing page"

---

## 1. Visual Theme & Atmosphere

The interface should read like a **printed academic report that happens to be interactive**. Paper-white surfaces, ink-black text, hairline rules, and a single navy accent. No gradients, no glass, no floating cards, no neon. Visual hierarchy comes from **typography and spacing**, not from shadows or color blocks. Data — especially the Gantt chart — is the ornament.

Keywords: *restrained, legible, reproducible, instrument-like, calm.*

**Explicitly avoided:** radial gradients, glassmorphism, pill badges, hover-lift cards, neon cyan/purple accents, Space Grotesk, emoji-led navigation, "AI dashboard" template look.

---

## 2. Color Palette & Roles

| Descriptive name | Hex | Role |
|---|---|---|
| Warm paper white | `#FBFAF7` | App background |
| Pure sheet | `#FFFFFF` | Panels, charts, tables |
| Ink black | `#1A1A1A` | Headings, primary text |
| Graphite | `#5F5F5F` | Body text, secondary labels |
| Faint graphite | `#8A8A8A` | Captions, axis ticks |
| Hairline rule | `#DAD5C9` | Borders, dividers, table rules |
| Strong rule | `#B9B2A3` | Axis lines, emphasized rules |
| Academic navy | `#1F4E79` | Primary accent, buttons, active nav |
| Wash blue | `#EAF0F6` | Selected rows, quiet callouts |
| Moss green | `#3F6B4F` | "Best" metric highlight |
| Ochre | `#8C5A1B` | Warnings, idle CPU |
| Brick red | `#8C2F1B` | Errors, invalid input |

**Chart palette (muted, print-safe):**
`#1F4E79` · `#2E75B6` · `#A6611A` · `#4D7C5F` · `#7F5A83` · `#B08D57` · `#6B7B8C` · `#9C4A3C`
Idle CPU is always `#B9B2A3`.

---

## 3. Typography Rules

| Role | Family | Weight / size | Notes |
|---|---|---|---|
| Display / H1 | Source Serif 4, Georgia, serif | 600, 2.1–2.3rem | Tight tracking (-0.01em) |
| Section / H2 | Source Serif 4, Georgia, serif | 600, 1.35rem | Followed by a hairline rule |
| Subsection / H3 | Source Serif 4, Georgia, serif | 600, 1.05rem | |
| Body | Inter, system sans | 400, 0.95rem / 1.6 | Max line length ~72ch |
| Labels / kickers | IBM Plex Mono | 500, 0.68rem, uppercase | Letter-spacing 0.14em |
| Data / tables / axes | IBM Plex Mono | 400–500, 0.8–0.9rem | `font-variant-numeric: tabular-nums` |

Rule: **serif for prose and headings, mono for anything numeric or machine-like, sans only for body copy.**

---

## 4. Component Stylings

- **Stat blocks:** no card. A 2px ink top rule, mono uppercase label, serif 1.8rem value, mono note. Sits directly on paper.
- **Panels:** `#FFFFFF`, 1px `#DAD5C9` border, 2px radius, **no shadow**.
- **Buttons:** solid `#1F4E79`, white text, 2px radius, mono uppercase 0.72rem, 0.14em tracking. Hover darkens to `#173B5C`; no lift, no glow.
- **Inputs / selectboxes:** white fill, 1px hairline border, 2px radius, navy focus ring (2px offset).
- **Tabs:** text-only, mono uppercase; active tab gets a 2px navy bottom border. No filled pills.
- **Tables:** 1px hairline rules, mono numerals, white header with uppercase mono labels; no zebra striping.
- **Alerts:** 3px left border in the semantic color, `#FBFAF7` fill, no icon noise.
- **Sidebar:** paper background, 1px right rule, mono "CONTENTS" label, plain radio list, dataset summary in mono.
- **Footer:** mono 0.68rem, muted, separated by a hairline.

---

## 5. Layout Principles

- Content column: max-width **1120px**, centered, 2.5rem top / 4rem bottom padding.
- 8pt spacing scale: 4 / 8 / 12 / 16 / 24 / 32 / 48.
- Stats in a 4-column grid (2 on narrow screens), separated by vertical hairlines rather than cards.
- **The Gantt chart is the hero** of the Overview and Simulator pages — full content width, directly under the stats.
- One primary action per page. Secondary actions are outlined buttons, not filled.
- Whitespace is the main separator; rules are the second.

---

## 6. Data Visualization Rules

- White paper and plot backgrounds; hairline grid `#E7E2D8`; axis lines `#B9B2A3`.
- Muted palette only; no default Plotly colors.
- Titles in serif, left-aligned; axis labels and ticks in mono, 10–11px.
- No chartjunk: no background fills, no 3D, no drop shadows, no rainbow scales.
- Gantt: one row, 1px white separators between slices, process ID inside the block in mono, gray idle blocks, hover shows start / end / duration.
- Annotate directly where possible instead of relying on legends.

---

## 7. Motion & Interaction

- Allowed: 120ms ease on color and border only.
- Disallowed: translate/lift, scale, glow, gradient shifts, entrance animations.
- Interactivity lives in the data: Plotly hover, zoom, pan, and Streamlit controls.

---

## 8. References

- **Tufte CSS** — Edward Tufte / Dave Liepmann: well-set typography, sidenotes, tight integration of graphics. https://edwardtufte.github.io/tufte-css/
- **Distill.pub** — academic journal layout for interactive science.
- **Our World in Data** — data-first charts, restrained color, direct labelling.
- **Observable** — interactive notebooks and exploratory dashboards.
- **Linear** — professional minimal UI, hairline borders, restrained accent.
- **Grafana** — technical dashboards, mono numerals, dense tables.
- **arXiv** — document-like reading rhythm and section rules.

---

## 9. Implementation Notes (Streamlit)

Design tokens live in the `CSS` string at the top of `app.py`:

```css
:root{
  --paper:#FBFAF7; --surface:#FFFFFF; --ink:#1A1A1A; --muted:#5F5F5F;
  --faint:#8A8A8A; --rule:#DAD5C9; --rule-strong:#B9B2A3;
  --accent:#1F4E79; --accent-dark:#173B5C; --wash:#EAF0F6;
  --ok:#3F6B4F; --warn:#8C5A1B; --bad:#8C2F1B;
}
```

- Headings: `font-family:'Source Serif 4',Georgia,serif`.
- Labels and numerals: `font-family:'IBM Plex Mono',monospace; font-variant-numeric:tabular-nums`.
- Sidebar: `[data-testid="stSidebar"]{background:var(--paper);border-right:1px solid var(--rule)}`.
- Tables: `[data-testid="stDataFrame"]{border:1px solid var(--rule);border-radius:2px}`.
- Charts: every Plotly figure passes through `style_fig()` in `app.py` or `make_gantt()` in `utils/gantt_chart.py`.

**Rule of thumb:** if a new component would need a shadow or a gradient to look right, it does not belong in this system.

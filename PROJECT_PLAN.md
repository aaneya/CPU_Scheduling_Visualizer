# CPU Scheduling Studio — Team Project Plan

**Repo:** https://github.com/aaneya/CPU_Scheduling_Visualizer  
**Stack:** Streamlit + Plotly + Pandas, Python 3.10+  
**Team size:** 3 members  
**Status:** MVP complete and pushed to `main`  

---

## 1. What has been done (complete to date)

| Area | Deliverable | Status |
|------|-------------|--------|
| **Core engine** | `algorithms/_common.py` — shared validation + non-preemptive scheduler | ✅ Done |
| **Algorithms** | `fcfs.py`, `sjf.py`, `priority.py`, `round_robin.py`, `srtf.py` (preemptive SJF) | ✅ Done |
| **Priority aging** | Optional starvation-prevention boost in `priority.py` | ✅ Done |
| **Metrics** | `utils/metrics.py` — WT, TAT, RT, CPU utilization, throughput, context switches | ✅ Done |
| **Gantt charts** | `utils/gantt_chart.py` — Plotly interactive Gantt, stable per-PID colors, gray idle blocks | ✅ Done |
| **Dashboard** | `app.py` — Streamlit app, 6 pages: Overview, Workload, Simulator, Analysis, Compare, About | ✅ Done |
| **Navigation** | Top header nav bar (replaced fragile sidebar) | ✅ Done |
| **Workload editing** | Inline data editor: add/delete rows, edit cells, load samples, generate random, import/export CSV | ✅ Done |
| **All-four view** | Run all policies at once: 4 Gantt traces, comparison table, per-process tabs, CSV downloads | ✅ Done |
| **Design system** | `DESIGN.md` — academic/technical theme (paper white, serif headings, mono data, navy accent) | ✅ Done |
| **Theme config** | `.streamlit/config.toml` — light theme, navy primary, paper background | ✅ Done |
| **Tests** | `tests/test_algorithms.py` + `tests/test_metrics.py` — 18 pytest cases (traces, validation, metrics) | ✅ Done |
| **CI** | `.github/workflows/ci.yml` — pytest on every push / PR via GitHub Actions | ✅ Done |
| **README** | `README.md` — setup, usage, screenshots, tech stack, teammate roles, test instructions | ✅ Done |
| **Screenshots** | `docs/screenshots/` — real captured images of Overview, Workload, Simulator, Compare | ✅ Done |
| **PDF** | `CPU_Scheduling_Studio_Capstone_Project.pdf` — 10-page capstone document | ✅ Done |
| **GitHub** | Repo `aaneya/CPU_Scheduling_Visualizer`, CI green, all commits on `main` | ✅ Done |

---

## 2. Team task division (3 members)

### Member A — Algorithms & Core Engine
**Files:** `algorithms/`, `utils/metrics.py`, `tests/test_algorithms.py`

- Maintain correctness of FCFS, SJF, SRTF, Priority, Round Robin
- Verify exact execution traces against hand calculations
- Add optional preemptive Priority / aging parameters
- Document pseudocode + Big-O for each policy
- Ensure `validate()` catches empty input, negative arrival, zero burst, duplicate PID
- Keep algorithms UI-free (importable, testable without Streamlit)

### Member B — Frontend UI & Visualization
**Files:** `app.py`, `utils/gantt_chart.py`, `DESIGN.md`, `.streamlit/`, `docs/screenshots/`

- Maintain the 6-page Streamlit dashboard
- Gantt chart styling, per-PID color stability, idle-block rendering
- Header navigation + page layout (stat blocks, tables, tabs)
- Academic design tokens (paper background, serif headings, mono data, navy accent)
- Regenerate screenshots in `docs/screenshots/` after UI changes
- Keep Streamlit toolbar hidden, no broken sidebar dependencies

### Member C — Testing, CI & Documentation
**Files:** `tests/`, `.github/workflows/ci.yml`, `README.md`, `PROJECT_PLAN.md`, `CPU_Scheduling_Studio_Capstone_Project.pdf`

- Run `pytest -q` locally before every push
- Keep GitHub Actions CI green (18 tests passing)
- Add new pytest cases whenever a feature changes
- Update README usage steps, screenshots, and teammate roles
- Regenerate the capstone PDF when scope changes
- Handle repo hygiene: commits, branch protection, issues tracker

---

## 3. Suggested weekly script (4-week capstone sprint)

### Week 1 — Foundation & engine
- [ ] Member A: Pin down algorithm traces, write `validate()`, add tests
- [ ] Member B: Scaffold 6 pages, header nav, Gantt chart on Overview
- [ ] Member C: Set up GitHub repo, CI workflow, requirements files

**Week 1 demo:** Run one algorithm, see one Gantt chart, CI passes.

### Week 2 — Workload & comparison
- [ ] Member A: Add SRTF + priority aging, extend algorithm tests
- [ ] Member B: Editable workload table, CSV import/export, all-four view
- [ ] Member C: Write metric definitions, update README with screenshots

**Week 2 demo:** Edit processes by hand, run all 4 algorithms side by side.

### Week 3 — Polish & testing
- [ ] Member A: Edge-case tests (idle CPU, quantum=1, all-same-burst)
- [ ] Member B: Design polish (DESIGN.md tokens, screenshots, no broken sidebar)
- [ ] Member C: 100% test pass rate on CI, capstone PDF draft

**Week 3 demo:** Full dashboard, 18 tests green, PDF ready.

### Week 4 — Capstone finish
- [ ] All: Viva prep (be ready to explain every trace + metric formula)
- [ ] Member C: Finalize PDF, protect `main` branch, submit repo link
- [ ] All: Record a 3-minute walkthrough video (optional but recommended)

**Week 4 demo:** Complete project deployed, repo link submitted.

---

## 4. How to run the project

```bash
# 1. Clone
git clone https://github.com/aaneya/CPU_Scheduling_Visualizer.git
cd CPU_Scheduling_Visualizer

# 2. Environment
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

# 3. Install
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt   # for tests

# 4. Run dashboard
streamlit run app.py
# Open http://localhost:8501

# 5. Run tests
pytest -q
```

---

## 5. Repo structure

```
CPU_Scheduling_Visualizer/
├── app.py                      # Streamlit dashboard (all 6 pages + header nav)
├── DESIGN.md                   # Design system: tokens, type, components
├── README.md                   # Setup, usage, screenshots, roles
├── PROJECT_PLAN.md             # This file
├── requirements.txt            # streamlit>=1.50, plotly, pandas, numpy
├── requirements-dev.txt        # + pytest
├── .gitignore                  # venv, __pycache__, .DS_Store, .pytest_cache
├── .streamlit/
│   └── config.toml             # Light academic theme
├── .github/
│   └── workflows/ci.yml        # pytest on push / PR
├── docs/
│   └── screenshots/            # Overview, workload, simulator, compare
├── tests/
│   ├── test_algorithms.py      # FCFS/SJF/SRTF/Priority/RR traces + validation
│   └── test_metrics.py         # WT/TAT/RT, utilization, switches
├── algorithms/
│   ├── __init__.py             # ALGORITHMS registry (FCFS, SJF, SRTF, Priority, RR)
│   ├── _common.py              # validate() + schedule_nonpreemptive()
│   ├── fcfs.py
│   ├── sjf.py
│   ├── srtf.py                 # preemptive SJF
│   ├── priority.py             # non-preemptive + optional aging
│   └── round_robin.py          # preemptive, configurable quantum
└── utils/
    ├── __init__.py
    ├── gantt_chart.py          # Plotly Gantt, stable PID colors
    └── metrics.py              # WT/TAT/RT, utilization, throughput, switches
```

---

## 6. Viva / demo talking points

- **FCFS:** `P1(0-5) → P2(5-8) → ...` — convoy effect example
- **SJF:** Shortest burst first among arrived jobs — minimizes avg waiting
- **SRTF:** Preemptive SJF — new shorter job interrupts running job
- **Priority:** Lower number = higher priority; aging prevents starvation
- **Round Robin:** Time-slice rotation — bounded response time
- **Metrics:** WT = TAT − burst; TAT = completion − arrival; RT = first start − arrival
- **Utilization:** busy time ÷ (last completion − first arrival) × 100
- **Context switches:** direct transitions between two different non-idle processes
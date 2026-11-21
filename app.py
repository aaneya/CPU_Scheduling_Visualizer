from __future__ import annotations

import random

import pandas as pd
import plotly.express as px
import streamlit as st

from algorithms import ALGORITHMS
from algorithms._common import validate
from utils.gantt_chart import PALETTE, make_gantt
from utils.metrics import calculate_metrics

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="CPU Scheduling Studio",
    page_icon="§",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# Academic / technical stylesheet — tokens documented in DESIGN.md
# ----------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root{
  --paper:#FBFAF7; --surface:#FFFFFF; --ink:#1A1A1A; --muted:#5F5F5F;
  --faint:#8A8A8A; --rule:#DAD5C9; --rule-strong:#B9B2A3;
  --accent:#1F4E79; --accent-dark:#173B5C; --wash:#EAF0F6;
  --ok:#3F6B4F; --warn:#8C5A1B; --bad:#8C2F1B;
}

html, body, .stApp{background:var(--paper); color:var(--ink);}
.stApp{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;}
[data-testid="stHeader"]{background:transparent;}
[data-testid="stToolbar"]{display:none;}
[data-testid="stDecoration"]{display:none;}
#MainMenu{visibility:hidden;}
.block-container{max-width:1120px; padding:2.5rem 2rem 4rem;}

h1,h2,h3,h4{font-family:'Source Serif 4',Georgia,serif !important; color:var(--ink) !important; font-weight:600 !important;}
h1{font-size:2.15rem; letter-spacing:-.01em; margin:.15rem 0 .35rem !important;}
h2{font-size:1.35rem; border-bottom:1px solid var(--rule); padding-bottom:.35rem; margin-top:2rem !important;}
h3{font-size:1.05rem; margin-top:1.4rem !important;}
p, li{font-size:.95rem; line-height:1.6; color:var(--muted);}
a{color:var(--accent); text-decoration:none; border-bottom:1px solid var(--rule-strong);}

/* page header */
.page-head{border-bottom:1px solid var(--rule); padding-bottom:1.1rem; margin-bottom:1.6rem;}
.kicker{font-family:'IBM Plex Mono',monospace; font-size:.68rem; letter-spacing:.14em;
  text-transform:uppercase; color:var(--accent); margin-bottom:.35rem;}
.lede{color:var(--muted); font-size:.95rem; margin:.1rem 0 0; max-width:72ch;}

/* stat blocks — rules, not cards */
.stat{border-top:2px solid var(--ink); padding:.65rem 0 0;}
.stat-label{font-family:'IBM Plex Mono',monospace; font-size:.66rem; letter-spacing:.12em;
  text-transform:uppercase; color:var(--faint);}
.stat-value{font-family:'Source Serif 4',Georgia,serif; font-size:1.75rem; font-weight:600;
  color:var(--ink); line-height:1.2; margin:.2rem 0 .1rem; font-variant-numeric:tabular-nums;}
.stat-note{font-family:'IBM Plex Mono',monospace; font-size:.66rem; color:var(--faint);}

/* panels */
.panel{background:var(--surface); border:1px solid var(--rule); border-radius:2px;
  padding:1.1rem 1.25rem; margin:.5rem 0 1rem;}
.panel p:last-child{margin-bottom:0;}

/* sidebar */
[data-testid="stSidebar"]{background:var(--paper); border-right:1px solid var(--rule);}
[data-testid="stSidebar"] .block-container{padding:1.4rem 1.1rem;}
[data-testid="stSidebar"] [role="radiogroup"] label{font-family:'IBM Plex Mono',monospace;
  font-size:.74rem; color:var(--muted); padding:.12rem 0;}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{color:var(--accent);}
.monogram{display:inline-block; font-family:'IBM Plex Mono',monospace; font-size:.72rem;
  letter-spacing:.08em; color:var(--accent); border:1px solid var(--accent);
  padding:.2rem .45rem; margin-bottom:.7rem;}
.side-title{font-family:'Source Serif 4',Georgia,serif; font-size:1.15rem; font-weight:600;
  color:var(--ink); line-height:1.25;}
.side-sub{font-family:'IBM Plex Mono',monospace; font-size:.64rem; letter-spacing:.1em;
  text-transform:uppercase; color:var(--faint); margin:.25rem 0 1.4rem;}
.side-label{font-family:'IBM Plex Mono',monospace; font-size:.64rem; letter-spacing:.14em;
  text-transform:uppercase; color:var(--faint); margin:.4rem 0 .35rem;}
.side-meta{font-family:'IBM Plex Mono',monospace; font-size:.72rem; color:var(--muted);
  line-height:1.7;}

/* controls */
.stButton > button{border-radius:2px; font-family:'IBM Plex Mono',monospace;
  font-size:.7rem; letter-spacing:.08em; text-transform:uppercase; min-height:38px;
  transition:background-color .12s ease, border-color .12s ease;}
.stButton > button[kind="primary"]{background:var(--accent); border:1px solid var(--accent);}
.stButton > button[kind="primary"] p{color:#fff !important;}
.stButton > button[kind="primary"]:hover{background:var(--accent-dark); border-color:var(--accent-dark);}
.stButton > button[kind="primary"]:hover p{color:#fff !important;}
.stButton > button[kind="secondary"]{background:transparent; border:1px solid var(--rule-strong);}
.stButton > button[kind="secondary"] p{color:var(--ink) !important;}
.stButton > button[kind="secondary"]:hover{border-color:var(--accent); background:var(--wash);}
.stButton > button[kind="secondary"]:hover p{color:var(--accent) !important;}
[data-testid="stSelectbox"] label, [data-testid="stNumberInput"] label{
  font-family:'IBM Plex Mono',monospace; font-size:.66rem; letter-spacing:.1em;
  text-transform:uppercase; color:var(--faint);}
[data-baseweb="select"] > div, [data-testid="stNumberInput"] input{
  border-radius:2px !important; border-color:var(--rule-strong) !important; background:var(--surface) !important;}
[data-baseweb="select"] > div:focus-within, [data-testid="stNumberInput"] input:focus{
  border-color:var(--accent) !important; box-shadow:0 0 0 1px var(--accent) !important;}

/* tabs — text with an underline, not pills */
.stTabs [data-baseweb="tab-list"]{gap:1.4rem; border-bottom:1px solid var(--rule);}
.stTabs [data-baseweb="tab"]{background:transparent; border-radius:0; padding:.45rem 0;
  font-family:'IBM Plex Mono',monospace; font-size:.7rem; letter-spacing:.08em;
  text-transform:uppercase; color:var(--faint);}
.stTabs [aria-selected="true"]{color:var(--accent) !important; border-bottom:2px solid var(--accent);}

/* tables */
[data-testid="stDataFrame"]{border:1px solid var(--rule); border-radius:2px; overflow:hidden;}
[data-testid="stDataFrame"] *{font-family:'IBM Plex Mono',monospace !important; font-size:.78rem !important;}

/* markdown tables */
[data-testid="stMarkdownContainer"] table{width:100%; border-collapse:collapse; margin:.9rem 0;}
[data-testid="stMarkdownContainer"] th{text-align:left; font-family:'IBM Plex Mono',monospace;
  font-size:.66rem; letter-spacing:.08em; text-transform:uppercase; font-weight:500;
  color:var(--faint); border-bottom:1px solid var(--rule-strong); padding:.45rem .6rem;}
[data-testid="stMarkdownContainer"] td{font-family:'IBM Plex Mono',monospace; font-size:.78rem;
  color:var(--muted); border-bottom:1px solid var(--rule); padding:.45rem .6rem;}

/* alerts */
[data-testid="stAlert"]{border-radius:2px; border:1px solid var(--rule); border-left:3px solid var(--accent);
  background:var(--paper); font-family:'IBM Plex Mono',monospace; font-size:.78rem;}
[data-testid="stAlert"][data-baseweb="notification"]{color:var(--muted);}

hr{border:none; border-top:1px solid var(--rule); margin:1.6rem 0;}
.footer{font-family:'IBM Plex Mono',monospace; font-size:.66rem; color:var(--faint);
  border-top:1px solid var(--rule); padding-top:.8rem; margin-top:3rem; letter-spacing:.04em;}
.note{font-family:'IBM Plex Mono',monospace; font-size:.7rem; color:var(--faint); line-height:1.6;}
.def{font-family:'IBM Plex Mono',monospace; font-size:.78rem; color:var(--muted); line-height:1.8;}
.def b{color:var(--ink); font-weight:500;}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Sample workloads
# ----------------------------------------------------------------------------
SAMPLES = {
    "Basic": [
        {"Process": "P1", "Arrival Time": 0, "Burst Time": 5, "Priority": 2},
        {"Process": "P2", "Arrival Time": 1, "Burst Time": 3, "Priority": 1},
        {"Process": "P3", "Arrival Time": 2, "Burst Time": 8, "Priority": 3},
        {"Process": "P4", "Arrival Time": 3, "Burst Time": 6, "Priority": 2},
    ],
    "Same arrival": [
        {"Process": "P1", "Arrival Time": 0, "Burst Time": 7, "Priority": 3},
        {"Process": "P2", "Arrival Time": 0, "Burst Time": 3, "Priority": 1},
        {"Process": "P3", "Arrival Time": 0, "Burst Time": 5, "Priority": 2},
        {"Process": "P4", "Arrival Time": 0, "Burst Time": 2, "Priority": 4},
    ],
    "Idle periods": [
        {"Process": "P1", "Arrival Time": 2, "Burst Time": 3, "Priority": 2},
        {"Process": "P2", "Arrival Time": 3, "Burst Time": 2, "Priority": 1},
        {"Process": "P3", "Arrival Time": 9, "Burst Time": 4, "Priority": 3},
    ],
    "Round Robin demo": [
        {"Process": "P1", "Arrival Time": 0, "Burst Time": 8, "Priority": 2},
        {"Process": "P2", "Arrival Time": 1, "Burst Time": 4, "Priority": 1},
        {"Process": "P3", "Arrival Time": 2, "Burst Time": 5, "Priority": 3},
        {"Process": "P4", "Arrival Time": 4, "Burst Time": 2, "Priority": 2},
    ],
}

PAGES = [
    "Overview",
    "Workload",
    "Simulator",
    "Analysis",
    "Compare",
    "About",
]

# ----------------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------------
if "processes" not in st.session_state:
    st.session_state.processes = SAMPLES["Basic"]
if "algorithm" not in st.session_state:
    st.session_state.algorithm = "FCFS"
if "quantum" not in st.session_state:
    st.session_state.quantum = 2
if "page" not in st.session_state:
    st.session_state.page = "Overview"
if "show_all" not in st.session_state:
    st.session_state.show_all = False

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def run(algo, processes=None, quantum=None):
    data = processes if processes is not None else st.session_state.processes
    fn = ALGORITHMS[algo]
    if algo == "Round Robin":
        return fn(data, quantum or st.session_state.quantum)
    return fn(data)


def simulation(algo=None):
    algo = algo or st.session_state.algorithm
    result = run(algo)
    table, summary = calculate_metrics(st.session_state.processes, result)
    return result, table, summary


def header(kicker, title, subtitle=""):
    st.markdown(
        f'<div class="page-head"><div class="kicker">{kicker}</div>'
        f"<h1>{title}</h1><p class=\"lede\">{subtitle}</p></div>",
        unsafe_allow_html=True,
    )


def stat(label, value, note=""):
    st.markdown(
        f'<div class="stat"><div class="stat-label">{label}</div>'
        f'<div class="stat-value">{value}</div>'
        f'<div class="stat-note">{note}</div></div>',
        unsafe_allow_html=True,
    )


def stat_row(items):
    cols = st.columns(len(items))
    for col, (label, value, note) in zip(cols, items):
        with col:
            stat(label, value, note)


def style_fig(fig, height=None):
    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="IBM Plex Mono, monospace", size=11, color="#5F5F5F"),
        title=dict(
            font=dict(family="Source Serif 4, Georgia, serif", size=15, color="#1A1A1A"),
            x=0,
            xanchor="left",
        ),
        margin=dict(l=52, r=20, t=52, b=46),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10), title=None),
        xaxis=dict(gridcolor="#E7E2D8", linecolor="#B9B2A3", zeroline=False,
                   tickfont=dict(family="IBM Plex Mono, monospace", size=10, color="#8A8A8A")),
        yaxis=dict(gridcolor="#E7E2D8", linecolor="#B9B2A3", zeroline=False,
                   tickfont=dict(family="IBM Plex Mono, monospace", size=10, color="#8A8A8A")),
    )
    if height:
        fig.update_layout(height=height)
    return fig


def show_gantt(result, key=None):
    st.plotly_chart(
        make_gantt(result["segments"]),
        width="stretch",
        key=key,
        config={"displaylogo": False, "scrollZoom": True},
    )


def show_timeline(result):
    rows = [
        {
            "Process": s["pid"],
            "Start": s["start"],
            "End": s["end"],
            "Duration": s["end"] - s["start"],
        }
        for s in result["segments"]
    ]
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)


def show_metrics(summary):
    stat_row(
        [
            ("Avg waiting", f"{summary['Average Waiting Time']:.2f}", "time units"),
            ("Avg turnaround", f"{summary['Average Turnaround Time']:.2f}", "time units"),
            ("Avg response", f"{summary['Average Response Time']:.2f}", "time units"),
        ]
    )
    st.write("")
    stat_row(
        [
            ("CPU utilization", f"{summary['CPU Utilization']:.1f}%", "busy / elapsed"),
            ("Throughput", f"{summary['Throughput']:.3f}", "processes / unit"),
            ("Context switches", str(summary["Context Switches"]), "between bursts"),
        ]
    )


METRICS = [
    "Average Waiting Time",
    "Average Turnaround Time",
    "Average Response Time",
    "CPU Utilization",
    "Throughput",
    "Context Switches",
]
LOWER_IS_BETTER = {
    "Average Waiting Time",
    "Average Turnaround Time",
    "Average Response Time",
    "Context Switches",
}


def clean_records(edited):
    """Normalise a data-editor frame into process dicts."""
    frame = edited.dropna(how="all").copy()
    records = []
    for _, row in frame.iterrows():
        pid = str(row.get("Process", "") or "").strip()
        if not pid:
            continue
        records.append(
            {
                "Process": pid,
                "Arrival Time": int(row["Arrival Time"]) if pd.notna(row["Arrival Time"]) else 0,
                "Burst Time": int(row["Burst Time"]) if pd.notna(row["Burst Time"]) else 0,
                "Priority": int(row["Priority"]) if pd.notna(row["Priority"]) else 0,
            }
        )
    return records


def collect_all():
    """Run all four policies on the current workload."""
    results = {}
    rows = []
    for algo in ALGORITHMS:
        res = run(algo)
        tbl, summ = calculate_metrics(st.session_state.processes, res)
        results[algo] = (res, tbl, summ)
        rows.append({"Algorithm": algo, **summ})
    return results, pd.DataFrame(rows)


def render_all_traces(results):
    cols = st.columns(2)
    for i, (algo, (res, _, summ)) in enumerate(results.items()):
        with cols[i % 2]:
            st.markdown(f"#### {algo}")
            st.markdown(
                f'<div class="note">avg waiting {summ["Average Waiting Time"]:.2f} · '
                f'avg turnaround {summ["Average Turnaround Time"]:.2f} · '
                f'avg response {summ["Average Response Time"]:.2f}</div>',
                unsafe_allow_html=True,
            )
            show_gantt(res, key=f"gantt_all_{algo}")


def styled_comparison(comp):
    def mark_best(series):
        target = series.min() if series.name in LOWER_IS_BETTER else series.max()
        return [
            "font-weight:600; color:#1F4E79;" if v == target else "color:#5F5F5F;"
            for v in series
        ]

    return (
        comp.set_index("Algorithm")[METRICS]
        .style.format("{:.2f}")
        .apply(mark_best, subset=METRICS, axis=0)
    )


def process_editor(key="process_editor", heading="## Process table"):
    st.markdown(heading)
    st.caption(
        "Edit any cell, add rows, or delete rows. Process IDs must be unique; "
        "arrival ≥ 0 and burst > 0. Click Apply to recalculate every page."
    )
    frame = pd.DataFrame(
        st.session_state.processes,
        columns=["Process", "Arrival Time", "Burst Time", "Priority"],
    )
    edited = st.data_editor(
        frame,
        num_rows="dynamic",
        width="stretch",
        hide_index=True,
        key=key,
        column_config={
            "Process": st.column_config.TextColumn(required=True),
            "Arrival Time": st.column_config.NumberColumn(min_value=0, step=1, required=True),
            "Burst Time": st.column_config.NumberColumn(min_value=1, step=1, required=True),
            "Priority": st.column_config.NumberColumn(step=1, required=True),
        },
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            "Apply changes & recalculate",
            key=f"{key}_apply",
            type="primary",
            width="stretch",
        ):
            try:
                records = clean_records(edited)
                validate(records)
                st.session_state.processes = records
                st.session_state.show_all = True
                st.success(
                    f"Applied {len(records)} processes. All results now use the new values."
                )
            except Exception as exc:
                st.error(str(exc))
    with c2:
        st.download_button(
            "Download workload CSV",
            data=pd.DataFrame(st.session_state.processes).to_csv(index=False).encode(),
            file_name="workload.csv",
            mime="text/csv",
            key=f"{key}_download",
            width="stretch",
        )


# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div class="monogram">CS</div>'
        '<div class="side-title">CPU Scheduling Studio</div>'
        '<div class="side-sub">Operating Systems Lab</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="side-label">Contents</div>', unsafe_allow_html=True)
    page = st.radio(
        "Contents",
        PAGES,
        index=PAGES.index(st.session_state.page),
        label_visibility="collapsed",
    )
    st.session_state.page = page

    st.markdown("---")
    st.markdown('<div class="side-label">Current dataset</div>', unsafe_allow_html=True)
    total_burst = sum(int(p["Burst Time"]) for p in st.session_state.processes)
    st.markdown(
        f'<div class="side-meta">{len(st.session_state.processes)} processes<br>'
        f"{total_burst} CPU units</div>",
        unsafe_allow_html=True,
    )
    if st.button("Reset dataset", width="stretch"):
        st.session_state.processes = SAMPLES["Basic"]
        st.rerun()

    st.markdown("---")
    st.markdown(
        '<div class="side-meta">Design system<br><span style="color:#8A8A8A">DESIGN.md</span></div>',
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------
page = st.session_state.page
try:
    result, table, summary = simulation()
except Exception:
    result, table, summary = None, None, None

# --- Overview ---------------------------------------------------------------
if page == "Overview":
    header(
        "Operating Systems · Capstone",
        "CPU Scheduling Studio",
        "A simulator for four CPU scheduling policies, with an interactive execution "
        "trace and comparable performance metrics.",
    )

    if summary:
        stat_row(
            [
                ("Processes", str(len(table)), "in current workload"),
                ("Algorithm", st.session_state.algorithm, "selected policy"),
                ("Avg waiting", f"{summary['Average Waiting Time']:.2f}", "time units"),
                ("Avg turnaround", f"{summary['Average Turnaround Time']:.2f}", "time units"),
            ]
        )

        st.markdown("## Execution trace")
        show_gantt(result)
        st.markdown(
            '<div class="note">Each block is one CPU allocation. Grey blocks are idle '
            "periods. Hover for start, end, and duration; drag to zoom.</div>",
            unsafe_allow_html=True,
        )

        left, right = st.columns([1.7, 1])
        with left:
            st.markdown("## Current workload")
            st.dataframe(
                pd.DataFrame(st.session_state.processes),
                width="stretch",
                hide_index=True,
            )
        with right:
            st.markdown("## How to read this")
            st.markdown(
                '<div class="def">'
                "<b>Waiting</b> — ready but not running.<br>"
                "<b>Turnaround</b> — arrival to completion.<br>"
                "<b>Response</b> — arrival to first CPU slice.<br>"
                "<b>Utilization</b> — busy share of elapsed time.<br>"
                "<b>Throughput</b> — completions per unit time."
                "</div>",
                unsafe_allow_html=True,
            )
            if st.button("Open simulator", type="primary", width="stretch"):
                st.session_state.page = "Simulator"
                st.rerun()

# --- Workload ---------------------------------------------------------------
elif page == "Workload":
    header(
        "Workload design",
        "Process Manager",
        "Define the process set used by every simulation. Edit any value by hand, "
        "or import a CSV; every page recalculates after you apply.",
    )

    with st.expander("Import workload from CSV"):
        st.caption("Required columns: Process, Arrival Time, Burst Time, Priority.")
        uploaded = st.file_uploader("CSV file", type=["csv"], key="workload_upload")
        if uploaded is not None and st.button("Import CSV", key="import_csv"):
            try:
                incoming = pd.read_csv(uploaded)
                columns = ["Process", "Arrival Time", "Burst Time", "Priority"]
                if not all(c in incoming.columns for c in columns):
                    st.error(f"CSV must contain: {', '.join(columns)}")
                else:
                    records = clean_records(incoming[columns])
                    validate(records)
                    st.session_state.processes = records
                    st.session_state.show_all = True
                    st.success(f"Imported {len(records)} processes.")
            except Exception as exc:
                st.error(str(exc))

    a, b, c = st.columns([1.4, 1, 1])
    with a:
        sample = st.selectbox("Sample dataset", list(SAMPLES))
        if st.button("Load sample", width="stretch"):
            st.session_state.processes = [dict(p) for p in SAMPLES[sample]]
            st.rerun()
    with b:
        count = st.number_input("Random count", min_value=1, max_value=20, value=5, step=1)
        if st.button("Generate random", width="stretch"):
            st.session_state.processes = [
                {
                    "Process": f"P{i + 1}",
                    "Arrival Time": random.randint(0, 8),
                    "Burst Time": random.randint(1, 12),
                    "Priority": random.randint(1, 5),
                }
                for i in range(int(count))
            ]
            st.rerun()
    with c:
        if st.button("Add process", width="stretch"):
            used = {p["Process"] for p in st.session_state.processes}
            n = 1
            while f"P{n}" in used:
                n += 1
            st.session_state.processes.append(
                {"Process": f"P{n}", "Arrival Time": 0, "Burst Time": 1, "Priority": 1}
            )
            st.rerun()
        if st.button("Clear all", width="stretch"):
            st.session_state.processes = []
            st.rerun()

    process_editor()

    if st.session_state.processes:
        frame = pd.DataFrame(st.session_state.processes)
        st.markdown("## Workload profile")
        stat_row(
            [
                ("Process count", str(len(frame)), "rows"),
                ("Total burst", str(int(frame["Burst Time"].sum())), "CPU units"),
                ("Latest arrival", str(int(frame["Arrival Time"].max())), "time units"),
                (
                    "Priority range",
                    f"{frame['Priority'].min()}–{frame['Priority'].max()}",
                    "lower = higher",
                ),
            ]
        )

# --- Simulator --------------------------------------------------------------
elif page == "Simulator":
    header(
        "Simulation",
        "Algorithm Simulator",
        "Choose a policy, run it on the current workload, and inspect the trace "
        "and per-process results.",
    )

    with st.expander("Edit process values", expanded=False):
        process_editor(key="sim_editor", heading="#### Workload table")

    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.session_state.algorithm = st.selectbox(
            "Scheduling algorithm",
            list(ALGORITHMS),
            index=list(ALGORITHMS).index(st.session_state.algorithm),
        )
    with c2:
        if st.session_state.algorithm == "Round Robin":
            st.session_state.quantum = st.number_input(
                "Time quantum",
                min_value=1,
                max_value=100,
                value=int(st.session_state.quantum),
                help="Maximum CPU time a process receives before rotating to the ready queue.",
            )
        elif st.session_state.algorithm == "Priority":
            st.caption("Lower numeric value = higher priority. Non-preemptive.")
        elif st.session_state.algorithm == "SJF":
            st.caption("Shortest burst among arrived processes. Non-preemptive.")
        else:
            st.caption("Earliest arrival first; input order breaks ties. Non-preemptive.")

    if st.button("Run simulation", type="primary"):
        try:
            validate(st.session_state.processes)
            st.success("Simulation complete.")
        except Exception as exc:
            st.error(str(exc))

    try:
        result, table, summary = simulation()
        st.markdown("## Summary")
        show_metrics(summary)
        st.markdown("## Execution")
        t1, t2, t3 = st.tabs(["Gantt", "Per-process metrics", "Timeline segments"])
        with t1:
            show_gantt(result)
        with t2:
            st.dataframe(table, width="stretch", hide_index=True)
        with t3:
            show_timeline(result)
    except Exception as exc:
        st.error(str(exc))

    st.markdown("---")
    if st.button("Run all four algorithms", type="primary", width="stretch"):
        st.session_state.show_all = True

    if st.session_state.show_all:
        try:
            validate(st.session_state.processes)
            results, comp = collect_all()
            st.markdown("## All four policies")
            render_all_traces(results)
            st.markdown("## Comparison")
            st.dataframe(styled_comparison(comp), width="stretch")
            st.download_button(
                "Download comparison CSV",
                data=comp.to_csv(index=False).encode(),
                file_name="comparison.csv",
                mime="text/csv",
                key="sim_compare_download",
            )
        except Exception as exc:
            st.error(str(exc))

# --- Analysis ---------------------------------------------------------------
elif page == "Analysis":
    header(
        "Performance",
        "Performance Analytics",
        "Per-process timing and the distribution of CPU time for the selected policy.",
    )

    try:
        result, table, summary = simulation()
        st.markdown("## Summary")
        show_metrics(summary)

        left, right = st.columns(2)
        with left:
            fig = px.bar(
                table,
                x="Process",
                y=["Waiting Time", "Turnaround Time", "Response Time"],
                barmode="group",
                color_discrete_sequence=["#1F4E79", "#A6611A", "#4D7C5F"],
                title="Per-process time metrics",
                labels={"value": "time units", "variable": ""},
            )
            st.plotly_chart(style_fig(fig, height=360), width="stretch")
        with right:
            busy = summary["Total CPU Burst Time"]
            idle = max(0, summary["Total Simulation Time"] - busy)
            fig = px.pie(
                names=["CPU busy", "Idle"],
                values=[busy, idle],
                hole=0.66,
                color_discrete_sequence=["#1F4E79", "#DAD5C9"],
                title="CPU time distribution",
            )
            fig.update_traces(textfont=dict(family="IBM Plex Mono, monospace", size=11))
            st.plotly_chart(style_fig(fig, height=360), width="stretch")

        st.markdown("## Metric definitions")
        st.markdown(
            '<div class="def">'
            "<b>Waiting time</b> = turnaround − burst.<br>"
            "<b>Turnaround time</b> = completion − arrival.<br>"
            "<b>Response time</b> = first start − arrival.<br>"
            "<b>CPU utilization</b> = busy time ÷ elapsed time × 100.<br>"
            "<b>Throughput</b> = completed processes ÷ elapsed time.<br>"
            "<b>Context switches</b> = direct transitions between different processes."
            "</div>",
            unsafe_allow_html=True,
        )
    except Exception as exc:
        st.error(str(exc))

# --- Compare ----------------------------------------------------------------
elif page == "Compare":
    header(
        "Side by side",
        "Algorithm Comparison",
        "All four policies run against the same workload. Best value per metric is "
        "highlighted; Round Robin uses the current time quantum.",
    )

    try:
        validate(st.session_state.processes)
        results, comp = collect_all()

        st.markdown("## Execution traces — all four")
        render_all_traces(results)

        st.markdown("## Comparison table")
        st.dataframe(styled_comparison(comp), width="stretch")
        st.download_button(
            "Download comparison CSV",
            data=comp.to_csv(index=False).encode(),
            file_name="comparison.csv",
            mime="text/csv",
            key="compare_download",
        )

        st.markdown("## Average time metrics")
        long = comp.melt(
            id_vars="Algorithm",
            value_vars=[
                "Average Waiting Time",
                "Average Turnaround Time",
                "Average Response Time",
            ],
            var_name="Metric",
            value_name="Time",
        )
        fig = px.bar(
            long,
            x="Algorithm",
            y="Time",
            color="Metric",
            barmode="group",
            color_discrete_sequence=["#1F4E79", "#A6611A", "#4D7C5F"],
            labels={"Metric": ""},
        )
        st.plotly_chart(style_fig(fig, height=340), width="stretch")

        left, right = st.columns(2)
        with left:
            fig = px.bar(
                comp,
                x="Algorithm",
                y="CPU Utilization",
                color="Algorithm",
                color_discrete_sequence=PALETTE,
                title="CPU utilization (%)",
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(style_fig(fig, height=320), width="stretch")
        with right:
            fig = px.bar(
                comp,
                x="Algorithm",
                y="Throughput",
                color="Algorithm",
                color_discrete_sequence=PALETTE,
                title="Throughput (processes / unit)",
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(style_fig(fig, height=320), width="stretch")

        st.markdown("## Per-process results")
        tabs = st.tabs(list(ALGORITHMS))
        for tab, (algo, (_, tbl, _)) in zip(tabs, results.items()):
            with tab:
                st.dataframe(tbl, width="stretch", hide_index=True)
                st.download_button(
                    f"Download {algo} CSV",
                    data=tbl.to_csv(index=False).encode(),
                    file_name=f"{algo.lower().replace(' ', '_')}_metrics.csv",
                    mime="text/csv",
                    key=f"dl_{algo}",
                )

        st.markdown("## Observations")
        best = {
            m: (comp[m].idxmin() if m in LOWER_IS_BETTER else comp[m].idxmax())
            for m in METRICS
        }
        for m in METRICS:
            i = best[m]
            direction = "lowest" if m in LOWER_IS_BETTER else "highest"
            st.markdown(
                f"- **{comp.loc[i, 'Algorithm']}** recorded the {direction} "
                f"{m.lower()} ({comp.loc[i, m]:.2f})."
            )
        st.markdown(
            '<div class="note">Interpretation depends on workload shape. SJF favours '
            "short jobs; Round Robin favours fairness; priority favours urgent work.</div>",
            unsafe_allow_html=True,
        )
    except Exception as exc:
        st.error(str(exc))

# --- About ------------------------------------------------------------------
else:
    header(
        "Reference",
        "About CPU Scheduling",
        "Definitions and design notes for the simulator.",
    )

    st.markdown("## Policies")
    concepts = [
        (
            "FCFS — First Come, First Served",
            "Processes run in arrival order until completion. Simple and predictable, "
            "but a long job delays every shorter job behind it (convoy effect).",
        ),
        (
            "SJF — Shortest Job First",
            "Among arrived processes, the shortest burst runs next. Minimises average "
            "waiting time when burst lengths are known; non-preemptive here.",
        ),
        (
            "Priority",
            "The arrived process with the lowest numeric priority runs next. "
            "Non-preemptive. Aging would be required to prevent starvation.",
        ),
        (
            "Round Robin",
            "Each ready process receives up to one time quantum. Unfinished processes "
            "return to the queue, giving bounded response time and fairness.",
        ),
    ]
    for title, body in concepts:
        st.markdown(f"### {title}")
        st.markdown(body)

    st.markdown("## Metric formulas")
    st.markdown(
        "| Metric | Formula |\n"
        "|---|---|\n"
        "| Turnaround time | completion − arrival |\n"
        "| Waiting time | turnaround − burst |\n"
        "| Response time | first start − arrival |\n"
        "| CPU utilization | busy time ÷ elapsed time × 100 |\n"
        "| Throughput | completions ÷ elapsed time |\n"
        "| Context switches | direct transitions between different processes |"
    )

    st.markdown("## Design")
    st.markdown(
        "The interface follows a technical/academic direction: paper-white surfaces, "
        "hairline rules, serif headings, monospace data, and a single navy accent. "
        "The full token set and rationale are documented in `DESIGN.md`."
    )

# ----------------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------------
st.markdown(
    '<div class="footer">CPU Scheduling Studio · B.Tech CSE Capstone · 2026 · '
    "Design system: DESIGN.md</div>",
    unsafe_allow_html=True,
)

# CPU Scheduling Studio

An interactive Streamlit dashboard for learning and comparing CPU scheduling policies. Edit a process workload, run four scheduling algorithms, inspect execution on a Plotly Gantt timeline, and compare real performance metrics side by side.

## Features

- Editable workload with add, delete, sample loading, reset, and random generation.
- Four correct schedulers: FCFS, non-preemptive SJF, non-preemptive priority, and preemptive Round Robin.
- Arrival-aware execution, idle CPU periods, deterministic tie breaking, and Round Robin slices.
- Interactive Gantt chart with hover timing, zoom, pan, process colors, and idle blocks.
- Per-process completion, turnaround, waiting, and response times.
- CPU utilization, throughput, burst and elapsed time, and context switch metrics.
- Automatic comparison of all algorithms on the same workload with dynamically selected best results.
- Student-friendly metric and algorithm explanations.
- Dark responsive dashboard with overview, simulator, analytics, comparison, and process manager pages.

## Algorithms

| Algorithm | Policy |
| --- | --- |
| FCFS | Earliest arrival first; input order breaks ties. Non-preemptive. |
| SJF | Shortest burst among processes that have arrived. Non-preemptive. |
| Priority | Lowest numeric priority among arrived processes. Non-preemptive. |
| Round Robin | Ready-queue rotation in configurable time slices. Preemptive. |

## Technology

Python 3.10+, Streamlit, Plotly, Pandas, and NumPy.

## Project structure

```text
CPU-Scheduling-Visualizer/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── algorithms/
│   ├── __init__.py
│   ├── _common.py
│   ├── fcfs.py
│   ├── sjf.py
│   ├── priority.py
│   └── round_robin.py
├── utils/
│   ├── __init__.py
│   ├── metrics.py
│   └── gantt_chart.py
└── assets/
    └── logo.png
```

## Install on Windows

Open PowerShell in the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` in that terminal, then activate again.

## Run

```powershell
streamlit run app.py
```

Streamlit prints a local URL, normally `http://localhost:8501`.

## Usage

1. Choose a sample dataset on **Process Manager** or edit the table. Save changes before leaving the editor.
2. Open **Algorithm Simulator** and choose a policy. For Round Robin, set a positive time quantum.
3. Inspect the Gantt blocks and timeline; idle periods are shown in gray.
4. Open **Performance Analytics** for the selected policy or **Algorithm Comparison** to run all policies over the same workload.

Included datasets cover a basic workload, same arrival times, separated arrival times with idle CPU, and a Round Robin demonstration.

## Metrics and formulas

- Turnaround time = Completion time − Arrival time
- Waiting time = Turnaround time − Burst time
- Response time = First execution start − Arrival time
- CPU utilization = CPU busy time ÷ total simulation time × 100
- Throughput = Completed processes ÷ total simulation time
- Context switches count direct transitions between different process IDs; transitions involving idle CPU are excluded.

All values are derived from the produced execution segments. Initial idle time is included when the first process arrives later.

## Screenshots

Capture the Overview, Gantt Visualization, and Algorithm Comparison pages here for a repository presentation.

## Future improvements

- Preemptive SJF (Shortest Remaining Time First) and aging for priority scheduling.
- Workload import/export as CSV and downloadable comparison reports.
- More datasets and an instructional step-through mode.

## Repository description

Interactive Streamlit CPU scheduling simulator with Gantt charts and algorithm performance comparison for operating systems students.

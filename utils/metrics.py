"""Performance metrics for CPU scheduling simulations.

Elapsed-time convention
-----------------------
"Total Simulation Time" is the elapsed time of the schedule, measured from
the FIRST ARRIVAL to the LAST COMPLETION. Time before the first process
arrives is not counted, so an initial IDLE block does not inflate the
denominator. CPU Utilization and Throughput are therefore:

    elapsed         = last completion time - first arrival time
    CPU Utilization = 100 * (total non-IDLE segment time) / elapsed
    Throughput      = number of processes / elapsed

Context-switch convention
-------------------------
A context switch is counted only for a direct transition between two
different non-IDLE processes. Transitions that involve an IDLE segment
(IDLE -> process or process -> IDLE) are not counted.
"""

import pandas as pd


def calculate_metrics(processes, result):
    """Compute per-process and system metrics for one scheduling run.

    Elapsed time ("Total Simulation Time") runs from the first arrival to
    the last completion, so CPU Utilization and Throughput ignore time
    before the first process arrives. Context Switches counts only direct
    transitions between two different non-IDLE processes; transitions to or
    from an IDLE segment are excluded.

    Returns:
        table: DataFrame with one row per process (Completion, Turnaround,
            Waiting and Response times).
        summary: dict of system metrics with the keys "Average Waiting
            Time", "Average Turnaround Time", "Average Response Time",
            "CPU Utilization", "Throughput", "Total CPU Burst Time",
            "Total Simulation Time" and "Context Switches".
    """
    columns = ['Process', 'Arrival Time', 'Burst Time', 'Priority',
               'Completion Time', 'Turnaround Time', 'Waiting Time',
               'Response Time']
    rows = []
    for p in processes:
        pid = str(p.get('Process', p.get('pid')))
        arrival = int(p['Arrival Time'])
        burst = int(p['Burst Time'])
        ct = result['completion'][pid]
        tat = ct - arrival
        wt = tat - burst
        rt = result['first_start'][pid] - arrival
        rows.append({'Process': pid, 'Arrival Time': arrival,
                     'Burst Time': burst,
                     'Priority': int(p.get('Priority', 0)),
                     'Completion Time': ct, 'Turnaround Time': tat,
                     'Waiting Time': wt, 'Response Time': rt})
    table = pd.DataFrame(rows, columns=columns)

    segments = result['segments']
    busy = sum(s['end'] - s['start'] for s in segments if s['pid'] != 'IDLE')

    # Elapsed time: last completion minus first arrival. If there are no
    # processes, fall back to the first segment start so the empty workload
    # does not crash (elapsed stays 0 and all rates become 0).
    last_completion = max(result['completion'].values(), default=0)
    first_arrival = min(
        (int(p['Arrival Time']) for p in processes),
        default=min((s['start'] for s in segments), default=0),
    )
    elapsed = last_completion - first_arrival

    switches = sum(
        1 for a, b in zip(segments, segments[1:])
        if a['pid'] != b['pid'] and a['pid'] != 'IDLE' and b['pid'] != 'IDLE'
    )

    summary = {
        'Average Waiting Time': table['Waiting Time'].mean(),
        'Average Turnaround Time': table['Turnaround Time'].mean(),
        'Average Response Time': table['Response Time'].mean(),
        'CPU Utilization': 100 * busy / elapsed if elapsed else 0,
        'Throughput': len(table) / elapsed if elapsed else 0,
        'Total CPU Burst Time': busy,
        'Total Simulation Time': elapsed,
        'Context Switches': switches,
    }
    return table, summary

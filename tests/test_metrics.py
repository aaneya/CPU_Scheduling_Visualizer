import pytest

from algorithms import ALGORITHMS
from utils.metrics import calculate_metrics

WORKLOAD = [
    {"Process": "P1", "Arrival Time": 0, "Burst Time": 5, "Priority": 2},
    {"Process": "P2", "Arrival Time": 1, "Burst Time": 3, "Priority": 1},
    {"Process": "P3", "Arrival Time": 2, "Burst Time": 8, "Priority": 3},
    {"Process": "P4", "Arrival Time": 3, "Burst Time": 6, "Priority": 2},
]


def test_fcfs_summary():
    result = ALGORITHMS["FCFS"](WORKLOAD)
    _, summary = calculate_metrics(WORKLOAD, result)
    assert summary["Average Waiting Time"] == pytest.approx(5.75)
    assert summary["Average Turnaround Time"] == pytest.approx(11.25)
    assert summary["Average Response Time"] == pytest.approx(5.75)
    assert summary["CPU Utilization"] == pytest.approx(100.0)
    assert summary["Throughput"] == pytest.approx(4 / 22)
    assert summary["Context Switches"] == 3


def test_fcfs_per_process_values():
    result = ALGORITHMS["FCFS"](WORKLOAD)
    table, _ = calculate_metrics(WORKLOAD, result)
    row = table.set_index("Process").loc["P4"]
    assert row["Completion Time"] == 22
    assert row["Turnaround Time"] == 19
    assert row["Waiting Time"] == 13
    assert row["Response Time"] == 13


def test_round_robin_context_switches():
    result = ALGORITHMS["Round Robin"](WORKLOAD, 2)
    _, summary = calculate_metrics(WORKLOAD, result)
    assert summary["Context Switches"] == 11


def test_idle_time_lowers_utilization():
    workload = [
        {"Process": "P1", "Arrival Time": 2, "Burst Time": 2, "Priority": 1},
        {"Process": "P2", "Arrival Time": 8, "Burst Time": 2, "Priority": 1},
    ]
    result = ALGORITHMS["FCFS"](workload)
    _, summary = calculate_metrics(workload, result)
    # Elapsed runs from the first arrival (2) to the last completion (10).
    assert summary["Total Simulation Time"] == 8
    assert summary["CPU Utilization"] == pytest.approx(50.0)
    assert summary["Throughput"] == pytest.approx(2 / 8)


def test_utilization_uses_first_arrival_not_zero():
    workload = [
        {"Process": "P1", "Arrival Time": 5, "Burst Time": 5, "Priority": 1},
    ]
    result = ALGORITHMS["FCFS"](workload)
    _, summary = calculate_metrics(workload, result)
    # Elapsed is 10 - 5 = 5, not 10; utilization ignores time before arrival.
    assert summary["Total Simulation Time"] == 5
    assert summary["CPU Utilization"] == pytest.approx(100.0)
    assert summary["Throughput"] == pytest.approx(1 / 5)

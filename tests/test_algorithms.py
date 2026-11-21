import pytest

from algorithms import ALGORITHMS
from algorithms._common import validate

WORKLOAD = [
    {"Process": "P1", "Arrival Time": 0, "Burst Time": 5, "Priority": 2},
    {"Process": "P2", "Arrival Time": 1, "Burst Time": 3, "Priority": 1},
    {"Process": "P3", "Arrival Time": 2, "Burst Time": 8, "Priority": 3},
    {"Process": "P4", "Arrival Time": 3, "Burst Time": 6, "Priority": 2},
]


def segments(result):
    return [(s["pid"], s["start"], s["end"]) for s in result["segments"]]


def test_fcfs_trace():
    assert segments(ALGORITHMS["FCFS"](WORKLOAD)) == [
        ("P1", 0, 5),
        ("P2", 5, 8),
        ("P3", 8, 16),
        ("P4", 16, 22),
    ]


def test_sjf_trace():
    assert segments(ALGORITHMS["SJF"](WORKLOAD)) == [
        ("P1", 0, 5),
        ("P2", 5, 8),
        ("P4", 8, 14),
        ("P3", 14, 22),
    ]


def test_srtf_trace():
    workload = [
        {"Process": "P1", "Arrival Time": 0, "Burst Time": 8, "Priority": 1},
        {"Process": "P2", "Arrival Time": 1, "Burst Time": 3, "Priority": 1},
        {"Process": "P3", "Arrival Time": 2, "Burst Time": 1, "Priority": 1},
    ]
    assert segments(ALGORITHMS["SRTF"](workload)) == [
        ("P1", 0, 1),
        ("P2", 1, 2),
        ("P3", 2, 3),
        ("P2", 3, 5),
        ("P1", 5, 12),
    ]


def test_priority_trace():
    assert segments(ALGORITHMS["Priority"](WORKLOAD)) == [
        ("P1", 0, 5),
        ("P2", 5, 8),
        ("P4", 8, 14),
        ("P3", 14, 22),
    ]


def test_priority_aging_changes_order():
    workload = [
        {"Process": "P1", "Arrival Time": 0, "Burst Time": 4, "Priority": 1},
        {"Process": "P2", "Arrival Time": 0, "Burst Time": 5, "Priority": 5},
        {"Process": "P3", "Arrival Time": 4, "Burst Time": 1, "Priority": 2},
    ]
    assert segments(ALGORITHMS["Priority"](workload)) == [
        ("P1", 0, 4),
        ("P3", 4, 5),
        ("P2", 5, 10),
    ]
    assert segments(ALGORITHMS["Priority"](workload, aging=True, aging_interval=1)) == [
        ("P1", 0, 4),
        ("P2", 4, 9),
        ("P3", 9, 10),
    ]


def test_round_robin_trace():
    assert segments(ALGORITHMS["Round Robin"](WORKLOAD, 2)) == [
        ("P1", 0, 2),
        ("P2", 2, 4),
        ("P3", 4, 6),
        ("P1", 6, 8),
        ("P4", 8, 10),
        ("P2", 10, 11),
        ("P3", 11, 13),
        ("P1", 13, 14),
        ("P4", 14, 16),
        ("P3", 16, 18),
        ("P4", 18, 20),
        ("P3", 20, 22),
    ]


def test_idle_cpu_is_recorded():
    workload = [
        {"Process": "P1", "Arrival Time": 2, "Burst Time": 3, "Priority": 1},
        {"Process": "P2", "Arrival Time": 9, "Burst Time": 2, "Priority": 1},
    ]
    assert segments(ALGORITHMS["FCFS"](workload)) == [
        ("IDLE", 0, 2),
        ("P1", 2, 5),
        ("IDLE", 5, 9),
        ("P2", 9, 11),
    ]


def test_srtf_idle_cpu_is_recorded():
    workload = [
        {"Process": "P1", "Arrival Time": 3, "Burst Time": 2, "Priority": 1},
        {"Process": "P2", "Arrival Time": 7, "Burst Time": 1, "Priority": 1},
    ]
    assert segments(ALGORITHMS["SRTF"](workload)) == [
        ("IDLE", 0, 3),
        ("P1", 3, 5),
        ("IDLE", 5, 7),
        ("P2", 7, 8),
    ]


@pytest.mark.parametrize(
    "workload",
    [
        [],
        [{"Process": "P1", "Arrival Time": -1, "Burst Time": 2, "Priority": 1}],
        [{"Process": "P1", "Arrival Time": 0, "Burst Time": 0, "Priority": 1}],
        [
            {"Process": "P1", "Arrival Time": 0, "Burst Time": 1, "Priority": 1},
            {"Process": "P1", "Arrival Time": 1, "Burst Time": 1, "Priority": 1},
        ],
    ],
)
def test_validate_rejects_bad_workloads(workload):
    with pytest.raises(ValueError):
        validate(workload)


def test_round_robin_rejects_bad_quantum():
    with pytest.raises(ValueError):
        ALGORITHMS["Round Robin"](WORKLOAD, 0)

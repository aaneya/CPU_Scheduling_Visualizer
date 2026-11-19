"""Scheduling algorithms returning execution segments and completion times."""
from .fcfs import fcfs
from .sjf import sjf
from .priority import priority
from .round_robin import round_robin

ALGORITHMS = {"FCFS": fcfs, "SJF": sjf, "Priority": priority, "Round Robin": round_robin}

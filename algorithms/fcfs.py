from ._common import schedule_nonpreemptive
def fcfs(processes):
    """First come first served; ties retain input order."""
    return schedule_nonpreemptive(processes, lambda p:(p['arrival'],p['order']))

from ._common import schedule_nonpreemptive
def sjf(processes):
    """Non-preemptive shortest job among arrived processes."""
    return schedule_nonpreemptive(processes, lambda p:(p['burst'],p['arrival'],p['order']))

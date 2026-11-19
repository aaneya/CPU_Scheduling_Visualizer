from ._common import schedule_nonpreemptive
def priority(processes):
    """Non-preemptive priority; lower numeric value means higher priority."""
    return schedule_nonpreemptive(processes, lambda p:(p['priority'],p['arrival'],p['order']))

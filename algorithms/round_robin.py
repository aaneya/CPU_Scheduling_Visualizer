from collections import deque
from ._common import validate
def round_robin(processes, quantum=2):
    """Preemptive RR. Arrivals during a slice join before the interrupted job."""
    jobs=validate(processes); quantum=int(quantum)
    if quantum <= 0: raise ValueError("Time quantum must be greater than zero.")
    jobs.sort(key=lambda p:(p['arrival'],p['order'])); remaining={p['pid']:p['burst'] for p in jobs}
    completion={}; first={}; seg=[]; q=deque(); i=0; t=0
    while i<len(jobs) or q:
        if not q and i<len(jobs) and t<jobs[i]['arrival']:
            seg.append({"pid":"IDLE","start":t,"end":jobs[i]['arrival']}); t=jobs[i]['arrival']
        while i<len(jobs) and jobs[i]['arrival']<=t: q.append(jobs[i]); i+=1
        p=q.popleft(); first.setdefault(p['pid'],t); end=t+min(quantum,remaining[p['pid']])
        seg.append({"pid":p['pid'],"start":t,"end":end}); remaining[p['pid']]-=end-t; t=end
        while i<len(jobs) and jobs[i]['arrival']<=t: q.append(jobs[i]); i+=1
        if remaining[p['pid']]: q.append(p)
        else: completion[p['pid']]=t
    return {"segments":seg,"completion":completion,"first_start":first}

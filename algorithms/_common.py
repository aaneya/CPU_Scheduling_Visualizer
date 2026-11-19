def validate(processes):
    if not processes:
        raise ValueError("Add at least one process.")
    seen = set()
    clean = []
    for i, p in enumerate(processes):
        pid = str(p.get("Process", p.get("pid", f"P{i+1}"))).strip()
        arrival, burst, priority = int(p["Arrival Time"]), int(p["Burst Time"]), int(p.get("Priority", 0))
        if not pid or pid in seen: raise ValueError("Process IDs must be non-empty and unique.")
        if arrival < 0 or burst <= 0: raise ValueError(f"{pid}: arrival must be ≥ 0 and burst must be > 0.")
        seen.add(pid)
        clean.append({"pid": pid, "arrival": arrival, "burst": burst, "priority": priority, "order": i})
    return clean

def schedule_nonpreemptive(processes, key):
    jobs = validate(processes); pending = jobs[:]; t = 0; segments=[]; completion={}; first={}
    while pending:
        ready=[p for p in pending if p['arrival'] <= t]
        if not ready:
            nxt=min(p['arrival'] for p in pending)
            if nxt > t: segments.append({"pid":"IDLE","start":t,"end":nxt})
            t=nxt; ready=[p for p in pending if p['arrival'] <= t]
        p=min(ready,key=key); start=t; t += p['burst']
        segments.append({"pid":p['pid'],"start":start,"end":t}); first[p['pid']]=start; completion[p['pid']]=t; pending.remove(p)
    return {"segments":segments,"completion":completion,"first_start":first}

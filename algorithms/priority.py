from ._common import schedule_nonpreemptive, validate


def priority(processes, aging=False, aging_interval=1):
    """Non-preemptive priority; lower numeric value means higher priority.

    With ``aging=False`` (the default) the scheduler is exactly the classic
    non-preemptive priority scheduler.

    With ``aging=True``, long-waiting processes receive a boost so they
    cannot be starved by a stream of higher-priority arrivals. At each
    scheduling decision every arrived process is ranked by an effective
    priority::

        effective = priority - (waiting_time // aging_interval)

    where ``waiting_time = current_time - arrival``. Lower effective priority
    wins; ties are broken by arrival time and then by original input order.
    ``aging_interval`` must be a positive integer.
    """
    if not aging:
        return schedule_nonpreemptive(processes, lambda p: (p["priority"], p["arrival"], p["order"]))
    jobs = validate(processes)
    aging_interval = int(aging_interval)
    if aging_interval <= 0:
        raise ValueError("Aging interval must be greater than zero.")
    pending = jobs[:]
    t = 0
    segments = []
    completion = {}
    first = {}
    while pending:
        ready = [p for p in pending if p["arrival"] <= t]
        if not ready:
            nxt = min(p["arrival"] for p in pending)
            segments.append({"pid": "IDLE", "start": t, "end": nxt})
            t = nxt
            ready = [p for p in pending if p["arrival"] <= t]
        p = min(
            ready,
            key=lambda x: (
                x["priority"] - ((t - x["arrival"]) // aging_interval),
                x["arrival"],
                x["order"],
            ),
        )
        start = t
        t += p["burst"]
        segments.append({"pid": p["pid"], "start": start, "end": t})
        first[p["pid"]] = start
        completion[p["pid"]] = t
        pending.remove(p)
    return {"segments": segments, "completion": completion, "first_start": first}

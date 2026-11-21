from ._common import validate


def srtf(processes):
    """Shortest Remaining Time First (preemptive SJF).

    At every scheduling decision the arrived process with the smallest
    remaining burst runs. A newly arrived job preempts the running job only
    when its remaining burst is strictly shorter; ties in remaining time are
    broken by arrival time and then by original input order. Periods when no
    process has arrived are reported as ``IDLE`` segments. Consecutive slices
    of the same process (a job that keeps the CPU across an arrival) are
    coalesced into one segment.
    """
    jobs = validate(processes)
    jobs.sort(key=lambda p: (p["arrival"], p["order"]))
    remaining = {p["pid"]: p["burst"] for p in jobs}
    arrived = []
    idx = 0
    t = 0
    segments = []
    completion = {}
    first = {}
    while idx < len(jobs) or arrived:
        while idx < len(jobs) and jobs[idx]["arrival"] <= t:
            arrived.append(jobs[idx])
            idx += 1
        if not arrived:
            nxt = jobs[idx]["arrival"]
            segments.append({"pid": "IDLE", "start": t, "end": nxt})
            t = nxt
            continue
        p = min(arrived, key=lambda x: (remaining[x["pid"]], x["arrival"], x["order"]))
        # Run until the job finishes or the next arrival, whichever comes first.
        if idx < len(jobs) and t + remaining[p["pid"]] > jobs[idx]["arrival"]:
            end = jobs[idx]["arrival"]
        else:
            end = t + remaining[p["pid"]]
        if segments and segments[-1]["pid"] == p["pid"] and segments[-1]["end"] == t:
            segments[-1]["end"] = end
        else:
            segments.append({"pid": p["pid"], "start": t, "end": end})
        first.setdefault(p["pid"], t)
        remaining[p["pid"]] -= end - t
        t = end
        if remaining[p["pid"]] <= 0:
            completion[p["pid"]] = t
            arrived.remove(p)
    return {"segments": segments, "completion": completion, "first_start": first}

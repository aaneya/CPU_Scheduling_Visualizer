import pandas as pd
def calculate_metrics(processes, result):
    rows=[]
    for p in processes:
        pid=str(p.get('Process',p.get('pid'))); arrival=int(p['Arrival Time']); burst=int(p['Burst Time'])
        ct=result['completion'][pid]; tat=ct-arrival; wt=tat-burst; rt=result['first_start'][pid]-arrival
        rows.append({'Process':pid,'Arrival Time':arrival,'Burst Time':burst,'Priority':int(p.get('Priority',0)),'Completion Time':ct,'Turnaround Time':tat,'Waiting Time':wt,'Response Time':rt})
    table=pd.DataFrame(rows)
    seg=result['segments']; busy=sum(s['end']-s['start'] for s in seg if s['pid']!='IDLE'); total=max((s['end'] for s in seg),default=0)-min((s['start'] for s in seg),default=0)
    switches=sum(1 for a,b in zip(seg,seg[1:]) if a['pid']!=b['pid'] and a['pid']!='IDLE' and b['pid']!='IDLE')
    summary={'Average Waiting Time':table['Waiting Time'].mean(),'Average Turnaround Time':table['Turnaround Time'].mean(),'Average Response Time':table['Response Time'].mean(),'CPU Utilization':100*busy/total if total else 0,'Throughput':len(table)/total if total else 0,'Total CPU Burst Time':busy,'Total Simulation Time':total,'Context Switches':switches}
    return table,summary

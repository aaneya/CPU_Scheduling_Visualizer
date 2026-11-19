from __future__ import annotations
import random
import pandas as pd
import plotly.express as px
import streamlit as st
from algorithms import ALGORITHMS
from algorithms._common import validate
from utils.metrics import calculate_metrics
from utils.gantt_chart import make_gantt, PALETTE

st.set_page_config(page_title='CPU Scheduling Studio',page_icon='⚡',layout='wide',initial_sidebar_state='expanded')
CSS='''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
.stApp{background:radial-gradient(ellipse at 16% 0%,#152344 0%,#0B1020 42%,#0B1020 100%);color:#F1F5F9;font-family:'DM Sans',sans-serif}h1,h2,h3{font-family:'Space Grotesk',sans-serif!important;color:#F8FAFC!important}.block-container{padding-top:2rem;padding-bottom:3rem;max-width:1450px}.section-kicker{color:#22D3EE;text-transform:uppercase;letter-spacing:.16em;font-size:.73rem;font-weight:700;margin-bottom:.3rem}.hero{padding:1.6rem 1.8rem;border:1px solid #293755;border-radius:22px;background:linear-gradient(120deg,rgba(99,102,241,.2),rgba(34,211,238,.06) 65%,rgba(168,85,247,.14));margin-bottom:1.2rem}.hero h1{font-size:2.5rem;margin:0}.hero p{color:#A9B8D0;margin:.45rem 0 0}.status{display:inline-flex;align-items:center;gap:8px;color:#A7F3D0;font-size:.82rem;background:#064E3B55;padding:7px 12px;border-radius:99px;border:1px solid #10B98155}.dot{width:8px;height:8px;background:#34D399;border-radius:50%;box-shadow:0 0 12px #34D399}.card{background:linear-gradient(145deg,#182238,#131B2D);border:1px solid #293750;border-radius:16px;padding:18px 20px;min-height:122px;box-shadow:0 10px 30px #05091433;transition:transform .18s,border-color .18s}.card:hover{transform:translateY(-2px);border-color:#5265A0}.card-label{color:#94A3B8;font-size:.82rem}.card-value{font-family:'Space Grotesk';font-size:1.7rem;font-weight:700;color:#F8FAFC;margin:.45rem 0}.card-note{color:#73839D;font-size:.76rem}.panel{background:#151C2E;border:1px solid #293750;border-radius:18px;padding:20px;margin:10px 0 18px}.algo{background:linear-gradient(145deg,#19243A,#141B2D);border:1px solid #2A3854;border-radius:16px;padding:18px;height:100%;min-height:180px}.algo h3{margin:.4rem 0}.algo p{color:#9AAAC2;font-size:.9rem}.pill{display:inline-block;border-radius:8px;padding:4px 9px;background:#6366F133;color:#A5B4FC;font-size:.72rem;font-weight:700;letter-spacing:.05em}.stButton>button{border-radius:10px;border:1px solid #43558A;background:linear-gradient(100deg,#4F46E5,#6366F1);color:white;font-weight:600;min-height:42px;transition:all .16s}.stButton>button:hover{border-color:#22D3EE;color:white;box-shadow:0 0 20px #6366F144;transform:translateY(-1px)}.stTabs [data-baseweb=tab-list]{gap:8px}.stTabs [data-baseweb=tab]{background:#141D30;border-radius:9px;padding:9px 15px;color:#AAB8CD}.stTabs [aria-selected=true]{background:#343B78!important;color:#fff!important}.stDataFrame{border:1px solid #2B3851;border-radius:12px;overflow:hidden}.stSelectbox label,.stNumberInput label,.stSlider label{color:#B9C7DA}.small-muted{color:#8FA0B9;font-size:.88rem}
</style>'''
st.markdown(CSS,unsafe_allow_html=True)

SAMPLES={
 'Basic':[{"Process":"P1","Arrival Time":0,"Burst Time":5,"Priority":2},{"Process":"P2","Arrival Time":1,"Burst Time":3,"Priority":1},{"Process":"P3","Arrival Time":2,"Burst Time":8,"Priority":3},{"Process":"P4","Arrival Time":3,"Burst Time":6,"Priority":2}],
 'Same arrival':[{"Process":"P1","Arrival Time":0,"Burst Time":7,"Priority":3},{"Process":"P2","Arrival Time":0,"Burst Time":3,"Priority":1},{"Process":"P3","Arrival Time":0,"Burst Time":5,"Priority":2},{"Process":"P4","Arrival Time":0,"Burst Time":2,"Priority":4}],
 'Idle periods':[{"Process":"P1","Arrival Time":2,"Burst Time":3,"Priority":2},{"Process":"P2","Arrival Time":3,"Burst Time":2,"Priority":1},{"Process":"P3","Arrival Time":9,"Burst Time":4,"Priority":3}],
 'Round Robin demo':[{"Process":"P1","Arrival Time":0,"Burst Time":8,"Priority":2},{"Process":"P2","Arrival Time":1,"Burst Time":4,"Priority":1},{"Process":"P3","Arrival Time":2,"Burst Time":5,"Priority":3},{"Process":"P4","Arrival Time":4,"Burst Time":2,"Priority":2}]}
if 'processes' not in st.session_state: st.session_state.processes=SAMPLES['Basic']
if 'algorithm' not in st.session_state: st.session_state.algorithm='FCFS'
if 'quantum' not in st.session_state: st.session_state.quantum=2
if 'page' not in st.session_state: st.session_state.page='Overview'
if 'last_run' not in st.session_state: st.session_state.last_run=0

def run(algo, processes=None, quantum=None):
    data=processes if processes is not None else st.session_state.processes
    fn=ALGORITHMS[algo]
    return fn(data, quantum or st.session_state.quantum) if algo=='Round Robin' else fn(data)

def simulation(algo=None):
    algo=algo or st.session_state.algorithm
    res=run(algo); tbl,metrics=calculate_metrics(st.session_state.processes,res)
    return res,tbl,metrics

def heading(kicker,title,subtitle=''):
    st.markdown(f'<div class="section-kicker">{kicker}</div><h1 style="margin:0 0 .2rem">{title}</h1><p class="small-muted" style="margin-top:0">{subtitle}</p>',unsafe_allow_html=True)
def kpi(label,value,note=''):
    st.markdown(f'<div class="card"><div class="card-label">{label}</div><div class="card-value">{value}</div><div class="card-note">{note}</div></div>',unsafe_allow_html=True)
def show_metrics(m):
    specs=[('Avg waiting',f"{m['Average Waiting Time']:.2f}",'time units'),('Avg turnaround',f"{m['Average Turnaround Time']:.2f}",'time units'),('Avg response',f"{m['Average Response Time']:.2f}",'time units'),('CPU utilization',f"{m['CPU Utilization']:.1f}%",'busy / total elapsed'),('Throughput',f"{m['Throughput']:.3f}",'processes per time unit'),('Context switches',str(m['Context Switches']),'between process bursts')]
    cols=st.columns(3)
    for c,(a,b,d) in zip(cols*2,specs):
        with c:kpi(a,b,d)
def show_chart(res): st.plotly_chart(make_gantt(res['segments']),use_container_width=True,config={'displayModeBar':True,'scrollZoom':True})
def show_timeline(res):
    data=[{'Process':s['pid'],'Start Time':s['start'],'End Time':s['end'],'Duration':s['end']-s['start']} for s in res['segments']]
    st.dataframe(pd.DataFrame(data),use_container_width=True,hide_index=True)
def process_editor():
    st.markdown('<div class="panel">',unsafe_allow_html=True)
    st.markdown('#### Process table')
    st.caption('Edit cells directly. Process IDs must be unique; arrival ≥ 0 and burst > 0.')
    df=pd.DataFrame(st.session_state.processes,columns=['Process','Arrival Time','Burst Time','Priority'])
    edited=st.data_editor(df,num_rows='dynamic',use_container_width=True,hide_index=True,key='process_editor',column_config={'Process':st.column_config.TextColumn(required=True),'Arrival Time':st.column_config.NumberColumn(min_value=0,step=1,required=True),'Burst Time':st.column_config.NumberColumn(min_value=1,step=1,required=True),'Priority':st.column_config.NumberColumn(step=1,required=True)})
    if st.button('Save process changes',key='save_processes'):
        try:
            records=edited.fillna(0).to_dict('records'); validate(records); st.session_state.processes=records; st.success(f'Saved {len(records)} processes.')
        except Exception as e: st.error(str(e))
    st.markdown('</div>',unsafe_allow_html=True)

with st.sidebar:
    st.image('assets/logo.png',width=54)
    st.markdown('<div style="padding:0 5px 18px"><div style="font-family:Space Grotesk;font-size:1.2rem;font-weight:700;color:#F8FAFC">CPU SCHEDULING<br><span style="color:#818CF8">STUDIO</span></div><div style="font-size:.76rem;color:#8292AA;margin-top:6px">OPERATING SYSTEMS LAB</div></div>',unsafe_allow_html=True)
    st.markdown('<span class="status"><span class="dot"></span>Simulation engine ready</span>',unsafe_allow_html=True)
    pages=['Overview','Process Manager','Algorithm Simulator','Gantt Visualization','Performance Analytics','Algorithm Comparison','About']
    page=st.radio('NAVIGATION',pages,index=pages.index(st.session_state.page),label_visibility='visible')
    st.session_state.page=page
    st.markdown('---')
    st.markdown('<span class="small-muted">CURRENT DATASET</span>',unsafe_allow_html=True)
    st.caption(f"{len(st.session_state.processes)} processes · {sum(int(p['Burst Time']) for p in st.session_state.processes)} CPU units")
    if st.button('↺ Reset to sample',use_container_width=True): st.session_state.processes=SAMPLES['Basic']; st.rerun()

page=st.session_state.page
try:
    res,tbl,m=simulation()
except Exception as e:
    res,tbl,m=None,None,None

if page=='Overview':
    st.markdown('<div class="hero"><div class="section-kicker">OPERATING SYSTEMS · INTERACTIVE LAB</div><h1>CPU Scheduling Studio</h1><p>Simulate, visualize, and analyze how the operating system allocates processor time.</p><br><span class="status"><span class="dot"></span>Simulation engine ready</span></div>',unsafe_allow_html=True)
    if m:
        cs=st.columns(4)
        for c,(lab,val,note) in zip(cs,[('Processes',str(len(tbl)),'in current workload'),('Selected algorithm',st.session_state.algorithm,'scheduler'),('Average waiting',f"{m['Average Waiting Time']:.2f}",'time units'),('Average turnaround',f"{m['Average Turnaround Time']:.2f}",'time units')]):
            with c:kpi(lab,val,note)
    st.markdown('### Quick actions')
    q1,q2,q3,q4=st.columns(4)
    for c,label,target in [(q1,'▶ Start simulation','Algorithm Simulator'),(q2,'＋ Add / edit processes','Process Manager'),(q3,'⇄ Compare algorithms','Algorithm Comparison'),(q4,'✦ Load sample dataset','Overview')]:
        with c:
            if st.button(label,use_container_width=True):
                if target=='Overview': st.session_state.processes=SAMPLES['Basic']
                else: st.session_state.page=target
                st.rerun()
    st.markdown('### Explore the schedulers')
    descriptions={'FCFS':'Arrival-order execution with predictable, non-preemptive service.','SJF':'Chooses the shortest available job to reduce average wait.','Priority':'Runs the available process with the strongest priority.','Round Robin':'Shares CPU time fairly using a configurable time slice.'}
    cols=st.columns(4)
    for c,(a,d) in zip(cols,descriptions.items()):
        with c:
            st.markdown(f'<div class="algo"><span class="pill">{a.upper()}</span><h3>{a}</h3><p>{d}</p></div>',unsafe_allow_html=True)
            if st.button(f'Explore {a}',key=f'explore_{a}',use_container_width=True): st.session_state.algorithm=a; st.session_state.page='Algorithm Simulator'; st.rerun()
    st.markdown('### Current workload')
    st.dataframe(pd.DataFrame(st.session_state.processes),use_container_width=True,hide_index=True)
elif page=='Process Manager':
    heading('WORKLOAD DESIGN','Process Manager','Create and tune the workload used by every simulation.')
    a,b,c=st.columns([1.3,1,1])
    with a:
        sample=st.selectbox('Sample dataset',list(SAMPLES))
        if st.button('Load selected dataset',use_container_width=True): st.session_state.processes=SAMPLES[sample].copy(); st.rerun()
    with b:
        count=st.number_input('Random process count',min_value=1,max_value=20,value=5,step=1)
        if st.button('Generate random',use_container_width=True): st.session_state.processes=[{'Process':f'P{i+1}','Arrival Time':random.randint(0,8),'Burst Time':random.randint(1,12),'Priority':random.randint(1,5)} for i in range(int(count))]; st.rerun()
    with c:
        if st.button('＋ Add process',use_container_width=True):
            ids={p['Process'] for p in st.session_state.processes}; n=1
            while f'P{n}' in ids:n+=1
            st.session_state.processes.append({'Process':f'P{n}','Arrival Time':0,'Burst Time':1,'Priority':1}); st.rerun()
        if st.button('Clear all',use_container_width=True): st.session_state.processes=[]; st.rerun()
    process_editor()
    if st.session_state.processes:
        st.markdown('### Workload profile'); prof=pd.DataFrame(st.session_state.processes); cols=st.columns(4)
        for c,(x,v) in zip(cols,[('Process count',len(prof)),('Total burst',int(prof['Burst Time'].sum())),('Latest arrival',int(prof['Arrival Time'].max())),('Priority range',f"{prof['Priority'].min()}–{prof['Priority'].max()}")]):
            with c:kpi(x,str(v),'current dataset')
elif page=='Algorithm Simulator':
    heading('SIMULATION','Algorithm Simulator','Select a scheduling policy and inspect its execution and metrics.')
    c1,c2=st.columns([1.2,1])
    with c1: st.session_state.algorithm=st.selectbox('Scheduling algorithm',list(ALGORITHMS),index=list(ALGORITHMS).index(st.session_state.algorithm))
    with c2:
        if st.session_state.algorithm=='Round Robin': st.session_state.quantum=st.number_input('Time quantum',min_value=1,max_value=100,value=int(st.session_state.quantum),help='Time Quantum determines how long a process can execute before the CPU switches to another ready process.')
        elif st.session_state.algorithm=='Priority':st.info('Lower numerical value means higher priority. Non-preemptive scheduling.')
        elif st.session_state.algorithm=='SJF':st.info('Non-preemptive: selects the shortest process that has already arrived.')
        else:st.info('First come, first served. Ties preserve the input order.')
    if st.button('▶ Run simulation',type='primary'):
        try:validate(st.session_state.processes); st.session_state.last_run+=1; st.success('Simulation complete.')
        except Exception as e:st.error(str(e))
    try:
        res,tbl,m=simulation(); show_metrics(m)
        t1,t2,t3=st.tabs(['Execution chart','Process results','Timeline'])
        with t1:show_chart(res)
        with t2:st.dataframe(tbl,use_container_width=True,hide_index=True)
        with t3:show_timeline(res)
    except Exception as e:st.warning(str(e))
elif page=='Gantt Visualization':
    heading('EXECUTION TRACE','Gantt Visualization','Follow each CPU time slice across the workload timeline.')
    c1,c2=st.columns([2,1])
    with c1:st.session_state.algorithm=st.selectbox('Algorithm',list(ALGORITHMS),index=list(ALGORITHMS).index(st.session_state.algorithm),key='gantt_algo')
    with c2:
        if st.session_state.algorithm=='Round Robin':st.session_state.quantum=st.number_input('Quantum',min_value=1,max_value=100,value=int(st.session_state.quantum),key='gantt_quantum')
    try:
        res,tbl,m=simulation(); show_chart(res)
        st.markdown('### Execution segments');show_timeline(res)
        st.caption('Hover over a block for start, end, and duration. Gray blocks represent idle CPU time; zoom and pan with Plotly controls.')
    except Exception as e:st.error(str(e))
elif page=='Performance Analytics':
    heading('PERFORMANCE','Performance Analytics','Understand how this scheduling policy behaves for the current workload.')
    try:
        res,tbl,m=simulation();show_metrics(m)
        l,r=st.columns(2)
        with l:
            fig=px.bar(tbl,x='Process',y=['Waiting Time','Turnaround Time','Response Time'],barmode='group',color_discrete_sequence=['#6366F1','#22D3EE','#A855F7'],title='Per-process time metrics');fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font_color='#CBD5E1',legend_title='');st.plotly_chart(fig,use_container_width=True)
        with r:
            fig=px.pie(names=['CPU busy','Idle'],values=[m['Total CPU Burst Time'],max(0,m['Total Simulation Time']-m['Total CPU Burst Time'])],hole=.68,color_discrete_sequence=['#6366F1','#26334A'],title='CPU time distribution');fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',font_color='#CBD5E1');st.plotly_chart(fig,use_container_width=True)
        st.markdown('### Metric guide')
        st.markdown('- **Waiting time:** time spent ready but not executing (turnaround − burst).\n- **Turnaround time:** total time from arrival to completion.\n- **Response time:** delay until the first CPU allocation.\n- **CPU utilization:** share of elapsed simulation time spent executing.\n- **Throughput:** completed processes per elapsed time unit.\n- **Context switches:** transitions directly between different processes; idle transitions are excluded.')
    except Exception as e:st.error(str(e))
elif page=='Algorithm Comparison':
    heading('SIDE-BY-SIDE','Algorithm Comparison','Run every scheduler against the same process dataset.')
    st.caption('Comparison uses the current Round Robin quantum. Lower time and switch counts are better; higher utilization and throughput are generally better. Results depend on workload shape.')
    try:
        validate(st.session_state.processes); rows=[]
        for a in ALGORITHMS:
            rr=run(a); _,mm=calculate_metrics(st.session_state.processes,rr);rows.append({'Algorithm':a,**mm})
        comp=pd.DataFrame(rows); metriccols=['Average Waiting Time','Average Turnaround Time','Average Response Time','CPU Utilization','Throughput','Context Switches']
        best={x:(comp[x].idxmax() if x in ('CPU Utilization','Throughput') else comp[x].idxmin()) for x in metriccols}
        cards=st.columns(3)
        for c,x in zip(cards,metriccols):
            i=best[x]
            with c:kpi('Best · '+x,comp.loc[i,'Algorithm'],f"{comp.loc[i,x]:.2f} {'%' if x=='CPU Utilization' else ''}")
        long=comp.melt(id_vars='Algorithm',value_vars=metriccols,var_name='Metric',value_name='Value')
        fig=px.bar(long,x='Algorithm',y='Value',color='Algorithm',facet_col='Metric',facet_col_wrap=3,color_discrete_sequence=PALETTE,title='Scheduler metrics comparison');fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font_color='#CBD5E1',showlegend=False,height=620);fig.for_each_annotation(lambda a:a.update(text=a.text.split('=')[-1]));st.plotly_chart(fig,use_container_width=True)
        st.markdown('### Comparison table')
        styled=comp.set_index('Algorithm')[metriccols].style.format('{:.2f}').highlight_min(subset=[x for x in metriccols if x not in ['CPU Utilization','Throughput']],color='#14532D').highlight_max(subset=['CPU Utilization','Throughput'],color='#14532D')
        st.dataframe(styled,use_container_width=True)
        st.markdown('### Workload insights')
        for x in metriccols:
            i=best[x]; direction='highest' if x in ('CPU Utilization','Throughput') else 'lowest'
            st.markdown(f"- **{comp.loc[i,'Algorithm']}** achieved the {direction} {x.lower()} for this workload ({comp.loc[i,x]:.2f}).")
    except Exception as e:st.error(str(e))
else:
    heading('LEARN','About CPU Scheduling','A practical guide to the concepts behind the simulation.')
    st.markdown('''<div class="panel"><h3>What is CPU scheduling?</h3><p>The operating system scheduler chooses which ready process gets the CPU next. Good scheduling balances responsiveness, fairness, throughput, and efficient CPU use.</p></div>''',unsafe_allow_html=True)
    concepts=[('FCFS','First Come First Serve','Processes run in arrival order until they finish. Easy to understand, but a long job can make shorter jobs wait.'),('SJF','Shortest Job First','The available process with the smallest burst runs to completion. It can reduce average waiting time when burst lengths are known.'),('Priority','Priority Scheduling','The available process with the lowest numeric priority runs first. Long-term systems can use aging to avoid starvation; this simulator is non-preemptive.'),('Round Robin','Round Robin','Each ready process receives up to one time quantum. An unfinished process returns to the end of the ready queue, giving an interactive feel.')]
    for title,sub,body in concepts:st.markdown(f'<div class="panel"><span class="pill">{title}</span><h3>{sub}</h3><p class="small-muted">{body}</p></div>',unsafe_allow_html=True)
    st.markdown('### Key metrics')
    st.markdown('''- **Waiting time:** Turnaround − Burst. Total time ready without using the CPU.  
- **Turnaround time:** Completion − Arrival. Total elapsed time in the system.  
- **Response time:** First start − Arrival. Time until the process first receives CPU.  
- **CPU utilization:** Busy CPU time ÷ total simulation time × 100.  
- **Throughput:** Completed processes ÷ total simulation time.  
- **Context switches:** Direct transitions between different running processes in the timeline.''')

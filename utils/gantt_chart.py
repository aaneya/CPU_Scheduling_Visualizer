import plotly.graph_objects as go
PALETTE=['#6366F1','#22D3EE','#A855F7','#F472B6','#34D399','#FBBF24','#FB7185','#60A5FA']
def make_gantt(segments):
    pids=list(dict.fromkeys(s['pid'] for s in segments)); colors={'IDLE':'#475569'}
    colors.update({p:PALETTE[i%len(PALETTE)] for i,p in enumerate(x for x in pids if x!='IDLE')})
    fig=go.Figure()
    for s in segments:
        dur=s['end']-s['start']
        fig.add_trace(go.Bar(x=[dur],y=['CPU'],base=[s['start']],orientation='h',name=s['pid'],marker_color=colors[s['pid']],marker_line_color='#0B1020',marker_line_width=2,showlegend=False,text=[s['pid']],textposition='inside',insidetextanchor='middle',hovertemplate=f"<b>{s['pid']}</b><br>Start: {s['start']}<br>End: {s['end']}<br>Duration: {dur}<extra></extra>"))
    end=max((s['end'] for s in segments),default=1)
    fig.update_layout(barmode='overlay',height=230,margin=dict(l=35,r=20,t=15,b=35),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font_color='#CBD5E1',xaxis=dict(title='Time units',range=[0,end],dtick=1,gridcolor='#26334A',zeroline=False),yaxis=dict(showticklabels=False),hoverlabel=dict(bgcolor='#151C2E'))
    return fig

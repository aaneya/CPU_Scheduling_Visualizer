import plotly.graph_objects as go

# Muted, print-safe palette — see DESIGN.md
PALETTE = [
    "#1F4E79", "#2E75B6", "#A6611A", "#4D7C5F",
    "#7F5A83", "#B08D57", "#6B7B8C", "#9C4A3C",
]
INK = "#1A1A1A"
MUTED = "#5F5F5F"
FAINT = "#8A8A8A"
RULE = "#DAD5C9"
GRID = "#E7E2D8"
IDLE = "#B9B2A3"
SURFACE = "#FFFFFF"
SERIF = "Source Serif 4, Georgia, serif"
MONO = "IBM Plex Mono, SFMono-Regular, Consolas, monospace"


def make_gantt(segments):
    """Horizontal execution trace. One CPU row, muted process colors, gray idle."""
    pids = list(dict.fromkeys(s["pid"] for s in segments))
    colors = {"IDLE": IDLE}
    colors.update(
        {p: PALETTE[i % len(PALETTE)] for i, p in enumerate(x for x in pids if x != "IDLE")}
    )

    fig = go.Figure()
    for s in segments:
        dur = s["end"] - s["start"]
        fig.add_trace(
            go.Bar(
                x=[dur],
                y=["CPU"],
                base=[s["start"]],
                orientation="h",
                name=s["pid"],
                marker_color=colors[s["pid"]],
                marker_line_color=SURFACE,
                marker_line_width=1,
                showlegend=False,
                text=[s["pid"]],
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(family=MONO, size=10, color="#FFFFFF"),
                hovertemplate=(
                    f"<b>{s['pid']}</b><br>"
                    f"start&nbsp;&nbsp;{s['start']}<br>"
                    f"end&nbsp;&nbsp;&nbsp;&nbsp;{s['end']}<br>"
                    f"duration&nbsp;{dur}"
                    "<extra></extra>"
                ),
            )
        )

    end = max((s["end"] for s in segments), default=1)
    fig.update_layout(
        barmode="overlay",
        height=210,
        margin=dict(l=18, r=18, t=18, b=42),
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font=dict(family=MONO, size=11, color=MUTED),
        hoverlabel=dict(
            bgcolor=SURFACE,
            bordercolor=RULE,
            font=dict(family=MONO, size=11, color=INK),
        ),
        xaxis=dict(
            title=dict(text="time (units)", font=dict(family=MONO, size=10, color=FAINT)),
            range=[0, end],
            dtick=1,
            gridcolor=GRID,
            gridwidth=1,
            linecolor=IDLE,
            linewidth=1,
            zeroline=False,
            tickfont=dict(family=MONO, size=10, color=FAINT),
        ),
        yaxis=dict(showticklabels=False, showgrid=False),
    )
    return fig

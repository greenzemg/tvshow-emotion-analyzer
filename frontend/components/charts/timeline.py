import solara
import plotly.express as px
import pandas as pd
import frontend.components.charts.emotion_colors as emotion_colors


@solara.component
def EmotionTimeline(df: pd.DataFrame, video_name: str):
    """
    Displays the emotional fluctuation over time for a single video.
    """
    with solara.Card(f"Timeline: {video_name}"):
        emotion_cols = [
            "angry",
            "disgust",
            "fear",
            "happy",
            "sad",
            "surprise",
            "neutral",
        ]
        plot_cols = [c for c in emotion_cols if c in df.columns]

        if plot_cols:
            fig = px.line(
                df,
                x="timestamp",
                y=plot_cols,
                labels={"value": "Confidence score (%)", "timestamp": "Time"},
                color_discrete_map=emotion_colors.EMOTION_COLORS,
                markers=True,
                height=400,
            )
            fig.update_layout(
                xaxis_title="Time",
                yaxis_title="Probability (0-100)",
                margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                ),
            )
            solara.FigurePlotly(fig)
        else:
            solara.Text("No emotion columns found.")

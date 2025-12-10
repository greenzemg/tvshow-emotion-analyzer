import solara
import plotly.express as px
import pandas as pd
import frontend.components.charts.emotion_colors as emotion_colors


@solara.component
def DominantEmotionTimeline(df: pd.DataFrame, video_name: str):
    """
    Displays a scatter plot of the dominant emotion over time.
    Helps visualize state changes (e.g., when the mood shifts).
    """
    with solara.Card("Dominant Emotion Flow: " + video_name):
        if "dominant_emotion" in df.columns and "timestamp" in df.columns:
            # We map emotions to specific colors for consistency if possible,
            # but auto-coloring works for MVP.

            fig = px.scatter(
                df,
                x="timestamp",
                y="dominant_emotion",
                color="dominant_emotion",
                color_discrete_map=emotion_colors.EMOTION_COLORS,
                title="Dominant Emotion States",
                height=400,
                labels={"timestamp": "Time", "dominant_emotion": "State"},
            )

            # Update markers to be distinct
            fig.update_traces(
                marker=dict(size=10, line=dict(width=1, color="DarkSlateGrey"))
            )

            # Improve layout
            fig.update_layout(
                xaxis_title="Time",
                yaxis_title="Emotion",
                margin=dict(l=20, r=20, t=40, b=20),
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                ),
            )

            solara.FigurePlotly(fig)
        else:
            solara.Text("No dominant emotion data found.")

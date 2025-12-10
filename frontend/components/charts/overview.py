import solara
import plotly.express as px
import pandas as pd
from frontend.components.charts.emotion_colors import EMOTION_COLORS


@solara.component
def GlobalOverviewChart(df: pd.DataFrame):
    """
    Displays a Grouped Bar Chart comparing average emotional intensity across all videos.
    """
    with solara.Card("Global Overview"):
        # solara.Markdown("_Compare the average emotional intensity across all videos._")

        emotion_cols = [
            "angry",
            "disgust",
            "fear",
            "happy",
            "sad",
            "surprise",
            "neutral",
        ]
        valid_cols = [c for c in emotion_cols if c in df.columns]

        if valid_cols:
            # Group by filename and get mean
            df_grouped = df.groupby("file_name")[valid_cols].mean().reset_index()

            # Transform for Plotly (Wide to Long)
            df_melted = df_grouped.melt(
                id_vars=["file_name"], var_name="Emotion", value_name="Intensity"
            )

            fig = px.bar(
                df_melted,
                x="file_name",
                y="Intensity",
                color="Emotion",
                color_discrete_map=EMOTION_COLORS,
                barmode="group",
                height=350,
            )
            fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            solara.FigurePlotly(fig)
        else:
            solara.Text("No emotion data available.")

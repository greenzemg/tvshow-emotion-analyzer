import solara
import plotly.express as px
import pandas as pd


@solara.component
def ComparisonHeatmap(df: pd.DataFrame):
    """
    Displays a Heatmap to identify emotion outliers across videos.
    """
    with solara.Card("Emotion Heatmap Comparison"):
        # solara.Markdown("_Darker colors indicate higher intensity/probability._")

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
            df_matrix = df_grouped.set_index("file_name")

            # Dynamic height
            h = max(350, len(df_matrix) * 40)

            fig = px.imshow(
                df_matrix,
                labels=dict(x="Emotion", y="Video File", color="Intensity"),
                x=valid_cols,
                y=df_matrix.index,
                color_continuous_scale="RdBu_r",
                aspect="auto",
                height=h,
            )
            fig.update_xaxes(side="top")
            fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))

            solara.FigurePlotly(fig)
        else:
            solara.Text("No emotion data available.")

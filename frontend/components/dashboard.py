import solara
import os
import pandas as pd
import plotly.express as px

# import plotly.graph_objects as go
import frontend.state.global_state as state

from frontend.components.charts.overview import GlobalOverviewChart
from frontend.components.charts.heatmap import ComparisonHeatmap
from frontend.components.charts.timeline import EmotionTimeline
from frontend.components.charts.dominant_timeline import DominantEmotionTimeline


# Helper Functions
def time_to_seconds(timestamp_str):
    """Converts 'MM:SS' string to seconds (int) for plotting."""
    try:
        parts = str(timestamp_str).split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    # TODO: Handle the exception properly
    except (ValueError, TypeError):
        return 0
    return 0


@solara.component
def AnalyticsDashboard():
    """Right Panel: Visualization using reusable Chart Cards."""

    raw_path = os.path.join(state.output_path.value, "analysis_results.csv")
    summary_path = os.path.join(state.output_path.value, "summary_report.csv")

    has_raw = os.path.exists(raw_path)

    # Local state for selected video
    selected_video = solara.use_reactive(None)

    with solara.Column(
        style={"height": "100%", "min-height": "600px", "overflow-y": "auto"},
    ):
        solara.Markdown("## Analytics Dashboard")

        if state.is_processing.value:
            with solara.Column(
                align="center", gap="20px", style={"margin-top": "50px"}
            ):
                solara.SpinnerSolara(size="lg")
                solara.Text(
                    f"Status: {state.status_message.value}",
                    style={"font-size": "1.2em"},
                )

        elif has_raw:
            try:
                # Load Data
                df_raw = pd.read_csv(raw_path)

                if df_raw.empty:
                    solara.Warning("Analysis file is empty.")
                    return

                # SECTION 1: OVERVIEW 
                with solara.Columns([1, 1]):
                    GlobalOverviewChart(df_raw)
                    # solara.Markdown("<br>")
                    ComparisonHeatmap(df_raw)

                solara.Markdown("---")

                # SECTION 2: ANALYSIS PER VIDEO
                solara.Markdown("## 🔎 Detail View")

                videos = df_raw["file_name"].unique().tolist()

                # Auto-select first video
                if selected_video.value is None and videos:
                    selected_video.value = videos[0]

                solara.Select(
                    label="Select Video to Analyze", values=videos, value=selected_video
                )

                if selected_video.value:
                    # Prepare data for the specific video
                    df_video = df_raw[
                        df_raw["file_name"] == selected_video.value
                    ].copy()

                    # Sort by time
                    df_video["seconds"] = df_video["timestamp"].apply(time_to_seconds)
                    df_video = df_video.sort_values("seconds")

                    # 3D Landscape for the specific video
                    # Video3DChart(df_video, selected_video.value)
                    # solara.Markdown("<br>")

                    # Grid Layout for Detail Charts
                    with solara.Columns([1, 1]):
                        EmotionTimeline(df_video, selected_video.value)
                        # DominantEmotionDistribution(df_video)
                        DominantEmotionTimeline(df_video, selected_video.value)

                # SECTION 3: SUMMARY TABLE 
                if os.path.exists(summary_path):
                    solara.Markdown("---")

                    with solara.Card("📋 Summary Statistics"):
                        try:
                            df_summary = pd.read_csv(summary_path)
                            if not df_summary.empty:
                                solara.DataFrame(df_summary)
                            else:
                                solara.Text(
                                    "Summary file is empty.",
                                    style={"font-style": "italic"},
                                )
                        except Exception as csv_err:
                            solara.Error(f"Could not read summary: {csv_err}")

            except Exception as e:
                solara.Error(f"Error processing dashboard: {e}")

        else:
            with solara.Column(
                align="center", style={"margin-top": "50px", "color": "gray"}
            ):
                solara.Text("No analysis data found.")
                solara.Text("Please run an analysis to generate reports.")

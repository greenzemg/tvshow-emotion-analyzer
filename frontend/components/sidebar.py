import solara
import os
import frontend.state.global_state as state


def get_files(path):
    """Returns a list of files in a directory."""
    if os.path.exists(path):
        try:
            return [f for f in os.listdir(path) if not f.startswith(".")]
        except OSError:
            pass
    return []


@solara.component
def ConfigSidebar():
    """Sidebar: Configuration controls linked to Global State."""

    # Local error state for validation visual feedback
    input_error = solara.use_reactive("")
    output_error = solara.use_reactive("")

    # Refresh trigger state
    refresh_counter = solara.use_reactive(0)

    # Validation Logic 
    input_path_val = state.input_path.value
    output_path_val = state.output_path.value

    # Check existence
    input_exists = os.path.isdir(input_path_val) and os.path.exists(input_path_val)
    output_exists = os.path.isdir(output_path_val) and os.path.exists(output_path_val)

    # Sync errors
    if not input_exists and input_path_val:
        input_error.value = "Folder not found"
    else:
        input_error.value = ""

    if not output_exists and output_path_val:
        output_error.value = "Folder not found"
    else:
        output_error.value = ""

    # Fetch Files
    # Dependency on refresh_counter ensures re-execution
    _ = refresh_counter.value
    input_files = get_files(input_path_val) if input_exists else []
    output_files = get_files(output_path_val) if output_exists else []

    # UI Layout 
    with solara.Column(gap="2px", style="padding-left: 10px;"):
        solara.Text(
            "⚙️ Configuration", style={"font-weight": "bold", "font-size": "1.1em"}
        )

        # ==========================================
        # SECTION 1: Input Folder & Files
        # ==========================================
        with solara.Row(justify="space-between"):
            solara.Markdown(
                "#### 📂 Input Folder", style="margin-bottom: 0px; font-size: 0.9em;"
            )
            solara.Button(
                icon_name="mdi-refresh",
                on_click=lambda: refresh_counter.set(refresh_counter.value + 1),
                icon=True,
                text=False,
                small=True,
            )

        solara.InputText(
            label="Path to video folder",
            value=state.input_path,
            on_value=state.update_input_path,
            error=bool(input_error.value),
            message=input_error.value if input_error.value else None,
        )

        # File List (Scrollable)
        with solara.Column(
            style={
                "max-height": "150px",
                "overflow-y": "auto",
                "padding": "5px",
                "background-color": "#f9f9f9",
            }
        ):
            if not input_files:
                solara.Text(
                    "No videos found",
                    style={
                        "font-style": "italic",
                        "color": "gray",
                        "font-size": "0.8em",
                    },
                )
            else:
                with solara.Column(gap="2px"):
                    for f in input_files:
                        if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
                            solara.Text(f"🎥 {f}", style={"font-size": "0.8em"})

        # ==========================================
        # SECTION 2: Output Folder & Files
        # ==========================================
        with solara.Row(justify="space-between"):
            solara.Markdown(
                "#### 📂 Output Folder", style="margin-bottom: 0px; font-size: 0.9em;"
            )
            solara.Button(
                icon_name="mdi-refresh",
                on_click=lambda: refresh_counter.set(refresh_counter.value + 1),
                icon=True,
                text=False,
                small=True,
            )

        solara.InputText(
            label="Path to save results",
            value=state.output_path,
            on_value=state.update_output_path,
            error=bool(output_error.value),
            message=output_error.value if output_error.value else None,
        )

        # File List (Scrollable)
        with solara.Column(
            style={
                "max-height": "150px",
                "overflow-y": "auto",
                "padding": "5px",
                "background-color": "#f9f9f9",
            }
        ):
            if not output_files:
                solara.Text(
                    "No reports found",
                    style={
                        "font-style": "italic",
                        "color": "gray",
                        "font-size": "0.8em",
                    },
                )
            else:
                with solara.Column(gap="2px"):
                    for f in output_files:
                        if f.endswith(".csv"):
                            solara.Text(f"📊 {f}", style={"font-size": "0.8em"})

        solara.Markdown("---")

        # ==========================================
        # SECTION 3: Parameters
        # ==========================================
        solara.Text("PARAMETERS", style={"font-weight": "bold", "font-size": "1.1em"})

        solara.SliderInt(
            label="Frame Stride",
            value=state.frame_stride,
            min=1,
            max=60,
            thumb_label=True,
        )
        solara.Markdown(
            "*Higher stride = Faster speed*", style="font-size: 0.8em; color: gray;"
        )

        solara.Select(
            label="Model",
            value=state.detector_model,
            values=["DeepFace", "Model A", "Model C"],
        )

        solara.Markdown("---")

        # ==========================================
        # SECTION 4: Actions
        # ==========================================
        run_disabled = (not input_exists) or state.is_processing.value

        solara.Button(
            "RUN ANALYSIS",
            color="primary",
            icon_name="mdi-play",
            full_width=True,
            disabled=run_disabled,
            on_click=state.run_analysis_threaded,
        )

        solara.Button(
            "RESET SETTINGS",
            color="grey",
            icon_name="mdi-refresh",
            full_width=True,
            outlined=True,
            on_click=state.reset_settings,
        )

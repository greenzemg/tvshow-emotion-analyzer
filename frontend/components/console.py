import solara
import logging
import frontend.state.global_state as state


# Module-level flag to prevent multiple handler registrations
_handler_initialized = False


# LOGGING INTERCEPTOR
class SolaraLogHandler(logging.Handler):
    """
    Custom logging handler that pushes log records to the Solara UI state.
    """

    def emit(self, record):
        try:
            msg = self.format(record)
            state.add_log(msg)
        except Exception:
            self.handleError(record)


def setup_ui_logging():
    """
    Attaches the UI handler to the root logger.
    Safe to call multiple times (uses module flag to prevent duplicates).
    """
    global _handler_initialized

    if _handler_initialized:
        return

    root_logger = logging.getLogger()

    # Remove any existing SolaraLogHandler instances first
    handlers_to_remove = [
        h for h in root_logger.handlers if isinstance(h, SolaraLogHandler)
    ]
    for h in handlers_to_remove:
        root_logger.removeHandler(h)

    # Add the handler
    handler = SolaraLogHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s", datefmt="%H:%M:%S"
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    _handler_initialized = True


# Initialize logging immediately when this module is imported
setup_ui_logging()


# UI COMPONENT
@solara.component
def DebugConsole():
    """Bottom Panel: Shows system logs."""

    with solara.Card(
        "🖥️ Process Activities",
        style={
            "height": "200px",
            "background-color": "#1e1e1e",
            "color": "#00ff00",
            "overflow-y": "auto",
            "font-family": "monospace",
            "font-size": "0.9em",
        },
    ):
        if not state.logs.value:
            solara.Text(
                "> System ready. Logs will appear here...",
                style={"font-family": "monospace", "color": "#F7F2F2"},
            )

        # Display logs - each in its own Column to force new line
        with solara.Column(gap="0px", style="padding: 0; margin: 0;"):
            for log_line in state.logs.value:
                solara.Text(
                    f"> {log_line}",
                    style={
                        "font-family": "monospace",
                        "background-color": "#1e1e1e",
                        "color": "#E9E6E6",
                        "display": "block",
                        "white-space": "pre-wrap",
                        "margin": "0",
                        "padding": "1px 0",
                    },
                )

import solara

from frontend.components.sidebar import ConfigSidebar
from frontend.components.console import DebugConsole
from frontend.components.dashboard import AnalyticsDashboard


@solara.component
def Page():
    # 1. Sidebar Area
    with solara.Sidebar():
        ConfigSidebar()

    # 2. Main Content Area (Full Screen Height)
    with solara.Column(style={"height": "95vh", "padding": "10px"}):

        solara.Title("TV Show Emotion Analyzer")

        # Dashboard
        AnalyticsDashboard()

        # Bottom Section: Console
        with solara.Column(style={"margin-top": "15px", "flex-shrink": "0"}):
            DebugConsole()

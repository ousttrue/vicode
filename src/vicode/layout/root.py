from prompt_toolkit.application.current import get_app
import prompt_toolkit.layout
import prompt_toolkit.filters


class RootLayout:
    def __init__(self) -> None:
        from .sidebar_window import SidebarWindow
        from .editor_window import EditorWindow
        from .panel_window import PanelWindow
        from .command_window import CommandWindow
        self.panel = PanelWindow()
        self.sidebar = SidebarWindow()
        self.editor = EditorWindow()
        self.command = CommandWindow()

        inner = prompt_toolkit.layout.HSplit([
            self.editor,
            self.panel,
        ])

        outer = prompt_toolkit.layout.VSplit([
            self.sidebar,
            inner,
        ])

        self.container = prompt_toolkit.layout.HSplit([
            outer,
            self.command,
        ])

        self.has_focus = prompt_toolkit.filters.Condition(
            self._has_focus_any_window)

    def _has_focus_any_window(self):
        app = get_app()
        if app.layout.has_focus(self.editor.window) or app.layout.has_focus(self.panel.window) or app.layout.has_focus(self.sidebar.window):
            return True
        return False

    def __pt_conainer__(self) -> prompt_toolkit.layout.Container:
        return self.container

from prompt_toolkit.application.current import get_app
import prompt_toolkit.layout
import prompt_toolkit.filters
import prompt_toolkit.key_binding


class RootLayout:
    def __init__(self, kb: prompt_toolkit.key_binding.KeyBindings) -> None:
        from .sidebar_window import SidebarWindow
        from .editor_window import EditorWindow
        from .panel_window import PanelWindow
        from .command_window import CommandWindow
        from .message_window import MessageWindow
        self.panel = PanelWindow(kb)
        self.sidebar = SidebarWindow()
        self.editor = EditorWindow(kb)
        self.command = CommandWindow(kb)
        self.message = MessageWindow()

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
            prompt_toolkit.layout.ConditionalContainer(
                self.command, self.command.has_focus),
            prompt_toolkit.layout.ConditionalContainer(
                self.message, ~self.command.has_focus),
        ])

        self.has_focus = prompt_toolkit.filters.Condition(
            self._has_focus_any_window)

    def _has_focus_any_window(self):
        app = get_app()
        if self.editor.has_focus() or self.panel.has_focus() or app.layout.has_focus(self.sidebar.window):
            return True
        return False

    def __pt_conainer__(self) -> prompt_toolkit.layout.Container:
        return self.container

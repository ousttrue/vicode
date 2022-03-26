from prompt_toolkit.application.current import get_app
import prompt_toolkit.layout
import prompt_toolkit.filters
import prompt_toolkit.key_binding


class RootLayout:
    def __init__(self, kb: prompt_toolkit.key_binding.KeyBindings) -> None:
        self.kb = kb
        from .tab_window import TabWindow
        from ..editor.editor_window import EditorWindow
        from .command_window import CommandWindow
        from .message_window import MessageWindow
        from .logger_window import LoggerWindow
        self.sidebar = TabWindow(kb, style='class:sidebar', width=24)
        self.panel = TabWindow(kb, style='class:panel', height=16)
        self.editor = EditorWindow(kb)

        self.command = CommandWindow(kb)
        self.message = MessageWindow()
        self.logger = LoggerWindow(kb)
        self.panel.add(self.logger)

        inner = prompt_toolkit.layout.HSplit([
            self.editor,
            self.panel,
        ])

        outer = prompt_toolkit.layout.VSplit([
            self.sidebar,
            inner
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

        from ..event import EventType, DISPATCHER
        DISPATCHER.register(EventType.LspLaunched, self.on_lsp_launched)

    def on_lsp_launched(self, handler):
        from .diagnostics import Diagnostics
        diagnostics = Diagnostics(self.kb, handler.filetype)
        self.panel.add(diagnostics)

        from .. import lsp
        handler.client.callbacks[lsp.client.NotificationTypes.diagnostics] = diagnostics.on_diagnostics

    def _has_focus_any_window(self):
        app = get_app()
        if self.editor.has_focus() or self.sidebar.has_focus() or self.panel.has_focus():
            return True
        return False

    def __pt_conainer__(self) -> prompt_toolkit.layout.Container:
        return self.container

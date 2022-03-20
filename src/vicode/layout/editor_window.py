from prompt_toolkit.application.current import get_app
import prompt_toolkit.layout
import prompt_toolkit.buffer
import prompt_toolkit.key_binding
import prompt_toolkit.widgets
import prompt_toolkit.filters


class EditorWindow:
    def __init__(self) -> None:
        from .statusbar_window import StatusBarWindow, StatusBarRulerWindow

        self.buffer = prompt_toolkit.buffer.Buffer()
        self.control = prompt_toolkit.layout.BufferControl(self.buffer)
        self.window = prompt_toolkit.layout.Window(self.control)

        self.status = prompt_toolkit.layout.VSplit(
            [
                StatusBarWindow(lambda: 'status'),
                StatusBarRulerWindow(lambda: 'ruler'),
            ],
            # Ignore actual status bar width.
            width=prompt_toolkit.layout.dimension.Dimension()
        )

        self.window_status = prompt_toolkit.layout.HSplit(
            [
                self.window,
                self.status
            ])

        self.container = prompt_toolkit.layout.FloatContainer(
            content=prompt_toolkit.layout.Window(
                char=' ', ignore_content_width=True, ignore_content_height=True),
            floats=[
                prompt_toolkit.layout.Float(
                    self.window_status, left=0, top=0, right=0, bottom=0)
            ],
            style='class:editor')

        self.has_focus = prompt_toolkit.filters.has_focus(self.container)

        def on_active_changed(active):
            self.window_status.children[0] = active.__pt_container__()
            get_app().layout.focus(active)

        from .documents import Documents
        self.documents = Documents(on_active_changed)

    def __pt_container__(self) -> prompt_toolkit.layout.Container:
        return self.container

    def focus(self, event: prompt_toolkit.key_binding.KeyPressEvent):
        if self.documents.focus(event.app):
            return
        event.app.layout.focus(self.window)

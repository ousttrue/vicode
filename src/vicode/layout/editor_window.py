from typing import List, Optional
import pathlib
from prompt_toolkit.application.current import get_app
import prompt_toolkit.layout
import prompt_toolkit.buffer
import prompt_toolkit.key_binding
import prompt_toolkit.widgets
import prompt_toolkit.filters


class Document:
    def __init__(self, location: pathlib.Path) -> None:
        self.location = location
        self.textarea = prompt_toolkit.widgets.TextArea()
        self.textarea.text = location.read_text()

        from .statusbar_window import StatusBarWindow, StatusBarRulerWindow
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
                self.textarea,
                self.status
            ])

    def __pt_container__(self) -> prompt_toolkit.layout.Container:
        return self.window_status

    def __str__(self) -> str:
        return f'{self.location.name}'


class EditorWindow:
    def __init__(self, kb: prompt_toolkit.key_binding.KeyBindings) -> None:
        from .tab_window import TabWindow
        self.container = TabWindow(kb)
        self.has_focus = self.container.has_focus

    def __pt_container__(self) -> prompt_toolkit.layout.AnyContainer:
        return self.container.__pt_container__()

    def focus(self, event: prompt_toolkit.key_binding.KeyPressEvent):
        self.container.focus()

    def open_location(self, path: pathlib.Path):
        document = Document(path)
        self.container.tabs.add(document)

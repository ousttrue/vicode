import pathlib
from prompt_toolkit.application.current import get_app
import prompt_toolkit.layout
import prompt_toolkit.buffer
import prompt_toolkit.key_binding
import prompt_toolkit.widgets
import prompt_toolkit.filters


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
        from .editor_document import EditorDocument
        document = EditorDocument(path)
        self.container.add(document)

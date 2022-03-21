import pathlib
from prompt_toolkit.application.current import get_app
import prompt_toolkit.layout
import prompt_toolkit.buffer
import prompt_toolkit.key_binding
import prompt_toolkit.widgets
import prompt_toolkit.filters
from .tab_window import TabWindow


class EditorWindow(TabWindow):
    def __init__(self, kb: prompt_toolkit.key_binding.KeyBindings) -> None:
        super().__init__(kb, style='class:editor')

    def open_location(self, path: pathlib.Path):
        from .editor_document import EditorDocument
        document = EditorDocument(path)
        self.add(document)

from typing import NamedTuple, Optional
import pathlib
import prompt_toolkit.layout
import prompt_toolkit.buffer
import prompt_toolkit.key_binding
import prompt_toolkit.widgets
import prompt_toolkit.filters
from .tab_window import TabWindow


class OpenCommand(NamedTuple):
    location: pathlib.Path
    row: int = 0
    col: int = 0


class EditorWindow(TabWindow):
    def __init__(self, kb: prompt_toolkit.key_binding.KeyBindings) -> None:
        super().__init__(kb, style='class:editor')

        from ..event import EventType, DISPATCHER
        DISPATCHER.register(EventType.OpenCommand, self.open_location)

    def open_location(self, item):
        if isinstance(item, pathlib.Path):
            item = OpenCommand(item)
        assert(isinstance(item, OpenCommand))

        from .editor_document import EditorDocument
        for tab in self._tabs:
            if isinstance(tab, EditorDocument):
                if tab.location == item.location:
                    self.activate(tab)
                    tab.textarea.buffer.cursor_position = tab.textarea.buffer.document.translate_row_col_to_index(
                        item.row, item.col)
                    self.focus()
                    return

        tab = EditorDocument(item.location)
        tab.textarea.buffer.cursor_position = tab.textarea.buffer.document.translate_row_col_to_index(
            item.row, item.col)

        self.add(tab)

    def on_activated(self):
        if self._active is None:
            return
        from .editor_document import EditorDocument
        from ..event import EventType, DISPATCHER
        DISPATCHER.enqueue(EventType.DocumentActivated, self._active)

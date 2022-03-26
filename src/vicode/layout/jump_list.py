from typing import NamedTuple, List
import pathlib
import logging
from prompt_toolkit.application.current import get_app
import prompt_toolkit.key_binding
import prompt_toolkit.layout
import prompt_toolkit.filters
import prompt_toolkit.buffer
logger = logging.getLogger(__name__)


class JumpItem(NamedTuple):
    location: pathlib.Path
    row: int
    col: int
    text: str


class JumpList:
    '''
    input_processors でカーソル行をハイライトする
    '''

    def __init__(self, kb: prompt_toolkit.key_binding.KeyBindings, name: str, style: str = '') -> None:
        self.kb = kb
        self._items: List[JumpItem] = []
        self._buffer = prompt_toolkit.buffer.Buffer(name=name, read_only=True)
        self._control = prompt_toolkit.layout.BufferControl(
            self._buffer, focusable=True)
        self._container = prompt_toolkit.layout.Window(
            self._control, style=style)
        self.has_focus = prompt_toolkit.filters.has_focus(self._container)
        self._text = ''

        self._bind(self.jump, 'enter')

    def jump(self, event):
        row, col = self._buffer.document.translate_index_to_position(
            self._buffer.cursor_position)
        item = self._items[row]
        if isinstance(item, JumpItem):
            # logger.debug('enter')
            from ..event import EventType, DISPATCHER
            from ..editor.editor_window import OpenCommand
            DISPATCHER.enqueue(EventType.OpenCommand, OpenCommand(
                item.location, row=item.row, col=item.col))

    def __pt_container__(self) -> prompt_toolkit.layout.Container:
        return self._container

    def _bind(self, callback, *args):
        from prompt_toolkit.filters import vi_navigation_mode
        self.kb.add(
            *args, filter=(self.has_focus & vi_navigation_mode))(callback)

    def push_item(self, item: JumpItem):
        self._items.append(item)
        self._text += (item.text.rstrip() + '\n')
        self._buffer.read_only = prompt_toolkit.filters.Condition(
            lambda: False)
        self._buffer.text = self._text
        self._buffer.read_only = prompt_toolkit.filters.Condition(lambda: True)
        self._buffer.cursor_position = len(self._text)
        get_app().invalidate()

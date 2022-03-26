from typing import Optional
import logging
import re
import pathlib
import nerdfonts
from prompt_toolkit.application.current import get_app
import prompt_toolkit.widgets
import prompt_toolkit.layout
import prompt_toolkit.key_binding
import prompt_toolkit.key_binding.vi_state
import prompt_toolkit.selection
import prompt_toolkit.lexers
import prompt_toolkit.document
import prompt_toolkit.buffer
import prompt_toolkit.completion
import prompt_toolkit.filters

logger = logging.getLogger(__name__)


def create_lexer(location: Optional[pathlib.Path]) -> prompt_toolkit.lexers.Lexer:
    if location:
        return prompt_toolkit.lexers.PygmentsLexer.from_filename(str(location), sync_from_start=False)
    else:
        return prompt_toolkit.lexers.SimpleLexer()


FILE_TYPE_MAP = {
    '.py': 'python',
}


class DocumentWordsCompleter(prompt_toolkit.completion.Completer):
    """
    Completer that completes on words that appear already in the open document.

    TODO: LSP
    """

    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor()

        # Create a set of words that could be a possible completion.
        words = set()

        for w in re.split(r'\W', document.text):
            if len(w) > 1:
                if w.startswith(word_before_cursor) and w != word_before_cursor:
                    words.add(w)

        # Yield Completion instances.
        for w in sorted(words):
            yield prompt_toolkit.completion.Completion(w, start_position=-len(word_before_cursor))


class EditorDocument:
    def __init__(self, location: pathlib.Path, kb: prompt_toolkit.key_binding.KeyBindings) -> None:
        self.location = location
        self.buffer = prompt_toolkit.buffer.Buffer(
            completer=DocumentWordsCompleter()
        )
        self.has_focus = prompt_toolkit.filters.has_focus(self.buffer)
        self.control = prompt_toolkit.layout.BufferControl(
            self.buffer, lexer=create_lexer(location))
        self.container = prompt_toolkit.layout.Window(self.control, left_margins=[
            prompt_toolkit.layout.NumberedMargin(),
        ])
        self.buffer.text = location.read_text()

        self.ft = FILE_TYPE_MAP[location.suffix.lower()]

        from ..layout.statusbar_window import StatusBarWindow, StatusBarRightWindow
        self.status = prompt_toolkit.layout.VSplit(
            [
                StatusBarWindow(self.get_status),
                StatusBarRightWindow(self.get_status_right),
            ],
            # Ignore actual status bar width.
            width=prompt_toolkit.layout.dimension.Dimension()
        )

        self.window_status = prompt_toolkit.layout.HSplit(
            [
                self.status,
                self.container,
            ])

        self.kb = kb
        self._bind(self.apply_formatter, "escape", "F")

    def _bind(self, callback, *args):
        from prompt_toolkit.filters import vi_navigation_mode
        self.kb.add(
            *args, filter=(self.has_focus & vi_navigation_mode))(callback)

    def apply_formatter(self, event):
        logger.debug('format')

    @property
    def filetype(self) -> Optional[str]:
        return self.ft

    def __pt_container__(self) -> prompt_toolkit.layout.Container:
        return self.window_status

    def __str__(self) -> str:
        return f'{self.location.name}'

    def get_status(self):
        app = get_app()

        insert_mode = app.vi_state.input_mode in (
            prompt_toolkit.key_binding.vi_state.InputMode.INSERT,
            prompt_toolkit.key_binding.vi_state.InputMode.INSERT_MULTIPLE)
        replace_mode = app.vi_state.input_mode == prompt_toolkit.key_binding.vi_state.InputMode.REPLACE
        sel = self.buffer.selection_state
        temp_navigation = app.vi_state.temporary_navigation_mode
        visual_line = sel is not None and sel.type == prompt_toolkit.selection.SelectionType.LINES
        visual_block = sel is not None and sel.type == prompt_toolkit.selection.SelectionType.BLOCK
        visual_char = sel is not None and sel.type == prompt_toolkit.selection.SelectionType.CHARACTERS

        text = []
        if get_app().layout.has_focus(self.buffer):
            if insert_mode:
                if temp_navigation:
                    text.append(('class:status.mode.insert', '(insert)'))
                # elif editor.paste_mode:
                #     return ' -- INSERT (paste)--'
                else:
                    text.append(('class:status.mode.insert', ' INSERT '))
            elif replace_mode:
                if temp_navigation:
                    text.append(('class:status.mode.replace', '(replace)'))
                else:
                    text.append(('class:status.mode.replace', ' REPLACE '))
            elif visual_block:
                text.append(('class:status.mode.visual', ' VISUAL BLOCK '))
            elif visual_line:
                text.append(('class:status.mode.visual', ' VISUAL LINE '))
            elif visual_char:
                text.append(('class:status.mode.visual', ' VISUAL '))
            else:
                text.append(('class:status.mode.normal', ' NORMAL '))
        else:
            text.append(('class:status.mode.nofocus', ' NOFOCUS '))

        # text.append(('class:status.location', ' '))
        # text.append(('class:status.location', self.location.name))
        # text.append(('class:status.location', ' '))

        return text

    def get_status_right(self):
        text = []

        text.append(('class:status.filetype', f' {self.ft} '))
        if self.ft == '.py':
            text.append(('class:status.filetype',
                        f'{nerdfonts.icons["dev_python"]} '))

        row = self.buffer.document.cursor_position_row + 1
        col = self.buffer.document.cursor_position_col + 1
        text.append(('class:status.row', f'{row:4d}'))

        info = self.container.render_info
        if info:
            if info.full_height_visible:
                text.append(('class:status.row', ' All '))
            elif info.top_visible:
                text.append(('class:status.row', ' Top '))
            elif info.bottom_visible:
                text.append(('class:status.row', ' Bot '))
            else:
                percentage = info.vertical_scroll_percentage
                text.append(('class:status.row', f' {percentage:02d}% '))

        text.append(('class:status.col', f'{col:4d}'))

        return text

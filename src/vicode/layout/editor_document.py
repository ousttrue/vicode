from typing import Optional
import pathlib
import nerdfonts
from prompt_toolkit.application.current import get_app
import prompt_toolkit.widgets
import prompt_toolkit.layout
import prompt_toolkit.key_binding.vi_state
import prompt_toolkit.selection


FILE_TYPE_MAP = {
    '.py': 'python',
}


class EditorDocument:
    def __init__(self, location: pathlib.Path) -> None:
        self.location = location
        self.textarea = prompt_toolkit.widgets.TextArea()
        self.textarea.text = location.read_text()

        self.ft = FILE_TYPE_MAP[location.suffix.lower()]

        from .statusbar_window import StatusBarWindow, StatusBarRightWindow
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
                self.textarea,
            ])

        # from ..event import EventType, DISPATCHER
        # DISPATCHER.enqueue(EventType.BufferCreated, self)

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
        sel = self.textarea.buffer.selection_state
        temp_navigation = app.vi_state.temporary_navigation_mode
        visual_line = sel is not None and sel.type == prompt_toolkit.selection.SelectionType.LINES
        visual_block = sel is not None and sel.type == prompt_toolkit.selection.SelectionType.BLOCK
        visual_char = sel is not None and sel.type == prompt_toolkit.selection.SelectionType.CHARACTERS

        text = []
        if get_app().layout.has_focus(self.textarea.buffer):
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

        row = self.textarea.document.cursor_position_row + 1
        col = self.textarea.document.cursor_position_col + 1
        text.append(('class:status.row', f'{row:4d}'))

        info = self.textarea.window.render_info
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

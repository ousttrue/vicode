import prompt_toolkit.layout
import prompt_toolkit.widgets


class MessageWindow:
    def __init__(self):
        self._text = [
            ('', 'message')
        ]
        self.container = prompt_toolkit.widgets.FormattedTextToolbar(
            self.get_text)

    def __pt_container__(self) -> prompt_toolkit.layout.Container:
        return self.container

    def get_text(self):
        # eb = editor.editor_layout.editor_root.window_arrangement.active_editor_buffer

        # lineno = eb.buffer.document.cursor_position_row
        # errors = eb.report_errors

        # for e in errors:
        #     if e.lineno == lineno:
        #         return e.formatted_text

        # return []
        return self._text

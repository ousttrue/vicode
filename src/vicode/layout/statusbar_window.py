from prompt_toolkit.application.current import get_app
import prompt_toolkit.layout
import prompt_toolkit.widgets
import prompt_toolkit.filters


class StatusBarRulerWindow:
    """
    The right side of the Vim toolbar, showing the location of the cursor in
    the file, and the vectical scroll percentage.
    """

    def __init__(self, get_tokens):
        # def get_scroll_text():
        #     info = buffer_window.render_info

        #     if info:
        #         if info.full_height_visible:
        #             return 'All'
        #         elif info.top_visible:
        #             return 'Top'
        #         elif info.bottom_visible:
        #             return 'Bot'
        #         else:
        #             percentage = info.vertical_scroll_percentage
        #             return '%2i%%' % percentage

        #     return ''

        # def get_tokens():
        #     main_document = buffer.document

        #     return [
        #         ('class:cursorposition', '(%i,%i)' % (main_document.cursor_position_row + 1,
        #                                               main_document.cursor_position_col + 1)),
        #         ('', ' - '),
        #         ('class:percentage', get_scroll_text()),
        #         ('', ' '),
        #     ]

        self.container = prompt_toolkit.layout.containers.Window(
            prompt_toolkit.layout.controls.FormattedTextControl(get_tokens),
            char=' ',
            align=prompt_toolkit.layout.containers.WindowAlign.RIGHT,
            style='class:toolbar.status',
            height=1,
        )

    def __pt_container__(self) -> prompt_toolkit.layout.Container:
        return self.container


class StatusBarWindow:
    """
    The status bar, which is shown below each window in a tab page.
    """

    def __init__(self, get_text):
        # def get_text():
        #     app = get_app()

        #     insert_mode = app.vi_state.input_mode in (
        #         InputMode.INSERT, InputMode.INSERT_MULTIPLE)
        #     replace_mode = app.vi_state.input_mode == InputMode.REPLACE
        #     sel = editor_buffer.buffer.selection_state
        #     temp_navigation = app.vi_state.temporary_navigation_mode
        #     visual_line = sel is not None and sel.type == SelectionType.LINES
        #     visual_block = sel is not None and sel.type == SelectionType.BLOCK
        #     visual_char = sel is not None and sel.type == SelectionType.CHARACTERS

        #     def mode():
        #         if get_app().layout.has_focus(editor_buffer.buffer):
        #             if insert_mode:
        #                 if temp_navigation:
        #                     return ' -- (insert) --'
        #                 elif editor.paste_mode:
        #                     return ' -- INSERT (paste)--'
        #                 else:
        #                     return ' -- INSERT --'
        #             elif replace_mode:
        #                 if temp_navigation:
        #                     return ' -- (replace) --'
        #                 else:
        #                     return ' -- REPLACE --'
        #             elif visual_block:
        #                 return ' -- VISUAL BLOCK --'
        #             elif visual_line:
        #                 return ' -- VISUAL LINE --'
        #             elif visual_char:
        #                 return ' -- VISUAL --'
        #         return '                     '

        #     def recording():
        #         if app.vi_state.recording_register:
        #             return 'recording '
        #         else:
        #             return ''

        #     return ''.join([
        #         ' ',
        #         recording(),
        #         (str(editor_buffer.location) or ''),
        #         (' [New File]' if editor_buffer.is_new else ''),
        #         ('*' if editor_buffer.has_unsaved_changes else ''),
        #         (' '),
        #         mode(),
        #     ])

        self.container = prompt_toolkit.widgets.FormattedTextToolbar(
            get_text,
            style='class:toolbar.status')

    def __pt_container__(self) -> prompt_toolkit.layout.Container:
        return self.container

from prompt_toolkit.application.current import get_app
import prompt_toolkit.layout
import prompt_toolkit.widgets
import prompt_toolkit.filters


class StatusBarRightWindow:
    def __init__(self, get_tokens):

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
    def __init__(self, get_text):
        self.container = prompt_toolkit.widgets.FormattedTextToolbar(
            get_text,
            style='class:toolbar.status')

    def __pt_container__(self) -> prompt_toolkit.layout.Container:
        return self.container

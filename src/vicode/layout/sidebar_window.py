import prompt_toolkit.layout


class SidebarWindow:
    def __init__(self) -> None:
        self.control = prompt_toolkit.layout.FormattedTextControl(
            lambda: "sidebar")
        self.window = prompt_toolkit.layout.Window(self.control)

        self.container = prompt_toolkit.layout.FloatContainer(
            content=prompt_toolkit.layout.Window(char=' ', ignore_content_width=True, ignore_content_height=True, width=24), floats=[], style='class:sidebar')

    def __pt_container__(self) -> prompt_toolkit.layout.Container:
        return self.container

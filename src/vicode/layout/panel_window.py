import prompt_toolkit.layout
import prompt_toolkit.buffer


class PanelWindow:
    def __init__(self) -> None:
        self.buffer = prompt_toolkit.buffer.Buffer()
        self.control = prompt_toolkit.layout.BufferControl(self.buffer)
        self.window = prompt_toolkit.layout.Window(self.control)

        self.container = prompt_toolkit.layout.FloatContainer(
            content=prompt_toolkit.layout.Window(
                char=' ', ignore_content_width=True, ignore_content_height=True, height=12),
            floats=[
                prompt_toolkit.layout.Float(
                    self.window, left=0, top=0, right=0, bottom=0)
            ],
            style='class:panel')

    def __pt_container__(self) -> prompt_toolkit.layout.Container:
        return self.container

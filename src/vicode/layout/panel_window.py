import prompt_toolkit.layout
import prompt_toolkit.buffer
import prompt_toolkit.key_binding
import prompt_toolkit.filters
from .tab_window import TabWindow


class PanelWindow(TabWindow):
    def __init__(self, kb: prompt_toolkit.key_binding.KeyBindings) -> None:
        super().__init__(kb, height=12, style='class:panel')

        from .logger_window import LoggerWindow
        self.logger = LoggerWindow()

        self.add(self.logger)

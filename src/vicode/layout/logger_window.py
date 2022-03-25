import pathlib
import logging
import prompt_toolkit.layout
import prompt_toolkit.formatted_text
import prompt_toolkit.buffer
import prompt_toolkit.filters
import prompt_toolkit.key_binding
from .jump_list import JumpList, JumpItem
logger = logging.getLogger(__name__)

NL = ('', '\n')
DEFAULT = '#AAAAAA bg:#000000'
DEBUG = DEFAULT
INFO = '#FFFFFF bg:#888888'
WARN = '#FFFFFF bg:#996600'
ERROR = '#FFFFFF bg:#990000'


class LoggerWindow(logging.Handler, JumpList):
    def __init__(self, kb: prompt_toolkit.key_binding.KeyBindings) -> None:
        super().__init__()
        JumpList.__init__(self, kb, name='logger')
        # self.logs: prompt_toolkit.formatted_text.StyleAndTextTuples = []
        # self.control = prompt_toolkit.layout.FormattedTextControl(
        #     lambda: self.logs, focusable=True)
        # self.container = prompt_toolkit.layout.Window(
        #     self.control, style=DEFAULT)

        # set root logger
        self.setFormatter(logging.Formatter(
            '%(filename)s:%(lineno)s: %(message)s'))
        logging.getLogger().handlers = [self]

    def emit(self, record: logging.LogRecord):
        msg = self.format(record)

        item = JumpItem(pathlib.Path(record.pathname), record.lineno-1, 0, msg)
        self.push_item(item)

        # match record.levelno:
        #     case logging.DEBUG:
        #         self.logs.append((DEFAULT, '[DEBUG]'))
        #     case logging.INFO:
        #         self.logs.append((INFO, '[INFO ]'))
        #     case logging.WARN:
        #         self.logs.append((WARN, '[WARN ]'))
        #     case logging.ERROR:
        #         self.logs.append((ERROR, '[ERROR]'))
        #     case _:
        #         raise NotImplementedError()
        # self.logs.append(('', msg))
        # self.logs.append(NL)
        # if self.get_line_count() > 8:
        #     self.container.vertical_scroll = self.get_line_count() - 8

    def write(self, m):
        pass

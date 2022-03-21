import logging
import prompt_toolkit.layout
import prompt_toolkit.formatted_text
from prompt_toolkit.application.current import get_app

NL = ('', '\n')
DEFAULT = '#AAAAAA bg:#000000'
DEBUG = DEFAULT
INFO = '#FFFFFF bg:#888888'
WARN = '#FFFFFF bg:#996600'
ERROR = '#FFFFFF bg:#990000'


class LoggerWindow(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.logs: prompt_toolkit.formatted_text.StyleAndTextTuples = []
        self.control = prompt_toolkit.layout.FormattedTextControl(
            lambda: self.logs, focusable=True)
        self.container = prompt_toolkit.layout.Window(
            self.control, style=DEFAULT)

        # set root logger
        self.setFormatter(logging.Formatter(
            '%(filename)s:%(levelno)s: %(message)s'))
        logging.getLogger().handlers = [self]

    def __pt_container__(self) -> prompt_toolkit.layout.Container:
        return self.container

    def __str__(self) -> str:
        return f'logger({self.get_line_count()})'

    def emit(self, record: logging.LogRecord):
        msg = self.format(record)

        match record.levelno:
            case logging.DEBUG:
                self.logs.append((DEFAULT, '[DEBUG]'))
            case logging.INFO:
                self.logs.append((INFO, '[INFO ]'))
            case logging.WARN:
                self.logs.append((WARN, '[WARN ]'))
            case logging.ERROR:
                self.logs.append((ERROR, '[ERROR]'))
            case _:
                raise NotImplementedError()
        self.logs.append(('', msg))
        self.logs.append(NL)
        # if self.get_line_count() > 8:
        #     self.container.vertical_scroll = self.get_line_count() - 8
        get_app().invalidate()

    def write(self, m):
        pass

    def get_line_count(self):
        return len([x for x in self.logs if x == NL])

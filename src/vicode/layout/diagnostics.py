import pathlib
from .jump_list import JumpList, JumpItem
from .. import lsp


class Diagnostics(JumpList):
    def __init__(self, kb, filetype: str) -> None:
        self.filetype = filetype
        super().__init__(kb, filetype)

    def __str__(self) -> str:
        return self.filetype

    def on_diagnostics(self, data: lsp.protocol.PublishDiagnosticsParams):
        location = pathlib.Path(data['uri'])
        for d in data['diagnostics']:
            start = d['range']['start']
            self.push_item(
                JumpItem(location, start['line'], start['character'], d['message']))

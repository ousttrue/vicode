from typing import List, Optional
import pathlib
import prompt_toolkit.widgets
import prompt_toolkit.layout


class Document:
    def __init__(self, location: pathlib.Path) -> None:
        self.location = location
        self.textarea = prompt_toolkit.widgets.TextArea()
        self.textarea.text = location.read_text()

    def __pt_container__(self) -> prompt_toolkit.layout.Container:
        return self.textarea.__pt_container__()


class Documents:
    def __init__(self) -> None:
        self.documents: List[Document] = []
        self.active: Optional[Document] = None

    def open_location(self, path: pathlib.Path):
        document = Document(path)
        self.documents.append(document)
        self.activate(document)

    def activate(self, document: Document):
        if self.active == document:
            return
        self.active = document
        from ..event import DISPATCHER, EventType
        DISPATCHER.enqueue(EventType.DocumentActivate, document)

    def activate_next(self, event):
        if not self.active:
            index = -1
        else:
            index = self.documents.index(self.active)
        self.activate(self.documents[index+1])

    def activate_prev(self, event):
        if not self.active:
            index = len(self.documents)
        else:
            index = self.documents.index(self.active)
        self.activate(self.documents[index-1])

    def focus(self, app) -> bool:
        if not self.active:
            return False
        app.layout.focus(self.active)
        return True

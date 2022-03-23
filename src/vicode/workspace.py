from typing import Dict, Optional, NamedTuple
import os
import asyncio
import pathlib
import logging
from .layout.editor_document import EditorDocument
from . import lsp

logger = logging.getLogger(__name__)


def get_workspace_dir(path: pathlib.Path) -> pathlib.Path:
    if path.is_file():
        path = path.parent

    return path


class DocumentActivate(NamedTuple):
    close_path: Optional[pathlib.Path]
    path: pathlib.Path
    filetype: str
    text: str
    version: int


async def process_async(queue: asyncio.Queue, client: lsp.client.Client, loop: asyncio.AbstractEventLoop):
    logger.debug(f'{client}: launch...')
    await client.launch(loop)

    # initialize
    response = await client.request_initialize(lsp.protocol.InitializeParams(
        processId=os.getpid(),
        capabilities=lsp.protocol.ClientCapabilities(),
    ))

    # initialized
    client.notify_initialized(lsp.protocol.InitializedParams())

    logger.info(f'{client}: initialized')

    while True:
        lsp_command = await queue.get()
        logger.debug(type(lsp_command))
        match lsp_command:
            case DocumentActivate(active, path, filetype, text, version):
                if active:
                    client.notify_textDocument_didClose(lsp.protocol.DidCloseTextDocumentParams(
                        textDocument=lsp.protocol.TextDocumentIdentifier(
                            uri=str(active)
                        )
                    ))

                logger.info(f'notify_textDocument_didOpen')
                client.notify_textDocument_didOpen(lsp.protocol.DidOpenTextDocumentParams(
                    textDocument=lsp.protocol.TextDocumentItem(
                        uri=str(path),
                        languageId=filetype,
                        version=version,
                        text=text
                    )
                ))


class ClientHandler:
    def __init__(self, filetype: str, client: lsp.client.Client):
        self.filetype = filetype
        self.client = client
        self._active: Optional[pathlib.Path] = None
        self._version = 0
        self.queue = asyncio.Queue()

    def on_error(self, message: str):
        logger.warn(f'{self}: {message}')

    def activate(self, path: pathlib.Path, filetype: str, text: str):
        if path == self._active:
            return
        self.queue.put_nowait(DocumentActivate(
            self._active, path, filetype, text, 1))
        self._version = 1
        self._active = path


class WorkSpace:
    def __init__(self, path: pathlib.Path) -> None:
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.workspace_dir = get_workspace_dir(path)
        logger.info(f'{self.workspace_dir}')
        from .event import EventType, DISPATCHER
        DISPATCHER.register(EventType.DocumentActivated, self.on_document_activated)

        self.lsp: Dict[str, ClientHandler] = {}

    def on_document_activated(self, buffer):
        assert(isinstance(buffer, EditorDocument))
        filetype = buffer.filetype
        if not filetype:
            return

        client = self.get_or_launch_lsp(filetype)
        if client:
            client.activate(buffer.location, filetype, buffer.textarea.text)

    def get_or_launch_lsp(self, filetype: str) -> Optional[ClientHandler]:
        assert(isinstance(self.loop, asyncio.AbstractEventLoop))
        handler = self.lsp.get(filetype)
        if not handler:
            client = lsp.client.create_client(self.workspace_dir, filetype)
            if not client:
                return
            handler = ClientHandler(filetype, client)
            self.lsp[filetype] = handler
            self.loop.create_task(process_async(
                handler.queue, handler.client,  self.loop))

        return handler

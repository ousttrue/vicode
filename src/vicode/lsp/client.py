'''
https://microsoft.github.io/language-server-protocol/specifications/specification-current/
'''
from typing import Optional
import pathlib
import platform
import asyncio
import logging
from . import jsonrpc_2_0
from .import protocol
logger = logging.getLogger(__name__)

if platform.system() == 'Windows':
    LSP_COMMAND_MAP = {
        'python': ['C:/Python310/Scripts/pyls.exe'],
    }
else:
    LSP_COMMAND_MAP = {
        'python': ['pyls'],
    }


class Client:
    def __init__(self, *command: str, workspace_dir: Optional[pathlib.Path] = None) -> None:
        self.command = command
        self.workspce_dir = workspace_dir

    async def launch(self, loop: asyncio.AbstractEventLoop):
        self._process = await asyncio.subprocess.create_subprocess_exec(*self.command,
                                                                        stdin=asyncio.subprocess.PIPE,
                                                                        stdout=asyncio.subprocess.PIPE,
                                                                        stderr=asyncio.subprocess.PIPE,
                                                                        )

        self.rpcDispatcher = jsonrpc_2_0.RpcDispatcher()
        loop.create_task(self._out_async())
        loop.create_task(self._err_async())

    # def __del__(self):
    #     if isinstance(self._process.returncode, int):
    #         return
    #     self.notify_exit()

    async def _out_async(self):
        if not self._process:
            return
        if not self._process.stdout:
            return
        logger.debug('read stdout')
        while True:
            if self._process.stdout.at_eof():
                logger.error('end stdout')
                break

            await self.rpcDispatcher.read_rpc_message_async(self._process.stdout)

    async def _err_async(self):
        if not self._process:
            return
        if not self._process.stderr:
            return
        logger.debug('read stderr')
        while True:
            if self._process.stderr.at_eof():
                logger.error('end stderr')
                break
            l = await self._process.stderr.readline()
            logger.error(l.decode('utf-8'))

    async def request_initialize(self, params: protocol.InitializeParams):
        '''
        https://microsoft.github.io/language-server-protocol/specifications/specification-current/#initialize
        '''
        assert(self._process.stdin)
        future = self.rpcDispatcher.request(
            self._process.stdin, 'initialize', params)
        return await future

    async def request_shutdown(self):
        '''
        https://microsoft.github.io/language-server-protocol/specifications/specification-current/#shutdown
        '''
        assert(self._process.stdin)
        future = self.rpcDispatcher.request(
            self._process.stdin, 'shutdown', None)
        return await future

    def notify_exit(self):
        '''
        https://microsoft.github.io/language-server-protocol/specifications/specification-current/#exit        
        '''
        assert(self._process.stdin)
        self.rpcDispatcher.notify(self._process.stdin, 'exit', None)

    def notify_initialized(self, params: protocol.InitializedParams):
        '''
        https://microsoft.github.io/language-server-protocol/specifications/specification-current/#initialized
        '''
        assert(self._process.stdin)
        self.rpcDispatcher.notify(self._process.stdin, 'initialized', params)

    def notify_textDocument_didOpen(self, params: protocol.DidOpenTextDocumentParams):
        '''
        https://microsoft.github.io/language-server-protocol/specifications/specification-current/#textDocument_didOpen        
        '''
        assert(self._process.stdin)
        self.rpcDispatcher.notify(
            self._process.stdin, 'textDocument/didOpen', params)

    def notify_textDocument_didClose(self, params: protocol.DidCloseTextDocumentParams):
        '''
        https://microsoft.github.io/language-server-protocol/specifications/specification-current/#textDocument_didClose        
        '''
        assert(self._process.stdin)
        self.rpcDispatcher.notify(
            self._process.stdin, 'textDocument/didClose', params)


async def popen_pyls(loop: asyncio.events.AbstractEventLoop) -> Client:
    return await popen(loop, *LSP_COMMAND_MAP['python'])


async def popen(loop: asyncio.events.AbstractEventLoop, *command: str) -> Client:

    client = Client(*command)
    await client.launch(loop)
    return client


def create_client(workspace_dir: pathlib.Path, filetype: str) -> Optional[Client]:
    command = LSP_COMMAND_MAP.get(filetype)
    if not command:
        return

    client = Client(*command, workspace_dir=workspace_dir)

    return client

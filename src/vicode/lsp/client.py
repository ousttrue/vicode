'''
https://microsoft.github.io/language-server-protocol/specifications/specification-current/
'''
import asyncio
import logging
from . import jsonrpc_2_0
from .import protocol
logger = logging.getLogger(__name__)


class Client:
    def __init__(self, loop: asyncio.events.AbstractEventLoop, process: asyncio.subprocess.Process) -> None:
        assert(process)
        assert(process.stdin)
        self.loop = loop
        self._process = process
        self.rpcDispatcher = jsonrpc_2_0.RpcDispatcher()
        self.loop.create_task(self._out_async())
        self.loop.create_task(self._err_async())

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


async def popen(loop: asyncio.events.AbstractEventLoop, path='C:/Python310/Scripts/pyls.exe', *args):
    proc = await asyncio.subprocess.create_subprocess_exec(path, *args,
                                                           stdin=asyncio.subprocess.PIPE,
                                                           stdout=asyncio.subprocess.PIPE,
                                                           stderr=asyncio.subprocess.PIPE,
                                                           )
    return Client(loop, proc)

'''
https://microsoft.github.io/language-server-protocol/specifications/specification-current/
'''
import asyncio
import logging
from . import jsonrpc_2_0
from .import basic_structures
from .import protocol
logger = logging.getLogger(__name__)


class LanguageServer:
    def __init__(self, loop: asyncio.events.AbstractEventLoop, process: asyncio.subprocess.Process) -> None:
        assert(process)
        assert(process.stdin)
        self.loop = loop
        self._process = process
        self.rpcDispatcher = jsonrpc_2_0.RpcDispatcher()
        self.loop.create_task(self._out_async())
        self.loop.create_task(self._err_async())

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

    async def requestInitialize(self, params: protocol.InitializeParams):
        assert(self._process.stdin)
        future = self.rpcDispatcher.request(
            self._process.stdin, 'initialize', params)
        return await future


async def popen(loop: asyncio.events.AbstractEventLoop, path='C:/Python310/Scripts/pyls.exe', *args):
    proc = await asyncio.subprocess.create_subprocess_exec(path, *args,
                                                           stdin=asyncio.subprocess.PIPE,
                                                           stdout=asyncio.subprocess.PIPE,
                                                           stderr=asyncio.subprocess.PIPE,
                                                           )
    return LanguageServer(loop, proc)

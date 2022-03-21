from typing import TypedDict, Dict
import re
import json
import asyncio
import logging
logger = logging.getLogger(__name__)


class Request(TypedDict):
    # "2.0"
    jsonrpc: str
    # increment
    id: int
    # "textDocument/didOpen"
    method: str
    params: dict


def make_request(request_id: int, method: str, params) -> Request:
    return Request(
        jsonrpc="2.0",
        id=request_id,
        method=method,
        params=params
    )


CONTENT_TYPE = re.compile(r'^Content-Length: (\d+)\r\n$')


class LanguageServer:
    def __init__(self, loop: asyncio.events.AbstractEventLoop, process: asyncio.subprocess.Process) -> None:
        assert(process)
        assert(process.stdin)
        self.loop = loop
        self._process = process
        self._request_id = 1

        self._request_map: Dict[int, asyncio.Future] = {}

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
            # header
            length = 0
            while True:
                l = await self._process.stdout.readline()
                if l == b'\r\n':
                    break

                header = l.decode('ascii')
                m = CONTENT_TYPE.match(header)
                if m:
                    length = int(m.group(1))
            # body
            body = await self._process.stdout.read(length)

            await self.process_message_async(json.loads(body))

    async def process_message_async(self, value: dict):
        message_id = value.get('id')
        if isinstance(message_id, int):
            method = value.get('method')
            if method:
                # request
                return await self.process_request_async(message_id, method, value.get('params'))

            error = value.get('error')
            if error:
                # error response
                return await self.process_error_async(message_id, error)

            # success response
            await self.process_response_async(message_id, value.get('result'))
        else:
            code = value.get('code')
            if isinstance(code, int):
                # notification
                await self.process_notification_async(code, value.get('message'), value.get('data'))
            else:
                raise RuntimeError(value)

    async def process_request_async(self, message_id: int, method: str, params):
        raise NotImplementedError()

    async def process_response_async(self, message_id: int, result):
        future = self._request_map[message_id]
        future.set_result(result)

    async def process_error_async(self, message_id: int, error):
        raise NotImplementedError()

    async def process_notification_async(self, code: int, message, data):
        raise NotImplementedError()

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

    def _request(self, method: str, params: dict):
        assert(self._process.stdin)
        request_id = self._request_id
        self._request_id += 1
        future = asyncio.Future()
        assert(request_id not in self._request_map)
        self._request_map[request_id] = future

        request = make_request(request_id, method, params)
        bin = json.dumps(request).encode('utf-8')

        # write
        header = f'Content-Length: {len(bin)}\r\n'
        self._process.stdin.write(header.encode('ascii'))
        self._process.stdin.write(b'\r\n')
        self._process.stdin.write(bin)

        return future

    async def requestInitialize(self):
        future = self._request('initialize', {
            'capabilities': {}
        })
        return await future


async def popen(loop: asyncio.events.AbstractEventLoop, path='C:/Python310/Scripts/pyls.exe', *args):
    proc = await asyncio.subprocess.create_subprocess_exec(path, *args,
                                                           stdin=asyncio.subprocess.PIPE,
                                                           stdout=asyncio.subprocess.PIPE,
                                                           stderr=asyncio.subprocess.PIPE,
                                                           )
    return LanguageServer(loop, proc)

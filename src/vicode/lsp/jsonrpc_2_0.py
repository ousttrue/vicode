from typing import TypedDict, Dict
import re
import asyncio
import json


class Message(TypedDict):
    # "2.0"
    jsonrpc: str


class Request(Message):
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


class RpcDispatcher:
    def __init__(self) -> None:
        self._request_id = 1
        self._request_map: Dict[int, asyncio.Future] = {}

    async def read_rpc_message_async(self, stdout: asyncio.StreamReader):
        length = 0
        while True:
            l = await stdout.readline()
            if l == b'\r\n':
                break

            header = l.decode('ascii').rstrip()
            key, value = header.split(':', 1)
            match key:
                case 'Content-Length':
                    length = int(value)
                case 'Content-Type':
                    pass
                case _:
                    # unknown
                    raise NotImplementedError(header)
        # body
        body = await stdout.read(length)
        message = json.loads(body)

        message_id = message.get('id')
        if isinstance(message_id, int):
            method = message.get('method')
            if method:
                # request
                return await self.process_request_async(message_id, method, message.get('params'))

            error = message.get('error')
            if error:
                # error response
                return await self.process_error_async(message_id, error)

            # success response
            await self.process_response_async(message_id, message.get('result'))
        else:
            method = message.get('method')
            if method:
                # notification
                await self.process_notification_async(method, message.get('params'))
            else:
                raise RuntimeError(message)

    async def process_request_async(self, message_id: int, method: str, params):
        raise NotImplementedError()

    async def process_response_async(self, message_id: int, result):
        future = self._request_map[message_id]
        future.set_result(result)

    async def process_error_async(self, message_id: int, error):
        raise NotImplementedError()

    async def process_notification_async(self, method: str, data):
        raise NotImplementedError()

    def request(self, stdin: asyncio.StreamWriter, method: str, params: dict) -> asyncio.Future:
        request_id = self._request_id
        self._request_id += 1
        future = asyncio.Future()
        assert(request_id not in self._request_map)
        self._request_map[request_id] = future

        request = make_request(request_id, method, params)
        bin = json.dumps(request).encode('utf-8')

        # write
        header = f'Content-Length: {len(bin)}\r\n'
        stdin.write(header.encode('ascii'))
        stdin.write(b'\r\n')
        stdin.write(bin)

        return future

from typing import TypedDict, Dict, Any, Optional
import asyncio
import json
import logging

logger = logging.getLogger(__name__)


class Message(TypedDict):
    # "2.0"
    jsonrpc: str


class ParamsOptional(TypedDict, total=False):
    params: dict


class Request(Message, ParamsOptional):
    # increment
    id: int
    # "textDocument/didOpen"
    method: str


def make_request(request_id: int, method: str, params) -> Request:
    if params is None:
        return Request(
            jsonrpc="2.0",
            id=request_id,
            method=method,
        )
    else:
        return Request(
            jsonrpc="2.0",
            id=request_id,
            method=method,
            params=params
        )


class Notification(Message, ParamsOptional):
    method: str


def make_notification(method: str, params) -> Notification:
    if params is None:
        return Notification(
            jsonrpc="2.0",
            method=method,
        )
    else:
        return Notification(
            jsonrpc="2.0",
            method=method,
            params=params
        )


def send_message(stdin: asyncio.StreamWriter, message):
    bin = json.dumps(message).encode('utf-8')

    # write
    header = f'Content-Length: {len(bin)}\r\n'
    stdin.write(header.encode('ascii'))
    stdin.write(b'\r\n')
    stdin.write(bin)


class RpcDispatcher:
    def __init__(self) -> None:
        self._request_id = 1
        self._request_map: Dict[int, asyncio.Future] = {}
        self._notify_map: Dict[str, Any] = {}

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
        callback = self._notify_map.get(method)
        if not callback:
            logger.warning(f'unknown notification: {method} => {data}')
            return
        callback(data)

    def request(self, stdin: asyncio.StreamWriter, method: str, params) -> asyncio.Future:
        request_id = self._request_id
        self._request_id += 1
        future = asyncio.Future()
        assert(request_id not in self._request_map)
        self._request_map[request_id] = future

        message = make_request(request_id, method, params)
        send_message(stdin, message)

        return future

    def notify(self, stdin: asyncio.StreamWriter, method: str, params):
        message = make_notification(method, params)
        send_message(stdin, message)

    def on_notify(self, method: str, callback):
        self._notify_map[method] = callback

from typing import Any, NamedTuple, Dict, TypeAlias, Callable
import logging
import asyncio
from enum import Enum, auto


logger = logging.getLogger(__name__)


class EventType(Enum):
    DocumentActivate = auto()


class EventValue(NamedTuple):
    event_type: EventType
    payload: Any


EventHandler: TypeAlias = Callable[[Any], None]


class EventDispatcher:
    def __init__(self) -> None:
        self._queue = asyncio.Queue()
        self._handlers: Dict[EventType, EventHandler] = {}

    def start(self, loop: asyncio.events.AbstractEventLoop):
        loop.create_task(self._worker())

    def register(self, event_type: EventType, handler: EventHandler):
        assert(event_type not in self._handlers)
        self._handlers[event_type] = handler

    def _handle(self, event_type: EventType, palyload: Any) -> bool:
        try:
            self._handlers[event_type](palyload)
            return True
        except Exception as e:
            logger.exception(e)
            raise

    async def _worker(self):
        logger.info('start worker')
        while True:
            if not self._queue.empty():
                event = self._queue.get_nowait()
            else:
                event = await self._queue.get()
            logger.debug(event)

            if not self._handle(*event):
                logger.error('unhandled event: %s', event)

    def enqueue(self, event_type: EventType, payload: Any):
        self._queue.put_nowait(EventValue(event_type, payload))


DISPATCHER = EventDispatcher()

from typing import Any, NamedTuple, Dict, TypeAlias, Callable, Optional
import logging
import asyncio
from enum import Enum, auto


logger = logging.getLogger(__name__)


class EventType(Enum):
    # acitive
    OpenCommand = auto()
    BufferFocusCommand = auto()
    # passive
    Invalidated = auto()
    BufferCreated = auto()
    DocumentActivated = auto()
    LspLaunched = auto()


class EventValue(NamedTuple):
    event_type: EventType
    payload: Any

    def __str__(self) -> str:
        return f'<{self.event_type}, {self.payload}>'


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
        handler = self._handlers.get(event_type)
        if not handler:
            logger.error(f'handler not found: {event_type}')
            return False

        try:
            handler(palyload)
            return True
        except Exception as e:
            logger.exception(e)
            # raise
            return False

    async def _worker(self):
        logger.info('start worker')
        while True:
            event = await self._queue.get()
            logger.debug(event)

            try:
                if not self._handle(*event):
                    logger.error('unhandled event: %s', event)
            except Exception as e:
                logger.exception(e)

    def enqueue(self, event_type: EventType, payload: Any):
        self._queue.put_nowait(EventValue(event_type, payload))


DISPATCHER = EventDispatcher()

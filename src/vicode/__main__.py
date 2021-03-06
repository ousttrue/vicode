import asyncio
import logging
import pathlib
import argparse
import prompt_toolkit
import prompt_toolkit.layout
import prompt_toolkit.output
import prompt_toolkit.cursor_shapes
import prompt_toolkit.key_binding
import prompt_toolkit.key_binding.vi_state
import prompt_toolkit.enums


class App:
    def __init__(self) -> None:
        self.kb = prompt_toolkit.key_binding.KeyBindings()
        from .layout.root import RootLayout
        from .layout.style import STYLE
        self.root = RootLayout(self.kb)
        self.application = prompt_toolkit.Application(
            layout=prompt_toolkit.layout.Layout(
                self.root.container,
                self.root.editor
            ),
            full_screen=True,

            key_bindings=self.kb,
            editing_mode=prompt_toolkit.enums.EditingMode.VI,

            style=STYLE,
            color_depth=prompt_toolkit.output.color_depth.ColorDepth.DEPTH_24_BIT,
            cursor=prompt_toolkit.cursor_shapes.CursorShape.BLOCK,
        )

        self._bind(self.root.sidebar.focus, 'c-w', 'h')
        self._bind(self.root.editor.focus, 'c-w', 'l')
        self._bind(self.root.panel.focus, 'c-w', 'j')
        self._bind(self.root.editor.focus, 'c-w', 'k')
        self._bind(self.focus_command, ':')

        from.event import DISPATCHER, EventType

        def on_focus(container):
            assert(container)
            self.application.layout.focus(container)
            self.application.invalidate()

        DISPATCHER.register(EventType.BufferFocusCommand, on_focus)

        from .workspace import WorkSpace
        self.workspace = WorkSpace(pathlib.Path('.'))

    def _bind(self, callback, *args):
        from prompt_toolkit.filters import vi_navigation_mode
        self.kb.add(
            *args, filter=(self.root.has_focus & vi_navigation_mode))(callback)

    def get_current_window(self) -> prompt_toolkit.layout.Window:
        return self.application.layout.current_window

    def focus(self, target):
        self.application.layout.focus(target)

    def focus_command(self, event: prompt_toolkit.key_binding.KeyPressEvent):
        event.app.layout.focus(self.root.command.buffer)
        event.app.vi_state.input_mode = prompt_toolkit.key_binding.vi_state.InputMode.INSERT

    async def run_async(self):
        def pre_run():
            assert(isinstance(self.application.loop, asyncio.AbstractEventLoop))
            from .event import DISPATCHER
            DISPATCHER.start(self.application.loop)

            # Start in navigation mode.
            self.application.vi_state.input_mode = prompt_toolkit.key_binding.vi_state.InputMode.NAVIGATION

            self.workspace.loop = self.application.loop

        await self.application.run_async(pre_run=pre_run)


async def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("location", nargs="*")
    args = parser.parse_args()

    app = App()
    from .event import EventType, DISPATCHER
    for location in args.location:
        DISPATCHER.enqueue(EventType.OpenCommand,
                           pathlib.Path(location).absolute())
    await app.run_async()


if __name__ == '__main__':
    asyncio.run(main())


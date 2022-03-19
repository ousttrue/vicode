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
        self.root = RootLayout()
        self.application = prompt_toolkit.Application(
            layout=prompt_toolkit.layout.Layout(self.root.container),
            full_screen=True,

            key_bindings=self.kb,
            editing_mode=prompt_toolkit.enums.EditingMode.VI,

            style=STYLE,
            color_depth=prompt_toolkit.output.color_depth.ColorDepth.DEPTH_24_BIT,
            cursor=prompt_toolkit.cursor_shapes.CursorShape.BLOCK,
        )

        self._bind(self.focus_sidebar, 'c-w', 'h')
        self._bind(self.focus_panel, 'c-w', 'j')
        self._bind(self.focus_editor, 'c-w', 'k')
        self._bind(self.focus_editor, 'c-w', 'l')
        self._bind(self.focus_command, ':')

    def _bind(self, callback, *args):
        from prompt_toolkit.filters import vi_navigation_mode
        self.kb.add(
            *args, filter=(self.root.has_focus & vi_navigation_mode))(callback)

    def get_current_window(self) -> prompt_toolkit.layout.Window:
        return self.application.layout.current_window

    def focus(self, target):
        self.application.layout.focus(target)

    def focus_sidebar(self, event):
        self.focus(self.root.sidebar.buffer)

    def focus_editor(self, event):
        self.focus(self.root.editor.buffer)

    def focus_panel(self, event):
        self.focus(self.root.panel.buffer)

    def focus_command(self, event: prompt_toolkit.key_binding.KeyPressEvent):
        event.app.layout.focus(self.root.command.buffer)
        event.app.vi_state.input_mode = prompt_toolkit.key_binding.vi_state.InputMode.INSERT

    async def run_async(self):
        def pre_run():
            # Start in navigation mode.
            self.application.vi_state.input_mode = prompt_toolkit.key_binding.vi_state.InputMode.NAVIGATION
        await self.application.run_async(pre_run=pre_run)


async def main():
    app = App()
    await app.run_async()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

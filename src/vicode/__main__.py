import prompt_toolkit
import prompt_toolkit.layout
import prompt_toolkit.output
import prompt_toolkit.cursor_shapes
import prompt_toolkit.key_binding


class App:
    def __init__(self) -> None:
        self.kb = prompt_toolkit.key_binding.KeyBindings()
        from .layout.root import RootLayout
        from .layout.style import STYLE
        # side / editor_bottom
        self.root = RootLayout()
        self.application = prompt_toolkit.Application(
            layout=prompt_toolkit.layout.Layout(self.root.container),
            full_screen=True,
            key_bindings=self.kb,
            style=STYLE,
            color_depth=prompt_toolkit.output.color_depth.ColorDepth.DEPTH_24_BIT,
            cursor=prompt_toolkit.cursor_shapes.CursorShape.BLOCK,
        )


async def main():
    app = App()
    await app.application.run_async()

if __name__ == '__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(main())

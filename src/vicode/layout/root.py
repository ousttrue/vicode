import prompt_toolkit.layout


class RootLayout:
    def __init__(self) -> None:
        from .sidebar_window import SidebarWindow
        from .editor_window import EditorWindow
        from .panel_window import PanelWindow
        self.panel = PanelWindow()
        self.sidebar = SidebarWindow()
        self.editor = EditorWindow()

        inner = prompt_toolkit.layout.HSplit([
            self.editor,
            self.panel,
        ])

        self.container = prompt_toolkit.layout.VSplit([
            self.sidebar,
            inner,
        ])

    def __pt_conainer__(self) -> prompt_toolkit.layout.Container:
        return self.container

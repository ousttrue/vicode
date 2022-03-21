from typing import List, Optional
from prompt_toolkit.application.current import get_app
import prompt_toolkit
import prompt_toolkit.key_binding
import prompt_toolkit.layout
import prompt_toolkit.filters
import prompt_toolkit.widgets


class TabWindow:
    '''
    +-------------+
    |tab [tab] tab|
    +-------------+
    |active window|
    +-------------+
    active: selected and visible
    focus: active and has_focus(cursor)
    '''

    def __init__(self, kb: prompt_toolkit.key_binding.KeyBindings, style='', height: prompt_toolkit.layout.AnyDimension = None) -> None:
        self.kb = kb

        self._tabs: List[prompt_toolkit.layout.AnyContainer] = []
        self._active: Optional[prompt_toolkit.layout.AnyContainer] = None
        padding = prompt_toolkit.layout.Window(
            height=1, width=prompt_toolkit.layout.Dimension(weight=99))
        self.tabbar = prompt_toolkit.layout.containers.VSplit(
            [padding], height=1, padding=1)

        self.empty_control = prompt_toolkit.layout.FormattedTextControl(lambda: [
                                                                        ('', 'empty')], focusable=True)
        self.empty = prompt_toolkit.layout.Window(
            self.empty_control, align=prompt_toolkit.layout.WindowAlign.CENTER)

        self.tabbar_body = prompt_toolkit.layout.HSplit(
            [
                self.tabbar,
                self.empty,
            ])

        self.container = prompt_toolkit.layout.FloatContainer(
            content=prompt_toolkit.layout.Window(
                char=' ', ignore_content_width=True, ignore_content_height=True, height=height),
            floats=[
                prompt_toolkit.layout.Float(
                    self.tabbar_body, left=0, top=0, right=0, bottom=0)
            ],
            style=style
        )

        self.has_focus = prompt_toolkit.filters.has_focus(self.container)

        self._bind(self.activate_next, 'escape', 'l')
        self._bind(self.activate_prev, 'escape', 'h')

    def __pt_container__(self) -> prompt_toolkit.layout.Container:
        return self.container

    def _bind(self, callback, *args):
        from prompt_toolkit.filters import vi_navigation_mode
        self.kb.add(
            *args, filter=(self.has_focus & vi_navigation_mode))(callback)

    def add(self, container: prompt_toolkit.layout.AnyContainer, is_active=True):
        self._tabs.append(container)

        def get_title():
            style = 'class:tab.active' if self._active == container else 'class:tab'
            text = str(container)
            return [(style, text)]
        pos = len(self.tabbar.children)-1
        self.tabbar.children.insert(pos,
                                    prompt_toolkit.widgets.FormattedTextToolbar(get_title))
        if is_active:
            self.activate(container)

    def activate(self, document: prompt_toolkit.layout.AnyContainer):
        if self._active == document:
            return
        self._active = document
        self.tabbar_body.children[1] = prompt_toolkit.layout.to_container(
            self._active)
        get_app().layout.focus(self._active)
        get_app().invalidate()

    def activate_next(self, event: prompt_toolkit.key_binding.KeyPressEvent):
        if not self._active:
            index = 0
        else:
            index = self._tabs.index(self._active) + 1
        if index < len(self._tabs):
            self.activate(self._tabs[index])

    def activate_prev(self, event: prompt_toolkit.key_binding.KeyPressEvent):
        if not self._active:
            index = len(self._tabs)-1
        else:
            index = self._tabs.index(self._active)-1
        if index >= 0 and index < len(self._tabs):
            self.activate(self._tabs[index])

    def focus(self, event=None):
        if self._active:
            get_app().layout.focus(self._active)
        else:
            get_app().layout.focus(self.empty)

from typing import List, Optional
from prompt_toolkit.application.current import get_app
import prompt_toolkit
import prompt_toolkit.key_binding
import prompt_toolkit.layout
import prompt_toolkit.filters


class Tabs:
    '''
    active: selected and visible
    focus: active and has_focus(cursor)
    '''

    def __init__(self, on_activated) -> None:
        self.on_tab_activated = on_activated
        self._tabs: List[prompt_toolkit.layout.AnyContainer] = []
        self._active: Optional[prompt_toolkit.layout.AnyContainer] = None

    def activate(self, document: prompt_toolkit.layout.AnyContainer):
        if self._active == document:
            return
        self._active = document
        # from ..event import DISPATCHER, EventType
        # DISPATCHER.enqueue(EventType.Invalidated, None)
        self.on_tab_activated(document)
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

    def add(self, container: prompt_toolkit.layout.AnyContainer, is_active=True):
        self._tabs.append(container)
        if is_active:
            self.activate(container)

    def get_text(self):
        text = []
        for i, tab in enumerate(self._tabs):
            style = 'class:tab.active' if tab == self._active else 'class:tab'
            text.append((style, f'{i} {tab}'))
        return text

    def focus(self) -> bool:
        if not self._active:
            return False
        get_app().layout.focus(self._active)
        return True


class TabBar:
    def __init__(self) -> None:
        self.control = prompt_toolkit.layout.controls.FormattedTextControl()
        self.contrainer = prompt_toolkit.layout.containers.Window(
            self.control, height=1)

    def set_text(self, text):
        # self.control.reset()
        self.control.text = text


class TabWindow:
    '''
    +-------------+
    |tab [tab] tab|
    +-------------+
    |active window|
    +-------------+
    '''

    def __init__(self, kb: prompt_toolkit.key_binding.KeyBindings) -> None:
        self.kb = kb
        self.tabs = Tabs(self.on_active_changed)
        self.tabbar = TabBar()

        self.empty_control = prompt_toolkit.layout.FormattedTextControl(lambda: [
                                                                        ('', 'empty')], focusable=True)
        self.empty = prompt_toolkit.layout.Window(
            self.empty_control, align=prompt_toolkit.layout.WindowAlign.CENTER)

        self.tabbar_body = prompt_toolkit.layout.HSplit(
            [
                self.tabbar.contrainer,
                self.empty,
            ])

        self.container = prompt_toolkit.layout.FloatContainer(
            content=prompt_toolkit.layout.Window(
                char=' ', ignore_content_width=True, ignore_content_height=True),
            floats=[
                prompt_toolkit.layout.Float(
                    self.tabbar_body, left=0, top=0, right=0, bottom=0)
            ],
            style='class:editor')

        self.has_focus = prompt_toolkit.filters.has_focus(self.container)

        self._bind(self.tabs.activate_next, 'escape', 'l')
        self._bind(self.tabs.activate_prev, 'escape', 'h')

    def on_active_changed(self, active: prompt_toolkit.layout.AnyContainer):
        self.tabbar_body.children[1] = prompt_toolkit.layout.to_container(
            active)
        self.tabbar.set_text(self.tabs.get_text())
        get_app().layout.focus(active)
        get_app().invalidate()
        # DISPATCHER.register(EventType.BufferFocusCommand, on_active_changed)

    def __pt_container__(self) -> prompt_toolkit.layout.Container:
        return self.container

    def focus(self):
        if not self.tabs.focus():
            get_app().layout.focus(self.empty)

    def _bind(self, callback, *args):
        from prompt_toolkit.filters import vi_navigation_mode
        self.kb.add(
            *args, filter=(self.has_focus & vi_navigation_mode))(callback)

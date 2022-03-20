from prompt_toolkit.application.current import get_app
import prompt_toolkit.buffer
import prompt_toolkit.filters
import prompt_toolkit.layout
import prompt_toolkit.layout.processors
import prompt_toolkit.key_binding
import prompt_toolkit.key_binding.vi_state


class CommandWindow:

    def __init__(self, kb: prompt_toolkit.key_binding.KeyBindings):
        # Create history and search buffers.

        def handle_action(buff: prompt_toolkit.buffer.Buffer) -> bool:
            ' When enter is pressed in the Vi command line. '
            text = buff.text  # Remember: leave_command_mode resets the buffer.

            self.leave()

            # from .handler import handle_command
            # handle_command(text)
            # Execute command.
            if text in ('q', 'qa'):
                get_app().exit()

            # clear
            return False

        self.buffer = prompt_toolkit.buffer.Buffer(
            accept_handler=handle_action,
            multiline=False,
        )
        self.has_focus = prompt_toolkit.filters.has_focus(self.buffer)

        self.control = prompt_toolkit.layout.controls.BufferControl(self.buffer,
                                                                    input_processors=[
                                                                        prompt_toolkit.layout.processors.BeforeInput(':')],
                                                                    )

        self.container = prompt_toolkit.layout.Window(
            self.control, height=1)

        @kb.add('escape', filter=self.has_focus)
        @kb.add('c-c', filter=self.has_focus)
        @kb.add('backspace', filter=self.has_focus & prompt_toolkit.filters.Condition(lambda: self.buffer.text == ''))
        def leave_command_mode(event):
            """
            Leaving command mode.
            """
            self.leave()

    def __pt_container__(self) -> prompt_toolkit.layout.Container:
        return self.container

    def leave(self):
        get_app().layout.focus_last()

        # First leave command mode. We want to make sure that the working
        # pane is focussed again before executing the command handlers.
        get_app().vi_state.input_mode = prompt_toolkit.key_binding.vi_state.InputMode.NAVIGATION

        self.buffer.reset(
            # append_to_history=append_to_history
        )

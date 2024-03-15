
from prompt_toolkit.completion import Completer, Completion

class MyCompleter(Completer):
    """
    Custom completer for command-line input.

    Attributes:
        commands (list): List of available commands.

    Methods:
        get_completions: Retrieves completion suggestions for the current input.
    """
    def __init__(self, commands):
        """
        Initializes a MyCompleter instance.

        Args:
            commands (list): List of available commands.
        """
        self.commands = commands

    def get_completions(self, document, complete_event):
        """
        Retrieves completion suggestions for the current input.

        Args:
            document (Document): The current input document.
            complete_event: The completion event.

        Yields:
            Completion: Completion suggestions for the current input.
        """
        text = document.text_before_cursor
        if " " not in text:
            for command in self.commands:
                if command.startswith(text):
                    yield Completion(command, start_position=-len(text))
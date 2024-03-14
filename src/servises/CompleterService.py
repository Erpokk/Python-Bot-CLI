
from prompt_toolkit.completion import Completer, Completion

class MyCompleter(Completer):
    def __init__(self, commands):
        self.commands = commands

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if " " not in text:
            for command in self.commands:
                if command.startswith(text):
                    yield Completion(command, start_position=-len(text))
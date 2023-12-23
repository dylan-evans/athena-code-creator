
from openai.types.beta.threads import ThreadMessage
from openai.types.beta.thread import Thread
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt


class ChatView:
    def __init__(self, console: Console):
        self.console = console

    def show_assistant_message(self, message: ThreadMessage):
        values = (con.text.value for con in message.content if con.type == "text")
        for text in values:
            panel = Panel(
                Markdown(text),
                title=f"Assistant {message.assistant_id or ''}",
                style="white on color(237)"
            )
            self.console.print(panel)

    def show_user_message(self, message: ThreadMessage):
        values = (con.text.value for con in message.content if con.type == "text")
        for text in values:
            self.console.print(text)

    def show_thread(self, thread: Thread):
        pass


class ChatPrompt:
    """
    This class captures chat prompts interactively, which includes
    the capability to handle multiline prompts and acc commands.
    """
    def __init__(self, console: Console):
        self.console = console

    def chat_prompt(self):
        while True:
            line = Prompt.get_input(
                self.console,
                "[bold red]chat:[/bold red] ",
                password=False
            ).strip()
            if not line:
                continue
            if line.startswith("\\"):  # Multiline mode
                pass
            if line.startswith("/"):  # Command mode
                pass


import time
import readline
from logging import info, basicConfig, WARNING
from typing import Any

import openai
import click
#from print_color import print
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from openai.types.beta.threads.run_submit_tool_outputs_params import RunSubmitToolOutputsParams, ToolOutput
from openai.types.beta.threads.required_action_function_tool_call import RequiredActionFunctionToolCall, Function
from openai.types.beta.threads.thread_message import ThreadMessage

from athena_code_creator.tool_functions import BaseFunction, WriteFileFunction, ReadFileFunction, ExecFunction
from athena_code_creator.config import AthenaConfig
from .assistant import AssistantInterface

from progress.spinner import Spinner

ACC_CONFIG = "athena-code-creator.json"

ConfigMap = dict[str, str]


def main():
    cli()


@click.group()
def cli():
    basicConfig(level=WARNING)


@cli.command
def init():
    """Setup assistants in a given path."""


@cli.command
def remove_assistant():
    """Remove current assistant."""


@cli.command
@click.argument("message")
def send(message):
    acc, thread = setup_athena()
    info("Sending request")
    console = Console()
    console.print(f"[bold red]chat:[/bold red] {message}")
    send_cmd(console, thread, message)


@cli.command
@click.option("--message", "-m")
def chat(message):
    acc, thread = setup_athena()
    info("Sending request")
    console = Console()

    if message:
        console.print(f"[bold red]chat:[/bold red] {message}")
        send_cmd(console, thread, message)

    while True:
        line = Prompt.get_input(console, "[bold red]chat:[/bold red] ", password=False)
        if not line:
            continue
        send_cmd(console, thread, line)


def send_cmd(console, thread, line):
    op = thread.send(line)
    with console.status("Working...", spinner="bouncingBall") as status:
        while not op.ready():
            for mesg in op.get_log_messages():
                console.log(mesg)
            time.sleep(0.2)
        resp = op.get_response()

    for content in resp.content:
        if content.type == "text":
            console.print(Panel(Markdown(content.text.value), title=f"GPT", style="white on color(237)"))


def setup_athena() -> AssistantInterface:
    # Use OPENAI_API_KEY environment var
    client = openai.OpenAI()
    functions = [WriteFileFunction, ReadFileFunction, ExecFunction]
    config, config_exists = AthenaConfig.load_config_or_get_defaults(ACC_CONFIG)
    if config_exists:
        acc = AssistantInterface.retrieve(client, config.assistant_id, functions)
        thread = acc.retrieve_thread(config.thread_id)
    else:
        acc = create_athena(client, functions)
        thread = acc.create_thread()

    if not config_exists:
        info("Writing config file")
        config.assistant_id = acc.assistant.id
        config.thread_id = thread.thread.id
        config.save(ACC_CONFIG)
    return acc, thread


def create_athena(client: openai.OpenAI, functions: list[BaseFunction]):
    return AssistantInterface.create(client, functions, {
        "name": "Athena Code Creator",
        "instructions": """\
            You are a cutting edge code creator working with an Engineer to create code.
            * Work in the local directory, place files under "./".
            * Output will be printed to the terminal as markdown via the python library "rich".
        """,
        "tools": [{"type": "code_interpreter"}] + [{"type": "function", "function": func.get_function()} for func in functions],
#        "model": "gpt-3.5-turbo-1106",
        "model": "gpt-4-1106-preview",
    })

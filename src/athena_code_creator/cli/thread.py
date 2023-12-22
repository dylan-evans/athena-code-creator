
import click

from .cli import cli, CLI


@cli.group
@click.pass_obj
def thread(obj: CLI):
    if obj.config.selected_assistant_id is None:
        raise click.ClickException("No assistant selected")


@thread.command
@click.pass_obj
def create(obj: CLI):
    with obj.console.status("Working..."):
        thread = obj.openai.beta.threads.create()
    obj.config.selected_thread_id = thread.id
    obj.console.print(f"Thread [bold]{thread.id}[/bold] created and selected.")



@thread.command
@click.pass_obj
def delete(obj: CLI):
    pass


@thread.command
@click.pass_obj
def list(obj: CLI):
    pass

@thread.command
@click.pass_obj
def create(obj: CLI):
    pass

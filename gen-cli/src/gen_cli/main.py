import click
from .build import build
from .list import list_repositories, list_tags
from .deploy import deploy
from .setup import setup
from .utils import get_registry_address, is_setup_complete

class PrivateRegistryCLI(click.MultiCommand):
    def list_commands(self, ctx):
        return ['setup', 'build', 'list-repositories', 'list-tags', 'deploy']

    def get_command(self, ctx, cmd_name):
        if cmd_name == 'setup':
            return setup
        elif not is_setup_complete() and cmd_name != 'setup':
            click.echo("Please run 'gen-cli setup' first to configure the registry address.", err=True)
            return None
        elif cmd_name == 'build':
            return build
        elif cmd_name == 'list-repositories':
            return list_repositories
        elif cmd_name == 'list-tags':
            return list_tags
        elif cmd_name == 'deploy':
            return deploy

@click.command(cls=PrivateRegistryCLI)
@click.pass_context
def cli(ctx):
    """CLI for interacting with GenSphere platform."""
    ctx.ensure_object(dict)
    if is_setup_complete():
        ctx.obj['registry_address'] = get_registry_address()

if __name__ == "__main__":
    cli()
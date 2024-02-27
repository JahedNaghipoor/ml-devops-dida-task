import logging

import typer

from ml_devops_dida_task import __title__, __version__, util

logger = logging.getLogger('ml_devops_dida_task')

app = typer.Typer(name='ml_devops_dida_task')


def version_callback(version: bool):
    if version:
        typer.echo(f"{__title__} {__version__}")
        raise typer.Exit()


ConfigOption = typer.Option(
    ...,
    '-c',
    '--config',
    metavar='PATH',
    help="path to the program configuration"
)
VersionOption = typer.Option(
    None,
    '-v',
    '--version',
    callback=version_callback,
    is_eager=True,
    help="print the program version and exit"
)


@app.command()
def main(config_file: str = ConfigOption, version: bool = VersionOption):
    """
    In this sample project you are going to deploy a simple text classification service based on a pretrained NLP

    Note: This is the entry point of your command line application. The values of the CLI params
    that are passed to this application will show up als parameters to this function.
    This docstring is where you describe what your command line application does.
    Try running `python -m ml_devops_dida_task --help` to see how this shows up in the
    command line.
    """
    config = util.load_config(config_file)
    util.logging_setup(config)
    logger.info("Looks like you're all set up. Let's get going!")
    # TODO your journey starts here


if __name__ == "__main__":
    app()

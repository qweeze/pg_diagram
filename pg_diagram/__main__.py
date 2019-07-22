import click

from . import base


@click.command()
@click.argument(
    'schema',
    type=click.File(),
)
@click.option(
    '-f', '--format',
    type=click.Choice(['png', 'svg', 'dot']),
    default='png',
    help='Output format',
)
@click.option(
    '-o', '--output',
    type=click.File(mode='wb'),
    required=True,
)
def main(schema, format: str, output):
    """Converts postgresql schema to ER diagram"""
    try:
        graph = base.create_graph(*base.parse(schema.read()))
    except base.ParseError as exc:
        click.secho(
            f'Could not parse statement:\n{exc.statement}',
            fg='red',
        )
        exit(1)

    output.write(base.render(graph, format=format))


if __name__ == '__main__':
    main()

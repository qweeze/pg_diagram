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
    graph = base.create_graph(*base.parse(schema.read()))
    output.write(base.render(graph, format=format))


if __name__ == '__main__':
    main()

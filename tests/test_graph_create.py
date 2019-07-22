import pathlib

from pg_diagram import base


def test_grapth_create():
    schema = pathlib.Path('tests/schema.sql').read_text()
    graph = base.create_graph(*base.parse(schema))
    data = base.render(graph, format='dot')
    assert data.decode() == pathlib.Path('tests/graph.dot').read_text()

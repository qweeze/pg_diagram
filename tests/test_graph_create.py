from pathlib import Path

from pg_diagram import graph, parsing


def test_grapth_create() -> None:
    schema = Path("tests/schema.sql").read_text()
    g = graph.create_graph(parsing.parse(schema))
    data = graph.render(g, fmt="dot")
    assert data.decode() == Path("tests/graph.dot").read_text()

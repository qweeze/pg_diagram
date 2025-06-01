import tempfile
from pathlib import Path

import graphviz

from .parsing import ParseResult


def create_graph(parsed: ParseResult) -> graphviz.Digraph:
    graph = graphviz.Digraph(
        name="ERD",
        graph_attr={"randkir": "LR", "overlap": "false"},
        node_attr={"shape": "record", "fontsize": "9", "fontname": "Verdana"},
    )

    for table in parsed.tables:
        label = (
            '<\n<table border="0" cellborder="1" cellspacing="0" cellpadding="4">'
            + f'<tr><td bgcolor="lightblue"><b>{table.name}</b></td></tr>'
            + "\n".join(
                f"<tr>"
                f'<td port="{col.name}" align="left">'
                f"<b>{col.name}</b>: "
                f"{'<b>[PK]</b> ' if col.primary_key else ''}"
                f"<i>{col.data_type} "
                f"{' NOT NULL' if col.not_null else ''}</i>"
                "</td>"
                "</tr>"
                for col in table.columns.values()
            )
            + "</table>>"
        )
        graph.node(
            name=table.name,
            shape="none",
            label=label,
        )

    for fkey in parsed.foreign_keys:
        graph.edge(
            f"{fkey.table_name}:{fkey.column_name}",
            f"{fkey.foreign_table_name}:{fkey.foreign_column_name}",
        )

    return graph


def render(graph: graphviz.Digraph, fmt: str) -> bytes:
    with tempfile.TemporaryDirectory() as dirpath:
        graph.render("graph", format=fmt, directory=dirpath)
        data: bytes = (Path(dirpath) / f"graph.{fmt}").read_bytes()
    return data

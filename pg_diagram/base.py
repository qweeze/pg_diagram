import functools
import operator
import pathlib
import re
import tempfile
import typing as t
from dataclasses import dataclass

import graphviz
import sqlparse
import pyparsing as pp


@dataclass
class ForeignKey:
    table_name: str
    column_name: str
    foreign_table_name: str
    foreign_column_name: str


@dataclass
class Column:
    name: str
    data_type: str
    not_null: bool = False
    primary_key: bool = False


@dataclass
class Table:
    name: str
    columns: t.Dict[str, Column]


def _identifier(name: str) -> pp.Token:
    return (
        pp.Optional(pp.Suppress('"')) +
        pp.Word(pp.alphanums + '_')(name) +
        pp.Optional(pp.Suppress('"'))
    )


def _ignore(*words: str) -> pp.Token:
    return functools.reduce(
        operator.add,
        (pp.Optional(pp.CaselessKeyword(w)) for w in words),
    )


primary_key_expr: pp.ParseExpression = (
    _ignore('ALTER TABLE', 'ONLY', 'IF EXISTS') +
    _identifier('schema') + pp.Suppress('.') + _identifier('table_name') +
    _ignore('ADD CONSTRAINT') + _identifier('constraint_name') +
    _ignore('PRIMARY KEY') +
    pp.Suppress('(') + _identifier('column_name') + pp.Suppress(')')
)


foreign_key_expr: pp.ParseExpression = (
    _ignore('ALTER TABLE', 'ONLY', 'IF EXISTS') +
    _identifier('schema') + pp.Suppress('.') + _identifier('table_name') +
    _ignore('ADD CONSTRAINT') + _identifier('constraint_name') +
    _ignore('FOREIGN KEY') +
    pp.Suppress('(') + _identifier('column_name') + pp.Suppress(')') +
    _ignore('REFERENCES') +
    _identifier('foreign_schema') + pp.Suppress('.') + _identifier('foreign_table_name') +
    pp.Suppress('(') + _identifier('foreign_column_name') + pp.Suppress(')')
)


create_table_expr: pp.ParseExpression = (
    _ignore('CREATE', 'GLOBAL', 'LOCAL', 'TEMPORARY', 'TEMP', 'UNLOGGED', 'TABLE', 'IF NOT EXISTS') +
    _identifier('schema') + pp.Suppress('.') + _identifier('table_name') +
    pp.Suppress('(') +
    pp.delimitedList(
        (pp.Suppress('CONSTRAINT' + pp.Regex(r'[^\n,]+')))
        |
        pp.Group(
            _identifier('name') + _identifier('data_type') +
            pp.Suppress(pp.Optional(pp.Word(r'\[\]'))) +
            _ignore('WITHOUT TIME ZONE', 'WITH TIME ZONE', 'PRECISION', 'VARYING') +
            pp.Optional(pp.Suppress('(') + pp.Regex(r'\d+\s*,*\s*\d*') + _ignore('CHAR', 'BYTEST') + pp.Suppress(')')) +
            pp.Suppress(pp.Optional(pp.CaselessKeyword('DEFAULT') + 'false' | 'true')) +
            pp.Suppress(
                pp.Optional(
                    pp.Regex(
                        r"(?!--)(\b(COMMENT|DEFAULT)\b\s+[^,]+|([A-Za-z0-9_'\": -]|[^\x01-\x7E])*)",
                        re.IGNORECASE,
                    ),
                ),
            ) +
            pp.Suppress(pp.Optional(pp.Word(r'\[\]'))) +
            pp.Optional(pp.CaselessKeyword('NOT NULL'))('not_null').setParseAction(bool),
        ),
    )('columns') +
    pp.Suppress(')')
)


class ParseError(Exception):
    def __init__(self, statement: str):
        self.statement = statement


def parse(schema: str) -> t.Tuple[t.List[Table], t.List[ForeignKey]]:
    tables: t.Dict[str, Table] = {}
    foreign_keys: t.List[ForeignKey] = []

    schema = '\n'.join(
        line for line in schema.split('\n')
        if not line.startswith('--')
    )
    statements: t.List[str] = sqlparse.split(schema)

    for statement in statements:
        _stmt_upper = statement.upper()
        if not _stmt_upper.startswith('CREATE TABLE'):
            continue

        try:
            res: pp.ParseResults = create_table_expr.parseString(statement)
        except pp.ParseException:
            raise ParseError(statement)
        table = Table(
            name=res['table_name'],
            columns={
                col.name: Column(**dict(col))
                for col in res['columns']
            },
        )
        tables[table.name] = table

    for statement in statements:
        _stmt_upper = statement.upper()
        if not _stmt_upper.startswith('ALTER TABLE'):
            continue

        if 'PRIMARY KEY' in _stmt_upper:
            try:
                res = primary_key_expr.parseString(statement)
            except pp.ParseException:
                raise ParseError(statement)
            column: Column = tables[res['table_name']].columns[res['column_name']]
            column.primary_key = True

        elif 'FOREIGN KEY' in _stmt_upper:
            try:
                res = foreign_key_expr.parseString(statement)
            except pp.ParseException:
                raise ParseError(statement)
            foreign_keys.append(
                ForeignKey(
                    table_name=res['table_name'],
                    column_name=res['column_name'],
                    foreign_table_name=res['foreign_table_name'],
                    foreign_column_name=res['foreign_column_name'],
                ),
            )

    return list(tables.values()), foreign_keys


def create_graph(
    tables: t.List[Table],
    foreign_keys: t.List[ForeignKey],
) -> graphviz.Digraph:
    graph = graphviz.Digraph(
        name='ERD',
        graph_attr={'randkir': 'LR', 'overlap': 'false'},
        node_attr={'shape': 'record', 'fontsize': '9', 'fontname': 'Verdana'},
    )

    for table in tables:
        label = (
            '<\n<table border="0" cellborder="1" cellspacing="0" cellpadding="4">' +
            f'<tr><td bgcolor="lightblue"><b>{table.name}</b></td></tr>' +
            '\n'.join(
                f'<tr>'
                f'<td port="{col.name}" align="left">'
                f'<b>{col.name}</b>: '
                f'{"<b>[PK]</b> " if col.primary_key else ""}'
                f'<i>{col.data_type} '
                f'{" NOT NULL" if col.not_null else ""}</i>'
                '</td>'
                '</tr>'
                for col in table.columns.values()
            ) +
            '</table>>'
        )
        graph.node(
            name=table.name,
            shape='none',
            label=label,
        )

    for fkey in foreign_keys:
        graph.edge(
            f'{fkey.table_name}:{fkey.column_name}',
            f'{fkey.foreign_table_name}:{fkey.foreign_column_name}',
        )

    return graph


def render(graph: graphviz.Digraph, format: str) -> bytes:
    with tempfile.TemporaryDirectory() as dirpath:
        graph.render('graph', format=format, directory=dirpath)
        data: bytes = (pathlib.Path(dirpath) / f'graph.{format}').read_bytes()
    return data

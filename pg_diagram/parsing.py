from dataclasses import dataclass

import sqlglot
from sqlglot import expressions as e


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
    columns: dict[str, Column]


@dataclass
class ParseResult:
    tables: list[Table]
    foreign_keys: list[ForeignKey]


def parse(schema: str, dialect: str = "postgres") -> ParseResult:
    tables = {}
    foreign_keys = []

    statements = sqlglot.parse(schema, dialect=dialect)
    for stmt in statements:
        match stmt:
            case e.Create(this=e.Schema(this=e.Table(name=table_name))):
                tables[table_name] = Table(
                    name=table_name,
                    columns={
                        c.name: Column(
                            name=c.name,
                            data_type=str(c.kind),
                            not_null=c.find(e.NotNullColumnConstraint) is not None,
                            primary_key=c.find(e.PrimaryKeyColumnConstraint)
                            is not None,
                        )
                        for c in stmt.find_all(e.ColumnDef)
                    },
                )

    for stmt in statements:
        match stmt:
            case e.Alter(this=e.Table(name=table_name), actions=[e.AddConstraint()]):
                if pk := stmt.find(e.PrimaryKey):
                    for column in pk.find_all(e.Column):
                        if col := tables[table_name].columns.get(column.name):
                            col.primary_key = True

                    continue

                if not (fk := stmt.find(e.ForeignKey)):
                    continue

                match fk.find(e.Reference):
                    case e.Reference(
                        this=e.Schema(
                            this=e.Table() as foreign_table,
                            expressions=[e.Identifier() as foreign_column],
                        )
                    ):
                        foreign_keys.append(
                            ForeignKey(
                                table_name=table_name,
                                column_name=fk.expressions[0].name,
                                foreign_table_name=foreign_table.name,
                                foreign_column_name=foreign_column.name,
                            )
                        )

    return ParseResult(
        tables=list(tables.values()),
        foreign_keys=foreign_keys,
    )

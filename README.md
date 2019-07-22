## pg_diagram

[![PyPI version](https://badge.fury.io/py/pg-diagram.svg)](https://badge.fury.io/py/pg-diagram)

A tool for creating [Entity-relationship diagrams](https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model) for PostgreSQL

### Installation

- install [Graphviz](https://graphviz.org)
-
    ```bash
    pip install pg-diagram
    ```
### Usage
```bash
pg_diagram --format svg -o diagram.svg schema.sql
```
```bash
# or feed output of pg_dump
pg_dump --schema-only mydb | pg_diagram -o mydb.png -
```

### Sample output
<p align="center">
  <img src="https://github.com/qweeze/pg_diagram/raw/master/diagram.png?raw=true" alt="diagram image"/>
</p>

import argparse

from . import graph, parsing


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Converts postgresql schema to ER diagram",
    )
    parser.add_argument("schema", type=argparse.FileType("r"))
    parser.add_argument("-f", "--format", choices=["png", "svg", "dot"], default="png")
    parser.add_argument("-o", "--output", type=argparse.FileType("wb"), default="-")
    args = parser.parse_args()

    g = graph.create_graph(parsing.parse(args.schema.read()))
    args.output.write(graph.render(g, fmt=args.format))


if __name__ == "__main__":
    main()

import sys
import ast


class MyVisitor(ast.NodeVisitor):
    def visit(self, node):
        print(f'Visitando nodo: {type(node).__name__}')
        self.generic_visit(node)


def parse_file(file_name: str):
    with open(file_name, "r", encoding="utf-8") as f:
        source = f.read()

    return ast.parse(source, filename=file_name)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python z3jc <archivo.py>")
        sys.exit(1)

    ast = parse_file(sys.argv[1])
    visitor = MyVisitor()
    visitor.visit(ast)


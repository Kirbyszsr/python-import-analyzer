import ast
import unparse


class DecoratorTransformer(ast.NodeTransformer):
    def visit_BinOp(self, node):
        # print(node.__dict__)
        node.op = ast.Mult
        # print(node.__dict__)
        return node

    def visit_FunctionDef(self, node):
        for element in node.decorator_list:
            print(element.id)



expr = """
@staticmethod
def add(arg1,arg2):
    if arg1 == 1:
        return arg1 + arg2
    else:
        return arg1
"""

expr_ast = ast.parse(expr)
# print(ast.dump(expr_ast))
transformer = DecoratorTransformer()

modified = transformer.visit(expr_ast)
from typing import Optional


def calculate_expression(expression: str) -> str:
    """Safely evaluate a simple arithmetic expression.

    Supports +, -, *, /, parentheses, and decimal numbers.
    Returns a string for easy inclusion in LLM messages.
    """
    import ast
    import operator as op

    operators = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.USub: op.neg,
        ast.UAdd: op.pos,
    }

    def eval_node(node: ast.AST) -> float:
        if isinstance(node, ast.Num):  # type: ignore[attr-defined]
            return float(node.n)  # type: ignore[attr-defined]
        if isinstance(node, ast.UnaryOp) and type(node.op) in (ast.USub, ast.UAdd):
            return operators[type(node.op)](eval_node(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow):
            return operators[type(node.op)](eval_node(node.left), eval_node(node.right))
        if isinstance(node, ast.Expression):
            return eval_node(node.body)
        raise ValueError("Unsupported expression")

    try:
        parsed = ast.parse(expression, mode="eval")
        result = eval_node(parsed)
        # Avoid trailing .0 for integers
        if result.is_integer():
            return str(int(result))
        return str(result)
    except Exception as exc:  # noqa: BLE001
        return f"Error evaluating expression: {exc}"



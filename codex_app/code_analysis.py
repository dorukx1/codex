import ast
from typing import List


def analyze_code(code: str) -> List[str]:
    """Simple analysis to look for inefficient patterns."""
    suggestions = []
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            if isinstance(node.iter, ast.Call) and getattr(node.iter.func, 'id', '') == 'range':
                suggestions.append('Consider using list comprehensions or built-in sum() functions where appropriate.')
    if not suggestions:
        suggestions.append('No obvious issues detected.')
    return suggestions

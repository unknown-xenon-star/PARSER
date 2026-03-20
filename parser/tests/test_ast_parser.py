import unittest

from python_parser import parse_source


class ParseSourceTests(unittest.TestCase):
    def test_parse_module_structure(self) -> None:
        source = '''
"""Example module."""

import os
from pkg import thing as alias

VALUE = 3

@decorator
def func(a: int, b=2, *, flag=True) -> str:
    """Function doc."""
    local = a + b
    return str(local)

class Example(Base):
    """Class doc."""
    enabled = True

    def method(self, name: str) -> None:
        message = f"hi {name}"
'''.strip()

        parsed = parse_source(source, filename="example.py")

        self.assertEqual(parsed["module_docstring"], "Example module.")
        self.assertEqual(len(parsed["imports"]), 2)
        self.assertEqual(parsed["assignments"][0]["targets"], ["VALUE"])

        function = parsed["functions"][0]
        self.assertEqual(function["name"], "func")
        self.assertEqual(function["decorators"], ["decorator"])
        self.assertEqual(function["arguments"], ["a: int", "b = 2", "*", "flag = True"])
        self.assertEqual(function["returns"], "str")
        self.assertEqual(function["assignments"][0]["targets"], ["local"])

        klass = parsed["classes"][0]
        self.assertEqual(klass["name"], "Example")
        self.assertEqual(klass["bases"], ["Base"])
        self.assertEqual(klass["attributes"][0]["targets"], ["enabled"])
        self.assertEqual(klass["methods"][0]["name"], "method")

    def test_parse_async_function(self) -> None:
        parsed = parse_source(
            """
async def run(task, /, *, retries=3, **kwargs):
    result = await task()
""".strip()
        )

        function = parsed["functions"][0]
        self.assertEqual(function["kind"], "async_function")
        self.assertEqual(function["arguments"], ["task", "*", "retries = 3", "**kwargs"])
        self.assertEqual(function["assignments"][0]["targets"], ["result"])


if __name__ == "__main__":
    unittest.main()

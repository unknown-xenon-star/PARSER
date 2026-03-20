from __future__ import annotations

import ast
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


def _segment_to_str(node: ast.AST | None) -> str | None:
    if node is None:
        return None
    return ast.unparse(node)


def _name_from_target(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return ast.unparse(node)
    if isinstance(node, (ast.Tuple, ast.List)):
        parts = [_name_from_target(item) for item in node.elts]
        filtered = [part for part in parts if part]
        return ", ".join(filtered) if filtered else None
    return None


def _decorators(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> list[str]:
    return [ast.unparse(decorator) for decorator in node.decorator_list]


def _arguments(args: ast.arguments) -> list[str]:
    values: list[str] = []

    positional = list(args.posonlyargs) + list(args.args)
    default_offset = len(positional) - len(args.defaults)
    for index, arg in enumerate(positional):
        value = arg.arg
        annotation = _segment_to_str(arg.annotation)
        if annotation:
            value = f"{value}: {annotation}"
        if index >= default_offset:
            default = args.defaults[index - default_offset]
            value = f"{value} = {ast.unparse(default)}"
        values.append(value)

    if args.vararg:
        vararg = f"*{args.vararg.arg}"
        annotation = _segment_to_str(args.vararg.annotation)
        if annotation:
            vararg = f"{vararg}: {annotation}"
        values.append(vararg)
    elif args.kwonlyargs:
        values.append("*")

    for index, arg in enumerate(args.kwonlyargs):
        value = arg.arg
        annotation = _segment_to_str(arg.annotation)
        if annotation:
            value = f"{value}: {annotation}"
        default = args.kw_defaults[index]
        if default is not None:
            value = f"{value} = {ast.unparse(default)}"
        values.append(value)

    if args.kwarg:
        kwarg = f"**{args.kwarg.arg}"
        annotation = _segment_to_str(args.kwarg.annotation)
        if annotation:
            kwarg = f"{kwarg}: {annotation}"
        values.append(kwarg)

    return values


@dataclass
class AssignmentInfo:
    targets: list[str] = field(default_factory=list)
    value: str | None = None
    lineno: int | None = None


@dataclass
class FunctionInfo:
    name: str
    kind: str
    lineno: int | None = None
    end_lineno: int | None = None
    docstring: str | None = None
    decorators: list[str] = field(default_factory=list)
    arguments: list[str] = field(default_factory=list)
    returns: str | None = None
    assignments: list[AssignmentInfo] = field(default_factory=list)


@dataclass
class ClassInfo:
    name: str
    lineno: int | None = None
    end_lineno: int | None = None
    docstring: str | None = None
    decorators: list[str] = field(default_factory=list)
    bases: list[str] = field(default_factory=list)
    methods: list[FunctionInfo] = field(default_factory=list)
    attributes: list[AssignmentInfo] = field(default_factory=list)


@dataclass
class ModuleInfo:
    module_docstring: str | None = None
    imports: list[dict[str, Any]] = field(default_factory=list)
    assignments: list[AssignmentInfo] = field(default_factory=list)
    functions: list[FunctionInfo] = field(default_factory=list)
    classes: list[ClassInfo] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ModuleParser:
    def parse(self, source: str, filename: str = "<unknown>") -> ModuleInfo:
        tree = ast.parse(source, filename=filename)
        module = ModuleInfo(module_docstring=ast.get_docstring(tree))

        for node in tree.body:
            if isinstance(node, ast.Import):
                module.imports.append(
                    {
                        "kind": "import",
                        "names": [
                            {"name": alias.name, "asname": alias.asname}
                            for alias in node.names
                        ],
                        "lineno": getattr(node, "lineno", None),
                    }
                )
            elif isinstance(node, ast.ImportFrom):
                module.imports.append(
                    {
                        "kind": "from",
                        "module": node.module,
                        "level": node.level,
                        "names": [
                            {"name": alias.name, "asname": alias.asname}
                            for alias in node.names
                        ],
                        "lineno": getattr(node, "lineno", None),
                    }
                )
            elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                module.assignments.extend(self._parse_assignment(node))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                module.functions.append(self._parse_function(node))
            elif isinstance(node, ast.ClassDef):
                module.classes.append(self._parse_class(node))

        return module

    def _parse_class(self, node: ast.ClassDef) -> ClassInfo:
        info = ClassInfo(
            name=node.name,
            lineno=getattr(node, "lineno", None),
            end_lineno=getattr(node, "end_lineno", None),
            docstring=ast.get_docstring(node),
            decorators=_decorators(node),
            bases=[ast.unparse(base) for base in node.bases],
        )

        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                info.methods.append(self._parse_function(item))
            elif isinstance(item, (ast.Assign, ast.AnnAssign)):
                info.attributes.extend(self._parse_assignment(item))

        return info

    def _parse_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> FunctionInfo:
        info = FunctionInfo(
            name=node.name,
            kind="async_function" if isinstance(node, ast.AsyncFunctionDef) else "function",
            lineno=getattr(node, "lineno", None),
            end_lineno=getattr(node, "end_lineno", None),
            docstring=ast.get_docstring(node),
            decorators=_decorators(node),
            arguments=_arguments(node.args),
            returns=_segment_to_str(node.returns),
        )

        for item in node.body:
            if isinstance(item, (ast.Assign, ast.AnnAssign)):
                info.assignments.extend(self._parse_assignment(item))

        return info

    def _parse_assignment(self, node: ast.Assign | ast.AnnAssign) -> list[AssignmentInfo]:
        if isinstance(node, ast.Assign):
            targets = [_name_from_target(target) for target in node.targets]
            return [
                AssignmentInfo(
                    targets=[target for target in targets if target],
                    value=_segment_to_str(node.value),
                    lineno=getattr(node, "lineno", None),
                )
            ]

        target = _name_from_target(node.target)
        value = _segment_to_str(node.value) if node.value else None
        if node.annotation:
            annotated = f"{target}: {ast.unparse(node.annotation)}" if target else ast.unparse(node.annotation)
            if value:
                value = f"{annotated} = {value}"
            else:
                value = annotated

        return [
            AssignmentInfo(
                targets=[target] if target else [],
                value=value,
                lineno=getattr(node, "lineno", None),
            )
        ]


def parse_source(source: str, filename: str = "<unknown>") -> dict[str, Any]:
    return ModuleParser().parse(source, filename=filename).to_dict()


def parse_file(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    return parse_source(path.read_text(encoding="utf-8"), filename=str(path))

import ast
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class SymbolInfo:
    name: str
    full_name: str
    symbol_type: str

    line_start: Optional[int] = None
    line_end: Optional[int] = None

    parent_symbol: Optional[str] = None

    args: List[str] = field(default_factory=list)
    return_type: Optional[str] = None

    decorators: List[str] = field(default_factory=list)
    bases: List[str] = field(default_factory=list)

    docstring: Optional[str] = None

    is_async: bool = False

    calls: List[str] = field(default_factory=list)

    code: Optional[str] = None


@dataclass
class FileMetadata:
    imports: List[str]
    full_imports: List[str]
    symbols: List[SymbolInfo]


class MetadataVisitor(ast.NodeVisitor):
    def __init__(self, source_lines: List[str]):
        self.imports = set()
        self.full_imports = set()

        self.symbols: List[SymbolInfo] = []

        self.current_class: Optional[str] = None
        self.class_stack: List[str] = []

        self.function_depth = 0

        self.source_lines = source_lines

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.full_imports.add(alias.name)

            root_module = alias.name.split(".")[0]
            if root_module:
                self.imports.add(root_module)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if not node.module:
            return

        root_module = node.module.split(".")[0]
        self.imports.add(root_module)

        for alias in node.names:
            self.full_imports.add(
                f"{node.module}.{alias.name}"
            )

    def visit_ClassDef(self, node: ast.ClassDef):
        full_name = ".".join(self.class_stack + [node.name])

        symbol = SymbolInfo(
            name=node.name,
            full_name=full_name,
            symbol_type="class",
            line_start=node.lineno,
            line_end=getattr(node, "end_lineno", node.lineno),
            parent_symbol=self.current_class,
            docstring=ast.get_docstring(node),
            bases=[
                base_name
                for base in node.bases
                if (base_name := self._safe_unparse(base))
            ],
            code=self._extract_code(node),
        )

        self.symbols.append(symbol)

        self.class_stack.append(node.name)

        previous_class = self.current_class
        self.current_class = node.name

        for child in node.body:
            self.visit(child)

        self.class_stack.pop()
        self.current_class = previous_class

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._handle_function(node, is_async=False)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._handle_function(node, is_async=True)

    def _handle_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        is_async: bool,
    ):
        is_nested = self.function_depth > 0
        is_method = self.current_class is not None

        if is_nested:
            symbol_type = "nested_function"
        elif is_method:
            symbol_type = "method"
        else:
            symbol_type = "function"

        full_name = self._build_full_name(node.name)

        symbol = SymbolInfo(
            name=node.name,
            full_name=full_name,
            symbol_type=symbol_type,
            line_start=node.lineno,
            line_end=getattr(node, "end_lineno", node.lineno),
            parent_symbol=self.current_class,
            args=[arg.arg for arg in node.args.args],
            return_type=self._safe_unparse(node.returns),
            decorators=[
                decorator
                for dec in node.decorator_list
                if (decorator := self._safe_unparse(dec))
            ],
            docstring=ast.get_docstring(node),
            is_async=is_async,
            calls=self._get_function_calls(node),
            code=self._extract_code(node),
        )

        self.symbols.append(symbol)

        self.function_depth += 1

        for child in ast.iter_child_nodes(node):
            self.visit(child)

        self.function_depth -= 1

    def _build_full_name(self, name: str) -> str:
        if self.class_stack:
            return ".".join(self.class_stack + [name])

        return name

    def _safe_unparse(self, node) -> Optional[str]:
        try:
            return ast.unparse(node)
        except Exception:
            return None

    def _resolve_name(self, node) -> Optional[str]:
        if isinstance(node, ast.Name):
            return node.id

        if isinstance(node, ast.Attribute):
            parent = self._resolve_name(node.value)

            if parent:
                return f"{parent}.{node.attr}"

            return node.attr

        return None

    def _extract_code(self, node) -> str:
        try:
            return "\n".join(
                self.source_lines[
                    node.lineno - 1 : node.end_lineno
                ]
            )
        except Exception:
            return ""

    def _get_function_calls(self, node) -> List[str]:
        calls = set()

        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                call_name = self._resolve_name(child.func)

                if call_name:
                    calls.add(call_name)

        return sorted(calls)


def extract_metadata(source_code: str) -> FileMetadata:
    try:
        tree = ast.parse(source_code)
    except (SyntaxError, ValueError):
        return FileMetadata(
            imports=[],
            full_imports=[],
            symbols=[],
        )

    source_lines = source_code.splitlines()

    visitor = MetadataVisitor(source_lines)
    visitor.visit(tree)

    return FileMetadata(
        imports=sorted(visitor.imports),
        full_imports=sorted(visitor.full_imports),
        symbols=sorted(
            visitor.symbols,
            key=lambda s: s.line_start or 0,
        ),
    )


def extract_metadata_from_file(
    file_path: str,
) -> FileMetadata:
    try:
        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as f:
            source_code = f.read()

        return extract_metadata(source_code)

    except OSError:
        return FileMetadata(
            imports=[],
            full_imports=[],
            symbols=[],
        )

if __name__=="__main__":
    print(extract_metadata_from_file("nodes.py"))

# -*- coding: utf-8 -*-

"""
Generate the m.py module that provides lazy-loading access to all Request/Response classes.

Usage::

    .venv/bin/python scripts/gen_m.py
"""

import typing as T
from pathlib import Path
from sanhe_confluence_sdk.paths import path_enum

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
dir_methods = path_enum.dir_package / "methods"
path_m_py = dir_methods / "m.py"

# Directories to skip (common contains shared utilities, not Request/Response pairs)
SKIP_DIRS = {"common", "__pycache__"}


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------
def snake_to_pascal(name: str) -> str:
    """
    Convert snake_case to PascalCase.

    Example: get_spaces -> GetSpaces
    """
    return "".join(word.capitalize() for word in name.split("_"))


def discover_methods() -> T.List[T.Dict[str, str]]:
    """
    Discover all Request/Response classes in the methods directory.

    Returns a list of dicts with keys:
    - subdir: subdirectory name (e.g., "space", "page", "label")
    - module: module name without .py (e.g., "get_spaces")
    - class_prefix: PascalCase prefix (e.g., "GetSpaces")
    - request_class: full class name (e.g., "GetSpacesRequest")
    - response_class: full class name (e.g., "GetSpacesResponse")
    - import_path: relative import path (e.g., ".space.get_spaces")
    """
    methods = []

    for subdir in sorted(dir_methods.iterdir()):
        if not subdir.is_dir():
            continue
        if subdir.name in SKIP_DIRS:
            continue

        for py_file in sorted(subdir.glob("*.py")):
            if py_file.name.startswith("_"):
                continue  # Skip __init__.py and other private files

            module_name = py_file.stem  # e.g., "get_spaces"
            class_prefix = snake_to_pascal(module_name)  # e.g., "GetSpaces"

            methods.append(
                {
                    "subdir": subdir.name,
                    "module": module_name,
                    "class_prefix": class_prefix,
                    "request_class": f"{class_prefix}Request",
                    "response_class": f"{class_prefix}Response",
                    "import_path": f".{subdir.name}.{module_name}",
                }
            )

    return methods


def validate_classes(methods: T.List[T.Dict[str, str]]) -> None:
    """
    Validate that all discovered Request/Response classes actually exist.

    Raises ValueError if any class is missing.
    """
    import importlib

    errors = []

    for method in methods:
        module_path = f"sanhe_confluence_sdk.methods.{method['subdir']}.{method['module']}"
        try:
            mod = importlib.import_module(module_path)
        except ImportError as e:
            errors.append(f"Cannot import module {module_path}: {e}")
            continue

        for class_name in [method["request_class"], method["response_class"]]:
            if not hasattr(mod, class_name):
                errors.append(f"Class {class_name} not found in {module_path}")

    if errors:
        raise ValueError("Validation errors:\n" + "\n".join(f"  - {e}" for e in errors))


# ------------------------------------------------------------------------------
# Code Generation
# ------------------------------------------------------------------------------
dir_scripts = Path(__file__).absolute().parent
path_template = dir_scripts / "m.py.jinja2"


def generate_m_py(methods: T.List[T.Dict[str, str]]) -> str:
    """
    Generate the m.py module content using Jinja2.
    """
    from jinja2 import Template

    template = Template(path_template.read_text())
    return template.render(methods=methods)


# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
def main():
    print("Discovering methods...")
    methods = discover_methods()
    print(f"Found {len(methods)} methods:")
    for method in methods:
        print(f"  - {method['subdir']}/{method['module']}: {method['request_class']}, {method['response_class']}")

    print("\nValidating classes...")
    validate_classes(methods)
    print("All classes validated successfully!")

    print(f"\nGenerating {path_m_py}...")
    content = generate_m_py(methods)
    path_m_py.write_text(content)
    print("Done!")


if __name__ == "__main__":
    main()

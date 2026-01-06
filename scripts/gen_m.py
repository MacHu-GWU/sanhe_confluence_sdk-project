# -*- coding: utf-8 -*-

"""
Generate the m.py module that provides lazy-loading access to all BaseModel subclasses.

Usage::

    .venv/bin/python scripts/gen_m.py
"""

import typing as T
import inspect
from pathlib import Path
from sanhe_confluence_sdk.paths import path_enum

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
dir_methods = path_enum.dir_package / "methods"
path_m_py = dir_methods / "m.py"

# Directories to skip (common contains shared utilities, not Request/Response pairs)
SKIP_DIRS = {"common", "__pycache__"}

# Base classes to exclude from the generated m.py (these are abstract base classes)
BASE_CLASSES = {
    "BaseModel",
    "BaseRequest",
    "BaseResponse",
    "PathParams",
    "QueryParams",
    "BodyParams",
}


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------
def discover_modules() -> T.List[T.Dict[str, T.Any]]:
    """
    Discover all modules and their BaseModel subclasses in the methods directory.

    Returns a list of dicts with keys:
    - subdir: subdirectory name (e.g., "space", "page", "label")
    - module: module name without .py (e.g., "get_spaces")
    - import_path: relative import path (e.g., ".space.get_spaces")
    - classes: list of class names that are BaseModel subclasses (sorted alphabetically)

    Modules are sorted by their path (subdir/module) in natural order.
    Classes within each module are sorted alphabetically.
    """
    import importlib
    from sanhe_confluence_sdk.methods.model import BaseModel

    modules = []

    # Sort subdirs by name for external ordering
    for subdir in sorted(dir_methods.iterdir()):
        if not subdir.is_dir():
            continue
        if subdir.name in SKIP_DIRS:
            continue

        # Sort py files by name for external ordering
        for py_file in sorted(subdir.glob("*.py")):
            if py_file.name.startswith("_"):
                continue  # Skip __init__.py and other private files

            module_name = py_file.stem  # e.g., "get_spaces"

            # Import the module to inspect its classes
            module_path = f"sanhe_confluence_sdk.methods.{subdir.name}.{module_name}"
            try:
                mod = importlib.import_module(module_path)
            except ImportError as e:
                print(f"Warning: Cannot import {module_path}: {e}")
                continue

            # Find all BaseModel subclasses defined in this module
            classes = []
            for name, obj in inspect.getmembers(mod, inspect.isclass):
                # Check if it's a subclass of BaseModel
                if not issubclass(obj, BaseModel):
                    continue
                # Skip base classes
                if name in BASE_CLASSES:
                    continue
                # Only include classes defined in this module (not imported)
                if obj.__module__ != module_path:
                    continue
                classes.append(name)

            # Sort classes alphabetically (internal ordering)
            classes.sort()

            if classes:
                modules.append(
                    {
                        "subdir": subdir.name,
                        "module": module_name,
                        "import_path": f".{subdir.name}.{module_name}",
                        "classes": classes,
                    }
                )

    return modules


# ------------------------------------------------------------------------------
# Code Generation
# ------------------------------------------------------------------------------
dir_scripts = Path(__file__).absolute().parent
path_template = dir_scripts / "m.py.jinja2"


def generate_m_py(modules: T.List[T.Dict[str, T.Any]]) -> str:
    """
    Generate the m.py module content using Jinja2.
    """
    from jinja2 import Template

    template = Template(path_template.read_text())
    return template.render(modules=modules)


# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
def main():
    print("Discovering modules and BaseModel subclasses...")
    modules = discover_modules()

    total_classes = sum(len(m["classes"]) for m in modules)
    print(f"Found {len(modules)} modules with {total_classes} classes:")

    for module in modules:
        print(f"  - {module['subdir']}/{module['module']}: {', '.join(module['classes'])}")

    print(f"\nGenerating {path_m_py}...")
    content = generate_m_py(modules)
    path_m_py.write_text(content)
    print("Done!")


if __name__ == "__main__":
    main()

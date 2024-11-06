# Copyright (c) 2012 Adam Karpierz
# SPDX-License-Identifier: Zlib

__all__ = ('import_file',)


def import_file(path, name=None):

    import sys
    from pathlib import Path
    import importlib.util

    path = Path(path)

    if not path.exists():
        raise ImportError("No module named {}".format(path.stem))

    if name is None:  name = path.stem
    if path.is_dir(): path = path/"__init__.py"
    spec = importlib.util.spec_from_file_location(name, str(path))

    if spec is None:
        raise ImportError("Cannot import module named {}".format(name))

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    return module

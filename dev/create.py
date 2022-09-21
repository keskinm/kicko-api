import importlib
import os

tables = []
search_dirs = ['tables']
while search_dirs:
    search_dir = search_dirs.pop()
    basenames = os.listdir(search_dir)
    paths = [os.path.join(search_dir, basename) for basename in basenames if '__pycache__' not in basename]
    for path in paths:
        if os.path.isdir(path):
            search_dirs.append(path)
        elif os.path.isfile(path):
            path = path.replace('/', '.').strip('.py')
            tables.append(path)
        else:
            raise ValueError(f"unknown path {path}")

for table in tables:
    table_module = importlib.import_module(table)
    create = getattr(table_module, "create")
    create()

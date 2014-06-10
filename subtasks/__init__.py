"""
Load all subtask modules in this folder.
"""

import os
import glob
import inspect
import importlib

PACKAGE = __package__
namespace = globals()

for f in glob.glob(os.path.dirname(__file__)+"/*.py"):
    name = os.path.basename(f)[:-3]
    if name != '__init__':
        module = importlib.import_module("%s.%s" % (PACKAGE, name))
        for (k, v) in inspect.getmembers(module):
            if k.isupper():
                if isinstance(v, str):
                    namespace[k] = v.format(**globals())
                else:
                    namespace[k] = v

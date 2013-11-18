
import inspect
import glob
import os
import sys
import imp
from collections import defaultdict


class ClassyPlugins(object):

    def __init__(self):
        # This is the main lookup dictionary.  The keys are the base classes and
        # each value is a list of the implementing sub classes.
        self._found = defaultdict(list)

    def _get_module(self, filename):
        """ Based on the filename provided, it loads the module and returns the
        module object.  It does not currently load the module into globals
        """
        dirs = [os.path.dirname(filename)]
        name = os.path.basename(filename).strip(".py")
        # File the python module at the directory/name we specified.
        _file, path, des = imp.find_module(name, dirs)
        mod = None
        try:
            mod = imp.load_module("foo", _file, path, des)
        finally:
            # Always close the open file handle from imp.find_module()
            if _file:
                _file.close()
        return mod

    def _inspect_module(self, mod):
        """ Given a module object, it looks through all the classes in that
        module.
        """
        for name, obj in inspect.getmembers(mod):
            if not name.startswith("_"):
                if inspect.isclass(obj):
                    parents = inspect.getmro(obj)
                    for i in range(1, len(parents)):
                        self._found[parents[i]].append(obj)

    def find(self, pattern):
        """ Finds python files matching the pattern specified.  The pattern can
        be for a single python file, multiple python files (use wildcard in
        pattern), or a directory.  All matched python files are loaded and its
        classes inspected.
        """
        if pattern.endswith(".py"):
            files = glob.glob(pattern)
        elif pattern.endswith("*"):
            files = glob.glob(pattern + ".py")
        elif pattern.endswith(os.sep):
            files = glob.glob(pattern + "*.py")
        else:
            files = glob.glob(pattern + os.sep + "*.py")
        for filename in files:
            mod = self._get_module(filename)
            self._inspect_module(mod)

    def use(self, baseclass):
        if baseclass in self._found:
            return self._found[baseclass]
        return []

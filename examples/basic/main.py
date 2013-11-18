
from classyplugins import ClassyPlugins
import interfaces

if __name__ == '__main__':
    clp = ClassyPlugins()
    clp.find("plugins/plugin.py")
    classes = clp.use(interfaces.PluginBase)
    for cls in classes:
        inst = cls()
        inst.print_message("Hello World")

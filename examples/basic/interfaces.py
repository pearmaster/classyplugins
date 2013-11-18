import abc

class PluginBaseClass(object):
    
    @abc.abstractmethod
    def print_message(self, msg):
        return

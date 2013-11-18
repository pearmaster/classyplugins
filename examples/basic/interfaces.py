import abc

class PluginBase(object):
    
    @abc.abstractmethod
    def print_message(self, msg):
        return

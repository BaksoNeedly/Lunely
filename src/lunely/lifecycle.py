from collections.abc import Callable

Handler = Callable[[], any]

class Lifecycle:
    
    def __init__(self):
        self._startup_hooks: list[Handler] = []
        self._shutdown_hooks: list[Handler] = []
        
    def add_shutdown_hook(self, function: Handler) -> Handler:
        self._shutdown_hooks.append(function)
        return function
    
    def run_shutdown(self):
        for function in reversed(self._shutdown_hooks):
            function()
            
    def add_startup_hook(self, function: Handler) -> Handler:
        self._startup_hooks.append(function)
        return function
    
    def run_startup(self):
        for function in reversed(self._startup_hooks):
            function()
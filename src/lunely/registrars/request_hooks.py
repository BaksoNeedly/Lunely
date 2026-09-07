from lunely.hooks.request_hooks import Handler

class RequestHooksRegistrar():
    
    def __init__(self) -> None:
        self._hooks: list[Handler] = []
        
    def register(self) -> None:
        pass
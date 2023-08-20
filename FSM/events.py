class Event:
    def __init__(self):
        self.handlers = []

    def __call__(self):
        def wrapper(handler):
            self.handlers.append(handler)
        return wrapper

    def execute(self, **kwargs):
        for handler in self.handlers:
            handler(**kwargs)


class DepthUpdateEvent(Event):
    def __init__(self):
        super().__init__()


class AnalysisUpdateEvent(Event):
    def __init__(self):
        super().__init__()


class SaveDataEvent(Event):
    def __init__(self):
        super().__init__()

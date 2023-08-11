class DepthUpdateEvent:
    def __init__(self):
        self.handlers = []

    def __call__(self):
        def wrapper(handler):
            self.handlers.append(handler)
        return wrapper

    def execute(self, **kwargs):
        for handler in self.handlers:
            handler(**kwargs)


class Router:
    def __init__(self):
        self.depth_update = DepthUpdateEvent()

    def __call__(self, **kwargs):
        print(kwargs.keys())
        self.depth_update.execute(**kwargs)


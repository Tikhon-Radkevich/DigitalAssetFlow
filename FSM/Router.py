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


class AnalysisUpdateEvent:
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
        self.analysis_update = AnalysisUpdateEvent()

    def __call__(self, **kwargs):
        depth = kwargs["depth"]
        analysis = kwargs["analysis"]
        self.depth_update.execute(depth=depth)
        self.analysis_update.execute(analysis=analysis)


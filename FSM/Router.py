from events import DepthUpdateEvent, AnalysisUpdateEvent, SaveDataEvent


class Router:
    def __init__(self):
        self.depth_update = DepthUpdateEvent()
        self.analysis_update = AnalysisUpdateEvent()
        self.save_data = SaveDataEvent()

    def __call__(self, **kwargs):
        storage = kwargs["storage"]
        depth = kwargs["depth"]
        analysis = kwargs["analysis"]
        self.depth_update.execute(depth=depth, storage=storage)
        self.analysis_update.execute(analysis=analysis, storage=storage)
        self.save_data.execute(storage=storage)


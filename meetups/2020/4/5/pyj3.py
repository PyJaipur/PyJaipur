class Actor:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    def run_in_background(self, *args, **kwargs):
        # api call to run in background?
        # Insert job into a job queue?
        pass


def baad_mein(function):
    return Actor(function)


@baad_mein
def run_my_big_ml_model(*inputs, model_revision=0):
    pass

from rx import from_iterable

obs = from_iterable(range(4))
obs.subscribe(print)

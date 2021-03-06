import rx
from rx import operators as ops

source = rx.of("Alpha", "Beta", "Gamma", "Delta", "Epsilon")

composed = source.pipe(ops.map(lambda s: len(s)), ops.filter(lambda i: i >= 5))

composed.subscribe(lambda value: print(f"Received {value}"))

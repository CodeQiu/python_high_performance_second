from rx import from_iterable

obs = from_iterable(range(4))
obs.subscribe(on_next=lambda x: print(f"Next item: {x}"), on_completed=lambda: print("No more data"))

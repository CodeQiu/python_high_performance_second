def parrot():
    while True:
        message = yield
        print(f"Parrot says: {message}")


generator = parrot()
generator.send(None)
generator.send("Hello")
generator.send("World")

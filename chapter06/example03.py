import threading


def fetch_square(number: float):
    def on_done(response):
        if response["success"]:
            print(f'{number} ** 2 is {response["result"]}')

    network_request_async(number, on_done)


def network_request_async(number: float, on_done):
    def timer_done():
        on_done({"success": True, "result": number ** 2})

    timer = threading.Timer(1, timer_done)
    timer.start()


fetch_square(2.1)
fetch_square(3)
fetch_square(4)

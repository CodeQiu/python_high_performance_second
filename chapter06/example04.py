from concurrent.futures import Future
import threading


def network_request_async(number: float):
    future = Future()
    result = {"success": True, "result": number ** 2}
    timer = threading.Timer(1, lambda: future.set_result(result))
    timer.start()
    return future


def fetch_square(number: float):
    fut = network_request_async(number)

    def on_done_future(future):
        response = future.result()
        if response["success"]:
            print(f'{number} ** 2 is {response["result"]}')

    fut.add_done_callback(on_done_future)


fetch_square(2)
fetch_square(3)
fetch_square(4)

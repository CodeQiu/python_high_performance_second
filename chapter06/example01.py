import time


def network_request(number: float):
    time.sleep(1)
    return {"success": True, "result": number ** 2}


def fetch_square(number: float):
    response = network_request(number)
    if response["success"]:
        print(f'Result is: {response["result"]}')


fetch_square(2)
fetch_square(3)
fetch_square(4)

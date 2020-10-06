import asyncio

loop = asyncio.get_event_loop()


async def network_request(number: float):
    await asyncio.sleep(1)
    return {"success": True, "result": number ** 2}


async def fetch_square(number: float):
    response = await network_request(number)
    if response["success"]:
        print(f'{number} ** 2 is {response["result"]}')


# loop.run_until_complete(fetch_square(2))
# loop.run_until_complete(fetch_square(3))
# loop.run_until_complete(fetch_square(4))

asyncio.ensure_future(fetch_square(2))
asyncio.ensure_future(fetch_square(3))
asyncio.ensure_future(fetch_square(4))
loop.run_forever()
# 要停止循环，可按Ctrl-C

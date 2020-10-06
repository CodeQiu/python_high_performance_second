import asyncio

loop = asyncio.get_event_loop()


async def wait_and_print(msg: str):
    await asyncio.sleep(2)
    print(f"Message: {msg}")


loop.run_until_complete(wait_and_print("Hello"))

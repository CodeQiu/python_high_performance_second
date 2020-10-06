import time
from concurrent.futures import ThreadPoolExecutor
import asyncio

loop = asyncio.get_event_loop()
executor = ThreadPoolExecutor(max_workers=3)


def wait_and_return(msg: str) -> str:
    time.sleep(1)
    return msg


fut = loop.run_in_executor(executor, wait_and_return, "Hello, asyncio executor")
print(loop.run_until_complete(fut))

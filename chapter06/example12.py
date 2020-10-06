import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor

loop = asyncio.get_event_loop()

executor = ThreadPoolExecutor(max_workers=2)


# async def fetch_urls(urls):
#     response = []
#     for url in urls:
#         response.append(await loop.run_in_executor(executor, requests.get, url))
#     return response


def fetch_urls(urls):
    return asyncio.gather(*[loop.run_in_executor(executor, requests.get, url) for url in urls])


url_list = ["https://www.baidu.com", "https://www.tencent.com", "https://www.alibaba.com", "https://www.jd.com",
            "https://www.pinduoduo.com", "https://www.vip.com"]
for resp in loop.run_until_complete(fetch_urls(url_list)):
    print(f"{resp.url}'s status code is {resp.status_code}")

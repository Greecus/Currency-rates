import platform
import aiohttp
import asyncio
import sys
import datetime
from concurrent.futures import ThreadPoolExecutor


async def get_currency_rates(currency:str,start_date:str):
    adress=f'http://api.nbp.pl/api/exchangerates/rates/c/{currency}/{start_date}/today/?format=json'
    async with aiohttp.ClientSession(adress) as session:
        async with session.get() as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            print('Cookies: ', response.cookies)
            print(response.ok)
            result = await response.json()
            return result
        
async def main():
    number_of_days=int(sys.argv[1])
    start_date=datetime.date.today()-datetime.timedelta(days=number_of_days)

    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor(2) as pool:
        futures = [loop.run_in_executor(pool, get_currency_rates, currency,start_date.strftime("%Y-%m-%d")) for currency in ['EUR','USD']]
        result = await asyncio.gather(*futures, return_exceptions=True)
        return result

        

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)

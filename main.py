import platform
import aiohttp
import asyncio
import sys
import datetime
import json

CURRENCIES = ['eur','usd']
async def get_currency_rates(currency:str,start_date:str,end_date:str):
    adress=f'http://api.nbp.pl/api/exchangerates/rates/c/{currency}/{start_date}/{end_date}/?format=json'
    async with aiohttp.ClientSession() as session:
        async with session.get(adress) as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            print('Cookies: ', response.cookies)
            print(response.ok)
            result = await response.json()
            return result
        
async def main():
    try:
        number_of_days = int(sys.argv[1])
    except IndexError:
        number_of_days = int(input("How many days back:"))
    if number_of_days>10:
        print("Limit is 10 days")
        number_of_days = 10
    start_date=datetime.date.today()-datetime.timedelta(days = number_of_days)
    end_date=datetime.date.today()-datetime.timedelta(days = 1)
    start_date_str=start_date.strftime("%Y-%m-%d")
    end_date_str=end_date.strftime("%Y-%m-%d")

    result = await asyncio.gather(*[get_currency_rates(currency,start_date_str,end_date_str) for currency in CURRENCIES], return_exceptions=True)
    result_dict={}
    for date in (start_date + datetime.timedelta(days=n) for n in range(number_of_days)):
        result_dict.update({date.strftime("%Y-%m-%d"):{currency.upper():{} for currency in CURRENCIES}})
    for currency in result:
        for daily_rates in currency['rates']:
            result_dict[daily_rates['effectiveDate']][currency['code']] = {'sale':daily_rates['ask'],'purchase':daily_rates['bid']}
    return result_dict

        

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)

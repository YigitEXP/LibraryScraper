## Python kütüphanelerini ne işe yaradığıyla birlikte çekip dictionary şeklinde kaydedecek bir yapı yazıyoruz 

import asyncio
import aiohttp
import json
from tqdm import tqdm ## ilerleme durum çubuğu

limit = 0
while True:
    try:
        limit = input("How many libraries would you like to pull? --> ")
        break
    except ValueError:
        print("Please enter a number")
        continue
        
async def fetch_summary(session,name):
    try:
        url = f"https://pypi.org/pypi/{name}/json"
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                data = await response.json()
                return name, data["info"]["summary"] or "No Summary"
            data.close()
            return name, "Error: No Summary"
    
    except Exception as e:
        return name, "Error:  Failed To Fetch"

async def main():
    print("Pocket names fetching...")
    
    async with aiohttp.ClientSession() as session:
        async with session.get("https://pypi.org/simple/") as response:
            simple = response
            text = await simple.text()
    
    package_names = []
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(text, "html.parser")
    for link in soup.find_all('a'):
        name = link.text.strip()
        if name:
            package_names.append(name)
    
    summaries = {}
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_summary(session,name) for name in package_names[:int(limit)]]
        for f in tqdm(asyncio.as_completed(tasks),total=len(tasks)):
            name, summary = await f
            summaries[name] = summary

    with open("fast_pypi_summary.json","w",encoding="utf-8") as f:
        json.dump(summaries,f,indent=2)
    
    print("Process finished")
    
if __name__ == "__main__":
    asyncio.run(main())
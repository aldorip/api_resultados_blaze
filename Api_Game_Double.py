import aiohttp
import asyncio
from datetime import datetime

class ApiDouble:
    def __init__(self, base_url, proxies=None):
        self.base_url = base_url.rstrip("/")
        self.proxies = proxies
        self.session = None

    async def start_session(self):
        if self.session is None or self.session.closed:
            connector = aiohttp.TCPConnector(ssl=False)
            self.session = aiohttp.ClientSession(connector=connector)

    async def fetch(self, endpoint):
        await self.start_session()
        url = f"{self.base_url}/{endpoint}"
        async with self.session.get(url, proxy=self.proxies) as response:
            if response.status == 200:
                return await response.json()
            return None

    async def close(self):
        if self.session:
            await self.session.close()

    async def get_current(self):
        await self.start_session()
        endpoint = f"api/singleplayer-originals/originals/roulette_games/current/1"

        async with self.session.get(f"{self.base_url}/{endpoint}", proxy=self.proxies) as response:
            if response.status == 200:
                return await response.json()
            return None

    async def get_last_doubles(self):
        endpoint = "api/singleplayer-originals/originals/roulette_games/recent/1"
        data = await self.fetch(endpoint)
        if data:
            result = {
                "items": [
                    {
                        "color": "B" if i["color"] == 0 else "V" if i["color"] == 1 else "P",
                        "value": i["roll"],
                        "created_date": datetime.strptime(i["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
                    } for i in data
                ]
            }
            return result
        return False

# Exemplo de uso:
async def main():
    while True:
        game_double = ApiDouble("https://blaze.bet.br")
        try:
            current = await game_double.get_current()
            status = current.get("status")
            
            if status == "complete":

                last_doubles = await game_double.get_last_doubles()
                numbers = [item["value"] for item in last_doubles["items"]]
                print("Numeros:", *numbers[0:10])

                colors = [item["color"] for item in last_doubles["items"]]
                print("Cores:", *colors[0:10])

                await asyncio.sleep(3)

            else:
                print("status:", status)
                
            await asyncio.sleep(1)
        
        except Exception as e:
            print("Erro:", e)
            await game_double.close()
        finally:
            await game_double.close()    

asyncio.run(main())

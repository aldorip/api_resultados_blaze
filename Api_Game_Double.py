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

    async def get_last_doubles(self):
        endpoint = "api/singleplayer-originals/originals/roulette_games/recent/1"
        data = await self.fetch(endpoint)
        if data:
            result = {
                "items": [
                    {
                        "color": "branco" if i["color"] == 0 else "vermelho" if i["color"] == 1 else "preto",
                        "value": i["roll"],
                        "created_date": datetime.strptime(i["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
                    } for i in data
                ]
            }
            return result
        return False

# Exemplo de uso:
async def main():
    game_double = ApiDouble("https://blaze.bet.br")
    last_doubles = await game_double.get_last_doubles()
    print("Últimos Doubles:", last_doubles)
    await game_double.close()
    

asyncio.run(main())

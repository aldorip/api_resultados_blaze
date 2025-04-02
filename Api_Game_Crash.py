import aiohttp
import asyncio

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

    async def get_last_crashs(self):
        endpoint = "api/singleplayer-originals/originals/crash_games/recent/4"
        data = await self.fetch(endpoint)
        if data:
            result = {
                "items": [
                    {
                        "color": "preto" if float(i["crash_point"]) < 2 else "verde",
                        "point": i["crash_point"]
                    } for i in data
                ]
            }
            return result
        return False

# Exemplo de uso:
async def main():
       
    game_crash = ApiDouble("https://blaze.bet.br")
    last_crashs = await game_crash.get_last_crashs()
    print("Últimos Crashs:", last_crashs)
    await game_crash.close()

asyncio.run(main())

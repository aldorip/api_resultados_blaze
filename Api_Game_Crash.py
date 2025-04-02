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
    
    async def get_current(self):
        await self.start_session()
        endpoint = f"api/singleplayer-originals/originals/crash_games/current/1"

        async with self.session.get(f"{self.base_url}/{endpoint}", proxy=self.proxies) as response:
            if response.status == 200:
                return await response.json()
            return None

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
    while True:
        game_double = ApiDouble("https://blaze.bet.br")
        try:
            current = await game_double.get_current()
            status = current.get("status")
            
            if status == "complete":
                last_doubles = await game_double.get_last_crashs()
                numbers = [item["point"] for item in last_doubles["items"]]
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

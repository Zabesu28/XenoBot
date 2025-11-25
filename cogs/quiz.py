import aiohttp

async def fetch_quiz_data():
    url = 'https://opentdb.com/api.php?amount=10&category=15&difficulty=medium&type=multiple'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data['results']
            else:
                return None
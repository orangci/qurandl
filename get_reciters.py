import aiohttp
import asyncio
import re

BASE_URL = "https://www.quranicaudio.com/quran/"
DOWNLOAD_LINK_PATTERN = re.compile(r'href="https://download\.quranicaudio\.com/quran/([^/]+)/001\.mp3"')


async def fetch_reciter_id(session, page_id):
    url = f"{BASE_URL}{page_id}"
    try:
        async with session.get(url) as response:
            html = await response.text()
            match = DOWNLOAD_LINK_PATTERN.search(html)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Error on page {page_id}: {e}")
    return None


async def scrape_all_reciters():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_reciter_id(session, i) for i in range(1, 162)]
        results = await asyncio.gather(*tasks)

        # Filter out None and remove duplicates
        unique_ids = sorted(set(filter(None, results)))

        # Write to reciters.py
        with open("reciters.py", "w") as f:
            f.write("reciters = [\n")
            for reciter in unique_ids:
                f.write(f'    "{reciter}",\n')
            f.write("]\n")


if __name__ == "__main__":
    asyncio.run(scrape_all_reciters())

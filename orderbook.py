
import asyncio
from websockets import connect
import aiofiles
import sys
import json
import httpx
import time
from datetime import datetime



async def orderbook_download(pair):

    pair_lower = pair.lower()
    websocket_url = f"wss://stream.binance.com:9443/ws/{pair_lower}@depth"
    rest_url = f"https://api.binance.com/api/v3/depth"

    params = {
            "symbol":pair.upper(),
            "limit":5000,
            }
    today = datetime.now().date()

    async with httpx.AsyncClient() as client:
        snapshot = await client.get(rest_url, params=params)

    snapshot = snapshot.json()
    snapshot["time"] = time.time()

    async with aiofiles.open(f"{pair_lower}-snapshots-{today}.txt", mode = "a") as f:
        await f.write(json.dumps(snapshot) + "\n")

    async with connect(websocket_url) as websocket:

        while True:
            data = await websocket.recv()
            print(data)

            async with aiofiles.open(f"{pair_lower}-updates-{today}.txt", mode = "a") as f:
                await f.write(data + "\n")

    print("Hello")

    pass

asyncio.run(orderbook_download("UNIUSDT"))

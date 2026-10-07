import json
import asyncio 
from datetime import datetime, timedelta
from typing import Optional
from utility import Song, client, normalize_audius, AUDIUS_TOKEN

#remove the below line later 
from utility import store, load

REFRESH_DAYS = timedelta(days = 1)
suggestions = {}

async def trending():
    res = await client.get(
        "https://api.audius.co/v1/tracks/recommended?limit=40",
        headers={
          "Authorization": f"Bearer {AUDIUS_TOKEN}"
        }
    )  
    return res.json()['data']

async def resonating():
    
    res = await client.get(
        "https://api.audius.co/v1/tracks/most-shared?limit=40",
        headers={
          "Authorization": f"Bearer {AUDIUS_TOKEN}"
            }
        )
    return res.json()['data']


async def try_out():
    res = await client.get(
        "https://api.audius.co/v1/tracks/feeling-lucky?limit=20",
        headers={
          "Authorization": f"Bearer {AUDIUS_TOKEN}"
        }
    )
    res = res.json()['data']
    tasks = [normalize_audius(song) for song in res]

    res = asyncio.gather(*tasks)
    return res

async def get_songs():
    to = await try_out()
    nonlocal suggestions

    if not suggestions:
        tr = await trending()
        reson = await resonating()
        suggestions = {
            "last_updated": datetime.now(),
            "trending":     tr,
            "try_out":      to,
            "resonating":        reson,
        }

    elif suggestion['last_updated'] - datetime.now() >= REFRESH_DAYS:
        tr = await trending()
        reson = await resonating()
        suggestions = {
            "last_updated": datetime.now(),
            "trending":     tr,
            "try_out":      to,
            "resonating":        reson,
        }
    
    else :
        suggestions['try_out'] = to

    return suggestions

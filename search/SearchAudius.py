#remove the below line later 
from utility import store, load
##################################################

from utility import Song, client, normalize_audius, AUDIUS_TOKEN
from urllib.parse import urlencode
import asyncio 

async def search_audius(query: str, genre: list[str] = None, limit=10) -> list[Song]:    
    params = {
        "query": query,
        "limit": limit,
        "sort_method": "relevant"}
    params = urlencode({**params, "genre": genre} if genre is not None else params)

    url = f"https://api.audius.co/v1/tracks/search?" + params

    res = await client.get(
        url,
        headers={
          "Authorization": f"Bearer {AUDIUS_TOKEN}"
        }
    ) 
    tracks = res.json()['data']
    coroutine = [normalize_audius(track) for track in tracks]

    songs = asyncio.gather(*coroutine)
    return songs

def store(obj, name):
    import pickle
    with open(f"/workspaces/nightfall/variables/{name}.pkl", "wb") as f:
        pickle.dump(obj, f)

def load( varname):
    import pickle 
    with open(f"/workspaces/nightfall/variables/{varname}.pkl", "rb") as f:
        return pickle.load(f)

from dataclasses import dataclass, field
import httpx
import os
AUDIUS_TOKEN = os.getenv("AUDIUS_TOKEN") or "AUDIUS_SECRET_TOKEN"

client = httpx.AsyncClient()

@dataclass(slots=True)
class Song:

    id: str
    source_name: str
    source_id: str

    title: str
    artist: list[str]
    album: dict = dict
    album_artist: Optional[str] = None
    duration: Optional[int] = None
    genre: Optional[str] = None
    mood: Optional[str]= None
    tags: list[str] = field(default_factory=list)
    release_date: Optional[str] = None
    play_count: Optional[int] = None
    artwork_url: Optional[str] = None

    stream_url: Optional[str] = None 
    preview_url: Optional[str] = None
    download_url: Optional[str] = None
    is_downloadable: bool = False

    license_name: Optional[str] = None 
    is_streamable: bool = False
    is_available: bool = True

async def normalize_audius(track: dict):
    user = track.get('user') or {}
    stream = track.get("stream") or {}
    download = track.get("download") or {}
    artwork = track.get("artwork") or {}

    raw_tags = track.get("tags") or ""
    tags = [t.strip() for t in raw_tags.split(",") if t.strip()]

    is_downloadable = bool(track.get("is_downloadable"))
    handle = user.get("handle") or ""

    return Song(
        id = str(uuid.uuid4()),
        source_name = "Audius",
        source_id = track.get("id"),
        title = track.get("title"),
        
        artist = [a for a in \
                 [track.get("cover_original_artist"), *(track.get("collaborators") or [])] if a]  or \
                 [handle] or [], 
        album = track.get("album_backlink"),
        album_artist = handle or None,
        duration = track.get("duration"),
        genre = track.get("genre"),
        mood = track.get("mood"),
        tags = tags, 
        release_date = track.get("release_date"),
        play_count = track.get("play_count", 0), 
        artwork_url = artwork.get("150x150") or artwork.get("480x480"),
        stream_url = stream.get("url"),
        preview_url = track.get("preview"),
        download_url = download.get("url") if is_downloadable else None,
        is_downloadable = is_downloadable, 
        license_name = track.get("license") or "Audius (unspecified)",
        is_streamable = bool(track.get("is_streamable")),
        is_available=bool(track.get("is_available", True)),
    )
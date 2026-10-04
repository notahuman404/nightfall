from dataclasses import dataclass

@dataclass(slots=True)
class Song():

    id:str
    source_name: str
    source_id: str

    title: str 
    artist: list[str]
    album: str | None = None
    album_artist : str
    duration: Optional[int] = None
    genre: Optional[str] = None
    tags: list[str] = field(default_factory=list) 
    year: Optional[int] = None

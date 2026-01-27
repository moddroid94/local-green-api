from fastapi import FastAPI
from parquet_handler import Handler

app = FastAPI()
db = Handler()


@app.get("/")
async def root():
    data = db.get_db()
    return {"tables": data}


@app.get("/tracks")
async def get_tracks_by_id(ids: str, market: str = "all"):
    track = db.get_track_by_id(ids, market)
    return {"tracks": [track]}


@app.get("/albums/{ids}")
async def get_albums_by_id(ids: str, market: str = "all"):
    album = db.get_album_by_id(ids, market)
    return album


@app.get("/artists/{ids}")
async def get_artists_by_id(ids: str, market: str = "all"):
    artist = db.get_artist_by_id(ids, market)
    return artist

from fastapi import FastAPI
from parquet_handler import Handler
import re

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


@app.get("/search")
async def search_catalog(
    q: str,
    type: str,
    limit: int = 10,
    offset: int = 0,
    market: str = "all",
    inlcude_external: bool = True,
):
    query = q + " "  # adds end space to simplify regex to catch last section
    params = re.findall(
        r"^(([^:]+)+ )|(isrc:(\w+))|(track:((\w+ )+))|(artist:((\w+ )+))|(album:((\w+ )+))",
        query,
    )
    base_query = ""
    artist_filter = ""
    album_filter = ""
    isrc_filter = ""
    track_filter = ""

    # catched params as "track:track name " so we split at ":" and remove the trailing space where present.
    for p in params:
        if p[0] != "":  # text query
            base_query = p[0][:-1]
            continue
        if p[2] != "":  # isrc code
            isrc_filter = p[2].split(":")[1]
            continue
        if p[4] != "":  # track name
            track_filter = p[4].split(":")[1][:-1]
            continue
        if p[7] != "":  # artist name
            artist_filter = p[7].split(":")[1][:-1]
            continue
        if p[10] != "":  # album name
            album_filter = p[10].split(":")[1][:-1]
            continue
    result_list = db.search(
        base_query,
        track_filter,
        artist_filter,
        album_filter,
        isrc_filter,
        type,
        limit,
        offset,
    )

    return result_list

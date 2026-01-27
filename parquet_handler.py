import duckdb
import os
import numpy

file_paths = [
    "spotify_clean_parquet/tracks.parquet",
    "spotify_clean_parquet/track_artists.parquet",
    "spotify_clean_parquet/artist_genres.parquet",
    "spotify_clean_parquet/artists.parquet",
    "spotify_clean_parquet/artist_images.parquet",
    "spotify_clean_parquet/albums.parquet",
    "spotify_clean_parquet/artist_albums.parquet",
    "spotify_clean_parquet/album_images.parquet",
    "spotify_clean_parquet/available_markets.parquet",
]
tracks_db = "spotify_clean_parquet/tracks.parquet"
tracks_artist_db = "spotify_clean_parquet/track_artists.parquet"
artists_db = "spotify_clean_parquet/artists.parquet"
artist_genre_db = "spotify_clean_parquet/artist_genres.parquet"
artist_albums_db = "spotify_clean_parquet/artist_albums.parquet"
albums_db = "spotify_clean_parquet/albums.parquet"


class Handler:
    def __init__(self):
        pass

    def get_db(self):
        tables = {}
        for path in file_paths:
            try:
                table_name = os.path.basename(path)

                # DuckDB 'DESCRIBE' fetches metadata instantly without loading rows
                # We convert the result to a list of column names
                query = f"DESCRIBE SELECT * FROM '{path}'"
                columns = duckdb.sql(query).df()["column_name"].tolist()
                tables[table_name] = set(columns)

            except Exception as e:
                return f"{os.path.basename(path):<25} | Error: {e}"
        return tables

    def album_row_to_json(self, album, artist):
        return {
            "rowid": album.rowid.values.tolist()[0],
            "id": album.id.values.tolist()[0],
            "name": album.name.values.tolist()[0],
            "type": "album",
            "album_type": album.album_type.values.tolist()[0],
            "external_id_upc": album.external_id_upc.values.tolist()[0],
            "copyright_c": album.copyright_c.values.tolist()[0],
            "label": album.label.values.tolist()[0],
            "popularity": album.popularity.values.tolist()[0],
            "release_date": album.release_date.values.tolist()[0],
            "release_date_precision": album.release_date_precision.values.tolist()[0],
            "total_tracks": album.total_tracks.values.tolist()[0],
            "artists": artist,
        }

    def artist_row_to_json(self, artist):
        return {
            "rowid": artist.rowid.values.tolist()[0],
            "id": artist.id.values.tolist()[0],
            "name": artist.name.values.tolist()[0],
            "type": "artist",
            "genres": [],
            "followers": {
                "href": None,
                "total": artist.followers_total.values.tolist()[0],
            },
            "popularity": artist.popularity.values.tolist()[0],
        }

    def track_row_to_json(self, track):
        return {
            "rowid": track.rowid.values.tolist()[0],
            "album_rowid": track.album_rowid.values.tolist()[0],
            "album": {},
            "artists": [],
            "id": track.id.values.tolist()[0],
            "name": track.name.values.tolist()[0],
            "type": "track",
            "explicit": track.explicit.values.tolist()[0],
            "external_ids": {"isrc": track.external_id_isrc.values.tolist()[0]},
            "popularity": track.popularity.values.tolist()[0],
            "duration_ms": track.duration_ms.values.tolist()[0],
            "disc_number": track.disc_number.values.tolist()[0],
            "track_number": track.track_number.values.tolist()[0],
        }

    def track_pandas_to_json(self, track, artists):
        return {
            "rowid": track.rowid,
            "album_rowid": track.album_rowid,
            "artists": artists,
            "id": track.id,
            "name": track.name,
            "type": "track",
            "explicit": track.explicit,
            "external_ids": {"isrc": track.external_id_isrc},
            "popularity": track.popularity,
            "duration_ms": track.duration_ms,
            "disc_number": track.disc_number,
            "track_number": track.track_number,
        }

    def build_track_json(self, track, album, artist):
        return {
            "album": self.album_row_to_json(album, artist),
            "artists": artist,
            "id": track.id.values.tolist()[0],
            "name": track.name.values.tolist()[0],
            "type": "track",
            "explicit": track.explicit.values.tolist()[0],
            "external_ids": {"isrc": track.external_id_isrc.values.tolist()[0]},
            "popularity": track.popularity.values.tolist()[0],
            "duration_ms": track.duration_ms.values.tolist()[0],
            "disc_number": track.disc_number.values.tolist()[0],
            "track_number": track.track_number.values.tolist()[0],
            "is_playable": True,
        }

    def build_album_json(self, tracks, album, artist):
        return {
            "rowid": album.rowid.values.tolist()[0],
            "id": album.id.values.tolist()[0],
            "name": album.name.values.tolist()[0],
            "type": "album",
            "tracks": {"items": tracks},
            "album_type": album.album_type.values.tolist()[0],
            "external_ids": {"upc": album.external_id_upc.values.tolist()[0]},
            "copyrights": [
                {"text": album.copyright_c.values.tolist()[0], "type": "C"},
                {"text": album.copyright_p.values.tolist()[0], "type": "P"},
            ],
            "label": album.label.values.tolist()[0],
            "popularity": album.popularity.values.tolist()[0],
            "release_date": album.release_date.values.tolist()[0],
            "release_date_precision": album.release_date_precision.values.tolist()[0],
            "total_tracks": album.total_tracks.values.tolist()[0],
            "artists": artist,
        }

    def get_track_by_id(self, rowid: str, market: str):
        con = duckdb.connect()
        track = con.execute(f"""
        SELECT * 
        FROM '{tracks_db}'
        WHERE id = '{rowid}'
        """).df()

        album = con.sql(
            f"""
        SELECT * FROM '{albums_db}'
        WHERE rowid = {track.album_rowid.values[0]}
        """
        ).df()

        artistrows = con.sql(f"""
        SELECT * from '{tracks_artist_db}'
        WHERE track_rowid = {track.rowid.values[0]}
        """).df()

        artists = []
        for i in artistrows.artist_rowid.values:
            tempartist = con.sql(
                f"""SELECT * FROM '{artists_db}' WHERE rowid = {i}"""
            ).df()
            artists.append(self.artist_row_to_json(tempartist))

        con.close()

        return self.build_track_json(track, album, artists)

    def get_album_by_id(self, rowid: str, market: str):
        con = duckdb.connect()
        album = con.execute(
            f"""
        SELECT * FROM '{albums_db}'
        WHERE id = '{rowid}'
        """
        ).df()

        tracksrows = con.execute(f"""
        SELECT * 
        FROM '{tracks_db}'
        WHERE album_rowid = '{album.rowid.values[0]}'
        """).df()

        tracklist = []
        for t in tracksrows.itertuples():
            trackartistsrows = con.sql(f"""
                SELECT artist_rowid from '{tracks_artist_db}'
                WHERE track_rowid = '{t.rowid}'
                """).df()

            artists = []
            for i in trackartistsrows.values:
                tempartist = con.sql(
                    f"""SELECT * FROM '{artists_db}' WHERE rowid = {i[0]}"""
                ).df()
                artists.append(self.artist_row_to_json(tempartist))

            tracklist.append(self.track_pandas_to_json(t, artists))

        albumartistsrows = con.sql(f"""
        SELECT artist_rowid from '{artist_albums_db}'
        WHERE album_rowid = '{album.rowid.values[0]}'
        """).df()

        artists = []
        for i in albumartistsrows.values:
            tempartist = con.sql(
                f"""SELECT * FROM '{artists_db}' WHERE rowid = {i[0]}"""
            ).df()
            artists.append(self.artist_row_to_json(tempartist))

        con.close()

        return self.build_album_json(tracklist, album, artists)

    def get_artist_by_id(self, rowid: str, market: str):
        con = duckdb.connect()

        artistrow = con.sql(
            f"""SELECT * FROM '{artists_db}' WHERE id = '{rowid}'"""
        ).df()
        artist = self.artist_row_to_json(artistrow)
        con.close()

        return artist

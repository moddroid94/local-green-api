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
        self.con = duckdb.connect()

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

    def album_df_to_SimplifiedAlbum(self, album, artist):
        return {
            "rowid": album.rowid.values.tolist()[0],
            "id": album.id.values.tolist()[0],
            "name": album.name.values.tolist()[0],
            "type": "album",
            "album_type": album.album_type.values.tolist()[0],
            "popularity": album.popularity.values.tolist()[0],
            "release_date": album.release_date.values.tolist()[0],
            "release_date_precision": album.release_date_precision.values.tolist()[0],
            "total_tracks": album.total_tracks.values.tolist()[0],
            "artists": artist,
        }

    def artist_df_to_ArtistObject(self, artist):
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

    def track_df_to_SimplifiedTrack(self, track):
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

    def track_df_to_TrackObject(self, track, album, artist):
        return {
            "album": self.album_df_to_SimplifiedAlbum(album, artist),
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

    def album_df_to_AlbumObject(self, tracks, album, artist):
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

    def trackPd_to_SimplifiedTrack(self, track, artists):
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

    def trackPd_to_TrackObject(self, track, album, artist):
        return {
            "rowid": track.rowid,
            "album_rowid": track.album_rowid,
            "album": self.album_df_to_SimplifiedAlbum(album, artist),
            "artists": artist,
            "id": track.id,
            "name": track.name,
            "type": "track",
            "explicit": track.explicit,
            "external_ids": {"isrc": track.external_id_isrc},
            "popularity": track.popularity,
            "duration_ms": track.duration_ms,
            "disc_number": track.disc_number,
            "track_number": track.track_number,
            "is_playable": True,
        }

    def _get_artistRowIdRows_for_track_rowid(self, track_rowid):
        return self.con.sql(f"""
        SELECT artist_rowid from '{tracks_artist_db}'
        WHERE track_rowid = {track_rowid}
        """).df()

    def _get_artistRowIdRows_for_album_rowid(self, album_rowid):
        return self.con.sql(f"""
        SELECT artist_rowid from '{artist_albums_db}'
        WHERE album_rowid = '{album_rowid}'
        """).df()

    def _fetch_albumRow_by_rowid(self, album_rowid):
        return self.con.sql(
            f"""
        SELECT * FROM '{albums_db}'
        WHERE rowid = {album_rowid}
        """
        ).df()

    def _fetch_albumRow_by_id(self, album_id):
        return self.con.execute(
            f"""
        SELECT * FROM '{albums_db}'
        WHERE id = '{album_id}'
        """
        ).df()

    def _fetch_trackRow_by_id(self, track_id):
        return self.con.execute(f"""
        SELECT * 
        FROM '{tracks_db}'
        WHERE id = '{track_id}'
        """).df()

    def _fetch_artistRow_by_rowid(self, artist_rowid):
        return self.con.sql(f"""
        SELECT * 
        FROM '{artists_db}'
        WHERE rowid = {artist_rowid}
        """).df()

    def _fetch_artistRow_by_id(self, artist_id):
        return self.con.execute(f"""
        SELECT * 
        FROM '{artists_db}'
        WHERE id = '{artist_id}'
        """).df()

    def _fetch_trackRows_by_album_rowid(self, album_rowid):
        return self.con.sql(f"""
        SELECT * 
        FROM '{tracks_db}'
        WHERE album_rowid = '{album_rowid}'
        """).df()

    def get_track_by_id(self, baseid: str, market: str):
        trackRow = self._fetch_trackRow_by_id(baseid)

        albumRow = self._fetch_albumRow_by_rowid(trackRow.album_rowid.values[0])

        artistRowIdRows = self._get_artistRowIdRows_for_track_rowid(
            trackRow.rowid.values[0]
        )

        artistObjectDict = []
        for i in artistRowIdRows.values:
            artistRow = self._fetch_artistRow_by_rowid(i[0])
            artistObjectDict.append(self.artist_df_to_ArtistObject(artistRow))

        return self.track_df_to_TrackObject(trackRow, albumRow, artistObjectDict)

    def get_album_by_id(self, baseid: str, market: str):
        albumRow = self._fetch_albumRow_by_id(baseid)

        trackRows = self._fetch_trackRows_by_album_rowid(albumRow.rowid.values[0])

        SimplifiedTrackDict = []
        for trackPd in trackRows.itertuples():
            artistRowIdRows = self._get_artistRowIdRows_for_track_rowid(trackPd.rowid)

            trackArtistObjectDict = []
            for i in artistRowIdRows.values:
                artistRow = self._fetch_artistRow_by_rowid(i[0])
                trackArtistObjectDict.append(self.artist_df_to_ArtistObject(artistRow))

            SimplifiedTrackDict.append(
                self.trackPd_to_SimplifiedTrack(trackPd, trackArtistObjectDict)
            )

        artistRowIdRows = self._get_artistRowIdRows_for_album_rowid(
            albumRow.rowid.values[0]
        )

        albumArtistObjectDict = []
        for i in artistRowIdRows.values:
            artistRow = self._fetch_artistRow_by_rowid(i[0])
            albumArtistObjectDict.append(self.artist_df_to_ArtistObject(artistRow))

        return self.album_df_to_AlbumObject(
            SimplifiedTrackDict, albumRow, albumArtistObjectDict
        )

    def get_artist_by_id(self, baseid: str, market: str):
        artistRow = self._fetch_artistRow_by_id(baseid)

        return self.artist_df_to_ArtistObject(artistRow)

    def _search_track_type(
        self,
        db,
        base_query,
        track_filter,
        artist_filter,
        album_filter,
        isrc_filter,
        limit,
    ):
        trackObjectDict = []

        trackRows = self.con.execute(f"""
        SELECT * 
        FROM '{db}'
        WHERE name LIKE '%{base_query}%'
        """).df()

        filtering = False
        if (
            artist_filter != ""
            or album_filter != ""
            or track_filter != ""
            or isrc_filter != ""
        ):
            filtering = True

        for trackPd in trackRows.itertuples():
            if len(trackObjectDict) < limit:
                # isrc filter, if not identical then skips immediately
                if isrc_filter != "" and filtering is True:
                    if trackPd.isrc != isrc_filter:
                        continue
                # filter by album, skips the track if album filter is not contained in album name
                trackAlbumRow = self._fetch_albumRow_by_rowid(trackPd.album_rowid)
                if album_filter != "" and filtering is True:
                    if album_filter not in trackAlbumRow.name.values[0]:
                        continue

                trackArtistRowIdRows = self._get_artistRowIdRows_for_track_rowid(
                    trackPd.rowid
                )

                trackArtistObjectDict = []
                for i in trackArtistRowIdRows.values:
                    artistRow = self._fetch_artistRow_by_rowid(i[0])
                    trackArtistObjectDict.append(
                        self.artist_df_to_ArtistObject(artistRow)
                    )
                # filter by artist, does not add tracks without the specified artist
                trackHasArtist = False
                if artist_filter != "" and filtering is True:
                    for ArtistObject in trackArtistObjectDict:
                        if artist_filter in ArtistObject["name"]:
                            trackHasArtist = True
                    if not trackHasArtist:
                        continue

                trackObjectDict.append(
                    self.trackPd_to_TrackObject(
                        trackPd, trackAlbumRow, trackArtistObjectDict
                    )
                )
            else:
                break
        return trackObjectDict

    def search(
        self,
        base_query,
        track_filter,
        artist_filter,
        album_filter,
        isrc_filter,
        search_type,
        limit,
        offset,
    ):
        match search_type:
            case "track":
                db = tracks_db
                trackObjectDict = self._search_track_type(
                    db,
                    base_query,
                    track_filter,
                    artist_filter,
                    album_filter,
                    isrc_filter,
                    limit,
                )
            case "album":
                db = albums_db
                trackObjectDict = ["NotYetImplemented"]
            case "artist":
                db = artists_db
                trackObjectDict = ["NotYetImplemented"]
            case _:
                trackObjectDict = ["Unknown Type Parameter"]

        return {
            search_type: {
                "href": "",
                "limit": limit,
                "next": None,
                "offset": offset,
                "previous": None,
                "total": len(trackObjectDict),
                "items": trackObjectDict,
            }
        }

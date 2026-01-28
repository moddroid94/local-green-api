# Local Spotify WebAPI Clone

This is a simple project I've built to tag my own music with the immense catalog of Spotify.

After the anna's leak the metadata dataset was made available as a parquet file, for the full 256M rows of metadata the whole db is now only ~30GB in size.

You can find it here: https://www.kaggle.com/datasets/lordpatil/spotify-metadata-by-annas-archive/data

Given the very low space needed I decided to try and emulate the responses of the Spotify API to leverage the already built integrations for metadata in tools like Beets or Picard.

Result: It worked quite well, apart from artworks, the most important infos are available and retrieved correctly, and the only change needed is the url that the integration points to.

### This is still a rough demo, it **mostly** follows the specs but some fields are completely missing, so it may not work correctly with all the integrations yet.



## Usage & Development

The project is managed using uv, more at [installation](https://docs.astral.sh/uv/getting-started/installation/)

- Download the datase and unzip it into the root folder
- Sync the dependency with ```uv sync```
- Run with ```fastapi dev main.py```
- The API should be available at http://127.0.0.1:8000


#### Ps: the routes are **not** prefixed with /v1/ like spotify API.

Headers are ignored, market availability too and all the href/link fields are missing.

## Supported Methods
- Get Several Tracks 
(only 1 track at a time, but with multi-track response schema)
- Get Albums
- Get Artist
- Search*

<br>

*allowed query types are:

`track` with query filters:
`artist:`
`album:`
`isrc:`



## Example Request-Response
<details>

<summary>Get Albums</summary>

### Request: ```http://127.0.0.1:8000/albums/3EncU2oR8VzeuWvLKPIEQd```

### Response:
```json 
{
  "rowid": 767985,
  "id": "3EncU2oR8VzeuWvLKPIEQd",
  "name": "Pivot (Camo & Krooked Remix) / Sinkhole (Skeptical Remix)",
  "type": "album",
  "tracks": {
    "items": [
      {
        "rowid": 9368406,
        "album_rowid": 767985,
        "artists": [
          {
            "rowid": 2501390,
            "id": "54qqaSH6byJIb8eFWxe3Pj",
            "name": "Mefjus",
            "type": "artist",
            "genres": [],
            "followers": {
              "href": null,
              "total": 72765
            },
            "popularity": 52
          },
          {
            "rowid": 4929842,
            "id": "2N8IPNZTiNo3nj4mreOlHU",
            "name": "Camo & Krooked",
            "type": "artist",
            "genres": [],
            "followers": {
              "href": null,
              "total": 237761
            },
            "popularity": 54
          }
        ],
        "id": "5w5Yy1iT2oAHMHi0ecFGRV",
        "name": "Pivot - Camo & Krooked Remix",
        "type": "track",
        "explicit": 0,
        "external_ids": {
          "isrc": "UKACT1830493"
        },
        "popularity": 11,
        "duration_ms": 266181,
        "disc_number": 1,
        "track_number": 1
      },
      {
        "rowid": 9368407,
        "album_rowid": 767985,
        "artists": [
          {
            "rowid": 2501390,
            "id": "54qqaSH6byJIb8eFWxe3Pj",
            "name": "Mefjus",
            "type": "artist",
            "genres": [],
            "followers": {
              "href": null,
              "total": 72765
            },
            "popularity": 52
          },
          {
            "rowid": 5138393,
            "id": "28ee6rnxMl8AqwcroPfivP",
            "name": "Skeptical",
            "type": "artist",
            "genres": [],
            "followers": {
              "href": null,
              "total": 26163
            },
            "popularity": 37
          }
        ],
        "id": "4pQp4qcip75nJACmwsDstb",
        "name": "Sinkhole - Skeptical Remix",
        "type": "track",
        "explicit": 0,
        "external_ids": {
          "isrc": "UKACT1830494"
        },
        "popularity": 16,
        "duration_ms": 277674,
        "disc_number": 1,
        "track_number": 2
      }
    ]
  },
  "album_type": "single",
  "external_ids": {
    "upc": "5057272089689"
  },
  "copyrights": [
    {
      "text": "2018 Vision Recordings",
      "type": "C"
    },
    {
      "text": "2018 Vision Recordings",
      "type": "P"
    }
  ],
  "label": "Vision Recordings",
  "popularity": 7,
  "release_date": "2018-11-02",
  "release_date_precision": "day",
  "total_tracks": 2,
  "artists": [
    {
      "rowid": 2501390,
      "id": "54qqaSH6byJIb8eFWxe3Pj",
      "name": "Mefjus",
      "type": "artist",
      "genres": [],
      "followers": {
        "href": null,
        "total": 72765
      },
      "popularity": 52
    },
    {
      "rowid": 4929842,
      "id": "2N8IPNZTiNo3nj4mreOlHU",
      "name": "Camo & Krooked",
      "type": "artist",
      "genres": [],
      "followers": {
        "href": null,
        "total": 237761
      },
      "popularity": 54
    },
    {
      "rowid": 5138393,
      "id": "28ee6rnxMl8AqwcroPfivP",
      "name": "Skeptical",
      "type": "artist",
      "genres": [],
      "followers": {
        "href": null,
        "total": 26163
      },
      "popularity": 37
    }
  ]
}
```
</details>
<br>
<details>

<summary>Get Several Tracks</summary>

### Request: ```http://127.0.0.1:8000/tracks?ids=4pQp4qcip75nJACmwsDstb```

### Response:
```json 
{
  "tracks": [
    {
      "album": {
        "rowid": 767985,
        "id": "3EncU2oR8VzeuWvLKPIEQd",
        "name": "Pivot (Camo & Krooked Remix) / Sinkhole (Skeptical Remix)",
        "type": "album",
        "album_type": "single",
        "external_id_upc": "5057272089689",
        "copyright_c": "2018 Vision Recordings",
        "label": "Vision Recordings",
        "popularity": 7,
        "release_date": "2018-11-02",
        "release_date_precision": "day",
        "total_tracks": 2,
        "artists": [
          {
            "rowid": 2501390,
            "id": "54qqaSH6byJIb8eFWxe3Pj",
            "name": "Mefjus",
            "type": "artist",
            "genres": [],
            "followers": {
              "href": null,
              "total": 72765
            },
            "popularity": 52
          },
          {
            "rowid": 5138393,
            "id": "28ee6rnxMl8AqwcroPfivP",
            "name": "Skeptical",
            "type": "artist",
            "genres": [],
            "followers": {
              "href": null,
              "total": 26163
            },
            "popularity": 37
          }
        ]
      },
      "artists": [
        {
          "rowid": 2501390,
          "id": "54qqaSH6byJIb8eFWxe3Pj",
          "name": "Mefjus",
          "type": "artist",
          "genres": [],
          "followers": {
            "href": null,
            "total": 72765
          },
          "popularity": 52
        },
        {
          "rowid": 5138393,
          "id": "28ee6rnxMl8AqwcroPfivP",
          "name": "Skeptical",
          "type": "artist",
          "genres": [],
          "followers": {
            "href": null,
            "total": 26163
          },
          "popularity": 37
        }
      ],
      "id": "4pQp4qcip75nJACmwsDstb",
      "name": "Sinkhole - Skeptical Remix",
      "type": "track",
      "explicit": 0,
      "external_ids": {
        "isrc": "UKACT1830494"
      },
      "popularity": 16,
      "duration_ms": 277674,
      "disc_number": 1,
      "track_number": 2,
      "is_playable": true
    }
  ]
}
```
</details>
<br>
<details>

<summary>Get Artist</summary>

### Request: ```http://127.0.0.1:8000/artists/54qqaSH6byJIb8eFWxe3Pj```

### Response:
```json 
{
  "rowid": 2501390,
  "id": "54qqaSH6byJIb8eFWxe3Pj",
  "name": "Mefjus",
  "type": "artist",
  "genres": [],
  "followers": {
    "href": null,
    "total": 72765
  },
  "popularity": 52
}
```
</details>
<br>
<details>

<summary>Search</summary>

### Request: ```http://127.0.0.1:8000/search?q=Crank%20-%20Kasra%20album:Resonance%20&type=track&limit=1```

### Response:
```json 
{
  "track": {
    "href": "",
    "limit": 1,
    "next": null,
    "offset": 0,
    "previous": null,
    "total": 1,
    "items": [
      {
        "rowid": 9329915,
        "album_rowid": 762445,
        "album": {
          "rowid": 762445,
          "id": "1vqbno1uvn9oBuE6nPD5MR",
          "name": "The Resonance V",
          "type": "album",
          "album_type": "album",
          "popularity": 11,
          "release_date": "2023-02-17",
          "release_date_precision": "day",
          "total_tracks": 15,
          "artists": [
            {
              "rowid": 2968258,
              "id": "4YWj8sohRDjL9deiuRvEEY",
              "name": "Noisia",
              "type": "artist",
              "genres": [],
              "followers": {
                "href": null,
                "total": 283349
              },
              "popularity": 50
            },
            {
              "rowid": 3902266,
              "id": "3W1ubrHvNSMltB1l7zo6xt",
              "name": "Kasra",
              "type": "artist",
              "genres": [],
              "followers": {
                "href": null,
                "total": 19665
              },
              "popularity": 34
            }
          ]
        },
        "artists": [
          {
            "rowid": 2968258,
            "id": "4YWj8sohRDjL9deiuRvEEY",
            "name": "Noisia",
            "type": "artist",
            "genres": [],
            "followers": {
              "href": null,
              "total": 283349
            },
            "popularity": 50
          },
          {
            "rowid": 3902266,
            "id": "3W1ubrHvNSMltB1l7zo6xt",
            "name": "Kasra",
            "type": "artist",
            "genres": [],
            "followers": {
              "href": null,
              "total": 19665
            },
            "popularity": 34
          }
        ],
        "id": "16Ek7OlxiIipZ59CYT3vVG",
        "name": "Crank - Kasra Remix",
        "type": "track",
        "explicit": 0,
        "external_ids": {
          "isrc": "UKU932390011"
        },
        "popularity": 5,
        "duration_ms": 248372,
        "disc_number": 1,
        "track_number": 10,
        "is_playable": true
      }
    ]
  }
}
```
</details>
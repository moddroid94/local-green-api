# Local Green WebAPI Clone

## Disclaimer
This project is not affiliated with, endorsed by, or connected to Spotify AB or any other music streaming service. This is independent open-source software that provides API infrastructure for querying music metadata databases.

## Warning
This repository does not include any databases or copyrighted data. You must obtain the .parquet databases separately. This project only provides the API server code to query existing databases.

The author(s) of this project are not responsible for how you obtain or use the underlying data. Users are solely responsible for ensuring their use of any databases complies with applicable laws and terms of service. This software is provided "as is" without warranty of any kind.

## Info
This is a simple project I've built to tag my own music with the immense catalog of Spotify.

After the anna's leak the metadata dataset was made available as a parquet file, for the full 256M rows of metadata the whole db is now only ~30GB in size.

You can find it here: https://www.kaggle.com/datasets/lordpatil/spotify-metadata-by-annas-archive/data

Given the very low space needed I decided to try and emulate the responses of the Spotify API to leverage the already built integrations for metadata in tools like Beets or Picard.

Result: It worked quite well, apart from artworks, the most important infos are available and retrieved correctly, the only changes being the API url and an auth bypass.

### This is still a rough demo, it **mostly** follows the specs but most methods are missing, so it may not work correctly with all the integrations yet.



## Usage & Development

The project is managed using uv, more at [installation](https://docs.astral.sh/uv/getting-started/installation/)

- Download the datase and unzip it into the root folder
- Sync the dependency with ```uv sync```
- Run with ```fastapi dev main.py```
- The API should be available at http://127.0.0.1:8000


#### Ps: the routes are **not** prefixed with /v1/ like spotify API.

Headers are ignored, market availability too.

## Supported Methods
- Get Several Tracks<sup>1</sup> (Return Spec Compliant)
- Get Albums (Full Spec Compliant)
- Get Artist (Full Spec Compliant)
- Search<sup>2</sup> (Return Spec Compliant)

<br>
1) Only 1 track at a time, but with multi-track response schema

<br>
2) Allowed query types are:

- `track` with query filters:
`artist:`
`album:`
`isrc:`

<br>

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
    "href": "https://api.spotify.com/v1/albums/3EncU2oR8VzeuWvLKPIEQd/tracks",
    "next": null,
    "total": 2,
    "previous": null,
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
            "popularity": 52,
            "href": "https://api.spotify.com/v1/artists/54qqaSH6byJIb8eFWxe3Pj",
            "uri": "spotify:artist:54qqaSH6byJIb8eFWxe3Pj",
            "external_url": {
              "spotify": "https://open.spotify.com/artist/54qqaSH6byJIb8eFWxe3Pj"
            }
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
            "popularity": 54,
            "href": "https://api.spotify.com/v1/artists/2N8IPNZTiNo3nj4mreOlHU",
            "uri": "spotify:artist:2N8IPNZTiNo3nj4mreOlHU",
            "external_url": {
              "spotify": "https://open.spotify.com/artist/2N8IPNZTiNo3nj4mreOlHU"
            }
          }
        ],
        "id": "5w5Yy1iT2oAHMHi0ecFGRV",
        "name": "Pivot - Camo & Krooked Remix",
        "type": "track",
        "external_url": {
          "spotify": "https://open.spotify.com/track/5w5Yy1iT2oAHMHi0ecFGRV"
        },
        "href": "https://api.spotify.com/v1/tracks/5w5Yy1iT2oAHMHi0ecFGRV",
        "uri": "spotify:track:5w5Yy1iT2oAHMHi0ecFGRV",
        "preview_url": null,
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
            "popularity": 52,
            "href": "https://api.spotify.com/v1/artists/54qqaSH6byJIb8eFWxe3Pj",
            "uri": "spotify:artist:54qqaSH6byJIb8eFWxe3Pj",
            "external_url": {
              "spotify": "https://open.spotify.com/artist/54qqaSH6byJIb8eFWxe3Pj"
            }
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
            "popularity": 37,
            "href": "https://api.spotify.com/v1/artists/28ee6rnxMl8AqwcroPfivP",
            "uri": "spotify:artist:28ee6rnxMl8AqwcroPfivP",
            "external_url": {
              "spotify": "https://open.spotify.com/artist/28ee6rnxMl8AqwcroPfivP"
            }
          }
        ],
        "id": "4pQp4qcip75nJACmwsDstb",
        "name": "Sinkhole - Skeptical Remix",
        "type": "track",
        "external_url": {
          "spotify": "https://open.spotify.com/track/4pQp4qcip75nJACmwsDstb"
        },
        "href": "https://api.spotify.com/v1/tracks/4pQp4qcip75nJACmwsDstb",
        "uri": "spotify:track:4pQp4qcip75nJACmwsDstb",
        "preview_url": null,
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
  "external_url": {
    "spotify": "https://open.spotify.com/album/3EncU2oR8VzeuWvLKPIEQd"
  },
  "href": "https://api.spotify.com/v1/albums/3EncU2oR8VzeuWvLKPIEQd",
  "uri": "spotify:album:3EncU2oR8VzeuWvLKPIEQd",
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
  "images": [],
  "genres": [],
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
      "popularity": 52,
      "href": "https://api.spotify.com/v1/artists/54qqaSH6byJIb8eFWxe3Pj",
      "uri": "spotify:artist:54qqaSH6byJIb8eFWxe3Pj",
      "external_url": {
        "spotify": "https://open.spotify.com/artist/54qqaSH6byJIb8eFWxe3Pj"
      }
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
      "popularity": 54,
      "href": "https://api.spotify.com/v1/artists/2N8IPNZTiNo3nj4mreOlHU",
      "uri": "spotify:artist:2N8IPNZTiNo3nj4mreOlHU",
      "external_url": {
        "spotify": "https://open.spotify.com/artist/2N8IPNZTiNo3nj4mreOlHU"
      }
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
      "popularity": 37,
      "href": "https://api.spotify.com/v1/artists/28ee6rnxMl8AqwcroPfivP",
      "uri": "spotify:artist:28ee6rnxMl8AqwcroPfivP",
      "external_url": {
        "spotify": "https://open.spotify.com/artist/28ee6rnxMl8AqwcroPfivP"
      }
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
            "popularity": 52,
            "href": "https://api.spotify.com/v1/artists/54qqaSH6byJIb8eFWxe3Pj",
            "uri": "spotify:artist:54qqaSH6byJIb8eFWxe3Pj",
            "external_url": {
              "spotify": "https://open.spotify.com/artist/54qqaSH6byJIb8eFWxe3Pj"
            }
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
            "popularity": 37,
            "href": "https://api.spotify.com/v1/artists/28ee6rnxMl8AqwcroPfivP",
            "uri": "spotify:artist:28ee6rnxMl8AqwcroPfivP",
            "external_url": {
              "spotify": "https://open.spotify.com/artist/28ee6rnxMl8AqwcroPfivP"
            }
          }
        ],
        "external_url": {
          "spotify": "https://open.spotify.com/album/3EncU2oR8VzeuWvLKPIEQd"
        },
        "href": "https://api.spotify.com/v1/albums/3EncU2oR8VzeuWvLKPIEQd",
        "uri": "spotify:album:3EncU2oR8VzeuWvLKPIEQd",
        "images": []
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
          "popularity": 52,
          "href": "https://api.spotify.com/v1/artists/54qqaSH6byJIb8eFWxe3Pj",
          "uri": "spotify:artist:54qqaSH6byJIb8eFWxe3Pj",
          "external_url": {
            "spotify": "https://open.spotify.com/artist/54qqaSH6byJIb8eFWxe3Pj"
          }
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
          "popularity": 37,
          "href": "https://api.spotify.com/v1/artists/28ee6rnxMl8AqwcroPfivP",
          "uri": "spotify:artist:28ee6rnxMl8AqwcroPfivP",
          "external_url": {
            "spotify": "https://open.spotify.com/artist/28ee6rnxMl8AqwcroPfivP"
          }
        }
      ],
      "id": "4pQp4qcip75nJACmwsDstb",
      "name": "Sinkhole - Skeptical Remix",
      "type": "track",
      "external_url": {
        "spotify": "https://open.spotify.com/track/4pQp4qcip75nJACmwsDstb"
      },
      "href": "https://api.spotify.com/v1/tracks/4pQp4qcip75nJACmwsDstb",
      "uri": "spotify:track:4pQp4qcip75nJACmwsDstb",
      "preview_url": null,
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
  "popularity": 52,
  "href": "https://api.spotify.com/v1/artists/54qqaSH6byJIb8eFWxe3Pj",
  "uri": "spotify:artist:54qqaSH6byJIb8eFWxe3Pj",
  "external_url": {
    "spotify": "https://open.spotify.com/artist/54qqaSH6byJIb8eFWxe3Pj"
  }
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
              "popularity": 50,
              "href": "https://api.spotify.com/v1/artists/4YWj8sohRDjL9deiuRvEEY",
              "uri": "spotify:artist:4YWj8sohRDjL9deiuRvEEY",
              "external_url": {
                "spotify": "https://open.spotify.com/artist/4YWj8sohRDjL9deiuRvEEY"
              }
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
              "popularity": 34,
              "href": "https://api.spotify.com/v1/artists/3W1ubrHvNSMltB1l7zo6xt",
              "uri": "spotify:artist:3W1ubrHvNSMltB1l7zo6xt",
              "external_url": {
                "spotify": "https://open.spotify.com/artist/3W1ubrHvNSMltB1l7zo6xt"
              }
            }
          ],
          "external_url": {
            "spotify": "https://open.spotify.com/album/1vqbno1uvn9oBuE6nPD5MR"
          },
          "href": "https://api.spotify.com/v1/albums/1vqbno1uvn9oBuE6nPD5MR",
          "uri": "spotify:album:1vqbno1uvn9oBuE6nPD5MR",
          "images": []
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
            "popularity": 50,
            "href": "https://api.spotify.com/v1/artists/4YWj8sohRDjL9deiuRvEEY",
            "uri": "spotify:artist:4YWj8sohRDjL9deiuRvEEY",
            "external_url": {
              "spotify": "https://open.spotify.com/artist/4YWj8sohRDjL9deiuRvEEY"
            }
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
            "popularity": 34,
            "href": "https://api.spotify.com/v1/artists/3W1ubrHvNSMltB1l7zo6xt",
            "uri": "spotify:artist:3W1ubrHvNSMltB1l7zo6xt",
            "external_url": {
              "spotify": "https://open.spotify.com/artist/3W1ubrHvNSMltB1l7zo6xt"
            }
          }
        ],
        "id": "16Ek7OlxiIipZ59CYT3vVG",
        "name": "Crank - Kasra Remix",
        "type": "track",
        "external_url": {
          "spotify": "https://open.spotify.com/track/16Ek7OlxiIipZ59CYT3vVG"
        },
        "href": "https://api.spotify.com/v1/tracks/16Ek7OlxiIipZ59CYT3vVG",
        "uri": "spotify:track:16Ek7OlxiIipZ59CYT3vVG",
        "preview_url": null,
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

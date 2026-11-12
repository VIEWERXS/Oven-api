from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ytmusicapi import YTMusic

app = FastAPI()
yt = YTMusic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def format_tracks(results):
    tracks = []
    for t in results:
        if not t.get("videoId"):
            continue
        thumbs = t.get("thumbnails", [])
        cover = thumbs[-1]["url"] if thumbs else ""
        artists = t.get("artists", [])
        artist_name = artists[0]["name"] if artists else "Artista"
        album = t.get("album")
        album_name = album["name"] if album and isinstance(album, dict) else "Sencillo"
        
        tracks.append({
            "id": t["videoId"],
            "title": t.get("title", "Sin título"),
            "artist": artist_name,
            "album": album_name,
            "cover": cover,
            "dur": t.get("duration_seconds") or 180
        })
    return tracks

@app.get("/search")
def search(q: str):
    return format_tracks(yt.search(q, filter="songs", limit=20))

@app.get("/popular")
def popular():
    return format_tracks(yt.search("top hits reggaeton pop", filter="songs", limit=20))

@app.get("/newest")
def newest():
    return format_tracks(yt.search("estrenos musica urbana", filter="songs", limit=15))

@app.get("/tag")
def by_tag(t: str):
    return format_tracks(yt.search(f"{t} hits", filter="songs", limit=15))
      

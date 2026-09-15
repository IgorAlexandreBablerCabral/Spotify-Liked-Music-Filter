import os
from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

SCOPES = (
    "user-library-read "
    "playlist-modify-public "
    "playlist-modify-private"
)

# Limites da API
LIKED_TRACKS_LIMIT = 50       # max por request
ARTIST_BATCH_SIZE = 50        # max artists por request
PLAYLIST_TRACK_BATCH = 100    # max tracks por request ao adicionar

# Gêneros ignorados (muito amplos ou genéricos demais)
GENRES_BLACKLIST = {
    "music", "songs", "canzone", "musica"
}

# Prefixo das playlists criadas
PLAYLIST_PREFIX = "SGO"

# Limite mínimo de músicas para criar uma playlist de gênero
MIN_TRACKS_PER_GENRE = 3

# Cache
CACHE_FILE = "genre_cache.json"
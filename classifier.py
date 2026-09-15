import spotipy
from collections import defaultdict
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

from config import (
    ARTIST_BATCH_SIZE,
    GENRES_BLACKLIST,
)
from cache import load_cache, save_cache

console = Console()


def classify_tracks_by_genre(sp: spotipy.Spotify, tracks: list[dict]) -> dict:
    """
    Para cada track, consulta os gêneros dos artistas na API do Spotify.
    Retorna: { "rock": [track, ...], "mpb": [track, ...], ... }
    """
    # 1. Coletar todos os artist_ids únicos
    artist_ids = set()
    for track in tracks:
        for artist in track["artists"]:
            artist_ids.add(artist["id"])

    console.print(f"[bold cyan]🎸 Artistas únicos encontrados:[/] {len(artist_ids)}\n")

    # 2. Carregar cache existente
    genre_cache = load_cache()
    uncached_ids = [aid for aid in artist_ids if aid not in genre_cache]

    console.print(
        f"[dim]Artistas já em cache:[/] {len(artist_ids) - len(uncached_ids)} | "
        f"[dim]A consultar:[/] {len(uncached_ids)}\n"
    )

    # 3. Consultar gêneros dos artistas não-cacheados (em batch)
    if uncached_ids:
        _fetch_artist_genres(sp, uncached_ids, genre_cache)
        save_cache(genre_cache)

    # 4. Mapear tracks → gêneros
    genre_map: dict[str, list[dict]] = defaultdict(list)

    for track in tracks:
        track_genres = set()
        for artist in track["artists"]:
            artist_genres = genre_cache.get(artist["id"], [])
            track_genres.update(artist_genres)

        if not track_genres:
            genre_map["outros"].append(track)
        else:
            for genre in track_genres:
                genre_map[genre].append(track)

    # 5. Remover gêneros da blacklist
    for bl in GENRES_BLACKLIST:
        genre_map.pop(bl, None)

    # 6. Estatísticas
    sorted_genres = sorted(genre_map.items(), key=lambda x: -len(x[1]))
    console.print("[bold]📊 Distribuição por gênero:[/]\n")
    for genre, genre_tracks in sorted_genres[:20]:
        console.print(f"  [cyan]{genre:<30}[/] {len(genre_tracks):>5} músicas")

    if len(sorted_genres) > 20:
        console.print(f"  [dim]... e mais {len(sorted_genres) - 20} gêneros[/]")

    console.print(f"\n[green]✓[/] {len(genre_map)} gêneros identificados.\n")

    return dict(genre_map)


def _fetch_artist_genres(sp: spotipy.Spotify, artist_ids: list[str], cache: dict):
    """Consulta os gêneros dos artistas em batches de 50."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("Consultando gêneros...", total=len(artist_ids))

        for i in range(0, len(artist_ids), ARTIST_BATCH_SIZE):
            batch = artist_ids[i : i + ARTIST_BATCH_SIZE]
            artists_data = sp.artists(batch)["artists"]

            for artist in artists_data:
                if artist:
                    cache[artist["id"]] = artist.get("genres", [])

            progress.update(task, advance=len(batch))
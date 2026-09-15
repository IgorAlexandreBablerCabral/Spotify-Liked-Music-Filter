import spotipy
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

from config import (
    PLAYLIST_PREFIX,
    PLAYLIST_TRACK_BATCH,
    MIN_TRACKS_PER_GENRE,
)

console = Console()


def create_genre_playlists(
    sp: spotipy.Spotify, genre_map: dict[str, list[dict]]
) -> list[dict]:
    """
    Para cada gênero com músicas suficientes, cria uma playlist
    e adiciona as músicas.
    Retorna lista de {genre, playlist_url, track_count}
    """
    user_id = sp.current_user()["id"]
    results = []

    # Filtrar gêneros com músicas suficientes
    valid_genres = {
        genre: tracks
        for genre, tracks in genre_map.items()
        if len(tracks) >= MIN_TRACKS_PER_GENRE
    }

    skipped = len(genre_map) - len(valid_genres)
    if skipped > 0:
        console.print(
            f"[dim]Ignorando {skipped} gêneros com menos de "
            f"{MIN_TRACKS_PER_GENRE} músicas[/]\n"
        )

    console.print(f"[bold cyan]📝 Criando {len(valid_genres)} playlists...[/]\n")

    sorted_genres = sorted(valid_genres.items(), key=lambda x: -len(x[1]))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("Criando playlists...", total=len(sorted_genres))

        for genre, tracks in sorted_genres:
            # Criar playlist
            playlist_name = f"{PLAYLIST_PREFIX} · {genre.title()}"
            playlist_desc = (
                f"Auto-organizado pelo SGO · "
                f"{len(tracks)} músicas · "
                f"Gênero: {genre}"
            )

            playlist = sp.user_playlist_create(
                user=user_id,
                name=playlist_name,
                public=False,
                description=playlist_desc,
            )

            # Adicionar tracks em batches de 100
            track_uris = list({t["track_uri"] for t in tracks})  # deduplicar
            for j in range(0, len(track_uris), PLAYLIST_TRACK_BATCH):
                batch = track_uris[j : j + PLAYLIST_TRACK_BATCH]
                sp.playlist_add_items(playlist["id"], batch)

            results.append(
                {
                    "genre": genre,
                    "playlist_url": playlist["external_urls"]["spotify"],
                    "track_count": len(track_uris),
                }
            )

            progress.update(task, advance=1)

    console.print(f"\n[green]✓[/] {len(results)} playlists criadas com sucesso!\n")
    return results
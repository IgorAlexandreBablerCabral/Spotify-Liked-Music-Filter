import spotipy
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

from config import LIKED_TRACKS_LIMIT

console = Console()


def collect_liked_tracks(sp: spotipy.Spotify) -> list[dict]:
    """
    Coleta TODAS as músicas curtidas do usuário.
    Retorna uma lista de dicts com: track_name, artists, track_uri, album
    """
    tracks = []
    offset = 0

    # Primeira chamada para saber o total
    initial = sp.current_user_saved_tracks(limit=1, offset=0)
    total = initial["total"]
    console.print(f"\n[bold cyan]🎵 Total de músicas curtidas:[/] {total}\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("Coletando músicas...", total=total)

        while offset < total:
            results = sp.current_user_saved_tracks(
                limit=LIKED_TRACKS_LIMIT, offset=offset
            )

            for item in results["items"]:
                track = item["track"]
                if track is None:
                    continue

                tracks.append(
                    {
                        "track_name": track["name"],
                        "track_uri": track["uri"],
                        "artists": [
                            {
                                "id": a["id"],
                                "name": a["name"],
                            }
                            for a in track["artists"]
                        ],
                        "album": track["album"]["name"],
                    }
                )

            offset += LIKED_TRACKS_LIMIT
            progress.update(task, advance=LIKED_TRACKS_LIMIT)

    console.print(f"[green]✓[/] {len(tracks)} músicas coletadas.\n")
    return tracks
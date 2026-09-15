#!/usr/bin/env python3
"""
Spotify Genre Organizer (SGO)
Organiza suas músicas curtidas do Spotify por gênero automaticamente.
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from rich.console import Console
from rich.panel import Panel

from config import (
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SPOTIPY_REDIRECT_URI,
    SCOPES,
)
from collector import collect_liked_tracks
from classifier import classify_tracks_by_genre
from playlist_creator import create_genre_playlists
from reporter import print_report

console = Console()


def main():
    console.print(
        Panel.fit(
            "[bold white]Spotify Genre Organizer[/]\n"
            "[dim]Organize suas músicas curtidas por gênero automaticamente[/]",
            border_style="green",
        )
    )

    # ---- 1. Autenticação ----
    console.print("\n[bold]🔐 Autenticando com o Spotify...[/]")
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope=SCOPES,
            open_browser=True,
            cache_path=".spotify_token_cache",
        )
    )

    user = sp.current_user()
    console.print(
        f"[green]✓[/] Conectado como: [bold]{user['display_name']}[/]\n"
    )

    # ---- 2. Coletar músicas curtidas ----
    tracks = collect_liked_tracks(sp)
    if not tracks:
        console.print("[red]Nenhuma música curtida encontrada. Saindo.[/]")
        return

    # ---- 3. Classificar por gênero ----
    genre_map = classify_tracks_by_genre(sp, tracks)

    # ---- 4. Confirmar antes de criar playlists ----
    console.print(
        f"\n[bold yellow]⚡ Serão criadas playlists para "
        f"{len(genre_map)} gêneros.[/]"
    )
    confirm = input("Deseja continuar? (s/n): ").strip().lower()
    if confirm != "s":
        console.print("[red]Operação cancelada.[/]")
        return

    # ---- 5. Criar playlists ----
    results = create_genre_playlists(sp, genre_map)

    # ---- 6. Relatório final ----
    print_report(results, total_tracks=len(tracks))

    console.print("[bold green]🎉 Concluído! Abra o Spotify para ver suas playlists.[/]\n")


if __name__ == "__main__":
    main()
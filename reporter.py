import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def print_report(results: list[dict], total_tracks: int):
    """Exibe um relatório bonito no terminal e salva em JSON."""

    # ---- Tabela no terminal ----
    table = Table(
        title="Relatório Final - Spotify Genre Organizer",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("#", style="dim", width=4)
    table.add_column("Gênero", style="cyan", min_width=25)
    table.add_column("Músicas", justify="right", style="green")
    table.add_column("Playlist", style="blue underline")

    for i, r in enumerate(results, 1):
        table.add_row(
            str(i),
            r["genre"].title(),
            str(r["track_count"]),
            r["playlist_url"],
        )

    console.print(table)

    # ---- Resumo ----
    summary = (
        f"[bold]Total de músicas analisadas:[/] {total_tracks}\n"
        f"[bold]Playlists criadas:[/] {len(results)}\n"
        f"[bold]Data:[/] {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )
    console.print(Panel(summary, title="Resumo", border_style="green"))

    # ---- Salvar JSON ----
    report_data = {
        "generated_at": datetime.now().isoformat(),
        "total_tracks_analyzed": total_tracks,
        "playlists_created": len(results),
        "playlists": results,
    }

    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    console.print("[dim]Relatório salvo em report.json[/]\n")
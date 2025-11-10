from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.table import Table

from player_stats import PlayerStats
from player_reader import PlayerReader

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    while True:
        console = Console()

        list_of_nationalities = "[USA/FIN/CAN/SWE/CZE/RUS/SLO/FRA/GBR/SVK/DEN/NED/AUT/BLR/GER/SUI/NOR/UZB/LAT/AUS]"
        nationality = input(f"Nationality {list_of_nationalities} ")
        players = stats.top_scorers_by_nationality(nationality)

        table_data =[]

        for player in players:
            table_data.append([f"[cyan]{player.name}[/]",
            f"[magenta]{player.team}",
            f"[green]{player.goals}",
            f"[green]{player.assists}",
            f"[green]{player.points}"
            ])

        table = Table(show_footer=False)
        table_centered = Align.center(table)

        console.clear()

        with Live(table_centered, console=console,
                screen=False):
            table.add_column("Released", no_wrap=True)
            table.add_column("Teams", no_wrap=True)
            table.add_column("Goals", justify='right', no_wrap=True)
            table.add_column("Assists", justify='right', no_wrap=True)
            table.add_column("Points", justify='right', no_wrap=True)
            for row in table_data:
                table.add_row(*row)

            # table_width = console.measure(table).maximum

            # table.width = None

if __name__ == "__main__":
    main()

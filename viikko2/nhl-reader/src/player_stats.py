from player_reader import PlayerReader

class PlayerStats():
    def __init__(self, player_reader : PlayerReader):
        self.reader = player_reader

        self._players = self.reader.get_players()

    def top_scorers_by_nationality(self, nationality):     
        filtered_by_nationality = filter(lambda player: player.nationality == nationality, self._players)

        sort_by_points = sorted(list(filtered_by_nationality), key=lambda player: player.points, reverse=True)

        return sort_by_points
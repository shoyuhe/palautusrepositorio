from statistics_service import StatisticsService
from player_reader import PlayerReader
from player import Player
import unittest

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search(self):
        player_search = self.stats.search("Lemieux")
        self.assertEqual(player_search.name, "Lemieux")

    def test_search_no_player(self):
        player_search = self.stats.search("Player")
        self.assertEqual(player_search, None)

    def test_team(self):
        test_EDM_list = self.stats.team("EDM") 
        expected_list = ["Semenko", "Kurri", "Gretzky"]
        self.assertEqual([player.name for player in test_EDM_list], expected_list)

    def test_top(self):
        top_scorers = self.stats.top(2)
        expected_list = ["Gretzky", "Lemieux"]
        self.assertEqual([player.name for player in top_scorers], expected_list)

if __name__ == "__main__":
    unittest.main()
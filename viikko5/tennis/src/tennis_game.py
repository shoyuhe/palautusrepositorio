class TennisGame:
    Tennis_Score_Name = {0: "Love", 1: "Fifteen", 2: "Thirty", 3: "Forty"}

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = 0
        self.player2_points = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.player1_points += 1
        else:
            self.player2_points += 1

    def get_score(self):
        if self.if_tied():
            return self.tied_score()
        if self.if_endgame():
            return self.advantage_or_win()
        return self.game_score()

    def game_score(self):
        player1_score_name = self.Tennis_Score_Name[self.player1_points]
        player2_score_name = self.Tennis_Score_Name[self.player2_points]
        return f"{player1_score_name}-{player2_score_name}"

    #Tie
    def if_tied(self):
        return self.player1_points == self.player2_points

    def tied_score(self):
        if self.player1_points <= 2:
            return f"{self.Tennis_Score_Name[self.player1_points]}-All"
        return "Deuce"

    #Endgame
    def if_endgame(self):
        return self.player1_points >= 4 or self.player2_points >= 4

    def advantage_or_win(self):
        score_diff = self.player1_points - self.player2_points

        if score_diff == 1:
            return "Advantage player1"
        if score_diff == -1:
            return "Advantage player2"
        if score_diff >= 2:
            return "Win for player1"
        return "Win for player2"

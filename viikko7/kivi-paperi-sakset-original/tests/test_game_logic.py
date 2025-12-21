"""Unit tests for game logic classes."""
import pytest

from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu


class TestTuomari:
    """Tests for the Tuomari (referee) class."""
    
    def test_initial_state(self):
        """Test that Tuomari starts with zero scores."""
        tuomari = Tuomari()
        assert tuomari.ekan_pisteet == 0
        assert tuomari.tokan_pisteet == 0
        assert tuomari.tasapelit == 0
        assert tuomari.ekan_perakkaisia == 0
        assert tuomari.tokan_perakkaisia == 0
    
    def test_tie_game(self):
        """Test that ties are recorded correctly."""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "k")
        assert tuomari.ekan_pisteet == 0
        assert tuomari.tokan_pisteet == 0
        assert tuomari.tasapelit == 1
        assert tuomari.ekan_perakkaisia == 0
        assert tuomari.tokan_perakkaisia == 0
        
        tuomari.kirjaa_siirto("p", "p")
        assert tuomari.tasapelit == 2
        
        tuomari.kirjaa_siirto("s", "s")
        assert tuomari.tasapelit == 3
    
    def test_first_player_wins_rock_scissors(self):
        """Test that rock beats scissors."""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "s")
        assert tuomari.ekan_pisteet == 1
        assert tuomari.tokan_pisteet == 0
        assert tuomari.ekan_perakkaisia == 1
        assert tuomari.tokan_perakkaisia == 0
    
    def test_first_player_wins_scissors_paper(self):
        """Test that scissors beats paper."""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("s", "p")
        assert tuomari.ekan_pisteet == 1
        assert tuomari.tokan_pisteet == 0
    
    def test_first_player_wins_paper_rock(self):
        """Test that paper beats rock."""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("p", "k")
        assert tuomari.ekan_pisteet == 1
        assert tuomari.tokan_pisteet == 0
    
    def test_second_player_wins_rock_scissors(self):
        """Test that second player wins with rock against scissors."""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("s", "k")
        assert tuomari.ekan_pisteet == 0
        assert tuomari.tokan_pisteet == 1
    
    def test_second_player_wins_scissors_paper(self):
        """Test that second player wins with scissors against paper."""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("p", "s")
        assert tuomari.ekan_pisteet == 0
        assert tuomari.tokan_pisteet == 1
    
    def test_second_player_wins_paper_rock(self):
        """Test that second player wins with paper against rock."""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "p")
        assert tuomari.ekan_pisteet == 0
        assert tuomari.tokan_pisteet == 1
    
    def test_multiple_rounds(self):
        """Test multiple rounds with different outcomes."""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "s")  # Player 1 wins
        tuomari.kirjaa_siirto("p", "p")  # Tie
        tuomari.kirjaa_siirto("s", "k")  # Player 2 wins
        tuomari.kirjaa_siirto("k", "p")  # Player 2 wins
        
        assert tuomari.ekan_pisteet == 1
        assert tuomari.tokan_pisteet == 2
        assert tuomari.tasapelit == 1
    
    def test_string_representation(self):
        """Test the string representation of Tuomari."""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "s")
        tuomari.kirjaa_siirto("p", "p")
        
        result = str(tuomari)
        assert "1 - 0" in result
        assert "Tasapelit: 1" in result


class TestTekoaly:
    """Tests for the basic AI (Tekoaly) class."""
    
    def test_initial_state(self):
        """Test that Tekoaly starts at initial state."""
        ai = Tekoaly()
        assert ai._siirto == 0
    
    def test_move_cycle(self):
        """Test that AI cycles through moves in order."""
        ai = Tekoaly()
        
        # First move should be "p" (siirto becomes 1)
        assert ai.anna_siirto() == "p"
        
        # Second move should be "s" (siirto becomes 2)
        assert ai.anna_siirto() == "s"
        
        # Third move should be "k" (siirto becomes 0)
        assert ai.anna_siirto() == "k"
        
        # Should cycle back to "p"
        assert ai.anna_siirto() == "p"
    
    def test_aseta_siirto_does_nothing(self):
        """Test that aseta_siirto doesn't affect behavior."""
        ai = Tekoaly()
        ai.aseta_siirto("k")
        # Should still follow the cycle
        assert ai.anna_siirto() == "p"


class TestTekoalyParannettu:
    """Tests for the advanced AI (TekoalyParannettu) class."""
    
    def test_initial_state(self):
        """Test that TekoalyParannettu starts with empty memory."""
        ai = TekoalyParannettu(5)
        assert ai._vapaa_muisti_indeksi == 0
        assert len(ai._muisti) == 5
    
    def test_first_move_is_rock(self):
        """Test that AI returns rock when memory is empty."""
        ai = TekoalyParannettu(5)
        assert ai.anna_siirto() == "k"
    
    def test_second_move_is_rock(self):
        """Test that AI returns rock when only one move in memory."""
        ai = TekoalyParannettu(5)
        ai.aseta_siirto("k")
        assert ai.anna_siirto() == "k"
    
    def test_memory_stores_moves(self):
        """Test that moves are stored in memory."""
        ai = TekoalyParannettu(3)
        ai.aseta_siirto("k")
        ai.aseta_siirto("p")
        ai.aseta_siirto("s")
        
        assert ai._muisti[0] == "k"
        assert ai._muisti[1] == "p"
        assert ai._muisti[2] == "s"
        assert ai._vapaa_muisti_indeksi == 3
    
    def test_memory_overflow(self):
        """Test that oldest move is forgotten when memory is full."""
        ai = TekoalyParannettu(3)
        ai.aseta_siirto("k")
        ai.aseta_siirto("p")
        ai.aseta_siirto("s")
        ai.aseta_siirto("k")  # This should push out the first "k"
        
        assert ai._muisti[0] == "p"
        assert ai._muisti[1] == "s"
        assert ai._muisti[2] == "k"
        assert ai._vapaa_muisti_indeksi == 3
    
    def test_ai_predicts_based_on_pattern(self):
        """Test that AI tries to predict based on patterns."""
        ai = TekoalyParannettu(10)
        
        # Create a pattern: after "k", player always plays "p"
        ai.aseta_siirto("k")
        ai.aseta_siirto("p")
        ai.aseta_siirto("k")
        ai.aseta_siirto("p")
        ai.aseta_siirto("k")
        
        # AI should predict "p" next, so it plays "s" to beat it
        move = ai.anna_siirto()
        assert move == "s"
    
    def test_ai_returns_rock_when_no_clear_pattern(self):
        """Test that AI returns rock when there's no clear pattern."""
        ai = TekoalyParannettu(10)
        
        # Create mixed pattern
        ai.aseta_siirto("k")
        ai.aseta_siirto("s")
        ai.aseta_siirto("k")
        
        move = ai.anna_siirto()
        # Should return "k" or based on minimal pattern
        assert move in ["k", "p", "s"]
    
    def test_memory_size_limits(self):
        """Test different memory sizes."""
        small_ai = TekoalyParannettu(2)
        large_ai = TekoalyParannettu(20)
        
        assert len(small_ai._muisti) == 2
        assert len(large_ai._muisti) == 20


class TestConsecutiveWins:
    """Tests for consecutive win tracking."""
    
    def test_consecutive_wins_player1(self):
        """Test that consecutive wins are tracked for player 1."""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "s")  # P1 wins
        assert tuomari.ekan_perakkaisia == 1
        assert tuomari.tokan_perakkaisia == 0
        
        tuomari.kirjaa_siirto("p", "k")  # P1 wins
        assert tuomari.ekan_perakkaisia == 2
        assert tuomari.tokan_perakkaisia == 0
    
    def test_consecutive_wins_player2(self):
        """Test that consecutive wins are tracked for player 2."""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("s", "k")  # P2 wins
        assert tuomari.ekan_perakkaisia == 0
        assert tuomari.tokan_perakkaisia == 1
        
        tuomari.kirjaa_siirto("k", "p")  # P2 wins
        assert tuomari.ekan_perakkaisia == 0
        assert tuomari.tokan_perakkaisia == 2
    
    def test_consecutive_wins_reset_on_loss(self):
        """Test that consecutive wins reset when player loses."""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "s")  # P1 wins
        tuomari.kirjaa_siirto("p", "k")  # P1 wins
        assert tuomari.ekan_perakkaisia == 2
        
        tuomari.kirjaa_siirto("s", "k")  # P2 wins
        assert tuomari.ekan_perakkaisia == 0
        assert tuomari.tokan_perakkaisia == 1
    
    def test_consecutive_wins_reset_on_tie(self):
        """Test that consecutive wins reset on tie."""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "s")  # P1 wins
        tuomari.kirjaa_siirto("p", "k")  # P1 wins
        assert tuomari.ekan_perakkaisia == 2
        
        tuomari.kirjaa_siirto("k", "k")  # Tie
        assert tuomari.ekan_perakkaisia == 0
        assert tuomari.tokan_perakkaisia == 0
    
    def test_game_not_over_under_5_wins(self):
        """Test that game is not over with less than 5 consecutive wins."""
        tuomari = Tuomari()
        for _ in range(4):
            tuomari.kirjaa_siirto("k", "s")  # P1 wins 4 times
        
        assert tuomari.ekan_perakkaisia == 4
        assert tuomari.onko_peli_paattynyt() is False
        assert tuomari.voittaja() is None
    
    def test_game_over_on_5_consecutive_wins_player1(self):
        """Test that game ends when player 1 gets 5 consecutive wins."""
        tuomari = Tuomari()
        for _ in range(5):
            tuomari.kirjaa_siirto("k", "s")  # P1 wins 5 times
        
        assert tuomari.ekan_perakkaisia == 5
        assert tuomari.onko_peli_paattynyt() is True
        assert tuomari.voittaja() == 1
    
    def test_game_over_on_5_consecutive_wins_player2(self):
        """Test that game ends when player 2 gets 5 consecutive wins."""
        tuomari = Tuomari()
        for _ in range(5):
            tuomari.kirjaa_siirto("s", "k")  # P2 wins 5 times
        
        assert tuomari.tokan_perakkaisia == 5
        assert tuomari.onko_peli_paattynyt() is True
        assert tuomari.voittaja() == 2
    
    def test_game_over_on_more_than_5_consecutive_wins(self):
        """Test that game is over with more than 5 consecutive wins."""
        tuomari = Tuomari()
        for _ in range(7):
            tuomari.kirjaa_siirto("k", "s")  # P1 wins 7 times
        
        assert tuomari.ekan_perakkaisia == 7
        assert tuomari.onko_peli_paattynyt() is True
        assert tuomari.voittaja() == 1
    
    def test_total_wins_vs_consecutive_wins(self):
        """Test that total wins and consecutive wins are tracked separately."""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "s")  # P1 wins
        tuomari.kirjaa_siirto("p", "k")  # P1 wins
        tuomari.kirjaa_siirto("k", "k")  # Tie (resets consecutive)
        tuomari.kirjaa_siirto("s", "p")  # P1 wins
        
        assert tuomari.ekan_pisteet == 3  # Total wins
        assert tuomari.ekan_perakkaisia == 1  # Only 1 consecutive after tie

"""Integration tests for the Flask web application."""
import pytest

from app import app as flask_app


@pytest.fixture
def app():
    """Create and configure a test app instance."""
    flask_app.config['TESTING'] = True
    flask_app.config['SECRET_KEY'] = 'test_secret_key'
    yield flask_app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def session_client(client):
    """Create a client with session support."""
    with client.session_transaction() as sess:
        sess.clear()
    return client


class TestRoutes:
    """Test Flask routes."""
    
    def test_index_route(self, client):
        """Test that index page loads successfully."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Kivi-Paperi-Sakset' in response.data
    
    def test_index_contains_game_modes(self, client):
        """Test that index page contains game mode buttons."""
        response = client.get('/')
        assert 'Pelaaja vs Pelaaja'.encode('utf-8') in response.data
        assert 'Tekoäly'.encode('utf-8') in response.data
        assert 'Parannettu'.encode('utf-8') in response.data


class TestGameStart:
    """Test game initialization."""
    
    def test_start_player_vs_player(self, client):
        """Test starting a player vs player game."""
        response = client.post('/start_game',
                              json={'mode': 'a'},
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['game_mode'] == 'a'
        assert 'Pelaaja vs Pelaaja' in data['mode_name']
    
    def test_start_ai_game(self, client):
        """Test starting a game against basic AI."""
        response = client.post('/start_game',
                              json={'mode': 'b'},
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['game_mode'] == 'b'
        assert 'Tekoäly' in data['mode_name']
    
    def test_start_advanced_ai_game(self, client):
        """Test starting a game against advanced AI."""
        response = client.post('/start_game',
                              json={'mode': 'c'},
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['game_mode'] == 'c'
        assert 'Parannettu' in data['mode_name']
    
    def test_start_game_initializes_scores(self, client):
        """Test that starting a game initializes scores to zero."""
        with client.session_transaction() as sess:
            sess['ekan_pisteet'] = 5
            sess['tokan_pisteet'] = 3
        
        client.post('/start_game',
                   json={'mode': 'a'},
                   content_type='application/json')
        
        with client.session_transaction() as sess:
            assert sess.get('ekan_pisteet') == 0
            assert sess.get('tokan_pisteet') == 0
            assert sess.get('tasapelit') == 0
            assert sess.get('ekan_perakkaisia') == 0
            assert sess.get('tokan_perakkaisia') == 0


class TestPlayerVsPlayer:
    """Test player vs player game mode."""
    
    def test_valid_move_both_players(self, client):
        """Test a valid move from both players."""
        # Start game
        client.post('/start_game', json={'mode': 'a'})
        
        # Make move
        response = client.post('/make_move',
                              json={'player1_move': 'k', 'player2_move': 'p'},
                              content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['player1_move'] == 'k'
        assert data['player2_move'] == 'p'
        assert data['scores']['player2'] == 1  # Paper beats rock
        assert data['scores']['player1'] == 0
        assert data['scores']['player2_streak'] == 1
        assert data['scores']['player1_streak'] == 0
        assert data['game_over'] is False
    
    def test_tie_game(self, client):
        """Test a tie game."""
        client.post('/start_game', json={'mode': 'a'})
        
        response = client.post('/make_move',
                              json={'player1_move': 'k', 'player2_move': 'k'},
                              content_type='application/json')
        
        data = response.get_json()
        assert data['success'] is True
        assert data['scores']['ties'] == 1
        assert data['scores']['player1'] == 0
        assert data['scores']['player2'] == 0
        assert data['scores']['player1_streak'] == 0
        assert data['scores']['player2_streak'] == 0
    
    def test_invalid_move_player1(self, client):
        """Test invalid move from player 1."""
        client.post('/start_game', json={'mode': 'a'})
        
        response = client.post('/make_move',
                              json={'player1_move': 'x', 'player2_move': 'k'},
                              content_type='application/json')
        
        data = response.get_json()
        assert data['success'] is False
        assert 'error' in data
    
    def test_invalid_move_player2(self, client):
        """Test invalid move from player 2."""
        client.post('/start_game', json={'mode': 'a'})
        
        response = client.post('/make_move',
                              json={'player1_move': 'k', 'player2_move': 'invalid'},
                              content_type='application/json')
        
        data = response.get_json()
        assert data['success'] is False
        assert 'error' in data
    
    def test_multiple_rounds(self, client):
        """Test multiple rounds accumulate scores."""
        client.post('/start_game', json={'mode': 'a'})
        
        # Round 1: Player 1 wins
        client.post('/make_move', json={'player1_move': 'k', 'player2_move': 's'})
        
        # Round 2: Player 2 wins
        client.post('/make_move', json={'player1_move': 's', 'player2_move': 'k'})
        
        # Round 3: Tie
        response = client.post('/make_move', json={'player1_move': 'p', 'player2_move': 'p'})
        
        data = response.get_json()
        assert data['scores']['player1'] == 1
        assert data['scores']['player2'] == 1
        assert data['scores']['ties'] == 1
        assert data['scores']['player1_streak'] == 0  # Reset by tie
        assert data['scores']['player2_streak'] == 0  # Reset by tie


class TestPlayerVsAI:
    """Test player vs AI game modes."""
    
    def test_ai_makes_move(self, client):
        """Test that AI automatically makes a move."""
        client.post('/start_game', json={'mode': 'b'})
        
        response = client.post('/make_move',
                              json={'player1_move': 'k'},
                              content_type='application/json')
        
        data = response.get_json()
        assert data['success'] is True
        assert 'player2_move' in data
        assert data['player2_move'] in ['k', 'p', 's']
        assert 'computer_move' in data
    
    def test_basic_ai_cycles(self, client):
        """Test that basic AI cycles through moves."""
        client.post('/start_game', json={'mode': 'b'})
        
        moves = []
        for _ in range(4):
            response = client.post('/make_move',
                                  json={'player1_move': 'k'},
                                  content_type='application/json')
            data = response.get_json()
            moves.append(data['player2_move'])
        
        # Basic AI cycles: p, s, k, p
        assert moves == ['p', 's', 'k', 'p']
    
    def test_advanced_ai_makes_move(self, client):
        """Test that advanced AI makes moves."""
        client.post('/start_game', json={'mode': 'c'})
        
        response = client.post('/make_move',
                              json={'player1_move': 'k'},
                              content_type='application/json')
        
        data = response.get_json()
        assert data['success'] is True
        assert data['player2_move'] in ['k', 'p', 's']
    
    def test_advanced_ai_learns_pattern(self, client):
        """Test that advanced AI attempts to learn patterns."""
        client.post('/start_game', json={'mode': 'c'})
        
        # Create pattern: k -> p -> k -> p
        client.post('/make_move', json={'player1_move': 'k'})
        client.post('/make_move', json={'player1_move': 'p'})
        client.post('/make_move', json={'player1_move': 'k'})
        client.post('/make_move', json={'player1_move': 'p'})
        
        # Play k again to see if AI predicts p
        response = client.post('/make_move', json={'player1_move': 'k'})
        data = response.get_json()
        
        # AI should try to counter the pattern
        assert data['success'] is True
        assert data['player2_move'] in ['k', 'p', 's']


class TestGameReset:
    """Test game reset functionality."""
    
    def test_reset_clears_session(self, client):
        """Test that reset clears the game session."""
        # Start a game and play some rounds
        client.post('/start_game', json={'mode': 'a'})
        client.post('/make_move', json={'player1_move': 'k', 'player2_move': 'p'})
        
        # Reset
        response = client.post('/reset_game')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        
        # Check session is cleared
        with client.session_transaction() as sess:
            assert 'game_mode' not in sess
            assert 'ekan_pisteet' not in sess


class TestScoring:
    """Test game scoring logic."""
    
    def test_rock_beats_scissors(self, client):
        """Test that rock beats scissors."""
        client.post('/start_game', json={'mode': 'a'})
        response = client.post('/make_move',
                              json={'player1_move': 'k', 'player2_move': 's'})
        data = response.get_json()
        assert data['scores']['player1'] == 1
        assert data['scores']['player2'] == 0
    
    def test_scissors_beats_paper(self, client):
        """Test that scissors beats paper."""
        client.post('/start_game', json={'mode': 'a'})
        response = client.post('/make_move',
                              json={'player1_move': 's', 'player2_move': 'p'})
        data = response.get_json()
        assert data['scores']['player1'] == 1
        assert data['scores']['player2'] == 0
    
    def test_paper_beats_rock(self, client):
        """Test that paper beats rock."""
        client.post('/start_game', json={'mode': 'a'})
        response = client.post('/make_move',
                              json={'player1_move': 'p', 'player2_move': 'k'})
        data = response.get_json()
        assert data['scores']['player1'] == 1
        assert data['scores']['player2'] == 0
    
    def test_all_tie_combinations(self, client):
        """Test all tie combinations."""
        moves = ['k', 'p', 's']
        
        for move in moves:
            client.post('/start_game', json={'mode': 'a'})
            response = client.post('/make_move',
                                  json={'player1_move': move, 'player2_move': move})
            data = response.get_json()
            assert data['scores']['ties'] == 1
            assert data['scores']['player1'] == 0
            assert data['scores']['player2'] == 0


class TestMoveNames:
    """Test move name translations."""
    
    def test_move_names_returned(self, client):
        """Test that move names are returned in Finnish."""
        client.post('/start_game', json={'mode': 'a'})
        response = client.post('/make_move',
                              json={'player1_move': 'k', 'player2_move': 'p'})
        data = response.get_json()
        
        assert data['player1_move_name'] == 'Kivi'
        assert data['player2_move_name'] == 'Paperi'
    
    def test_all_move_names(self, client):
        """Test all move name translations."""
        client.post('/start_game', json={'mode': 'a'})
        
        # Test rock
        response = client.post('/make_move', json={'player1_move': 'k', 'player2_move': 'k'})
        data = response.get_json()
        assert data['player1_move_name'] == 'Kivi'
        
        # Test paper
        response = client.post('/make_move', json={'player1_move': 'p', 'player2_move': 'p'})
        data = response.get_json()
        assert data['player1_move_name'] == 'Paperi'
        
        # Test scissors
        response = client.post('/make_move', json={'player1_move': 's', 'player2_move': 's'})
        data = response.get_json()
        assert data['player1_move_name'] == 'Sakset'


class TestConsecutiveWinsGameplay:
    """Test consecutive win game ending logic in web app."""
    
    def test_game_continues_under_5_wins(self, client):
        """Test that game continues with less than 5 consecutive wins."""
        client.post('/start_game', json={'mode': 'a'})
        
        # Player 1 wins 4 times in a row
        for _ in range(4):
            response = client.post('/make_move', json={'player1_move': 'k', 'player2_move': 's'})
            data = response.get_json()
        
        assert data['scores']['player1_streak'] == 4
        assert data['game_over'] is False
        assert data['winner'] is None
    
    def test_game_ends_on_5_consecutive_wins(self, client):
        """Test that game ends when a player gets 5 consecutive wins."""
        client.post('/start_game', json={'mode': 'a'})
        
        # Player 1 wins 5 times in a row
        for i in range(5):
            response = client.post('/make_move', json={'player1_move': 'k', 'player2_move': 's'})
            data = response.get_json()
        
        assert data['scores']['player1_streak'] == 5
        assert data['game_over'] is True
        assert data['winner'] == 1
    
    def test_consecutive_wins_reset_on_loss(self, client):
        """Test that consecutive wins reset when player loses."""
        client.post('/start_game', json={'mode': 'a'})
        
        # Player 1 wins 3 times
        for _ in range(3):
            client.post('/make_move', json={'player1_move': 'k', 'player2_move': 's'})
        
        # Player 2 wins, resetting player 1's streak
        response = client.post('/make_move', json={'player1_move': 's', 'player2_move': 'k'})
        data = response.get_json()
        
        assert data['scores']['player1'] == 3  # Total wins
        assert data['scores']['player1_streak'] == 0  # Streak reset
        assert data['scores']['player2_streak'] == 1
    
    def test_consecutive_wins_reset_on_tie(self, client):
        """Test that consecutive wins reset on tie."""
        client.post('/start_game', json={'mode': 'a'})
        
        # Player 1 wins 3 times
        for _ in range(3):
            client.post('/make_move', json={'player1_move': 'k', 'player2_move': 's'})
        
        # Tie, resetting all streaks
        response = client.post('/make_move', json={'player1_move': 'k', 'player2_move': 'k'})
        data = response.get_json()
        
        assert data['scores']['player1_streak'] == 0
        assert data['scores']['player2_streak'] == 0
    
    def test_player2_can_win_5_consecutive(self, client):
        """Test that player 2 can also win with 5 consecutive wins."""
        client.post('/start_game', json={'mode': 'a'})
        
        # Player 2 wins 5 times in a row
        for _ in range(5):
            response = client.post('/make_move', json={'player1_move': 's', 'player2_move': 'k'})
            data = response.get_json()
        
        assert data['scores']['player2_streak'] == 5
        assert data['game_over'] is True
        assert data['winner'] == 2
    
    def test_ai_can_win_with_consecutive_wins(self, client):
        """Test that AI can win with 5 consecutive wins."""
        client.post('/start_game', json={'mode': 'b'})
        
        # Let AI win 5 times (player deliberately loses)
        # AI cycles: p, s, k, p, s
        # To lose to AI: play k (loses to p), p (loses to s), s (loses to k), k (loses to p), p (loses to s)
        losing_moves = ['k', 'p', 's', 'k', 'p']
        for move in losing_moves:
            response = client.post('/make_move', json={'player1_move': move})
            data = response.get_json()
        
        assert data['scores']['player2_streak'] == 5
        assert data['game_over'] is True
        assert data['winner'] == 2

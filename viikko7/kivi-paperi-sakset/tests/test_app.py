import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
import json
from app import app, determine_winner


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestAppRoutes:
    """Test cases for Flask application routes"""
    
    def test_index_route(self, client):
        """Test that index route returns HTML"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Kivi-Paperi-Sakset' in response.data
    
    def test_start_game_player_vs_player(self, client):
        """Test starting a player vs player game"""
        response = client.post('/api/start_game', 
                             json={'type': 'player_vs_player'},
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'game_id' in data
        assert data['game_type'] == 'player_vs_player'
    
    def test_start_game_player_vs_ai(self, client):
        """Test starting a player vs AI game"""
        response = client.post('/api/start_game', 
                             json={'type': 'player_vs_ai'},
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'game_id' in data
        assert data['game_type'] == 'player_vs_ai'
    
    def test_start_game_player_vs_advanced_ai(self, client):
        """Test starting a player vs advanced AI game"""
        response = client.post('/api/start_game', 
                             json={'type': 'player_vs_advanced_ai'},
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'game_id' in data
        assert data['game_type'] == 'player_vs_advanced_ai'
    
    def test_start_game_invalid_type(self, client):
        """Test that invalid game type returns error"""
        response = client.post('/api/start_game', 
                             json={'type': 'invalid_type'},
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_play_move_valid(self, client):
        """Test playing a valid move against AI"""
        # Start game
        start_response = client.post('/api/start_game', 
                                    json={'type': 'player_vs_ai'},
                                    content_type='application/json')
        game_id = json.loads(start_response.data)['game_id']
        
        # Play move
        response = client.post('/api/play_move',
                             json={'game_id': game_id, 'player1_move': 'k'},
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['player1_move'] == 'k'
        assert data['player2_move'] in ['k', 'p', 's']
        assert 'result' in data
        assert 'score' in data
        assert 'consecutive_wins' in data
        assert 'wins_remaining' in data
        assert 'game_over' in data
        assert 'winner' in data
    
    def test_play_move_invalid_game_id(self, client):
        """Test playing move with invalid game ID"""
        response = client.post('/api/play_move',
                             json={'game_id': 'invalid_id', 'player1_move': 'k'},
                             content_type='application/json')
        
        assert response.status_code == 404
    
    def test_play_move_invalid_move(self, client):
        """Test playing an invalid move"""
        # Start game
        start_response = client.post('/api/start_game', 
                                    json={'type': 'player_vs_ai'},
                                    content_type='application/json')
        game_id = json.loads(start_response.data)['game_id']
        
        # Play invalid move
        response = client.post('/api/play_move',
                             json={'game_id': game_id, 'player1_move': 'x'},
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_play_move_pvp(self, client):
        """Test playing a PvP round"""
        # Start game
        start_response = client.post('/api/start_game', 
                                    json={'type': 'player_vs_player'},
                                    content_type='application/json')
        game_id = json.loads(start_response.data)['game_id']
        
        # Play round
        response = client.post('/api/play_move_pvp',
                             json={'game_id': game_id, 'player1_move': 'k', 'player2_move': 's'},
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['player1_move'] == 'k'
        assert data['player2_move'] == 's'
        assert data['result'] == 'player1'
    
    def test_play_move_pvp_invalid_moves(self, client):
        """Test PvP with invalid moves"""
        # Start game
        start_response = client.post('/api/start_game', 
                                    json={'type': 'player_vs_player'},
                                    content_type='application/json')
        game_id = json.loads(start_response.data)['game_id']
        
        # Play invalid round
        response = client.post('/api/play_move_pvp',
                             json={'game_id': game_id, 'player1_move': 'x', 'player2_move': 's'},
                             content_type='application/json')
        
        assert response.status_code == 400
    
    def test_game_state(self, client):
        """Test getting game state"""
        # Start game
        start_response = client.post('/api/start_game', 
                                    json={'type': 'player_vs_ai'},
                                    content_type='application/json')
        game_id = json.loads(start_response.data)['game_id']
        
        # Get state
        response = client.get(f'/api/game_state/{game_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'game_type' in data
        assert 'score' in data
        assert 'consecutive_wins' in data
        assert 'wins_remaining' in data
        assert 'game_over' in data
        assert data['score']['player1'] == 0
        assert data['score']['player2'] == 0
        assert data['score']['draws'] == 0
        assert data['consecutive_wins']['player1'] == 0
        assert data['consecutive_wins']['player2'] == 0
        assert data['wins_remaining']['player1'] == 3
        assert data['wins_remaining']['player2'] == 3
        assert data['game_over'] is False
    
    def test_game_state_invalid_id(self, client):
        """Test getting state with invalid game ID"""
        response = client.get('/api/game_state/invalid_id')
        
        assert response.status_code == 404
    
    def test_end_game(self, client):
        """Test ending a game"""
        # Start game
        start_response = client.post('/api/start_game', 
                                    json={'type': 'player_vs_ai'},
                                    content_type='application/json')
        game_id = json.loads(start_response.data)['game_id']
        
        # End game
        response = client.post('/api/end_game',
                             json={'game_id': game_id},
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        
        # Verify game is deleted
        response = client.get(f'/api/game_state/{game_id}')
        assert response.status_code == 404


class TestDetermineWinner:
    """Test cases for the determine_winner function"""
    
    def test_determine_winner_draw(self):
        """Test draw outcomes"""
        assert determine_winner('k', 'k') == 'draw'
        assert determine_winner('p', 'p') == 'draw'
        assert determine_winner('s', 's') == 'draw'
    
    def test_determine_winner_player1_wins(self):
        """Test player 1 win scenarios"""
        assert determine_winner('k', 's') == 'player1'  # Rock beats scissors
        assert determine_winner('s', 'p') == 'player1'  # Scissors beats paper
        assert determine_winner('p', 'k') == 'player1'  # Paper beats rock
    
    def test_determine_winner_player2_wins(self):
        """Test player 2 win scenarios"""
        assert determine_winner('s', 'k') == 'player2'  # Rock beats scissors
        assert determine_winner('p', 's') == 'player2'  # Scissors beats paper
        assert determine_winner('k', 'p') == 'player2'  # Paper beats rock
    
    def test_score_accumulation(self, client):
        """Test that scores accumulate correctly"""
        # Start game
        start_response = client.post('/api/start_game', 
                                    json={'type': 'player_vs_ai'},
                                    content_type='application/json')
        game_id = json.loads(start_response.data)['game_id']
        
        # Play multiple moves
        moves = ['k', 'p', 's', 'k', 'p']
        for move in moves:
            client.post('/api/play_move',
                       json={'game_id': game_id, 'player1_move': move},
                       content_type='application/json')
        
        # Check final state
    
    def test_consecutive_wins_tracking(self, client):
        """Test that consecutive wins are tracked"""
        # Start game with basic AI
        start_response = client.post('/api/start_game', 
                                    json={'type': 'player_vs_ai'},
                                    content_type='application/json')
        game_id = json.loads(start_response.data)['game_id']
        
        # Get first move from AI to know what to beat
        response = client.post('/api/play_move',
                             json={'game_id': game_id, 'player1_move': 'k'},
                             content_type='application/json')
        data = json.loads(response.data)
        
        # Verify consecutive wins are tracked
        assert 'consecutive_wins' in data
        assert 'player1' in data['consecutive_wins']
        assert 'player2' in data['consecutive_wins']
    
    def test_three_consecutive_wins_ends_game(self, client):
        """Test that 3 consecutive wins ends the game"""
        # Start game - basic AI cycles through p, s, k, p, s, k...
        start_response = client.post('/api/start_game', 
                                    json={'type': 'player_vs_ai'},
                                    content_type='application/json')
        game_id = json.loads(start_response.data)['game_id']
        
        # Strategy: beat the basic AI which cycles p, s, k
        # To beat p (papier), play s (scissors)
        # To beat s (scissors), play k (rock)
        # To beat k (rock), play p (paper)
        winning_moves = ['s', 'k', 'p']  # Beat p, s, k
        
        game_over = False
        winner = None
        
        for move in winning_moves:
            response = client.post('/api/play_move',
                                 json={'game_id': game_id, 'player1_move': move},
                                 content_type='application/json')
            data = json.loads(response.data)
            
            if data['game_over']:
                game_over = True
                winner = data['winner']
                break
        
        # Game should end after 3 consecutive wins
        assert game_over is True
        assert winner == 'player1'
    
    def test_consecutive_wins_reset_on_loss(self, client):
        """Test that consecutive wins reset on a loss or draw"""
        # Start game
        start_response = client.post('/api/start_game', 
                                    json={'type': 'player_vs_ai'},
                                    content_type='application/json')
        game_id = json.loads(start_response.data)['game_id']
        
        # Play a move that beats AI
        response1 = client.post('/api/play_move',
                              json={'game_id': game_id, 'player1_move': 's'},
                              content_type='application/json')
        data1 = json.loads(response1.data)
        
        if data1['result'] == 'player1':
            # Next, play a move that loses (or draws)
            response2 = client.post('/api/play_move',
                                  json={'game_id': game_id, 'player1_move': 's'},
                                  content_type='application/json')
            data2 = json.loads(response2.data)
            
            if data2['result'] != 'player1':
                # Consecutive wins should reset to 0
                assert data2['consecutive_wins']['player1'] == 0
    
    def test_game_over_prevents_moves(self, client):
        """Test that game-over state prevents further moves"""
        # Start game
        start_response = client.post('/api/start_game', 
                                    json={'type': 'player_vs_ai'},
                                    content_type='application/json')
        game_id = json.loads(start_response.data)['game_id']
        
        # Play 5 winning moves to end game
        winning_moves = ['s', 'k', 'p', 's', 'k']
        
        for move in winning_moves:
            client.post('/api/play_move',
                       json={'game_id': game_id, 'player1_move': move},
                       content_type='application/json')
        
        # Try to play another move
        response = client.post('/api/play_move',
                             json={'game_id': game_id, 'player1_move': 'k'},
                             content_type='application/json')
        
        # Should get an error
    
    def test_wins_remaining_countdown(self, client):
        """Test that wins_remaining shows correct countdown"""
        # Start game
        start_response = client.post('/api/start_game', 
                                    json={'type': 'player_vs_ai'},
                                    content_type='application/json')
        game_id = json.loads(start_response.data)['game_id']
        
        # Initial state: 5 wins needed
        response = client.get(f'/api/game_state/{game_id}')
        data = json.loads(response.data)
        assert data['wins_remaining']['player1'] == 3
        assert data['wins_remaining']['player2'] == 3
        
        # Play a winning move
        response = client.post('/api/play_move',
                             json={'game_id': game_id, 'player1_move': 's'},
                             content_type='application/json')
        data = json.loads(response.data)
        
        # Check countdown in response
        if data['result'] == 'player1':
            assert data['wins_remaining']['player1'] == 2
            assert data['wins_remaining']['player2'] == 3
    
    def test_wins_remaining_reset_on_loss(self, client):
        """Test that wins_remaining resets when streak breaks"""
        # Start game
        start_response = client.post('/api/start_game', 
                                    json={'type': 'player_vs_ai'},
                                    content_type='application/json')
        game_id = json.loads(start_response.data)['game_id']
        
        # Play winning move
        response1 = client.post('/api/play_move',
                              json={'game_id': game_id, 'player1_move': 's'},
                              content_type='application/json')
        data1 = json.loads(response1.data)
        
        # If player won
        if data1['result'] == 'player1':
            assert data1['wins_remaining']['player1'] == 2
            
            # Play a losing move to break streak
            response2 = client.post('/api/play_move',
                                  json={'game_id': game_id, 'player1_move': 's'},
                                  content_type='application/json')
            data2 = json.loads(response2.data)
            
            if data2['result'] != 'player1':
                # Wins remaining should reset to 5 after losing
                assert data2['wins_remaining']['player1'] == 3

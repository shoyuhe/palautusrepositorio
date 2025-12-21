from flask import Flask, render_template, request, jsonify, session
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from kps import KPSPelaajaVsPelaaja, KPSPelaajaVsTekoaly, luo_peli
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu
from tuomari import Tuomari
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store game instances in session
games = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start_game', methods=['POST'])
def start_game():
    data = request.json
    game_type = data.get('type')  # 'player_vs_player', 'player_vs_ai', 'player_vs_advanced_ai'
    
    game_id = secrets.token_hex(8)
    
    if game_type == 'player_vs_player':
        peli = KPSPelaajaVsPelaaja()
    elif game_type == 'player_vs_ai':
        peli = KPSPelaajaVsTekoaly(Tekoaly())
    elif game_type == 'player_vs_advanced_ai':
        peli = KPSPelaajaVsTekoaly(TekoalyParannettu(10))
    else:
        return jsonify({'error': 'Invalid game type'}), 400
    
    # Initialize game state
    peli.tuomari = Tuomari()
    peli.game_type = game_type
    peli.player1_consecutive_wins = 0
    peli.player2_consecutive_wins = 0
    peli.game_over = False
    peli.winner = None
    
    games[game_id] = peli
    
    return jsonify({
        'game_id': game_id,
        'game_type': game_type
    })

@app.route('/api/play_move', methods=['POST'])
def play_move():
    data = request.json
    game_id = data.get('game_id')
    player1_move = data.get('player1_move')  # 'k', 'p', 's'
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    peli = games[game_id]
    
    # Check if game is already over
    if peli.game_over:
        return jsonify({'error': 'Game is already over'}), 400
    
    # Validate move
    valid_moves = ['k', 'p', 's']
    if player1_move not in valid_moves:
        return jsonify({'error': 'Invalid move. Use k (kivi), p (paperi), or s (sakset)'}), 400
    
    # Get player 2's move
    if peli.game_type == 'player_vs_player':
        # For player vs player, this would need to be passed
        return jsonify({'error': 'Player 2 move required'}), 400
    else:
        # AI players
        player2_move = peli.tekoaly.anna_siirto()
        peli.tekoaly.aseta_siirto(player1_move)
    
    # Record the move
    peli.tuomari.kirjaa_siirto(player1_move, player2_move)
    
    # Determine winner of this round
    result = determine_winner(player1_move, player2_move)
    
    # Update consecutive wins
    if result == 'player1':
        peli.player1_consecutive_wins += 1
        peli.player2_consecutive_wins = 0
    elif result == 'player2':
        peli.player2_consecutive_wins += 1
        peli.player1_consecutive_wins = 0
    else:  # draw
        peli.player1_consecutive_wins = 0
        peli.player2_consecutive_wins = 0
    
    # Check for 5 consecutive wins
    game_over = False
    winner = None
    if peli.player1_consecutive_wins >= 3:
        peli.game_over = True
        peli.winner = 'player1'
        game_over = True
        winner = 'player1'
    elif peli.player2_consecutive_wins >= 3:
        peli.game_over = True
        peli.winner = 'player2'
        game_over = True
        winner = 'player2'
    
    return jsonify({
        'player1_move': player1_move,
        'player2_move': player2_move,
        'result': result,
        'score': {
            'player1': peli.tuomari.ekan_pisteet,
            'player2': peli.tuomari.tokan_pisteet,
            'draws': peli.tuomari.tasapelit
        },
        'consecutive_wins': {
            'player1': peli.player1_consecutive_wins,
            'player2': peli.player2_consecutive_wins
        },
        'wins_remaining': {
            'player1': max(0, 3 - peli.player1_consecutive_wins),
            'player2': max(0, 3 - peli.player2_consecutive_wins)
        },
        'game_over': game_over,
        'winner': winner
    })

@app.route('/api/play_move_pvp', methods=['POST'])
def play_move_pvp():
    data = request.json
    game_id = data.get('game_id')
    player1_move = data.get('player1_move')
    player2_move = data.get('player2_move')
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    peli = games[game_id]
    
    # Check if game is already over
    if peli.game_over:
        return jsonify({'error': 'Game is already over'}), 400
    
    # Validate moves
    valid_moves = ['k', 'p', 's']
    if player1_move not in valid_moves or player2_move not in valid_moves:
        return jsonify({'error': 'Invalid move. Use k (kivi), p (paperi), or s (sakset)'}), 400
    
    # Record the move
    peli.tuomari.kirjaa_siirto(player1_move, player2_move)
    
    # Determine winner of this round
    result = determine_winner(player1_move, player2_move)
    
    # Update consecutive wins
    if result == 'player1':
        peli.player1_consecutive_wins += 1
        peli.player2_consecutive_wins = 0
    elif result == 'player2':
        peli.player2_consecutive_wins += 1
        peli.player1_consecutive_wins = 0
    else:  # draw
        peli.player1_consecutive_wins = 0
        peli.player2_consecutive_wins = 0
    
    # Check for 5 consecutive wins
    game_over = False
    winner = None
    if peli.player1_consecutive_wins >= 3:
        peli.game_over = True
        peli.winner = 'player1'
        game_over = True
        winner = 'player1'
    elif peli.player2_consecutive_wins >= 3:
        peli.game_over = True
        peli.winner = 'player2'
        game_over = True
        winner = 'player2'
    
    return jsonify({
        'player1_move': player1_move,
        'player2_move': player2_move,
        'result': result,
        'score': {
            'player1': peli.tuomari.ekan_pisteet,
            'player2': peli.tuomari.tokan_pisteet,
            'draws': peli.tuomari.tasapelit
        },
        'consecutive_wins': {
            'player1': peli.player1_consecutive_wins,
            'player2': peli.player2_consecutive_wins
        },
        'wins_remaining': {
            'player1': max(0, 3 - peli.player1_consecutive_wins),
            'player2': max(0, 3 - peli.player2_consecutive_wins)
        },
        'game_over': game_over,
        'winner': winner
    })

@app.route('/api/game_state/<game_id>', methods=['GET'])
def get_game_state(game_id):
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    peli = games[game_id]
    
    return jsonify({
        'game_type': peli.game_type,
        'score': {
            'player1': peli.tuomari.ekan_pisteet,
            'player2': peli.tuomari.tokan_pisteet,
            'draws': peli.tuomari.tasapelit
        },
        'consecutive_wins': {
            'player1': peli.player1_consecutive_wins,
            'player2': peli.player2_consecutive_wins
        },
        'wins_remaining': {
            'player1': max(0, 3 - peli.player1_consecutive_wins),
            'player2': max(0, 3 - peli.player2_consecutive_wins)
        },
        'game_over': peli.game_over,
        'winner': peli.winner
    })

def determine_winner(move1, move2):
    """Determine winner using the original game logic"""
    if move1 == move2:
        return 'draw'
    elif move1 == 'k' and move2 == 's':
        return 'player1'
    elif move1 == 's' and move2 == 'p':
        return 'player1'
    elif move1 == 'p' and move2 == 'k':
        return 'player1'
    else:
        return 'player2'

@app.route('/api/end_game', methods=['POST'])
def end_game():
    data = request.json
    game_id = data.get('game_id')
    
    if game_id in games:
        del games[game_id]
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)

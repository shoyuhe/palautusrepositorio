from flask import Flask, render_template, request, jsonify, session
import secrets
from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store game state in session
def get_tuomari():
    if 'ekan_pisteet' not in session:
        session['ekan_pisteet'] = 0
        session['tokan_pisteet'] = 0
        session['tasapelit'] = 0
        session['ekan_perakkaisia'] = 0
        session['tokan_perakkaisia'] = 0
    
    tuomari = Tuomari()
    tuomari.ekan_pisteet = session['ekan_pisteet']
    tuomari.tokan_pisteet = session['tokan_pisteet']
    tuomari.tasapelit = session['tasapelit']
    tuomari.ekan_perakkaisia = session['ekan_perakkaisia']
    tuomari.tokan_perakkaisia = session['tokan_perakkaisia']
    return tuomari

def save_tuomari(tuomari):
    session['ekan_pisteet'] = tuomari.ekan_pisteet
    session['tokan_pisteet'] = tuomari.tokan_pisteet
    session['tasapelit'] = tuomari.tasapelit
    session['ekan_perakkaisia'] = tuomari.ekan_perakkaisia
    session['tokan_perakkaisia'] = tuomari.tokan_perakkaisia

def get_tekoaly():
    game_mode = session.get('game_mode', 'b')
    
    if game_mode == 'b':
        if 'tekoaly_siirto' not in session:
            session['tekoaly_siirto'] = 0
        tekoaly = Tekoaly()
        tekoaly._siirto = session['tekoaly_siirto']
        return tekoaly
    elif game_mode == 'c':
        if 'tekoaly_muisti' not in session:
            session['tekoaly_muisti'] = [None] * 10
            session['tekoaly_vapaa_muisti_indeksi'] = 0
        tekoaly = TekoalyParannettu(10)
        tekoaly._muisti = session['tekoaly_muisti']
        tekoaly._vapaa_muisti_indeksi = session['tekoaly_vapaa_muisti_indeksi']
        return tekoaly
    return None

def save_tekoaly(tekoaly):
    game_mode = session.get('game_mode', 'b')
    
    if game_mode == 'b':
        session['tekoaly_siirto'] = tekoaly._siirto
    elif game_mode == 'c':
        session['tekoaly_muisti'] = tekoaly._muisti
        session['tekoaly_vapaa_muisti_indeksi'] = tekoaly._vapaa_muisti_indeksi

def onko_ok_siirto(siirto):
    return siirto in ["k", "p", "s"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    game_mode = data.get('mode', 'a')
    
    # Reset game state
    session.clear()
    session['game_mode'] = game_mode
    session['ekan_pisteet'] = 0
    session['tokan_pisteet'] = 0
    session['tasapelit'] = 0
    session['ekan_perakkaisia'] = 0
    session['tokan_perakkaisia'] = 0
    
    if game_mode == 'b':
        session['tekoaly_siirto'] = 0
    elif game_mode == 'c':
        session['tekoaly_muisti'] = [None] * 10
        session['tekoaly_vapaa_muisti_indeksi'] = 0
    
    mode_names = {
        'a': 'Pelaaja vs Pelaaja',
        'b': 'Pelaaja vs Tekoäly',
        'c': 'Pelaaja vs Parannettu Tekoäly'
    }
    
    return jsonify({
        'success': True,
        'game_mode': game_mode,
        'mode_name': mode_names.get(game_mode, 'Tuntematon')
    })

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    ekan_siirto = data.get('player1_move')
    tokan_siirto = data.get('player2_move')
    game_mode = session.get('game_mode', 'a')
    
    if not onko_ok_siirto(ekan_siirto):
        return jsonify({'success': False, 'error': 'Virheellinen siirto pelaaja 1'})
    
    # Get computer move if playing against AI
    computer_move = None
    if game_mode in ['b', 'c'] and tokan_siirto is None:
        tekoaly = get_tekoaly()
        tokan_siirto = tekoaly.anna_siirto()
        computer_move = tokan_siirto
        save_tekoaly(tekoaly)
    
    if not onko_ok_siirto(tokan_siirto):
        return jsonify({'success': False, 'error': 'Virheellinen siirto pelaaja 2'})
    
    # Update game state
    tuomari = get_tuomari()
    tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
    save_tuomari(tuomari)
    
    # For advanced AI, remember the player's move
    if game_mode == 'c':
        tekoaly = get_tekoaly()
        tekoaly.aseta_siirto(ekan_siirto)
        save_tekoaly(tekoaly)
    
    move_names = {
        'k': 'Kivi',
        'p': 'Paperi',
        's': 'Sakset'
    }
    
    return jsonify({
        'success': True,
        'player1_move': ekan_siirto,
        'player1_move_name': move_names[ekan_siirto],
        'player2_move': tokan_siirto,
        'player2_move_name': move_names[tokan_siirto],
        'computer_move': computer_move,
        'scores': {
            'player1': tuomari.ekan_pisteet,
            'player2': tuomari.tokan_pisteet,
            'ties': tuomari.tasapelit,
            'player1_streak': tuomari.ekan_perakkaisia,
            'player2_streak': tuomari.tokan_perakkaisia
        },
        'game_over': tuomari.onko_peli_paattynyt(),
        'winner': tuomari.voittaja()
    })

@app.route('/reset_game', methods=['POST'])
def reset_game():
    session.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)

let currentGameId = null;
let currentGameType = null;
let player1Move = null;
let player2Move = null;
let gameOver = false;

const moveEmojis = {
    'k': '✋ Kivi',
    'p': '📄 Paperi',
    's': '✂️ Sakset'
};

const moveNames = {
    'k': 'Kivi',
    'p': 'Paperi',
    's': 'Sakset'
};

function startGameType(gameType) {
    currentGameType = gameType;
    
    fetch('/api/start_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            type: gameType
        })
    })
    .then(response => response.json())
    .then(data => {
        currentGameId = data.game_id;
        
        // Hide menu and show game screen
        document.getElementById('menu-screen').classList.remove('active');
        document.getElementById('game-screen').classList.add('active');
        
        // Set player names and initialize game UI
        if (gameType === 'player_vs_player') {
            document.getElementById('player1-name').textContent = 'Pelaaja 1';
            document.getElementById('player2-name').textContent = 'Pelaaja 2';
            showGameMode('pvp');
        } else if (gameType === 'player_vs_ai') {
            document.getElementById('player1-name').textContent = 'Sinä';
            document.getElementById('player2-name').textContent = 'Tekoäly';
            showGameMode('ai');
        } else if (gameType === 'player_vs_advanced_ai') {
            document.getElementById('player1-name').textContent = 'Sinä';
            document.getElementById('player2-name').textContent = 'Parannettu Tekoäly';
            showGameMode('ai');
        }
        
        updateScore();
    });
}

function showGameMode(mode) {
    // Hide all game modes
    document.getElementById('pvp-game').classList.remove('active');
    document.getElementById('ai-game').classList.remove('active');
    
    // Show selected game mode
    if (mode === 'pvp') {
        document.getElementById('pvp-game').classList.add('active');
    } else if (mode === 'ai') {
        document.getElementById('ai-game').classList.add('active');
    }
    
    // Reset game content
    const gameContent = document.getElementById('game-content');
    gameContent.innerHTML = '';
    
    if (mode === 'pvp') {
        gameContent.appendChild(document.getElementById('pvp-game'));
    } else if (mode === 'ai') {
        gameContent.appendChild(document.getElementById('ai-game'));
    }
}

function setPlayer1Move(move) {
    player1Move = move;
    
    // Update button styles
    document.querySelectorAll('#pvp-game .player-section:first-child .move-btn').forEach(btn => {
        btn.classList.remove('selected');
        if (btn.dataset.move === move) {
            btn.classList.add('selected');
        }
    });
    
    // Check if both players have selected moves
    if (player1Move && player2Move) {
        document.getElementById('play-btn').style.display = 'inline-block';
    }
}

function setPlayer2Move(move) {
    player2Move = move;
    
    // Update button styles
    document.querySelectorAll('#pvp-game .player-section:last-child .move-btn').forEach(btn => {
        btn.classList.remove('selected');
        if (btn.dataset.move === move) {
            btn.classList.add('selected');
        }
    });
    
    // Check if both players have selected moves
    if (player1Move && player2Move) {
        document.getElementById('play-btn').style.display = 'inline-block';
    }
}

function playRoundPvP() {
    if (!player1Move || !player2Move) {
        alert('Molempien pelaajien on valittava siirto!');
        return;
    }
    
    fetch('/api/play_move_pvp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            game_id: currentGameId,
            player1_move: player1Move,
            player2_move: player2Move
        })
    })
    .then(response => response.json())
    .then(data => {
        // Show result
        showRoundResult(data);
        
        // Reset selections
        player1Move = null;
        player2Move = null;
        document.getElementById('play-btn').style.display = 'none';
        
        // Clear button selections
        document.querySelectorAll('#pvp-game .move-btn').forEach(btn => {
            btn.classList.remove('selected');
        });
        
        // Update score
        updateScore();
    });
}

function playMoveAI(move) {
    if (gameOver) {
        alert('Peli on jo päättynyt. Palaa päävalikkoon aloittaaksesi uuden pelin.');
        return;
    }
    
    fetch('/api/play_move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            game_id: currentGameId,
            player1_move: move
        })
    })
    .then(response => response.json())
    .then(data => {
        // Show result
        showRoundResult(data);
        
        // Update score
        updateScore();
    });
}

function showRoundResult(data) {
    const resultText = document.getElementById('last-round-text');
    const move1 = moveEmojis[data.player1_move];
    const move2 = moveEmojis[data.player2_move];
    
    let resultMessage = `Sinä: ${move1} | Vastustaja: ${move2} | `;
    
    if (data.result === 'draw') {
        resultMessage += '🤝 Tasapeli!';
    } else if (data.result === 'player1') {
        resultMessage += '🎉 Voitit kierroksen!';
    } else {
        resultMessage += '😢 Vastustaja voitti kierroksen.';
    }
    
    // Add consecutive wins info
    if (data.consecutive_wins) {
        resultMessage += `\n\nPerättäiset voitot: Sinä ${data.consecutive_wins.player1} - Vastustaja ${data.consecutive_wins.player2}`;
    }
    
    // Add countdown info
    if (data.wins_remaining) {
        const p1Remaining = data.wins_remaining.player1;
        const p2Remaining = data.wins_remaining.player2;
        resultMessage += `\nVoittoon tarvitaan: Sinä ${p1Remaining} - Vastustaja ${p2Remaining}`;
    }
    
    resultText.textContent = resultMessage;
    document.getElementById('last-round-info').style.display = 'block';
    
    // Check if game is over
    if (data.game_over) {
        gameOver = true;
        setTimeout(() => {
            if (data.winner === 'player1') {
                alert('🎉 Onneksi olkoon! Voitit pelin 3 peräkkäisellä voitolla!');
            } else {
                alert('😢 Peli päättyi! Vastustaja voitti 3 peräkkäisellä voitolla.');
            }
            endGame();
        }, 500);
    }
}

function updateScore() {
    fetch(`/api/game_state/${currentGameId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('player1-score').textContent = data.score.player1;
            document.getElementById('player2-score').textContent = data.score.player2;
            document.getElementById('draws-score').textContent = data.score.draws;
            
            // Update countdown
            if (data.wins_remaining) {
                const p1Remaining = data.wins_remaining.player1;
                const p2Remaining = data.wins_remaining.player2;
                
                document.getElementById('player1-countdown').textContent = 
                    `${p1Remaining} voitto${p1Remaining !== 1 ? 'a' : ''} jäljellä`;
                document.getElementById('player2-countdown').textContent = 
                    `${p2Remaining} voitto${p2Remaining !== 1 ? 'a' : ''} jäljellä`;
            }
        });
}

function endGame() {
    fetch('/api/end_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            game_id: currentGameId
        })
    })
    .then(() => {
        // Reset game variables
        currentGameId = null;
        currentGameType = null;
        player1Move = null;
        player2Move = null;
        
        // Return to menu
        document.getElementById('game-screen').classList.remove('active');
        document.getElementById('menu-screen').classList.add('active');
        
        // Clear last round info
        document.getElementById('last-round-info').style.display = 'none';
    });
}

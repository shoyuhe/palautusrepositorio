# Kivi-Paperi-Sakset Web Edition

A web-based implementation of the classic Rock-Paper-Scissors game with AI opponents, built with Flask and featuring the original game logic.

## Features

- **Three Game Modes:**
  - Player vs Player - Play against a friend on the same device
  - Player vs Basic AI - Challenge a basic AI that cycles through moves
  - Player vs Advanced AI - Face an improved AI that learns from your moves

- **Beautiful Web Interface:**
  - Modern, responsive design
  - Real-time score tracking
  - Round result display
  - Mobile-friendly layout

- **Original Game Logic:**
  - Uses the core Python game logic from the original command-line version
  - Fair game mechanics using the original `Tuomari` (Judge) class
  - AI implementations (`Tekoaly` and `TekoalyParannettu`) integrated seamlessly

## Project Structure

```
kivi-paperi-sakset/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── src/
│   ├── kps.py            # Game classes (original code)
│   ├── tuomari.py        # Score tracking (original code)
│   ├── tekoaly.py        # Basic AI (original code)
│   └── tekoaly_parannettu.py  # Advanced AI (original code)
├── templates/
│   └── index.html        # Main game page
└── static/
    ├── style.css         # Styling
    └── script.js         # Client-side game logic
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## How to Play

### Game Rules
- **Kivi (Rock)** beats **Sakset (Scissors)**
- **Sakset (Scissors)** beats **Paperi (Paper)**
- **Paperi (Paper)** beats **Kivi (Rock)**

### Player vs Player
1. Select "Ihmistä vastaan" (Play against Human)
2. Player 1 selects their move
3. Player 2 selects their move
4. Click "Pelaa kierros" (Play Round)
5. Results are displayed and score updated

### Player vs AI
1. Select "Tekoälyä vastaan" (Play against AI) or "Parannettua tekoälyä vastaan" (Play against Advanced AI)
2. Click a move button (Kivi, Paperi, or Sakset)
3. AI makes its move automatically
4. Round results are displayed
5. Repeat until you want to stop

## Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **Game Logic:** Original Python implementation

## Authors

- Original game logic: Matti Luukkainen
- Web adaptation: Sofia

## License

MIT

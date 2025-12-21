# Kivi-Paperi-Sakset - Testing Documentation

## Test Suite Overview

This project includes comprehensive automated tests for both the game logic and the web interface.

### Test Coverage

- **58 tests total** - All passing ✅
- **90% coverage** for the Flask web application ([src/app.py](src/app.py))
- **100% coverage** for core game logic:
  - [src/tuomari.py](src/tuomari.py) - Referee/scoring system with consecutive win tracking
  - [src/tekoaly.py](src/tekoaly.py) - Basic AI
  - [src/tekoaly_parannettu.py](src/tekoaly_parannettu.py) - Advanced AI with memory

## Game Rules

The game continues until one player achieves **5 consecutive wins**. Key features:
- Consecutive wins are tracked separately from total wins
- A tie resets both players' consecutive win counters to 0
- When a player loses, their consecutive win counter resets to 0
- The game automatically ends when a player reaches 5 consecutive wins

## Test Files

### [tests/test_game_logic.py](tests/test_game_logic.py)
Unit tests for core game logic classes:

- **TestTuomari** (12 tests)
  - Initial state with consecutive win counters
  - Tie games reset consecutive wins
  - Win conditions (rock beats scissors, scissors beats paper, paper beats rock)
  - Multiple rounds
  - String representation

- **TestTekoaly** (3 tests)
  - Initial state
  - Move cycling pattern
  - State persistence

- **TestTekoalyParannettu** (8 tests)
  - Initial state
  - Memory management
  - Pattern recognition
  - Memory overflow handling
  - AI prediction logic

- **TestConsecutiveWins** (11 tests)
  - Consecutive win tracking for both players
  - Reset on loss or tie
  - Game ending at 5 consecutive wins
  - Winner determination
  - Separation of total wins vs consecutive wins

### [tests/test_app.py](tests/test_app.py)
Integration tests for the Flask web application:

- **TestRoutes** (2 tests)
  - Index page loading
  - Game mode buttons presence

- **TestGameStart** (4 tests)
  - Starting player vs player games
  - Starting AI games (basic and advanced)
  - Score initialization

- **TestPlayerVsPlayer** (5 tests)
  - Valid moves
  - Tie games
  - Invalid move handling
  - Multiple rounds

- **TestPlayerVsAI** (4 tests)
  - AI move generation
  - Basic AI cycling behavior
  - Advanced AI learning patterns

- **TestGameReset** (1 test)
  - Session clearing

- **TestScoring** (4 tests)
  - All win condition combinations
  - Tie combinations

- **TestMoveNames** (2 tests)
  - Finnish move name translations

## Running Tests

### Run all tests
```bash
poetry run pytest
```

### Run with verbose output
```bash
poetry run pytest -v
```

### Run specific test file
```bash
poetry run pytest tests/test_game_logic.py
```

### Run specific test class
```bash
poetry run pytest tests/test_app.py::TestPlayerVsPlayer
```

### Run specific test
```bash
poetry run pytest tests/test_game_logic.py::TestTuomari::test_initial_state
```

### Run with coverage report
```bash
poetry run pytest --cov=src --cov-report=html
```
This generates an HTML coverage report in `htmlcov/index.html`

### Run with coverage in terminal
```bash
poetry run pytest --cov=src --cov-report=term-missing
```

## Test Configuration

Test configuration is defined in [pyproject.toml](pyproject.toml):

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --cov=src --cov-report=term-missing"
```

## Dependencies

Testing dependencies:
- `pytest` - Test framework
- `pytest-flask` - Flask testing utilities
- `pytest-cov` - Coverage reporting

## Continuous Testing

For development, you can use pytest's watch mode (requires pytest-watch):
```bash
poetry add --group dev pytest-watch
poetry run ptw
```

## Test Structure

```
tests/
├── conftest.py           # Pytest configuration and fixtures
├── test_game_logic.py    # Unit tests for game logic
└── test_app.py           # Integration tests for Flask app
```

## Writing New Tests

When adding new features, follow these patterns:

### Unit Tests
```python
class TestNewFeature:
    def test_feature_behavior(self):
        # Arrange
        obj = SomeClass()
        
        # Act
        result = obj.some_method()
        
        # Assert
        assert result == expected_value
```

### Integration Tests
```python
class TestNewEndpoint:
    def test_endpoint_response(self, client):
        # Make request
        response = client.post('/endpoint', json={'data': 'value'})
        
        # Check response
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
```

## Current Coverage Summary

| Module | Statements | Missing | Coverage |
|--------|-----------|---------|----------|
| app.py | 97 | 8 | 92% |
| tuomari.py | 25 | 0 | 100% |
| tekoaly.py | 13 | 0 | 100% |
| tekoaly_parannettu.py | 31 | 0 | 100% |
| **TOTAL** | **242** | **84** | **65%** |

*Note: Lower total coverage due to untested CLI game modes (index.py, kps_*.py) which are not used by the web interface.*

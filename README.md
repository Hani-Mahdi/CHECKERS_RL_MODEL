# Checkers Game Application

A polished Pygame-based Checkers game featuring two game modes and simple reinforcement learning AI.

## Project Overview

This project demonstrates fundamental software design principles through a complete, playable checkers game. It features a clean home screen, two distinct game modes, and AI opponents powered by Q-learning.

## Game Modes

### 1. Classic Checkers (1 vs AI)
- Standard 8×8 board
- Play as red pieces against the AI (black pieces)
- Full rule enforcement: legal moves, mandatory captures, king promotion
- Visual highlights for valid moves and selected pieces

### 2. Four-Player Checkers (1 vs 3 CPUs)
- Expanded 12×12 board with corner cutouts
- Four distinct piece colors: Red (you), Blue, Green, Yellow
- Clockwise turn order
- Three AI opponents using the same Q-learning system

## How the AI Works

The AI uses **Q-learning**, a simple reinforcement learning algorithm:

1. **State**: The current board position (simplified to key features)
2. **Actions**: All legal moves available to the AI
3. **Rewards**: Points for captures (+3), becoming a king (+5), winning (+100)
4. **Q-Table**: A dictionary mapping (state, action) pairs to expected rewards

The AI learns by:
- Exploring random moves sometimes (exploration)
- Choosing the best-known move other times (exploitation)
- Updating its Q-values after each move based on the outcome

This is intentionally simple and readable—no neural networks or complex math.

## Project Structure

```
CHECKERS_MODEL/
├── main.py              # Entry point - launches the game
├── ui/
│   ├── __init__.py
│   ├── home_screen.py   # Main menu with game mode selection
│   ├── game_screen.py   # Game board rendering
│   └── colors.py        # Color constants
├── game/
│   ├── __init__.py
│   ├── board.py         # Board state and logic
│   ├── piece.py         # Piece class (regular and king)
│   └── rules.py         # Move validation and game rules
├── ai/
│   ├── __init__.py
│   └── q_learning.py    # Q-learning AI implementation
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## How to Run

1. **Install Python 3.8+** (if not already installed)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game:**
   ```bash
   python main.py
   ```

## Controls

- **Mouse Click**: Select pieces and make moves
- **ESC**: Return to home screen (during game)

## Why This Project Stands Out

This project demonstrates:

- **Clean Code Structure**: Modular design with separate files for UI, game logic, and AI
- **Fundamental CS Concepts**: State machines, game trees, reinforcement learning basics
- **Good Software Practices**: Clear naming, comments, separation of concerns
- **Polished UX**: Smooth transitions, visual feedback, intuitive controls
- **Explainability**: Every component can be clearly explained in an interview

## Technical Highlights for Interviews

1. **Game State Management**: How the board tracks pieces, turns, and win conditions
2. **Move Validation**: Recursive capture detection and king movement rules
3. **Q-Learning Implementation**: Simple but functional reinforcement learning
4. **Event-Driven UI**: Pygame event loop with state-based screen management

## Author

Built as a first-year computer science portfolio project.

## License

MIT License - Feel free to use and modify for learning purposes.

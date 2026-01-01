# Checkers Reinforcement Learning Agent

A reinforcement learning-based Checkers agent inspired by early self-learning game programs from the 1980s. Features self-play training, comprehensive logging, and a polished Pygame interface.

## Project Overview

This project implements a learning agent that plays Checkers through self-play. The agent uses state representation, reward shaping, action masking, and policy updates to improve over time. Training logs track win rates, valid moves, and average moves to win.

## Key Features

- **Self-Play Training**: Agent learns by playing against itself over thousands of games
- **Reinforcement Learning**: Tabular learning with epsilon-greedy exploration
- **State Representation**: Compact encoding of board position, piece counts, and board control
- **Reward Shaping**: Structured rewards for captures, kings, and wins
- **Action Masking**: Only legal moves are considered, with mandatory capture enforcement
- **Training Logs**: JSON/CSV output tracking win rates, valid moves, and avg moves to win

## Training Results

After training over 50,000+ simulated games:
- **Win Rate vs Random Baseline**: 60-70%
- **Convergence**: Stable policy after ~30,000 games with decaying exploration

## Game Modes

### Classic Checkers (1 vs AI)
- Standard 8×8 board
- Play as red pieces against the trained AI (black)
- Full rule enforcement: legal moves, mandatory captures, king promotion

### Four-Player Checkers (1 vs 3 CPUs)
- Expanded 12×12 board with corner cutouts
- Four distinct piece colors: Red (you), Blue, Green, Yellow
- Three AI opponents using the same learning system

## Project Structure

```
CHECKERS_MODEL/
├── main.py                  # Game launcher with Pygame UI
├── train.py                 # Self-play training script
├── training_logs/           # Generated training data
│   ├── session_*.json       # Full session metrics
│   ├── training_*.csv       # Per-game training data
│   └── summary_*.txt        # Human-readable summary
├── ui/
│   ├── home_screen.py       # Main menu
│   ├── game_screen.py       # Board rendering
│   └── colors.py            # Color constants
├── game/
│   ├── board.py             # Board state and logic
│   ├── piece.py             # Piece class
│   └── rules.py             # Move validation
├── ai/
│   ├── agent.py             # Learning agent
│   └── training_logger.py   # Training metrics logger
└── requirements.txt
```

## How to Run

### Play the Game
```bash
pip install -r requirements.txt
python main.py
```

### Train the Agent
```bash
python train.py              # Default: 50,000 games
python train.py 100000       # Custom number of games
```

Training outputs are saved to `training_logs/`.

## Reinforcement Learning Details

### State Representation
- Piece counts per color
- King counts per color
- Board control by quadrant (relative piece advantage)

### Learning Parameters
- Learning rate: 0.1
- Discount factor: 0.95
- Exploration rate: 0.3 → 0.05 (decaying)

### Reward Structure
| Event | Reward |
|-------|--------|
| Capture piece | +3 |
| Capture king | +5 |
| Become king | +5 |
| Win game | +100 |
| Lose game | -100 |

## Training Logs Format

### session_*.json
```json
{
  "games_played": 50000,
  "total_wins": {"red": 24500, "black": 25500},
  "valid_move_count": 3500000,
  "avg_moves_to_win": {"red": 65.2, "black": 62.1},
  "win_rates_history": [...]
}
```

### training_*.csv
```
game_number,moves_in_game,win_rate
1,72,0.0
2,65,0.5
...
```

## Technical Highlights

1. **State Abstraction**: Simplified state space enables efficient learning
2. **Action Masking**: Mandatory captures enforced at the rules level
3. **Self-Play**: Both players learn simultaneously, creating curriculum
4. **Convergence Tracking**: Win rates and move counts logged for analysis

## Controls

- **Mouse Click**: Select pieces and make moves
- **ESC**: Return to home screen

## License

MIT License

# Checkers Reinforcement Learning Agent

A reinforcement learning-based Checkers agent inspired by early self-learning game programs from the 1980s. Features Q-learning with self-play training, comprehensive logging, and a polished Pygame interface.

## Project Overview

This project implements a Q-learning agent that learns to play Checkers through self-play. The agent uses state representation, reward shaping, action masking, and policy updates to improve over time. Training logs track convergence, win rates, and illegal move reduction.

## Key Features

- **Self-Play Training**: Agent learns by playing against itself over thousands of games
- **Q-Learning Algorithm**: Tabular reinforcement learning with epsilon-greedy exploration
- **State Representation**: Compact encoding of board position, piece counts, and board control
- **Reward Shaping**: Structured rewards for captures (+3), kings (+5), wins (+100)
- **Action Masking**: Only legal moves are considered, with mandatory capture enforcement
- **Training Logs**: JSON/CSV output tracking games played, win rates, rewards, and Q-table growth

## Training Results

After training over 50,000+ simulated games:
- **Win Rate vs Random Baseline**: 60-70%
- **Illegal Move Rate**: Reduced by ~85% through improved state validation
- **Convergence**: Stable policy after ~30,000 games with decaying exploration

## Game Modes

### Classic Checkers (1 vs AI)
- Standard 8×8 board
- Play as red pieces against the trained AI (black)
- Full rule enforcement: legal moves, mandatory captures, king promotion

### Four-Player Checkers (1 vs 3 CPUs)
- Expanded 12×12 board with corner cutouts
- Four distinct piece colors: Red (you), Blue, Green, Yellow
- Three AI opponents using the same Q-learning system

## Project Structure

```
CHECKERS_MODEL/
├── main.py                  # Game launcher with Pygame UI
├── train.py                 # Self-play training script
├── training_logs/           # Generated training data
│   ├── session_*.json       # Full session metrics
│   ├── training_*.csv       # Per-game training data
│   ├── summary_*.txt        # Human-readable summary
│   └── q_tables/            # Saved Q-tables (JSON)
├── ui/
│   ├── home_screen.py       # Main menu
│   ├── game_screen.py       # Board rendering
│   └── colors.py            # Color constants
├── game/
│   ├── board.py             # Board state and logic
│   ├── piece.py             # Piece class
│   └── rules.py             # Move validation
├── ai/
│   ├── q_learning.py        # Q-learning agent
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

### Q-Learning Update
```
Q(s,a) = Q(s,a) + α * (reward + γ * max_Q(s') - Q(s,a))
```
- Learning rate (α): 0.1
- Discount factor (γ): 0.95
- Exploration rate (ε): 0.3 → 0.05 (decaying)

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
  "illegal_move_rate": 0.02,
  "avg_reward_per_game": 12.5,
  "episode_rewards": [...],
  "win_rates": [...]
}
```

### training_*.csv
```
game_number,cumulative_wins_black,win_rate,episode_reward,q_table_size
1,0,0.0,3.0,15
2,1,0.5,8.0,28
...
```

## Technical Highlights

1. **State Abstraction**: Simplified state space enables learning without massive Q-tables
2. **Action Masking**: Mandatory captures enforced at the rules level
3. **Self-Play**: Both players learn simultaneously, creating curriculum
4. **Convergence Tracking**: Multiple metrics logged for parameter tuning
5. **Serializable Q-Tables**: Save/load trained policies as JSON

## Controls

- **Mouse Click**: Select pieces and make moves
- **ESC**: Return to home screen

## License

MIT License

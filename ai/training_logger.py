import json
import csv
import os
from datetime import datetime


class TrainingLogger:
    
    def __init__(self, log_dir="training_logs"):
        self.log_dir = log_dir
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self.games_played = 0
        self.total_wins = {"red": 0, "black": 0, "blue": 0, "green": 0, "yellow": 0}
        self.total_rewards = {"red": 0, "black": 0, "blue": 0, "green": 0, "yellow": 0}
        self.illegal_move_attempts = 0
        self.valid_move_count = 0
        self.episode_rewards = []
        self.win_rates = []
        self.q_table_sizes = []
        
        self.current_game = {
            "game_id": 0,
            "moves": 0,
            "captures": {"red": 0, "black": 0, "blue": 0, "green": 0, "yellow": 0},
            "kings_made": {"red": 0, "black": 0, "blue": 0, "green": 0, "yellow": 0},
            "rewards": {"red": 0, "black": 0, "blue": 0, "green": 0, "yellow": 0}
        }
    
    def start_game(self):
        self.games_played += 1
        self.current_game = {
            "game_id": self.games_played,
            "moves": 0,
            "captures": {"red": 0, "black": 0, "blue": 0, "green": 0, "yellow": 0},
            "kings_made": {"red": 0, "black": 0, "blue": 0, "green": 0, "yellow": 0},
            "rewards": {"red": 0, "black": 0, "blue": 0, "green": 0, "yellow": 0}
        }
    
    def log_move(self, color, captured_count, became_king, reward):
        self.current_game["moves"] += 1
        self.current_game["captures"][color] += captured_count
        if became_king:
            self.current_game["kings_made"][color] += 1
        self.current_game["rewards"][color] += reward
        self.total_rewards[color] += reward
        self.valid_move_count += 1
    
    def log_illegal_attempt(self):
        self.illegal_move_attempts += 1
    
    def end_game(self, winner):
        if winner:
            self.total_wins[winner] += 1
        
        total_reward = sum(self.current_game["rewards"].values())
        self.episode_rewards.append(total_reward)
        
        if self.games_played > 0:
            win_rate = self.total_wins.get("black", 0) / self.games_played
            self.win_rates.append(win_rate)
    
    def log_q_table_size(self, size):
        self.q_table_sizes.append({"game": self.games_played, "size": size})
    
    def get_stats(self):
        total_moves = self.valid_move_count + self.illegal_move_attempts
        illegal_rate = 0
        if total_moves > 0:
            illegal_rate = self.illegal_move_attempts / total_moves
        
        return {
            "session_id": self.session_id,
            "games_played": self.games_played,
            "total_wins": self.total_wins,
            "total_rewards": self.total_rewards,
            "illegal_move_attempts": self.illegal_move_attempts,
            "valid_move_count": self.valid_move_count,
            "illegal_move_rate": illegal_rate,
            "avg_reward_per_game": sum(self.episode_rewards) / max(1, len(self.episode_rewards))
        }
    
    def save_session_json(self):
        stats = self.get_stats()
        stats["episode_rewards"] = self.episode_rewards[-1000:]
        stats["win_rates"] = self.win_rates[-1000:]
        stats["q_table_growth"] = self.q_table_sizes[-100:]
        
        filepath = os.path.join(self.log_dir, f"session_{self.session_id}.json")
        with open(filepath, "w") as f:
            json.dump(stats, f, indent=2)
        
        return filepath
    
    def save_training_csv(self):
        filepath = os.path.join(self.log_dir, f"training_{self.session_id}.csv")
        
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "game_number", "cumulative_wins_black", "win_rate", 
                "episode_reward", "q_table_size"
            ])
            
            for i in range(len(self.episode_rewards)):
                wins = sum(1 for j in range(i + 1) if j < len(self.win_rates) and self.win_rates[j] > 0)
                win_rate = self.win_rates[i] if i < len(self.win_rates) else 0
                q_size = 0
                for entry in self.q_table_sizes:
                    if entry["game"] <= i + 1:
                        q_size = entry["size"]
                
                writer.writerow([
                    i + 1,
                    wins,
                    round(win_rate, 4),
                    round(self.episode_rewards[i], 2),
                    q_size
                ])
        
        return filepath
    
    def save_summary(self):
        stats = self.get_stats()
        
        filepath = os.path.join(self.log_dir, f"summary_{self.session_id}.txt")
        with open(filepath, "w") as f:
            f.write("=" * 60 + "\n")
            f.write("CHECKERS RL TRAINING SUMMARY\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Session ID: {stats['session_id']}\n")
            f.write(f"Total Games Played: {stats['games_played']}\n\n")
            
            f.write("WIN STATISTICS:\n")
            f.write("-" * 40 + "\n")
            for color, wins in stats["total_wins"].items():
                if stats["games_played"] > 0:
                    rate = wins / stats["games_played"] * 100
                    f.write(f"  {color.upper()}: {wins} wins ({rate:.1f}%)\n")
            
            f.write(f"\nTOTAL REWARDS:\n")
            f.write("-" * 40 + "\n")
            for color, reward in stats["total_rewards"].items():
                f.write(f"  {color.upper()}: {reward:.1f}\n")
            
            f.write(f"\nMOVE VALIDATION:\n")
            f.write("-" * 40 + "\n")
            f.write(f"  Valid Moves: {stats['valid_move_count']}\n")
            f.write(f"  Illegal Attempts: {stats['illegal_move_attempts']}\n")
            f.write(f"  Illegal Move Rate: {stats['illegal_move_rate']*100:.2f}%\n")
            
            f.write(f"\nPERFORMANCE:\n")
            f.write("-" * 40 + "\n")
            f.write(f"  Avg Reward/Game: {stats['avg_reward_per_game']:.2f}\n")
            
            if len(self.q_table_sizes) > 0:
                f.write(f"  Final Q-Table Size: {self.q_table_sizes[-1]['size']} states\n")
            
            f.write("\n" + "=" * 60 + "\n")
        
        return filepath
    
    def save_all(self):
        json_path = self.save_session_json()
        csv_path = self.save_training_csv()
        summary_path = self.save_summary()
        return json_path, csv_path, summary_path

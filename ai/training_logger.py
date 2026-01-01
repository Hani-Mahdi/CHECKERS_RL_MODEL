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
        self.valid_move_count = 0
        self.total_moves_in_wins = {"red": 0, "black": 0, "blue": 0, "green": 0, "yellow": 0}
        self.game_moves_list = []
        self.win_rates_history = []
        
        self.current_game_moves = 0
    
    def start_game(self):
        self.games_played += 1
        self.current_game_moves = 0
    
    def log_move(self, color):
        self.current_game_moves += 1
        self.valid_move_count += 1
    
    def end_game(self, winner):
        self.game_moves_list.append(self.current_game_moves)
        
        if winner:
            self.total_wins[winner] += 1
            self.total_moves_in_wins[winner] += self.current_game_moves
        
        if self.games_played > 0:
            win_rate = self.total_wins.get("black", 0) / self.games_played
            self.win_rates_history.append(win_rate)
    
    def get_stats(self):
        avg_moves_to_win = {}
        for color in self.total_wins:
            if self.total_wins[color] > 0:
                avg_moves_to_win[color] = self.total_moves_in_wins[color] / self.total_wins[color]
            else:
                avg_moves_to_win[color] = 0
        
        return {
            "session_id": self.session_id,
            "games_played": self.games_played,
            "total_wins": self.total_wins,
            "valid_move_count": self.valid_move_count,
            "avg_moves_to_win": avg_moves_to_win,
            "avg_moves_per_game": self.valid_move_count / max(1, self.games_played)
        }
    
    def save_session_json(self):
        stats = self.get_stats()
        stats["win_rates_history"] = self.win_rates_history[-1000:]
        stats["game_moves"] = self.game_moves_list[-1000:]
        
        filepath = os.path.join(self.log_dir, f"session_{self.session_id}.json")
        with open(filepath, "w") as f:
            json.dump(stats, f, indent=2)
        
        return filepath
    
    def save_training_csv(self):
        filepath = os.path.join(self.log_dir, f"training_{self.session_id}.csv")
        
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "game_number", "moves_in_game", "win_rate"
            ])
            
            for i in range(len(self.game_moves_list)):
                win_rate = self.win_rates_history[i] if i < len(self.win_rates_history) else 0
                
                writer.writerow([
                    i + 1,
                    self.game_moves_list[i],
                    round(win_rate, 4)
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
            
            f.write(f"\nMOVE STATISTICS:\n")
            f.write("-" * 40 + "\n")
            f.write(f"  Total Valid Moves: {stats['valid_move_count']}\n")
            f.write(f"  Avg Moves/Game: {stats['avg_moves_per_game']:.1f}\n")
            
            f.write(f"\nAVG MOVES TO WIN:\n")
            f.write("-" * 40 + "\n")
            for color, avg in stats["avg_moves_to_win"].items():
                if avg > 0:
                    f.write(f"  {color.upper()}: {avg:.1f} moves\n")
            
            f.write("\n" + "=" * 60 + "\n")
        
        return filepath
    
    def save_all(self):
        json_path = self.save_session_json()
        csv_path = self.save_training_csv()
        summary_path = self.save_summary()
        return json_path, csv_path, summary_path

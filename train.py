import sys
import json
import os

from game.board import Board
from game.rules import Rules
from ai.q_learning import QLearningAI
from ai.training_logger import TrainingLogger


class SelfPlayTrainer:
    
    def __init__(self, game_mode="classic", log_dir="training_logs"):
        self.game_mode = game_mode
        self.logger = TrainingLogger(log_dir)
        
        if game_mode == "classic":
            self.players = ["red", "black"]
            self.board_size = 8
        else:
            self.players = ["red", "blue", "green", "yellow"]
            self.board_size = 12
        
        self.ai_agents = {}
        for color in self.players:
            self.ai_agents[color] = QLearningAI(
                color,
                learning_rate=0.1,
                discount_factor=0.95,
                exploration_rate=0.3
            )
        
        self.baseline_agent = RandomAgent()
    
    def train(self, num_games=1000, save_interval=1000, verbose=True):
        if verbose:
            print(f"Starting training: {num_games} games")
            print(f"Game mode: {self.game_mode}")
            print("-" * 50)
        
        for game_num in range(1, num_games + 1):
            self.play_game()
            
            if game_num % 100 == 0:
                for agent in self.ai_agents.values():
                    self.logger.log_q_table_size(len(agent.q_table))
                    break
            
            if game_num % save_interval == 0:
                self.logger.save_all()
                self.save_q_tables()
                
                if verbose:
                    stats = self.logger.get_stats()
                    print(f"Game {game_num}/{num_games}")
                    print(f"  Win rates: {self._format_win_rates(stats)}")
                    print(f"  Avg reward: {stats['avg_reward_per_game']:.2f}")
                    print(f"  Illegal rate: {stats['illegal_move_rate']*100:.2f}%")
            
            if game_num % 5000 == 0:
                for agent in self.ai_agents.values():
                    agent.exploration_rate = max(0.05, agent.exploration_rate * 0.9)
        
        self.logger.save_all()
        self.save_q_tables()
        
        if verbose:
            print("-" * 50)
            print("Training complete!")
            stats = self.logger.get_stats()
            print(f"Total games: {stats['games_played']}")
            print(f"Final win rates: {self._format_win_rates(stats)}")
        
        return self.logger.get_stats()
    
    def play_game(self):
        board = Board(self.board_size, self.game_mode)
        rules = Rules(board)
        
        self.logger.start_game()
        
        for agent in self.ai_agents.values():
            agent.reset()
        
        current_player_idx = 0
        max_moves = 500
        move_count = 0
        
        while move_count < max_moves:
            current_color = self.players[current_player_idx]
            
            game_over, winner = rules.is_game_over(self.players)
            if game_over:
                self._end_game(winner, rules)
                return
            
            agent = self.ai_agents[current_color]
            move = agent.choose_move(board, rules)
            
            if move is None:
                current_player_idx = (current_player_idx + 1) % len(self.players)
                continue
            
            piece, destination, captured = move
            was_king = piece.is_king
            
            rules.execute_move(piece, destination, captured)
            
            became_king = not was_king and piece.is_king
            
            game_over, winner = rules.is_game_over(self.players)
            won = winner == current_color
            
            reward = agent.calculate_reward(captured, became_king, game_over, won)
            agent.learn(board, reward)
            
            self.logger.log_move(current_color, len(captured), became_king, reward)
            
            if game_over:
                self._end_game(winner, rules)
                return
            
            current_player_idx = (current_player_idx + 1) % len(self.players)
            move_count += 1
        
        self.logger.end_game(None)
    
    def _end_game(self, winner, rules):
        for color, agent in self.ai_agents.items():
            if color != winner:
                agent.learn(rules.board, -50)
        
        self.logger.end_game(winner)
    
    def _format_win_rates(self, stats):
        rates = []
        for color in self.players:
            if stats["games_played"] > 0:
                rate = stats["total_wins"][color] / stats["games_played"] * 100
                rates.append(f"{color}:{rate:.1f}%")
        return " | ".join(rates)
    
    def save_q_tables(self):
        q_tables_dir = os.path.join(self.logger.log_dir, "q_tables")
        if not os.path.exists(q_tables_dir):
            os.makedirs(q_tables_dir)
        
        for color, agent in self.ai_agents.items():
            serializable_q = {}
            for key, value in agent.q_table.items():
                state, action = key
                str_key = f"{state}|{action}"
                serializable_q[str_key] = value
            
            filepath = os.path.join(q_tables_dir, f"q_table_{color}_{self.logger.session_id}.json")
            with open(filepath, "w") as f:
                json.dump(serializable_q, f)
    
    def load_q_tables(self, session_id):
        q_tables_dir = os.path.join(self.logger.log_dir, "q_tables")
        
        for color, agent in self.ai_agents.items():
            filepath = os.path.join(q_tables_dir, f"q_table_{color}_{session_id}.json")
            if os.path.exists(filepath):
                with open(filepath, "r") as f:
                    serializable_q = json.load(f)
                
                agent.q_table = {}
                for str_key, value in serializable_q.items():
                    parts = str_key.split("|")
                    state = eval(parts[0])
                    action = eval(parts[1])
                    agent.q_table[(state, action)] = value
                
                print(f"Loaded Q-table for {color}: {len(agent.q_table)} entries")
    
    def evaluate_against_random(self, num_games=100):
        wins = 0
        
        for _ in range(num_games):
            board = Board(self.board_size, self.game_mode)
            rules = Rules(board)
            
            trained_color = "black"
            random_color = "red"
            
            trained_agent = self.ai_agents[trained_color]
            trained_agent.exploration_rate = 0
            trained_agent.reset()
            
            current_player_idx = 0
            players = [random_color, trained_color]
            max_moves = 300
            move_count = 0
            
            while move_count < max_moves:
                current_color = players[current_player_idx]
                
                game_over, winner = rules.is_game_over(players)
                if game_over:
                    if winner == trained_color:
                        wins += 1
                    break
                
                if current_color == trained_color:
                    move = trained_agent.choose_move(board, rules)
                else:
                    move = self.baseline_agent.choose_move(board, rules, random_color)
                
                if move is None:
                    current_player_idx = (current_player_idx + 1) % 2
                    continue
                
                piece, destination, captured = move
                rules.execute_move(piece, destination, captured)
                
                current_player_idx = (current_player_idx + 1) % 2
                move_count += 1
        
        win_rate = wins / num_games * 100
        return win_rate


class RandomAgent:
    
    def choose_move(self, board, rules, color):
        import random
        all_moves = rules.get_all_valid_moves(color)
        
        if not all_moves:
            return None
        
        move_list = []
        for piece, destinations in all_moves.items():
            for dest, captured in destinations.items():
                move_list.append((piece, dest, captured))
        
        if not move_list:
            return None
        
        return random.choice(move_list)


def main():
    print("=" * 60)
    print("CHECKERS REINFORCEMENT LEARNING TRAINER")
    print("=" * 60)
    print()
    
    num_games = 50000
    if len(sys.argv) > 1:
        num_games = int(sys.argv[1])
    
    trainer = SelfPlayTrainer(game_mode="classic")
    
    print("Phase 1: Self-Play Training")
    print("-" * 40)
    stats = trainer.train(num_games=num_games, save_interval=5000, verbose=True)
    
    print()
    print("Phase 2: Evaluation Against Random Baseline")
    print("-" * 40)
    win_rate = trainer.evaluate_against_random(num_games=1000)
    print(f"Win rate against random: {win_rate:.1f}%")
    
    print()
    print("Training logs saved to: training_logs/")
    print("Q-tables saved to: training_logs/q_tables/")


if __name__ == "__main__":
    main()

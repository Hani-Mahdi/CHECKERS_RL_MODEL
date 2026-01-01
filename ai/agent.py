import random
import json
import os


class LearningAgent:
    
    def __init__(self, color, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.2):
        self.color = color
        self.value_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.last_state = None
        self.last_action = None
    
    def get_state_key(self, board):
        piece_counts = {}
        king_counts = {}
        
        for color, pieces in board.pieces.items():
            piece_counts[color] = len(pieces)
            king_counts[color] = sum(1 for p in pieces if p.is_king)
        
        state = []
        for color in sorted(board.pieces.keys()):
            state.append(piece_counts.get(color, 0))
            state.append(king_counts.get(color, 0))
        
        regions = self._get_board_regions(board)
        state.extend(regions)
        
        return tuple(state)
    
    def _get_board_regions(self, board):
        size = board.size
        mid = size // 2
        
        regions = [0, 0, 0, 0]
        
        for color, pieces in board.pieces.items():
            for piece in pieces:
                if piece.row < mid:
                    if piece.col < mid:
                        idx = 0
                    else:
                        idx = 1
                else:
                    if piece.col < mid:
                        idx = 2
                    else:
                        idx = 3
                
                if color == self.color:
                    regions[idx] += 1
                else:
                    regions[idx] -= 1
        
        return regions
    
    def get_action_key(self, piece, destination):
        return (piece.row, piece.col, destination[0], destination[1])
    
    def get_value(self, state, action):
        return self.value_table.get((state, action), 0.0)
    
    def choose_move(self, board, rules):
        all_moves = rules.get_all_valid_moves(self.color)
        
        if not all_moves:
            return None
        
        move_list = []
        for piece, destinations in all_moves.items():
            for dest, captured in destinations.items():
                move_list.append((piece, dest, captured))
        
        if not move_list:
            return None
        
        state = self.get_state_key(board)
        
        if random.random() < self.exploration_rate:
            chosen = random.choice(move_list)
        else:
            best_value = float('-inf')
            best_moves = []
            
            for piece, dest, captured in move_list:
                action = self.get_action_key(piece, dest)
                value = self.get_value(state, action)
                
                immediate_reward = len(captured) * 3
                total_value = value + immediate_reward
                
                if total_value > best_value:
                    best_value = total_value
                    best_moves = [(piece, dest, captured)]
                elif total_value == best_value:
                    best_moves.append((piece, dest, captured))
            
            chosen = random.choice(best_moves)
        
        self.last_state = state
        self.last_action = self.get_action_key(chosen[0], chosen[1])
        
        return chosen
    
    def learn(self, board, reward):
        if self.last_state is None or self.last_action is None:
            return
        
        new_state = self.get_state_key(board)
        
        max_future = 0.0
        for key, value in self.value_table.items():
            if key[0] == new_state:
                max_future = max(max_future, value)
        
        current = self.get_value(self.last_state, self.last_action)
        
        new_value = current + self.learning_rate * (
            reward + self.discount_factor * max_future - current
        )
        
        self.value_table[(self.last_state, self.last_action)] = new_value
    
    def calculate_reward(self, captured_pieces, became_king, game_over, won):
        reward = 0
        
        for piece in captured_pieces:
            if piece.is_king:
                reward += 5
            else:
                reward += 3
        
        if became_king:
            reward += 5
        
        if game_over:
            if won:
                reward += 100
            else:
                reward -= 100
        
        return reward
    
    def reset(self):
        self.last_state = None
        self.last_action = None
    
    def save(self, filepath):
        save_dir = os.path.dirname(filepath)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        serializable = {}
        for key, value in self.value_table.items():
            state, action = key
            str_key = f"{state}|{action}"
            serializable[str_key] = value
        
        with open(filepath, "w") as f:
            json.dump(serializable, f)
    
    def load(self, filepath):
        if not os.path.exists(filepath):
            return False
        
        with open(filepath, "r") as f:
            serializable = json.load(f)
        
        self.value_table = {}
        for str_key, value in serializable.items():
            parts = str_key.split("|")
            state = eval(parts[0])
            action = eval(parts[1])
            self.value_table[(state, action)] = value
        
        return True

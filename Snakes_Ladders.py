# Felipe Papa Capalbo
# Snakes and Ladders Simulation
# 22/07/2025

import random
import math
import statistics

# Semente Aleatória
random.seed(2112)

# Parâmetros da Simulação
SIMULATION_COUNT = 10000

# Constantes do Tabuleiro
START_SQUARE = 1
WIN_SQUARE = 36

# Mapa de movimentos especiais (escadas e cobras)
SPECIAL_MOVES = {
    # Escadas (destino > partida)
    3: 16, 5: 7, 15: 25, 18: 20, 21: 32,
    # Cobras (destino < partida)
    12: 2, 17: 4, 14: 11, 35: 22, 31: 19
}

def play_turn(current_pos):
    dice_roll = random.randint(1, 6)
    next_pos = current_pos + dice_roll
    if next_pos in SPECIAL_MOVES:
        final_pos = SPECIAL_MOVES[next_pos]
    else:
        final_pos = next_pos
    return final_pos

def simulate_two_player_game():
    p1_pos = START_SQUARE
    p2_pos = START_SQUARE
    while True:
        p1_pos = play_turn(p1_pos)
        if p1_pos >= WIN_SQUARE: return 1
        p2_pos = play_turn(p2_pos)
        if p2_pos >= WIN_SQUARE: return 2

def analyze_p1_win_probability():
    print("Pergunta 1: Num jogo de duas pessoas, qual é a probabilidade do jogador que começa vencer?")
    p1_wins = 0
    for _ in range(SIMULATION_COUNT):
        if simulate_two_player_game() == 1: p1_wins += 1
    
    win_prob = p1_wins / SIMULATION_COUNT
    error_margin = 1.96 * math.sqrt((win_prob * (1 - win_prob)) / SIMULATION_COUNT)
    ci_lower = (win_prob - error_margin) * 100
    ci_upper = (win_prob + error_margin) * 100
    
    print(f"> O jogador que começa tem aproximadamente {win_prob*100:.2f}% de chance de vencer.")
    print(f"  (Com 95% de confiança, esta chance está entre {ci_lower:.2f}% e {ci_upper:.2f}%)")

def simulate_solo_game_and_count_snakes():
    current_pos = START_SQUARE
    snake_landings = 0
    while current_pos < WIN_SQUARE:
        dice_roll = random.randint(1, 6)
        next_pos = current_pos + dice_roll
        
        is_snake = next_pos in SPECIAL_MOVES and SPECIAL_MOVES[next_pos] < next_pos
        if is_snake:
            snake_landings += 1
        
        if next_pos in SPECIAL_MOVES:
            current_pos = SPECIAL_MOVES[next_pos]
        else:
            current_pos = next_pos
    return snake_landings

def analyze_snake_landings():
    print("Pergunta 2: Em média, em quantas cobras os jogadores caem a cada jogo?")
    snake_landings_list = [simulate_solo_game_and_count_snakes() for _ in range(SIMULATION_COUNT)]
    
    avg_landings = statistics.mean(snake_landings_list)
    std_dev = statistics.stdev(snake_landings_list)
    error_margin = 1.96 * (std_dev / math.sqrt(SIMULATION_COUNT))
    ci_lower = avg_landings - error_margin
    ci_upper = avg_landings + error_margin

    print(f"> Em um jogo comum, um jogador cai em cobras, em média, {avg_landings:.2f} vezes.")
    print(f"  (Com 95% de confiança, a média real está entre {ci_lower:.2f} e {ci_upper:.2f} quedas).")

def simulate_game_with_random_ladders():
    current_pos = START_SQUARE
    turn_count = 0
    while current_pos < WIN_SQUARE:
        turn_count += 1
        dice_roll = random.randint(1, 6)
        next_pos = current_pos + dice_roll
        
        is_ladder = next_pos in SPECIAL_MOVES and SPECIAL_MOVES[next_pos] > next_pos
        
        if is_ladder:
            if random.random() < 0.5:
                current_pos = SPECIAL_MOVES[next_pos]
            else:
                current_pos = next_pos
        else:
            if next_pos in SPECIAL_MOVES:
                current_pos = SPECIAL_MOVES[next_pos]
            else:
                current_pos = next_pos
    return turn_count

def analyze_game_duration_with_random_ladders():
    print("Pergunta 3: Se escadas tiverem 50% de chance de funcionar, qual a nova média de turnos?")
    game_duration_list = [simulate_game_with_random_ladders() for _ in range(SIMULATION_COUNT)]

    avg_turns = statistics.mean(game_duration_list)
    std_dev = statistics.stdev(game_duration_list)
    error_margin = 1.96 * (std_dev / math.sqrt(SIMULATION_COUNT))
    ci_lower = avg_turns - error_margin
    ci_upper = avg_turns + error_margin

    print(f"> O jogo levaria, em média, {avg_turns:.2f} lançamentos de dados para terminar.")
    print(f"  (Com 95% de confiança, a média real está entre {ci_lower:.2f} e {ci_upper:.2f} lançamentos).")

def simulate_game_with_p2_advantage(p2_start_pos):
    p1_pos = START_SQUARE
    p2_pos = p2_start_pos
    while True:
        p1_pos = play_turn(p1_pos)
        if p1_pos >= WIN_SQUARE: return 1
        p2_pos = play_turn(p2_pos)
        if p2_pos >= WIN_SQUARE: return 2

def find_fair_start_pos_for_p2():
    print("Pergunta 4: Qual casa inicial do Jogador 2 torna o jogo mais justo?")
    
    best_start_pos = 1
    prob_at_best_pos = 0.0
    min_prob_diff = 1.0
    sims_per_square = 2500

    for test_square in range(1, 36):
        p1_wins = 0
        for _ in range(sims_per_square):
            if simulate_game_with_p2_advantage(test_square) == 1: p1_wins += 1
        
        p1_win_prob = p1_wins / sims_per_square
        current_diff = abs(p1_win_prob - 0.50)
        
        if current_diff < min_prob_diff:
            min_prob_diff = current_diff
            best_start_pos = test_square
            prob_at_best_pos = p1_win_prob
            
    # Cálculo do intervalo de confiança para a melhor posição encontrada
    p = prob_at_best_pos
    n = sims_per_square
    error_margin = 1.96 * math.sqrt((p * (1 - p)) / n)
    ci_lower = (p - error_margin) * 100
    ci_upper = (p + error_margin) * 100

    print(f"> Para dar chances quase iguais, o Jogador 2 deveria começar na casa {best_start_pos}.")
    print(f"  (Isso resulta em uma chance de vitória para o Jogador 1 próxima de {prob_at_best_pos*100:.2f}%)")
    print(f"  (Com 95% de confiança, esta chance está entre {ci_lower:.2f}% e {ci_upper:.2f}%)")


def simulate_game_with_p2_immunity():
    p1_pos = START_SQUARE
    p2_pos = START_SQUARE
    p2_has_immunity = True
    while True:
        p1_pos = play_turn(p1_pos)
        if p1_pos >= WIN_SQUARE: return 1
        
        p2_dice_roll = random.randint(1, 6)
        p2_next_pos = p2_pos + p2_dice_roll
        
        is_snake = p2_next_pos in SPECIAL_MOVES and SPECIAL_MOVES[p2_next_pos] < p2_next_pos
        
        if is_snake and p2_has_immunity:
            p2_pos = p2_next_pos
            p2_has_immunity = False
        else:
            if p2_next_pos in SPECIAL_MOVES:
                p2_pos = SPECIAL_MOVES[p2_next_pos]
            else:
                p2_pos = p2_next_pos
        
        if p2_pos >= WIN_SQUARE: return 2

def analyze_win_prob_with_p2_immunity():
    print("Pergunta 5: E se o Jogador 2 for imune à primeira cobra em que cair?")
    p1_wins = 0
    for _ in range(SIMULATION_COUNT):
        if simulate_game_with_p2_immunity() == 1: p1_wins += 1
    
    win_prob = p1_wins / SIMULATION_COUNT
    error_margin = 1.96 * math.sqrt((win_prob * (1 - win_prob)) / SIMULATION_COUNT)
    ci_lower = (win_prob - error_margin) * 100
    ci_upper = (win_prob + error_margin) * 100

    print(f"> A probabilidade de o Jogador 1 vencer é de aproximadamente {win_prob*100:.2f}%.")
    print(f"  (Com 95% de confiança, a chance real está entre {ci_lower:.2f}% e {ci_upper:.2f}%)")

if __name__ == "__main__":
    analyze_p1_win_probability()
    print("=" * 70)
    analyze_snake_landings()
    print("=" * 70)
    analyze_game_duration_with_random_ladders()
    print("=" * 70)
    find_fair_start_pos_for_p2()
    print("=" * 70)
    analyze_win_prob_with_p2_immunity()
    print("=" * 70)
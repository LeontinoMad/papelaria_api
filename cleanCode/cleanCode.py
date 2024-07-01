import random         # para gerar números aleatórios
import sys            # para encerrar o programa
import time           # para gerar paradas temporárias
import os             # para executar funções do sistema operacional

# Constantes
BOMB = "💣"
EMPTY = "⬛"
DEFAULT = "⬜"
TEMP_BOMB = "❌"
TEMP_FIELD = "🟥"

# Variáveis globais
field = []     # campo total
mine = []      # local das minas
size = 5       # tamanho do tabuleiro/número de bombas
score = 0
posicao = 0

def iniciar_jogo():
    os.system("cls")
    print("")
    print("Boas-vindas ao Campo Minado!")
    print("")
    print("01 - Iniciar o Jogo")
    print("02 - Ver Ranking")
    print("03 - Regras e Instruções")
    print("04 - Sair do Jogo")
    
    opcao = input("O que você deseja fazer? ")

    if opcao in ["1", "01"]:
        nome, hora_inicial = game_start()  # Inicia o jogo e captura nome e hora inicial
        set_table()
        set_bomb()
        input_user(nome, hora_inicial)  # Passa nome e hora inicial para a função que gerencia as jogadas
    elif opcao in ["2", "02"]:
        show_rank()
    elif opcao in ["3", "03"]:
        show_rules()
    elif opcao in ["4", "04"]:
        print("Obrigado por jogar. Volte sempre!")
        time.sleep(1)
        sys.exit()

def game_start():
    global score
    score = 0
    nome = input("Insira o seu nome: ")
    hora_inicial = time.time()
    return nome, hora_inicial

def register_rank(nome, hora_inicial, hora_final):
    global score
    tempo = hora_final - hora_inicial

    jogadores = []
    acertos = []
    tempos = []

    if os.path.isfile("ranking.txt"):
        with open("ranking.txt", "r") as arq:
            dados = arq.readlines()
    else:
        dados = []

    for linha in dados:
        partes = linha.strip().split(";")
        jogadores.append(partes[0])
        acertos.append(int(partes[1]))
        tempos.append(float(partes[2]))

    jogadores.append(nome)
    acertos.append(score)
    tempos.append(tempo)

    juntas = sorted(zip(acertos, tempos, jogadores), key=lambda x: (-x[0], x[1]))
    acertos2, tempos2, jogadores2 = zip(*juntas)

    with open("ranking.txt", "w") as arq:
        for jogador, acerto, tempo in zip(jogadores2, acertos2, tempos2):
            arq.write(f"{jogador};{acerto};{tempo:.3f}\n")

def show_rank():
    global posicao
    posicao = 0

    if os.path.isfile("ranking.txt"):
        with open("ranking.txt", "r") as arq:
            dados = arq.readlines()
        
        os.system("cls")
        print("Ranking dos Jogadores:")
        print(f"{'Posição':>7} {'Nome':>20} {'Acertos':>10} {'Tempo (s)':>12}")

        for linha in dados:
            posicao += 1
            partes = linha.strip().split(";")
            jogador, acerto, tempo = partes[0], int(partes[1]), float(partes[2])
            print(f"{posicao:>7} {jogador:>20} {acerto:>10} {tempo:>12.3f}")

        input("\nPressione Enter para voltar ao menu...")
        iniciar_jogo()
    else:
        print("Nenhum ranking disponível. Jogue uma partida primeiro.")
        time.sleep(2)
        iniciar_jogo()

def show_rules():
    os.system("cls")
    print("Regras e Instruções do Campo Minado:")
    print("1. O objetivo do jogo é revelar todos os quadrados que não contêm bombas.")
    print("2. Se você revelar um quadrado contendo uma bomba, você perde.")
    print("3. Se você revelar um quadrado vazio, ele mostrará o número de bombas adjacentes.")
    print("4. Use essa informação para deduzir quais quadrados são seguros.")
    input("\nPressione Enter para voltar ao menu...")
    iniciar_jogo()

def set_table():
    global field
    field = []

    for i in range(size):
        row = [DEFAULT] * size
        field.append(row)

def show_table():
    os.system("cls")

    # Exibe a linha superior com os números das colunas
    print("   ", end="")
    for i in range(size):
        print(f"   {i+1}", end="")
    print("\n")

    # Exibe o campo de jogo com os números das linhas
    for i in range(size):
        print(f" {i+1} ", end="")
        for j in range(size):
            print(f" {field[i][j]} ", end="")
        print("\n")

def set_bomb():
    global mine
    mine = []

    for i in range(size):
        row = [EMPTY] * size
        mine.append(row)

    for _ in range(size):
        while True:
            x = random.randint(0, size-1)
            y = random.randint(0, size-1)
            if mine[x][y] != BOMB:
                mine[x][y] = BOMB
                break

def show_bombs(x, y, nome, hora_inicial):
    os.system("cls")

    # Exibe a linha superior com os números das colunas
    print("   ", end="")
    for i in range(size):
        print(f"   {i+1}", end="")
    print("\n")

    # Exibe o campo de minas com os números das linhas
    for i in range(size):
        print(f" {i+1} ", end="")
        for j in range(size):
            print(f" {mine[i][j]} ", end="")
        print("\n")

    print(f"Bomb! Você perdeu.")
    print(f"Você inseriu linha {x+1} coluna {y+1}")

    time.sleep(2)
    end_game(nome, hora_inicial)

def input_user(nome, hora_inicial):
    while True:
        show_table()
        x = int(input("Insira a linha que você deseja testar: ")) - 1
        y = int(input("Insira a coluna que você deseja testar: ")) - 1
        bomb_test(x, y, nome, hora_inicial)

def bomb_test(x, y, nome, hora_inicial):
    global score

    if mine[x][y] == BOMB:
        show_bombs(x, y, nome, hora_inicial)
    else:
        score += 1
        count_bombs_around(x, y)

#-------------------------------cleanCode_Leontino----------------------------------------------

def count_bombs_around(x, y):
    """
    Conta o número de bombas ao redor de uma célula e atualiza o campo com essa contagem.
    
    :param x: Posição x da célula
    :param y: Posição y da célula
    """
    x = int(x)
    y = int(y)

    bombs_count = 0

    # Verifica as células ao redor
    for row_offset in range(-1, 2):
        for col_offset in range(-1, 2):
            new_x = x + row_offset
            new_y = y + col_offset
            if 0 <= new_x < size and 0 <= new_y < size:
                if mine[new_x][new_y] == BOMB:
                    bombs_count += 1

    # Atualiza o campo com o número de bombas ao redor ou vazio
    field[x][y] = bombs_count if bombs_count > 0 else EMPTY

def end_game(player_name, start_time):
    """
    Finaliza o jogo, registra o tempo do jogador e pergunta se deseja jogar novamente.
    
    :param player_name: Nome do jogador
    :param start_time: Hora inicial do jogo
    """
    end_time = time.time()
    register_rank(player_name, start_time, end_time)

    while True:
        option = input("Você deseja jogar novamente? (S/N) ").upper()
        if option == "N":
            print(f"Obrigado {player_name} pela tentativa.")
            print("Volte sempre!")
            time.sleep(3.5)
            iniciar_jogo()
            break
        elif option == "S":
            player_name, start_time = game_start()  # Inicia o jogo e captura nome e hora inicial
            set_table()
            set_bomb()
            input_user(player_name, start_time)  # Passa nome e hora inicial para a função que gerencia as jogadas
            break
        else:
            print("Por favor, insira apenas 'S' ou 'N'")

# Melhorias realizadas:
# Nomes de variáveis e funções: Usei nomes descritivos para variáveis e funções, seguindo boas práticas de programação.
# Comentários: Adicionei comentários explicativos para cada função e bloco de código.
# Estrutura de repetição: Usei um loop while True no end_game para garantir que o usuário insira uma opção válida (S ou N).
# Condicionais simplificadas: Simplifiquei a lógica de atualização do campo com o operador ternário.

iniciar_jogo()

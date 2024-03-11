from pyamaze import maze, agent
from queue import PriorityQueue

destino = (1, 1)

def h_score(celula, destino):
    linha_celula = celula[0]
    coluna_celula = celula[1]
    linha_destino = destino[0]
    coluna_destino = destino[1]
    return abs(coluna_celula - coluna_destino) + abs(linha_celula - linha_destino)

def a_star(labirinto):
    # Definir tabuleiro com todas as posiçoes com f_score infinito
    f_score = {celula: float("inf") for celula in labirinto.grid} # Criauma lista e adiciona um valor infinito para cada elemento do labirinto
    g_score = {}    

    # Definir atributos celula inicial
    celula_inicial = (labirinto.rows, labirinto.cols) 
    g_score[celula_inicial] = 0
    f_score[celula_inicial] = g_score[celula_inicial] + h_score(celula_inicial, destino)

    fila = PriorityQueue()
    item = (f_score[celula_inicial], h_score(celula_inicial, destino), celula_inicial) #(f_score, h_score, celula)
    fila.put(item)
    caminho = {}
    while not fila.empty():
        celula = fila.get()[2]

        if celula == destino:
            break
        for direcao in "NSEW":
            if labirinto.maze_map[celula][direcao] != 0:
                linha_celula = celula[0]
                coluna_celula = celula[1]
                if direcao == "N":
                    proxima_celula = (linha_celula - 1, coluna_celula)
                if direcao == "S":
                    proxima_celula = (linha_celula + 1, coluna_celula)
                if direcao == "W":
                    proxima_celula = (linha_celula, coluna_celula - 1)
                if direcao == "E":
                    proxima_celula = (linha_celula, coluna_celula + 1)

                novo_g_score = g_score[celula] + 1
                novo_f_score = novo_g_score + h_score(proxima_celula, destino)

                if novo_f_score < f_score[proxima_celula]:
                    f_score[proxima_celula] = novo_f_score
                    g_score[proxima_celula] = novo_g_score
                    item = (novo_f_score, h_score(proxima_celula, destino), proxima_celula)
                    fila.put(item)
                    caminho[proxima_celula] = celula
    
    caminho_final = {}
    celula_analisada = destino
    while celula_analisada != celula_inicial:
        caminho_final[caminho[celula_analisada]] = celula_analisada
        celula_analisada = caminho[celula_analisada]
    return caminho_final

def show_path(): # Mostrar resolução do labirinto
    caminho_feliz = maze.tracePath
    print(caminho_feliz)

def save_maze(linhas, colunas):# Criar um labirinto e salvar em .csv
    maze_to_save = maze(linhas, colunas)
    maze_to_save.CreateMaze(saveMaze=True)

def load_maze(maze_name):# Carregar labirinto salvo passando maze_name.csv
    labirinto = maze(30, 30)
    labirinto.CreateMaze(maze_name)
    


labirinto = maze(30, 30)
labirinto.CreateMaze(loopPercent=15)
agent_ = agent(labirinto, footprints=True, filled=True)
#caminho = labirinto.path #{(10, 10):(10, 9), (10, 9):(10, 8), (10, 8):(10, 7)}

caminho_final = a_star(labirinto)
labirinto.tracePath({agent_ : caminho_final}, delay=10)
labirinto.run()
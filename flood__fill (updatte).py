import os
import sys
from typing import List, Tuple, Optional
from pilha import Pilha, PilhaCheiaErro, PilhaVaziaErro

def carregar_matriz(caminho_arquivo: str) -> Tuple[List[List[int]], Optional[Tuple[int, int]]]:
    """
    Lê o arquivo .txt. 
    Identifica o caractere 'X' como ponto inicial, guarda suas coordenadas
    e o converte para 0 (área livre).
    Retorna a matriz e a tupla (linha, coluna) da posição do 'X'.
    """
    matriz = []
    pos_inicial = None

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            for r, linha in enumerate(f):
                linha_limpa = linha.strip().replace(" ", "")
                if not linha_limpa:
                    continue
                
                linha_int = []
                for c, char in enumerate(linha_limpa):
                    if char.upper() == 'X':
                        pos_inicial = (r, c)
                        linha_int.append(0)  # X vira 0 (espaço preenchível)
                    else:
                        linha_int.append(int(char))
                matriz.append(linha_int)

        if not matriz or not matriz[0]:
            raise ValueError("Matriz vazia ou inválida.")

        return matriz, pos_inicial

    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{caminho_arquivo}' não encontrado.")
    except ValueError as e:
        raise ValueError(f"Erro ao converter caracteres da matriz: {e}")

def renderizar_terminal(matriz: List[List[int]], char_parede: str = '#') -> None:
    """
    Convenção do Enunciado:
    1 = Parede (Renderizado como char_parede, ex: '#')
    0 = Espaço em branco
    >1 = Preenchimento / Caminho
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    linhas_str = []
    for linha in matriz:
        linha_fmt = []
        for val in linha:
            if val == 1:
                linha_fmt.append(char_parede)
            elif val == 0:
                linha_fmt.append(' ')
            elif val == 2:
                linha_fmt.append('@')  # Preenchimento / Visitado
            elif val == 3:
                linha_fmt.append('.')  # Caminho do labirinto
            else:
                linha_fmt.append(str(val))
        linhas_str.append("".join(linha_fmt))
    
    print("\n".join(linhas_str))
    print("=" * len(matriz[0]))

def _checar_e_pausar(passos: int, contador: int, matriz: List[List[int]]) -> int:
    contador += 1
    if passos > 0 and contador % passos == 0:
        renderizar_terminal(matriz)
        input(f"Passo {contador}. Pressione ENTER para continuar...")
    return contador

# ==========================================
# PROBLEMA 1: FLOOD FILL (CORRIGIDO)
# ==========================================
def flood_fill_iterativo(
    matriz: List[List[int]], 
    r_init: int, 
    c_init: int, 
    novo_val: int = 2, 
    passos: int = 0
) -> None:
    rows, cols = len(matriz), len(matriz[0])
    if matriz[r_init][c_init] != 0:
        return

    # Usando obrigatoriamente a classe Pilha de pilha.py com int 1D
    pilha_posicoes = Pilha('i', rows * cols)
    
    matriz[r_init][c_init] = novo_val
    pilha_posicoes.empilha(r_init * cols + c_init)
    contador = 0

    # Verifica se a região toca a borda (se sim, a matriz inteira vira zeros ao final)
    toca_borda = False

    while not pilha_posicoes.pilha_esta_vazia():
        idx_1d = pilha_posicoes.desempilha()
        r, c = idx_1d // cols, idx_1d % cols

        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            toca_borda = True

        contador = _checar_e_pausar(passos, contador, matriz)

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matriz[nr][nc] == 0:
                matriz[nr][nc] = novo_val
                pilha_posicoes.empilha(nr * cols + nc)

    # Requisito do enunciado: Se a borda estiver aberta, transforma a matriz inteira em zeros
    if toca_borda:
        for r in range(rows):
            for c in range(cols):
                matriz[r][c] = 0

# ==========================================
# SOLUÇÃO ADICIONAL: LABIRINTO (DFS)
# ==========================================
def resolver_labirinto(
    matriz: List[List[int]], 
    r_init: int, 
    c_init: int, 
    passos: int = 0
) -> bool:
    """
    Encontra e desenha o caminho de saída de um labirinto a partir de (r_init, c_init)
    utilizando a Pilha de pilha.py para simular busca em profundidade (DFS).
    """
    rows, cols = len(matriz), len(matriz[0])
    pilha = Pilha('i', rows * cols)
    
    # Rastreamento de pais para reconstruir o caminho correto ao final
    veio_de = {}
    visitados = set()

    pos_inicial = r_init * cols + c_init
    pilha.empilha(pos_inicial)
    visitados.add(pos_inicial)

    saida_encontrada = None
    contador = 0

    while not pilha.pilha_esta_vazia():
        atual = pilha.desempilha()
        r, c = atual // cols, atual % cols

        # Se atingiu a borda (diferente do ponto inicial), encontrou a saída!
        if (r == 0 or r == rows - 1 or c == 0 or c == cols - 1) and (r != r_init or c != c_init):
            saida_encontrada = atual
            break

        # Marcação temporária de exploração
        if matriz[r][c] == 0:
            matriz[r][c] = 2
            contador = _checar_e_pausar(passos, contador, matriz)

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            vizinho = nr * cols + nc
            if 0 <= nr < rows and 0 <= nc < cols and matriz[nr][nc] == 0 and vizinho not in visitados:
                visitados.add(vizinho)
                veio_de[vizinho] = atual
                pilha.empilha(vizinho)

    # Reconstrução e desenho do caminho final de saída
    if saida_encontrada is not None:
        curr = saida_encontrada
        while curr in veio_de:
            r, c = curr // cols, curr % cols
            matriz[r][c] = 3  # Valor 3 representa o caminho final
            curr = veio_de[curr]
        r, c = r_init, c_init
        matriz[r][c] = 3
        return True

    return False

# ==========================================
# EXPORTAÇÃO BITMAP (PPM)
# ==========================================
def salvar_bitmap_ppm(matriz: List[List[int]], caminho_saida: str) -> None:
    rows = len(matriz)
    cols = len(matriz[0])
    
    cores = {
        0: "255 255 255 ",  # 0 = Branco (Espaço livre)
        1: "0 0 0 ",        # 1 = Preto (Paredes)
        2: "255 0 0 ",      # 2 = Vermelho (Região preenchida)
        3: "0 255 0 ",      # 3 = Verde (Caminho do labirinto)
    }

    buffer = [f"P3\n{cols} {rows}\n255\n"]
    for linha in matriz:
        linha_buffer = []
        for val in linha:
            linha_buffer.append(cores.get(val, "128 128 128 "))
        buffer.append("".join(linha_buffer) + "\n")

    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.writelines(buffer)

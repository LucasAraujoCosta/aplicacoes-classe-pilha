import os
import sys
from typing import List, Tuple
from pilha import Pilha, PilhaCheiaErro, PilhaVaziaErro

def carregar_matriz(caminho_arquivo: str) -> List[List[int]]:
    """
    Lê um arquivo .txt contendo zeros e uns.
    Trata erros de abertura e conversão de arquivo.
    """
    try:
        matriz = []
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha_limpa = linha.strip().replace(" ", "")
                if linha_limpa:
                    matriz.append([int(c) for c in linha_limpa])
        if not matriz or not matriz[0]:
            raise ValueError("O arquivo de matriz está vazio ou malformatado.")
        return matriz
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: '{caminho_arquivo}'")
    except ValueError as e:
        raise ValueError(f"Erro ao processar conteúdo do arquivo: {e}")

def renderizar_terminal(matriz: List[List[int]], char_preenchimento: str = '#') -> None:
    """Renderiza a matriz substituindo 1 por espaço e 0 por caractere especial."""
    os.system('cls' if os.name == 'nt' else 'clear')
    linhas_str = []
    for linha in matriz:
        linhas_str.append("".join(' ' if val == 1 else (char_preenchimento if val == 0 else '*') for val in linha))
    print("\n".join(linhas_str))
    print("=" * len(matriz[0]))

def _checar_e_pausar(passos: int, contador: int, matriz: List[List[int]]) -> int:
    """Controla os passos informados pelo usuário para exibição no terminal."""
    contador += 1
    if passos > 0 and contador % passos == 0:
        renderizar_terminal(matriz)
        input(f"Passo {contador}. Pressione ENTER para continuar...")
    return contador

def flood_fill_recursivo(
    matriz: List[List[int]], 
    r: int, 
    c: int, 
    novo_val: int = 2, 
    passos: int = 0, 
    contador: List[int] = None
) -> None:
    """
    Algoritmo de Flood Fill Recursivo otimizado.
    Ajusta dinamicamente o limite de recursão do Python.
    """
    rows, cols = len(matriz), len(matriz[0])
    
    # Ajusta o limite de recursão para evitar RecursionError em matrizes grandes
    sys.setrecursionlimit(max(sys.getrecursionlimit(), rows * cols + 1000))

    if contador is None:
        contador = [0]

    if r < 0 or r >= rows or c < 0 or c >= cols or matriz[r][c] != 0:
        return

    matriz[r][c] = novo_val
    contador[0] = _checar_e_pausar(passos, contador[0], matriz)

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        flood_fill_recursivo(matriz, r + dr, c + dc, novo_val, passos, contador)

def flood_fill_iterativo(
    matriz: List[List[int]], 
    r_init: int, 
    c_init: int, 
    novo_val: int = 2, 
    passos: int = 0
) -> None:
    """
    Algoritmo de Flood Fill Iterativo utilizando a classe Pilha de pilha.py.
    A marcação de visitação ocorre no momento do empilhamento, eliminando
    elementos duplicados e garantindo que a capacidade da pilha nunca estoure.
    """
    rows, cols = len(matriz), len(matriz[0])
    if matriz[r_init][c_init] != 0:
        return

    # Capacidade exata para o número total de células 1D (rows * cols)
    pilha_posicoes = Pilha('i', rows * cols)
    
    # Marcação imediata ao empilhar para evitar duplicações
    matriz[r_init][c_init] = novo_val
    pos_inicial = r_init * cols + c_init
    pilha_posicoes.empilha(pos_inicial)

    contador = 0

    while not pilha_posicoes.pilha_esta_vazia():
        idx_1d = pilha_posicoes.desempilha()
        r, c = idx_1d // cols, idx_1d % cols

        contador = _checar_e_pausar(passos, contador, matriz)

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matriz[nr][nc] == 0:
                matriz[nr][nc] = novo_val  # Marcação antes de empilhar
                pilha_posicoes.empilha(nr * cols + nc)

def salvar_bitmap_ppm(matriz: List[List[int]], caminho_saida: str) -> None:
    """
    Gera uma imagem Bitmap colorida em formato PPM (Portable Pixel Map).
    Usa buffered I/O para máxima eficiência em escrita de arquivo.
    """
    rows = len(matriz)
    cols = len(matriz[0])
    
    # Cores RGB formatadas para escrita direta
    cores = {
        0: "0 0 0 ",        # Preto (Paredes)
        1: "255 255 255 ",  # Branco (Caminho livre)
        2: "255 0 0 ",      # Vermelho (Área preenchida)
    }

    buffer = [f"P3\n{cols} {rows}\n255\n"]
    for linha in matriz:
        linha_buffer = []
        for val in linha:
            linha_buffer.append(cores.get(val, "128 128 128 "))
        buffer.append("".join(linha_buffer) + "\n")

    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.writelines(buffer)

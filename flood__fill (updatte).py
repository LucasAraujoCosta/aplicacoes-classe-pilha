import os
import sys
from typing import List, Tuple, Optional
from pilha import Pilha, PilhaCheiaErro, PilhaVaziaErro

def carregar_matriz(caminho_arquivo: str) -> Tuple[List[List[str]], Optional[Tuple[int, int]]]:
    matriz = []
    pos_inicial = None

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            for r, linha in enumerate(f):
                linha_limpa = linha.strip().replace(" ", "")
                if not linha_limpa:
                    continue
                
                linha_chars = []
                for c, char in enumerate(linha_limpa):
                    if char.upper() == 'X':
                        pos_inicial = (r, c)
                        linha_chars.append('1')  # 'X' vira '1' para preenchimento
                    else:
                        linha_chars.append(char)
                matriz.append(linha_chars)

        if not matriz or not matriz[0]:
            raise ValueError("Matriz vazia ou inválida.")

        return matriz, pos_inicial

    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{caminho_arquivo}' não encontrado.")


def renderizar_terminal(matriz: List[List[str]]) -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    linhas_str = []
    for linha in matriz:
        linha_fmt = []
        for val in linha:
            if val == '1':
                linha_fmt.append(' ')   # '1' vira espaço
            elif val == '0':
                linha_fmt.append('#')   # '0' representa borda/parede
            elif val == '2':
                linha_fmt.append('@')   # Preenchido
            elif val == '3':
                linha_fmt.append('.')   # Caminho do Labirinto
            else:
                linha_fmt.append(val)
        linhas_str.append("".join(linha_fmt))
    
    print("\n".join(linhas_str))
    print("=" * len(matriz[0]))


def _checar_e_pausar(passos: int, contador: int, matriz: List[List[str]]) -> int:
    contador += 1
    if passos > 0 and contador % passos == 0:
        renderizar_terminal(matriz)
        input(f"Passo {contador}. Pressione ENTER para continuar...")
    return contador


# ==========================================
# SOLUÇÃO 1: RECURSIVA (FLOOD FILL)
# ==========================================
def flood_fill_recursivo(
    matriz: List[List[str]], 
    r: int, 
    c: int, 
    passos: int = 0, 
    contador: List[int] = [0]
) -> bool:
    rows, cols = len(matriz), len(matriz[0])
    
    # Verifica limites ou se a célula não é '1'
    if r < 0 or r >= rows or c < 0 or c >= cols or matriz[r][c] != '1':
        return False

    # Marca a célula com o caractere de preenchimento
    matriz[r][c] = '2'
    contador[0] = _checar_e_pausar(passos, contador[0], matriz)

    # Chamadas recursivas nas 4 direções
    toca_borda = (r == 0 or r == rows - 1 or c == 0 or c == cols - 1)
    
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if flood_fill_recursivo(matriz, r + dr, c + dc, passos, contador):
            toca_borda = True

    return toca_borda


# ==========================================
# SOLUÇÃO 2: ITERATIVA COM PILHA (FLOOD FILL)
# ==========================================
def flood_fill_iterativo(
    matriz: List[List[str]], 
    r_init: int, 
    c_init: int, 
    passos: int = 0
) -> None:
    rows, cols = len(matriz), len(matriz[0])
    if matriz[r_init][c_init] != '1':
        return

    pilha_posicoes = Pilha('i', rows * cols)
    
    matriz[r_init][c_init] = '2'
    pilha_posicoes.empilha(r_init * cols + c_init)
    contador = 0
    toca_borda = False

    while not pilha_posicoes.pilha_esta_vazia():
        idx_1d = pilha_posicoes.desempilha()
        r, c = idx_1d // cols, idx_1d % cols

        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            toca_borda = True

        contador = _checar_e_pausar(passos, contador, matriz)

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matriz[nr][nc] == '1':
                matriz[nr][nc] = '2'
                pilha_posicoes.empilha(nr * cols + nc)

    # Se vazou a borda, preenche toda a matriz com zeros
    if toca_borda:
        for r_idx in range(rows):
            for c_idx in range(cols):
                matriz[r_idx][c_idx] = '0'


# ==========================================
# EXPORTAÇÃO BITMAP (PPM)
# ==========================================
def salvar_bitmap_ppm(matriz: List[List[str]], caminho_saida: str) -> None:
    rows = len(matriz)
    cols = len(matriz[0])
    
    cores = {
        '1': "255 255 255 ",  # Fundo branco
        '0': "0 0 0 ",        # Parede preta
        '2': "255 0 0 ",      # Preenchimento vermelho
        '3': "0 255 0 ",      # Labirinto verde
    }

    buffer = [f"P3\n{cols} {rows}\n255\n"]
    for linha in matriz:
        linha_buffer = []
        for val in linha:
            linha_buffer.append(cores.get(val, "128 128 128 "))
        buffer.append("".join(linha_buffer) + "\n")

    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.writelines(buffer)


if __name__ == "__main__":
    pasta_script = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(pasta_script, "matriz.txt")

    if os.path.exists(caminho):
        matriz, pos_inicial = carregar_matriz(caminho)
        
        if pos_inicial:
            r, c = pos_inicial
            
            # Exibe a matriz inicial
            print("Matriz Inicial:")
            renderizar_terminal(matriz)
            input("Pressione ENTER para iniciar a execução...")

            # Execução com Pilha (mude para flood_fill_recursivo se desejar)
            flood_fill_iterativo(matriz, r, c, passos=5)
            
            print("Matriz Final:")
            renderizar_terminal(matriz)
            salvar_bitmap_ppm(matriz, os.path.join(pasta_script, "resultado.ppm"))
        else:
            print("Erro: Posição 'X' não encontrada no arquivo de entrada.")
    else:
        print(f"Erro: Arquivo '{caminho}' não encontrado.")

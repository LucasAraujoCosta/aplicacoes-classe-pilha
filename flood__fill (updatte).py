import os
import sys
from typing import List, Tuple, Optional, Dict
from pilha import Pilha

# ==========================================
# PALETA DE CORES (TERMINAL E PPM BITMAP)
# ==========================================
# Mapeia identificadores de cor para (Caractere Terminal, Código RGB PPM)
PALETA_CORES: Dict[str, Tuple[str, str]] = {
    'VERMELHO': ('@', "255 0 0 "),
    'VERDE':    ('$', "0 255 0 "),
    'AZUL':     ('%', "0 0 255 "),
    'AMARELO':  ('&', "255 255 0 "),
    'ROXO':     ('M', "128 0 128 "),
    'CIANO':    ('C', "0 255 255 "),
}

def carregar_matriz(caminho_arquivo: str) -> Tuple[List[List[str]], Optional[Tuple[int, int]]]:
    matriz = []
    pos_inicial = None

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8-sig') as f:
            for r, linha in enumerate(f):
                linha_limpa = linha.strip().replace(" ", "")
                if not linha_limpa:
                    continue
                
                linha_chars = []
                for c, char in enumerate(linha_limpa):
                    if char.upper() == 'X':
                        pos_inicial = (r, c)
                        linha_chars.append('1')  # 'X' vira '1' para preenchimento
                    elif char in ('0', '1'):
                        linha_chars.append(char)
                
                if linha_chars:
                    matriz.append(linha_chars)

        if not matriz:
            raise ValueError("O arquivo não contém uma matriz válida.")

        return matriz, pos_inicial

    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{caminho_arquivo}' não foi encontrado.")

# ==========================================
# RENDERIZAÇÃO NO TERMINAL
# ==========================================
def renderizar_terminal(matriz: List[List[str]], paleta: Dict[str, Tuple[str, str]]) -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    linhas_str = []
    
    # Mapeia o caractere da cor de volta para exibição
    mapa_char = {v[0]: v[0] for v in paleta.values()}

    for linha in matriz:
        linha_fmt = []
        for val in linha:
            if val == '1':
                linha_fmt.append(' ')   # '1' é região livre -> vira espaço
            elif val == '0':
                linha_fmt.append('#')   # '0' é parede -> vira '#'
            elif val in mapa_char:
                linha_fmt.append(val)   # Exibe o caractere da cor escolhida
            else:
                linha_fmt.append(val)
        linhas_str.append("".join(linha_fmt))
    
    print("\n".join(linhas_str))
    print("=" * len(matriz[0]))

def _checar_e_pausar(passos: int, contador: int, matriz: List[List[str]], paleta: Dict[str, Tuple[str, str]]) -> int:
    contador += 1
    if passos > 0 and contador % passos == 0:
        renderizar_terminal(matriz, paleta)
        input(f"Passo {contador}. Pressione [ENTER] para continuar...")
    return contador

# ==========================================
# FLOOD FILL COM CORES (ITERATIVO COM PILHA)
# ==========================================
def flood_fill_paint(
    matriz: List[List[str]], 
    r_init: int, 
    c_init: int, 
    char_cor: str = '@',
    passos: int = 0
) -> None:
    """
    Preenche uma região com uma cor especificada (char_cor) usando a TAD Pilha.
    Se a borda for aberta (vazamento), preenche toda a matriz com '0's.
    """
    rows, cols = len(matriz), len(matriz[0])
    cor_alvo = matriz[r_init][c_init]

    # Só preenche se a célula não for parede ('0') e for diferente da cor de destino
    if cor_alvo == '0' or cor_alvo == char_cor:
        return

    pilha_posicoes = Pilha('i', rows * cols)
    
    matriz[r_init][c_init] = char_cor
    pilha_posicoes.empilha(r_init * cols + c_init)
    
    contador = 0
    toca_borda = False

    while not pilha_posicoes.pilha_esta_vazia():
        idx_1d = pilha_posicoes.desempilha()
        r, c = idx_1d // cols, idx_1d % cols

        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            toca_borda = True

        contador = _checar_e_pausar(passos, contador, matriz, PALETA_CORES)

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matriz[nr][nc] == cor_alvo:
                matriz[nr][nc] = char_cor
                pilha_posicoes.empilha(nr * cols + nc)

    # Requisito do enunciado: Se a borda for aberta, a matriz inteira vira zeros
    if toca_borda:
        for r_idx in range(rows):
            for c_idx in range(cols):
                matriz[r_idx][c_idx] = '0'

# ==========================================
# EXPORTAÇÃO BITMAP (PPM COM CORES MS-PAINT)
# ==========================================
def salvar_bitmap_ppm(matriz: List[List[str]], caminho_saida: str) -> None:
    rows = len(matriz)
    cols = len(matriz[0])
    
    # Mapeamento dinâmico de cores RGB
    mapa_rgb = {
        '1': "255 255 255 ",  # Fundo livre = Branco
        '0': "0 0 0 ",        # Parede/Borda = Preto
    }
    for _, (char_c, rgb) in PALETA_CORES.items():
        mapa_rgb[char_c] = rgb

    buffer = [f"P3\n{cols} {rows}\n255\n"]
    for linha in matriz:
        linha_buffer = []
        for val in linha:
            linha_buffer.append(mapa_rgb.get(val, "128 128 128 "))
        buffer.append("".join(linha_buffer) + "\n")

    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.writelines(buffer)


# ==========================================
# EXECUÇÃO INTERATIVA
# ==========================================
if __name__ == "__main__":
    pasta_script = os.path.dirname(os.path.abspath(__file__))
    caminho_txt = os.path.join(pasta_script, "matriz.txt")

    if os.path.exists(caminho_txt):
        matriz, pos_inicial = carregar_matriz(caminho_txt)
        
        if pos_inicial:
            r, c = pos_inicial
            
            print("===========================================")
            print("       FERRAMENTA PAINT - FLOOD FILL       ")
            print("===========================================")
            print("Escolha a cor de preenchimento:")
            
            opcoes_cores = list(PALETA_CORES.keys())
            for idx, cor in enumerate(opcoes_cores, 1):
                print(f"[{idx}] {cor}")
            
            idx_escolha = input("Digite o número da cor desejada [Padrão 1 - VERMELHO]: ").strip()
            idx_escolha = int(idx_escolha) - 1 if idx_escolha.isdigit() and 1 <= int(idx_escolha) <= len(opcoes_cores) else 0
            
            nome_cor_escolhida = opcoes_cores[idx_escolha]
            char_cor, _ = PALETA_CORES[nome_cor_escolhida]

            passos_input = input("Digite a quantidade P de passos para pausa (0 = sem paradas): ").strip()
            passos = int(passos_input) if passos_input.isdigit() else 0

            print("\nMatriz Original:")
            renderizar_terminal(matriz, PALETA_CORES)
            input("Pressione [ENTER] para iniciar o preenchimento...")

            # Executa o preenchimento com a cor selecionada
            flood_fill_paint(matriz, r, c, char_cor=char_cor, passos=passos)

            print(f"\nMatriz Final (Preenchida com {nome_cor_escolhida}):")
            renderizar_terminal(matriz, PALETA_CORES)
            
            caminho_ppm = os.path.join(pasta_script, f"resultado_{nome_cor_escolhida.lower()}.ppm")
            salvar_bitmap_ppm(matriz, caminho_ppm)
            print(f"Imagem Bitmap gerada em: {caminho_ppm}")

        else:
            print("Erro: Posição 'X' não encontrada na matriz.")
    else:
        print(f"Erro: Arquivo '{caminho_txt}' não encontrado.")

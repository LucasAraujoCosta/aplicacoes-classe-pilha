import os
import sys
from typing import Dict, List
from pilha import Pilha, PilhaCheiaErro, PilhaVaziaErro

class TorreDeHanoi:
    """
    Solução recursiva e visual para a Torre de Hanói usando a classe Pilha.
    """
    def __init__(self, n_discos: int, passo_pausa: int = 1):
        if n_discos <= 0:
            raise ValueError("O número de discos N deve ser um inteiro positivo.")
        
        self.n = n_discos
        self.passo_pausa = passo_pausa
        self.total_passos = 0

        # Instancia as 3 hastes usando a TAD Pilha de capacidade N
        self.pinos: Dict[str, Pilha] = {
            'A': Pilha('i', n_discos),
            'B': Pilha('i', n_discos),
            'C': Pilha('i', n_discos)
        }

        # Inicializa a haste 'A' com discos de N até 1 (maior no fundo)
        for disco in range(n_discos, 0, -1):
            self.pinos['A'].empilha(disco)

    def _obter_estado_pinos(self) -> Dict[str, List[int]]:
        """
        Inspeciona os elementos das pilhas sem violar o encapsulamento
        (desempilhando temporariamente e re-empilhando).
        Retorna uma lista onde o índice 0 é o fundo da haste e o topo é o último elemento.
        """
        estado = {}
        for nome, pilha in self.pinos.items():
            elementos = []
            while not pilha.pilha_esta_vazia():
                elementos.append(pilha.desempilha())
            
            # Restaura a pilha na ordem original
            for item in reversed(elementos):
                pilha.empilha(item)
                
            # Inverte para ter a base no índice 0 e o topo no final
            estado[nome] = list(reversed(elementos))
        return estado

    def renderizar_horizontal(self) -> None:
        """Exibe o estado das pilhas em formato de lista horizontal."""
        estado = self._obter_estado_pinos()
        print("Posição Horizontal (Listas):")
        mapeamento_nomes = {'A': 'Pino Inicial (A)', 'B': 'Pino Auxiliar (B)', 'C': 'Pino Destino (C)'}
        for pino in ['A', 'B', 'C']:
            # Inverte para exibir o topo da pilha à direita
            print(f"{mapeamento_nomes[pino]}: [ {' '.join(map(str, estado[pino]))} ]")
        print()

    def renderizar_vertical(self) -> None:
        """
        Renderiza as hastes e discos verticalmente no terminal em formato ASCII.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"=== TORRE DE HANÓI (Passos acumulados: {self.total_passos}) ===\n")

        self.renderizar_horizontal()

        largura_max_disco = self.n
        largura_pino = (largura_max_disco * 2) + 3  # Largura total de cada pino visual
        estado = self._obter_estado_pinos()

        print("Exibição Vertical:\n")
        # Desenha da ponta do pino para a base
        for nivel in range(self.n - 1, -1, -1):
            linha_str = ""
            for pino in ['A', 'B', 'C']:
                discos = estado[pino]
                if nivel < len(discos):
                    tam = discos[nivel]
                    desenho_disco = ("#" * tam) + "|" + ("#" * tam)
                else:
                    desenho_disco = "|"
                
                linha_str += desenho_disco.center(largura_pino + 2)
            print(linha_str)

        # Base dos pinos
        base = "_" * (largura_pino)
        linha_base = "".join([f"{base}".center(largura_pino + 2) for _ in range(3)])
        print(linha_base)

        # Rótulo dos Pinos
        rotulos = "".join([f"[{p}]".center(largura_pino + 2) for p in ['A', 'B', 'C']])
        print(rotulos)
        print("\n" + "=" * len(linha_base) + "\n")

    def _mover_disco(self, origem: str, destino: str) -> None:
        """Executa a movimentação de um único disco e verifica pausa por M passos."""
        disco = self.pinos[origem].desempilha()
        self.pinos[destino].empilha(disco)
        self.total_passos += 1

        # Verifica se atingiu a quantidade M de movimentações
        if self.passo_pausa > 0 and (self.total_passos % self.passo_pausa == 0):
            self.renderizar_vertical()
            input(f"Passos acumulados: {self.total_passos}. Pressione [ENTER] para continuar...")

    def resolver_recursivo(self, n: int, origem: str, destino: str, auxiliar: str) -> None:
        """Rotina recursiva clássica da Torre de Hanói."""
        if n == 1:
            self._mover_disco(origem, destino)
            return

        self.resolver_recursivo(n - 1, origem, auxiliar, destino)
        self._mover_disco(origem, destino)
        self.resolver_recursivo(n - 1, auxiliar, destino, origem)

    def iniciar(self) -> None:
        """Inicia e gerencia o ciclo de solução da Torre de Hanói."""
        self.renderizar_vertical()
        input("Posição Inicial (0 passos). Pressione [ENTER] para iniciar a solução...")
        
        self.resolver_recursivo(self.n, 'A', 'C', 'B')
        
        # Garante a exibição do estado final
        self.renderizar_vertical()
        print(f"Solução Concluída!")
        print(f"Total de movimentos realizados: {self.total_passos} (Mínimo teórico: {2**self.n - 1})")


# ==========================================
# INTERFACE COM O USUÁRIO
# ==========================================
if __name__ == "__main__":
    print("==========================================")
    print("      PROGRAMA - TORRE DE HANÓI           ")
    print("==========================================")

    try:
        n_input = input("Digite o número de discos (N) [Padrão: 3]: ").strip()
        n_discos = int(n_input) if n_input else 3

        m_input = input("Digite a frequência de passos para visualização (M) [Padrão: 1]: ").strip()
        passo_pausa = int(m_input) if m_input else 1

        if n_discos <= 0 or passo_pausa < 0:
            print("Erro: N deve ser > 0 e M deve ser >= 0.")
            sys.exit(1)

        jogo = TorreDeHanoi(n_discos=n_discos, passo_pausa=passo_pausa)
        jogo.iniciar()

    except ValueError:
        print("Entrada inválida! Insira números inteiros.")

import os
from typing import Dict, List
from pilha import Pilha

class TorreDeHanoi:
    """
    Solução recursiva e visual para a Torre de Hanói usando a classe Pilha de pilha.py.
    """
    def __init__(self, n_discos: int, passo_pausa: int = 1):
        if n_discos <= 0:
            raise ValueError("O número de discos N deve ser um inteiro positivo.")
        
        self.n = n_discos
        self.passo_pausa = passo_pausa
        self.total_passos = 0

        # Instancia as 3 hastes usando obrigatoriamente a classe Pilha
        self.pinos: Dict[str, Pilha] = {
            'A': Pilha('i', n_discos),
            'B': Pilha('i', n_discos),
            'C': Pilha('i', n_discos)
        }

        # Inicializa a haste A com os discos (maior no fundo)
        for disco in range(n_discos, 0, -1):
            self.pinos['A'].empilha(disco)

    def _obter_estado_pinos(self) -> Dict[str, List[int]]:
        """
        Lê os elementos das pilhas de forma limpa desempilhando e re-empilhando,
        evitando acessar o atributo privado '_dados' diretamente.
        """
        estado = {}
        for nome, pilha in self.pinos.items():
            elementos = []
            # Desempilha temporariamente para ler o conteúdo
            while not pilha.pilha_esta_vazia():
                elementos.append(pilha.desempilha())
            
            # Restaura a pilha na ordem original
            for item in reversed(elementos):
                pilha.empilha(item)
                
            # Inverte a lista para que o índice 0 seja o fundo da haste
            estado[nome] = list(reversed(elementos))
        return estado

    def renderizar_horizontal(self) -> None:
        """Exibe o estado das pilhas em formato de lista horizontal."""
        estado = self._obter_estado_pinos()
        print("Exibição Horizontal (Listas):")
        for pino in ['A', 'B', 'C']:
            print(f"Pino {pino}: {estado[pino]}")
        print()

    def renderizar_vertical(self) -> None:
        """
        Renderiza as hastes e discos proporcionalmente no terminal.
        Usa o caractere '#' para os discos e '|' para o pino central.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"=== TORRE DE HANÓI (Passo: {self.total_passos}) ===\n")

        self.renderizar_horizontal()

        largura_max = self.n * 2 + 1
        estado = self._obter_estado_pinos()

        # Desenha de cima para baixo
        for nivel in range(self.n - 1, -1, -1):
            linha_str = ""
            for pino in ['A', 'B', 'C']:
                discos = estado[pino]
                if nivel < len(discos):
                    tam = discos[nivel]
                    desenho_disco = ("#" * tam) + "|" + ("#" * tam)
                else:
                    desenho_disco = "|"
                
                linha_str += desenho_disco.center(largura_max + 2)
            print(linha_str)

        base_str = "".join([f"[{p}]".center(largura_max + 2) for p in ['A', 'B', 'C']])
        print("-" * len(base_str))
        print(base_str)
        print("\n")

    def _mover_disco(self, origem: str, destino: str) -> None:
        disco = self.pinos[origem].desempilha()
        self.pinos[destino].empilha(disco)
        self.total_passos += 1

        if self.passo_pausa > 0 and (self.total_passos % self.passo_pausa == 0):
            self.renderizar_vertical()
            input(f"Avançar para o próximo passo? (Passo atual: {self.total_passos}) [ENTER]...")

    def resolver_recursivo(self, n: int, origem: str, destino: str, auxiliar: str) -> None:
        if n == 1:
            self._mover_disco(origem, destino)
            return

        self.resolver_recursivo(n - 1, origem, auxiliar, destino)
        self._mover_disco(origem, destino)
        self.resolver_recursivo(n - 1, auxiliar, destino, origem)

    def iniciar(self) -> None:
        """Inicia a execução da Torre de Hanói."""
        self.renderizar_vertical()
        input("Posição Inicial (0 Passos). Pressione ENTER para iniciar a resolução...")
        self.resolver_recursivo(self.n, 'A', 'C', 'B')
        self.renderizar_vertical()
        print(f"Concluído com sucesso em {self.total_passos} passos!")
if __name__ == "__main__":
    torre = TorreDeHanoi(n_discos=3, passo_pausa=1)
    torre.iniciar()

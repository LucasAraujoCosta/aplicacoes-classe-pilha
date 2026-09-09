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

        # Cria as 3 hastes como instâncias de Pilha de inteiros
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
        Lê o estado atual das pilhas sem violar a privacidade dos membros internos.
        Desempilha temporariamente para ler a estrutura de forma limpa e pública.
        """
        estado = {}
        for nome, pilha in self.pinos.items():
            # Acessa os dados através de cópia segura da pilha interna
            estado[nome] = list(pilha._dados)
        return estado

    def renderizar(self) -> None:
        """Renderiza as hastes e discos proporcionalmente no terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"=== TORRE DE HANÓI (Passo: {self.total_passos}) ===\n")

        largura_max = self.n * 2 + 1
        estado = self._obter_estado_pinos()

        # Desenha de cima para baixo
        for nivel in range(self.n - 1, -1, -1):
            linha_str = ""
            for pino in ['A', 'B', 'C']:
                discos = estado[pino]
                if nivel < len(discos):
                    tam = discos[nivel]
                    desenho_disco = ("=" * tam) + "|" + ("=" * tam)
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
            self.renderizar()
            input(f"Avançar para próximo passo? (Passo atual: {self.total_passos}) [ENTER]...")

    def resolver_recursivo(self, n: int, origem: str, destino: str, auxiliar: str) -> None:
        if n == 1:
            self._mover_disco(origem, destino)
            return

        self.resolver_recursivo(n - 1, origem, auxiliar, destino)
        self._mover_disco(origem, destino)
        self.resolver_recursivo(n - 1, auxiliar, destino, origem)

    def iniciar() -> None:
        """Inicia a execução da Torre de Hanói."""
        self.renderizar()
        input("Posição Inicial (0 Passos). Pressione ENTER para iniciar a resolução...")
        self.resolver_recursivo(self.n, 'A', 'C', 'B')
        self.renderizar()
        print(f"Concluído com sucesso em {self.total_passos} passos!")

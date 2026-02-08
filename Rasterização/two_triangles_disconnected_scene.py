from src.base import BaseScene, Color
from src.shapes import Triangle

class Scene(BaseScene):
    def __init__(self):
        super().__init__("Two Triangles Disconnected (Simple)")
        self.background = Color(1, 1, 1)

        # ======= Base igual ao 1.3 (diagonal) =======
        P0 = (0.8, 1.0)   # canto inferior esquerdo
        P1 = (2.0, 3.0)   # topo do meio
        P2 = (2.8, 1.0)   # baixo do meio
        P3 = (4.2, 3.1)   # topo direito

        # Triângulo vermelho (igual ao 1.3)
        self.add(Triangle(P0, P1, P2), Color(1.0, 0.0, 0.0))

        # ======= Distanciar o azul sem complicar =======
        gap = 1.00  # <<< mude isso: 0.05, 0.10, 0.30, 0.60, 1.00 ...

        P1b = (P1[0] + gap, P1[1])
        P2b = (P2[0] + gap, P2[1])
        P3b = (P3[0] + gap, P3[1])

        # Triângulo azul (mesma forma/inclinação, só deslocado)
        self.add(Triangle(P1b, P3b, P2b), Color(0.0, 0.6, 1.0))

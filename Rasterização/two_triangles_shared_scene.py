from src.base import BaseScene, Color
from src.shapes import Triangle

class Scene(BaseScene):
    def __init__(self):
        super().__init__("Two Triangles")
        self.background = Color(1, 1, 1)


        P0 = (0.8, 1.0)   # canto inferior esquerdo (vermelho)
        P1 = (2.0, 3.0)   # vértice de cima (compartilhado)
        P2 = (2.8, 1.0)   # vértice de baixo (compartilhado)  <-- X diferente do P1!
        P3 = (4.2, 3.1)   # canto superior direito (azul)

        
        self.add(Triangle(P0, P1, P2), Color(1.0, 0.0, 0.0))

        self.add(Triangle(P1, P3, P2), Color(0.0, 0.6, 1.0))

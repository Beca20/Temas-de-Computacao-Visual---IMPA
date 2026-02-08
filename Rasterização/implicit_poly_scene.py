from src.base import BaseScene, Color
from src.shapes import ImplicitFunction

class Scene(BaseScene):
    def __init__(self):
        super().__init__("Implicit Polynomial Region")
        self.background = Color(1, 1, 1)

        def f(p):
            x, y = p
            return (
                0.004
                + 0.110*x
                - 0.177*y
                - 0.174*(x**2)
                + 0.224*x*y
                - 0.303*(y**2)
                - 0.168*(x**3)
                + 0.327*(x**2)*y
                - 0.087*x*(y**2)
                - 0.013*(y**3)
                + 0.235*(x**4)
                - 0.667*(x**3)*y
                + 0.745*(x**2)*(y**2)
                - 0.029*x*(y**3)
                + 0.072*(y**4)
            )

        # ImplicitFunction considera "dentro" quando f(x,y) <= 0
        self.add(ImplicitFunction(f), Color(0, 0, 0))

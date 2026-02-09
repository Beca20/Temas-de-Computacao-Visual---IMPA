import math
from src.base import BaseScene, Color
from src.shapes import ImplicitFunction


ANGLE_DEG = 30.0  
ANGLE_RAD = math.radians(ANGLE_DEG)

CENTER = (0.15, 0.5)


def rotate_point(p, center, ang):
    x, y = p
    cx, cy = center

    x -= cx
    y -= cy

    c = math.cos(ang)
    s = math.sin(ang)

    xr = x * c - y * s
    yr = x * s + y * c

    return (xr + cx, yr + cy)


class Scene(BaseScene):
    def __init__(self):
        super().__init__(f"Implicit Rotated ({ANGLE_DEG} deg)")
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
        def f_rot(p):
            p_unrot = rotate_point(p, CENTER, -ANGLE_RAD)
            return f(p_unrot)

        self.add(ImplicitFunction(f_rot), Color(0, 0, 0))

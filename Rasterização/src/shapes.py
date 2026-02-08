from .base import Shape

class Circle(Shape):
    def __init__(self, center, radius):
        super().__init__("circle")
        self.center = center
        self.radius = radius

    def in_out(self, point):
        dx = point[0] - self.center[0]
        dy = point[1] - self.center[1]
        return (dx * dx + dy * dy) <= (self.radius * self.radius)

class Triangle(Shape):
    def __init__(self, vertex1, vertex2, vertex3):
        super().__init__("triangle")
        self.v1 = vertex1
        self.v2 = vertex2
        self.v3 = vertex3

        # Bounding box (acelera rejeição rápida)
        xs = (self.v1[0], self.v2[0], self.v3[0])
        ys = (self.v1[1], self.v2[1], self.v3[1])
        self.min_x = min(xs)
        self.max_x = max(xs)
        self.min_y = min(ys)
        self.max_y = max(ys)

        # Área assinada *2 (pra detectar degeneração)
        self.area2 = self._edge(self.v1, self.v2, self.v3)

    @staticmethod
    def _edge(a, b, p):
        # z do produto vetorial 2D: (b-a) x (p-a)
        return (p[0] - a[0]) * (b[1] - a[1]) - (p[1] - a[1]) * (b[0] - a[0])

    def in_out(self, point):
        x, y = point

        # Triângulo degenerado (área ~ 0): não contém nada
        if abs(self.area2) < 1e-18:
            return False

        # Rejeição rápida pelo bounding box
        if x < self.min_x or x > self.max_x or y < self.min_y or y > self.max_y:
            return False

        eps = 1e-12

        e1 = self._edge(self.v1, self.v2, point)
        e2 = self._edge(self.v2, self.v3, point)
        e3 = self._edge(self.v3, self.v1, point)

        # Dentro se não há mistura de sinais (borda conta como dentro)
        has_neg = (e1 < -eps) or (e2 < -eps) or (e3 < -eps)
        has_pos = (e1 >  eps) or (e2 >  eps) or (e3 >  eps)

        return not (has_neg and has_pos)
    
    
class ImplicitFunction(Shape):
    def __init__(self, function):
        super().__init__("implicit_function")
        self.func = function

    def in_out(self, point):
        return self.func(point) <= 0
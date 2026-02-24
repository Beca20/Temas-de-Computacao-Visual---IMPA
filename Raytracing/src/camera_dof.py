import math
import random
from .ray import Ray


class ThinLensCamera:

    def __init__(
        self,
        eye,
        look_at,
        up,
        fov,
        img_width,
        img_height,
        lens_radius=0.0,
        d=1.0,
        f=None,
        zoom=1.0,
    ):
        self.eye = eye
        self.img_width = img_width
        self.img_height = img_height

        self.w = (eye - look_at).normalize()
        up = up.normalize()
        self.u = up.cross(self.w).normalize()
        self.v = self.w.cross(self.u).normalize()

        aspect_ratio = img_height / img_width
        self.su = 2 * math.tan(math.radians(fov) / 2)
        self.sv = self.su * aspect_ratio

        self.lens_radius = float(lens_radius)
        self.d = float(d)
        self.zoom = float(zoom)

        if f is None:
            self.f = (look_at - eye).length()
        else:
            self.f = float(f)

    def _sample_unit_disk(self):
        r = math.sqrt(random.random())
        t = 2.0 * math.pi * random.random()
        return r * math.cos(t), r * math.sin(t)

    def _ray_direction(self, px, py, lx, ly):
        pfx = px * self.f / self.d
        pfy = py * self.f / self.d

        direction = (self.u * (pfx - lx)) + (self.v * (pfy - ly)) - (self.w * self.f)
        return direction.normalize()

    def ray(self, x, y):
       
        px = (self.su * (x / self.img_width) - self.su / 2.0) / self.zoom
        py = (self.sv * (y / self.img_height) - self.sv / 2.0) / self.zoom

        if self.lens_radius <= 0.0:
            p_view = self.eye + self.u * px + self.v * py - self.w * self.d
            return Ray(self.eye, (p_view - self.eye).normalize())

        # sample point no disco unitário -> ponto na lente
        dx, dy = self._sample_unit_disk()
        lx = dx * self.lens_radius
        ly = dy * self.lens_radius

        # origem do raio (na lente): eye + lx*u + ly*v
        origin = self.eye + self.u * lx + self.v * ly

        # direção segundo Listing 10.3
        direction = self._ray_direction(px, py, lx, ly)

        return Ray(origin, direction)
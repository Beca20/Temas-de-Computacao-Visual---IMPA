import numpy as np
from .ray import Ray
from src.vector3d import Vector3D
from .base import Shape, HitRecord, CastEpsilon


class Ball(Shape):
    def __init__(self, center, radius):
        super().__init__("ball")
        self.center = center
        self.radius = radius

    def hit(self, ray):
        # Ray-sphere intersection
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return HitRecord(False, float('inf'), None, None)
        else:
            hit, point, normal = False, None, None
            t = (-b - discriminant**0.5) / (2.0 * a)
            if t > CastEpsilon:
                hit = True
                point = ray.point_at_parameter(t)
                normal = (point - self.center).normalize()
            else:
                t = (-b + discriminant**0.5) / (2.0 * a)
                if t > CastEpsilon:
                    hit = True
                    point = ray.point_at_parameter(t)
                    normal = (point - self.center).normalize()

            return HitRecord(hit, t, point, normal)

class Plane(Shape):
    def __init__(self, point, normal):
        super().__init__("plane")
        self.point = point
        self.normal = normal.normalize()

    def hit(self, ray):
        denom = self.normal.dot(ray.direction)
        if abs(denom) > 1e-6:
            t = (self.point - ray.origin).dot(self.normal) / denom
            if t >= CastEpsilon:
                point = ray.point_at_parameter(t)
                return HitRecord(True, t, point, self.normal)
        return HitRecord(False, float('inf'), None, None)

class PlaneUV(Shape):
    def __init__(self, point, normal, forward_direction):
        super().__init__("plane")
        self.point = point
        self.normal = normal.normalize()
        self.forward_direction = forward_direction.normalize()
        # compute right direction
        self.right_direction = self.normal.cross(self.forward_direction).normalize()

    def hit(self, ray):
        denom = self.normal.dot(ray.direction)
        if abs(denom) > 1e-6:
            t = (self.point - ray.origin).dot(self.normal) / denom
            if t >= CastEpsilon:
                point = ray.point_at_parameter(t)
                # Calculate UV coordinates
                vec = point - self.point
                u = vec.dot(self.right_direction)
                v = vec.dot(self.forward_direction)
                uv = Vector3D(u, v, 0)
                return HitRecord(True, t, point, self.normal, uv=uv)
        return HitRecord(False, float('inf'), None, None)

class ImplicitFunction(Shape):
    def __init__(self, function):
        super().__init__("implicit_function")
        self.func = function

    def in_out(self, point):
        return self.func(point) <= 0


class Cube(Shape):

    def __init__(self, center: Vector3D, size: float):
        super().__init__("cube")
        self.center = center
        self.size = float(size)
        self.h = self.size / 2.0

    def hit(self, ray):
        # Ray-box intersection using the "slabs" method.
        # Work in cube-local coordinates by translating the ray.
        o = ray.origin - self.center
        d = ray.direction
        h = self.h
        eps = 1e-12

        tmin = -float('inf')
        tmax = float('inf')

        def update_axis(o_c, d_c, min_v, max_v, tmin, tmax):
            if abs(d_c) < eps:
                # Ray is parallel to slab. No hit if origin not within slab.
                if o_c < min_v or o_c > max_v:
                    return None
                return tmin, tmax
            inv_d = 1.0 / d_c
            t1 = (min_v - o_c) * inv_d
            t2 = (max_v - o_c) * inv_d
            if t1 > t2:
                t1, t2 = t2, t1
            tmin = max(tmin, t1)
            tmax = min(tmax, t2)
            if tmax < tmin:
                return None
            return tmin, tmax

        res = update_axis(o.x, d.x, -h, h, tmin, tmax)
        if res is None:
            return HitRecord(False, float('inf'), None, None)
        tmin, tmax = res

        res = update_axis(o.y, d.y, -h, h, tmin, tmax)
        if res is None:
            return HitRecord(False, float('inf'), None, None)
        tmin, tmax = res

        res = update_axis(o.z, d.z, -h, h, tmin, tmax)
        if res is None:
            return HitRecord(False, float('inf'), None, None)
        tmin, tmax = res

        # choose first valid hit
        if tmin > CastEpsilon:
            t = tmin
        elif tmax > CastEpsilon:
            # ray starts inside the cube
            t = tmax
        else:
            return HitRecord(False, float('inf'), None, None)

        point = ray.point_at_parameter(t)
        p_local = point - self.center

        # Determine normal by the closest face.
        tol = 1e-6
        nx = ny = nz = 0.0
        if abs(p_local.x - h) < tol:
            nx = 1.0
        elif abs(p_local.x + h) < tol:
            nx = -1.0
        elif abs(p_local.y - h) < tol:
            ny = 1.0
        elif abs(p_local.y + h) < tol:
            ny = -1.0
        elif abs(p_local.z - h) < tol:
            nz = 1.0
        elif abs(p_local.z + h) < tol:
            nz = -1.0
        else:
            # Fallback: pick axis of maximal absolute coordinate
            ax = abs(p_local.x)
            ay = abs(p_local.y)
            az = abs(p_local.z)
            if ax >= ay and ax >= az:
                nx = 1.0 if p_local.x > 0 else -1.0
            elif ay >= ax and ay >= az:
                ny = 1.0 if p_local.y > 0 else -1.0
            else:
                nz = 1.0 if p_local.z > 0 else -1.0

        normal = Vector3D(nx, ny, nz).normalize()

        if abs(normal.x) > 0.5:      # face ±X -> usa (y,z)
         u = p_local.y + h
         v = p_local.z + h
        elif abs(normal.y) > 0.5:    # face ±Y -> usa (x,z)
            u = p_local.x + h
            v = p_local.z + h
        else:                        # face ±Z -> usa (x,y)
         u = p_local.x + h
         v = p_local.y + h

        uv = Vector3D(u, v, 0.0)

        return HitRecord(True, t, point, normal.normalize(), uv=uv)
      
      


class Cylinder(Shape):

    def __init__(self, center: Vector3D, radius: float, height: float, capped: bool = True):
        super().__init__("cylinder")
        self.center = center
        self.radius = float(radius)
        self.height = float(height)
        self.hz = self.height / 2.0
        self.capped = bool(capped)

    def hit(self, ray):
        # Translate ray into cylinder-local coordinates
        o = ray.origin - self.center
        d = ray.direction
        r = self.radius
        hz = self.hz

        eps = 1e-12
        best_t = float('inf')
        best_point = None
        best_normal = None

        a = d.x * d.x + d.y * d.y
        b = 2.0 * (o.x * d.x + o.y * d.y)
        c = o.x * o.x + o.y * o.y - r * r

        if abs(a) > eps:
            disc = b * b - 4.0 * a * c
            if disc >= 0.0:
                sqrt_disc = disc ** 0.5
                t1 = (-b - sqrt_disc) / (2.0 * a)
                t2 = (-b + sqrt_disc) / (2.0 * a)
                if t1 > t2:
                    t1, t2 = t2, t1

                for t in (t1, t2):
                    if t <= CastEpsilon:
                        continue
                    z = o.z + d.z * t
                    if -hz - 1e-9 <= z <= hz + 1e-9:
                        if t < best_t:
                            p = ray.point_at_parameter(t)
                            p_local = p - self.center
                            n_local = Vector3D(p_local.x, p_local.y, 0.0).normalize()
                            best_t = t
                            best_point = p
                            best_normal = n_local

        if self.capped and abs(d.z) > eps:
            for z_plane, nz in ((hz, 1.0), (-hz, -1.0)):
                t = (z_plane - o.z) / d.z
                if t <= CastEpsilon:
                    continue
                x = o.x + d.x * t
                y = o.y + d.y * t
                if (x * x + y * y) <= r * r + 1e-9:
                    if t < best_t:
                        best_t = t
                        best_point = ray.point_at_parameter(t)
                        best_normal = Vector3D(0.0, 0.0, nz)

        if best_point is None:
            return HitRecord(False, float('inf'), None, None)

        return HitRecord(True, best_t, best_point, best_normal.normalize())
    
class ObjectTransform(Shape):
 

    def __init__(self, obj: Shape, matrix_3x3, translation: Vector3D = None):
        super().__init__("object_transform")
        self.obj = obj

        M = np.array(matrix_3x3, dtype=float)
        if M.shape != (3, 3):
            raise ValueError("ObjectTransform expects a 3x3 matrix.")
        self.M = M
        self.M_inv = np.linalg.inv(self.M)
        self.M_inv_T = self.M_inv.T

        self.t = translation if translation is not None else Vector3D(0, 0, 0)

    def _mv(self, M, v: Vector3D) -> Vector3D:
        x = M[0, 0] * v.x + M[0, 1] * v.y + M[0, 2] * v.z
        y = M[1, 0] * v.x + M[1, 1] * v.y + M[1, 2] * v.z
        z = M[2, 0] * v.x + M[2, 1] * v.y + M[2, 2] * v.z
        return Vector3D(x, y, z)

    def hit(self, ray):
        # WORLD -> OBJECT
        o_shift = ray.origin - self.t
        o_obj = self._mv(self.M_inv, o_shift)
        d_obj_raw = self._mv(self.M_inv, ray.direction)

        # If Ray() normalizes direction, we must correct t back to world.
        s = d_obj_raw.length()
        if s < 1e-12:
            return HitRecord(False, float("inf"), None, None)

        ray_obj = Ray(o_obj, d_obj_raw, depth=ray.depth)

        h = self.obj.hit(ray_obj)
        if not h.hit:
            return HitRecord(False, float("inf"), None, None)

        # t back to world parameterization
        t_world = h.t / s

        # OBJECT -> WORLD
        p_world = self._mv(self.M, h.point) + self.t
        n_world = self._mv(self.M_inv_T, h.normal).normalize()

        return HitRecord(True, t_world, p_world, n_world, uv=h.uv)
    


class AlgebraicSurface(Shape):

    def __init__(self, f, grad_f, box_min: Vector3D, box_max: Vector3D,
                 samples: int = 220, bisect_iters: int = 35, f_eps: float = 1e-6):
        super().__init__("algebraic_surface")
        self.f = f
        self.grad_f = grad_f
        self.bmin = box_min
        self.bmax = box_max
        self.samples = samples
        self.bisect_iters = bisect_iters
        self.f_eps = f_eps

    def _aabb_hit_interval(self, ray):
        o = ray.origin
        d = ray.direction
        eps = 1e-12

        tmin = -float("inf")
        tmax = float("inf")

        def axis_interval(o_c, d_c, min_v, max_v, tmin, tmax):
            if abs(d_c) < eps:
                if o_c < min_v or o_c > max_v:
                    return None
                return tmin, tmax
            inv = 1.0 / d_c
            t1 = (min_v - o_c) * inv
            t2 = (max_v - o_c) * inv
            if t1 > t2:
                t1, t2 = t2, t1
            tmin = max(tmin, t1)
            tmax = min(tmax, t2)
            if tmax < tmin:
                return None
            return tmin, tmax

        r = axis_interval(o.x, d.x, self.bmin.x, self.bmax.x, tmin, tmax)
        if r is None:
            return None
        tmin, tmax = r

        r = axis_interval(o.y, d.y, self.bmin.y, self.bmax.y, tmin, tmax)
        if r is None:
            return None
        tmin, tmax = r

        r = axis_interval(o.z, d.z, self.bmin.z, self.bmax.z, tmin, tmax)
        if r is None:
            return None
        tmin, tmax = r

        return tmin, tmax

    def _bisect_root(self, ray, a, b, fa, fb):
        # assumes sign change or one endpoint near zero
        if abs(fa) < self.f_eps:
            return a
        if abs(fb) < self.f_eps:
            return b

        lo, hi = a, b
        flo, fhi = fa, fb

        for _ in range(self.bisect_iters):
            mid = 0.5 * (lo + hi)
            pmid = ray.point_at_parameter(mid)
            fmid = self.f(pmid)

            if abs(fmid) < self.f_eps:
                return mid

            # keep the side with sign change
            if flo * fmid <= 0.0:
                hi, fhi = mid, fmid
            else:
                lo, flo = mid, fmid

        return 0.5 * (lo + hi)

    def hit(self, ray):
        interval = self._aabb_hit_interval(ray)
        if interval is None:
            return HitRecord(False, float("inf"), None, None)

        t_enter, t_exit = interval
        if t_exit <= CastEpsilon:
            return HitRecord(False, float("inf"), None, None)

        t0 = max(t_enter, CastEpsilon)
        t1 = t_exit
        if t1 <= t0:
            return HitRecord(False, float("inf"), None, None)

        # uniform sampling
        n = max(10, int(self.samples))
        dt = (t1 - t0) / n

        best_t = float("inf")
        best_p = None
        best_n = None

        prev_t = t0
        prev_p = ray.point_at_parameter(prev_t)
        prev_f = self.f(prev_p)

        # if we start very close to the surface
        if abs(prev_f) < self.f_eps:
            g = self.grad_f(prev_p)
            return HitRecord(True, prev_t, prev_p, g.normalize())

        for i in range(1, n + 1):
            t = t0 + i * dt
            p = ray.point_at_parameter(t)
            fv = self.f(p)

            # exact/near hit
            if abs(fv) < self.f_eps:
                if t < best_t:
                    g = self.grad_f(p)
                    best_t, best_p, best_n = t, p, g.normalize()

            # sign change => root in [prev_t, t]
            if prev_f * fv < 0.0:
                root_t = self._bisect_root(ray, prev_t, t, prev_f, fv)
                if root_t > CastEpsilon and root_t < best_t:
                    rp = ray.point_at_parameter(root_t)
                    g = self.grad_f(rp)
                    best_t, best_p, best_n = root_t, rp, g.normalize()

            prev_t, prev_f = t, fv

        if best_p is None:
            return HitRecord(False, float("inf"), None, None)

        return HitRecord(True, best_t, best_p, best_n)



# Mitchel surface
def mitchel_f(p: Vector3D) -> float:
    x, y, z = p.x, p.y, p.z
    r2 = y*y + z*z
    return 4.0 * (x**4 + (r2**2) + 17.0 * (x*x) * r2) - 20.0 * (x*x + r2) + 17.0

def mitchel_grad(p: Vector3D) -> Vector3D:
    x, y, z = p.x, p.y, p.z
    r2 = y*y + z*z
    dx = 16.0*(x**3) + 136.0*x*r2 - 40.0*x
    dy = 16.0*y*r2 + 136.0*(x*x)*y - 40.0*y
    dz = 16.0*z*r2 + 136.0*(x*x)*z - 40.0*z
    return Vector3D(dx, dy, dz)



# Heart surface
def heart_f(p: Vector3D) -> float:
    x, y, z = p.x, p.y, p.z
    A = x*x + (9.0/4.0)*y*y + z*z - 1.0
    return (A**3) - (x*x)*(z**3) - (9.0/80.0)*(y*y)*(z**3)

def heart_grad(p: Vector3D) -> Vector3D:
    x, y, z = p.x, p.y, p.z
    A = x*x + (9.0/4.0)*y*y + z*z - 1.0

    dx = 6.0*x*(A**2) - 2.0*x*(z**3)

    dy = (27.0/2.0)*y*(A**2) - (9.0/40.0)*y*(z**3)

    dz = 6.0*z*(A**2) - 3.0*(x*x)*(z*z) - (27.0/80.0)*(y*y)*(z*z)

    return Vector3D(dx, dy, dz)
import math
from src.base import BaseScene, Color
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import AreaLight
from src.materials import SimpleMaterialWithShadows, CheckerboardMaterial
from src.shapes import PlaneUV, ObjectTransform, AlgebraicSurface, mitchel_f, mitchel_grad, heart_f, heart_grad


def scale(sx, sy, sz):
    return [[sx, 0,  0],
            [0,  sy, 0],
            [0,  0,  sz]]


class Scene(BaseScene):
    def __init__(self):
        super().__init__("Task 3 - Mitchel & Heart")

        self.background = Color(0.72, 0.82, 1.0)
        self.ambient_light = Color(0.12, 0.12, 0.12)
        self.max_depth = 10

        self.camera = Camera(
            eye=Vector3D(14, -14, 9),
            look_at=Vector3D(0.0, 0.0, 1.2),
            up=Vector3D(0, 0, 1),
            fov=32,
            img_width=900,
            img_height=650,
        )

        self.lights = [
            AreaLight(
                position=Vector3D(6, -2, 10),
                look_at=Vector3D(0, 0, 1),
                up=Vector3D(0, 0, 1),
                width=4,
                height=4,
                color=Color(0.8, 0.8, 1),
                intensity=1.6,
            )
        ]

        red = SimpleMaterialWithShadows(
            ambient_coefficient=0.35, diffuse_coefficient=0.8,
            diffuse_color=Color(0.8, 0.2, 0.2),
            specular_coefficient=0.35, specular_color=Color(1, 1, 1),
            specular_shininess=64,
        )
        pink = SimpleMaterialWithShadows(
            ambient_coefficient=0.35, diffuse_coefficient=0.8,
            diffuse_color=Color(0.9, 0.3, 0.5),
            specular_coefficient=0.35, specular_color=Color(1, 1, 1),
            specular_shininess=64,
        )
        ground = CheckerboardMaterial(
            ambient_coefficient=1.0, diffuse_coefficient=0.9,
            square_size=1.0,
            white_color=Color(0.92, 0.92, 0.92),
            black_color=Color(0.18, 0.18, 0.18),
        )

        self.add(
            PlaneUV(
                point=Vector3D(0, 0, 0),
                normal=Vector3D(0, 0, 1),
                forward_direction=Vector3D(1, 1, 0),
            ),
            ground,
        )

        bmin = Vector3D(-2.0, -2.0, -2.0)
        bmax = Vector3D( 2.0,  2.0,  2.0)

        mitchel_obj = AlgebraicSurface(mitchel_f, mitchel_grad, bmin, bmax, samples=260)
        heart_obj   = AlgebraicSurface(heart_f, heart_grad, bmin, bmax, samples=260)

     
        M_mitchel = scale(1.0, 1.0, 1.0)
        M_heart   = scale(1.2, 1.2, 1.2)

        self.add(ObjectTransform(mitchel_obj, M_mitchel, translation=Vector3D(-3.0, 0.0, 2.2)), red)
        self.add(ObjectTransform(heart_obj,   M_heart,   translation=Vector3D( 3.0, 0.0, 1.2)), pink)

        
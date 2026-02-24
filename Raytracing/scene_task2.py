import math
from src.base import BaseScene, Color
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import AreaLight
from src.materials import SimpleMaterialWithShadows, CheckerboardMaterial
from src.shapes import PlaneUV, Cube, ObjectTransform


def rot_z(theta):
    c, s = math.cos(theta), math.sin(theta)
    return [
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1],
    ]


def scale(sx, sy, sz):
    return [
        [sx, 0,  0],
        [0,  sy, 0],
        [0,  0,  sz],
    ]


class Scene(BaseScene):
    def __init__(self):
        super().__init__("Task 2 - ObjectTransform")

        self.background = Color(0.72, 0.82, 1.0)
        self.ambient_light = Color(0.12, 0.12, 0.12)
        self.max_depth = 10

        self.camera = Camera(
            eye=Vector3D(14, -14, 8),
            look_at=Vector3D(0.0, 0.0, 1.0),
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
                color=Color(1, 1, 1),
                intensity=1.4,
            )
        ]

        # materials
        red = SimpleMaterialWithShadows(
            ambient_coefficient=0.4,
            diffuse_coefficient=0.8,
            diffuse_color=Color(0.75, 0.15, 0.15),
            specular_coefficient=0.35,
            specular_color=Color(1, 1, 1),
            specular_shininess=64,
        )
        green = SimpleMaterialWithShadows(
            ambient_coefficient=0.35,
            diffuse_coefficient=0.8,
            diffuse_color=Color(0.15, 0.7, 0.25),
            specular_coefficient=0.35,
            specular_color=Color(1, 1, 1),
            specular_shininess=64,
        )
        blue = SimpleMaterialWithShadows(
            ambient_coefficient=0.35,
            diffuse_coefficient=0.8,
            diffuse_color=Color(0.15, 0.25, 0.8),
            specular_coefficient=0.35,
            specular_color=Color(1, 1, 1),
            specular_shininess=64,
        )
        yellow = SimpleMaterialWithShadows(
            ambient_coefficient=0.35,
            diffuse_coefficient=0.8,
            diffuse_color=Color(0.9, 0.75, 0.15),
            specular_coefficient=0.35,
            specular_color=Color(1, 1, 1),
            specular_shininess=64,
        )
        ground = CheckerboardMaterial(
            ambient_coefficient=1.0,
            diffuse_coefficient=0.9,
            square_size=1.0,
            white_color=Color(0.92, 0.92, 0.92),
            black_color=Color(0.18, 0.18, 0.18),
        )

        # ground plane
        self.add(
            PlaneUV(
                point=Vector3D(0, 0, 0),
                normal=Vector3D(0, 0, 1),
                forward_direction=Vector3D(1, 1, 0),
            ),
            ground,
        )

        base_cube = Cube(center=Vector3D(0, 0, 0), size=2.0)
        z_on_floor = 1.0

        I = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
        self.add(ObjectTransform(base_cube, I, translation=Vector3D(4.5, 0.0, z_on_floor)), red)

        M_rot = rot_z(math.radians(25))
        self.add(ObjectTransform(base_cube, M_rot, translation=Vector3D(1.5, 0.0, z_on_floor)), green)

        M_scale = scale(1.6, 0.8, 1.2)
        self.add(ObjectTransform(base_cube, M_scale, translation=Vector3D(-1.5, 0.0, z_on_floor)), blue)

        k = 0.7
        M_shear = [
            [1.0, k,   0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
        self.add(ObjectTransform(base_cube, M_shear, translation=Vector3D(-4.5, 0.0, z_on_floor)), yellow)
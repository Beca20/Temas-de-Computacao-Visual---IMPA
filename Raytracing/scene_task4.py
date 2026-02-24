from src.base import BaseScene, Color
from src.shapes import Plane, PlaneUV, Ball
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import PointLight
from src.materials import MirrorMaterial, SimpleMaterialWithShadows, CheckerboardMaterial

MAX_DEPTH = 100



class Scene(BaseScene):
    def __init__(self):
        super().__init__("Task 4 - Two Mirrors")

        self.background = Color(0.02, 0.02, 0.03)
        self.ambient_light = Color(0.0, 0.0, 0.0)
        self.max_depth = MAX_DEPTH

        self.camera = Camera(
            eye=Vector3D(-0.8, 0.0, 1.2),
            look_at=Vector3D(1.0, 0.0, 1.2),
            up=Vector3D(0, 0, 1),
            fov=55,
            img_width=900,
            img_height=650,
        )

        self.lights = [
            PointLight(position=Vector3D(0.0, -6.0, 6.0), color=Color(1, 1, 1), intensity=2.8),
        ]

        mirror = MirrorMaterial(reflectance=1.0, tint=Color(1, 1, 1))

        floor = CheckerboardMaterial(
            ambient_coefficient=1.0,
            diffuse_coefficient=0.9,
            square_size=1.0,
            white_color=Color(0.92, 0.92, 0.92),
            black_color=Color(0.18, 0.18, 0.18),
        )

        matte_red = SimpleMaterialWithShadows(
            ambient_coefficient=0.05,
            diffuse_coefficient=0.95,
            diffuse_color=Color(0.9, 0.2, 0.2),
            specular_coefficient=0.0,  
            specular_color=Color(1, 1, 1),
            specular_shininess=32,
        )

        matte_blue = SimpleMaterialWithShadows(
            ambient_coefficient=0.05,
            diffuse_coefficient=0.95,
            diffuse_color=Color(0.2, 0.3, 0.9),
            specular_coefficient=0.0,
            specular_color=Color(1, 1, 1),
            specular_shininess=32,
        )

        self.add(
            PlaneUV(
                point=Vector3D(0, 0, 0),
                normal=Vector3D(0, 0, 1),
                forward_direction=Vector3D(1, 1, 0),
            ),
            floor,
        )

        
        self.add(Plane(point=Vector3D(-2.0, 0.0, 0.0), normal=Vector3D(1, 0, 0)), mirror)
        self.add(Plane(point=Vector3D( 2.0, 0.0, 0.0), normal=Vector3D(-1, 0, 0)), mirror)

        self.add(Ball(center=Vector3D(0.0, 1.0, 1.0), radius=0.55), matte_red)
        self.add(Ball(center=Vector3D(0.6, -0.8, 0.7), radius=0.35), matte_blue) 
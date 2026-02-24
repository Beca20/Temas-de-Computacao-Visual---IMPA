# Scene to test Task 1 objects: Cube + Cylinder
from src.base import BaseScene, Color
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import AreaLight
from src.materials import SimpleMaterialWithShadows, CheckerboardMaterial
from src.shapes import PlaneUV, Cube, Cylinder


class Scene(BaseScene):
    def __init__(self):
        super().__init__("Task 1 - Cube & Cylinder")

        # background + ambient
        self.background = Color(0.72, 0.82, 1.0)
        self.ambient_light = Color(0.12, 0.12, 0.12)
        self.max_depth = 10

        # camera (z is "up" in this project)
        self.camera = Camera(
            eye=Vector3D(10, -10, 6),
            look_at=Vector3D(1.0, 0.0, 1.0),
            up=Vector3D(0, 0, 1),
            fov=35,
            img_width=900,
            img_height=650,
        )

        # soft area light
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

        # materials
        red = SimpleMaterialWithShadows(
            ambient_coefficient=0.4,
            diffuse_coefficient=0.8,
            diffuse_color=Color(0.75, 0.15, 0.15),
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
        ground = CheckerboardMaterial(
            ambient_coefficient=1.0,
            diffuse_coefficient=0.9,
            square_size=1.0,
            white_color=Color(0.92, 0.92, 0.92),
            black_color=Color(0.18, 0.18, 0.18),
        )

        #  objects (natural coords, centered & axis-aligned) 
        self.add(Cube(center=Vector3D(0, 0, 1.0), size=2.0), red)
        self.add(Cylinder(center=Vector3D(3.2, 0.0, 1.0), radius=1.0, height=2.0, capped=True), blue)

        # ground plane with UVs for checkerboard
        self.add(
            PlaneUV(
                point=Vector3D(0, 0, 0),
                normal=Vector3D(0, 0, 1),
                forward_direction=Vector3D(1, 1, 0),
            ),
            ground,
            
        )

from src.base import BaseScene, Color
from src.vector3d import Vector3D
from src.light import PointLight
from src.materials import CheckerboardMaterial
from src.shapes import PlaneUV, Cube, ObjectTransform

from src.camera_dof import ThinLensCamera as Camera

LENS_RADIUS = 0.10    
VIEW_DIST   = 1.00     
FOCAL_DIST  = None     
ZOOM        = 1.00

FOCUS_POINT = Vector3D(0.0, -10.5, 2.2)


def scale(sx, sy, sz):
    return [
        [sx, 0,  0],
        [0,  sy, 0],
        [0,  0,  sz],
    ]


class Scene(BaseScene):
    def __init__(self):
        super().__init__("Task 5 - Thin Lens DOF")


        self.background = Color(0.72, 0.82, 1.0)
        self.ambient_light = Color(0.12, 0.12, 0.12)
        self.max_depth = 10

        self.camera = Camera(
            eye=Vector3D(0.0, -16.0, 2.2),
            look_at=FOCUS_POINT,
            up=Vector3D(0, 0, 1),
            fov=30,
            img_width=900,
            img_height=650,
            lens_radius=LENS_RADIUS,
            d=VIEW_DIST,
            f=FOCAL_DIST,
            zoom=ZOOM,
        )

        self.lights = [
            PointLight(position=Vector3D(4.0, -8.0, 7.0),  color=Color(1, 1, 1), intensity=1.6)        ]

        ground = CheckerboardMaterial(
            ambient_coefficient=0.15,
            diffuse_coefficient=0.9,
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

        dark = Color(0.18, 0.18, 0.18)

        yellow = CheckerboardMaterial(0.15, 0.9, 0.25, white_color=Color(0.95, 0.85, 0.20), black_color=dark)
        green  = CheckerboardMaterial(0.15, 0.9, 0.25, white_color=Color(0.20, 0.85, 0.25), black_color=dark)
        red    = CheckerboardMaterial(0.15, 0.9, 0.25, white_color=Color(0.95, 0.20, 0.20), black_color=dark)

        base = Cube(center=Vector3D(0, 0, 0), size=2.0)
        M_box = scale(0.9, 0.6, 2.4)
        z_on_floor = 1.2

        self.add(ObjectTransform(base, M_box, translation=Vector3D(-2.0, -3.0, z_on_floor)), yellow)
        self.add(ObjectTransform(base, M_box, translation=Vector3D(0.0,  0.0, z_on_floor)), green)
        self.add(ObjectTransform(base, M_box, translation=Vector3D(2.5,  3.0, z_on_floor)), red)
import trimesh

Color = tuple[int, int, int, int]

COLORS: dict[str, Color] = {
    "bark": (92, 64, 45, 255),
    "bark_dark": (60, 40, 28, 255),
    "leaf": (34, 139, 34, 255),
    "leaf_light": (80, 180, 70, 255),
    "leaf_dark": (20, 100, 30, 255),
    "needle": (20, 80, 35, 255),
    "needle_light": (40, 130, 55, 255),
}


def apply_color(mesh: trimesh.Trimesh, color_name: str) -> trimesh.Trimesh:
    mesh.visual.face_colors = COLORS[color_name]
    return mesh

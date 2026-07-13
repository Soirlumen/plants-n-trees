import trimesh

Color = tuple[int, int, int, int]

# Barvy držíme na jednom místě, aby šly měnit bez zásahu do generování meshů.
# Hodnoty jsou RGBA.
COLORS: dict[str, Color] = {
    "bark": (72, 34, 27, 255),
    "bark_dark": (45, 22, 18, 255),
    "leaf": (34, 139, 34, 255),
    "leaf_light": (80, 180, 70, 255),
    "leaf_dark": (20, 100, 30, 255),
    "leaf_purple": (92, 68, 118, 255),
    "leaf_purple_dark": (65, 45, 88, 255),
    "leaf_purple_soft": (118, 92, 145, 255),
    "leaf_sakura_soft": (244, 199, 211, 255),
    "leaf_sakura_dark": (196, 128, 154, 255),
    "leaf_neon_coral": (255, 76, 92, 255),
    "leaf_crimson_pink": (238, 38, 96, 255),
    "leaf_orange": (249, 135, 10, 255),
}


def apply_color(mesh: trimesh.Trimesh, color_name: str) -> trimesh.Trimesh:
    """Přiřadí všem plochám meshe jednu barvu z paletky"""
    mesh.visual.face_colors = COLORS[color_name]
    return mesh

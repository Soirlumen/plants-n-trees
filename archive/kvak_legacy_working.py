import copy

import numpy as np
import trimesh
from trimesh.transformations import rotation_matrix


def do_the_sentence(iterations:int,axiom:str,rules:dict)->str:
     result=axiom
     for x in range(iterations):
          pom=''
          #print(result)
          for y in result:
               pom+=rules.get(y)
               result=pom
     return result
trava = [4,
         'X',
         { 'F':'FF',
           'X':'F-[[X]+X]+F[+FX]-X',
           '[':'[',
           ']':']',
           '+':'+',
           '-':'-'
}]

strom=[3,
     "X",
     {
    "X": "F[+X][-X][&X][^X]FX",  # X = větev (rekurze)
    "F": "FF",                   # F = krok vpřed / segment
           '[':'[',
           ']':']',
           '+':'+',
           '-':'-',
           "&":"&",
           "^":"^",
}]

# === L-system ===
strom=[4,
     "X",
     {
    "X": "F[+X][-X][&X][^X]FX",
    "F": "FF",
           '[':'[',
           ']':']',
           '+':'+',
           '-':'-',
           "&":"&",
           "^":"^",
}]
sentence = do_the_sentence(iterations=strom[0], axiom=strom[1], rules=strom[2])

# === Parametry ===
ANGLE = 27
ANGLE_RAD = np.radians(ANGLE)
SHRINK_LENGTH = 0.95
SHRINK_RADIUS = 0.95

# === Počáteční stav želvy ===
state = {
    "pos": np.array([0.0, 0.0, 0.0]),
    "dir": np.array([0.0, 1.0, 0.0]),  # směrem nahoru
    "length": 0.9,
    "radius": 0.1,
}

stack = []
meshes = []

# === Interpretace L-systemu ===
for char in sentence:

    if char == "F":
        start = state["pos"]
        end = start + state["dir"] * state["length"]

        cyl = trimesh.creation.cylinder(
            radius=state["radius"],
            segment=[start, end],
            sections=5
        )

        meshes.append(cyl)
        state["pos"] = end

        state["length"] *= SHRINK_LENGTH
        state["radius"] *= SHRINK_RADIUS

    elif char == "+":
        # rotace kolem Z (vpravo)
        R = rotation_matrix(ANGLE_RAD, [0, 0, 1])
        state["dir"] = R[:3, :3] @ state["dir"]

    elif char == "-":
        # rotace kolem Z (vlevo)
        R = rotation_matrix(-ANGLE_RAD, [0, 0, 1])
        state["dir"] = R[:3, :3] @ state["dir"]

    elif char == "&":
        # rotace dolů (k X)
        R = rotation_matrix(ANGLE_RAD, [1, 0, 0])
        state["dir"] = R[:3, :3] @ state["dir"]

    elif char == "^":
        # rotace nahoru (k X)
        R = rotation_matrix(-ANGLE_RAD, [1, 0, 0])
        state["dir"] = R[:3, :3] @ state["dir"]

    elif char == "[":
        stack.append(copy.deepcopy(state))

    elif char == "]":
        state = stack.pop()

    elif char == "X":
        pass  # strukturální symbol

# === Export / vizualizace ===
# spojíme všechny meshe do jednoho – rychlejší pro 3D
tree_mesh = trimesh.util.concatenate(meshes)
scene = trimesh.Scene([tree_mesh])

scene.show()  # pokud chceš vizualizaci, můžeš odkomentovat
tree_mesh.export("tree.obj")

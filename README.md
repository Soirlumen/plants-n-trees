Miroslava Novotná, AIPV PGR2 2026
zadání: generování a vizualizace 3D L-systémů z příkazové řádky
výstup: .obj a vizualizace
Presety: stromy, je možné doplnit další
## Řešení:
### L-systém
- abeceda (definované symboly), axiom (počáteční věta), pravidla (na co se znak přepíše)
- opakovaná aplikace pravidel po zadaný počet iterací
- deterministický strom (v presetu jako "tree")
- stochastický (v presetu "stochastic-tree", "oak-tree", "dense-stochastic-tree", "stochastic-grass", "stochastic-bush")
- vytvoření výsledného řetězce představujícího strukturu stromu
#### Grafická interpretace
- pomocí **3D turtle grafiky**
- vytvoření počátečního stavu želvy:
    - pozice
    - orientace (osy Heading, Left, Up)
    - počáteční délka větve
    - počáteční poloměr větve
- postupně se zpracovávají symboly
- mapování symbolů na konkrétní akce:
   - `F` – vytvoření nové větve
   - `+`, `-` – otočení kolem osy Up (doprava/doleva)
   - `&`, `^` – otočení kolem osy Left
   - `\`, `/` – otočení kolem osy Heading
   - `|` – otočení o 180°
   - `[` – uložení aktuálního stavu želvy
   - `]` – obnovení předchozího stavu želvy
   - `X` – růstový parametr/vytvoření listů
### Generování geometrie
- vytvoření větví jako válců
- výpočet počátečního a koncového bodu každé větve
- postupné zkracování délky větví
- postupné zmenšování poloměru větví
- nastavení počtu segmentů válce
- vytváření dvojice listů na koncích větví
- orientace listů podle aktuální orientace větve
- spojení všech vytvořených meshů do jednoho výsledného objektu
### Náhodnost generování
- možnost zadání hodnoty **seed**
- možnost náhodné odchylky úhlů větvení
- pravděpodobnostní výběr přepisovacích pravidel
### Výstup programu
- vytvoření výsledného 3D modelu
- export do formátu OBJ
- možnost zobrazení výsledného modelu

### Spuštění
pokud není nainstalovaný uv
ze stránky: https://docs.astral.sh/uv/getting-started/installation/
**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
* **Mac / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
restartovat commandline!

a následně spustit uv
```
uv sync
uv pip install -e .
```

lze vyzkoušet předpřipravené stromy
```
uv run nudny-strom
uv run strom
uv run jiny-strom
uv run kerik
uv run trava
uv run dalsi-strom
```

anebo do parseru postupně napsat parametry, např.

```
uv run py -m src.lsystem_visualizer.cli --preset dense-stochastic-tree --iterations 6 --angle 29 --shrink-length 0.94 --shrink-radius 0.90 --start-length 0.36 --start-radius 0.15 --leaf-length 0.4 --leaf-width 0.15 --leaf-fork-angle 35 --stochasticity 20 --seed 3854 --leaf-color leaf_purple --show
```

| **Argument (Přepínač)** | **Výchozí hodnota** | **Popis / Význam**                                                                  |
| ----------------------- | ------------------- | ----------------------------------------------------------------------------------- |
| `--preset`              | `"tree"`            | Výběr přednastaveného typu L-systému (omezeno na klíče v `PRESETS`).                |
| `--iterations`          | `None`              | Počet kroků/generací L-systému. Pokud chybí, vezme se hodnota z vybraného preset_u. |
| `--angle`               | `27.0`              | Výchozí úhel rotace želvy ve stupních při změně směru.                              |
| `--shrink-length`       | `0.9`               | Koeficient zkrácení délky větve v každém dalším kroku růstu.                        |
| `--shrink-radius`       | `0.85`              | Koeficient zúžení tloušťky větve v každém dalším kroku růstu.                       |
| `--output`              | `"tree.obj"`        | Cesta a název souboru, kam se výsledný 3D model vyexportuje.                        |
| `--show`                | `False`             | Pokud je zadáno, po vygenerování otevře okno s 3D náhledem modelu.                  |
| `--seed`                | `None`              | Seed pro generátor náhodných čísel (zaručuje stejný tvar při stochastice).          |
| `--stochasticity`       | `0.0`               | Míra náhodnosti / odchylky úhlu větvení (0.0 znamená dokonale geometrický).         |
| `--no-leaves`           | `False`             | Pokud je zadáno, strom se vygeneruje úplně bez listí.                               |
| `--leaf-length`         | `1.2`               | Základní délka jednoho listu.                                                       |
| `--leaf-width`          | `0.6`               | Základní šířka jednoho listu.                                                       |
| `--leaf-fork-angle`     | `40.0`              | Úhel rozevření dvojice listů na konci větve.                                        |
| `--leaf-color`          | `"leaf"`            | Barva listí (omezeno na klíče v registru `COLORS`).                                 |
| `--start-length`        | `0.9`               | Počáteční délka prvního (kmenového) segmentu.                                       |
| `--start-radius`        | `0.1`               | Počáteční poloměr (tloušťka) kmene na startu.                                       |
| `--branch-color`        | `"bark"`            | Barva větví a kmene (omezeno na klíče v registru `COLORS`).                         |

### Zdroje
- PRUSINKIEWICZ, Przemyslaw a LINDENMAYER, Aristid. The Algorithmic Beauty of Plants. Elektronické vydání. Springer-Verlag, 2006. ISBN 978-0-387-94676-4.
- MATEMATICKÉ MODELOVÁNÍ POMOCÍ L-SYSTÉMŮ. Bakalářská práce. Brno: Vysoké učení technické v Brně, Fakulta strojního inženýrství, Ústav matematiky, 2010.
- L-systémy pro interaktívni modelování rostlin. Diplomová. Brno: Masarykova univerzita, Fakulta informatiky, 2013.
- https://chatgpt.com/share/6a493411-0f10-83ed-96c0-094c911b4cc9
- https://share.gemini.google/W4JdJNtp8DE8
- L-system. Online. In: Wikipedia: the free encyclopedia. San Francisco (CA): Wikimedia Foundation, 2001-2026. Dostupné z: https://en.wikipedia.org/wiki/L-system. [cit. 2026-07-07].
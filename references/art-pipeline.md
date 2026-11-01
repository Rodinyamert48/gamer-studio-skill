# Art Pipeline — style, production, naming, import, licensing

The studio cannot paint by hand, so art is produced **programmatically and reproducibly**:
vector (SVG), code-generated pixel art, procedural textures, shader-based visuals, Blender
Python scripts for 3D, or verified-licence external packs. Every generated asset should be
re-creatable from a script or source file kept in the repo.

## 1. Flow
```
Art Director: ART_BIBLE (style, palette, proportions, budgets)
  → Concept Artist: concept sheets / mood boards (SVG/HTML/MD with palette + silhouettes)
    → Character / Environment / Props Artists: production assets (+ source scripts)
      → Technical Artist: import settings, atlases, materials/shaders, budgets check
        → Animator / VFX & Lighting: motion, effects, lighting
          → Art Director review → integrate → QA visual pass
```

## 2. `studio/ART_BIBLE.md` must define
- Style statement (1 paragraph) + 3 visual pillars.
- Palette: 8–24 hex colours with roles (background, foreground, player, enemy, UI, accent, danger).
- Resolution & scale: pixel art base (e.g. 16×16 tiles, 320×180 internal, integer scaling) or
  vector/3D scale (1 unit = 1 m, character height).
- Silhouette & readability rules (player always highest contrast; hazards use danger colour).
- Line, shading and lighting conventions; outline yes/no; light direction.
- Animation style (frame counts, frame rate e.g. 12 fps for pixel art).
- Technical budgets (see §6).

## 3. Production techniques (choose per style)
| Style | Technique |
|---|---|
| Pixel art | Python (Pillow) or JS scripts drawing palette-indexed pixels into PNG sheets; keep the generator script in `tools/art/` |
| Flat / vector | Hand-written SVG; export to PNG at needed sizes (`rsvg-convert`, `inkscape`, Pillow+cairosvg, or Playwright screenshot) or use SVG directly on web |
| Procedural textures | noise (Perlin/simplex), gradients, tiling patterns via Python/numpy or shaders |
| Shader-driven | engine shaders (Godot `.gdshader`, Unity Shader Graph/HLSL, GLSL for web) for water, fog, dissolve, outlines |
| Low-poly 3D | Blender Python (`blender -b -P make_asset.py`) → glTF/GLB; or primitives assembled in-engine |
| Greybox | engine primitives / coloured rectangles with correct collision sizes |
| External packs | only CC0 / CC-BY / explicitly permissive sources (e.g. Kenney.nl CC0, OpenGameArt with per-asset licence check, Poly Haven CC0); log in `studio/ASSET_LICENSES.md` |

Never trace, copy or recreate characters, logos, UI or art from existing commercial games.

## 4. Naming convention
`<category>_<name>[_<variant>][_<state>][_<index>].<ext>` — lowercase `snake_case`.

| Prefix | Use | Example |
|---|---|---|
| `chr_` | characters | `chr_player_idle_sheet.png`, `chr_slime_green_walk_01.png` |
| `env_` | environment/tiles/backgrounds | `env_forest_tileset.png`, `env_bg_mountains_far.png` |
| `prp_` | props/items | `prp_chest_wood_open.png`, `prp_sword_iron.glb` |
| `ui_` | UI | `ui_btn_primary_hover.png`, `ui_icon_coin.svg` |
| `vfx_` | effects | `vfx_hit_spark_sheet.png` |
| `mat_` / `shd_` / `tex_` | materials, shaders, textures | `mat_water.tres`, `shd_outline.gdshader`, `tex_rock_albedo.png` |
| `anm_` | standalone animation data | `anm_player_attack.tres` |
| `fnt_` | fonts | `fnt_main_regular.ttf` |

Sprite sheets: uniform cell size, row = animation, document cell size & frame counts in the
sheet's sidecar (`*.json`) or ART_BIBLE.

## 5. Folder layout (adapt to engine)
```
assets/
  characters/  environment/  props/  ui/  vfx/  fonts/
  _source/        # SVG, .blend, generator inputs (not shipped if engine allows exclusion)
tools/art/        # generator scripts (pixel art, atlas packing, svg export)
```

## 6. Budgets (defaults — Technical Artist adjusts per platform)
| Item | Mobile / Web | Desktop |
|---|---|---|
| 2D sprite sheet | ≤ 2048² per atlas | ≤ 4096² |
| Character (3D) | 1.5–5k tris | 10–30k tris |
| Prop (3D) | 100–2k tris | 500–8k tris |
| Texture | 512–1024² | 1024–2048² (4096 hero only) |
| Draw calls / frame | < 100 | < 1000 (engine dependent) |
| Particles alive | < 500 | < 5000 |

## 7. Import settings
- Pixel art: nearest filtering, no mipmaps, no compression artefacts (lossless), integer scaling, snap to pixel.
- Smooth 2D/UI: linear filtering, mipmaps for scaled content, premultiplied alpha where supported.
- 3D: glTF/GLB preferred; consistent scale/up-axis; generate collision on import only when intended.
- Audio-visual sync data (hit frames) recorded in animation metadata/events.

## 8. Review checklist (Art Director)
- [ ] Matches ART_BIBLE palette/scale/silhouette rules
- [ ] Readable at gameplay size and on target resolutions
- [ ] Named & placed per convention; source/generator committed
- [ ] Within budget; imports cleanly with correct settings
- [ ] Licence recorded for every non-original asset

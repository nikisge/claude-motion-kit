---
name: motion-3d
description: "Use when a motion graphics piece needs real 3D (product shot, metal, glass, depth of field, macro, object that transforms or assembles, camera shot list) in HyperFrames via Three.js, or when 3D models should come from Blender (Blender MCP, headless Blender, glTF/GLB export). Trigger words: 3D, Produktfilm, Metall, Glas, Tiefenunschärfe, Bokeh, Three.js, Blender, GLB."
---

# Motion 3D: echtes 3D in HyperFrames (+ Blender als Modell-Quelle)

Zwei Wege, je nach Ziel:

| Ziel | Weg | Status |
|---|---|---|
| Produkt-/Objektfilm aus Grundformen: Drehteile, Rändelung, Glas, Metall, Leuchtstreifen, Zusammenbau, 3D-Text | **hf3d** (Three.js-Studio in HyperFrames, `hf3d/`) | im Einsatz getestet |
| Komplexe Modelle (Figuren, Fahrzeuge, Architektur), die man nicht aus Grundformen baut | **Blender als Modell-Quelle** → GLB → hf3d | ungetestet, nach Recherche (Oktober 2026) |

Grundsatz: Gerendert wird in HyperFrames (seek-sicher, gleiches Prüfwerkzeug wie der Rest). Blender liefert Modelle,
nicht den Film. Ein echter Blender-Render (Cycles) ist ein eigenes Projekt mit eigenen Renderzeiten.

## Weg 1: hf3d (Three.js-Studio)

```bash
cd projects/<name>/hf
bash <dieser-skill>/hf3d/install.sh . --template    # Three.js r181 + hf3d.js + Schrift nach vendor/hf3d, Vorlage als index.html
npx hyperframes lint
npx hyperframes snapshot --at 0.7,2,3.3 --describe false
```

Was drin ist (API und alle Fallstricke: `hf3d/README.md`):
- `createStudio`: Studio-Umgebung ohne HDR-Datei, Verlauf statt Schwarz, weiche Schatten, Tiefenunschärfe, Bloom,
  Korn/Vignette, ACES. `studioLights` (Key/Rim/Fill).
- `mat.*`: gebürstetes/poliertes Metall, Glas (Transmission + Dispersion), Soft-Touch, Keramik, Hochglanz, Emissive.
- `shotRig`: Shot-Liste mit Start/Ende, Pfad, Brennweite in mm, Fokusziel, Bokeh. Einträge = harte Schnitte, Pfade = Fahrten.
- Helfer: `lathe`, `knurl`, `roundedBox`, `ribbon`, `extrudeText`, `extrudeSVG`, `Swarm` (Instancing: Morph,
  Explosion, Zusammenbau).
- Beispiel: `examples/rondo/index.html` (10 Einstellungen in 9,6 s; Render ~2 min, Speicherspitze ~1,8 GB auf einem
  MacBook mit 24 GB).

Die fünf häufigsten Fehler:
1. Root ohne `data-no-timeline` (wenn keine GSAP-Timeline): Lint-Fehler und lange Wartezeit je Render.
2. Metall ohne Umgebung ist schwarz. Glas wirkt nur mit Struktur dahinter und von vorn.
3. Schärfe auf ein konkretes Objekt legen, nicht auf die Bildmitte.
4. Bewegungsunschärfe nur für ganze Einstellungen ein- oder ausschalten.
5. Kamera im Makro rechnen statt raten: sichtbare Höhe = 2 · Abstand · tan(vFOV/2), vFOV bei 50 mm ≈ 22°.

## Weg 2: Blender als Modell-Quelle (ungetestet)

Belegter Standardweg (Stand 19.10.2026): **[ahujasid/mcp-for-blender](https://github.com/ahujasid/mcp-for-blender)**
(MIT). Ein Blender-Addon öffnet einen lokalen Server, Claude Code steuert Blender über MCP, auch mit beliebigem
Python-Code (`execute_blender_code`), und sieht Ansichten zur Selbstprüfung.

```bash
uvx mcp-for-blender setup                 # wenn uv da ist: richtet Claude Code ein und installiert das Addon
# manuell:
claude mcp add blender uvx mcp-for-blender
uvx mcp-for-blender install-addon
```

Danach in Blender das Addon verbinden. Ablauf für einen Film:
1. Modell in Blender bauen oder laden lassen, Maßstab in Metern, Ursprung sinnvoll setzen.
2. Als **GLB** exportieren (`bpy.ops.export_scene.gltf(filepath="model.glb", export_format="GLB")`), Texturen ≤ 4096 px.
3. In hf3d laden: `import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js"` (liegt in `hf3d/vendor`), im
   `ready`-Promise laden (`loadAsync`), Materialien bei Bedarf durch `mat.*` ersetzen. GLB lokal ins Projekt legen,
   keine Netz-Fetches beim Rendern.
4. Kamera, Licht und Schnitt bleiben in HyperFrames.

Ohne MCP geht es headless: `blender -b -P build.py` (Skript baut und exportiert das Modell). `-a` rendert eine
Animation als Bildfolge, falls doch in Blender gerendert werden soll.

Bekannte Stolpersteine (laut README, nicht selbst gemessen): uv nimmt eventuell conda/pyenv-Python
(`UV_PYTHON_PREFERENCE=only-managed`), das Addon muss laufen, vor jedem Befehl speichern (Code läuft ungeprüft in
Blender), große Aufgaben in kleine Schritte teilen. Renderzeiten und Speicher vorher selbst testen.

Weitere Blender-Wege: `RESOURCES.md` im Repo-Hauptordner.

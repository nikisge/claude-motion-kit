# hf3d: 3D-Studio für HyperFrames

Getestete Three.js-Vorlage (r181, lokal), mit der ein Agent in einer HyperFrames-Komposition schnell Produkt-3D
auf Premium-Niveau baut: Materialien, Studio-Licht, Verlauf statt Schwarz, Tiefenunschärfe, Bloom, Korn, eine
Kamera mit Shot-Liste und Helfer für prozedurale Objekte. Seek-sicher nach
`hyperframes/skills/hyperframes-animation/adapters/three.md`: jedes Bild ist eine reine Funktion von `t`.

| Datei | Inhalt |
|---|---|
| `hf3d.js` | die Bibliothek (ein ES-Modul) |
| `vendor/three/` | `three.module.min.js` + `three.core.min.js` 0.181.2 und die benutzten Addons (MIT, `LICENSE.txt`) |
| `fonts/Geist-Bold.ttf` | Schrift für 3D-Buchstaben (OFL, `Geist-OFL.txt`) |
| `install.sh` | kopiert alles nach `<hf>/vendor/hf3d/` (nach jeder Änderung an `hf3d.js` erneut ausführen) |
| `template.html` | Startpunkt: 3 Einstellungen, Metall + Glas + Leuchtstreifen, DoF |
| `../examples/rondo/index.html` | Demo-Film „RONDO“ (Komposition; mit `install.sh` in ein HF-Projekt kopieren) |

## Start

```bash
cd projects/<name> && export HYPERFRAMES_NO_TELEMETRY=1
npx -y hyperframes@0.8.149 init hf --non-interactive
bash <motion-3d>/hf3d/install.sh hf --template   # Vorlage wird index.html; <motion-3d> = Ordner dieses Skills
cd hf && npx -y hyperframes@0.8.149 lint
npx -y hyperframes@0.8.149 snapshot --at 0.7,2,3.3 --no-end --describe false
```

Gerüst jeder Komposition (siehe `template.html`):

```html
<script type="importmap">{ "imports": { "three": "./vendor/hf3d/three/three.module.min.js",
  "three/addons/": "./vendor/hf3d/three/addons/", "hf3d": "./vendor/hf3d/hf3d.js" } }</script>
<div id="root" data-composition-id="main" data-no-timeline data-start="0" data-duration="9.6"
     data-width="1920" data-height="1080" data-fps="30"><canvas id="stage" width="1920" height="1080"></canvas></div>
<script type="module">
  import { THREE, createStudio, shotRig, studioLights, mat, lathe } from "hf3d";
  const studio = createStudio({ canvas: document.getElementById("stage"), env: "studio", background: {…}, post: {…} });
  const rig = shotRig([ … ]);
  studio.run((t) => { rig.apply(t, studio.camera, studio.post); /* Objekte aus t setzen */ }, { ready, cuts: rig.cuts });
</script>
```

HTML-Text (GSAP) kann zusätzlich darüber liegen; dann statt `data-no-timeline` eine Timeline registrieren.

## API in Kürze

**`createStudio(o)`** · `env`: `"studio"` (Softboxen, `envOptions: { tone: "bright" | "dark", key, strip, walls, floor }`),
`"room"` (RoomEnvironment) oder eine eigene Szene; per PMREM, keine HDR-Datei. `envIntensity`, `envRotation`
(je Einstellung änderbar: `studio.scene.environmentRotation.y`, wirkt wie HDRI drehen).
`background`: Verlauf `{ top, bottom, glow, glowPos, glowSize, glowStrength, glow2…, angle }`, zur Laufzeit
`studio.background.set({…})`; `null` = kein Hintergrund. `shadows` (PCF soft). `exposure`, `tone: "aces" | "neutral"`.
`post: false` schaltet alles ab, sonst `{ dof: { bokeh, maxBlur, quality } | false, bloom: { strength, radius, threshold } | false,
grain, vignette, aberration, msaa }`; zur Laufzeit `studio.post.o.*`, `studio.post.bloom.strength`.
`motionBlur: { samples, shutter }` oder Funktion `(t) => … | null` (Zwischenbilder gemittelt, kostet n-fach).

**Licht + Boden** · `studioLights(scene, { key, rim, fill, target, shadow })` (Key wirft Schatten) ·
`shadowFloor({ opacity })` (nur Schatten, Verlauf bleibt) · `contactShadow({ size, opacity })` (weicher Fleck, billig).

**Materialien `mat.*`** · `brushedMetal` (Anisotropie + geseedete Rillen-Textur; `repeat` steuert Rillenrichtung/-dichte) ·
`polishedMetal` · `glass` (Transmission, `thickness`, `ior`, `dispersion`, `attenuationColor/Distance`) · `softTouch` ·
`ceramic` · `glossyPlastic` · `emissive` (Intensität > Bloom-Schwelle = Glühen). Leuchtende Instanzen: `MeshBasicMaterial`
mit `toneMapped: false` und HDR-Farbe je Instanz (`setColorAt`, Werte > 1).

**Kamera `shotRig(shots)`** · je Eintrag `{ start, end, pos, target, lens, focus, bokeh, ease, roll, shake }`.
`pos`/`target`: Punkt (steht), 2 Punkte (lineare Fahrt), ≥ 3 Punkte (Catmull-Rom-Fahrt), `Object3D` oder `(u, t) => Vector3`.
`lens` in mm (Vollformat; Makro 85–135 mm nah ran), auch `[von, bis]` (Zoom). `focus`: Zahl, Punkt, `Object3D`,
`"target"` (Standard) oder Liste `[a, b]` + `focusEase` (Schärfe ziehen). `bokeh`: px-Unschärfe für Unendlich, auch `[von, bis]`.
Zwischen zwei Einträgen = harter Schnitt; `rig.cuts` gibt die Schnittzeiten (für Sichtbarkeitsfenster nach three.md
und für `run(…, { cuts })`). Eigene Felder (z. B. `bg`, `envRot`, `exposure`) stehen in `rig.apply(t).shot`.

**Formen** · `roundedBox(w, h, d, r)` (Tasten, Geräte) · `lathe([[r, y], …], { fillet })` (Drehteile: Knöpfe, Ringe,
Gehäuse) · `knurl(geo, { ribs, depth, yMin, yMax })` (Rändelung) · `ribbon(points, { width, twist })` (Glas-/Lichtbänder) ·
`loadFont(url)` + `extrudeText` / `extrudeLetters` (3D-Buchstaben, einzeln animierbar) · `extrudeSVG(svgText, { depth, scale })`.

**Instancing `new Swarm({ geometry, material, count, seed })`** · `.layout(name, liste)` mit `layouts.grid | sphere | ring |
scatter | fromGeometry(geo, n, seed)`; `.blend(a, b, u, { stagger, arc, spin, order: "random" | "x" | "y" | "radial" | fn })`
für Morph, Explosion, Zusammenbau. Alles geseedet.

**Zeit** · `seg(t, a, b, ease.*)`, `ease.inOut | out | expoOut | spring | …`, `rng(seed)`, `noise1(x, seed)`.

## Demo „RONDO“ (`../examples/rondo/`)

Erfundener Drehregler aus Grundformen (Drehteile, Rändelung, Rauchglas mit Dispersion, 72 Leucht-Striche, Keramik-Tasten).
9,6 s, 30 fps, 10 Einstellungen: Zündung (3/4 von oben) → Makro Rändelung (Fahrt, Bewegungsunschärfe) → Draufsicht mit
Kamera-Roll → Tastendruck → Explosionszeichnung (Orbit) → Glas-Makro mit Schärfeverlagerung (dunkel) → Zusammenbau aus
135 Segmenten (Swarm) → Held mit orangen Glasbändern → Makro-Rückfahrt → Endkarte (Buchstaben steigen, 1,4 s).

- Gemessen mit `ref_metrics.py` gegen den Referenzfilm kimi-3 und einen frühen Versuch ohne 3D-Studio („ohne hf3d“).
- **Gemessen (MacBook M-Serie, 24 GB, `hardware gpu`, Screenshot-Aufnahme, 5 Worker):** Render 1:52–2:01 min für 288 Bilder
  (≈ 0,4 s/Bild, davon Bewegungsunschärfe 8× auf 1,65 s), Speicherspitze 1,4–1,8 GB (Wächter). Einzelbild-`snapshot` 0,6–0,85 GB.

| ref_metrics | Kimi-3 | ohne hf3d | RONDO |
|---|---|---|---|
| Schnitte / neue Ansichten je 10 s | 4,3 / 5,4 | 2,9 / 3,3 | 9,4 / 10,4 |
| Ø Einstellung | 2,1 s | 3,1 s | 1,0 s |
| Bildänderung je Bild / Kamera steht | 5,7 / 14 % | 2,3 / 57 % | 5,6 / 15 % |
| Einstieg (0–2 s) Bildänderung | 9,3 | 0,2 | 8,0 |
| leere Strecken > 0,3 s | 0 | 3 (bis 1,2 s) | 0 |
| Kontrast / Sättigung | 45,7 / 0,17 | 33,1 / 0,25 | 33,6 / 0,09 |

**Ehrlich gegen Kimi-3:** Erreicht: Kamera fährt in jeder Einstellung, Makros mit echter Tiefenunschärfe, Metall mit
Anisotropie, Glas, das das Display darunter bricht, Glasbänder, Verlauf statt Schwarz, keine leeren Bilder, Text nur auf
der Endkarte, ein Zusammenbau aus Teilen statt Zerfall. Sichtbar näher an Kimi-3 als der Versuch ohne hf3d in Tempo, Material und Licht.
Nicht erreicht: das Produkt ist einfacher (eine Dose mit Ring statt Tastatur mit Beschriftung, Display-UI, Knöpfen); die
Oberflächen haben weniger Verlaufsreichtum (Alu-Seiten wirken flach grau), Kontrast und Sättigung liegen deutlich unter
Kimi-3 (33,6 vs 45,7 / 0,09 vs 0,17); Kimi lebt von längeren, schnellen Kameraflügen (Median 1,8 s) statt vieler
Schnitte; der Rändel-Makro hat an der Ringkante sichtbare Facetten; kein Ton. Nächster Hebel: wärmere, sattere
Verläufe + dunklere Akzentteile für Kontrast, ein Produkt mit mehr Teilen (Tasten-Instancing, Display als Canvas-Textur),
2–3 lange Flüge statt 10 Schnitte.

## Fallstricke (gemessen beim Bau)

- **`data-no-timeline` am Root**, wenn keine GSAP-Timeline registriert ist: sonst Lint-Fehler und 45 s Wartezeit je Render.
- **`snapshot` immer mit `--describe false`**: ist `GEMINI_API_KEY` gesetzt, schickt es sonst jedes Bild an Gemini (bezahlt).
- **Metall braucht Umgebung**: ohne `env` schwarz; in hellen Szenen `tone: "bright"`, sonst spiegelt Metall einen dunklen Raum.
  Glanz zu hart oder an falscher Stelle → `environmentRotation` je Einstellung drehen statt Lichter umzubauen.
- **Glas**: wirkt nur mit Struktur dahinter (vor leerem Verlauf unsichtbar/milchig) und von vorn; flach unter
  streifendem Blick ist es ein grauer Spiegel. Glasbänder deshalb in fast senkrechten Ebenen zur Kamera,
  `specularIntensity`/`envMapIntensity` senken. Transmission rendert die Szene ein zweites Mal je Bild (Kosten).
- **DoF**: Schärfe auf ein konkretes Objekt (`focus: mesh`), nicht auf die Bildmitte; `bokeh` > 24 px franst an
  Vordergrundkanten aus. Hintergrund-Verlauf liegt bei „unendlich“ und wird maximal weich (gewollt).
- **Bloom**: Spiegelnde Drehteile (gedrehtes Alu, polierte Kappen) erzeugen Blendflecken; Schwelle ≥ 1,5 und
  `bloom.strength` je Einstellung, zur Not Kappe matter machen.
- **Bewegungsunschärfe**: nur für ganze Einstellungen ein-/ausschalten (sonst springt die Schärfe mitten im Shot, der
  Schnitt-Detektor meldet einen falschen Schnitt); `run(…, { cuts: rig.cuts })` übergeben, sonst mitteln die ersten
  Bilder nach einem Schnitt das vorige Motiv hinein; bei sehr schnellen Starts (`expoOut`) treppt sie mit 8 Proben → `ease: "out"`.
- **Rändelung/Displacement** braucht viele Stützpunkte im Profil (sonst keine Wirkung) und Rippen, die über die Kanten
  auslaufen (eine Rampe im Band erzeugt Zahn-Facetten im Makro).
- **Kamera im Makro** rechnen statt raten: sichtbare Höhe = 2 · Abstand · tan(vFOV/2), vFOV bei 50 mm ≈ 22°, 85 mm ≈ 13°.
- Keine Ebene/Textur über 4096 px; `Math.random`/`Date.now` nie (Lint, Determinismus); Fonts per `loadFont` im `ready`.

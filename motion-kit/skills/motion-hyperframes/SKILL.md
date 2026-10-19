---
name: motion-hyperframes
description: Use when building, checking or rendering a motion graphics film, style frame or animatic in HyperFrames (HTML/GSAP/SVG/Three.js compositions), when setting up a HyperFrames project, or when a HyperFrames render shows banding, wrong colours, black backgrounds, missing frames or missing motion blur.
---

# Motion HyperFrames: Bau-Modul

Brücke zwischen `motion-director` (Ablauf, Stil, Critic) und den offiziellen HyperFrames-Skills von HeyGen
(Technik). **Der Ablauf kommt aus motion-director.** Die HyperFrames-Workflows (`/hyperframes`, product-launch-video,
motion-graphics …) bringen eigene Briefing-Schleifen mit, die ersetzt der Director-Prozess. Ihre Technikregeln gelten voll.

## Einrichten (pro Projekt)

```bash
claude plugin marketplace add heygen-com/hyperframes   # offizielle Skills (einmal)
claude plugin install hyperframes@hyperframes          # alternativ ohne Plugin: npx hyperframes skills update
cd projects/<name>
export HYPERFRAMES_NO_TELEMETRY=1
npx -y hyperframes@<version> init hf --non-interactive   # Version festhalten, nie @latest mitten im Projekt
```

## Welchen HyperFrames-Skill wann lesen

| Aufgabe | Skill |
|---|---|
| Kompositions-Vertrag: `data-*`, Clips, Tracks, Sub-Kompositionen, Determinismus | `hyperframes-core` (vor dem ersten HTML) |
| Bewegung, GSAP, Übergänge; Three.js (`adapters/three.md`); Motion Blur | `hyperframes-animation` |
| Kamera, Zoom, Punch-in, Match/Whip, Masken, SVG-Draw | `hyperframes-keyframes` |
| Befehle, Render-Optionen, Fehlersuche | `hyperframes-cli` |
| Baustein suchen | `hyperframes-registry` |

Ton nicht in HyperFrames bauen: Der Mix kommt aus `motion-sound` und wird am Ende angelegt.

## Eigene Komponenten zuerst

Eigenes Design je Film, Bausteine selbst bauen (`hf/components/<name>.html`). Der Katalog
(`npx hyperframes catalog --query "<Bewegung, englisch>"`) ist Fundgrube: Quelltext lesen, Technik verstehen, in
eigenes Design übersetzen. Nie ein Katalog-Look 1:1, das ist genau der Look, den jedes KI-Video hat.

## Prüfen

```bash
npx hyperframes lint                      # schnell, nach jedem größeren Schritt
npx hyperframes check                     # Laufzeit, Layout/Überlauf, Kontrast (WCAG)
npx hyperframes snapshot --at 1.2,4.0,9.5 --describe false   # Einzelbilder; ohne --describe false wird ein bezahltes Bildmodell gefragt
npx hyperframes render --quality draft --output ../renders/draft.mp4   # Animatic, schnell
```
Danach die Prüfungen aus `motion-director/references/rules.md`.

## Rendern + Mastern (gegen Banding)

Normale MP4 = 8 Bit: Verläufe und Glows bekommen Stufen. Deshalb verlustfrei rendern und mit 10 Bit + feinem Korn
mastern:
```bash
npx hyperframes render --format mov --quality delivery --output ../renders/master.mov
bash scripts/master_10bit.sh ../renders/master.mov ../renders/film.mp4 0.35 ../renders/mix.wav
```
Das Skript korrigiert die Farbmatrix (BT.601 ohne Tags → BT.709), legt feines 10-Bit-Korn auf die Helligkeit, legt
den Ton an und warnt bei transparentem Bild. Achtung: 10-Bit-H.264 spielt QuickTime nicht ab (VLC, mpv, ffplay,
Browser gehen). Zum Verschicken zusätzlich eine 8-Bit-Kopie (`-pix_fmt yuv420p -crf 18`).

## Speicher

Renders mit 3D, Glas oder großen Ebenen brauchen viel RAM. Darum: **ein Render gleichzeitig**, keine Render-Schleifen
im Hintergrund, erst ein Einzelbild rendern und den Speicher beobachten, **keine Ebene über 4096 px je Seite**.

## Motion Blur

| Weg | Wann | Grenze |
|---|---|---|
| Registry-Baustein `motion-blur` (Zwischenzeiten, Shutter-Winkel) | schnelle Einzelelemente | nur `transform`; teuer auf großen Containern |
| Engine-Motion-Blur | ganze Bilder | nur über die Producer-API, nicht mit Shader-Übergängen |

Nie auf Lesefahrten (Text/Seiten), nur wo das Auge nicht lesen soll.

## Fallstricke (gemessen bzw. aus Issues, Stand Oktober 2026)

- Hintergrund auf `<body>` statt auf dem Root `[data-composition-id]`: im MOV transparent, im MP4 schwarz.
- `z-index: -1` rendert nicht. Animationen, die ein Skript vor dem Runtime-Laden anlegt, können einen Frame
  danebenliegen; CSS-Animationen in Shadow-Roots/Pseudo-Elementen ebenso.
- Stiller Rückfall auf langsame Screenshot-Aufnahme: Render-Zusammenfassung lesen.
- `Math.random`/`Date.now` blockt der Lint: Zufall immer geseedet. Endlos-`repeat` verboten.
- Große CSS-Blurs bremsen stark. Assets nach Neubau unter neuem Dateinamen ablegen (Cache nach Pfad).

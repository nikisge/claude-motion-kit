---
name: motion-hyperframes
description: "Use when building, checking or rendering a motion graphics film, style frame or animatic in HyperFrames (HTML/GSAP/SVG/Three.js compositions), when combining generated clips with code layers in HyperFrames, when setting up a HyperFrames project, or when a HyperFrames render shows banding, wrong colours, black backgrounds, missing frames or missing motion blur."
---

# Motion HyperFrames: Bau-Modul

Brücke zwischen `motion-director` (Ablauf, Stil) und den offiziellen HyperFrames-Skills von HeyGen (Technik).
**Der Ablauf kommt aus motion-director.** Die HyperFrames-Workflows (`/hyperframes`, product-launch-video …) bringen
eigene Briefing- und Freigabeschleifen mit, die ersetzt der Director-Prozess. Ihre Technikregeln gelten voll.

## Wie aus Code Video wird (in einem Satz)

Claude baut kein Video, Claude baut eine Webseite, die weiß, wie sie zu jeder Sekunde aussieht. HyperFrames öffnet
sie in einem unsichtbaren Browser, stellt die Uhr auf 0,000 s, fotografiert, stellt sie auf 0,033 s, fotografiert,
und so weiter (30 Bilder je Sekunde). ffmpeg klebt die Bilder zur MP4. Ebenen liegen wie Spuren im Schnittprogramm
übereinander (`data-start`, `data-duration`, `data-track-index`), die Bewegung ist ein pausiertes Drehbuch
(GSAP-Timeline oder eine Funktion von t), das der Renderer Bild für Bild ansteuert. Ändern heißt: Drehbuch ändern,
neu fotografieren. Darum sieht es ohne Vorgaben nach Website aus: Die Bausteine sind die einer Website.

## Version

Stand 08.11.2026: **0.9.23** ist aktuell (npm). Die Filme vom November 2026 liefen auf **0.9.17**. Zwischen 0.9.17
und 0.9.23 kamen nur Fehlerbehebungen und Studio-/Cloud-Funktionen, keine neuen oder entfernten CLI-Befehle (selbst
verglichen). Für Nutzer heißt das: neue Projekte auf 0.9.23 starten, laufende Projekte auf ihrer Version lassen.
Relevant aus den Release-Notes: ein `set` vor oder mitten in einem Tween löscht dessen Ende nicht mehr (0.9.19, 0.9.23),
Seiten-Timer laufen bei jeder Worker-Zahl im Takt des Films (0.9.22), Motion Blur meldet, was er erfasst (0.9.20).

## Einrichten (pro Projekt)

```bash
claude plugin marketplace add heygen-com/hyperframes   # offizielle Skills (einmal)
claude plugin install hyperframes@hyperframes          # ohne Plugin: npx hyperframes skills update
cd projects/<name>
export HYPERFRAMES_NO_TELEMETRY=1
npx -y hyperframes@0.9.23 init hf --non-interactive   # Version festhalten, nie @latest mitten im Projekt
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

Bewährt für ganze Welten: **eine Funktion von t** (`film.js`), die Kamera, Licht, Schärfe und alle Objekte aus der
Zeit berechnet. Das ist seek-sicher und macht eine durchgehende Kamerafahrt ohne Schnitt einfach.

## Generierte Clips und Code kombinieren

- Modell-Clips als `<video class="clip">` mit `data-media-start` auf eigene Spuren legen, Code-Ebenen darüber.
- Masken über echtem Video (`clip-path`, SVG-Maske) für Wipes zwischen echt und neu gezeichnet, auf derselben
  Quellzeit framegenau übereinander.
- Rahmen als Fenster: Standbild mit ausgestanztem Inneren fliegt an der Kamera vorbei, dahinter läuft der nächste Clip.
- Zwischen zwei Modell-Clips ein harter Schnitt im Bewegungs-Blur, keine Überblendung (sonst Doppelbelichtung).
- Clips mit 24 oder 12 fps in einem 30-fps-Film: Doppelbilder einplanen oder vorher umrechnen.
- Details und Kosten: `motion-higgsfield`.

## Prüfen

```bash
npx hyperframes lint                      # schnell, nach jedem größeren Schritt
npx hyperframes check                     # Laufzeit, Layout/Überlauf, Kontrast (WCAG)
npx hyperframes snapshot --at 1.2,4.0,9.5 --no-end      # Einzelbilder zu genauen Zeiten
npx hyperframes snapshot --review         # je Szene Start und Mitte, Streifen um jeden Schnitt, Handy-Breite
npx hyperframes snapshot --at 2,5 --against ref.mp4     # Bild neben der Referenz zur selben Zeit
npx hyperframes render --quality draft --output ../renders/draft.mp4   # Animatic, schnell
```
`snapshot` schickt seit 0.9.16 nichts mehr an ein bezahltes Bildmodell (`--describe` ist aus). Nützlich im Feinschliff
außerdem `hyperframes measure` (Schnitte, Bewegung, Look eines Videos) und `hyperframes audio` (wo Töne landen); die
Kit-Werkzeuge `ref_metrics` und `motion_check` bleiben die Referenz für die Stil-Schwellen. Danach die Prüfungen aus
`motion-director/references/rules.md`.

## Rendern + Mastern (gegen Banding)

Normale MP4 = 8 Bit: Verläufe und Glows bekommen Stufen. Deshalb verlustfrei rendern und mit 10 Bit + feinem Korn
mastern:
```bash
npx hyperframes render --format mov --quality delivery --workers 3 --output ../renders/master.mov
bash scripts/master_10bit.sh ../renders/master.mov ../renders/film.mp4 0.35 ../renders/mix.wav
```
Das Skript korrigiert die Farbmatrix (BT.601 ohne Tags → BT.709), legt feines 10-Bit-Korn auf die Helligkeit, legt
den Ton an und warnt bei transparentem Bild. 10-Bit-H.264 spielen QuickTime und Browser nicht ab (VLC, mpv, ffplay
gehen). Zum Verschicken und für Review-Seiten zusätzlich eine 8-Bit-Kopie (`-pix_fmt yuv420p -crf 18`).

`--workers` fest setzen (z. B. 3). Mit automatischer Worker-Zahl kam bei uns einmal ein Film heraus, in dem eine
große Ebene fehlte.

## Speicher und Renderzeit

Renders mit 3D, Glas oder großen Ebenen brauchen viel RAM. Darum: **ein Render gleichzeitig**, keine Render-Schleifen
im Hintergrund, erst ein Einzelbild rendern und den Speicher beobachten, **keine Ebene über 4096 px je Seite**.
Arbeiten mehrere Agenten auf einem Rechner: eine gemeinsame Sperre (`mkdir render.lock` ist atomar, `rmdir` beim Ende),
auch für Snapshots und ffmpeg-Mastering. Lange Renders als normalen Hintergrund-Befehl starten, nicht per
`nohup … &` (HyperFrames brach dabei ab), und das Skript während des Laufs nicht ändern.

## Motion Blur

| Weg | Wann | Grenze |
|---|---|---|
| Registry-Baustein `motion-blur` (Zwischenzeiten, Shutter-Winkel) | schnelle Einzelelemente | nur `transform`; teuer auf großen Containern |
| Capture-Unschärfe `data-motion-blur="on"` | ganze Bilder | in 0.9.17 meldete `check` keinen Fehler, der Renderer schaltete sie aber ab („renderer-off, distributed-render“, auch mit `--workers 1`). In 0.9.23 ungetestet: Render-Zusammenfassung lesen |
| Eigene Unschärfe über hohe fps | ganze Bilder, sicher | Renderzeit × 8 |
| Eigene Richtungsunschärfe (SVG) aus der Kamerageschwindigkeit | nur Kamerafahrten | max. ~10 px, Lesestellen aus |

Rezept für den sicheren Weg (180°-Verschluss): mit 240 fps als ProRes rendern, dann je 5 Bilder gewichtet mitteln.
120 fps mit 3 Stützstellen gab getreppte Doppelkanten.
```bash
npx hyperframes render --format mov --prores-profile hq --quality delivery --fps 240 --output m240.mov
ffmpeg -i m240.mov -vf "tmix=frames=5:weights='1 2 2 2 1',select='eq(mod(n\,8)\,2)',setpts=N/30/TB,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709" \
  -r 30 -c:v prores_ks -profile:v 3 -pix_fmt yuv422p10le master30.mov
```
`setparams` ist nötig: Ohne BT.709-Tag hält `master_10bit.sh` das Bild für BT.601 und verschiebt die Farben.
Nie auf Lesefahrten (Text/Seiten), nur wo das Auge nicht lesen soll.

## Fallstricke (gemessen bzw. aus Issues, Stand November 2026)

- Hintergrund auf `<body>` statt auf dem Root `[data-composition-id]`: im MOV transparent, im MP4 schwarz.
- `mix-blend-mode` innerhalb einer `preserve-3d`-Welt klappt sie in Chrome flach (Ebenen liegen verzerrt auf der Fläche).
- `z-index: -1` rendert nicht. Animationen, die ein Skript vor dem Runtime-Laden anlegt, können einen Frame
  danebenliegen; CSS-Animationen in Shadow-Roots/Pseudo-Elementen ebenso.
- Stiller Rückfall auf langsame Screenshot-Aufnahme: Render-Zusammenfassung lesen.
- 4K: Canvas/WebGL bleibt in eigener Auflösung.
- `Math.random`/`Date.now` blockt der Lint: Zufall immer geseedet. Endlos-`repeat` verboten.
- Große CSS-Blurs bremsen stark. Assets nach Neubau unter neuem Dateinamen ablegen (Cache nach Pfad).

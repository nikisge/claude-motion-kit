# Stilkarte: Apple Premium

**Wann wählen:** wenn ein Produkt, eine Zahl oder eine Fähigkeit „teuer" wirken soll; Keynote-Momente, Feature-Reveal,
Showreel-Passagen, Endkarten. Auch als Würze in anderen Stilen (ein Apple-Moment im Clean-SaaS-Film).

**Bildidee:** Eine Einstellung = eine Idee. Ein Ding ist laut (Licht, Farbe, Zahl), alles andere schweigt.
Formen verwandeln sich in die nächste Form, statt zu schneiden (apple-wonderful-tools: 60 s, eine Form, nie ein Schnitt).

## Leitreferenzen (Grammatik, nie Inhalt)

| Ref | Zeit | Was passiert | Übernehmen |
|---|---|---|---|
| apple-wonderful-tools | 0:00–0:02 | Handschrift „hello" auf Weiß, wird zum Bildschirm eines kleinen Macs | Schrift als Objekt im Objekt |
| | 0:02–0:07 | Kreise ordnen sich zum iPod-Clickwheel, Menü-Labels erscheinen | **Kreis-Morph**: Grundform → bekanntes Objekt |
| | 0:07–0:12 | Home-Button → Fingerabdruck (pink, Linien zeichnen sich) → Face-ID-Rahmen → Haken | Strich-Animation trägt Bedeutung |
| | 0:13–0:19 | Toggle → bunte iMac-Schalen im Kreis → zerfallen in weiße Scherben → Striche | Farbexplosion als Pause zwischen Grautönen |
| | 0:20–0:36 | Kreis → Lochmuster → Mac-Pro-Gitter → Würfel; Striche fächern, kreuzen, werden zu Kabel → AirPods | **Linie wird Objekt** |
| | 0:54–0:59 | Kamera-Linse wächst zum Kamerabuckel, Rahmen zum Handy, App-Kacheln entstehen als Umrisse | Umriss vor Fläche |
| leo-apple | 0:00–0:09 | Raster aus 4 Keynote-Momenten: Siri-Glow, Lichtband am Horizont, „Take your design anywhere" baut sich Wort für Wort auf, grünes 24-hour-Feld, Chrom-„PRO" mit Rauch | **harte Farbflächen** + **Lichtband** + **Typo wächst Wort für Wort** |

## Messwerte (motion_check 11.10.2026 + Bögen)

| | Wechsel/10 s | Median-Einstellung | längste | eingefroren | Text im Bild |
|---|---|---|---|---|---|
| apple-wonderful-tools | 2,0 (Morph zählt kaum als Wechsel) | 1,5 s | 20,8 s (eine Morph-Kette) | 5,4 s | 10 % |
| leo-apple | 7,5 | 1,0 s | 2,1 s | 0 | 96 % |

- Pro Morph-Zustand 1,0–1,5 s, Verwandlung 0,4–0,7 s; Halte am Ziel ~0,5 s, nie länger als 2 s.
- Text: 1–4 Wörter, Display-Größe 120–220 px @1080p, Gewicht 600–700, eng gesetzt (−2 bis −4 % Laufweite).

## Startwerte

- **Farbe:** Schwarz #000 oder Hellgrau #E9E9EB / Weiß, **eine** laute Fläche pro Einstellung (Grün #30D158,
  Magenta #D62C8A, Siri-Verlauf). Metall: Verlauf #F5F5F7 → #8E8E93 → #2C2C2E mit hartem Glanzband.
- **Typo:** eine Familie, Inter Display / SF-artig (Inter Tight, Geist). Keine Serife. Satzzeichen hängen.
- **Komposition:** zentriert, Objekt 30–50 % der Bildhöhe, sehr viel Leerraum; Raster-Montage (2×2) nur als Höhepunkt.
- **Kamera:** fast still; wenn, dann langsame Dolly 2–4 % über die Einstellung oder Orbit um ein 3D-Objekt.
- **Übergänge:** Form-Morph (Pfad-Interpolation, Kreis → Rechteck → Objekt), Match-Cut auf gleiche Form, Lichtband
  wischt. Überblenden nur als Lichtblende (Weiß), nie als Kreuzblende von zwei Bildern.
- **Easing:** `cubic-bezier(0.65, 0, 0.35, 1)` für Morphs, expo-out 0,5 s für Ankunft, kein Überschwingen bei Typo,
  winziges (2 %) bei Objekten.

## Sound-Charakter

Sparsam, trocken, teuer: weiche Sub-Hits auf Form-Landungen, feine Klicks/Ticks für Mechanik, Glas-Schimmer für Licht,
Musik minimal (Piano, Puls, 60–90 BPM) oder ein einziger treibender Loop bei der Raster-Montage. Stille ist
ein Werkzeug: 0,3–0,5 s vor dem großen Reveal.

## Signature Moves (Bauweise)

1. **Form-Morph-Kette:** SVG-Pfade mit gleicher Punktzahl (oder flubber/`MorphSVGPlugin`, GSAP ist frei nutzbar),
   je Zustand ein Pfad; Tween 0,5 s `power2.inOut`, dazwischen 0,5–1 s Halten mit 1 % Scale-Drift.
2. **Strich zeichnet Objekt:** SVG `stroke-dasharray/offset` 0,6–1,0 s, danach Füllung in 0,2 s; Fingerabdruck =
   10–20 konzentrische Pfade mit Stagger 30 ms.
3. **Lichtband/Horizont-Glow:** horizontale Ellipse mit `filter: blur(40px)` + `mix-blend-mode: screen`, Siri-Farben,
   fährt 1,2 s; darunter ein 1-px-Horizont. Gegen Banding: MOV rendern, 10 Bit + Grain (`motion-hyperframes`).
4. **Typo wächst Wort für Wort:** jedes Wort tritt mit `scale 0.92→1` + Opacity in 0,25 s auf den Beat, Zeile
   umbricht live (echtes Layout), letzter Satzteil kriegt Markierungsrahmen (Auswahl-Box mit Griffen).
5. **Chrom-Wort:** Text als `background-clip:text` mit Metallverlauf + bewegtem Glanzband (`light-sweep`); in
   Three.js: TextGeometry mit `MeshPhysicalMaterial(metalness 1, roughness 0.15)` + HDRI-Umgebung.
6. **Farbfeld-Schlag:** volle grüne Fläche schlägt auf den Downbeat ein, Zahl darin mit Tiefenunschärfe von 12→0 px.

## Slop-Fallen

- „Apple-Look" = schwarzer Hintergrund + weiße Typo + nichts passiert. Ohne Licht oder Morph ist es eine Folie.
- Zwei laute Dinge gleichzeitig (Farbe **und** Effekt **und** Text).
- Glanz/Glow auf allem. Ein Glanz pro Einstellung.
- Kreuzblende zwischen Szenen. Hier immer Morph, Match-Cut oder Licht.
- Echte Apple-Marken/Geräte nachbauen: nur Grammatik übernehmen, eigene Objekte.

## Variationen

- **Hell + Strich-Morph** (Wonderful Tools) für Erklär-Objekte · **Schwarz + Licht + Farbfeld** (Keynote) für Reveals.
- Mischen mit Kinetic Type (Wort-Wachsen) oder 3D-Objekt-Story (Chrom-Objekt im Orbit).
- Eigenes: die Morph-Kette erzählt die Geschichte des Kunden (Werkzeug → Prozess → Ergebnis) statt Apple-Geräte.

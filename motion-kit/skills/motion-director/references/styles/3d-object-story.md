# Stilkarte: 3D-Objekt-Story

**Wann wählen:** wenn ein Ding (Produkt, Symbol, Maskottchen, Icon) die Geschichte tragen kann; Hardware, Marken-Objekte,
„was steckt drin", Showcase-Momente. Leitfilm: kimi-3 (3D-Objekt, Licht, Storytelling).

**Bildidee:** Das Objekt ist die Erklärung. Es wird gezeigt wie ein Schmuckstück (Makro, Licht, Tiefenunschärfe),
dann verändert es sich (leuchtet, zerlegt sich, wechselt Material) und erzählt so die Fähigkeit.

## Leitreferenzen (Grammatik, nie Inhalt)

| Ref | Zeit | Was passiert | Übernehmen |
|---|---|---|---|
| kimi-3-couldve-never-done-this | 0:00–0:01 | Totale: Werkstatt, Tastatur auf Schneidematte unter Lampe | Objekt erst im Kontext, dann isoliert |
| | 0:01–0:03 | Makro mit flacher Schärfe über Tasten und Display, Rack-Focus | **Makro + Tiefenunschärfe** = Wertigkeit |
| | 0:03–0:04 | Objekt schwebt schräg vor Orange-Weiß-Verlauf, dünnes Band zieht Bögen | Held-Pose mit einer Linie als Begleiter |
| | 0:04–0:06 | Tasten leuchten als Welle cyan auf (Licht wandert durch das Objekt) | **Licht erzählt die Funktion** |
| | 0:06–0:07 | Tastenkappen wechseln wellenartig die Farbe | Varianten durch Material-Welle statt Schnitt |
| | 0:08–0:13 | dunkle Variante mit rotem Hintergrundlicht, Untersicht, Teile stapeln sich | Lichtstimmung wechseln = neues Kapitel |
| | 0:13–0:17 | Explosionsansicht schwebt, Band umschlingt sie, dann Logo auf Weiß | Zerlegung als Finale |
| voxel-icon-skill | 0:00–0:18 | Raster aus Voxel-Icons umrahmt die Mitte, Cursor klickt Icon, großes Voxel-Objekt baut sich in der Mitte auf und dreht | **Icon → großes Objekt**, Raster als Bühne |

## Messwerte (motion_check 11.10.2026)

| | Wechsel/10 s | Median-Einstellung | längste | harte Schnitte |
|---|---|---|---|---|
| kimi-3 | 4,9 | 1,6 s | 3,7 s | 7 in 18 s |
| voxel-icon-skill | 1,0 | – | 18,9 s (eine Bühne) | 0 |

- Objekt-Einstellungen 1,2–2,5 s, Kamerafahrten langsam (Orbit 10–25°/s, Dolly 3–6 % pro Sekunde).
- Text fast keiner: 0–2 Wörter am Objekt (Display-Inhalt), Logo am Ende.

## Startwerte

- **Farbe:** neutrale Studiobühne (Warmweiß #F4EFEA mit Orange-Verlauf #F26B3A, oder Graphit #1C1C1E), Objekt mit
  2–3 Materialfarben, ein Lichtakzent (Cyan #5AD8FF oder Rot #FF3B30) für den Funktions-Moment.
- **Typo:** minimal, eine Grotesk; Logo am Schluss klein (≤ 12 % Bildbreite).
- **Komposition:** Objekt 40–70 % der Bildfläche, diagonal angeschnitten; Makros dürfen 90 % füllen.
- **Kamera:** physische Kamera: Brennweite 50–85 mm (Three.js `fov` 20–30), Blende flach (Bokeh), langsame Fahrten
  `sine.inOut`; ein Rack-Focus pro Kapitel.
- **Licht:** Key von oben-links (warm), Rim von hinten (kalt), HDRI-Umgebung für Reflexionen, weicher Bodenschatten.
- **Übergänge:** Licht wechselt (Blackout → neues Licht), Material-Welle, Kamera fährt durch das Objekt, Match-Cut
  auf gleiche Objektkante.
- **Easing:** Objekt-Ankunft Feder mit 4 % Überschwinger, Rotation `power2.out`, Kamera `sine.inOut` (nie linear).

## Werkzeug und ehrliche Grenze

- **3D-Studio `motion-3d/hf3d`** (Three.js in HyperFrames, seek-sicher, `motion-hyperframes`): Material-Presets
  (Metall, Glas, Soft-Touch, Keramik, Emissive), Studio-Umgebung ohne HDR-Datei, Verlauf statt Schwarz, Tiefenunschärfe,
  Bloom, Shot-Liste mit Brennweite/Fokus, Drehteile, Rändelung, Glasbänder, 3D-Text, Instancing. Demo „RONDO“ in `motion-3d/examples/rondo`.
- **Kein Blender** installiert: Modelle aus Code (Three.js-Geometrie, Voxel aus Würfel-Instanzen, extrudierte SVGs).
  Kimi-3-Fotorealismus (Pfadverfolgung) ist mit Echtzeit-3D **nicht** ganz erreichbar: Ziel ist „Studio-Produktfilm in
  Echtzeit" (saubere Materialien, gutes Licht, Bokeh, Bewegung), nicht Rendering-Realismus. Kimi-3 ist Ziel-Referenz
  für Grammatik und Dichte (Shot-Tabelle in `refs/study/kimi-3-couldve-never-done-this/study.md`).
- Gegen Banding in Verläufen/Bokeh: MOV rendern → 10 Bit + Grain.

## Sound-Charakter

Material-Foley: Klacken (Tasten, Plastik), Metall-Ticks, weiche Luft beim Schweben, ein tiefer warmer Hit bei der
Zerlegung, elektrisches Summen/Schimmer beim Licht-Moment. Musik: ruhige Elektronik 90–110 BPM oder Ambient-Pad.

## Signature Moves (Bauweise)

1. **Makro-Fahrt mit Rack-Focus:** Three.js-Kamera 6–10 cm über dem Objekt (Szenenmaßstab realistisch), Fokusdistanz
   per Tween von Vorder- auf Hinterkante in 0,8 s; `BokehPass` aperture 0.002–0.01.
2. **Licht-Welle durch das Objekt:** Instanzen (Tasten, Voxel, Kacheln) bekommen `emissiveIntensity` nach
   `max(0, 1 - |dist(i) - v·t| / w)`, Bloom dazu; seek-sicher, weil rein aus t berechnet.
3. **Material-Welle (Variantenwechsel):** gleiche Formel, aber Farbe/Material wechselt hinter der Wellenfront.
4. **Explosionsansicht:** jede Teilgruppe `position += normal * ease(t) * d`, Stagger 60 ms von außen nach innen,
   Kamera zieht gleichzeitig 15 % zurück; Rückweg als Finale.
5. **Voxel-Aufbau:** Objekt aus `InstancedMesh`-Würfeln, Würfel fallen schichtweise ein (y-Sortierung, 8 ms Stagger),
   leichte Feder; Icon im Raster ist dasselbe Objekt verkleinert (Match).
6. **Begleit-Band:** eine Bézier-Röhre (`TubeGeometry`) mit transparentem Orange, `drawRange` wächst entlang t.

## Slop-Fallen

- Objekt dreht sich einfach im Kreis auf Verlauf (Turntable ohne Geschichte).
- Plastik-Look: Standardmaterial ohne Umgebung/Reflexion, harte Schlagschatten, keine Tiefenunschärfe.
- Zu viele Objekte. Eins, höchstens eine Familie.
- KI-generierte 3D-Bilder als Standbild „animiert" (Parallax-Wackeln). Wenn Bild-KI, dann als echtes Startbild für ein Videomodell, nicht als Wackelbild.
- Kamera ohne Ziel (Fahrt, die nirgends ankommt).

## Variationen

- **Studio-Produkt** (kimi-3) · **Spielzeug-/Voxel-Welt** (voxel-icon, buck-expedia als Welt-Gefühl) · **Chrom-Symbol** (tesseract-Würfel).
- Mischen: 3D-Held-Objekt als Rahmen für Clean-SaaS-UI (Display zeigt echte UI als Textur), oder als Schluss-Objekt
  eines Kinetic-Type-Films.
- Eigenes: das Objekt aus dem Kunden-Alltag (Ordner, Stempel, Maschine) statt Tech-Gadget.

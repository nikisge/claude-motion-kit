# Stilkarte: Kinetic Type (handwerklich)

**Wann wählen:** Manifest, Haltung, Showreel-Intro, Hook in den ersten 3 s, Musik-getriebene Stücke, Zitate. Wenn es
kein Produkt-UI gibt und **Sprache + Rhythmus** die Geschichte tragen. Leitfilme: how-do-you-communicate
(handwerklich, schwer nachzubauen) und glyph (eigenständig, kreativ).

**Bildidee:** Typo ist ein Darsteller, kein Untertitel. Sie wechselt Maßstab (riesig ↔ winzig), Material (Pixel, Tinte,
3D-Buchstaben) und Rolle (Satz, Objekt, Muster). Zwischen den Worten passieren Bilder, die das Wort *meinen*.

## Leitreferenzen (Grammatik, nie Inhalt)

| Ref | Zeit | Was passiert | Übernehmen |
|---|---|---|---|
| how-do-you-communicate | 0:00–0:02 | „how do" riesig mit gestrichelten Hilfslinien, schnappt zu winzigem Satz in der Mitte | **Maßstabssprung** als Hook |
| | 0:02–0:04 | cyanfarbener 4-Zack-Stern peitscht ins Bild, Pixel-Objekte fliegen, Kritzel-Linie | ein greller Fremdkörper bricht die Ruhe |
| | 0:04–0:06 | Schwarz, Wärmebild-Profil, kleiner Satz „you dont." tippt | Hell/Dunkel-Wechsel auf jedem Takt |
| | 0:06–0:13 | Ring aus Pixel-Objekten (Platte, Kamera, Münze, Herz) dreht, je ein Wort + Cursor auf Schwarz („action.", „intention.", „curiosity.") | **ein Wort + blinkender Cursor** zwischen Bildern |
| | 0:13–0:20 | Tintenkleckse fressen Objekte, Buchstaben L O V E schweben einzeln, rote Handschlaufen umkreisen sie | Handgezeichnetes über gesetzter Typo |
| glyph | 0:00–0:10 | bunte 3D-Buchstaben „Glyph" über Symbolmuster, Mini-Roboter schiebt Buchstaben weg, Fachwörter tickern darunter | **Buchstaben sind Körper** (stoßen, kippen) |
| | 0:10–0:14 | Schwarzes Loch saugt Muster und Buchstaben ein, Bild krümmt sich, Sterne bleiben | Finale: alles kollabiert in einen Punkt |
| olexdsgn-animation-sketches (Zusatz) | 0:00–0:18 | pro Wort eine neue Vollbild-Welt (Rauschen, Tauben, rote Silhouetten, Zahlenregen), Wort klein in der Mitte | **ein kleines Wort pro Takt über wechselnden Welten** |
| mvsm-robinhood (Rhythmus) | 0:03–0:26 | dunkle Sport-Einstellungen im Spotlicht, dünne Datenlinien und %-Pillen zeichnen sich über die Spieler | Haarlinien-Grafik **auf** Bild, nicht daneben |
| | 0:27–0:30 | „Trade Every Play" tippt sich in Serife auf Schwarz, Logo | Endkarte klein und leise |
| buck-expedia-mattel (Rhythmus) | 0:01 / 0:15 | Fernglas-Iris-Blende, Wolken-Wipe als Szenenwechsel | Übergang durch ein Ding der Welt |
| | 0:27–0:30 | Schluss-Titel schreibt sich: Großbuchstaben + Handschrift gemischt, Gelb-Rahmen schlägt ein | Typo-Mischung Versal + Skript |

Hinweis: Buck und ManvsMachine sind keine Typo-Filme (3D-Spielzeugwelt bzw. Realfilm). Sie liefern hier nur
Schnitt-Rhythmus, Markenfarbe als Wiederholung und Endtitel-Verhalten.

## Messwerte (motion_check 11.10.2026)

| | Wechsel/10 s | Median-Einstellung | längste | harte Schnitte |
|---|---|---|---|---|
| how-do-you-communicate | 8,8 | 0,8 s | 3,2 s | 17 in 20 s |
| glyph | 4,0 | 1,8 s | 4,6 s | 0 (durchgehend) |
| olexdsgn | 5,6 | 1,1 s | 6,5 s | 10 in 22 s |
| mvsm-robinhood | 5,7 | 1,5 s | 3,5 s | 2 (Rest weiche Wechsel) |
| buck-expedia-mattel | 5,7 | 1,5 s | 2,9 s | 12 in 30 s |

- Text: 1 Wort pro Takt (40–60 % der Momente), Sätze höchstens 9 Wörter und dann **klein** (28–40 px @1080p).
  Hero-Wort 200–400 px. Lesezeit für Einzelwort ≥ 0,4 s, für Satz Regel 3 Wörter/s + 1 s.
- Schnitte auf Beat (120–128 BPM: alle 2 Schläge ≈ 0,94–1,0 s), Varianz Pflicht: 0,25 s / 0,5 s / 2 s gemischt.

## Startwerte

- **Farbe:** Papierweiß #EDEBE6 ↔ Fast-Schwarz #121212 im Wechsel, ein Schreiakzent (Rot #E3262B oder Cyan #2DE2E6).
  Glyph-Variante: 4–5 Bonbonfarben auf Creme, Buchstaben mit weichem Glanz.
- **Typo:** eine kräftige Grotesk (Bricolage Grotesque, Space Grotesk, Inter Black) + ein Fremdmaterial
  (Pixel-Font, Handschrift/Tinte, Mono). Laufweite eng (−3 %), Kleinschreibung erlaubt.
- **Komposition:** Wort exakt mittig oder auf Hilfslinie; Hilfslinien/Kreuze sichtbar lassen (Design-Werkzeug-Ästhetik).
- **Kamera:** meist still; Akzente durch Zoom-Schnapp (Scale 3→1 in 0,3 s expo-out) und kurze Wackler (Shake 4 px, 6 Frames).
- **Übergänge:** harter Schnitt auf Beat (Normalfall), Tintenklecks/Iris, Smash zu Schwarz, Objekt-Wipe.
- **Easing:** Typo-Ankunft expo-out 0,25–0,4 s ohne Überschwingen; Objekte Feder mit 8–15 % Überschwinger;
  Austritt in 0,15 s in-cubic oder harter Schnitt.

## Sound-Charakter

Musik führt (Beat-Raster aus `tools/beats.py`). Auf jedem Wortschlag ein kurzer Transient (Klick, Tasten-Anschlag,
Stempel), auf Hell/Dunkel-Wechseln ein tiefer Puls; Glitch/Tape-Stop für Brüche. Typing-Geräusch nur, wenn ein Cursor
sichtbar tippt. Pausen in der Musik = Pausen in der Typo.

## Signature Moves (Bauweise)

1. **Maßstabssprung mit Hilfslinien:** Wort bei 600 px mit gestrichelten Grundlinien (SVG `stroke-dasharray 6 6`),
   schnappt in 0,3 s auf 40 px Satz; Linien bleiben 4 Frames länger. GSAP `scale` auf Wrapper, Satz per SplitText.
2. **Wort + Cursor auf Schwarz:** Mono/Grotesk 72 px, Cursor-Block blinkt 2 Hz (seek-sicher: `Math.floor(t*4)%2`),
   Buchstaben tippen mit 30–45 ms; davor/danach ein Bild der Welt 0,5–1 s.
3. **Buchstaben als Körper:** jeder Buchstabe eigenes Element (HTML oder Three.js-Extrusion), Rotation ±8°, Stoß
   per Feder; Muster-Hintergrund als Kachel mit langsamer Drift. Echtes 3D-Glanzmaterial → Three.js.
4. **Objekt-Ring:** 8–12 Objekte auf Kreisbahn (Polar-Koordinaten aus t), Ring dreht 20°/s, Objekte springen auf Beat
   nach innen. Pixel-Objekte als SVG-Rects (eigene Zeichnung, keine Emoji-Sets).
5. **Tinte frisst Bild:** Maske aus wachsenden Kreisen mit `feTurbulence`-Rand (SVG), 0,5 s; danach Schwarz.
6. **Handschlaufe um Buchstaben:** SVG-Pfad mit Trim 0,6 s, leichte Unregelmäßigkeit (2–3 Kontrollpunkte jitter, geseedet).

## Slop-Fallen

- Jedes Wort mit demselben Fade-up + Blur. Variiere: Schnapp, Tippen, Stoß, Schnitt.
- Glow-Strich-Titel mit Neon (motionmaxxing: „zu slopped“).
- Ganze Sätze groß über das Bild. Groß nur ein Wort, Sätze klein.
- Text, der das Gesprochene wiederholt (Echo) bei YouTube-Einblendungen.
- Kinetik ohne Bild-Bedeutung: zwischen den Worten muss ein Bild kommen, das das Wort meint.

## Variationen

- **Collage/Mixed Media** (how-do): Pixel + Foto + Tinte · **3D-Buchstaben-Spiel** (glyph) · **Ein Wort pro Welt** (olexdsgn).
- Mischen: kinetischer Hook (3 s) vor einem Clean-SaaS-Film; Datenlinien auf Footage (mvsm) für Zahlen-Momente.
- Eigenes: die Worte aus der eigenen Stimme/dem Skript, eigene Handschrift abfotografiert als Material.

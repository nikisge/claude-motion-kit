# Stilkarte: Whiteboard-Erklärer (YouTube-Einblendungen, Excalidraw-artig)

**Wann wählen:** Einblendungen in YouTube-Videos neben oder statt der Kamera: Abläufe, Architekturen,
Vergleiche, „wie funktioniert das". Auch Erklär-Animationen bis ~60 s. Eigener Stil für seinen Kanal
(Feedback 11.10.: „Erklärgrafik/Whiteboard-Stil (Excalidraw-artig) für seine YouTube-Einblendungen").

**Bildidee:** Eine Skizze, die sich während des Sprechens selbst zeichnet. Hand-gezeichnete Kästen, Pfeile, Kritzel,
eine Schrift wie mit Filzstift. Ein Element nach dem anderen, genau dann, wenn es gesagt wird. Am Ende steht ein
Diagramm, das man als Standbild verstehen würde.

## Leitreferenzen (nur Erklär-Logik, nicht der Look)

Kurzgesagt und Vox sind **nicht** der Look (flache Vektorwelt bzw. Archiv-Collage), sondern Vorbild für das
**Erklären**: konkrete Metapher, Etikett am Objekt, Maßstab durch Kamera, Zählen durch Menge.

| Ref | Zeit | Was passiert | Übernehmen (Logik) |
|---|---|---|---|
| kurzgesagt-civilization | 0:00–0:05 | Fußabdruck im Sand, Spross wächst daraus, wird Ranke | **abstrakter Begriff → ein konkretes Ding** |
| | 0:05–0:08 | Ranke verzweigt, an jedem Zweig ein Medaillon (Vieh, Weizen, Werkzeug) | Verzweigung = Kategorien, je ein Bild-Icon |
| | 0:08–0:18 | Tor „Year 0", Figur „Year 2026"; Kamera zieht weg, Tor schrumpft zum Punkt, Etikett wird „Year 12,026" | **Maßstab durch Rückfahrt**, Etiketten zählen mit |
| kurzgesagt-mars-basis | 0:24–0:25 | Kreis-Iris öffnet die nächste Szene im Bild | Übergang aus einem Bildteil heraus |
| | 0:32–0:36 | Planet mit Umlaufbahnen, kleine Objekte kreisen | Diagramm darf lebendig bleiben (Nebenbewegung) |
| vox-green-new-deal | 0:09–0:12 | Liniendiagramm auf Creme: Kurve zeichnet sich, gestrichelte Prognose, Marker mit Wert | Kurve **zeichnet sich**, Prognose gestrichelt |
| | 0:18–0:26 | ein Dokument wird zu 14 Seiten im Raster, Textmarker-Pinsel streicht den Titel an | **Menge zählen** (Seiten nummerieren), Marker auf Schlüsselwort |

## Messwerte (motion_check 11.10.2026)

| | Wechsel/10 s | Median-Einstellung | längste | eingefroren |
|---|---|---|---|---|
| kurzgesagt-civilization | 2,9 | 1,5 s | 13,4 s (Rückfahrt) | 1,1 s |
| kurzgesagt-mars-basis | 1,6 | 4,8 s | 13,0 s | 2,0 s |
| vox-green-new-deal | 5,1 | 1,6 s | 8,3 s | 13,4 s (Dokument-Halte) |

- Erklärbilder dürfen 4–13 s stehen, **wenn** ständig ein Element dazukommt oder etwas Kleines lebt.
- Für Einblendungen gilt das Sprechtempo: ein neues Element ~80 ms **vor** dem Wort, das es meint (Wortzeiten aus dem Transkript).
- Text: Etiketten 1–3 Wörter, 36–48 px @1080p (im 1114 × 886-Slot ≥ 32 px), höchstens 6 Etiketten im Endbild.

## Startwerte

- **Farbe:** Hintergrund Papierweiß #FAF8F3 (oder Tafel #1E2321 für dunkle Videos), Strich #1E1E1E 2,5–3 px,
  Füllfarben aus Excalidraw-Palette gedämpft: Blau #A5D8FF, Grün #B2F2BB, Gelb #FFEC99, Rot #FFC9C9; Akzent-Strich
  Rot #E03131 nur für „das Wichtige". Schraffur (hachure) statt Vollflächen.
- **Typo:** Excalifont/Virgil (OFL, aus Excalidraw) oder Caveat/Kalam (Google Fonts, OFL); Zahlen mit Mono.
- **Komposition:** Flussrichtung links → rechts oder oben → unten, 3–5 Knoten, großzügige Abstände; im Slot neben der
  Kamera nichts in die 8 % am Rand.
- **Kamera:** steht meist; sanfter Pan/Zoom (≤ 10 %) mit, wenn das Diagramm wächst; Rückfahrt nur für Maßstab.
- **Übergänge:** Strich zeichnet sich (Trim), Element wird durchgestrichen und ersetzt, Pfeil führt ins nächste Bild,
  Radierer wischt. Am Ende einer Einblendung: alles zieht sich zum Punkt oder wird weggewischt (0,3 s).
- **Easing:** Strich `power1.inOut` (zeichnet wie eine Hand), Kästen poppen `back.out(1.6)` in 0,25 s, Pfeile 0,35 s.

## Sound-Charakter

Leise und organisch: Filzstift-Kratzen beim Zeichnen (nur kurz, unter −20 dB), weiches Papier-Pop beim Erscheinen,
Radierer-Wischen. Keine Musik-Hits über der Stimme; Stimme hat Vorrang (Musik ≥ 16 dB darunter oder aus).

## Signature Moves (Bauweise)

1. **Rough-Strich zeichnet sich:** Formen mit rough.js (MIT) erzeugen (geseedet, `seed` fest), SVG-Pfade per
   `stroke-dashoffset` animieren, Füll-Schraffur 0,15 s nach dem Umriss. HyperFrames-Bausteine `whiteboard-ink`,
   `svg-stroke-trace` als Fundgrube.
2. **Boil/Leben:** Strichpfade alle 2–3 Frames leicht neu erzeugen (3 Seeds im Wechsel, `hw-boil`-Prinzip), nur bei
   Haltezeiten > 2 s, sonst ruhig.
3. **Pfeil mit Absicht:** gekrümmter Pfeil (Bézier mit leichtem Bogen), Spitze erscheint als letzter Frame-Schlag.
4. **Durchstreichen + Ersetzen:** roter Strich über das Alte in 0,2 s, das Neue zeichnet sich daneben.
5. **Zählen durch Menge** (Vox-Logik): ein Kasten wird zu N Kästen im Raster, Nummern ticken, Kamera zieht zurück.
6. **Marker-Strich:** halbtransparenter gelber Balken (`mix-blend-mode: multiply`) unter dem Schlüsselwort, wächst
   von links in 0,25 s.

## Slop-Fallen

- Perfekte Rechtecke mit Handschrift-Font = Folie im Kostüm. Strich muss unregelmäßig sein (rough.js roughness 1–1,5).
- Alles erscheint auf einmal. Ein Element pro Satzteil.
- Den gesprochenen Satz hinschreiben (Echo). Nur Etiketten am Objekt.
- Icons aus Icon-Sets in Kacheln, Eyebrow-Punkte, Nummern 01/02/03.
- Zu dünne Striche/zu kleine Schrift im YouTube-Slot (Handy-Zuschauer).

## Variationen

- **Hell Papier** (Standard) · **dunkle Tafel** mit Kreide-Strich (für dunkle Videos) · **Rasterpapier** (simi 0:27).
- Mischen: Storyboard/Skizze (echte Fotos auf der Skizze), Clean SaaS (echter Screenshot wird in die Skizze geklebt).
- Eigenes: eigene Excalidraw-Boards als Ausgangsmaterial nachzeichnen lassen.

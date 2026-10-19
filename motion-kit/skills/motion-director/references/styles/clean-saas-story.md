# Stilkarte: Clean SaaS Story

**Wann wählen:** Produkt- oder Feature-Launch, Tool-Demo, „so funktioniert unser Ablauf". Immer dann, wenn echte UI
die Hauptrolle spielt und der Film **einen** Gedanken zeigen soll („Claude ist in jeder App", „ein Prompt findet Leads").
Der Maßstab für „simpel + ein Gedanke“ kommt aus dieser Karte (claude-google-workspace).

**Bildidee:** Die Kamera ist ein ruhiger Finger, der auf echte Oberflächen zeigt. Ein Objekt (Pille, Würfel, Icon,
Textzeile) wird über den ganzen Film zu etwas anderem. Kein Schnitt nötig, weil jedes Ding das nächste *ist*.

## Leitreferenzen (Grammatik, nie Inhalt)

Bögen: `refs/study/<slug>/sheet_*.jpg`, Einzelbild zur Zeit t: `frames/f_NNNN.jpg` mit NNNN = 2·t + 0,5 (alle 0,5 s).

| Ref | Zeit | Was passiert | Übernehmen |
|---|---|---|---|
| claude-google-workspace | 0:00–0:04 | drei App-Icons auf Creme, Serifen-Titel blendet darunter ein | Ruhe: 3 Elemente, Mitte, viel Luft |
| | 0:06–0:09 | Push vom ganzen Dokument in die Menüleiste bis „Extensions › Claude" bildfüllend, Cursor klickt | **Kamera taucht in das eine Detail, das zählt** |
| | 0:16 / 0:31 / 0:47 | koralle Verlaufswelle wischt über Doc, Sheet, Slides: das Ergebnis ist da | **ein „Magie-Moment", 3× gleich wiederholt** = Rhythmus durch Wiederholung |
| | 0:54–0:57 | Stern-Logo zeichnet sich, Wortmarke tippt sich Buchstabe für Buchstabe | Logo als letzte, kleinste Bewegung |
| tesseract-design | 0:00–0:04 | Chromwürfel schwebt in Wüste mit Wolken (Welt) | Held-Objekt in einer Welt statt Logo |
| | 0:04–0:09 | Würfel zerfällt zu gestapelten Design-Ebenen mit Etiketten (Texture, Shadows …) | **Objekt explodiert in seine Bestandteile** = Erklärung ohne Text |
| | 0:11–0:24 | UI-Karten, Prompt tippt, Würfel-Karte wird gezogen, Kamera taucht in die Karte | UI-Momente mit Cursor, Kamera folgt der Hand |
| | 0:25–0:31 | Welt wird VHS-Bild, Rückfahrt zeigt Röhrenmonitor im Raum, Logo auf dem Schirm | **Rahmenwechsel als Schluss** (Bild im Bild) |
| adipanda | 0:00–0:05 | riesiges „find lea…" unscharf, schrumpft zu kleinem Satz auf Verlauf, Wörter tauschen | Typo wechselt Maßstab statt Position |
| | 0:05–0:10 | Wort-Pille im Satz wächst zur Prompt-Box, Box schrumpft zur weißen Blase, wird „Lead Scout"-Pille | **Pille ↔ Box ↔ Pille**: jeder Übergang ist ein Morph |
| | 0:17–0:21 | X-Icon fliegt in 3D an, kippt, wird zur X-Oberfläche | Icon → App: Objekt öffnet sich zum Ort |
| | 0:38–0:42 | Karte schrumpft zurück in den Satz „find new [Logo] leads today" | Kreis schließt sich: Ende = Anfang |

## Messwerte (motion_check 11.10.2026)

| | Wechsel/10 s | Median-Einstellung | längste | harte Schnitte | „eingefroren" |
|---|---|---|---|---|---|
| claude-google-workspace | 1,3 | 3,0 s | 31 s (eine Fahrt) | 0 | 24 s (gewollte Halte) |
| tesseract-design | 5,4 | 1,4 s | 5,0 s | 0 | 0 |
| adipanda | 3,6 | 2,2 s | 5,4 s | 0 | 0 |

- Übergänge 0,5–1,0 s, fast alle als Morph oder Kamerafahrt, **keine harten Schnitte**.
- Text: 3–6 Wörter pro Satz, klein (≈ 40–56 px @1080p), zentriert; UI-Text echt und lesbar gehalten (≥ 1,5 s).
- Achtung: claude-google-workspace fällt durch `motion_check` (19 harte Flags, Tempo 1,3) und ist trotzdem der
  Lieblingsreferenz. Für die ruhige Variante gelten die Stil-Schwellen in `motion-director/references/rules.md`.

## Startwerte (Ausgangspunkt, nicht Gesetz)

- **Farbe:** hell: Creme #F7F5F0 / Off-White, Tinte #1A1A1A, **ein** Akzent (Koralle #D97757 oder Markenfarbe),
  Akzent nur im Magie-Moment. Dunkel-Variante (tesseract): Pflaume #1B1020, Orange-Glut #F08A4B, Violett #7E5BEF.
  Verlauf-Variante (adipanda): weich geblurrte Cyan/Blau/Rosa-Felder, nie hart.
- **Typo:** eine Grotesk (Inter, Geist, Söhne-artig) + optional eine Serife für Titel (Instrument Serif, Newsreader).
  Titel 56–72 px, Satz 40–48 px, Gewicht 400–500 (nicht fett). Kursiv-Serife als Akzent im Sans-Satz ist erlaubt.
- **Komposition:** ein Ding in der Mitte, ≥ 40 % Leerraum; UI wird bildfüllend gezeigt, sobald die Kamera drin ist.
- **Kamera:** Push-in 1,0–1,5 s `power3.inOut` / in_out_quint auf ein Ziel, dann ≥ 1 s Halten mit 1–2 % Drift.
- **Übergänge:** Morph (Pille ↔ Box), Dive (Kamera fährt in Karte), Wipe-Welle (Verlauf wischt Ergebnis frei).
- **Easing:** Ankunft expo-out 0,4–0,6 s; UI-Elemente Feder mit 3–5 % Überschwinger; Text-Blur-in 0,4 s (blur 12→0 px).

## Sound-Charakter

Leise, trocken, präzise. Echte UI-Klicks (−14 bis −10 dB unter Musik-Peak), weiche Luft-Whooshes nur bei Dives,
ein heller „Magie"-Schimmer im Ergebnis-Moment, Musik minimal (Piano/weiche Elektronik 90–110 BPM) oder gar keine.
Stille vor dem Logo (3–8 Frames).

## Signature Moves (Bauweise)

1. **Pillen-Morph** (Wort → Box → Pille): HTML-Element mit `border-radius`, `width/height` über einen FLIP-Wrapper
   (`transform: scale` auf Außen-, Gegen-Skalierung auf Innen-Element), Text per Crossfade 4 Frames. GSAP Timeline.
2. **Dive in die UI:** Kamera-Wrapper (`div` mit `transform-origin` auf dem Ziel) `scale 1→3.5` in 1,2 s
   `power3.inOut`, Motion Blur nur während der Fahrt (HyperFrames-Komponente `motion-blur` auf dem bewegten Kind).
3. **Magie-Welle:** radialer/linearer Verlauf (Akzent → transparent) als Maske, fährt in 0,8 s über die Fläche; darunter
   wechselt der Zustand (alt → neu). CSS `mask-image` + `background-position`-Tween; Grain darüber.
4. **Objekt explodiert in Ebenen:** 6–12 gleiche Ebenen (CSS-3D `translateZ` gestaffelt, `rotateX 55° rotateZ -35°`),
   Abstand 0 → 40 px mit Stagger 40 ms, Etiketten an Haarlinien. Three.js nur, wenn Licht/Material nötig ist.
5. **Rahmen-Rückfahrt:** die ganze Szene als Unter-Komposition in einen Monitor/Rahmen legen, Kamera zieht zurück
   (`scale 1 → 0.35`), Scanlines/Rundung erst ab 50 % des Wegs.

## Slop-Fallen

- Verlauf-Glaskarten im Raster mit Icons und Eyebrow-Text = der KI-Standardlook. Nie mehr als **eine** Karte im Fokus.
- Feature-Tour (5 Features, je 3 s). Eine Mechanik zeigen, höchstens 3× wiederholen.
- UI klein in viel Weiß. Wenn UI, dann groß; wenn klein, dann als Objekt (Icon, Pille).
- Erfundene UI mit Lorem-Text. Echte Screens oder sauber nachgebaute mit echten Inhalten.
- Alles fadet von unten rein. Ankunft ist Morph, Dive oder Maßstabswechsel.

## Variationen

- **Hell + Serife** (Workspace) · **dunkle Welt + Held-Objekt** (Tesseract) · **Verlauf + Pillen-Morph** (adipanda).
- Mischen: Held-Objekt-Welt aus 3D-Objekt-Story als Rahmen, Clean-UI im Inneren.
- Eigenes einbringen: eine Materialität (Papier, Glas, Druckraster) durchhalten statt Standard-Verlauf.

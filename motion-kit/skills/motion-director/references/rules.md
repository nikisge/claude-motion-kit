# Prüfregeln mit Zahlen

Startwerte aus dem Lernpfad (`content/youtube/planning/premium-motion-graphics/referenzen/lernpfad-bibliotheken-2026-10-11.md`)
und eigenen Messungen. Stilkarten dürfen abweichen; die Abweichung steht dann in der Karte oder im Brief.

## Bewegung

| Regel | Wert |
|---|---|
| Eintritt eines Elements | 0,3–0,6 s, `expo.out` (0.16, 1, 0.3, 1) |
| Austritt | 0,2–0,3 s, `power3.in`, oder harter Schnitt |
| Kamerafahrt | 0,8–4 s, in-out (0.65, 0, 0.35, 1) oder `sine.inOut` |
| Dinge mit Gewicht (UI, Objekte) | Feder (Steifigkeit ~300, Dämpfung ~26), 4–8 % Überschwinger |
| Weg eines Elements | 40–120 px @1080p; Skalierung ab 0,9–0,96 (nie von 0); Rotation ≤ ±6° |
| Stagger | Listen 60–120 ms · Wörter 40–60 ms · Buchstaben 20–40 ms |
| Ursache → Wirkung | Wirkung 4–8 Frames nach dem Auslöser |
| Beat | Ankunft 2–3 Frames **vor** dem Schlag fertig |
| Animierte Eigenschaften | nur `transform` und `opacity` (Filter/Blur sparsam: teuer und ruckelt) |
| Motion Blur | nur auf schnellen Bewegungen, die das Auge nicht lesen soll; **nie auf Lesefahrten** über Seiten/Text |
| Drift in Haltezeiten | 1–3 % Zoom oder Schwenk über die Einstellung |
| Tiefe | ≥ 3 Ebenen mit Parallaxe; Schärfe trennt Ebenen |
| Eine laute Sache | pro Einstellung führt **ein** Element; der Rest steht oder driftet |

## Text und Lesbarkeit

| Regel | Wert |
|---|---|
| Lesezeit | 3 Wörter/s + 1 s (Einzelwort ≥ 0,4 s) |
| Untertitel | ≤ 20 Zeichen/s, ≤ 42 Zeichen/Zeile, ≤ 2 Zeilen |
| Größen @1080p | Hero 140–200 px · Titel 96–120 · Text 44–60 · Beschriftung/Untertitel ≥ 28 |
| Im YouTube-Slot (1114 × 886) | Etiketten ≥ 32 px, höchstens 6 im Endbild |
| Schriften | 1–2 Familien; Display eng gesetzt (−1 … −3 %) |
| Kontrast | ≥ 4,5:1 für Text (`npx hyperframes check` misst WCAG) |
| Sicherheitsrand | 8–10 % am Bildrand; vertikal: oben ~220 px, unten ~420 px, rechts ~140 px frei |
| Werte vor Farbe | Graustufen-Probe: Hauptobjekt hebt sich auch ohne Farbe ab; max. 3 Farben + Neutrale, Akzent nur am Ziel des Auges |
| Negativraum | großzügig; UI groß im Bild, nicht klein in viel Weiß |

## Zeit und Tempo

| Regel | Wert |
|---|---|
| Einstellungslängen | Titel 2,5–4 s · Inhalt 4–8 s (mit Bewegung darin) · Outro 2–3 s |
| Hook | Social ≤ 1,5 s, Launch ≤ 3 s; Bewegung ab Frame 1 |
| Payoff | alle 3–5 s etwas Unerwartetes (Objektverwandlung, Kamera-Überraschung, Schlag) |
| Leseruhe | langsame Fahrt auf das nächste Ziel, **kein Einfrieren** |
| Endkarte | letzte 3 s; Logo landet ≤ 0,6 s davor; Claim nicht früher |
| Musik-Tempo | 60–80 BPM edel · 90–110 ruhig-modern · 115–128 kinetisch |

Gemessenes Referenz-Tempo (Bildwechsel/10 s, `motion_check` 11.10.2026): Apple-Montage 7,5 · how-do-you-
communicate 8,8 · higgsfield 5,9 · tesseract 5,4 · kimi-3 4,9 · glyph 4,0 · adipanda 3,6 · Apple-Wonderful-Tools
2,0 · claude-google-workspace 1,3 · eigene Folien-Fassung 1,2. Tempo allein macht keine Qualität: der ruhigste
Film (claude-google-workspace) war im Test der Maßstab für „simpel + ein Gedanke“.

## `motion_check` nach Stil

`uv run motion-inspo/scripts/motion_check.py render.mp4 [Optionen]`. Der Standard ist auf Launch-Tempo kalibriert; ruhige Stile
brauchen andere Schwellen. **Immer hart, in jedem Stil:** `headline_slide`, `echo`.

| Stil | Optionen | Was erlaubt ist |
|---|---|---|
| Launch, Storyboard/Skizze, 3D-Objekt | Standard (`--max-shot 3.5 --long-shots 1 --min-tempo 3`) | 0 harte Flags; eine geplante lange Fahrt |
| Kinetic Type | `--max-shot 2.5 --min-tempo 5` | 0 harte Flags |
| Clean-SaaS hell, Apple-Premium | `--max-shot 8 --long-shots 2 --min-tempo 1.5 --end-card 4` | `frozen` nur an geplanten Haltepunkten (im Storyboard als „Halt" markiert, je ≤ 2,5 s); `static_sentence` nur bei echtem UI-Inhalt, der seine Lesezeit braucht. Jede Ausnahme in `check/notes.md` mit Zeitstempel begründen |
| Whiteboard-Einblendung | `--max-shot 13 --long-shots 3 --min-tempo 1.5 --script abschnitt.txt` | lange Bilder, wenn ständig ein Element dazukommt; `echo` hart |
| Social vertikal | `--max-shot 3 --min-tempo 5` | 0 harte Flags |

Bestanden heißt nur „keine bekannte Slop-Form". Ob es gut ist, entscheidet der Critic an den Bildern.

## Vor dem Critic (Reihenfolge)

1. **Asset-Bogen** geprüft (Masken, Schatten, Schrift).
2. **Render ↔ Animatic/Style Frame** je Storyboard-Zeile als Vollbild vergleichen; mittlere Abweichung ≤ 5 Stufen
   (0–255), Markierungen pixelgenau. Größere Abweichung = Engine-/Cache-Fehler, nicht Geschmack. Assets nach
   Neubau unter **neuem Dateinamen** ablegen, Engines cachen nach Pfad.
3. `motion_check` nach Stil grün.
4. Einzelbilder an jedem Übergang (4 Bilder/s Kontaktbogen) selbst angesehen.

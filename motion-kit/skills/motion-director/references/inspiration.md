# Inspiration: Referenzen finden und in Grammatik zerlegen

Referenzen sind **Grammatik, nie Vorlage**. Übernommen werden Tempo, Übergangsarten, Kameraverhalten,
Typo-Verhalten, Ton-Rolle. Nie Inhalt, Layout 1:1, Farben einer fremden Marke oder Assets. Clips gehören ihren
Urhebern: nur lokal studieren (`refs/clips/` ist gitignored), nie hochladen.

## Modus „Inspo nachbauen“ (jeder neue Film, Pflicht im Showcase)

Wie bei Webseiten: Man muss gute Beispiele geben. Stilkarten allein reichen nicht, darum hat **jeder Film
genau eine Ziel-Referenz**: vom Nutzer genannt, sonst selbst gewählt (Produkt-/3D-Film z. B. `kimi-3-couldve-never-done-this`;
sonst ein passender Clip aus `motion-inspo/references/referenzfilme.md` im gewählten Stil). Nachbauen heißt **Grammatik und
Niveau** treffen (Tempo, Einstellungsgrößen, Kamera, Material, Licht, Textmenge), nie Produkt, Inhalt, Marke, Farben 1:1.

1. **Messen**: `uv run motion-inspo/scripts/ref_metrics.py <ref.mp4> --no-ocr` (Schnitte und neue Ansichten je 10 s, Einstellungs-
   längen, Text-, Leer- und Steh-Anteil, Bildänderung, Helligkeit/Kontrast/Sättigung, Einstieg 0–2 s).
2. **Shot für Shot zerlegen** (Bogen mit 4 Bildern/s, `sheet.py --every 0.25`) in `projects/<name>/ref.md`:
   ```markdown
   | # | Zeit | Dauer | Einstellung | Kamera | Objekt / was passiert | Material / Licht | Übergang |
   |---|---|---|---|---|---|---|---|
   | 1 | 0,0–1,1 | 1,1 | Totale, Raum | Push-in, 35 mm | Gerät auf Tisch | warmes Fensterlicht | harter Schnitt auf Makro |
   ```
   Einstellung = Makro / Nah / Halbnah / Totale; Kamera = Fahrt, Richtung, Brennweite geschätzt, Schärfe.
3. **Ziele ableiten** (in den Brief): Schnittdichte und neue Ansichten ≥ 80 % der Referenz; Textanteil ≤ Referenz
   + 10 Punkte; keine leere Strecke > 0,3 s außer geplanter Stille; Einstieg bewegt sich ≥ 80 % der Referenz;
   „Kamera steht“ ≤ Referenz + 15 Punkte; Kontrast/Sättigung in der Nähe der Referenz, sonst begründen.
4. **Prüfen**: `uv run motion-inspo/scripts/ref_metrics.py render.mp4 --ref <ref.mp4> --out check/metrics` gibt beide nebeneinander
   und hakt die Ziele ab. Die Tabelle geht an den Critic. Beispielzeile siehe oben.

Lehre aus Kimi-3 (gemessen): nur 4,3 harte Schnitte je 10 s, Median-Einstellung 1,8 s; die gefühlte Dichte („jede
Sekunde ein neues Bild“) kommt aus schnellen Kameraflügen (Bildänderung 5,7 je Bild, Kamera steht nur 14 %), Makros
mit Tiefenunschärfe und Materialwechseln. Viele Schnitte allein holen das nicht ein. OCR zählt Beschriftungen auf dem
Produkt (Tasten) als Text: Textanteil immer an den Bildern gegenprüfen.

## Quellen (in dieser Reihenfolge)

1. **Stilkarten** `motion-director/references/styles/`: Leitreferenzen mit Zeitstempeln und Messwerten, schon zerlegt.
2. **Referenzfilme nach Stil** `motion-inspo/references/referenzfilme.md` (50 Links mit Stil und Notiz) und
   dein eigener Geschmack: Lege `refs/taste.md` an (was dich begeistert, was „Slop“ ist) und halte ihn aktuell.
   Bereits studiert: `refs/study/<slug>/` (Bogen, Einzelbilder, Schnitte, Tempo).
3. **Neue Clips** mit `motion-inspo/scripts/refs.py`:
   ```bash
   cd MS
   python3 motion-inspo/scripts/refs.py search product launch 3d keyboard --n 15   # ~2.500 X-Launchvideos + 55 kuratierte
   python3 motion-inspo/scripts/refs.py get <x.com-status|whatships|youtube|vimeo-url> --name <slug>
   python3 motion-inspo/scripts/refs.py study <slug> --every 0.5                    # Bilder, Bogen, Schnitte, Tempo
   uv run motion-inspo/scripts/motion_check.py refs/clips/<slug>.mp4 --out refs/study/<slug>/check   # Messwerte
   ```
   Für das Review mit dem Nutzer: die wichtigsten Momente als Zeitfenster notieren und als Kontaktbögen zeigen
   (Bildfolgen, Clips, Bögen, Crops, Paletten) und `tools/review.py` (Moodboard-Seite), siehe SKILL.md „Review-Ablauf“.
   Suchbegriffe englisch, nach **Bewegung** statt Branche: „camera dives into ui", „kinetic type scale jump",
   „object becomes logo", „paper collage top down".
4. **Bibliotheken, Skills, Inspo-Seiten**: `RESOURCES.md` im Repo-Hauptordner
   (`content/youtube/planning/premium-motion-graphics/referenzen/lernpfad-bibliotheken-2026-10-11.md`).

Einzelbild zu Zeitpunkt t: `refs/study/<slug>/frames/f_NNNN.jpg` mit NNNN = 2·t + 0,5 (bei `--every 0.5`).

## Wie viele

Normaler Auftrag: 2–3 Referenzen. Neuer Film: 3–6. Showcase: 4–8 aus mindestens zwei Stilwelten. Mehr ist
Prokrastination: nach dem Zerlegen wird gebaut.

## Zerlegen (je Referenz ≤ 10 Zeilen in `projects/<name>/brief.md` oder `refs.md`)

```markdown
### <slug> (<Urheber>, <Link>)
- Messung (`ref_metrics`): <Schnitte/10 s> · <neue Ansichten/10 s> · Median-Einstellung <s> · Text <%> · steht <%>
- Grammatik:
  - 0:02–0:04 Übergang: <was trägt wohin> (Objekt-Match / Schnitt auf Beat / Iris aus Bildteil …)
  - 0:05 Kamera: <Fahrt, Ziel, Dauer, Kurve geschätzt>
  - Typo-Verhalten: <wie Text erscheint, Größe, wie lange>
  - Ton-Rolle: <Musik führt/trägt, Akzente worauf>
- Nehmen wir: <1–2 Dinge, konkret>
- Nehmen wir nicht: <was nicht zu unserem Auftrag/Geschmack passt>
```

Gute Fragen beim Ansehen (Bogen mit 4 Bildern/s, nicht nur 1/s):
- Wo ist **die eine laute Sache** in jeder Einstellung?
- Was trägt den Übergang? Was passiert in den 3–6 Frames um den Schnitt?
- Wo steht die Kamera still, und warum hält das Bild trotzdem (Drift, Licht, Nebenbewegung)?
- Wie lange ist Text sichtbar, wie viele Wörter? (Gegen die Lesezeit-Regel prüfen.)
- Was ist der Staun-Moment, und wie würde ich ihn mit meinem Werkzeug bauen?

## Gegen Gleichförmigkeit

- Nicht zweimal hintereinander dieselbe Stilkarte als Hauptstil, wenn der Auftrag es nicht verlangt.
- Mischen: Grammatik aus zwei Karten (z. B. Storyboard-Ablegen + 3D-Licht-Welle).
- Eigener Einfall aus dem **Auftrag** ableiten (Material, Objekt, Ort des Kunden), nicht aus der Referenz.
- Was in Tests als „Slop“ markiert wurde (motionmaxxing, interface, oki-home: Neon-Glow-Titel, glatte Generik), ist Anti-Referenz.

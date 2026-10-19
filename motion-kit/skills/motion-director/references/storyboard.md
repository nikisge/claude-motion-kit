# Storyboard und Animatic

## Vertrag (`projects/<name>/storyboard.md`)

Eine Zeile pro Einstellung. **Alle Spalten außer „Typo" sind Pflicht.** Eine leere Pflichtspalte heißt: die
Einstellung ist noch nicht gedacht. Eine Spalte für Überschrift oder Fließtext gibt es nicht.

| # | Beat (s / Frame) | Bild: was man passieren sieht | Bewegung + Auslöser | Kamera | Übergang raus (Objekt) | Typo (opt., ≤ 1 Wort, am Objekt) | Ton | Werkzeug | Referenz |
|---|---|---|---|---|---|---|---|---|---|

- **Bild** ist ein Vorgang mit Verb: „Etikettenband reißt, Lampe springt auf Rot", nicht „Problem: Stillstand".
- **Bewegung + Auslöser:** was bewegt sich wodurch (Klick, Beat, Ursache aus der Vorzeile). Wirkung 4–8 Frames
  nach der Ursache.
- **Kamera:** Fahrt/Schwenk/Zoom mit Richtung und **Ziel** oder „steht, Drift 2 %". Vor jeder Fahrt muss ihr Ziel
  lesbar sein, am Ziel ≥ 0,8 s Halt (als langsame Weiterfahrt, nicht als Einfrieren).
- **Übergang raus:** welches Objekt in die nächste Einstellung trägt. „Schnitt auf Beat" erlaubt, „Blende" nur mit
  Grund.
- **Typo:** ein Wort/eine Zahl am Objekt oder auf dem Beat; ganze Sätze nur als echter UI-Inhalt.
- **Ton:** das hörbare Ereignis oder „Stille". Grundlage für die Cue-Liste (`motion-sound`).
- **Referenz:** slug + Zeitstempel der Grammatik, die diese Zeile nimmt.

## Satz → Bild

Frage immer: **Was müsste man filmen, damit der Satz ohne Text verstanden wird?**

| Aussage | Folie (so nicht) | Bild, das es zeigt |
|---|---|---|
| „Jede Antwort mit Beleg" | Headline + Haken-Icon | Kamera folgt der Quellenpille in die Seite, die Zeile leuchtet auf |
| „Wissen auf tausende Seiten verteilt" | Headline + Stapel-Grafik | Rückwärtsfahrt aus einer Seite, bis tausende Seiten schweben |
| „Weniger Stillstand" | Balkendiagramm | Lampe springt von Rot auf Grün, das Band läuft wieder |
| „300 € jeden Monat" | Zahl links, Satz rechts | Kalenderblätter fallen, ein Zähler bucht je Blatt 300 € ab |
| „10x schneller" | zwei Balken | zwei Spuren starten gleichzeitig, eine ist fertig, die andere lädt noch |
| „Daten bleiben lokal" | Schloss-Icon | Datenpaket will hinaus und prallt an der Gehäusewand ab |

Muster: **Vergleich** = gleichzeitiger Start · **Menge** = Kamera zieht zurück · **Prozess** = ein Objekt wandert
durch die Stationen · **Ursache → Wirkung** = Auslöser, Wirkung 4–8 Frames später · **Zahl** = Objekt in der Welt.

## Dramaturgie wählen (nicht immer dieselbe)

| Muster | Ablauf | passt zu |
|---|---|---|
| Problem → Fall → Beweis → Ergebnis → Marke | 5 Akte (`formats.md`, Launchfilm) | Produkt-Launch |
| Ein Gedanke, eine Fahrt | eine durchgehende Kamerafahrt durch ein Objekt | Clean-SaaS, Apple-Feature |
| Manifest | Wort pro Takt, Bilder dazwischen, Kollaps ins Logo | Kinetic Type, Showreel-Intro |
| Ursprung → Prozess → Ergebnis | Dinge werden hingelegt, Status-Karten, Ergebnis wächst | Storyboard/Skizze |
| Frage → Diagramm wächst → Standbild | Element pro Satzteil, Endbild ist verständlich | Whiteboard-Einblendung |
| Kapitel mit Stilwechsel | jede Passage eine andere Stilkarte, ein roter Faden | Showcase, Showreel |

Im Standardprozess für Launchfilme 2–3 Varianten (anderer Haken, anderes Herzstück) skizzieren, eine wählen und
die Wahl begründen (der Nutzer entscheidet, im One-Shot du).

## Animatic

- **Beat-Raster:** `uv run motion-inspo/scripts/beats.py track.mp3 --fps 30 --out <projekt>/beats.json` (oder `--bpm 120 --dur 30 --out …`). Haupt-
  ereignisse auf Downbeats, Nebenbewegungen auf Schläge, nichts Wichtiges daneben. Einblendungen: Wort-
  zeiten aus dem Transkript statt Musik, Wirkung ~80 ms vor dem Wort.
- Grob, aber **mit echtem Timing und echten Kamerafahrten**: Style-Frame-Ebenen, die sich bewegen. Kein Feinschliff.
- Gleich gegen `motion_check` messen (Schwellen je Stil in `rules.md`): Flags im Animatic sind billig, im fertigen
  Film teuer.
- Endkarte = letzte 3 s; das Logo landet ≤ 0,6 s davor. Claim nicht früher einblenden.
- Kontaktbogen (`python3 motion-inspo/scripts/sheet.py animatic.mp4 check/animatic --every 0.25`) ist die Abgabe für das Gate
  bzw. für Critic-Durchgang 1.

## Beispiel (fiktive Belege-App, falsch → richtig)

| Fassung | Bild | Bewegung + Auslöser | Kamera | Übergang raus | Typo |
|---|---|---|---|---|---|
| Folie | „Belege in Sekunden erfassen." oben links, Screenshot darunter | Text fährt hoch, Bild blendet ein | steht | Überblendung | ganzer Satz |
| richtig | Kassenbon liegt auf dem Tisch, der Kamerarahmen der App rastet auf ihm ein, Betrag und Datum heben sich vom Papier und landen im Formular | Einrasten auf Downbeat, Felder fliegen auf die Achtel | Push-in auf den Bon, Tisch unscharf | das Formular wird zur Kachel in der Monatsliste | „0,8 s" am Timer |

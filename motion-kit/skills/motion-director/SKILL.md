---
name: motion-director
description: "Use when making or revising any motion graphics piece or styled AI video (launch film, documentary-style clip, explainer animation, YouTube insert, whiteboard graphic, social/vertical clip, showreel, one-shot showcase, 3D world) and before writing scene code; also when a motion piece looks like slides, a website or generic AI output, or feels static or slow. Runs the three steps Inspo, Werkzeugkasten (HyperFrames, Higgsfield, this kit), Feinschliff. Trigger words: Motion Graphics, Animation, Launchvideo, Erklärvideo, Doku-Stil, Einblendung, Showcase, Stil, KI-Slop, \"wie ein Motion Designer\"."
---

# Motion Director: arbeiten wie ein Motion Designer

Das Modell kann animieren. Was fehlt, sind **Geschmack, konkrete Vorbilder und ein Ablauf mit Prüfungen**. Ohne das
baut es eine Website, die sich bewegt: Kästen, Karten, Verläufe, alles blendet von unten ein. Dieser Skill gibt den
Ablauf in drei Schritten vor, die Werkzeuge kommen aus den anderen Skills.

Grundhaltung:
- **Nie von null drauflos.** Ohne konkrete Referenz rät das Modell, und das Ergebnis sieht aus wie jedes KI-Video.
- Referenzen liefern **Grammatik** (Tempo, Übergänge, Kamera, Ton), nie Inhalt.
- **Ein Film, ein Stil**, höchstens ein passender zweiter als eigener Dreh. Dazu mindestens ein eigener Einfall.
- **Story und Inspo legt der Nutzer fest**, der Agent hat Freiheit bei Shots und Umsetzung.
- Du baust **eigene** Komponenten. Kataloge (HyperFrames-Registry) sind Fundgrube, kein Baukasten.

Projekte liegen in `projects/<name>/` im Arbeitsordner.

## Den Weg wählen

| Auftrag | Weg |
|---|---|
| neuer Film (Launch, Doku, Erklärer, Showreel, 3D-Welt) | die drei Schritte unten |
| YouTube-Einblendung, Whiteboard-Grafik | die drei Schritte, schlank: Wortzeiten statt Musik (`references/formats.md`) |
| „One-Shot“, „zeig, was du kannst“, Test ohne Rückfragen | One-Shot-Modus (unten) |
| kleiner Auftrag (eine Szene, Logo-Sting, Fix nach Feedback) | Ziel in einem Satz, Storyboard-Zeile anpassen, bauen, Ausschnitt prüfen (`motion_check --from/--to`), zeigen |

## Schritt 1: Inspo

1. **Brief** (`references/brief.md`): ein Satz Wirkung („Danach weiß/fühlt der Zuschauer: …“), Format, Ton-Rolle.
   Bei erzählten Formaten steht die Story vorher fest.
2. **Stil wählen:** Stilkarte aus `references/styles/README.md`. Eine Karte, bewusst gewählt und in einem Satz begründet.
3. **Ziel-Referenz:** ein konkreter Film, dessen Grammatik und Niveau du treffen willst (`motion-inspo`, whatships,
   YouTube). Messen (`ref_metrics.py`) und Shot für Shot zerlegen (`references/inspiration.md`). 1–2 weitere
   Referenzen nur als Grammatik.
4. **Geschmack laden:** `refs/taste.md` lesen (siehe „Learnings speichern“). Was dort als Slop steht, ist verboten.

## Schritt 2: Werkzeugkasten

Drei Bausteine, jeder für das, was er am besten kann:

| Baustein | Wofür | Skill |
|---|---|---|
| **HyperFrames** | Hier wird alles gebaut: Kamera, Typo, Grafik, Masken, Übergänge, Three.js, Schnitt. Code wird Video | `motion-hyperframes`, 3D: `motion-3d` |
| **Higgsfield** | was Code nicht kann: echtes Video neu zeichnen (Genjutsu), gestaltete Welten (Seedance, Kling), Bilder als Bausteine, Bild → 3D-Modell, Musik und Foley. Immer mit Preis vorher | `motion-higgsfield` |
| **Dieses Kit** | Prozess, Stilkarten, Storyboard, Prüfwerkzeuge, Ton | `motion-inspo`, `motion-sound`, dieser Skill |

Reihenfolge im Werkzeugkasten:

1. **Storyboard-Review-Seite** (`references/storyboard.md`): Richtungen, Spannungskurve, Shotliste, Style Frames
   (`references/style-frames.md`), Kostentabelle, Risiken. **Gate: der Nutzer entscheidet an Bildern.** Das ist der
   am besten belegte Hebel des ganzen Kits.
2. **Animatic** auf dem Beat-Raster oder den Wortzeiten. Gleich gegen `motion_check` messen.
3. **Generierungen** (falls geplant): erst Entwurf in niedriger Auflösung, Kontaktbogen, dann Final. Preis je Job vorher.
4. **Bauen**, die schwerste Einstellung zuerst. Änderungen immer zuerst ins Storyboard, dann in den Code.
5. **Ton** mit `motion-sound` (Cue-Liste, Mix auf −14 LUFS). Gibt es eine Stimme, bestimmt sie die Bildzeiten.

Welches Material wofür:

| Wenn | Werkzeug |
|---|---|
| UI, Typo, 2,5D-Kamera, SVG, Karten, Diagramme, Papierschnitt | HyperFrames |
| Produkt, Metall, Glas, Tiefenunschärfe; stilisierte 3D-Welt | `motion-3d` (Three.js), Modelle optional aus Bild → 3D |
| echte Vergangenheit, echte Personen, echte Orte | **echtes Archivmaterial** (gemeinfrei), nie KI-„Archivfotos“ |
| gestaltete Welt, Material-Look, Figur in Bewegung | Videomodell oder Genjutsu (`motion-higgsfield`), Schrift und Übergänge aus Code |
| Ton | `motion-sound` |

## Schritt 3: Feinschliff

1. **Selbst prüfen:** `motion_check` mit den Schwellen des Stils (`references/rules.md`), `ref_metrics` gegen die
   Ziel-Referenz, Kontaktbogen mit 4 Bildern/s, Lesbarkeit am echten Frame.
2. **Ton prüfen:** Report von `sound_place`, `sound_verify` am fertigen MP4, optional
   [Earshot](https://github.com/Leonxlnx/earshot) `critique` (`motion-sound`). Am Ende hört ein Mensch mit Kopfhörer.
3. **Feedback vom Nutzer:** Gefühl plus Zeitstempel („der Sound nach dem Ring ist zu extrem, 15 s“), kein
   3-Seiten-Prompt. Jede Rückmeldung in Storyboard-Sprache übersetzen (Bild / Bewegung / Kamera / Übergang / Ton).
4. **Höchstens 2 Korrekturrunden**, dann die beste Fassung abgeben und Schwächen ehrlich nennen. Feedback rettet kein
   geratenes Konzept: Wenn es nach zwei Runden nicht trägt, zurück zu Schritt 1.
5. **Optional: unabhängiger Critic** (`references/critic.md`), ein frischer Subagent, der nur Bilder und Zahlen sieht.
   Nützlich für Bildfehler an Nähten, kein Pflichtschritt.
6. **Fertigstellen:** Export 10 Bit + feines Korn gegen Banding, 8-Bit-Kopie zum Teilen, kurzer Bericht.

## Learnings speichern

Damit jeder Film besser startet als der letzte:
- **`refs/taste.md`** im Arbeitsordner: Referenzen, die der Nutzer gut fand (mit Zeitstempel und warum), und
  Anti-Referenzen („Slop“, mit dem Satz, den er dazu gesagt hat). Vor jedem Film lesen.
- **`projects/<name>/DECISIONS.md`**: was nur für diesen Film gilt (Story, abgelehnte Richtung, Pegel).
- **Allgemeines** wandert in die Stilkarte oder den Skill, wo es hingehört. Hat ein Film einen neuen Stil etabliert,
  der funktioniert hat: neue Stilkarte (`references/styles/README.md`, „Neue Karte anlegen“).
- Lob auch speichern: Was gut ankam, ist genauso wertvoll wie eine Ablehnung.

## One-Shot- / Showcase-Modus

Keine Rückfragen, kein Warten auf Freigaben, all-out (`references/formats.md` → Showcase).
1. **Ideen-Runde** (`brief.md`): 5 Story-Ideen in je einem Satz. Streiche die erste und jede, deren Held ein
   Werkzeug des Fachs ist (Keyframe, Zeitleiste, Kurve, Cursor).
2. Brief, Stil, Ziel-Referenz, eigener Einfall: selbst entscheiden und begründen.
3. **Mindestens zwei Staun-Einstellungen** planen (Technik, Sekunde, Grund) und zuerst bauen.
4. Storyboard-Seite für dich selbst, optional Critic vor dem Animieren.
5. Bauen, prüfen, Ton, optional Critic am Ende. Bei niedrigem „Staunen“ die Staun-Einstellungen stärker machen statt
   Kleinigkeiten zu polieren. Credits nur innerhalb eines vorher gesetzten Deckels.

## Die Sätze, die alles entscheiden

- **Jede Einstellung ist ein Bild, das etwas tut**, kein Satz mit Illustration. Text höchstens ein Wort am Objekt.
- **Jeder Übergang ist ein Objekt** (Display wird UI, Rahmen wird Fenster, Lichtpunkt reist weiter). Überblenden ist
  der Notfall.
- **Ein roter Faden** (Linie, Faden, Lichtpunkt, Objekt) läuft durch alle Einstellungen.
- **Nichts steht ohne Grund still:** Leseruhe ist eine langsame Fahrt, kein Einfrieren. **Stille ist geplant:**
  vor dem Treffer 0,5–1 s Atem.
- **Eine laute Sache pro Einstellung.**
- **Keine Folien- und Website-Karten** (Titel + Text, Feature-Kacheln, Icon-Raster, Nummern 01/02/03, Eyebrow-Labels)
  und **keine typische KI-Endkarte** (Logo + Claim + URL auf leerer Fläche).
- **Das stärkste Bild gehört in die ersten 2 Sekunden.** Der Film beginnt mitten in der Bewegung.
- **Videomodelle für gestaltete Welten, nicht für Wirklichkeit.** Fotorealistische KI-Szenen wirken schnell billig.

## Was in Tests am meisten gebracht hat

1. **Konkrete Inspo zuerst** und eine gemessene Ziel-Referenz. Gefühlte Dichte kommt meist aus Kamerafahrten, nicht
   aus Schnitten.
2. **Das abgenommene Storyboard**, bevor eine Sekunde animiert oder generiert wird.
3. **Echtes Material im Film:** Archivkarten und -fotos, eigene Aufnahmen, die ein Modell neu zeichnet.
4. **Geschmack als Daten** (`refs/taste.md`) und Feedback mit Zeitstempeln.

## Referenzen

`brief.md` · `inspiration.md` · `storyboard.md` · `style-frames.md` · `rules.md` (Zahlen, Prüfschwellen) ·
`formats.md` · `styles/` (Stilkarten) · `critic.md` (optional)

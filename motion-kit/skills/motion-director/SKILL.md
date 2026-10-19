---
name: motion-director
description: "Use when making or revising any motion graphics piece (launch film, explainer animation, YouTube insert, whiteboard graphic, social/vertical clip, showreel, one-shot showcase) and before writing scene code; also when a motion piece looks like slides, a website or generic AI output, or feels static or slow. Trigger words: Motion Graphics, Animation, Launchvideo, Erklärvideo, Einblendung, Showcase, Stil, \"wie ein Motion Designer\"."
---

# Motion Director: arbeiten wie ein Motion Designer

Das Modell kann animieren. Was fehlt, sind **Geschmack, konkrete Vorbilder und ein Ablauf mit Prüfungen**. Dieser
Skill liefert genau das. Die Engine ist austauschbar (Standard: HyperFrames, HTML + GSAP + Three.js → MP4).

Grundhaltung:
- Du baust **eigene** Komponenten und ein **eigenes** Design für jeden Film. Kataloge (HyperFrames-Registry,
  Rezepte) sind Fundgrube, kein Baukasten.
- Referenzen liefern **Grammatik** (Tempo, Übergänge, Kamera, Typo-Verhalten), nie Inhalt.
- Gegen KI-Gleichförmigkeit: je Film **eine bewusste Stilentscheidung** plus **mindestens ein eigener Einfall**.
- Nie „von null drauflos“: Ohne konkrete Referenz rät das Modell, und das Ergebnis sieht aus wie jedes KI-Video.

Werkzeuge liegen im Skill `motion-inspo` (`scripts/refs.py`, `sheet.py`, `ref_metrics.py`, `motion_check.py`,
`beats.py`). Projekte liegen in `projects/<name>/` im Arbeitsordner.

## Erst den Auftrag lesen, dann den Weg wählen

| Auftrag | Weg | Format-Teil in `references/formats.md` |
|---|---|---|
| neuer Film (Launch, Erklärer, Showreel) | Standardprozess | Launchfilm / Erklär-Animation / Showreel |
| YouTube-Einblendung, Whiteboard-Grafik | Standardprozess, schlank (Wortzeiten statt Musik) | YouTube-Einblendung |
| Social / vertikal | Standardprozess, Hook zuerst | Social vertikal |
| „One-Shot“, „Showcase“, „zeig, was du kannst“, Test ohne Rückfragen | One-Shot-Modus | Showcase |
| kleiner Auftrag (eine Szene ändern, Logo-Sting, Zahl animieren, Fix nach Feedback) | schlanker Weg | – |

**Schlanker Weg:** Ziel in einem Satz, betroffene Einstellung im Storyboard anpassen (falls vorhanden), bauen,
`motion_check` auf dem Ausschnitt (`--from/--to`), Einzelbilder ansehen, zeigen. Kein neuer Brief, kein Critic.

## Standardprozess (neuer Film)

1. **Brief** (`references/brief.md`): ein Versprechen, ein Gedanke, Zielgefühl, Format, Marke, Ton-Rolle.
2. **Stil + Ziel-Referenz:**
   - Stilkarte(n) aus `references/styles/README.md` wählen, mischen oder eigene ableiten.
   - **Eine Ziel-Referenz** suchen (`motion-inspo`, whatships.com), messen (`ref_metrics.py`) und Shot für Shot
     zerlegen. Die Messwerte werden Ziele im Brief (`references/inspiration.md`).
   - 2–5 weitere Referenzen nur als Grammatik. Eigenen Einfall festhalten.
3. **Inspo + Moodboard mit dem Nutzer:** Referenz-Momente als Bildfolgen zeigen, 2–3 Story-Richtungen anbieten.
   Der Nutzer entscheidet an echten Bildern, nicht an Beschreibungen. **Gate.**
4. **3 Style Frames** im Ziel-Werkzeug (`references/style-frames.md`). **Gate: Nutzer gibt frei.**
5. **Storyboard + Animatic** auf dem Beat-Raster (`references/storyboard.md`, `beats.py`). **Gate.**
6. **Bauen**, Einstellung für Einstellung. Die schwerste Einstellung zuerst.
7. **Prüfen:**
   - `motion_check.py render.mp4` mit den Schwellen des Stils (`references/rules.md`),
   - `ref_metrics.py render.mp4 --ref ziel.mp4 --out check/metrics`,
   - Kontaktbogen mit 4 Bildern/s selbst ansehen,
   - dann ein **unabhängiger Critic** (`references/critic.md`), der nur Bilder und Zahlen sieht, keinen Code.
8. **Ton** mit Skill `motion-sound` (Cue-Liste, Mix auf −14 LUFS).
9. **Fertigstellen:** Export (10 Bit + feines Korn gegen Banding), Kontaktbogen, kurzer Bericht.

Änderungen gehen immer zuerst ins Storyboard, dann in den Code.

**Höchstens 2 Critic-Runden nach der ersten Fassung**, dann die beste Fassung abgeben und Schwächen ehrlich nennen.
Endlose Verbesserungsschleifen kosten Stunden und bringen jeweils nur wenige Punkte.

## One-Shot- / Showcase-Modus

Keine Rückfragen, kein Warten auf Freigaben, all-out. Der Zuschauer soll staunen und verstehen, was du für ihn bauen
kannst (`references/formats.md` → Showcase).

1. **Ideen-Runde** (`brief.md`): 5 Story-Ideen in je einem Satz. Streiche die erste, die dir eingefallen ist, und
   jede, deren Held ein Werkzeug des Fachs ist (Keyframe, Zeitleiste, Easing-Kurve, Cursor). Wähle die, die man
   nacherzählen kann.
2. Brief, Stil, Ziel-Referenz (gemessen + zerlegt), eigener Einfall: selbst entscheiden und begründen.
3. **Mindestens zwei Staun-Einstellungen** planen (Technik, Sekunde, Grund), die schwer zu bauen sind. Sie werden
   zuerst gebaut.
4. Style Frames + Storyboard + Animatic für dich selbst.
5. **Critic vor dem Animieren** (Subagent, starkes Modell, frischer Kontext). Erst nach FREIGABE animieren.
6. Bauen, prüfen, Ton.
7. **Critic am Ende** auf dem fertigen Render. Unter der Showcase-Schwelle: die schwächste Stelle zuerst, bei
   niedrigem „Staunen“ die Staun-Einstellungen stärker machen statt Kleinigkeiten zu polieren.

## Werkzeug wählen

| Wenn | Werkzeug |
|---|---|
| UI, Typo, 2,5D-Kamera, SVG, Diagramme | HyperFrames (Skills von HeyGen: `npx hyperframes skills`) |
| echtes 3D (Produkt, Metall, Glas, Tiefenunschärfe) | Skill `motion-3d` (Three.js in HyperFrames, optional Blender) |
| echte Welt, Menschen, Orte | Videomodelle (Kling, Seedance, Veo …), kostet Credits; im Schnitt jede KI-Einstellung mit Code-Kamerafahrt beleben |
| Ton | Skill `motion-sound` |

## Die Sätze, die alles entscheiden

- **Jede Einstellung ist ein Bild, das etwas tut**, kein Satz mit Illustration. Text höchstens ein Wort am Objekt.
- **Jeder Übergang ist ein Objekt** (Display wird UI, Chip wird Seite). Überblenden ist der Notfall.
- **Nichts steht ohne Grund still:** Leseruhe ist eine langsame Fahrt zum nächsten Ziel, kein Einfrieren.
- **Eine laute Sache pro Einstellung.** Wer alles gleichzeitig animiert, animiert nichts.
- **Keine Folien- und Website-Karten** (Titel + Text, Feature-Kacheln, Icon-Raster, Nummern 01/02/03) und **keine
  typischen KI-Endkarten** (Logo + Claim + URL auf leerer Fläche). Das Ende ist ein Bild, das etwas tut, oder ein
  Objekt, das zum Logo wird.
- **Das stärkste Bild gehört in die ersten 2 Sekunden.** Der Film beginnt mitten in der Bewegung, nie mit einer
  Aufblende aus Schwarz.

## Was in Tests am meisten gebracht hat

1. **Eine gemessene Ziel-Referenz pro Film.** Gefühlte Dichte kommt meist aus Kamerafahrten, nicht aus Schnitten.
   Die Messung zeigt das, das Auge allein nicht.
2. **Ein unabhängiger Critic.** Wer gebaut hat, bewertet sich im Schnitt deutlich zu gut und übersieht
   Bildfehler, die ein frischer Blick auf den Kontaktbogen sofort findet.
3. **Eine Ideen-Runde ohne „Werkzeug als Held“.** Filme scheitern öfter an der Story als am Handwerk.
4. **Geschmack als Daten:** Referenzen, die der Nutzer gut findet, und Anti-Referenzen („slop“) schriftlich festhalten.

## Referenzen

`brief.md` · `inspiration.md` · `style-frames.md` · `storyboard.md` · `rules.md` (Zahlen, Prüfschwellen) ·
`critic.md` · `formats.md` · `styles/` (Stilkarten)

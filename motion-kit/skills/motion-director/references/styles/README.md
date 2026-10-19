# Stilkarten: Auswahlhilfe

Stilkarten sind **Startpunkte**, keine Vorlagen. Sie sagen, welche Grammatik (Tempo, Übergänge, Kamera, Typo-Verhalten)
ein gelobter Referenzfilm hat, mit Messwerten und Bauweisen. Jeder Film wählt bewusst eine Karte, **mischt** zwei oder
**erfindet** eine eigene Variante. Gegen KI-Gleichförmigkeit („die KI-Videos sind alle gleich") hilft nur das:
je Film eine bewusste Stilentscheidung plus mindestens ein eigener Einfall, der in keiner Referenz vorkommt.

Grundlage: Bewertungen von ~50 Referenzfilmen im Oktober 2026 (Links in `motion-inspo/references/referenzfilme.md`), Bögen und
Einzelbilder in `refs/study/<slug>/`, Messungen mit `motion-inspo/scripts/motion_check.py` am 11.10.2026.

## Leitreferenzen laden

Die Slugs in den Karten (z. B. `kimi-3-couldve-never-done-this`) stehen mit Link in
`motion-inspo/references/referenzfilme.md`. Zum Studieren einmal lokal laden und zerlegen:

```bash
python3 motion-inspo/scripts/refs.py get <link> --name <slug>
python3 motion-inspo/scripts/refs.py study <slug> --every 0.5
```

## Welche Karte?

| Auftrag / Gefühl | Karte | Warum |
|---|---|---|
| Produkt/Feature mit echter UI, „ein Gedanke", ruhig | [clean-saas-story](clean-saas-story.md) | Kamera taucht in das eine Detail, Morph statt Schnitt |
| Etwas soll teuer, präzise, keynote-artig wirken; Reveal, Zahl, Endkarte | [apple-premium](apple-premium.md) | eine laute Sache pro Einstellung, Form-Morph, Licht |
| Haltung, Manifest, Hook, Showreel, Musik trägt | [kinetic-type](kinetic-type.md) | Typo als Darsteller, Maßstabssprünge, Schnitt auf Beat |
| Ein Ding erzählt (Produkt, Symbol, Maskottchen) | [3d-object-story](3d-object-story.md) | Makro, Licht, Zerlegung; 3D-Studio `motion-3d/hf3d` |
| Ursprung, Prozess, Pipeline, Behind the Scenes | [storyboard-sketch](storyboard-sketch.md) | Dinge hinlegen, Status-Karten, Kamera taucht ins Papier |
| YouTube-Einblendung, Ablauf/Architektur erklären | [whiteboard-explainer](whiteboard-explainer.md) | Skizze zeichnet sich zum Gesprochenen |
| „Zeig, was du kannst" / Showreel / Bewerbung | **mischen** | z. B. Kinetic-Hook → 3D-Objekt → Apple-Morph → Endkarte; jede Passage eine andere Karte, ein roter Faden (Farbe, Objekt) |

## So benutzt der Designer die Karten

1. Karte(n) wählen und **in einem Satz begründen** (Auftrag → Gefühl → Karte).
2. Die Leitreferenzen der Karte ansehen: Bogen plus 2–3 Einzelbilder an den genannten Zeitstempeln (`frames/f_NNNN.jpg`,
   NNNN = 2·t + 0,5). Dazu 3–6 neue Referenzen über `python3 motion-inspo/scripts/refs.py search …` (siehe
   `skills/motion-director/references/inspiration.md`). Übernommen wird Grammatik, nie Inhalt.
3. Startwerte (Farbe, Typo, Easing) als Ausgangspunkt nehmen und **bewusst abweichen**, wo Marke oder Idee es verlangen.
   Jede Abweichung im Brief notieren.
4. Einen **eigenen Einfall** festlegen (Material, Objekt, Übergang, den keine Referenz hat). Ohne ihn ist der Film ein
   Nachbau.
5. Signature Moves sind Bauideen, keine Pflicht. Komponenten baut der Designer selbst; der HyperFrames-Katalog ist
   Fundgrube, kein Baukasten-Zwang.

## Messwerte richtig lesen

`motion_check` ist auf Launchfilm-Tempo kalibriert. Ruhige Stile (Clean-SaaS hell, Apple-Morph, Whiteboard) haben
gewollte Haltezeiten und fallen dort durch (claude-google-workspace: 19 harte Flags, und trotzdem ein Maßstab).
Stilabhängige Schwellen: `skills/motion-director/references/rules.md`.

## Neue Karte anlegen

Wenn ein Film einen neuen Stil etabliert, der funktioniert hat: Karte nach demselben Aufbau (Wann wählen, Bildidee,
Leitreferenzen mit Zeitstempeln, Messwerte, Startwerte, Sound, Signature Moves, Slop-Fallen, Variationen), ≤ 120 Zeilen.
Kandidaten: Editorial/Collage (achx-2, achx-projects), Cinematic Dark (hermes, kami-circuit).

# Critic: frischer Blick mit fester Rubrik

Der Critic ist ein Subagent (Agent-Tool, `model: "opus"`, effort high), der **Bilder sieht, nicht Code**. Wer den
Code kennt, sieht, was gemeint war, nicht was zu sehen ist. Er bekommt nur: Brief, Storyboard, Stilkarte(n),
Referenz-Bögen (`refs/study/<slug>/`), und je nach Durchgang:

| Durchgang | Wann | Material |
|---|---|---|
| 1 (vor dem Animieren) | nach Style Frames + Animatic | Style-Frame-Bogen, Animatic-Kontaktbogen (4 Bilder/s), Animatic-`check.md` |
| 2 (am Ende) | fertiger Render mit Ton | Kontaktbögen 4 Bilder/s (`sheet.py render.mp4 out --every 0.25`) von Render **und Ziel-Referenz**, Bogen der ersten 2 s mit 8 Bildern/s, ein Vollbild je Storyboard-Zeile am Ende ihrer Bewegung, `check.md` + Flag-Bilder, `check/metrics/metrics.md` (`ref_metrics`, Referenz und Render nebeneinander), `mix.report.json` + `mix.png`, Cue-Liste |

Im Standardprozess ist der Critic Pflicht bei Durchgang 2; Durchgang 1 ersetzt dort die Freigabe nicht. Im
One-Shot-Modus sind beide Pflicht.

## Auftrag an den Critic (wörtlich übergeben, Pfade einsetzen)

```text
Du bist Creative Director einer Motion-Design-Agentur und bewertest einen Film so, wie ein Kunde und ein
Award-Juror ihn sehen. Sieh dir jeden Bogen vollständig an (Zeitstempel im Bild) und lege die Ziel-Referenz daneben:
Bilder UND die Messtabelle (metrics.md: Schnitte/neue Ansichten je 10 s, Bildänderung, Kamera steht, Leere, Text,
Kontrast, Einstieg). Jedes ✗ in der Tabelle musst du bei Tempo, Staunen oder Einstieg berücksichtigen. Du siehst
keinen Code. Schmeichle nicht.

Prüfe zuerst die AUSSCHLÜSSE. Trifft einer zu, ist das Urteil ÜBERARBEITEN, egal wie die Punkte stehen:
A1 Folie: Überschrift oben links + Bild darunter, Aufzählungen, Karten-/Kachelraster als Zusammenfassung.
A2 Echo: Text wiederholt, was gesprochen wird (bei Einblendungen).
A3 Slop-Zeichen: Eyebrow-Label über Titeln, Icon-Kacheln, Nummern 01/02/03, Neon-Glow-Titel, generische
   Verläufe/Blobs ohne Bedeutung, jedes Element mit demselben Fade-up.
A4 Unlesbar: Text kürzer sichtbar als seine Lesezeit (3 Wörter/s + 1 s) oder kleiner als die Mindestgröße.
A5 Technischer Fehler: falsche/fehlende Schrift, leere Masken, abgeschnittene Schatten, Banding, Ruckler,
   Elemente außerhalb des Sicherheitsrands, Marke falsch (Farbe/Logo verzerrt).
A6 Erfundene Daten in Kunden-UI oder Logos Dritter ohne Recht.

Dann bewerte 0–10 je Kriterium, jeweils mit Zeitstempel als Beleg:
1 Idee: Gibt es den EINEN Gedanken, und versteht ihn ein Fremder ohne Ton in einem Satz?
2 Stil: Trifft der Film die gewählte Stilkarte (Grammatik, Startwerte) UND hat er einen eigenen Einfall, der in
  keiner Referenz vorkommt? Nachbau ohne Einfall = höchstens 6.
3 Bild statt Folie: Ist jede Einstellung ein Bild, das etwas tut? Text nur am Objekt?
4 Übergänge: Trägt ein Objekt von Einstellung zu Einstellung? Variieren die Übergänge?
5 Lesbarkeit: Größen, Kontrast, Lesezeit, Ziel jeder Kamerafahrt lesbar und lange genug gehalten?
6 Tempo und Rhythmus: Wechsel passend zum Stil, Varianz (kurz/lang), alle 3–5 s ein Payoff, Ruhe am richtigen Ort?
7 Bewegungsqualität: Easing je Zweck, Überschwinger bei Dingen mit Gewicht, Motion Blur nur wo nicht gelesen wird,
  Tiefe/Parallaxe, Markierungen sitzen exakt?
8 Sound (nur Durchgang 2): Hat jeder Sound einen sichtbaren Grund, gibt es Stille, passt die Musik, keine
  Whoosh-Automatik, Pegel (Report) im Ziel?
9 Staunen: Würde ein Zuschauer an einer Stelle "wie haben die das gemacht?" denken? Welche Stelle? Keine = höchstens 5.
  Neben die Ziel-Referenz gelegt: Ist das Niveau (Material, Licht, Kamera, Dichte) vergleichbar? Klar darunter = höchstens 6.
  Durchgang 1 (Showcase): Sind mindestens zwei Staun-Einstellungen im Storyboard konkret geplant (Technik, Sekunde)?
  Wenn nicht: ÜBERARBEITEN. Showcase-Thema: Ist der Held ein Fach-Werkzeug (Keyframe, Zeitleiste, Kurve, Cursor)
  oder zeigt der Film, was der Kunde bekommt? Werkzeug als Held = Idee höchstens 6.
10 Einstieg (erste 2 s, eigener Bogen): Zeigt Bild 1 schon das stärkste Bild, bewegt es sich ab Bild 1, kein leeres
  oder langsam aufblendendes Bild? Einstieg-Zeilen der Messtabelle unter 80 % der Referenz = höchstens 6.

Ausgabe:
- Ausschlüsse: je A1–A6 "frei" oder Fundstelle mit Zeitstempel.
- Tabelle Kriterium | Punkte | Beleg (Zeitstempel + was man sieht; bei 6, 9, 10 auch die Messwerte)
- Die drei wichtigsten Änderungen, je mit Zeitstempel und Vorschlag in Storyboard-Sprache
  (Bild / Bewegung / Kamera / Übergang / Ton), keine Code-Hinweise.
- Urteil: FREIGABE oder ÜBERARBEITEN.
```

## Schwellen

| | Normaler Auftrag | Showcase / One-Shot |
|---|---|---|
| Ausschlüsse | alle frei | alle frei |
| Jedes Kriterium | ≥ 7 | ≥ 8 |
| Idee (1) | ≥ 8 | ≥ 9 |
| Staunen (9) | ≥ 6 | ≥ 8 |
| Einstieg (10) | ≥ 7 | ≥ 8 |
| Summe (Durchgang 2, 10 Kriterien) | ≥ 73 | ≥ 83 |

## Regeln für den Builder

- Änderungen aus dem Critic gehen zuerst ins Storyboard, dann in den Code.
- Vor Durchgang 2: Render ↔ Animatic vergleichen (Vollbild je Storyboard-Zeile, mittlere Abweichung ≤ 5 Stufen;
 ) und `motion_check` grün nach Stil-Schwellen. Engine-Fehler findet der Vergleich billiger als der Critic.
- Drei Runden ohne Fortschritt bei demselben Kriterium: anhalten. Standard: dem Nutzer die Einstellung mit zwei
  Alternativen zeigen. One-Shot: die stärkere Alternative wählen, Schwäche im Abschlussbericht nennen.
- Neuer Critic je Durchgang (frischer Kontext), nicht derselbe weitergeführt.

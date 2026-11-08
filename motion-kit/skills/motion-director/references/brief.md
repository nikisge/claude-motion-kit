# Director's Brief (vor allem anderen, ≤ 1 Seite, `projects/<name>/brief.md`)

Ein Brief, der nicht auf eine Seite passt, hat mehr als einen Gedanken. Im One-Shot-Modus füllst du ihn selbst aus
und begründest jede Entscheidung in einem Halbsatz.

```markdown
# Brief: <Projekt>

- **Auftragstyp + Weg:** Launchfilm | Erklär-Animation | YouTube-Einblendung | Social vertikal | Showreel |
  Showcase · Standardprozess | One-Shot | schlank
- **Ideen-Runde (nur One-Shot/Showcase):** 5 Story-Ideen je 1 Satz; gestrichen: die erste, alle mit Fach-Werkzeug
  als Held; gewählt + warum.
- **Das Versprechen (1 Satz):** „Danach weiß/fühlt der Zuschauer: …“. Nicht was das Produkt ist.
- **Story (bei erzählten Formaten):** steht vor dem Storyboard fest und wird vom Nutzer gewählt, nicht vom Agenten
  erfunden. Der Agent hat Freiheit bei Shots und Umsetzung, nicht bei Story und Inspo.
- **Der eine Gedanke (Bild):** das Bild, an das man sich morgen erinnert (z. B. „der Fehlercode fliegt in die Frage").
- **Zielgefühl (3 Wörter):** z. B. ruhig, präzise, warm.
- **Publikum + Plattform:** wer, wo (X, YouTube neben Kamera, Reels), stumm oder mit Ton?
- **Format:** 16:9 / 9:16 / 1:1 · Länge s · fps · Ausgabe (MP4 10 Bit, MOV mit Alpha …). fps: **30** Standard
  (YouTube), 60 bei sehr schneller UI/Kamera, 24 nur bei bewusst filmischem Stil mit Begründung.
- **Stil:** Stilkarte(n) aus `motion-director/references/styles/` + Begründung (Auftrag → Gefühl → Karte). Bewusste Abweichungen.
- **Referenzen (3–6):** slug/URL + Zeitstempel + welche Grammatik wir nehmen (siehe `inspiration.md`).
- **Eigener Einfall:** was es in keiner Referenz gibt (Material, Objekt, Übergang, Perspektive).
- **Marke:** Farben (Hex, aus der Datei gemessen, nicht nur aus der Spezifikation), Schriften, Logo-Datei,
  echte Screenshots/Frontend. Abweichung Datei ↔ Spezifikation notieren.
- **Text auf dem Bild:** welche einzelnen Wörter/Zahlen erlaubt sind; Lesezeit (rules.md).
- **Ton-Rolle:** Musik führt / trägt / keine; 3–4 Sound-Familien; wo Stille ist (Skill `motion-sound`).
- **Ziel-Referenz:** ein Film, dessen Grammatik und Niveau wir treffen wollen, + seine `ref_metrics`-Zahlen (`inspiration.md`).
- **Werkzeug:** HyperFrames (3D über Skill `motion-3d`) / + Higgsfield für das, was Code nicht kann (Skill
  `motion-higgsfield`: Kosten, Freigabe je Generierung).
- **Gates:** Storyboard-Review-Seite (Richtungen, Style Frames, Kosten) → Animatic → Ton → Abnahme (Standard); im
  One-Shot optional Critic 1 + Critic 2.
- **Kosten (falls Higgsfield):** Deckel in Credits, Preis je geplanter Generierung vorab (Skill `motion-higgsfield`).
- **Nicht tun:** was ausdrücklich nicht vorkommen soll (aus Feedback, Marke, Auftrag).
```

## Prüffragen vor dem Weitergehen

- Kann ich den Film in einem Satz erzählen, der mit einem Verb beginnt? Wenn nein: zu viele Gedanken.
- Würde der erste Frame stumm funktionieren (X, Reels spielen ohne Ton)?
- Ist der eigene Einfall wirklich eigen, oder steht er in einer Stilkarte unter „Signature Moves"?
- Bei Kundenmaterial: sind alle Texte/Daten echt (nie erfunden), und darf ich die Logos verwenden?

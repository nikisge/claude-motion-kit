# Änderungen

## 0.2.0 (08.11.2026)

Der Ablauf hat jetzt drei Schritte: Inspo, Werkzeugkasten, Feinschliff. Dazu kommen Higgsfield als zweiter Baustein
und vier neue Stile.

### Neu

- Skill `motion-higgsfield`: MCP einrichten, welches Werkzeug wofür (Genjutsu, Seedance, Kling, Bild → 3D, Bilder,
  Ton), Kosten vor jedem Job rechnen, Freigabekarte, Nähte zwischen Modell-Clips und Code. Ungetestete Ideen sind
  markiert.
- Stilkarte **Doku mit Archivmaterial**: wahre Geschichte mit Erzählerstimme, Karte und gemeinfreies Archiv als Rückgrat.
- Stilkarte **Gestaltete Welt**: echte Aufnahme kippt in eine Welt aus einem Material (Videomodell + Code).
- Stilkarte **3D-Welt**: Geschichte ohne Worte in einer Miniaturwelt, Licht als Höhepunkt, Path Tracing.
- Stilkarte **Papierschnitt-Erklärer**: Reise durch verschachtelte Maßstäbe mit Sprecher.
- Neue Referenzfilme in `referenzfilme.md` (nur Links mit Zeitstempeln).
- `CHANGELOG.md`.

### Geändert

- `motion-director`: Ablauf in drei Schritten plus „Learnings speichern“. Die Storyboard-Review-Seite ist das
  wichtigste Tor vor dem Bauen (Richtungen, Spannungskurve, Shotliste, Standbilder, Faktencheck, Kosten, Risiken).
  Ein Film = ein Stil, ein roter Faden. Die Stimme bestimmt die Bildzeiten.
- Critic-Subagent ist jetzt optional statt Pflicht.
- `motion-hyperframes`: auf HyperFrames 0.9.23 (getestet war 0.9.17, die Befehle sind gleich), neue Prüfbefehle
  (`snapshot --review/--against`, `measure`, `audio`), generierte Clips mit Code kombinieren, Bewegungsunschärfe über
  hohe fps und Mitteln.
- `motion-sound`: Earshot als externe Prüfung im Feinschliff, Abschnitt zu Sprecher-KI, Treffer gegen die Stimme
  messen, echte Aufnahmen (Openverse) vor KI-Sounds, Stimmspur nie dehnen.
- `motion-3d`: neuer Weg „Modelle aus Bildern + Path Tracing“ mit gemessenen Renderzeiten.
- README nach den drei Schritten, Stiltabelle mit 10 Karten, Installation mit optionalem Higgsfield-MCP und Earshot.
- `RESOURCES.md`: Sterne und Links vom 08.11.2026, neue Abschnitte Higgsfield und Nachbar-Kits.

### Entfernt

- Eine SFX-Quelle aus Quellenliste und Lizenztabelle (7 Einträge).
- Interne Pfade und Bezüge aus Beispielen.
- „Critic ist der größte Hebel“: der größte Hebel ist das Storyboard, das du vor dem Bauen abnimmst.

## 0.1.0 (19.10.2026)

Erste öffentliche Version: 5 Skills, 6 Stilkarten, Prüfwerkzeuge, Sound-Bibliothek, 3D-Studio.

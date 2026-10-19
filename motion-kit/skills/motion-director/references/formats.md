# Formate: was je Auftragstyp anders ist

Gemeinsam für alle: Brief, Stil, Storyboard-Vertrag, Prüfregeln, Critic (siehe SKILL.md). Hier nur das Spezifische.

## Launchfilm (X, 30–45 s, 16:9)

| Akt | Anteil | Was passiert | Nicht |
|---|---|---|---|
| 1 Haken | 0–3 s | Problem oder Versprechen sofort im Bild, erstes Frame funktioniert stumm | Logo zuerst, Fade aus Schwarz |
| 2 Ein Fall | ~30 % | **ein** Anwendungsfall komplett, echte UI im Tempo, Kamera taucht ins Detail | Feature-Tour |
| 3 Mechanik/Beweis | ~25 % | eine lange Fahrt (Herzstück) zeigt *warum*, oder ein zweiter Fall beweist „kein Einzelfall" | Erklärfolien |
| 4 Ergebnis | ~20 % | Nutzen als Ergebnis-Bilder, 2–3 s je Schnitt, höchstens ein Wort | Vorteilsliste, Raster |
| 5 Auflösung | letzte 3 s | ein Objekt aus dem Film wird zum Logo, Claim | Logo-Intro ohne Bezug |

UI ist echt (Frontend per Playwright @2x oder Kunden-Screenshots), Daten nie erfunden. Ton: Musik führt
(115–128 BPM), Schlüsselereignisse auf Downbeats. Export: Master (MOV/10 Bit) + MP4 1080p; 1:1 und 9:16 werden
**neu komponiert**, nicht beschnitten.

## Erklär-Animation (30–120 s, 16:9, oft mit Sprecher)

- Pro Aussage ein Bild, das sie zeigt (Satz → Bild, `storyboard.md`); Metapher konkret (Kurzgesagt-Logik:
  abstrakter Begriff → ein Ding; Maßstab durch Rückfahrt; Menge durch Zählen).
- Timing nach Sprechtext (Wortzeiten), nicht nach Musik; Musik trägt leise.
- Ein Kapitel = ein Bildraum; Kapitelwechsel durch ein Objekt (Iris aus einem Bildteil, Kamera fährt in ein Ding).
- Text: Etiketten am Objekt, 1–3 Wörter; das Endbild jedes Kapitels ist als Standbild verständlich.
- Stilkarten: `whiteboard-explainer`, `storyboard-sketch`, `3d-object-story`.

## YouTube-Einblendung / Whiteboard-Grafik (neben der Kamera)

| | Typo-Insert | Erklär-Insert |
|---|---|---|
| Wofür | die **eine** Kernaussage oder Zahl eines Abschnitts | Abläufe, Vergleiche, Mengen, „wie funktioniert das" |
| Bild | große Typo, Wort für Wort zur Sprache, Marker-Strich | ein Vorgang, der das Gesagte zeigt; Whiteboard-Stil (Excalidraw-artig) |
| Text | Schlüsselwörter, ≤ 3 Zeilen | ≤ 3 Wörter je Etikett, nie den gesprochenen Satz |
| Häufigkeit | ≤ 1 pro ~60 s | Normalfall |
| Messung | `motion_check` ohne `--script` | `motion_check --script abschnitt.txt` (Echo = hart) |

1. Wortzeiten aus einem Transkript mit Zeitstempeln je Wort (z. B. Whisper mit `word_timestamps`, ElevenLabs Scribe).
2. Jede Wirkung ~80 ms vor dem Wort. Ein Element pro Satzteil.
3. Feste Fläche neben der Kamera (z. B. linke Bildhälfte) oder Vollbild für kurze Momente; Hintergrund transparent
   (MOV/WebM mit Alpha) oder Papier.
4. „Warum eine Grafik hier?" muss beantwortbar sein; oft ist ein Zoom auf den Bildschirm besser.
5. Ton: meist keine Musik (das Video hat eigene), 0–2 leise Akzente, Stimme duckt alles (`motion-sound`).

## Social vertikal (Shorts, Reels, TikTok; 1080 × 1920)

- Hook in 1–1,5 s: Ergebnis oder Konflikt zuerst, Bewegung ab Frame 1, kein Logo.
- Schutzzonen: oben ~220 px, unten ~420 px, rechts ~140 px (vor Export im Overlay der Ziel-App prüfen).
- Untertitel Pflicht (stumm), 2–4 Wörter je Block, oberes Drittel bis Mitte, Wort-Highlight.
- Eine Idee pro 2–3 s, Tempo ≥ 5 Wechsel/10 s, harte Schnitte auf Wortgrenzen.
- Neu komponieren, nicht croppen; Hauptobjekt größer. Loop-Ende: letztes Bild führt ins erste.

## Showreel / Bewerbungsfilm (30–90 s)

- Zeigt **Bandbreite mit rotem Faden**: jede Passage eine andere Stilkarte (z. B. Kinetic-Hook → 3D-Objekt →
  Clean-SaaS-Fahrt → Apple-Endkarte), verbunden durch ein Objekt oder eine Farbe, das durch alle Passagen wandert.
- Bewirbt sich jemand mit dem Film: der stärkste Moment in die ersten 5 s, Name/Kontakt als Endkarte.
- Nur eigene Arbeit bzw. Arbeit mit Recht zur Nutzung; Kundenlogos nur mit Freigabe.
- Ton: Musik führt, Schnitte auf Takt, Stilwechsel auf Taktanfängen; Sound-Design als eigene Passage.

## Showcase / One-Shot („zeig, was du kannst")

- **Zeigen statt erklären.** Thema ist, was der Zuschauer (Kunde, Startup) von dir bekommt, nicht wie dein Fach
  funktioniert. Verboten als Held oder Bildsprache: Keyframes, Zeitleisten, Kurven-Editor, Easing-Kurven, Cursor,
  Ebenen-Paletten, Render-Balken. Das ist die erste Idee jedes Modells und erzählt nichts.
- **Story als Klammer, Stile als Beweise.** Bewährte Form: jeder Stil ist ein Stück aus einem echten Launch- oder
  Erklärfilm für ein erfundenes Produkt (z. B. Kapitel 1 Produkt-Reveal in 3D, Kapitel 2 Erklärung im Storyboard-Stil,
  Kapitel 3 kinetische Typo zum Claim). Die Klammer sagt in einem Satz, was der Kunde bekommt
  („Euer Launch, in jedem Stil, den ihr braucht"). Ein Gedanke trägt (Idee-Kriterium ≥ 9), kein Effekt-Katalog.
- **Mindestens zwei Staun-Einstellungen**, die man nicht in einer Stunde nachbaut, z. B.: ein 3D-Objekt, das sich
  verwandelt und die Geschichte trägt (Kimi-3-Niveau); eine durchgehende Kamerafahrt durch eine Welt, in der die Stile
  Räume sind; ein Morph (Partikel, Flüssigkeit, Papier faltet sich zu Objekt); ein Übergang, bei dem ein Objekt aus
  einem Stil der Rahmen des nächsten wird; Licht/Material, das echt wirkt (Glas, Metall, Tiefenunschärfe).
- Dazu: mindestens drei klar verschiedene Stilkarten, eigenes Sound-Design mit Stille vor dem Höhepunkt, Endkarte
  mit Haltung.
- **Einstieg zeigt sofort das stärkste Bild**: Bild 1 ist schon Material, Licht und Bewegung (kein Aufbau, kein
  Logo, kein leeres Papier, kein Aufblenden). Die ersten 2 s bewegen sich mindestens so viel wie die Ziel-Referenz.
- **Objekt-Übergänge sind echte Verwandlungen**: Form A wird sichtbar zu Form B (Teile setzen sich neu zusammen,
  Fläche faltet sich, Objekt wird Rahmen des Nächsten). Zerfallen in Partikel, Einblenden, Überblenden oder
  „Würfel wird viele Würfel“ zählen nicht.
- **Text höchstens kurz**: kein Satz auf leerem Grund, Wörter nur am Objekt; Endkarte ≤ 3 s. Leere Bilder > 0,3 s
  nur als geplante Stille.
- **Dichte wie die Ziel-Referenz**: Einstellungen, Makros und Kamerafahrten nach `ref_metrics` der Ziel-Referenz
  (Produkt-3D: Kimi-3, ~5 neue Ansichten je 10 s, Kamera steht < 30 %), 3D über Skill `motion-3d`.
- Ablauf im One-Shot-Modus (SKILL.md): Ideen-Runde, Critic vor dem Animieren und am Ende, Schwellen „Showcase" in
  `critic.md`.

## Export (alle)

- Master: MOV (verlustfreie Bilder) → 10 Bit H.264/HEVC + feines Korn gegen Banding (Befehle in
  `motion-hyperframes`). Prüfen: `ffprobe` Dauer/fps = Brief.
- Lieferung: MP4 1080p hohe Bitrate je Format; Ton −14 LUFS, ≤ −1 dBTP (`motion-sound`).
- Abgabe-Ordner: `renders/` (gitignored), `check/` (motion_check, Kontaktbögen, Critic-Berichte), `brief.md`,
  `storyboard.md`, `cues.json`.

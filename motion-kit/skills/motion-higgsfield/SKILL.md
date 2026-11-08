---
name: motion-higgsfield
description: "Use when a motion piece needs material that code cannot make: real footage redrawn in a new look (Higgsfield Genjutsu), designed worlds or figures from video models (Seedance, Kling), images as building blocks or start/end frames, image to 3D model (GLB) for Three.js, upscaling, music or foley; when setting up the Higgsfield MCP in Claude Code; or before any Higgsfield generation that costs credits. Trigger words: Higgsfield, MCP, Genjutsu, Seedance, Kling, KI-Video, generierter Shot, Bild zu 3D, GLB, Upscale, Credits."
---

# motion-higgsfield: was Code nicht kann, mit Preis vorher

**Rolle:** Higgsfield liefert Material, der Code liefert die exakte Grafik. Nie umgekehrt: UI, Text, Zahlen und Logos
erzeugt kein Videomodell (falsche Buchstaben, erfundene Oberflächen). Gebaut und geschnitten wird in HyperFrames
(`motion-hyperframes`), der Ablauf kommt aus `motion-director`.

**Die wichtigste Regel:** Videomodelle für **gestaltete Welten**, nicht für Wirklichkeit. Wolle, Filz, Tusche,
Spielzeug, Papier, Miniatur: gut. Fotorealistische KI-Szenen und KI-„Archivfotos“ wurden in unseren Tests abgelehnt.
Echte Archivquellen (gemeinfreie Karten, Fotos, Dokumente, z. B. Wikimedia Commons) schlagen KI-Fotos.

## MCP in Claude Code einrichten

```bash
claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp
```

Dann in Claude Code `/mcp` öffnen, `higgsfield` wählen, **Authenticate**. Es öffnet sich ein Browser-Login mit deinem
Higgsfield-Konto, kein API-Key. Danach kennt Claude die Higgsfield-Werkzeuge (Bild, Video, 3D, Audio, Upscale,
Presets wie Genjutsu, Preisabfrage). Prüfen: Frag Claude „Welche Higgsfield-Werkzeuge hast du, und was kostet ein
5-s-Seedance-Entwurf in 480p?“. Die Antwort kommt aus einer Preisabfrage und kostet nichts.

- **MCP-Generierungen kosten Credits.** Der MCP braucht einen bezahlten Tarif. „Unbegrenzt“ und Gratis-Generierungen
  gelten laut Higgsfield nur auf higgsfield.ai, nicht über MCP oder CLI.
- Tarife (Stand 05.11.2026, higgsfield.ai/pricing, DE, zzgl. MwSt., ändern sich): Starter 19 €/Monat mit 270 Credits
  und nur ausgewählten Modellen; Plus 59 €/Monat (47 € jährlich) mit 1.200 Credits und allen Modellen, vom Tarif-Finder
  für „MCP, CLI“ empfohlen.
- Alternative ohne MCP: offizielle CLI `npm i -g @higgsfield/cli`, `higgsfield auth login`, Skills mit
  `npx skills add higgsfield-ai/skills` ([higgsfield-ai/cli](https://github.com/higgsfield-ai/cli)).

## Vor jeder Generierung

1. **Preis abfragen**, bevor etwas gebucht wird (die Werkzeuge haben eine Preisabfrage, z. B. `get_cost`; Genjutsu
   über die Preset-Liste). Erst die gültigen Parameter des Modells lesen.
2. **Freigabekarte** schreiben (`references/freigabekarte.md`): Zweck, Modell, Parameter, Prompt, Referenzen, Preis.
   Der Mensch gibt genau diese Karte frei. Allgemeines Gefallen ist keine Freigabe.
3. **Keine automatischen Wiederholungen**, keine Ketten. Kommt der Status nur langsam, nicht neu abschicken, sondern
   den Job abfragen. Ein fehlgeschlagener Job (z. B. HTTP 502) wurde bei uns nicht abgebucht; im Zweifel den
   Credit-Stand prüfen, bevor du es noch einmal versuchst.
4. **Ledger führen** (`projects/<name>/ledger.md`): Job-ID, Preis, tatsächliche Credits, Ergebnis angenommen oder
   verworfen. Einen Deckel je Film festlegen und einhalten.
5. **Entwurf zuerst:** niedrige Auflösung testen, Kontaktbogen mit 4 Bildern/s über die volle Laufzeit, erst dann Final.

## Wann welches Werkzeug

| Aufgabe | Werkzeug (Namen Stand 11/2026, `/mcp` zeigt die aktuelle Liste) | Danach im Code |
|---|---|---|
| echtes Video in einen neuen Look (Wolle, Knete, Spielzeug, Anime), Bewegung bleibt echt | **Genjutsu** (Video-zu-Video) | Code-Maske als Übergang echt → Look, Code-Objekte darüber |
| gestaltete Welt, Figur, Flug, Reise | **Seedance 2.5** (`omni_reference` mit Start-/Endbild und Figurenreferenz, `video_extension`) | Schnitt auf Beat, Typo am Objekt, Zeitrampen |
| kurzer Welt-Shot 2–5 s mit Startbild | **Kling 3.0** | wie oben |
| Übergang Objekt → Grafik | Videomodell mit Start- **und** Endbild, Endbild = leeres Display | HyperFrames setzt die echte UI ins Display |
| Style Frame, Start-/Endbild, Requisite, Textur | Bildmodelle (Nano Banana Pro / 2.1, GPT Image) | Ausschnitt freistellen, als Ebene in der Code-Welt |
| Objekt als 3D-Modell | **Bild → 3D**: Bild der Requisite, dann `sam_3_3d` (texturiertes GLB) | GLB in Three.js laden (`motion-3d`) |
| Entwurf auf 1080p | Video-Upscale (`bytedance_video_upscale`, Modus standard) | – |
| Person/Objekt als Ebene, Tiefe | Hintergrund entfernen (`sam_3_video`), Tiefenkarte (`depth_anything_video`) | Grafik läuft hinter der Figur, Parallaxe |
| Musik auf Filmlänge, laute Einzelgeräusche | ElevenLabs Music, Text-zu-Audio | Mix in `motion-sound` |

### Genjutsu (Video-zu-Video)

- **Was es macht:** Dein Video gibt Bewegung, Kamera, Bildaufbau und Timing vor. Das Modell zeichnet jedes Bild in
  einem neuen Look neu. Wie Motion Capture für ganze Videos: die Bewegung kommt von dir, das Kostüm vom Modell.
  Darum wirkt es weniger „KI-zappelig“ als ein Prompt-Video.
- **Modi:** Motion Transfer / Styles (alles neu zeichnen, Bewegung bleibt), Object Swap (ein Element tauschen).
  Eingabe laut Higgsfield 3–30 s (im MCP stand 4–30 s), Ausgabe bis 1080p.
- **Eigener Prompt und eigene Farbwelt sind Pflicht.** Mit Standardwerten sieht es aus wie Higgsfields eigene Vorschau.
  Unser Prompt sagte, was bleiben muss („keep the red yarn string bright red, matte natural wool, no plastic shine,
  no logos“).
- **Ohne Referenzbild war besser:** Ein Referenzbild übernahm Pose und Bildaufbau, die Hand folgte der Aufnahme nicht
  mehr. Ohne Referenz, mit dem Prompt „Bildaufbau und Bewegung halten“, folgte alles dem Original.
- Ein Code-Objekt, das **vor** Genjutsu ins Video gerechnet wird (z. B. ein Faden am Handgelenk), überlebt die
  Verwandlung und wird Teil des neuen Looks. So entsteht ein roter Faden durch alle Werkzeuge.
- Ausgabe bei uns mit **12 fps**: Die Verwandlung stottert gegen 30-fps-Material. Kurz halten oder mit einer
  Code-Maske überdecken.

### Seedance und Kling

- **Seedance-Entwurf** mit `draft:true` kostet den 480p-Preis. Ist er gut: mit `draft_job_id` denselben Take in
  1080p neu rechnen, **oder** den Entwurf für 1 Credit hochskalieren (am echten Frame sichtbar besser als lokales
  Lanczos + Schärfen). Ein 720p-Final ohne `draft_job_id` ist ein neuer Wurf, nicht derselbe Take.
- Videomodelle liefern meist 24 fps. Für 30-fps-Filme: Zwischenbilder helfen in langsamen Teilen und schmieren in
  schnellen. Die brauchbaren Sekunden je Clip notieren und chirurgisch schneiden.
- **Kontinuität:** eine Figur, ein Ort. Alle Takes mit derselben Figurenreferenz, trotzdem wechselt die Figur leicht
  (Haube, Schnabel, Proportion). Startbilder mit bis zu 4 Referenzen (Figur, Drehansicht, Ort) halten sie stabiler.
  Verworfenes nie als Referenz weitergeben.
- **Typische Mängel**, die nur der Kontaktbogen findet: Fäden und Stäbe hängen senkrecht wie Stützen, Pseudo-Schrift
  auf Bildschirmen und im Himmel, Logo-Glanzpunkte, Objekte gleiten statt zu springen, Sprünge bei schnellen
  Bewegungen, Gesichter in Wolken und Mustern.
- In jeden Prompt: „flies freely, no stick, no rod, no string“ (wo es passt), „No text, no letters“, Ton aus
  (`generate_audio:false`, den Ton bauen wir selbst). Maßstab ausdrücklich nennen („reaches only the figure's waist“).

### Bild → 3D-Modell

- Bild der Requisite einzeln auf neutralem Grund im Zielstil malen lassen (z. B. „matte toy diorama“), dann
  `sam_3_3d`: texturiertes GLB für 1 Credit. Großer Sprung gegenüber Code-Grundformen.
- Bei Mehrteilern hebt SAM oft nur einen Teil (eine Mühle: nur das Flügelkreuz). Teile einzeln heben und im Code
  zusammensetzen; drehende Teile so sogar getrennt animierbar.
- Gruppen („drei Bäume“) ausdrücklich als Gruppe prompten, sonst kommt ein einzelner flacher Busch.
- Alternative: Meshy `image_to_3d` (20 ohne, 30 mit Textur), für einfache Requisiten unnötig teuer.

### Bilder als Bausteine für Code-Welten

- Holzstich- oder Papier-Requisiten auf einer Tafel generieren, lokal freistellen, mit Papierrand und Schatten als
  Pop-up-Ebenen in einer Code-Welt aufstellen. Wirkt wie Handwerk, nicht wie KI-Bild.
- Papier- und Materialplatten (Faser, Korn) als kachelbare Textur für SVG-Filter. Zwei Platten reichen meist.

### Audio

- Text-zu-Audio liefert gute **laute, konkrete Einzelereignisse** (Wumms, Klick, Flügelschlag, Atem). Prompt im
  Stil „LOUD close-up recording of …, clearly audible, full volume, no music“.
- Zarte, tonale oder stehende Geräusche (Federkratzen, Glas-Tick, Summen, Stichgeräusch) ergeben meist Rauschen oder
  Stille. Dafür echte Aufnahmen (`motion-sound`, Openverse). Jedes Ergebnis per Spektrogramm prüfen.
- Musik-Generierung hält die Dauer nicht immer ein und liefert manchmal nur eine statt zwei Varianten. Generierte
  Musik klingt schnell generisch („inspirational corporate“); für einen fertigen Film lohnt ein ausgewählter Track.

## Kosten vorher rechnen (Beispielpreise, Stand 06.11.2026, ändern sich)

Gemessen per Preisabfrage im Plus-Tarif. Vor jedem Auftrag neu abfragen.

| Was | Credits |
|---|---|
| Seedance 2.5, 5 s, 480p / 720p / 1080p | 15 / 35 / 80 |
| Seedance 2.5, 10 s, 480p / 720p / 1080p | 30 / 70 / 160 |
| Seedance-Entwurf (`draft:true`), 7 s → derselbe Take in 1080p | 21 → 112 |
| Video-Upscale 480p → 1080p, Modus standard | 1 |
| Kling 3.0, 5 s | ca. 10 (abgebucht wurden bei uns 8,75) |
| Genjutsu-Stil, 5-s-Video, 480p / 720p / 1080p | 16,5 / 36,5 / 56,5 |
| Genjutsu-Stil, 4-s-Video, 480p / 720p | 13,5–16,5 / 29,5 |
| Bild, Nano Banana Pro 2k / Nano Banana 2.1 1k | 2 / 1,5 |
| Bild → 3D, `sam_3_3d` / Meshy mit Textur | 1 / 30 |
| Text-zu-Audio, 2 s / 3 s | 0,5 / 0,75 |
| Musik (ElevenLabs Music, 2 Varianten bestellt), ca. 20 s / ca. 36 s | ca. 6 / ca. 10,5 |

Ton im Seedance-Job und der Entwurfsmodus kosten nichts extra. Hochladen eigener Medien kostet nichts.

**Richtwerte aus echten Filmen (15–20 s):** Ein Film mit Genjutsu und drei Seedance-Takes lag bei rund 260 Credits,
davon rund 30 für verworfene Tests. Ein Film, der fast nur aus Code und Archiv besteht, lag bei 4–20 Credits (ein paar
Bilder, Musik, Foley). Eine 3D-Welt mit zehn Requisiten aus Bild → 3D: rund 20 Credits. Plane eine Reserve von etwa
25 % für einen zweiten Versuch am riskantesten Shot.

## Kombination mit Code (die Nähte)

Der Wow entsteht an den Nähten, wo der Zuschauer nicht mehr sagt, was gefilmt, generiert oder gebaut ist:
- **Code-Maske über echtem Video:** Das echte Bild verwandelt sich Reihe für Reihe in den Genjutsu-Look (Wipe mit
  Material-Kante und Schatten), auf derselben Quellzeit, framegenau.
- **Code-Objekt als roter Faden:** vor der Generierung ins Video gerechnet, danach im Code weitergeführt (Faden wird
  Schrift, Linie wird Route).
- **Rahmen wird Fenster:** Ein Bilderrahmen oder Display im Clip wird per Maske ausgestanzt, dahinter läuft schon der
  nächste Clip. Die Kamera fliegt hindurch.
- **Harter Schnitt im Bewegungs-Blur** statt Überblendung. Überblendungen zwischen zwei Modell-Clips zeigen fast
  immer eine Doppelbelichtung.
- **Zeitrampe in die Stille:** Modell-Clip in Zeitlupe (100 → 20 %), Ton weg, dann der Treffer.
- **Code-Titel im Material der Welt** (gestickt, gemalt, gedruckt) statt Banner über dem Bild. Er muss in der Welt
  verankert sein, sonst hängt er über allem.
- **Blend Modell-Clip ↔ Code:** Endbild des Modell-Clips = Startbild der Code-Szene (z. B. leeres Display, in das die
  echte UI kommt).

## Noch ungetestet (als Idee markiert)

- **Code-Animatic → Genjutsu:** grobe Bewegung, Kamera und Layout aus HyperFrames, das Material kommt vom Modell.
  Schrift im Bild wird dabei vermutlich verwaschen, also danach per Code darüberlegen. Erst ein Testclip in 480p.
- **Billiges Motion Capture:** sich mit dem Handy filmen, per Genjutsu als Figur in die Welt des Films setzen.
- **Object Swap für Produkte:** Gegenstand in einer echten Aufnahme durch das eigene Produkt ersetzen.
- **Katana** (Higgsfield-Workflow für Claude, baut ein Referenzvideo mit eigenen Figuren nach): nicht im Kit-Prozess
  getestet. Achtung, das ist das Gegenteil von „Grammatik statt Nachbau“.

## Prompts

Ein Bild → eine Handlung → eine Kamerabewegung. Kamera-Sprache statt Adjektive („langsamer Push-in, 35 mm, über die
linke Schulter“). Was das Startbild schon zeigt, nicht noch einmal beschreiben. Prompts für die Modelle auf Englisch,
Bildtext mit Umlauten ausdrücklich („STÖRUNG“ mit Ö), keine erfundenen Marken oder Fehlercodes.

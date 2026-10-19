# Sound-Handwerk: Schichten, Timing, Musik schneiden

## Schichten („layered cake")

Ein wichtiger Moment ist selten ein Sample. Bis zu drei Schichten, jede mit eigener Aufgabe:

| Schicht | Aufgabe | Beispiel | Pegel (vor Master) |
|---|---|---|---|
| Transient | der Anschlag, sagt *wann* | Klick, Tick, Pop, Kartenkante | −8 … −12 dB |
| Körper | das Gewicht, sagt *wie groß* | tiefer Puls, Holz-Hit, Papier-Klatsch | −12 … −16 dB, LPF 2–4 kHz |
| Textur | der Raum/Charakter, sagt *woraus* | Swish-Luft, Glitzer, Papierrascheln | −16 … −22 dB, HPF 300–400 Hz |

- Kleine Ereignisse (Chip erscheint): nur Transient. Mittlere (Antwort landet): Transient + Textur. Große (Logo,
  Reveal): alle drei, plus Stille davor.
- **Pan folgt der Bewegung:** was von links kommt, beginnt links (`pan −0,3 … −0,5`), Logo in der Mitte = 0.
- HPF 200–400 Hz auf allem außer Körper und Musik; Hall ~0,15 auf Texturen klebt sie in einen Raum.
- Familien statt Sammelsurium: 3–4 Familien pro Film (z. B. „weiche UI", „Papier", „ein tiefer Puls", Musik).
  Jede Familie hat 2–4 Varianten; dieselbe Datei nie zweimal hintereinander, sonst `vary`.

## Timing (Startwerte, am Bild prüfen)

| Ereignis | Platzierung |
|---|---|
| Pop/Klick/Landung | `align: peak` **auf** dem Frame, an dem es sichtbar landet (+0 … +50 ms) |
| Whoosh/Swish | Spitze ~150 ms **vor** der schnellsten Stelle bzw. dem Bewegungsende; nie über die ganze Fahrt |
| Riser | `align: end` auf den Reveal; danach 3–8 Frames fast Stille, dann der Hit |
| Tippen | nur wenn ein Cursor sichtbar tippt; Spur mit `trim` auf die Tippdauer kürzen |
| Kamerafahrt ohne Ereignis | nichts (Musik trägt) |
| Schnitt | Ton darf 2–4 Frames vor dem Bild wechseln (J-Cut): wirkt flüssiger |
| Einblendung zum Wort | Akzent ~80 ms vor dem Wort (Scribe-Wortzeiten) |

Dichte: Launchfilm 4–10 Cues/10 s, Erklärer 2–5, Einblendung 0–2. Mehr als ein Cue pro 0,5 s nur bei Tipp- oder
Stakkato-Passagen. Der Report nennt `cues_per_10s`.

## Musik schneiden

- Takte zählen: bei 120 BPM 1 Takt = 2,0 s. Schnitte im Stück immer auf Taktanfang (`beats.py` liefert `bars`).
- Ausschnitt so wählen, dass der Energiesprung (`energy_curve` im Index, Zehntel des Stücks) auf dem Reveal liegt.
  Zeit im Stück = Index der Zehntel × Länge/10.
- Länger als das Stück nötig? Zwei `music`-Einträge mit überlappendem Crossfade (0,5–1 s) an Taktgrenzen.
- Ende: entweder Ausklang (fade_out 1,5–3 s) oder hartes Ende auf einem Downbeat + Hall-Fahne eines SFX. Nie
  mitten im Takt abschneiden.
- Musik setzt gern **später** ein als das Bild (nach dem Hook), oder fällt für den Kernsatz kurz aus. Diese Lücken
  sind wirkungsvoller als jeder Effekt.
- BPM im Index ist gemessen (librosa) und kann halbiert/verdoppelt sein: Raster mit `beats.py` am Stück prüfen.

## Was gute Referenzen hörbar machen

- Apple/Clean-SaaS: fast nur Musik + 3–5 sehr leise UI-Transienten, große Momente durch Stille.
- Kinetic Type: Transient auf jedem Wortschlag, Pausen in der Musik = Pausen in der Typo.
- Storyboard/Skizze: Foley (Papier, Tisch) ist der Star, Musik leise.
- Whiteboard: Stift-Kratzen kurz und leise, keine Musik-Hits über der Stimme.

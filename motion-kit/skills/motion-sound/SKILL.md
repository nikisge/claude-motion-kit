---
name: motion-sound
description: "Use when a motion graphics film, animation or video insert needs sound (music choice, sound effects, cue list, ducking, loudness master) or when sounds are added to the local sound library. Trigger words: Sound, Ton, Musik, SFX, Geräusch, Whoosh, Cue-Liste, Mischung, LUFS."
---

# Motion Sound: Sound-Designer

Du bist Sound-Designer. **Du entscheidest**, was klingt, wie laut und wo Stille ist. Die Skripte suchen, messen,
platzieren und mischen nach deiner Cue-Liste; sie entscheiden nichts. Skripte liegen in `scripts/` dieses Skills,
die Bibliothek liegt in `sound/` im Arbeitsordner (oder in `$MOTION_SOUND_ROOT`).

## Einrichten (einmal)

1. Sounds von den Quellen in `library/LICENSES.md` laden (alle CC0 bzw. Pixabay-Lizenz, ohne Konto) nach
   `sound/sfx/<paket>/` und `sound/music/`. `library/sources.json` nach `sound/sources.json` kopieren.
2. Index bauen: `uv run scripts/sound_index.py` (misst Länge, Lautheit, Angriff, BPM, Energiekurve).

Ohne Bibliothek geht es auch: dann je Film 3–6 passende CC0-Dateien suchen, Lizenz notieren, direkt in die Cue-Liste.

## Was der Auftrag braucht

| Auftrag | Ton-Rolle |
|---|---|
| Launchfilm / Showreel | Musik führt (Beat-Raster `motion-inspo/scripts/beats.py`), Hauptereignisse auf Downbeats, Foley sparsam, Stille vor dem Logo |
| Erklär-Animation | Musik trägt leise, Foley am Objekt, der Kernsatz bekommt Ruhe |
| YouTube-Einblendung | Stimme ist der Star: meist keine Musik, 1–3 leise Akzente, Stimme duckt alles |
| Social vertikal | Hook-Sound in der ersten Sekunde, dichter, Musik lauter (stummes Abspielen mitdenken: Bild muss allein tragen) |
| Showcase / One-Shot | Sound ist Teil der Show: Schichten, Riser in den Reveal, ein Moment echter Stille |
| Kleiner Auftrag | 1 Musik-Ausschnitt oder 2–4 Cues, kein Konzept-Papier |

## Ablauf

1. **Konzept (3 Sätze im Brief):** Rolle der Musik (führt / trägt / keine), 3–4 Sound-Familien (z. B. Papier,
   weiche UI-Klicks, ein tiefer Puls), wo Stille ist. Startpunkt: „Sound“ der gewählten Stilkarte
   (`motion-director/references/styles/`).
2. **Musik wählen:** `python3 scripts/sound_search.py --music --mood ruhig --bpm 90-110`. Du hörst nicht: Entscheide
   über Stimmung, BPM und `energy_curve` und lege den Ausschnitt (`src_in`) so, dass ein Energiesprung auf den Reveal
   fällt. Raster: `uv run motion-inspo/scripts/beats.py track.mp3 --fps 30 --out <projekt>/beats.json --plot <projekt>/check/beats.png`.
   Ein Stück ohne klaren Kick taugt selten als treibende Showcase-Musik.
3. **Cue-Liste schreiben** (`cues.json` im Projekt), aus Storyboard + gerendertem Bild: Jeder Cue hat ein `note`
   mit seinem Bildgrund. Format: `references/cues.md`. Handwerk (Schichten, Timing, Musik schneiden):
   `references/craft.md`.
4. **Suchen:** `python3 scripts/sound_search.py papier --max-dur 0.6 --attack fast` (Wörter deutsch/englisch,
   `--cat`, `--dark/--bright`, `--not`). Angriff und Spitzenzeit bestimmen `align`.
5. **Platzieren + mischen:** `uv run scripts/sound_place.py cues.json --video film.mp4 --out mix.wav --mux film_ton.mp4`.
   Ergebnis: Mix auf −14 LUFS / ≤ −1 dBTP, `mix.report.json`, `mix.png` (Wellenform, Cue-Marker, Ducking-Kurve).
6. **Prüfen** nach `references/mix-check.md`, nach dem Export am MP4:
   `python3 scripts/sound_verify.py film.mp4 cues.json --out <projekt>/check/sound`. Optional im Feinschliff:
   **Earshot** als externe Prüfung (unten).
7. **Freigabe:** Der Mensch bekommt den Ton **allein** (mix.wav), die Cue-Liste und 5 Zeitstempel zum Anhören mit
   Kopfhörer (`HOEREN.md`). Der Agent misst nur, er hört nicht.

## Wer macht was: motion-sound und Earshot

Kein Entweder-oder. **motion-sound macht den Ton** (Bibliothek mit geprüften Lizenzen, Cue-Liste mit Bildgrund,
Platzieren, Ducking, Master auf −14 LUFS). **[Earshot](https://github.com/Leonxlnx/earshot) hört und prüft ihn**
(MIT, CPU, als CLI oder MCP-Server). Earshot ist nicht in diesem Kit, nur verlinkt. Installation laut README:
`uv tool install "earshot[mcp] @ git+https://github.com/Leonxlnx/earshot"`, dann `earshot doctor --fetch`
(lädt zwei Modelle, ca. 1,1 GB).

| Earshot-Befehl | Wofür im Feinschliff |
|---|---|
| `critique film.mp4` | Scorecard gegen 7 professionelle Launchfilme, mit Zeitstempeln und „FIX FIRST“ |
| `timeline film.wav --video film.mp4 --cues cues.json` | Hörprotokoll: Ereignisse, Lautheit, Sync von Ton zu Schnitt |
| `sheet film.wav -o check/earshot.png` | Bild mit Frames, Ereignissen, Spektrogramm, Lautheit |
| `match` / `rank` / `find` | den passenden Sound für eine Beschreibung finden (z. B. „a quill pen writing on paper“) |

Was Earshot bei uns gefunden hat: zu viele markante Schläge, fast mono, ein dünner Boden (zu wenig Tiefton). Nach der
Korrektur (Akzente 2–3 dB leiser, mehr Pan mit der Bewegung, Tiefton unter Treffer und Reveal) stieg das Urteil von
„close“ auf „launch-grade“.

**Grenzen:** Das Profil sind musikgeführte Launchfilme ohne Sprecher. Bei Filmen mit Stimme meldet Earshot die
Silbendichte der Stimme als „zu viele Schläge“ und die Mono-Stimme als „fast mono“. Diese Punkte mit Verstand lesen.
Earshot hat auch eine Bank mit Sounds aus Code (`sfx`, `kit`): für einzelne Lücken brauchbar (bei uns ein kurzer
Faden-Zip), aber jeden Sound im Mix prüfen. Earshot ersetzt das Hören nicht: Am Ende entscheidet ein Mensch mit Kopfhörer.

## Stimme (Sprecher-KI)

- **Faires Casting:** Hörproben auf −23 LUFS mit reiner Verstärkung, ohne Limiter (bei −16 LUFS clippen rohe
  TTS-Takes). Gleicher Text, gleiche Pausen, Namen der Stimmen blind vergeben.
- **Keine Temporaffung von TTS.** Ein auf 1,12 geraffter Take klang gehetzt und unnatürlich. Die Bildzeiten folgen der
  Stimme, nicht umgekehrt. Lieber einen Satz streichen.
- **Regie über Pausen und Musik, nicht über Flüstern.** Geflüsterte oder verschwörerische Sprecher-Regie klingt schnell
  anzüglich. Spannung entsteht durch eine Pause vor dem Satz und durch Musik, die wegbricht.
- Ganze, erzählende Sätze statt Telegrammstil („Panne? Werkstatt.“ versteht ohne Vorwissen niemand).
- Prüfen über Wortzeiten (Transkript mit Zeitstempeln je Wort), dann mit Kopfhörer.

## Treffer gegen Stimme messen

Soll ein Treffer lauter wirken als die Stimme: K-gewichtet (wie LUFS) in 100-ms-Fenstern messen, Treffer gegen die
lauteste Stimmstelle. Ein Treffer 3–4 dB über der Stimmspitze trägt. Wenn etwas „zu extrem“ wirkt, per Stem-Differenz
suchen (Mix einmal mit, einmal ohne das Element): Oft ist es nicht der Treffer, sondern die Musik, die danach
anschwillt. Dann nur diesen Eintrag ändern (`gain_path`, Tiefpass), nicht den ganzen Mix.

## Harte Regeln

- **Kein automatischer Whoosh** auf jeden Übergang. Jeder Sound braucht einen sichtbaren Grund; im Zweifel weg.
- **Nie einen Soundtrack im Code synthetisieren.** Das klingt billig. Sounds kommen aus der Bibliothek.
- Nie zweimal dieselbe Datei hintereinander; Wiederholungen mit `vary: true` (±2 dB, Rate 0,96–1,04).
- Stille ist ein Werkzeug: 3–8 Frames fast Stille vor dem großen Reveal.
- 3–4 Sound-Familien pro Film, nicht mehr.
- Stimme hat Vorrang: Musik 16–22 dB unter der Stimme.
- Nie eine Sprecher-Spur raffen, um eine Länge zu treffen.
- Nur Dateien mit geprüfter Lizenz. Neue Quelle: Lizenz auf der Originalseite prüfen, in `sound/sources.json`
  eintragen, Index neu bauen.

## Lücken füllen: echte Aufnahmen, dann KI

**Echte Aufnahmen zuerst:** Für zarte, reale Geräusche (Federkiel, Stoff, Holz) über
[openverse.org](https://openverse.org) eine CC0-Aufnahme suchen (`library/LICENSES.md`). Earshot `rank` hilft, aus
mehreren Kandidaten den passendsten zu finden.

**KI-generierte Sounds** (z. B. Text-zu-Audio über Higgsfield, `motion-higgsfield`):

Text-zu-Audio-Modelle liefern gute **konkrete, laute Einzelereignisse** (Riss, Wurf, Wind, Atem). Prompt im Stil
„LOUD close-up recording of …, clearly audible, full volume, no music“. Zarte, tonale, stehende oder rhythmische
Wünsche (Glas-Tick, Pfiff, Uhrticken, Gerätebrummen) ergeben meist nur Rauschen: dafür lieber Bibliothek. Jedes
Ergebnis vor Nutzung per Spektrogramm prüfen.

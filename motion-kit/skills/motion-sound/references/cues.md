# Cue-Liste (`cues.json`) für `motion-sound/scripts/sound_place.py`

Die Cue-Liste ist die Partitur des Sound-Designers. Sie liegt im Projekt neben dem Storyboard und ist die Grundlage
für die Ton-Freigabe. Pfade relativ zur `cues.json`, zu `motion-studio/` oder zu `motion-studio/sound/`.

## Felder

| Ebene | Feld | Bedeutung | Standard |
|---|---|---|---|
| oben | `fps` | für Frame-Zeiten `"f123"` | 30 |
| | `duration` | Filmlänge s | Videolänge bzw. letzter Cue + 3 s |
| | `master.lufs` / `master.true_peak` | Ziel | −14 / −1,0 |
| `voice` | `file` | Sprachspur; `"@video"` = Ton des Videos | – |
| | `t`, `gain_db` | Start, Pegel | 0, 0 |
| `music[]` | `file`, `t` | Datei, Start im Film | –, 0 |
| | `src_in`, `src_out` | Ausschnitt im Stück (s) | 0, Ende |
| | `gain_db`, `fade_in`, `fade_out` | Pegel vor Master, Blenden (s) | −10, 0,3, 1,0 |
| | `duck_db` | Absenkung unter Stimme (Attack 0,2 s, Hold 0,3 s, Release 0,8 s) | −12 |
| | `hpf`, `lpf` | Filter auf dem Ausschnitt (z. B. HPF 350 = „Atemzug“ vor dem Höhepunkt; für einen Filterwechsel denselben `src`-Punkt in zwei Einträgen kohärent überblenden) | – |
| | `gain_path` | `[[film_t, dB], …]` Lautstärke-Automation auf `gain_db` (linear in dB), z. B. Crescendo in den Höhepunkt statt Plateau | – |
| `cues[]` | `t` | Zeit: `1.25` (s), `"f30"` (Frame), `"0:01.25"` | – |
| | `file` | SFX aus der Bibliothek | – |
| | `align` | was auf `t` liegt: `onset` (erster hörbarer Moment), `start`, `peak` (lautester Moment), `end` | onset |
| | `gain_db` | Pegel vor Master | −10 |
| | `pan` | −1 links … 1 rechts (konstante Leistung): folgt der Bewegung | 0 |
| | `pan_path` | `[[film_t, pan], …]`: Pan wandert über die Zeit (linear, an den Enden gehalten), z. B. Flattern folgt dem Flieger; ersetzt `pan` | – |
| | `gain_path` | `[[film_t, dB], …]` auch für Cues: Wind schwillt an und fällt weg, ohne zweite Datei | – |
| | `rate` | Tempo+Tonhöhe (0,96–1,04 für Varianz, 0,8 für „schwerer") | 1 |
| | `trim` | `[von, bis]` s innerhalb der Datei | ganz |
| | `fade_in`, `fade_out` | s | 0, 0,01 |
| | `hpf`, `lpf` | Hoch-/Tiefpass Hz (HPF 200–400 räumt Matsch weg) | – |
| | `reverb` | Hallanteil 0–1 (~0,15 = „im selben Raum") | 0 |
| | `duck_music_db` | Musik kurz absenken um diesen Cue (Onset −0,05 s bis Spitze +0,3 s) | – |
| | `vary` | deterministisch ±2 dB, Rate 0,96–1,04 | false |
| | `note` | **Bildgrund** des Cues (Pflicht für dich, erscheint im PNG) | – |

Unbekannte Felder (`_film`, `_why`) werden ignoriert: gut für Notizen.

## Beispiel (Selbsttest, `motion-studio/sound/selftest/cues.json`, 10 s Launchfilm)

```json
{
 "fps": 24, "duration": 10.0,
 "master": {"lufs": -14, "true_peak": -1.0},
 "music": [{"file": "sound/music/beat-work.mp3", "t": 2.0, "gain_db": -9, "fade_in": 0.03, "fade_out": 0.8,
            "note": "Musik erst ab f48, wenn das Problem zur Frage wird"}],
 "cues": [
  {"t": "f0", "file": "sound/sfx/hyperframes-pixabay/impact-bass-1.mp3", "gain_db": -14, "lpf": 2500,
   "trim": [0, 1.4], "fade_out": 0.6, "note": "Störung: tiefer Puls"},
  {"t": "f12", "file": "sound/sfx/kenney/interface-sounds/Audio/error_007.ogg", "gain_db": -19, "pan": 0.35,
   "lpf": 6000, "note": "Lampe Schlag 2 (Schlag 1 trägt der Puls)"},
  {"t": 1.32, "file": "sound/sfx/oga-cc0/swishes/swish-7.wav", "align": "peak", "gain_db": -12, "hpf": 300,
   "reverb": 0.15, "note": "E1895 fliegt"},
  {"t": "f37", "file": "sound/sfx/hyperframes-pixabay/pop.mp3", "align": "peak", "gain_db": -13,
   "note": "Code rastet ein"},
  {"t": 4.8, "file": "sound/sfx/kenney/interface-sounds/Audio/confirmation_002.ogg", "gain_db": -15,
   "reverb": 0.15, "duck_music_db": -3, "note": "Antwort"}
 ]
}
```

Lesart: Musik setzt bewusst erst bei 2,0 s ein (davor nur Störung + Stille zwischen 1,6 und 2,0 s), der Flug hat
einen weichen Swish mit Spitze auf der schnellsten Stelle, das Einrasten ein Pop **auf** dem Frame, die Antwort ein
leiser Klang, unter dem die Musik kurz Platz macht. Kein Sound auf dem Kamera-Rückzug, weil dort nichts landet.

## Aufruf

```bash
cd content/youtube/editing-suite/motion-studio
uv run motion-sound/scripts/sound_place.py projects/<p>/cues.json --video projects/<p>/renders/film.mp4 \
  --out projects/<p>/renders/mix.wav --mux projects/<p>/renders/film_ton.mp4
```
`--png` legt den Bildpfad fest (Standard `<out>.png`), `--no-strip` lässt die Filmbilder weg. Ohne `--video` wird
nur der Ton gerendert (z. B. Ton-Freigabe vor dem Schluss-Render).

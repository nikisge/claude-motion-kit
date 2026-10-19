# Sound-Bibliothek: Quellen und Lizenzen

Stand Oktober 2026. Alle Quellen ohne Konto und ohne Kosten, lizenzrechtlich sauber für kommerzielle Videos
(YouTube, Kundenfilme). **Die Audiodateien sind nicht in diesem Repo** (Pixabay verbietet das Weiterverbreiten als
Paket). Lade sie von den Original-Seiten nach `sound/sfx/<paket>/` bzw. `sound/music/` in deinem Arbeitsordner und
baue dann den Index. `sources.json` liefert dabei die Lizenzspalte.

**Regel:** Nur Dateien verwenden, die im Index eine Lizenz haben. `sound_place.py` warnt bei Dateien außerhalb des
Index oder mit Lizenz `UNBEKANNT`. Neue Quellen: erst Lizenz auf der Originalseite prüfen, Eintrag in
`sources.json`, dann `uv run motion-sound/scripts/sound_index.py`.

## Bestand im Originalprojekt (854 Dateien nach Duplikat-Bereinigung, ~106 MB)

| Ordner | Dateien | Quelle | Urheber | Lizenz |
|---|---|---|---|---|
| `sfx/kenney/` (8 Pakete: casino, digital, impact, interface, music-jingles, rpg, sci-fi, ui) | 604 | kenney.nl/assets/&lt;paket&gt; | Kenney | CC0 1.0 (`License.txt` je Paket) |
| `sfx/hyperframes-pixabay/` | 17 (+2 Duplikate) | Pixabay, gebündelt im HyperFrames-Repo | Pixabay-Urheber, siehe `CREDITS.md` | Pixabay Content License |
| `sfx/remotion-cc0/` | 7 | remotion.dev/docs/sfx/&lt;name&gt; | Remotion | CC0 (je Doku-Seite ausgewiesen) |
| `sfx/oga-cc0/100-cc0-sfx/` | 97 (Haushaltsgeräusche Toilette/Mikrowelle/Geschirr vom Index ausgenommen) | opengameart.org/content/100-cc0-sfx | rubberduck | CC0 |
| `sfx/oga-cc0/sfx-breaking-and-falling/` | 75 | opengameart.org/content/75-cc0-breaking-falling-hit-sfx | rubberduck | CC0 |
| `sfx/oga-cc0/swishes/` | 13 | opengameart.org/content/swishes-sound-pack | artisticdude | CC0 |
| `sfx/oga-cc0/bookflip-sfx/` | 13 | opengameart.org/content/book-flip-sounds | Voltiment555 | CC0 |
| `sfx/oga-cc0/book-flips/` | 10 | opengameart.org/content/10-book-page-flips | StarNinjas | CC0 |
| `sfx/oga-cc0/ding/` | 4 | opengameart.org/content/4-metal-dingsrings | StarNinjas | CC0 |
| `sfx/oga-cc0/misc/air-whoosh.wav` | 1 | opengameart.org/content/air-whoosh | pyranostudios | CC0 |
| `sfx/oga-cc0/misc/map-open/close.wav` | 2 | opengameart.org/content/opening-and-closing-a-map-sounds | Spring Spring | CC0 |
| `sfx/oga-cc0/misc/equipment-clicks.wav` | 1 | opengameart.org/content/equipment-clicks-ii | LFA | CC0 |
| `sfx/oga-cc0/misc/bell-ding-1..4.wav` | 4 | opengameart.org/content/bell-dingschimes | PWL | CC0 |
| `music/` | 11 | archive.org (Items unten) | Loyalty Freak Music, Komiku, Monplaisir | CC0 (Item-Lizenz `licenseurl` geprüft) |

OpenGameArt-Lizenzen am 11.10.2026 auf jeder Paketseite geprüft (nur CC0 gelistet). Die CC0-Suchfilter von OGA sind
nicht streng; abgelehnt wurden u. a. „writing scribbles" (CC-BY-SA) und „paper crumple" (CC-BY 4.0).

### Musik (11 Stücke, verschiedene Stimmungen/Tempi)

| Datei | Titel, Künstler | archive.org-Item | BPM (gemessen) | Stimmung (nach Album/Titel + Lautheitsverlauf) |
|---|---|---|---|---|
| `ambient-hope-komiku.mp3` | Ambiant Hope, Komiku | monplaisirchillandambiantsongsfrommonplaisirciesprojectsundercreativecommons0andpublicdomain | 99 | ruhig, hoffnungsvoll, Aufbau |
| `calm-softly.mp3` | Softly, Loyalty Freak Music | LoyaltyFreakMusicMELODIESWITHABEAT2018030251947223 | 70 | ruhig, gleichmäßig |
| `lofi-sugar-and-coffee.mp3` | Sugar and coffee, Loyalty Freak Music / Lack of Color | loyalty-freak-music-lofi-ambient-songs | 76 | Lo-Fi warm |
| `lofi-aeroplane.mp3` | Aeroplane, Loyalty Freak Music / Lack of Color | loyalty-freak-music-lofi-ambient-songs | 76 | Lo-Fi verträumt |
| `beat-work.mp3` | Work, Loyalty Freak Music | LoyaltyFreakMusicMELODIESWITHABEAT2018030251947223 | 118 | mittlerer elektronischer Beat |
| `rise-sky-5.mp3` | Sky 5 (The Rise, The Walk, The Hope), Monplaisir | monplaisirchillandambiant… (s. o.) | 118 | aufsteigend, optimistisch |
| `drive-free-to-use-1.mp3` | Free To Use 1, Monplaisir | Monplaisir-FreeToUse | 129 | treibend, große Dynamik |
| `playful-shoepop.mp3` | Shoepop, Loyalty Freak Music | LoyaltyFreakMusicMELODIESWITHABEAT2018030251947223 | 99 | verspielt, poppig |
| `playful-awkward-cute-dance.mp3` | Awkward cute dance, Komiku | komiku-the-adventure-goes-on-vol.-2 | 89 | verspielt, schräg |
| `tension-intense-fight.mp3` | Intense fight, Komiku | komiku-the-adventure-goes-on-vol.-2 | 92 (evtl. 184) | Spannung, drängend |
| `tech-high-technologic.mp3` | High Technologic Beat Explosion, Loyalty Freak Music | LoyaltyFreakMusicROBOTDANCE2017113032423755 | 92 (evtl. 184) | elektronisch, technisch |

Links: `https://archive.org/details/<item>`. BPM per librosa gemessen, Halb-/Doppeltempo möglich; Stimmungen sind **nicht per Ohr geprüft** (der Agent hört nicht):
vor dem Einsatz anhören, ggf. in `sources.json` korrigieren (`mood`, `bpm` überschreiben die Messung).

## Pixabay Content License: was zu beachten ist

Kommerziell frei, ohne Namensnennung, auch in bearbeiteter Form im Video. Nicht erlaubt: die Sounds **eigenständig**
weiterverbreiten/verkaufen (z. B. als Sound-Paket). Darum liegen die Dateien nur lokal, im Repo nur Metadaten.
Duplikate im Upstream-Paket: `whoosh.mp3` = `whoosh-short.mp3`, `click.mp3` = `click-soft.mp3` (je einmal indexiert).

## Bewusst nicht aufgenommen

| Quelle | Grund |
|---|---|
| FreePD.com | Seite geschlossen (Stand 10/2026) |
| Freesound.org | Download nur mit Konto/OAuth; Lizenzen je Sound gemischt (viel CC-BY/CC-BY-NC) |
| Pixabay Musik/SFX direkt | keine API für Audio, Bot-Sperre; Konto nötig |
| Sonniss GDC-Bundles | sehr groß (>20 GB), Lizenz verbietet Nutzung für KI-Training, eigene AGB |
| Remotion-Meme-Sounds (vine boom, bruh …) | Rechte unklar, nicht als CC0 ausgewiesen |
| Incompetech (Kevin MacLeod) | CC-BY: Namensnennung in jeder Beschreibung nötig; vermeidbar |
| YouTube Audio Library | nur über Studio-Konto, Lizenz an YouTube gebunden |
| Selbst synthetisierter Soundtrack im Code | Regel: nie (klingt billig); Sounds kommen aus der Bibliothek |

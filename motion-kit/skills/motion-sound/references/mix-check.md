# Mischung und Prüfung

## Pegel (relativ, vor dem Master)

| Element | ohne Stimme | mit Stimme |
|---|---|---|
| Musik | −8 … −12 dB | 16–22 dB unter der Stimme (Ducking −12 dB, Attack 0,2 s, Hold 0,3 s, Release 0,8 s) |
| UI-SFX (Klick, Pop) | −8 … −14 dB | −14 … −20 dB |
| Whoosh/Swish | −8 … −12 dB | −16 … −22 dB |
| Großer Hit (Logo) | −6 … −10 dB, Musik mit `duck_music_db −3 … −6` | selten |

Master: −14 LUFS integriert (YouTube-Norm), True Peak ≤ −2 dBTP im WAV, damit nach AAC im MP4 ≤ −1,5 dBTP bleibt; LRA 4–10 LU (sehr kurze Filme < 15 s dürfen darunter liegen).
`sound_place.py` hebt/senkt den Gesamtpegel und begrenzt Spitzen (4× überabgetastet), dann misst es nach
(eigene BS.1770-Messung und unabhängig `ffmpeg ebur128`). Beide Werte stehen im Report.

## Prüfen (du hörst nicht: prüfe, was messbar und sichtbar ist)

1. **Report-Warnungen** (`mix.report.json`, auch in der Konsole) alle abarbeiten:
   - „gleiche Datei zweimal hintereinander" → andere Variante oder `vary`.
   - „Limiter greift bis X dB" (> 6 dB) → der lauteste Cue ist zu laut, nicht der Master.
   - „Musik nur X LU unter Stimme" → Musik runter oder `duck_db` tiefer.
   - „ragt aus dem Film" / „nicht im Index" / „Lizenz UNBEKANNT" → beheben, nie ignorieren.
2. **`mix.png` ansehen:** liegt jeder rote Cue-Marker über dem Filmbild, das ihn begründet? Gibt es Stellen, an
   denen etwas Großes passiert und die Wellenform flach bleibt (fehlender Akzent) oder Stellen ohne Ereignis mit
   Spitzen (überflüssiger Cue)? Ist vor dem großen Reveal eine sichtbare Lücke? Zeigt die orange Ducking-Kurve
   Absenkungen genau unter der Stimme?
3. **Dichte:** `cues_per_10s` gegen die Tabelle in `craft.md`. Zu viele Cues sind der häufigste Fehler.
4. **Familien zählen:** mehr als 4 verschiedene Klangfamilien in der Cue-Liste → streichen.
5. **Stems:** `stems_lufs_after_gain` zeigt SFX-, Musik-, Stimm-Lautheit. SFX lauter als Musik ist bei Filmen ohne
   Stimme ein Warnsignal (Effektgewitter), außer bei Showcase-Momenten.
6. **Gegenprobe Bild:** an kritischen Cues einen Frame-Bogen ziehen
   (`python3 motion-inspo/scripts/sheet.py film.mp4 check/cue --every 0.0417 --from 4.6 --to 5.0`): liegt die Landung wirklich auf
   dem Frame, auf den der Cue zielt? Bei Abweichung `t` in Frames (`"f115"`) statt Sekunden angeben.

## Höhepunkt gegen Limiter (gemessen an einem 45-s-Launchfilm, 10/2026)

Bei festem Ziel (−14 bis −14,5 LUFS) ist der Spielraum begrenzt: Musik mit ~13 dB Crest erreicht ohne Limiter nur etwa
M −12,5 LUFS. Jedes dB, das der Höhepunkt darüber liegt, kostet Limiter-Arbeit und Crest. Darum den Höhepunkt
**ansteigen** lassen (`gain_path`-Crescendo, Spitze erst kurz vor dem Bruch), Rausch-Betten (Wind, Flattern) dort leiser,
Senken nicht zu tief (sonst hebt der Master alles an). Messen: Limiter-Arbeit und Crest je Sekunde, Lautheit je
Abschnitt (ffmpeg `ebur128`). Onset-Dichte (spektraler Fluss) misst vor allem den Musik-Rhythmus:
weniger SFX senken sie kaum, die Cue-Zahl je 10 s ist das ehrlichere Maß für Foley-Dichte.

## Nach dem Export (Pflicht, am MP4, nicht am WAV)

`python3 motion-sound/scripts/sound_verify.py <film.mp4> <cues.json> --out <projekt>/check/sound` misst den fertigen Film
(ffmpeg ebur128 nach AAC: Lautheit, True Peak, Mono-Summe für Handy-Lautsprecher), legt je Cue ein Bild davor und
danach ab, zeichnet die Wellenform und schreibt `HOEREN.md` mit 5 Zeitstempeln für die Kopfhörer-Probe durch einen Menschen.
Jedes PROBLEM beheben. Die Bilder vor/nach jedem Cue ansehen: sieht man den Grund für den Ton genau dort?
Im Bericht nie „klingt gut“ schreiben, sondern Messwerte + die 5 Zeitstempel nennen.

## Ton-Freigabe

Normaler Auftrag: Der Nutzer bekommt `mix.wav` (Ton **allein**, ohne Bild) und die Cue-Liste mit `note`-Spalte. Ton
allein zeigt sofort, ob er zu voll, zu billig oder zu laut ist. One-Shot/Showcase: Critic bewertet „Sound" in der
Rubrik; der Designer behebt und rendert neu.

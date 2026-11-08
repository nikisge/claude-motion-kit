# Stilkarte: 3D-Welt (Three.js, stilisiert, Path Tracing)

**Wann wählen:** eine Geschichte ohne Worte in einer kleinen, stilisierten Welt: Diorama, schwebende Insel, Dorf,
Werkstatt, Miniatur-Stadt. Für Intros, Showcases, „während du schläfst, passiert …“-Geschichten. Licht ist der
Hauptdarsteller. Nicht für Produkt-Makros (dafür [3d-object-story](3d-object-story.md)) und nicht für YouTube-
Erklärstellen (dort wirkt eine dunkle 3D-Bühne schnell schwer; besser Whiteboard oder Papierschnitt).

**Bildidee:** Eine einzige Kamerafahrt umkreist eine Miniaturwelt. Die Welt verändert sich über die Zeit (etwas wird
gebaut, Licht wechselt von Abend über Nacht zum Morgen), und der Höhepunkt ist ein Licht-Ereignis: die Sonne bricht
durch, Fenster gehen an, ein Leuchtturm zündet. Matte Materialien wie Spielzeug, Tiefenunschärfe wie bei einem
Miniatur-Foto.

## Leitreferenzen (Grammatik, nie Inhalt)

| Ref | Was passiert | Übernehmen |
|---|---|---|
| [Higgsfield, schwebende Insel](https://x.com/higgsfield_ai/status/2111509918490755394) | Insel im Wolkenmeer, Nähe mit Nebel, Dorf taucht gestaffelt hinter Segeln auf, ein Licht geht als Höhepunkt an, Rückfahrt zur Totalen | **Licht-Ereignis als Treffer**, gestaffeltes Auftauchen, Rückfahrt am Ende |
| [Leon Lin, Three.js-Szene über den Wolken](https://x.com/LexnLin/status/2117230395406364857) ([Repo](https://github.com/Leonxlnx/halo-above-the-clouds)) | Echtzeit-Three.js, eine Architektur über dem Wolkenmeer, lizenzierte Musik | Wolkenmeer als Bühne, Ruhe |
| [Leon Lin, Maskottchen-Film](https://x.com/LexnLin/status/2110389810258968965) | eigener Three.js-Renderer, keine Schrift, nur echte freie Sounds | **Film ohne Text**, Ton aus echten Aufnahmen |

Wie Higgsfield die Insel gebaut hat, ist nicht belegt (Blender oder Unreal sind möglich). Übernommen wird nur die
Grammatik.

## Messwerte (Apple M5, HyperFrames-Beispiel `path-traced-3d`, 11/2026)

| | Wert |
|---|---|
| Raster-Vorschau | ~1 s/Bild |
| 1080p path-traced, 16 / 32 / 64 spp | ~7 / ~14 / ~28 s/Bild |
| 19 s Film, 24 fps, 32 spp | gut 2 h Render + wenige Minuten Entrauschen |
| RAM-Spitze | ≤ 2 GB |

Ehrlicher Stand: Standbilder und eine 540p-Vorschau sind gebaut und gelobt, ein fertiger 1080p-Film nicht.

## Startwerte

- **Modelle:** Requisiten über Bild → 3D (`motion-3d`, `motion-higgsfield`, ~1–2,5 Credits je Objekt), Grundformen
  nur für Boden, Wege, Zeltplanen. Eine Figur mit Persönlichkeit (Helm, Lampe, Haltung), nicht nur ein Klotz.
- **Material:** matt (Filz, Holz, Keramik ohne Klarlack). Fenster mit eigener Maske, nachts warm leuchtend.
- **Licht:** tiefe Sonne als Flächenlicht mit Radius; Abendrot → blaue Stunde → Nacht mit warmen Fenstern →
  Morgengrauen → Sonne. Kurzes Überblenden der Belichtung (0,7 s verzögert) beim Treffer.
- **Himmel:** eigene Shader-Ebene (Wolkenmeer, Streifenwolken, Sterne, Sonnenscheibe), die dem Tracer das
  Umgebungslicht liefert.
- **Kamera:** ein Pfad durch ~20 Schlüssel (Catmull-Rom), Miniatur-Unschärfe (große Blende, flache Schärfe),
  24 fps. Die Figur bleibt in jedem Bild sichtbar: in der Raster-Vorschau prüfen.

## Sound-Charakter

Vier Familien: Natur-Atmo (Wind, Grillen, Vögel), Holz-Foley (jedes Bauteil ein Klack, Tonhöhe steigt mit dem
Tempo), Figur (kleine Klicks, ein Reim zwischen Anfang und Ende, z. B. derselbe Reißverschluss), Musik (verspielt auf
Takt im Aufbau, bricht vor dem Treffer ab, warme Fläche danach). Vor dem Treffer 0,8–1 s nur Wind. Alles aus echten
Aufnahmen, nichts im Code synthetisiert.

## Signature Moves (Bauweise)

1. **Zeitraffer-Aufbau:** Teile wachsen mit Überschwinger, die Abstände werden kürzer (z. B. 0,55 → 0,26 s), die
   Kamera kreist dabei schneller.
2. **Licht als Uhr:** ein ganzer Tag in einer Fahrt, ohne Schnitt.
3. **Licht-Treffer:** Sonnenrand bricht in wenigen Bildern direkt neben der Figur durch, Fenster und Lampen gehen aus.
4. **Stille am Rand:** Figur klein am Ende eines Stegs oder Felsens, Kamera fast still.
5. **Rückfahrt zur Totalen:** die fertige Welt im Wolkenmeer als letztes Bild.
6. **Requisiten erzählen den Fortschritt:** ein Stapel schrumpft, eine Karre leert sich, während gebaut wird.

## Slop-Fallen

- Block-Häuser, Kugelwolken, Low-Poly-Standard: sieht nach Tech-Demo aus, nicht nach Welt.
- Rauschen in Wolken und Schatten. Nativ rendern und entrauschen; hochskaliertes 540p entrauscht der Denoiser nicht.
- Klarlack und Glanz auf allem (Plastik-Look), Standardlicht ohne Tageszeit.
- Kamera verliert die Figur bei schnellen Fahrten (in der Vorschau sofort sichtbar, im Path Tracing teuer).
- Renderzeit unterschätzt: erst messen (1 Bild), dann planen. Ein Render gleichzeitig.
- KI-3D-Bild als Wackelbild statt echter Modelle.

## Variationen

- **Insel im Wolkenmeer** · **Werkstatt auf dem Tisch** · **Stadt bei Nacht** (Fenster schreiben ein Wort).
- Schneller und billiger: nur Raster-Rendering mit gutem Licht, ohne Path Tracing, für Vorschau-nahe Qualität.
- Mischen: Treffer-Bild als Standbild für ein Videomodell, wenn eine Bewegung in 3D zu teuer wird.

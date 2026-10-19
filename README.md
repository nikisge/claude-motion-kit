# Claude Motion Kit

Motion Graphics in **verschiedenen Stilen** mit Claude Code und [HyperFrames](https://github.com/heygen-com/hyperframes).

HyperFrames allein reicht nicht: Ohne Stil und ohne Vorbilder sieht jedes KI-Video gleich aus (Verlauf, Glaskarten,
Fade-up, Logo auf leerer Fläche). Dieses Kit gibt Claude das, was fehlt: **einen Ablauf wie bei einem Motion
Designer, Stilkarten, echte Referenzfilme und Werkzeuge, die messen statt raten.**

Entstanden aus einem echten Projekt (Oktober 2026), noch nicht fertig (Version 0.1). Es ist bewusst schlank: 5
Skills, ein paar Python-Skripte, keine eigene App.

## Was den Unterschied macht

In unseren Tests (zwei Blindrunden mit gleichem Auftrag, HyperFrames pur gegen HyperFrames mit diesem Prozess, dazu
ein 45-s-Film über drei Critic-Runden) haben vier Dinge am meisten gebracht. Mehr Skills oder Repos gehörten nicht dazu:

1. **Eine gemessene Ziel-Referenz pro Film.** Ein echter Launchfilm wird mit `ref_metrics.py` gemessen (Schnitte,
   Kamerabewegung, Einstieg …) und dient als Ziel. Gefühlte Dichte kommt meist aus Kamerafahrten, nicht aus Schnitten.
2. **Ein unabhängiger Critic.** Ein frischer Subagent sieht nur Bilder und Zahlen, keinen Code. Wer gebaut hat,
   bewertet sich im Schnitt deutlich zu gut.
3. **Eine Ideen-Runde ohne „Werkzeug als Held“.** Filme scheitern öfter an der Story als am Handwerk.
4. **Geschmack als Daten:** Referenzen, die man gut findet, und Anti-Referenzen („Slop“) schriftlich festhalten.

## Der Prozess

```
Brief (1 Versprechen, 1 Bild)
  → Stil wählen (Stilkarte) + EINE Ziel-Referenz suchen und messen
  → Inspo/Moodboard mit dir abstimmen
  → 3 Style Frames (Standbilder im echten Look)
  → Storyboard + Animatic auf dem Beat-Raster
  → Bauen (schwerste Einstellung zuerst)
  → Prüfen: motion_check (Slop-Muster) + ref_metrics (gegen die Referenz) + Kontaktbogen
  → Critic (höchstens 2 Runden)
  → Ton (Cue-Liste, −14 LUFS)
  → Export (10 Bit + Korn gegen Banding)
```

Für „zeig, was du kannst“ ohne Rückfragen gibt es einen One-Shot-Modus (Ideen-Runde, zwei geplante Staun-Momente,
Critic vor und nach dem Animieren).

## Stile

| Stil | Wann | Leitreferenzen |
|---|---|---|
| **Clean SaaS Story** | Produkt mit echter UI, ein Gedanke, ruhig | claude-google-workspace, adipanda |
| **Apple Premium** | teuer, präzise, keynote-artig; Reveal, Zahl | apple-wonderful-tools, leo-apple |
| **Kinetic Type** | Manifest, Hook, Musik trägt | how-do-you-communicate, glyph |
| **3D-Objekt-Story** | ein Ding erzählt (Produkt, Symbol) | kimi-3-couldve-never-done-this |
| **Storyboard / Skizze** | Prozess, Pipeline, Behind the Scenes | simi-launch, higgsfield-motion-pipeline |
| **Whiteboard-Explainer** | YouTube-Einblendung, Abläufe erklären | Kurzgesagt, Vox |

Jede Karte (`motion-kit/skills/motion-director/references/styles/`) enthält: Bildidee, Leitreferenzen mit
Zeitstempeln, Messwerte, Startwerte (Farbe, Typo, Easing), Sound, typische Moves und Slop-Fallen. Karten sind
Startpunkte: mischen, abweichen und **einen eigenen Einfall** pro Film festlegen.

50 Referenzfilme nach Stil (nur Links): [`referenzfilme.md`](motion-kit/skills/motion-inspo/references/referenzfilme.md).
Weitere Skills mit anderen Stilen, Inspo-Seiten und Blender: [`RESOURCES.md`](RESOURCES.md).

## Installieren

Der einfachste Weg: Sag es deinem Coding-Agenten (Claude Code, Codex, Cursor …). Kopier diesen Satz in den Chat:

```
Installiere mir https://github.com/nikisge/claude-motion-kit nach der Anleitung "Für Agenten" in der README.
```

**HyperFrames ist nicht in diesem Repo.** HyperFrames ist die Render-Engine von HeyGen (npm-Paket + eigene Skills) und
wird extern installiert. Dieses Kit ist die Schicht darüber: Prozess, Stile, Referenzen und Prüfwerkzeuge. Der Skill
`motion-hyperframes` zeigt dem Agenten nur, wie er HyperFrames dafür benutzt.

### Für Agenten

1. Voraussetzungen prüfen und fehlende nennen (nicht ungefragt systemweit installieren): Node 22+, `ffmpeg`,
   Python 3.10+, `uv`.
2. HyperFrames-Skills installieren:
   - Claude Code: `claude plugin marketplace add heygen-com/hyperframes` und `claude plugin install hyperframes@hyperframes`
   - andere Agenten: `npx hyperframes skills update`
3. Dieses Kit installieren:
   - Claude Code: `claude plugin marketplace add nikisge/claude-motion-kit` und
     `claude plugin install motion-kit@claude-motion-kit`
   - andere Agenten: `npx skills add nikisge/claude-motion-kit --all` (installiert die 5 Skills aus
     `motion-kit/skills/` in den Skill-Ordner des Agenten)
4. Prüfen: Die Skills `motion-director`, `motion-inspo`, `motion-hyperframes`, `motion-3d` und `motion-sound` sind
   verfügbar (bei Claude Code nach einem Neustart der Sitzung).
5. Dem Nutzer kurz sagen, was installiert wurde, und einen Beispiel-Prompt aus „Loslegen“ vorschlagen.

Hinweise: Die Text-Prüfungen in `motion_check.py` nutzen macOS-OCR, auf Linux/Windows laufen nur die Bild- und
Zeitprüfungen. Blender ist optional (Skill `motion-3d`) und wird nur auf ausdrücklichen Wunsch eingerichtet.

## Loslegen

In Claude Code, in einem leeren Arbeitsordner:

```
Mach mir einen 20-Sekunden-Launchfilm für <Produkt>. Nutze motion-director.
Stil: Kinetic Type. Such dir eine Ziel-Referenz auf whatships und miss sie, bevor du baust.
```

```
Finde mir 5 Referenzen für "camera dives into ui" und zeig mir die Kontaktbögen.
```

```
Prüf diesen Render gegen die Referenz und sag mir ehrlich, wo er schwächer ist.
```

## Was drin ist

| Skill | Wofür | Werkzeuge |
|---|---|---|
| `motion-director` | Ablauf, Brief, Storyboard, Prüfregeln mit Zahlen, Critic-Rubrik, Formate, **Stilkarten** | – |
| `motion-inspo` | Referenzen suchen (whatships, flowjam), laden, zerlegen, messen; Slop-Prüfung | `refs.py`, `sheet.py`, `ref_metrics.py`, `motion_check.py`, `beats.py` |
| `motion-hyperframes` | Bauen, prüfen, rendern, mastern in HyperFrames; Fallstricke | `master_10bit.sh` |
| `motion-3d` | Echtes 3D in HyperFrames (Metall, Glas, Tiefenunschärfe, Shot-Liste); Blender als Modell-Quelle | `hf3d` (Three.js-Studio), Beispielfilm `rondo` |
| `motion-sound` | Sound-Design: Cue-Liste, Suchen, Platzieren, Mischen auf −14 LUFS, Prüfen | `sound_index.py`, `sound_search.py`, `sound_place.py`, `sound_verify.py` |

## Ehrliche Grenzen

- Der Agent hört nicht. Ton wird gemessen, entscheiden muss am Ende dein Ohr.
- Musik ist der schwächste Baustein: Freie CC0-Musik gibt es wenig, und die Auswahl läuft ohne Hören.
- Der Blender-Teil ist nach Recherche geschrieben, nicht in einem echten Film getestet.
- Ein Durchlauf mit Critic dauert eher Stunden als Minuten. „One Shot“ in 5 Minuten ist Marketing.
- Referenzclips gehören ihren Urhebern: nur lokal studieren, nie neu hochladen.

## Lizenz

MIT für Skills und Skripte. Mitgelieferte Fremdteile (Three.js, Schrift Geist) behalten ihre Lizenz, siehe `LICENSE`.

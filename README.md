# Claude Motion Kit

KI-Videos in **echten Stilen** statt KI-Slop, gebaut mit Claude Code, [HyperFrames](https://github.com/heygen-com/hyperframes)
und optional [Higgsfield](https://higgsfield.ai).

Ohne Vorgaben baut ein Agent eine Website, die sich bewegt: zentrierter Titel auf Verlauf, Glaskarten mit Icons, alles
blendet von unten ein, Text wiederholt das Gesprochene, am Ende Logo und Claim auf leerer Fläche. Das liegt nicht an der
KI, sondern daran, dass sie rät, wenn sie kein Vorbild hat. Dieses Kit gibt ihr einen Ablauf wie bei einem Motion
Designer: **Inspo zuerst, dann der richtige Werkzeugkasten, dann Feinschliff**, und es speichert, was dir gefällt.

Version 0.2 (November 2026). Entstanden an echten Videos, bewusst schlank: 6 Skills, 10 Stilkarten, ein paar
Python-Skripte, keine eigene App. Video dazu: folgt.

## Die 3 Schritte

### 1. Inspo

Nie von null anfangen. Erst einen Stil wählen (Stilkarte), dann **eine konkrete Ziel-Referenz** suchen (z. B. auf
[whatships.com](https://whatships.com) oder YouTube), messen und Shot für Shot zerlegen. Gefühlte Dichte kommt meist aus
Kamerafahrten, nicht aus Schnitten, und das zeigt erst die Messung. Bei erzählten Formaten steht die Story fest, bevor
gebaut wird.

### 2. Werkzeugkasten

Drei Bausteine, jeder für das, was er am besten kann:

| Baustein | Wofür |
|---|---|
| **HyperFrames** | Hier wird alles gebaut. Claude schreibt eine Webseite, die zu jeder Sekunde weiß, wie sie aussieht; HyperFrames fotografiert sie Bild für Bild zu einem Video. Kamera, Typo, Masken, Übergänge, Three.js, Schnitt |
| **Higgsfield** (optional, kostet Credits) | Was Code nicht kann: echtes Video in einem neuen Look neu zeichnen (Genjutsu), gestaltete Welten aus Videomodellen (Seedance, Kling), Bilder als Bausteine, Bild → 3D-Modell für Three.js. Per MCP direkt in Claude Code, Preis vor jedem Job |
| **Dieses Kit** | der Prozess, die Stilliste, das Storyboard, Prüfwerkzeuge, Ton |

Der wichtigste Teil aus dem Kit ist das **Storyboard**: eine Review-Seite mit Richtungen, Spannungskurve, Shotliste,
Standbildern und Kosten, die du abnimmst, bevor eine Sekunde animiert oder generiert wird. Das spart Credits und Frust.

Eine Regel, die viel Slop verhindert: **Videomodelle für gestaltete Welten, nicht für Wirklichkeit.** Wolle, Papier,
Tusche, Miniatur: gut. Fotorealistische KI-Szenen und KI-„Archivfotos“: wirken billig. Echtes Material (eigene
Aufnahmen, gemeinfreie Archive) schlägt KI-Bilder.

### 3. Feinschliff

- Selbst prüfen: Slop-Muster messen (`motion_check`), gegen die Referenz messen (`ref_metrics`), Kontaktbogen mit
  4 Bildern pro Sekunde, Lesbarkeit am echten Frame.
- Ton prüfen: Pegel und Sync messen, optional extern mit [Earshot](https://github.com/Leonxlnx/earshot). Am Ende hört
  ein Mensch mit Kopfhörer.
- Dein Feedback: Gefühl plus Zeitstempel, kein 3-Seiten-Prompt. Höchstens zwei Runden, dann abgeben.
- Optional ein unabhängiger Critic-Subagent, der nur Bilder sieht. Hilft bei Bildfehlern, ist aber kein Pflichtschritt.

### Learnings speichern

Was dir gefällt und was du als Slop ablehnst, landet in `refs/taste.md` und wird vor jedem Film gelesen. Was nur für
einen Film gilt, steht in seiner `DECISIONS.md`. Hat ein Film einen neuen Stil etabliert, wird daraus eine Stilkarte.
So startet jedes Video auf dem Stand des letzten.

## Stile

| Stil | Wann | Werkzeug |
|---|---|---|
| **Clean SaaS Story** | Produkt mit echter UI, ein Gedanke, ruhig | HyperFrames |
| **Apple Premium** | teuer, präzise, keynote-artig; Reveal, Zahl | HyperFrames |
| **Kinetic Type** | Manifest, Hook, Musik trägt | HyperFrames |
| **3D-Objekt-Story** | ein Ding erzählt (Produkt, Symbol) | HyperFrames + Three.js |
| **Storyboard / Skizze** | Prozess, Pipeline, Behind the Scenes | HyperFrames |
| **Whiteboard-Erklärer** | YouTube-Einblendung, Abläufe erklären | HyperFrames |
| **Doku mit Archivmaterial** (neu) | wahre Geschichte mit Erzählerstimme; Karte und Archiv als Rückgrat, eine Fahrt | HyperFrames + gemeinfreies Archiv, wenige Bilder aus Higgsfield |
| **Gestaltete Welt** (neu) | echte Aufnahme kippt in eine Welt aus Material; Launch, Intro | Higgsfield (Genjutsu, Seedance) + HyperFrames-Nähte |
| **3D-Welt** (neu) | Geschichte ohne Worte in einer Miniaturwelt, Licht als Höhepunkt | Three.js + Higgsfield Bild → 3D, Path Tracing |
| **Papierschnitt-Erklärer** (neu) | „Was passiert, wenn …“: Reise durch Maßstäbe mit Sprecher | HyperFrames |

Jede Karte (`motion-kit/skills/motion-director/references/styles/`) enthält: wann wählen, Bildidee, Leitreferenzen mit
Zeitstempeln, Messwerte, Startwerte, Sound, typische Moves und Slop-Fallen. Karten sind Startpunkte: Grammatik
übernehmen, eigene Geschichte erzählen, **einen eigenen Einfall** pro Film festlegen.

Referenzfilme nach Stil (nur Links): [`referenzfilme.md`](motion-kit/skills/motion-inspo/references/referenzfilme.md).
Weitere Skills, Repos, Inspo-Seiten und Blender: [`RESOURCES.md`](RESOURCES.md). Änderungen: [`CHANGELOG.md`](CHANGELOG.md).

## Installieren

Der einfachste Weg: Sag es deinem Coding-Agenten. Kopier diesen Satz in den Chat:

```
Installiere mir https://github.com/nikisge/claude-motion-kit nach der Anleitung "Für Agenten" in der README.
```

**HyperFrames, Higgsfield und Earshot sind nicht in diesem Repo.** Sie werden extern installiert bzw. verbunden. Dieses
Kit ist die Schicht darüber: Prozess, Stile, Referenzen und Prüfwerkzeuge.

### Für Agenten

1. Voraussetzungen prüfen und fehlende nennen (nicht ungefragt systemweit installieren): Node 22+, `ffmpeg`,
   Python 3.10+, `uv`.
2. HyperFrames-Skills installieren:
   - Claude Code: `claude plugin marketplace add heygen-com/hyperframes` und `claude plugin install hyperframes@hyperframes`
   - andere Agenten: `npx hyperframes skills update`
   - In Projekten eine feste Version nutzen: `npx -y hyperframes@0.9.23 init hf --non-interactive`
3. Dieses Kit installieren:
   - Claude Code: `claude plugin marketplace add nikisge/claude-motion-kit` und
     `claude plugin install motion-kit@claude-motion-kit`
   - andere Agenten: `npx skills add nikisge/claude-motion-kit --all` (installiert die 6 Skills aus
     `motion-kit/skills/` in den Skill-Ordner des Agenten)
4. Optional, nur auf Wunsch des Nutzers:
   - **Higgsfield-MCP** (braucht einen bezahlten Higgsfield-Tarif, jede Generierung kostet Credits):
     `claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp`, dann in Claude Code `/mcp` →
     `higgsfield` → Authenticate (Browser-Login). Details: Skill `motion-higgsfield`.
   - **Earshot** (Ton-Prüfung, lädt ~1,1 GB Modelle): Anleitung im [Earshot-README](https://github.com/Leonxlnx/earshot#install).
5. Prüfen: Die Skills `motion-director`, `motion-inspo`, `motion-hyperframes`, `motion-higgsfield`, `motion-3d` und
   `motion-sound` sind verfügbar (bei Claude Code nach einem Neustart der Sitzung).
6. Dem Nutzer kurz sagen, was installiert wurde, und einen Beispiel-Prompt aus „Loslegen“ vorschlagen.

Hinweise: Die Text-Prüfungen in `motion_check.py` nutzen macOS-OCR, auf Linux/Windows laufen nur die Bild- und
Zeitprüfungen. Blender ist optional (Skill `motion-3d`) und wird nur auf ausdrücklichen Wunsch eingerichtet.

## Loslegen

In Claude Code, in einem leeren Arbeitsordner:

```
Mach mir einen 20-Sekunden-Launchfilm für <Produkt>. Nutze motion-director.
Stil: Kinetic Type. Such dir eine Ziel-Referenz auf whatships und miss sie, bevor du baust.
Zeig mir zuerst die Storyboard-Seite.
```

```
Ich will einen 18-Sekunden-Clip im Stil "Doku mit Archivmaterial" über <wahre Geschichte>.
Such gemeinfreies Archivmaterial, zeig mir 2 Richtungen und das Storyboard, bevor du baust.
```

```
Ich habe eine Aufnahme von mir (clip.mp4). Plane einen Clip im Stil "Gestaltete Welt" mit Higgsfield.
Rechne mir vorher die Credits für jeden Shot aus, Entwürfe nur in 480p.
```

```
Prüf diesen Render gegen die Referenz und sag mir ehrlich, wo er schwächer ist.
```

## Was drin ist

| Skill | Schritt | Wofür | Werkzeuge |
|---|---|---|---|
| `motion-director` | alle | Ablauf in 3 Schritten, Brief, Storyboard-Review-Seite, Prüfregeln mit Zahlen, Formate, **Stilkarten**, optionaler Critic | – |
| `motion-inspo` | 1, 3 | Referenzen suchen (whatships, flowjam), laden, zerlegen, messen; Slop-Prüfung | `refs.py`, `sheet.py`, `ref_metrics.py`, `motion_check.py`, `beats.py` |
| `motion-hyperframes` | 2 | Bauen, prüfen, rendern, mastern in HyperFrames; generierte Clips mit Code kombinieren; Fallstricke | `master_10bit.sh` |
| `motion-higgsfield` | 2 | MCP einrichten, welches Higgsfield-Werkzeug wofür, Kosten vorher rechnen, Nähte zwischen Modell und Code | Freigabekarte |
| `motion-3d` | 2 | Echtes 3D in HyperFrames: Produkt (Metall, Glas, Tiefenunschärfe), 3D-Welten mit Modellen aus Bildern und Path Tracing; Blender als Modell-Quelle | `hf3d` (Three.js-Studio), Beispielfilm `rondo` |
| `motion-sound` | 2, 3 | Sound-Design: Cue-Liste, Suchen, Platzieren, Mischen auf −14 LUFS, Prüfen; Stimme; Earshot als externe Prüfung | `sound_index.py`, `sound_search.py`, `sound_place.py`, `sound_verify.py` |

## Ehrliche Grenzen

- Der Agent hört nicht. Ton wird gemessen (auch mit Earshot), entscheiden muss am Ende dein Ohr.
- Ein guter 20-s-Film dauert Stunden, nicht Minuten. „One Shot“ in 5 Minuten ist Marketing.
- Higgsfield kostet Credits, über MCP gibt es keine Gratis-Generierungen. Ohne Higgsfield gehen 7 der 10 Stile
  komplett (die Doku braucht höchstens ein paar Illustrationen); für „Gestaltete Welt“ gibt es keinen Gratis-Ersatz.
- Videomodelle halten Figuren zwischen Takes nicht perfekt gleich, und der Kontaktbogen findet Fehler, die man beim
  Abspielen übersieht.
- Der 3D-Welt-Stil ist als Standbilder und Vorschau getestet, ein fertiger 1080p-Film mit Path Tracing braucht
  Stunden Renderzeit. Der Blender-Teil ist nach Recherche geschrieben, nicht in einem Film getestet.
- Referenzclips gehören ihren Urhebern: nur lokal studieren, nie neu hochladen.

## Lizenz

MIT für Skills und Skripte. Mitgelieferte Fremdteile (Three.js, Schrift Geist) behalten ihre Lizenz, siehe `LICENSE`.

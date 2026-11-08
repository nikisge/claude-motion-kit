# Ressourcen: Skills, Repos, Inspo-Seiten, Higgsfield, Blender

Stand 08.11.2026. Sterne, Lizenz und letzter Push direkt aus der GitHub-API, alle Repos erreichbar und nicht
archiviert. Bewertet nach README, Dateibaum und Lizenz, nicht nach einem Testlauf, außer es steht „getestet“ dabei.
Die Szene ist jung und ändert sich wöchentlich: Ideen übernehmen, nicht blind alles installieren.

## Engine

| Repo | ★ | Lizenz | Was |
|---|---|---|---|
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | 81k | Apache-2.0 | HTML + GSAP + Three.js → MP4, gebaut für Agenten. Eigene Skills, Lint/Check, Registry mit Bausteinen (u. a. `path-traced-3d`). **Getestet** mit 0.9.17, aktuell 0.9.23, Basis dieses Kits |
| [heygen-com/hyperframes-launches](https://github.com/heygen-com/hyperframes-launches) | 663 | Apache-2.0 | Echte HeyGen-Launchfilme als HyperFrames-Code. Timings und Easings lesbar: die beste „so machen es Profis“-Quelle |
| [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | 18k | MIT | Offizielle GSAP-Skills: korrekte API, kein Geschmack |

## Stile (verschiedene Looks)

| Repo | ★ | Lizenz | Was | Urteil |
|---|---|---|---|---|
| [Vincentwei1021/mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15) | 3,3k | MIT | 15 Stile (Flat-Vector, Line-Art, Isometrie, 3D, Collage, Liquid, Bauhaus, Synthwave, Pixel, HUD …), je 10 s, mit komplettem Prompt, Quellcode und Bewertungsrubrik | Bester Stil-Katalog. Eigene Engine, nicht HyperFrames |
| [moritzkremb/framejam](https://github.com/moritzkremb/framejam) | 69 | MIT | 30 Stil-Presets als `style.json` + Poster, HyperFrames-basiert, Stil wählen statt beschreiben | Format für Stilkarten stark, App-Teil noch jung |
| [charlie947/motion-graphics-skills](https://github.com/charlie947/motion-graphics-skills) | 608 | MIT | Skills nach Zweck: Launch, Apple-Keynote-Film, Vox-Erklärer, Charts, 3D-Titel; eine Marken-Datei, die alle Skills lesen | Gutes Muster „Marke → Stil → Skill“ |
| [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy) | 26k | MIT | Isometrische, interaktive Erklärfiguren (Maschinen, Systeme) als SVG | Starker Erklär-Stil, aber keine Video-Engine |
| [nutllwhy/code-brand-film](https://github.com/nutllwhy/code-brand-film) | 195 | MIT | 15-s-Markenfilm in HyperFrames mit drei Prüfskripten (Code, Layout, Frames) | Sauber gebaut, Doku chinesisch |
| [bangtutorial/bang-motion](https://github.com/bangtutorial/bang-motion) | 1,8k | MIT | Openers, Promos, kinetische Typo; „eine durchgehende Welt, keine Folien“ | Gute Anti-Folien-Rahmung |

## Prozess, Regeln, Qualität

| Repo | ★ | Lizenz | Was |
|---|---|---|---|
| [echris6/motion-video-kit](https://github.com/echris6/motion-video-kit) | 1,4k | MIT | Bewegungsgrammatik aus 28 Launchfilmen, unabhängiger Critic, messbare Checks. Beste inhaltliche Basis |
| [howseen-ai/claude-motion-design](https://github.com/howseen-ai/claude-motion-design) | 795 | MIT | Eigene Engine mit Subframe-Motion-Blur (180°-Shutter), Federn, Shared-Element-Übergängen. Motion Blur ist der Hebel gegen den Website-Look |
| [per-simmons/launch-video-clone](https://github.com/per-simmons/launch-video-clone) | 21 | MIT | Referenzclip → Frame-Sheets, Bewegungsspuren, Easing-Kurven; Render gegen Referenz bewerten. Klein, aber genau die Referenz-Methode |
| [Sunwood-ai-labs/hyperframes-motion-reel-skill](https://github.com/Sunwood-ai-labs/hyperframes-motion-reel-skill) | 180 | MIT | Beat-Raster, reine Fade-Ketten verboten, Morph zwischen Szenen |
| [Tejashmakwana/motionmaxxing](https://github.com/Tejashmakwana/motionmaxxing) | 1,4k | Apache-2.0 | Qualitätsstufen gegen Folien-Look (z. B. „keine Eck-Labels, Zähler, Timecodes“). Achtung: Teil eines Produkts des Autors, und der eigene Promo-Clip wirkte im Test eher generisch |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | 55k | MIT | UI-Mikro-Animation (`animation-vocabulary`, `improve-animations`) |

Nicht empfohlen: `JohnHeibel/PDoomVideo` (keine Lizenz), `Miftahul-Islam-Efaz/Motion-graphics-skill` (kommerzielle
Lizenz verbietet Weitergabe), `GTKottman/mortiflix-oss` nur als Prozess-Vorbild (AGPL).

## Higgsfield (generierte Bilder, Videos, 3D)

| Quelle | ★ | Lizenz | Was |
|---|---|---|---|
| [Higgsfield](https://higgsfield.ai) (MCP: `https://mcp.higgsfield.ai/mcp`) | – | Dienst, bezahlt | Genjutsu, Seedance, Kling, Bildmodelle, Bild → 3D, Ton direkt in Claude Code. **Getestet**, Skill `motion-higgsfield` |
| [higgsfield-ai/cli](https://github.com/higgsfield-ai/cli) | 698 | MIT | dieselben Modelle aus dem Terminal, für Skripte |
| [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) | 1,9k | MIT | offizielle Agent-Skills zu den Modellen und Prompts |
| [higgsfield-ai/higgsfield-video-engineer](https://github.com/higgsfield-ai/higgsfield-video-engineer) | 4 | MIT | Filme ganz aus Code mit eigenem WebGPU-Path-Tracer auf der lokalen GPU. Sehr jung, nicht getestet |

## Nachbarn (verlinkt, nicht eingebaut)

Andere Kits mit ähnlichem Ziel. Kein Wettbewerb: jedes setzt einen anderen Schwerpunkt, manche ergänzen dieses Kit
direkt.

| Repo | ★ | Lizenz | Was | Verhältnis zu diesem Kit |
|---|---|---|---|---|
| [Leonxlnx/earshot](https://github.com/Leonxlnx/earshot) | 4,3k | MIT | „Ohren“ für Agenten: Ton analysieren (`critique`, `timeline`, `sheet`), Sounds suchen, CLI und MCP, nur CPU. **Getestet** (v0.4.1) | Ergänzung: `motion-sound` macht den Ton, Earshot prüft ihn. Bewertet Filme mit Sprecher strenger als nötig |
| [Leonxlnx/cinetic](https://github.com/Leonxlnx/cinetic) | 1,1k | MIT | Kinoartige Launchfilme aus Code, vom Agenten geführt | anderer Ansatz für denselben Schritt 2 |
| [Leonxlnx/cook](https://github.com/Leonxlnx/cook) | 41 | MIT | Ziel, Messlatte und Zeit vorgeben, Agent baut, bis es zur Referenz passt | passt zu Schritt 1 + 3 (gegen Referenz bauen) |
| [NiazMorshed2007/reanimate](https://github.com/NiazMorshed2007/reanimate) | 1,4k | MIT | Animation Bild für Bild zerlegen und belegen, dass der Nachbau gleich läuft | gut für Schritt 1 (Bewegung messen). Zum Lernen, nicht zum Kopieren |
| [alchaincyf/huashu-motion](https://github.com/alchaincyf/huashu-motion) | 2,5k | MIT | Produktfilme mit eigener Musik, Änderungen per Zeigen aufs Bild | Ideen für Feedback-Schleife; Doku vor allem chinesisch |

## Inspo-Seiten (Referenzfilme)

| Quelle | Was | Zugriff |
|---|---|---|
| **[whatships.com](https://whatships.com)** | ~2.500 Launchvideos von X, Kategorie Motion, Studios | `refs.py search` (maschinenlesbarer Suchindex) |
| [flowjam.com/library](https://flowjam.com/library) | 55 kuratierte Launchfilme (Slack, Framer, Descript, Jitter …) | `refs.py search` |
| [skillry.dev](https://skillry.dev) / [yihui-dev/awesome-claude-motion-videos](https://github.com/yihui-dev/awesome-claude-motion-videos) (★ 14) | über 100 mit Claude gemachte Motion-Videos von X, mit Original-Post | `data/videos.json` |
| [mikenevermiss/motionpromptgallery](https://github.com/mikenevermiss/motionpromptgallery) (★ 72) | Motion-Clips mit dem Prompt dahinter | `data/items.json` |
| [motionographer.com](https://motionographer.com) | Breakdowns, Profi-Arbeiten | WordPress-API |
| Studio-Vimeos: Buck, ManvsMachine, Ordinary Folk, Giant Ant | Profi-Markenfilme | `vimeo.com/<studio>/videos` |
| Kurzgesagt, Vox | Maßstab für Erklär-Animation | YouTube |
| [Wikimedia Commons](https://commons.wikimedia.org), Bibliotheken, Patent- und Zeitungsarchive | gemeinfreies Archivmaterial für den Doku-Stil | Lizenz je Datei notieren |
| [artofthetitle.com](https://www.artofthetitle.com) | Titelsequenzen, Typo in Bewegung | Feed |
| [60fps.design](https://60fps.design) | UI-Motion-Shots | nur manuell (AGB verbieten Scraping) |

Alle Videos gehören ihren Urhebern: lokal studieren, Grammatik übernehmen, nie neu hochladen.

## Blender mit Claude Code

| Weg | ★ | Lizenz | Was | Stolpersteine |
|---|---|---|---|---|
| [ahujasid/mcp-for-blender](https://github.com/ahujasid/mcp-for-blender) | 34k | MIT | Standardweg: Blender-Addon + MCP, Claude führt Python in Blender aus und sieht Ansichten. `uvx mcp-for-blender setup` | Python-Version bei uv, Addon muss laufen, vorher speichern |
| Blender headless | – | GPL | `blender -b -P skript.py` baut/exportiert ohne Oberfläche, `-a` rendert Bildfolgen | Renderzeiten selbst messen |
| [elithril/blender-kiln](https://github.com/elithril/blender-kiln) | 197 | MIT | Claude-Code-Plugin: Asset beschaffen, bereinigen, texturieren, als GLB exportieren | jung, klein |
| [scenario-labs/blender-plugin](https://github.com/scenario-labs/blender-plugin) | 963 | GPL-3.0 | Blender-5-Erweiterung mit eigenem MCP, KI-Bilder/3D im Viewport | braucht Scenario-Konto und Credits |

Empfehlung: Blender als **Modell-Quelle** (GLB) für HyperFrames/Three.js, nicht als Render-Engine. Siehe Skill
`motion-3d`.

## Sound (frei, kommerziell nutzbar)

Kenney (CC0), OpenGameArt CC0-Pakete, Pixabay über das HyperFrames-Repo, CC0-Musik auf archive.org, echte
Einzelaufnahmen über [Openverse](https://openverse.org) (Lizenz je Datei prüfen). Prüfen statt raten:
[Earshot](https://github.com/Leonxlnx/earshot). Vollständige Liste mit Links und Lizenzhinweisen: `motion-kit/skills/motion-sound/library/LICENSES.md`.

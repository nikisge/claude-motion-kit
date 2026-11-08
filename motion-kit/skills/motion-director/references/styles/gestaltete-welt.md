# Stilkarte: Gestaltete Welt (echtes Video + Videomodell + Code)

**Wann wählen:** Launchfilm, Intro, Showcase oder Kanal-Opener mit Wow-Moment; immer dann, wenn eine echte Aufnahme
(du, ein Raum, ein Produkt in der Hand) in eine gestaltete Welt kippen soll. 10–30 s. Braucht Credits (Skill
`motion-higgsfield`).

**Bildidee:** Der Film beginnt in einer echten Aufnahme. Dann wird das Bild in einem Material neu gezeichnet (Wolle,
Filz, Knete, Papier, Tusche), die Kamera fliegt in eine Welt aus genau diesem Material, und am Ende schreibt die Welt
selbst den Titel. Ein Objekt (ein Faden, ein Licht, ein Tier) läuft als roter Faden durch alle Werkzeuge. An den
Nähten kann der Zuschauer nicht sagen, was gefilmt, generiert oder gebaut ist.

## Leitreferenzen (Grammatik, nie Inhalt)

| Ref | Zeit (ca.) | Was passiert | Übernehmen |
|---|---|---|---|
| [a-ha, „Take On Me“ (1985)](https://www.youtube.com/watch?v=djV11Xbc914) | ca. 0:50–1:10 | eine Hand zieht die Person aus der echten Welt in die gezeichnete | **Übergang echt → gezeichnet als Geste** |
| [Higgsfield, Tusche-Clip](https://x.com/higgsfield_ai/status/2111523780598419923) | ganz, Wolke ab ~0:08 | ein Wesen, eine Reise, eine Wolke schluckt alles, dann bricht Licht durch | **eine Figur, eine Reise, Stille in der Wolke** |
| Higgsfields eigene Genjutsu-Vorschauen (higgsfield.ai) | – | echt und neu gezeichnet im selben Bild | die Split-Naht; **nicht** den Look (taghelle Pastell-Spielzeugwelt) |

## Messwerte und Zielwerte

- Eine Fahrt, vier Werkzeug-Nähte, keine Überblendung. 15–18 s reichen.
- Spannungskurve auf einem Takt-Raster (z. B. 100 BPM, Takt 2,4 s): Haken bis 2,4 s, Zug, **0,8 s Atem in Stille**,
  Treffer auf dem Downbeat, Ausklang.
- Ton bei einem gelungenen Film (Earshot `critique`): launch-grade, −14,5 LUFS, Stille-Einbruch 0,45 s vor dem
  Treffer, Ton-Einsatz an jedem Schnitt innerhalb eines Frames.
- Kosten: rund 260 Credits für Genjutsu + drei Seedance-Takes inklusive verworfener Tests (Stand 11/2026).

## Startwerte

- **Material:** eines für die ganze Welt (auch die Schrift ist daraus). Am besten aus der echten Aufnahme abgeleitet
  (Strickpulli → Wolle, Holztisch → Schnitzwerk), dann ist es nicht ausgedacht.
- **Licht:** das Licht der echten Aufnahme übernehmen (z. B. warmes Abendlicht), nicht das Standardlicht des Modells.
- **Farbe:** gedeckte Materialfarben (Creme, Hafer, Kamel) und **genau eine** Akzentfarbe für den roten Faden.
- **Kamera:** Code-Push auf der echten Aufnahme, dann die Kamera der Modell-Clips, Code-Parallaxe darüber.
- **Typo:** im Material gestickt, gemalt oder gelegt, entlang des roten Fadens. Lesbar auf Handygröße prüfen.

## Werkzeug je Abschnitt

| Abschnitt | Werkzeug |
|---|---|
| Haken in echter Aufnahme + Leitobjekt | Rohmaterial + Code (Objekt auf eine Körperstelle getrackt, vor der Generierung eingerechnet) |
| Verwandlung | Genjutsu auf derselben Quellzeit + Code-Maske (Wipe Reihe für Reihe, Kante im Material) |
| Reise | Seedance-Takes mit Start-/Endbild und Figurenreferenz, Entwurf in 480p, dann Upscale |
| Atem | Code-Zeitrampe auf dem Modell-Clip, Ton weg |
| Treffer + Titel | Modell-Clip + Code-Titel im Material |

## Sound-Charakter

Jedes Bildereignis hat seinen Ton aus dem Material der Welt (Nadelklick, Woll-Wumms, Flügelschlag aus Filz, Watte),
framegenau, mit steigender Tonhöhe bei Reihen. Musik führt auf dem Raster, bricht vor dem Treffer hart ab, kommt auf
dem Downbeat zurück. Je Buchstabe des Titels ein kurzes Material-Geräusch.

## Signature Moves (Bauweise)

1. **Material-Wipe:** das echte Bild verwandelt sich diagonal Reihe für Reihe (2 Frames je Reihe), die Front als
   Material-Kante mit Schatten, Tonhöhe steigt mit.
2. **Leitobjekt wird Figur:** der Faden knotet sich zum Tier, das Licht wird zum Vogel (Seedance mit Start = letztes
   Genjutsu-Bild).
3. **Rahmen wird Fenster:** ein Bild an der Wand im echten Raum ist das Tor in die Welt, die Kamera fliegt hindurch.
4. **Stille in der Wolke:** weiß-weiche Fläche, Zeitlupe, ein einzelner leiser Klick, dann der Durchbruch.
5. **Die Welt schreibt den Titel:** das Leitobjekt zieht die Buchstaben im Material, dann wird es abgeschnitten.
6. **Ende ist ein Bild, das noch etwas tut** (Figur fliegt weiter, dreht kurz den Kopf), keine Endkarte.

## Slop-Fallen

- Der Look von Higgsfields Vorschau (Standardwerte, kein eigener Prompt, keine eigene Farbwelt).
- Videomodell für Wirklichkeit (fotorealistische Menschen, Orte, Produkte): wirkt billig und unheimlich.
- Überblendung zwischen zwei Modell-Clips: Doppelbelichtung. Harter Schnitt im Bewegungs-Blur.
- Figur ändert sich zwischen den Takes; Stützen unter fliegenden Dingen; Pseudo-Schrift; Gesichter in Wolken.
- Titel als Banner über allem statt in der Welt verankert.
- Zu niedlich für das Publikum: Tempo hilft, die Verwandlung muss in ~1,2 s sitzen, nicht in 3.
- Fremde Logos im echten Material (Kleidung, Geräte): Ausschnitt wählen oder weichzeichnen.

## Variationen

- **Wolle/Filz** · **Tusche/Papier** · **Knete/Stop-Motion** · **Spielzeug-CGI**: jeweils eigenes Material, eigene
  Foley-Familie.
- Ohne eigene Aufnahme: Start im Code (Animatic) statt im echten Video. Code-Animatic → Genjutsu ist ungetestet.

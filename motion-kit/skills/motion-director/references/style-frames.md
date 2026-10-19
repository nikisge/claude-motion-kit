# Style Frames: das Aussehen festlegen, bevor sich etwas bewegt

Ein Style Frame ist ein **fertig gestaltetes Standbild in voller Auflösung** aus dem späteren Film: echte Typo,
echte Farben, echte Assets, Licht, Korn. Kein Moodboard, keine Skizze, kein Bild-KI-Entwurf. Wirkt ein Style
Frame wie eine Folie, ist die Einstellung falsch, nicht die spätere Animation.

## Welche drei

| Situation | Die drei Frames |
|---|---|
| Stil steht (Normalfall) | **Hook** (erstes starkes Bild) · **Herzstück** (der eine Gedanke) · **Endkarte** |
| Richtung offen, Nutzer soll wählen | dasselbe Schlüsselbild in **2–3 Richtungen** (z. B. Clean-SaaS hell vs. Apple dunkel vs. Skizze), danach 3 Frames der gewählten |
| One-Shot / Showcase | Hook · Herzstück · Endkarte, plus ein Frame des „Staun-Moments", falls es ein anderer ist |

## So entstehen sie

1. **Im Ziel-Werkzeug bauen**, nicht in einem Zeichenprogramm: HyperFrames-Szene mit fester Zeit und
   `npx hyperframes snapshot --at <t> --describe false` (`motion-hyperframes`; 3D über Skill `motion-3d`).
   So wird aus dem Style Frame später direkt die Szene.
2. **Asset-Bogen zuerst**: jede Ebene (UI-Screenshot, Logo, Typo-PNG) einmal 1:1 auf dem
   Hintergrund ansehen, bevor sie in einen Frame oder eine Animation geht. Prüfen: leere Masken/Icons
   (CSS-`mask-image` mit Dateipfad bleibt in Headless-Chromium leer), abgeschnittene Schatten (Rand ≥
   Versatz + Weichzeichnung), richtige Schrift geladen (HTML per Datei öffnen, nicht `set_content`).
3. **Markenfarbe messen**: Pixelwert der Logo-Datei gegen die Spezifikation. Weichen sie ab, gilt die Datei
   fürs Logo; Akzente in Logonähe an die Datei angleichen, Abweichung im Brief notieren.
4. **Neben die Referenzen legen:** Style Frame und 2–3 Referenzbilder der gewählten Stilkarte als ein Bogen. Frage:
   Spielt das in derselben Liga (Tiefe, Licht, Typo-Größe, Weißraum)? Wo ist es flacher?
5. **Regeln prüfen** (`rules.md`): Typo-Größen, Kontrast ≥ 4,5:1, Sicherheitsrand 8–10 %, höchstens 2 Schriften,
   Werte vor Farbe (Graustufen-Probe: ist das Hauptobjekt auch in Grau das hellste/dunkelste?).

## Abgabe

`projects/<name>/check/style-frames.jpg` (alle Frames + Referenzen auf einem Bogen, mit Zeitstempel/Szene) und je
Frame eine PNG in voller Auflösung. Im Standardprozess: der Nutzer gibt frei. Im One-Shot-Modus: gehen in Critic-
Durchgang 1.

## Typische Fehler

- Style Frame zeigt den ruhigsten Moment statt des stärksten.
- Drei Frames, drei verschiedene Filme (kein roter Faden in Farbe, Licht, Objekt).
- Platzhalter-Text („Lorem", erfundene Daten) im Frame: Kundendaten sind echt oder es gibt keinen Frame.
- Mehr als eine laute Sache pro Frame.

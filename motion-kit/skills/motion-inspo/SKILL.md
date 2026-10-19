---
name: motion-inspo
description: Use when a motion graphics piece needs references or inspiration (launch videos, styles, camera moves), when a reference clip should be downloaded, studied or measured, or when a render is to be compared against a reference or checked for slide/slop patterns. Trigger words: Inspo, Referenz, whatships, Launchvideo-Beispiele, Stil finden, ref_metrics, motion_check, Kontaktbogen.
---

# Motion Inspo: Referenzen finden, zerlegen, messen

Gute Motion Graphics entstehen nicht aus Beschreibungen, sondern aus **konkreten Vorbildern**. Dieser Skill findet
Referenzfilme, lädt sie zum Studieren, zerlegt sie in Einzelbilder und misst sie. Mit denselben Messungen prüfst du
später deinen eigenen Render.

**Rechte:** Referenzclips gehören ihren Urhebern. Nur lokal studieren, nie neu hochladen, nie ins Repo
(`refs/clips/` gehört in `.gitignore`). Übernommen wird **Grammatik** (Tempo, Übergänge, Kamera), nie Inhalt.

Alle Skripte liegen in `scripts/` dieses Skills. Sie schreiben in `refs/` im aktuellen Arbeitsordner
(oder in `$MOTION_REFS_ROOT`). Voraussetzungen: `python3`, `ffmpeg`, `uv` (für Skripte mit Abhängigkeiten).

## Quellen

1. **`references/referenzfilme.md`**: 50 bewertete Referenzfilme nach Stil (Clean SaaS, Premium-Produkt, Kinetische
   Typo, 3D-Objekt, Erklärfilm, Editorial/Collage, Cinematic Dark), inklusive Anti-Referenzen.
2. **whatships.com** (~2.500 Launchvideos von X) und **flowjam.com/library** (55 kuratierte Launchfilme), über
   `refs.py search`.
3. Weitere Seiten und Datensätze: `RESOURCES.md` im Repo-Hauptordner.

## Befehle

```bash
python3 scripts/refs.py search product launch 3d keyboard --n 15   # whatships + flowjam durchsuchen
python3 scripts/refs.py get <x.com-status | whatships | youtube | vimeo-url> --name <slug>   # nach refs/clips/
python3 scripts/refs.py study <slug> --every 0.5                    # Einzelbilder, Bogen, Schnitte, Tempo -> refs/study/<slug>/
python3 scripts/sheet.py <video.mp4> <out-prefix> --every 0.25      # Kontaktbogen mit Zeitstempeln (4 Bilder/s)
uv run scripts/ref_metrics.py <ref.mp4> --no-ocr                    # Ziel-Referenz messen
uv run scripts/ref_metrics.py render.mp4 --ref <ref.mp4> --out check/metrics   # eigener Render gegen Referenz
uv run scripts/motion_check.py render.mp4 [--script sprechtext.txt]           # Folien-/Slop-Muster finden
uv run scripts/beats.py track.mp3 --fps 30 --out beats.json         # Beat-Raster aus der Musik
```

Suchbegriffe englisch und nach **Bewegung** statt Branche: „camera dives into ui“, „kinetic type scale jump“,
„object becomes logo“, „paper collage top down“.

## Was die Messungen bedeuten

`ref_metrics.py` misst: Schnitte und neue Ansichten je 10 s, Einstellungslängen, Anteil „Kamera steht“, Bildänderung
je Bild, leere Strecken, Textanteil, Helligkeit/Kontrast/Sättigung und den Einstieg (erste 2 s). Daraus werden Ziele:
Dichte ≥ 80 % der Referenz, „Kamera steht“ ≤ Referenz + 15 Punkte, Einstieg bewegt sich ≥ 80 % der Referenz.

Wichtigste Lehre aus den Messungen: Gefühlte Dichte („jede Sekunde ein neues Bild“) kommt meist aus **schnellen
Kamerafahrten und Materialwechseln**, nicht aus vielen Schnitten. Ein gemessener 3D-Produktfilm hatte nur 4,3 Schnitte
je 10 s, aber die Kamera stand nur 14 % der Zeit.

`motion_check.py` findet bekannte Slop-Formen: Überschrift oben links + Bild darunter (Folie), Sätze, die stillstehen,
Text, der den Sprechtext wiederholt (Echo), eingefrorene Zeit, zu lange Einstellungen, Textwände, Kachelraster.
Bestanden heißt nur „keine bekannte Slop-Form“. Ob es gut ist, entscheidet der Blick auf die Bilder.
Schwellen je Stil: `motion-director/references/rules.md`. Die Text-Prüfungen nutzen macOS-OCR (`ocrmac`); auf anderen
Systemen laufen nur die Bild- und Zeitprüfungen.

## Zerlegen (je Referenz ≤ 10 Zeilen)

Ablauf und Vorlage: `motion-director/references/inspiration.md`. Kurz: Bogen mit 4 Bildern/s ansehen, je Einstellung
Zeit, Einstellungsgröße, Kamera, was passiert, Material/Licht, Übergang. Dann „Nehmen wir“ / „Nehmen wir nicht“.

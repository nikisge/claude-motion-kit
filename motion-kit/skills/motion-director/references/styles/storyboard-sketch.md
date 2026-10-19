# Stilkarte: Storyboard / Skizze (Sachen hinlegen, Prozess erzählen)

**Wann wählen:** Gründer-/Ursprungsgeschichte, Prozess oder Pipeline erklären („erst A, dann B, dann C"), Behind the
Scenes, Workflow eines Agenten. Leitfilme: simi-launch (Sachen hinlegen, Geschichte erzählen) und
higgsfield-motion-pipeline (Pipeline als Erklärfluss).

**Bildidee:** Eine Arbeitsfläche von oben (Tisch, Schneidematte, Papier). Dinge werden **hingelegt**: Fotos, Zettel,
Stempel, Karten, Etiketten. Die Kamera fährt in ein Ding hinein, und es wird zur nächsten Szene. Prozess-Schritte
erscheinen als kleine Status-Karten, deren Ergebnis sich danach sichtbar baut.

## Leitreferenzen (Grammatik, nie Inhalt)

| Ref | Zeit | Was passiert | Übernehmen |
|---|---|---|---|
| simi-launch | 0:00–0:03 | Draufsicht: grüne Schneidematte, Papierbogen, Hände legen ein Foto ab, Weltkarte daneben | **Draufsicht + Ablegen** als Grundbewegung |
| | 0:02–0:04 | Länder-Ausschnitt, Briefmarke, zweites Foto werden aufs Papier gelegt; Untertitel klein unten | Collage wächst Stück für Stück zur Aussage |
| | 0:04–0:07 | Logo-Etiketten (Uni, Investor) werden wie Sticker aufgeklebt | Namen als **physische Etiketten** |
| | 0:08–0:11 | Push in die Weltkarte, Flugbogen zeichnet sich zwischen Stecknadeln, Etiketten reisen mit | **Kamera taucht ins Papier**, Linie erzählt Reise |
| | 0:27–0:29 | helles Rasterpapier, „LLMs … arrived": Raster aus Kacheln füllt sich mit Bildern, ein blaues Quadrat bleibt | Raster-Kacheln als Zähl-/Mengen-Bild |
| higgsfield-motion-pipeline | 0:13–0:19 | Pixel-Maskottchen neben realer Figur, Fragen schweben („Objects? Shapes? VFX?"), Code-Zeilen | Figur + Gedankenblasen = innerer Prozess |
| | 0:19–0:21 | Prompt-Leiste unten tippt „I need a promo. Fast." | **echte UI-Zeile als Auslöser** |
| | 0:22–0:23 | weißes Feld, ein Satz mit Spinner-Stern: „Promo brief received. Starting with the reserve logo." | **Status-Karte** = Schritt im Prozess |
| | 0:23–0:28 | Logo baut sich: grüner Kreis, Zacken-Rand, Figur, Sprechblase | Ergebnis des Schritts entsteht sofort |
| | 0:55–0:60 | grünes Strahlen-Poster: Bild mit Sticker-Rand, große Versal-Titel, Bild-Kacheln reihen sich | Schritt-Ergebnisse sammeln sich zum Endprodukt |

## Messwerte (motion_check 11.10.2026)

| | Wechsel/10 s | Median-Einstellung | längste | harte Schnitte |
|---|---|---|---|---|
| simi-launch | 4,7 | 1,4 s | 10,5 s (Interview) | 22 in 60 s |
| higgsfield-motion-pipeline | 5,9 | 1,4 s | 4,5 s | 16 in 73 s |

- Ablege-Bewegung 0,4–0,7 s mit Überschwingen in der Rotation (±3–6°), danach liegt das Ding still (Papier bewegt
  sich nicht von selbst; Leben kommt von der Kamera-Drift 1–2 %).
- Status-Karte: 1 Satz, 6–10 Wörter, 1,2–2 s sichtbar, Text tippt mit 25–35 ms/Zeichen.
- Untertitel/Beschriftung klein (28–34 px @1080p), unten mittig oder als Etikett am Objekt.

## Startwerte

- **Farbe:** Schneidematten-Grün #2F6B57 oder Holz #B98A5E als Fläche, Papier #F3EEE4 / Kraft #D8C3A0, Tinte #222,
  Akzent Rot #D9412B (Stecknadel, Stempel). Prozess-Variante: Weiß #FFFFFF + Marken-Grün #1F7A3E + Gelb #F5C542.
- **Typo:** Schreibmaschine/Mono für Etiketten (IBM Plex Mono), Grotesk für Status-Karten (Inter 500), Versal-Display
  für Endtitel (Anton, Archivo Black). Handschrift nur für Notizen am Rand.
- **Komposition:** Draufsicht, Papier füllt 60–80 % des Bildes, Objekte leicht schief (±2–8°), weiche Kontaktschatten
  (y 6–14 px, blur 18–30 px, 25 % Schwarz).
- **Kamera:** Draufsicht mit Drift; Push-in in ein Objekt 1,0–1,4 s `power2.inOut`; nie kippen (bleibt flach).
- **Übergänge:** Push-in ins Papier (Karte, Foto, Bildschirm), Papier wird weggezogen (Wipe durch die Hand-Bewegung),
  Status-Karte → Ergebnis.
- **Easing:** Ablegen = `back.out(1.4)` auf Position + Feder auf Rotation; Aufkleben = Scale 1.08 → 1 in 0,2 s.

## Sound-Charakter

Foley von Papier und Tisch: Papier gleitet, Foto klatscht leise, Sticker zieht ab, Stempel-Schlag, Stift kratzt.
Für Prozess-Schritte: weicher UI-Ping je Status-Karte, Tippen nur bei sichtbarem Tippen. Musik warm, akustisch oder
Lo-Fi 80–100 BPM, leise (Foley ist der Star).

## Signature Moves (Bauweise)

1. **Ablegen mit Schatten:** Element startet 8 % größer, 120 px versetzt, Rotation +6°, Schatten weit und blass;
   landet in 0,5 s (`back.out`), Schatten zieht sich zusammen (Höhe → 0). Optional Hand: freigestellte PNG-Hand
   (eigene Aufnahme/Freigabe) fährt mit und wieder raus.
2. **Push ins Papier:** Kamera-Wrapper skaliert auf Zielobjekt (Karte), unterwegs Papierstruktur sichtbar (Grain +
   Papier-Textur als `background-image`, eigene Fotografie oder prozedural über `feTurbulence`).
3. **Flugbogen zwischen Nadeln:** SVG-Quadratkurve, `stroke-dashoffset` 0,8 s, Etikett läuft auf dem Pfad
   (`getPointAtLength` aus t), Nadeln poppen 0,15 s vorher.
4. **Status-Karte:** weißes Feld (oder Karte auf Papier), Spinner-Stern dreht 180°/s, Satz tippt; bei „fertig"
   wird der Stern zum Haken (Morph 0,3 s) und das Ergebnis schiebt sich darunter ins Bild.
5. **Sticker aufkleben:** Ecke kommt mit `rotateY 40° → 0` (CSS-3D, perspective 900), kurzer Glanzstreifen.
6. **Kachel-Raster füllt sich:** 3×3 Kacheln, Bilder klappen mit Stagger 50 ms auf, eine Kachel bleibt als Farbfläche
   und wird zum nächsten Objekt (Match).

## Slop-Fallen

- Clip-Art-Collage ohne Geschichte (alles liegt rum, nichts passiert).
- Gleichmäßig verteilte Objekte im Raster. Hinlegen ist unordentlich und bewusst komponiert.
- Status-Karten ohne sichtbares Ergebnis danach (dann ist es eine Folie mit Ladekreis).
- Echte Logos/Marken Dritter als Sticker ohne Recht dazu. Eigene oder Kunden-Marken.
- Papier-Textur als flaches Filter-Overlay über alles statt als Material der Dinge.

## Variationen

- **Schreibtisch-Collage** (simi) · **Prozess mit Status-Karten** (higgsfield) · **Rasterpapier-Diagramm** (simi 0:27).
- Mischen: Whiteboard-Erklärer (Skizzen statt Fotos) oder Kinetic Type für den Hook.
- Eigenes: der eigene Schreibtisch abfotografiert als Bühne, eigene Zettel/Handschrift als Objekte.

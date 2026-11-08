# Stilkarte: Doku mit Archivmaterial

**Wann wählen:** eine wahre Geschichte erzählen (Person, Ereignis, Erfindung, Firmengeschichte), Rückblick, „wie es
dazu kam“. Erzählerstimme trägt, 15–90 s, auch als Kapitel in einem YouTube-Video. Nicht für Produkt-Features.

**Bildidee:** Echtes Material liegt auf einem Tisch: eine historische Karte, Fotoabzüge, Dokumente, Ausschnitte. Die
Kamera fährt ohne Schnitt durch diese Welt, schräg im Raum mit Tiefenschärfe. Ein roter Faden (eine Tintenlinie, eine
Route, ein Faden) verbindet alles und trägt jeden Übergang. Das Licht erzählt die Zeit.

## Leitreferenzen (Grammatik, nie Inhalt)

| Ref | Zeit (ca.) | Was passiert | Übernehmen |
|---|---|---|---|
| [Zane Hoyer, Doku-Intro](https://youtu.be/e2Fykz51Nxg) | 0:02–0:05 | ein Fotoabzug steigt aus der dunklen Karte, Push-in | Material steht im Raum auf statt einzublenden |
| | 0:05–0:09 | Kamera gleitet vom Porträt zum nächsten Objekt | **eine Fahrt statt Schnitte** |
| | 0:08–0:13 | Fahrt über die Karte zum nächsten Ort | Karte als Rückgrat der Geschichte |
| | 0:18–0:24 | Musik fällt ~4 s vor dem Treffer ab, Stimme setzt 1 s aus, Höhen-Swell 0,9 s vorher, Treffer framegenau mit 0,2 s Ruck | **Stille vor dem Treffer** |
| | 0:31–0:33 | ein Sound pro Wort | Ton-Ereignis je Bildereignis |
| [Simplicissimus, „Die größte Tragödie in der Mathematik“](https://youtu.be/CDXIZqPA_aA) | 0:09, 0:14–0:17 | nur Ton: Papier-Whoosh, als etwas fliegt; Musikbett baut auf und wird unter der Erzählung leiser | Bett-Dynamik unter der Stimme |

Anders als die Referenz: keine großen Jahreszahlen als Titel, keine dunkle Datenkarte, keine Signatur-Moves 1:1
(z. B. der Stempel als Treffer). Ein eigener Treffer gehört zur eigenen Geschichte.

## Messwerte

| | Schnitte/10 s | neue Ansichten/10 s | längste Einstellung | Kamera steht |
|---|---|---|---|---|
| Zane-Doku (40-s-Ausschnitt, `ref_metrics`) | 1,24 | 3,46 | 22 s | 20 % |

- Dichte kommt aus der Fahrt, nicht aus Schnitten: alle 2–3 s ein neues Ziel, dazwischen keine Standbilder.
- Ton: etwa alle 1,5–2,5 s ein Ereignis. 15–20 Ereignisse auf 18 s reichen, 27 waren zu dicht.
- Lesezeit: ein Wort in einer Quelle (Kringel) braucht ≥ 1,5 s Ruhe.

## Startwerte

- **Material:** echte, gemeinfreie Quellen (Wikimedia Commons, Bibliotheken, Patent- und Zeitungsarchive). Lizenz je
  Datei in eine Tabelle. **Keine KI-Bilder echter Personen**, keine KI-„Archivfotos“. Fehlende Gegenstände als
  Holzstich- oder Papier-Ausschnitt (Bildmodell, freigestellt) im Stil der Zeit, klar als Illustration erkennbar.
- **Farbe:** warmes Papier (#efe6d2) auf dunklem Holz, die Karte per Lab-Umfärbung nach Sepia ziehen, damit ihre
  eigenen Farben nicht mit dem Akzent konkurrieren. **Eine** Akzentfarbe (Tintenrot #b3241c), nur für den roten Faden.
- **Licht als Uhr:** Grading über den Film (Dämmerung #4a6788 → Tag #f2dfba → Abend #d0844f → fast dunkel → Lampe).
- **Typo:** Serif der Zeit (z. B. EB Garamond), höchstens ein Ortsetikett und eine Zahl. Kein Text wiederholt die Stimme.
- **Kamera:** eine durchgehende Fahrt, Neigung 14–64°, Tiefenschärfe oben und unten, Kranfahrt nach oben für den
  Überblick, kleine Erschütterung nur auf Treffern. Bewegungsunschärfe nur bei Reißschwenks.
- **Stimme:** ruhig, eher tief, ganze erzählende Sätze. Die Stimme bestimmt die Bildzeiten.

## Sound-Charakter

Raumton (Nacht, Uhr nur wenn hörbar), Papier, Feder auf Papier (echte Aufnahme, nicht generiert), Glas, Holz.
Musik: Drone, darüber ein Ostinato, das mit jeder Station steigt, hart abbricht, dann 1 s nur Feder und Atem, dann der
Treffer allein (Schlag + Akkord), danach warmer Ausklang deutlich unter der Stimme. Treffer 3–4 dB über der lautesten
Stimmstelle (`motion-sound`, „Treffer gegen Stimme messen“).

## Signature Moves (Bauweise)

1. **Das Objekt zieht die Linie:** ein Fotoabzug oder Gegenstand gleitet wie ein Schlitten über die Karte und
   hinterlässt den roten Faden (SVG-Pfad mit wachsender Länge, Tinte saugt sich mit Turbulenz-Filter ins Papier).
2. **Die Linie stockt, wenn etwas schiefgeht:** Feder wird trocken und blass, bis die Lösung im Bild liegt.
3. **Kringel auf einem echten Wort in einer echten Quelle:** das Wort per OCR im Scan finden, nicht nachsetzen.
4. **Pop-up-Ausschnitte:** Illustrationen mit Papierrand und weichem Schatten stehen im Raum auf und bleiben liegen.
5. **Licht ist die Uhrzeit:** ein Tag in einer Einstellung, Fensterlicht wandert über ein Gesicht.
6. **Klammer:** Anfang und Ende spiegeln sich (dunkel → dunkel, Abfahrt → Rückkehr).
7. **Schlusscollage:** Kranfahrt nach oben, die ganze Reise liegt entlang der Linie.

## Slop-Fallen

- KI-Reenactment-Szenen und KI-„Archivfotos“: wirken billig und machen den Film nicht epischer.
- Telegrammstil („Panne? Werkstatt.“): ohne Vorwissen unverständlich.
- Geflüsterte oder verschwörerische Sprecher-Regie: klingt schnell anzüglich. Spannung über Pausen und Musik.
- Die Karte erschlägt alles (zu viele Farben, Akzent geht unter). Rote Flecken lesen sich als Blut: Tinte rund ins
  Papier saugen lassen, keine Spritzer.
- Signatur der Referenz übernehmen (Stempel, Jahreszahl-Titel): das ist Nachbau, kein Stil.
- Zu dichter Ton, Whoosh auf jeder Fahrt, Treffer leiser als die Stimme.
- Unbelegte Aussagen. Jede Aussage im Film braucht einen Beleg; was nicht überliefert ist, wird nicht behauptet.

## Variationen

- **Tischkarte** (Standard) · **Zeitungsarchiv** (Schlagzeilen als Ausschnitte) · **Firmengeschichte** (eigene alte
  Fotos und Dokumente statt Karte).
- Mischen: Whiteboard-Erklärer für eine Mechanik mitten in der Doku, als eigenes Kapitel mit eigenem Bildraum.

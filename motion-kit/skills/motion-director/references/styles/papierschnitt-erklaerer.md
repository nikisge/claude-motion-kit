# Stilkarte: Papierschnitt-Erklärer (Maßstabsreise)

**Wann wählen:** erklären, was im Hintergrund passiert, wenn etwas Alltägliches passiert („was passiert, wenn …“,
„wohin geht …“, „wie groß ist …“). Eine Reise durch Maßstäbe mit Anfang, Mitte und Ende, 15–60 s, mit Sprecher. Für
reine Abläufe neben der Kamera ist der [whiteboard-explainer](whiteboard-explainer.md) schneller.

**Bildidee:** Wir folgen einem einzigen warmen Element (Lichtpunkt, Nachricht, Tropfen) durch eine kalte Welt aus
Papier. Die Kamera fährt in einer Bewegung durch verschachtelte Welten: jede liegt sichtbar in der vorigen
(Zimmer im Haus, Haus auf dem Planeten, Gerät im Gebäude, Bauteil im Gerät). Am Ende kehrt das Element dorthin
zurück, wo es angefangen hat, und das erste Bild beantwortet sich selbst.

## Leitreferenzen (Prinzipien, keine Bilder)

| Ref | Zeit | Was passiert | Übernehmen |
|---|---|---|---|
| [Kurzgesagt, „AI Slop Is Destroying The Internet“](https://www.youtube.com/watch?v=_zfN9wnPvU0) | 0:15–0:19 | leuchtender Globus auf Violett | **kalte Welt, ein warmer Akzent** |
| | 2:01–2:08 | ein Lichtpunkt glüht in violetter Nacht, dann strahlt er warm über die Landschaft | **das warme Element beleuchtet seine Umgebung** |
| | 3:28–3:32 | Planetenrand von oben, leuchtende Linie zieht über die Krümmung | Maßstab durch Rückfahrt bis zum Planeten |
| | 4:13–4:16 | Figur am Laptop: runde Formen, zwei Töne je Fläche, Licht vom Bildschirm | Figuren aus Flächen ohne Konturen |
| | 6:36–6:41 | Kamera taucht über leuchtende Regalreihen hinab, Parallaxe | Hineinfahrt mit Tiefe |
| `kurzgesagt-civilization` (`referenzfilme.md`) | 0:08–0:18 | Kamera zieht weg, das Ziel schrumpft zum Punkt | Maßstabssprung als Erklärung |

Nachbauen, nie Clips oder Figuren übernehmen. Der eigene Dreh (hier: Papier) macht es zum eigenen Stil.

## Zielwerte

- Eine Kamera, keine Überblendung: jeder Übergang ist ein Maßstabssprung (logarithmischer Zoom mit Drehpunkt).
- Spannungskurve: Haken (Frage + Auslöser) ≤ 2,5 s, Sog durch 4–5 Maßstäbe, **0,7 s echte Stille** (im Mix unter
  −65 dB gemessen), Treffer, schnelle Rückfahrt, Ankunft.
- Das Treffer-Wort ist das größte und kontrastreichste Bild des Films.
- Musik 16–18 dB unter der Stimme.

## Startwerte

- **Farbe:** kalte Welt (Violett, Blau, Türkis), warm ist **nur** das Element, dem wir folgen, und was es berührt.
  Das Auge folgt automatisch dem einzigen warmen Ding.
- **Form:** runde Flächen ohne Konturen, zwei Töne je Fläche, Glühen statt Linien.
- **Papier:** jede Ebene ist ein Blatt mit Faserkorn, unruhiger Schnittkante (SVG-Turbulenz), heller Lichtkante oben
  und weichem Schatten auf die Ebene darunter. Filterwerte mit 1/Zoom skalieren, sonst werden Kante und Faser bei
  jedem Maßstab anders. Faser aus 1–2 Papierplatten (Bildmodell oder Scan, nahtlos gekachelt).
- **Typo:** eine Grotesk (z. B. Geist), Etiketten mit einem Wort am Objekt. Keine Karten, Kacheln, Nummern.
- **Figur:** einfach, über die Schulter; reagiert am Ende (Kopfdrehung ins Licht).

## Sound-Charakter

Musik trägt leise und kommt auf dem Takt nach der Stille zurück. Vier Familien: weiche Tasten- und UI-Klicks; Glas
und Licht (nur am warmen Element); Luft (nur bei den großen Sprüngen, Spitze an der schnellsten Stelle, Beginn vor der
Bewegung); tiefe Maschine (Lüfter, Surren, Tiefton unter dem Treffer und dem großen Reveal). Earshot meldete ohne
Tiefton einen „dünnen Boden“.

## Signature Moves (Bauweise)

1. **Verschachtelte Welten:** jede Welt ist ein Fenster in der vorigen (Zimmer = Fenster im Haus-Querschnitt). Die
   Kamera zoomt durch, statt zu blenden.
2. **Querschnitt:** Haus, Gebäude, Gerät, Bauteil von der Seite aufgeschnitten, damit man sieht, was drin passiert.
3. **Welle durch Schichten:** ein Vorgang als Lichtwelle, die durch gestapelte Papierstreifen läuft.
4. **Stück für Stück:** das Ergebnis entsteht in Teilen, jedes Teil schneller als das vorige, jedes reist sofort los.
5. **Ende spiegelt den Anfang:** derselbe Ort, jetzt mit Antwort; die Figur dreht sich ins warme Licht.
6. **Eigene Bewegungsunschärfe** bei den Sprüngen (hohe fps rendern und mitteln, `motion-hyperframes`).

## Slop-Fallen

- Kurzgesagt-Kopie: Figuren, Vögel, Farben 1:1. Ohne eigenen Dreh ist es ein Vektor-Klon.
- Überblendungen zwischen Ebenen statt Maßstabssprung: man sieht kurz zwei Bilder übereinander.
- Mehrere Stile gemischt (Whiteboard + Kurzgesagt + Doku): „wild zusammengewürfelt“.
- Dekoration statt Erklärung (Leiterbahn-Muster, das nichts zeigt).
- Fachlich ungenaue Metapher: erst Faktencheck, dann Grafik. Eine Grafik darf keine falsche Aussage verstärken.
- Text, der die Stimme wiederholt.

## Variationen

- **Papierschnitt** (Standard) · **Pappe/Cardboard** (gröbere Kanten, Wellpappe) · **Scherenschnitt** (Silhouetten
  im Gegenlicht).
- Mischen: Whiteboard-Skizze für eine Detailstelle, als eigenes Kapitel.

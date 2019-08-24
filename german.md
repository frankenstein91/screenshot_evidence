# Digitale Screenshots mit Echtheitsnachweis

<table border="0"><tr>  <td><a href="https://gittron.me/bots/0xf5fecdad30cae3a9f8664ef783b20e84"><img src="https://s3.amazonaws.com/od-flat-svg/0xf5fecdad30cae3a9f8664ef783b20e84.png" alt="gittron" width="50"/></a></td><td><a href="https://gittron.me/bots/0xf5fecdad30cae3a9f8664ef783b20e84">SUPPORT US WITH GITTRON</a></td></tr></table>

## Autoren
* Menzel, Erik
* Tornack, Frank <linux@dreamofjapan.de>
* Lehner, Tim

## Einleitung
Es ist heutzutage kein Problem, das aktuelle Bild eines oder mehrerer Bildschirme zu speichern. 
Ein Bildschrimfoto zu erstellen ist heutzutage nahezu selbstverständlich. Häufig werden Bildschrimfotos genutzt, 
um zu dokumentieren wann was getan wurde, zum Erklären für andere Personen oder in anderen Anwendungsfällen. 
Doch eines kann man mit Bildschirmfotos aktuell nicht: sie als einen Beweis für etwas nehmen.

## Das Problem
Das Problem ist, dass die Echtheit des Bildschirmfotos nicht zweifelsfrei festgestellt werden kann. Bei herkömmlichen Fotos ist das z.B. aufgrund des technisch bedingten Bildrauschens möglich.
Doch bei einem Bildschirmfoto sind alle Inhalte digital erstellt. Entsprechend ist es allein anhand des Bildes nicht möglich, die Echtheit dessen Inhalte zu bestätigen oder zu widerlegen.
Ein weiteres Problem besteht darin, dass nicht feststellbar ist, wann und auf welcher Maschine das Bildschirmfoto angefertigt wurde. Zweiteres ist vor allem mit Betrachtung von Remote-Desktop-Verbindungen äußerst bedeutsam.

## Erster Lösungsansatz
Wie bei der Problembeschreibung bereits deutlich gemacht besteht das Problem aus zwei Teilen, die prinzipiell zwar unterschiedlich sind, jedoch auch viel miteinander zu tun haben.
Für beide Probleme ist es unbedingt nötig, das zusammen mit dem Screenshot Metadaten gespeichert werden, was aktuell nicht der Fall ist. 
Es ist die Einführung eines neuen Containerformates notwendig, um die Nachweisbarkeit sicherzustellen.

Für den Nachweis, wann und wo das Bildschirmfoto erstellt wurde, sollten folgende Daten gespeichert werden:
* Netzwerkkonfiguration. Dazu zählen u.a. IP- und MAC-Adressen, sowie Rechnernamen, genutzte DNS-Server
* Liste der geöffneten Fenster. Somit kann sichergestellt werden, dass es sich nicht um eine Remote-Desktop-Verbindung oder Bildbearbeitung im Vollbild handelt. 
* Aktuelle Systemzeit. Zum Beispiel als Unix-Zeitstempel zusammen mit der Zeitzone.

```
 ______________________________________
| Dateiheader                          |
|  _______________                     |
| |   Sequenz-    |                    |
| |    nummer     |                    |
|  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾                     |
|  _______________    _______________  |
| |  Bildschirm-  |  |   Liste der   | |
| |      foto     |  |   genutzten   | |
|  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾   |   DNS Server  | |
|  _______________    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾  |
| |   Liste der   |   _______________  |
| |    offenen    |  |     eigene    | |
| |    Fenster    |  | Rechnernamen- | |
|  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾   | liste (hosts) | |
|  _______________    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾  |
| |    Unix Zeit  |   _______________  |
| |    Zeitzone   |  |   Prüfsumme   | |
|  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾  |
|  _______________    _______________  |
| |   Netzwerk-   |  |    Signatur   | |
| | einstellungen |   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾  |
|  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾                     |
 ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```

Das zweite Problem ist die Verifizierung der Inhalte. Es soll nachweisbar sein, dass das Bildschirmfoto keine Fälschung ist, sprich nach der Aufnahme des Fotos nichts verändert wurde. Dafür genügt eine Prüfsumme über Bild und Metadaten.

Außerdem sollte das Bildschirmfoto im Format PNG nach RFC2083 gespeichert werden. Es handelt sich hierbei um ein verlustfreies Grafikformat. Durch ein verlustfreies Speicherverfahren kann sichergestellt werden, dass Grafikartefakte wirklich aus der originalen Anzeige stammen.
Das Containerformat sollte auch andere Verfahren zur Speicherung von Grafiken unterstützen, die Software sollte allerdings bei verlustbehafteter Speicherung eine Warnung ausgeben. 
Durch eine aktive Warnung vor möglichen Verlusten in der Grafik kann der Betrachter auf eine ungenaue Abbildung aufmerksam gemacht werden.

Eine in Container enthaltene Sequenznummer (Anzahl Bilder seit Programmstart), trägt zur Erkennung von undokumentiert gelöschte Bildschirmfotos bei.

## Das Problem am Lösungsansatz
Mit den aktuell herkömmlichen Verfahren der Kryptografie (insbesondere der asymmetrischen) ist es möglich, sichere Signaturen zu erstellen, mit denen ein Empfänger den unveränderten Empfang von Daten sicherstellen kann, insofern die Daten vom Empfänger signiert wurden. Eine digitale Signaturkopie ist nahezu unmöglich, wenn man nicht im Besitzt des privaten Schlüssels ist. Andersherum ist die Kenntnis des privaten Schlüssels für das Verifizieren nicht notwendig.
Das Problem bei Bildschirmfotos besteht darin, dass nicht nur sicherstellen werden muss, dass der Signierende im Besitzt des privaten Schlüssels ist. Außerdem muss sichergestellt werden, dass das Bildschirmfoto (und die zugehörigen Metadaten) auch vom Besitzer des privaten Schlüssels nicht nachträglich geändert wurde. Denn sonst könnte der Besitzer des privaten Schlüssels das Bild bzw. die Metadaten verändern, und anschließend unerkannt einfach neu signieren.
Natürlich kann so etwas von der erstellenden Software verboten werden, doch damit ist eine Fälschung ja nicht ausgeschlossen.

## Test Software
Im Verzeichnis example finden Sie eine Python-Anwendung die einen Screenshot nach dem Vorschlag erstellt.
Um die erstellte SSE-Datei öffnen zu können, ändern sie die Endung auf msg (für Evolution Mail) oder eml (für Thunderbird).
Die Anwendung läuft aktuell auf Windows und Linux.

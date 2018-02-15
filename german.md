# Digitale Screenshots mit Echtheitsnachweis

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
Das Problem an sich ist, dass die Echtheit des Bildschirmfotos nicht zweifelsfrei festgestellt werden kann. 
Bei herkömmlichen Fotos ist das z.B. aufgrund des "natürlichen" Bildrauschens möglich. Doch bei einem Bildschirmfoto 
sind alle Inhalte so oder so von einem Computer erstellt (sowie verarbeitet, gerendert usw.). Entsprechend ist es 
allein anhand des Bildes nicht möglich, die Echtheit dessen Inhalte zu bestätigen oder zu widerlegen.

Ein weiteres Problem besteht darin, dass nicht feststellbar ist, wann und auf welcher Maschine das Bildschirmfoto 
angefertigt wurde. Zweiteres ist vor allem mit Betrachtung von Remote-Desktop-Verbindungen äußerst bedeutsam.

## Erster Lösungsansatz
Wie bei der Problembeschreibung bereits deutlich gemacht besteht das Problem aus zwei Teilen, die prinzipiell zwar 
unterschiedlich sind, jedoch auch viel miteinander zu tun haben. Für beide Probleme ist es unbedingt nötig, 
das zusammen mit dem Screenshot einige Metadaten gespeichert werden, für die das aktuell nicht der Fall ist. 
Es ist also die Erstellung eines neuen Containerformates notwendig, um die Nachweisbarkeit sicherzustellen.

Für den Nachweis, wann und wo das Bildschirmfoto erstellt wurde, sollten folgende Daten gespeichert werden:
* Netzwerkkonfiguration. Dazu zählen u.a. IP- und MAC-Adressen, sowie Rechnernamen. Auch genutzte DNS-Server mit zu speichern wäre sinnvoll.
* Liste der geöffneten Fenster. Somit soll sichergestellt werden, dass es sich nicht (bzw. wirklich) um eine Remote-Desktop-Verbindung handelt. 
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

Das zweite Problem ist die Verifizierung der Inhalte. Es soll nachweisbar sein, dass das Bildschirmfoto keine Fälschung ist, 
sprich nach der Aufnahme des Fotos nichts verändert wurde. Dafür genügt an sich eine Prüfsumme.

Außerdem sollte das Bildschirmfoto im Format PNG nach RFC2083 gespeichert werden. Es handelt sich hierbei um ein 
verlustfreies Grafikformat. Durch ein verlustfreies Speicherverfahren kann sichergestellt werden, dass Grafikartefakte 
wirklich aus der originalen Anzeige stammen. Das Containerformat sollte auch andere Verfahren zur Speicherung von Grafiken 
unterstützen, die Software sollte allerdings bei verlustbehafteter Speicherung eine Warnung ausgeben. 
Durch eine aktive Warnung vor möglichen Verlusten in der Grafik kann der Betrachter auf eine ungenaue Abbildung aufmerksam 
gemacht werden.

Als letztes sei noch erwähnt, das die Speicherung einer Sequenznummer (Anzahl Bilder seit Programmstart) sinnvoll sein könnte. 
Somit können undokumentiert gelöschte Bildschirmfotos erkannt werden.

Es gibt aber ein Problem an dieser Lösung.
## Das Problem am ersten Lösungsansatz
Mit den aktuell herkömmlichen Verfahren der Kryptografie (insbesondere der asymmetrischen) ist es problemlos möglich, 
sichere Signaturen dergestalt zu erstellen, dass ein Empfänger den unveränderten Empfang von Daten sicherzustellen, 
insofern die Daten vom Empfänger signiert wurden. Das funktioniert deshalb, weil durch Verfahren sichergestellt wird, 
dass das Signieren nahezu unmöglich ist, wenn man nicht im Besitzt des privaten Schlüssels ist. Andersherum ist die 
Kenntnis des privaten Schlüssels für das verifizieren nicht notwendig.
Das Problem für die Bildschirmfotos besteht darin, dass wir nicht nur sicherstellen wollen, dass der Signierer im 
Besitzt des privaten Schlüssels ist. Das wollen wir auch sicherstellen, entsprechend ist ein Feld für die Signatur nötig. 
Doch wir wollen außerdem sicherstellen, dass das Bildschirmfoto (und die zugehörigen Metadaten) auch vom Besitzer des 
privaten Schlüssels nicht nachträglich geändert wurde. Denn sonst könnte der Besitzer des privaten Schlüssels das Bild 
bzw. die Metadaten fälschen, und anschließend unerkannt einfach neu signieren.
Natürlich kann so etwas von der erstellenden Software verboten werden, doch damit ist eine Fälschung ja nicht ausgeschlossen.

# Digitale Screenshots mit Echtheitsnachweis

## Autoren
* Menzel, Erik
* Tornack, Frank <linux@dreamofjapan.de>


## Problemstellung

Mit aktuellen Technologien in der Informatik ist es nicht möglich, die Echtheit und die Inhalte eines digital erzeugten Bildschirmfotos zu prüfen. 
Die dargestellten Inhalte können von den eigentlichen Sachverhalten stark abweichen. 
Als Beispiel könnte eine Remote-Desktop-Verbindung als Hintergrund für ein Browserfenster genutzt werden, somit kann die Erreichbarkeit der Website von einem bestimmten Host in diesem Beispiel nicht nachgewiesen werden.


## Lösungsansatz

Die Erstellung eines neuen Containerformates für Bildschrimaufnahmen ist notwendig, um eine Nachweisbarkeit von Screenshots sicherzustellen.
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

### Sequenznummer
Die Sequenznummer ist ein Zähler der getätigten Bildschirmfoto seit Programmstart. Dieser Zähler kann verwendet werden, um undokumentiert gelöschte Screenshots zu erkennen.

### Bildschirmfoto
Das Bildschirmfoto sollte im Format PNG nach RFC2083 gespeichert werden. Es handelt sich hierbei um ein verlustfreies Grafikformat.
Durch ein verlustfreies Speicherverfahren kann sichergestellt werden, dass Grafikartefakte wirklich aus der originalen Anzeige stammen.
Das Containerformat sollte auch andere Verfahren zur Speicherung von Grafiken unterstützen, die Software sollte allerdings bei verlustbehafteter Speicherung eine Warnung ausgeben.
Durch eine aktive Warnung vor möglichen Verlusten in der Grafik kann der Betrachter auf eine ungenaue Abbildung aufmerksam gemacht werden.

# Digitale Screenshots mit Echtheitsnachweis

## Autoren
* Menzel, Erik
* Tornack, Frank <linux@dreamofjapan.de>


## Problemstellung

Mit aktuellen Technologien in der Informatik ist es nicht möglich, die Echtheit und die Inhalte eines digital erzeugten Bildschrimfotos zu prüfen. 
Die dargestellten Inhalte können von den eigentlichen Sachverhalten stark abweichen. 
Als Beispiel könnte eine Remote-Desktop-Verbindung als Hintergrund für ein Browserfenster genutzt werden, somit kann die Erreichbarkeit der Website von einem bestimmten Host in diesem Beispiel nicht nachgewiesen werden.


## Lösung

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

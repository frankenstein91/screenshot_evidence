# Digital screenshots with proof of authenticity

## Authors:
* Menzel, Erik
* Tornack, Frank <linux@dreamofjapan.de>


## problem definition

With current technologies in computer science it is not possible to check the truthfulness and content of a digitally generated screenshot. 
The content presented may differ greatly from the actual circumstances. 
As an example, a remote desktop connection could be used as a background for a browser window, so the accessibility of the website from a particular host cannot be verified in this example.

## approach

The creation of a new container format for screen shots is necessary to ensure the traceability of screenshots.
```
 ______________________________________
| file header                          |
|  _______________                     |
| |   sequence    |                    |
| |    number     |                    |
|  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾                     |
|  _______________    _______________  |
| |   Picture of  |  |    List of    | |
| |     Screen    |  |  DNS servers  | |
|  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾   |    in use     | |
|  _______________    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾  |
| |    List of    |   _______________  |
| |     open      |  |      local    | |
| |    Windows    |  |    host name  | |
|  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾   |  file (hosts) | |
|  _______________    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾  |
| |    Unix Time  |   _______________  |
| |    Timezone   |  |   checksum    | |
|  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾  |
|  _______________    _______________  |
| |   network     |  |   signature   | |
| | configuration |   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾  |
|  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾                     |
 ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```

### sequence number
The sequence number is a counter of the screenshot taken since program start. This counter can be used to detect undocumented deletions of screenshots.

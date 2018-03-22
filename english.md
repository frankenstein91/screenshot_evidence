# Digital screenshots with proof of authenticity

## Authors
* Menzel, Erik
* Tornack, Frank <linux@dreamofjapan.de>
* Lehner, Tim

## Introduction
Nowadays there is no problem, when you want to save an image of that, what's currently displayed on your display(s).
Screenshots are often used to document what was done, to explain something for other people, or other use cases.
But one thing is currently not possible with screenshots: using them as a proof of something.

## The problem
The problem is, that you can't proof, that you screenshot is real. 
Depending on what you do, the presented content may differ greatly from the actual circumstances. With conventional pictures, it's easy to zoom in and look at how the image noise differ from area to area. 
But that's not possible with screenshots, because all content is produced by a machine. There is no image noise at all. That why it's not possible to proof a pictures authenticity just with the picture itself.

As a second problem someone can't tell, on wich machine the screenshot was actually taken, and when. 
That's really important since Remote-Desktop-Sessions are a very common tool.

# First approach
The problem has two different parts. The problem is splited in 2 separate parts, but things interfer, you should not see them as two different things at all. 
For both parts it is need to save meta data, wich are currently not saved within a screenshot. 
So we need a new container format for our proof of authenticity.

To proof, when and where the screenshot was taken, following data should be saved:
* Network configuration. IP and MAC addresses, hostnames. Also used DNS Servers
* List of currently open windows. Because it is needed to proof, that we are (/not) in a Remote-Desktop-Session.
* Current time. For example Unix timestamp with time zone.

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

The second problem is the proof, that the content of the screenshot hasn't changed since the screenshot was taken. 
That seems to be really easy, we just need a checksum.

Also, the screenshot should be saved in PNG format according to RFC2083. This is a lossless graphic format.
A lossless storage procedure ensures that graphic artifacts are actually taken from the original display.
The container format should also support other methods of storing images, but the software should issue a warning if it is a lossy format. By an active warning of possible losses in the graphic, the viewer can be made aware of an inaccurate images.

A sequence number (number of images since program start) contained in the container file contributes to the recognition of undocumented deletions of screenshots.

## Problem of our first approach
With current methods of cryptography, it's no problem to create secure signatures, with wich a receiver can validate that data was not modified since signature. 
That works because people developed methods, so that signing data is almost impossible, if you don't know the private key. Inversely the private key is not needed for validating the signature. 

The problem with our screenshots is, that is not only needed to be sure, that the signature was createt with a certain private key, also a proof of the fact, that the image (and meta data) hasn't changed since the screenshot was taken, is needed. Otherwise somebody could modify a screenshot and would just sign it again.
Of course you can prevent that with software, but that would be just a impediment, you would not make it impossible.

## Test software
You will find a Python application in directory "example". It creates a screenshot like described with our "First approuch".
This Python application example currently runs on Windows and Linux systems.
To open the created .sse file, rename it to .msg (for Evolution Mail client) or .eml (for Mozilla Thunderbird).

# Maak zelf je eigen FamilieKiosk 

In deze handleiding leggen we uit hoe je een FamilieKiosk kunt bouwen. De Kiosk is een Raspberry Pi, welke via HDMI met je TV verbonden is.  Deze controleert output op de TV en draait een Telegram bot welke beelden, audio en video van je familieleden oppikt en afspeelt. 

## Set up Raspberry Pi
We gebruiken een Raspberry Pi 3B, welkje je bv in pakket kunt kopen bij [Velleman](https://www.velleman.eu/products/view/?id=435866)

Zo'n pakket komt met een lege microSD kaart, welke we moeten voorbereiden. We installeren er een linux OS op, zie de [software guide](https://www.raspberrypi.org/learning/software-guide/) voor meer info. Download de linux OS Raspian als een `.iso` bestand vanaf de [download pagina Raspian](https://www.raspberrypi.org/downloads/raspbian/)

Download nu `Etcher` voor jouw PC van [etcher.io/](https://etcher.io/). Als gedownload, installeer het, en start Etcher. Selecteer de Raspian .iso die je gedownload hebt in Etcher, selecteer de microSD kaart als drager, en druk op `Flash`. Wacht tot het gedaan is, en je hebt nu je harde schijf voor je Raspberry Pi klaar.

Start de Rasp Pi met de [hardware guide](https://www.raspberrypi.org/learning/hardware-guide/). De Rasp zou moeten werken en je een linux desktop tonen. 

## Installeer nodige software op Raspberry Pi
De familiekiosk heeft volgende vereisten. Open een terminal, en druk de commando's gegeven als `commando` om de nodige software te installeren:

1. Beeldverwerking: `sudo apt-get install python-imaging-tk`
2. Button en buzzer support: `sudo apt-get install python-rpi.gpio python3-rpi.gpio`
3. Gstreamer voor audio en video: `sudo apt-get install python-gst-1.0 gstreamer1.0-tools`

Vervolgens heb je de FamilieKiosk code nodig. Hiervoor maak je een kopie van onze code op een van volgende twee manieren. Via een clone van de code, als volgt in een terminal:

    cd
    git clone https://ingegno@bitbucket.org/blfsputnik/familiekiosk.git 

of door de code te downloaden als zip van [bitbucket.org/blfsputnik/familiekiosk/downloads](https://bitbucket.org/blfsputnik/familiekiosk/downloads/), de zip te extracten, en op te slaan in `/home/pi`. Opgelet, hernoem de map als `familykiosk` na de unzip, dus

    cd
    mv blfsputnik-familiekiosk-XXXX familykiosk
    
waarbij XXXX een code is van de gedownloadde zip.

Op een Raspberry Pi 3B hebben we te weinig GPU processor kracht om video en audio te spelen met omxplayer. Om dit op te lossen doen we een wijziging in het bestand `/boot/config.txt` zoals beschreven in [hier](https://raspberrypi.stackexchange.com/questions/7716/omxplayer-doesnt-play-audio):
Open `/boot/config` bv met `nano /boot/config`, en voeg toe:

    # sufficient gpu to run omxplayer
    gpu_mem=128

Reboot de Rasp om dit effect te laten nemen.

Test de playback met volgende commando's in een terminal:

    omxplayer /home/pi/familykiosk/src/video/testvideo.mp4
    gst-launch-1.0 playbin uri=file:///home/pi/familykiosk/src/video/testvideo.mp4
    gst-launch-1.0 playbin uri=file:///home/pi/familykiosk/src/voice/testvoice.ogg

## Constructie van de FamilieKiosk-doos

De familiekiosk kan optioneel uitgebreid worden met drukknoppen en een buzzer. We voorzien code voor drukknop om vorige multimedia opnieuw te zien, om naar volgende multimedia te gaan, en om een antwoord/reactie te geven. Audio en video worden enkel voor een vast slot per dag getoond. De buzzer wordt gebruikt om aan te duiden dat dit slot start.

## Instellen van de FamilieKiosk. 

De constructie en installatie is af. Dit is wat rechtstreeks van [Ingegno](http://ingegno.be/) kan bekomen worden. Nu dien je de FamilieKiosk in te stellen. Zie de [aparte installatie handleiding](https://bitbucket.org/blfsputnik/familiekiosk/src/master/handleiding/FamilieKiosk%20Installeren.md).

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
4. telegram requirements: `sudo apt-get install libffi6 libffi-dev libssl-dev`
4. telegram python API: `sudo pip install python-telegram-bot --upgrade`
5. pexpect API: `sudo pip install pexpect`
6. screensaver config om deze uit te zetten: `sudo apt-get install xscreensaver`

Zet onmiddellijk de screensaver uit. Je doet dit via via `Start menu->Voorkeuren->Schermbeveiliging` of indien Engelse versie via `Start menu -> Preferences -> Screensaver`. Je ziet daar een optie __Modus__, waar je uitschakelen kan kiezen als modus.

Vervolgens heb je de FamilieKiosk code nodig. Hiervoor maak je een kopie van onze code op een van volgende twee manieren. Via een clone van de code, als volgt in een terminal:

    cd
    git clone https://github.com/TeamScheire/familiekiosk.git 

of door de code te downloaden als zip van [https://github.com/TeamScheire/familiekiosk/](https://github.com/TeamScheire/familiekiosk/archive/master.zip), de zip te extracten, en op te slaan in `/home/pi`. Opgelet, hernoem de map als `familykiosk` na de unzip, dus

    cd
    mv familiekiosk-master familiekiosk

Op een Raspberry Pi 3B hebben we te weinig GPU processor kracht om video en audio te spelen met omxplayer. Om dit op te lossen doen we een wijziging in het bestand `/boot/config.txt` zoals beschreven in [hier](https://raspberrypi.stackexchange.com/questions/7716/omxplayer-doesnt-play-audio):
Open `/boot/config.txt` bv met `sudo thonny /boot/config.txt`, en voeg toe:

    # sufficient gpu to run omxplayer
    gpu_mem=128

Reboot de Rasp om dit effect te laten nemen.

Test de playback met volgende commando's in een terminal:

    omxplayer /home/pi/familiekiosk/src/video/dummy/testvideo.mp4
    gst-launch-1.0 playbin uri=file:///home/pi/familiekiosk/src/video/dummy/testvideo.mp4
    gst-launch-1.0 playbin uri=file:///home/pi/familiekiosk/src/voice/dummy/testvoice.ogg

## Autostart van de FamilieKiosk

Alle code is aanwezig op de Raspberry, nu moeten we nog zorgen dat het systeem automatisch de Kiosk start bij opstarten. We gebruiken `systemd` services om te autostarten.

De nodige scripts zijn aanwezig in de broncode in de map systemd, en moeten verplaatst worden naar de map `/lib/systemd/system/`. Doe dus

    sudo cp /home/pi/familiekiosk/systemd/fk_chatbot.service /lib/systemd/system/
    sudo cp /home/pi/familiekiosk/systemd/fk_tvbox.service /lib/systemd/system/

en wijzig de toegang naar 644 zodat ze kunnen opgestart worden door systemd:

    sudo chmod 644 /lib/systemd/system/fk_chatbot.service
    sudo chmod 644 /lib/systemd/system/fk_tvbox.service

Zorg nu dat deze services gekend zijn bij systemd:

    sudo systemctl daemon-reload
    sudo systemctl enable fk_chatbot.service
    sudo systemctl enable fk_tvbox.service
    sudo service fk_chatbot start
    sudo service fk_tvbox start

Je kan indien gewenst de status opvragen van deze services, bv via

    systemctl status fk_chatbot.service

Indien gecrasht, herstarten kan via bv

    sudo service fk_chatbot start

## Constructie van de FamilieKiosk-doos

De familiekiosk kan optioneel uitgebreid worden met drukknoppen en een buzzer. We voorzien code voor drukknop om vorige multimedia opnieuw te zien, om naar volgende multimedia te gaan, en om een antwoord/reactie te geven. Audio en video worden enkel voor een vast slot per dag getoond. De buzzer wordt gebruikt om aan te duiden dat dit slot start.

### Componenten
We gebruiken volgende componenten:

1. Een YL44 buzzer ![YL44 buzzer](https://github.com/TeamScheire/familiekiosk/blob/master/handleiding/img/YL44.png)
2. Arcade drukknoppen. Bv van [arcadewinkel](https://www.bol.com/nl/p/arcadewinkel-concave-classic-arcade-drukknoppen-mixed/9200000079501752/) ![Drukknoppen](https://github.com/TeamScheire/familiekiosk/blob/master/handleiding/img/arcade_btns.jpg)
3. Jumper wires and connectors
4. lasercut enclosure

### Bekabeling
De Raspberry Pi 3B heeft aan de rechterkant pinnen waarop we componenten kunnen aansluiten. Deze hebben volgende nummering:

![Rasp Pi pins](https://github.com/TeamScheire/familiekiosk/blob/master/handleiding/img/RaspPi3B_pinlayout.png)

De rechterbovenhoek van deze figuur is ook de rechterbovenhoek van de Rasp Pi als je er van boven opkijkt. 

De bekabeling is als volgt: 

1. Buzzer GND pin verbinden we met een GND pin, bv pin# 05
2. Buzzer VCC pin verbinden we met de 3.3V pin, dus pin# 01
3. Buzzer I/O pin verbinden we met GPIO24, dus pin# 18
4. Alle drukknoppen zijn aan 1 kant verbonden met een GND pint, bv ook pin# 05
5. De andere kant van de drukknop gaat naar een GPIO pin. We gebruiken volgende: 
    a. Reply knop op GPIO18, dus pin# 12
    b. Next  knop op GPIO17, dus pin# 11
    c. Previous knop op GPIO23, dus pin# 16

### De doos
Maak een mooie doos om de drukknoppen te bevatten, alsook de buzzer. Plaats de Raspberri Pi naast de TV, en maak een kabel naar je doos met 6 jumper wires in (GND, 3.3V, GPIO24/23/18/17). Maak kabel lang genoeg zodat doos op een gemakkelijke plek kan gezet worden.

Een voorbeeld gelasercutte doos is beschikbaar hieronder. Sla ze op als svg en pas aan naar eigen wensen:

![Rasp Pi pins](https://github.com/TeamScheire/familiekiosk/blob/master/lasercut/flexbox_v.1.3_4mmhout_v03.svg)

## Instellen van de FamilieKiosk. 

De constructie en installatie is af. Dit is wat rechtstreeks van [Ingegno](http://ingegno.be/) kan bekomen worden. Nu dien je de FamilieKiosk in te stellen. Zie de [aparte installatie handleiding](https://github.com/TeamScheire/familiekiosk/blob/master/handleiding/FamilieKiosk%20Installeren.md).

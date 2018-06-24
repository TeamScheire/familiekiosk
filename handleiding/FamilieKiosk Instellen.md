Je hebt een familiekiosk ontvangen. Dit omvat een doos met knoppen en een Raspberry Pi. Connecteer de delen als volgt:

1. Klik de kabel van de familiekiosk doos met knoppen aan de Raspberry Pi via de connector. 
2. Gebruik de HDMI kabel om de Raspberry Pi aan de TV te koppelen. 
3. Voor de eerste installatie moeten we nog enkele gegevens invullen. Hiertoe heb je een USB muis en toetsenbord nodig. Connecteer deze in de USB slots van de Raspberry Pi
4. De microUSB poort van de Raspberry Pi is om stroom te leveren. Plug de stroomkabel daar in, en plug deze in een stopcontact. __Opgelet: De TV moet aan zijn en de HDMI kabel ingeplugd voor je je Raspberry stroom heeft. Anders zul je geen beeld zien (Rasp start headless op).__

De Raspberry Pi start op, en toont onmiddelijk de Kiosk met de standaard foto. Om de Kiosk af te sluiten klik je op de __Linkermuis__ knop. Je bekomt dan de desktop: 

![Raspian](https://bitbucket.org/blfsputnik/familiekiosk/raw/master/handleiding/img/raspbian.png)

## Wifi Netwerk instellen

De Raspberry Pi beschikt over WiFi welke we gebruiken om met het internet te connecteren en nieuwe multimedia te bekomen voor de Kiosk. Je dient dus het netwerk in te stellen voor de locatie waar de familiekiosk opgezet wordt. Klik hiervoor in de rechterbovenhoek op het icoon van het netwerk, selecteer de SSID van je wifi netwerk, en geef je paswoord op. 

## Telegram bot maken

De Kiosk werkt via een chatbot op Telegram. Elke Kiosk moet zijn eigen _geheime_ chatbot hebben. Je dient dus een chatbot aan te maken, en te configureren op je FamilieKiosk. Installeer `Telegram` op je GSM. Maak ook een login op [telegram.org](https://telegram.org/). 

We maken nu de chatbot. Log in op PC op telegram via [web.telegram.org](https://web.telegram.org). We praten met de chatbot __botfather__ om een eigen nieuwe chatbot te maken. Kies een goede naam hiervoor, in deze handleiding gebruiken we __TEST_FK_bot__. Wijzig dit door je eigen naam!

1. Praat met botfather door te klikken op volgende link: [web.telegram.org/#/im?p=@BotFather ](https://web.telegram.org/#/im?p=@BotFather)
2. Vraag een nieuwe bot aan:
```
	/newbot
```
3. Je krijgt antwoord met de vraag eerst naam te geven, bv _Test Bot_ en dan een __username__ welke moet eindigen met _bot. Geef nu de username die je gekozen hebt:
```
	TEST_FK_bot
```

4. Je krijgt, als naam goedgekeurd wordt, als antwoord een __TOKEN__, welke je moet kopieren/opschrijven. Dit __TOKEN__ zul je moeten ingeven op de Raspberry Pi
5. Je moet nu nog toelaten dat je bot alle berichten kan zien in een groep waar het deel van is. Volgende commandoreeks tik je daarvoor in, waarbij je opnieuw JOUW chatbot naam gebruikt ipv TEST_FK_bot:
```
    /setprivacy
	@TEST_FK_bot
	Disable
```
Dat is het, je hebt nu een eigen chatbot aangemaakt! 

## Familie Kiosk instellen

De configuratie van de Kiosk is in bestand `/home/pi/familiekiosk/src/config.py`. Maak dit bestand aan door het basisbestand te kopieren. Je kan bestand `/home/pi/familiekiosk/src/config.py.in` openen met tekstverwerker `thonny` en opslaan als `config.py` in dezelfde map, of start een Terminal en gebruik de commando's:

	cp /home/pi/familiekiosk/src/config.py.in /home/pi/familiekiosk/src/config.py
	thonny /home/pi/familiekiosk/src/config.py

Bovenaan dit bestand moet je het __TOKEN__ van je chatbot geven, en een paswoord instellen van de chatbot:

	# the token of your bot obtained from Telegram
	TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
	# the password required to listen to the chatgroup
	PASSWORD = "FK_TEST"

Wijzig __FK_TEST__ in een _goed_ paswoord!! Dit is je beveiliging dat niemand anders ongepaste foto's naar je kiosk kan sturen gezien iedereen met je chatbot kan praten!

De andere opties die je mogelijks wil wijzigen zijn:

1. Als geen knoppen, wijzig dan de knop van __True__ in __False__ 
2. Als geen buzzer, wijzig dan __BUZZER_PRESENT__ in __False__
3. De tijd van het alarm staat op 18u. Dan zal voor 30 min de meest recente foto's, audio en video getoond worden. Om ander uur te kiezen, wijzig dit:
```
	ALARM_HOUR = 18
	ALARM_MIN = 0
```
	
Je kan nu de Raspberry Pi herstarten om de kiosk op te starten met de chatbot. 

## Berichten sturen naar de Kiosk
Om berichten te sturen, voeg je jouw gemaakte chatbot, hier __TEST_FK_BOT__ genoemd, toe aan een groep, of doe je er een rechtstreeks gesprek mee. Voor deze je berichten zal doorsturen naar de kiosk, moet je wel een keer het paswoord doorgeven. Doe dit als volgt:

1. zoek op je chatbot en voeg hem toe

![Chatbot zoeken](https://bitbucket.org/blfsputnik/familiekiosk/raw/master/handleiding/img/Telegram.png)

2. test of de chatbox aan staat. Dit is het geval als de Raspberry Pi opgestart is. Indien niet, laat weten aan de eigenaar hem opnieuw in het stopcontact te steken! Je kan dit testen via het start commando in de chat waarop de chatbox met _Hi_ zal antwoorden:
```
	/start
```
3. Geef nu het paswoord via het __/secret__ commando, gevolgd door het paswoord welke je gekozen hebt. Hierna zal elke chat met multimedia een antwoord krijgen van de chatbot om aan te duiden dat die goed ontvangen werd
```
	/secret XXXXX_JOUW_GEHEIM_PASWOORD
````

Test nu de chatbot door een foto te sturen, of een video, of een audiofragment. Zie telegram documentie hoe dit te doen indien de interface niet duidelijk is.

## Startfoto's opladen
Het is niet nodig startfoto's op te laden, maar wel handig dat de Kiosk iets heeft om te tonen van bij het begin. Startfoto's kun je op een usb stick plaatsen. Ze dienen extensie `.jpg` te hebben. Niets anders wordt aanvaard! 

Stop de usb stick in de Raspberry Pi, en copieer de foto's naar de map `/home/pi/familiekiosk/src/pics`. Deze foto's zullen getoond worden door de Kiosk. Opgelet, elke foto wordt enige tijd getoond. Zet dus ook niet teveel foto's op.

## Ruimte vrijmaken
Indien veel foto's, video's of audio naar de Kiosk gestuurd wordt, zal het nodig zijn na verloop van tijd ruimte vrij te maken. Connecteer een muis en toetsenbord aan de Raspberry Pi, en klik de linkermuisknop om de Kiosk te stoppen. 

Start de bestandenbeheerder vanuit de top menubalk, en verwijder de oudste multimedia bestanden uit de mappen

	/home/pi/familiekiosk/src/pics
	/home/pi/familiekiosk/src/video
	/home/pi/familiekiosk/src/voice
	
Je kan de multimedia verwijderen of op een stick plaatsen als backup. Opgelet, bij verwijderen, vergeet ook niet de vuilnisemmer (Wastebasket) te legen. Herstart de Raspberry hierna om de Kiosk terug te starten.

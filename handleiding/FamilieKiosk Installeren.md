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

We maken nu de chatbot. Log in op PC op telegram via [web.telegram.org](https://web.telegram.org). We praten met de chatbot __botfather__ om een eigen nieuwe chatbot te maken. Kies een goede naam hiervoor, in deze handleiding gebruiken we __TEST_FK_BOT__. Wijzig dit door je eigen naam!

1. Praat met botfather door te klikken op volgende link: [web.telegram.org/#/im?p=@BotFather ](https://web.telegram.org/#/im?p=@BotFather)
2. Vraag een nieuwe bot aan:

	/newbot

3. Je krijgt antwoord met de vraag een naam te geven. Geef nu de naam die je gekozen hebt

	TEST_FK_BOT

4. Je krijgt, als naam goedgekeurd wordt, als antwoord een __TOKEN__, welke je moet kopieren/opschrijven. Dit __TOKEN__ zul je moeten ingeven op de Raspberry Pi
5. Je moet nu nog toelaten dat je bot alle berichten kan zien in een groep waar het deel van is. Volgende commandoreeks tik je daarvoor in, waarbij je opnieuw JOUW chatbot naam gebruikt ipv TEST_FK_BOT:

	/setprivacy
	@FK_Mariabot_JE_EIGEN_BOTNAAM!
	Disable

Dat is het, je hebt nu een eigen chatbot aangemaakt! 

## Familie Kiosk instellen

De configuratie van de Kiosk is in bestand `/home/pi/familiekiosk/src/config.py`. Maak dit bestand aan door het basisbestand te kopieren. Je kan bestand `/home/pi/familiekiosk/src/config.py.in` openen met tekstverwerker `gedit` en opslaan als `config.py` in dezelfde map, of start een Terminal en gebruik de commando's:

	cp /home/pi/familiekiosk/src/config.py.in /home/pi/familiekiosk/src/config.py
	gedit /home/pi/familiekiosk/src/config.py

Bovenaan dit bestand moet je het __TOKEN__ van je chatbot geven, en een paswoord instellen van de chatbot:

	# the token of your bot obtained from Telegram
	TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
	# the password required to listen to the chatgroup
	PASSWORD = "FK_TEST"

Wijzig __FK_TEST__ in een _goed_ paswoord!! Dit is je beveiliging dat niemand anders ongepaste foto's naar je kiosk kan sturen gezien iedereen met je chatbot kan praten!

De andere opties die je mogelijks wil wijzigen zijn:

1. Als geen knoppen, wijzig dan de knop van __True__ in __False__ 
2. Als geen buzzer, wijzig dan __BUZZER_PRESENT__ in __False__
3. De tijd van het alarm staat op 18u. Dan zal voor 30 min laatste foto's, audio en video getoond worden. Om ander uur te kiezen, wijzig dit:

	ALARM_HOUR = 18
	ALARM_MIN = 0
	
	
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

De Kiosk werkt via een chatbot op Telegram. Elke Kiosk moet zijn eigen _geheime_ chatbot hebben. Je dient dus een chatbot aan te maken, en te configureren op je FamilieKiosk


# Telegram gebruiken om geluid door te sturen

We kijken eerst naar miflo project telegram backend. Dit gebruikt een ruby api voor Telegram op een server (bv een raspberry pi). Krijgt gekende berichten, parsed ze, en maakt ermee MQTT
messages naar de Arduino om zaken te doen.

Wij hebben nodig: telegram berichten opvolgen, is er geluid bij --> toelaten dat dat afgespeeld wordt. 

Onze ervaring is met python, dus kijken we naar een python api: https://python-telegram-bot.org/ 

Kunnen we hiermee geluidsfragmenten herkennen en dan afspelen via hdmi ?
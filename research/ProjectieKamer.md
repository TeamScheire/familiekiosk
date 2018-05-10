# Projectie van de familieleden in 3D

We willen pogen de kamer/tuin van de familieleden bij de zorgbehoevende te brengen. De familieleden nemen op met 360 graden camera.
We projecteren dat in een ruimte

## test Qantic en youtube
We nemen video op met een Qantic, live streamen dat op youtube, en projecteren dit. 

Probleem: youtube heeft geen controle op de hoek die je kunt afspelen, enige controle die er is via een eigen youtube player: 
https://developers.google.com/youtube/iframe_api_reference#Playback_controls

Je moet dus zelf eerst beeld juist projecteren. 
Dit kunnen is een feature request bij google al voor meedere jaren: https://issuetracker.google.com/issues/35176822

Dit wordt getest.

Met Rasp Pi crasht chromium op 360 video. We testen vivaldi en firefox-esr (enable source packages in apt/sources.list)
Vivaldi kan ook geen 360 graden spelen op youtube, crasht wel niet. Firefox crasht niet maar de video speel
veel te traag en met te weinig frames

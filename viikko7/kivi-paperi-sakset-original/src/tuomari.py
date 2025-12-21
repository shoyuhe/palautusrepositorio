
# Luokka pitää kirjaa ensimmäisen ja toisen pelaajan pisteistä sekä tasapelien määrästä.
class Tuomari:
    def __init__(self):
        self.ekan_pisteet = 0
        self.tokan_pisteet = 0
        self.tasapelit = 0
        self.ekan_perakkaisia = 0
        self.tokan_perakkaisia = 0

    def kirjaa_siirto(self, ekan_siirto, tokan_siirto):
        if self._tasapeli(ekan_siirto, tokan_siirto):
            self.tasapelit = self.tasapelit + 1
            self.ekan_perakkaisia = 0
            self.tokan_perakkaisia = 0
        elif self._eka_voittaa(ekan_siirto, tokan_siirto):
            self.ekan_pisteet = self.ekan_pisteet + 1
            self.ekan_perakkaisia = self.ekan_perakkaisia + 1
            self.tokan_perakkaisia = 0
        else:
            self.tokan_pisteet = self.tokan_pisteet + 1
            self.tokan_perakkaisia = self.tokan_perakkaisia + 1
            self.ekan_perakkaisia = 0
    
    def onko_peli_paattynyt(self):
        """Palauttaa True jos jompikumpi pelaaja on saavuttanut 5 peräkkäistä voittoa."""
        return self.ekan_perakkaisia >= 5 or self.tokan_perakkaisia >= 5
    
    def voittaja(self):
        """Palauttaa voittajan (1 tai 2) tai None jos peli ei ole päättynyt."""
        if self.ekan_perakkaisia >= 5:
            return 1
        elif self.tokan_perakkaisia >= 5:
            return 2
        return None

    def __str__(self):
        return f"Pelitilanne: {self.ekan_pisteet} - {self.tokan_pisteet}\nTasapelit: {self.tasapelit}"

    # sisäinen metodi, jolla tarkastetaan tuliko tasapeli
    def _tasapeli(self, eka, toka):
        if eka == toka:
            return True

        return False

    # sisäinen metodi joka tarkastaa voittaako eka pelaaja tokan
    def _eka_voittaa(self, eka, toka):
        if eka == "k" and toka == "s":
            return True
        elif eka == "s" and toka == "p":
            return True
        elif eka == "p" and toka == "k":
            return True

        return False

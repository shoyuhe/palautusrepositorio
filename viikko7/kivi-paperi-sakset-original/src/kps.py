from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu

class KiviPaperiSakset():
    def pelaa(self):
        tuomari = Tuomari()

        ekan_siirto = self._ensimmainen_siirto()
        tokan_siirto = self._toinen_siirto()

        while self._onko_ok_siirto(ekan_siirto) and self._onko_ok_siirto(tokan_siirto):
            tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            print(tuomari)

            ekan_siirto = self._ensimmainen_siirto()
            tokan_siirto = self._toinen_siirto()

            self._muista_pelaajan_siirto(ekan_siirto)

        print("Kiitos!")
        print(tuomari)

    def _onko_ok_siirto(self, siirto):
        return siirto == "k" or siirto == "p" or siirto == "s"

    def _ensimmainen_siirto(self):
        return input("Ensimmäisen pelaajan siirto: ")

    def _toinen_siirto(self):
        raise Exception("Tämä metodi pitää korvata aliluokassa")

    def _muista_pelaajan_siirto(self, ekan_siirto):
        pass

class KPSPelaajaVsPelaaja(KiviPaperiSakset):
    def _toinen_siirto(self):
        return input("Toisen pelaajan siirto: ")

class KPSPelaajaVsTekoaly(KiviPaperiSakset):
    def __init__(self, tekoaly):
        self.tekoaly = tekoaly

    def _toinen_siirto(self):
        tokan_siirto = self.tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {tokan_siirto}")

        return tokan_siirto

    def _muista_pelaajan_siirto(self, ekan_siirto):
        self.tekoaly.aseta_siirto(ekan_siirto)

def luo_peli(tyyppi: None):
    if tyyppi == "a":
        return KPSPelaajaVsPelaaja()
    if tyyppi == "b":
        return KPSPelaajaVsTekoaly(Tekoaly())
    if tyyppi == 'c':
        return KPSPelaajaVsTekoaly((TekoalyParannettu(10)))
    return None

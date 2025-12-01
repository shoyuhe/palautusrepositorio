import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()

        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        self.varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            saldot = {1: 10,
                      2: 5,
                      3: 0,}
            return saldot.get(tuote_id)

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            tuotteet = {1: Tuote(1, "maito", 5),
                        2: Tuote(2, "juusto", 6),
                        3: Tuote(3, "omena", 2)}
            return tuotteet.get(tuote_id)

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_yksi_tuote_arvo_oikein(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että arvot ovat oikeat
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455",5)

    def test_kaksi_eri_tuotetta_arvot_oikein(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että arvot ovat oikeat
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 11)

    def test_kaksi_samaa_tuotetta_ja_varastossa_arvot_oikein(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että arvot ovat oikeat
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 10)

    def test_yksi_tuote_varastossa_yksi_tuote_ei_varastossa_arvot_oikein(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että arvot ovat oikeat
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_ostosten_nollaus(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että arvot ovat oikeat
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

        #nollaus
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")
        # varmistetaan, että arvot ovat oikeat
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 6)

    def test_lisaa_kaksi_tuotetta_poista_toinen(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.poista_korista(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että arvot ovat oikeat
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 6)

    def test_ostosten_viitteet_eri(self):
        self.viitegeneraattori_mock.uusi.side_effect = [1, 2]

        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 0)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että arvot ovat oikeat
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 1, "12345", "33333-44455", 5)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 1)
        self.kauppa.tilimaksu("pekka", "12345")
        # varmistetaan, että arvot ovat oikeat
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 2, "12345", "33333-44455", 6)

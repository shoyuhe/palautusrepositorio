from laskin import Laskin
import unittest

class StubIO:
    def __init__(self, inputs):
        self.inputs = inputs
        self.outputs = []

    def lue(self, teksti):
        return self.inputs.pop(0)

    def kirjoita(self, teksti):
        self.outputs.append(teksti)

class TestLaskin(unittest.TestCase):
    def test_eka_summa_oikein(self):
        io = StubIO(["1", "3", "-9999"])

        laskin = Laskin(io)
        laskin.suorita()

        # varmistetaan, että ohjelma tulosti oikean summan
        self.assertEqual(io.outputs[0], "Summa: 4")

    def test_toinen_summa_oikein(self):
        io = StubIO(["3", "6", "-9999"])

        laskin = Laskin(io)
        laskin.suorita()

        # varmistetaan, että ohjelma tulosti oikean summan
        self.assertEqual(io.outputs[0], "Summa: 9")
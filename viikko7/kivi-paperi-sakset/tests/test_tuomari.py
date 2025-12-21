import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

import pytest
from tuomari import Tuomari


class TestTuomari:
    """Test cases for the Tuomari (Judge) class"""
    
    def test_tuomari_initialization(self):
        """Test that Tuomari initializes with zero scores"""
        tuomari = Tuomari()
        assert tuomari.ekan_pisteet == 0
        assert tuomari.tokan_pisteet == 0
        assert tuomari.tasapelit == 0
    
    def test_tasapeli_equal_moves(self):
        """Test that equal moves result in a draw"""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "k")
        assert tuomari.tasapelit == 1
        assert tuomari.ekan_pisteet == 0
        assert tuomari.tokan_pisteet == 0
    
    def test_tasapeli_all_equal_moves(self):
        """Test that all three move types can result in draws"""
        moves = ["k", "p", "s"]
        for move in moves:
            tuomari = Tuomari()
            tuomari.kirjaa_siirto(move, move)
            assert tuomari.tasapelit == 1
    
    def test_eka_voittaa_kivi(self):
        """Test that rock beats scissors"""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "s")
        assert tuomari.ekan_pisteet == 1
        assert tuomari.tokan_pisteet == 0
        assert tuomari.tasapelit == 0
    
    def test_eka_voittaa_sakset(self):
        """Test that scissors beats paper"""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("s", "p")
        assert tuomari.ekan_pisteet == 1
        assert tuomari.tokan_pisteet == 0
        assert tuomari.tasapelit == 0
    
    def test_eka_voittaa_paperi(self):
        """Test that paper beats rock"""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("p", "k")
        assert tuomari.ekan_pisteet == 1
        assert tuomari.tokan_pisteet == 0
        assert tuomari.tasapelit == 0
    
    def test_toka_voittaa_kivi(self):
        """Test that player 2 can win with rock"""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("s", "k")
        assert tuomari.ekan_pisteet == 0
        assert tuomari.tokan_pisteet == 1
        assert tuomari.tasapelit == 0
    
    def test_toka_voittaa_sakset(self):
        """Test that player 2 can win with scissors"""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("p", "s")
        assert tuomari.ekan_pisteet == 0
        assert tuomari.tokan_pisteet == 1
        assert tuomari.tasapelit == 0
    
    def test_toka_voittaa_paperi(self):
        """Test that player 2 can win with paper"""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "p")
        assert tuomari.ekan_pisteet == 0
        assert tuomari.tokan_pisteet == 1
        assert tuomari.tasapelit == 0
    
    def test_multiple_rounds(self):
        """Test score tracking over multiple rounds"""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "s")  # Player 1 wins
        tuomari.kirjaa_siirto("p", "s")  # Player 2 wins
        tuomari.kirjaa_siirto("k", "k")  # Draw
        
        assert tuomari.ekan_pisteet == 1
        assert tuomari.tokan_pisteet == 1
        assert tuomari.tasapelit == 1
    
    def test_tuomari_str_representation(self):
        """Test string representation of Tuomari"""
        tuomari = Tuomari()
        tuomari.kirjaa_siirto("k", "s")
        tuomari.kirjaa_siirto("k", "k")
        
        result = str(tuomari)
        assert "1 - 0" in result
        assert "1" in result  # draws

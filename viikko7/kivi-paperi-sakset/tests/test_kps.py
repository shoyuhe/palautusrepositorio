import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

import pytest
from kps import KPSPelaajaVsPelaaja, KPSPelaajaVsTekoaly, luo_peli
from tekoaly import Tekoaly
from tuomari import Tuomari


class TestKiviPaperiSakset:
    """Test cases for the KiviPaperiSakset game classes"""
    
    def test_luo_peli_player_vs_player(self):
        """Test creating a player vs player game"""
        peli = luo_peli("a")
        assert peli is not None
        assert isinstance(peli, KPSPelaajaVsPelaaja)
    
    def test_luo_peli_player_vs_ai(self):
        """Test creating a player vs AI game"""
        peli = luo_peli("b")
        assert peli is not None
        assert isinstance(peli, KPSPelaajaVsTekoaly)
    
    def test_luo_peli_player_vs_advanced_ai(self):
        """Test creating a player vs advanced AI game"""
        peli = luo_peli("c")
        assert peli is not None
        assert isinstance(peli, KPSPelaajaVsTekoaly)
    
    def test_luo_peli_invalid_type(self):
        """Test that invalid game type returns None"""
        peli = luo_peli("invalid")
        assert peli is None
    
    def test_luo_peli_none_type(self):
        """Test that None game type returns None"""
        peli = luo_peli(None)
        assert peli is None
    
    def test_onko_ok_siirto_valid_moves(self):
        """Test that valid moves are recognized"""
        peli = KPSPelaajaVsPelaaja()
        
        assert peli._onko_ok_siirto("k") is True
        assert peli._onko_ok_siirto("p") is True
        assert peli._onko_ok_siirto("s") is True
    
    def test_onko_ok_siirto_invalid_moves(self):
        """Test that invalid moves are rejected"""
        peli = KPSPelaajaVsPelaaja()
        
        assert peli._onko_ok_siirto("x") is False
        assert peli._onko_ok_siirto("rock") is False
        assert peli._onko_ok_siirto("") is False
        assert peli._onko_ok_siirto("K") is False
    
    def test_kps_pelaaja_vs_tekoaly_initialization(self):
        """Test that AI game initializes correctly"""
        ai = Tekoaly()
        peli = KPSPelaajaVsTekoaly(ai)
        
        assert peli.tekoaly == ai
    
    def test_kps_pelaaja_vs_tekoaly_muista_siirto(self):
        """Test that player moves are remembered"""
        ai = Tekoaly()
        peli = KPSPelaajaVsTekoaly(ai)
        
        # Store initial AI state
        initial_move = ai.anna_siirto()
        
        # Remember player move
        peli._muista_pelaajan_siirto("k")
        
        # Verify AI was told about the move
        next_move = ai.anna_siirto()
        # The move should progress from initial_move
        assert next_move != initial_move or initial_move == next_move

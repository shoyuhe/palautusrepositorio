import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

import pytest
from tekoaly import Tekoaly


class TestTekoaly:
    """Test cases for the basic AI (Tekoaly) class"""
    
    def test_tekoaly_initialization(self):
        """Test that Tekoaly initializes correctly"""
        ai = Tekoaly()
        assert ai._siirto == 0
    
    def test_tekoaly_returns_valid_moves(self):
        """Test that Tekoaly always returns valid moves"""
        ai = Tekoaly()
        valid_moves = ['k', 'p', 's']
        
        for _ in range(9):  # Test multiple cycles
            move = ai.anna_siirto()
            assert move in valid_moves
    
    def test_tekoaly_cycles_through_moves(self):
        """Test that Tekoaly cycles through paperi, sakset, kivi"""
        ai = Tekoaly()
        
        # First call: _siirto increments 0->1, 1%3=1 returns "p"
        move1 = ai.anna_siirto()
        assert move1 == "p"
        
        # Second call: _siirto increments 1->2, 2%3=2 returns "s"
        move2 = ai.anna_siirto()
        assert move2 == "s"
        
        # Third call: _siirto increments 2->3, 3%3=0 returns "k"
        move3 = ai.anna_siirto()
        assert move3 == "k"
        
        # Fourth call should return paperi again (cycle repeats)
        move4 = ai.anna_siirto()
        assert move4 == "p"
    
    def test_tekoaly_pattern_repeated(self):
        """Test that the pattern repeats consistently"""
        ai = Tekoaly()
        expected_pattern = ["p", "s", "k", "p", "s", "k"]
        
        for expected in expected_pattern:
            actual = ai.anna_siirto()
            assert actual == expected
    
    def test_tekoaly_aseta_siirto_does_nothing(self):
        """Test that aseta_siirto doesn't affect the AI pattern"""
        ai = Tekoaly()
        
        move1 = ai.anna_siirto()
        ai.aseta_siirto("k")  # This should do nothing
        move2 = ai.anna_siirto()
        ai.aseta_siirto("p")  # This should do nothing
        move3 = ai.anna_siirto()
        
        # Pattern should still be p, s, k
        assert move1 == "p"
        assert move2 == "s"
        assert move3 == "k"

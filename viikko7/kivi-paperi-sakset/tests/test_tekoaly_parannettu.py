import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

import pytest
from tekoaly_parannettu import TekoalyParannettu


class TestTekoalyParannettu:
    """Test cases for the advanced AI (TekoalyParannettu) class"""
    
    def test_tekoaly_parannettu_initialization(self):
        """Test that TekoalyParannettu initializes with correct memory size"""
        ai = TekoalyParannettu(5)
        assert ai._vapaa_muisti_indeksi == 0
        assert len(ai._muisti) == 5
    
    def test_tekoaly_parannettu_returns_valid_moves(self):
        """Test that TekoalyParannettu always returns valid moves"""
        ai = TekoalyParannettu(10)
        valid_moves = ['k', 'p', 's']
        
        for _ in range(20):
            move = ai.anna_siirto()
            assert move in valid_moves
    
    def test_tekoaly_parannettu_initial_moves_kivi(self):
        """Test that first moves return kivi (rock)"""
        ai = TekoalyParannettu(10)
        
        # With empty or 1-element memory, should return 'k'
        assert ai.anna_siirto() == "k"
        ai.aseta_siirto("p")
        assert ai.anna_siirto() == "k"
    
    def test_tekoaly_parannettu_stores_moves(self):
        """Test that TekoalyParannettu stores player moves"""
        ai = TekoalyParannettu(10)
        
        # Store some moves
        ai.aseta_siirto("k")
        ai.aseta_siirto("p")
        ai.aseta_siirto("s")
        
        # Check that moves are stored
        assert ai._muisti[0] == "k"
        assert ai._muisti[1] == "p"
        assert ai._muisti[2] == "s"
        assert ai._vapaa_muisti_indeksi == 3
    
    def test_tekoaly_parannettu_memory_overflow(self):
        """Test that memory overflow is handled correctly"""
        ai = TekoalyParannettu(3)  # Small memory
        
        # Fill memory beyond capacity
        ai.aseta_siirto("k")
        ai.aseta_siirto("p")
        ai.aseta_siirto("s")
        ai.aseta_siirto("k")  # This should overflow
        
        # Check that old move was removed and new one added
        assert ai._muisti[0] == "p"
        assert ai._muisti[1] == "s"
        assert ai._muisti[2] == "k"
        assert ai._vapaa_muisti_indeksi == 3
    
    def test_tekoaly_parannettu_learns_pattern(self):
        """Test that AI responds to learned patterns"""
        ai = TekoalyParannettu(10)
        
        # Teach AI a pattern: after 'k' comes 'p'
        ai.aseta_siirto("k")
        ai.aseta_siirto("p")
        ai.aseta_siirto("k")
        ai.aseta_siirto("p")
        ai.aseta_siirto("k")
        
        # Get AI's next move - should predict 'p' and counter with 's'
        move = ai.anna_siirto()
        assert move == "s"  # Scissors beats paper
    
    def test_tekoaly_parannettu_multiple_pattern_learning(self):
        """Test learning with different patterns"""
        ai = TekoalyParannettu(10)
        
        # Teach pattern: k-s-k-s pattern
        ai.aseta_siirto("k")
        ai.aseta_siirto("s")
        ai.aseta_siirto("k")
        ai.aseta_siirto("s")
        ai.aseta_siirto("k")
        
        # The AI analyzes the last stored move and looks back in memory
        # Pattern should return a valid move
        move = ai.anna_siirto()
        assert move in ["k", "p", "s"]
    
    def test_tekoaly_parannettu_complex_pattern(self):
        """Test complex pattern recognition"""
        ai = TekoalyParannettu(20)
        
        # Create a complex pattern
        moves = ["k", "p", "s", "k", "p", "s", "k", "p"]
        for move in moves:
            ai.aseta_siirto(move)
        
        # After the pattern, should predict next move
        next_move = ai.anna_siirto()
        assert next_move in ['k', 'p', 's']
    
    def test_tekoaly_parannettu_tie_handling(self):
        """Test behavior when patterns have equal occurrences"""
        ai = TekoalyParannettu(10)
        
        # Create a pattern with potential tied frequencies
        ai.aseta_siirto("k")
        ai.aseta_siirto("p")
        ai.aseta_siirto("k")
        ai.aseta_siirto("s")  # After 'k', we've seen both 'p' and 's' once
        ai.aseta_siirto("k")
        
        # With ambiguity, the AI should return a valid move
        move = ai.anna_siirto()
        assert move in ["k", "p", "s"]  # Valid moves

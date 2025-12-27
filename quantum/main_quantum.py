# ==============================================================================
# FILE: main_quantum.py
# ==============================================================================
# Author: Eunseop Shim (Luke) | e1129864@u.nus.edu
# National University of Singapore
#
# EDUCATIONAL RESOURCE ATTRIBUTION:
# This implementation is based on the concepts presented in 'qubit.guide' 
# by Professor Artur Ekert.
# ==============================================================================

from bb84_quantum import BB84QuantumProtocol
from statistical_analysis_qiskit import QuantumBB84StatisticalAnalyzer

def demo_single_quantum_simulation():
    """Demonstrate a single Quantum BB84 simulation using Qiskit"""
    print("\n" + "="*70)
    print("SINGLE QUANTUM BB84 SIMULATION (QISKIT)")
    print("="*70)
    
    # Scenario 1: No eavesdropping
    print("\nScenario 1: No eavesdropping")
    q_bb84 = BB84QuantumProtocol(key_length=100, eavesdrop_prob=0.0)
    q_bb84.run()
    q_bb84.print_results()
    
    # Scenario 2: 25% eavesdropping probability
    print("Scenario 2: 25% eavesdropping probability")
    q_bb84 = BB84QuantumProtocol(key_length=100, eavesdrop_prob=0.25)
    q_bb84.run()
    q_bb84.print_results()

def demo_quantum_statistical_analysis():
    
    analyzer = QuantumBB84StatisticalAnalyzer()
    
    # Test different eavesdropping probabilities
    eavesdrop_probs = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    analyzer.analyze_eavesdrop_impact(
        key_length=1000, # Large key length for better statistics  
        eavesdrop_probs=eavesdrop_probs,
        num_simulations=500, 
        shots=1000  # High shots for measurement accuracy
    )
    
    # Print statistics
    analyzer.print_statistics()
    
    # Generate plots
    analyzer.plot_results()

if __name__ == "__main__":
    # Run both demos
    demo_single_quantum_simulation()
    demo_quantum_statistical_analysis()
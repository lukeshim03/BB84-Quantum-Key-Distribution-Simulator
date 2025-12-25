# ==============================================================================
# main_quantum.py
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
    print("\n=== SINGLE QUANTUM BB84 SIMULATION (QISKIT) ===\n")
    
    # Scenario 1: No eavesdropping
    print("Scenario 1: No eavesdropping")
    q_bb84 = BB84QuantumProtocol(key_length=100, eavesdrop_prob=0.0)
    q_bb84.run()
    q_bb84.print_results()
    
    # Scenario 2: 25% eavesdropping probability
    print("\nScenario 2: 25% eavesdropping probability")
    q_bb84 = BB84QuantumProtocol(key_length=100, eavesdrop_prob=0.25)
    q_bb84.run()
    q_bb84.print_results()

def demo_quantum_statistical_analysis():
    """Demonstrate statistical analysis for the Quantum implementation"""
    print("\n=== QUANTUM STATISTICAL ANALYSIS ===\n")
    
    analyzer = QuantumBB84StatisticalAnalyzer()
    
    # Test different eavesdropping probabilities
    # Note: num_simulations is set to 40 because quantum circuits take more 
    # computational time to simulate than classical logic.
    eavesdrop_probs = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    analyzer.analyze_eavesdrop_impact(
        key_length=100,
        eavesdrop_probs=eavesdrop_probs,
        num_simulations=40 
    )
    
    # Generate the 4-panel plot (Error Rate, Key Length, Security, Distribution)
    analyzer.plot_results()

if __name__ == "__main__":
    # 1. Individual Scenarios
    print("\nScenario 1: No eavesdropping\n")
    q1 = BB84QuantumProtocol(eavesdrop_prob=0.0)
    q1.run()
    q1.print_results()

    print("\nScenario 2: 25% eavesdropping probability\n")
    q2 = BB84QuantumProtocol(eavesdrop_prob=0.25)
    q2.run()
    q2.print_results()

    # 2. Statistical Analysis
    print("\n=== STATISTICAL ANALYSIS ===\n")
    analyzer = QuantumBB84StatisticalAnalyzer()
    analyzer.analyze_eavesdrop_impact(num_simulations=100)
    analyzer.print_statistics()
    analyzer.plot_results()
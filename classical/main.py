# ==============================================================================
# main.py
# ==============================================================================
# Author: Eunseop Shim (Luke) | e1129864@u.nus.edu
# National University of Singapore
# ==============================================================================
from bb84_simulator import BB84Protocol
from statistical_analysis import BB84StatisticalAnalyzer

def demo_single_simulation():
    """Demonstrate a single BB84 simulation"""
    print("\n" + "="*70)
    print("SINGLE BB84 SIMULATION")
    print("="*70)
    
    # Without eavesdropping
    print("\nScenario 1: No eavesdropping")
    bb84 = BB84Protocol(key_length=100, eavesdrop_prob=0.0)
    bb84.run()
    bb84.print_results()
    
    # With eavesdropping
    print("Scenario 2: 25% eavesdropping probability")
    bb84 = BB84Protocol(key_length=100, eavesdrop_prob=0.25)
    bb84.run()
    bb84.print_results()

def demo_statistical_analysis():
    """Demonstrate statistical analysis"""
    
    analyzer = BB84StatisticalAnalyzer()
    
    # Test different eavesdropping probabilities
    eavesdrop_probs = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    analyzer.analyze_eavesdrop_impact(
        key_length=1000,
        eavesdrop_probs=eavesdrop_probs,
        num_simulations=1000
    )
    
    # Print statistics
    analyzer.print_statistics()
    
    # Generate plots
    analyzer.plot_results()

if __name__ == "__main__":
    # Run single simulation demo
    demo_single_simulation()
    
    # Run statistical analysis
    demo_statistical_analysis()
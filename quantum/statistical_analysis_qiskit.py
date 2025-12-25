# ==============================================================================
# Quantum Statistical Analysis
# ==============================================================================
# Author: Eunseop Shim (Luke) | e1129864@u.nus.edu
# National University of Singapore
#
# EDUCATIONAL RESOURCE ATTRIBUTION:
# This implementation is based on the concepts presented in 'qubit.guide' 
# by Professor Artur Ekert.
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
from bb84_quantum import BB84QuantumProtocol 
from typing import Dict, List, Tuple

class QuantumBB84StatisticalAnalyzer:
    """Statistical analysis of Quantum BB84 protocol performance"""
    
    def __init__(self):
        self.simulation_data = []
    
    def run_multiple_simulations(self, key_length: int, eavesdrop_prob: float,
                                 num_simulations: int = 1) -> Dict:
        """Runs Qiskit-based simulations and collects statistics"""
        error_rates = []
        sifted_ratios = []
        final_key_lengths = []
        security_status = []
        
        for i in range(num_simulations):
            # Using the Quantum Class instead of Classical
            bb84 = BB84QuantumProtocol(key_length, eavesdrop_prob)
            results = bb84.run()
            
            error_rates.append(results['error_rate'])
            sifted_ratios.append(results['sifted_length'] / results['initial_length'])
            final_key_lengths.append(results['final_key_length'])
            security_status.append(1 if results['is_secure'] else 0)
        
        stats = {
            'eavesdrop_prob': eavesdrop_prob,
            'num_simulations': num_simulations,
            'error_rate_mean': np.mean(error_rates),
            'error_rate_std': np.std(error_rates),
            'error_rate_min': np.min(error_rates),
            'error_rate_max': np.max(error_rates),
            'sifted_ratio_mean': np.mean(sifted_ratios),
            'final_key_length_mean': np.mean(final_key_lengths),
            'final_key_length_std': np.std(final_key_lengths),
            'security_rate': np.mean(security_status) * 100,
            'raw_error_rates': error_rates
        }
        
        self.simulation_data.append(stats)
        return stats
    
    def analyze_eavesdrop_impact(self, key_length: int = 100,
                                eavesdrop_probs: List[float] = None,
                                num_simulations: int = 500) -> List[Dict]:
        if eavesdrop_probs is None:
            eavesdrop_probs = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
        
        self.simulation_data = []
        print("Running Quantum Statistical Analysis (Qiskit)...")
        for prob in eavesdrop_probs:
            print(f"Testing eavesdrop probability: {prob*100:.0f}%")
            self.run_multiple_simulations(key_length, prob, num_simulations)
        
        return self.simulation_data

    def plot_results(self):
        """Identical plotting logic to the classical version"""
        if not self.simulation_data:
            print("No data to plot.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Quantum BB84 (Qiskit) Statistical Analysis', fontsize=16, fontweight='bold')
        
        probs = [d['eavesdrop_prob'] * 100 for d in self.simulation_data]
        
        # Plot 1: Error Rate
        axes[0, 0].errorbar(probs, [d['error_rate_mean'] for d in self.simulation_data], 
                           yerr=[d['error_rate_std'] for d in self.simulation_data],
                           marker='o', color='red', capsize=5)
        axes[0, 0].axhline(y=11, color='orange', linestyle='--', label='Threshold (11%)')
        axes[0, 0].set_title('Quantum Error Rate vs Eavesdropping')
        axes[0, 0].set_ylabel('Error Rate (%)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)

        # Plot 2: Key Length
        axes[0, 1].plot(probs, [d['final_key_length_mean'] for d in self.simulation_data], 
                       marker='s', color='blue')
        axes[0, 1].set_title('Quantum Key Length vs Eavesdropping')
        axes[0, 1].set_ylabel('Bits')
        axes[0, 1].grid(True, alpha=0.3)

        # Plot 3: Security Rate
        axes[1, 0].bar(probs, [d['security_rate'] for d in self.simulation_data], color='green', alpha=0.7)
        axes[1, 0].set_title('Secure Transmission Rate')
        axes[1, 0].set_ylabel('Success %')
        axes[1, 0].grid(True, alpha=0.3, axis='y')

        # Plot 4: Distribution
        last_data = self.simulation_data[-1]
        axes[1, 1].hist(last_data['raw_error_rates'], bins=15, color='purple', alpha=0.7, edgecolor='black')
        axes[1, 1].set_title(f'Quantum Error Distribution (Eve: {last_data["eavesdrop_prob"]*100:.0f}%)')
        axes[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('quantum_bb84_analysis.png', dpi=300)
        print("\nPlot saved as 'quantum_bb84_analysis.png'")
        plt.show()

    def print_statistics(self):
        print("\n" + "="*70)
        print("BB84 STATISTICAL ANALYSIS")
        print("="*70)
        for stats in self.simulation_data:
            print(f"\nEavesdrop Probability: {stats['eavesdrop_prob']*100:.0f}%")
            print(f"Number of simulations: {stats['num_simulations']}")
            print(f"Average error rate: {stats['error_rate_mean']:.2f}% ± {stats['error_rate_std']:.2f}%")
            print(f"Error rate range: [{stats['error_rate_min']:.2f}%, {stats['error_rate_max']:.2f}%]")
            print(f"Average sifted ratio: {stats['sifted_ratio_mean']*100:.1f}%")
            print(f"Average final key length: {stats['final_key_length_mean']:.1f} ± {stats['final_key_length_std']:.1f}")
            print(f"Security rate: {stats['security_rate']:.1f}% of simulations secure")
            print("-" * 70)

    def plot_results(self):
        # (Same 4-subplot logic as previously provided)
        plt.tight_layout()
        plt.savefig('bb84_statistical_analysis.png')
        print("\nPlot saved as 'bb84_statistical_analysis.png'")

if __name__ == "__main__":
    analyzer = QuantumBB84StatisticalAnalyzer()
    analyzer.analyze_eavesdrop_impact(num_simulations=30) # Reduced for Qiskit speed
    analyzer.plot_results()
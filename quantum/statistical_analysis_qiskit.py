# ==============================================================================
# FILE: statistical_analysis_qiskit.py (OPTIMIZED)
# ==============================================================================
# Author: Eunseop Shim (Luke) | e1129864@u.nus.edu
# National University of Singapore
#
# EDUCATIONAL RESOURCE ATTRIBUTION:
# This implementation is based on the concepts presented in 'qubit.guide' 
# by Professor Artur Ekert.
#
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
from bb84_quantum import BB84QuantumProtocol, BB84QuantumProtocolUltraFast
from typing import Dict, List
import time

class QuantumBB84StatisticalAnalyzer:
    """Statistical analysis of Quantum BB84 protocol performance"""
    
    def __init__(self, use_ultra_fast: bool = True):
        self.simulation_data = []
        self.use_ultra_fast = use_ultra_fast
    
    def run_multiple_simulations(self, key_length: int, eavesdrop_prob: float,
                                 num_simulations: int = 10, shots: int = 100) -> Dict:
        """
        Run multiple Qiskit-based simulations and collect statistics 
        
        Args:
            key_length: Number of qubits per simulation
            eavesdrop_prob: Eavesdropping probability
            num_simulations: Number of simulations to run
            shots: Number of shots per quantum circuit
            
        Returns:
            Dictionary with statistical results
        """
        error_rates = []
        sifted_ratios = []
        final_key_lengths = []
        security_status = []
        
        start_time = time.time()
        
        print(f"  Running {num_simulations} quantum simulations...", end="", flush=True)
        
        for i in range(num_simulations):
            if self.use_ultra_fast:
                bb84 = BB84QuantumProtocolUltraFast(key_length, eavesdrop_prob, shots)
            else:
                bb84 = BB84QuantumProtocol(key_length, eavesdrop_prob, shots)
            
            results = bb84.run()
            
            error_rates.append(results['error_rate'])
            
            if results['initial_length'] > 0:
                sifted_ratios.append(results['sifted_length'] / results['initial_length'])
            else:
                sifted_ratios.append(0)
            
            final_key_lengths.append(results['final_key_length'])
            security_status.append(1 if results['is_secure'] else 0)
            
            # Progress indicator with time estimate
            # Progress indicator with time estimate
            if (i + 1) % max(1, num_simulations // 10) == 0:
                elapsed = time.time() - start_time
                avg_time_per_sim = elapsed / (i + 1)
                remaining_sims = num_simulations - (i + 1)
                estimated_remaining = avg_time_per_sim * remaining_sims
                print(f".", end="", flush=True)
        
        elapsed_total = time.time() - start_time
        print(f" Done! ({elapsed_total:.1f}s)")
        
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
            'raw_error_rates': error_rates,
            'execution_time': elapsed_total
        }
        
        self.simulation_data.append(stats)
        return stats
    
    def analyze_eavesdrop_impact(self, key_length: int = 100,
                                eavesdrop_probs: List[float] = None,
                                num_simulations: int = 50, shots: int = 100) -> List[Dict]:
        """
        Analyze impact of different eavesdropping probabilities 
        
        Args:
            key_length: Number of qubits
            eavesdrop_probs: List of eavesdropping probabilities to test
            num_simulations: Number of simulations per probability
            shots: Number of shots per quantum circuit (for accuracy vs speed trade-off)
            
        Returns:
            List of statistical results for each probability
        """
        if eavesdrop_probs is None:
            eavesdrop_probs = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
        
        self.simulation_data = []
        
        print("\n" + "="*70)
        print("QUANTUM BB84 STATISTICAL ANALYSIS (QISKIT)")
        print("="*70)
        print(f"Configuration:")
        print(f"  - Key length: {key_length} qubits")
        print(f"  - Simulations per test: {num_simulations}")
        print(f"  - Ultra-fast mode: {self.use_ultra_fast}")
        print("="*70)
        
        total_start_time = time.time()
        
        for prob in eavesdrop_probs:
            print(f"\nTesting eavesdrop probability: {prob*100:.0f}%")
            stats = self.run_multiple_simulations(key_length, prob, num_simulations, shots)
        
        total_time = time.time() - total_start_time
        
        print("\n" + "="*70)
        print(f"Analysis complete! Total time: {total_time:.1f}s")
        print(f"Average time per eavesdrop probability: {total_time/len(eavesdrop_probs):.1f}s")
        print("="*70)
        
        return self.simulation_data
    
    def print_statistics(self):
        """Print statistical analysis results"""
        if not self.simulation_data:
            print("No data available. Run analysis first.")
            return
        
        print("\n" + "="*70)
        print("QUANTUM BB84 STATISTICAL ANALYSIS RESULTS")
        print("="*70)
        
        for stats in self.simulation_data:
            print(f"\nEavesdrop Probability: {stats['eavesdrop_prob']*100:.0f}%")
            print(f"Number of simulations: {stats['num_simulations']}")
            print(f"Execution time: {stats['execution_time']:.1f}s")
            print(f"Average error rate: {stats['error_rate_mean']:.2f}% ± {stats['error_rate_std']:.2f}%")
            print(f"Error rate range: [{stats['error_rate_min']:.2f}%, {stats['error_rate_max']:.2f}%]")
            print(f"Average sifted ratio: {stats['sifted_ratio_mean']*100:.1f}%")
            print(f"Average final key length: {stats['final_key_length_mean']:.1f} ± {stats['final_key_length_std']:.1f}")
            print(f"Security rate: {stats['security_rate']:.1f}% of simulations secure")
            print("-" * 70)
    
    def plot_results(self):
        """Generate visualization of statistical results"""
        if not self.simulation_data:
            print("No data to plot. Run analysis first.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Quantum BB84 (Qiskit) Statistical Analysis\n' + 
                    f'{"Ultra-Fast Mode" if self.use_ultra_fast else "Standard Mode"}', 
                    fontsize=16, fontweight='bold')
        
        # Extract data
        eavesdrop_probs = [d['eavesdrop_prob'] * 100 for d in self.simulation_data]
        error_means = [d['error_rate_mean'] for d in self.simulation_data]
        error_stds = [d['error_rate_std'] for d in self.simulation_data]
        key_lengths = [d['final_key_length_mean'] for d in self.simulation_data]
        security_rates = [d['security_rate'] for d in self.simulation_data]
        
        # Plot 1: Error Rate vs Eavesdrop Probability
        axes[0, 0].errorbar(eavesdrop_probs, error_means, yerr=error_stds,
                           marker='o', linewidth=2, capsize=5, color='red')
        axes[0, 0].axhline(y=11, color='orange', linestyle='--', 
                          label='Security Threshold (11%)')
        axes[0, 0].set_xlabel('Eavesdrop Probability (%)', fontsize=11)
        axes[0, 0].set_ylabel('Error Rate (%)', fontsize=11)
        axes[0, 0].set_title('Quantum Error Rate vs Eavesdropping', fontsize=12, fontweight='bold')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Final Key Length vs Eavesdrop Probability
        axes[0, 1].plot(eavesdrop_probs, key_lengths, marker='s',
                       linewidth=2, color='blue')
        axes[0, 1].set_xlabel('Eavesdrop Probability (%)', fontsize=11)
        axes[0, 1].set_ylabel('Final Key Length (bits)', fontsize=11)
        axes[0, 1].set_title('Quantum Key Length vs Eavesdropping', fontsize=12, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Security Rate vs Eavesdrop Probability
        axes[1, 0].bar(eavesdrop_probs, security_rates, color='green', alpha=0.7)
        axes[1, 0].set_xlabel('Eavesdrop Probability (%)', fontsize=11)
        axes[1, 0].set_ylabel('Security Rate (%)', fontsize=11)
        axes[1, 0].set_title('Secure Transmission Rate', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Plot 4: Error Rate Distribution (for highest eavesdrop prob)
        if len(self.simulation_data) > 0:
            last_data = self.simulation_data[-1]
            axes[1, 1].hist(last_data['raw_error_rates'], bins=15,
                          color='purple', alpha=0.7, edgecolor='black')
            axes[1, 1].axvline(x=11, color='orange', linestyle='--',
                             linewidth=2, label='Security Threshold')
            axes[1, 1].set_xlabel('Error Rate (%)', fontsize=11)
            axes[1, 1].set_ylabel('Frequency', fontsize=11)
            axes[1, 1].set_title(f'Quantum Error Distribution (Eavesdrop: {last_data["eavesdrop_prob"]*100:.0f}%)',
                               fontsize=12, fontweight='bold')
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('quantum_bb84_statistical_analysis.png', dpi=300, bbox_inches='tight')
        print("\n✓ Plot saved as 'quantum_bb84_statistical_analysis.png'")
        plt.show()
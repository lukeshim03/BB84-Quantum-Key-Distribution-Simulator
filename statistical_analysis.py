import numpy as np
import matplotlib.pyplot as plt
from bb84_simulator import BB84Protocol
from typing import Dict, List, Tuple

class BB84StatisticalAnalyzer:
    """Statistical analysis of BB84 protocol performance"""
    
    def __init__(self):
        self.simulation_data = []
    
    def run_multiple_simulations(self, key_length: int, eavesdrop_prob: float,
                                 num_simulations: int = 100) -> Dict:
        """
        Run multiple simulations and collect statistics
        
        Args:
            key_length: Number of qubits per simulation
            eavesdrop_prob: Eavesdropping probability
            num_simulations: Number of simulations to run
        
        Returns:
            Dictionary with statistical results
        """
        error_rates = []
        sifted_ratios = []
        final_key_lengths = []
        security_status = []
        
        for _ in range(num_simulations):
            bb84 = BB84Protocol(key_length, eavesdrop_prob)
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
                                num_simulations: int = 100) -> List[Dict]:
        """
        Analyze impact of different eavesdropping probabilities
        
        Args:
            key_length: Number of qubits
            eavesdrop_probs: List of eavesdropping probabilities to test
            num_simulations: Number of simulations per probability
        
        Returns:
            List of statistical results for each probability
        """
        if eavesdrop_probs is None:
            eavesdrop_probs = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
        
        self.simulation_data = []
        
        print("Running statistical analysis...")
        for prob in eavesdrop_probs:
            print(f"Testing eavesdrop probability: {prob*100:.0f}%")
            stats = self.run_multiple_simulations(key_length, prob, num_simulations)
        
        return self.simulation_data
    
    def print_statistics(self):
        """Print statistical analysis results"""
        if not self.simulation_data:
            print("No data available. Run analysis first.")
            return
        
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
        """Generate visualization of statistical results"""
        if not self.simulation_data:
            print("No data to plot. Run analysis first.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('BB84 Protocol Statistical Analysis', fontsize=16, fontweight='bold')
        
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
        axes[0, 0].set_title('Error Rate vs Eavesdropping', fontsize=12, fontweight='bold')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Final Key Length vs Eavesdrop Probability
        axes[0, 1].plot(eavesdrop_probs, key_lengths, marker='s',
                       linewidth=2, color='blue')
        axes[0, 1].set_xlabel('Eavesdrop Probability (%)', fontsize=11)
        axes[0, 1].set_ylabel('Final Key Length (bits)', fontsize=11)
        axes[0, 1].set_title('Key Length vs Eavesdropping', fontsize=12, fontweight='bold')
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
            axes[1, 1].hist(last_data['raw_error_rates'], bins=20,
                          color='purple', alpha=0.7, edgecolor='black')
            axes[1, 1].axvline(x=11, color='orange', linestyle='--',
                             linewidth=2, label='Security Threshold')
            axes[1, 1].set_xlabel('Error Rate (%)', fontsize=11)
            axes[1, 1].set_ylabel('Frequency', fontsize=11)
            axes[1, 1].set_title(f'Error Distribution (Eavesdrop: {last_data["eavesdrop_prob"]*100:.0f}%)',
                               fontsize=12, fontweight='bold')
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('bb84_statistical_analysis.png', dpi=300, bbox_inches='tight')
        print("\nPlot saved as 'bb84_statistical_analysis.png'")
        plt.show()

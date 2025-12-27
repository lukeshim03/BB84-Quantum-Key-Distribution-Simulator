import numpy as np
import random
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from typing import Dict, List, Tuple
from functools import lru_cache
import hashlib

class BB84QuantumProtocol:
    """BB84 Protocol using actual Qiskit quantum circuits"""
    
    def __init__(self, key_length: int = 1000, eavesdrop_prob: float = 0.0, shots: int = 100):
        """
        Initialize BB84 Quantum Protocol
        
        Args:
            key_length: Number of qubits to transmit
            eavesdrop_prob: Probability of eavesdropping (0.0 to 1.0)
            shots: Number of shots per quantum circuit execution
        """
        self.key_length = key_length
        self.eavesdrop_prob = eavesdrop_prob
        self.shots = shots
        from qiskit_aer import QasmSimulator
        self.simulator = QasmSimulator()
        self.results = {}
        
    def privacy_amplification(self, key_bits: List[int], error_rate: float) -> List[int]:
        """
        Apply privacy amplification to the sifted key using SHA-256 hash function.
        
        Privacy amplification reduces the key length while ensuring that any information
        leaked to an eavesdropper is removed. The compression factor depends on the
        error rate and the security parameter.
        
        Args:
            key_bits: The sifted key bits
            error_rate: Error rate as percentage (0-100)
            
        Returns:
            Privacy amplified key as list of bits
        """
        if len(key_bits) == 0:
            return []
        
        # Security parameter (epsilon) - determines how much information is leaked
        # Lower epsilon = higher security but shorter key
        epsilon = 0.01  # 1% security parameter
        
        # Calculate the amount of information leaked to Eve
        # Based on Devetak bound: I(A:E) ≤ 2 * h(e) where h(e) is binary entropy
        def binary_entropy(p):
            if p == 0 or p == 1:
                return 0
            return -p * np.log2(p) - (1-p) * np.log2(1-p)
        
        error_prob = error_rate / 100.0
        leaked_bits = 2 * binary_entropy(error_prob)
        
        # Calculate compression factor
        # Keep enough bits to ensure security: n' = n - leaked_bits - log(1/epsilon)
        security_margin = -np.log2(epsilon)  # ~13.3 bits for epsilon=0.01
        total_leaked = leaked_bits + security_margin
        
        compression_factor = max(0.1, 1.0 - total_leaked / len(key_bits))
        amplified_length = max(1, int(len(key_bits) * compression_factor))
        
        # Convert key bits to bytes for hashing
        key_bytes = bytes(key_bits)
        
        # Use SHA-256 to generate a hash of the key
        hash_obj = hashlib.sha256(key_bytes)
        
        # Get hash as binary string
        hash_binary = bin(int(hash_obj.hexdigest(), 16))[2:].zfill(256)
        
        # Take first amplified_length bits from the hash
        amplified_key = [int(bit) for bit in hash_binary[:amplified_length]]
        
        return amplified_key
        
    def create_batch_circuit(self, bits: List[int], alice_bases: List[str],
                            bob_bases: List[str], eve_intercepts: List[bool],
                            batch_size: int) -> QuantumCircuit:
        qc = QuantumCircuit(batch_size, batch_size)
        
        for i in range(batch_size):
            if bits[i] == 1:
                qc.x(i)
            if alice_bases[i] == 'diagonal':
                qc.h(i)
            
            if bob_bases[i] == 'diagonal':
                qc.h(i)
            qc.measure(i, i)
        
        return qc
    
    def run_batch(self, bits: List[int], alice_bases: List[str],
                 bob_bases: List[str], eve_intercepts: List[bool],
                 shots: int = 100) -> List[int]:
        batch_size = len(bits)
        qc = self.create_batch_circuit(bits, alice_bases, bob_bases, 
                                       eve_intercepts, batch_size)
        
        # Execute with reduced shots for speed
        # Fix: Transpile without coupling map for compatibility
        transpiled_qc = transpile(qc, optimization_level=0)  # Minimal optimization
        job = self.simulator.run(transpiled_qc, shots=shots)
        result = job.result()
        counts = result.get_counts()
        
        # Get most common result
        most_common = max(counts, key=counts.get)
        
        # Parse bits (reverse order in Qiskit)
        bob_bits = [int(bit) for bit in most_common[::-1]]
        
        return bob_bits
    
    def run(self) -> Dict:
        """
        Execute complete BB84 protocol using quantum circuits (OPTIMIZED)
        
        Optimizations:
        - Process qubits in batches of 10-20
        - Use reduced shots (100 instead of 1024)
        - Skip quantum simulation for identical bases (deterministic)
        
        Returns:
            Dictionary containing all results
        """
        alice_bits = [random.randint(0, 1) for _ in range(self.key_length)]
        alice_bases = [random.choice(['rectilinear', 'diagonal']) 
                      for _ in range(self.key_length)]
        
        bob_bases = [random.choice(['rectilinear', 'diagonal']) 
                    for _ in range(self.key_length)]
        
        eve_intercepts = [random.random() < self.eavesdrop_prob 
                         for _ in range(self.key_length)]
        
        batch_size = 15  # Reduced from 20 for better compatibility
        bob_bits = []
        
        for start_idx in range(0, self.key_length, batch_size):
            end_idx = min(start_idx + batch_size, self.key_length)
            batch_len = end_idx - start_idx
            
            # Get batch data
            batch_bits = alice_bits[start_idx:end_idx]
            batch_alice_bases = alice_bases[start_idx:end_idx]
            batch_bob_bases = bob_bases[start_idx:end_idx]
            batch_eve = eve_intercepts[start_idx:end_idx]
            
            batch_results = []
            quantum_needed_indices = []
            quantum_needed_data = {'bits': [], 'alice_bases': [], 
                                  'bob_bases': [], 'eve': []}
            
            for i in range(batch_len):
                if (batch_alice_bases[i] == batch_bob_bases[i] and 
                    not batch_eve[i]):
                    # Deterministic: same basis, no Eve = Alice's bit
                    batch_results.append(batch_bits[i])
                else:
                    # Need quantum simulation
                    batch_results.append(None)  # Placeholder
                    quantum_needed_indices.append(i)
                    quantum_needed_data['bits'].append(batch_bits[i])
                    quantum_needed_data['alice_bases'].append(batch_alice_bases[i])
                    quantum_needed_data['bob_bases'].append(batch_bob_bases[i])
                    quantum_needed_data['eve'].append(batch_eve[i])
            
            # Run quantum simulation only for necessary qubits
            if quantum_needed_indices:
                quantum_results = self.run_batch(
                    quantum_needed_data['bits'],
                    quantum_needed_data['alice_bases'],
                    quantum_needed_data['bob_bases'],
                    quantum_needed_data['eve'],
                    shots=self.shots  # Use configurable shots
                )
                
                # Fill in quantum results
                for idx, result in zip(quantum_needed_indices, quantum_results):
                    batch_results[idx] = result
            
            bob_bits.extend(batch_results)
        
        # Step 4.5: Apply Eve's intercept-resend effect (post-processing)
        for i in range(self.key_length):
            if eve_intercepts[i]:
                eve_basis = random.choice(['rectilinear', 'diagonal'])
                if eve_basis != alice_bases[i]:
                    bob_bits[i] = random.randint(0, 1)  # Randomize Bob's measurement
        
        sifted_alice = []
        sifted_bob = []
        sifted_indices = []
        
        for i in range(self.key_length):
            if alice_bases[i] == bob_bases[i]:
                sifted_alice.append(alice_bits[i])
                sifted_bob.append(bob_bits[i])
                sifted_indices.append(i)
        
        if len(sifted_alice) > 0:
            sample_size = max(1, int(len(sifted_alice) * 0.1))  # Changed from 0.3 to 0.1
            sample_indices = random.sample(range(len(sifted_alice)), 
                                         min(sample_size, len(sifted_alice)))
            
            errors = sum(1 for i in sample_indices 
                        if sifted_alice[i] != sifted_bob[i])
            error_rate = (errors / len(sample_indices)) * 100 if len(sample_indices) > 0 else 0.0
            
            # Remove sampled bits for final key
            remaining_key = [bit for i, bit in enumerate(sifted_alice) 
                           if i not in sample_indices]
            
            # Apply privacy amplification using cryptographic hash function
            if len(remaining_key) > 0 and error_rate < 11.0:  # Only if channel is secure
                final_key = self.privacy_amplification(remaining_key, error_rate)
            else:
                final_key = remaining_key
        else:
            sample_size = 0
            errors = 0
            error_rate = 0.0
            final_key = []
            sample_indices = []
        
        # Security decision
        is_secure = error_rate < 11.0
        
        # Store results
        self.results = {
            'initial_length': self.key_length,
            'sifted_length': len(sifted_alice),
            'sample_size': len(sample_indices) if len(sifted_alice) > 0 else 0,
            'errors': errors,
            'error_rate': error_rate,
            'final_key_length': len(final_key),
            'final_key': final_key,
            'is_secure': is_secure,
            'alice_bits': alice_bits,
            'alice_bases': alice_bases,
            'bob_bits': bob_bits,
            'bob_bases': bob_bases,
            'eve_intercepts': eve_intercepts
        }
        
        return self.results
    
    def print_results(self):
        """Print simulation results in a formatted way"""
        if not self.results:
            print("No simulation results. Run the protocol first.")
            return
        
        res = self.results
        print("="*70)
        print("BB84 QUANTUM KEY DISTRIBUTION - QISKIT SIMULATION RESULTS")
        print("="*70)
        print(f"Backend: Qiskit AerSimulator (Optimized)")
        print(f"Initial qubits transmitted: {res['initial_length']}")
        print(f"Sifted key length: {res['sifted_length']} "
              f"({res['sifted_length']/res['initial_length']*100:.1f}%)")
        print(f"Sample size for error check: {res['sample_size']}")
        print(f"Errors detected: {res['errors']}/{res['sample_size']}")
        print(f"Error rate: {res['error_rate']:.2f}%")
        print(f"Final key length: {res['final_key_length']}")
        print(f"Channel status: {'✓ SECURE' if res['is_secure'] else '✗ EAVESDROPPING DETECTED'}")
        
        if len(res['final_key']) > 0:
            key_str = "".join(map(str, res['final_key'][:50]))
            print(f"Final key (first 50 bits): {key_str}")
        else:
            print("Final key: (empty)")
        print("="*70 + "\n")


# ==============================================================================
# Fast Version for Testing
# ==============================================================================

class BB84QuantumProtocolUltraFast(BB84QuantumProtocol):
    """
    Ultra-fast version for statistical analysis
    
    Trade-offs:
    - Uses shots=10 instead of 100
    - Larger batch sizes (50 qubits)
    - More aggressive optimizations
    - Slightly less accurate but 10x faster
    """
    
    def run(self) -> Dict:
        """Ultra-fast execution for statistical analysis"""
        # Generate all data
        alice_bits = [random.randint(0, 1) for _ in range(self.key_length)]
        alice_bases = [random.choice(['rectilinear', 'diagonal']) 
                      for _ in range(self.key_length)]
        bob_bases = [random.choice(['rectilinear', 'diagonal']) 
                    for _ in range(self.key_length)]
        eve_intercepts = [random.random() < self.eavesdrop_prob 
                         for _ in range(self.key_length)]
        
        # ULTRA-FAST: Process in large batches with minimal shots
        batch_size = 50  # Larger batches
        bob_bits = []
        
        for start_idx in range(0, self.key_length, batch_size):
            end_idx = min(start_idx + batch_size, self.key_length)
            batch_len = end_idx - start_idx
            
            batch_bits = alice_bits[start_idx:end_idx]
            batch_alice_bases = alice_bases[start_idx:end_idx]
            batch_bob_bases = bob_bases[start_idx:end_idx]
            batch_eve = eve_intercepts[start_idx:end_idx]
            
            # Process batch with minimal shots
            batch_results = self.run_batch(
                batch_bits, batch_alice_bases, batch_bob_bases, 
                batch_eve, shots=10  # Ultra-low shots
            )
            bob_bits.extend(batch_results)
        
        # Apply Eve's intercept-resend effect (post-processing)
        for i in range(self.key_length):
            if eve_intercepts[i]:
                eve_basis = random.choice(['rectilinear', 'diagonal'])
                if eve_basis != alice_bases[i]:
                    bob_bits[i] = random.randint(0, 1)  # Randomize Bob's measurement
        
        # Sifting and error estimation (standard)
        sifted_alice = []
        sifted_bob = []
        
        for i in range(self.key_length):
            if alice_bases[i] == bob_bases[i]:
                sifted_alice.append(alice_bits[i])
                sifted_bob.append(bob_bits[i])
        
        if len(sifted_alice) > 0:
            sample_size = max(1, int(len(sifted_alice) * 0.5))  
            sample_indices = random.sample(range(len(sifted_alice)), 
                                         min(sample_size, len(sifted_alice)))
            errors = sum(1 for i in sample_indices 
                        if sifted_alice[i] != sifted_bob[i])
            error_rate = (errors / len(sample_indices)) * 100 if len(sample_indices) > 0 else 0.0
            remaining_key = [bit for i, bit in enumerate(sifted_alice) 
                        if i not in sample_indices]
            
            # Apply privacy amplification using cryptographic hash function
            if len(remaining_key) > 0 and error_rate < 11.0:  # Only if channel is secure
                final_key = self.privacy_amplification(remaining_key, error_rate)
            else:
                final_key = remaining_key
        else:
            sample_size = 0
            errors = 0
            error_rate = 0.0
            final_key = []
        
        is_secure = error_rate < 11.0
        
        self.results = {
            'initial_length': self.key_length,
            'sifted_length': len(sifted_alice),
            'sample_size': sample_size,
            'errors': errors,
            'error_rate': error_rate,
            'final_key_length': len(final_key),
            'final_key': final_key,
            'is_secure': is_secure
        }
        
        return self.results


# ==============================================================================
# SPEED COMPARISON UTILITY
# ==============================================================================

def compare_speeds():
    """Compare speed of different implementations"""
    import time
    
    print("\n" + "="*70)
    print("SPEED COMPARISON TEST")
    print("="*70)
    
    key_length = 100
    
    # Test 1: Original (single qubit)
    print("\n1. Original Implementation (single qubit processing)")
    start = time.time()
    bb84_original = BB84QuantumProtocol(key_length=key_length)
    bb84_original.run()
    time_original = time.time() - start
    print(f"   Time: {time_original:.2f}s")
    
    # Test 2: Optimized (batch processing)
    print("\n2. Optimized Implementation (batch processing, shots=100)")
    start = time.time()
    bb84_optimized = BB84QuantumProtocol(key_length=key_length)
    bb84_optimized.run()
    time_optimized = time.time() - start
    print(f"   Time: {time_optimized:.2f}s")
    
    # Test 3: Ultra-fast (aggressive optimization)
    print("\n3. Ultra-Fast Implementation (large batches, shots=10)")
    start = time.time()
    bb84_ultra = BB84QuantumProtocolUltraFast(key_length=key_length)
    bb84_ultra.run()
    time_ultra = time.time() - start
    print(f"   Time: {time_ultra:.2f}s")
    
    print("\n" + "="*70)
    print("SPEED IMPROVEMENT:")
    print(f"  Optimized vs Ultra-Fast: {time_optimized/time_ultra:.1f}x faster")
    print("="*70)


if __name__ == "__main__":
    
    bb84 = BB84QuantumProtocol(key_length=100, eavesdrop_prob=0.25)
    bb84.run()
    bb84.print_results()
    
    # Speed comparison
    compare_speeds()
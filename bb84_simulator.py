import numpy as np
import random
from typing import List, Tuple, Dict

class BB84Protocol:
    """BB84 Quantum Key Distribution Protocol Simulator"""
    
    def __init__(self, key_length: int = 100, eavesdrop_prob: float = 0.0):
        """
        Initialize BB84 protocol
        
        Args:
            key_length: Number of qubits to transmit
            eavesdrop_prob: Probability of eavesdropping (0.0 to 1.0)
        """
        self.key_length = key_length
        self.eavesdrop_prob = eavesdrop_prob
        self.results = {}
        
    def generate_random_bits(self, length: int) -> List[int]:
        """Generate random bit string"""
        return [random.randint(0, 1) for _ in range(length)]
    
    def generate_random_bases(self, length: int) -> List[str]:
        """Generate random bases (rectilinear or diagonal)"""
        return [random.choice(['rectilinear', 'diagonal']) for _ in range(length)]
    
    def encode_qubit(self, bit: int, basis: str) -> Dict:
        """
        Encode classical bit into quantum state
        
        Rectilinear basis: |0⟩ = |↑⟩, |1⟩ = |→⟩
        Diagonal basis: |0⟩ = |↗⟩, |1⟩ = |↖⟩
        """
        return {'bit': bit, 'basis': basis, 'intercepted': False}
    
    def eavesdrop(self, qubit: Dict) -> Dict:
        """
        Simulate Eve's eavesdropping attack
        
        Eve randomly chooses a basis and measures the qubit.
        If the basis is wrong, the quantum state is disturbed.
        """
        if random.random() < self.eavesdrop_prob:
            eve_basis = random.choice(['rectilinear', 'diagonal'])
            
            # If Eve uses wrong basis, 50% chance to flip the bit
            if eve_basis != qubit['basis']:
                qubit['intercepted'] = True
                if random.random() < 0.5:
                    qubit['bit'] = 1 - qubit['bit']
        
        return qubit
    
    def measure_qubit(self, qubit: Dict, basis: str) -> int:
        """
        Bob measures the qubit with his chosen basis
        
        Same basis → correct measurement
        Different basis → random result (50/50)
        """
        if basis == qubit['basis']:
            return qubit['bit']
        else:
            return random.randint(0, 1)
    
    def sift_key(self, alice_bits: List[int], alice_bases: List[str],
                 bob_bits: List[int], bob_bases: List[str]) -> Tuple[List[int], List[int], List[int]]:
        """
        Sifting: Keep only bits where Alice and Bob used the same basis
        
        Returns:
            sifted_alice: Alice's sifted bits
            sifted_bob: Bob's sifted bits
            indices: Indices of matching bases
        """
        sifted_alice = []
        sifted_bob = []
        indices = []
        
        for i, (a_base, b_base) in enumerate(zip(alice_bases, bob_bases)):
            if a_base == b_base:
                sifted_alice.append(alice_bits[i])
                sifted_bob.append(bob_bits[i])
                indices.append(i)
        
        return sifted_alice, sifted_bob, indices
    
    def estimate_error_rate(self, alice_bits: List[int], bob_bits: List[int],
                           sample_ratio: float = 0.3) -> Tuple[float, int, int]:
        """
        Estimate error rate by sacrificing some bits
        
        Returns:
            error_rate: Percentage of errors
            errors: Number of errors
            sample_size: Number of bits sampled
        """
        if len(alice_bits) == 0:
            return 0.0, 0, 0
        
        sample_size = max(1, min(int(len(alice_bits) * sample_ratio), len(alice_bits)))
        sample_indices = random.sample(range(len(alice_bits)), sample_size)
        
        errors = sum(1 for i in sample_indices if alice_bits[i] != bob_bits[i])
        error_rate = (errors / sample_size) * 100
        
        return error_rate, errors, sample_size
    
    def generate_final_key(self, sifted_bits: List[int], 
                          sample_indices: List[int]) -> List[int]:
        """Generate final key by removing sampled bits"""
        return [bit for i, bit in enumerate(sifted_bits) 
                if i not in sample_indices]
    
    def run(self) -> Dict:
        """
        Execute complete BB84 protocol
        
        Returns:
            Dictionary containing all results
        """
        # Step 1: Alice prepares random bits and bases
        alice_bits = self.generate_random_bits(self.key_length)
        alice_bases = self.generate_random_bases(self.key_length)
        
        # Step 2: Alice encodes and sends qubits (with potential eavesdropping)
        qubits = []
        for bit, basis in zip(alice_bits, alice_bases):
            qubit = self.encode_qubit(bit, basis)
            qubit = self.eavesdrop(qubit)
            qubits.append(qubit)
        
        # Step 3: Bob chooses random bases and measures
        bob_bases = self.generate_random_bases(self.key_length)
        bob_bits = [self.measure_qubit(qubit, basis) 
                   for qubit, basis in zip(qubits, bob_bases)]
        
        # Step 4: Sifting (basis reconciliation)
        sifted_alice, sifted_bob, sifted_indices = self.sift_key(
            alice_bits, alice_bases, bob_bits, bob_bases
        )
        
        # Step 5: Error estimation
        error_rate, errors, sample_size = self.estimate_error_rate(
            sifted_alice, sifted_bob
        )
        
        # Step 6: Generate final key
        sample_indices_used = random.sample(range(len(sifted_alice)), 
                                           min(sample_size, len(sifted_alice)))
        final_key = self.generate_final_key(sifted_alice, sample_indices_used)
        
        # Determine if channel is secure (typical threshold: 11%)
        is_secure = error_rate < 11.0
        
        # Store results
        self.results = {
            'initial_length': self.key_length,
            'sifted_length': len(sifted_alice),
            'sample_size': sample_size,
            'errors': errors,
            'error_rate': error_rate,
            'final_key_length': len(final_key),
            'final_key': final_key,
            'is_secure': is_secure,
            'alice_bits': alice_bits,
            'alice_bases': alice_bases,
            'bob_bits': bob_bits,
            'bob_bases': bob_bases,
            'qubits': qubits,
            'sifted_indices': sifted_indices
        }
        
        return self.results
    
    def print_results(self):
        """Print simulation results in a formatted way"""
        if not self.results:
            print("No simulation results. Run the protocol first.")
            return
        
        print("\n" + "="*60)
        print("BB84 QUANTUM KEY DISTRIBUTION - SIMULATION RESULTS")
        print("="*60)
        print(f"Initial qubits transmitted: {self.results['initial_length']}")
        print(f"Sifted key length: {self.results['sifted_length']} "
              f"({self.results['sifted_length']/self.results['initial_length']*100:.1f}%)")
        print(f"Sample size for error check: {self.results['sample_size']}")
        print(f"Errors detected: {self.results['errors']}/{self.results['sample_size']}")
        print(f"Error rate: {self.results['error_rate']:.2f}%")
        print(f"Final key length: {self.results['final_key_length']}")
        print(f"Channel status: {'✓ SECURE' if self.results['is_secure'] else '✗ EAVESDROPPING DETECTED'}")
        print(f"Final key (first 50 bits): {''.join(map(str, self.results['final_key'][:50]))}")
        print("="*60 + "\n")
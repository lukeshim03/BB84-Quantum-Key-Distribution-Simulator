import numpy as np
import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

class BB84QuantumProtocol:
    def __init__(self, key_length=100, eavesdrop_prob=0.0):
        self.key_length = key_length
        self.eavesdrop_prob = eavesdrop_prob
        self.simulator = AerSimulator()
        self.results = {}
        
    def run(self):
        alice_bits = [random.randint(0, 1) for _ in range(self.key_length)]
        alice_bases = [random.choice(['rectilinear', 'diagonal']) for _ in range(self.key_length)]
        bob_bases = [random.choice(['rectilinear', 'diagonal']) for _ in range(self.key_length)]
        
        qc = QuantumCircuit(self.key_length, self.key_length)
        for i in range(self.key_length):
            if alice_bits[i] == 1: qc.x(i)
            if alice_bases[i] == 'diagonal': qc.h(i)
            
            if random.random() < self.eavesdrop_prob:
                eve_basis = random.choice(['rectilinear', 'diagonal'])
                if eve_basis == 'diagonal': qc.h(i)
                qc.measure(i, i)
                if eve_basis == 'diagonal': qc.h(i)
            
            if bob_bases[i] == 'diagonal': qc.h(i)
            qc.measure(i, i)

        result = self.simulator.run(qc, shots=1).result()
        counts = list(result.get_counts().keys())[0]
        bob_bits = [int(bit) for bit in counts[::-1]]

        sifted_alice, sifted_bob = [], []
        for i in range(self.key_length):
            if alice_bases[i] == bob_bases[i]:
                sifted_alice.append(alice_bits[i])
                sifted_bob.append(bob_bits[i])

        s_len = len(sifted_alice)
        sample_size = max(1, int(s_len * 0.3)) if s_len > 0 else 0
        
        errors = 0
        if sample_size > 0:
            sample_indices = random.sample(range(s_len), sample_size)
            errors = sum(1 for i in sample_indices if sifted_alice[i] != sifted_bob[i])
            final_key = [bit for i, bit in enumerate(sifted_alice) if i not in sample_indices]
        else:
            final_key = []

        error_rate = (errors / sample_size * 100) if sample_size > 0 else 0.0
        
        self.results = {
            'initial_length': self.key_length,
            'sifted_length': s_len,
            'sample_size': sample_size,
            'errors': errors,
            'error_rate': error_rate,
            'final_key_length': len(final_key),
            'final_key': final_key,
            'is_secure': error_rate < 11.0
        }
        return self.results

    def print_results(self):
        res = self.results
        print("="*60)
        print("BB84 QUANTUM KEY DISTRIBUTION - SIMULATION RESULTS")
        print("="*60)
        print(f"Initial qubits transmitted: {res['initial_length']}")
        print(f"Sifted key length: {res['sifted_length']} ({res['sifted_length']/res['initial_length']*100:.1f}%)")
        print(f"Sample size for error check: {res['sample_size']}")
        print(f"Errors detected: {res['errors']}/{res['sample_size']}")
        print(f"Error rate: {res['error_rate']:.2f}%")
        print(f"Final key length: {res['final_key_length']}")
        print(f"Channel status: {'✓ SECURE' if res['is_secure'] else '✗ EAVESDROPPING DETECTED'}")
        key_str = "".join(map(str, res['final_key'][:50]))
        print(f"Final key (first 50 bits): {key_str}")
        print("="*60)
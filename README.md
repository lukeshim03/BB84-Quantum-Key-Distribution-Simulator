# BB84 Quantum Key Distribution Simulator(Classical Way)

A comprehensive Python implementation of the BB84 quantum key distribution protocol, first proposed by Charles Bennett and Gilles Brassard in 1984.

## Overview

This project simulates the complete BB84 protocol including:
- Quantum bit preparation and transmission
- Eavesdropping attack simulation
- Basis reconciliation (sifting)
- Error rate estimation
- Statistical analysis of protocol performance

## Features

- ✅ Complete BB84 protocol implementation
- ✅ Eavesdropping detection simulation
- ✅ Statistical analysis with multiple runs
- ✅ Visualization of results
- ✅ Detailed step-by-step logging
- ✅ Configurable parameters (key length, eavesdrop probability)

## Installation

```bash
# Clone the repository
git clone https://github.com/lukeshim03/bb84-simulator.git
cd bb84-simulator

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Single Simulation

```python
from bb84_simulator import BB84Protocol

# Create protocol instance
bb84 = BB84Protocol(key_length=100, eavesdrop_prob=0.25)

# Run simulation
results = bb84.run()

# Print results
bb84.print_results()
```

### Statistical Analysis

```python
from statistical_analysis import BB84StatisticalAnalyzer

# Create analyzer
analyzer = BB84StatisticalAnalyzer()

# Run analysis with different eavesdrop probabilities
analyzer.analyze_eavesdrop_impact(
    key_length=100,
    eavesdrop_probs=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
    num_simulations=100
)

# Display results
analyzer.print_statistics()
analyzer.plot_results()
```

### Run Complete Demo

```bash
python main.py
```

## Project Structure

```
BB84-QKD-Simulator/
├── README.md
├── requirements.txt
├── bb84_simulator.py         # Core BB84 protocol implementation
├── statistical_analysis.py   # Statistical analysis tools
├── main.py                   # Demo and examples
├── docs/
│   └── theory.md            # Theoretical background
└── results/
    └── sample_outputs/      # Sample simulation results
```

## Theory

### BB84 Protocol Steps

1. **Preparation**: Alice generates random bits and randomly chooses bases (rectilinear + or diagonal ×) to encode each bit into a quantum state

2. **Transmission**: Qubits are sent through quantum channel (potentially intercepted by Eve)

3. **Measurement**: Bob randomly chooses bases and measures each qubit

4. **Sifting**: Alice and Bob publicly compare their bases and keep only bits where they used the same basis (~50% of bits)

5. **Error Checking**: They sacrifice some bits to estimate the error rate

6. **Key Generation**: If error rate is below threshold (~11%), remaining bits form the secure key

### Security Basis

The security of BB84 relies on fundamental quantum mechanical principles:
- **No-cloning theorem**: Quantum states cannot be perfectly copied
- **Measurement disturbance**: Measuring a quantum state disturbs it
- **Heisenberg uncertainty principle**: Non-commuting observables cannot be simultaneously measured

Any eavesdropping attempt will introduce detectable errors.

## Results

### Expected Performance

| Eavesdrop Probability | Expected Error Rate | Key Retention |
|-----------------------|---------------------|---------------|
| 0%                    | ~0%                 | ~35-40%       |
| 10%                   | ~2.5%               | ~35-40%       |
| 25%                   | ~6.25%              | ~35-40%       |
| 50%                   | ~12.5%              | ~35-40%       |

*Note: Key retention = (final key length / initial transmission length)*

### Sample Output

```
============================================================
BB84 QUANTUM KEY DISTRIBUTION - SIMULATION RESULTS
============================================================
Initial qubits transmitted: 100
Sifted key length: 48 (48.0%)
Sample size for error check: 14
Errors detected: 1/14
Error rate: 7.14%
Final key length: 34
Channel status: ✓ SECURE
Final key (first 50 bits): 1011001110101001011010011101010110
============================================================
```

## Advanced Usage

### Custom Noise Models

```python
# Implement custom eavesdropping strategy
class CustomBB84(BB84Protocol):
    def eavesdrop(self, qubit):
        # Your custom eavesdropping logic
        pass
```

### Performance Testing

```python
# Test with different key lengths
for length in [50, 100, 200, 500, 1000]:
    bb84 = BB84Protocol(key_length=length)
    results = bb84.run()
    print(f"Length {length}: {results['final_key_length']} bits retained")
```

## Applications

- **Quantum Cryptography Research**: Understanding QKD protocols
- **Security Analysis**: Testing eavesdropping detection
- **Education**: Teaching quantum information theory
- **Protocol Development**: Baseline for advanced QKD protocols

## Future Enhancements

- [ ] E91 protocol (entanglement-based QKD)
- [ ] B92 protocol (two-state QKD)
- [ ] Privacy amplification algorithms
- [ ] Information reconciliation (error correction)
- [ ] Realistic channel noise models
- [ ] Photon loss simulation
- [ ] Multi-photon pulses
- [ ] Real quantum hardware integration (IBM Qiskit)

## References

1. Bennett, C. H., & Brassard, G. (1984). "Quantum cryptography: Public key distribution and coin tossing." *Proceedings of IEEE International Conference on Computers, Systems and Signal Processing*, 175-179.

2. Ekert, A. K. (1991). "Quantum cryptography based on Bell's theorem." *Physical Review Letters*, 67(6), 661.

3. Shor, P. W., & Preskill, J. (2000). "Simple proof of security of the BB84 quantum key distribution protocol." *Physical Review Letters*, 85(2), 441.

4. Scarani, V., et al. (2009). "The security of practical quantum key distribution." *Reviews of Modern Physics*, 81(3), 1301.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Author

Eunseop Shim(Luke)
- Email: e1129864@u.nus.edu
- GitHub: @lukeshim03

## Acknowledgments

- Inspired by the pioneering work of Charles Bennett and Gilles Brassard
- Special thanks to Professor Artur Ekert for his foundational contributions to quantum cryptography

# BB84 Protocol: Theoretical Background

## Introduction

The BB84 protocol, proposed by Charles Bennett and Gilles Brassard in 1984, is the first quantum key distribution (QKD) protocol. It allows two parties (Alice and Bob) to establish a shared secret key over an insecure channel, with security guaranteed by the laws of quantum mechanics.

## Quantum States Used

BB84 uses four quantum states, organized in two conjugate bases:

### Rectilinear Basis (+)
- |0⟩ = |↑⟩ (vertical polarization) represents bit 0
- |1⟩ = |→⟩ (horizontal polarization) represents bit 1

### Diagonal Basis (×)
- |0⟩ = |↗⟩ (diagonal polarization at +45°) represents bit 0
- |1⟩ = |↖⟩ (diagonal polarization at -45°) represents bit 1

## Protocol Steps

### 1. Quantum Transmission

**Alice's Actions:**
1. Generate a random bit string: {0, 1, 0, 1, 1, 0, ...}
2. For each bit, randomly choose a basis (+ or ×)
3. Encode the bit in the chosen basis
4. Send the quantum state to Bob

**Example:**
```
Alice's bits:   0  1  0  1  1  0  1  0
Alice's bases:  +  ×  +  ×  +  ×  +  ×
Quantum states: |↑⟩ |↖⟩ |↑⟩ |↖⟩ |→⟩ |↗⟩ |→⟩ |↗⟩
```

### 2. Quantum Measurement

**Bob's Actions:**
1. For each received qubit, randomly choose a basis
2. Measure the qubit in the chosen basis
3. Record the measurement result

**Important Quantum Principle:**
- If Bob uses the SAME basis as Alice → he gets the correct bit
- If Bob uses a DIFFERENT basis → he gets a random result (50% chance either way)

**Example:**
```
Alice's bases:  +  ×  +  ×  +  ×  +  ×
Bob's bases:    +  +  ×  ×  +  ×  ×  +
Match?          ✓  ✗  ✗  ✓  ✓  ✓  ✗  ✗
Bob's results:  0  ?  ?  1  1  0  ?  ?
```

### 3. Basis Reconciliation (Sifting)

**Public Communication:**
1. Alice and Bob publicly announce their basis choices (NOT the bit values)
2. They discard all bits where they used different bases
3. Keep only the bits where bases matched (~50% of original)

**Example:**
```
Original length: 8 bits
After sifting: 4 bits (indices 0, 3, 4, 5)
Sifted key (Alice): 0, 1, 1, 0
Sifted key (Bob):   0, 1, 1, 0  (if no eavesdropping)
```

### 4. Error Estimation

**Security Check:**
1. Alice and Bob randomly select a subset of sifted bits (~30%)
2. They publicly compare these bits
3. Calculate error rate = (number of mismatches) / (sample size)
4. If error rate > threshold (~11%), abort (eavesdropping detected)

**Why 11% threshold?**
The theoretical analysis shows that if error rate exceeds 11%, Eve can potentially extract more information about the key than the uncertainty between Alice and Bob, making the key insecure.

### 5. Privacy Amplification (Not in basic simulation)

In real implementations, additional steps compress the key to remove any partial information Eve might have gained.

## Eavesdropping Analysis

### Eve's Dilemma

If Eve (eavesdropper) tries to intercept qubits:

1. **She must measure them** to get information
2. **She doesn't know the correct basis** (50% chance of guessing wrong)
3. **Wrong basis measurement disturbs the quantum state**
4. **She must resend qubits to Bob** (to avoid detection)
5. **Disturbed states cause errors** between Alice and Bob

### Example Attack Scenario

```
Alice sends:        |↑⟩ (bit 0 in + basis)
Eve intercepts and measures in × basis → gets |↗⟩ or |↖⟩ (random)
Eve resends:        |↗⟩ (bit 0 in × basis)
Bob measures in + basis → gets |↑⟩ or |→⟩ (random, 50% error!)
```

### Error Rate Calculation

If Eve intercepts with probability P:
- She uses wrong basis 50% of the time
- This causes Bob to measure wrong value 50% of the time
- Expected error rate ≈ P × 0.5 × 0.5 = P/4 = 25% of P

**Examples:**
- P = 0% → Error rate ≈ 0%
- P = 25% → Error rate ≈ 6.25%
- P = 50% → Error rate ≈ 12.5% (exceeds threshold!)

## Security Proof (Simplified)

### Information Theoretic Security

The security of BB84 relies on:

1. **No-Cloning Theorem**: Eve cannot make perfect copies of unknown quantum states

2. **Measurement Disturbance**: Any measurement by Eve necessarily disturbs the quantum state

3. **Heisenberg Uncertainty**: The bases (+ and ×) are conjugate observables - measuring in one basis destroys information about the other

### Quantitative Analysis

For a sifted key of length n bits with error rate e:

**Alice and Bob's mutual information:** I(A:B) ≈ n(1 - H(e))
where H(e) is the binary entropy function

**Eve's information:** I(A:E) ≤ n × f(e)

The key is secure when I(A:B) > I(A:E)

For BB84, this condition is satisfied when e < 11%

## Practical Considerations

### Real-World Challenges

1. **Photon Loss**: Not all qubits reach Bob (typical: 10-20% loss per km)
2. **Detector Efficiency**: Detectors don't register every photon (80-90% efficiency)
3. **Dark Counts**: Spontaneous detector clicks create noise
4. **Multi-photon Pulses**: Weak lasers produce occasional multi-photon pulses
5. **Side Channels**: Timing attacks, detector blinding, etc.

### Key Rate Formula

Realistic key generation rate:
```
R = R₀ × η_total × (1 - QBER) × f_EC × f_PA
```
Where:
- R₀ = repetition rate (GHz)
- η_total = total efficiency (detection × transmission)
- QBER = quantum bit error rate
- f_EC = error correction efficiency factor
- f_PA = privacy amplification factor

### Distance Limitations

Without quantum repeaters:
- Fiber optics: ~200 km maximum
- Free space (satellite): ~1000 km demonstrated
- Attenuation: ~0.2 dB/km in fiber

## Advanced Variants

### Decoy State Protocol
Uses multiple intensity levels to detect photon-number-splitting attacks

### Measurement-Device-Independent (MDI) QKD
Removes detector side-channel vulnerabilities

### Twin-Field QKD
Extends distance range by using phase measurements

### Continuous-Variable QKD
Uses continuous properties of light (quadratures)

## Comparison with E91

| Feature | BB84 | E91 |
|---------|------|-----|
| Quantum resource | Single photons | Entangled pairs |
| Basis choice | Random (prepare-measure) | Random (measurement) |
| Security test | Error rate | Bell inequality |
| Implementation | Simpler | More complex |

## Mathematical Framework

### Density Matrix Formulation

States in rectilinear basis:
```
|↑⟩ = |0⟩ = [1, 0]ᵀ
|→⟩ = |1⟩ = [0, 1]ᵀ
```

States in diagonal basis:
```
|↗⟩ = (|0⟩ + |1⟩)/√2 = [1/√2, 1/√2]ᵀ
|↖⟩ = (|0⟩ - |1⟩)/√2 = [1/√2, -1/√2]ᵀ
```

### Measurement Operators

Rectilinear basis projectors:
```
Π₀⁺ = |↑⟩⟨↑| = [1 0; 0 0]
Π₁⁺ = |→⟩⟨→| = [0 0; 0 1]
```

Diagonal basis projectors:
```
Π₀ˣ = |↗⟩⟨↗| = 1/2[1 1; 1 1]
Π₁ˣ = |↖⟩⟨↖| = 1/2[1 -1; -1 1]
```

## Conclusion

BB84 demonstrates that quantum mechanics can provide information-theoretic security for key distribution. While practical implementations face challenges, the protocol's fundamental security guarantees make it a cornerstone of quantum cryptography.

## References

1. Bennett, C. H., & Brassard, G. (1984). Quantum cryptography: Public key distribution and coin tossing.

2. Shor, P. W., & Preskill, J. (2000). Simple proof of security of the BB84 quantum key distribution protocol.

3. Scarani, V., et al. (2009). The security of practical quantum key distribution.

4. Lo, H. K., Curty, M., & Tamaki, K. (2014). Secure quantum key distribution.
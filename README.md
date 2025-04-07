# Differential Power Analysis (DPA)

This project demonstrates the implementation and analysis of **Differential Power Analysis (DPA)** side-channel attacks on AES. It is based on a demo script using a **Hamming Weight leakage model** and **correlation** as a distinguisher.

## Project Goals

The main objective is to explore various DPA attack strategies by extending and modifying the provided script to answer three key questions:


### 1. Attack at Bit-Level Instead of Byte-Level

#### a. Using a Single Bit Leakage Model
- Each individual bit of the intermediate variable (S-Box output) is analyzed.
- The attack uses **correlation** to identify the correct key.
- Key function: `shift_and_get_lsb(Y, bit_pos)` to extract individual bits.

#### b. Using a *Difference of Means (DoM)* Distinguisher
- Power traces are divided into two groups based on the guessed bit (0 or 1).
- A **t-statistic** is computed for each key hypothesis to distinguish correct guesses.

📌 **Result:** Both methods work well, but DoM is significantly faster (30 min vs 4 hours), although it requires more traces for high accuracy.


### 2. Attack on SubBytes Input (i.e., AddRoundKey Output)

- The script is modified to attack a *linear* intermediate variable (AddRoundKey output).
- The **DoM distinguisher** is used for efficiency.

📌 **Result:** Only 4 out of 16 key bytes are correctly recovered. This confirms that attacking **non-linear** operations (like SubBytes) is more effective.


### 3. How Many Traces Are Needed to Recover the Key?

Experiments are run using different numbers of power traces.

- With **DoM**, around **660–700 traces** are needed to correctly recover 15/16 key bytes.
- With **correlation**, only **105 traces** are enough to fully recover the key.

📊 A summary table shows key recovery performance depending on the number of traces.

---

## Key Takeaways

- Bit-level attacks provide higher precision but require more computation.
- DoM is much faster but less effective with a small number of traces.
- Attacking linear functions (e.g., AddRoundKey) is significantly harder.
- There's a clear trade-off between **processing time** and **number of traces required**.

---

## Requirements

- Python 3.x
- NumPy, Matplotlib
- Provided power trace dataset (not included due to licensing/privacy)

---

## Code Structure

- `corrAttack_bit(...)`: bit-level attack using correlation
- `dom_attack_bit(...)`: bit-level attack using DoM
- `Initialise_only_ADK(...)`: setup for attacking AddRoundKey
- `calculate_t_statistic(...)`: computes t-statistic for DoM
- Output includes graphical plots of attack results





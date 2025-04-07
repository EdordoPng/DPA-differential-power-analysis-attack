# This is the demo script that performs a DPA style attack on a set of power traces.
#  
# It is based on a differential attack, using a Hamming weight leakage model, and correlation as a distinguisher.

# Author: Elisabeth Oswald
# Comments: Edoardo Diana

import transactionReader
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

class AESAttack(object):
    global sbox
    sbox = [
        # ... (S-Box values unchanged for brevity)
    ]
    
    global key
    key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]

    def Sbox(self, X):
        y = np.zeros(len(X)).astype(int)
        for i in range(len(X)):
            y[i] = sbox[X[i]]
        return y
    
    # The add round key performs an XOR between a specific byte x and the corresponding key guess
    def ADK(self, X, k):
        y = np.zeros(len(X)).astype(int)
        for i in range(len(X)):
            y[i] = X[i] ^ k
        return y

    # Hamming weight function
    # This will be used as the power prediction model

    # Note that presumably we have chosen the intermediate value resulting from the SubBytes operation
    # since it is a non-linear operation in AES
    def HW(self, X):
        y = np.zeros(len(X)).astype(int)
        for i in range(len(X)):
            y[i] = bin(X[i]).count("1")
        return y
    
    def maxCorr(self, hw, traces):
        maxcorr = 0
        corr = np.zeros(trs.number_of_samples)
        for i in range(trs.number_of_samples):
            [corr[i], pv] = pearsonr(hw, traces[:, i])
            if abs(corr[i]) > maxcorr:
                maxcorr = abs(corr[i])
        return [maxcorr, corr]
    
    # Note that N is the number of traces to be used; it's set to N = 500 in the main
    def Initialise(self, N):
        trs = transactionReader.transactionReader(
            "Measured_power_traces_for_AES_attack.trs")
        trs.read_header()
        # Call the function to read the traces; it reads from trace 0 up to the last with index number_of_samples
        trs.read_traces(N, 0, trs.number_of_samples)
        HWguess = np.zeros((16, 256, N)).astype(int)
        # HWguess is structured as:
        #[[0 0 0 ... 0 0 0]
        #[0 0 0 ... 0 0 0]
        # ...
        #[0 0 0 ... 0 0 0]]

        for byteno in range(16):
            # For each of the 16 bytes that make up the state, we need to try 2^8 = 256 key hypotheses
            # So we take that byte and call it X
            X = trs.plaintext[:, byteno]

            # Print the byte number being analyzed (from 0 to 15)
            print("byteno={0}\n".format(byteno))
            # Iterate through each key hypothesis
            for kg in range(256):
                # This operation gives the input that will go into the substitution box
                Y = AESAttack().ADK(X, kg)
                # This matrix Y below has a dimension of 500 (num of traces) * 256
                # The result Y is the value we want to attack in a DPA attack
                # Y represents the desired intermediate value
                Y = AESAttack().Sbox(Y)
                
                # HWguess stores the hypothetical power consumption
                HWguess[byteno, kg] = AESAttack().HW(Y)

        return [trs, HWguess]

    def corrAttack(self, trs, ax, byteno, Nm):
        ax.clear()
        maxkg = 0
        # A variable to store the highest correlation value observed
        maxcorr_k = 0
        # Iterate through all key guesses
        for kg in range(256):
            # Get the hypothetical power consumption for this byte and key guess
            hw = HWguess[byteno, kg]
            # Use the hypothetical power consumption and the traces to compute correlation and its max value
            [maxcorr, corr] = AESAttack().maxCorr(hw[0:Nm], trs.traces[0:Nm, :])
            if maxcorr > maxcorr_k:
                maxkg = kg
                maxcorr_k = maxcorr
            if kg == key[byteno]:
                ax.plot(corr, 'r-', alpha=1)
            else:
                ax.plot(corr, color=(0.8, 0.8, 0.8), alpha=0.8)
        ax.set_xlim([1, trs.number_of_samples])                  
        ax.set_ylim([-1, 1])
        ax.title.set_text('Byte {0}=0x{1:2x}'.format(byteno, maxkg))
        ax.set_xlabel('Samples')
        ax.set_ylabel(r'$\rho$')

        return maxkg


if __name__ == '__main__':
        # Initialize the attack using N = 500 number of traces
        # By calling Initialise we get the 500 traces stored in the file,
        # and the hypothetical power consumption obtained using Hamming Weight
        # as the power model (this was applied to the intermediate values from the S-box operation)

        [trs, HWguess] = AESAttack().Initialise(500)
        plt.ion()
        fig = plt.figure()
        ax = []
        for byteno in range(16):
            # For each of the 16 bytes in the state, we create a plot
            ax.append(fig.add_subplot(4, 4, byteno + 1))

        for Nm in range(1, 10):
            fig.suptitle('N={0}'.format(Nm * 50))
            print("N={0}\n".format(Nm * 50))
            # For all 16 bytes of the state
            for byteno in range(16):
                print("byte={0}\n".format(byteno))
                # For this byte, we perform the attack and see the trace correlations
                AESAttack().corrAttack(trs, ax[byteno], byteno, Nm * 50)
                fig.canvas.draw()
                fig.canvas.flush_events()
                plt.show()
                plt.tight_layout()
                plt.pause(.001)

        plt.ioff()
        plt.show()

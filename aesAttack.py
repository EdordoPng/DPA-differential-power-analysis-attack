import transactionReader
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

# Atuthor : Edoardo Diana

class AESAttack(object):
    global sbox
    sbox = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]

    global key

    ######################################## Start Demo Script Code ########################################

    key= [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
    #Byte: 0      1     2    3      4     5    6      7    8     9     10    11    12    13    14    15

    def Sbox(self, X):
        y = np.zeros(len(X)).astype(int)
        for i in range(len(X)):
            y[i] = sbox[X[i]]
        return y

    def ADK(self, X, k):
        y = np.zeros(len(X)).astype(int)
        for i in range(len(X)):
            y[i] = X[i] ^ k
        return y

    # y is an array that holds how many 1 there are in X
    def HW (self, X):
        y = np.zeros(len(X)).astype(int)
        for i in range(len(X)):
            y[i] = bin(X[i]).count("1")
        return y

    def maxCorr(self, hw, traces):
        maxcorr = 0
        # corr : array that stores correlation values for each time sample. 
        # Has the same length as number of samples per track
        corr = np.zeros(trs.number_of_samples)

        # The loop runs through each time sample (trace columns), representing the data 
        # collected at a given time
        for i in range(trs.number_of_samples):
            [corr[i], pv] = pearsonr(hw, traces[:, i])
            if abs(corr[i]) > maxcorr:
                maxcorr = abs(corr[i])
        return [maxcorr, corr]

    def Initialise(self, N):
        trs = transactionReader.transactionReader("Measured_power_traces_for_AES_attack.trs")
        trs.read_header()
        trs.read_traces(N, 0, trs.number_of_samples)
        print(trs.number_of_samples)
        HWguess = np.zeros((16, 256, N)).astype(int) 

        for byteno in range(16):
            X = trs.plaintext[:, byteno]
            print("byteno={0}\n".format(byteno))
            for kg in range(256):
                Y = AESAttack().ADK(X, kg)
                Y = AESAttack().Sbox(Y)
                HWguess[byteno, kg] = AESAttack().HW(Y)
        return [trs, HWguess]
    

    def corrAttack(self, trs, ax, byteno, Nm):
        ax.clear()
        maxkg = 0
        maxcorr_k = 0
        for kg in range(256):
            hw = HWguess[byteno, kg]
            [maxcorr, corr] = AESAttack().maxCorr(hw[0:Nm], trs.traces[0:Nm, :])
            if maxcorr > maxcorr_k:
                maxkg = kg
                maxcorr_k = maxcorr
                print(maxkg)
            if kg == key[byteno]:
                print(kg)
                ax.plot(corr, 'r-', alpha=1)
            else:
                ax.plot(corr, color=(0.8, 0.8, 0.8), alpha=0.8)
        ax.set_xlim([1, trs.number_of_samples])
        ax.set_ylim([-1, 1])
        ax.title.set_text('Byte {0}=0x{1:2x}'.format(byteno, maxkg))
        print(maxkg)
        ax.set_xlabel('Samples')
        ax.set_ylabel(r'$\rho$')

        return maxkg
    
    ######################################## End Demo Script Code ########################################


    def Initialise_only_ADK(self, N):
        '''
        This one is equivalent to the Initialise one, but here we attack the input of the SubBytes operation
        '''
        trs = transactionReader.transactionReader("Measured_power_traces_for_AES_attack.trs")
        trs.read_header()
        trs.read_traces(N, 0, trs.number_of_samples)
        print(trs.number_of_samples)
        HWguess = np.zeros((16, 256, N)).astype(int) 

        for byteno in range(16):
            X = trs.plaintext[:, byteno]
            print("byteno={0}\n".format(byteno))
            for kg in range(256):
                Y = AESAttack().ADK(X, kg)
                # Commented line, we are interested in the input of Sbox, so the output of the ARK
                # Y = AESAttack().Sbox(Y)
                HWguess[byteno, kg] = AESAttack().HW(Y)
        return [trs, HWguess]

    
    
    def shift_and_get_lsb(self, X, bit_position):
        '''This function does the right shift of bits composing X by a number o positions
        The AND with 1 (in binary) let us obtain the least significant value that is the bit 
        in which we are interested in
        '''
        return (X >> bit_position) & 1

    def Initialise_bit(self, N):
        '''This funtion reads the traces from file and returns the tridimensional array HWguess that contains
        our guesses about that bit in that byte about that key guess
        '''
        trs = transactionReader.transactionReader("Measured_power_traces_for_AES_attack.trs")
        trs.read_header()
        trs.read_traces(N, 0, trs.number_of_samples)

        # Because we decided to work on bit instead of bytes, we add a new dimension that works on the 8 bits
        HWguess = np.zeros((16, 256, 8, N)).astype(int) 

        for byteno in range(16):
            X = trs.plaintext[:, byteno]
            print("byteno={0}\n".format(byteno))
            for kg in range(256):
                Y = AESAttack().ADK(X, kg)
                Y = AESAttack().Sbox(Y)
                # Now go along all the single 8 bits
                for bit_pos in range(8):  
                    HWguess[byteno, kg, bit_pos] = AESAttack().shift_and_get_lsb(Y, bit_pos)

        return [trs, HWguess]

    def corrAttack_bit(self, trs, ax, byteno, Nm):
        '''This function performs the correlation attack using the maxCorr function'''
        
        # Nm are the number of traces to utilize
        maxkg = 0
        maxcorr_k = 0
        for kg in range(256):
            for bit_pos in range(8):
                bit_values = HWguess[byteno, kg, bit_pos]
                maxcorr, corr = AESAttack.maxCorr(self, bit_values[:Nm], trs.traces[:Nm, :])
                if maxcorr > maxcorr_k:
                    maxkg = kg
                    maxcorr_k = maxcorr
                if kg == key[byteno]:
                    ax.plot(corr, 'r-', alpha=1)
                else:
                    ax.plot(corr, color=(0.8, 0.8, 0.8), alpha=0.8)
            ax.set_xlim([1, trs.number_of_samples])
            ax.set_ylim([-1, 1])
            ax.title.set_text(f'Byte {byteno}, Bit {bit_pos}, Key=0x{maxkg:02x}')
            ax.set_xlabel('Samples')
            ax.set_ylabel(r'$\rho$')
        return maxkg

    def calculate_t_statistic(self, trs, leakage):
        '''
        This function calculates the t-statistic using the formula inside the provided report.
        Also identifies the point (sample i) where the difference between the two classes is 
        statistically more significant.
        '''

        # trs is the matrix of traces, where each line represents a single acquisition and each 
        # column represents a sample of that track

        # variable that we will give in output
        max_difference = 0
        
        # Split into groups
        group_0 = trs[leakage == 0, :]
        group_1 = trs[leakage == 1, :]

        group_0_means = np.mean(group_0, axis=0)  
        group_1_means = np.mean(group_1, axis=0) 
        
        # Obtain the variance 
        group_0_variance = np.var(group_0, axis=0, ddof=1)
        group_1_variance = np.var(group_1, axis=0, ddof=1)

        # Number of samples for group 0 and group 1
        # 0 is used to return only the number of rows (i.e., of the first dimension)
        n0 = group_0.shape[0]
        n1 = group_1.shape[0]

        # Standard Deviation
        standardError = np.sqrt(group_0_variance / n0 + group_1_variance / n1)
        standardError[standardError == 0] = np.inf

        t_statistic = (group_1_means - group_0_means) / standardError  # differenza tra le medie dei due gruppi

        # Calculate the absolute maximum value of the t-statistic vector
        # Using the absolute value because the t-statistic can be positive or negative
        max_difference = np.max(np.abs(t_statistic))

        return max_difference, t_statistic
    
    def dom_attack_bit(self, trs, ax, byteno, Nm):
        '''
        This function is structured in a similar way as corrAttack_bit, but here we use the DoM as distingusher
        '''
        ax.clear()
        maxkg = 0
        maxmean_k = 0
        for kg in range(256):
            for bit_position in range(8):

                # Take the respective bit guess from the tridimensional array obtained HWguess from Initialise_bit
                leakage_bit_value = HWguess[byteno, kg, bit_position]
                [max_DoM, t_statistic] = AESAttack().calculate_t_statistic(trs.traces[0:Nm, :], leakage_bit_value[:Nm])

                if (max_DoM > maxmean_k):
                    maxkg = kg
                    maxmean_k = max_DoM
                if (kg == key[byteno]):
                    ax.plot(t_statistic, 'r-', alpha=1)
                else:
                    ax.plot(t_statistic, color=(0.8, 0.8, 0.8), alpha=0.8)
        ax.set_xlim([1, trs.number_of_samples])
        ax.set_ylim([maxmean_k * (-1), maxmean_k * 1])
        ax.title.set_text('Byte {0}=0x{1:2x}'.format(byteno, maxkg))
        ax.set_xlabel('Samples')
        ax.set_ylabel(r'$\rho$')
        return maxkg


if __name__ == '__main__':

    ####### Initialize section #######                                              (uncomment just one of them)

    # 1)  This one works on bytes and attacks the SubBytes operation output
    #[trs, HWguess] = AESAttack().Initialise(1000)

    # 2) This one works on bits and attacks the SubBytes operation output
    [trs, HWguess] = AESAttack().Initialise_bit(1000)
    
    # 3) This one works on bytes and attacks the SubBytes operation input, so the ARK operation output
    #[trs, HWguess] = AESAttack().Initialise_only_ADK(1000)


    plt.ion()
    fig = plt.figure()
    ax = []
    for byteno in range(16):
        ax.append(fig.add_subplot(4, 4, byteno+1))

    for Nm in range(1, 10):
        fig.suptitle('N={0}'.format(Nm * 100))
        print("N={0}\n".format(Nm * 100))

        for byteno in range(16):
            print("byte={0}\n".format(byteno))
            
            ####### Statistical analysis section #######                            (uncomment just one of them)

            # 0) Correlation as distinguisher, target bytes
            #AESAttack().corrAttack(trs, ax[byteno], byteno, Nm*100)
            
            # 1) Correlation as distinguisher, target bits
            AESAttack().corrAttack_bit(trs, ax[byteno], byteno, Nm*100)
            
            # 2) Difference of Means as distinguisher, target bits
            #AESAttack().dom_attack_bit(trs, ax[byteno], byteno, Nm*100)
            
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.show()
            plt.tight_layout()
            plt.pause(.001)

    plt.ioff()
    plt.show()



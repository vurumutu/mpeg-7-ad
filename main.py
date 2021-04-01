from scipy.io import wavfile
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import numpy as np


class Descriptors:
    def __init__(self, audio_file: str):
        self.samplerate, self.data = wavfile.read(audio_file)
        self.N = self.data.shape[0]
        self.fft = fft(self.data)
        self.fftfreq = fftfreq(self.N, 1.0 / 800.0)[:self.N // 2]

    def print_info(self):
        print("Sample Rate: ", self.samplerate)
        print("Sample number: ", self.N)
        print(self.fft)

    def plot_fourier(self):
        plt.plot(self.fftfreq, 2.0 / self.N * np.abs(self.fft[0:self.N // 2]))
        plt.grid()
        plt.show()

    def save_as_xml(self):
        # TODO
        pass

    def log_attack_time(self):
        pass

    def audio_spectrum_centroid(self):
        '''
            Audio spectrum centroid is defined as follows:
                        sum(k*F[k])
                    c = --------------
                        sum(F[k])
            where k is a bin in DFT spectrum and F[k] is corresponding amplitude.
            Conceptually it is connected to perceived brightness of sound.
            More info:
            https://www.sciencedirect.com/topics/engineering/spectral-centroid
        :return:
        '''
        for i in range(self.fftfreq.size):
            # print(i)
            nominator = np.log2(self.fftfreq[i]/1000) #* self.fft[i]
        denominator = np.sum(self.fft)
        c = nominator/denominator
        return c

    def audio_spectrum_spread(self):
        '''
            Audio spectrum spread is defined as follows:
                                sum( (k-c_i)^2 *F[k])
                    S_i = sqrt(  --------------  )
                                sum(F[k])
            where k is a bin in DFT spectrum, F[k] is corresponding amplitude and c is spectrum centroid.
            It is the second central moment of the spectrum.
            More info:
            https://www.sciencedirect.com/topics/engineering/spectral-centroid
        :return:
        '''
        for i in range(self.fftfreq.size):
            nominator = np.log2(self.fftfreq[i]/1000) #* self.fft[i]
        denominator = np.sum(self.fft)
        c = nominator/denominator
        return c


if __name__ == "__main__":
    pass

from scipy.io import wavfile
from scipy.fft import fft, fftfreq
from scipy.stats.mstats import gmean
import matplotlib.pyplot as plt
from math import log10
import numpy as np


class Descriptors:
    def __init__(self, audio_file: str, bits: int):
        self.fs, self.data = wavfile.read(audio_file)
        # TODO handling of multiple channels
        self.bits = bits
        normalize_v = np.vectorize(self.normalize)
        self.data = normalize_v(self.data)
        self.N = len(self.data)
        self.fft = fft(self.data)[:self.N // 2]
        self.fft = np.abs(self.fft)
        self.fftfreq = fftfreq(self.N, 1.0 / self.fs)[:self.N // 2]

    def normalize(self, element: float):
        return element/(2 ** float(self.bits)*2)

    def print_info(self):
        print("Sample Rate: ", self.fs)
        print("How many samples: ", self.N)

    def plot_fourier(self):
        plt.plot(self.fftfreq, self.fft)
        plt.grid()
        plt.show()

    def save_as_xml(self):
        # TODO
        pass

    def log_attack_time(self, _envelope, thresh_min=0.2, thresh_max=0.9):
        '''
        LAT is defined as log in base of 10 of time that passes between beginning of the sound to the maximum intensity.
        To avoid problems such as random noises, default threshold are different than 0 and 100%.
        Usually start = 20% of maximum envelope value, end = 90% of said value.
        This function requires information from audio_spectrum_envelope.
        :return: float
        '''
        def find_nearest_value_index(_array, _value):
            temp_array = _array - _value
            temp_array = np.abs(temp_array)
            closest_value_index = temp_array.argmin()
            # TODO multiple values
            return closest_value_index
        maximum_intensity = np.amax(_envelope)
        lower_value = thresh_min*maximum_intensity
        upper_value = thresh_max*maximum_intensity
        lower_value_index = find_nearest_value_index(_envelope, lower_value)
        upper_value_index = find_nearest_value_index(_envelope, upper_value)
        attack_time = (upper_value_index - lower_value_index)/self.fs
        lat = log10(attack_time)
        return lat

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
        nominator = 0
        for i in range(self.fftfreq.size):
            nominator += self.fftfreq[i] * self.fft[i]
        denominator = np.sum(self.fft)
        c = nominator/denominator
        return c

    def audio_spectrum_spread(self, c: float):
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
        nominator = 0
        for i in range(self.fftfreq.size):
            nominator += (self.fftfreq[i]-c)**2 * self.fft[i]
        denominator = np.sum(self.fft)
        s = np.sqrt(nominator/denominator)
        return s

    def audio_spectrum_flatness(self):
        '''
        Ratio of geometric and arithmetic means:
                (product(x(n)))^(1/N)
        SFM_b =  ------------
                (1/N)*(sum(xn))

        Answers the question: How much do spectrum deviates from being flat in given band. It shows if signal is
        noisy or tonal.
        SFM close to one is achieved by white noise.
        SFM close to zero is achieved by chirp signal.????
        :return:
        '''
        nominator = gmean(self.fft)
        denominator = np.mean(self.fft)

        sf = nominator/denominator
        return sf

    def audio_spectrum_envelope(self):
        '''
        Computing envelope of a signal.
        edge = 2^(rm)*x
        r - resolution in octaves
        m - real number
        :return:
        '''

        pass


if __name__ == "__main__":
    pass

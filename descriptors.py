from scipy.io import wavfile
from scipy.fft import fft, fftfreq
from scipy.stats.mstats import gmean
import matplotlib.pyplot as plt
from math import log10
import numpy as np
import xml.etree.cElementTree as eT


class Descriptors:
    def __init__(self, audio_file: str, bits: int):
        self.fs, self.data = wavfile.read(audio_file)
        # TODO handling of multiple channels
        self.bits = bits
        # normalization of vector - according to PCM
        normalize_v = np.vectorize(self.normalize)
        self.data = normalize_v(self.data)
        self.N = len(self.data)
        # FFT is symetrical - we only nead half of the data
        self.fft = fft(self.data)[:self.N // 2]
        self.fft = np.abs(self.fft)
        # FFT is symetrical - we only nead half of the frequencies
        self.fftfreq = fftfreq(self.N, 1.0 / self.fs)[:self.N // 2]
        self.FRAME_SIZE = 1024
        self.HOP_LENGTH = 512
        # Descriptors - stored for saving in xml
        self.lat = 0
        self.asc = 0
        self.ass = 0
        self.asf = 0

    def normalize(self, element: float) -> float:
        return element/(2 ** float(self.bits)*2)

    def print_info(self):
        print("Sample Rate: ", self.fs)
        print("How many samples: ", self.N)

    def plot_fourier(self):
        plt.plot(self.fftfreq, self.fft)
        plt.grid()
        plt.show()

    def save_as_xml(self, file_name: str):
        root = eT.Element("root")
        doc = eT.SubElement(root, "descriptors")

        eT.SubElement(doc, "audio_spectrum_centroid").text = str(self.asf)
        eT.SubElement(doc, "audio_spectrum_spread").text = str(self.ass)
        eT.SubElement(doc, "audio_spectrum_flatness").text = str(self.asf)
        eT.SubElement(doc, "log_attack_time").text = str(self.lat)

        tree = eT.ElementTree(root)
        with open(file_name, 'w') as f:
            tree.write(f, encoding='unicode')

    def log_attack_time(self, _envelope, thresh_min=0.2, thresh_max=0.9) -> float:
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
        upper_value_index = find_nearest_value_index(_envelope, upper_value)
        # we are limiting our search to the values before the biggest value - we search for initial attack time
        # amplitude at the end of recording may be the lowest which doesnt make sense for LAT
        lower_value_index = find_nearest_value_index(_envelope[:upper_value_index], lower_value)
        attack_time = (upper_value_index - lower_value_index)/self.fs
        lat = log10(attack_time)
        self.lat = lat
        return self.lat

    def audio_spectrum_centroid(self) -> float:
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
        nominator = np.sum(self.fftfreq * self.fft)
        denominator = np.sum(self.fft)
        self.asc = nominator/denominator
        return self.asc

    def audio_spectrum_spread(self, c: float) -> float:
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
        nominator = np.sum((self.fftfreq-c)**2 * self.fft)
        denominator = np.sum(self.fft)
        self.ass = np.sqrt(nominator/denominator)
        return self.ass

    def audio_spectrum_flatness(self) -> float:
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
        self.asf = nominator/denominator
        return self.asf

    def audio_spectrum_envelope(self) -> np.ndarray:
        # TODO more detailed version
        '''
        :return:
        '''
        return np.array([max(self.data[i:i+self.FRAME_SIZE]) for i in range(0, self.N, self.HOP_LENGTH)])

    def helper_frames_to_time(self, _envelope) -> np.ndarray:
        frames_to_time = np.repeat(_envelope, self.HOP_LENGTH)
        return frames_to_time

    def plot_envelope(self, _envelope):
        t = self.helper_frames_to_time(_envelope)
        plt.plot(self.data, "b")
        plt.plot(t, "r")
        plt.grid()
        plt.show()

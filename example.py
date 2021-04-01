from main import Descriptors

audio_descriptors = Descriptors("01.wav")
audio_descriptors.print_info()
audio_descriptors.plot_fourier()
audio_descriptors.audio_spectrum_centroid()

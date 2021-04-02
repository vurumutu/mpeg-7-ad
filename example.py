from main import Descriptors

audio_descriptors = Descriptors("wilhelm_mono.wav", bits=16)
audio_descriptors.print_info()

audio_envelope = audio_descriptors.audio_spectrum_envelope()
print("LAT: ", audio_descriptors.log_attack_time(audio_descriptors.fft))
c = audio_descriptors.audio_spectrum_centroid()
print("ASC: ", c)
print("ASS: ", audio_descriptors.audio_spectrum_spread(c))
print("ASF: ", audio_descriptors.audio_spectrum_flatness())

audio_descriptors.plot_fourier()



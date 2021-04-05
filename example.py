from descriptors import Descriptors

audio_descriptors = Descriptors("wilhelm_mono.wav", bits=16)
print(audio_descriptors)
audio_envelope = audio_descriptors.audio_spectrum_envelope()
print("LAT: ", audio_descriptors.log_attack_time(audio_descriptors.helper_frames_to_time(audio_envelope)))
c = audio_descriptors.audio_spectrum_centroid()
print("ASC: ", c)
print("ASS: ", audio_descriptors.audio_spectrum_spread(c))
print("ASF: ", audio_descriptors.audio_spectrum_flatness())

audio_descriptors.plot_envelope(audio_envelope)
audio_descriptors.plot_fourier()

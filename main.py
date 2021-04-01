from scipy.io import wavfile


class Descriptors:
    def __init__(self, audio_file: str):
        self.samplerate, self.data = wavfile.read(audio_file)

    def print_info(self):
        print("Sample Rate: ", self.samplerate)

    def save_as_xml(self):
        # TODO
        pass

    def log_attack_time(self):
        pass


if __name__ == "__main__":
    pass

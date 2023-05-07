import wave

class WavFileReader:

    def __init__(self, filename):
        self.filename = filename
        self.framerate = None
        self.sampwidth = None
        self.nframes = None
        self.data = None

    def read(self):
        with wave.open(self.filename, "rb") as wavfile:
            self.framerate = wavfile.getframerate()
            self.sampwidth = wavfile.getsampwidth()
            self.nframes = wavfile.getnframes()
            data = wavfile.readframes(self.nframes)
            self.data = signal.bytes2int(data, self.sampwidth)

        return self.framerate, self.sampwidth, self.nframes, self.data
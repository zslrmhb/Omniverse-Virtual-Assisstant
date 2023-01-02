# text-to-speech module utilizting the Riva SDK

import riva.client
import riva.client.audio_io
from config import URI


class TTSService:
    def __init__(self, language='en-US', sample_rate_hz=44100):
        """
        :param language: language code
        :param sample_rate_hz: sample rate herz
        """
        self.auth = riva.client.Auth(uri=URI)
        self.service = riva.client.SpeechSynthesisService(self.auth)
        self.langauge = language
        self.voice = "English-US.Male-1"
        self.sample_rate_hz = sample_rate_hz

    def speak(self, text) -> None:
        """
        :param text: text to speak
        :return: None
        """
        sound_stream = riva.client.audio_io.SoundCallBack(

            3, nchannels=1, sampwidth=2, framerate=self.sample_rate_hz
        )
        responses = self.service.synthesize_online(
            text, None, self.langauge, sample_rate_hz=self.sample_rate_hz
        )
        for resp in responses:
            sound_stream(resp.audio)

        sound_stream.close()

    def get_audio_bytes(self, text) -> bytes:
        """
        :param text: text to speak
        :return: speech audio
        """
        resp = self.service.synthesize(text, self.voice, self.langauge, sample_rate_hz=self.sample_rate_hz)
        return resp.audio
